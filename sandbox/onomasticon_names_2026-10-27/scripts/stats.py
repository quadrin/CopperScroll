import csv, sys, math
O = sys.argv[1]; sfx = sys.argv[2] if len(sys.argv) > 2 else ''
s = list(csv.DictReader(open(f'{O}/summary{sfx}.csv')))
c2 = list(csv.DictReader(open(f'{O}/c2_result{sfx}.csv')))
def pb_tail(ps, k):   # Poisson-binomial P(X >= k)
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist):
            new[i] += d * (1 - p); new[i + 1] += d * p
        dist = new
    return sum(dist[k:])
def fisher_two(a, b, c, d):  # 2x2 [[a,b],[c,d]] two-sided
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def pr(x): return math.comb(c1, x) * math.comb(n - c1, r1 - x) / math.comb(n, r1)
    p0 = pr(a); lo = max(0, r1 - (n - c1)); hi = min(r1, c1)
    return sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 + 1e-12)
for col, c1col, c2col in [('match_primary', 'c1_rate_primary', 'primary'), ('any', 'c1_rate_any_set', 'any')]:
    if col == 'any':
        obs = sum(1 for r in s if r['match_primary'] == '1' or r['match_latin_only'] == '1' or r['match_body'] == '1')
    else:
        obs = sum(int(r[col]) for r in s)
    ps = [float(r[c1col]) for r in s]
    k2 = sum(1 for r in c2 if r[c2col] == 'True')
    print(f"[{col}] scroll {obs}/40 = {obs/40:.3f}; C1 expected {sum(ps):.1f}/40 = {sum(ps)/40:.3f}, P(X>={obs}) = {pb_tail(ps, obs):.3f}; "
          f"C2 {k2}/40 = {k2/40:.3f}, Fisher two-sided scroll vs C2 p = {fisher_two(obs, 40-obs, k2, 40-k2):.3f}")
