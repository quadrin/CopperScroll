import csv, sys, re, json
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
areas = {
 'tell_es_sultan': r'Sultan|Ain es-S|Elisa|Alt-Jericho|Tell es-S|Eriha|Jericho',
 'qarantal_duk': r'Karantal|Qarantal|Kuruntul|Duk|Nu.?[ae]?ime|Nu\'eime|Auja|Audscha',
 'wadi_qelt': r'Kelt|Qelt|Chosiba|Kosiba|Georg|Der el-K|Jisr',
 'qumran': r'Kumran|Qumran|Feschcha|Feshkha|Totes Meer|Toten Meer|Nordende|Ras',
 'siloam': r'Silwan|Siloa|Siloah|Kidron|Kedron|Josaphat|Hinnom|Ophel|Jerusalem',
}
out = {}
for k, pat in areas.items():
    hits = [r for r in rows if re.search(pat, r['title']+' '+r['context'], re.I)]
    out[k] = hits
    print(f'== {k}: {len(hits)}')
    for r in hits[:400]:
        print(f"  {r['signature']:<16} {r['date'][:22]:<22} {r['title'][:150]}  || {r['context'][-70:]}")
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
