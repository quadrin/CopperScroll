"""B3 scoring wrapper around the round-1 model, unchanged.

model.py, abs_score.py and frozen_params.json are verbatim copies of round 1 (commit bd06dcc6).
Run-time path adaptations only (no file edits):
  1. model.PRIV  -> SP/products/B3/stacks   (round 1: /root/novel/private_outputs/B/stacks)
  2. abs_score.REND -> SP/products/B3/renderings (round 1: /root/novel/private_outputs/B/renderings);
     the os.makedirs call that abs_score runs at import is suppressed during the import, so nothing is
     created under /root. B3 never passes save=, so no rendering is written.
Parameters: P = dict(model.DEFAULT); P.update(frozen_params.json), exactly as round-1 confirm.py.
Scoring: abs_score.score_line(col, line, cands, P) exactly as round 1 (registration shared by the
candidates of ONE set; line score = sum over the column's cuts)."""
import os, sys, json, csv, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
import model as m
m.PRIV = f'{SP}/products/B3/stacks'
_mk = os.makedirs
os.makedirs = lambda *a, **k: None
try:
    import abs_score as A
finally:
    os.makedirs = _mk
A.REND = f'{SP}/products/B3/renderings'
FROZEN = json.load(open(f'{HERE}/frozen_params.json'))
P = dict(m.DEFAULT); P.update(FROZEN)


def score_set(col, line, cands):
    tot, info = A.score_line(col, line, list(cands), P)
    return tot, info


def strips(info):
    return ';'.join(f"{i['cut']}:{i['status']}:o{i.get('orient','')}:y{i.get('y','')}" for i in info)


if __name__ == '__main__' and sys.argv[1:2] == ['verify']:
    # reproduce round-1 confirmatory log-likelihoods for the given held-out lines (exposed, published numbers)
    R1 = f'{SP}/products/B3/r1_pinned/research/novel_2026-10-30/B_analysis_by_synthesis'
    rows = list(csv.DictReader(open(f'{R1}/calibration_rankings.csv')))
    items = {(x['col'], x['line']): x for x in json.load(open(f'{HERE}/calibration_items.json'))}
    want = [tuple(map(int, a.split(':'))) for a in sys.argv[2:]]
    out = []
    for c, l in want:
        it = items[(c, l)]
        tot, info = score_set(c, l, it['candidates'])
        for r in rows:
            if (int(r['col']), int(r['line'])) == (c, l):
                d = round(tot[r['candidate']], 3) - float(r['loglik'])
                out.append(dict(col=c, line=l, candidate=r['candidate'], r1_loglik=r['loglik'],
                                b3_loglik=round(tot[r['candidate']], 3), diff=round(d, 3),
                                r1_strips=r['strips'], b3_strips=strips(info)))
                print(c, l, r['loglik'], round(tot[r['candidate']], 3), round(d, 3), r['strips'] == strips(info), flush=True)
    path = f'{HERE}/verify_round1_reproduction.csv'
    old = list(csv.DictReader(open(path))) if os.path.exists(path) else []
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(old + out)
