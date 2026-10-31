"""Analysis-by-synthesis scoring of a finite candidate set for one line (direction B).
Registration (candidate-symmetric, text of other lines not used):
  for each strip (cut) holding the column and each 180-degree orientation, the line's nominal row is
  y_nom = Hs * (0.05 + 0.9 * (l - 0.5) / N)   (N = lines in the column, Hs = strip height in px),
  nominal line pitch s = 0.9 * Hs / N, search window y_nom +- WIN * s.
  Every candidate c gives a score curve L_c(o, y) (max over horizontal offset, per-frame light fit).
  Location (o*, y*) = argmax over o, y of mean_c L_c(o, y)  -> shared by all candidates.
  Candidate score on the strip = max of L_c(o*, y) for |y - y*| <= LOC * s.
Line score = sum over the column's strips. Rank 1 = highest. Ties at the top count as a miss for the truth."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as m
HERE = os.path.dirname(os.path.abspath(__file__))
REND = '/root/novel/private_outputs/B/renderings'; os.makedirs(REND, exist_ok=True)
COL_CUTS = {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [10, 11], 6: [11, 12], 7: [13, 14], 8: [15],
            9: [16, 17], 10: [17, 18], 12: [21, 22]}   # Puech 2006 radiograph captions; cut 1 has no lit frames
NLINES = {1: 15, 2: 15, 3: 13, 4: 14, 5: 14, 6: 14, 7: 16, 8: 16, 9: 17, 10: 17, 11: 17, 12: 13}
WIN = 1.5; LOC = 0.15
def fit_window(obs, M, regs, yc, sp, P, ylo, yhi):
    half = int(round(P['band'] * sp))
    a, b = max(0, ylo - half), min(obs.shape[1], yhi + half + 1)
    sc, tb = m.fit_map(obs[:, a:b], M[a:b], regs, yc, sp, P)
    ys = np.arange(a, b)
    keep = (ys >= ylo) & (ys <= yhi)
    return ys[keep], sc[keep], tb[keep]
def score_line(col, line, cands, P, save=None):
    N = NLINES[col]; tot = {c: 0.0 for c in cands}; info = []
    for cut in COL_CUTS[col]:
        per_o = {}
        for o in (0, 1):
            S, M, lab = m.load_stack(cut, bool(o), P)
            Hs = S.shape[1]; s = 0.9 * Hs / N; h = P['rho'] * s
            obs = m.prep_obs(S, M, s, P)
            ynom = Hs * (0.05 + 0.9 * (line - 0.5) / N)
            ylo, yhi = int(max(0, ynom - WIN * s)), int(min(Hs - 1, ynom + WIN * s))
            curves = {}
            for c in cands:
                regs, yc = m.render_line(c, h, P)
                ys, sc, tb = fit_window(obs, M, regs, yc, s, P, ylo, yhi)
                curves[c] = (sc, tb)
                if save and o == 0 and c == cands[0]: pass
            per_o[o] = (ys, curves, s, h)
        best = None
        for o, (ys, curves, s, h) in per_o.items():
            mean = np.mean([curves[c][0] for c in cands], 0)
            mean[~np.isfinite(mean)] = -np.inf
            i = int(np.argmax(mean))
            if best is None or mean[i] > best[0]: best = (float(mean[i]), o, int(ys[i]))
        if best is None or not np.isfinite(best[0]):
            info.append(dict(cut=cut, status='no valid rows')); continue
        _, o, ystar = best
        ys, curves, s, h = per_o[o]
        sel = np.abs(ys - ystar) <= LOC * s
        per = {}
        for c in cands:
            v = curves[c][0][sel]; j = int(np.argmax(v))
            per[c] = float(v[j]); tot[c] += per[c]
            if save:
                regs, yc = m.render_line(c, h, P)
                np.savez_compressed(f'{REND}/{save}_cut{cut:02d}_c{cands.index(c)}.npz', gx=regs[0], gy=regs[1],
                                    groove=regs[2], y=ys[sel][j], t=curves[c][1][sel][j], orient=o, sp=s)
        info.append(dict(cut=cut, status='scored', orient=o, y=ystar, sp=round(s, 2), per=per))
    return tot, info
