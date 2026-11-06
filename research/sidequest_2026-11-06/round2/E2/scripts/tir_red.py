# Extract red road pixels from TIR North (1993, Roll's roads) and georeference by the printed Israel-grid lines
import numpy as np
from PIL import Image; Image.MAX_IMAGE_PIXELS=None
from pyproj import Transformer
ex=np.array([548,1173.5,1800,2426,3053,3684,4312.5,4938.5,5566.5,6194.5,6824.5,7455.5,8083,8714.5,9346.5,9979.5,10612.5]); ev=80+10*np.arange(len(ex))
ny=np.array([902,1531,2162,2791.5,3418,4044.5,4671,5300.5,5926,6553,7180,7799,8434.5,9061,9688,10314.5,10943,12193,12823,14077.5]); nv=np.array([300,290,280,270,260,250,240,230,220,210,200,190,180,170,160,150,140,120,110,90])
be=np.polyfit(ex,ev,1); bn=np.polyfit(ny,nv,1)
print('E fit',be,'resid m',np.round((np.polyval(be,ex)-ev)*1000,1)); print('N fit',bn,'resid m',np.round((np.polyval(bn,ny)-nv)*1000,1))
im=Image.open('/home/claude/swarm/scratch/E2r2/tir_north.jpg')
W,H=im.size; B=4; pts=[]
for y0 in range(0,H,800):
    a=np.asarray(im.crop((0,y0,W,min(H,y0+800)))).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(r>150)&(g<110)&(b<130)&(r-g>80)
    h=(m.shape[0]//B)*B; w=(m.shape[1]//B)*B
    mb=m[:h,:w].reshape(h//B,B,w//B,B).sum((1,3))>=3
    yy,xx=np.nonzero(mb)
    pts.append(np.c_[xx*B+B/2,yy*B+B/2+y0])
P=np.vstack(pts)
# map area only, drop legend, inset, title strip
keep=(P[:,0]>590)&(P[:,0]<10840)&(P[:,1]>902)&(P[:,1]<14077)
keep&=~((P[:,0]<3400)&(P[:,1]<3500))     # legend and scale block
keep&=~((P[:,0]<1700)&(P[:,1]>4600)&(P[:,1]<6400))  # research-area inset
P=P[keep]
E=np.polyval(be,P[:,0])*1000; N=np.polyval(bn,P[:,1])*1000
x,y=Transformer.from_crs(28191,2039,always_xy=True).transform(E,N)
np.save('/home/claude/swarm/scratch/E2r2/tir_red_itm.npy',np.c_[x,y,P])
print('red blocks',len(P))
