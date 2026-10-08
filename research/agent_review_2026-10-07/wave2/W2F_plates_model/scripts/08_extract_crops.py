"""Extract fixed-size, scale-normalised letter windows from the copy photographs.

Window: centred on (x = stroke-centroid of the letter in the registered facsimile, mapped to the
photo; y = centre of the letter's facsimile box, mapped). Size 1.0 H wide x 1.25 H high, where H =
per-column median photo height of full-height letters (בכהחתרמ). Resampled to 32 x 40 px.
Pixel values: grayscale / Gaussian background (sigma = 0.5 H), then per-window z-score.
For each letter: the original window + NAUG augmented windows (shift U(-0.1,0.1) H in x and y,
scale U(0.92,1.08), rotation U(-4,4) deg), RNG seed 20261006.
Only the window CENTRE comes from the facsimile; window size is fixed per column, so the drawn
letter extent does not leak into the crop.
Usage: python3 -I 08_extract_crops.py labels.csv out_prefix
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cv2
NAUG = 8; OW, OH = 32, 40
FULL = set('בכהחתרמ')
def column_H(rows):
    H = {}
    for col in range(1,13):
        hs = [float(r['fac_h'])*float(r['scale']) for r in rows if int(r['col'])==col and r['letter'] in FULL]
        H[col] = float(np.median(hs)) if hs else None
    return H
def norm_plate(col, H):
    g = np.asarray(Image.open(copy_plate_path(col)).convert('L')).astype(np.float32)
    bg = ndi.gaussian_filter(g, 0.5*H)
    return g/(bg+1.0)
def window(img, cx, cy, H, dx=0, dy=0, sc=1.0, rot=0.0):
    # map output pixel (u,v) -> source; output centre = (OW/2, OH/2); output px size = H/32 * sc
    s = (H/OW)*sc
    th = np.deg2rad(rot)
    R = np.array([[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]])*s
    c_out = np.array([OW/2-0.5, OH/2-0.5]); c_src = np.array([cx+dx*H, cy+dy*H])
    A = np.hstack([R, (c_src - R@c_out)[:,None]])
    w = cv2.warpAffine(img, A.astype(np.float32), (OW, OH), flags=cv2.INTER_AREA | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
    w = (w - w.mean())/(w.std()+1e-6)
    return w
if __name__ == '__main__':
    lab, outp = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(lab, encoding='utf-8')))
    H = column_H(rows)
    rng = np.random.default_rng(20261006)
    X = np.zeros((len(rows), 1+NAUG, OH, OW), np.float32)
    cache = {}
    for i,r in enumerate(rows):
        col = int(r['col'])
        if col not in cache: cache = {col: norm_plate(col, H[col])}
        img = cache[col]
        cx, cy = float(r['px']), float(r['pby'])
        X[i,0] = window(img, cx, cy, H[col])
        for k in range(NAUG):
            X[i,1+k] = window(img, cx, cy, H[col], dx=rng.uniform(-.1,.1), dy=rng.uniform(-.1,.1), sc=rng.uniform(.92,1.08), rot=rng.uniform(-4,4))
    np.save(outp + '_X.npy', X)
    json.dump({str(k): v for k,v in H.items()}, open(outp + '_H.json','w'), indent=1)
    print(X.shape, H)
