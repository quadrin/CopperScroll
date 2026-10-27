import numpy as np, math, json, sys
class Grid:
    def __init__(s,f):
        d=np.load(f); s.dem=d['dem']; s.area=d['area']; s.rec=d['rec']; s.Z=int(d['Z']); s.tx0=int(d['tx0']); s.ty0=int(d['ty0']); s.res=float(d['res'])
        s.H,s.W=s.dem.shape
    def ll2px(s,lat,lon):
        n=2**s.Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
        return (y-s.ty0)*256-0.5,(x-s.tx0)*256-0.5
    def px2ll(s,r,c):
        n=2**s.Z; x=s.tx0+(c+0.5)/256; y=s.ty0+(r+0.5)/256
        return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))), x/n*360-180
    def snap(s,lat,lon,thr,maxd=1500):
        r0,c0=s.ll2px(lat,lon); R=int(maxd/s.res)+1
        rs=slice(max(0,int(r0)-R),min(s.H,int(r0)+R)); cs=slice(max(0,int(c0)-R),min(s.W,int(c0)+R))
        sub=s.area[rs,cs]>=thr; rr,cc=np.nonzero(sub); rr=rr+rs.start; cc=cc+cs.start
        d=np.hypot(rr-r0,cc-c0)*s.res; i=np.argmin(d); return (int(rr[i]),int(cc[i])),float(d[i])
    def down(s,cell,stop=None,maxn=100000):
        p=[cell]
        while len(p)<maxn:
            r,c=p[-1]; rr,cc=s.rec[r,c]
            if rr<0: break
            p.append((int(rr),int(cc)))
            if stop and stop(p[-1]): break
        return p
    def length(s,path):
        return sum(math.hypot(a[0]-b[0],a[1]-b[1]) for a,b in zip(path,path[1:]))*s.res
    def network(s,reach,thr=0.25):
        """channel cells (area>=thr) whose first hit on the reach is not reach[0] (i.e. tributaries joining within the reach) plus the reach."""
        R={c:i for i,c in enumerate(reach)}
        lab=np.full((s.H,s.W),-2,np.int32)   # -2 unknown, -1 not in, >=0 index of first reach cell hit
        for c,i in R.items(): lab[c]=i
        rr,cc=np.nonzero(s.area>=thr)
        order=np.argsort(s.area[rr,cc])  # small first doesn't matter; iterative with memo
        for k in order:
            r,c=int(rr[k]),int(cc[k])
            if lab[r,c]!=-2: continue
            path=[(r,c)]
            while True:
                a,b=path[-1]; x,y=s.rec[a,b]
                if x<0: v=-1; break
                x,y=int(x),int(y)
                if lab[x,y]!=-2: v=lab[x,y]; break
                if s.area[x,y]<thr: v=-1; break
                path.append((x,y))
            for p in path: lab[p]=v
        m=(lab>0)|((lab==0)&False)
        for c in reach: m[c]=True
        return m
    def dist_to(s,mask,lat,lon,maxd=3000):
        r0,c0=s.ll2px(lat,lon); R=int(maxd/s.res)+1
        rs=slice(max(0,int(r0)-R),min(s.H,int(r0)+R)); cs=slice(max(0,int(c0)-R),min(s.W,int(c0)+R))
        rr,cc=np.nonzero(mask[rs,cs])
        if len(rr)==0: return None,None
        rr=rr+rs.start; cc=cc+cs.start; d=np.hypot(rr-r0,cc-c0)*s.res; i=np.argmin(d)
        return float(d[i]),(int(rr[i]),int(cc[i]))
