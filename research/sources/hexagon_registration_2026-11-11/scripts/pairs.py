import sys, pickle, numpy as np, cv2, os
sys.path.insert(0,'/home/claude/dem')
import auto
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
L=lambda n: pickle.load(open('/home/claude/dem/A_%s.pkl'%n,'rb'))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
O='/mnt/user-data/outputs/gis/date_pairs/'; os.makedirs(O,exist_ok=True)
imgs={}
def get(p):
    if p not in imgs: imgs[p]=np.asarray(Image.open(p).convert('L'))
    return imgs[p]
def rect(path,A,ox,oy,E0,N0,size,res):
    # output pixel (i,j) -> E=E0+i*res, N=N0-j*res ; need source px: [x,y] = inv(M)*( [E,N]-c ) - origin
    M=A[:2].T; c=A[2]; Mi=np.linalg.inv(M)
    # src = Mi@([E0,N0]-c) + Mi@[res*i, -res*j] - [ox,oy]
    B=Mi@np.array([[res,0],[0,-res]]); t=Mi@(np.array([E0,N0])-c)-np.array([ox,oy])
    W=np.hstack([B,t[:,None]]).astype(np.float64)
    return cv2.warpAffine(get(path),W,(size,size),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP)
def pair(tag,lat,lon,half=350,res=0.7):
    E,N=auto.T.transform(lon,lat); size=int(2*half/res); E0,N0=E-half,N+half
    a=rect('/home/claude/hx2/kaf_rot.png',L('a015c'),0,0,E0,N0,size,res)
    if tag=='tell_er_rameh': b=rect('/home/claude/hx6/ram_rot.png',L('a017e_both'),-1500,6000,E0,N0,size,res)
    else: b=rect('/home/claude/hx5/kaf_dec_rot.png',L('a017e_both'),0,0,E0,N0,size,res)
    def st(x):
        x=x.astype(float); lo,hi=np.percentile(x[x>0],[1,99]) if (x>0).any() else (0,255); return np.clip((x-lo)/(hi-lo+1e-6)*255,0,255).astype('uint8')
    c=Image.new('L',(size*2+12,size+40),255); c.paste(Image.fromarray(st(a)),(0,40)); c.paste(Image.fromarray(st(b)),(size+12,40)); c=c.convert('RGB'); d=ImageDraw.Draw(c)
    d.text((8,8),'25 June 1974 (A015c)',fill=(0,0,0),font=font); d.text((size+20,8),'1 December 1974 (A017e)   north up, %.1f m/px, %d m wide'%(res,2*half),fill=(0,0,0),font=font)
    for off in (0,size+12):
        bx=off+20; by=size+40-25; d.line((bx,by,bx+100/res,by),fill=(255,255,0),width=4); d.text((bx,by-26),'100 m',fill=(255,255,0),font=font)
    c.save(O+'kafrein_1974_jun_dec_%s.jpg'%tag,quality=88); print(tag,c.size)
pair('habbasa',31.8394,35.6792)
pair('barakat_and_dam_end',31.8528,35.6735)
pair('plateau_fort',31.8417,35.6842,250,0.5)
pair('tell_er_rameh',31.8257,35.6444)
pair('tell_el_hammam',31.8407,35.6740,400,0.8)
