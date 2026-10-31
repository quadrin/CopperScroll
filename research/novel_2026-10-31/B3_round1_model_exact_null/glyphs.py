"""Glyph skeletons for the forward model.
Source 1 (preferred): the hand tracing of VII 7-11 on the Jordan Museum photograph of strip 13
(registration/photo_tracing_strip13.json): stroke polylines of the scroll's own engraved letters
(column VII). Only strokes marked 'seen' and 'inferred' are both used (the tracer drew both).
Source 2 (fallback, logged): DejaVu Sans Hebrew glyphs, skeletonised, for letters the tracing lacks.
Output: glyphs.json  {letter: {"src":..., "w":width_in_Lh, "top":y_top, "bot":y_bot,
                      "polys": [[[x,y],...],...]}} with x in [0,w] (x grows to the right), y in Lh units,
body letters spanning y 0..1 (baseline at 1).
"""
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.morphology import skeletonize
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
OUT = os.path.join(os.path.dirname(__file__), 'glyphs.json')
ASC = {'ל'}; DESC = {'ק', 'ן', 'ף', 'ץ'}
ALL = list('אבגדהוזחטיכלמנסעפצקרשת') + list('ךםןףץ')
def tracing():
    d = json.load(open(f'{REPO}/registration/photo_tracing_strip13.json'))
    inst = []  # (letter, [polylines])
    for wid, w in d['words'].items():
        cur = None
        for s in w['strokes']:
            L = s['letter']; P = np.array(s['points'], float)
            if cur is not None and cur[0] == L:
                # same label: new instance if this stroke starts far left of the current instance's box
                allp = np.vstack(cur[1]); x0 = allp[:, 0].min()
                if P[:, 0].max() < x0 - 5 and L in 'כ':  # repeated letter in ככרין
                    inst.append(cur); cur = (L, [P])
                else: cur[1].append(P)
            else:
                if cur is not None: inst.append(cur)
                cur = (L, [P])
        if cur is not None: inst.append(cur)
    # reference letter height: median vertical extent of body letters
    hs = [np.ptp(np.vstack(p)[:, 1]) for L, p in inst if L not in ASC | DESC | {'י', 'ו'}]
    Lh = float(np.median(hs))
    best = {}
    for L, polys in inst:
        allp = np.vstack(polys)
        ext = np.ptp(allp[:, 1])
        if L not in best or abs(ext - Lh) < abs(np.ptp(np.vstack(best[L])[:, 1]) - Lh): best[L] = polys
    out = {}
    for L, polys in best.items():
        allp = np.vstack(polys); x0, x1 = allp[:, 0].min(), allp[:, 0].max(); y0, y1 = allp[:, 1].min(), allp[:, 1].max()
        if L in ASC: ytop_n = 1 - (y1 - y0) / Lh; off = y1 - Lh  # bottom at baseline
        else: off = y0; ytop_n = 0.0
        pl = [[[(x - x0) / Lh, (y - off) / Lh] for x, y in p] for p in polys]
        ys = [q[1] for p in pl for q in p]
        out[L] = dict(src='strip13_tracing_colVII', w=max((x1 - x0) / Lh, 0.08), top=min(ys), bot=max(ys), polys=pl)
    return out, Lh
def font_glyph(L, size=200):
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size)
    im = Image.new('L', (size * 2, size * 2), 0); ImageDraw.Draw(im).text((size // 2, size // 2), L, fill=255, font=f)
    a = np.array(im) > 128; sk = skeletonize(a)
    ys, xs = np.nonzero(sk)
    # reference body height from bet
    return xs.astype(float), ys.astype(float), a
def fonts():
    xb, yb, _ = font_glyph('ב'); Lh = np.ptp(yb); base = yb.max()
    out = {}
    for L in ALL:
        xs, ys, _ = font_glyph(L)
        if len(xs) == 0: continue
        x0 = xs.min(); top_body = base - Lh
        pts = [[[(x - x0) / Lh, (y - top_body) / Lh]] for x, y in zip(xs, ys)]  # point cloud as 1-point polylines
        yy = [(y - top_body) / Lh for y in ys]
        out[L] = dict(src='DejaVuSans_skeleton_fallback', w=float(np.ptp(xs) / Lh), top=min(yy), bot=max(yy), polys=pts)
    return out
if __name__ == '__main__':
    tr, Lh = tracing(); fo = fonts()
    g = {}
    for L in ALL:
        if L in tr: g[L] = tr[L]
        elif L in fo: g[L] = fo[L]
    # final forms not traced: ם from ם font; ן traced
    json.dump(g, open(OUT, 'w'), ensure_ascii=False)
    print('tracing Lh units', Lh)
    for L in ALL: print(L, g[L]['src'][:12], round(g[L]['w'], 2), round(g[L]['top'], 2), round(g[L]['bot'], 2))
