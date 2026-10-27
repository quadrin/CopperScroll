import sys,json,math; sys.path.insert(0,sys.argv[1]); R=sys.argv[2]
import numpy as np
from net import Grid
F=json.load(open(R+'/data/features.json'))
g=Grid(R+'/data/jer.npz'); M=np.load(R+'/data/masks_jer.npz')
gb=Grid(R+'/data/buq.npz')
# Buqeia network: channels >=0.25 km2 inside convex hull of Patrich 'Hyrcania Valley' sites + forts 35, 91, 101
sites=json.load(open(R.rsplit('/',1)[0]+'/ms/sites.json'))
pts=[(x['lat'],x['lon']) for x in sites if 'Hyrcania Valley' in x['text'][:200] or x['n'] in (35,91,101)]
def hull(P):
    P=sorted(set(P))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
Hh=hull(pts)
from matplotlib.path import Path
poly=Path([(lo,la) for la,lo in Hh])
rr,cc=np.nonzero(gb.area>=0.25)
ll=np.array([gb.px2ll(r,c) for r,c in zip(rr,cc)])
inside=poly.contains_points(ll[:,::-1])
bmask=np.zeros(gb.area.shape,bool); bmask[rr[inside],cc[inside]]=True
np.save(R+'/data/buq_net.npy',bmask)
json.dump(Hh,open(R+'/data/buq_hull.json','w'))
print('Buqeia hull vertices',len(Hh),'network cells',int(bmask.sum()),'~%.1f km'%(bmask.sum()*gb.res/1000))
out=[]
for f in F:
    if f['lat'] is None: out.append(dict(f,stem_m=None,net_m=None)); continue
    if f['v']=='buq':
        d,_=gb.dist_to(bmask,f['lat'],f['lon']); ds=None
        ins=bool(poly.contains_point((f['lon'],f['lat'])))
        out.append(dict(f,stem_m=None,net_m=round(d) if d is not None else None,in_hull=ins))
    else:
        ds,_=g.dist_to(M[f['v']+'_stem'],f['lat'],f['lon'],6000); dn,_=g.dist_to(M[f['v']+'_net'],f['lat'],f['lon'],6000)
        out.append(dict(f,stem_m=round(ds) if ds is not None else None,net_m=round(dn) if dn is not None else None))
for o in out: print(o['v'],o['id'],'stem',o['stem_m'],'net',o['net_m'],o.get('in_hull',''),'|',o['name'][:70])
json.dump(out,open(R+'/out/feature_distances.json','w'),indent=1,ensure_ascii=False)
