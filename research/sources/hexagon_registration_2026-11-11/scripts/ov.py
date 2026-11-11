import sys, pickle, numpy as np, cv2
sys.path.insert(0,'/home/claude/dem'); sys.path.insert(0,'/home/claude/gis')
import auto
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
L=lambda n: pickle.load(open('/home/claude/dem/A_%s.pkl'%n,'rb'))
def rect(path,A,ox,oy,E0,N0,W,H,res):
    M=A[:2].T; c=A[2]; Mi=np.linalg.inv(M); B=Mi@np.array([[res,0],[0,-res]]); t=Mi@(np.array([E0,N0])-c)-np.array([ox,oy])
    src=np.asarray(Image.open(path).convert('L'))
    return cv2.warpAffine(src,np.hstack([B,t[:,None]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
def stretch(x,g=1.0):
    x=x.astype(float); lo,hi=np.percentile(x,[1,99.5]); y=np.clip((x-lo)/(hi-lo+1e-6),0,1)**g; return (y*255).astype('uint8')
def overlay(base,plan_path,ppm,res,anchor_plan,anchor_img,out,thr=110,crop=None,rot=0):
    p=np.asarray(Image.open(plan_path).convert('L'))
    if crop: x0,y0,x1,y1=crop; p=p[y0:y1,x0:x1]; anchor_plan=(anchor_plan[0]-x0,anchor_plan[1]-y0)
    s=(1/ppm)/res
    M=cv2.getRotationMatrix2D(anchor_plan,rot,s); M[0,2]+=anchor_img[0]-anchor_plan[0]; M[1,2]+=anchor_img[1]-anchor_plan[1]
    w=cv2.warpAffine(p,M,(base.shape[1],base.shape[0]),flags=cv2.INTER_AREA,borderValue=255)
    rgb=np.dstack([base]*3).copy(); m=w<thr; rgb[m]=(0.35*rgb[m]+0.65*np.array([255,0,0])).astype('uint8')
    Image.fromarray(rgb).save(out,quality=90); return rgb
