"""Run 18 copy search: formula-signature windows over DSS (ETCBC dss 2.0.2) and BHSA 2021.
Usage: python -I search.py <spec.json> <dss_units.json> <bhsa_units.json> <outdir>
"""
import sys, json, re, random, collections

spec = json.load(open(sys.argv[1], encoding='utf-8'))
DSS = json.load(open(sys.argv[2], encoding='utf-8'))
BHSA = json.load(open(sys.argv[3], encoding='utf-8'))
OUT = sys.argv[4]
W = spec['window_words']
FOLD = str.maketrans('ךםןףץ', 'כמנפצ')
CARD = re.compile(spec['cardinal_regex'])
DIRRE = re.compile(spec['direction_prefix_regex'])
NUMMARK = re.compile('[֑-֯]')  # cantillation-type marks used for numeral signs in the dss Unicode


def cons(s):
    return ''.join(ch for ch in s if 'א' <= ch <= 'ת').translate(FOLD)


def part_info(p, variant):
    """returns (class or None, is_number)"""
    g = p['g']
    isnum = p.get('typ') == 'numr' or bool(NUMMARK.search(g))
    c = '' if isnum else cons(g)
    if variant.get('rec') and p.get('ncons') and p['nrec'] * 2 >= p['ncons']:
        return None, False
    if not isnum and (p.get('sp') == 'numr' or p.get('cl') == 'card' or (c and CARD.match(c))):
        isnum = True
    cls = None
    if c:
        raw = ''.join(ch for ch in g if '\u05D0' <= ch <= '\u05EA')
        for k, forms in variant['classes'].items():
            if c in forms:
                cls = k
                break
        if cls == 'TALENT' and c == 'ככ' and raw != 'ככ':
            cls = None  # 3Q15 writes the abbreviation with medial kaf; final-kaf כך is 'thus', not an attested spelling
        if cls is None and DIRRE.match(c):
            cls = 'DIRECTION'
        if cls == 'DIRECTION' and variant.get('dir4'):
            cls = 'DIR_' + DIRRE.match(c).group(1)
    return cls, isnum


def annotate(words, variant):
    """words: list of graphical words (with parts). Returns per word: set of classes, measure_followed_by_number flag,
    number-after-measure flag (NUM attributed to the word holding the number)."""
    flat = []  # (word index, cls, isnum)
    for i, w in enumerate(words):
        for p in w['parts']:
            cls, isnum = part_info(p, variant)
            flat.append((i, cls, isnum))
    n = len(words)
    classes = [set() for _ in range(n)]
    mnum = [False] * n
    for j, (i, cls, isnum) in enumerate(flat):
        if cls:
            classes[i].add(cls)
        if cls in spec['measures'] and j + 1 < len(flat) and flat[j + 1][2] and flat[j + 1][0] in (i, i + 1):
            mnum[i] = True
            classes[flat[j + 1][0]].add('NUM')
    return classes, mnum


def windows(classes, mnum, strict):
    n = len(classes)
    hits = []
    for s in range(max(1, n - W + 1)):
        e = min(n, s + W)
        if not any(mnum[s:e]):
            continue
        cl = set().union(*classes[s:e])
        if strict:
            cl.discard('NUM')
        if len(cl) >= 3:
            hits.append(s)
    return hits


def loci(hits):
    out = []
    for s in hits:
        if out and s <= out[-1][1]:
            out[-1][1] = s + W - 1
        else:
            out.append([s, s + W - 1])
    return out


def clean(words):
    return [w for w in words if cons(w['t']) or any(p.get('typ') == 'numr' or NUMMARK.search(p['g']) for p in w['parts'])]


def category(u):
    sc = u['scroll']
    if u['biblical'] == 'BHSA':
        return 'BHSA'
    if sc == '3Q15':
        return '3Q15'
    qumran = bool(re.match(r'^(\d+Q|1Q|CD|KhQ|PAM|Pam|XQ|Xq|X\d)', sc)) or sc.startswith(('1QS', '1QM', '1QH', '1Qp', '1Qisa'))
    bib = u['biblical'] in ('1', '2')
    if qumran:
        return 'QUMRAN_BIB' if bib else 'QUMRAN_NONBIB'
    return 'OTHER_SITES_BIB' if bib else 'OTHER_SITES_NONBIB'


def run(variant_name, variant, strict, units, shuffle=True):
    stats = collections.Counter()
    hitrows = []
    for ui, u in enumerate(units):
        words = clean(u['words'])
        cat = category(u)
        stats[(cat, 'words')] += len(words)
        stats[(cat, 'units')] += 1
        classes, mnum = annotate(words, variant)
        hs = windows(classes, mnum, strict)
        if not hs:
            continue
        L = loci(hs)
        stats[(cat, 'loci')] += len(L)
        stats[(cat, 'hit_units')] += 1
        row = dict(category=cat, scroll=u['scroll'], fragment=u['fragment'], n_words=len(words), n_loci=len(L), loci=[])
        for a, b in L:
            b = min(b, len(words) - 1)
            cl = sorted(set().union(*classes[a:b + 1]))
            row['loci'].append(dict(lines=sorted(set(w['line'] for w in words[a:b + 1]), key=str),
                                    ref=words[a].get('ref', ''), classes=cl,
                                    text=' '.join(w['full'] or w['t'] for w in words[a:b + 1])))
        if shuffle and cat != 'BHSA':
            rng = random.Random(20261027 + ui)
            k = 0
            idx = list(range(len(words)))
            for _ in range(1000):
                rng.shuffle(idx)
                sw = [words[i] for i in idx]
                c2, m2 = annotate(sw, variant)
                if windows(c2, m2, strict):
                    k += 1
            row['shuffle_k'] = k
            row['p'] = round((k + 1) / 1001, 4)
        hitrows.append(row)
    return stats, hitrows


if __name__ == '__main__':
    base = dict(classes=spec['classes'])
    variants = {
        'MAIN': (base, False),
        'STRICT': (base, True),
        'V_amt': (dict(classes={**spec['classes'], 'CUBIT': spec['classes']['CUBIT'] + ['אמת']}), False),
        'V_rec': (dict(classes=spec['classes'], rec=True), False),
        'V_dir4': (dict(classes=spec['classes'], dir4=True), False),
    }
    allunits = DSS + BHSA
    summary = {}
    for name, (v, strict) in variants.items():
        stats, rows = run(name, v, strict, allunits, shuffle=True)
        cats = sorted(set(c for c, _ in stats))
        summary[name] = {c: dict(units=stats[(c, 'units')], words=stats[(c, 'words')], hit_units=stats[(c, 'hit_units')],
                                 loci=stats[(c, 'loci')],
                                 loci_per_10k=round(stats[(c, 'loci')] * 1e4 / stats[(c, 'words')], 3) if stats[(c, 'words')] else None)
                         for c in cats}
        json.dump(rows, open(f'{OUT}/hits_{name}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(name, json.dumps(summary[name], ensure_ascii=False))
    json.dump(summary, open(f'{OUT}/summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
