import numpy as np, cv2
from PIL import Image
S=4284/1500.
def lines_to_pts(rows,cols):
    # rows: {val:((x,y),(x,y))} in display coords; returns photo pts (full res) and grid (col,row)
    P=[];G=[]
    def L(p,q): p=np.array([*p,1.]);q=np.array([*q,1.]); return np.cross(p,q)
    for r,(a,b) in rows.items():
        for c,(d,e) in cols.items():
            x=np.cross(L(a,b),L(d,e)); P.append([x[0]/x[2]*S,x[1]/x[2]*S]); G.append([c,r])
    return np.array(P,np.float32),np.array(G,np.float32)
def grid2img(f,x0,y0,anchor=(608,560),ar=47.0,ac=17.0,th=13.0):
    t=np.radians(th); e=np.array([20*np.cos(t),20*np.sin(t)]); n=np.array([20*np.sin(t),-20*np.cos(t)])
    # img = anchor + (c-ac)*e + (r-ar)*n ; then (img-[x0,y0])*f
    A=np.array([[e[0],n[0],anchor[0]-ac*e[0]-ar*n[0]-x0],[e[1],n[1],anchor[1]-ac*e[1]-ar*n[1]-y0],[0,0,1/f]])*f
    return A
def warp(photo,rows,cols,base,f,x0,y0,out,color=(255,0,0),th=13.0,blk=41,C=12):
    P,G=lines_to_pts(rows,cols); H,_=cv2.findHomography(P,G)
    M=grid2img(f,x0,y0,th=th)@H
    p=np.asarray(Image.open(photo).convert('L')); p=cv2.adaptiveThreshold(cv2.GaussianBlur(p,(0,0),1.5),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blk,C)
    w=cv2.warpPerspective(p,M,(base.shape[1],base.shape[0]),flags=cv2.INTER_AREA,borderValue=255)
    m=w<128; base[m]=(0.35*base[m]+0.65*np.array(color)).astype('uint8'); return base,H
R26={43:((343,270),(255,1815)),42:((483,270),(428,1815)),41:((622,270),(607,1815)),40:((765,270),(783,1815)),39:((903,270),(958,1815)),38:((1042,270),(1135,1815))}
C26={15:((185,1612),(1312,1607)),16:((195,1440),(1298,1437)),17:((203,1278),(1285,1268)),18:((210,1110),(1272,1105)),21:((240,665),(1240,665)),23:((265,405),(1215,398))}
R35={29:((385,287),(540,1880)),30:((550,298),(680,1867)),31:((693,307),(818,1853)),32:((840,318),(953,1840))}
C35={38:((283,383),(1097,385)),39:((283,538),(1097,500)),40:((283,688),(1095,645)),41:((285,835),(1097,780)),42:((285,985),(1090,925)),43:((285,1130),(1100,1053)),44:((287,1283),(1105,1187)),46:((293,1560),(1095,1460)),47:((296,1710),(1090,1583)),48:((298,1848),(1090,1720))}
if __name__=='__main__':
    b=np.asarray(Image.open('/home/claude/c67/tul78_rect.png')); x0,y0,x1,y1=300,380,1300,1120; f=2
    base=cv2.resize(b[y0:y1,x0:x1],None,fx=f,fy=f,interpolation=cv2.INTER_CUBIC); Image.fromarray(base).save('pal78_x2.jpg',quality=90)
    rgb=np.dstack([base]*3).copy()
    rgb,H26=warp('0547.jpg',R26,C26,rgb,f,x0,y0,None)
    rgb,H35=warp('0551.jpg',R35,C35,rgb,f,x0,y0,None,color=(255,120,0))
    Image.fromarray(rgb).save('pal78_grid_overlay.jpg',quality=90); print(rgb.shape)
