# Koḥlit as a small landmark network

8 October 2026 UTC. Exploratory method work. It makes no identification claim, adds no outcome-ledger count and changes no registered result.

## The lesson applied

J. T. Wood found the Artemision at Ephesus (1863–69) step by step. An inscription in the theatre led him to a city gate. The gate led him to a road, and the road to the precinct wall. Each step rested on a different kind of evidence. As this round's brief puts it, he also set aside a misleading literary distance.

Here each Koḥlit model becomes a chain of reference points:

- Each step names one relation from the text, the feature assigned to it, and the evidence for it, with its kind and its field lineage.
- The chain marks which relations were used to select the model.
- The next link must test a relation that was **not** used to select the model. It says what should be found, where, in which record, and which result would contradict the model.
- Stated distances are set aside until both end points are fixed: Entry 11's four cubits (a digging depth), Entry 4's six cubits, and Entry 16's 14, 40 or 41 cubits (restored). The rarity count's 1 km and 10 m are project tolerances, not text.

## Files

| File | What it holds |
|---|---|
| [chain.json](chain.json) | 18 relations, 12 reading dependencies, 49 records, 28 models and 56 next links |
| [next_links.md](next_links.md) | The most findable next link of each model, ranked, with its record and whether it is already requested (generated) |
| [registration_protocol.md](registration_protocol.md) | How to register the incoming pre-camp photographs and plans north of Tell es-Sultan, with the reference-point table |
| [reference_points.json](reference_points.json) | The same 17 reference-point candidates, machine-readable |
| [check_chain.py](check_chain.py) | Checks the unused-relation rule and lists dependencies; writes next_links.md |
| [registration.py](registration.py) | Similarity or affine fit with one withheld check point, measured error and threshold verdicts |
| `test_check_chain.py`, `test_registration.py` | 40 unit tests |

## Models

The 28 models are:
- Tell es-Sultan, Kh. el-Marjama, Kh. Qumran and Qarn Sarṭaba;
- the 22 other units that the rarity count leaves at two of three conditions, Kh. Samiyye among them;
- the Janoaḥ route.

Kh. el-Marjama meets only one condition (graves to the north), but the brief names it. The 26 two-of-three units come from the registered `unit_results.csv` (primary rules, with Nigro, after both addenda). The checker confirms that no two-of-three unit is missing.

The relationships workbench has 40 retained combinations. All 40 are mapped:
- 28 unknown combinations belong to six surviving assignments, held by the Tell es-Sultan, Kh. el-Marjama and Janoaḥ models.
- 12 contradicted combinations belong to the 1898 reservoir and the church-crypt basin. They are kept as contradicted branches.

### The four named chains

| Model | Reference points already used, and their evidence | Next unused link | Record | Requested? |
|---|---|---|---|---|
| Tell es-Sultan | a ruin mound (Kenyon III); spring basin at the east foot (Dorrell; SWP words); north-slope graves (Kenyon III 173–174; Nigro cat. 53); NS1, D9 or the later quarry pits to the north (Kenyon II–III) | tombs within 10 m of a pit mouth in the strip just north of the tell | Garstang Museum JG/8; PEF Garstang Papers and pre-1948 photographs; Nigro's records | yes |
| | | quarry pits cut while the graves were still open, with no fill later than 135 CE | Kenyon III plate volume: eastern section at 37.50–38.00 m N, Pl. 111b | no |
| | | finds sealed under the basin rim no later than the first century | fieldwork behind the 1898 back wall (Dorrell p. 112) | no |
| Kh. el-Marjama | Hellenistic and Roman surface record (Highlands 732 from Kallai); Dhahr Mirzbaneh tombs to the north (WBADB S1647) | the pool's actual position (45°–135°) and a date not after 135 CE | Kallai 1972 pp. 172–173 | no |
| Kh. Qumran | caves to the north (Cave XI/20, WBADB); northern cemetery (de Vaux 1973 pp. 57–58) | under Milik's reading, a north-sector cave with a north-facing opening | 2002 cave-survey entries; IAA cave records | IAA: yes |
| Qarn Sarṭaba | the Herodian pool on the east side (Zertal p. 471); cave-cisterns or robbing pits to the north | graves in the north sector, ideally at a pit mouth | Tsafrir and Magen 1984; Bar-Adon 1972 | no |

### What the chains show

- **Tell es-Sultan.**
  - The steps are not independent: the graves, the pits and the mound all rest on Kenyon's 1952–58 expedition. The checker flags this.
  - The requested pre-camp records can test only where an opening lies relative to graves. They cannot contradict the model, and they cannot date the opening.
  - The records that could contradict the model are not on the pending list: Kenyon III's plate volume (eastern section, Pl. 111b), Kenyon's field records, and a sealed context at the spring.
- **Entry 15 at Tell es-Sultan.** It is excluded as a test. Puech, who proposed the model, restored both the Koḥlit link and the direction.
- **The "northern corner".** The 1908 plan (Dorrell Figs 20–21, already inspected) shows the reservoir's north end curved along the old spring-house wall. This bears on Entry 11's "northern corner", but only for post-ancient states. Any test must use records outside Dorrell's selection, with the prediction registered first.
- **Kh. el-Marjama.** One library scan, Kallai 1972 pp. 172–173, can decide both the position and the date of the pool. The CORONA dark square lies about 5° inside the 135° edge, so its registration must reach about 15 m.
- **Shared rows.** In 11 two-of-three units, one WBADB row supplies both the pit and the graves. The tombs-at-the-mouth relation at that row is therefore the natural next test.
- **Exploratory measurement already possible.** ESI 9 Fig. 124 (already inspected) shows Kh. el-Ghirur's cistern mouths and a sarcophagus about 20 m south-east of that site. Measuring them now would be exploratory, not an unseen test (units S845 and S843).
- **The anchor matters.** With the WBADB point for Tell es-Sultan (50 m precision), a feature 150 m away counts as "north" only within about 11° of due north. The anchor's precision, not the photograph's registration, sets this limit.

## Ranking of next links

[next_links.md](next_links.md) ranks the most findable next link of each model. The order is:
1. Tier: supplied or open-access record not yet read, then requested, then library scan, then archive order or fieldwork.
2. Whether the record can contradict the model.
3. Reading robustness.

Results:
- **Tier 1, 9 models.** Their link uses a supplied or open-access record not yet read for that relation.
  - Five are opening-facing tests under Milik's reading at caves cited by WBADB: Qumran, Tulul Abu el-ʿAlaiq, Kypros, Tell es-Samrat and S3961. They test RB-M only.
  - The other four: Zertal Vol. 4 Site 194 (Tell esh-Sheikh Dhiab), HA 28–29 (Tananir), Highlands pp. 700–702 (Udala), and the IAA notices on Kh. ʿAlmit (S2849).
- **Tier 2, 2 models.** They wait on requested records: the XII 10 image (Janoaḥ reading gate) and the Garstang, PEF and Nigro records (Tell es-Sultan).
- **Tier 3, 17 models.** They need a library scan: Kallai, Gophna and Porat, Dinur and Feig, Feldstein, Sion, Finkelstein 1993, Ben-Yosef and Bar, Tsafrir and Magen, Patrich and Rubin, or Peleg.
- 7 of the 28 top links use a record already on the ACTIVE_TEST pending list.
- Contradiction strength of the 28 top links: 11 can contradict outright; 16 only through an explicit absence statement in the source; 1 (Tell es-Sultan's photographs) can only confirm.

## Dependencies on disputed or restored readings

`check_chain.py --deps` lists them per model and per link.
- 52 of the 56 links depend on a reading choice.
  - The commonest are the "buried" branch, which drops the tombs (24 links), Lefkovits's "in the east of" (21), and the disputed second word of XII 10 (15).
  - The other two are Milik's "opening to the north" (6) and Allegro's reading of IV 11 (1).
- 6 links test a relation whose reading is itself disputed: the opening facing and Entry 19's eastern pit.
- No next link uses a restored relation.
- The Janoaḥ model exists only if XII 10 reads שבינח, so its first link is a reading gate under the frozen protocol, not a landmark prediction.

## What stays unknown, and why

- **Construction dates and accessible-use dates** for every assigned pool, pit and grave group. The sources give typology, relative order or first photographs, not dated use.
- **The strip just north of Tell es-Sultan.** It was never searched and is built over. Photographs can show where openings were, not when they were open.
- **Kallai's pool at ʿEin Samiya.** Its pages are unread, so the pool has no position and no date.
- **The regional denominator.** The rarity count left m ≫ k, so a chain for one model gives no discrimination against the others.
- **Unseen tests.** None exists yet. A next link becomes one only if its prediction is registered before its record is opened. Links on records already inspected are exploratory; the checker warns on them.

## Run and test

From the repository root:

```sh
python3 -I research/assessments/kohlit_chain/check_chain.py
python3 -I research/assessments/kohlit_chain/check_chain.py --deps
python3 -I research/assessments/kohlit_chain/check_chain.py --check-ranking research/assessments/kohlit_chain/next_links.md
python3 -I -m unittest discover -s research/assessments/kohlit_chain -p 'test_*.py'
```

The checker runs the relationships evaluator read-only and compares the stored rarity values with `unit_results.csv`. Current output: 0 errors and 21 warnings. Twenty warnings are shared lineages among selection steps; one is a link whose only record is already inspected (Udala's pool). `registration.py RECORD.json` runs one registration (see the protocol).

## Provenance and limits

- The per-feature evidence of the 22 generic models comes from the frozen `match.py`, run read-only on the merged coder sheets (`coded_v3`) and packet v4. Those packets are third-party data outside Git. `chain.json` keeps only short citations; quotations are shortened to 10 words or fewer.
- A scratch helper assembled `chain.json`; it is not in the repository.
- Condition values in `chain.json` are checked against the registered results.
- No web source was opened, no message was sent, and no image of XII 8–12 was viewed.
- Puech 2006 and Lefkovits 2000 were not consulted; the repository's reading records sufficed.

## Proposed changes to shared files (for the integrator)

- `research/ACTIVE_TEST.md`, "Key reports" line: append ` · [Koḥlit landmark chain](assessments/kohlit_chain/README.md) and [registration protocol](assessments/kohlit_chain/registration_protocol.md)`.
- `research/ACTIVE_TEST.md`, question 2: append "Before any Garstang, PEF or Nigro record is opened, register chain link SULTAN-1 and follow the registration protocol; a located opening does not date it."
- Optional, for the integrator to decide: add Kenyon III's plate volume (eastern section, Pl. 111b) and Kallai 1972 pp. 172–173 as library-scan targets. They are the records that could contradict the Tell es-Sultan quarry branch and decide the Marjama pool.
