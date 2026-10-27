import json,re,html,sys
out=[]
for fn in sys.argv[1:-1]:
    d=json.load(open(fn))['d']; g=json.loads(d) if isinstance(d,str) else d
    for x in g['features']:
        p={k['key']:k['value'] for k in x['properties']}
        lo,la=x['geometry']['coordinates'][:2]
        desc=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html.unescape(p.get('description_heb') or '')))
        out.append({'map':fn.split('_')[0],'site':p.get('site_num'),'id':p.get('id'),'name':(p.get('name_heb') or '').strip(),'lat':la,'lon':lo,'desc':desc,'bib':re.sub(r'<[^>]+>','',html.unescape(p.get('bibliography_heb') or ''))})
json.dump(out,open(sys.argv[-1],'w'),indent=0,ensure_ascii=False)
print(len(out))
