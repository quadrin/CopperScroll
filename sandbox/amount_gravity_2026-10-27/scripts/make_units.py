# Build the unit list for run 21 (amount vs walking time from the Temple Mount).
# Written and run BEFORE any walking time is computed.
import csv, json, sys, re
REPO = '/home/claude/copperscroll'
P = f'{REPO}/research/measurements/sequence/places.csv'
SUMS = f'{REPO}/research/first_tests_2026-10-24/method10_hoards/scroll_sums.json'
AMT = f'{REPO}/research/agent_review_2026-10-07/wave1/T08_real_or_legend/data/scroll_amounts.csv'
ANC = '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/route_travel_time_2026-10-27/out/anchors.csv'
out = sys.argv[1]

TALENT = 21.3      # kg, light talent (Lefkovits 2000 p. 473 via method 10 registration)
KARSH = 0.071      # kg, light karsh = 1/300 talent
pl = {r['place_id']: r for r in csv.DictReader(open(P, encoding='utf-8'))}

# placement set B: every entry with medium or high in entries_best_supported
B = {}
for pid, r in pl.items():
    for tok in r['entries_best_supported'].split():
        m = re.match(r'(\w+)\((\w+)\)', tok)
        if m and m.group(2) in ('medium', 'high'):
            B.setdefault(m.group(1), []).append(pid)
assert all(len(v) == 1 for v in B.values()), B
# placement set A: run 8's primary anchors (sets column contains 'P'); D1 kept as a labelled deviation
anc = list(csv.DictReader(open(ANC, encoding='utf-8')))
A = {a['entry']: a['place_id'] for a in anc if 'P' in a['sets'].split()}
D1 = {a['entry']: a['place_id'] for a in anc if 'D1' in a['sets'].split()}

sums = json.load(open(SUMS))
amts = list(csv.DictReader(open(AMT, encoding='utf-8')))

def region(pid):
    g = pl[pid]['map_group']
    if g == 'jerusalem': return 'Jerusalem'
    if g == 'jericho': return 'Jericho/Qumran'
    if pid in ('gerizim', 'beth_shean', 'ibziq'): return 'north'
    return 'other (Judaean desert)'   # Mar Saba, Natuf etc.: not named by the rule

rows = []
for e in sorted(set(B) | set(A) | set(D1), key=lambda e: (int(re.sub(r'\D', '', e)), e)):
    pid = (B.get(e) or [None])[0] or A.get(e) or D1.get(e)
    ss = [s for s in sums if s['entry'] == e]
    karsh = sum(s['value'] * (KARSH if s['unit'] == 'kk' else TALENT) for s in ss) if ss else None
    talent = sum(s['value'] * TALENT for s in ss) if ss else None
    unc = any(s['status'] != 'ok' for s in ss)
    counts = [f"{a['value']} {a['unit']} ({a['object']}; {a['status']})" for a in amts
              if a['entry'] == e and a['weight_unit'] == 'False']
    rows.append(dict(entry=e, place_id=pid, place=pl[pid]['name'], lat=pl[pid]['lat'], lon=pl[pid]['lon'],
                     region=region(pid), in_A='1' if e in A else '0', in_D1='1' if e in D1 else '0',
                     in_B='1' if e in B else '0',
                     sums='; '.join(f"{s['value']:g} {s['unit']} {s['metal']} ({s['status']})" for s in ss),
                     kg_karsh='' if karsh is None else round(karsh, 3),
                     kg_talent='' if talent is None else round(talent, 3),
                     any_uncertain='1' if unc else '0', counts=' | '.join(counts)))
w = csv.DictWriter(open(out, 'w', newline='', encoding='utf-8'), fieldnames=list(rows[0]))
w.writeheader(); [w.writerow(r) for r in rows]
for r in rows: print(r['entry'], r['place_id'], r['region'], 'A' if r['in_A'] == '1' else '-', 'B' if r['in_B'] == '1' else '-',
                     r['kg_karsh'], r['kg_talent'], r['counts'])
