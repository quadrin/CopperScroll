import json, numpy as np, cv2
from PIL import Image, ImageDraw
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}
cp=json.load(open('cp_fit.json')); s=cp['m_per_px']; th=np.radians(cp['theta_deg']); tx,ty=cp['L110_px']
a=np.array(Image.open('F007_c_ruin_29180_19840.png')).astype(np.float32); X0,Y0=29180,19840
c_,sn=np.cos(th),np.sin(th)
img=lambda x,z:(tx+(c_*x+sn*z)/s, ty+(-sn*x+c_*z)/s)
cent=json.load(open('pool_centres_px.json'))
EIGHT={'L71':['L71'],'L56/58':['L56','L58'],'L91':['L91'],'L110':[],'L48/49':['L48-L49'],'L117':['L117'],'L118':['L118'],'L138':['L138']}
tiles=[]
for name in EIGHT:
    cx,cy=cent[name]; w=h=36; k=8
    x0,y0=int(round(cx))-w//2,int(round(cy))-h//2
    c=a[y0-Y0:y0-Y0+h, x0-X0:x0-X0+w]
    lo,hi=np.percentile(a[100:260,100:260],1),np.percentile(a[100:260,100:260],99)   # one stretch for all tiles
    c=np.clip((c-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    big=cv2.resize(c,(w*k,h*k),interpolation=cv2.INTER_CUBIC)
    t1=Image.fromarray(big).convert('RGB'); t2=t1.copy(); dr=ImageDraw.Draw(t2)
    T=lambda x,z:((img(x,z)[0]-x0+0.5)*k,(img(x,z)[1]-y0+0.5)*k)
    if name=='L110':
        X,Y=T(0,0); r=2.31/s*k; dr.ellipse([X-r,Y-r,X+r,Y+r],outline=(255,40,40),width=1)
    for i in EIGHT[name]:
        pp=[T(*q) for q in E[i]['geometry']['points']]; dr.line(pp+[pp[0]],fill=(255,40,40),width=1)
    # 5 m scale bar
    L=5/s*k; ImageDraw.Draw(t1).line([(8,w*k-10),(8+L,w*k-10)],fill=(255,255,0),width=3)
    for t in (t1,t2): ImageDraw.Draw(t).text((6,4),name,fill=(255,255,0))
    tiles.append((t1,t2))
W=tiles[0][0].width
cv=Image.new('RGB',(4*(2*W+6)+30, 2*(W+6)),'white')
for i,(t1,t2) in enumerate(tiles):
    col=i%4; row=i//4
    X=col*(2*W+16); Y=row*(W+6)
    cv.paste(t1,(X,Y)); cv.paste(t2,(X+W+2,Y))
cv.save('judge_tiles.png'); print(cv.size)
for i,(t1,t2) in enumerate(tiles):
    pair=Image.new('RGB',(2*W+4,W),'white'); pair.paste(t1,(0,0)); pair.paste(t2,(W+4,0)); pair.save(f'jt_{i}_{list(EIGHT)[i].replace("/","-")}.png')
