import sys,json,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import S,M
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
from pyproj import Transformer
R=np.load('/home/claude/swarm/scratch/E2r2/tir_red_itm.npy'); xy=R[:,:2]
# densify itinere
D=[];K=[]
for i,s in enumerate(S):
    s=np.asarray(s,float)
    for a,b in zip(s[:-1],s[1:]):
        n=max(1,int(np.hypot(*(b-a))//50)); t=np.linspace(0,1,n+1)[:,None]; D.append(a+t*(b-a)); K+=[i]*(n+1)
D=np.vstack(D);K=np.array(K)
TI=cKDTree(D); d,j=TI.query(xy)
bb=(xy[:,0].min(),xy[:,0].max(),xy[:,1].min(),xy[:,1].max())
print('red blocks',len(xy),'within 300 m %.3f 1 km %.3f 2 km %.3f'%((d<300).mean(),(d<1000).mean(),(d<2000).mean()))
far=d>2000; F=xy[far]
TF=cKDTree(F); pairs=TF.query_pairs(150,output_type='ndarray')
A=coo_matrix((np.ones(len(pairs)),(pairs[:,0],pairs[:,1])),shape=(len(F),len(F)))
nc,lab=connected_components(A,directed=False)
I2L=Transformer.from_crs(2039,4326,always_xy=True); O=Transformer.from_crs(2039,28191,always_xy=True)
out=[]
for c in range(nc):
    m=lab==c
    if m.sum()<40: continue   # <~40 blocks = <~0.6 km of line
    p=F[m]; ext=np.hypot(*(p.max(0)-p.min(0)))
    cx,cy=p.mean(0); dd=d[far][m]
    lon,lat=I2L.transform(cx,cy); oe,on=O.transform(cx,cy)
    out.append(dict(cluster=c,n_blocks=int(m.sum()),extent_km=round(ext/1000,1),E_itm=round(cx),N_itm=round(cy),oig=f'{oe/1000:.1f}/{on/1000:.1f}',lat=round(lat,4),lon=round(lon,4),median_d_km=round(float(np.median(dd))/1000,1),max_d_km=round(float(dd.max())/1000,1),px=f'{int(R[far][m][:,2].mean())},{int(R[far][m][:,3].mean())}'))
out.sort(key=lambda r:-r['n_blocks'])
json.dump(out,open('/home/claude/swarm/scratch/E2r2/tir_far_clusters.json','w'),indent=0)
for r in out[:45]: print(r)
# reverse: itinere densified points inside TIR north map area with no red within 1.5 km
TR=cKDTree(xy); inside=(D[:,0]>bb[0])&(D[:,0]<bb[1])&(D[:,1]>bb[2])&(D[:,1]<bb[3])
dr,_=TR.query(D[inside]); Ki=K[inside]
import collections
c=collections.defaultdict(lambda:[0,0])
for k,v in zip(Ki,dr): c[k][0]+=1; c[k][1]+= v>1500
rev=[(M[k]['fid'],M[k]['name'],M[k]['cert'],round(n*0.05,1),round(f*0.05,1)) for k,(n,f) in c.items() if f*0.05>=3]
rev.sort(key=lambda r:-r[4])
print('ITINERE lines with >=3 km farther than 1.5 km from any TIR red:')
for r in rev: print(r)
json.dump(rev,open('/home/claude/swarm/scratch/E2r2/itinere_not_on_tir.json','w'))
