import re,glob,csv,json,collections
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
P=re.compile(r'\b([ABGSCLKX])[-–‐ ]?(\d{2,5}(?:/\d{2,4})?)\b')
own={}
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    m=re.search(r'Permit',t)
    if not m: own[rid]=[];continue
    seg=t[m.start():m.start()+120]
    seg=seg.split(';')[0].split('map')[0].split(')')[0]
    own[rid]=sorted(set(a+'-'+b for a,b in P.findall(seg)))
inv=collections.defaultdict(list)
for rid,ps in own.items():
    for p in ps: inv[p].append(rid)
rows=[]
for p,ids in inv.items():
    if len(ids)>1:
        rows.append((p,[(i,meta.get(i,{}).get('volume'),meta.get(i,{}).get('date'),meta.get(i,{}).get('title_en'),meta.get(i,{}).get('type_en')) for i in sorted(ids,key=int)]))
json.dump({'own':own},open('/home/claude/swarm/scratch/B1b/own_permits.json','w'))
print(len(own),sum(1 for v in own.values() if v),len(inv),len(rows))
for p,l in sorted(rows,key=lambda x:x[0]):
    print(p,' || '.join(f"{i}/v{v}/{d}/{t}/{ty}" for i,v,d,t,ty in l))
