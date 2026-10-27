import sys,json,math; sys.path.insert(0,sys.argv[1]); R=sys.argv[2]
import numpy as np
from net import Grid
g=Grid(R+'/data/jer.npz')
st={k:[tuple(c) for c in v] for k,v in json.load(open(R+'/data/stems_raw.json')).items()}
def cut(stem,lon0,lon1):
    lons=[g.px2ll(*c)[1] for c in stem]
    i0=min(range(len(stem)),key=lambda i:abs(lons[i]-lon0)); i1=min(range(len(stem)),key=lambda i:abs(lons[i]-lon1))
    return stem[i0:i1+1]
reach={'nuw':st['nuw'],'auj':st['auj'],'qelt':cut(st['qelt_up'],35.4250,35.4597)}
masks={}
for k,r in reach.items():
    m=g.network(r,0.25)
    stem=np.zeros_like(m); 
    for c in r: stem[c]=True
    masks[k+'_net']=m; masks[k+'_stem']=stem
    print(k,'reach %.0f m'%g.length(r),'start',[round(v,5) for v in g.px2ll(*r[0])],'end',[round(v,5) for v in g.px2ll(*r[-1])],'network cells',int(m.sum()),'km of channel ~%.1f'%(m.sum()*g.res/1000))
np.savez_compressed(R+'/data/masks_jer.npz',**masks)
json.dump({k:[list(c) for c in v] for k,v in reach.items()},open(R+'/data/reaches_jer.json','w'))
