"""Lane H confirmatory run (one run after the freeze commit).

    python3 -I run_confirmatory.py BUILD_DIR CALIB_JSON TARGETS_JSON OUT_DIR

BUILD_DIR holds dss_train.txt, rab_train.txt and q15_words.json from prep.py.
Model: interpolated modified Kneser-Ney character 8-gram on DSS (non-biblical, no 3Q15) and
on Mishnah+Tosefta, mixed 0.5/0.5 per character. Context: up to W=3 graphic words each side
(a foreign word or an empty token stops the context; a number is the symbol 9).
Score: ln P(candidate + ' ' + right context | left context).
"""
import sys, os, json, math, csv
import numpy as np
from scipy.stats import binomtest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm import KN, Mix
from prior import window, score, softmax_T, fit_temperature

ORDER, LAM, W = 8, 0.5, 3
ALPHA, MIN_HELD = 0.01, 100
ALPHA_DIV = 0.01


def tokens_of(words):
    return [None if (w['kind'] == 'foreign' or not w['string']) else w['string'] for w in words]


def group_scores(model, toks, i, j, cands):
    l, r = window(toks, i, j, W)
    return [score(model, l, c, r) for c in cands]


def main():
    B, CAL, TGT, OUT = sys.argv[1:5]
    os.makedirs(OUT, exist_ok=True)
    rd = lambda f: [l.rstrip('\n') for l in open(os.path.join(B, f), encoding='utf-8') if l.strip()]
    model = Mix([KN(ORDER).fit(rd('dss_train.txt')), KN(ORDER).fit(rd('rab_train.txt'))], [LAM, 1 - LAM])
    words = json.load(open(os.path.join(B, 'q15_words.json')))
    toks = tokens_of(words)
    cal = json.load(open(CAL))
    K = cal['K']
    rows = []
    groups = {'calibration_training': [], 'held_out': [], 'names_descriptive': []}
    for it in cal['items'] + cal['names']:
        cands = [it['true']] + it['rivals']
        sc = group_scores(model, toks, it['token_index'], it['token_index'] + 1, cands)
        top1 = int(sc[0] > max(sc[1:]))
        rank = 1 + sum(s > sc[0] for s in sc[1:]) + sum(s == sc[0] for s in sc[1:])
        groups[it['split']].append((sc, 0))
        rows.append({'test': 'substitution', 'id': it['id'], 'split': it['split'], 'true': it['true'],
                     'candidates': '|'.join(cands), 'scores': '|'.join(f'{s:.4f}' for s in sc),
                     'top1': top1, 'rank_of_true': rank})
    dgroups = {'calibration_training': [], 'held_out': []}
    for it in cal['division']:
        sc = group_scores(model, toks, it['token_index'], it['token_index'] + it['span'], it['candidates'])
        top1 = int(sc[0] > max(sc[1:]))
        rank = 1 + sum(s > sc[0] for s in sc[1:]) + sum(s == sc[0] for s in sc[1:])
        dgroups[it['split']].append((sc, 0))
        rows.append({'test': 'division', 'id': it['id'], 'split': it['split'], 'true': it['candidates'][0],
                     'candidates': '|'.join(it['candidates']), 'scores': '|'.join(f'{s:.4f}' for s in sc),
                     'top1': top1, 'rank_of_true': rank})
    with open(os.path.join(OUT, 'calibration_results.csv'), 'w', newline='', encoding='utf-8') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader(); wr.writerows(rows)
    # primary test
    held = [r for r in rows if r['test'] == 'substitution' and r['split'] == 'held_out']
    n = len(held); k = sum(r['top1'] for r in held); p0 = 1 / (K + 1)
    pv = binomtest(k, n, p0, alternative='greater').pvalue
    passed = bool(n >= MIN_HELD and pv < ALPHA)
    # temperature from calibration-training only
    T, nll_cal = fit_temperature(groups['calibration_training'])
    def nll(gs, T):
        return float(-np.mean([np.log(softmax_T(s, T)[t]) for s, t in gs])) if gs else None
    def mean_p_true(gs, T):
        return float(np.mean([softmax_T(s, T)[t] for s, t in gs])) if gs else None
    def ece(gs, T, bins=10):
        conf, acc = [], []
        for s, t in gs:
            p = softmax_T(s, T); conf.append(p.max()); acc.append(int(np.argmax(p) == t))
        conf, acc = np.array(conf), np.array(acc); e = 0.0
        for b in range(bins):
            m = (conf > b / bins) & (conf <= (b + 1) / bins)
            if m.any():
                e += m.mean() * abs(conf[m].mean() - acc[m].mean())
        return float(e)
    # secondary: division
    dh = [r for r in rows if r['test'] == 'division' and r['split'] == 'held_out']
    dn, dk = len(dh), sum(r['top1'] for r in dh)
    dpv = binomtest(dk, dn, 0.25, alternative='greater').pvalue if dn else None
    Td, _ = fit_temperature(dgroups['calibration_training']) if dgroups['calibration_training'] else (None, None)
    nm = [r for r in rows if r['split'] == 'names_descriptive']
    # descriptive: rivals that are attested words in the training text ("hard" rivals)
    vocab = set()
    for f in ('dss_train.txt', 'rab_train.txt'):
        for l in rd(f):
            vocab.update(l.split())
    pair_n = pair_k = 0; hard_items = hard_top = 0
    for r in held:
        cands = r['candidates'].split('|'); sc = [float(x) for x in r['scores'].split('|')]
        att = [j for j in range(1, len(cands)) if cands[j] in vocab]
        if att:
            hard_items += 1; hard_top += int(all(sc[0] > sc[j] for j in att))
        for j in att:
            pair_n += 1; pair_k += int(sc[0] > sc[j])
    res = {
        'primary': {'test': 'substitution top-1 on held-out agreed 3Q15 words', 'n': n, 'top1': k,
                    'top1_rate': k / n if n else None, 'K_rivals': K, 'chance': p0, 'expected_by_chance': n * p0,
                    'p_exact_binomial_one_sided': pv, 'alpha': ALPHA, 'min_held_out': MIN_HELD, 'passed': passed},
        'calibration': {'temperature_T': T, 'nll_calibration_training': nll_cal,
                        'held_out_nll_T': nll(groups['held_out'], T), 'held_out_nll_T1': nll(groups['held_out'], 1.0),
                        'held_out_nll_uniform': math.log(K + 1),
                        'held_out_mean_p_true_T': mean_p_true(groups['held_out'], T),
                        'held_out_ece_T': ece(groups['held_out'], T)},
        'secondary_division': {'n': dn, 'top1': dk, 'chance': 0.25, 'expected_by_chance': dn * 0.25,
                               'p_exact_binomial_one_sided': dpv, 'alpha': ALPHA_DIV,
                               'passed': bool(dn and dpv < ALPHA_DIV),
                               'held_out_mean_p_true_T': mean_p_true(dgroups['held_out'], T)},
        'names_descriptive': {'n': len(nm), 'top1': sum(r['top1'] for r in nm),
                              'mean_p_true_T': mean_p_true(groups['names_descriptive'], T)},
        'descriptive_attested_rivals': {'held_out_items_with_attested_rival': hard_items,
                                        'true_above_all_attested_rivals': hard_top,
                                        'pairs_true_vs_attested_rival': pair_n, 'pairs_true_higher': pair_k,
                                        'true_word_attested_in_training': sum(r['true'] in vocab for r in held)},
        'model': {'order': ORDER, 'lambda_dss': LAM, 'window_words': W},
    }
    # targets
    tg = json.load(open(TGT))
    trows = []
    if passed:
        for t in tg['targets']:
            cands = [c['string'] for c in t['candidates']]
            sc = np.array(group_scores(model, toks, t['token_start'], t['token_end'], cands))
            lp = sc - (sc.max() + np.log(np.exp(sc - sc.max()).sum()))
            pc = softmax_T(sc, T)
            H = float(-(pc * np.log2(pc)).sum()); Hmax = math.log2(len(cands))
            for c, l, p in zip(t['candidates'], lp, pc):
                trows.append({'locus': t['locus'], 'candidate': c['string'], 'log_prior': f'{l:.4f}',
                              'calibrated_probability': f'{p:.4f}',
                              'notes': f"T={T:.3f}; entropy {H:.2f} of max {Hmax:.2f} bits; "
                                       f"{'length/division differs among candidates: calibrated only by the secondary division test (passed=' + str(res['secondary_division']['passed']) + ')' if len(set(tuple(i for i, ch in enumerate(x) if ch == ' ') + (len(x),) for x in cands)) > 1 else 'same length: covered by the primary substitution calibration'}; "
                                       f"source: {c['source']}"})
        res['targets_scored'] = True
    else:
        res['targets_scored'] = False
    with open(os.path.join(OUT, 'target_priors.csv'), 'w', newline='', encoding='utf-8') as f:
        if trows:
            wr = csv.DictWriter(f, fieldnames=['locus', 'candidate', 'log_prior', 'calibrated_probability', 'notes'])
            wr.writeheader(); wr.writerows(trows)
        else:
            f.write('NOT RUN: the primary held-out test did not pass, so priors are not evidence.\n')
    json.dump(res, open(os.path.join(OUT, 'confirmatory_result.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
