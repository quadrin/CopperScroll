import numpy as np, sys
sys.path.insert(0,'/home/claude/dem')
from scipy import ndimage as ndi
from PIL import Image
import warp, auto
from reg import hp, ncc_shift
Image.MAX_IMAGE_PIXELS=None
_cache={}
def img(path,f,s):
    k=(path,f,s)
    if k not in _cache:
        im=Image.open(path).convert('L'); W,H=im.size; r=s/f
        _cache[k]=(np.asarray(im.resize((int(W/r),int(H/r)),Image.BOX),float),W*f,H*f)
    return _cache[k]
def matches(wins,A,bbox,az,alt,s,blk,cmin,maxs=12):
    P=[];G=[];C=[]
    for path,x0,y0,f in wins:
        I,TW,TH=img(path,f,s)
        D=np.asarray(warp.render(auto.mk(A),x0,y0,TW,TH,s,bbox,az,alt),float)
        h=min(I.shape[0],D.shape[0]); w_=min(I.shape[1],D.shape[1]); I2=hp(ndi.gaussian_filter(I[:h,:w_],1.0)); D2=hp(D[:h,:w_])
        Dp=np.pad(D2,maxs,mode='constant')
        for by in range(0,h-blk+1,blk//2):
            for bx in range(0,w_-blk+1,blk//2):
                Ib=I2[by:by+blk,bx:bx+blk]
                if Ib.std()<1e-6: continue
                a=Ib-Ib.mean(); na=np.sqrt((a*a).sum()); best=(-2,0,0)
                for dy in range(-maxs,maxs+1):
                    for dx in range(-maxs,maxs+1):
                        b=Dp[by+dy+maxs:by+dy+maxs+blk,bx+dx+maxs:bx+dx+maxs+blk]; b=b-b.mean(); c=(a*b).sum()/(na*np.sqrt((b*b).sum())+1e-9)
                        if c>best[0]: best=(c,dx,dy)
                c,dx,dy=best
                if c<cmin or abs(dx)>=maxs-1 or abs(dy)>=maxs-1: continue
                X=x0+(bx+blk/2)*s; Y=y0+(by+blk/2)*s
                P.append([X,Y,1]); G.append(auto.w(A,X+dx*s,Y+dy*s)); C.append(c)
    return np.array(P,float),np.array(G),np.array(C)
def fit(P,G,quad=False):
    if quad: P=np.c_[P,(P[:,0]/1e4)**2,(P[:,0]*P[:,1])/1e8]
    A=np.linalg.lstsq(P,G,rcond=None)[0]; r=P@A-G; return A,r
def solve(wins,A,bbox,az=190,alt=28,stages=((80,30,0.5,12),(40,40,0.55,12),(20,50,0.6,12),(20,50,0.6,12)),verbose=True,mode='affine'):
    k=None
    for st in stages:
        s,blk,cmin,ms=st[:4]
        P,G,C=matches(wins,A,bbox,az,alt,s,blk,cmin,ms)
        if len(P)<4: print('  stage',s,'too few',len(P)); continue
        Pl,Gl=P,G
        if mode=='shift' or (len(st)>4 and st[4]=='shift'):
            sh=np.median(G-P@A,axis=0); A2=A.copy(); A2[2]+=sh; r=P@A2-G; k=np.ones(len(P),bool)
        else:
            A2,r=fit(P,G); d=np.hypot(*r.T); k=d<max(2.5*np.sqrt((d**2).mean()),1.5*s)
            A2,r=fit(P[k],G[k])

        if verbose: print('  stage s=%d n=%d kept=%d c=%.2f rms=%.0f m scales %.3f %.3f'%(s,len(P),k.sum(),C.mean(),np.sqrt((r**2).sum(1).mean()),np.hypot(*A2[0]),np.hypot(*A2[1])))
        A=A2
    return A,Pl[k] if len(k)==len(Pl) else Pl,Gl[k] if len(k)==len(Gl) else Gl
def ll(A,x,y):
    lo,la=auto.Ti.transform(*auto.w(A,x,y)); return round(la,5),round(lo,5)
def pxll(A,la,lo): return np.round(auto.px(A,*auto.T.transform(lo,la)))
