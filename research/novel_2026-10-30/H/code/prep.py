"""Lane H corpus preparation (EXPLORATORY build step; the frozen protocol hashes this file).

Builds normalised character text for a character language model and the 3Q15 graphic-word table.

    python3 -I prep.py TF_DIR SEFARIA_DIR SEFARIA_MANIFEST OUT_DIR

Normalisation (same for every source):
  * Hebrew consonants only; final letters map to base letters (ך→כ, ם→מ, ן→נ, ף→פ, ץ→צ).
  * Matres lectionis are kept as written (no spelling change).
  * Word separator: one space. A break in the text (gap, illegible letter, restoration,
    abbreviation, foreign word) ends a segment; one segment per output line.
  * A number written with numeral signs becomes the single symbol '9' (3Q15 and DSS alike).

ETCBC DSS (Text-Fabric tf/2.0.2), training text:
  * non-biblical scrolls only (scroll feature biblical is empty); words with lang 'a' (Aramaic) or
    'g' (Greek) are breaks; scrolls whose words are >50% Aramaic are dropped whole;
  * every node of scroll 3Q15 is removed;
  * a word with a reconstructed sign (rec), a missing sign, an illegible sign, or an alternative
    reading (alt) is a break, and the whole graphic word it belongs to is dropped; signs removed by
    an editor (rem) are dropped; corrections kept.
  * lines of one fragment are joined with a space.
  * biblical scrolls are written to a separate file (bib_train.txt); whether they enter the model
    is a model option chosen on the development split;
  * split by scroll: 10% of scrolls (seed 20261030) form the development split.
Sefaria Mishnah (Kaufmann MS ed. Be'eri; one tractate Torat Emet) and Tosefta (Vilna/Machon Mamre):
  * HTML tags and parenthesised text (scripture references) are removed; square brackets dropped
    (their letters kept); vowel points and cantillation removed; maqaf becomes a space;
  * a token holding ״ " ׳ ' (abbreviation or numeral) is a break; . : ; ? ! end a segment;
  * split by tractate: 10% of tractates per collection (seed 20261030) form the development split.
"""
import sys, os, re, json, random, hashlib, collections
from tf.fabric import Fabric

FINAL = str.maketrans('ךםןףץ', 'כמנפצ')
HEB = set('אבגדהוזחטיכלמנסעפצקרשת')


def norm_word(s):
    s = s.translate(FINAL)
    return ''.join(ch for ch in s if ch in HEB)


def build_dss(tfdir, biblical=False, TF=None):
    TF = TF or Fabric(locations=tfdir, silent='deep')
    api = TF.load('otype scroll biblical lang glyph after type rec rem alt unc cor morpho fragment line', silent='deep')
    F, L = api.F, api.L
    scrolls = {}
    q15 = None
    used = set()
    for sc in F.otype.s('scroll'):
        name = F.scroll.v(sc)
        if name == '3Q15':
            q15 = sc
            continue
        if (F.biblical.v(sc) is not None) != biblical:
            continue
        words = L.d(sc, 'word')
        if not words:
            continue
        na = sum(1 for w in words if F.lang.v(w) == 'a')
        if na > 0.5 * len(words):
            continue
        segs = []
        cur = []
        buf = ''
        last_frag = None
        def flush():
            nonlocal cur, buf
            if buf:
                cur.append(buf); buf = ''
            if cur:
                segs.append(' '.join(cur)); cur = []
        for w in words:
            frag = L.u(w, 'fragment')
            frag = frag[0] if frag else None
            if frag != last_frag:
                flush(); last_frag = frag
            t = F.type.v(w)
            if t == 'punct':
                if buf:
                    cur.append(buf); buf = ''
                continue
            if F.lang.v(w) in ('a', 'g'):
                buf = ''
                flush(); continue
            signs = L.d(w, 'sign')
            bad = False
            txt = ''
            isnum = False
            for s in signs:
                st = F.type.v(s)
                if F.rem.v(s):
                    continue
                if st in ('missing', 'unc') or F.rec.v(s) or F.alt.v(s):
                    bad = True; break
                if st == 'numr':
                    isnum = True; continue
                if st == 'cons':
                    txt += F.glyph.v(s)
            used.add(w)
            if bad:
                buf = ''  # drop the partial graphic word too
                flush(); continue
            if isnum:
                if buf:
                    cur.append(buf); buf = ''
                cur.append('9')
            else:
                buf += norm_word(txt)
            if F.after.v(w) is not None and buf:
                cur.append(buf); buf = ''
        flush()
        scrolls[name] = segs
    return scrolls, q15, api, used, TF


def q15_table(api, q15):
    """Graphic words of 3Q15 with column, line, ETCBC word index, normalised string and flags."""
    F, L = api.F, api.L
    rows = []
    for ln in L.d(q15, 'line'):
        col = F.fragment.v(L.u(ln, 'fragment')[0])
        lno = F.line.v(ln)
        gw = []
        cur = []
        for w in L.d(ln, 'word'):
            if F.type.v(w) == 'punct':
                continue
            cur.append(w)
            if F.after.v(w) is not None:
                gw.append(cur); cur = []
        if cur:
            gw.append(cur)
        for i, ws in enumerate(gw):
            txt = ''; flags = set(); isnum = False; foreign = False
            for w in ws:
                if F.lang.v(w) in ('a', 'g'):
                    foreign = True
                for s in L.d(w, 'sign'):
                    st = F.type.v(s)
                    if F.rem.v(s):
                        flags.add('rem'); continue
                    if st in ('missing', 'unc'):
                        flags.add(st)
                    if F.rec.v(s): flags.add('rec')
                    if F.alt.v(s): flags.add('alt')
                    if F.unc.v(s): flags.add('uncertain_letter')
                    if F.cor.v(s): flags.add('cor')
                    if st == 'numr': isnum = True
                    if st == 'cons': txt += F.glyph.v(s)
            morph = [ (api.F.morpho.v(w) or '') for w in ws ] if hasattr(api.F, 'morpho') else []
            rows.append({'column': int(col), 'line': int(lno), 'word_index': i,
                         'string': '9' if isnum else ('' if foreign else norm_word(txt)),
                         'kind': 'number' if isnum else ('foreign' if foreign else 'hebrew'),
                         'flags': sorted(flags), 'morph': morph})
    return rows


def strip_rab(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\([^)]*\)', ' ', s)
    s = re.sub(r'[֑-ׇ]', lambda m: ' ' if m.group(0) == '־' else '', s)
    s = s.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    segs = []
    for part in re.split(r'[.:;?!\n]+', s):
        cur = []
        for tok in part.split():
            if re.search('[״"׳\']', tok):
                if cur: segs.append(' '.join(cur)); cur = []
                continue
            w = norm_word(tok)
            if w:
                cur.append(w)
        if cur:
            segs.append(' '.join(cur))
    return segs


def flat(t):
    if isinstance(t, str):
        yield t
    else:
        for x in t:
            yield from flat(x)


def main():
    tfdir, sefdir, sefman, out = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    rng = random.Random(20261030)
    scrolls, q15, api, used, TF = build_dss(tfdir)
    bscrolls, _, _, bused, _ = build_dss(tfdir, biblical=True, TF=TF)
    q15_words = set(api.L.d(q15, 'word')) | set(api.L.d(q15, 'sign'))
    q15_left = len(q15_words & (used | bused))
    # 3Q15 table
    rows = q15_table(api, q15)
    json.dump(rows, open(os.path.join(out, 'q15_words.json'), 'w'), ensure_ascii=False)
    names = sorted(scrolls)
    dev = set(rng.sample(names, max(1, len(names) // 10)))
    with open(os.path.join(out, 'dss_train.txt'), 'w') as ft, open(os.path.join(out, 'dss_dev.txt'), 'w') as fd:
        for n in names:
            (fd if n in dev else ft).write('\n'.join(scrolls[n]) + '\n' if scrolls[n] else '')
    with open(os.path.join(out, 'bib_train.txt'), 'w') as fb:
        for n in sorted(bscrolls):
            if bscrolls[n]:
                fb.write('\n'.join(bscrolls[n]) + '\n')
    # Sefaria
    man = json.load(open(sefman))
    ok = [r for r in man if r['status'] == 'ok']
    mish = sorted(r['file'] for r in ok if r['title'].startswith('Mishnah'))
    tos = sorted(r['file'] for r in ok if r['title'].startswith('Tosefta'))
    devr = set(rng.sample(mish, max(1, len(mish) // 10))) | set(rng.sample(tos, max(1, len(tos) // 10)))
    with open(os.path.join(out, 'rab_train.txt'), 'w') as ft, open(os.path.join(out, 'rab_dev.txt'), 'w') as fd:
        for fn in mish + tos:
            d = json.load(open(os.path.join(sefdir, fn)))
            segs = []
            for s in flat(d['text']):
                segs += strip_rab(s)
            (fd if fn in devr else ft).write('\n'.join(segs) + '\n')
    stats = {'dss_scrolls_kept': len(names), 'dss_dev_scrolls': sorted(dev), 'rab_dev_files': sorted(devr),
             'q15_scroll_node': q15,
             'q15_scrolls_in_training': sum(1 for n in list(names) + list(bscrolls) if n == '3Q15'),
             'q15_word_nodes_read_into_training': q15_left,
             'nodes_read_into_training': len(used | bused),
             'biblical_scrolls': len(bscrolls),
             'q15_graphic_words': len(rows)}
    for fn in ['dss_train.txt', 'dss_dev.txt', 'rab_train.txt', 'rab_dev.txt', 'bib_train.txt']:
        b = open(os.path.join(out, fn), 'rb').read()
        stats[fn] = {'chars': len(b.decode('utf-8')), 'sha256': hashlib.sha256(b).hexdigest()}
    json.dump(stats, open(os.path.join(out, 'prep_stats.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in stats.items() if k not in ('dss_dev_scrolls', 'rab_dev_files')}, indent=1))


if __name__ == '__main__':
    main()
