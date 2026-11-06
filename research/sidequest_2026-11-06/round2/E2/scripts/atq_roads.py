import glob,re,sys,csv,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import nearest,M,cert
from pyproj import Transformer
O2N=Transformer.from_crs(28191,2039,always_xy=True)
base='/home/claude/swarm/scratch/E2r2/atq/text/'
ROAD=re.compile(r'roman road|paved road|ancient road|road segment|section of (?:a|the) road|milestone|imperial road|roadbed|road bed|via\b',re.I)
MR=re.compile(r'map\s*ref(?:erence)?s?\.?\s*(?:\((?:NIG|OIG|New Israel Grid|Old Israel Grid)\)\s*)?(?:NIG|OIG)?\s*:?\s*(\d{4,6})\s*(?:[–\-]\s*\d{1,6})?\s*/\s*(\d{4,6})',re.I)
def sc(v): return {4:100,5:10,6:1}[len(v)]
rows=[]
for f in sorted(glob.glob(base+'vol-*/*/*.txt')):
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    hits=ROAD.findall(t)
    if len(hits)<3: continue
    m=MR.search(t)
    if not m: rows.append(dict(file=f[len(base):],nroad=len(hits),ref='',E='',N='',d='',road='',cert='',terms=';'.join(sorted(set(h.lower() for h in hits))))); continue
    e,n=m.group(1),m.group(2); E=int(e)*sc(e); N=int(n)*sc(n)
    if N<350000: # OIG
        E,N=O2N.transform(E,N) if E>100000 else (E+50000,N+500000)
    elif N>=1000000: N-=500000
    if not(120000<E<290000 and 360000<N<800000): continue
    d,k=nearest(np.array([E,N],float))
    rows.append(dict(file=f[len(base):],nroad=len(hits),ref=m.group(0)[-30:],E=round(E),N=round(N),d=round(d),road=M[k]['name'],cert=M[k]['cert'],terms=';'.join(sorted(set(h.lower() for h in hits)))))
w=csv.DictWriter(open('/home/claude/swarm/scratch/E2r2/atq_roads.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows))
for r in sorted(rows,key=lambda r:-(r['d'] or 0)):
    if r['d']!='' and r['d']>1500: print(r['d'],r['nroad'],r['file'][:85],r['road'][:28],r['cert'],'|',r['terms'][:80])
