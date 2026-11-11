import numpy as np, sys
sys.path.insert(0,'/home/claude/dem')
from scipy import ndimage as ndi
from PIL import Image
import warp
Image.MAX_IMAGE_PIXELS=None
def hp(a,s=12): a=a.astype(float); return a-ndi.uniform_filter(a,s)
def ncc_shift(I,D,maxs=12):
    best=(-2,0,0)
    h,w=I.shape
    for dy in range(-maxs,maxs+1):
        for dx in range(-maxs,maxs+1):
            a=I[maxs:h-maxs,maxs:w-maxs]; b=D[maxs+dy:h-maxs+dy,maxs+dx:w-maxs+dx]
            a=a-a.mean(); b=b-b.mean(); c=(a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-9)
            if c>best[0]: best=(c,dx,dy)
    return best
def run(impath,tl,x0,y0,s,bbox,az,alt=28,blk=70,rot180=False):
    im=Image.open(impath).convert('L'); W,H=im.size
    I=np.asarray(im.resize((W//s,H//s),Image.BOX),float)
    D=np.asarray(warp.render(tl,x0,y0,W,H,s,bbox,az,alt),float)[:I.shape[0],:I.shape[1]]
    I=hp(ndi.gaussian_filter(I,1.2)); D=hp(D)
    out=[]
    for by in range(0,I.shape[0]-blk+1,blk):
        for bx in range(0,I.shape[1]-blk+1,blk):
            c,dx,dy=ncc_shift(I[by:by+blk,bx:bx+blk],D[by:by+blk,bx:bx+blk])
            out.append((bx+blk//2,by+blk//2,round(c,2),dx,dy))
    return out
