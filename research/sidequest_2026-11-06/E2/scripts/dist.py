import numpy as np,json,csv,pandas as pd
from pyproj import Transformer
S=np.load('/home/claude/swarm/scratch/E2/roads_itm.npy',allow_pickle=True)
M=json.load(open('/home/claude/swarm/scratch/E2/roads_meta.json'))
A=[];B=[];K=[]
for i,s in enumerate(S):
    s=np.asarray(s,float); A.append(s[:-1]); B.append(s[1:]); K+= [i]*(len(s)-1)
A=np.vstack(A);B=np.vstack(B);K=np.array(K)
D=B-A; L2=(D**2).sum(1); L2[L2==0]=1e-9
def nearest(p,mask=None):
    a,d,l2,k=(A,D,L2,K) if mask is None else (A[mask],D[mask],L2[mask],K[mask])
    t=np.clip(((p-a)*d).sum(1)/l2,0,1); q=a+t[:,None]*d
    dd=np.hypot(*(p-q).T); j=dd.argmin(); return dd[j],k[j]
cert=np.array([M[k]['cert'] for k in K]); typ=np.array([M[k]['type'] for k in K])
masks={'all':None,'certain':cert=='Certain','main':typ=='Main Road'}
# HA sites
ha=json.load(open('/home/claude/swarm/scratch/E2/ha_itm.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
rows=[]
for rid,(e,n) in ha.items():
    p=np.array([e,n],float); r=dict(src='HA',report_id=rid,E=e,N=n,title=meta.get(rid,{}).get('title_en',''),volume=meta.get(rid,{}).get('volume',''))
    for nm,m in masks.items():
        d,k=nearest(p,m); r['d_'+nm]=round(d); 
        if nm=='all': r['road_fid']=M[k]['fid']; r['road_name']=M[k]['name']; r['road_cert']=M[k]['cert']
    rows.append(r)
# CHRE / project catalogue
tr=Transformer.from_crs(4326,2039,always_xy=True)
h=pd.read_csv('/home/claude/copperscroll/research/comparanda/hoards_full/hoards.csv')
for _,x in h.iterrows():
    if pd.isna(x.lat): continue
    e,n=tr.transform(x.lon,x.lat); p=np.array([e,n])
    r=dict(src='CAT',report_id=x['id'],E=round(e),N=round(n),title=x.site,volume='',cat_from=x.date_from,cat_to=x.date_to,how_found=x.how_found,include=x.include,object_class=x.object_class,country=x.country)
    for nm,m in masks.items():
        d,k=nearest(p,m); r['d_'+nm]=round(d)
        if nm=='all': r['road_fid']=M[k]['fid']; r['road_name']=M[k]['name']; r['road_cert']=M[k]['cert']
    rows.append(r)
pd.DataFrame(rows).to_csv('/home/claude/swarm/scratch/E2/all_dist.csv',index=False)
print(len(rows))
