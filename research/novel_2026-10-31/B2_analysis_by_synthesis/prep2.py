"""B2 step 1 (tooling): full-resolution strip crops per cut and per light frame.

Reads the USC 1988 WSRP full-resolution TIFF copies in the private bucket through hexview.py
(never a custom reader). For each cut present in the bucket:
  1. frames used = lighting codes RCT RLT RRT RCB RLB RRB RT RB (raking centre/left/right x top/bottom;
     RT/RB only on cuts 4, 17, 21). Other codes (FRS, RET, REB, RFR, RBC, RCS, RTC) are not used.
  2. strip columns from a 1/16 overview: foreground (copper brighter than the black velvet by > 22 grey
     levels above the 5th percentile) in at least 72 % of the rows. The colour card and ruler are shorter
     than the strip, so they drop out even where they touch it.
  3. strip box read at WORK scale (0.5 of full resolution, about 77 px per cm, letters 50-75 px high).
  4. strip axis from the box mask's second moments; frame rotated so the strip is vertical and cropped.
Cross-frame registration is NOT done: SIFT on the corrosion texture found 0-108 inliers between
lights, and silhouette ECC reached only 0.82-0.86 for side lights (the shadowed edge moves).
Each light frame is therefore modelled on its own (scores are summed over frames).
Outputs: private crops SP/products/B2/strips/ctNN.npz (never committed) and public numbers
prep2_frames.json (frame keys, tile sizes, boxes, angles, crop sizes, sha256 of the npz).
"""
import sys, os, json, hashlib, time
import numpy as np, cv2
SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
sys.path.insert(0, SP + '/tools/hexview')
import hexview as hv
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = SP + '/products/B2/strips'
WORK = 0.5
CODES = ['RCT', 'RLT', 'RRT', 'RCB', 'RLB', 'RRB', 'RT', 'RB']
CUTS = [2, 3, 4, 5, 6, 7, 8, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23]


def frames(cut):
    ks = [k for k in hv.index()['items'] if k.startswith(f'usc:DSS_3Q15_CT{cut}_')]
    by = {k.split('_')[3]: k for k in ks}
    return [(c, by[c]) for c in CODES if c in by]


def gray(a):
    return a if a.ndim == 2 else cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)


def fg(g, sig):
    b = cv2.GaussianBlur(g, (0, 0), sig)
    return b > np.percentile(b, 5) + 22


def strip_box(key):
    _, _, t = hv.tile_rec(key, '-')
    s = 1 / 16
    m = fg(gray(hv.overview(key, '-', scale=s)), 1.5)
    frac = m.mean(0)
    cols = np.nonzero(frac >= 0.72 * frac.max())[0]
    runs = np.split(cols, np.nonzero(np.diff(cols) > 2)[0] + 1)
    run = max(runs, key=len)
    x0, x1 = run[0], run[-1] + 1
    rows = np.nonzero(m[:, x0:x1].mean(1) > 0.3)[0]
    y0, y1 = rows[0], rows[-1] + 1
    mg = 8
    return [int(max(0, (x0 - mg) / s)), int(max(0, (y0 - mg) / s)), int(min(t['width'], (x1 + mg) / s)),
            int(min(t['height'], (y1 + mg) / s))]


def rectify(a):
    m = fg(a, 4)
    frac = m.mean(0)
    cols = np.nonzero(frac >= 0.35 * frac.max())[0]
    ys, xs = np.nonzero(m[:, cols.min():cols.max() + 1]); xs = xs + cols.min()
    c = np.cov(np.vstack([xs, ys]).astype(float))
    ev, evec = np.linalg.eigh(c)
    v = evec[:, 1]
    ang = float(np.degrees(np.arctan2(v[0], v[1])))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    h, w = a.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -ang, 1.0)
    r = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR)
    mr = fg(r, 4)
    frac = mr.mean(0)
    cols = np.nonzero(frac >= 0.35 * frac.max())[0]
    x0, x1 = cols.min(), cols.max() + 1
    rows = np.nonzero(mr[:, x0:x1].mean(1) > 0.5)[0]
    y0, y1 = rows.min(), rows.max() + 1
    return r[y0:y1, x0:x1], mr[y0:y1, x0:x1], ang


def run(cut):
    t0 = time.time()
    recs, arrs = [], {}
    for code, key in frames(cut):
        bx = strip_box(key)
        a = gray(hv.box(key, '-', *bx, scale=WORK))
        r, m, ang = rectify(a)
        _, _, t = hv.tile_rec(key, '-')
        arrs[code] = r; arrs[code + '_mask'] = m.astype(np.uint8)
        recs.append(dict(code=code, key=key, tile_wh=[t['width'], t['height']], box=bx, angle_deg=round(ang, 3),
                         crop_hw=list(r.shape)))
    os.makedirs(OUT, exist_ok=True)
    p = f'{OUT}/ct{cut:02d}.npz'
    np.savez_compressed(p, **arrs)
    return dict(cut=cut, frames=recs, work_scale=WORK, seconds=round(time.time() - t0, 1),
                npz_sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest())


if __name__ == '__main__':
    cuts = [int(x) for x in sys.argv[1:]] or CUTS
    jp = f'{HERE}/prep2_frames.json'
    allinfo = json.load(open(jp)) if os.path.exists(jp) else {}
    for c in cuts:
        info = run(c)
        allinfo[str(c)] = info
        print(c, [(r['code'], r['crop_hw'], r['angle_deg']) for r in info['frames']], info['seconds'], flush=True)
        json.dump(allinfo, open(jp, 'w'), indent=1)
