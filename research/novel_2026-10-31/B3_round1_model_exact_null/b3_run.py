"""B3 runs. Scores candidate sets with the round-1 model, unchanged (via b3_score.py).

  python3 b3_run.py explore_r1   EXPLORATORY: round 1's 25 exposed lines, truth sets and decoy sets
                                 -> explore_r1_rankings.csv, explore_r1_summary.json
  python3 b3_run.py explore_r1_wrongline | explore_r1_wrongcol | explore_r1_summary   EXPLORATORY controls, same lines
  python3 b3_run.py confirm_shard k n   CONFIRMATORY (once, after the freeze): items_b3.json[k::n], all three sets
  python3 b3_run.py confirm_merge n     merge the n shards -> confirm_rankings.csv, confirm_result.json
                                        (b3_stats.evaluate), then targets only on PASS -> target_rankings_b3.csv

One row per candidate. 'centre' = the string the set was built around (truth for a truth set, decoy for a
decoy set). centre_first = 1 only if the centre's score is strictly greater than every other score in its
set (a tie counts against the centre)."""
import os, sys, json, csv, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import b3_score as S
import b3_stats as ST
PRIVRUN = f'{S.SP}/products/B3/runs'   # shard outputs before the merge (numbers only)
os.makedirs(PRIVRUN, exist_ok=True)


def score(kind, it, cands, run, at_col=None, at_line=None):
    t0 = time.time()
    at_col = at_col or it['col']; at_line = at_line or it['line']
    tot, info = S.score_set(at_col, at_line, cands)
    centre = cands[0]
    best_other = max(tot[c] for c in cands if c != centre)
    rank = lambda k: 1 + sum(1 for c in cands if c != k and tot[c] >= tot[k])
    rows = []
    for c in cands:
        rows.append(dict(run=run, set=it['set'], kind=kind, col=it['col'], line=it['line'], scored_at_col=at_col, scored_at_line=at_line,
                         n_candidates=len(cands),
                         candidate=c, is_centre=int(c == centre), is_truth=int(c == it['truth']),
                         loglik=round(tot[c], 3), rank=rank(c), centre_rank=rank(centre),
                         centre_first=int(tot[centre] > best_other),
                         margin_centre_minus_best_other=round(tot[centre] - best_other, 3),
                         p_null=it['p_null'], strips=S.strips(info)))
    print(run, kind, it['col'], it['line'], 'centre rank', rank(centre), 'of', len(cands),
          f'{time.time() - t0:.0f}s', flush=True)
    return rows


def write(path, rows):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def run_sets(items, run, kinds=('truth', 'decoy', 'wrongcol')):
    rows = []
    for it in items:
        if 'truth' in kinds: rows += score('truth', it, it['candidates'], run)
        if 'decoy' in kinds: rows += score('decoy', it, it['decoy_candidates'], run)
        if 'wrongline' in kinds: rows += score('wrongline', it, it['candidates'], run, at_line=it['wrong_line'])
        if 'wrongcol' in kinds: rows += score('wrongcol', it, it['candidates'], run, at_col=it['wrong_col'],
                                              at_line=it['wrong_col_line'])
    return rows


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'explore_r1_wrongline':
        # EXPLORATORY, added after the explore_r1 truth/decoy run had started: wrong-line sets of the 25 exposed lines
        items = json.load(open(f'{HERE}/items_r1_decoy.json'))
        write(f'{HERE}/explore_r1_wrongline_rankings.csv', run_sets(items, 'exploratory_r1', kinds=('wrongline',)))
    elif mode == 'explore_r1_wrongcol':
        # EXPLORATORY: wrong-column sets of the 25 exposed lines (the design frozen for the new lines)
        items = json.load(open(f'{HERE}/items_r1_decoy.json'))
        write(f'{HERE}/explore_r1_wrongcol_rankings.csv', run_sets(items, 'exploratory_r1', kinds=('wrongcol',)))
    elif mode == 'explore_r1_summary':
        rows = list(csv.DictReader(open(f'{HERE}/explore_r1_rankings.csv')))
        rows += list(csv.DictReader(open(f'{HERE}/explore_r1_wrongline_rankings.csv')))
        if os.path.exists(f'{HERE}/explore_r1_wrongcol_rankings.csv'):
            rows += list(csv.DictReader(open(f'{HERE}/explore_r1_wrongcol_rankings.csv')))
        out = {}
        for wk in ('wrongline', 'wrongcol'):
            if not any(r['kind'] == wk for r in rows): continue
            for sel in ('r1_heldout', 'r1_train', 'all'):
                out[f'{sel}__control_{wk}'] = ST.evaluate([r for r in rows if sel == 'all' or r['set'] == sel], wkind=wk)
        out['pairwise_by_template_class_all25'] = ST.pairwise(rows, kinds=('truth', 'wrongline', 'wrongcol'))
        json.dump(out, open(f'{HERE}/explore_r1_summary.json', 'w'), indent=1)
        print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'per_line'} for k, v in out.items()}, indent=1))
    elif mode == 'explore_r1':
        items = json.load(open(f'{HERE}/items_r1_decoy.json'))
        rows = run_sets(items, 'exploratory_r1', kinds=('truth', 'decoy'))
        write(f'{HERE}/explore_r1_rankings.csv', rows)
        out = {}
        for sel in ('r1_heldout', 'r1_train', 'all'):
            rr = [r for r in rows if sel == 'all' or r['set'] == sel]
            out[sel] = ST.evaluate(rr)
        json.dump(out, open(f'{HERE}/explore_r1_summary.json', 'w'), indent=1)
        print(json.dumps(out, indent=1))
    elif mode == 'confirm_shard':
        # CONFIRMATORY, once: shard k of n scores items[k::n] (truth, decoy and wrong-column sets)
        k, n = int(sys.argv[2]), int(sys.argv[3])
        out = f'{PRIVRUN}/confirm_shard_{k}_of_{n}.csv'
        assert not os.path.exists(out) and not os.path.exists(f'{HERE}/confirm_rankings.csv'), 'already run'
        items = json.load(open(f'{HERE}/items_b3.json'))[k::n]
        write(out, run_sets(items, 'confirmatory'))
    elif mode == 'confirm_merge':
        assert not os.path.exists(f'{HERE}/confirm_rankings.csv'), 'confirmatory run already merged'
        n = int(sys.argv[2])
        rows = []
        for k in range(n): rows += list(csv.DictReader(open(f'{PRIVRUN}/confirm_shard_{k}_of_{n}.csv')))
        items = json.load(open(f'{HERE}/items_b3.json'))
        order = {(it['col'], it['line']): i for i, it in enumerate(items)}
        kord = {'truth': 0, 'decoy': 1, 'wrongcol': 2}
        rows.sort(key=lambda r: (order[(int(r['col']), int(r['line']))], kord[r['kind']]))
        assert len({(r['col'], r['line'], r['kind']) for r in rows}) == 3 * len(items)
        write(f'{HERE}/confirm_rankings.csv', rows)
        res = ST.evaluate(rows)
        res['diagnostics_not_part_of_pass'] = ST.diagnostics(rows)
        json.dump(res, open(f'{HERE}/confirm_result.json', 'w'), indent=1)
        print('CONFIRMATORY RESULT', json.dumps({k: v for k, v in res.items() if k != 'per_line'}, indent=1), flush=True)
        if res['pass']:
            import b3_targets
            b3_targets.run(res)
        else:
            write(f'{HERE}/target_rankings_b3.csv', [dict(target='ALL', label='', candidate='', loglik='', rank='',
                  delta_from_best='', lean='', strips='NOT RUN: frozen decision rule not passed (targets not scored)')])
