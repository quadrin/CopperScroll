"""Check (not training, not a clean holdout -- see protocol exposure log): do the Copper Scroll's own engraved-vs-corrected
letter pairs fit the Vorlage model better than the edition model and a uniform model?
Pairs (rule): readings of 'Puech 2015' in research/text/edition_confusions/variants.csv written in Hebrew script that contain
X(Y) with X one Hebrew letter and Y exactly one Hebrew letter (Puech's siglum: engraved X, corrected to Y); one per
(column, line, word_index, X, Y); finals = base letters; XII 8-12 is absent from that file by construction.
Statistic: mean over pairs of log2 p_V(pair) - log2 p_E(pair), and of log2 p_V - log2(1/231); sign test (pairs with p_V > p_E).
Plus: engraver supralinear insertions (ETCBC cor=3 in 3Q15) listed descriptively (insertions are not substitutions).
usage: python3 -I check_copper.py REPO DATA_DIR OUT.json
"""
import sys, csv, re, json, math
REPO, DD, OUT = sys.argv[1:4]
FIN = str.maketrans('ךםןףץ', 'כמנפצ'); HEB = 'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
key = lambda a, b: tuple(sorted((a, b)))
PV = {key(r['letter_1'], r['letter_2']): float(r['p']) for r in csv.DictReader(open(f'{DD}/vorlage_confusion_matrix.csv', encoding='utf-8'))}
PE = {key(r['letter_1'], r['letter_2']): float(r['rate']) for r in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/confusions.csv', encoding='utf-8'))}
seen = {}
for x in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/variants.csv', encoding='utf-8')):
    for ed, rd in ((x['edition_a'], x['reading_a']), (x['edition_b'], x['reading_b'])):
        if 'Puech 2015' not in ed: continue
        for m in re.finditer(f'([{HEB}])\\(([{HEB}])\\)', rd):
            a, b = m.group(1).translate(FIN), m.group(2).translate(FIN)
            if a == b: continue
            seen[(x['column'], x['line'], x['word_index'], a, b)] = rd
pairs = [dict(place=f'{k[0]} {k[1]} w{k[2]}', engraved=k[3], corrected=k[4], reading=v, p_V=PV[key(k[3], k[4])], p_E=PE.get(key(k[3], k[4]), 1 / 409)) for k, v in seen.items()]
n = len(pairs)
lv = [math.log2(p['p_V']) - math.log2(p['p_E']) for p in pairs]
lu = [math.log2(p['p_V']) - math.log2(1 / 231) for p in pairs]
wins = sum(1 for p in pairs if p['p_V'] > p['p_E'])
def sign_p(k, n): return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
res = dict(n_pairs=n, mean_log2_V_over_E=round(sum(lv) / n, 4), mean_log2_V_over_uniform=round(sum(lu) / n, 4),
           V_beats_E=wins, sign_test_p_one_sided=round(sign_p(wins, n), 5), pairs=pairs)
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in res.items() if k != 'pairs'}, ensure_ascii=False))
