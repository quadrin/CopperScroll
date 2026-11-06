import pandas as pd,numpy as np
from scipy.stats import mannwhitneyu
from scipy.spatial import cKDTree
d=pd.read_csv('/home/claude/swarm/scratch/E2/all_dist.csv',dtype={'report_id':str})
ha=d[d.src=='HA'].copy(); cat=d[(d.src=='CAT')].copy()
H=pd.read_csv('/home/claude/swarm/scratch/E2/ha_hoards.csv')
null=ha[~ha.report_id.astype(int).isin(H.report_id)]
T=cKDTree(null[['E','N']].values)
def localpct(r,col,R=15000):
    idx=T.query_ball_point([r.E,r.N],R)
    if len(idx)<10: return np.nan
    v=null[col].values[idx]; return (np.sum(v<r[col])+0.5*np.sum(v==r[col]))/len(v)
for col in ['d_all','d_main']:
  for lab,sub in [('CAT all w/ coords',cat),('CAT include=1',cat[cat.include==1]),('CAT excavated',cat[(cat.include==1)&(cat.how_found=='excavation')]),('CAT not excavated',cat[(cat.include==1)&(cat.how_found!='excavation')]),('CAT dedup coords',cat[cat.include==1].drop_duplicates(['E','N']))]:
    lp=sub.apply(lambda r: localpct(r,col),axis=1).dropna()
    print(col,f"{lab:22s} n={len(sub):3d} median={sub[col].median()/1000:5.2f}km <=1km {np.mean(sub[col]<=1000):.2f}  local pct mean={lp.mean():.2f} n={len(lp)} (Wilcoxon vs .5: p={__import__('scipy.stats',fromlist=['x']).wilcoxon(lp-0.5).pvalue:.3f})")
# random-point null within 3 km of any HA site, inside Israel/WB box
S=np.load('/home/claude/swarm/scratch/E2/roads_itm.npy',allow_pickle=True)
rng=np.random.default_rng(42)
E0,E1,N0,N1=ha.E.min(),ha.E.max(),ha.N.min(),ha.N.max()
TT=cKDTree(ha[['E','N']].values)
pts=[]
while len(pts)<3000:
    p=np.c_[rng.uniform(E0,E1,5000),rng.uniform(N0,N1,5000)]
    dd,_=TT.query(p); pts+=list(p[dd<3000])
pts=np.array(pts[:3000])
A=[];B=[]
for s in S: s=np.asarray(s,float); A.append(s[:-1]); B.append(s[1:])
A=np.vstack(A);B=np.vstack(B);D=B-A;L2=(D**2).sum(1);L2[L2==0]=1e-9
def nd(p):
    t=np.clip(((p-A)*D).sum(1)/L2,0,1); q=A+t[:,None]*D; return np.hypot(*(p-q).T).min()
rd=np.array([nd(p) for p in pts])
print(f"random pts within 3km of an HA site: n=3000 median={np.median(rd)/1000:.2f}km <=1km {np.mean(rd<=1000):.2f} <=500m {np.mean(rd<=500):.2f}")
print(f"HA sites: median={ha.d_all.median()/1000:.2f} <=1km {np.mean(ha.d_all<=1000):.2f} <=500m {np.mean(ha.d_all<=500):.2f}")
# local version: for each HA site, random pts within 15km local percentile
np.save('/home/claude/swarm/scratch/E2/rand_d.npy',np.c_[pts,rd])
