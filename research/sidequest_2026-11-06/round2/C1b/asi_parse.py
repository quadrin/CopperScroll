import json,re,csv,sys,html
rows=[]
for mid,mnum in [(68,'109/4'),(78,'109/5'),(62,'109/7')]:
    try: d=json.load(open(f'/home/claude/swarm/scratch/D2/asi/GetPolygonsSites_Eng__MapId-{mid}.json'))['d']
    except Exception as e: print('miss',mid,e,file=sys.stderr); continue
    for f in d['features']:
        p={x['key']:x['value'] for x in f['properties']}
        lon,lat=f['geometry']['coordinates'][:2]
        desc=re.sub('<[^>]+>',' ',html.unescape(p.get('description_heb') or ''))
        desc=re.sub(r'\s+',' ',desc).strip()
        name=re.sub('<[^>]+>','',html.unescape(p.get('name_heb') or '')).strip()
        rows.append(dict(map=mnum,site=p['site_num'],db_id=p['id'],name=name,lat=lat,lon=lon,desc=desc))
w=csv.DictWriter(open('asi_109_4_5_7.csv','w'),fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
print(len(rows))
