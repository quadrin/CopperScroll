# Arrival register: predictions frozen before requested items arrive

**What it is:** for each of 22 requested or wanted items, what every live model in the repository predicts the item will show, frozen and hashed before it arrives.
**Main result:** none of the items has arrived. Four XII 10 image items tie at the top of the ranking (2.24 expected Koḥlit classes excluded each); Kochavi 1972 comes next (2.21 Koḥlit classes plus 1.55 chain models). The Tell es-Sultan records separate no registered class.
**What stays unknown:** what the items will show. Whether any reply comes. Expected values use a declared convention, not probabilities.

9 October 2026 UTC. Worker: arrival-register. Exploratory. No identification, deposit or outcome-ledger count. No registered result is changed, and no closed or parked test is reopened.

## The idea

Ventris's grid was proved by Pylos tablet Ta 641. The tablet had been dug up but not read when the grid was fixed. Read with the grid unchanged, it spelled "tripods" beside drawings of tripods. Here the project waits for many replies and files. If we write down, before each arrives, what every live model predicts it will show, each arrival becomes a test instead of something explained afterwards.

**A prediction counts only if it was committed and pushed before the item arrived.** As of 9 October 2026 none of the listed items has arrived. Parts that arrived earlier are marked "arrived before registration: not a test" in their item files.

## Files

| File | What it holds |
|---|---|
| [items/](items/) | One file per item: what it is, holder, request date, status, what arrived earlier, handling, and every model's prediction with outcome ids |
| [register.json](register.json) | The same, machine-readable, with source-file hashes and the ranking |
| [ARRIVAL_PROCEDURE.md](ARRIVAL_PROCEDURE.md) | Who opens an item, how it is compared with its frozen file, how partial and inconclusive results are recorded |
| [RANKING_PLAN.md](RANKING_PLAN.md) | The ranking plan, frozen before the ranking was computed |
| [RANKING.md](RANKING.md) | Items ranked by expected separations, with a sensitivity table |
| [MANIFEST.md](MANIFEST.md) | SHA-256 of every frozen file |
| `specs.py` | Hand-written item data; every prediction names its source model |
| `build_register.py` | Builds register.json, items/ and RANKING.md from specs.py and the repository, read-only |
| `arrival.py` | Checks the manifest; validates an outcome record |
| `test_arrivals.py` | 19 unit tests |

## Sources of the predictions

Predictions restate existing models only. Each item file cites them.
- The 28 Koḥlit models and their next links: `assessments/kohlit_chain/chain.json`.
- The 10 Koḥlit classes, 7 XII 10 strings, 6 Entry 25 classes and 3 closed branches: `feature_workbench/decisions/discriminate.py`, run read-only.
- The IV/17 and Tell es-Sultan coverage joins: `feature_workbench/coverage/evaluate.py`, run read-only.
- The Entry 60 registry v2 targets: `agent_review_2026-10-07/wave2/W2B_model_v1/registry_v2_entry60.json`.
- The closed results' reopening criteria: `ACTIVE_TEST.md`.
- Item-specific models: the saw-gap check, the R11 engraving-order protocol, the J19 St Andrew alternatives, the Qumran dam referents, the A(C)94 geometry bands, the rarity rules and the observation-process audit.

Where a model makes no prediction about an item, the item file says so. For the XII 10 and 21/22 items there is no letter prediction. Those files carry only the table from frozen-protocol outcomes (commit fd3f334) to the model classes that survive. No image of XII 8–12 or of the 21/22 cut was opened.

## Status of the items on 9 October 2026

Checked against ACTIVE_TEST, the shared status file of 8 October, the outreach records and the Drive index. **No item has arrived.**
- Pending (16 items): USC, Manchester Museum, Joan Taylor, ÉBAF copy and X-rays, ÉBAF Qumran volumes, University of Manchester Library, Høgenhaven, Garstang Museum, PEF, IAA, Zuckerman, Szanton, Bar-Nathan and Porat, Staff Officer for Archaeology, Reeder and Jol, and the Mosaic Centre (scan promised for mid-October).
- Partial (1): Nigro replied that karstic cavities are common in the strip; his records have not come.
- Not obtained, not requested (4): Zertal vol. I, Kochavi 1972, the L-656 file, and Kenyon III's plate volume. Kenyon III is not on the brief's list. It is added because the decisions module ranks it second.
- Declined (1): Facsimile Editions. Listed, not ranked.

**Arrived before registration: not a test.**
- Nigro's statement that cavities exist in the strip.
- Qumran vol. II (Humbert and Gunneweg 2003). It has been in the repository since 28 September.
- The C.10a.1 and C.10.1 Allegro photographs. Their previews were inspected on 5 October, so study scans add resolution, not a new observation.
- The published, low-resolution Figure 4.6.
- Meinardus pp. 181–182, 186–190 and 193–194 (user-reported snippets) and the derivative "Herodian" attribution of pp. 183–184.

## Results

### Ranking

Universe: 26 decision classes and 25 chain models outside the decision roster. E is the expected number of classes excluded if the item arrives, under the frozen plan. See [RANKING.md](RANKING.md).

| Rank | Item | E_total | Koḥlit classes in E | Notes |
|---|---|---|---|---|
| 1–4 (tie) | ÉBAF X-rays; Manchester Museum; Joan Taylor; USC masters | 7.47 each | 2.24 | 5.23 is XII 10 strings. The four are substitutes: the first copy that passes the protocol's gates is the observation. |
| 5 | Kochavi 1972 | 3.77 | 2.21 | 1.55 chain models over 16 contradictable links, mostly absence-statement only |
| 6 | Univ. of Manchester Library TPA/1/132 | 1.87 | 0.56 | Only if the file holds a photograph of segment 21/22 made before the cut (coverage ¼) |
| 7 | Kenyon III plates (added) | 1.67 | 1.67 | Can exclude the quarry-pit classes c02–c05 |
| 8 | L-656 file | 0.60 | 0 | Entry 25 only. No decisive row until a mouth-aspect rule is frozen. |
| 9 | IAA cave records | 0.33 | 0 | The only item that can separate RB-M from RB-P (opening facing, at 5 non-roster models) |
| 10–12 | Bar-Nathan and Porat; Szanton; Staff Officer (Wadi) | 0.25; 0.25; 0.125 | 0 | Each can exclude one closed named branch |
| 13–14 | Reeder and Jol; ÉBAF Qumran volumes | 0.06; 0.04 | 0 | Qumran links with low coverage |
| 15–21 | Meinardus; Zuckerman; Garstang; Høgenhaven; Nigro; PEF; Zertal vol. I | 0 | 0 | See below |

- The top seven ranks do not move when the decisive share changes from ¼ to ¾. L-656, IAA, A(C)94 and Siloam swap places at ¾.
- No item guarantees any separation. Every item has a silent or inconclusive outcome that leaves every class alive.

### Items that separate nothing, and why

- **Garstang Museum, PEF, Nigro.** These were requested for active question 2. Their chain links (SULTAN-1, -5, -6) are one-sided: they can confirm a mouth–tomb pair, but cannot contradict. A new pit in the strip is not one of the registered pit roles, so it separates no decision class. Photographs locate an opening but do not date it.
- **Høgenhaven.** One reader, not blinded, outside the protocol's two-reader design. The protocol maps any such reading to "not identifiable".
- **Meinardus and Zuckerman.** Each is the named record for reopening a closed result: entry 29 St Andrew and R11. Neither changes a live class. For R11 the protocol's terminal rule still needs an authenticated crossing.
- **Zertal vol. I.** It touches 6 main-set units. So k ≤ 6 while m ≥ 307, and the rarity verdict "not measurable" cannot change.

### Deterministic predictions worth noting

- **L-656 file.** With the file alone, all 8 IV/17 coverage joins stay undeterminable. Each branch also needs a model declaration that no record supplies.
- **Tell es-Sultan coverage.** All 4 joins stay undeterminable whatever the Garstang, PEF, Nigro or Kenyon records show, because Entry 60 gives no distance.
- **USC masters and letter controls.** The 20 USC masters alone cannot run the series S1 calibration. That needs masters of cuts 1–18.
- **Cut letter at 21/22.** It can become decisive only through an authenticated image made before the cut (protocol line 45). The Manchester cutting photographs and film, and possibly TPA/1/132, are the only requested routes to such an image.

## What stays unknown

- What any item will show. Whether and when replies come. The ranking is conditional on arrival.
- The coverage factors (1, ½, ¼, 0) and the equal halves are declared conventions, not estimates.
- Unused status of every XII 10 image. The protocol records prior exposure of USC cuts 21–23 and of the DQCAAS Allegro compositions. Its audit must run before release.
- The exact identity of ÉBAF's "Qumran vols I–II" (inferred as Humbert and Chambon 1994 and Humbert and Gunneweg 2003).

## Freeze record

- RANKING_PLAN.md written and hashed at 2026-10-09T18:13:49Z, SHA-256 `51fb2c36d9175ab52d8cba18fbb2aefe4dc523bfe6618b0830823592200bf30e`. The first ranking was computed at 18:20:46Z.
- Sources: repository base 05eca99, branch analogues-2026-10-09. register.json lists the SHA-256 of every source file used.
- Registration commit: _to be filled by the integrator with the commit that first adds MANIFEST.md, and its push time._

## Run and test

From the repository root:

```sh
python3 -I -B research/preregistration/arrivals/build_register.py        # rebuild (only before registration)
python3 -I research/preregistration/arrivals/arrival.py check            # verify the frozen files
python3 -I research/preregistration/arrivals/arrival.py status
python3 -I research/preregistration/arrivals/arrival.py validate research/preregistration/arrivals/outcomes/<file>.json
python3 -I -B -m unittest discover -s research/preregistration/arrivals -t research/preregistration/arrivals
```

`-B` keeps Python from writing `__pycache__` into the folder. If upstream source files change later, the "matches committed" test skips; the frozen copy is kept.

## Limits

- The register restates models; it adds no new theory. Coverage factors are this worker's declared judgement, labelled per item.
- Puech 2006 and Lefkovits 2000 on the owner's computer were not needed and were not read. No web source was opened and no message was sent. Drive was not used beyond the repository's Drive index.

## Proposed changes to shared files (for the integrator)

1. `research/ACTIVE_TEST.md`, "Key reports" line: append ` · [Arrival register](preregistration/arrivals/README.md)`.
2. `research/ACTIVE_TEST.md`, after "Pending requests": add one line: "Before opening any arrival, run `arrival.py check` and follow `preregistration/arrivals/ARRIVAL_PROCEDURE.md`."
3. Fill the "Registration commit" line above with the commit that first adds MANIFEST.md.
4. Before the L-656 file or the IAA records arrive, freeze two things. First, an Entry 25 mouth-aspect rule. Second, the IV/17 target declarations: zone outline, origin point, sector, depth band and radial tolerance. Without them neither item can separate the bearing classes or decide coverage.
5. Optional: register the supplied but unread Tier 1 records in the same way before anyone reads them. These are the ʿAtiqot 41 cave entries, Zertal vol. 4 site 194, HA 28–29, Highlands pp. 700–702 and the IAA notices on Kh. ʿAlmit. They are the cheapest Pylos-type tests in the repository.
