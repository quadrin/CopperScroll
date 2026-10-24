import json, numpy as np, cv2, sys
from PIL import Image
exec(open('fit_plan.py').read().split('best=[]')[0])
dark=cv2.GaussianBlur(255-a,(0,0),0.8)
# local high-pass so broad tone does not dominate
dark=dark-cv2.GaussianBlur(dark,(0,0),6)
for name,I in (('edge',img),('dark',dark.astype(np.float32))):
    best=[]
    for s in np.arange(0.60,1.30,0.02):
        for thd in np.arange(-6,22,1.0):
            t,mask=render(s,np.radians(thd))
            r=cv2.matchTemplate(I,t,cv2.TM_CCOEFF_NORMED,mask=mask)
            ax,ay=29346-X0-40,19999-Y0-60
            sub=r[ay-25:ay+26,ax-25:ax+26]
            j=np.unravel_index(np.nanargmax(sub),sub.shape)
            best.append((round(float(sub[j]),4),round(float(s),3),float(thd),int(ax-25+j[1])+40+X0,int(ay-25+j[0])+60+Y0))
    best.sort(reverse=True)
    print(name); [print('  ',b) for b in best[:8]]
    # best per scale
    bys={}
    for b in best:
        bys.setdefault(b[1],b)
    print('  per scale:', [ (k,v[0],v[2],v[3],v[4]) for k,v in sorted(bys.items())][::3])
