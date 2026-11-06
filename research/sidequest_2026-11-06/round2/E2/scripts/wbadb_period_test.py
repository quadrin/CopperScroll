import sys,csv,re,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import nearest,M,cert
from pyproj import Transformer
tr=Transformer.from_crs(28191,2039,always_xy=True)
rows=list(csv.DictReader(open('/home/claude/swarm/scratch/B2/wbadb_sites.csv')))
P=[];
typ=np.array([M[k]['type'] for k in range(len(M))])
for r in rows:
    try: x=float(r['oig_x']);y=float(r['oig_y'])
    except: continue
    if not(100000<x<300000 and 0<y<300000): continue
    per=(r['major_periods']+','+r['other_periods'])
    rom = bool(re.search(r'\bRom|\bByz|\bHel',per))
    nonrom = (per.strip(', ')!='') and not rom
    if not (rom or nonrom): continue
    E,N=tr.transform(x,y); p=np.array([E,N])
    dc,_=nearest(p,cert=='Certain'); dj,_=nearest(p,cert=='Conjectured'); dh,_=nearest(p,cert=='Hypothetical'); da,_=nearest(p)
    P.append((E,N,int(rom),dc,dj,dh,da,r['wb_id'],r['zone']))
A=np.array([p[:7] for p in P],float)
np.save('/home/claude/swarm/scratch/E2r2/wbadb_period.npy',A)
print('n',len(A),'rom',int(A[:,2].sum()),'nonrom',int((A[:,2]==0).sum()))
from scipy.spatial import cKDTree
T=cKDTree(A[:,:2]); rng=np.random.default_rng(0)
for j,lab in [(3,'Certain'),(4,'Conjectured'),(5,'Hypothetical'),(6,'any')]:
    for R in (5000,10000):
        pct=[]
        for i in np.where(A[:,2]==1)[0]:
            nb=[k for k in T.query_ball_point(A[i,:2],R) if A[k,2]==0]
            if len(nb)<5: continue
            d=A[nb,j]; pct.append(((d<A[i,j]).sum()+0.5*(d==A[i,j]).sum())/len(d))
        pct=np.array(pct); bs=[rng.choice(pct,len(pct)).mean() for _ in range(1000)]
        print(lab,R,'n',len(pct),'mean pct %.3f'%pct.mean(),'CI %.3f-%.3f'%tuple(np.percentile(bs,[2.5,97.5])),'| med d rom %.0f nonrom %.0f'%(np.median(A[A[:,2]==1,j]),np.median(A[A[:,2]==0,j])))
