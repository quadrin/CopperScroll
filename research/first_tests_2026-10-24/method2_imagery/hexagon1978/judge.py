import json, numpy as np, cv2
from PIL import Image, ImageDraw
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}
cp=json.load(open('cp_fit.json')); s=cp['m_per_px']; th=np.radians(cp['theta_deg']); tx,ty=cp['L110_px']
a=np.array(Image.open('F007_c_ruin_29180_19840.png')).astype(np.float32); X0,Y0=29180,19840
c_,sn=np.cos(th),np.sin(th)
img=lambda x,z:(tx+(c_*x+sn*z)/s, ty+(-sn*x+c_*z)/s)
EIGHT={'L71':['L71'],'L56/58':['L56','L58'],'L91':['L91'],'L110':[],'L48/49':['L48-L49'],'L117':['L117'],'L118':['L118'],'L138':['L138']}
x0,y0,w,h,k=29300,19945,130,130,6
c=a[y0-Y0:y0-Y0+h, x0-X0:x0-X0+w]
lo,hi=np.percentile(c,1),np.percentile(c,99); c=np.clip((c-lo)/(hi-lo)*255,0,255).astype(np.uint8)
big=cv2.resize(c,(w*k,h*k),interpolation=cv2.INTER_CUBIC)
T=lambda x,z:((img(x,z)[0]-x0+0.5)*k,(img(x,z)[1]-y0+0.5)*k)
clean=Image.fromarray(big).convert('RGB'); ov=clean.copy(); dr=ImageDraw.Draw(ov); dc=ImageDraw.Draw(clean)
cent={}
for name,ids in EIGHT.items():
    if name=='L110':
        cx,cy=T(0,0); r=2.31/s*k; dr.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(255,40,40),width=2); pts=[(cx,cy)]
    else:
        pts=[]
        for i in ids:
            pp=[T(*q) for q in E[i]['geometry']['points']]; dr.line(pp+[pp[0]],fill=(255,40,40),width=2); pts+=pp
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    cent[name]=(cx,cy)
    dr.text((cx+14,cy-14),name,fill=(255,60,60))
    # clean version: four short ticks 40 px out from the centre, label offset
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        dc.line([(cx+dx*44,cy+dy*44),(cx+dx*60,cy+dy*60)],fill=(255,40,40),width=2)
    dc.text((cx+46,cy-58),name,fill=(255,60,60))
ov.save('judge_overlay.png'); clean.save('judge_clean.png')
json.dump({n:[float(v[0])/6+x0-0.5,float(v[1])/6+y0-0.5] for n,v in cent.items()},open('pool_centres_px.json','w'),indent=1)
print(json.load(open('pool_centres_px.json')))
