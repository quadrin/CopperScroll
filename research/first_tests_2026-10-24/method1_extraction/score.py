"""Score the Method 1 extraction test.

Usage: python3 -I score.py model_rows.csv [human_rows.csv]

Without human rows: runs the mechanical half of the stop rule (any period, size,
depth, location or quote string that does not occur verbatim in the report text
counts as invented or misquoted).
With human rows: also matches model rows to human rows per report and type and
reports detection recall/precision and field accuracy.
"""
import csv, re, sys, os, difflib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ['period_as_given', 'dated_in_window', 'size_as_given', 'depth_as_given', 'location_as_given', 'count']


def norm(s):
    s = (s or '').replace(' ', ' ').replace('–', '-').replace('—', '-').replace('×', 'x')
    s = s.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()


def text_of(n):
    return norm(open(os.path.join(HERE, 'texts', f'{int(n):03d}.txt'), encoding='utf-8').read())


def load(p):
    return [r for r in csv.DictReader(open(p, encoding='utf-8'))]


def mechanical(rows):
    bad = defaultdict(list)
    for r in rows:
        if r['feature_type'] == 'none':
            continue
        t = text_of(r['report'])
        for f in ['period_as_given', 'size_as_given', 'depth_as_given', 'location_as_given', 'quote']:
            v = norm(r.get(f))
            if v and v not in t:
                bad[f].append((r['report'], r['feature_type'], r.get(f)))
    return bad


def nums(s):
    return sorted(re.findall(r'\d+(?:[.,]\d+)?', norm(s).replace(',', '.')))


def same(f, a, b):
    a, b = norm(a), norm(b)
    if not a and not b:
        return True
    if not a or not b:
        return False
    if f in ('size_as_given', 'depth_as_given', 'count'):
        return nums(a) == nums(b)
    if f == 'dated_in_window':
        return a == b
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.8 or a in b or b in a


def match(model, human):
    """Greedy match within (report, type) by label/location/quote similarity."""
    pairs, um, uh = [], [], []
    g = defaultdict(lambda: ([], []))
    for r in model:
        g[(r['report'], r['feature_type'])][0].append(r)
    for r in human:
        g[(r['report'], r['feature_type'])][1].append(r)
    for k, (ms, hs) in g.items():
        if k[1] == 'none':
            continue
        cand = []
        for i, m in enumerate(ms):
            for j, h in enumerate(hs):
                key_m = norm(m['label'] + ' ' + m['location_as_given'] + ' ' + m['quote'])
                key_h = norm(h['label'] + ' ' + h['location_as_given'] + ' ' + h['quote'])
                cand.append((difflib.SequenceMatcher(None, key_m, key_h).ratio(), i, j))
        cand.sort(reverse=True)
        used_m, used_h = set(), set()
        for s, i, j in cand:
            if i in used_m or j in used_h:
                continue
            used_m.add(i); used_h.add(j); pairs.append((ms[i], hs[j]))
        um += [m for i, m in enumerate(ms) if i not in used_m]
        uh += [h for j, h in enumerate(hs) if j not in used_h]
    return pairs, um, uh


def main():
    model = load(sys.argv[1])
    bad = mechanical(model)
    n = sum(1 for r in model if r['feature_type'] != 'none')
    print(f'model rows (excluding none): {n}')
    for f in ['period_as_given', 'size_as_given', 'depth_as_given', 'location_as_given', 'quote']:
        print(f'  {f}: {len(bad[f])} not verbatim in the report')
        for b in bad[f][:10]:
            print('    ', b)
    if len(sys.argv) < 3:
        return
    human = load(sys.argv[2])
    pairs, um, uh = match(model, human)
    nh = sum(1 for r in human if r['feature_type'] != 'none')
    print(f'human rows: {nh}; matched: {len(pairs)}; recall {len(pairs)/max(nh,1):.2f}; precision {len(pairs)/max(n,1):.2f}')
    tot = ok = 0
    per = defaultdict(lambda: [0, 0])
    for m, h in pairs:
        for f in FIELDS:
            s = same(f, m.get(f), h.get(f))
            per[f][0] += s; per[f][1] += 1; ok += s; tot += 1
    for f in FIELDS:
        print(f'  {f}: {per[f][0]}/{per[f][1]}')
    print(f'field accuracy on matched rows: {ok}/{tot} = {ok/max(tot,1):.3f}')
    inv = [(m['report'], f, m[f]) for m, h in pairs for f in ('size_as_given', 'depth_as_given', 'period_as_given') if norm(m.get(f)) and not norm(h.get(f))]
    print(f'model values where the human left the field blank: {len(inv)}')
    for x in inv[:20]:
        print('   ', x)


if __name__ == '__main__':
    main()
