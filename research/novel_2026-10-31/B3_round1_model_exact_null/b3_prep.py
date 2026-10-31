"""B3 step 1: rebuild the round-1 private stacks with the round-1 prep.py, unchanged.

prep.py is a verbatim copy of round 1 (bd06dcc6). Only its private output folder is redirected, by
setting the module global prep.PRIV at run time (no edit to the file). Output stacks go to
SP/products/B3/stacks/ (never committed). This script writes prep_registration_b3.json (numbers) and
compares every registration number with round 1's prep_registration.json (pinned copy at bd06dcc6):
reference frame, frames used, per-frame inliers, input-frame sha256, strip angle and crop size.
npz files are zip archives with a time stamp, so their file hashes cannot match round 1's; the content
hash of the arrays is recorded instead (stack_content_b3.sha256)."""
import os, sys, json, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
R1 = f'{SP}/products/B3/r1_pinned/research/novel_2026-10-30/B_analysis_by_synthesis'
import prep
prep.PRIV = f'{SP}/products/B3/stacks'
os.makedirs(prep.PRIV, exist_ok=True)


def content_hash(p):
    d = np.load(p)
    h = hashlib.sha256()
    for k in ('stack', 'mask', 'labels', 'ucs', 'films'):
        a = np.ascontiguousarray(d[k]); h.update(k.encode()); h.update(str(a.dtype).encode())
        h.update(str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


if __name__ == '__main__':
    cuts = [int(c) for c in sys.argv[1:]] or list(range(2, 24))
    old = json.load(open(f'{R1}/prep_registration.json'))
    res, cmp, ch = {}, {}, {}
    for c in cuts:
        r = prep.register(c); res[str(c)] = r
        o = old.get(str(c))
        same = {}
        for k in ('ref', 'n_frames', 'n_used', 'strip_angle_deg', 'crop_wh'):
            same[k] = (r.get(k) == o.get(k))
        same['reg'] = ([(x['uc'], x['inliers'], x['used'], x.get('sha256')) for x in r['reg']] ==
                       [(x['uc'], x['inliers'], x['used'], x.get('sha256')) for x in o['reg']])
        cmp[str(c)] = same
        ch[str(c)] = content_hash(f'{prep.PRIV}/cut{c:02d}.npz')
        print(c, {k: v for k, v in r.items() if k != 'reg'}, 'identical' if all(same.values()) else same, flush=True)
    json.dump(dict(registration=res, identical_to_round1=cmp), open(f'{HERE}/prep_registration_b3.json', 'w'), indent=1)
    with open(f'{HERE}/stack_content_b3.sha256', 'w') as f:
        for c in sorted(ch, key=int): f.write(f'{ch[c]}  cut{int(c):02d}.npz (array content)\n')
