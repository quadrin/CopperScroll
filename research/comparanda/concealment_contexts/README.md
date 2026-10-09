# Concealment contexts

What it is: a base-rate comparison of the Copper Scroll's hiding places with 158 recorded concealments (68 with a known context) from the southern Levant, 150 BCE to 135 CE.
Main result: the mixes differ (DIFFERENT; D = 0.67, permutation p = 0.00005). The scroll favours water installations and tombs; recorded hoards favour buildings and caves.
What stays unknown: whether the difference comes from a literary list, a different kind of deposit, or reporting bias. Chance and market finds rarely keep their context, so the bias check cannot be completed.

## Plan freeze

- PLAN.md SHA-256: `6d797192bffdb92473237347a6fbe59a93593eca6bd7fc32e3f54acc647369d1`
- Frozen: 2026-10-09T18:07:40Z, before any comparison data were coded.
- PLAN.md section 2 records what I had seen before the freeze.

## Files

- `PLAN.md`: the frozen plan (window, region, definition, categories, statistic, decision wording).
- `comparanda.csv`: 181 candidate concealments, one row each. 161 are eligible; 20 are excluded with a reason. The last seven columns are derived by `concealment.py build`.
- `scroll_contexts.csv`: the scroll's 61 canonical entries, coded for the project translation (P) and three edition branches (Pu = Puech, M = Milik, L = Lefkovits). Each branch change cites a `text/readings.json` id.
- `concealment.py`: build, run and check. Standard library only.
- `results.json`, `RESULTS.md`: the output of `run`.
- `sources_read.csv`: every URL read, with access date and SHA-256 for saved pages.
- `test_concealment.py`: tests for the plan hash, schema, category mapping and determinism.

## Sources

- S1. T02 `hoards.json` (76 records). I reused its find-context text and citations.
- S2. CHRE (chre.ashmus.ox.ac.uk), open access. I listed all CHRE hoards for Israel, the Palestinian Territories and Jordan with a terminal year from -200 to 140. 171 have a midpoint date in the main window. T02 already held 85 detail records; I fetched the other 86 on 9 October.
- S3. Non-coin concealments: Qumran Cave 1 scroll jars and the Cave of Letters vessel cache (both from T02), the Cave of Letters documents and the Masada synagogue genizah (new).
- S4. Eleven web searches by object type only. The rule stopped the search after three searches in a row added no row.
- S5. I did not use the Drive library.

## Result (main run)

Coarse groups, unknown contexts excluded. Counts are INFERENCE: my coding of the reported contexts.

| group | scroll entries | comparanda clusters |
|---|---|---|
| G1 water installation | 29 (48%) | 3 (4%) |
| G2 tomb | 9 (15%) | 2 (3%) |
| G3 cave | 5 (8%) | 19 (28%) |
| G4 structure | 8 (13%) | 41 (60%) |
| G5 open air | 9 (15%) | 3 (4%) |
| unknown (excluded) | 1 | 90 |

- Chi-square 58.7. Permutation p = 0.00005. This is the smallest value 20,000 permutations can give.
- Dissimilarity D = 0.67 (bootstrap 95% interval 0.54 to 0.79). About two thirds of one list would have to change group to match the other.
- Verdict (frozen wording): **DIFFERENT**. "The scroll's mix of hiding places differs from the recorded regional practice. This is compatible with a literary or idealised list, with a list of a different kind of deposit than the recorded hoards, or with reporting bias in the archaeological record. It does not identify any place and does not show that the deposits did or did not exist."
- Largest residuals: water installations (+5.7) and structures (-5.5).
- The three comparanda in water installations are EVIDENCE as reported: a small pool in a Jerusalem building, a sewage pipe under a bath floor at ʿEin Tzur, and a jar "in an ancient cistern" near Hebron (one of two 19th-century accounts).

## Sensitivity runs

| run | D | p | verdict |
|---|---|---|---|
| window 63 BCE to 70 CE | 0.63 | 0.00005 | NOT TESTABLE (26 known comparanda; the rule needs 30) |
| Judaea and the Jordan valley | 0.65 | 0.00005 | DIFFERENT |
| branch Pu (Puech) | 0.65 | 0.00005 | DIFFERENT |
| branch M (Milik) | 0.68 | 0.00005 | DIFFERENT |
| branch L (Lefkovits) | 0.65 | 0.00005 | DIFFERENT |
| scroll pits set to unknown | 0.64 | 0.00005 | DIFFERENT |
| rows instead of clusters | 0.67 | 0.00005 | DIFFERENT |
| coins and metal only | 0.66 | 0.00005 | DIFFERENT |
| fine categories (C01 to C14) | 0.69 | 0.00005 | DIFFERENT |

- By the frozen rule the main verdict is **not robust**: the narrow window gives NOT TESTABLE. The cause is sample size, not direction. The narrow window removes the Bar Kokhba refuge caves; structures then dominate even more (18 of 26).
- The edition branches move at most three entries between groups. No branch changes the verdict.

## Reporting-bias check

| check | n | p | D | verdict |
|---|---|---|---|---|
| B1 excavated vs chance or market | 62 vs 5 | 0.105 | 0.48 | INCONCLUSIVE |
| B2a scroll vs excavated finds | 60 vs 62 | 0.00005 | 0.69 | DIFFERENT |
| B2b scroll vs chance or market finds | 60 vs 5 | 0.17 | 0.43 | NOT TESTABLE |

- B3: the share of unknown context is 16% for excavated finds, 57% for chance finds, 88% for looted or market finds and 98% where the finder is not recorded.
- By the frozen rule the main verdict is **reporting-sensitive**: B2a and B2b differ. In practice the comparison rests on excavated finds. Excavators mostly dig settlements and refuge caves. Chance and market finds, which might come from fields, cisterns or tombs, have almost no recorded context. So the record cannot show whether such places were rare or just unrecorded.

## What this means (INFERENCE)

- The result speaks only to the kind of list (R12). It supports no identification and no location.
- A real retrieval list would name stable landmarks (cisterns, pools, conduits, tombs) to guide a searcher. An excavation report names the immediate find context (a room floor, a niche). Part of the difference may therefore come from two ways of describing a place, not from two ways of hiding.
- The 29 scroll entries in water installations include 7 "pits" (שית, שיח, שוחה, שיא). Treating them as unknown does not change the verdict.
- The scroll's entries are not independent deposits. They are one edited text.

## Choices made while coding (exploratory, after the freeze)

These applied the frozen rules to cases the plan did not name. Each is flagged in the CSV.

- Excluded (20 rows): four shipwreck finds (accidental loss); a street find the source calls "not deliberately concealed"; mint debris; six single coins; a dealer's lot; two groups the sources do not accept as hoards; two grave-associated finds; two duplicates (CHRE 8132 = 18771; CHRE 8455 probably = 8500); and Qumran Cave 3 itself.
- CHRE "Uncertain structure" or a building type with no placement: structure, placement not stated (C14).
- CHRE "Natural feature" with only "cliff" or "desert": unknown.
- CHRE 8124 (Qumran Locus 83) has land use "Cave" in CHRE. I coded it as a cave and flagged a possible database error; de Vaux 1956: 566 was not checked.
- Hebron 1889: cistern, following Gillman's record as reported by Mason and Visonà 2014: 164.
- Modiʿin 2016: "rock crevice against a wall" coded as wall cavity.
- Duma and El Fawar rest on informants' accounts (Mildenberg 1984: 50–51).
- Masada genizah: deposition range 66 to 74 CE assumed from the rebel occupation.
- Scroll entry 23: the deposit is taken to lie at the heap, where the measure ends. Entry 40: in the channel(?). Entry 41: unknown. Entry 52: open ground under a slab.
- B1 was judged testable because the run holds 67 known comparanda in total, although one group has only 5.

## Run and test

From the repository root:

```
python3 -I -B research/comparanda/concealment_contexts/concealment.py build
python3 -I -B research/comparanda/concealment_contexts/concealment.py run
python3 -I -B research/comparanda/concealment_contexts/concealment.py check
python3 -I -B -m unittest discover -s research/comparanda/concealment_contexts -t research/comparanda/concealment_contexts
```

`run` takes about 10 seconds. The seed is fixed (20261009), so outputs are byte-identical.

## Failed or unused links

- https://www.yahoo.com/news/archaeologists-discovered-160-mysterious-coins-130000343.html: WebFetch returned "There was an error while fetching." Search snippets suggest the 2024 Jordan valley hoard, already row t02H18. Not verified.
- https://www.hadashot-esi.org.il/Search.aspx?lang=en: HTTP 301 to curl; not followed. Web searches limited to that site returned no HA-ESI pages.
- coinhoards.org (IGCH) was not tried; T02 found it blocked by robots. Hellenistic hoards are therefore under-represented.
- Primary reports behind several rows (Yadin 1963; Yadin and Talmon, Masada VI; de Vaux 1956; Mildenberg 1984) are not open access. Rows cite them through CHRE or open secondary pages.
