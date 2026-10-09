"""Build variants.csv, confusions.csv and confusions.json from the three variant sources.

    python3 -I research/text/edition_confusions/build.py          # rebuild the outputs
    python3 -I research/text/edition_confusions/build.py --check  # rebuild in memory and compare

Inputs (all in this folder): variants_manual.csv (sources PN, RJ), ap_variants.csv (source AP,
written by build_ap.py) and ap_overrides.csv. Rules: PLAN.md (frozen). Standard library only.
Final forms are counted as their base letters.
"""
import argparse, csv, hashlib, io, json, random, re, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from align import (LETTERS, YW, N_UNORDERED_PAIRS, base, nfc, has_latin_translit,  # noqa: E402
                   translit_to_hebrew, levenshtein_ops, pair_key)
from exclusion import is_excluded, mentions_excluded, ROMAN  # noqa: E402

SEED = 20261009
N_BOOT = 2000
ABEGG = 'Abegg (ETCBC dss 2.0.1)'
# Years for ordering when a name carries none (first publication of the edition used).
CANONICAL_YEAR = {'Abegg': 2006, 'Allegro': 1960, 'Milik': 1962, 'Luria': 1963, 'Pixner': 1983,
                  'Wolters': 1996, 'Muchowski': 1993, 'Beyer': 1994, 'Lefkovits': 2000, 'Puech': 2015}
VARIANT_FIELDS = ['id', 'column', 'line', 'word_index', 'word_index_method', 'source',
                  'edition_a', 'reading_a', 'page_a', 'edition_b', 'reading_b', 'page_b',
                  'letters_a', 'letters_b', 'class', 'class_engraved', 'substitutions', 'shape_pairs',
                  'insertions', 'deletions', 'transposition', 'shape_events', 'yod_waw_events', 'note']
SIG = {'[': 'L', '[[': 'E', '(': 'P', '{': 'C', '<': 'A'}
CLOSE = {']': '[', ']]': '[[', ')': '(', '}': '{', '>': '<'}


# ------------------------------------------------------------------ parsing

def parse_reading(reading: str):
    """Return [(letter, states, token_index)] for a reading written with sigla.
    States: L lacuna [ ], E editor's supplement [[ ]], P correction ( ), C cancelled { }, A inserted < >.
    A reading starting with '#' is a description, not letters (e.g. a numeral sign)."""
    s = nfc(reading or '').strip()
    if s.startswith('#'):
        return []
    if has_latin_translit(s):
        s = translit_to_hebrew(s)
    out, stack, tok, seen = [], [], 0, False
    i = 0
    while i < len(s):
        two, ch = s[i:i + 2], s[i]
        if two in ('[[', ']]'):
            if two == '[[':
                stack.append('[[')
            elif '[[' in stack:
                stack.remove('[[')
            i += 2
            continue
        if ch in '[({<':
            stack.append(ch)
        elif ch in '])}>':
            if CLOSE[ch] in stack:
                stack.reverse(); stack.remove(CLOSE[ch]); stack.reverse()
        elif ch.isspace():
            if seen:
                tok += 1
                seen = False
        elif base(ch) in LETTERS:
            out.append((base(ch), frozenset(SIG[x] for x in stack), tok))
            seen = True
        i += 1
    return out


def letters_of(seq, engraved=False):
    if engraved:
        seq = [x for x in seq if not ({'E', 'P'} & x[1])]
    return seq


def tokens_of(seq):
    groups = defaultdict(str)
    for ch, _, t in seq:
        groups[t] += ch
    return [groups[k] for k in sorted(groups)]


def classify(a_seq, b_seq, note='', engraved=False):
    """Frozen class rules (PLAN.md section 6). Returns (class, ops, yw_consonantal)."""
    a_seq, b_seq = letters_of(a_seq, engraved), letters_of(b_seq, engraved)
    la, lb = ''.join(x[0] for x in a_seq), ''.join(x[0] for x in b_seq)
    yw_cons = '[yw-consonantal]' in note
    if la == lb:
        return ('DIVISION' if tokens_of(a_seq) != tokens_of(b_seq) else 'SAME'), [], yw_cons
    ops = levenshtein_ops(la, lb)
    diff = [o for o in ops if o[0] != '=']
    states = []
    for op, x, y, i, j in diff:
        if i is not None:
            states.append(a_seq[i][1])
        if j is not None:
            states.append(b_seq[j][1])
    if any('L' in st for st in states):
        return 'RESTORATION', ops, yw_cons
    if '[emended]' in note or (not engraved and any(st & {'E', 'P', 'C', 'A'} for st in states)):
        return 'OTHER', ops, yw_cons
    if len(diff) / max(len(la), len(lb)) > 0.5:
        return 'OTHER', ops, yw_cons
    subs = [o for o in diff if o[0] == 'S']
    if any(yw_cons or not (o[1] in YW and o[2] in YW) for o in subs):
        return 'SHAPE', ops, yw_cons
    if not yw_cons and all(o[0] == 'S' or (o[1] or o[2]) in YW for o in diff):
        return 'MATRES', ops, yw_cons
    return 'OTHER', ops, yw_cons


# ------------------------------------------------------------------ editions

def edition_year(name: str) -> int:
    m = re.search(r'(1[89]\d\d|20\d\d)', name)
    if m:
        return int(m.group(1))
    return CANONICAL_YEAR.get(name.split()[0], 9999)


def order_key(name):
    return (edition_year(name), name)


# ------------------------------------------------------------------ sources

def read_csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def load_etcbc_words():
    from build_ap import load_etcbc
    return {k: v[1] for k, v in load_etcbc().items()}


def load_rows():
    rows = []
    for r in read_csv(HERE / 'variants_manual.csv'):
        rows.append({'column': r['column'], 'line': int(r['line']), 'word_index': r['word_index'],
                     'source': r['src'], 'edition_a': r['edition_a'].strip(), 'reading_a': r['reading_a'],
                     'page_a': r['page_a'], 'edition_b': r['edition_b'].strip(), 'reading_b': r['reading_b'],
                     'page_b': r['page_b'], 'note': r['note']})
    ap = read_csv(HERE / 'ap_variants.csv')
    ov = read_csv(HERE / 'ap_overrides.csv')
    okey = {(o['column'], o['line'], o['word_index'], o['puech2015_generated']): o for o in ov if o['action'] != 'add'}
    used = set()
    ap_rows = []
    for r in ap:
        k = (r['column'], r['line'], r['word_index'], r['puech2015'])
        o = okey.get(k)
        note = r['parse_note']
        if o:
            used.add(k)
            if o['action'] == 'drop':
                continue
            r = dict(r, word_index=o['new_word_index'], abegg=o['new_abegg'], puech2015=o['new_puech2015'])
            note = 'override: ' + o['note']
        ap_rows.append((r, note))
    unused = set(okey) - used
    if unused:
        raise ValueError(f'ap_overrides.csv rows that match nothing: {sorted(unused)}')
    for o in ov:
        if o['action'] == 'add':
            ap_rows.append(({'column': o['column'], 'line': o['line'], 'word_index': o['new_word_index'],
                             'abegg': o['new_abegg'], 'puech2015': o['new_puech2015'],
                             'puech2015_page': read_page(o['column'])}, 'override: ' + o['note']))
    for r, note in ap_rows:
        rows.append({'column': r['column'], 'line': int(r['line']), 'word_index': r['word_index'],
                     'source': 'AP', 'edition_a': ABEGG, 'reading_a': r['abegg'],
                     'page_a': f"3Q15 {r['column']} {r['line']}", 'edition_b': 'Puech 2015',
                     'reading_b': r['puech2015'], 'page_b': f"p. {r.get('puech2015_page') or read_page(r['column'])}",
                     'note': note})
    return rows


def read_page(col):
    from build_ap import PUECH2015_PAGE
    return PUECH2015_PAGE[col]


# ------------------------------------------------------------------ word positions

def word_indices(wi: str):
    return [int(x) for x in wi.split('-')] if wi else []


def match_word_index(words: dict, seq):
    """Best contiguous span of 1-3 ETCBC words for a reading (normalised distance <= 0.5)."""
    target = ''.join(x[0] for x in seq)
    if not target or not words:
        return ''
    idx = sorted(words)
    best = None
    for n in (1, 2, 3):
        for s in range(len(idx) - n + 1):
            span = idx[s:s + n]
            if span[-1] - span[0] != n - 1:
                continue
            txt = ''.join(x[0] for x in parse_reading(' '.join(words[w] for w in span)))
            ops = levenshtein_ops(txt, target)
            d = sum(1 for o in ops if o[0] != '=') / max(len(txt), len(target), 1)
            key = (d, n, span[0])
            if best is None or key < best[0]:
                best = (key, span)
    if best and best[0][0] <= 0.5:
        return '-'.join(str(w) for w in best[1]) if len(best[1]) > 1 else str(best[1][0])
    return ''


def sub_word(row, b_seq, j):
    """ETCBC word index for a substitution at letter j of reading B."""
    idx = word_indices(row['word_index'])
    if not idx:
        return 'w?' + row['letters_b']
    ntok = len(tokens_of(b_seq))
    if len(idx) > 1 and ntok == len(idx) and j is not None:
        return f'w{idx[b_seq[j][2]]}'
    return f'w{idx[0]}'


# ------------------------------------------------------------------ build

def analyse(rows, etcbc_words):
    out = []
    for r in rows:
        if is_excluded(r['column'], r['line']):
            raise ValueError(f"excluded position in sources: {r['column']} {r['line']}")
        for k in ('reading_a', 'reading_b', 'note', 'page_a', 'page_b'):
            if mentions_excluded(r[k]):
                raise ValueError(f"excluded zone mentioned in {k} at {r['column']} {r['line']}")
        a_seq, b_seq = parse_reading(r['reading_a']), parse_reading(r['reading_b'])
        r = dict(r)
        r['letters_a'] = ''.join(x[0] for x in a_seq)
        r['letters_b'] = ''.join(x[0] for x in b_seq)
        method = 'given'
        if not r['word_index']:
            words = etcbc_words.get((r['column'], r['line']), {})
            r['word_index'] = match_word_index(words, b_seq) or match_word_index(words, a_seq)
            method = 'matched' if r['word_index'] else 'unknown'
        r['word_index_method'] = method
        cls, ops, ywc = classify(a_seq, b_seq, r['note'])
        cls_e, ops_e, _ = classify(a_seq, b_seq, r['note'], engraved=True)
        r['class'], r['class_engraved'] = cls, cls_e
        # orientation: earlier edition -> later edition
        forward = order_key(r['edition_a']) <= order_key(r['edition_b'])
        r['_events'] = events(r, ops, a_seq, b_seq, ywc, forward)
        r['_events_engraved'] = events(r, ops_e, letters_of(a_seq, True), letters_of(b_seq, True), ywc, forward)
        subs = [e for e in r['_events'] if e[0] == 'S']
        r['substitutions'] = ';'.join(f'{e[2]}' for e in subs)
        r['shape_pairs'] = ';'.join(e[1] for e in subs if e[4]) if cls == 'SHAPE' else ''
        r['shape_events'] = ';'.join(f'{e[1]}@{place_of(r, e[3])}' for e in subs if e[4]) if cls == 'SHAPE' else ''
        r['yod_waw_events'] = ';'.join(f'{e[1]}@{place_of(r, e[3])}' for e in subs if not e[4]) \
            if cls in ('SHAPE', 'MATRES') else ''
        r['insertions'] = ''.join(e[1] for e in r['_events'] if e[0] == 'I')
        r['deletions'] = ''.join(e[1] for e in r['_events'] if e[0] == 'D')
        od = Counter(e[2] for e in subs)
        r['transposition'] = 'yes' if any(f'{b}→{a}' in od for a, b in (x.split('→') for x in od)) else ''
        out.append(r)
    # merge rows that give the same place, editions and letters
    merged, seen = [], {}
    for r in out:
        k = (r['column'], r['line'], r['word_index'], r['edition_a'], r['edition_b'], r['letters_a'], r['letters_b'])
        if k in seen:
            m = seen[k]
            m['source'] = '+'.join(sorted(set(m['source'].split('+')) | {r['source']}))
            if r['note'] and r['note'] not in m['note']:
                m['note'] = (m['note'] + ' | ' + r['note']).strip(' |')
            continue
        seen[k] = r
        merged.append(r)
    merged.sort(key=lambda r: (ROMAN.index(r['column']), r['line'], word_indices(r['word_index'])[:1] or [999],
                               r['word_index'], r['source'], r['edition_a'], r['letters_a'], r['edition_b'],
                               r['letters_b'], r['reading_a'], r['reading_b']))
    for n, r in enumerate(merged, 1):
        r['id'] = f'V{n:04d}'
    return merged


def events(row, ops, a_seq, b_seq, ywc, forward):
    """(kind, unordered pair or letter, ordered label, place_word, counts_as_shape) per difference."""
    ev = []
    for op, x, y, i, j in ops:
        if op == '=':
            continue
        if op == 'S':
            first, second = (x, y) if forward else (y, x)
            is_yw = x in YW and y in YW
            word = sub_word(row, b_seq, j)
            ev.append(('S', pair_key(x, y), f'{first}→{second}', word, ywc or not is_yw))
        else:
            letter = x if op == 'D' else y
            # D: in A not in B. Re-orient to earlier -> later.
            kind = op if forward else ('I' if op == 'D' else 'D')
            word = sub_word(row, b_seq, j) if j is not None else sub_word(row, b_seq, None)
            ev.append((kind, letter, kind + letter, word, False))
    return ev


def place_of(r, word):
    return f"{r['column']} {r['line']} {word}"


def tally(rows, cls_key='class', ev_key='_events', keep=lambda r: True):
    """Count SHAPE substitutions per pair, by row occurrence and by place."""
    by_place = defaultdict(set)
    by_place_ord = defaultdict(set)
    count_rows, count_rows_ord = Counter(), Counter()
    editions = defaultdict(set)
    ins, dels = defaultdict(set), defaultdict(set)
    for r in rows:
        if r[cls_key] != 'SHAPE' or not keep(r):
            continue
        for kind, key, label, word, shape in r[ev_key]:
            p = place_of(r, word)
            if kind == 'S' and shape:
                count_rows[key] += 1
                count_rows_ord[label] += 1
                by_place[key].add(p)
                by_place_ord[label].add(p)
                editions[key].update((r['edition_a'], r['edition_b']))
            elif kind == 'I':
                ins[key].add(p)
            elif kind == 'D':
                dels[key].add(p)
    return {'by_place': by_place, 'by_place_ord': by_place_ord, 'count_rows': count_rows,
            'count_rows_ord': count_rows_ord, 'editions': editions, 'ins': ins, 'dels': dels}


def bootstrap(by_place, n_boot=N_BOOT, seed=SEED):
    """90% percentile interval of the add-one rate per pair, resampling places."""
    place_pairs = defaultdict(set)
    for pair, places in by_place.items():
        for p in places:
            place_pairs[p].add(pair)
    places = sorted(place_pairs)
    sizes = [len(place_pairs[p]) for p in places]
    where = defaultdict(list)
    for i, p in enumerate(places):
        for pair in place_pairs[p]:
            where[pair].append(i)
    rng = random.Random(seed)
    samples = defaultdict(list)
    n = len(places)
    for _ in range(n_boot):
        mult = Counter(rng.choices(range(n), k=n)) if n else Counter()
        total = sum(sizes[i] * m for i, m in mult.items())
        for pair in by_place:
            c = sum(mult.get(i, 0) for i in where[pair])
            samples[pair].append((c + 1) / (total + N_UNORDERED_PAIRS))
    ci = {}
    for pair, vals in samples.items():
        vals.sort()
        ci[pair] = (vals[int(0.05 * (len(vals) - 1))], vals[int(round(0.95 * (len(vals) - 1)))])
    return ci, n


def table(t, with_ci=True):
    N = sum(len(v) for v in t['by_place'].values())
    ci, n_places = bootstrap(t['by_place']) if with_ci else ({}, None)
    rows = []
    for pair, places in t['by_place'].items():
        x, y = pair.split('–')
        rows.append({'pair': pair, 'letter_1': x, 'letter_2': y, 'count_places': len(places),
                     'count_rows': t['count_rows'][pair],
                     'rate': round((len(places) + 1) / (N + N_UNORDERED_PAIRS), 6),
                     'ci90_low': round(ci[pair][0], 6) if with_ci else '',
                     'ci90_high': round(ci[pair][1], 6) if with_ci else '',
                     f'{x}→{y}_places': len(t['by_place_ord'].get(f'{x}→{y}', ())),
                     f'{y}→{x}_places': len(t['by_place_ord'].get(f'{y}→{x}', ())),
                     'n_editions': len(t['editions'][pair]),
                     'places': ';'.join(sorted(places, key=place_sort))})
    rows.sort(key=lambda r: (-r['count_places'], -r['count_rows'], LETTERS.index(r['letter_1']), LETTERS.index(r['letter_2'])))
    for k, r in enumerate(rows, 1):
        r['rank'] = k
    return rows, N, n_places


def place_sort(p):
    c, l, w = p.split(' ', 2)
    return (ROMAN.index(c), int(l), w)


def top(rows, k=10, key='count_places'):
    return [r['pair'] for r in sorted(rows, key=lambda r: (-r[key], -r['count_rows'] if key != 'count_rows' else -r['count_places'], r['pair']))[:k]]


def build_all():
    etcbc_words = load_etcbc_words()
    variants = analyse(load_rows(), etcbc_words)
    prim = tally(variants)
    prim_rows, N, n_places = table(prim)
    sens = {
        'engraved_letters': tally(variants, 'class_engraved', '_events_engraved'),
        'source_AP_only': tally(variants, keep=lambda r: 'AP' in r['source']),
        'notes_only_PN_RJ': tally(variants, keep=lambda r: r['source'] != 'AP'),
        'no_transposition_rows': tally(variants, keep=lambda r: not r['transposition']),
        'substitution_only_rows': tally(variants, keep=lambda r: not r['insertions'] and not r['deletions']),
    }
    top_primary = top(prim_rows)
    sensitivity = {}
    for name, t in sens.items():
        rws, n_, _ = table(t, with_ci=False)
        sensitivity[name] = {'N_place_substitutions': n_, 'top10': [(r['pair'], r['count_places']) for r in rws[:10]],
                             'top10_overlap_with_primary': len(set(r['pair'] for r in rws[:10]) & set(top_primary))}
    top_rows = top(prim_rows, key='count_rows')
    sum_rows = sum(prim['count_rows'].values())
    dependence = {
        'sum_count_rows': sum_rows, 'sum_count_places': N,
        'duplication_ratio_rows_per_place': round(sum_rows / N, 3) if N else None,
        'top10_by_places': top_primary, 'top10_by_rows': top_rows,
        'top10_overlap': len(set(top_primary) & set(top_rows)),
    }
    ordered = []
    for label, places in prim['by_place_ord'].items():
        ordered.append({'ordered_pair': label, 'count_places': len(places), 'count_rows': prim['count_rows_ord'][label]})
    ordered.sort(key=lambda r: (-r['count_places'], -r['count_rows'], r['ordered_pair']))
    indels = {'insertions_later_edition': {k: len(v) for k, v in sorted(prim['ins'].items())},
              'deletions_later_edition': {k: len(v) for k, v in sorted(prim['dels'].items())}}
    yw_places = sorted({e.split('@')[1] for r in variants for e in r['yod_waw_events'].split(';') if e},
                       key=place_sort)
    letter_load = Counter()
    for r in prim_rows:
        letter_load[r['letter_1']] += r['count_places']
        letter_load[r['letter_2']] += r['count_places']
    classes = Counter(r['class'] for r in variants)
    classes_e = Counter(r['class_engraved'] for r in variants)
    by_source = defaultdict(Counter)
    for r in variants:
        for s in r['source'].split('+'):
            by_source[s][r['class']] += 1
    meta = {
        'plan_sha256': hashlib.sha256((HERE / 'PLAN.md').read_bytes()).hexdigest(),
        'seed': SEED, 'bootstrap_replicates': N_BOOT, 'unordered_pairs_possible': N_UNORDERED_PAIRS,
        'N_place_substitutions': N, 'shape_places': n_places, 'variant_rows': len(variants),
        'rate': '(count_places + 1) / (N + 231)', 'final_forms': 'counted as base letters',
        'exclusion': 'see PLAN.md section 2 (enforced by exclusion.py and tests)',
    }
    conf_json = {'meta': meta, 'unordered': prim_rows, 'ordered': ordered, 'indels': indels,
                 'letter_involvement_places': dict(sorted(letter_load.items(), key=lambda kv: (-kv[1], LETTERS.index(kv[0])))),
                 'classes': dict(sorted(classes.items())), 'classes_engraved': dict(sorted(classes_e.items())),
                 'classes_by_source': {k: dict(sorted(v.items())) for k, v in sorted(by_source.items())},
                 'dependence': dependence, 'sensitivity': sensitivity,
                 'yod_waw_vowel_letter_places': {'count_places': len(yw_places), 'places': yw_places,
                                                 'note': 'yod-waw substitutions in MATRES and SHAPE rows; not in the SHAPE table'}}
    return variants, prim_rows, conf_json


def render(variants, prim_rows, conf_json):
    files = {}
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=VARIANT_FIELDS, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    for r in variants:
        w.writerow(r)
    files['variants.csv'] = buf.getvalue()
    buf = io.StringIO()
    fields = ['rank', 'pair', 'letter_1', 'letter_2', 'count_places', 'count_rows', 'rate', 'ci90_low', 'ci90_high',
              'forward_places', 'backward_places', 'n_editions', 'places']
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    for r in prim_rows:
        x, y = r['letter_1'], r['letter_2']
        w.writerow({**{k: r[k] for k in fields if k in r},
                    'forward_places': f"{x}→{y}: {r[f'{x}→{y}_places']}",
                    'backward_places': f"{y}→{x}: {r[f'{y}→{x}_places']}"})
    files['confusions.csv'] = buf.getvalue()
    files['confusions.json'] = json.dumps(conf_json, ensure_ascii=False, indent=1, sort_keys=False) + '\n'
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='rebuild in memory and compare with the files')
    args = ap.parse_args()
    files = render(*build_all())
    for name, text in files.items():
        if mentions_excluded(text):
            raise SystemExit(f'{name} mentions the excluded zone')
    if args.check:
        bad = [n for n, t in files.items() if (HERE / n).read_text(encoding='utf-8') != t]
        print('check:', 'OK' if not bad else f'differs: {bad}')
        sys.exit(1 if bad else 0)
    for name, text in files.items():
        (HERE / name).write_text(text, encoding='utf-8')
        print(name, hashlib.sha256(text.encode()).hexdigest()[:16])


if __name__ == '__main__':
    main()
