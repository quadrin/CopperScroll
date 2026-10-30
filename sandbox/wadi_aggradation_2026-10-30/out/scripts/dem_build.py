# Build a filled DEM, D8 receivers and drainage area (km2) for a bbox. Terrarium z14 tiles (AWS open data).
import sys, io, math, heapq, urllib.request, os
import numpy as np
from PIL import Image
S,W,N,E=map(float,sys.argv[1:5]); Z=int(sys.argv[5]); out=sys.argv[6]; cache=sys.argv[7]
URL='https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
def tile(lat,lon):
    n=2**Z; return (lon+180)/360*n,(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
tx0,ty0=[int(v) for v in tile(N,W)]; tx1,ty1=[int(v) for v in tile(S,E)]
H=(ty1-ty0+1)*256; Wd=(tx1-tx0+1)*256
dem=np.zeros((H,Wd)); os.makedirs(cache,exist_ok=True)
for ty in range(ty0,ty1+1):
    for tx in range(tx0,tx1+1):
        fp=os.path.join(cache,f'{Z}_{tx}_{ty}.png')
        if not os.path.exists(fp):
            open(fp,'wb').write(urllib.request.urlopen(URL.format(z=Z,x=tx,y=ty),timeout=60).read())
        a=np.asarray(Image.open(fp).convert('RGB'),dtype=float)
        dem[(ty-ty0)*256:(ty-ty0+1)*256,(tx-tx0)*256:(tx-tx0+1)*256]=a[...,0]*256+a[...,1]+a[...,2]/256-32768
lat0=(S+N)/2; res=40075016.686*math.cos(math.radians(lat0))/(2**Z*256)
filled=dem.copy(); done=np.zeros(dem.shape,bool); pq=[]
for r in range(H):
    for c in (0,Wd-1): heapq.heappush(pq,(filled[r,c],r,c)); done[r,c]=True
for c in range(Wd):
    for r in (0,H-1):
        if not done[r,c]: heapq.heappush(pq,(filled[r,c],r,c)); done[r,c]=True
nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
order=[]
while pq:
    z,r,c=heapq.heappop(pq); order.append(r*Wd+c)
    for dr,dc in nb:
        rr,cc=r+dr,c+dc
        if 0<=rr<H and 0<=cc<Wd and not done[rr,cc]:
            done[rr,cc]=True
            if filled[rr,cc]<=z: filled[rr,cc]=z+1e-4
            heapq.heappush(pq,(filled[rr,cc],rr,cc))
# vectorised D8 steepest descent
best=np.zeros((H,Wd)); recr=-np.ones((H,Wd),int); recc=-np.ones((H,Wd),int)
R,C=np.mgrid[0:H,0:Wd]
for dr,dc in nb:
    nbz=np.full((H,Wd),np.inf)
    nbz[max(0,-dr):H-max(0,dr), max(0,-dc):Wd-max(0,dc)] = filled[max(0,dr):H-max(0,-dr), max(0,dc):Wd-max(0,-dc)]
    s=(filled-nbz)/math.hypot(dr,dc)
    u=s>best; best[u]=s[u]; recr[u]=R[u]+dr; recc[u]=C[u]+dc
acc=np.ones(H*Wd); rf=recr.ravel(); cf=recc.ravel()
for idx in reversed(order):
    if rf[idx]>=0: acc[rf[idx]*Wd+cf[idx]]+=acc[idx]
area=acc.reshape(H,Wd)*res*res/1e6
np.savez_compressed(out,dem=dem,filled=filled,recr=recr,recc=recc,area=area,Z=Z,tx0=tx0,ty0=ty0,res=res)
print('grid',H,Wd,'res %.2f m'%res,'max area %.1f'%area.max())
