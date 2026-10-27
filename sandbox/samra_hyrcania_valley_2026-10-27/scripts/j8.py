# Along-valley distances between features on the DEM channel network (>=0.25 km2).
import sys,json; sys.path.insert(0,sys.argv[2])
from net import *
from pyproj import Transformer
T=Transformer.from_crs('EPSG:28191','EPSG:4326',always_xy=True)
def og(e,n): lo,la=T.transform(e,n); return (la,lo)
m=np.load(sys.argv[3]); masks={'model':m['M'],'controlQ':m['Q']}
outlets={'model':tuple(m['outM']),'controlQ':tuple(m['outQ'])}
F=json.load(open(sys.argv[4]))
def xy(p): return (p[1]*94650.0, p[0]*111195.0)
def path_len(cells,win=7):
    P=np.array([xy(px2ll(*p)) for p in cells])
    if len(P)<2: return 0.0,0.0
    d8=float(np.sum(np.hypot(*np.diff(P,axis=0).T)))
    if len(P)>win:
        k=np.ones(win)/win
        Sx=np.convolve(np.pad(P[:,0],(win//2,win//2),mode='edge'),k,'valid'); Sy=np.convolve(np.pad(P[:,1],(win//2,win//2),mode='edge'),k,'valid')
        sm=float(np.sum(np.hypot(np.diff(Sx),np.diff(Sy))))
    else: sm=d8
    return d8,sm
res_all={}
for vk in ('model','controlQ'):
    netm=network(masks[vk]); dist,ir,ic=dist_field(netm); stop=(int(outlets[vk][0]),int(outlets[vk][1]))
    snapped={}
    for f in F:
        la,lo=f['lat'],f['lon']; r,c=[int(round(v)) for v in ll2px(la,lo)]
        snapped[f['id']]=((int(ir[r,c]),int(ic[r,c])),float(dist[r,c]))
    res={}
    for f in F: res[f['id']]={'offset_m':round(snapped[f['id']][1])}
    pairs={}
    ids=[f['id'] for f in F]
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            ca,_=snapped[a]; cb,_=snapped[b]
            pa,_=chain_to_outlet(*ca,stop); pb,_=chain_to_outlet(*cb,stop)
            sa={x:k for k,x in enumerate(pa)}
            j=next((k for k,x in enumerate(pb) if x in sa),None)
            if j is None: pairs[a+'|'+b]=None; continue
            seg=pa[:sa[pb[j]]+1]+list(reversed(pb[:j]))
            d8,sm=path_len(seg)
            pairs[a+'|'+b]={'d8_m':round(d8),'smoothed_m':round(sm),'plus_offsets_d8_m':round(d8+snapped[a][1]+snapped[b][1]),'straight_m':round(math.hypot(*(np.array(xy((F[i]['lat'],F[i]['lon'])))-np.array(xy((F[ids.index(b)]['lat'],F[ids.index(b)]['lon'])))) ))}
    res_all[vk]={'offsets':res,'pairs':pairs}
json.dump(res_all,open(sys.argv[5],'w'),indent=1)
for vk,v in res_all.items():
    print('==',vk)
    for k,o in v['offsets'].items(): print('  offset',k,o['offset_m'])
    for k,p in v['pairs'].items(): print('  ',k,p)
