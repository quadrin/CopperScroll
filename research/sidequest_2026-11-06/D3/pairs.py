import json,csv,re,collections
r=json.load(open('/home/claude/swarm/scratch/D3/refs_raw.json'))
meta={x['id']:x for x in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
PAT=re.compile(r'(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?\s*/\s*(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?')
def sc(v): return {4:100,5:10,6:1}.get(len(v))
out=[]
for x in r:
    parts=[p for p in x['refs'].split(' | ') if p]
    vals=[]
    for p in parts:
        m=PAT.search(p)
        if m and sc(m.group(1)) and sc(m.group(3)):
            vals.append((int(m.group(1))*sc(m.group(1)),int(m.group(3))*sc(m.group(3)),p))
    # consecutive pairs: NIG then OIG
    for a,b in zip(vals,vals[1:]):
        de,dn=a[0]-b[0],a[1]-b[1]
        # candidate NIG/OIG pair if approx 50000 in E or 500000 in N
        if abs(abs(de)-50000)<3000 or abs(abs(dn)-500000)<30000 or (100000<a[0]<300000 and 550000<a[1]<820000 and 50000<b[0]<250000 and b[1]<350000):
            if not (de==50000 and dn==500000):
                out.append(dict(id=x['id'],lang=x['lang'],vol=meta[x['id']]['volume'],site=meta[x['id']]['title_en'],nig=a[2],oig=b[2],dE=de-50000,dN=dn-500000))
for o in out: print(o['id'],o['lang'],o['vol'],o['site'][:30].ljust(30),o['nig'][:28].ljust(28),'|',o['oig'][:28].ljust(28),o['dE'],o['dN'])
print(len(out))
