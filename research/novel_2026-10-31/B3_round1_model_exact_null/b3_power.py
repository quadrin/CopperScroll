"""B3 design check (before the freeze; no image is used): operating characteristics of candidate decision
rules on the actual set structures of items_b3.json (76 new lines).

Toy model (local additivity). At each varied position every letter gets a score e ~ N(0,1); the true letter
gets + s (image signal) + lam (image-independent preference for the true letter, e.g. a letter-shape prior
that correlates with letter frequency); the centre string of a set gets + beta (image-independent centre
bias). The truth set and the decoy set of a line share the letter scores (same image, same row); the
wrong-column scoring has independent scores and no image signal (s = 0), but keeps lam and beta.
A fraction f_tie of varied positions is invisible (substituted letter off the strip): the centre ties there.
Centre first <=> the centre's letter wins at every varied position.
Rules compared (P(pass) over 1000 replicates):
  O  = orchestrator's suggestion: C1 and decoy-first not significantly above its exact null and T > D
  S2 = C1 and the decoy sign test (P < 0.05)
  V  = C1 and the decoy sign test and the wrong-column sign test (the frozen rule, b3_stats.decide)
Output power_sim.json."""
import json, os, sys, numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import b3_stats as ST
from b3_items import diffpos


def structure(it):
    T = it['candidates'][0]
    pos = Counter(diffpos(T, v) for v in it['candidates'][1:])
    p0 = diffpos(T, it['decoy'])
    return [(a, j == p0) for j, a in pos.items()]


def sim_line(st, s, beta, lam, f_tie, rng):
    t_ok = d_ok = w_ok = True
    for a, is_p0 in st:
        if rng.random() < f_tie: t_ok = d_ok = w_ok = False; continue
        e_true = rng.normal() + s + lam; e_w = rng.normal(size=a)
        if not is_p0:
            ok = e_true + beta > e_w.max(); t_ok &= ok; d_ok &= ok
        else:
            t_ok &= e_true + beta > e_w.max()
            d_ok &= e_w[0] + beta > np.concatenate([[e_true], e_w[1:]]).max()
        w_ok &= rng.normal() + lam + beta > rng.normal(size=a).max()
    return int(t_ok), int(d_ok), int(w_ok)


if __name__ == '__main__':
    items = json.load(open(f'{HERE}/items_b3.json'))
    sts = [structure(it) for it in items]; ps = [it['p_null'] for it in items]
    rng = np.random.default_rng(7); R = 1000; out = []
    grid = [(s, b, l) for s in (0.0, 0.5, 1.0, 1.5) for b in (0.0, 0.5) for l in (0.0, 0.5)]
    for f_tie in (0.0, 0.15):
        for s, beta, lam in grid:
            acc = Counter(); M = Counter()
            for _ in range(R):
                tdw = [sim_line(st, s, beta, lam, f_tie, rng) for st in sts]
                t, d, w = zip(*tdw)
                r = ST.decide(t, d, w, ps)
                M['T'] += r['T_truth_first']; M['D'] += r['D_decoy_first']; M['W'] += r['W_wrong_truth_first']
                acc['C1'] += r['C1']
                acc['O'] += r['C1'] and r['P_D_diag'] >= 0.05 and r['T_truth_first'] > r['D_decoy_first']
                acc['S2'] += r['C1'] and r['C2']
                acc['V'] += r['pass']
            row = dict(f_tie=f_tie, s=s, beta=beta, lam=lam, **{f'mean_{k}': round(M[k] / R, 2) for k in 'TDW'},
                       **{k: round(acc[k] / R, 3) for k in ('C1', 'O', 'S2', 'V')})
            out.append(row); print(row, flush=True)
    json.dump(dict(n_lines=len(items), expected_null=round(sum(ps), 3), reps=R, rows=out),
              open(f'{HERE}/power_sim.json', 'w'), indent=1)
