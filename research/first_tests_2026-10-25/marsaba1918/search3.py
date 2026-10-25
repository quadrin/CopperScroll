import numpy as np, render, time, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.optimize import minimize
W,H=240,165
ph=np.asarray(Image.open('frame_area.png').resize((W,H),Image.LANCZOS),float)
def hp(a,s=6):
    a=a-gaussian_filter(a,s); return (a-a.mean())/(a.std()+1e-9)
P=hp(ph)
def score(cam,step=3):
    img,cov=render.render(cam,W,H,step=step)
    if cov<0.85: return -1
    return float((hp(img)*P).mean())
rng=np.random.default_rng(int(sys.argv[1]))
cands=[]
t=time.time()
for i in range(6000):
    hf=rng.uniform(36,46)
    cam=[rng.uniform(-14000,2000),rng.uniform(-8000,10000),rng.uniform(2600,3200),rng.uniform(205,265),rng.uniform(18,40),rng.uniform(-5,5),W/2/np.tan(np.radians(hf/2))]
    cands.append((score(cam),cam))
cands.sort(key=lambda x:-x[0]); print('rand',time.time()-t,[round(c[0],3) for c in cands[:8]],flush=True)
res=[]
for s0,c0 in cands[:12]:
    f=lambda x: -score(list(x),step=2)
    r=minimize(f,c0,method='Nelder-Mead',options={'maxiter':300})
    res.append((-r.fun,list(r.x))); print(round(s0,3),'->',round(-r.fun,3),[round(float(v),1) for v in r.x],flush=True)
res.sort(key=lambda x:-x[0]); np.save(f'search3_{sys.argv[1]}.npy',np.array([[s,*c] for s,c in res]))
