"""EXPLORATORY (training cuts only; never cuts 7 or 8 before the freeze).

python3 -I explore.py CUT SCALE [VIEWS]
Prints registration diagnostics, pitch and per-band numbers; writes diagnostic overlays to SP/products/C2.
"""
import sys, os
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copper as C, fetch

FORBIDDEN = {7, 8}

cut = int(sys.argv[1]); scale = float(sys.argv[2])
views = sys.argv[3] if len(sys.argv) > 3 else 'LCR'
assert cut not in FORBIDDEN, 'cuts 7 and 8 are reserved for the confirmatory run'
fr = C.load_cut(cut, scale, f'exploratory training cut {cut}')
for v in views:
    if 'R' + v + 'T' not in fr or 'R' + v + 'B' not in fr:
        continue
    R = C.relief_view(fr['R' + v + 'T'], fr['R' + v + 'B'], scale)
    if R is None:
        print(v, 'no strip'); continue
    px = R['px_cm']
    kp, ap, bl, prof = C.bands(R['E'], R['mask'], px)
    print(f"view {v} win={R['win']} reg={R['reg']} pitch_cm={(kp or 0) / px:.3f} acf={ap}")
    for b in bl:
        cm = C.band_columns(R['E'], R['GX'], R['mask'], b, px)
        print(f"  y={b['y']:5d} ext_cm={b['fwhm_px'] / px:.2f} pitch_cm={b['pitch_px'] / px:.2f} h={b['h']:.3f} con={b['contrast']:.2f} "
              + ' '.join(f'{k}={v:.3f}' for k, v in cm.items()))
    S = R['S']; x0, x1, y0, y1 = R['win']
    sc = np.percentile(np.abs(S[y0:y1, x0:x1]), 99)
    vis = np.clip(0.5 + 0.5 * S / sc, 0, 1)
    img = (np.dstack([vis] * 3) * 255).astype(np.uint8)
    for b in bl:
        cv2.line(img, (x0, b['y']), (x1, b['y']), (255, 0, 0), 1)
        cv2.line(img, (x0, b['y_ext0']), (x1, b['y_ext0']), (0, 200, 0), 1)
        cv2.line(img, (x0, b['y_ext1']), (x1, b['y_ext1']), (0, 200, 0), 1)
    cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 1)
    crop = img[:, max(0, x0 - 40):x1 + 40]
    out = os.path.join(fetch.PROD, f'expl_cut{cut}_{v}_s{scale:g}_S_overlay.png')
    cv2.imwrite(out, crop[..., ::-1])
    print(out)
