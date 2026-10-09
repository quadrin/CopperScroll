"""Source AP: Abegg/ETCBC (data/scroll-text.js) against the Puech 2015 transcription, word by word.

The Puech 2015 extract is outside the repository (copyrighted). This script reads it once and
stores only the places where the two editions differ (a few letters each) in ap_variants.csv.

    python3 -I research/text/edition_confusions/build_ap.py --puech2015 PATH

Column XII lines 8-12 are dropped from both texts as soon as each line is parsed, before any
comparison. Unknown line numbers in column XII are dropped too.

A row is a connected group of ETCBC words and Puech tokens linked by aligned letters, where the
letters or the word division differ. Both readings are written with the same sigla:
[ ] restored, [[ ]] supplied by a modern editor (ETCBC flag c), { } engraved but removed
(ETCBC x; Puech's copyist cancellation), < > engraved above the line or inserted by the copyist
(ETCBC s; Puech < >), ( ) Puech's correction of an engraving error. Classes are assigned by
build.py with the rules frozen in PLAN.md.

ap_overrides.csv drops rows that are artefacts of the PDF extract (numerals and Greek moved by
right-to-left layout) and replaces rows where the extract's bracket order is garbled.
"""
import argparse, csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from align import LETTERS, base, levenshtein_ops  # noqa: E402
from exclusion import is_excluded, ROMAN  # noqa: E402

OUT = HERE / 'ap_variants.csv'
# Printed page of each Puech 2015 transcription column (running heads of the extract).
PUECH2015_PAGE = {'I': 25, 'II': 38, 'III': 43, 'IV': 48, 'V': 54, 'VI': 59, 'VII': 62, 'VIII': 68,
                  'IX': 75, 'X': 85, 'XI': 93, 'XII': 106}
FIELDS = ['column', 'line', 'word_index', 'abegg', 'puech2015', 'puech2015_page', 'parse_note']
ETCBC_SIGLA = {'r': ('[', ']'), 'c': ('[[', ']]'), 'x': ('{', '}'), 's': ('<', '>'), 'u': ('', ''), '': ('', '')}


def load_etcbc():
    s = (ROOT / 'data' / 'scroll-text.js').read_text(encoding='utf-8')
    d = json.loads(s[s.index('window.SCROLL_TEXT = ') + 21:].rstrip().rstrip(';'))
    out = {}
    for c in d['columns']:
        col = ROMAN[c['c'] - 1]
        for l in c['lines']:
            if is_excluded(col, l['l']):
                continue  # dropped before anything else
            seq, words = [], {}
            for wi, w in enumerate(l['w']):
                text = ''
                for seg, flag in w.get('h', []):
                    if flag == 'g':
                        continue
                    letters = ''.join(ch for ch in seg if base(ch) in LETTERS)
                    if not letters:
                        continue
                    o, c_ = ETCBC_SIGLA.get(flag, ('', ''))
                    text += o + letters + c_
                    for ch in letters:
                        seq.append((base(ch), wi))
                if text:
                    words[wi] = text
            out[(col, l['l'])] = (seq, words)
    return out


_MARKS = re.compile('[‎‏‪-‮⁦-⁩]')


def parse_puech_lines(path: Path):
    """Return {(column, line): raw text}. Lines in XII 8-12 never leave this function."""
    lines = path.read_text(encoding='utf-8').split('\n')
    heads = [i for i, l in enumerate(lines) if re.match(r'^Col\. ([IVX]+) \(Figure \d+\)\s*$', l)][:12]
    out = {}
    for h in heads:
        col = re.match(r'^Col\. ([IVX]+)', lines[h]).group(1)
        for l in lines[h + 1:h + 45]:
            if l.startswith('Translation') or l.strip().startswith(('Commentary', '©')):
                break
            if not re.search(r'[א-ת]', l):
                continue
            body = _MARKS.sub('', l).rstrip()
            m = re.search(r'(\d{1,2})\s*$', body)
            if not m:
                continue  # no line number: skipped (in column XII this keeps unknown lines out)
            num = int(m.group(1))
            if is_excluded(col, num):
                continue
            body = body[:m.start()].rstrip()
            e = re.search(r'\d{1,2}a?\s*[()]\s*$', body)  # entry number such as ")6(" or "12a("
            if e:
                body = body[:e.start()].rstrip()
                body = re.sub(r'^\s*[()]', '', body)
            out[(col, num)] = body.strip()
    return out


def puech_tokens(body: str):
    """Hebrew tokens of a Puech line with their sigla, and the letter sequence (letter, token)."""
    s = body.replace('(?)', ' ').replace(')?(', ' ').replace('(sic)', ' ').replace('sic', ' ')
    s = re.sub(r'[0-9°|?]', ' ', s)
    s = re.sub(r'[A-Za-zͰ-Ͽἀ-῿∀-⋿]', ' ', s)
    note = []
    if '/' in s:
        note.append('alternative X/Y in the edition')
    if re.search(r'^\s*[\])]|[\[(]\s*$', s):
        note.append('bracket at a line edge (right-to-left extract)')
    tokens = [t for t in re.split(r'[\s/]+', s) if re.search(r'[א-ת]', t)]
    seq = []
    for ti, t in enumerate(tokens):
        for ch in t:
            if base(ch) in LETTERS:
                seq.append((base(ch), ti))
    return seq, tokens, '; '.join(note)


def components(e_seq, p_seq):
    ops = levenshtein_ops(''.join(x[0] for x in e_seq), ''.join(x[0] for x in p_seq))
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in {('E', x[1]) for x in e_seq}:
        find(e)
    for p in {('P', x[1]) for x in p_seq}:
        find(p)
    for op, x, y, i, j in ops:
        if i is not None and j is not None:
            parent[find(('E', e_seq[i][1]))] = find(('P', p_seq[j][1]))
    groups = {}
    for node in list(parent):
        groups.setdefault(find(node), set()).add(node)
    comp_ops = {}
    for op in ops:
        node = ('E', e_seq[op[3]][1]) if op[3] is not None else ('P', p_seq[op[4]][1])
        comp_ops.setdefault(find(node), []).append(op)
    return groups, comp_ops


def build(puech_path: Path):
    et = load_etcbc()
    p15 = parse_puech_lines(puech_path)
    rows = []
    for (col, ln), (e_seq, e_words) in sorted(et.items(), key=lambda kv: (ROMAN.index(kv[0][0]), kv[0][1])):
        body = p15.get((col, ln))
        if body is None or not e_seq:
            continue
        p_seq, p_tokens, note = puech_tokens(body)
        groups, comp_ops = components(e_seq, p_seq)
        found = []
        for root, nodes in groups.items():
            ews = sorted(n[1] for n in nodes if n[0] == 'E')
            pts = sorted(n[1] for n in nodes if n[0] == 'P')
            ops = comp_ops.get(root, [])
            if all(o[0] == '=' for o in ops) and len(ews) <= 1 and len(pts) <= 1:
                continue
            found.append((ews, pts, ops))
        # Layout artefacts: a word missing on one side and present on the other with the same letters.
        lone_e = {tuple(sorted(e_words[w] for w in f[0])): f for f in found if f[0] and not f[1]}
        lone_p = {tuple(sorted(p_tokens[t] for t in f[1])): f for f in found if f[1] and not f[0]}
        artefacts = set()
        for k, f in lone_e.items():
            if k in lone_p:
                artefacts.add(id(f)); artefacts.add(id(lone_p[k]))
        for f in found:
            ews, pts, ops = f
            a_txt = ' '.join(e_words[w] for w in ews if w in e_words)
            b_txt = ' '.join(p_tokens[t] for t in pts)
            n = note + ('; ' if note else '') + 'layout artefact' if id(f) in artefacts else note
            wi = '-'.join(str(w) for w in ews) if len(ews) > 1 else (str(ews[0]) if ews else '')
            rows.append({'column': col, 'line': ln, 'word_index': wi, 'abegg': a_txt, 'puech2015': b_txt,
                         'puech2015_page': PUECH2015_PAGE[col], 'parse_note': n.strip('; ')})
    # Full sort key: set iteration order varies between runs (string hashing), so no ties may remain.
    rows.sort(key=lambda r: (ROMAN.index(r['column']), int(r['line']),
                             int(str(r['word_index']).split('-')[0]) if r['word_index'] else 999,
                             r['word_index'], r['abegg'], r['puech2015'], r['parse_note']))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--puech2015', type=Path, required=True)
    args = ap.parse_args()
    rows = build(args.puech2015)
    for r in rows:
        if is_excluded(r['column'], r['line']):
            raise SystemExit('exclusion breach')
    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} rows -> {OUT.name}')


if __name__ == '__main__':
    main()
