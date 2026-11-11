import numpy as np, sys
sys.path.insert(0,'/home/claude/dem')
from scipy import ndimage as ndi
from PIL import Image, ImageDraw
from demtool import load
Image.MAX_IMAGE_PIXELS=None
def hill(a,az=165,alt=30):
    gy,gx=np.gradient(a,30.8,26.2); gy=-gy  # north positive
    az=np.radians(az); alt=np.radians(alt)
    sx,sy,sz=np.sin(az)*np.cos(alt),np.cos(az)*np.cos(alt),np.sin(alt)
    n=np.sqrt(gx**2+gy**2+1); return np.clip((-gx*sx-gy*sy+sz)/n,0,1)
def render(tolonlat,x0,y0,w,h,s,bbox,az=165,alt=30):
    a,t=load(*bbox); hs=hill(a,az,alt)
    X,Y=np.meshgrid(x0+np.arange(0,w,s),y0+np.arange(0,h,s))
    lon,lat=tolonlat(X.ravel(),Y.ravel())
    col=(lon-t.c)/t.a-0.5; row=(lat-t.f)/t.e-0.5
    v=ndi.map_coordinates(hs,[row,col],order=1).reshape(X.shape)
    return Image.fromarray((v*255).astype('uint8'))
def side(img,dem,out,step=200):
    W,H=img.size; c=Image.new('L',(W*2+10,H),255); c.paste(img,(0,0)); c.paste(dem.resize((W,H)),(W+10,0)); c=c.convert('RGB'); d=ImageDraw.Draw(c)
    for off in (0,W+10):
        for x in range(0,W,step): d.line((off+x,0,off+x,H),fill=(255,0,0),width=1)
        for y in range(0,H,step): d.line((off,y,off+W,y),fill=(255,0,0),width=1)
    c.save(out,quality=85)
