"""Build vorlage_confusion_matrix.csv: a letter-confusion model for copying from a Herodian ink exemplar.

Independent of the modern edition-confusion matrix (research/text/edition_confusions/), which is used only as a control.
Weights FIXED in this file before any Copper Scroll correction check and before any gazetteer scoring.

Components per unordered pair {x, y} of the 22 base letters (finals = base letters):
  D  Delitzsch 1920 (Die Lese- und Schreibfehler im Alten Testament, §§103-131): graphic confusions of the square
     (Aramaic/Jewish) script documented in the MT. Tier A (§§103-108, 'infolge äußerer Ähnlichkeit') = 3,
     tier B (§§109-115, similarity or indistinctness) = 2, tier C (§§116-131, indistinct part of sign; sporadic) = 1.
  Q  Qumran ancient scribal corrections (ETCBC dss 2.0.1, all scrolls but 3Q15): n events written->corrected;
     contribution = min(n, 3).
  S  Shape similarity in the 'Hebrew Square Habakkuk' traced font (1QpHab, ~0 CE): contribution =
     3 * max(0, (sim - s50) / (s_max - s50)) with s50 = median and s_max = maximum over the 231 pairs.
rate(x,y) = 0.01 + D + Q + S      (0.01 = floor so that every pair has a non-zero probability)
p(x,y)    = rate / sum(rate over 231 pairs)   (probability that one copying error is this pair)
usage: python3 -I build_model.py DATA_DIR
"""
import sys, csv, itertools, statistics, os
DD = sys.argv[1]
LET = 'אבגדהוזחטיכלמנסעפצקרשת'
key = lambda a, b: tuple(sorted((a, b)))
TIER = {'A': 3.0, 'B': 2.0, 'C': 1.0}
D, Dsec = {}, {}
for r in csv.DictReader(open(os.path.join(DD, 'delitzsch1920_pairs.csv'), encoding='utf-8')):
    k = key(r['letter_1'], r['letter_2']); v = TIER[r['tier']]
    if v > D.get(k, 0): D[k] = v; Dsec[k] = r['delitzsch_section']
Q = {}
for r in csv.DictReader(open(os.path.join(DD, 'qumran_ancient_corrections_pairs.csv'), encoding='utf-8')):
    Q[key(r['letter_1'], r['letter_2'])] = int(r['n_events'])
S = {}
for r in csv.DictReader(open(os.path.join(DD, 'shape_similarity_habakkuk.csv'), encoding='utf-8')):
    S[key(r['letter_1'], r['letter_2'])] = float(r['shape_sim'])
s50 = statistics.median(S.values()); smax = max(S.values())
rows = []
for a, b in itertools.combinations(LET, 2):
    k = key(a, b)
    d = D.get(k, 0.0); q = min(Q.get(k, 0), 3); s = 3 * max(0.0, (S[k] - s50) / (smax - s50))
    rows.append(dict(pair=f'{k[0]}–{k[1]}', letter_1=k[0], letter_2=k[1], delitzsch=d, delitzsch_section=Dsec.get(k, ''),
                     qumran_corrections=Q.get(k, 0), qumran_term=q, shape_sim=S[k], shape_term=round(s, 4), rate=round(0.01 + d + q + s, 4)))
tot = sum(r['rate'] for r in rows)
for r in rows: r['p'] = round(r['rate'] / tot, 6)
rows.sort(key=lambda r: (-r['rate'], r['pair']))
for i, r in enumerate(rows, 1): r['rank'] = i
with open(os.path.join(DD, 'vorlage_confusion_matrix.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['rank'] + [k for k in rows[0] if k != 'rank']); w.writeheader(); w.writerows(rows)
print('s50', round(s50, 4), 'smax', smax)
for r in rows[:30]: print(r['rank'], r['pair'], r['rate'], 'D', r['delitzsch'], 'Q', r['qumran_corrections'], 'S', r['shape_term'])
