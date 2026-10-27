"""Exploratory: cost of the K=2 segmentation with the first seam at 11 and the second seam moved."""
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore.py')).read().split('\nout = {}')[0]
exec(src)
cf, p = make(ALLBIN, list(ALLCAT)); F = cf(np.arange(N)); C = np.where(VALID, sum(F.values()), np.inf)
a = POS['11']
for e in ('47', '48', '49', '50', '51', '52', '55', '57', '58'):
    b = POS[e]
    print('seams 11 +', e, round(float(C[0, a] + C[a, b] + C[b, N]), 2), {f: round(float(F[f][a, b] + F[f][b, N]), 1) for f in F})
