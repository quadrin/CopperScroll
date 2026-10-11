# Columbaria (dovecotes) in Judea, scored against entries 38 and 44

**What it is.** An inventory of every recorded columbarium (dovecote) found in the ASI online survey, the West Bank Archaeological Database and a bounded set of publications for Judea, with each one scored against the "dovecote" reading of entries 38 (IX 1–3) and 44 (IX 17–X 2). It bears only on that reading.\
**Main result.** 179 counted rows (at least 269 columbaria). Entry 38: no recorded columbarium lies within 2 km of ʿAin en-Naṭuf or Kh. Badd Faluh (Netophah); the nearest is 5.5 km away. Entry 44 (Puech's reading): only Masada's three columbarium towers meet every clause, and only through Netzer's reconstruction and this worker's reading of his drawing. Under the text shown ("second upper storey", three levels) no columbarium meets every clause.\
**What stays unknown.** Most clauses are silent in the records: storeys for 174 of 179 rows, access for 156, date for 160. 36 of the 58 ASI sheets that touch the region are not online, including Beth Guvrin–Maresha and Hebron. The first publications of the Masada towers, Zissu's dovecote study and Kloner's Maresha report were not read.

Exploratory, 11 October 2026 (UTC). No identification claim. No registered result, outcome count or closed test changes. Labels: EVIDENCE (the source says it), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record).

## Freeze record

- `PLAN.md` SHA-256: `425021ad165163710ce3ab1bbadb5f2dfb998749abdbade4e9085bbd1334f906`.
- Frozen in commit `afdd69f` ("Freeze columbaria plan"), 2026-10-11T04:06:45Z, before any feature record was screened, read or coded. Exposure before the freeze is listed in PLAN §10. Only the ASI map list, the sheet grid and the WBADB field names had been fetched.
- `PLAN_AMENDMENT_1.md` SHA-256: `3009c7b1bb512330fe8049c1bdab0fa7b9eb1cd28b5b79cdbedf15893894ca6b`. It was written after the records were seen, so it is exploratory. It adds one source (Netzer's Jericho final report) and states nine coding rules that were decided while coding. The frozen plan is unchanged.
- No second coder was available in this lane. Every MATCH on a distinctive clause is listed below for checking. Four rows carry `check_flag = yes`.

## The text: what the inventory can and cannot test

The inventory bears only on the **dovecote** sense of שובך. Readings are edition-based.

- **Entry 38.** Nine named readers take שובך as a dovecote: Puech 2015 (pp. 75–77), Høgenhaven, Luria, Pixner, Beyer, Wolters, Vermes, Wise, García Martínez and Tigchelaar. Five do not: Milik 1962 (an opening in a cave or rock face; dovecote as his alternative), Lefkovits (a tower), Allegro 1960 (a "gutter (?)" at the bottom of a rain-water tank), Schiffman (a drain) and Thorion (a lattice). Of the four editions this project relies on, only Puech reads dovecote as his main sense (Lefkovits pp. 273–275; Puech p. 76 n. 318).
- **Entry 44.** Eight named readers take a dovecote: Puech (p. 86, "in the dovecote which is in Maṣadona/small fortress"), Beyer, Luria, Pixner, Wolters, García Martínez, Vermes and Wise. Three do not: Lefkovits (a tower at the Fort of Nobah), Milik (a man-hole in the aqueduct of ha-Masad) and Allegro (a gutter or sluice in the Stronghold of Senaah) (Lefkovits pp. 317–318).
- The place of entry 38 has three located branches: N1 ʿAin en-Naṭuf (Milik, Puech, Beyer), N2 Netophah at Kh. Badd Faluh (Lefkovits p. 275, after Avi-Yonah), and Lefkovits's Beth Netophah in Lower Galilee (outside the region, not scored). Allegro and Luria read הנטף as a rain-water tank or duct; that branch (N0) has no place clause.
- Entry 44 has two storey branches: the text shown, "in the second upper storey" (at least three levels), and Puech, "on the second level as one descends from the top" (at least two levels). Nobah and Oboth lie east of the Jordan in their authors' own glosses. Masada carries a dovecote only in Vermes ("at Mesad").

## Sources and access

| Source | What was read | Status |
|---|---|---|
| S1 ASI online (survey.iaa.org.il) | English and Hebrew GeoJSON of all 22 online maps that touch the region; 107 full site records with a columbarium word | Read. 153 responses in `data/asi_manifest.csv`, with SHA-256. No printed page numbers online. |
| S2 WBADB `WBADB_data1.xlsx` | All rows screened; 62 in-region hits read | Read. SHA-256 `3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b`. Not committed. |
| L5 Netzer 2001, *The Palaces of the Hasmoneans and Herod the Great* (owner's copy) | pp. 14, 44, 73, 82 (Fig. 100), 125, 127 | Read; page images of pp. 14 and 82 viewed |
| Netzer 2001, *Hasmonean and Herodian Palaces at Jericho, Final Reports I* (owner's copy) | pp. 2, 28, 91–92, 303, 335 | Read after the freeze (amendment 1) |
| L7 Kloner and Zissu 2013, *Opera Ipogea* 2, pp. 45–62 | sentences on columbaria, pp. 47–48, 52–54, 56, 61 | Read through WebFetch's text extraction only (direct download: HTTP 403) |
| L6 Avni, Dahari and Kloner 2008, ch. 4 (owner's extract) | pp. 119–120 | Read; no columbarium |
| S4 repository extractions | `tables/phase5_assessments.csv` JER 46; Koḥlit Stage 2 coded files; HA-ESI features | Read; the Koḥlit files only repeat WBADB rows; HA-ESI has no columbarium row |
| Puech 2015, Lefkovits 2000 (owner's copies) | entry pages listed above | Read for the text branches, before the freeze |

Text-span hashes and file hashes are in `data/sources_read.csv`. No PDF, page image or full text is stored in the repository.

**Not read.** Zissu 1995; Kloner and Hess 1985; Kloner 2003; Tepper 1986; Netzer 1991 (*Masada III*); Netzer 2006 (the owner's copy has no text layer; OCR was not run); Batz 2006b on the columbarium tower near Hebron; HA-ESI online reports (closed to robots). By rule: ʿAtiqot 41 cave entries and the other Tier 1 records, Kochavi 1972, the L-656 file and the IAA Archive cave records. The ASI survey record of Kh. ʿAlmit (102/579) was read in the screen, after the freeze, and is flagged `tier1_related`; the IAA notices on Kh. ʿAlmit (Tier 1) were not read.

## Method

1. **Region.** The polygon (34.85, 31.90), (35.55, 31.90), (35.45, 31.30), (34.75, 31.30), longitude/latitude in WGS 84 (EPSG:4326). It covers the Judean hills from north of Jerusalem to the Yattir–Eshtemoa line, the Shephelah, the Judean Desert and the Herodian fortresses west of the Jordan and the Dead Sea.
2. **Screen.** Frozen regular expressions (PLAN Appendix A, copied in `scripts/terms.json`) for columbarium, dovecote and pigeon-house in English, and קולומבריום, שובך and "מגדל/מערת יונים" in Hebrew. The ASI screen covered names, descriptions and finds; the WBADB screen covered names and components.
3. **Rows.** One row per columbarium that the source describes separately. A record with an undistinguished plural gives one row with `n_columbaria` empty. The same columbarium in a second source is kept with `dup_of` and not counted. 229 rows; 179 counted (ASI 154, WBADB 16, literature 9); 50 duplicates; 6 records excluded (`data/excluded.csv`).
4. **Coding.** Every candidate record was read in full, and each clause was coded from the record's own words. Silence is UNKNOWN, never FAIL. Points are the record's site point, with 100 m precision assumed for ASI and WBADB.
5. **Scoring.** `scripts/score.py` applies PLAN §2 and §7: survey level (points, and a fort named at the same site) and text level (the source's own placement). Scope `frozen` uses the frozen sources only; scope `all` also applies the amendment's source.

## Results

Counts are "k match, f fail, m unknown, of N" by counted row, scope `frozen`. The scope `all` changes only entry 38 N0 (16 instead of 17 dated in the window), because the Jericho final report calls the round tower's date indeterminable.

### Entry 38, dovecote branch

| Branch | Level | Result |
|---|---|---|
| N1 ʿAin en-Naṭuf, within 1 km | survey | 0 match, 179 fail, 0 unknown, of 179 |
| N1, within 1 km | text | 0 match, 179 fail, 0 unknown, of 179 |
| N2 Kh. Badd Faluh, within 1 km | survey and text | 0 match, 179 fail, 0 unknown, of 179 |
| N1 or N2, within 2 km | survey | 0 match, 179 fail, 0 unknown, of 179 |
| N0 (no place; dated in the window only) | survey | 17 match, 2 fail, 160 unknown, of 179 |

- The nearest recorded columbarium is WBADB S4114, Kh. Umm el-ʿAṣafir: 8.2 km from N1 and 5.5 km from N2.
- EVIDENCE: the ASI Map of Herodium (108/2), which holds both N1 and N2, has no record with a columbarium word in either language. Neither do the Judean Desert sheets (109/4, 109/5, 109/7) or ʿEin Gedi (147).
- INFERENCE: a FAIL here means that no *recorded* columbarium lies near the spring or Kh. Badd Faluh. It does not show that none exists. Hirschfeld's introduction says he investigated only "some of the many caves" (ASI Jerusalem lane, coverage statements), and no detection rate is known.

### Entry 44, dovecote branch

| Branch | Level | Result |
|---|---|---|
| Puech: fort, south of Jerusalem (S-A), at least two levels, way down from above, dated | survey | 3 match, 55 fail, 121 unknown, of 179 |
| Puech, same clauses | text | 3 match, 59 fail, 117 unknown, of 179 |
| Text shown: as above, with at least three levels | survey | 0 match, 57 fail, 122 unknown, of 179 |
| Text shown, same clauses | text | 0 match, 61 fail, 118 unknown, of 179 |
| Puech with "the south" as the south side of the fort (S-C) | text | 0 match, 45 fail, 134 unknown, of 179 |
| Puech with S-B1 (south of 31.62 N) / S-B2 (south of Hebron, 31.53 N) | text | 3 / 3 match; 74 / 159 fail; 102 / 17 unknown, of 179 |
| Puech with a tower counted as a fort (F+) | text | 3 match, 59 fail, 117 unknown, of 179 |
| Masada named (Vermes's "Mesad") | text | 3 match, 176 fail, 0 unknown, of 179 |

The three matches are Masada's two square and one round columbarium towers (`L-MASADA-SQ1`, `-SQ2`, `-RD`). What each clause rests on:
- **In the fortress.** EVIDENCE: "three on top of Masada" (Netzer, *Palaces* p. 127).
- **Two levels.** Published reconstruction, Fig. 100 (p. 82). The round tower's setup "was apparently similar" (CLAIM). Netzer also writes "We assume" these towers had a dovecote on the ground floor and a watchtower above (p. 14).
- **Way down from above.** INFERENCE from the Fig. 100 drawing: no ground-floor door, an outside ladder to an upper door, and openings between levels. For the round tower this is by analogy only. Flagged for checking.
- **Dated.** Netzer's "first phase (or, theoretically, even ... the Hasmoneans)" (p. 82).
- **The south.** The two square towers stand "at the western edge of Masada", so they fail S-C. The round tower's place on the summit is not given in the pages read.
- **Which level the dovecote occupies.** In the reconstruction the dovecote is the lower of two storeys. That is the second level counted from the top (Puech) only if the roof is not counted. It is not an "upper storey" (text shown).
- Masada was exposed before the freeze (PLAN §10).

### Per-clause tallies (scope `frozen`, counted rows)

| Clause | Match | Fail | Unknown |
|---|---|---|---|
| Inside a fortress, text level | 3 (Masada) | 36 | 140 |
| Fort named at the same site, survey level | 20 | 32 | 127 |
| Fort or tower (F+), text level | 6 (Masada 3, Cypros, Jericho round tower, WBADB S5978 tower near Hebron) | 37 | 136 |
| Two or more storeys or levels (L2) | 5 (Masada 3, Cypros, Jericho round tower; all reconstruction or CLAIM) | 0 | 174 |
| Three or more (L3) | 0 | 2 | 177 |
| Way down from above | 23 | 0 | 156 |
| South of Jerusalem (S-A) / south of 31.62 N / south of 31.53 N | 139 / 120 / 27 | 39 / 59 / 151 | 1 / 0 / 1 |
| South side of a fort or site (S-C) | 3 | 8 | 168 |
| Near a Netophah candidate (N1 or N2, 1 km or 2 km) | 0 | 179 | 0 |
| Dated in the window (D) | 17 | 2 | 160 |

- **Dated in the window (17).** Eight Jerusalem-area columbaria dated in the survey of Jerusalem (102/81, 140, 166, 211, 216, 234, 307, 472) and Kh. Kakul (102/131); Ramat Raḥel (106/95, through the INJ 17 note); Deir Tantur (WBADB E785); the Jericho round and square towers, Cypros, and the three Masada towers. None of the nine on Map 102 lies in a fort or has a recorded second level.
- **Way down from above (23).** Ceiling openings or "upper openings" (102/241, 102/549, Kh. ʿAlmit 102/579, 109/326b, 109/341, 109/368), shafts (102/131, 120/68), steps down into pits, cisterns and caves (109/24d, 109/70b, 109/194b, 109/210c, 109/349, 98/132, 98/169, 98/289, 98/327), Maresha's staircases (three rows) and the Masada towers.
- **Forts with columbaria outside them.** Ḥ. Ṭura (104/9), H. Qazra (109/326, 100 m south of the fortress) and Idna (109/220). These fail the text-level fort clause.
- **Columbarium towers.** Masada (3), Jericho west of the royal estate, Jericho square structure (Herodian), Cypros, and a tower in WBADB S5978/E978 (Batz, south Hebron hills; not dated, first publication not read). Horvat Abu Haf (Zissu 1995) is unplaced.
- **Niche counts** are given for 49 rows, from 10 to 2,000 (Maresha SC 30).

### Where the exposed sites land

- **Masada.** The only matches for entry 44 (Puech).
- **Maresha** (Kloner and Zissu 2013). 85 lower-city columbaria, "accessed by staircases"; 3rd–2nd centuries BCE (partly in the window); a walled lower city, not a fort; levels not stated. SC 30 went out of use as a columbarium early in the 2nd century BCE (FAIL on date).
- **Ramat Raḥel** (106/95). A fort and a Roman camp are recorded at the site, and the columbarium is dated by the S4 note. Its levels, access and place relative to the fort are not recorded (UNKNOWN).
- **ʿAin en-Naṭuf.** No columbarium is recorded nearby (FAIL at 1 and 2 km).

## Blocked

- Zissu 1995, "Two Herodian Dovecotes: Horvat Abu Haf and Horvat ʿAleq", JRA Suppl. 14 pp. 56–69: <https://www.academia.edu/14951435> (download needs a sign-in). Record: <https://cris.biu.ac.il/en/publications/two-herodian-dovecotes-horvat-abu-haf-and-horvat-aleq/>. The Hebrew version is in *Qadmoniot* 29.2 (1996); no copy was found online.
- Kloner 2003, *Maresha Excavations Final Report I* (IAA Reports 17), pp. 42–45: publisher <https://www.israelexplorationsociety.com/he/product-page/iaa-reports-17-maresha-excavations-final-report-i-subterranean-complexes-21>; catalogue <https://zenon.dainst.org/Record/000071243> (bot wall).
- Kloner and Hess 1985, ʿAtiqot (ES) 17 pp. 122–133: no open copy found; library.
- Tepper 1986, "The Rise and Fall of Dove-Raising" (Hebrew), pp. 170–196: cited at <https://library.biblicalarchaeology.org/endnote/endnote-1-this-place-is-for-the-birds/>; library.
- Netzer 1991, *Masada III*: library or the Israel Exploration Society. It is the first publication of the Masada towers, and the decisive source for their levels and entrances.
- Kloner and Zissu 2013 PDF, direct download HTTP 403 from the cloud workspace: <https://www.operaipogea.it/wp-content/uploads/2013/12/5A-Maresha_2013_02-compresso.pdf> (read through WebFetch).
- HA-ESI online reports (Deir Tantur, HA-ESI 119; Gillo, 118; Ramot, 120; Kh. Kharuf, 116): <https://www.hadashot-esi.org.il> has robots.txt "Disallow: /".
- Wikidata API: rate-limited; Maresha was placed from <https://en.wikipedia.org/wiki/Maresha>.

## What the owner could do

- Supply Netzer 1991 (*Masada III*), the pages on the columbarium towers: plans, sections and entrances. Or OCR the Masada pages of the owner's Netzer 2006 PDF.
- Supply Zissu 1995 (academia.edu sign-in) and Batz 2006b pp. 58–61 (the columbarium tower near Hebron).
- Supply Kloner 2003 pp. 42–45 and Kloner and Hess 1985 for the levels and entrances of Maresha's columbaria.

## Files

| File | Holds |
|---|---|
| `PLAN.md` | The frozen plan (do not edit) |
| `PLAN_AMENDMENT_1.md` | Post-freeze source addition and coding rules (exploratory) |
| `columbaria.csv` | One row per columbarium (229; 179 counted): source and record id or page, name, point (EPSG:4326) with basis and precision, construction, levels, niches, setting, clause codes with their basis, site periods, date code, quote of 12 words or fewer, flags |
| `scores.csv` | Clause codes and branch verdicts per counted row, for scopes `frozen` and `all` |
| `summary.json` | All tallies: headline, per clause, every branch combination, both scopes |
| `data/coding.json` | The hand coding that `assemble.py` turns into `columbaria.csv` |
| `data/candidates_asi.csv`, `data/candidates_wbadb.csv` | Screen hits: ids, points, matched terms, flag words, text hashes (no text) |
| `data/excluded.csv` | Records excluded, with reasons |
| `data/asi_manifest.csv` | Every ASI response: URL, status, size, SHA-256, time |
| `data/sources_read.csv` | Literature and data sources, pages, file and text-span hashes, access |
| `scripts/` | `fetch_asi.py`, `build_inventory.py`, `asi_records.py` (reader for the coder), `assemble.py`, `score.py`, `colcommon.py`, `terms.json` |
| `tests/test_columbaria.py` | Plan hash, terms vs appendix, rules on synthetic cases, schema, quote length, reproduction of the tables |

## Run and test

From the repository root:

```
python3 -I research/regional/columbaria/scripts/fetch_asi.py CACHE              # map list, grid, GeoJSON
python3 -I research/regional/columbaria/scripts/fetch_asi.py CACHE --records    # full records of the hits
python3 -I research/regional/columbaria/scripts/build_inventory.py CACHE WBADB_data1.xlsx
python3 -I research/regional/columbaria/scripts/assemble.py
python3 -I research/regional/columbaria/scripts/score.py
ASI_CACHE=CACHE WBADB_XLSX=WBADB_data1.xlsx python3 -I -m unittest discover -s research/regional/columbaria/tests -v
```

Without the two environment variables, the screen-rebuild test is skipped and the other ten tests run. All eleven passed with the worker's cache (11 October).

## Proposed changes for the integrator

- **Entry 38 (atlas caution and the DN 38 row).** Add: "No recorded columbarium lies within 2 km of ʿAin en-Naṭuf or Kh. Badd Faluh in the ASI Map of Herodium (108/2) or WBADB; the nearest is 5.5 km away. This is survey silence, and detection is unmeasured (columbaria lane, 11 October)." No confidence change: the dovecote is one of several readings.
- **Entry 44 (DN 39-45 row).** Add: "Of 179 recorded columbaria in Judea, only Masada's three towers meet every clause of Puech's reading, and only through Netzer's reconstruction (*Palaces* p. 82, Fig. 100). Masada was exposed, the 'Mesad' reading with a dovecote is Vermes's alone, and Milik's Masada reading is not a dovecote reading. Nothing meets the text shown ('second upper storey')." Exploratory; no identification claim.
- **Backlog.** If any question tracks entries 38 or 44, link this README once. Before any confirmatory use of Masada, *Masada III* is the next record to obtain.
- **Lanes.** The IAA lane could check the hadashot-esi reports listed above (Deir Tantur, Gillo, Ramot, Kh. Kharuf) for levels and entrances.
