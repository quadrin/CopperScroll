"""Letter substitutions that ANCIENT Qumran scribes corrected in their own ink manuscripts (all scrolls except 3Q15).

Source: ETCBC dss Text-Fabric 2.0.1 (Abegg, Bowley, Cook; conv. Jacobs, Naaijer, Roorda), CC BY-NC 4.0,
https://github.com/ETCBC/dss (tf/2.0.1). Features: rem (1 modern, 2 ancient removal), cor (2 ancient, 3 ancient supralinear).
Rule (fixed before counting): inside one word, a run of signs removed by an ancient hand (rem=2, cor=0) directly adjacent to a
run of the SAME length written by an ancient corrector (cor in {2,3}, rem=0); pair the letters position by position; keep
consonant pairs of two different square-script letters (final forms = base letters; paleo-Hebrew script excluded). Output is
counts per unordered pair and per direction (written -> corrected). 3Q15 is excluded so the Copper Scroll is not used.
usage: python3 build_qumran_corrections.py TFDIR OUT.csv
"""
import sys, csv
from collections import Counter
from tf.fabric import Fabric
TF, OUT = sys.argv[1], sys.argv[2]
api = Fabric(locations=TF, silent='deep').load('otype scroll glyph type cor rem script', silent='deep')
F, L = api.F, api.L
FIN = str.maketrans('ךםןףץ', 'כמנפצ'); HEB = set('אבגדהוזחטיכלמנסעפצקרשת')
pairs = Counter(); ex = {}
for w in F.otype.s('word'):
    sc = F.scroll.v(L.u(w, 'scroll')[0])
    if sc == '3Q15':
        continue
    sg = list(L.d(w, 'sign'))
    lab = []
    for s in sg:
        r = F.rem.v(s) or 0; c = F.cor.v(s) or 0
        lab.append('R' if r == 2 and c == 0 else ('C' if c in (2, 3) and r == 0 else ('B' if r == 2 else '.')))
    runs = []; i = 0
    while i < len(sg):
        j = i
        while j < len(sg) and lab[j] == lab[i]: j += 1
        runs.append((lab[i], i, j)); i = j
    for k in range(len(runs) - 1):
        a, b = runs[k], runs[k + 1]
        if {a[0], b[0]} == {'R', 'C'} and a[2] - a[1] == b[2] - b[1]:
            R, C = (a, b) if a[0] == 'R' else (b, a)
            for x, y in zip(range(R[1], R[2]), range(C[1], C[2])):
                if F.type.v(sg[x]) != 'cons' or F.type.v(sg[y]) != 'cons' or F.script.v(sg[x]) or F.script.v(sg[y]):
                    continue
                gx = (F.glyph.v(sg[x]) or '').translate(FIN); gy = (F.glyph.v(sg[y]) or '').translate(FIN)
                if gx in HEB and gy in HEB and gx != gy:
                    pairs[(gx, gy)] += 1; ex.setdefault((gx, gy), []).append(sc)
und = Counter()
for (x, y), n in pairs.items(): und[tuple(sorted((x, y)))] += n
rows = []
for (a, b), n in sorted(und.items(), key=lambda kv: (-kv[1], kv[0])):
    rows.append(dict(pair=f'{a}–{b}', letter_1=a, letter_2=b, n_events=n, n_1_to_2=pairs.get((a, b), 0), n_2_to_1=pairs.get((b, a), 0),
                     scrolls=';'.join(sorted(set(ex.get((a, b), []) + ex.get((b, a), []))))))
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('events', sum(und.values()), 'pairs', len(und))
