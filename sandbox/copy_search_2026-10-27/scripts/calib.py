"""Exploratory calibration: would a fragment-sized piece of 3Q15 itself hit, and survive the 1000-shuffle test at p<0.01?
Pieces = consecutive graphical words of one column, lengths 8/12/20/30/46+, starts every 4 words."""
import sys, json, random, importlib.util
spec_ = importlib.util.spec_from_file_location('s', sys.argv[4] + '/search.py')
S = importlib.util.module_from_spec(spec_)
OUTF = sys.argv[5]
sys.argv = ['x', sys.argv[1], sys.argv[2], sys.argv[3], '/dev/null']
spec_.loader.exec_module(S)
v = dict(classes=S.spec['classes'])
cols = [S.clean(u['words']) for u in S.DSS if u['scroll'] == '3Q15']
res = {}
for L in (8, 12, 20, 30):
    n = hit = surv = 0
    for ci, ws in enumerate(cols):
        for s in range(0, len(ws) - L + 1, 4):
            piece = ws[s:s + L]
            n += 1
            c, m = S.annotate(piece, v)
            if not S.windows(c, m, False):
                continue
            hit += 1
            rng = random.Random(1000 * L + 10 * ci + s)
            idx = list(range(L)); k = 0
            for _ in range(1000):
                rng.shuffle(idx)
                sw = [piece[i] for i in idx]
                c2, m2 = S.annotate(sw, v)
                if S.windows(c2, m2, False):
                    k += 1
            if (k + 1) / 1001 < 0.01:
                surv += 1
    res[L] = dict(pieces=n, hit=hit, survive_p01=surv)
    print(L, res[L])
json.dump(res, open(OUTF, 'w'), indent=1)
