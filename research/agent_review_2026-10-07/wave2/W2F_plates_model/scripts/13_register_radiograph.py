"""Locate a radiograph strip on the copy photograph of the same column (for crop placement only).
Both images -> stroke-energy maps (|high-pass|, blurred); coarse isotropic scale search
(0.70-1.30) x small rotations (-4..4 deg) with FFT cross-correlation at 1/2 size; report best
transform (radiograph px -> copy px) and normalised peak. Not used by the model.
Usage: python3 -I 13_register_radiograph.py col radiograph_file [more files]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cv2
def energy(g, s=4):
    hp = g - ndi.gaussian_filter(g, s*1.5)
    return ndi.gaussian_filter(np.abs(hp), s/2)
def norm(a): return ((a-a.mean())/(a.std()+1e-9)).astype(np.float32)
col = int(sys.argv[1]); files = sys.argv[2:]
g = load_gray(copy_plate_path(col))
D = 2
Ec = norm(cv2.resize(energy(g).astype(np.float32), None, fx=1/D, fy=1/D, interpolation=cv2.INTER_AREA))
out = {}
op = os.path.join(BASE,'data','radiograph_registration.json')
if os.path.exists(op): out = json.load(open(op))
for fn in files:
    r = np.asarray(Image.open(os.path.join(BASE,'plates','png',fn)).convert('L')).astype(np.float32)
    Er0 = energy(r).astype(np.float32)
    best = None
    for flip in (False, True):
        Erf = Er0[:, ::-1] if flip else Er0
        for s in np.arange(0.70, 1.31, 0.03):
            for rot in (-4,-2,0,2,4):
                h, w = Erf.shape
                M = cv2.getRotationMatrix2D((w/2, h/2), rot, s/D)
                cos, sin = abs(M[0,0]), abs(M[0,1]); nw = int(h*sin + w*cos)+2; nh = int(h*cos + w*sin)+2
                M[0,2] += nw/2 - w/2; M[1,2] += nh/2 - h/2
                R = cv2.warpAffine(Erf, M, (nw, nh))
                mask = cv2.warpAffine(np.ones_like(Erf), M, (nw, nh)) > 0.5
                Rn = np.zeros_like(R); Rn[mask] = (R[mask]-R[mask].mean())/(R[mask].std()+1e-9)
                H_ = Ec.shape[0]+nh; W_ = Ec.shape[1]+nw
                A = np.zeros((H_,W_),np.float32); B = np.zeros((H_,W_),np.float32)
                A[:Ec.shape[0],:Ec.shape[1]] = Ec; B[:nh,:nw] = Rn
                cc = np.fft.irfft2(np.fft.rfft2(A)*np.conj(np.fft.rfft2(B)), s=(H_,W_))
                k = np.unravel_index(np.argmax(cc), cc.shape); v = cc[k]/mask.sum()
                if best is None or v > best[0]:
                    dy, dx = k; dy = dy if dy < H_/2 else dy-H_; dx = dx if dx < W_/2 else dx-W_
                    # full transform radiograph(full px) -> copy(full px)
                    A3 = np.vstack([M,[0,0,1]]); T = np.array([[1,0,dx],[0,1,dy],[0,0,1]]); S = np.diag([D,D,1])
                    Fl = np.array([[-1,0,w-1],[0,1,0],[0,0,1]]) if flip else np.eye(3)
                    full = S @ T @ A3 @ Fl
                    best = (float(v), float(s), rot, flip, full[:2].tolist())
    out[fn] = dict(col=col, score=best[0], scale=best[1], rot=best[2], flip=best[3], A_rad2copy=best[4])
    print(fn, round(best[0],3), round(best[1],2), best[2], best[3], flush=True)
json.dump(out, open(op,'w'), indent=1)
