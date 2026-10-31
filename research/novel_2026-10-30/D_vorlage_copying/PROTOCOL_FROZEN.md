# Direction D: Vorlage copying-error emendations of the unplaced names (frozen protocol)

Written 30 Oct 2026 by worker D, before any confirmatory scoring. This is an exploratory method test under AGENTS.md. It makes no identification claim and changes no rating, ledger, ACTIVE_TEST or atlas data.

## Claim tested

Suppose the engraver copied 3Q15 from an ink exemplar (a Vorlage) in a Herodian formal or semi-cursive hand. Then some of the unplaced proper names may be miscopies. Their errors would follow how letters look in ink, not how modern editors confuse letters on copper.

**Prediction.** Single-letter emendations weighted by an ink-hand confusion model (V) recover more gazetteer names than:
- (i) the existing chance baselines;
- (ii) emendation sets of the same size drawn from control confusion models: (a) the modern edition-confusion matrix (E), and (b) uniform substitution.

## Novelty gate

- I searched for "Vorlage" and "exemplar" in `main` (7a3b3074), `origin/sandbox/methods` (eb0ef639) and `research/logs/`. There was no hit for a copying model.
- "Exemplar" occurs only in unrelated senses: the W2F letter-model spec, Greek word controls and the Dalman audit.
- Precedents:
  - The edition-confusion matrix, `research/text/edition_confusions/`. It counts how modern editors read copper letters differently.
  - T01, Palmer names with sound rules, chance-level (wave1/T01_place_names).
  - Sandbox run 19, Mandate field names, chance-level.
- What is new here:
  - The confusion model comes from ink-hand evidence that does not use the Copper Scroll.
  - The names are **emended** before matching. T01 and run 19 matched only the edition readings.

## Inputs (SHA-256)

### Built in this folder

| File | SHA-256 | What |
|---|---|---|
| `data/delitzsch1920_pairs.csv` | 3e505352…22a777 | 51 letter pairs from Delitzsch 1920 §§103–131 (tiers A/B/C), read from TOC p. IX and running heads/§ labels of pp. 103–119 |
| `data/qumran_ancient_corrections_pairs.csv` | 417548ff…618d33 | 72 ancient scribal letter corrections (49 pairs) in Qumran ink MSS, 3Q15 excluded |
| `data/shape_similarity_habakkuk.csv` | 2c5a5247…70ebb0 | 231 pair similarities in the traced 1QpHab hand |
| `data/vorlage_confusion_matrix.csv` | b5f40718…1790b9 | **Model V** (231 pairs, column `p`) |
| `data/neighbourhood.csv` | febff3f4…771b85 | All 3,413 one-substitution emendations, with V and E weights and ranks |
| `data/emendations_frozen.csv` | 4b7d1a35…fa8807 | **Frozen sets**: V top-10 and E top-10 per name (240 + 240 rows; 132 strings shared) |
| `data/gaz_S2.csv` | 95130ced…255f8d | Mandate window names; reproduces run 19 S2 byte for byte |
| `inputs/gaz_S4.csv` | 5378499b…a09f17 | Mandate sheets 18-12, 18-13, 19-14 read directly (run 19 A1, 478 names), copied from sb |
| `data/gaz_ASI.csv` | 03ce0d1d…fd3518 | 639 romanised ASI site names in the run 19 region box |
| `data/gazetteer_manifest.json` | a8dcfcf3…8f6cdc | Counts, raw hashes, exclusions |
| `scripts/askel.py` | b290f8d9…ec2cff | Run 19 skeleton code, copied verbatim from sb |
| `scripts/build_shape.py` | 71e5a47c…fc8bd5 | |
| `scripts/build_qumran_corrections.py` | b1386404…44f13d | |
| `scripts/build_model.py` | 75b20a1b…05b486 | |
| `scripts/build_gazetteers.py` | 6e1a47e3…7ed715 | |
| `scripts/emend.py` | fcbe6b3a…b0fee7 | |
| `scripts/check_copper.py` | 552847b4…6ae61b | |
| `scripts/run_test.py` | 1cbdc21a…b7b734 | The confirmatory runner |

### Existing repository files, used unchanged

| File | SHA-256 |
|---|---|
| T01 `data/scroll_names.json` | bfaef216…6fcf6c |
| T01 `data/palmer_names.csv` | acba0e5b…3b9e75 |
| T01 `data/chance_random_by_pattern.json` | 86c9f2e7…296781 |
| T01 `data/positive_controls.json` | 35b12604…d2f83b |
| T01 `scripts/toponym.py` | dea86acb…399d77 |
| T01 `scripts/chance.py` | 2b4fde8f…0827b1 |
| `research/text/edition_confusions/confusions.csv` (model E) | 765ebdca…d5e5ce |
| `research/text/edition_confusions/variants.csv` | 07be73c9…af8271 |
| `research/regional/mandate_maps/names.csv` | 0ebb11fa…508479 |
| `research/regional/asi_jerusalem/sites.csv` | b9eb0df7…6d1e22 |

### External sources, not committed

| Source | Location | SHA-256 | Licence and use |
|---|---|---|---|
| Delitzsch, *Die Lese- und Schreibfehler im Alten Testament* (Berlin–Leipzig: de Gruyter 1920) | https://archive.org/details/dieleseundschrei00deli, PDF `dieleseundschrei00deli.pdf` | see appendix | Public domain (author died 1922). Pages read: TOC p. IX (PDF p. 13); text pp. 103–119 (PDF pp. 117–133) |
| ETCBC `dss` Text-Fabric 2.0.1 | https://github.com/ETCBC/dss, commit dd296361 | — | CC BY-NC 4.0. Features `rem`/`cor` |
| Culmus Ancient Semitic Fonts 0.06-1, font `Hebrew-Square-Habakkuk.ttf` | https://sourceforge.net/projects/culmus/files/ancient_fonts/AncientSemiticFonts-0.06-1/AncientSemiticFonts-0.06-1.TTF.tgz/download | see appendix | Yoram Gnat, GPL-2. The README says the font follows the Habakkuk Commentary, Qumran, about 0 CE |

### Not used

- **Leon Levy DSS Digital Library images.** The site answers (HTTP 200), but no image was downloaded. Its terms forbid reuse without permission, and the scope is one bounded pass.
- **`https://commons.wikimedia.org/wiki/Category:Pesher_Habakkuk`** returned HTTP 404.
- **Tov, *Textual Criticism of the Hebrew Bible*.** No open copy was sought, because it is in copyright. Delitzsch 1920 is the documented public-domain graphic-confusion list used instead.

## Model V (frozen in `scripts/build_model.py`)

Each unordered pair of the 22 base letters gets a rate; final forms count as base letters.

**rate = 0.01 + D + Q + S**, where:

- **D: Delitzsch tier.**
  - Tier A = 3: §§103–108, "infolge äußerer Ähnlichkeit": ו–י, ד–ר, ה–ת, ה–ח, ב–כ, ע–צ.
  - Tier B = 2: §§109–115.
  - Tier C = 1: §§116–131, including the "sporadische Verschreibungen".
- **Q: ancient Qumran corrections.** Q = min(n, 3), where n counts events in which an ancient scribe removed letter x and wrote y in its place:
  - inside one word, a run of signs with `rem=2` sits next to a run of the same length with `cor` = 2 or 3;
  - the letters are paired by position;
  - all scrolls count except 3Q15.
- **S: shape similarity in the Habakkuk font.** S = 3 · max(0, (sim − median) / (max − median)), where sim is the best-shift cosine similarity of Gaussian-blurred (σ = 3 px) renderings at 96 px.
- **p(pair) = rate / Σ rate.**

The rule was fixed before any gazetteer was read for the emended strings. The six highest pairs are ו–י, ה–ח, ד–ר, ה–ת, ו–ז and ו–נ (`vorlage_confusion_matrix.csv`).

**Independence from model E.** No input comes from `research/text/edition_confusions/`. E is used only as a control.

## Control model E

- E is `confusions.csv`, column `rate` = (places + 1) / 409.
- Pairs that are not listed get the floor 1/409, from the README's formula.

## Names (rule)

- Source: T01 `scroll_names.json`, 40 names with their edition variant cores.
- A name counts as **unplaced** if `priority != 0` and its id is not jericho, achor or sekakah. This is run 19's `match.py` rule, which gives 24 names.
- The 24 names: kohlit, melah, manos, mdh, mattiyah, nebat, kippa, solomon, qi, hasor, shaveh, shalef, din, tekelet, qomah, nebo, tamar, pele, nab, zered, absalom, zadok, obed and horebbeh.
- All variant cores of each name are used.

## Emendation generator (frozen in `scripts/emend.py`)

- **Neighbourhood.** Every string made from one variant core by replacing one letter x with a different letter y.
  - Excluded: swaps between two of א ה ו י. Both matchers treat these as vowels, so the swap makes no new consonantal name.
  - Excluded: strings equal to another variant core of the same name.
  - Result: 3,413 strings.
- **Weight.** w_M(string) = p_M({x, y}). If a string can be reached in more than one way, its best weight is kept.
- **Frozen sets.**
  - V-set: the top K = 10 strings per name by w_V, 240 strings.
  - E-set: the top 10 by w_E, 240 strings.
  - Ties are broken by (variant order, position, letter order).
- Two-substitution emendations are **not** used. They are left out to keep the sets small and the chance rate bounded.

## Gazetteers and matching (existing rules, reused exactly)

The statistics count **one match unit per (string, gazetteer family)**. There are three families.

1. **Palmer** (SWP name lists, T01).
   - Pool: the T01 chance pool, which is tesseract records on priority sheets XIV, XV, XVII, XVIII, XXI and XXII (2,647 records). The scorer is `toponym.score` and the threshold is 0.75.
   - Statistic: hits = the number of records scoring ≥ 0.75.
   - Baseline: T01's random distribution for the string's consonant pattern, from `chance_random_by_pattern.json`.
     - The file has 100 random cores per pattern.
     - Patterns missing from it get 200 new random cores. These are drawn with T01's own `rand_job` and pool frequencies, with seeds 7,000,000 + 1000·j + t.
   - p = (1 + #random ≥ obs) / (n + 1).
   - **The string matches Palmer if p ≤ 0.05.**
   - Chance probability c_Palmer = the share of random cores of that pattern that would themselves reach p ≤ 0.05.
   - The whole 9,368-record list is not scored. The T01 chance baseline exists only for the priority-sheet pool, and that pool is reused unchanged.
2. **Mandate** (S2 ∪ S4, 707 rows): run 19's matcher.
   - Hebrew and Arabic consonant skeletons from `askel.py`, without the D1 or D2 deviations; generic heads are excluded.
   - **Match** = an identical skeleton, or edit distance 1 when both skeletons have 4 or more consonants.
   - Chance probability c = C1 = the share of 100 consonant shuffles of the string that match (seed 20261030, in sorted string order).
3. **ASI** (639 rows): the same matcher and the same C1.

## Statistics, tests and failure condition

- **M_V** = Σ over the V-set strings and the 3 families of match(string, family). **M_E** is the same for the E-set.
- **Test (i), chance baseline.**
  - The Poisson-binomial upper tail P(X ≥ M_V), where X is a sum of independent Bernoulli(c) over the same 720 string-family units. This is run 19's `pb_tail`.
  - Passes if p ≤ 0.05 and M_V > Σc.
- **Test (ii-a), edition-confusion control.**
  - D = matches of the V-only strings − matches of the E-only strings.
  - Permutation test: shuffle the union of V-only and E-only strings within each name (10,000 permutations, seed 20261031).
  - One-sided p = (1 + #(D_perm ≥ D_obs)) / 10,001.
  - Passes if p ≤ 0.05.
- **Test (ii-b), uniform control.**
  - Draw 10 strings per name uniformly from that name's neighbourhood, 10,000 times (seed 20261032).
  - p = (1 + #(M_U ≥ M_V)) / 10,001.
  - Passes if p ≤ 0.05.
- **Verdict.**
  - **Obtained:** (i), (ii-a) and (ii-b) all pass.
  - **Partly:** (i) passes together with one of (ii-a) or (ii-b).
  - **Not obtained:** otherwise.
- **Failure condition.** The Vorlage-weighted emendations do not give more gazetteer matches than the chance baseline (i) and than equal-size control sets (ii-a and ii-b).

## Exploratory candidates (reported, not identifications)

A V-set string is listed as a candidate hypothesis if either:
- it has a Mandate or ASI match with C1 ≤ 0.10, which is run 19's lead bar; or
- it has a Palmer match (p ≤ 0.05) and its best record scores ≥ 0.9.

Candidates are reported whatever the verdict. Without a passing test, they are chance-compatible hypotheses only. None counts as an identification.

## Copper Scroll correction check (descriptive, not training)

- `scripts/check_copper.py` takes Puech 2015's "engraved X, corrected Y" letters, written X(Y), from `variants.csv`.
- It compares mean log₂ p_V against p_E and against uniform 1/231, with a one-sided sign test.
- **Exposure.** While exploring, before the model weights were fixed, I printed the list of Puech X(Y) cases (38 strings; the dominant pairs were ן(ר), ו(ר) and ר(ו)). So this check is **not** a clean holdout. The model rule (Delitzsch tiers, min(n,3), the shape scale) was not changed after that.
- Engraver supralinear letters (ETCBC `cor=3`, 4 signs) are insertions, not substitutions. They are not scored.

## Exposure log before the freeze

- **T01 REPORT and run 19 RESULT read in full.** They show matches for the **original** readings. No emended string had been matched against any gazetteer.
- **Smoke test** (`run_test.py --smoke`) on 66 neighbours of two **placed** names, jericho and doq. It checked the code only and used none of the 24 unplaced names. Its output stays outside the repo (`/root/novel/work_D/smoke/`).
- **Edition-confusion README** main result (top pairs) was read.
- **Puech X(Y) list** printed, as above.
- **No images** of the scroll were opened. No reserved material was opened.

## What counts

- **Obtained:** the verdict is obtained. The method then becomes a usable prior for reading names, but each candidate still needs an independent geographic test.
- **Partly** or **not obtained:** as defined above.

## Appendix: full SHA-256 of every input

```
3e505352ddaf7f5f776fd5942d82bf284ec7fa20b0903bae78fbf017d722a777  data/delitzsch1920_pairs.csv
417548ff7fa6160c714c3e4ce2d56e37c1b70dcfae99e554f7532e9bd0618d33  data/qumran_ancient_corrections_pairs.csv
2c5a5247fb7214bf4e357801dce118d15b0075ccfaedf47a7bc6b4bef870ebb0  data/shape_similarity_habakkuk.csv
b5f40718eca02a8bf7aa8ca7c472272f7c7e646a97602b8af92f325aee1790b9  data/vorlage_confusion_matrix.csv
febff3f42477da95f29e977e6d6c2cdc61dceee17d25a7f950318958ea771b85  data/neighbourhood.csv
4b7d1a352916afc16300f2679f90f898d66c999bcba7c2f42db94c2278fa8807  data/emendations_frozen.csv
95130ceda475ca2223052747f66a18eafd2cc87189223035e13b8ab050255f8d  data/gaz_S2.csv
5378499b9242e8a0213cdd2ff0b2d02823ae4c5cee54107525d4c3b962a09f17  inputs/gaz_S4.csv
03ce0d1dad46dc2fc1611b1d2ada105dbfe662aecdb5d689defc8f3c80fd3518  data/gaz_ASI.csv
a8dcfcf3c6367e538b835a07460048acd453dff97d69b1c830850666568f6cdc  data/gazetteer_manifest.json
b290f8d9701b0ca0a96970205707cc4c8d83ec70de271e1c69fe7a6e55ec2cff  scripts/askel.py
71e5a47c3c4414eb52710a7021bb9ca69acc6793b7c7f337454fde1376fc8bd5  scripts/build_shape.py
b1386404d9d3ed840df51567c24494ee2d8c1b9ac3c1384191db7c03d544f13d  scripts/build_qumran_corrections.py
75b20a1b962dfadd73cbd221e25737f79f6e4a7002fcf402f0f2d00cda05b486  scripts/build_model.py
6e1a47e37322ed821e54a2bf6eaf38af071fb311148c8869f60d11e2117ed715  scripts/build_gazetteers.py
fcbe6b3a8f4d3f03efc4f7f5f2384bb3b65e6b0175a4bab05a980d224bb0fee7  scripts/emend.py
552847b455f0936a66e57b98d643750fcd196df1ed688b466dd9c54f5a6ae61b  scripts/check_copper.py
1cbdc21a4a33d813dd5670d9b2300fbea6a9b58b7c3837df1042dccc48b7b734  scripts/run_test.py
bfaef21601de684ce7ae5443f600a961e72949f23029b8c3d01f7905146fcf6c  research/agent_review_2026-10-07/wave1/T01_place_names/data/scroll_names.json
acba0e5b9138d6fa9095a5177b13eb5a9051e38f168a47fd9b3d6ab8473b9e75  research/agent_review_2026-10-07/wave1/T01_place_names/data/palmer_names.csv
86c9f2e725d0f1faf7d68fd2e2ee2683ed387cc699e26109d9f6d289f0296781  research/agent_review_2026-10-07/wave1/T01_place_names/data/chance_random_by_pattern.json
35b126047d78e83114ac123c6821c11d0cf0497b8d974ec0f7e1a265cfd2f83b  research/agent_review_2026-10-07/wave1/T01_place_names/data/positive_controls.json
dea86acb74a54f3a49fa96066a1044087d295f928b57c30a2ad89a7910399d77  research/agent_review_2026-10-07/wave1/T01_place_names/scripts/toponym.py
2b4fde8f6b90b6892fb8bb19125013ac559ab622942eb70f4a3fdbdb320827b1  research/agent_review_2026-10-07/wave1/T01_place_names/scripts/chance.py
765ebdca01c9f4a710223c0d1498b07569f62647537b8861e7d9b9c2fdd5e5ce  research/text/edition_confusions/confusions.csv
07be73c9c02a04f5d5214143e98205608b8325b8968da4431d43be3f7baf8271  research/text/edition_confusions/variants.csv
0ebb11fa5a452708196104d0de02f6994220870a97535781df7463c0f3508479  research/regional/mandate_maps/names.csv
b9eb0df70d7dcdfe0cea68fc76950357057c7ba31e3808354ed9959c376d1e22  research/regional/asi_jerusalem/sites.csv
654fc5c0e3541455b4a29bcd381acddf2e1f7c9f0db4b296e810180d09349c7e  Delitzsch 1920 PDF dieleseundschrei00deli.pdf (not committed)
90c58958ca6c536b81cafd12feb7466a5fa8118a0bf388a7c520b4534c44f8eb  AncientSemiticFonts-0.06-1.TTF.tgz (not committed)
564af99aea05f993cf2a72bf90182886a8ae455a349d719ca0ba8cf79e87b12c  Hebrew-Square-Habakkuk.ttf (not committed)
```
