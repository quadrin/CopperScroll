import sys,json,math; sys.path.insert(0,sys.argv[1])
from net import Grid
import numpy as np
R=sys.argv[2]
g=Grid(R+'/data/jer.npz')
osm=json.load(open(R+'/data/osm_feats.json'))
jordan=[p for k,v in osm.items() if v['tags'].get('waterway')=='river' and 'Jordan' in v['tags'].get('name:en','') for p in (v['pts'] or [])]
print('jordan pts',len(jordan))
J=np.array(jordan)
def near_jordan(cell,lim=150):
    la,lo=g.px2ll(*cell)
    d=np.hypot((J[:,0]-la)*111195,(J[:,1]-lo)*111195*math.cos(math.radians(la))).min()
    return d<lim
def trace(name,lat,lon):
    c,_=g.snap(lat,lon,1.0)
    p=g.down(c,stop=near_jordan)
    print(name,'cells',len(p),'length %.0f m'%g.length(p),'end',[round(v,5) for v in g.px2ll(*p[-1])],'elev',round(g.dem[p[-1]]))
    acc=0
    for i,(a,b) in enumerate(zip(p,p[1:])):
        acc+=math.hypot(a[0]-b[0],a[1]-b[1])*g.res
        if i%60==0: print('   %5.0f m'%acc,[round(v,5) for v in g.px2ll(*b)],'A=%.1f'%g.area[b],'z=%.0f'%g.dem[b])
    return p
out={}
out['nuw']=trace('Nuweimeh from Ain Duk',31.89585,35.42174)
out['auj']=trace('Aujah from spring',31.95541,35.38713)
out['qelt_up']=trace('Qelt from 35.40 canyon',31.8466,35.405)
json.dump({k:v for k,v in out.items()},open(R+'/data/stems_raw.json','w'))
