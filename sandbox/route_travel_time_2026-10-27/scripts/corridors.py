# EXPLORATORY: 1-hour detour corridors between consecutive primary anchors (not triggered by the rule).
# usage: build_costs.py <agg factor: 1=30m, 3=90m> <nbhd: 8|16> <out.npz>
import sys,csv,json,numpy as np,time
sys.path.insert(0,sys.argv[0].rsplit('/',1)[0])
from read_cop import read
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
R='/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/route_travel_time_2026-10-27'
agg=int(sys.argv[1]); nb=int(sys.argv[2]); outp=sys.argv[3]
S,N,W,E=31.60,32.58,35.15,35.62
a31,g=read(f'{R}/dl/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif')
a32,_=read(f'{R}/dl/Copernicus_DSM_COG_10_N32_00_E035_00_DEM.tif')
full=np.vstack([a32,a31])  # rows: lat 33 -> 31
d=1/3600.
r0=int(round((33-N)/d)); r1=int(round((33-S)/d)); c0=int(round((W-35)/d)); c1=int(round((E-35)/d))
dem=full[r0:r1,c0:c1].astype(np.float64); del full,a31,a32
assert dem.min()>-1000, dem.min()
if agg>1:
    h=(dem.shape[0]//agg)*agg; w=(dem.shape[1]//agg)*agg
    dem=dem[:h,:w].reshape(h//agg,agg,w//agg,agg).mean(axis=(1,3))
H,Wd=dem.shape; step=d*agg
lat=N-(np.arange(H)+0.5)*step; lon=W+(np.arange(Wd)+0.5)*step
dy=step*111320.0; dxr=step*111320.0*np.cos(np.radians(lat))  # metres
print('grid',H,Wd,H*Wd,'cell m',dy,dxr.mean(),flush=True)
offs=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
if nb==16: offs+= [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
idx=np.arange(H*Wd,dtype=np.int32).reshape(H,Wd)
rows=[];cols=[];vals=[]
for (oy,ox) in offs:
    ys=slice(max(0,-oy),H-max(0,oy)); xs=slice(max(0,-ox),Wd-max(0,ox))
    yt=slice(max(0,oy),H-max(0,-oy)); xt=slice(max(0,ox),Wd-max(0,-ox))
    src=idx[ys,xs]; dst=idx[yt,xt]
    dh=dem[yt,xt]-dem[ys,xs]
    latr=lat[ys][:,None]
    hx=ox*step*111320.0*np.cos(np.radians(latr)); hy=oy*dy
    dist=np.sqrt(hx**2+hy**2)  # m, broadcast
    dist=np.broadcast_to(dist,dh.shape)
    Sl=dh/dist
    v=6.0*np.exp(-3.5*np.abs(Sl+0.05))  # km/h, Tobler on-path
    t=(dist/1000.0)/v                    # hours
    rows.append(src.ravel()); cols.append(dst.ravel()); vals.append(t.ravel().astype(np.float32))
    print('off',oy,ox,flush=True)
rows=np.concatenate(rows); cols=np.concatenate(cols); vals=np.concatenate(vals)
G=csr_matrix((vals,(rows,cols)),shape=(H*Wd,H*Wd)); del rows,cols,vals
print('edges',G.nnz,flush=True)

pl={r['place_id']:r for r in csv.DictReader(open('/home/claude/copperscroll/research/measurements/sequence/places.csv',encoding='utf-8'))}
def node(p):
    la,lo=float(pl[p]['lat']),float(pl[p]['lon']); return idx[int((N-la)/step),int((lo-W)/step)]
pairs=[('10','jer_east_gate','35','mar_saba','11-34'),('35','mar_saba','49','jer_siloam','36-48'),('49','jer_siloam','51','jer_se_corner','50'),('51','jer_se_corner','57','gerizim','52-56')]
GT=G.T.tocsr()
res={}; masks={}
for ea,pa,eb,pb,between in pairs:
    a,b=node(pa),node(pb)
    fa=dijkstra(G,directed=True,indices=[a])[0]; tb=dijkstra(GT,directed=True,indices=[b])[0]
    base=fa[b]; det=(fa+tb-base).reshape(H,Wd)
    m=det<=1.0; masks[f'{ea}-{eb}']=m
    cellkm2=(dy*dxr[:,None]/1e6)*np.ones((1,Wd))
    inside={}
    for p,r in pl.items():
        if not r['lat']: continue
        la,lo=float(r['lat']),float(r['lon'])
        if not (S<la<N and W<lo<E): continue
        i=int((N-la)/step); j=int((lo-W)/step); inside[p]=round(float(det[i,j]),2)
    res[f'{ea}-{eb}']={'from':pa,'to':pb,'entries_between':between,'base_h':round(float(base),2),'corridor_km2':round(float(cellkm2[m].sum()),1),'detour_h_by_place':dict(sorted(inside.items(),key=lambda kv:kv[1]))}
    print(ea,eb,res[f'{ea}-{eb}']['base_h'],res[f'{ea}-{eb}']['corridor_km2'],flush=True)
json.dump(res,open(outp,'w'),indent=1,ensure_ascii=False)
np.savez_compressed(outp.replace('.json','_masks.npz'),lat=lat,lon=lon,**{k.replace('-','_'):v for k,v in masks.items()})
