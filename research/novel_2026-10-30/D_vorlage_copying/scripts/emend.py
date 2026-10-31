"""Emendation generator (frozen). One-substitution Vorlage emendations of the unplaced Copper Scroll names.

Names: research/agent_review_2026-10-07/wave1/T01_place_names/data/scroll_names.json. UNPLACED rule (run 19, match.py):
  a name is unplaced iff priority != 0 and id not in {jericho, achor, sekakah}  -> 24 names, all their variant cores.
Neighbourhood N(name): every string obtained from one variant core (final forms -> base letters) by replacing ONE letter x
  with another letter y of the 22, excluding (a) pairs with both x and y in {א, ה, ו, י} (matres lectionis / weak letters that
  both matching rules treat as vowels, so the swap makes no new consonantal name), and (b) strings equal to any variant core of
  the same name. A string reachable in several ways keeps its best weight under each model.
Weight under model M: w_M(s) = p_M({x, y}) of its substitution.
  V = Vorlage model (data/vorlage_confusion_matrix.csv, column p)
  E = modern edition-confusion model (research/text/edition_confusions/confusions.csv, column rate; pairs not listed get
      the README's floor (0+1)/(178+231) = 1/409)
Frozen set per model: top K = 10 strings per name by weight; ties broken by (variant order, position, target letter in
  alphabet order).
usage: python3 -I emend.py REPO DATA_DIR  -> DATA_DIR/neighbourhood.csv, DATA_DIR/emendations_frozen.csv
"""
import sys, os, csv, json
REPO, DD = sys.argv[1], sys.argv[2]
K = 10
LET = 'אבגדהוזחטיכלמנסעפצקרשת'
FIN = str.maketrans('ךםןףץ', 'כמנפצ')
WEAK = set('אהוי')
key = lambda a, b: tuple(sorted((a, b)))
names = json.load(open(f'{REPO}/research/agent_review_2026-10-07/wave1/T01_place_names/data/scroll_names.json', encoding='utf-8'))
PLACED = {'jericho', 'achor', 'sekakah'}
unplaced = [n for n in names if not (n['priority'] == 0 or n['id'] in PLACED)]
PV = {key(r['letter_1'], r['letter_2']): float(r['p']) for r in csv.DictReader(open(f'{DD}/vorlage_confusion_matrix.csv', encoding='utf-8'))}
PE = {key(r['letter_1'], r['letter_2']): float(r['rate']) for r in csv.DictReader(open(f'{REPO}/research/text/edition_confusions/confusions.csv', encoding='utf-8'))}
FLOOR_E = 1 / 409
rows = []
for n in unplaced:
    cores = [v['core'].translate(FIN) for v in n['variants']]
    best = {}
    for vi, core in enumerate(cores):
        for i, x in enumerate(core):
            if x not in LET: continue
            for y in LET:
                if y == x or (x in WEAK and y in WEAK): continue
                s = core[:i] + y + core[i + 1:]
                if s in cores: continue
                k = key(x, y)
                cand = dict(name_id=n['id'], name=n['name'], entries=n['entries'], variant=n['variants'][vi]['core'], variant_idx=vi,
                            position=i, written=x, emended_to=y, emendation=s, pair=f'{k[0]}–{k[1]}',
                            w_vorlage=PV[k], w_edition=PE.get(k, FLOOR_E), tiebreak=(vi, i, LET.index(y)))
                if s not in best:
                    best[s] = dict(cand, alt_paths=1)
                else:
                    b = best[s]; b['alt_paths'] += 1
                    if cand['w_vorlage'] > b['w_vorlage']:
                        for f in ('w_vorlage',): b[f] = cand[f]
                    if cand['w_edition'] > b['w_edition']: b['w_edition'] = cand['w_edition']
    lst = list(best.values())
    for model, f in (('V', 'w_vorlage'), ('E', 'w_edition')):
        lst.sort(key=lambda c: (-c[f], c['tiebreak']))
        for r_, c in enumerate(lst, 1):
            c[f'rank_{model}'] = r_
    rows += lst
for r in rows:
    r['in_V_topK'] = int(r['rank_V'] <= K); r['in_E_topK'] = int(r['rank_E'] <= K); del r['tiebreak']
cols = ['name_id', 'name', 'entries', 'emendation', 'variant', 'variant_idx', 'position', 'written', 'emended_to', 'pair', 'alt_paths',
        'w_vorlage', 'rank_V', 'in_V_topK', 'w_edition', 'rank_E', 'in_E_topK']
with open(f'{DD}/neighbourhood.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
fz = [dict(model=m, **{c: r[c] for c in cols}) for m in ('V', 'E') for r in sorted(rows, key=lambda r: (r['name_id'], r[f'rank_{m}'])) if r[f'in_{m}_topK']]
with open(f'{DD}/emendations_frozen.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['model'] + cols); w.writeheader(); w.writerows(fz)
print('unplaced names', len(unplaced), '| neighbourhood strings', len(rows), '| V set', sum(r['in_V_topK'] for r in rows),
      '| E set', sum(r['in_E_topK'] for r in rows), '| overlap', sum(r['in_V_topK'] and r['in_E_topK'] for r in rows))
