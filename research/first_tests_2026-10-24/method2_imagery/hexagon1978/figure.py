import json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}
cp=json.load(open('cp_fit.json')); s=cp['m_per_px']; th=np.radians(cp['theta_deg']); tx,ty=cp['L110_px']
a=np.array(Image.open('F007_c_ruin_29180_19840.png')).astype(np.float32); X0,Y0=29180,19840
c_,sn=np.cos(th),np.sin(th)
img=lambda x,z:(tx+(c_*x+sn*z)/s, ty+(-sn*x+c_*z)/s)
x0,y0,w,h,k=29302,19950,128,118,5
c=a[y0-Y0:y0-Y0+h, x0-X0:x0-X0+w]
lo,hi=np.percentile(c,1),np.percentile(c,99); c=np.clip((c-lo)/(hi-lo)*255,0,255).astype(np.uint8)
big=cv2.resize(c,(w*k,h*k),interpolation=cv2.INTER_CUBIC)
L=Image.fromarray(big).convert('RGB'); R=L.copy()
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
except: F=Fs=ImageFont.load_default()
T=lambda x,z:((img(x,z)[0]-x0+0.5)*k,(img(x,z)[1]-y0+0.5)*k)
RED,ORG,GRY=(235,30,30),(255,150,0),(80,170,255)
J={'L71':RED,'L56/58':RED,'L91':RED,'L110':RED,'L48/49':ORG,'L117':ORG,'L118':ORG,'L138':GRY}
IDS={'L71':['L71'],'L56/58':['L56','L58'],'L91':['L91'],'L48/49':['L48-L49'],'L117':['L117'],'L118':['L118'],'L138':['L138']}
OFF={'L71':(-46,4),'L56/58':(-10,22),'L91':(-58,0),'L110':(-60,-30),'L48/49':(16,-10),'L117':(10,10),'L118':(-56,-26),'L138':(18,-8)}
dr=ImageDraw.Draw(R)
for name,col in J.items():
    if name=='L110':
        cx,cy=T(0,0); r=2.31/s*k; dr.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=2); pts=[(cx,cy)]
    else:
        pts=[]
        for i in IDS[name]:
            pp=[T(*q) for q in E[i]['geometry']['points']]; dr.line(pp+[pp[0]],fill=col,width=2); pts+=pp
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    ox,oy=OFF[name]
    dr.text((cx+ox+1,cy+oy+1),name,fill=(0,0,0),font=F); dr.text((cx+ox,cy+oy),name,fill=col,font=F)
for im in (L,R):
    g=ImageDraw.Draw(im); bar=20/s*k
    g.rectangle([14,h*k-34,14+bar+8,h*k-8],fill=(0,0,0))
    g.line([(18,h*k-14),(18+bar,h*k-14)],fill=(255,255,255),width=4)
    g.text((18,h*k-32),'20 m',fill=(255,255,255),font=Fs)
# legend on R
g=ImageDraw.Draw(R); y=10
g.rectangle([w*k-190,6,w*k-6,74],fill=(0,0,0))
for txt,col in (('shows',RED),('possible (offset ≤3 m)',ORG),('does not show',GRY)):
    g.line([(w*k-182,y+9),(w*k-160,y+9)],fill=col,width=3); g.text((w*k-154,y),txt,fill=(255,255,255),font=Fs); y+=21
out=Image.new('RGB',(2*w*k+12,h*k),(255,255,255)); out.paste(L,(0,0)); out.paste(R,(w*k+12,0))
out.save('hexagon1978_qumran_pools.png'); print(out.size)
