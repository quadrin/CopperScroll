#!/usr/bin/env python3
"""Joint placement model for the Copper Scroll entries, v1 (W2-B).

Same generative model and exact forward-backward inference as T06 v0 (results/T06_joint_model/scripts/joint_model.py,
copied unmodified to ../wave1_copy/), with these additions:
  * places may be broad areas given as inline components "lat:lon:sigma|..." (column `components`);
  * candidate and name-group rows may be conditional on a reading (`conditional_on_reading`:
    'kohlit15', 'solomon23', 'xii10=janoah', 'xii10!=janoah');
  * the five Kohlit entries carry ten published proposals (`kohlit_proposal=yes`) whose prior odds are set by a
    named scheme (cfg['kohlit_scheme'], dict place_id -> odds); order-derived exclusion can be applied to the
    neighbours only (cfg['exclude_order_derived']) and/or to the Kohlit proposals (cfg['exclude_kohlit_od']);
  * XII 10 read "in Janoah" (cfg['readings']['xii10'] == 'janoah'): entry 60 leaves the Kohlit name group, its
    evidence becomes Kh. Yanun (+ elsewhere), and the Kohlit latent Z gets a coupling factor
        zf(Z) = (1 - rho_J) + rho_J * h(bearing Z->Janoah) * (1 + d_eff/ell_J)^(-nu_J) / mean_piZ(...)
    i.e. Janoah lies NORTH of Kohlit at a distance of order ell_J (h soft: exp(kappa(cos theta - 1)); hard:
    1 inside +-45 deg of north, 0.02 outside).  Janoah's location is fixed at Kh. Yanun (Zissu/Lefkovits).
  * run(L_override=...) lets an analysis clamp entries to a single state (used for order Bayes factors).
With no Kohlit-scheme odds other than Tell es-Sultan = low and no new places this reduces to v0 (checked in
analysis_v1.py: reproduce_v0()).
"""
import csv, json, math, os
import numpy as np

DEFAULT = dict(
    w_A=0.4, w_L=0.995, lam=2.0, ell=1.0, scales=(1.0, 10.0), scale_w=(0.5, 0.5),
    rho=0.9, nu=2.0, ell_n=1.0, temper=True, pi_mode='per_place', u=1.0, sigma_U=2.0,
    conf_p=dict(high=0.85, medium=0.6, low=0.3, weak=0.1, unknown=0.0),
    status_mult=dict(preferred=1.5, possible=1.0, weak=0.5),
    exclude_order_derived=(), exclude_kohlit_od=(),
    readings=dict(kohlit15=True, solomon23=True, xii10='milik_puech'),
    kohlit_scheme=None,  # None -> use row confidence/status (all 'weak'); else dict place_id -> odds (0 drops)
    janoah=dict(rho=0.9, ell=10.0, nu=3.0, kappa=2.0, mode='soft', target='kh_yanun', sep=3.0),
    strict_coords=False,
    drop_groups=(),
    transition='sinkhorn',
    grid_km=0, grid_mass=1.0, grid_bbox=(31.2, 32.9, 34.9, 35.8),  # background grid (0 = off)  # 'sinkhorn' (T06 v0) or 'fixed' (density-neutral, see local_transition)      # name groups to switch off (used when the group's members are clamped)
)

REG_COARSE = dict(JER='Jerusalem side', SOUTH='Jerusalem side', WEST='Jerusalem side',
                  JERICHO='Jordan valley/desert', QUMRAN='Jordan valley/desert', DESERT='Jordan valley/desert',
                  NORTH='North', SAMDES='Samarian desert', HEBNEG='Hebron/Negev', CARMEL='Carmel', TRANSJ='Transjordan')


def hav(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def bearing(lat1, lon1, lat2, lon2):
    """initial bearing (radians, 0 = north, clockwise) from point 1 to point 2"""
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2 - lon1)
    return np.arctan2(np.sin(dl) * np.cos(p2), np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl))


def cond_ok(cond, readings):
    if not cond:
        return True
    if '!=' in cond:
        k, v = cond.split('!=')
        return readings.get(k) != v
    if '=' in cond:
        k, v = cond.split('=')
        return readings.get(k) == v
    return bool(readings.get(cond, True))


class Data:
    def __init__(self, ind, suffix='v1'):
        rd = lambda f: list(csv.DictReader(open(os.path.join(ind, f), encoding='utf-8')))
        self.entries = rd(f'entries_{suffix}.csv')
        self.order = [e['entry'] for e in sorted(self.entries, key=lambda r: int(r['order']))]
        self.block = {e['entry']: e['block'] for e in self.entries}
        self.econf = {e['entry']: e['entry_confidence'] for e in self.entries}
        self.title = {e['entry']: e['title'] for e in self.entries}
        self.places = rd(f'places_{suffix}.csv')
        self.cands = rd(f'candidates_{suffix}.csv')
        self.groups_raw = rd(f'name_groups_{suffix}.csv')
        for r in self.cands:
            r.setdefault('conditional_on_reading', '')
            r.setdefault('kohlit_proposal', 'no')
        for p in self.places:
            p.setdefault('components', '')
        self.place = {p['place_id']: p for p in self.places}
        unknown = sorted({c['place_id'] for c in self.cands} - set(self.place))
        if unknown:
            raise SystemExit(f'candidates refer to unknown places: {unknown}')


class Model:
    def __init__(self, data, cfg):
        self.d, self.c = data, cfg
        self._states()
        self._pi()

    def _comps(self, pid):
        p = self.d.place[pid]
        if p.get('components'):
            out = []
            for tok in p['components'].split('|'):
                la, lo, s = (float(x) for x in tok.split(':'))
                out.append((la, lo, s))
            return out
        if p['lat'] in ('', None):
            return [c for m in p['mixture_of'].split('|') for c in self._comps(m)]
        return [(float(p['lat']), float(p['lon']), float(p['sigma_km']))]

    def _states(self):
        d, c = self.d, self.c
        P = d.place
        self.regions = sorted({p['model_region'] for p in d.places})
        self.states = [p['place_id'] for p in d.places] + ['U_' + r for r in self.regions]
        self.region_of = {p['place_id']: p['model_region'] for p in d.places}
        self.region_of.update({'U_' + r: r for r in self.regions})
        # optional uniform background grid of unlisted cells (density-robust check): region 'BG', not in group domains
        self.grid = []
        if c.get('grid_km'):
            la0, la1, lo0, lo1 = c.get('grid_bbox', (31.2, 32.9, 34.9, 35.8))
            dla = c['grid_km'] / 111.2
            dlo = c['grid_km'] / (111.32 * math.cos(math.radians((la0 + la1) / 2)))
            for i, la in enumerate(np.arange(la0 + dla / 2, la1, dla)):
                for j, lo in enumerate(np.arange(lo0 + dlo / 2, lo1, dlo)):
                    gid = f'G_{i:02d}_{j:02d}'
                    self.grid.append((gid, float(la), float(lo), c['grid_km'] / 2))
                    self.states.append(gid)
                    self.region_of[gid] = 'BG'
        self.S = len(self.states)
        self.idx = {s: i for i, s in enumerate(self.states)}
        gpos = {g[0]: g[1:] for g in self.grid}
        rows = []
        for s in self.states:
            if s in gpos:
                rows.append([(gpos[s], 1.0)])
            elif s.startswith('U_'):
                r = s[2:]
                mem = [p['place_id'] for p in d.places if p['model_region'] == r and
                       (p['lat'] not in ('', None) or p.get('components'))]
                cs = [(la, lo, math.hypot(sg, c['sigma_U'])) for m in mem for (la, lo, sg) in self._comps(m)]
                rows.append([(x, 1.0 / len(cs)) for x in cs])
            elif P[s]['lat'] in ('', None) and not P[s].get('components'):
                mem = P[s]['mixture_of'].split('|')
                rows.append([(self._comps(m)[0], 1.0 / len(mem)) for m in mem])
            else:
                cs = self._comps(s)
                rows.append([(x, 1.0 / len(cs)) for x in cs])
        allc = sorted({x for r in rows for x, _ in r})
        ci = {x: i for i, x in enumerate(allc)}
        W = np.zeros((self.S, len(allc)))
        for i, r in enumerate(rows):
            for x, w in r:
                W[i, ci[x]] += w
        A = np.array(allc)
        self.A = A
        D = hav(A[:, 0][:, None], A[:, 1][:, None], A[:, 0][None, :], A[:, 1][None, :])
        self.D = D
        self.Deff = np.sqrt(D ** 2 + A[:, 2][:, None] ** 2 + A[:, 2][None, :] ** 2)
        self.Bear = bearing(A[:, 0][:, None], A[:, 1][:, None], A[:, 0][None, :], A[:, 1][None, :])
        self.W = W
        self.n_listed = {r: sum(1 for p in d.places if p['model_region'] == r) for r in self.regions}

    def _pi(self):
        c = self.c
        pi = np.zeros(self.S)
        if c['pi_mode'] == 'per_place':
            nl = len(self.d.places)
            for i, s in enumerate(self.states):
                if s.startswith('G_'):
                    pi[i] = c.get('grid_mass', 1.0) * nl / len(self.grid)
                else:
                    pi[i] = c['u'] * self.n_listed[s[2:]] if s.startswith('U_') else 1.0
        elif c['pi_mode'] == 'region_equal':
            for i, s in enumerate(self.states):
                r = self.region_of[s]
                m = 1.0 / len(self.regions)
                pi[i] = m * c['u'] / (1 + c['u']) if s.startswith('U_') else m / (1 + c['u']) / self.n_listed[r]
        else:
            raise ValueError(c['pi_mode'])
        self.pi = pi / pi.sum()

    def kernel(self, lam, ell):
        return self.W @ ((1.0 + self.Deff / ell) ** (-lam)) @ self.W.T

    def dist_states(self, a, b):
        """expected component distance (km) between two states"""
        return float(self.W[self.idx[a]] @ self.D @ self.W[self.idx[b]])

    def transition(self, w, lam=None):
        lam = self.c['lam'] if lam is None else lam
        Pi = np.tile(self.pi, (self.S, 1))
        if w == 0:
            return Pi
        if not hasattr(self, '_Tloc'):
            self._Tloc = {}
        if lam not in self._Tloc:
            self._Tloc[lam] = self.local_transition(lam)
        return (1 - w) * Pi + w * self._Tloc[lam]

    def local_transition(self, lam):
        K = sum(a * self.kernel(lam, l) for a, l in zip(self.c['scale_w'], self.c['scales']))
        if self.c.get('transition', 'sinkhorn') == 'fixed':
            # density-neutral alternative: one global normaliser C (the largest pi-weighted row sum); the deficit
            # r(a) = 1 - sum_b pi(b) K(a,b) / C leaks to the background pi.  The arriving state's factor is then
            # K(a,b) only (no Sinkhorn scaling), so isolated places get no self-transition boost and dense
            # clusters no inbound penalty; the price is that pi is no longer exactly stationary.
            s = K @ self.pi
            C = s.max()
            T = self.pi[None, :] * K / C + (1.0 - s / C)[:, None] * self.pi[None, :]
            return T / T.sum(1, keepdims=True)
        v = np.ones(self.S)
        for _ in range(5000):
            nv = np.sqrt(v / (K @ (self.pi * v)))
            if np.max(np.abs(nv - v)) < 1e-13:
                v = nv
                break
            v = nv
        T = (v[:, None] * K * v[None, :]) * self.pi[None, :]
        T /= T.sum(1, keepdims=True)
        return T

    # ---------------------------------------------------------------- evidence
    def evidence(self, order, drop=()):
        c = self.c
        rd = c['readings']
        by = {}
        for r in self.d.cands:
            if not cond_ok(r.get('conditional_on_reading', ''), rd):
                continue
            koh = r.get('kohlit_proposal') == 'yes'
            if koh and r['order_derived'] in c['exclude_kohlit_od']:
                continue
            if (not koh) and r['order_derived'] in c['exclude_order_derived']:
                continue
            if c.get('strict_coords') and self.d.place[r['place_id']]['coords_in_places_json'] != 'yes':
                continue
            by.setdefault(r['entry'], []).append(r)
        out = {}
        for e in order:
            rows = [] if e in drop else by.get(e, [])
            odds = np.zeros(self.S)
            for r in rows:
                if r.get('kohlit_proposal') == 'yes' and c.get('kohlit_scheme') is not None:
                    o = float(c['kohlit_scheme'].get(r['place_id'], 0.0))
                elif r.get('prior_override'):
                    o = float(r['prior_override'])
                else:
                    p = c['conf_p'][r['confidence']]
                    o = p / (1 - p) * c['status_mult'][r['status']]
                if o > 0:
                    odds[self.idx[r['place_id']]] += o
            if not odds.any():
                out[e] = (np.ones(self.S), self.pi.copy(), [])
                continue
            cand = np.nonzero(odds)[0]
            P0 = np.zeros(self.S)
            P0[cand] = odds[cand] / (1 + odds.sum())
            rest = np.ones(self.S, bool); rest[cand] = False
            P0[rest] = (1.0 / (1 + odds.sum())) * self.pi[rest] / self.pi[rest].sum()
            out[e] = (P0 / self.pi, P0, list(cand))
        return out

    # ---------------------------------------------------------------- Janoah coupling on the Kohlit latent
    def janoah_factor(self, dom):
        J = self.c['janoah']
        t = self.idx[J['target']]
        tw = self.W[t]
        f = (1.0 + self.Deff / J['ell']) ** (-J['nu'])
        # separation term: Janoah is a different place NORTH of Kohlit, so coincident locations get ~0
        f = f * (1.0 - np.exp(-(self.D / J.get('sep', 3.0)) ** 2))
        if J['mode'] == 'hard':
            h = np.where(np.abs(self.Bear) <= math.radians(45), 1.0, 0.02)
        else:
            h = np.exp(J['kappa'] * (np.cos(self.Bear) - 1.0))
        hf = self.W[dom] @ (h * f) @ tw          # component a (Kohlit) -> component b (Janoah): bearing a->b
        return hf

    def groups(self, order, ev):
        if self.c['rho'] <= 0:
            return []
        rd = self.c['readings']
        G = {}
        for r in self.d.groups_raw:
            if not cond_ok(r.get('conditional_on_reading', ''), rd):
                continue
            if r['group'] in self.c.get('drop_groups', ()):
                continue
            if r['entry'] in order:
                G.setdefault(r['group'], []).append(r['entry'])
        pos = {e: i for i, e in enumerate(order)}
        Kn = self.kernel(self.c['nu'], self.c['ell_n'])
        U = [self.idx['U_' + r] for r in self.regions]
        out = []
        for g, mem in sorted(G.items()):
            if len(mem) < 2:
                continue
            dom = sorted(set(U) | {s for e in mem for s in ev[e][2]})
            k = Kn[:, dom]
            kn = k / (self.pi @ k)[None, :]
            eta = (1 - self.c['rho']) + self.c['rho'] * kn
            piZ = self.pi[dom] / self.pi[dom].sum()
            zf = None
            if g == 'Kohlit' and rd.get('xii10') == 'janoah' and self.c['janoah']['rho'] > 0:
                hf = self.janoah_factor(dom)
                rJ = self.c['janoah']['rho']
                zf = (1 - rJ) + rJ * hf / (piZ @ hf)
                piZ = piZ * zf
                piZ = piZ / piZ.sum()
            ps = sorted(pos[e] for e in mem)
            out.append(dict(name=g, members=mem, pos=ps, dom=dom, eta=eta, piZ=piZ, zf=zf, first=ps[0], last=ps[-1]))
        return out

    # ---------------------------------------------------------------- exact inference
    def run(self, order=None, drop=(), with_post=True, L_override=None, temper_override=None, skip_Z0=False):
        c = self.c
        order = order or self.d.order
        n = len(order)
        ev = self.evidence(order, drop)
        G = self.groups(order, ev)
        nG = len(G)
        L = np.array([ev[e][0] for e in order])
        if G and c['temper']:
            ng = {}
            for g in G:
                for p in g['pos']:
                    ng[p] = max(ng.get(p, 1), len(g['pos']))
            for p, k in ng.items():
                L[p] = L[p] ** (1.0 / k)
        if L_override:
            for e, vec in L_override.items():
                L[order.index(e)] = vec
        Tc = {}
        Ts = []
        for i in range(n):
            if i == 0:
                Ts.append(None); continue
            w = c['w_A'] if (self.d.block[order[i]] == 'A' and self.d.block[order[i - 1]] == 'A') else c['w_L']
            if w not in Tc:
                Tc[w] = self.transition(w)
            Ts.append(Tc[w])
        starts = [[k for k, g in enumerate(G) if g['first'] == i] for i in range(n)]
        ends = [[k for k, g in enumerate(G) if g['last'] == i] for i in range(n)]
        mems = [[k for k, g in enumerate(G) if i in g['pos']] for i in range(n)]
        dims = [len(g['dom']) for g in G]

        def shp(axis_k=None, size=None, base=None):
            s = [1] * (nG + 1)
            if base is not None:
                s[0] = base
            if axis_k is not None:
                s[axis_k + 1] = size
            return s

        def fwd(Lmat):
            alphas, logZ = [], 0.0
            carry = None
            for i in range(n):
                if i == 0:
                    a = self.pi.reshape(shp(base=self.S)).copy()
                else:
                    a = np.tensordot(Ts[i].T, carry, axes=(1, 0))
                for k in starts[i]:
                    a = a * G[k]['piZ'].reshape(shp(k, dims[k]))
                a = a * Lmat[i].reshape(shp(base=self.S))
                for k in mems[i]:
                    a = a * G[k]['eta'].reshape(shp(k, dims[k], self.S))
                z = a.sum()
                a = a / z
                logZ += math.log(z)
                alphas.append(a)
                carry = a
                for k in ends[i]:
                    carry = carry.sum(axis=k + 1, keepdims=True)
            return alphas, logZ

        alphas, logZE = fwd(L)
        logZ0 = fwd(np.ones_like(L))[1] if (G and not skip_Z0) else 0.0
        res = dict(order=order, logml=logZE - logZ0, logZE=logZE, ev=ev, groups=G)
        if not with_post:
            return res
        betas = [None] * n
        betas[n - 1] = np.ones_like(alphas[n - 1])
        for i in range(n - 2, -1, -1):
            m = betas[i + 1] * L[i + 1].reshape(shp(base=self.S))
            for k in mems[i + 1]:
                m = m * G[k]['eta'].reshape(shp(k, dims[k], self.S))
            for k in starts[i + 1]:
                m = m * G[k]['piZ'].reshape(shp(k, dims[k]))
                m = m.sum(axis=k + 1, keepdims=True)
            b = np.tensordot(Ts[i + 1], m, axes=(1, 0))
            b = b / max(b.max(), 1e-300)
            betas[i] = b
        post = np.zeros((n, self.S))
        zpost = {}
        for i in range(n):
            pr = alphas[i] * betas[i]
            pr = pr / pr.sum()
            post[i] = pr.reshape(self.S, -1).sum(1)
            for k in mems[i]:
                if G[k]['name'] not in zpost:
                    ax = tuple(j for j in range(nG + 1) if j != k + 1)
                    zpost[G[k]['name']] = dict(zip([self.states[s] for s in G[k]['dom']], pr.sum(axis=ax).ravel()))
        res.update(post=post, zpost=zpost)
        return res

    def region_probs(self, p):
        out = {r: 0.0 for r in self.regions}
        if self.grid:
            out['BG'] = 0.0
        for i, s in enumerate(self.states):
            out[self.region_of[s]] += p[i]
        return out


def cfg_with(**kw):
    c = json.loads(json.dumps(DEFAULT))
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k].update(v)
        else:
            c[k] = v
    c['exclude_order_derived'] = tuple(c['exclude_order_derived'])
    c['exclude_kohlit_od'] = tuple(c['exclude_kohlit_od'])
    c['scales'] = tuple(c['scales']); c['scale_w'] = tuple(c['scale_w'])
    return c


def write_csv(path, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)
