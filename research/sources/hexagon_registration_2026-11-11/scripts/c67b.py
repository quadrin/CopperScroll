import numpy as np, sys, pickle, cv2
sys.path.insert(0,'/home/claude/dem'); sys.path.insert(0,'/home/claude/gis')
import auto, c67reg as R
from PIL import Image
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS=None
L=lambda n: pickle.load(open('/home/claude/dem/A_%s.pkl'%n,'rb'))
H='/mnt/user-data/uploads/Copper Scroll/08 Working files/hexagon windows 2026-11-10/'
def rect(src,A,ox,oy,f,E0,N0,W,Hh,res):
    # source image px (u,v) at factor f: tile x = ox+u*f
    M=A[:2].T; c=A[2]; Mi=np.linalg.inv(M); B=Mi@np.array([[res,0],[0,-res]])/f; t=(Mi@(np.array([E0,N0])-c)-np.array([ox,oy]))/f
    return cv2.warpAffine(src,np.hstack([B,t[:,None]]),(W,Hh),flags=cv2.INTER_AREA|cv2.WARP_INVERSE_MAP)
def ref(name,E0,N0,W,Hh,res):
    cfg={'jer':('F017b_dec74_jericho_qelt_full_x15800_y1900.jpg','f017b',15800,1900,1),
         'pl':('F017b_dec74_plain_and_scarp_half_x14900_y8400_r2.jpg','f017b',14900,8400,2),
         'eb':('F017b_dec74_east_bank_half_x26000_y1500_r2.jpg','f017b_east',26000,1500,2)}[name]
    src=np.asarray(Image.open(H+cfg[0]).convert('L')); return rect(src,L(cfg[1]),cfg[2],cfg[3],cfg[4],E0,N0,W,Hh,res)
def cor(name,A,E0,N0,W,Hh,res):
    p,x0,y0,f=R.W[name]; src=np.asarray(Image.open(p).convert('L')); return rect(src,A,x0,y0,1,E0,N0,W,Hh,res)
