"""Segment Puech's facsimile (clean line drawing) into components, estimate letter height,
estimate skew and cluster components into text lines. Writes work/fac/lines_colNN.png
(each line's components drawn in one colour, line index at left) and data/fac_components_colNN.json.
Usage: python3 -I 04_fac_lines.py [cols...]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
from scipy.signal import find_peaks
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
os.makedirs(os.path.join(BASE,'work','fac'), exist_ok=True)
manual = {}
mp = os.path.join(BASE,'data','manual_lines.json')
if os.path.exists(mp): manual = json.load(open(mp))
cols = [int(c) for c in sys.argv[1:]] or list(range(1,13))
txt = load_text()
nlines = {c['c']: len(c['lines']) for c in txt['columns']}
PAL = [(255,80,80),(80,255,80),(80,160,255),(255,255,0),(255,0,255),(0,255,255),(255,160,0)]
for col in cols:
    f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
    lab, n = ndi.label(f, structure=np.ones((3,3)))
    objs = ndi.find_objects(lab)
    areas = ndi.sum(f, lab, range(1,n+1))
    comps = []
    for i,(sl,a) in enumerate(zip(objs, areas)):
        y0,y1 = sl[0].start, sl[0].stop; x0,x1 = sl[1].start, sl[1].stop
        comps.append(dict(id=i+1, x0=x0,x1=x1,y0=y0,y1=y1, area=int(a)))
    hs = np.array([c['y1']-c['y0'] for c in comps if c['area']>=40])
    Lh = float(np.median(hs))
    keep = []
    # dashed rulings: chains (>=3) of small dashes aligned vertically or horizontally
    small = [c for c in comps if c['area'] <= 60 and max(c['x1']-c['x0'], c['y1']-c['y0']) <= 26]
    dash_ids = set()
    for c in small:
        cxs, cys = (c['x0']+c['x1'])/2, (c['y0']+c['y1'])/2
        v = sum(1 for o in small if o is not c and abs((o['x0']+o['x1'])/2-cxs) <= 6 and abs((o['y0']+o['y1'])/2-cys) <= 45)
        h_ = sum(1 for o in small if o is not c and abs((o['y0']+o['y1'])/2-cys) <= 6 and abs((o['x0']+o['x1'])/2-cxs) <= 45)
        if v >= 2 or h_ >= 2: dash_ids.add(c['id'])
    # vertical rulings: cluster dash x-centres, fit x(y), remove narrow components on them
    rulings = []
    dl = sorted([c for c in comps if c['id'] in dash_ids and (c['y1']-c['y0']) >= (c['x1']-c['x0'])], key=lambda c: (c['x0']+c['x1'])/2)
    cl = []
    for c in dl:
        x = (c['x0']+c['x1'])/2
        if cl and x - (cl[-1][-1]['x0']+cl[-1][-1]['x1'])/2 <= 12: cl[-1].append(c)
        else: cl.append([c])
    for g_ in cl:
        if len(g_) >= 6:
            ys_ = np.array([(c['y0']+c['y1'])/2 for c in g_]); xs_ = np.array([(c['x0']+c['x1'])/2 for c in g_])
            rulings.append(np.polyfit(ys_, xs_, 1).tolist())
    def on_ruling(c):
        if (c['x1']-c['x0']) > 10: return False
        cy_ = (c['y0']+c['y1'])/2; cx_ = (c['x0']+c['x1'])/2
        return any(abs(np.polyval(r, cy_) - cx_) <= 7 for r in rulings)
    for c in comps:
        h = c['y1']-c['y0']; w = c['x1']-c['x0']
        if c['area'] < 12: continue
        if c['id'] in dash_ids: continue
        if on_ruling(c): continue
        if h > 2.0*Lh or w > 2.5*Lh: continue           # rulings, lacuna outlines, cracks
        keep.append(c)
    # restrict to column region if manual bounds given
    mb = manual.get(str(col), {})
    if 'x_range' in mb:
        xa, xb = mb['x_range']
        keep = [c for c in keep if xa <= (c['x0']+c['x1'])/2 <= xb]
    cx = np.array([(c['x0']+c['x1'])/2 for c in keep]); cy = np.array([(c['y0']+c['y1'])/2 for c in keep])
    wts = np.array([c['area'] for c in keep], float)
    xc = np.median(cx)
    bestS=None
    for sl in np.arange(-0.08,0.0801,0.0025):
        yp = cy - sl*(cx-xc)
        hgm,_ = np.histogram(yp, bins=np.arange(0, f.shape[0]+5, 4), weights=wts)
        hgm = ndi.gaussian_filter1d(hgm.astype(float), 1.5)
        sc = (hgm**2).sum()
        if bestS is None or sc>bestS[0]: bestS=(sc, sl)
    slope = mb.get('slope', bestS[1])
    yp = cy - slope*(cx-xc)
    hgm,edges = np.histogram(yp, bins=np.arange(0, f.shape[0]+5, 2), weights=wts)
    hgm = ndi.gaussian_filter1d(hgm.astype(float), Lh*0.15/2)
    pk,pr = find_peaks(hgm, distance=max(3,int(Lh*0.55/2)), prominence=hgm.max()*0.02)
    N = mb.get('n_lines', nlines[col])
    order = np.argsort(-pr['prominences'])[:N]          # keep the N most prominent peaks
    peaks = sorted((edges[pk[order]]+1).tolist())
    if 'peaks' in mb: peaks = mb['peaks']
    peaks = np.array(sorted(peaks))
    # line model y = a + b*(x-xc); start with global slope, refine per line (robust LSQ, slope clipped)
    A = peaks.astype(float).copy(); B = np.full(len(A), slope)
    anchors = {int(k): v for k,v in mb.get('anchors', {}).items()}   # 1-based line -> [[x,y],[x,y]]
    def apply_anchors():
        for k,((xa_,ya_),(xb_,yb_)) in anchors.items():
            B[k-1] = (yb_-ya_)/(xb_-xa_); A[k-1] = ya_ + B[k-1]*(xc-xa_)
    apply_anchors()
    W_ = cx.max()-cx.min()
    for it in range(4):
        dist = np.abs(cy[:,None] - (A[None,:] + B[None,:]*(cx[:,None]-xc)))
        lid = np.argmin(dist, axis=1)
        if it == 3: break
        for k in range(len(A)):
            m = lid==k
            if m.sum() >= 6 and (cx[m].max()-cx[m].min()) > 0.3*W_:
                X = cx[m]-xc; Y = cy[m]
                bb = np.polyfit(X, Y, 1, w=np.sqrt(wts[m]))
                r = np.abs(Y - np.polyval(bb, X)); keepm = r < max(8, 2.5*np.median(r))
                bb = np.polyfit(X[keepm], Y[keepm], 1, w=np.sqrt(wts[m][keepm]))
                B[k] = np.clip(bb[0], slope-0.03, slope+0.03); A[k] = np.average(Y[keepm]-B[k]*X[keepm], weights=wts[m][keepm])
        apply_anchors()
    for c,l in zip(keep, lid):
        c['line'] = int(l)
    out = dict(col=col, rulings=rulings, Lh=Lh, slope=float(slope), xc=float(xc), peaks=peaks.tolist(), line_a=A.tolist(), line_b=B.tolist(), n_detected=len(peaks),
               n_transcription_lines=nlines[col], comps=keep)
    json.dump(out, open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json'),'w'))
    vis = Image.fromarray((f*120).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(vis)
    for c in keep:
        d.rectangle([c['x0'],c['y0'],c['x1'],c['y1']], outline=PAL[c['line']%len(PAL)], width=2)
    for i,(a_,b_) in enumerate(zip(A,B)):
        d.line([(0,a_+b_*(0-xc)),(f.shape[1], a_+b_*(f.shape[1]-xc))], fill=(90,90,90), width=1)
        d.text((5, a_+b_*(40-xc)-10), str(i+1), fill=(255,255,255), font=font)
        d.text((f.shape[1]-40, a_+b_*(f.shape[1]-40-xc)-10), str(i+1), fill=(255,255,255), font=font)
    vis.resize((vis.size[0]//2, vis.size[1]//2)).save(os.path.join(BASE,'work','fac',f'lines_col{col:02d}.png'))
    print(col, 'Lh', Lh, 'slope', round(float(slope),4), 'detected lines', len(peaks), 'transcription lines', nlines[col])
