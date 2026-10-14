# Entry 25 existing-evidence audit — 13 October 2026 UTC

Claim evaluated: whether existing cave catalogue records satisfy entry 25's reported cave form under the saved pillar/terrace, cave/both-mouth aspect and four coding rule sets. This is exploratory. All evidence was already exposed in the repository. Identification of a particular ancient landmark remains **not identifiable from available evidence**.

## Actual result

Replaying the saved evaluator reproduces the frozen regional summary exactly. Joining the frozen inventory to the already committed phase 1–4 additions reproduces its current headline and complete all-match lists. The current input contains 643 cave catalogue records and 33 cluster records. Possible-duplicate merging gives 612 cave groups; these are provisional groups, not a verified count of distinct caves.

A new intersection of the saved outcomes finds **102 catalogue records that fail every one of the 16 separately scored form models**. Exact IDs, source rows and every clause-level contradiction witness are in `cave_form_intersection.json`; The adjacent `evaluate.py` generates the intersection and contradiction witnesses. All 16 models combine two landmark readings (B-PILLAR/B-TERRACE), two aspect attachments (cave/both-mouths), and four separately run coding rules (primary, s_open_ge2, s_singular_unknown, s_pillar_between).

These failures occupy 97 possible-duplicate groups whose every member fails the scored forms. Three further possible-duplicate groups mix failed records with surviving records:

- A41:II/49 with PAT:UMakkuk-5.
- A41:VII/11, VII/13, VII/15, VII/16 with WB:E325.
- A41:VIII/10, VIII/2, VIII/6, VIII/7, VIII/9 with WB:E333.

The mixed groups remain eligible through their best permitted member. None of these links establishes a definitive identity.

The other 541 cave catalogue records have at least one unknown or all-match scored form. `scored_form_survivors.json` preserves their exact IDs. All 33 cluster records remain unknown. Unknown evidence keeps a record eligible; it supplies no support for a match.

**Operational interpretation:** repeat reading or reranking of the same observations can stop for these 102 records for these 16 specified form models. Their existing contradictions already settle that bounded screen. A new source observation, documented coding error, authenticated textual correction or explicitly registered additional model could justify another evaluation. This result excludes neither the physical caves as a whole nor unscored interpretations. B-GATE (Allegro's Temple/gate reading), combined coding sensitivities, stricter phase and geometric sensitivity models lie outside this intersection. The exploratory screen closes on the stated evidence/specification without reopening any earlier closed test.

## Surviving documented matches

**Twin Cave** is the sole all-match record under the pillar/both-mouth models, including all four saved coding rule sets. Bar-Adon 1989 ch. B pp. [15]–17 / Fig. B1, as already extracted in `registration/entry25_twin_cave_features_2026-10-01.json`, reports two east-facing mouths with a thick rock pillar and northern/southern units. Missing mouth positions prevent a cave-level frontage calculation under the frozen two-part hull rule. Architectural dating, ancient threshold datum and target geometry remain unknown. The 1986 excavation's lack of indicative finds cannot test deposit absence because target coverage and detection remain unestablished.

**XII/53** is the sole all-match record under the pillar/cave models, including all four saved coding rule sets. Cohen and Israel, ʿAtiqot 41 pp. 207–210 / Plan 3 p. 209, report an east-facing opening split by built pillar W2. Its northern/southern parts are coded as two openings by inference. W2's date remains unknown; Early Roman finds date a layer adjoining W1, not W2. Both-mouth rock-jamb geometry remains unmeasurable because masonry supplies each inner jamb. The printed locator has a suspected digit error and cannot support a precise geographic target.

**IV/17** supplies a two-opening rock-pillar form and a northern member. Sion, ʿAtiqot 41 pp. 63–64 / Plan 5 p. 63, supports a qualitative eastern-cliff description in the older workbench form query. The regional numeric rule gives unknown cave-level aspect because all ancient rock-cut mouth chords cannot be recovered; the northern mouth interval is inconclusive at the primary sector, and masonry obscures the southern rock jamb. These evaluations use different aspect predicates. Their difference supplies no new archaeological contradiction.

**IV/11** fails exact-two-entrance models on the singular description, while `s_singular_unknown` retains it as unknown. Feig, ʿAtiqot 41 pp. 85–90 / Plan 1 p. 85, supplies an internal pillar and forecourt; the exterior opening pair remains unestablished. Thus IV/11 is absent from the 102-record intersection.

All terrace models have zero all-match catalogue rows and hundreds of unknowns. The screen therefore gives no basis to reject the terrace reading globally.

## Geometry and target checks performed

Recomputed Plan 5 northern chord: nominal 122.929° from the drawn north reference, using existing endpoint picks. A 27-combination declared-parameter grid applies r = 0.05/0.10/0.20 m, north allowance 3°/6°/10°, and scan distortion 0°/1°/3° against the four saved east sectors. The northern interval passes the primary sector in one low-uncertainty combination and remains inconclusive in the other 26. Every stricter eight-wind and sunrise case is inconclusive. The southern rock-cut chord remains unmeasurable in every run, so no result establishes both-mouth orientation. No north correction has been invented; the drawn arrow's convention remains unspecified.

Recomputed XII/53 whole-opening facade chord: nominal 61.374°. In the same grid it passes the primary sector in 24 cases and remains inconclusive in three. The strict eight-wind sector fails in one low-uncertainty case and remains inconclusive in the others. Sunrise cases all remain inconclusive; the broad sector passes throughout. This is a facade sensitivity check; the saved cave-level primary score uses the published compass word. Sensitivities change no frozen class outcome. This bounded geometric grid covers the stated r/n/d alternatives only; it does not claim the full A12 passage-axis, word, precision and phase sensitivity audit.

The inventory evaluator's reviewed quantity checks pass. Replayed form branches give IV/17 one compatible and three unknown, Twin Cave two compatible and two unknown, IV/11 four unknown. All 96 target-prerequisite branches per cave remain unknown. Missing ancient threshold elevation/datum/phase and horizontal origin/path prevent a complete digging target; changing the cubit or jar/book antecedent fills none of those fields.

The existing coverage report documents that Plan 5 has no cut limits, sections or levels. Its eight IV/17 target/footprint joins remain undeterminable. Sion's excavation at chamber centres establishes neither coverage nor noncoverage of a northern-opening target. This audit inspected the existing coverage report and inputs; it obtained no excavation geometry and makes no deposit-absence inference.

## Source and exposure scope

`source_manifest.json` lists exact GitHub paths, blob SHAs and returned URLs for the reports, committed catalogue tables, existing picks and evaluator code used here. Inputs were copied read-only for local verification; the delivered evaluator reads canonical repository paths. The adjacent `evaluate.py` requires no network. Source notes were already exposed, so these results supply no independent unseen prediction. No L-656 field-file arrival, IAA Archive cave-record arrival, protected source-plan image or new archival record was opened. No email, external write, map-marker change or status-ledger increment occurred.

Obtained — a reproducible 102-record intersection of existing reported-form contradictions, with exact witnesses and duplicate audit; particular-site identification remains not identifiable from available evidence.
