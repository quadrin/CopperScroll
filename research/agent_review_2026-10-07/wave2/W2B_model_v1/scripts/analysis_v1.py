#!/usr/bin/env python3
"""W2-B analyses on the v1 joint model.

  python3 -I analysis_v1.py STEP [--inputs ../inputs] [--out ../outputs]
STEP: v0check | density | fit | clamp | post | jsens | all
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joint_model_v1 as jm

PROPOSALS = ['tell_es_sultan', 'ein_samiya', 'muhalhil', 'beit_kahil', 'kuhlah', 'carmel_siah', 'mount_zion',
             'transjordan', 'ein_ghuweir', 'ein_feshkha']
KOH = ['4', '11', '15', '19', '60']
LOW, WEAK = 0.3 / 0.7, 0.1 / 0.9
SCHEMES = {
    'equal': {p: WEAK for p in PROPOSALS},                                    # agnostic among published proposals
    'atlas': {**{p: WEAK for p in PROPOSALS}, 'tell_es_sultan': LOW},        # T06/atlas: Tell es-Sultan the working hypothesis
    'v1': {**{p: WEAK for p in PROPOSALS}, 'tell_es_sultan': LOW, 'ein_samiya': LOW},  # order-free assessment (REPORT)
}
KERNELS = {
    'K1_sinkhorn': dict(transition='sinkhorn', grid_km=0),                   # T06 v0 kernel
    'K2_fixed': dict(transition='fixed', grid_km=0),                         # density-neutral arrival
    'K3_sinkhorn_grid': dict(transition='sinkhorn', grid_km=5, grid_mass=10.0),
    'K4_fixed_grid': dict(transition='fixed', grid_km=5, grid_mass=10.0),
}
EXCL = {
    'b0_none': dict(exclude_order_derived=(), exclude_kohlit_od=()),
    'b1_doc': dict(exclude_order_derived=('documented',), exclude_kohlit_od=()),
    'b2_doc_likely': dict(exclude_order_derived=('documented', 'likely'), exclude_kohlit_od=()),
    'b3_b2_plus_kohlit_od': dict(exclude_order_derived=('documented', 'likely'), exclude_kohlit_od=('documented', 'likely')),
}


def L10(x):
    return x / math.log(10)


def model(data, **kw):
    return jm.Model(data, jm.cfg_with(**kw))


# ------------------------------------------------------------------------------------------------ v0 check
def v0check(a):
    d0 = jm.Data(a.inputs, 'v0')
    m = model(d0, w_A=0.4, w_L=0.995, lam=2.0, rho=0.9, kohlit_scheme=None)
    r = m.run()
    ref = {row['entry']: row for row in csv.DictReader(open(os.path.join(
        a.inputs, '..', '..', '..', 'results', 'T06_joint_model', 'outputs', 'posterior_M3_joint_fitted.csv')))}
    pos = {e: i for i, e in enumerate(r['order'])}
    mx = max(abs(v - float(ref[e]['R_' + k])) for e in r['order'] for k, v in m.region_probs(r['post'][pos[e]]).items())
    out = dict(logml=round(r['logml'], 4), T06_M3_logml=8.6831, max_abs_region_diff=mx)
    print('v0 reproduction', out)
    json.dump(out, open(os.path.join(a.out, 'v0_reproduction_check.json'), 'w'), indent=1)


# ------------------------------------------------------------------------------------------------ density diagnostic
def density(a):
    """Why the T06 (Sinkhorn) kernel penalises Tell es-Sultan: inbound and self-transition factors T(a,b)/pi(b)."""
    rows = []
    for dname, suf in (('T06_v0_inputs', 'v0'), ('v1_inputs', 'v1')):
        d = jm.Data(a.inputs, suf)
        for kn, kk in KERNELS.items():
            if suf == 'v0' and kk.get('grid_km'):
                continue
            m = model(d, w_A=0.0, w_L=0.995, kohlit_scheme=SCHEMES['equal'], **kk)
            T = m.transition(0.995)
            for src in ('ibziq', 'gerizim', 'beth_shean', 'asla', 'wadi_qumran', 'jer_temple'):
                for dst in ('tell_es_sultan', 'jericho_area', 'U_JERICHO', 'ein_samiya', 'kh_yanun', 'carmel_siah', 'U_NORTH',
                            'jer_temple', 'beth_horon', 'kh_qumran', 'muhalhil', 'beit_kahil', 'mount_zion'):
                    if src not in m.idx or dst not in m.idx:
                        continue
                    rows.append(dict(inputs=dname, kernel=kn, src=src, dst=dst, dist_km=round(m.dist_states(src, dst), 1),
                                     T_over_pi=round(float(T[m.idx[src], m.idx[dst]] / m.pi[m.idx[dst]]), 3)))
            for s in ('tell_es_sultan', 'ein_samiya', 'carmel_siah', 'kh_yanun', 'ibziq', 'kh_qumran', 'jer_temple', 'beth_horon',
                      'beit_kahil'):
                if s in m.idx:
                    rows.append(dict(inputs=dname, kernel=kn, src=s, dst=s, dist_km=0.0,
                                     T_over_pi=round(float(T[m.idx[s], m.idx[s]] / m.pi[m.idx[s]]), 3)))
    jm.write_csv(os.path.join(a.out, 'density_diagnostic_transitions.csv'), rows)
    # wave-1 headline re-run on the T06 inputs with each kernel (entry 60 region posterior, M3 weights)
    d0 = jm.Data(a.inputs, 'v0')
    out = []
    for kn, kk in KERNELS.items():
        for (wa, wl) in ((0.4, 0.995), (0.0, 0.995), (0.0, 0.8)):
            for rho in (0.0, 0.9):
                m = model(d0, w_A=wa, w_L=wl, rho=rho, kohlit_scheme=None, **kk)
                r = m.run()
                pos = {e: i for i, e in enumerate(r['order'])}
                p = r['post'][pos['60']]
                rp = m.region_probs(p)
                out.append(dict(kernel=kn, w_A=wa, w_L=wl, rho=rho, e60_P_tell_es_sultan=round(float(p[m.idx['tell_es_sultan']]), 3),
                                **{f'e60_R_{k}': round(v, 3) for k, v in rp.items()}))
                print('T06 inputs', out[-1])
    jm.write_csv(os.path.join(a.out, 'wave1_entry60_by_kernel_T06inputs.csv'), out)


# ------------------------------------------------------------------------------------------------ weight fit
def fit(a):
    d = jm.Data(a.inputs, 'v1')
    rows = []
    for kn, kk in KERNELS.items():
        for en in ('b0_none', 'b2_doc_likely'):
            m = model(d, rho=0.9, kohlit_scheme=SCHEMES['equal'], **kk, **EXCL[en])
            for wa in (0.0, 0.4, 0.8):
                for wl in (0.0, 0.5, 0.8, 0.95, 0.995):
                    m.c['w_A'], m.c['w_L'] = wa, wl
                    t = time.time()
                    lm = m.run(with_post=False)['logml']
                    rows.append(dict(kernel=kn, excl=en, w_A=wa, w_L=wl, lam=2.0, logml=round(lm, 3)))
                    print(rows[-1], round(time.time() - t, 1), 's', flush=True)
    jm.write_csv(os.path.join(a.out, 'weight_fit_v1.csv'), rows)
    best = {}
    for kn in KERNELS:
        for en in ('b0_none', 'b2_doc_likely'):
            rr = [r for r in rows if r['kernel'] == kn and r['excl'] == en]
            b = max(rr, key=lambda r: r['logml'])
            best[f'{kn}|{en}'] = dict(w_A=b['w_A'], w_L=b['w_L'], logml=b['logml'],
                                      logml_at_0=[r for r in rr if r['w_A'] == 0 and r['w_L'] == 0][0]['logml'])
    json.dump(best, open(os.path.join(a.out, 'weight_fit_v1_best.json'), 'w'), indent=1)
    print(json.dumps(best, indent=1))


def fitted(a, kn, en):
    f = os.path.join(a.out, 'weight_fit_v1_best.json')
    best = json.load(open(f))
    key = f'{kn}|{"b0_none" if en in ("b0_none", "b1_doc") else "b2_doc_likely"}'
    return best[key]['w_A'], best[key]['w_L']


def order_settings(a, kn, en):
    wa, wl = fitted(a, kn, en)
    return {'off': (0.0, 0.0), 'fit': (wa, wl), 'wA0': (0.0, wl if wl > 0 else 0.995), 'weak': (0.0, 0.8),
            'T06': (0.4, 0.995)}


# ------------------------------------------------------------------------------------------------ clamp Bayes factors
def clamp(a):
    """Order Bayes factors for Kohlit locations, prior-free: clamp entries to one state, compare log ML."""
    d = jm.Data(a.inputs, 'v1')
    rows, land = [], []
    for kn, kk in KERNELS.items():
        for en in (('b0_none', 'b1_doc', 'b2_doc_likely') if not kk.get('grid_km') else ('b0_none', 'b2_doc_likely')):
            m = model(d, kohlit_scheme=SCHEMES['equal'], drop_groups=('Kohlit',), rho=0.9, **kk, **EXCL[en])
            one = np.ones(m.S)
            for on, (wa, wl) in order_settings(a, kn, en).items():
                if on == 'off' or (kk.get('grid_km') and on == 'wA0'):
                    continue
                m.c['w_A'], m.c['w_L'] = wa, wl
                for reading in ('milik_puech', 'janoah'):
                    m.c['readings']['xii10'] = reading

                    def score(c, ents):
                        v = np.zeros(m.S); v[m.idx[c]] = 1.0 / m.pi[m.idx[c]]
                        Lo = {e: one for e in KOH if not (reading == 'janoah' and e == '60')}
                        Lo.update({e: v for e in ents})
                        return m.run(with_post=False, L_override=Lo, skip_Z0=True)['logZE']
                    designs = {'tied_all': [e for e in KOH if not (reading == 'janoah' and e == '60')]}
                    per_entry = KOH if not kk.get('grid_km') else ['19', '60']
                    for e in per_entry:
                        if reading == 'janoah' and e == '60':
                            continue
                        designs[f'only_{e}'] = [e]
                    for dn, ents in designs.items():
                        base = score('tell_es_sultan', ents)
                        targets = PROPOSALS + (['kh_yanun'] if dn == 'only_60' else [])
                        for c in targets:
                            rows.append(dict(kernel=kn, excl=en, order=on, w_A=wa, w_L=wl, reading=reading, design=dn,
                                             candidate=c, dlog10_vs_tell=round(L10(score(c, ents) - base), 3)))
                    # landscape over all named/U states for the tied design (fit order only, b0/b2, no grid cells)
                    if on == 'fit' and en in ('b0_none', 'b2_doc_likely') and kn != 'K3_sinkhorn_grid':
                        ents = designs['tied_all']
                        base = score('tell_es_sultan', ents)
                        sc = []
                        for s in m.states:
                            if s.startswith('G_'):
                                continue
                            sc.append((L10(score(s, ents) - base), s))
                        sc.sort(reverse=True)
                        for rk, (v, s) in enumerate(sc):
                            land.append(dict(kernel=kn, excl=en, reading=reading, rank=rk + 1, state=s, region=m.region_of[s],
                                             dlog10_vs_tell=round(v, 3)))
                print(kn, en, on, 'done', flush=True)
    jm.write_csv(os.path.join(a.out, 'clamp_order_bayes_factors.csv'), rows)
    jm.write_csv(os.path.join(a.out, 'clamp_landscape_tied.csv'), land)


# ------------------------------------------------------------------------------------------------ posterior grid
def near_mass(m, p, c, km=10.0):
    ci = m.idx[c]
    dd = m.W @ m.D @ m.W[ci]
    return float(p[dd <= km].sum())


def summarize(m, r, tag):
    pos = {e: i for i, e in enumerate(r['order'])}
    out = []
    z = r.get('zpost', {}).get('Kohlit')
    zr = None
    if z:
        zr = {k: 0.0 for k in set(m.region_of.values())}
        for s, v in z.items():
            zr[m.region_of[s]] += v
    for c in PROPOSALS + ['kh_yanun']:
        row = dict(tag, candidate=c, region=m.region_of[c],
                   group_P=(round(float(z.get(c, 0.0)), 4) if z else ''),
                   group_P_region=(round(zr[m.region_of[c]], 4) if z else ''))
        for e in KOH:
            if e in pos:
                p = r['post'][pos[e]]
                row[f'e{e}_P'] = round(float(p[m.idx[c]]), 4)
                row[f'e{e}_P10km'] = round(near_mass(m, p, c), 4)
        out.append(row)
    return out


def post(a):
    d = jm.Data(a.inputs, 'v1')
    rows = []
    t0 = time.time()
    for kn in ('K1_sinkhorn', 'K2_fixed', 'K4_fixed_grid'):
        kk = KERNELS[kn]
        for en in ('b0_none', 'b2_doc_likely', 'b3_b2_plus_kohlit_od'):
            for tie in ('tied', 'untied'):
                m = model(d, kohlit_scheme=SCHEMES['equal'], rho=(0.9 if tie == 'tied' else 0.0), **kk, **EXCL[en])
                for on, (wa, wl) in order_settings(a, kn, en).items():
                    if on == 'T06':
                        continue
                    m.c['w_A'], m.c['w_L'] = wa, wl
                    for reading in ('milik_puech', 'janoah'):
                        m.c['readings']['xii10'] = reading
                        schemes = ['equal', 'atlas', 'v1'] if (on == 'fit' and en != 'b3_b2_plus_kohlit_od') else ['equal']
                        for sn in schemes:
                            m.c['kohlit_scheme'] = SCHEMES[sn]
                            r = m.run()
                            tag = dict(kernel=kn, excl=en, tie=tie, order=on, w_A=wa, w_L=wl, reading=reading, scheme=sn,
                                       logml=round(r['logml'], 3))
                            rows += summarize(m, r, tag)
                        m.c['kohlit_scheme'] = SCHEMES['equal']
                print(kn, en, tie, 'done', round(time.time() - t0), 's', flush=True)
                jm.write_csv(os.path.join(a.out, 'posterior_grid_v1.csv'), rows)
    jm.write_csv(os.path.join(a.out, 'posterior_grid_v1.csv'), rows)


def jsens(a):
    """Janoah coupling sensitivity (tied, fitted order, b0)."""
    d = jm.Data(a.inputs, 'v1')
    rows = []
    if os.environ.get('JSENS_LR_ONLY'):
        return jsens_lr(a, d)
    for kn in ('K1_sinkhorn', 'K2_fixed', 'K4_fixed_grid'):
        wa, wl = fitted(a, kn, 'b0_none')
        for sn in ('equal', 'v1'):
            m = model(d, kohlit_scheme=SCHEMES[sn], rho=0.9, w_A=wa, w_L=wl, **KERNELS[kn])
            m.c['readings']['xii10'] = 'janoah'
            for mode in ('soft', 'hard'):
                for ell in (5.0, 10.0, 20.0, 40.0):
                    for rJ in (0.0, 0.5, 0.9, 1.0):
                        m.c['janoah'].update(mode=mode, ell=ell, rho=rJ)
                        r = m.run()
                        rows += summarize(m, r, dict(kernel=kn, scheme=sn, mode=mode, ell_J=ell, rho_J=rJ))
            print(kn, sn, 'done', flush=True)
    jm.write_csv(os.path.join(a.out, 'janoah_sensitivity.csv'), rows)
    jsens_lr(a, d)


def jsens_lr(a, d):
    # pure Janoah likelihood ratio per candidate (continuous normalisation cancels): h * (1+d/ell)^-nu
    m = model(d, kohlit_scheme=SCHEMES['equal'])
    lr = []
    t = m.idx['kh_yanun']
    for c in PROPOSALS:
        dkm = m.dist_states(c, 'kh_yanun')
        for mode in ('soft', 'hard'):
            for ell in (5.0, 10.0, 20.0, 40.0):
                m.c['janoah'].update(mode=mode, ell=ell)
                hf = float(m.janoah_factor([m.idx[c]])[0])
                lr.append(dict(candidate=c, dist_to_kh_yanun_km=round(dkm, 1), mode=mode, ell_J=ell, hf=hf))
    for row in lr:
        ref = [x for x in lr if x['candidate'] == 'tell_es_sultan' and x['mode'] == row['mode'] and x['ell_J'] == row['ell_J']][0]
        row['dlog10_vs_tell'] = round(math.log10(row['hf'] / ref['hf']), 3)
    for row in lr:
        row['hf'] = f"{row['hf']:.3e}"
    jm.write_csv(os.path.join(a.out, 'janoah_likelihood_ratios.csv'), lr)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('step')
    ap.add_argument('--inputs', default=os.path.join(here, '..', 'inputs'))
    ap.add_argument('--out', default=os.path.join(here, '..', 'outputs'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    steps = ['v0check', 'density', 'fit', 'clamp', 'post', 'jsens'] if a.step == 'all' else [a.step]
    for s in steps:
        t = time.time()
        globals()[s](a)
        print('STEP', s, 'took', round(time.time() - t), 's', flush=True)
