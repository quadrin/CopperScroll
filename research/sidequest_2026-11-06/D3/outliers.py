import json,csv,re,collections,statistics
r=json.load(open('/home/claude/swarm/scratch/D3/refs_raw.json'))
meta={x['id']:x for x in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
PAT=re.compile(r'(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?\s*/\s*(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?')
def sc(v): return {4:100,5:10,6:1}.get(len(v))
def first(s):
    for part in s.split(' | '):
        m=PAT.search(part)
        if m and sc(m.group(1)) and sc(m.group(3)):
            return int(m.group(1))*sc(m.group(1)),int(m.group(3))*sc(m.group(3)),part
ref={(x['id'],x['lang']):first(x['refs']) for x in r}
groups=collections.defaultdict(list)
for rid,m in meta.items():
    g=m['group_en'].strip()
    if g in ('Jerusalem',) : continue
    groups[g].append(rid)
for g,ids in groups.items():
    pts=[]
    for rid in ids:
        for lang in ('en','he'):
            p=ref.get((rid,lang))
            if p and 100000<=p[0]<=300000 and 350000<=p[1]<=820000: pts.append((rid,lang,p))
    if len(set(x[0] for x in pts))<3: continue
    me=statistics.median(x[2][0] for x in pts); mn=statistics.median(x[2][1] for x in pts)
    for rid in ids:
        for lang in ('en','he'):
            p=ref.get((rid,lang))
            if not p: continue
            d=((p[0]-me)**2+(p[1]-mn)**2)**.5
            if d>4000:
                print(rid,lang,meta[rid]['volume'],g[:22].ljust(22),meta[rid]['title_en'][:28].ljust(28),p[2][:30].ljust(30),'med',int(me),int(mn),'d_km',round(d/1000,1))
