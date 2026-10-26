import csv, sys
O = sys.argv[1]; sfx = sys.argv[2] if len(sys.argv) > 2 else ''
G = {e['no']: e for e in csv.DictReader(open(f'{O}/gaz_onomasticon.csv'))}
M = {e['piggin']: e for e in csv.DictReader(open(f'{O}/gaz_madaba.csv'))}
h = list(csv.DictReader(open(f'{O}/scroll_hits{sfx}.csv')))
seen = {}
for r in h: seen.setdefault((r['name'], r['src'], r['gid']), []).append(r)
rows = []
for k, rs in seen.items():
    vs = sorted({f"{r['variant']}:{r['scroll_skel']}~{r['gform']}:{r['gskel']}({r['kind']},{r['set']})" for r in rs})
    sets = sorted({r['set'] for r in rs}); kinds = sorted({r['kind'] for r in rs})
    if k[1] == 'Onom':
        e = G[k[2]]; rows.append(dict(name=k[0], src='Onom', id=k[2], head=e['head'], kref=e['kref'], section=e['section'], sets='+'.join(sets), kinds='+'.join(kinds), match=' ; '.join(vs), text=e['text']))
    else:
        e = M[k[2]]; rows.append(dict(name=k[0], src='Madaba', id=k[2], head=e['ident'], kref=f"Piccirillo {e['piccirillo']}; Avi-Yonah {e['avi_yonah']}; Donner {e['donner']}", section='', sets='+'.join(sets), kinds='+'.join(kinds), match=' ; '.join(vs), text=e['greek'] + ' || ' + e['translation']))
with open(f'{O}/hits_unique{sfx}.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
print(len(rows))
