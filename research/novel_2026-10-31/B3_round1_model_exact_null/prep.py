"""Step 1 (EXPLORATORY tooling): register every recto frame of a cut to one reference frame,
rectify the strip to vertical, and save a private multi-light stack.
Inputs: USC public previews in images/previews/ (1988 WSRP film, ~1000 px). Outputs: private npz
stacks in /root/novel/private_outputs/B/stacks/ (never committed) + public numbers JSON."""
import cv2, numpy as np, csv, json, sys, os, hashlib
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PRIV = '/root/novel/private_outputs/B/stacks'
idx = list(csv.DictReader(open(f'{REPO}/research/sources/usc_copper_scroll_images/index.csv')))
def path(u):
    for d in ('cuts-01-10', 'original-scroll-remaining'):
        p = f'{REPO}/images/previews/{d}/{u}.jpg'
        if os.path.exists(p): return p
cl = cv2.createCLAHE(3.0, (8, 8)); sift = cv2.SIFT_create(nfeatures=6000, contrastThreshold=0.01)
SKIP = ('edge', 'frg', 'fragment', 'sd light', 'bot ctr', 'top ctr')
def frames(cut):
    out = []
    for r in idx:
        if r['cut'] == str(cut) and r['side'] == 'Recto' and r['item_type'].startswith('original'):
            lab = r['lighting_as_titled'].strip()
            if not lab or any(s in lab for s in SKIP): continue
            if path(r['uc_identifier']): out.append((r['uc_identifier'], lab, r['film'][:3]))
    return out
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def register(cut):
    fr = frames(cut)
    if len(fr) < 2: return None
    ims = {u: cv2.imread(path(u), 0) for u, _, _ in fr}
    F = {u: sift.detectAndCompute(cl.apply(ims[u]), None) for u in ims}
    # reference = frame with most total matches to the others
    def match(a, b, rot=0):
        ka, da = F[a]; kb, db = F[b]
        if da is None or db is None: return 0, None
        m = cv2.BFMatcher().knnMatch(da, db, k=2)
        g = [x for x, y in (p for p in m if len(p) == 2) if x.distance < 0.75 * y.distance]
        if len(g) < 12: return 0, None
        p1 = np.float32([ka[x.queryIdx].pt for x in g]); p2 = np.float32([kb[x.trainIdx].pt for x in g])
        H, inl = cv2.findHomography(p1, p2, cv2.RANSAC, 3.0)
        if H is None: return 0, None
        return int(inl.sum()), H
    us = list(ims)
    M = {}
    for i, a in enumerate(us):
        for b in us[i+1:]:
            n, H = match(a, b); M[(a, b)] = (n, H)
            M[(b, a)] = (n, np.linalg.inv(H) if H is not None else None)
    ref = max(us, key=lambda a: sum(M[(a, b)][0] for b in us if b != a))
    ref_im = ims[ref]; h, w = ref_im.shape
    reg = []; stack = []; labs = []
    for u, lab, film in fr:
        if u == ref: n, H = 9999, np.eye(3)
        else: n, H = M[(u, ref)]
        if n < 40 or H is None:
            reg.append(dict(uc=u, light=lab, film=film, inliers=n, used=False)); continue
        wimg = cv2.warpPerspective(ims[u], H, (w, h), flags=cv2.INTER_LINEAR)
        stack.append(wimg.astype(np.float32) / 255.); labs.append((u, lab, film))
        reg.append(dict(uc=u, light=lab, film=film, inliers=n, used=True, sha256=sha(path(u))))
    # strip mask from the mean of registered frames
    mean = np.mean(stack, 0)
    b = cv2.GaussianBlur((mean * 255).astype(np.uint8), (0, 0), 3)
    _, th = cv2.threshold(b, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    n, lab_im, st, _ = cv2.connectedComponentsWithStats(th)
    # strip = tall component nearest the image centre column
    best = None
    for k in range(1, n):
        x, y, ww, hh, area = st[k]
        if hh < 0.5 * h: continue
        cx = x + ww / 2; score = area - 3 * abs(cx - w / 2) * hh
        if best is None or score > best[0]: best = (score, k)
    if best is None: return dict(cut=cut, error='no strip found', reg=reg)
    mask = (lab_im == best[1]).astype(np.uint8)
    ys, xs = np.nonzero(mask)
    # fit strip axis: x as a function of y (centre line)
    rows = np.unique(ys); cxs = np.array([xs[ys == r].mean() for r in rows])
    slope, icpt = np.polyfit(rows, cxs, 1)
    ang = np.degrees(np.arctan(slope))
    Rm = cv2.getRotationMatrix2D((w / 2, h / 2), -ang, 1.0)
    rot = [cv2.warpAffine(s, Rm, (w, h)) for s in stack]
    mrot = cv2.warpAffine(mask * 255, Rm, (w, h)) > 127
    ys, xs = np.nonzero(mrot)
    # robust width: per-row extents, use 10-90 pct of left/right edges
    rows = np.unique(ys)
    L = np.array([xs[ys == r].min() for r in rows]); Rr = np.array([xs[ys == r].max() for r in rows])
    x0, x1 = int(np.percentile(L, 50)), int(np.percentile(Rr, 50))
    y0, y1 = int(rows.min()), int(rows.max())
    crop = np.stack([r[y0:y1, x0:x1] for r in rot])
    mcrop = mrot[y0:y1, x0:x1]
    np.savez_compressed(f'{PRIV}/cut{cut:02d}.npz', stack=crop, mask=mcrop,
                        labels=np.array([l[1] for l in labs]), ucs=np.array([l[0] for l in labs]),
                        films=np.array([l[2] for l in labs]))
    return dict(cut=cut, ref=ref, n_frames=len(fr), n_used=len(stack), strip_angle_deg=round(float(ang), 3),
                crop_wh=[int(x1 - x0), int(y1 - y0)], reg=reg)
if __name__ == '__main__':
    cuts = [int(c) for c in sys.argv[1:]]
    res = {}
    for c in cuts:
        r = register(c); res[c] = r
        print(c, None if r is None else {k: v for k, v in r.items() if k != 'reg'}, flush=True)
    out = os.path.join(os.path.dirname(__file__), 'prep_registration.json')
    old = json.load(open(out)) if os.path.exists(out) else {}
    old.update({str(k): v for k, v in res.items()})
    json.dump(old, open(out, 'w'), indent=1)
