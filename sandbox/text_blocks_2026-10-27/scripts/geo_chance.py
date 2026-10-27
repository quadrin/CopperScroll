"""Exploratory: chance that 2 seams placed uniformly at random (all valid K=2 segmentations, min length 3)
reach the rule's 'at least half match' bar, for each region set."""
import csv, os, itertools
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
ENT = [r['entry'] for r in csv.DictReader(open(os.path.join(OUT, 'feature_matrix.csv'), encoding='utf-8'))]
N = len(ENT); POS = {e: i for i, e in enumerate(ENT)}
P = {'9': 'J', '10': 'J', '35': 'J', '49': 'J', '51': 'J', '57': 'G', '58': 'B'}
D1 = dict(P, **{'31': 'Jer', '32': 'Jer', '55': 'J'}); D2 = dict(D1, **{'17': 'Jer', '20': 'S', '21': 'S', '22': 'S', '46': 'J'})
def ch(reg):
    an = sorted(reg, key=lambda e: POS[e]); return [(POS[a], POS[b]) for a, b in zip(an, an[1:]) if reg[a] != reg[b]]
for name, reg in (('P', P), ('D1', D1), ('D2', D2)):
    C = ch(reg); m = lambda t: any(pa - 1 <= t <= pb + 2 for pa, pb in C)
    segs = [(a, b) for a in range(3, N - 2) for b in range(a + 3, N - 2)]
    k = sum((m(a) + m(b)) >= 1 for a, b in segs)
    print(name, 'K=2 random segmentations reaching >=1/2 match:', k, '/', len(segs), round(k / len(segs), 3))
