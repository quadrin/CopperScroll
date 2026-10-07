#!/usr/bin/env python3
"""G-model: the T06 itinerary term re-expressed on a UNIFORM 5-km grid (density-neutral reference).

Why: in T06 (and v1 K1) the state space is the project gazetteer, which is dense around Jerusalem/Jericho/Qumran
and sparse elsewhere; the Sinkhorn-normalised kernel then (i) boosts self-transitions at isolated places and
(ii) damps transitions INTO dense clusters (Tell es-Sultan sits in the densest).  Here every state is a grid
cell of equal prior mass, so the transition depends on distance only (apart from edge effects, reduced by a
wide box).  Evidence: each candidate's prior odds are spread over cells with a Gaussian footprint
(s = max(sigma_place, 2.5 km)); 'elsewhere' is uniform.  Name groups are not modelled; Kohlit entries are
clamped together (tied) or one at a time (untied).

  python3 -I gmodel.py ../inputs ../outputs
"""
import csv, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joint_model_v1 as jm
from analysis_v1 import PROPOSALS, KOH, SCHEMES, EXCL, L10

BBOX = (31.0, 33.1, 34.6, 36.1)
CELL = 5.0


class GModel:
    def __init__(self, data, cfg, cell=CELL, bbox=BBOX):
        self.d, self.c = data, cfg
        la0, la1, lo0, lo1 = bbox
        dla = cell / 111.2
        dlo = cell / (111.32 * math.cos(math.radians((la0 + la1) / 2)))
        pts = [(la, lo) for la in np.arange(la0 + dla / 2, la1, dla) for lo in np.arange(lo0 + dlo / 2, lo1, dlo)]
        self.P = np.array(pts)
        self.N = len(pts)
        self.cell = cell
        self.pi = np.full(self.N, 1.0 / self.N)
        D = jm.hav(self.P[:, 0][:, None], self.P[:, 1][:, None], self.P[:, 0][None, :], self.P[:, 1][None, :])
        self.D = D
        self.Bear = jm.bearing(self.P[:, 0][:, None], self.P[:, 1][:, None], self.P[:, 0][None, :], self.P[:, 1][None, :])
        sc = cell / 2
        De = np.sqrt(D ** 2 + 2 * sc ** 2)
        self.K = sum(a * (1 + De / l) ** (-cfg['lam']) for a, l in zip(cfg['scale_w'], cfg['scales']))
        v = np.ones(self.N)
        for _ in range(20000):
            nv = np.sqrt(v / (self.K @ (self.pi * v)))
            if np.max(np.abs(nv - v)) < 1e-12:
                v = nv; break
            v = nv
        T = (v[:, None] * self.K * v[None, :]) * self.pi[None, :]
        self.Tloc = T / T.sum(1, keepdims=True)
        self.mdl = jm.Model(data, cfg)       # used only for place components / distances

    def footprint(self, pid):
        if not hasattr(self, '_fp'):
            self._fp = {}
        if pid in self._fp:
            return self._fp[pid]
        self._fp[pid] = self._footprint(pid)
        return self._fp[pid]

    def _footprint(self, pid):
        comps = self.mdl._comps(pid)
        f = np.zeros(self.N)
        for (la, lo, sg) in comps:
            s = max(sg, self.cell / 2)
            d = jm.hav(self.P[:, 0], self.P[:, 1], la, lo)
            f += np.exp(-0.5 * (d / s) ** 2) / len(comps)
        return f / f.sum()

    def evidence(self):
        key = (self.c['readings'].get('xii10'), json.dumps(self.c.get('kohlit_scheme'), sort_keys=True))
        if not hasattr(self, '_evc'):
            self._evc = {}
        if key not in self._evc:
            self._evc[key] = self._evidence()
        return self._evc[key]

    def _evidence(self):
        c = self.c
        rd = c['readings']
        by = {}
        for r in self.d.cands:
            if not jm.cond_ok(r.get('conditional_on_reading', ''), rd):
                continue
            koh = r.get('kohlit_proposal') == 'yes'
            if koh and r['order_derived'] in c['exclude_kohlit_od']:
                continue
            if (not koh) and r['order_derived'] in c['exclude_order_derived']:
                continue
            by.setdefault(r['entry'], []).append(r)
        ev = {}
        for e in self.d.order:
            P0 = np.zeros(self.N)
            tot = 0.0
            for r in by.get(e, []):
                if r.get('kohlit_proposal') == 'yes' and c.get('kohlit_scheme') is not None:
                    o = float(c['kohlit_scheme'].get(r['place_id'], 0.0))
                else:
                    p = c['conf_p'][r['confidence']]
                    o = p / (1 - p) * c['status_mult'][r['status']]
                if o > 0:
                    P0 += o * self.footprint(r['place_id'])
                    tot += o
            P0 = (P0 + self.pi) / (1 + tot)
            ev[e] = P0 / self.pi
        return ev

    def logml(self, w_A, w_L, L_override=None):
        ev = self.evidence()
        order = self.d.order
        L = np.array([ev[e] for e in order])
        if L_override:
            for e, vec in L_override.items():
                L[order.index(e)] = vec
        a = self.pi * L[0]
        z = a.sum(); a /= z; ll = math.log(z)
        for i in range(1, len(order)):
            w = w_A if (self.d.block[order[i]] == 'A' and self.d.block[order[i - 1]] == 'A') else w_L
            a = ((1 - w) * a.sum() * self.pi + w * (a @ self.Tloc)) * L[i]
            z = a.sum(); a /= z; ll += math.log(z)
        return ll

    def tied_landscape(self, w_A, w_L, ents, free=()):
        """log ML with entries `ents` all clamped to the same cell k, for every k at once (segment products).
        Entries in `free` get no evidence (L = 1)."""
        ev = self.evidence()
        order = self.d.order
        n = len(order)
        L = np.array([ev[e] for e in order])
        for e in free:
            L[order.index(e)] = 1.0
        cl = sorted(order.index(e) for e in ents)
        Ts = [None] + [((1 - (w_A if (self.d.block[order[i]] == 'A' and self.d.block[order[i - 1]] == 'A') else w_L))
                        * np.tile(self.pi, (self.N, 1)) +
                        (w_A if (self.d.block[order[i]] == 'A' and self.d.block[order[i - 1]] == 'A') else w_L) * self.Tloc)
                       for i in range(1, n)]
        # alpha into the first clamped position
        a = self.pi * L[0] if cl[0] > 0 else self.pi.copy()
        la = 0.0
        if cl[0] > 0:
            z = a.sum(); a /= z; la += math.log(z)
            for i in range(1, cl[0]):
                a = (a @ Ts[i]) * L[i]; z = a.sum(); a /= z; la += math.log(z)
            a = a @ Ts[cl[0]]
        tot = np.log(a) + la
        # segments between clamped positions: diagonal of the product
        for s_, t_ in zip(cl[:-1], cl[1:]):
            M = np.eye(self.N)
            lm = 0.0
            for i in range(s_ + 1, t_):
                M = (M @ Ts[i]) * L[i][None, :]
                z = M.max(); M /= z; lm += math.log(z)
            M = M @ Ts[t_]
            tot += np.log(np.diag(M)) + lm
        # beta after the last clamped position
        b = np.ones(self.N); lb = 0.0
        for i in range(n - 1, cl[-1], -1):
            b = Ts[i] @ (L[i] * b); z = b.max(); b /= z; lb += math.log(z)
        tot += np.log(b) + lb
        tot += len(cl) * np.log(1.0 / self.pi)
        return tot

    def janoah_hf(self, target_pid, mode='soft', ell=10.0, nu=3.0, kappa=2.0):
        """h(bearing cell->Janoah) * (1 + d/ell)^-nu for every cell (Janoah = target place, Gaussian footprint)."""
        f = self.footprint(target_pid)
        j = int(np.argmax(f))
        d = self.D[:, j]
        b = self.Bear[:, j]
        h = np.exp(kappa * (np.cos(b) - 1)) if mode == 'soft' else np.where(np.abs(b) <= math.radians(45), 1.0, 0.02)
        return h * (1 + np.sqrt(d ** 2 + 2 * (self.cell / 2) ** 2) / ell) ** (-nu) * (1 - np.exp(-(d / 3.0) ** 2))


def main(ind, out):
    d = jm.Data(ind, 'v1')
    rows_fit, rows_bf, rows_post, land = [], [], [], []
    for en in ('b0_none', 'b2_doc_likely'):
        cfg = jm.cfg_with(kohlit_scheme=SCHEMES['equal'], **EXCL[en])
        g = GModel(d, cfg)
        print('grid cells', g.N, flush=True)
        # ---- weight fit (no Kohlit clamping; Kohlit entries carry the equal-scheme proposals)
        best = None
        for wa in (0.0, 0.4, 0.8):
            for wl in (0.0, 0.5, 0.8, 0.9, 0.95, 0.99):
                lm = g.logml(wa, wl) - g.logml(0.0, 0.0)
                rows_fit.append(dict(excl=en, w_A=wa, w_L=wl, dlogml=round(lm, 3)))
                if best is None or lm > best[2]:
                    best = (wa, wl, lm)
        print(en, 'best', best, flush=True)
        orders = {'fit': best[:2], 'weak': (0.0, 0.8), 'T06': (0.4, 0.995)}
        pidx = {c: g.footprint(c) for c in PROPOSALS + ['kh_yanun']}
        for on, (wa, wl) in orders.items():
            for reading in ('milik_puech', 'janoah'):
                g.c['readings']['xii10'] = reading
                koh = [e for e in KOH if not (reading == 'janoah' and e == '60')]
                one = np.ones(g.N)

                def score_vec(vec, ents):
                    Lo = {e: one for e in koh}
                    Lo.update({e: vec for e in ents})
                    return g.logml(wa, wl, Lo)
                designs = {'tied_all': koh, **{f'only_{e}': [e] for e in koh}}
                for dn, ents in designs.items():
                    sc = {c: score_vec(pidx[c] / g.pi, ents) for c in PROPOSALS}
                    if dn == 'only_60':
                        sc['kh_yanun'] = score_vec(pidx['kh_yanun'] / g.pi, ents)
                    for c, v in sc.items():
                        rows_bf.append(dict(model='G_uniform_grid', excl=en, order=on, w_A=wa, w_L=wl, reading=reading, design=dn,
                                            candidate=c, dlog10_vs_tell=round(L10(v - sc['tell_es_sultan']), 3)))
                # ---- landscape over all cells for the tied design (fit order) -> posterior with an 'elsewhere' option
                if on in ('fit', 'weak'):
                    ents = koh
                    cellsc = g.tied_landscape(wa, wl, ents, free=[e for e in koh if e not in ents])
                    sc = {c: score_vec(pidx[c] / g.pi, ents) for c in PROPOSALS}
                    ref = sc['tell_es_sultan']
                    if on == 'fit':
                        for k in range(g.N):
                            land.append(dict(excl=en, reading=reading, lat=round(g.P[k, 0], 4), lon=round(g.P[k, 1], 4),
                                             dlog10_vs_tell=round(L10(cellsc[k] - ref), 3)))
                    for jmode in (['none'] if reading == 'milik_puech' else ['none', 'soft10', 'soft20', 'hard10']):
                        if jmode == 'none':
                            jf_c = {c: 1.0 for c in PROPOSALS}
                            jf_cells = np.ones(g.N)
                        else:
                            mode = 'soft' if jmode.startswith('soft') else 'hard'
                            ell = float(jmode[4:]) if mode == 'soft' else float(jmode[4:])
                            hf = g.janoah_hf('kh_yanun', mode=mode, ell=ell)
                            mean = float(g.pi @ hf)
                            jf_cells = 0.1 + 0.9 * hf / mean
                            jf_c = {c: float(pidx[c] @ jf_cells) for c in PROPOSALS}
                        for sn, sch in SCHEMES.items():
                            for order_on in (True, False):
                                tot_odds = sum(sch.values())
                                p_else = 1.0 / (1 + tot_odds)
                                mx = max(list(sc.values()) + [cellsc.max()])
                                lik = {c: (math.exp(sc[c] - mx) if order_on else 1.0) * jf_c[c] for c in PROPOSALS}
                                lik_else = float(g.pi @ ((np.exp(cellsc - mx) if order_on else np.ones(g.N)) * jf_cells))
                                num = {c: sch[c] / (1 + tot_odds) * lik[c] for c in PROPOSALS}
                                Z = sum(num.values()) + p_else * lik_else
                                for c in PROPOSALS:
                                    rows_post.append(dict(model='G_uniform_grid', excl=en, order=(on if order_on else 'off'),
                                                          reading=reading, janoah=jmode, scheme=sn, candidate=c,
                                                          P_group=round(num[c] / Z, 4)))
                                rows_post.append(dict(model='G_uniform_grid', excl=en, order=(on if order_on else 'off'),
                                                      reading=reading, janoah=jmode, scheme=sn, candidate='ELSEWHERE',
                                                      P_group=round(p_else * lik_else / Z, 4)))
            print(en, on, 'done', flush=True)
    jm.write_csv(os.path.join(out, 'gmodel_weight_fit.csv'), rows_fit)
    jm.write_csv(os.path.join(out, 'gmodel_order_bayes_factors.csv'), rows_bf)
    jm.write_csv(os.path.join(out, 'gmodel_group_posteriors.csv'), rows_post)
    jm.write_csv(os.path.join(out, 'gmodel_landscape_tied.csv'), land)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
