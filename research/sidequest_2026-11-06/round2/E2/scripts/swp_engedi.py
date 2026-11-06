import sys; sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts'); sys.path.insert(0,'/home/claude/swarm/scratch/C2/scripts')
import numpy as np
from tiles import mosaic,deg2num
from roadlib import S,M
from pyproj import Transformer
from PIL import ImageDraw
I2L=Transformer.from_crs(2039,4326,always_xy=True)
E0,N0,E1,N1=219000,594000,241000,620000; z=14
lon0,lat0=I2L.transform(E0,N1); lon1,lat1=I2L.transform(E1,N0)
im,org,ts=mosaic('pal63k-1880',z,lat0,lon0,lat1,lon1); d=ImageDraw.Draw(im)
def px(e,n):
    lon,lat=I2L.transform(e,n); x,y=deg2num(lat,lon,z); return ((x-org[0])*ts,(y-org[1])*ts)
R=np.load('/home/claude/swarm/scratch/E2r2/tir_red_itm.npy')
m=(R[:,0]>E0)&(R[:,0]<E1)&(R[:,1]>N0)&(R[:,1]<N1)
for e,n in R[m][::2,:2]:
    x,y=px(e,n); d.point((x,y),fill=(255,0,255))
for s,mm in zip(S,M):
    s=np.asarray(s,float)
    if s[:,0].max()<E0 or s[:,0].min()>E1 or s[:,1].max()<N0 or s[:,1].min()>N1: continue
    d.line([px(e,n) for e,n in s],fill=(0,90,255),width=3)
im.save('/home/claude/swarm/scratch/E2r2/img/swp_engedi.png'); im.thumbnail((1500,1500)); im.save('/home/claude/swarm/scratch/E2r2/img/swp_engedi_s.png'); print(im.size)
