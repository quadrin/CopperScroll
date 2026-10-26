import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locations import classify
SN, O = sys.argv[1], sys.argv[2]; sfx = sys.argv[3] if len(sys.argv) > 3 else ''
names = json.load(open(SN))
G = {e['no']: e for e in csv.DictReader(open(f'{O}/gaz_onomasticon.csv'))}
M = {e['piggin']: e for e in csv.DictReader(open(f'{O}/gaz_madaba.csv'))}
summ = {r['name']: r for r in csv.DictReader(open(f'{O}/summary{sfx}.csv'))}
hits = list(csv.DictReader(open(f'{O}/scroll_hits{sfx}.csv')))
KNOWN_RULE = {'jericho', 'achor', 'sekakah'}
rows = []
for h in hits:
    st, note = classify(h['src'], h['gid'], h['gform'], h['set'])
    if h['src'] == 'Onom':
        e = G[h['gid']]; cite = f"Onom. Wolf no. {h['gid']}, Klostermann {e['kref'] or '?'} ({e['note_head'].split('.')[-1].strip() if e['note_head'] else ''})"
        head = e['head']
    else:
        e = M[h['gid']]; cite = f"Madaba Piggin {h['gid']} = Piccirillo {e['piccirillo']}, Avi-Yonah {e['avi_yonah']}, Donner {e['donner']}"
        head = e['ident']
    rows.append(dict(name=h['name'], variant=h['variant'], who=h['who'], scroll_skel=h['scroll_skel'], set=h['set'], kind=h['kind'],
                     gazetteer_form=h['gform'], gaz_skel=h['gskel'], entry=head, citation=cite, position_status=st, location_note=note))
with open(f'{O}/all_matches{sfx}.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
out = []
for n in names:
    rs = [r for r in rows if r['name'] == n['id']]
    def loc(sets): return [r for r in rs if r['set'] in sets and r['position_status'] == 'in']
    lg = loc({'greek'}); la = loc({'greek', 'latin', 'body'})
    placed = n['priority'] == 0 or n['id'] in KNOWN_RULE
    s = summ[n['id']]; c1 = float(s['c1_rate_primary']); c1a = float(s['c1_rate_any_set'])
    def short(L): return '; '.join(sorted({f"{r['gazetteer_form']} [{r['citation'].split(',')[0]}] ({r['kind']})" for r in L}))[:400]
    out.append(dict(name=n['id'], label=n['name'], status='placed/known' if placed else 'unplaced',
        match_greek=int(s['match_primary']), any_set_match=int(int(s['match_primary']) or int(s['match_latin_only']) or int(s['match_body'])),
        n_located_greek=len({(r['citation']) for r in lg}), n_located_any=len({(r['citation'], r['gazetteer_form']) for r in la}),
        c1_greek=c1, c1_any=c1a,
        lead_literal=int((not placed) and bool(lg) and c1 < 1), lead_strict=int((not placed) and bool(lg) and c1 <= 0.05),
        lead_literal_anyset=int((not placed) and bool(la) and c1a < 1),
        located_greek=short(lg), located_other=short([r for r in la if r not in lg])))
with open(f'{O}/per_name{sfx}.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); [w.writerow(r) for r in out]
print('UNREVIEWED rows:', sum(1 for r in rows if r['position_status'] == 'UNREVIEWED'))
for k in ['match_greek', 'any_set_match', 'lead_literal', 'lead_strict', 'lead_literal_anyset']:
    print(k, sum(r[k] for r in out))
print('names with >=1 located Greek match:', sum(1 for r in out if r['n_located_greek']), '| unplaced:', sum(1 for r in out if r['n_located_greek'] and r['status']=='unplaced'))
for r in out:
    print(f"{r['name']:9} {r['status'][:8]:8} g={r['match_greek']} any={r['any_set_match']} locG={r['n_located_greek']} locAny={r['n_located_any']} C1={r['c1_greek']:.2f}/{r['c1_any']:.2f} lead={r['lead_literal']}{r['lead_strict']}{r['lead_literal_anyset']} | {r['located_greek'][:150]}")
