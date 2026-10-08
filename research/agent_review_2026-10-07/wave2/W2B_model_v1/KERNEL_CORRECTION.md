# Ordering kernel correction — 8 October 2026 UTC

The active T06 runner and `joint_model_v1.py` now default to W2B K2, the existing
fixed-normalizer alternative. With distance kernel K, background measure π,
s(a) = Σ_b π(b)K(a,b), and C = max_a s(a), its local transition is
Tloc(a,b) = π(b)[K(a,b)/C + 1 − s(a)/C]. The itinerary mixture remains
T = (1−w)π + w Tloc. Explicit `transition="sinkhorn"` retains the old algorithm
for historical reproduction. New command-line runs write to `outputs_fixed/`;
the historical reports and outputs remain available with their original scope.

K2 removes the destination-specific Sinkhorn multiplier that boosted isolated
places and penalized arrivals at the crowded Jericho cluster. It is the smallest
already-reviewed correction that preserves the distance kernel, component
uncertainties, evidence odds and exact inference. This choice is an exploratory
model decision based on the W2B diagnostic, not an independently validated spatial
prior. Its arrival factor is neutral to destination-specific rebalancing; the
whole model still depends on its finite state list and background prior.

π is generally not stationary under K2. Unobserved entries can drift even with
no evidence. The validator checks this against direct Markov propagation rather
than forcing the old stationarity assertion. K4 (K2 plus the existing 5-km
background grid) remains a sensitivity alternative. Adding a new candidate with
new prior mass can change results. Splitting a coincident state while preserving
its total mass leaves aggregate transitions unchanged; this does not imply
invariance to arbitrary candidate additions, evidence duplication or grid bounds.

## Validation

`scripts/test_order_kernel.py` passes six tests: row normalization/non-negativity,
order-off prior recovery, historical artifact regression, matching T06/v1 exact
inference in both modes, direct no-evidence propagation, preserved-mass coincident
splitting, and invalid-mode rejection (the first test combines two checks).
Legacy tied inference reproduces log ML 8.6831. On the unchanged T06 inputs,
untied entry 60 has Tell es-Sultan probability 0.300 with order off, 0.099 under
legacy Sinkhorn, and 0.279 under K2; the NORTH-region probability changes from
0.711 under legacy Sinkhorn to 0.104 under K2.

`scripts/check_order_kernel.py` records 30 bounded runs in
[kernel_sensitivity.csv](outputs_fixed/kernel_sensitivity.csv), with input/code
hashes in [kernel_validation.json](outputs_fixed/kernel_validation.json).
The grid, name ties, block-A weight and documented/likely order-derived exclusions
remain explicit. These probabilities describe the specified conditional model;
they are not probabilities that the site identification or treasure is correct.
The full old weight-fit/permutation program was not rerun. Old fitted weights are
sensitivity settings here, not new optimized weights or current significance claims.

## Entry-60 registry

[registry_v2_entry60.json](registry_v2_entry60.json) supersedes the seven historical
entry-60 records only, with the two W2B additions (Kh. Yanun and Tell Muhalhil).
All nine are exploratory. W2B's old heuristic probabilities remain explicitly
historical; current target probabilities are null. No confidence, coordinate,
outcome, source-count or identification increment follows from this model correction.

Tell es-Sultan stays first in the desk-work queue; the old order demotion is
withdrawn. Kenyon II's pits/shafts and graves do not establish the joint
pit-mouth/tomb-mouth relation. The 1898 reservoir supplies no Herodian pool match.
The Samiya target is north of Kh. el-Marjama; southern Roman tombs cannot supply
that northern relation. The supplied HA 76 p.19 settlement report lacks the
hydraulic observation; Kallai's exact pages/pool remain outstanding. Newly supplied
Kenyon III pp.173–174 describes about18 north-slope graves dated by type to the
first century AD and later undated quarry pits that truncate graves. III source
access is resolved; an early usable pit-mouth/tomb-mouth relation is unestablished,
and the separate E section/Plate111b remains needed. The Janoaḥ
reading routes entry 60 to Kh. Yanun/Yanun; report silence there is unknown coverage.

No new Manchester master image was inspected. The
[image protocol](../../wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md)
must be committed and its commit SHA recorded before any reserved image opens.
Known plates, editions and descriptions have prior exposure; newly supplied
copies cannot be called holdouts. No unused field prediction or regional
discrimination has been established. Entry-60 identification remains
**not identifiable from available evidence**.
