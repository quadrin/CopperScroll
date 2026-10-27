import numpy as np, math, json, sys
d=np.load(sys.argv[1]); area=d['area']; recr=d['recr']; recc=d['recc']; dem=d['dem']
Z=int(d['Z']); tx0=int(d['tx0']); ty0=int(d['ty0']); res=float(d['res']); H,W=area.shape
def ll2px(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return (y-ty0)*256-0.5,(x-tx0)*256-0.5
def px2ll(r,c):
    n=2**Z; x=tx0+(c+0.5)/256; y=ty0+(r+0.5)/256
    return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))), x/n*360-180
def snap(lat,lon,k=3):
    r,c=[int(round(v)) for v in ll2px(lat,lon)]
    return max((area[rr,cc],rr,cc) for rr in range(r-k,r+k+1) for cc in range(c-k,c+k+1))[1:]
def downpath(r,c,maxlen=1e9):
    p=[(r,c)]; s=0
    while recr[r,c]>=0 and s<maxlen:
        r2,c2=recr[r,c],recc[r,c]; s+=math.hypot(r2-r,c2-c)*res; r,c=r2,c2; p.append((r,c))
    return p
def catchment(r0,c0):
    # cells whose downstream path reaches (r0,c0): propagate via order of decreasing filled
    flat=np.arange(H*W); rf=recr.ravel(); cf=recc.ravel()
    tgt=np.where(rf>=0, rf*W+cf, -1)
    mask=np.zeros(H*W,bool); mask[r0*W+c0]=True
    order=np.argsort(d['filled'].ravel())  # ascending: receivers before donors
    for idx in order:
        t=tgt[idx]
        if t>=0 and mask[t]: mask[idx]=True
    return mask.reshape(H,W)
from scipy.ndimage import distance_transform_edt
def network(mask,thr=0.25):
    return mask & (area>=thr)
def dist_field(netmask):
    dist,(ir,ic)=distance_transform_edt(~netmask,return_indices=True)
    return dist*res,ir,ic
def chain_to_outlet(r,c,stop):
    # list of cells and cumulative distance downstream from (r,c) to stop cell
    p=[(r,c)]; cum=[0.0]
    while (r,c)!=stop and recr[r,c]>=0:
        r2,c2=recr[r,c],recc[r,c]; cum.append(cum[-1]+math.hypot(r2-r,c2-c)*res); r,c=r2,c2; p.append((r,c))
    return p,cum
def along(a,b,stop):
    pa,ca=chain_to_outlet(*a,stop); pb,cb=chain_to_outlet(*b,stop)
    da={x:ca[i] for i,x in enumerate(pa)}
    for j,x in enumerate(pb):
        if x in da: return da[x]+cb[j], x
    return None,None
