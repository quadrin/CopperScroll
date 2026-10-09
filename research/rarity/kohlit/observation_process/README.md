# Observation-process audit of the Koḥlit rarity count

**Status: exploratory.** This audit was written on 8 October 2026 UTC, after the registered result and both addenda were seen. Its scope rules are therefore a new exploratory model, not a correction of the registered test (AGENTS.md). It changes no registered number. `stage2/match.py` is imported and never changed.

## Why this audit

- In the [source-2 addendum](../stage2/addendum_s2/ADDENDUM.md), f rose from 1 to 20 (31 in the pre-70 set).
- Every new FAIL rests on one data-block field in a Zertal entry, "Cisterns: none", plus the lack of any other recorded pit that could qualify.
- Condition C2 needs a pit within 1 km to the north. The field describes the site. Nobody reports searching the northern sector.
- The first run's only FAIL (Kh. ʿAṭuf, S676) rests on one SWP sentence, "no tombs were found".
- An unsuccessful search is evidence only for the area and the feature class that it could have detected. The Air France 447 wreck was found after analysts modelled what each earlier, unsuccessful search could have detected (Stone et al. 2014, *Statistical Science* 29: 69–80). This audit applies the same idea to the count.

## What each survey tested

Details and page references are in [`surveys.csv`](surveys.csv). One row covers each source type used in the count.

- **WBADB rows (source 1).** WBADB compiles other surveys; it did no fieldwork of its own. Its component field lists only the "principal discoveries" (sourcebook p. 17). Isolated features are handled inconsistently (p. 14). The format cannot state an absence.
- **Highlands of Many Cultures (source 2, 48 units).** The team walked about 70% of the grid on foot (p. 11) and collected pottery over each site (p. 13). Steep rocky slopes got less attention (p. 13). Cisterns and tombs were recorded only in relation to central sites; isolated ones went to unpublished lists (p. 12). An entry has no cistern or tomb field. Its silence says nothing about cisterns or tombs.
- **Zertal, Vols. II–IV (source 2, 78 units).** The survey claims full coverage on foot (Vol. II p. 7). It records sites and features separately (p. 7). Each site entry starts with a data block. Item 11 of the block is the number of cistern openings (p. 8), and the area is the ground on which the structures stood (p. 8). Features outside sites appear in a "partial list" in Vol. II (pp. 772–782) and a list in Vol. III (pp. 565–571). Vol. IV publishes no feature list.
- **SWP Memoirs (source 3, 91 units).** The officers fixed points by triangulation and sketched the detail on horseback, over 50–660 square miles a month (Mem I pp. 29–31). Each sheet's Section B describes the ancient remains at named places (Mem I p. 41). Entries are free text with no search radius.
- **First excavation publications (source 4, 25 units).** A report covers its excavated areas. How far it reflects the whole site "cannot be simply assumed" (WBADB sourcebook p. 19). No absence statement was coded.
- **Nigro 2011 (source 5, 10 units).** This is a catalogue that compiles earlier sources and checks them in the field (p. v). No absence statement was coded.

## What the absence statements cover

[`absences.csv`](absences.csv) lists all 63 explicit absence statements in the merged sheets: 51 by coder A and 12 by coder B.

- **61 are the Zertal field "Cisterns: none".** The field counts cistern openings within the site record. The scope is therefore the site only. This is an inference from Zertal's method text (Vol. II pp. 7–8); no entry says it in words.
- **The class is narrower than C2.** The field names cisterns. C2 also counts caves, silos, shafts, pits, tunnels and underground chambers.
- **The area is small.** For the 31 units that FAIL, the site areas run from 0.5 to 34 dunams (median 3 dunams). If a site is a disc centred on the unit point, a quarter of it lies in the northern sector. Then a site record covers at most 1.1% of the sector (S829), and usually about 0.1%.
- **2 are the SWP sentence on Kh. ʿAṭuf (S676).** It covers the ruin and what the officers saw around it. It names tombs only; C3 also counts cist, pit and trench graves. The sentence is on printed Mem II p. 236; the coded "p. 30" is the packet's OCR page. The site area in the table comes from Zertal's entry for the same site (Vol. II Site 131).
- **None states a radius. None reaches the 1 km northern sector.**

## Re-evaluation under scope rules (exploratory)

**Rules.**
1. An absence statement counts toward FAIL only inside the area and the feature class that it covers.
2. Outside that scope the condition stays UNKNOWN, unless a source records a search of that area and publishes what it found there.
3. A statement reaches the C2 or C3 target only if it covers the whole 1 km northern sector and names the whole feature class.

`observation.py rescope` drops every absence statement that does not reach the target and runs `match.py` again. It also re-runs the registered sheets and stops unless they reproduce the committed addendum result.

**Result (R1; with Nigro; R2 has no FAIL and does not change).**

| Set | Branch | Registered k / f / m | Scope rules k / f / m |
|---|---|---|---|
| R1 main | A survey (headline) | 0 / 20 / 313 | 0 / 0 / 333 |
| R1 main | A text | 0 / 19 / 314 | 0 / 0 / 333 |
| R1 main | B | 5 / 19 / 309 | 5 / 0 / 328 |
| R1 pre-70 | A survey | 0 / 31 / 468 | 0 / 0 / 499 |
| R1 pre-70 | A text | 0 / 30 / 469 | 0 / 0 / 499 |
| R1 pre-70 | B | 6 / 30 / 463 | 6 / 0 / 493 |

- **f falls to 0 in every row and every variant.** k does not change, because the rules cannot create a match. m rises by the old f.
- **All the new m units are under a full-coverage survey.** In the headline row, m under full coverage rises from 248 to 268.
- **Which units move (primary rules).** All 31 units that FAIL become UNKNOWN. In the main set these are S676 (C3) and 19 C2 units: S241, S447, S493, S701, S790, S791, S1003, S1031, S1060, S1080, S1173, S1334, S1336, S1346, S1382, S1390, S1443, S1457 and S1474. In the pre-70 set only, 11 more move: S386, S418, S432, S458, S695, S770, S829, S841, S1296, S1319 and S1485.
- **Variants.** In the dated-only variant, 50 units FAIL under the registered rules and none under the scope rules. The other 19 are Zertal units whose undated pits stop a FAIL in the primary run. [`results/moved_units.csv`](results/moved_units.csv) lists every unit and variant. [`results/comparison.csv`](results/comparison.csv) gives every row of every table.

## Did the same surveys record pits in those sectors?

Rule 2 asks whether any source searched the sector. So Zertal's own volumes were read beyond the packets for the 30 Zertal units that FAIL on C2. Two kinds of record were checked: the data blocks of every neighbouring site, and the feature lists. Each record used was checked by eye against the page.

- **el-Khelayel (S695, pre-70 only).** Vol. II Index 3 (p. 774) lists three cisterns "on a northern slope of Jebel Tammun". They lie 854–985 m away, at bearings from 336° to 21°.
- **Kh. Tawil 3 (S1296, pre-70 only).** The neighbouring sites Kh. Tawil (1) and (2) each have "Cisterns: 2" (Vol. IV pp. 425 and 429). Both are WBADB rows in the packet, 447 m and 608 m to the north. Their WBADB components do not mention cisterns.
- **ʿIraq el-Mardom (S386, pre-70 only).** Kh. Mhallal, 200 m due north, has "Cisterns: 2" (Vol. II p. 261). At 100 m precision this bearing is not valid, so the cisterns could lie in the sector.
- **No other record.** For the other 27 units, no neighbouring site's "Cisterns" field and no listed feature puts a pit in the sector. The full descriptions of neighbouring sites were not read. Vol. IV has no feature list, so for its 18 units the sector's only published record is the entries of neighbouring sites.

[`sector_records.csv`](sector_records.csv) holds these six records. Under the registered rules plus these records, S695 and S1296 change from C2 FAIL to MATCH, and S386 from FAIL to UNKNOWN. In the pre-70 set, f falls from 31 to 28 (branch A survey) and from 30 to 27 (A text and B). The main set does not change. No unit becomes a branch match.

So for 3 of the 30 units, Zertal's own published record already contradicts or undercuts the FAIL. The packets held only the unit's own entry, and WBADB does not list these cisterns.

## Recommended rule for any future count

1. Record, for each absence statement, the search unit, the area it covers and the feature class it names. Take them from the survey's own methods chapter.
2. Count a FAIL only when the covered area contains the condition's whole target area and the named class contains the whole condition class. Otherwise record UNKNOWN.
3. Read a data-block field, such as "Cisterns: none", as a statement about the site record only, never about its surroundings.
4. Before any FAIL, read the same survey's other records for the target area: the entries of neighbouring sites and any feature list.
5. Credit a survey's coverage claim only for what it published. A partial feature list cannot support an absence.
6. Report f split by statement form, with the share of the target area that the statements cover.

## Limits

- The scope classes are inferences from the methods chapters. No entry states its own search area.
- The share of the sector assumes a round site centred on the unit point.
- The sector check used only Zertal's volumes. Zertal Vol. I was not supplied, so 14 Stage 2 units stay "not accessed" for source 2.
- For S676 (C3), the Vol. II feature list shows no grave within 1 km to the north. The other sources for its sector were already in the packet.
- Grid references in the Vol. IV text layer have OCR errors. Each record used was read on the page, but a misread grid could hide another record.
- Nothing here identifies a site or bears on the treasure.

## Files and how to run

| File | What it is |
|---|---|
| `surveys.csv` | One row per source type: what it sought, how it searched, its search unit, how it recorded features and what its absences can cover |
| `absences.csv` | Every explicit absence statement, with its scope and the registered value (written by `observation.py absences`) |
| `sector_records.csv` | Six pit records for the sector from Zertal's own volumes, outside the packets (hand-checked) |
| `observation.py` | `absences` and `rescope` commands; imports `stage2/match.py` |
| `merge_sheets.sh` | Rebuilds the merged coder sheets of the source-2 addendum, without matching |
| `test_observation_process.py` | Unit tests on synthetic data, and checks of the committed tables |
| `results/` | `comparison.csv`, `moved_units.csv`, `summary.json` |

```
sh merge_sheets.sh PACKETS_DIR MERGED_DIR
python3 -I observation.py absences PACKETS_DIR MERGED_DIR/A MERGED_DIR/B absences.csv
python3 -I observation.py rescope PACKETS_DIR MERGED_DIR/A MERGED_DIR/B results
python3 -I test_observation_process.py
```

PACKETS_DIR is packet v4, as for `stage2/addendum_s2/run_addendum.sh`. Packets are not in the repo, because they hold third-party text.

**Sources read for this audit.** WBADB sourcebook pp. 11–28; *Highlands* Vol. I pp. 11–22; Zertal Vol. II pp. 1–9, 261 and 772–782, Vol. III pp. 1–2 and 565–571, Vol. IV pp. 1–4, 425 and 429; SWP Memoirs I pp. 29–31, 37–39 and 41 (<https://archive.org/details/surveyofwesternp01conduoft>, OCR text, opened without error) and II p. 236; Nigro 2011 pp. iii–vi, 3 and 95. No link failed.
