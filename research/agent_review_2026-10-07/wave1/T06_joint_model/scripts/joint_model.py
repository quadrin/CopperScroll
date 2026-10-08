#!/usr/bin/env python3
"""Joint placement model for the Copper Scroll entries (v0).

Generative story (all terms optional / tunable):
  * Global state space = every gazetteer place (places_v0.csv) + one "unlisted site in region R" state U_R per
    model region.  Background measure pi over states (default: 1 per listed place, u*n_R for U_R).
  * Itinerary term: the deposit locations follow a Markov chain along the scroll order with transition
        T(a,b) = (1 - w) * pi(b) + w * pi(b) * Ks(a,b),
        K(a,b) = sum_k alpha_k * mean over location components of (1 + d_eff/ell_k)^(-lam)
    i.e. with probability w the next entry is a LOCAL step (distance-decaying kernel with a site scale
    ell_1 = 1 km and a district scale ell_2 = 10 km by default) and with 1 - w a jump to anywhere.  d_eff = sqrt(d^2 + sigma_a^2 + sigma_b^2) uses each place's stated precision; Ks is K after a
    fixed global normalization with each row deficit returned to pi (W2B K2; corrected 8 October UTC).
    pi is an initial/background measure, not generally stationary. Explicit transition='sinkhorn'
    reproduces the old stationary model. w = 0 => independent entries (control).
    Separate weights for transitions inside entries 1-19 (w_A) and elsewhere (w_L).
  * Repeated-name term: each name group g (entries naming the same place) has a latent location Z_g ~ pi
    (restricted to members' candidates + U states); each member gets a factor
        eta(x, Z) = (1 - rho) + rho * kn(x, Z),  kn = (1 + d_eff/ell_n)^(-nu) normalised so sum_x pi(x) eta(x,Z) = 1.
    Optional evidence tempering (L ** (1/n_g)) so one identification shared by n_g members counts once.
  * Evidence (published candidates + stated confidence): likelihood L_i(x) = P0_i(x) / pi(x) where P0_i is the
    stated-confidence prior (odds by confidence label x status multiplier; remainder = "elsewhere").  With
    w = 0 and rho = 0 the posterior equals P0 exactly (checked in self_test()).
Inference is exact: forward-backward along the scroll order with the name-group latents carried as extra
array axes between their first and last member.

Usage:
  python3 -I joint_model.py --inputs ../inputs --out ../outputs            # full v0 analysis
  python3 -I joint_model.py --inputs DIR --out DIR --quick                 # posterior tables only
Edit/append rows in candidates_v0.csv / places_v0.csv / name_groups_v0.csv to feed new evidence in.
"""
import argparse, csv, json, math, os, re, sys, time
import numpy as np

# ------------------------------------------------------------------------------------------------ defaults
DEFAULT = dict(
    w_A=0.8, w_L=0.8,                # itinerary weights (probability of a local step); 0 = control
    lam=2.0,                         # exponent of the local kernel (1 + d/ell)^-lam
    ell=1.0,                         # km scale used by the descriptive null statistic
    scales=(1.0, 10.0),              # km scales of the local kernel (site scale, district scale)
    scale_w=(0.5, 0.5),              # their mixture weights
    rho=0.0,                         # repeated-name tie strength (0..1)
    nu=2.0, ell_n=1.0,               # name kernel exponent / km scale
    temper=True,                     # temper evidence of name-group members by 1/n_g when rho > 0
    pi_mode='per_place', u=1.0,      # background measure
    sigma_U=2.0,                     # extra spread (km) of the unlisted-site states around listed places
    conf_p=dict(high=0.85, medium=0.6, low=0.3, weak=0.1, unknown=0.0),
    status_mult=dict(preferred=1.5, possible=1.0, weak=0.5),
    exclude_order_derived=(),        # e.g. ('documented',) or ('documented','likely')
    readings=dict(kohlit15=True, solomon23=True),
    strict_coords=False,             # True: ignore candidates whose place has no coordinates in places.json
    transition='fixed',              # W2B K2; 'sinkhorn' explicitly reproduces historical v0 outputs
)

REG_COARSE = dict(JER='Jerusalem side', SOUTH='Jerusalem side', WEST='Jerusalem side',
                  JERICHO='Jordan valley/desert', QUMRAN='Jordan valley/desert', DESERT='Jordan valley/desert',
                  NORTH='North')


def hav(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


# ------------------------------------------------------------------------------------------------ data
class Data:
    def __init__(self, ind):
        rd = lambda f: list(csv.DictReader(open(os.path.join(ind, f), encoding='utf-8')))
        self.entries = rd('entries_v0.csv')
        self.order = [e['entry'] for e in sorted(self.entries, key=lambda r: int(r['order']))]
        self.block = {e['entry']: e['block'] for e in self.entries}
        self.econf = {e['entry']: e['entry_confidence'] for e in self.entries}
        self.title = {e['entry']: e['title'] for e in self.entries}
        self.places = rd('places_v0.csv')
        self.cands = rd('candidates_v0.csv')
        self.groups_raw = rd('name_groups_v0.csv')
        self.place = {p['place_id']: p for p in self.places}
        unknown = sorted({c['place_id'] for c in self.cands} - set(self.place))
        if unknown:
            raise SystemExit(f'candidates refer to places missing from places_v0.csv: {unknown}')


class Model:
    def __init__(self, data, cfg):
        self.d, self.c = data, cfg
        self._states()
        self._pi()

    # -------------------------------------------------------------- states & location components
    def _states(self):
        d, c = self.d, self.c
        P = d.place
        self.regions = sorted({p['model_region'] for p in d.places})
        self.states = [p['place_id'] for p in d.places] + ['U_' + r for r in self.regions]
        self.S = len(self.states)
        self.idx = {s: i for i, s in enumerate(self.states)}
        self.region_of = {p['place_id']: p['model_region'] for p in d.places}
        self.region_of.update({'U_' + r: r for r in self.regions})
        comps = []  # (lat, lon, sigma)
        W = []      # rows: state -> weights over components

        def pt(pid):
            p = P[pid]
            return float(p['lat']), float(p['lon']), float(p['sigma_km'])
        rows = []
        for s in self.states:
            if s.startswith('U_'):
                r = s[2:]
                mem = [p['place_id'] for p in d.places if p['model_region'] == r and p['lat'] not in ('', None)]
                cs = [(*pt(m)[:2], math.hypot(pt(m)[2], c['sigma_U'])) for m in mem]
                rows.append([(x, 1.0 / len(cs)) for x in cs])
            elif P[s]['lat'] in ('', None):
                mem = P[s]['mixture_of'].split('|')
                rows.append([(pt(m), 1.0 / len(mem)) for m in mem])
            else:
                rows.append([(pt(s), 1.0)])
        allc = sorted({x for r in rows for x, _ in r})
        ci = {x: i for i, x in enumerate(allc)}
        W = np.zeros((self.S, len(allc)))
        for i, r in enumerate(rows):
            for x, w in r:
                W[i, ci[x]] += w
        A = np.array(allc)
        D = hav(A[:, 0][:, None], A[:, 1][:, None], A[:, 0][None, :], A[:, 1][None, :])
        self.Deff = np.sqrt(D ** 2 + A[:, 2][:, None] ** 2 + A[:, 2][None, :] ** 2)
        self.W = W
        self.n_listed = {r: sum(1 for p in d.places if p['model_region'] == r) for r in self.regions}

    def _pi(self):
        c = self.c
        pi = np.zeros(self.S)
        if c['pi_mode'] == 'per_place':
            for i, s in enumerate(self.states):
                pi[i] = c['u'] * self.n_listed[s[2:]] if s.startswith('U_') else 1.0
        elif c['pi_mode'] == 'region_equal':
            for i, s in enumerate(self.states):
                r = self.region_of[s]
                m = 1.0 / len(self.regions)
                pi[i] = m * c['u'] / (1 + c['u']) if s.startswith('U_') else m / (1 + c['u']) / self.n_listed[r]
        else:
            raise ValueError(c['pi_mode'])
        self.pi = pi / pi.sum()

    # -------------------------------------------------------------- kernels
    def kernel(self, lam, ell):
        return self.W @ ((1.0 + self.Deff / ell) ** (-lam)) @ self.W.T

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
        mode = self.c.get('transition', 'fixed')
        if mode == 'fixed':
            # W2B K2: one global normalizer, with row deficit returned to pi.
            # Arrival factors have no destination-specific Sinkhorn multiplier.
            # pi is an initial/background measure; it is not generally stationary.
            s = K @ self.pi
            C = float(s.max())
            if not np.isfinite(C) or C <= 0:
                raise ValueError('fixed kernel requires a finite positive normalizer')
            T = self.pi[None, :] * (K / C + (1.0 - s / C)[:, None])
            return T / T.sum(1, keepdims=True)
        if mode != 'sinkhorn':
            raise ValueError('unknown transition: ' + str(mode))
        v = np.ones(self.S)
        for _ in range(5000):
            nv = np.sqrt(v / (K @ (self.pi * v)))
            if np.max(np.abs(nv - v)) < 1e-13:
                v = nv
                break
            v = nv
        T = (v[:, None] * K * v[None, :]) * self.pi[None, :]
        T /= T.sum(1, keepdims=True)  # tiny correction after convergence
        return T

    # -------------------------------------------------------------- evidence
    def evidence(self, order, drop=()):
        """Return dict entry -> (L vector, P0 vector, candidate state indices)."""
        c = self.c
        by = {}
        for r in self.d.cands:
            if r['order_derived'] in c['exclude_order_derived']:
                continue
            if c.get('strict_coords') and self.d.place[r['place_id']]['coords_in_places_json'] != 'yes':
                continue
            by.setdefault(r['entry'], []).append(r)
        out = {}
        for e in order:
            rows = [] if e in drop else by.get(e, [])
            if not rows:
                out[e] = (np.ones(self.S), self.pi.copy(), [])
                continue
            odds = np.zeros(self.S)
            for r in rows:
                if r.get('prior_override'):
                    o = float(r['prior_override'])
                else:
                    p = c['conf_p'][r['confidence']]
                    o = p / (1 - p) * c['status_mult'][r['status']]
                odds[self.idx[r['place_id']]] += o
            cand = np.nonzero(odds)[0]
            P0 = np.zeros(self.S)
            P0[cand] = odds[cand] / (1 + odds.sum())
            rest = np.ones(self.S, bool); rest[cand] = False
            p_else = 1.0 / (1 + odds.sum())
            P0[rest] = p_else * self.pi[rest] / self.pi[rest].sum()
            out[e] = (P0 / self.pi, P0, list(cand))
        return out

    # -------------------------------------------------------------- name groups
    def groups(self, order, ev):
        if self.c['rho'] <= 0:
            return []
        rd = self.c['readings']
        G = {}
        for r in self.d.groups_raw:
            cond = r['conditional_on_reading']
            if cond and not rd.get(cond, True):
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
            ps = sorted(pos[e] for e in mem)
            out.append(dict(name=g, members=mem, pos=ps, dom=dom, eta=eta, piZ=piZ, first=ps[0], last=ps[-1]))
        return out

    # -------------------------------------------------------------- exact inference
    def run(self, order=None, drop=(), with_post=True):
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
                    s = shp(k, dims[k], self.S)
                    a = a * G[k]['eta'].reshape(s)
                z = a.sum()
                a = a / z
                logZ += math.log(z)
                alphas.append(a)
                carry = a
                for k in ends[i]:
                    carry = carry.sum(axis=k + 1, keepdims=True)
            return alphas, logZ

        alphas, logZE = fwd(L)
        logZ0 = fwd(np.ones_like(L))[1] if G else 0.0
        res = dict(order=order, logml=logZE - logZ0, ev=ev, groups=G)
        if not with_post:
            return res
        # backward
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

    # -------------------------------------------------------------- summaries
    def region_probs(self, p):
        out = {r: 0.0 for r in self.regions}
        for i, s in enumerate(self.states):
            out[self.region_of[s]] += p[i]
        return out

    def coarse_probs(self, p):
        rp = self.region_probs(p)
        out = {}
        for r, v in rp.items():
            out[REG_COARSE[r]] = out.get(REG_COARSE[r], 0.0) + v
        return out


# ------------------------------------------------------------------------------------------------ helpers
def cfg_with(**kw):
    c = json.loads(json.dumps(DEFAULT))
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k].update(v)
        else:
            c[k] = v
    c['exclude_order_derived'] = tuple(c['exclude_order_derived'])
    return c


def tv(p, q):
    ks = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0)) for k in ks)


def self_test(data):
    """w = 0, rho = 0 must reproduce the stated-confidence prior exactly; groups with rho>0 must run."""
    m = Model(data, cfg_with(w_A=0, w_L=0, rho=0))
    r = m.run()
    for i, e in enumerate(r['order']):
        assert np.allclose(r['post'][i], r['ev'][e][1], atol=1e-10), e
    assert abs(r['logml']) < 1e-9
    # Stationarity belongs only to the legacy Sinkhorn model.
    m2 = Model(data, cfg_with(w_A=0.9, w_L=0.9, rho=0, transition='sinkhorn'))
    T = m2.transition(0.9)
    assert np.allclose(m2.pi @ T, m2.pi, atol=1e-9)
    # Fixed K2 can drift without evidence; verify the forward Markov marginals.
    rr = Model(data, cfg_with(w_A=0.95, w_L=0.95, lam=3.0, rho=0))
    order = data.order
    res = rr.run(order=order, drop=set(order))
    q = rr.pi.copy()
    for i, e in enumerate(order):
        if i:
            q = q @ rr.transition(0.95)
        assert np.allclose(res['post'][i], q, atol=1e-8), e
    assert abs(res['logml']) < 1e-9
    # brute-force check of exact inference with groups on a short sub-order
    sub = ['4', '5', '6', '11', '13']
    mm = Model(data, cfg_with(w_A=0.8, w_L=0.8, rho=0.9, readings=dict(kohlit15=True, solomon23=True)))
    res = mm.run(order=sub)
    # brute force over x (S^5 too big) -> check via Gibbs-free identity: compare with groups simulated by
    # enumerating Z and running chain forward exactly
    ev = res['ev']; G = res['groups']
    L = np.array([ev[e][0] for e in sub])
    ng = {}
    for g in G:
        for p in g['pos']:
            ng[p] = max(ng.get(p, 1), len(g['pos']))
    for p, k in ng.items():
        L[p] = L[p] ** (1.0 / k)
    T = mm.transition(0.8)
    import itertools
    tot = 0.0; marg = np.zeros((len(sub), mm.S))
    for zs in itertools.product(*[range(len(g['dom'])) for g in G]):
        w = np.prod([g['piZ'][z] for g, z in zip(G, zs)])
        U = L.copy()
        for g, z in zip(G, zs):
            for p in g['pos']:
                U[p] = U[p] * g['eta'][:, z]
        # forward-backward on plain chain
        a = [mm.pi * U[0]]
        for i in range(1, len(sub)):
            a.append((a[-1] @ T) * U[i])
        b = [np.ones(mm.S)] * len(sub)
        for i in range(len(sub) - 2, -1, -1):
            b[i] = T @ (U[i + 1] * b[i + 1])
        Zc = a[-1].sum()
        tot += w * Zc
        for i in range(len(sub)):
            marg[i] += w * a[i] * b[i]
    marg /= tot
    assert np.allclose(marg, res['post'], atol=1e-8), np.abs(marg - res['post']).max()
    return True


# ------------------------------------------------------------------------------------------------ analyses
def posterior_table(m, r, ref=None):
    rows = []
    for i, e in enumerate(r['order']):
        p = r['post'][i]
        rp, cp = m.region_probs(p), m.coarse_probs(p)
        P0 = r['ev'][e][1]
        rp0 = m.region_probs(P0) if ref is None else ref[e]
        cand = r['ev'][e][2]
        top = np.argsort(-p)[:3]
        rows.append(dict(entry=e, block=m.d.block[e], confidence=m.d.econf[e], title=m.d.title[e],
                         candidates=';'.join(m.states[s] for s in cand),
                         p_on_candidates=round(float(p[cand].sum()), 4) if cand else 0.0,
                         p0_on_candidates=round(float(P0[cand].sum()), 4) if cand else 0.0,
                         top1=m.states[top[0]], p_top1=round(float(p[top[0]]), 4),
                         top2=m.states[top[1]], p_top2=round(float(p[top[1]]), 4),
                         top3=m.states[top[2]], p_top3=round(float(p[top[2]]), 4),
                         **{f'R_{k}': round(v, 4) for k, v in rp.items()},
                         **{f'R0_{k}': round(v, 4) for k, v in rp0.items()},
                         **{f'C_{k}': round(v, 4) for k, v in cp.items()},
                         tv_region_vs_prior=round(tv(rp, rp0), 4),
                         **{f'P_{m.states[s]}': round(float(p[s]), 4) for s in cand}))
    return rows


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


def _unused_coord_subsequence(data, cfg):
    """Entries with >=1 (non-excluded) candidate whose place has coordinates in places.json (strict) ."""
    ok = set()
    for r in data.cands:
        if r['order_derived'] in cfg['exclude_order_derived']:
            continue
        if data.place[r['place_id']]['coords_in_places_json'] == 'yes':
            ok.add(r['entry'])
    return [e for e in data.order if e in ok]


def null_tests(data, base_cfg, n_perm=20000, seed=1, w_grid=(0.25, 0.5, 0.75, 0.9, 0.98), lam_grid=(1.0, 2.0, 4.0, 8.0)):
    """Permutation tests of geographic coherence of the scroll order.

    Only entries with >= 1 candidate whose place has coordinates in places.json are used (strict), and only
    those candidates; a non-strict variant adds the derived/proxy places (tekoa_herodium, jordan_ford).
    Statistics: (i) descriptive mean expected log(1 + d_eff/ell) between consecutive entries (lower = more
    coherent); (ii) model log Bayes factor log ML(lambda) - log ML(0) (higher = more coherent).
    Null orders: full shuffles; shuffles within blocks A/B/C/D (local order beyond block grouping); and
    shuffles among entries whose top stated candidate lies in the same model region (keeps the sequence of
    regions, tests order WITHIN a region, i.e. route-like or same-site runs)."""
    rng = np.random.default_rng(seed)
    out = {}
    variants = [('all_candidates', (), True), ('no_documented_order_derived', ('documented',), True),
                ('no_documented_or_likely', ('documented', 'likely'), True),
                ('all_candidates_nonstrict', (), False)]
    for label, excl, strict in variants:
        cfg = cfg_with(**{**base_cfg, 'rho': 0.0, 'exclude_order_derived': excl, 'strict_coords': strict})
        m = Model(data, cfg)
        seq = [e for e in data.order if m.evidence([e])[e][2]]
        ev = m.evidence(seq)
        n = len(seq)
        Q = np.zeros((n, m.S))
        for i, e in enumerate(seq):
            cand = ev[e][2]
            Q[i, cand] = ev[e][1][cand]
            Q[i] /= Q[i].sum()
        C = m.W @ np.log1p(m.Deff / cfg['ell']) @ m.W.T
        pair = Q @ C @ Q.T
        obs = pair[np.arange(n - 1), np.arange(1, n)].mean()
        blocks = np.array([data.block[e] for e in seq])
        Lm = np.array([ev[e][0] for e in seq])

        def batch_logml(P, T):
            a = np.tile(m.pi, (P.shape[0], 1)) * Lm[P[:, 0]]
            z = a.sum(1); a /= z[:, None]; ll = np.log(z)
            for i in range(1, n):
                a = (a @ T) * Lm[P[:, i]]
                z = a.sum(1); a /= z[:, None]; ll += np.log(z)
            return ll
        ident = np.arange(n)[None, :]
        lind = batch_logml(ident, m.transition(0))[0]   # independence: order-invariant (= 0 by construction)
        Tl = {(w, lam): m.transition(w, lam) for w in w_grid for lam in lam_grid}
        res = dict(n_entries=n, entries=seq, strict_coords=strict, excluded=list(excl))
        # region of each entry's most probable stated candidate (for the within-region null)
        topreg = np.array([m.region_of[m.states[max(ev[e][2], key=lambda s_: ev[e][1][s_])]] for e in seq])
        for kind in ('full', 'within_block', 'within_region'):
            perms = np.empty((n_perm, n), int)
            for b in range(n_perm):
                if kind == 'full':
                    perms[b] = rng.permutation(n)
                else:
                    p = np.arange(n)
                    lab_ = blocks if kind == 'within_block' else topreg
                    for bl in sorted(set(lab_)):
                        ix = np.nonzero(lab_ == bl)[0]
                        p[ix] = rng.permutation(ix)
                    perms[b] = p
            sp = pair[perms[:, :-1], perms[:, 1:]].mean(1)
            res[f'desc_{kind}'] = dict(observed=round(float(obs), 4), null_mean=round(float(sp.mean()), 4),
                                       null_sd=round(float(sp.std()), 4),
                                       p_value=float((1 + (sp <= obs).sum()) / (1 + n_perm)))
            prof_obs, prof_null = -np.inf, np.full(n_perm, -np.inf)
            for (w, lam), T in Tl.items():
                lobs = batch_logml(ident, T)[0] - lind
                ll = np.concatenate([batch_logml(perms[i:i + 4000], T) for i in range(0, n_perm, 4000)]) - lind
                prof_obs, prof_null = max(prof_obs, lobs), np.maximum(prof_null, ll)
                if not (w == 0.98 and lam == 2.0):
                    continue
                res[f'logBF_w{w}_lam{lam}_{kind}'] = dict(observed=round(float(lobs), 3), null_mean=round(float(ll.mean()), 3),
                                                     null_q95=round(float(np.quantile(ll, 0.95)), 3),
                                                     p_value=float((1 + (ll >= lobs).sum()) / (1 + n_perm)))
            res[f'logBF_profile_{kind}'] = dict(observed=round(float(prof_obs), 3),
                                                null_mean=round(float(prof_null.mean()), 3),
                                                p_value=float((1 + (prof_null >= prof_obs).sum()) / (1 + n_perm)))
        out[label] = res
    return out


def fit_weights(data, base_cfg, wgrid=(0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.98, 0.995), lgrid=(1.0, 2.0, 4.0, 8.0)):
    """Type-II maximum likelihood over (w_A, w_L, lam). Note: candidates partly chosen using the order inflate it."""
    rows = []
    for lam in lgrid:
        for wa in wgrid:
            for wl in wgrid:
                m = Model(data, cfg_with(**{**base_cfg, 'w_A': wa, 'w_L': wl, 'lam': lam}))
                rows.append(dict(lam=lam, w_A=wa, w_L=wl, logml=round(m.run(with_post=False)['logml'], 4)))
    best = max(rows, key=lambda r: r['logml'])
    best_tied = max([r for r in rows if r['w_A'] == r['w_L']], key=lambda r: r['logml'])
    best_A0 = max([r for r in rows if r['w_A'] == 0], key=lambda r: r['logml'])
    return rows, best, best_tied, best_A0


def anchor_analysis(data, cfg, anchors):
    m = Model(data, cfg)
    full = m.run()
    pos = {e: i for i, e in enumerate(full['order'])}
    full_reg = {e: m.region_probs(full['post'][i]) for e, i in pos.items()}
    pi_reg = m.region_probs(m.pi)
    rows, infl = [], []
    for a in anchors:
        r = m.run(drop={a})
        ev_full = full['ev'][a]
        cand = ev_full[2]
        # the anchor's top candidate (by stated prior)
        top = max(cand, key=lambda s: ev_full[1][s])
        treg = m.region_of[m.states[top]]
        pa = r['post'][pos[a]]
        rp = m.region_probs(pa)
        rank = sorted(rp, key=lambda k: -rp[k]).index(treg) + 1
        rows.append(dict(entry=a, top_candidate=m.states[top], candidate_region=treg,
                         p_region_seq_only=round(rp[treg], 4), p_region_background=round(pi_reg[treg], 4),
                         lift=round(rp[treg] / pi_reg[treg], 3), region_rank=rank,
                         p_top_candidate_seq_only=round(float(pa[top]), 4),
                         p_top_candidate_background=round(float(m.pi[top]), 4),
                         p_any_candidate_seq_only=round(float(pa[cand].sum()), 4),
                         p_any_candidate_background=round(float(m.pi[cand].sum()), 4),
                         seq_only_top_region=max(rp, key=rp.get)))
        # influence of removing the anchor on every other entry
        ch = []
        for e, i in pos.items():
            if e == a:
                continue
            d_ = tv(m.region_probs(r['post'][i]), full_reg[e])
            if d_ > 0.02:
                ch.append((e, round(d_, 3)))
        ch.sort(key=lambda x: -x[1])
        infl.append(dict(removed=a, n_entries_changed_gt_0_02=len(ch),
                         max_tv=ch[0][1] if ch else 0.0, top_changed=';'.join(f'{e}:{v}' for e, v in ch[:6])))
    return rows, infl


def loo_all(data, cfg):
    """Leave-one-out predictive score for every entry with candidates: log(P_seq(candidate region)/pi(region))."""
    m = Model(data, cfg)
    full = m.run()
    pos = {e: i for i, e in enumerate(full['order'])}
    pi_reg = m.region_probs(m.pi)
    out = []
    for e in full['order']:
        cand = full['ev'][e][2]
        if not cand:
            continue
        P0 = full['ev'][e][1]
        r = m.run(drop={e})
        rp = m.region_probs(r['post'][pos[e]])
        # expected log-lift under the entry's own stated distribution over candidate regions
        creg = {}
        for s in cand:
            creg[m.region_of[m.states[s]]] = creg.get(m.region_of[m.states[s]], 0) + P0[s]
        tot = sum(creg.values())
        ll = sum(w / tot * math.log(rp[k] / pi_reg[k]) for k, w in creg.items())
        out.append(dict(entry=e, block=data.block[e], confidence=data.econf[e],
                        candidate_regions=';'.join(f'{k}:{v / tot:.2f}' for k, v in creg.items()),
                        seq_only_region_probs=';'.join(f'{k}:{v:.2f}' for k, v in sorted(rp.items(), key=lambda x: -x[1]) if v >= 0.05),
                        expected_log_lift=round(ll, 3)))
    return out


# ------------------------------------------------------------------------------------------------ main
TRACK = ['1', '2', '3', '4', '6', '11', '13', '14', '15', '16', '17', '19', '21', '23', '24', '25', '26', '27',
         '28', '29', '31', '32', '33', '34', '36', '37', '39', '40', '41', '42', '43', '44', '45', '47', '49', '50',
         '53', '54', '56', '60']


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('--inputs', default=os.path.join(here, '..', 'inputs'))
    ap.add_argument('--out', default=os.path.join(here, '..', 'outputs_fixed'))
    ap.add_argument('--config', default=None, help='JSON file overriding DEFAULT keys')
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--nperm', type=int, default=20000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    data = Data(a.inputs)
    t0 = time.time()
    assert self_test(data)
    print('self-test passed', round(time.time() - t0, 1), 's')
    over = json.load(open(a.config)) if a.config else {}
    summary = dict(version='v0-fixed-2026-10-08', date='2026-10-08', defaults=DEFAULT, config_overrides=over)

    # ---- 1. fit itinerary weights (type-II ML) without and with the name term
    fits = {}
    for lab, extra in [('rho0', dict(rho=0.0)), ('rho0.9', dict(rho=0.9))]:
        rows, best, best_t, best_a0 = fit_weights(data, {**over, **extra})
        write_csv(os.path.join(a.out, f'weight_fit_{lab}.csv'), rows)
        fits[lab] = dict(best=best, best_tied=best_t, best_wA0=best_a0,
                         logml_at_0=[r for r in rows if r['w_A'] == 0 and r['w_L'] == 0][0]['logml'])
        print('fit', lab, best, best_t, best_a0)
    summary['weight_fit'] = fits
    # main runs use lam fixed a priori at DEFAULT['lam'] (the free fit runs to the sharpest kernel, driven by
    # runs of identical candidates); the unconstrained optimum is kept as a variant.
    def best_at(lab, lam, cond=lambda r: True):
        rows = [r for r in csv.DictReader(open(os.path.join(a.out, f'weight_fit_{lab}.csv')))
                if float(r['lam']) == lam and cond(r)]
        r = max(rows, key=lambda r: float(r['logml']))
        return dict(lam=lam, w_A=float(r['w_A']), w_L=float(r['w_L']), logml=float(r['logml']))
    lam0 = cfg_with(**over)['lam']
    b0 = best_at('rho0', lam0)
    b9 = best_at('rho0.9', lam0)
    bt9 = best_at('rho0.9', lam0, lambda r: r['w_A'] == r['w_L'])
    bfree = fits['rho0.9']['best']
    summary['weight_fit_at_lam'] = dict(lam=lam0, rho0=b0, rho09=b9, rho09_tied=bt9)

    # ---- 2. main posteriors
    runs = {
        'M0_prior': dict(w_A=0, w_L=0, rho=0),
        'M1_itinerary_fitted': dict(w_A=b0['w_A'], w_L=b0['w_L'], lam=b0['lam'], rho=0),
        'M2_names_only': dict(w_A=0, w_L=0, rho=0.9),
        'M3_joint_fitted': dict(w_A=b9['w_A'], w_L=b9['w_L'], lam=b9['lam'], rho=0.9),
        'M4_joint_wA0': dict(w_A=0.0, w_L=b9['w_L'], lam=lam0, rho=0.9),
        'M6_joint_wA_eq_wL': dict(w_A=b9['w_L'], w_L=b9['w_L'], lam=lam0, rho=0.9),
        'M5_joint_free_fit': dict(w_A=bfree['w_A'], w_L=bfree['w_L'], lam=bfree['lam'], rho=0.9),
    }
    m0 = Model(data, cfg_with(**{**over, **runs['M0_prior']}))
    r0 = m0.run()
    ref = {e: m0.region_probs(r0['post'][i]) for i, e in enumerate(r0['order'])}
    allpost = {}
    for name, kw in runs.items():
        m = Model(data, cfg_with(**{**over, **kw}))
        r = m.run()
        rows = posterior_table(m, r, ref)
        write_csv(os.path.join(a.out, f'posterior_{name}.csv'), rows)
        allpost[name] = dict(cfg=kw, logml=round(r['logml'], 4), rows=rows,
                             zpost={g: {k: round(float(v), 4) for k, v in sorted(d.items(), key=lambda x: -x[1])[:5]}
                                    for g, d in r['zpost'].items()})
        print(name, kw, 'logml', round(r['logml'], 3))
    summary['runs'] = {k: dict(cfg=v['cfg'], logml=v['logml'], name_group_location_posteriors=v['zpost'])
                       for k, v in allpost.items()}
    json.dump(summary, open(os.path.join(a.out, 'summary.json'), 'w'), indent=1, default=str)
    if a.quick:
        return

    # ---- 3. pull table vs the stated-confidence prior
    pull = []
    for name in runs:
        if name == 'M0_prior':
            continue
        for row in allpost[name]['rows']:
            rp = {k[2:]: v for k, v in row.items() if k.startswith('R_')}
            r0p = {k[3:]: v for k, v in row.items() if k.startswith('R0_')}
            gain = {k: rp[k] - r0p[k] for k in rp}
            kmax = max(gain, key=gain.get)
            pull.append(dict(model=name, entry=row['entry'], block=row['block'], confidence=row['confidence'],
                             candidates=row['candidates'], tv=row['tv_region_vs_prior'],
                             region_gaining_most=kmax, gain=round(gain[kmax], 4),
                             p_region_prior=r0p[kmax], p_region_model=rp[kmax],
                             p_on_candidates_prior=row['p0_on_candidates'], p_on_candidates_model=row['p_on_candidates'],
                             top1=row['top1'], p_top1=row['p_top1']))
    write_csv(os.path.join(a.out, 'pull_table.csv'), pull)

    # ---- 4. anchors: leave-one-out and influence
    anchors = [e for e in data.order if data.econf[e] == 'medium']
    for lab, kw in [('itinerary_fitted', runs['M1_itinerary_fitted']), ('joint_fitted', runs['M3_joint_fitted'])]:
        rows, infl = anchor_analysis(data, cfg_with(**{**over, **kw}), anchors)
        write_csv(os.path.join(a.out, f'anchor_loo_{lab}.csv'), rows)
        write_csv(os.path.join(a.out, f'anchor_influence_{lab}.csv'), infl)
    for lab, kw in [('itinerary_fitted', runs['M1_itinerary_fitted']),
                    ('itinerary_wA0', dict(w_A=0.0, w_L=b0['w_L'], lam=lam0, rho=0))]:
        loo = loo_all(data, cfg_with(**{**over, **kw}))
        write_csv(os.path.join(a.out, f'loo_all_{lab}.csv'), loo)
        summary[f'loo_{lab}'] = {'all': round(float(np.mean([r['expected_log_lift'] for r in loo])), 3)}
        for bl in 'ABCD':
            v = [r['expected_log_lift'] for r in loo if r['block'] == bl]
            summary[f'loo_{lab}'][bl] = round(float(np.mean(v)), 3) if v else None

    # ---- 5. null tests
    nt = null_tests(data, over, n_perm=a.nperm)
    json.dump(nt, open(os.path.join(a.out, 'null_tests.json'), 'w'), indent=1)
    summary['null_tests'] = {k: {kk: vv for kk, vv in v.items() if kk != 'entries'} for k, v in nt.items()}

    # ---- 6. one-at-a-time sensitivity around the joint model (tracked entries; most probable region)
    base = dict(runs['M3_joint_fitted'])
    variants = [('base', {}), ('w_L0.5', dict(w_L=0.5)), ('w_L0.98', dict(w_L=0.98)),
                ('single_scale_1km', dict(scales=(1.0,), scale_w=(1.0,))), ('scales_1_5', dict(scales=(1.0, 5.0))),
                ('scales_1_20', dict(scales=(1.0, 20.0))),
                ('w_A0', dict(w_A=0.0)), ('w_A=w_L', dict(w_A=base['w_L'])),
                ('lam1', dict(lam=1.0)), ('lam4', dict(lam=4.0)),
                ('rho0', dict(rho=0.0)), ('rho0.5', dict(rho=0.5)), ('no_temper', dict(temper=False)),
                ('pi_region_equal', dict(pi_mode='region_equal')), ('u0.5', dict(u=0.5)), ('u2', dict(u=2.0)),
                ('sigmaU0.5', dict(sigma_U=0.5)), ('sigmaU5', dict(sigma_U=5.0)),
                ('conf_conservative', dict(conf_p=dict(medium=0.45, low=0.15))),
                ('conf_generous', dict(conf_p=dict(medium=0.75, low=0.45))),
                ('no_kohlit15', dict(readings=dict(kohlit15=False, solomon23=True))),
                ('shallum23', dict(readings=dict(kohlit15=True, solomon23=False))),
                ('drop_documented_od', dict(exclude_order_derived=('documented',))),
                ('drop_doc_likely_od', dict(exclude_order_derived=('documented', 'likely'))),
                ('strict_coords', dict(strict_coords=True)),
                ('nu1', dict(nu=1.0)), ('nu4', dict(nu=4.0))]
    sens = []
    for vn, kw in variants:
        m = Model(data, cfg_with(**{**over, **base, **kw}))
        r = m.run()
        pos = {e: i for i, e in enumerate(r['order'])}
        row = dict(variant=vn, logml=round(r['logml'], 3))
        for e in TRACK:
            cp = m.region_probs(r['post'][pos[e]])
            k = max(cp, key=cp.get)
            row[f'e{e}'] = f'{k}:{cp[k]:.2f}'
        sens.append(row)
    write_csv(os.path.join(a.out, 'sensitivity_oneatatime.csv'), sens)

    # ---- 7. itinerary weight sweep for tracked entries (lam fixed at the fitted value)
    sweep = []
    for w in (0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.98):
        for rho in (0.0, 0.9):
            for wa_mode in ('wA=wL', 'wA=0'):
                m = Model(data, cfg_with(**{**over, 'w_A': (w if wa_mode == 'wA=wL' else 0.0), 'w_L': w,
                                            'lam': lam0, 'rho': rho}))
                r = m.run()
                pos = {e: i for i, e in enumerate(r['order'])}
                row = dict(w=w, w_A_mode=wa_mode, rho=rho, logml=round(r['logml'], 3))
                for e in TRACK:
                    cp = m.region_probs(r['post'][pos[e]])
                    for reg in m.regions:
                        row[f'e{e}_{reg}'] = round(cp[reg], 3)
                sweep.append(row)
    write_csv(os.path.join(a.out, 'weight_sweep.csv'), sweep)
    json.dump(summary, open(os.path.join(a.out, 'summary.json'), 'w'), indent=1, default=str)
    print('done', round(time.time() - t0, 1), 's')


if __name__ == '__main__':
    main()

