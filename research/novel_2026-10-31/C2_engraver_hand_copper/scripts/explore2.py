"""EXPLORATORY single-frame stroke-energy profiles (training cuts only; never 7 or 8)."""
import sys, os
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copper as C, fetch

cut = int(sys.argv[1]); scale = float(sys.argv[2]); lights = sys.argv[3].split(',')
assert cut not in (7, 8)
fr = C.load_cut(cut, scale, f'exploratory training cut {cut}', lights=lights)
px = C.PX_PER_CM_FULL * scale
for L, a in fr.items():
    F = C.frame_profile(a, px)
    if F is None:
        print(L, 'no strip'); continue
    x0, x1, y0, y1 = F['win']
    mask = np.zeros(a.shape[:2], bool); mask[y0:y1, F['xa']:F['xb']] = True
    kp, ap, bl, prof = C.bands(F['Ey'], mask, px, inner=1.0, smooth_cm=0.06)
    print(L, 'win', F['win'], 'strip h cm', round((y1 - y0) / px, 1), 'pitch', round((kp or 0) / px, 2),
          'acf', ap and round(ap, 3), 'nb', len(bl))
    print('   y:', ' '.join(f"{b['y']}" for b in bl))
    print('   h:', ' '.join(f"{b['h']:.2f}" for b in bl))
    print('   ext_cm:', ' '.join(f"{b['fwhm_px'] / px:.2f}" for b in bl))
    g = C.gray(a); vis = (np.dstack([g] * 3) * 255).astype(np.uint8).copy()
    for b in bl:
        cv2.line(vis, (F['xa'], b['y_ext0']), (F['xb'], b['y_ext0']), (0, 255, 0), 1)
        cv2.line(vis, (F['xa'], b['y_ext1']), (F['xb'], b['y_ext1']), (255, 0, 0), 1)
    cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 0, 255), 1)
    cv2.imwrite(os.path.join(fetch.PROD, f'expl2_cut{cut}_{L}_s{scale:g}.jpg'), vis[:, max(0, x0 - 30):x1 + 30, ::-1])
