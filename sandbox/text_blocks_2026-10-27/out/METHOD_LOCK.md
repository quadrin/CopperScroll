# Run 13 method lock (written after step 1, before any segmentation is computed)

Feature matrix: out/feature_matrix.csv, SHA-256 f68c9c67bc5e7edc035fff2c84700d5c55409fe7fabdb758e4148bed31d08447, written 2026-10-27T06:01:20Z.
Sequence: the 61 entries in Puech order (1–12, 12a, 13–60), positions 0–60.

## Step 2, primary method (M1; the decision uses this one)
- Exact optimal segmentation by dynamic programming over all segmentations with K seams (the global optimum that PELT also finds), K = 1..5, minimum segment length 3 entries.
- Cost of a segment = −2 log-likelihood under independent per-feature models fitted by maximum likelihood inside the segment:
  Bernoulli for depth, vessels, direction, named, greek; multinomial for unit (5 levels: none, kk, kkrin, kkr, kk+kkrin), metal (4), digform (3);
  Gaussian for log(nwords) with segment mean and the variance fixed at the whole-sequence variance.
- Parameters per segment p = 5 + 4 + 3 + 2 + 1 = 15. BIC(K) = cost(K) + [(K+1)·p + K]·ln 61. K* = argmin BIC over K = 1..5 (the rule allows 1–5 seams).
- Statistic: gain G = BIC(0) − BIC(K*) (can be negative).

## Step 3, control
- 10,000 random permutations of the entry order (numpy default_rng seed 20261027); each permutation runs the identical procedure (K* re-chosen by BIC).
- p = share of permutations with G_perm ≥ G_obs; also reported as (count+1)/(10,001).

## Secondary method (M2; sensitivity only, does not decide)
- Same DP, K = 1..5, min length 3. Gower dissimilarity d_ij = mean over the 9 features of: 0/1 mismatch (binary and categorical), |ln n_i − ln n_j| / range(ln n) for nwords.
- Segment cost W_s = (1/n_s) Σ_{i<j in s} d_ij (distance analogue of the within-segment sum of squares); W(K) = Σ_s W_s.
- Criterion(K) = 61·ln(W(K)/61) + K·(9+1)·ln 61; gain = Criterion(0) − min_K Criterion(K); same 10,000 permutations.

## Step 4, geography
- Regions from run 8's anchors (sandbox/route_travel_time_2026-10-27/out/anchors.csv).
  Primary = run 8's anchor set P: 9, 10, 35, 49, 51 → Kidron/Jerusalem; 57 → Gerizim; 58 → Beth-shean.
  Deviation D1 (set D1 of that file): adds 31 Doq and 32 Choziba → Jericho, 55 Bethesda → Kidron/Jerusalem; 38 Naṭof is in none of the rule's five regions and is left out.
  Deviation D2 (set D2 of that file, circular per run 8): D1 plus 17 Nuweimeh → Jericho, 20–22 Qumran → Sekakah, 46 Ramat Raḥel → Kidron/Jerusalem.
- A regional change lies between consecutive anchors (in scroll order) of different regions, at positions pa < pb; the change boundary can be any t with pa < t ≤ pb (t = position of the first entry of the new block).
- Primary matching (literal "within ±2 entries of a change"): seam t matches if pa+1−2 ≤ t ≤ pb+2.
  Stricter alternative (reported): seam matches if |t − pb| ≤ 2 or |t − (pa+1)| ≤ 2 — i.e. near either end of the gap (identical to the primary when the gap is ≤ 5 entries).
- Supported (exploratory) iff p < 0.01 (M1) and ≥ half of the M1 seams match (primary regions P, primary matching).
