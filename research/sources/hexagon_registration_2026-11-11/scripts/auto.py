import numpy as np, sys, pickle
sys.path.insert(0,'/home/claude/dem')
from pyproj import Transformer
import reg
T=Transformer.from_crs(4326,2039,always_xy=True); Ti=Transformer.from_crs(2039,4326,always_xy=True)
def mk(A):
    def tl(x,y):
        E=A[0,0]*x+A[1,0]*y+A[2,0]; N=A[0,1]*x+A[1,1]*y+A[2,1]; return Ti.transform(E,N)
    return tl
def w(A,x,y): return np.array([x,y,1.])@A
def px(A,E,N): return np.linalg.solve(A[:2].T,np.array([E,N])-A[2])
def solve(wins,A,bbox,az=190,s=20,blk=50,iters=3,cmin=0.6,alt=28):
    """wins: list of (path,x0,y0) in the common pixel frame of A"""
    for it in range(iters):
        P=[];G=[];Cc=[]
        for path,x0,y0 in wins:
            for bx,by,c,dx,dy in reg.run(path,mk(A),x0,y0,s,bbox,az,alt,blk):
                if c<cmin or abs(dx)>=11 or abs(dy)>=11: continue
                X=x0+bx*s; Y=y0+by*s
                P.append([X,Y,1]); G.append(w(A,X+dx*s,Y+dy*s)); Cc.append(c)
        P=np.array(P,float);G=np.array(G)
        A2=np.linalg.lstsq(P,G,rcond=None)[0]; r=P@A2-G
        keep=np.hypot(*r.T)<2.5*np.sqrt((r**2).sum(1).mean())
        A2=np.linalg.lstsq(P[keep],G[keep],rcond=None)[0]; r=(P@A2-G)[keep]
        print('iter',it,'n',len(P),'kept',keep.sum(),'mean c %.2f'%np.mean(Cc),'rms %.0f m'%np.sqrt((r**2).sum(1).mean()),'scales %.3f %.3f'%(np.hypot(*A2[0]),np.hypot(*A2[1])))
        A=A2
    return A,P[keep],G[keep]
