import json,re,csv,collections
R=json.load(open('/home/claude/swarm/scratch/D3/refs_raw.json'))
bad=set(r['report_id'] for r in csv.DictReader(open('/home/claude/swarm/out/D3/ha_mapref_errors.csv')))
PAT=re.compile(r'(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?\s*/\s*(\d{3,7})')
def sc(v):
    return {3:1000,4:100,5:10,6:1,7:1}.get(len(v))
def conv(r):
    m=PAT.search(r)
    if not m: return None
    e,n=m.group(1),m.group(3)
    E=int(e)*sc(e) if sc(e) else None; N=int(n)*sc(n) if sc(n) else None
    if E is None or N is None: return None
    # OIG -> NIG
    if 50000<=E<=230000 and N<350000 and not (120000<=E<=280000 and 380000<=N<=800000):
        E+=50000; N+=500000
    elif N>=900000 and N<1200000 and E<230000:   # old grid south (+1e6)
        E+=50000; N=N-1000000+500000
    if 120000<=E<=290000 and 360000<=N<=800000: return E,N
    return None
out={}
for r in R:
    rid=r['id']
    if rid in bad: continue
    for ref in r['refs'].split(' | '):
        if not ref: continue
        c=conv(ref)
        if c:
            out.setdefault(rid,{}).setdefault(r['lang'],c); break
res={}
dis=0
for rid,d in out.items():
    en,he=d.get('en'),d.get('he')
    if en and he and (abs(en[0]-he[0])>2000 or abs(en[1]-he[1])>2000): dis+=1; continue
    res[rid]=he or en
print(len(R)//2,len(res),'disagree',dis)
json.dump(res,open('/home/claude/swarm/scratch/E2/ha_itm.json','w'))
