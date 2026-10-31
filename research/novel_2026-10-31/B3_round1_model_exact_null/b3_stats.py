"""B3 statistics and decision rule (frozen with PROTOCOL_FROZEN.md).

Per line i (three scorings with the frozen round-1 model):
  p_i = exact null chance that the centre of a set ranks strictly first
      = product over varied positions of 1/(a+1); identical for the truth set and its mirrored decoy set.
  t_i = 1 if the truth is strictly first in the truth set at its own line (a tie counts as 0)
  d_i = 1 if the decoy is strictly first in the decoy set at the line (a tie counts as 0)
  w_i = 1 if the truth is strictly first in the same truth set scored at the wrong column (c', l*) (a tie counts as 0)
T, D, W = sums. Under the exact null each is Poisson-binomial(p_1..p_n).
  C1 (signal beyond the exact null):      P(T >= T_obs) < 0.05.
  C2 (decoy control, centre bias):        exact one-sided sign test of t against d on discordant lines:
                                          n10 = #(t=1, d=0) > n01 = #(t=0, d=1) and P(Bin(n10+n01, 1/2) >= n10) < 0.05.
  C3 (wrong-column control, any image-independent preference for the true string):
                                          the same sign test of t against w: m10 > m01 and P < 0.05.
PASS iff C1 and C2 and C3.
Diagnostics (reported, not part of PASS): P(D >= D_obs) and P(W >= W_obs) under the exact null."""
import numpy as np
from math import comb
ALPHA = 0.05


def poibin_sf(ps, k):
    d = np.zeros(len(ps) + 1); d[0] = 1.0
    for q in ps: d = np.concatenate([d * (1 - q), [0]]) + np.concatenate([[0], d * q])
    return float(d[k:].sum())


def sign_p(n10, n01):
    n = n10 + n01
    if n == 0: return 1.0
    return sum(comb(n, k) for k in range(n10, n + 1)) / 2 ** n


def paired(a, b):
    n10 = sum(1 for x, y in zip(a, b) if x and not y); n01 = sum(1 for x, y in zip(a, b) if y and not x)
    n11 = sum(1 for x, y in zip(a, b) if x and y)
    return n10, n01, n11, sign_p(n10, n01)


def decide(t, d, w, ps):
    t, d, w, ps = list(map(int, t)), list(map(int, d)), list(map(int, w)), list(map(float, ps))
    T, D, W = sum(t), sum(d), sum(w)
    pT, pD, pW = poibin_sf(ps, T), poibin_sf(ps, D), poibin_sf(ps, W)
    n10, n01, n11, pS = paired(t, d)
    m10, m01, m11, pV = paired(t, w)
    c1, c2, c3 = pT < ALPHA, (n10 > n01) and pS < ALPHA, (m10 > m01) and pV < ALPHA
    return dict(n_lines=len(t), expected_null=round(sum(ps), 4),
                T_truth_first=T, P_T=round(pT, 6),
                D_decoy_first=D, P_D_diag=round(pD, 6), W_wrong_truth_first=W, P_W_diag=round(pW, 6),
                decoy_n10_truth_only=n10, decoy_n01_decoy_only=n01, decoy_n11_both=n11, P_sign_decoy=round(pS, 6),
                wrong_m10_right_only=m10, wrong_m01_wrong_only=m01, wrong_m11_both=m11, P_sign_wrong=round(pV, 6),
                C1=bool(c1), C2=bool(c2), C3=bool(c3), **{'pass': bool(c1 and c2 and c3)})


def evaluate(rows, wkind='wrongcol'):
    """rows: per-candidate dicts from b3_run.score (truth, decoy and wrong-column sets of the same lines).
    wkind = 'wrongcol' (frozen) or 'wrongline' (superseded exploratory same-column design).
    Lines missing any of the three scorings are not counted (none expected)."""
    lines = {}
    for r in rows:
        if int(r['is_centre']) != 1: continue
        lines.setdefault((int(r['col']), int(r['line'])), {})[r['kind']] = r
    keys = sorted(k for k in lines if all(x in lines[k] for x in ('truth', 'decoy', wkind)))
    g = lambda kind: [int(lines[k][kind]['centre_first']) for k in keys]
    t, d, w = g('truth'), g('decoy'), g(wkind)
    ps = [float(lines[k]['truth']['p_null']) for k in keys]
    out = decide(t, d, w, ps)
    m = [abs(float(lines[k]['truth']['margin_centre_minus_best_other'])) for k in keys]
    out['median_abs_truth_margin'] = round(float(np.median(m)), 3) if m else None
    out['n_ties_at_top'] = {kind: sum(1 for k in keys if float(lines[k][kind]['margin_centre_minus_best_other']) == 0.0)
                            for kind in ('truth', 'decoy', wkind)}
    out['per_line'] = [dict(col=k[0], line=k[1], p_null=p, truth_first=a, decoy_first=b, wrong_truth_first=c,
                            truth_rank=int(lines[k]['truth']['centre_rank']), decoy_rank=int(lines[k]['decoy']['centre_rank']),
                            wrong_truth_rank=int(lines[k][wkind]['centre_rank']))
                       for k, p, a, b, c in zip(keys, ps, t, d, w)]
    return out


FALLBACK = set('גזטנסצפךםף')   # round-1 glyphs.py: letter forms with font-skeleton templates (no scroll tracing)


def pairwise(rows, kinds=('truth', 'wrongcol')):
    """Diagnostic: fraction of variants scoring below the centre of their set, by template class of the substituted
    pair (from_fallback: centre letter has a font template; to_fallback: variant letter has one; traced_both)."""
    by = {}
    for r in rows:
        if r['kind'] in kinds: by.setdefault((r['kind'], int(r['col']), int(r['line'])), []).append(r)
    acc = {}
    for (k, c, l), rs in by.items():
        T = [r for r in rs if int(r['is_centre']) == 1][0]
        for r in rs:
            if int(r['is_centre']) == 1: continue
            i = [j for j, (a, b) in enumerate(zip(T['candidate'], r['candidate'])) if a != b][0]
            a, b = T['candidate'][i], r['candidate'][i]
            cl = 'to_fallback' if b in FALLBACK else 'from_fallback' if a in FALLBACK else 'traced_both'
            x = acc.setdefault(f'{k}:{cl}', [0, 0]); x[0] += float(r['loglik']) < float(T['loglik']); x[1] += 1
    return {k: dict(variant_below_centre=v[0], n=v[1], rate=round(v[0] / v[1], 3)) for k, v in sorted(acc.items())}


def diagnostics(rows):
    """Reported, not part of PASS: template-class pairwise rates; the test statistics without column I (cut 1
    missing) and without column VII (template column); per-column counts."""
    out = {'pairwise_by_template_class': pairwise(rows)}
    for name, col in (('without_column_I', 1), ('without_column_VII', 7)):
        out[name] = {k: v for k, v in evaluate([r for r in rows if int(r['col']) != col]).items() if k != 'per_line'}
    pc = {}
    for x in evaluate(rows)['per_line']:
        p = pc.setdefault(x['col'], dict(n=0, truth_first=0, decoy_first=0, wrong_truth_first=0, expected_null=0.0))
        p['n'] += 1; p['truth_first'] += x['truth_first']; p['decoy_first'] += x['decoy_first']
        p['wrong_truth_first'] += x['wrong_truth_first']; p['expected_null'] = round(p['expected_null'] + x['p_null'], 4)
    out['per_column'] = pc
    return out
