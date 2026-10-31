# B3: the round-1 analysis-by-synthesis model, unchanged, on new lines, with the exact null and two bias controls — frozen protocol

Frozen 31 October 2026 by Claude (worker B3, branch `claude/novel-2026-10-31-B3`), before any new line was scored. This is a **new frozen test specification of an unchanged model**. The 30 October round-1 result (`research/novel_2026-10-30/B_analysis_by_synthesis/`, final commit bd06dcc6, protocol SHA-256 `2ec4b4da…c319`) stays as registered: 4 of 13, p = 0.21 under its 1/K null, targets not scored. Nothing in `research/novel_2026-10-30/` is edited.

## 0. Novelty gate

- Round 1 judged its held-out count against a chance rate of 1/K. For sets made of the true line plus one-letter variants, the chance that the centre string ranks first is the product over varied positions of 1/(a+1) (B2, 31 October). This is a **documented analytical error** in round 1 (AGENTS.md reopening condition).
- Under the exact null, round 1's 4 of 13 has P = 0.0045. That rests on an untested assumption: no systematic preference for the true string that does not come from the image.
- New here: the same frozen model is scored on **76 lines it has never scored**, with the exact null and with **two bias controls registered before scoring**: a mirrored decoy set (centre bias) and a wrong-column scoring (any image-independent preference for the true string).

## 1. Claim tested

**Claim.** On lines it has never scored, the frozen round-1 model ranks the edition-agreed reading of a line above one-letter confusion variants more often than the exact null allows, and this excess comes from the image at that line, not from a preference for the centre string of a set or for the true string as such.

This tests a **reading method**. It is not an identification. It changes no rating, outcome-ledger entry, ACTIVE_TEST, OPEN_QUESTIONS or atlas record.

## 2. Model: round 1, unchanged

**Files copied verbatim** from commit bd06dcc6 (`research/novel_2026-10-30/B_analysis_by_synthesis/`), extracted with `git archive bd06dcc6`. `model_files_sha256.csv` lists, for each file, the SHA-256 of the copy here and of the file at bd06dcc6; all 11 are identical, and the 9 that round 1's protocol states match it.

| File | SHA-256 |
|---|---|
| model.py | `191855431575fcfe91a023c57b34527de707ef7355d7cb0b755c755c0b6ed39a` |
| abs_score.py | `6d0f1362145299bbbcc49f51d4cbd45158f9a105d63a33fa17c70963b3295c61` |
| frozen_params.json | `df825c762bb3784b71051744a6cc5f74bc1ab680403fcc8c7d4a06f030d23f39` |
| glyphs.json | `9a320070084363b3c7223ae30b29d86a2f690ca13defc19b9886f8879df4fefa` |
| glyphs.py, candidates.py, confirm.py, prep.py, targets.py, etcbc_lines.json, calibration_items.json | see `model_files_sha256.csv` |

Frozen parameters (round 1): prof = U, hw = 0.07, rho = 0.60, hp = 2.5, gap = 0.22, space = 0.45, band = 0.62, WIN = 1.5, LOC = 0.15. P = `dict(model.DEFAULT)` updated with `frozen_params.json`, as round-1 `confirm.py`. Scoring = round-1 `abs_score.score_line` (registration shared by the candidates of one set; nominal row ±1.5 pitch; both 180° orientations; line score = sum over the column's cuts; COL_CUTS and NLINES as round 1).

**Path adaptations, run time only; no file is edited** (`b3_score.py`, `b3_prep.py`):
1. `prep.PRIV` and `model.PRIV`: `/root/novel/private_outputs/B/stacks` → `SP/products/B3/stacks`.
2. `abs_score.REND`: `/root/novel/private_outputs/B/renderings` → `SP/products/B3/renderings`. The `os.makedirs` that abs_score runs at import is suppressed during the import, so nothing is created under `/root`.
3. prep.py's registration numbers are written by the wrapper to `prep_registration_b3.json`, not into round 1's file.
(SP = the session scratchpad. Stacks and renderings never enter the repository.)

**Images.** The USC Digital Library public previews of the 1988 West Semitic Research Project (WSRP) photographs already in the repository (`images/previews/cuts-01-10/`, `images/previews/original-scroll-remaining/`, index `research/sources/usc_copper_scroll_images/index.csv`). Not the bucket TIFFs.

**Reproduction checks (done before the freeze).**
- Stacks rebuilt with round-1 prep.py for cuts 2–23 (OpenCV 5.0.0, NumPy 2.5.3, SciPy 1.18.1). For every cut the reference frame, frames used, per-frame SIFT inliers, input-frame SHA-256, strip angle and crop size are identical to round 1's `prep_registration.json` (`prep_registration_b3.json`). The npz file hashes cannot match (zip time stamps); array-content hashes are in `stack_content_b3.sha256`.
- Round 1's 13 held-out candidate sets were re-scored: all 73 log-likelihoods and all strip registrations equal round 1's `calibration_rankings.csv` to the printed 3 decimals (`verify_round1_reproduction.csv`). These lines are exposed; this is a reproduction check only.

## 3. New lines (`b3_items.py` → `items_b3.json`, SHA-256 `c218373d01bb415cf816985a4bd31b49676efe956f1ca22d25be9d1b98317d49`)

Round 1's line-level rule used all its 25 eligible lines. New lines use a word-level rule, after B2 (`items2.py` on `origin/claude/novel-2026-10-31-B2`), inside round 1's scope.

**Undisputed word:** ETCBC word (Eep Talstra Centre for Bible and Computer, dss 2.0.1) with no flag, not Greek, at least 2 letters, and no row of `research/text/edition_confusions/variants.csv` on it. A word span ("1-2") marks every word of the span; a row without a word index marks every word of its line.

**Eligible line**, all of:
- column I–X; not a target line (I 12, VII 11, IX 10, X 15);
- not one of round 1's 25 calibration lines;
- not VII 7–11: round 1's glyph templates were traced from these lines on strip 13 (a stricter rule than B2's);
- not named in the first cell of a table row of `research/text/plate_check.md` (every "COL n" and "COL n–m" reference; round 1 and B2 read only the first reference);
- no Greek word; at least 6 letters; at least 3 letters in undisputed words.

Cuts: round-1 COL_CUTS (I: 2, 3, 4; II: 5, 6; III: 7, 8; IV: 9, 10; V: 10, 11; VI: 11, 12; VII: 13, 14; VIII: 15; IX: 16, 17; X: 17, 18). All have registered preview stacks. Cut 1 has no lit frame, so column I is scored on cuts 2–4, as in round 1.

**Result: 76 lines**, all held out (the model is frozen; nothing is trained). By column: I 10, II 10, III 4, IV 9, V 3, VI 8, VII 5, VIII 9, IX 10, X 8. Excluded: round-1 lines 25, plate check 33, too few letters 7, targets 4, template source 3, Greek 3. The list is in `items_b3.json`.

**Why these lines are unseen for this model.**
- The round-1 model never scored them: round 1 scored only its 25 lines (12 train, 13 held-out) and, in an abandoned design, rendered only the ETCBC text of columns III and VI on feasibility maps without any substituted candidate (round-1 protocol §7). Its parameters were tuned on the 12 train lines only.
- B2 scored many of the same lines, but with B2's own model (learned templates, full-resolution bucket TIFFs, its own registration and seed 31102026). That gives no ranking of these candidate sets by this model, and the B3 sets differ (round-1 seed). B3 did not open B2's ranking files.
- Other workers looked at cuts 7–8 (column III), 3, 5, 6, 10 and the XII 10 cuts by eye. A frozen automatic scorer cannot learn from that. B3 viewed no image (§9).
- Template leakage: the 17 traced templates come from VII 7–11, which are excluded.

## 4. Candidate sets

**Truth set** (`b3_items.truth_set`): round-1 `candidates.candidates()` with **one change** needed by the word rule. The enumerated (position, partner) options are restricted to letter positions inside undisputed words. Everything else is round 1's: K = 6 (truth + 5 variants), pairs = rows of `confusions.csv` with count_places ≥ 3, weights = pair rate, draws without replacement with `numpy.random.default_rng(20261030 + 100·col + line)`, final forms by round-1 `subst()`, line text = round 1's `' '.join` of the ETCBC words. 71 sets have 6 candidates, 4 have 5, 1 has 3.

**Decoy set** (centre-bias control, `b3_items.decoy_set`). Seeded rule: j* = `default_rng(20261031 + 100·col + line).integers(m)` over the m variants; the decoy D is variant j*, which differs from the truth T at one position p0. Decoy set = [D, T] + [D with variant j's substitution applied, for every j ≠ j*]. So every member is a one-letter confusion-pair substitution of D drawn by the same generator, the set always contains the real reading, and it has exactly the truth set's number of variants per position.

Why mirrored rather than re-running the generator on D (the orchestrator's first suggestion; refinement allowed before the freeze):
- A re-drawn set often leaves p0 unvaried. D is then right at every varied position, so a model with real signal puts D first about as often as T. The decoy-first count would then rise with signal, not only with bias.
- In the mirrored set the swap a↔b at p0 maps the truth set exactly onto the decoy set. Under "no image information at p0", truth-first and decoy-first have the same distribution **whatever the centre bias**. This makes an exact sign test possible.

**Wrong-column scoring** (control for any image-independent preference for the true string; `b3_items.wrong_col`). The truth set of line (c, l) is scored again, unchanged, by round-1 `abs_score.score_line(c′, l*, …)` with c′ = c + 5 for c ≤ 5 and c − 5 for c ≥ 6, and l* = min(l, NLINES[c′]). The pairs I–VI, II–VII, III–VIII, IV–IX and V–X share no cut, so the scored strips hold no part of line (c, l) in either orientation. Same model, same registration rule, another column's text.

Why this control is added: the mirrored decoy cannot separate image signal from an image-independent preference for the true letter at p0 (for example a template prior that favours one letter of a confusion pair; the truth is more often the frequent member: ו 249 / י 196, ב 234 / כ 180, ה 176 / ח 129 in the ETCBC text). The wrong-column scoring keeps every such preference and removes the image of the line.

Why a different column, not a different line of the same column (the first design, used only in exploration, §9): the round-1 registration searches both 180° orientations, so a window at line l ± 5 can fall on line l itself in the flipped strip. On round-1 line IV 5 (cut 9) it did, at exactly the same row.

## 5. Exact null

- For one set: P(centre strictly first) = ∏ over varied positions 1/(a+1), a = number of variants at that position (from the strings). Assumptions: a variant's score differs from the centre's only through its varied letter (local additivity), the letters at a position are exchangeable, and positions are independent. The truth set and its mirrored decoy set have the same p_i. Sum over the 76 lines: **E0 = 3.923**.
- T (truth-first count), D (decoy-first count), W (wrong-column truth-first count): each ~ Poisson-binomial(p_1 … p_76) under the exact null.
- **Ties.** The centre counts as first only if its score is strictly greater than every other score in its set (as round 1). The null assumes continuous scores. An exact tie (for example a substituted letter that falls off every strip) can only lower T, D and W, so C1 is conservative. A tied set counts as 0 for its centre; the sign tests use only discordant lines. The number of exact ties at the top is reported for each kind of set.

## 6. Decision rule and failure condition (`b3_stats.py`, SHA-256 `19a5c990b8b63483552a24f3ba129f2cd2e7cadb18a6fd32245a03c64fe98254`)

Per line: t_i, d_i, w_i ∈ {0, 1} as above.

- **C1 (beyond the exact null):** P(T ≥ T_obs) < 0.05. With these 76 lines: **T ≥ 8** (P(T ≥ 8) = 0.041; P(T ≥ 7) = 0.095).
- **C2 (decoy, centre bias):** n10 = #(t = 1, d = 0), n01 = #(t = 0, d = 1); n10 > n01 and the exact one-sided sign test P(Bin(n10 + n01, ½) ≥ n10) < 0.05. Smallest passing splits: 5–0, 7–1, 9–2, 10–3.
- **C3 (wrong column, any image-independent preference):** the same sign test of t against w: m10 = #(t = 1, w = 0) > m01 = #(t = 0, w = 1) and P(Bin(m10 + m01, ½) ≥ m10) < 0.05.
- **PASS iff C1 and C2 and C3.**
- **Failure condition:** any of C1–C3 fails. The targets are then not scored and `target_rankings_b3.csv` records "NOT RUN".
- Diagnostics, reported but not part of PASS (`b3_stats.diagnostics`): P(D ≥ D_obs) and P(W ≥ W_obs) under the exact null; counts of exact ties at the top; per-column counts; the same statistics without column I (cut 1 missing) and without column VII (template column); the share of variants scoring below the truth, by template class of the substituted pair (font-fallback letter in the truth, in the variant, or neither), at the line and at the wrong column.

**Why C2 is a sign test, not "decoy-first not above its null".** The orchestrator suggested: pass only if P_T < 0.05, decoy-first not significantly above its exact null, and truth-first > decoy-first. A design check on these 76 set structures (`b3_power.py` → `power_sim.json`; toy additive model, no image used; 1000 replicates per row) showed that rule's weaknesses:
- With a pure letter preference and no signal (λ = 0.5), it passes 27–67 % of the time; with a pure centre bias (β = 0.5), 11–17 %.
- With real signal (s = 1) plus a centre bias (β = 0.5) it fails 63–99 % of the time, because the decoy is right at all its other varied positions and so comes first above its null whenever the model reads.
- The frozen rule (C1 ∧ C2 ∧ C3) passed at most 2.9 % in every no-signal scenario (β, λ ∈ {0, 0.5}, 0 or 15 % invisible positions). With signal s = 1 (pairwise win rate 0.76) it passed 58–89 %, with s = 0.5 only 6–21 %. A weak true signal can therefore fail this test.

## 7. Outcomes

- **Obtained:** PASS; the targets are scored once (§8).
- **Partly:** C1 passes but C2 or C3 fails. The exact-null excess is seen again on unseen lines, but it is not shown to come from the image. Targets not scored.
- **Not obtained:** C1 fails (no excess over the exact null on unseen lines), or the run cannot execute. Targets not scored.

AGENTS.md line for the claim of §1: PASS → **supported relative to the registered alternatives** (exact chance, centre bias, image-independent preference). C1 fails → **rejected** for this model and specification on the previews. C1 passes, C2 or C3 fails → **not identifiable from available evidence**.

## 8. Targets, only after a PASS

Scored once with round-1 `targets.py` and `confirm.stage2` (verbatim; order IX 10, I 12, VII 11, X 15, XII 10 last; VII 11 is included because its cuts 13–14 have preview stacks) by `b3_targets.py`. Candidate strings as round 1: XII 10 R1 שכנה, R2 שבנה, R3 שבצח, R4 שבינח, R5 שכינה, R6 שכונה, R7 שבצהב; IX 10 Puech / Wolters / Allegro–Lefkovits; I 12 ניקרת / מקרת / נקרת; VII 11 המשמרה / המשטח; X 15 ETCBC–Milik / Puech.

Round-1 lean rule: a target **leans** to its top candidate only if its margin to the runner-up is at least the median absolute truth-minus-best-other margin of the 76 new truth sets; otherwise it is **undecided by this model**. Outputs are reported as model outputs with margins, not as readings. They come from exposed images and are exploratory reading evidence under the XII 10 protocol, which needs two human readers.

## 9. Exploratory phase and exposure log (all before this freeze)

**Images viewed by eye: none.** B3 opened no image, crop, stack or rendering for viewing. Every image access was by code: round-1 prep.py registration and round-1 model scoring.

**Read.** Round-1 protocol, note and code; B2's `items2.py` (code only); the 31 October summary README; the edition files the rules use (`variants.csv`, `confusions.csv`, first cells of `plate_check.md`, `etcbc_lines.json`). **Not opened:** B2's `calibration_rankings2.csv` and `heldout_result2.json`; any SULTAN-1, sealed, PROTECTED or "SCREEN FIRST" material; the bucket.

**Declared exposure of others (brief, wave 2).** Cuts 7–8 (column III; 4 new lines) were viewed by eye by A2, B2 and C2 and measured at band level by C2. Cuts 3 and 6 (A2) and cut 5 (C2) were viewed (columns I and II; 20 new lines). The XII 10 cuts are exposed. IX 10 on CT17 was read on 30 October (a target, not a calibration line). The orchestrator viewed a reduced CT10 window (bucket image; columns IV–V). None of these looks scored a B3 candidate set with this model, and the model has no free parameter left to learn from them.

**Computed before this freeze (exposed round-1 lines or text only).**
1. Stack rebuild and full reproduction of round 1's held-out log-likelihoods (§2).
2. Exact null from round 1's `calibration_rankings.csv`: 4 of 13, E0 = 0.781, P = 0.0045, as the orchestrator found.
3. Exploratory controls on round 1's 25 lines (12 train, 13 held-out), with their round-1 candidate sets and the §4 decoy rule (`items_r1_decoy.json`, `explore_r1_rankings.csv`, `explore_r1_wrongline_rankings.csv`, `explore_r1_wrongcol_rankings.csv`, `explore_r1_summary.json`):

| Round-1 lines | E0 | T (truth first) | D (decoy first) | W, same column l ± 5 (superseded) | W, wrong column | Decoy sign test n10–n01 (P) | Wrong-column sign test m10–m01 (P) |
|---|---|---|---|---|---|---|---|
| Held-out, 13 | 0.78 | 4 (P = 0.0045) | 2 | 4 | 3 (P = 0.034) | 3–1 (0.31) | 1–0 (0.50) |
| Train, 12 (tuned on) | 1.32 | 7 | 3 | 5 | 4 | 4–0 (0.063) | 3–0 (0.13) |
| All 25 | 2.10 | 11 | 5 | 9 | 7 (P = 0.002) | 7–1 (0.035) | 4–0 (0.063) |

Exploratory reading (exposed, partly tuned-on lines; not confirmatory):
- 3 of round 1's 4 held-out hits (VII 13, VIII 16, X 2) also rank first when the same set is scored on a column that does not contain the line.
- Variants that swap two traced letters scored below the truth in 51 of 77 pairs (0.66) at the line and in 50 of 77 (0.65) at the wrong column. When the truth letter has a font-fallback template, the traced-letter variant scored below it in 16 of 16 pairs at the line and 14 of 16 at the wrong column.
- So in exploration the round-1 excess over the exact null looks like an image-independent preference for the true string, not image signal. The decoy control alone would not have shown this (all 25: 7–1, P = 0.035).
- The round-1 registration can put different lines on the same row: X 2 and X 4 were both registered at cut 17, orientation 1, row 124.

**Choices made during exploration (logged).**
- The mirrored decoy design was chosen by reasoning and the toy check (§6) before any decoy score was seen.
- C2 as a sign test, and the third control with its sign test (C3), were fixed after the truth and decoy ranks of the first 11 exploratory lines (I 8 to VI 9) had been printed, and before any control output. The reason was the letter-preference loophole of the decoy (§4) and the toy check, not those ranks.
- The same-column wrong-line control was replaced by the wrong-column control after the exploratory registration log showed the flipped window on line IV 5 (cut 9, same row) and near VII 7 (cut 14, 2 px). The change removes the image of the line from the control, so it cannot make the control easier for a model that only has a bias.
- The decision rule (C1–C3, α = 0.05) was not changed after any control result. The template-class rates were added to the diagnostics after exploration; diagnostics are not part of PASS.
- No truth, decoy or control set of the 76 new lines has been scored.

## 10. Procedure

One confirmatory run after the freeze commit is pushed: `b3_run.py confirm_shard k 3` for k = 0, 1, 2 (each set scored once; numbers only, to SP/products/B3/runs), then `b3_run.py confirm_merge 3` → `confirm_rankings.csv`, `confirm_result.json`, `target_rankings_b3.csv`. Outputs are committed in a later commit. This file does not change after the freeze commit.

## 11. B3 files frozen with this protocol (SHA-256)

| File | Role | SHA-256 |
|---|---|---|
| b3_items.py | new lines, truth sets, mirrored decoy sets, wrong-column assignment | `8fb3a063ce3a6480ab7102050185278234a366de63086a1a0124a852e098e8d2` |
| items_b3.json | the 76 lines and their three sets | `c218373d01bb415cf816985a4bd31b49676efe956f1ca22d25be9d1b98317d49` |
| b3_score.py | run-time path adaptation of the round-1 model | `aa18ca5a816728bd756501cbe82ff23afc2d1822202fce2405ca7319524f7d6a` |
| b3_run.py | scoring runs, merge, call of the targets only on PASS | `da9252e924aca4254baf9d2aa51b1cfe353c3b7aa4a6244f7a883daf4ed123cd` |
| b3_stats.py | exact null, sign tests, decision rule, diagnostics | `19a5c990b8b63483552a24f3ba129f2cd2e7cadb18a6fd32245a03c64fe98254` |
| b3_targets.py | round-1 targets and lean rule | `5c85f84f2035af5c330f7b156789602d13602266bde6b1367786a22cb3646295` |
| b3_prep.py | stack rebuild with round-1 prep.py | `132817590ee6e6f3773162a208413d3087032f238aaa63ea0e128e237c569b85` |
| b3_power.py → power_sim.json | design check (toy model) | `0461218b1958eff7dafc6b3d91b735f9fde101a496a0440f584a8c28fe78a400` → `41d90efceedbcabfed40a2511954298813a9892002f1d252c2290cc19a0167b5` |
| model_files_sha256.csv | verbatim-copy check | `b93ae40fcc775894ce17bfdaedba7f74763b7882c90dc8752ee83d2ffcb73ef7` |
| prep_registration_b3.json | registration identical to round 1 | `98858a36feb116aa6fc5327332d591c282b4d3663f19739768248d1b2e791e86` |
| verify_round1_reproduction.csv | 73 of 73 round-1 log-likelihoods reproduced | `3f17d25a8ea5a3a66b1d570f631e3cf56872fcb0591c99417635e05bb20b1aa9` |
