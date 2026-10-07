import json, sys, csv, re
files = sys.argv[1:-1]; out = sys.argv[-1]
rows = {}
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for doc in d['response']['docs']:
        v = doc.get('view', [])
        sig = next((x for x in v if x.startswith('BS Pal., BayHStA')), '')
        url = next((x for x in v if x.startswith('https://www.gda.bayern.de/show/')), '')
        date = next((x for x in v if re.search(r'\b1[89]\d\d\b', x) and not x.startswith('BS') and not x.startswith('Bildsammlung')), '')
        ctx = doc.get('apd_context', '')
        if isinstance(ctx, list): ctx = ' | '.join(ctx)
        rows[doc['id']] = dict(ddb_id=doc['id'], signature=sig.replace('BS Pal., BayHStA, ',''), title=' / '.join(doc.get('label', [])), date=date, context=ctx.replace('Bildsammlung Palästina >> Bildsammlung Palästina >> ',''), gda_viewer=url, ddb_item='https://www.deutsche-digitale-bibliothek.de/item/'+doc['id'])
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(next(iter(rows.values())).keys()))
    w.writeheader()
    for r in sorted(rows.values(), key=lambda r: r['signature']):
        w.writerow(r)
print(len(rows))
