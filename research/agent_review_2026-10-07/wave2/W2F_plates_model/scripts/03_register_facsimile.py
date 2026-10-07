"""Register Puech's facsimile plate (even plates) onto the copy photograph (odd plates)
for each column.
Coarse: isotropic scale grid (0.90-1.12, step 0.005) + FFT cross-correlation at 1/3 size,
        blurred photo ink map vs blurred facsimile strokes.
Fine:   OpenCV ECC (MOTION_AFFINE) at 1/2 size, Gaussian sigma 2 then 1 (half-size px).
Output: data/registration.json with A_fac2photo (2x3 affine, facsimile px -> photo px),
        overlays in work/reg/ (facsimile strokes in red on the photo)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cv2
os.makedirs(os.path.join(BASE,'work','reg'), exist_ok=True)
def norm(a):
    return ((a-a.mean())/a.std()).astype(np.float32)
def inv_aff(M):
    A = np.vstack([M,[0,0,1]]); return np.linalg.inv(A)[:2]
outp = os.path.join(BASE,'data','registration.json')
res = json.load(open(outp)) if os.path.exists(outp) else {}
cols = [int(c) for c in sys.argv[1:]] or list(range(1,13))
for col in cols:
    g = load_gray(copy_plate_path(col)); ink = ink_map(g).astype(np.float32)
    f = np.asarray(Image.open(fac_plate_path(col)).convert('L')).astype(np.float32)/255.
    D = 3
    I = norm(ndi.gaussian_filter(cv2.resize(ink,None,fx=1/D,fy=1/D,interpolation=cv2.INTER_AREA),1.5))
    best=None
    for s in np.arange(0.90,1.12,0.005):
        F = cv2.resize(f,None,fx=s/D,fy=s/D,interpolation=cv2.INTER_AREA)
        F = norm(ndi.gaussian_filter(F,1.5))
        H = max(I.shape[0],F.shape[0])+100; W = max(I.shape[1],F.shape[1])+100
        A = np.zeros((H,W)); B = np.zeros((H,W)); A[:I.shape[0],:I.shape[1]]=I; B[:F.shape[0],:F.shape[1]]=F
        cc = np.fft.irfft2(np.fft.rfft2(A)*np.conj(np.fft.rfft2(B)),s=(H,W))
        k = np.unravel_index(np.argmax(cc),cc.shape); v = cc[k]/F.size
        dy,dx = k; dy = dy if dy<H/2 else dy-H; dx = dx if dx<W/2 else dx-W
        if best is None or v>best[0]: best=(float(v),float(s),int(dx*D),int(dy*D))
    v,s,dx,dy = best
    F2P = np.array([[s,0,dx],[0,s,dy]],dtype=np.float64)
    # ECC at half size: warp maps template(photo) coords -> input(facsimile) coords
    h = 0.5
    S = np.array([[h,0,0],[0,h,0],[0,0,1]])
    P2F = inv_aff(F2P)
    Mh = (S @ np.vstack([P2F,[0,0,1]]) @ np.linalg.inv(S))[:2].astype(np.float32)
    inkh = cv2.resize(ink,None,fx=h,fy=h,interpolation=cv2.INTER_AREA)
    fh = cv2.resize(f,None,fx=h,fy=h,interpolation=cv2.INTER_AREA)
    ecc=None
    for sig in (2.0,1.0):
        try:
            ecc, Mh = cv2.findTransformECC(norm(ndi.gaussian_filter(inkh,sig)), norm(ndi.gaussian_filter(fh,sig)), Mh,
                        cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6), None, 5)
        except cv2.error as e:
            print('ECC failed', col, sig, e, flush=True)
    P2F = (np.linalg.inv(S) @ np.vstack([Mh,[0,0,1]]) @ S)[:2]
    F2P = inv_aff(P2F)
    fw = cv2.warpAffine(f, F2P.astype(np.float32), (g.shape[1], g.shape[0]), flags=cv2.INTER_LINEAR)
    vis = np.stack([np.clip((g-g.mean())/g.std()*40+128,0,255)]*3, -1)
    vis[fw>0.4] = [255,0,0]
    Image.fromarray(vis.astype(np.uint8)).save(os.path.join(BASE,'work','reg',f'reg_col{col:02d}.png'))
    res[str(col)] = dict(coarse_corr=v, coarse_scale=s, coarse_dx=dx, coarse_dy=dy,
                    ecc=float(ecc) if ecc is not None else None, A_fac2photo=F2P.tolist())
    json.dump(res, open(outp,'w'), indent=1)
    print(col, best, ecc, np.round(F2P,4).tolist(), flush=True)
