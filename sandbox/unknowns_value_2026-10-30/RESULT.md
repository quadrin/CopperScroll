# Run 25 result: which missing records would settle the most sandbox verdicts?

Integrated 30 Oct 2026. Rule: [RULE.md](RULE.md), commit 8c6c2de, SHA-256 `5a2ac989…db744b` (checked). Inputs: every run's RULE.md and RESULT.md at dbfbf7f (`git diff dbfbf7f` is empty for all 22 run folders and mac_unblock), method 6 (`research/feature_workbench/decisions/`), the Drive index, the arrival register and ACTIVE_TEST. No new evidence was gathered and no run was re-scored. Exploratory.

Files: [out/units.csv](out/units.csv) (52 units), [out/records.csv](out/records.csv) (67 records), [out/links.csv](out/links.csv) (112 links: 81 EVIDENCE, 31 INFERENCE), [out/ranking_evidence.csv](out/ranking_evidence.csv), [out/ranking_all.csv](out/ranking_all.csv), [out/ranking_variants.json](out/ranking_variants.json), [out/undecidable.csv](out/undecidable.csv), [out/scripts/rank.py](out/scripts/rank.py). Reproduce: `python3 -I sandbox/unknowns_value_2026-10-30/out/scripts/rank.py`.

## Headline

Five records reach most of the open verdicts. Three of the five bear on one question: the fissure east of a reservoir (entry 22).

| # | Record | EVIDENCE units (runs) | Access state | What the owner would need to do |
|---|---|---|---|---|
| 1 | **Bar-Adon 1972**, in Kochavi (ed.), *Judaea, Samaria and the Golan* (ASI 1), pp. 92–149 (Buqeiʿa pp. 119–125) | 6 (runs 1, 5, 7, 12) | not in library on this branch | Nothing new, probably. The owner photographed this chapter on 29–30 Oct (branch `claude/kochavi-parts4-5-2026-10-30`, merged to main 30 Oct in PR #59, d5396b8). Re-read pp. 119–125 for the Kh. es-Samra cistern and the Sheikh Dhiab pools. |
| 2 | **Humbert & Chambon 1994**, *Fouilles de Khirbet Qumrân et de Aïn Feshkha* I: the plan with the "faille"; pp. 192, 195–199, 342 | 4 (runs 1, 10, 12, 17) | held by person, request pending (ÉBAF gift copy offered 8 Oct; postage quote pending) | Collect the gift copy from ÉBAF / J.-B. Humbert. Run the arrival check, then read the plan and pp. 192, 342. |
| 3 | **Magen & Peleg 2018**, JSP 18, pp. 58–66 (eastern dump section) | 3 (runs 1, 7, 12) | Mac online-only (22.9 MB) | On the Mac, mark the Drive file "available offline", then split out pp. 58–66. |
| 4 | **Stager 1976**, *BASOR* 221: 145–158 (Samra cistern plan) | 3 (runs 1, 7, 12) | not in library | Download from JSTOR, or a library copy. |
| 5 | **Wright & Milik 1961**, *Biblica* 42, Fig. 5, and **Meshel 1984**, *EI* 17: 251–256 (tied) | 3 each (runs 1, 7) | not in library (the Drive PDF of Wright & Milik lacks Fig. 5) | Library copies of the figure and the article. |

- These six records (five rows) reach 12 of the 30 units that have any EVIDENCE link.
- Two cheap actions also count. **Feldman p. 330 / Patrich 2002 Fig. 22** (2 units, runs 1 and 12) are already photographed and read in the repo, but nobody has checked them for the ground east of Hyrcania's double pool. **Netzer FR I Plans 1, 2, 14 and 26** (run 11, A1) are photographed too; their stair bearings were never extracted.
- **One Mac action would open five records:** making files "available offline" in Google Drive (Magen & Peleg 2018, Zertal & Bar 2019 MHCS 5, Netzer 2001 *Palaces*, Netzer FR I, sheets 19-12 and 18-14). Together they reach 8 units in runs 1, 7, 9, 11, 12 and 19 (EVIDENCE links).

## Ranking 1: EVIDENCE links only

Order: number of EVIDENCE-linked units, then runs touched, then easier access. Main access order: read < Drive ≤10 MB < Mac online-only = Drive >10 MB < not in library < held by person. A held record is placed last because a pending request is not in the owner's hands.

| Rank | Record | Units | Runs | Access |
|---|---|---|---|---|
| 1 | baradon1972-asi1 | 6 | 1, 5, 7, 12 | not in library |
| 2 | humbert-chambon1994 | 4 | 1, 10, 12, 17 | held, pending |
| 3 | magen-peleg2018-pp58-66 | 3 | 1, 7, 12 | Mac online-only |
| 4 | stager1976-basor221 | 3 | 1, 7, 12 | not in library |
| 5= | meshel1984-ei17 | 3 | 1, 7 | not in library |
| 5= | wright-milik1961-fig5 | 3 | 1, 7 | not in library |
| 7= | baradon1989-ghuweir | 3 | 1 | Drive >10 MB |
| 7= | zertal-bar2019-mhcs5 | 3 | 11 | Mac online-only |
| 9= | gutfeld2006-bar32-5 | 3 | 16 | not in library |
| 9= | peleg2009-jsp10-ekteif | 3 | 16 | not in library on this branch (read on main) |
| 11 | feldman-p330-patrich2002-fig22 | 2 | 1, 12 | read (not for this datum) |
| 12= | callegher-in-humbert2016, coin-hoards-VII-p34, coin-hoards-VIII-p65, hoard-catalogues-other | 2 | 4, 15 | not in library |

47 records have at least one EVIDENCE link. The full table is in `out/ranking_evidence.csv`.

## Ranking 2: EVIDENCE + INFERENCE

| Rank | Record | Units (EVIDENCE + INFERENCE) | Runs | Access |
|---|---|---|---|---|
| 1 | stager1976-basor221 | 8 (3 + 5) | 1, 7, 11, 12 | not in library |
| 2 | baradon1972-asi1 | 7 (6 + 1) | 1, 5, 7, 12 | not in library |
| 3 | humbert-chambon1994 | 5 (4 + 1) | 1, 10, 12, 17 | held, pending |
| 4 | gutfeld2006-bar32-5 | 5 (3 + 2) | 16 | not in library |
| 5= | haber2024-hyrcania | 4 (2 + 2) | 1, 7 | Drive >10 MB |
| 5= | mount-hyrcania-project-report | 4 (2 + 2) | 1, 7 | Drive >10 MB |
| 7 | magen-peleg2018-pp58-66 | 3 (3 + 0) | 1, 7, 12 | Mac online-only |

Stager moves to the top only on guesses about what his farm plans hold: Buqeiʿa dams, conduits, stairs and paired features. The two Hyrcania reports rise on guesses that they date dam 44 and the northern aqueduct.

## Ambiguities, done both ways

1. **What counts as a unit.** The rule lists unknown, not discriminating, strict-only fail and fragile. Eight units fit only by paraphrase: the result describes the condition but does not use the type word (for example a near-tie, "pass, but weak", "underpowered"). They are flagged `literal = no`. Variant V1 drops them. Top three: Bar-Adon 1972, Magen & Peleg pp. 58–66, Stager. Humbert & Chambon falls to 4th, because run 17 C4 is not literal.
2. **"The result names it for that unit."** Some results list records only under "Not accessible", without naming a unit. These are kept as EVIDENCE when the record's subject matches the criterion (`basis_kind = RESULT-list`). Variant V2 keeps only links that are named for the unit or supported by another source. Top three: Bar-Adon 1972 (4), Humbert & Chambon (4), Stager (3). Variant V3 (V1 and V2 together) gives the same top three.
3. **Access order.** The rule says "easier access" but does not rank the categories. V4 puts a pending request before "not in library". The top four do not change.
4. **"Structurally undecidable."** The rule's example is a missing observation. Some runs also fail because of their own rule, which no record can fix. Both readings are listed below.
5. **"Already read."** Feldman p. 330, Patrich Fig. 22 and Netzer FR I Plans 1, 2, 14 and 26 are read in the repo, but not for these units. Under linking criterion 2 they still link.

In every variant the same three or four records lead. The headline does not depend on these choices.

## Structurally undecidable runs

A run is listed if, with every linked record in hand, some criterion still could not be scored. **A**: no record can supply the observation. **B**: the run's own rule blocks it. Full table: `out/undecidable.csv`.

| Run | Kind | Why |
|---|---|---|
| 2 Greek letters | A, B | Entry 15's sum is in a lacuna; no Hebrew letter gives Η under the fixed table. (Neither can change the verdict.) |
| 4 Already found | A | Two hoards' contexts are lost at source: Hill 1936 says find circumstances are "not forthcoming", and the Jericho 1874 findspot is disputed. |
| 5 Koḥlit south of Yanun | B, A | K4 is set by the sectors. Surveys do not position pools or cisterns at most of the 49 candidates. |
| 9 Greek architecture | A | Pits in cistern floors, "closed with חליא" and tombs under corners are unknown at all 23 units; reports do not record them. |
| 10 Cave entries | A, B | Item clauses never fail (removal is always possible). The depth clause needs an excavation at the entrance. |
| 11 Achor | A | Milik's "tamarisks" reading needs ancient trees; no record can hold them. |
| 14 Imagery | B | Detection rate 0.75 is below 0.8, so "not seen" can never become a fail. |
| 15 Hoard contexts | A | As run 4. The Feshkha mass needs the coins, whose custodian is unconfirmed. |
| 18 Copy search | B | The shuffle test cannot be passed even by 3Q15. |
| 20 Middot | A, B | Middot never describes hiding places, so no strict pass is possible. |
| 21 Amount gravity | B | 5 weighed anchors; the floor is 6. More anchors need new placements, not records. |
| 22 Reverse lookup | B | With 10 shuffles the smallest p is 0.091. |

**Coverage gaps, not structural** (records are named for some units, none for others): run 1 (J6 at five places; J5 at three), run 7 (J6 great heap; J9 mound dating) and run 16 (tunnels ST3 and ST4 have no position).

**Could be settled by records:** runs 12 (E1, E4), 17 (C1), 19 (sheets).

**Runs with no verdict unit**, because their verdicts rest on completed counts or tests: 3 (purity rule) and 6 (onomasticon).

## Comparison with method 6

Method 6's queue was recomputed by its own script (`discriminate.py --summary`, run inside `rank.py`). Its order is: 1 XII 10; 2 Kenyon section; 3 IV/17 L-656; 4 (tied) Jericho contacts, Kallai, Siloam, Wadi.

- **Little overlap.** Only two method 6 records appear in any sandbox link. The IV/17 L-656 file is linked once, to run 10, as a RESULT-list "not opened" mention (EVIDENCE rank 46). The Wadi Nuʿeima bath file is linked once, to run 11 A1, by INFERENCE only.
- **So the order cannot be compared.** For the two shared records, method 6 has L-656 above Wadi, and so does the sandbox (1 unit against 0 EVIDENCE units). That is agreement on two records with almost no counts.
- **Method 6 ranks high, the sandbox does not need:** XII 10 (rank 1) and the Kenyon section (rank 2). No sandbox run uses the XII 10 reading or Tell es-Sultan's graves. Run 5 is conditional on the Janoaḥ reading but does not score it. Kallai pp. 172–173 is read and recorded in both.
- **The sandbox ranks high, method 6 does not list:** every record in the headline. Method 6 has no Qumran task ("No decision task concerns Qumran", arrival items), while the sandbox's open verdicts cluster on Qumran, Hyrcania and Kh. es-Samra (entries 20–24).
- The access categories differ in kind. Method 6's records are mostly requests to people, pending. The sandbox's top records are books, articles and online-only files that the owner can reach without a reply.

## Caveats

- **Branch state.** This branch (`sandbox/methods-round5`) does not hold the 29–30 Oct book reads. Main (PR #59, d5396b8, merged 30 Oct) has Bar-Adon 1972 and Peleg 2009 (JSP 10) read from the owner's photographs; the sandbox branch was cut before that merge. Their access state here is "not in library", following the committed files on this branch. On main, rank 1 is therefore "read; extract the Samra cistern and the Buqeiʿa pages". Nothing in the ranking order changes.
- **Units.** Units are coarse: one per criterion per run, with places pooled. A record that settles one place counts the same as one that settles all seven. Counts are not weights, and no verdict is predicted to change direction.
- **Links.** Each link was made by one reader (this agent) from the result texts. Run 1's evidence files were used where its RESULT points to them. INFERENCE links are guesses about content and should not be cited as needs.
- **Citations.** Several records are cited only as precisely as the runs cite them: Gophna & Porat 1972 pages; "Avigad/Geva" reports; DJD VI; Porat et al. 2019; Callegher "in Humbert et al. 2016". These are marked in `records.csv`.
- **Exposure.** Humbert & Chambon 1994 is an arrival-register item: read pp. 192 and 342 only after `arrival.py check`. The DJD III text volume (run 10) holds the 3Q15 edition, which is reserved.
- **Effort.** This run sent no requests and contacted no one. "Owner action" lines are suggestions only.

## Integrator check, 30 Oct 2026
- Rule SHA-256 checked (5a2ac989…). `out/scripts/rank.py` re-run with `python3 -I`; both rankings reproduce byte for byte.
- Correction: the branch holding the Bar-Adon 1972 and Peleg 2009 reads is merged to main (PR #59, d5396b8), not unmerged. Access states in `out/records.csv` follow the sandbox branch, as the rule's inputs did. Access is only the last tie-breaker, so the EVIDENCE ranking order of the top records does not change; Peleg 2009's place inside the 9= tie could move.
- Practical effect: the top record needs no new access. Its Buqeiʿa pages (pp. 119–125) are already photographed and need only to be read for the Kh. es-Samra cistern and the Sheikh Dhiab pools.
