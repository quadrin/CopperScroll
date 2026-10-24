import csv
from collections import Counter
P = {p['place_id']: p['model_region'] for p in csv.DictReader(open('/home/claude/quadrin/copperscroll/research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv'))}
P1P = {'tell_es_sultan','ein_samiya','kh_yanun','muhalhil','beit_kahil','kuhlah','carmel_siah','mount_zion','ein_ghuweir','ein_feshkha','iv17_abu_saraj','buqeia','gerizim','jer_siloam'}
P2P = {'mar_saba','hyrcania','natuf','tekoa_herodium','jordan_ford','beth_shean','ibziq','beth_horon','kh_salhab'}
P1G = {'JERICHO_ALL','QUMRAN_ALL','buqeia','gerizim','ein_samiya','kh_yanun','beit_kahil','kuhlah','carmel_siah','R_JD_CLIFFS','R_WADI_QELT'}
P2G = {'mar_saba','hyrcania','natuf','tekoa_herodium','beth_shean','ibziq','beth_horon','kh_salhab'}
def tier(r):
    t = []
    w2 = [x for x in r['within_2km'].split(';') if x]; w5 = [x for x in r['within_5km'].split(';') if x]
    regs = [x for x in r['regions'].split(';') if x]; tg = [x for x in r['title_groups'].split(';') if x]
    located = r['n_refs'] != '0'
    for p in w5:
        jer = P.get(p) == 'JER'
        if p in P1P or P.get(p) in ('JERICHO', 'QUMRAN'): t.append(1 if (not jer or p in w2) else 4)
        elif p in P2P: t.append(2)
        elif jer: t.append(3 if p in w2 else 4)
        else: t.append(2)
    for g in regs:
        t.append(1 if g in ('R_JERICHO_OASIS','R_QUMRAN_FESHKHA','R_BUQEIA','R_GERIZIM_NABLUS','R_WADI_QELT','R_JD_CLIFFS') else 2)
    if not located:  # name only: counts at the named place
        for g in tg:
            t.append(1 if g in P1G else (2 if g in P2G else 3))
    return min(t) if t else None
rows = list(csv.DictReader(open('online_candidates.csv')))
for r in rows: r['tier'] = tier(r)
keep = [r for r in rows if r['tier']]
drop = [r for r in rows if not r['tier']]
print('kept', len(keep), 'dropped (title match, map ref beyond 5 km)', len(drop))
c = Counter(r['tier'] for r in keep); print(sorted(c.items()))
words = Counter(); 
for r in keep: words[r['tier']] += int(r['en_words'] or 0)
print('words per tier', sorted(words.items()), 'total', sum(words.values()))
f = list(rows[0].keys())
with open('online_candidates_tiered.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=f, lineterminator='\n'); w.writeheader(); w.writerows(sorted(keep, key=lambda r: (r['tier'], int(r['volume']), int(r['id']))))
# P1 by place
pc = Counter()
for r in keep:
    if r['tier'] == 1:
        for p in (r['within_2km'] or r['within_5km'] or r['title_groups'] or r['regions']).split(';'): pc[p] += 1
print(pc.most_common(30))
