"""Register the b&w PS reference frame to the colour PS reference frame of the same cut (SIFT affine,
5-fold CV residual). Used as an independent check of the cut->column mapping: the b&w and colour
films were mapped to the column separately, so their mappings must agree once composed with this."""
import sys, os, json, glob
import numpy as np, cv2
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps_lib as P
out = {}
for f in sorted(glob.glob(os.path.join(P.PRIVATE, 'ps_cut*_bla.npz'))):
    cut = int(os.path.basename(f)[6:8])
    fc = f.replace('_bla', '_col')
    if not os.path.exists(fc) or cut >= 19:
        continue
    rb = str(np.load(f)['ref']); rc = str(np.load(fc)['ref'])
    gb, gc = P.load_gray(rb), P.load_gray(rc)
    mb, mc = P.strip_mask2(gb), P.strip_mask2(gc)
    best = None
    for rot in (0, 2):
        g = np.ascontiguousarray(np.rot90(gb, rot)); m = np.ascontiguousarray(np.rot90(mb, rot))
        r = P.sift_affine(gc, mc, g, m, min_inl=15)
        if r and r['ok'] and (best is None or r['inliers'] > best[1]['inliers']):
            best = (rot, r)
    if best is None:
        out[cut] = dict(ok=False); print(cut, 'fail'); continue
    rot, r = best
    h0, w0 = gb.shape
    R = np.eye(3) if rot == 0 else np.array([[-1, 0, w0 - 1], [0, -1, h0 - 1], [0, 0, 1.0]])
    H = r['H'] @ R  # bla ref px -> col ref px
    out[cut] = dict(ok=True, bla_ref=rb, col_ref=rc, rot_deg=rot * 90, inliers=r['inliers'],
                    cv_med_px=round(r['cv_med_px'], 3), bla_to_col=H.tolist())
    print(cut, rb, rc, rot * 90, r['inliers'], round(r['cv_med_px'], 2))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ps_runs', 'xfilm.json'), 'w'), indent=1)
