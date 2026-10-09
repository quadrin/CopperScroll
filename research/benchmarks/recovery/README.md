# Recovery benchmark

Built 8 October 2026 UTC. Exploratory method work. It makes no identification claim, and it adds no count to the outcome ledger.

## What it measures

`research/shared_tools/benchmarks.py` checks calculations: affine fits, plan distances and a failed registration. This benchmark tests the whole inference step that comes after them.

A case imitates a Copper Scroll entry. It has a short instruction, a redacted site description and three to six candidate features. The features come from a real survey or excavation report. A key, written from that report, says which candidate the instruction describes. The key can also say "none" (the feature is not among the candidates) or "insufficient" (the case cannot select one). Some information is removed on purpose, for example a direction, a distance or a date.

The procedure reads the instruction, tests every candidate with the project's rules, and returns a candidate, "none" or "insufficient_evidence". It also answers one withheld question, such as the side of the entrance. It answers only when the instruction or the selected candidate's record gives the answer.

The score counts correct selections, wrong selections, abstentions on decidable cases, and withheld answers among the cases where the procedure did not abstain.

## Files

| Path | What it is |
|---|---|
| `procedure.py`, `procedure_constants.json` | The rules, as small predicates that return true, false or unknown. |
| `harness.py` | Loads cases, writes one output per case, checks key hashes, writes `score.json`. |
| `ablate.py` | Development batch only: restores removed information and records what changes. |
| `dev/source_records.json` | Facts copied from five open-access reports: site numbers, map references, opening sides, dates, quotes of 12 words or fewer. |
| `dev/build_dev.py` | Builds the 12 cases, the key and `restore.json` from those facts. |
| `dev/dev-001.json` … `dev/dev-012.json` | The development cases. |
| `dev/key.json` | The development key. It is public; the reserved key is not. |
| `dev/restore.json` | The values each degradation removed. Only `ablate.py` reads it. |
| `dev/outputs/` | One output per case and `score.json`. |
| `dev/ablation.json` | Restoration and removal runs. |
| `tests/` | 33 unittest tests. |
| `reserved/` | The held-out batch. Another worker writes it. This worker never read any file in it. A final file listing of `research/benchmarks` showed only its file names. |

## Run

From the repository root, with Python 3.10 or later and no other packages:

```sh
python3 -I research/benchmarks/recovery/harness.py research/benchmarks/recovery/dev --key research/benchmarks/recovery/dev/key.json --verify-key
python3 -I research/benchmarks/recovery/harness.py research/benchmarks/recovery/dev --out research/benchmarks/recovery/dev/outputs --key research/benchmarks/recovery/dev/key.json
python3 -I research/benchmarks/recovery/ablate.py
python3 -I research/benchmarks/recovery/dev/build_dev.py
python3 -I -m unittest discover -s research/benchmarks/recovery/tests -v
```

The reserved batch is run once, by the integrator, after the procedure is frozen. First check the key, then score. Keep the key outside the repository and the outputs outside `reserved/`:

```sh
python3 -I research/benchmarks/recovery/harness.py research/benchmarks/recovery/reserved --key /path/outside/repo/reserved_key.json --verify-key
python3 -I research/benchmarks/recovery/harness.py research/benchmarks/recovery/reserved --out OUTPUT_DIR --key /path/outside/repo/reserved_key.json
```

`score.json` records the SHA-256 of `procedure.py`, `procedure_constants.json` and `harness.py`. The development run used procedure.py `5401b073…`, procedure_constants.json `23e12c74…` and harness.py `7e7f8cd6…`. A reserved run with other hashes did not use this procedure.

The harness loads only files named `dev-NNN.json` or `res-NNN.json`. It accepts a key as a JSON array, a JSON object keyed by case id, or JSON Lines. It refuses to score if any hash differs.

## Case format

Cases follow the integrator's fixed schema (8 October 2026). A case file holds `case_id`, `batch`, `instruction`, `context`, `candidates` (each with `id` and `features`: `type`, `position` {`bearing_deg`, `distance_m`, `relative_to`}, `opening`, `date` D/L/U, `notes`), `degradations`, `withheld_question`, `withheld_options` and `key_sha256`. A key entry holds `case_id`, `answer` (a candidate id, "none" or "insufficient"), `withheld_answer`, `sources` and `why`. Its hash is the SHA-256 of `json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`.

The procedure also reads three optional fields in `position`, if present:

- `kind`: `plan` (a bearing and distance), `words` (a direction word from a text) or `none`. Without it, a number in `bearing_deg` means `plan`, and a `direction` word means `words`.
- `direction`: a compass word, such as `southeast`, for a words position.
- `precision_m`: the coarser precision of the two points. A bearing is valid only if the distance is at least three times this value (Koḥlit packet rule).

Cases without these fields still run.

## The rules

Each rule comes from an existing project file. None of those files was changed.

1. **Direction words cover 90-degree sectors.** North is 315–45°, east 45–135°, and so on. A numeric bearing on a sector edge counts as inside (`match.py` `in_sector`). A verbal NE, SE, SW or NW gives unknown, unless the instruction uses the same word (`PROTOCOL.md` §4, position rule 3; `match.py` `position`).
2. **A words position with no distance counts as within the limit** (`PROTOCOL.md` §4). If the instruction gives no distance, the project's 1 km limit applies (`protocol_constants.json` `limits_m`). If the instruction gives a distance band ("at forty cubits"), a words position with no distance is unknown.
3. **A position measured from another point is unknown** (`match.py`: `relative_to` other than the unit).
4. **Cubits are 0.40–0.60 m.** This is the project's exploratory range (`research/assessments/entry29_jericho_pools/README.md`). "At N cubits" means 0.40N–0.60N m. "Within N cubits" means up to 0.60N m. A distance in metres is read as ±10 %; this one constant is the benchmark's own.
5. **Dates: D and U pass, L fails** (`PROTOCOL.md` §11; `match.py` `date_ok`).
6. **Unknown never counts as absence.** One contradicted predicate rejects a candidate. An unknown predicate leaves it alive (`feature_workbench/relationships/evaluate.py` `conjunction`).
7. **Decision.** No survivor gives "none". Two or more survivors give "insufficient_evidence". One survivor is selected only if every predicate is true. If one of its predicates is unknown, the output is "insufficient_evidence".
8. **Withheld question.** The procedure reads which property the question asks about: entrance side, date, or side of the reference. It answers from the instruction first, then from the selected candidate's recorded field. A value between two offered options, such as north-east when only north and east are offered, gives "unknown". Free-text `notes` are never read.

The instruction parser is a small word list and a few patterns. It finds the feature type, the direction and its reference point, the distance and the opening. Every output lists the parsed instruction and every predicate result in `reasons`, so a misreading is visible.

## Development batch

All features come from open-access Hadashot Arkheologiyot – Excavations and Surveys in Israel (HA-ESI) reports, read on 8 October 2026 UTC. They lie in Lower and Western Galilee and the northern Negev. None is in `tables/phase3_places.csv` or in Jerusalem, Jericho, Qumran, the Dead Sea cliffs or the Samaria and Manasseh hills. HA-ESI reports have no printed pages, so citations give the report URL, site numbers and figure numbers.

| Source | Cases |
|---|---|
| Lerer 2012, Horbat Qana, Survey, HA-ESI 124, sites 14–34, Fig. 1 ([id=2048](https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=2048)) | 001–003 |
| Aladjem 2014, Nahal Duda'im, Mishmar Ha-Negev Forest, HA-ESI 126, sites 9–21, Fig. 1 ([id=12657](https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=12657)) | 004–006 |
| Aladjem 2013, Horbat Za'aq, Survey, HA-ESI 125, sites 2–29, Figs. 1–2 ([id=4346](https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=4346)) | 007–008 |
| Abu Raya and Shapiro 2011, Ahihud, 'Akko–Karmi'el Railway, Survey, HA-ESI 123, sites 5–23, Fig. 1 ([id=1925](https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=1925)) | 009, 012 |
| Hanna 2012, Dabburiya, Har Devora, Survey, HA-ESI 124, sites 3–10, Figs. 1, 9–18 ([id=2179](https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=2179)) | 010–011 |

Evidence classes stay separate. Map references, opening sides and type words are the reports' records. Bearings and distances are computed here from those map references. "Probably a field watchtower" is the surveyor's label and is coded as uncertain. Dates are the surveyors' attributions: sherds of a period found at a feature, or a building style. In cases 010 and 011 some positions are the report's own words instead of computed values. No value was measured from an image. HA-ESI text is © Israel Antiquities Authority; quotes in `source_records.json` are 12 words or fewer, and no figure is stored here.

| Case | True feature (report site) | Removed on purpose | Key | Output | Result |
|---|---|---|---|---|---|
| 001 | Qana 20, tomb | nothing (control) | c4 | c4 | correct |
| 002 | Qana 22, tomb | instruction's opening | insufficient | insufficient | correct |
| 003 | Qana 34, tomb | true feature left out | none | c1 (Qana 16) | **wrong** |
| 004 | Duda'im 14, watchtower | instruction's direction | c1 | c1 | correct |
| 005 | Duda'im 14 | direction; rival's date (L → U) | insufficient | insufficient | correct |
| 006 | Duda'im 14 | direction; true feature left out | none | none | correct |
| 007 | Za'aq 2, building | nothing; words and map disagree | c5 | none | **wrong** |
| 008 | Za'aq 21, cave | nothing; six caves fit | insufficient | insufficient | correct |
| 009 | Ahihud 16, cave | direction; rival's distance | insufficient | insufficient | correct |
| 010 | Dabburiya 4, cave | nothing; source gives only "southeast" | insufficient | insufficient | correct |
| 011 | Dabburiya 8, cave | nothing; words positions without distance | c2 | c2 | correct |
| 012 | Ahihud 16, cave | a rival's distance | c5 | c5 | correct |

**Key conventions.** The key gives the true feature when the case can select it. It gives "insufficient" when two or more candidates fit every stated relation, or when the true feature's stated relation cannot be tested from the case. It gives "none" whenever the true feature is not among the candidates, even if another candidate fits. The same worker that wrote the procedure wrote these keys.

## Results

Selection: 10 of 12 correct. Two outputs were wrong. There were no abstentions on decidable cases. Five abstentions were correct.

Withheld question: 7 cases did not abstain. Six answers matched the key and one was "unknown". Two of the six matches are weak. In case 007 both key and output are "unknown". In case 003 the answer came from the wrong tomb, which happens to open on the same side.

Both errors are real failure modes, not coding slips.

- **Case 003, a fitting rival.** The true tomb (site 34, 199 m at 65°) was left out. Site 16 (191 m at 100°) is another tomb east of the wall at the same distance. The procedure selected it. The rules cannot detect an unrecorded true feature when a rival fits.
- **Case 007, words against map.** The report places site 2 "c. 200 m south of the ruin". Its map reference lies 283 m at 125° from the map reference the report gives for the ruin's survey. Our inference: that reference marks the survey's general location, not the ruin's centre. Twenty-four of the 39 sites in the ruin's precincts lie east of it. From the mean position of those 39 sites, site 2 lies 181 m at 168°, which agrees with the report's words. The procedure eliminated every candidate and answered "none". Coding site 2 from the report's words instead gives the right answer.

## What missing information does

`ablate.py` restores each subset of removed information in every case. It also removes one or two pieces of information from the five cases whose full form selects the true feature (001, 004, 009, 011, 012).

**One restored observation.**

- Case 005: restoring the rival's date (L) restores selection. Restoring the instruction's direction does not, because the rival is also east of the farm.
- Case 009: neither single restoration is enough. The instruction's direction and the rival's distance are both needed.
- Case 002: restoring the opening ("north") does not help. Sites 21 and 22 lie 70 m and 58 m from the wall. Both fall inside the 48–72 m band of 120 cubits. A cubit range of 0.40–0.60 m cannot separate features about 12 m apart at this distance.
- Case 003: putting the true tomb back gives "insufficient", because two tombs then fit.
- Case 006: putting the true tower back restores selection.
- Cases 008 and 010: nothing was removed on purpose, and the report holds nothing that restores selection. In case 010 the report says cave 4 is not marked on its map. Coding cave 4 from its printed map reference instead (233°, 763 m) gives a wrong "none".

**Removing information from the five decidable cases** (selection survives in n of 5):

| Removed | Survives |
|---|---|
| instruction's direction | 3 |
| instruction's distance (1 km default applies) | 1 |
| instruction's opening | 4 |
| all dates set to U | 4 |
| true feature's bearing | 0 |
| true feature's distance | 1 |
| true feature left out (correct answer "none") | 5 |
| true feature left out, and instruction's direction removed | 3 (2 false selections) |
| true feature left out, and instruction's distance removed | 1 (1 false selection) |
| true feature left out, and all dates U | 4 (1 false selection) |

In these cases the stated distance does most of the work. A missing bearing on the true feature always prevents selection, as the rules intend. A missing distance does too, except for a words position under the default limit (case 011). Leaving the true feature out is safe when the instruction is complete. It becomes dangerous when the instruction has also lost a direction, a distance or a date: then a rival can pass every test.

## Limits

- **This is not an independent test.** The same model family chose the sources, wrote the instructions, coded the candidates, wrote the keys and wrote the procedure. The cases were built knowing the rules. Only the sealed reserved batch, run once, is the test.
- The procedure was written before the cases. After the first development run, one parser rule was added: a depth such as "dig three cubits" is not read as a distance. No development instruction contains a depth, so no output changed. An ablation hook and the code hashes were also added.
- Most instructions were written from the same map references that place the candidates. They test the logic and the abstentions. Only cases 007, 010 and 011 use the source's own words against its own records.
- The cases are not independent of each other. Cases 001–003, 004–006, 007–008, 009 and 012, and 010–011 share sites and candidates.
- All five sources are short HA-ESI survey reports. Two are by one author. Excavation sections, plans and dated stratigraphy are not tested.
- The parser knows a short word list. A reserved case written in other words may be misread. The `reasons` field shows the parsed instruction, so a misreading can be found after the run. It must not be fixed and rerun on the same reserved cases.
- The key conventions for "none" and "insufficient" are this worker's reading of the schema. Case 003 shows where they meet.

## Access notes

- `https://www.ascsa.edu.gr/` (Athenian Agora picture books, considered as a source): curl failed with "SSL certificate problem: unable to get local issuer certificate". Not used.
- `https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/oip32.pdf` (Lamon 1935, *The Megiddo Water System*): returned an HTML page, not the PDF. Not used.
- HA-ESI pages carry a notice that the journal is moving to `https://publications.iaa.org.il`. The report URLs above may change.
