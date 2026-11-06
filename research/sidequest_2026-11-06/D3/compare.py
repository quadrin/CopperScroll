import json,re,csv,collections
r=json.load(open('/home/claude/swarm/scratch/D3/refs_raw.json'))
meta={x['id']:x for x in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
PAT=re.compile(r'(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?\s*/\s*(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?')
def scale(v):
    n=len(v);x=int(v);return {3:x*1000,4:x*100,5:x*10,6:x,7:None}.get(n)
def parse(s):
    out=[]
    for part in s.split(' | '):
        m=PAT.search(part)
        if not m: continue
        e,n=scale(m.group(1)),scale(m.group(3))
        if e is None or n is None: continue
        ok = 100000<=e<=300000 and 350000<=n<=820000
        out.append(dict(raw=part,e=e,n=n,ok=ok))
    return out
by=collections.defaultdict(dict)
for x in r: by[x['id']][x['lang']]=parse(x['refs'])
res=[]
for rid,d in by.items():
    en=[p for p in d.get('en',[]) if p['ok']]; he=[p for p in d.get('he',[]) if p['ok']]
    allen=d.get('en',[]); allhe=d.get('he',[])
    if not en or not he:
        # flag implausible-only
        if (allen and not en) or (allhe and not he):
            res.append(dict(id=rid,kind='implausible',en=' ; '.join(p['raw'] for p in allen),he=' ; '.join(p['raw'] for p in allhe),de='',dn=''))
        continue
    a,b=en[0],he[0]
    de,dn=a['e']-b['e'],a['n']-b['n']
    if abs(de)>50 or abs(dn)>50:
        res.append(dict(id=rid,kind='en_he_diff',en=a['raw'],he=b['raw'],de=de,dn=dn))
w=csv.DictWriter(open('/home/claude/swarm/scratch/D3/en_he_diff.csv','w'),fieldnames=['id','vol','site','kind','en','he','de','dn'])
w.writeheader()
for x in res:
    m=meta.get(x['id'],{});x['vol']=m.get('volume');x['site']=m.get('title_en');w.writerow(x)
print(collections.Counter(x['kind'] for x in res))
