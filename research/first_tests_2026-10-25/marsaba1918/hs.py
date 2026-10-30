import rasterio, numpy as np
from rasterio.windows import from_bounds
from PIL import Image, ImageDraw
src=rasterio.open('dl/dem.tif')
w=from_bounds(35.15,31.58,35.45,31.80,src.transform)
z=src.read(1,window=w).astype(float); T=src.window_transform(w)
np.save('dem_crop.npy',z); open('dem_T.txt','w').write(repr(tuple(T)[:6]))
lat=31.7
dzdx=np.gradient(z,axis=1)/(abs(T.a)*111320*np.cos(np.radians(lat))); dzdy=np.gradient(z,axis=0)/(abs(T.e)*110570)*(-1)
az=np.radians(214); el=np.radians(27)
lx,ly,lz=np.sin(az)*np.cos(el),np.cos(az)*np.cos(el),np.sin(el)
n=np.sqrt(dzdx**2+dzdy**2+1)
hs=np.clip((-dzdx*lx-dzdy*ly+lz)/n,0,1)
im=Image.fromarray((hs*255).astype(np.uint8)).convert('RGB')
d=ImageDraw.Draw(im)
pts={'MS':(31.7047,35.3317),'T1':(31.72564,35.32414),'T2':(31.69677,35.33571),'S99':(31.69992,35.33877),'S100':(31.70081,35.34879),'S108':(31.69098,35.35373)}
inv=~T
for k,(la,lo) in pts.items():
    c,r=inv*(lo,la); d.ellipse([c-4,r-4,c+4,r+4],outline=(255,0,0)); d.text((c+5,r-5),k,fill=(255,0,0))
for lo in np.arange(35.15,35.46,0.05):
    c,_=inv*(lo,31.8); d.line([c,0,c,im.height],fill=(0,120,255)); d.text((c+2,2),f'{lo:.2f}',fill=(0,0,255))
for la in np.arange(31.6,31.81,0.05):
    _,r=inv*(35.15,la); d.line([0,r,im.width,r],fill=(0,120,255)); d.text((2,r+2),f'{la:.2f}',fill=(0,0,255))
im=im.resize((im.width*2,im.height*2)); im.save('dem_hs.jpg',quality=85); print(z.shape,z.min(),z.max(),im.size)
