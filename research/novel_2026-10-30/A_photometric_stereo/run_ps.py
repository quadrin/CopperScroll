"""Per cut and film: register the multi-light previews, run uncalibrated photometric stereo,
integrate to relative depth. Arrays go to PRIVATE only; a numbers-only JSON per cut/film goes to ps_runs/.

Registration: within the top-lit group and within the bottom-lit group by SIFT + RANSAC affine
(frames under similar light share features); bottom group -> top group by silhouette ECC followed by
ECC on Laplacian magnitude of the group-mean images (polarity-free relief edges). Residuals: SIFT 5-fold
CV, and phase correlation of Laplacian magnitude in 4 tiles along the strip after warping.

Usage: python3 -I run_ps.py CUT [CUT ...]
"""
import sys, os, json
import numpy as np, cv2
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps_lib as P

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ps_runs')
os.makedirs(OUT, exist_ok=True); os.makedirs(P.PRIVATE, exist_ok=True)
TILE_MAX = 2.0  # px: maximum tile phase shift accepted after warping (cross-group check)


def group_of(t):
    return 'top' if 'top' in t else 'bot'


def run(cut, film):
    fr = P.frames_for(cut, film)
    rec = dict(cut=cut, film=film, n_frames=len(fr), frames=fr)
    if len(fr) < 3:
        rec['status'] = 'fewer than 3 light positions; PS not run'; return rec
    G = {u: P.load_gray(u) for u, _ in fr}
    M = {u: P.strip_mask2(G[u]) for u, _ in fr}
    T = dict(fr)
    groups = {}
    for u, t in fr:
        groups.setdefault(group_of(t), []).append(u)
    def gref_of(us):
        for u in us:
            if T[u].startswith('ctr') or T[u] in ('top light', 'bot light'):
                return u
        return us[0]
    regs = []; Hg = {}  # frame -> H to its group ref
    for gname, us in groups.items():
        r0 = gref_of(us); Hg[r0] = np.eye(3)
        for u in us:
            if u == r0: continue
            r = P.sift_affine(G[r0], M[r0], G[u], M[u])
            e = dict(frame=u, light=T[u], group=gname, to=r0, method='sift_affine')
            if r is None or not r['ok']:
                e.update(failed=True, inliers=None if r is None else r['inliers']); regs.append(e); continue
            Hg[u] = r['H']; e.update(inliers=r['inliers'], cv_med_px=round(r['cv_med_px'], 3), cv_p90_px=round(r['cv_p90_px'], 3)); regs.append(e)
    # main reference = top group ref if present
    main = 'top' if 'top' in groups else list(groups)[0]
    uref = gref_of(groups[main]); gref = G[uref]; mref = M[uref]; Hh, Ww = gref.shape
    Hs = {u: Hg[u] for u in groups[main] if u in Hg}
    for gname, us in groups.items():
        if gname == main: continue
        r0 = gref_of(us)
        mem = [u for u in us if u in Hg]
        meanimg = np.mean([cv2.warpPerspective(G[u], Hg[u], (G[r0].shape[1], G[r0].shape[0])).astype(np.float32) for u in mem], 0)
        meanref = np.mean([cv2.warpPerspective(G[u], Hs[u], (Ww, Hh)).astype(np.float32) for u in Hs], 0)
        r = P.register_sil(meanref.astype(np.uint8), mref, meanimg.astype(np.uint8), M[r0])
        e = dict(frame=r0, light=T[r0], group=gname, to=uref, method='silhouette+laplacian ECC on group means',
                 rot_deg=r['rot'], ecc_sil=round(r['ecc_sil'], 3), ecc_tex=round(r['ecc_tex'], 3), tex_drift_px=round(r['tex_drift_px'], 2))
        wm = cv2.warpPerspective(meanimg, r['H'], (Ww, Hh))
        tr = P.tile_residuals(meanref, wm, ndi.binary_erosion(mref, iterations=8))
        e['tile_shift_px'] = [round(float(np.hypot(a, b)), 2) for a, b, c in tr]
        okx = r['ecc_tex'] >= P.ECC_TEX_MIN and max(e['tile_shift_px']) <= TILE_MAX
        e['accepted'] = bool(okx); regs.append(e)
        if okx:
            for u in mem:
                Hs[u] = r['H'] @ Hg[u]
    use = [(u, T[u]) for u, _ in fr if u in Hs]
    rec.update(reference=uref, registration=regs, n_used=len(use), used=[t for _, t in use])
    if len(use) < 3:
        rec['status'] = 'fewer than 3 registered frames'; return rec
    W = {u: cv2.warpPerspective(G[u], Hs[u], (Ww, Hh), flags=cv2.INTER_LINEAR) for u, _ in use}
    # analysis mask = reference silhouette (filled), eroded; samples outside a frame's own warped
    # silhouette are zeroed so that PS treats them as shadow (excluded), not as data
    mask = ndi.binary_erosion(ndi.binary_fill_holes(mref), iterations=4)
    for u, _ in use:
        sil = cv2.warpPerspective(ndi.binary_fill_holes(M[u]).astype(np.uint8), Hs[u], (Ww, Hh), flags=cv2.INTER_NEAREST) > 0
        W[u] = np.where(sil, W[u], 0).astype(W[u].dtype)
    ph = []
    for u, t in use:
        if u == uref: continue
        tr = P.tile_residuals(W[uref], W[u], mask)
        ph.append(dict(frame=u, light=t, tile_shift_px=[round(float(np.hypot(a, b)), 2) for a, b, c in tr],
                       tile_response=[round(c, 3) for a, b, c in tr]))
    Is = [P.to_linear(W[u]) for u, _ in use]
    az = [P.TITLE_AZ[t] for _, t in use]
    try:
        _, _, _, diag = P.uncalibrated_ps(Is, mask, az, [0] * len(use))  # diagnostic only
    except Exception as ex:
        diag = dict(error=str(ex)[:200])
    N, alb, L, tdiag = P.titled_ps(Is, mask, az)
    diag['titled'] = tdiag
    z = P.frankot_chellappa(N, mask)
    np.savez_compressed(os.path.join(P.PRIVATE, f'ps_cut{cut:02d}_{film}.npz'), N=N.astype(np.float32), albedo=alb.astype(np.float32),
                        z=z.astype(np.float32), mask=mask, ref=uref, frames=np.array([u for u, _ in use]),
                        stack=np.stack([W[u] for u, _ in use]))
    X = np.stack([I[mask] for I in Is], 1)
    Bm = (np.nan_to_num(N) * alb[..., None])[mask]
    pred = np.clip(Bm @ L.T, 0, None)
    rel = float(np.median(np.abs(pred - X)) / np.median(X))
    rec.update(phase_residual=ph, ps=diag, lambertian_rel_median_abs_resid=round(rel, 4), mask_px=int(mask.sum()), status='ok')
    return rec


if __name__ == '__main__':
    for c in sys.argv[1:]:
        for film in ('bla', 'col'):
            res = run(int(c), film)
            json.dump(res, open(os.path.join(OUT, f'cut{int(c):02d}_{film}.json'), 'w'), indent=1, default=str)
            d = res.get('ps', {})
            print(c, film, res['status'], res.get('used'),
                  'reg', [(r['light'][:7], r.get('inliers'), r.get('cv_med_px'), r.get('ecc_tex'), r.get('tile_shift_px'), 'F' if r.get('failed') or r.get('accepted') is False else '') for r in res.get('registration', [])],
                  'tile_med', [float(np.median(p['tile_shift_px'])) for p in res.get('phase_residual', [])],
                  'sv', [round(x, 3) for x in d.get('sv_ratio', [])], 'curl', d.get('curl_ratio'), d.get('curl_ratio_other_mirror'),
                  'azerr', [round(a) for a in d.get('az_err_deg', [])], 'el', [round(a) for a in d.get('light_elev_est', [])],
                  'titled', d.get('titled'), 'resid', res.get('lambertian_rel_median_abs_resid'), flush=True)
