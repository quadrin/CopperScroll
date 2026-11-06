import sys; sys.path.insert(0,'/home/claude/swarm/scratch/C2/scripts'); sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from tiles import mosaic,deg2num
from roadlib import S,M
from pyproj import Transformer
from PIL import ImageDraw
import numpy as np
I2L=Transformer.from_crs(2039,4326,always_xy=True)
def view(layer,z,E0,N0,E1,N1,pts,out,suffix=''):
    lon0,lat0=I2L.transform(E0,N1); lon1,lat1=I2L.transform(E1,N0)
    im,org,ts=mosaic(layer,z,lat0,lon0,lat1,lon1,suffix)
    d=ImageDraw.Draw(im)
    def px(e,n):
        lon,lat=I2L.transform(e,n); x,y=deg2num(lat,lon,z); return ((x-org[0])*ts,(y-org[1])*ts)
    for s,m in zip(S,M):
        s=np.asarray(s,float)
        if s[:,0].max()<E0-5000 or s[:,0].min()>E1+5000 or s[:,1].max()<N0-5000 or s[:,1].min()>N1+5000: continue
        d.line([px(e,n) for e,n in s],fill=(0,200,0),width=2)
    for lab,e,n in pts:
        x,y=px(e,n); d.ellipse([x-6,y-6,x+6,y+6],outline=(255,0,0),width=2); d.text((x+8,y-8),lab,fill=(255,0,0))
    im.save(out); print(out,im.size)
if __name__=='__main__':
    pts=[('Devora1606',235790,733940),('KafrKama8521',241700,736500)]
    view(sys.argv[1],int(sys.argv[2]),*map(float,sys.argv[3:7]),pts,sys.argv[7])
