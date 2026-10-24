import json, sys, numpy as np, cv2
from PIL import Image, ImageDraw
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}
W=np.load('plan_walls.npy'); ox,oz=-20.0,-42.0; cell=0.25
a=np.array(Image.open('F007_c_ruin_29180_19840.png')).astype(np.float32); X0,Y0=29180,19840
EIGHT=['L71','L56','L58','L91','L110','L48-L49','L117','L118','L138']
def to_img(x,z,p):
    s,th,ax,ay=p; c,sn=np.cos(th),np.sin(th)
    return ax+(c*x+sn*z)/s, ay+(-sn*x+c*z)/s
def draw(p,x0,y0,w,h,k,out,walls=True,pools=True,labels=True,extra=None):
    c=a[y0-Y0:y0-Y0+h, x0-X0:x0-X0+w]
    lo,hi=np.percentile(c,1),np.percentile(c,99); c=np.clip((c-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    big=cv2.resize(c,(w*k,h*k),interpolation=cv2.INTER_CUBIC)
    im=Image.fromarray(big).convert('RGB'); dr=ImageDraw.Draw(im)
    T=lambda x,z:((to_img(x,z,p)[0]-x0+0.5)*k,(to_img(x,z,p)[1]-y0+0.5)*k)
    if walls:
        cs,_=cv2.findContours(W.astype(np.uint8),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for cc in cs:
            pts=[T(ox+(q[0][0]+0.5)*cell, oz+(q[0][1]+0.5)*cell) for q in cc]
            if len(pts)>1: dr.line(pts+[pts[0]],fill=(255,210,0),width=1)
    if pools:
        for kk in ['L117','L118','L138','L48-L49','L50','L56','L58','L91','L68','L69','L71']:
            pts=[T(*q) for q in E[kk]['geometry']['points']]
            col=(255,40,40) if kk in EIGHT else (60,160,255)
            dr.line(pts+[pts[0]],fill=col,width=2)
            if labels:
                cx=sum(q[0] for q in pts)/len(pts); cy=sum(q[1] for q in pts)/len(pts); dr.text((cx+6,cy-6),kk,fill=col)
        cx,cy=T(0,0); r=2.31/p[0]*k; dr.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(255,40,40),width=2)
        if labels: dr.text((cx+r+3,cy-6),'L110',fill=(255,40,40))
    if extra:
        for (u,v,col) in extra:
            X,Y=(u-x0+0.5)*k,(v-y0+0.5)*k; dr.ellipse([X-4,Y-4,X+4,Y+4],outline=col,width=2)
    im.save(out)
if __name__=='__main__':
    s,thd,ax,ay=map(float,sys.argv[1:5]); x0,y0,w,h,k=map(int,sys.argv[5:10])
    draw((s,np.radians(thd),ax,ay),x0,y0,w,h,k,sys.argv[10])
