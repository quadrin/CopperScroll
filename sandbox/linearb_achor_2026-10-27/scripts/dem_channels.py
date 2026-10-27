import sys, io, math, heapq, urllib.request, os, json
import numpy as np
from PIL import Image
# usage: dem_channels.py name lat0 lon0 S W N E zoom outdir
name=sys.argv[1]; lat0=float(sys.argv[2]); lon0=float(sys.argv[3])
S,W,N,E=map(float,sys.argv[4:8]); Z=int(sys.argv[8]); out=sys.argv[9]
URL='https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
def tile(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return x,y
tx0,ty0=[int(v) for v in tile(N,W)]; tx1,ty1=[int(v) for v in tile(S,E)]
H=(ty1-ty0+1)*256; Wd=(tx1-tx0+1)*256
dem=np.zeros((H,Wd))
cache=os.path.join(out,'tiles'); os.makedirs(cache,exist_ok=True)
for ty in range(ty0,ty1+1):
    for tx in range(tx0,tx1+1):
        fp=os.path.join(cache,f'{Z}_{tx}_{ty}.png')
        if not os.path.exists(fp):
            open(fp,'wb').write(urllib.request.urlopen(URL.format(z=Z,x=tx,y=ty),timeout=60).read())
        a=np.asarray(Image.open(fp).convert('RGB'),dtype=float)
        dem[(ty-ty0)*256:(ty-ty0+1)*256,(tx-tx0)*256:(tx-tx0+1)*256]=a[...,0]*256+a[...,1]+a[...,2]/256-32768
def px2ll(r,c):
    n=2**Z; x=tx0+(c+0.5)/256; y=ty0+(r+0.5)/256
    lon=x/n*360-180; lat=math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))); return lat,lon
def ll2px(lat,lon):
    x,y=tile(lat,lon); return (y-ty0)*256-0.5,(x-tx0)*256-0.5
res=40075016.686*math.cos(math.radians(lat0))/(2**Z*256)
# priority flood with epsilon
filled=dem.copy(); done=np.zeros(dem.shape,bool); pq=[]
for r in range(H):
    for c in (0,Wd-1):
        heapq.heappush(pq,(filled[r,c],r,c)); done[r,c]=True
for c in range(Wd):
    for r in (0,H-1):
        if not done[r,c]: heapq.heappush(pq,(filled[r,c],r,c)); done[r,c]=True
nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
order=[]
while pq:
    z,r,c=heapq.heappop(pq); order.append((r,c))
    for dr,dc in nb:
        rr,cc=r+dr,c+dc
        if 0<=rr<H and 0<=cc<Wd and not done[rr,cc]:
            done[rr,cc]=True
            if filled[rr,cc]<=z: filled[rr,cc]=z+1e-4
            heapq.heappush(pq,(filled[rr,cc],rr,cc))
# D8 receiver
rec=-np.ones((H,Wd,2),int)
for r in range(H):
    for c in range(Wd):
        best=0;bi=None
        for dr,dc in nb:
            rr,cc=r+dr,c+dc
            if 0<=rr<H and 0<=cc<Wd:
                s=(filled[r,c]-filled[rr,cc])/(math.hypot(dr,dc))
                if s>best: best=s;bi=(rr,cc)
        if bi: rec[r,c]=bi
acc=np.ones((H,Wd))
for r,c in reversed(order):
    rr,cc=rec[r,c]
    if rr>=0: acc[rr,cc]+=acc[r,c]
area=acc*res*res/1e6
np.savez_compressed(os.path.join(out,name+'.npz'),dem=dem,filled=filled,rec=rec,area=area,Z=Z,tx0=tx0,ty0=ty0,res=res)
r0,c0=ll2px(lat0,lon0)
print(name,'grid',H,Wd,'res %.1f m'%res,'S px',round(r0,1),round(c0,1),'elev at S %.0f'%dem[int(round(r0)),int(round(c0))])
for thr in (0.05,0.1,0.25,0.5,1.0,2.0):
    m=area>=thr
    rr,cc=np.nonzero(m)
    d=np.hypot(rr-r0,cc-c0)*res
    i=np.argmin(d)
    lat,lon=px2ll(rr[i],cc[i])
    brg=(math.degrees(math.atan2(cc[i]-c0,-(rr[i]-r0)))+360)%360
    print('thr %.2f km2: nearest channel cell %.0f m, bearing %.0f, at %.5f,%.5f, drainage %.2f km2, elev %.0f'%(thr,d[i],brg,lat,lon,area[rr[i],cc[i]],dem[rr[i],cc[i]]))
