import os,re,csv,collections,json
A='/home/claude/swarm/scratch/B1c2/atiqot/text'
T='/home/claude/swarm/scratch/R2/t/hadtext'
MON={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
arts={}
for r in csv.DictReader(open('/home/claude/swarm/scratch/B1c2/atiqot/data/articles.csv',encoding='utf-8')):
    arts[r.get('article_id') or r.get('id') or '']=r
PRE=re.compile(r'\b(?:Permit|License|Licence)s?\s*(?:Nos?\.?|Numbers?)?\s*:?\s*((?:A-?\s?\d{3,5}[\w\-/]*(?:\s*(?:,|and|&)\s*)?)+)',re.I)
def permits(s):
    out=set()
    for m in PRE.finditer(s):
        for p in re.findall(r'A-?\s?(\d{3,5})',m.group(1)): out.add(int(p))
    return out
def mapref(s):
    m=re.search(r'map\s*ref(?:erence)?s?\.?\s*(?:NIG\s*|OIG\s*)?:?\s*([\d][\d\s\-–/.,]{5,40})',s,re.I)
    if not m: return None
    nums=re.findall(r'\d{4,6}',m.group(1))
    return nums[:4] if len(nums)>=2 else None
def dates(s):
    return [(int(y),MON[mo.lower()]) for mo,y in re.findall(r'\b('+'|'.join(MON)+r')\b[^.;()]{0,30}?\b(19[5-9]\d|20[0-2]\d)\b',s,re.I)]
# HA side
ha=collections.defaultdict(list)
hainfo={}
for vol in os.listdir(f'{T}/en'):
    for fn in os.listdir(f'{T}/en/{vol}'):
        rid=fn.split('_')[0]
        t=re.sub(r'\s+',' ',open(f'{T}/en/{vol}/{fn}',encoding='utf-8',errors='ignore').read())
        op=t[:2500]
        ps=permits(op)|set(int(x) for x in re.findall(r'Images//(\d{3,5})-',t))
        hainfo[rid]=dict(vol=vol[4:],file=fn,mapref=mapref(op),dates=dates(op[:1200]),permits=sorted(ps))
        for p in ps: ha[p].append(rid)
rows=[]
for root,_,fs in os.walk(A):
    for fn in fs:
        if not fn.endswith('.txt'): continue
        t=re.sub(r'\s+',' ',open(os.path.join(root,fn),encoding='utf-8',errors='ignore').read())
        op=t
        ps=permits(op)
        if not ps: continue
        rel=os.path.relpath(os.path.join(root,fn),A)
        for p in ps:
            for rid in ha.get(p,[]):
                h=hainfo[rid]
                rows.append(dict(permit=p,atiqot=rel,ha_id=rid,ha_vol=h['vol'],ha_file=h['file'],
                  atq_mapref='/'.join(mapref(op) or []),atq_ctx=(lambda m: m.group(0) if m else '')(re.search(r'.{0,160}A-?\s?'+str(p)+r'\b.{0,160}',op)),ha_mapref='/'.join(h['mapref'] or []),
                  atq_dates=';'.join(f'{y}-{m:02d}' for y,m in dates(op[:15000])[:8]),ha_dates=';'.join(f'{y}-{m:02d}' for y,m in h['dates'][:4]),
                  n_atq_permits=len(ps),ha_permits=' '.join(map(str,h['permits']))))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1c2/ha_atiqot_join.csv','w',newline='',encoding='utf-8'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('pairs',len(rows),'atiqot articles',len(set(r['atiqot'] for r in rows)),'ha reports',len(set(r['ha_id'] for r in rows)))
