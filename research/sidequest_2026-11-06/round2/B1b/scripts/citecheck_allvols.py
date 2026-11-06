import re,glob,csv,json,unicodedata
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
own=json.load(open('/home/claude/swarm/scratch/B1b/own_permits.json'))['own']
owner={}
for k,v in own.items():
    for p in v: owner.setdefault(p,[]).append(k)
def toks(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\b([a-z]) (?=[a-z]\b)',r'\1',s)  # crude join of split letters
    return {w for w in re.findall(r'[a-z]{4,}',s.replace(' ','') if False else s) if w not in {'horbat','khirbat','tel','tell','street','north','south','east','west','survey','area','areas','the','nahal','jerusalem','city','old'}}
P=re.compile(r'Permit No[s]?\.? ?((?:[A-Z]-? ?\d{3,5}(?:/\d+)?[,; and]*)+)')
out=[]
import sys
for v in list(range(116,123))+list(range(130,138)):
  for f in glob.glob(f'/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-{v}/*.txt'):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    for m in P.finditer(t):
        for a,b in re.findall(r'([A-Z])-? ?(\d{3,5})',m.group(1)):
            p=f'{a}-{b}'
            if p in own.get(rid,[]): continue
            for o in owner.get(p,[]):
                if o==rid: continue
                ctx=t[max(0,m.start()-250):m.start()]
                ot=toks(meta[o]['title_en']+' '+meta[o]['group_en']); ct=toks(ctx); st=toks(meta[rid]['title_en'])
                # flag if owner's distinctive tokens absent from context and from citing title
                if ot and not (ot & ct) and not (ot & st):
                    out.append((rid,v,meta[rid]['title_en'],p,o,meta[o]['volume'],meta[o]['title_en'],ctx[-160:]))
for x in out: print(*x,sep=' | ')
print(len(out))
