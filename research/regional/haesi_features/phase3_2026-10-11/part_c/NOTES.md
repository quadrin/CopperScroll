# HA-ESI phase 3, part C: ESI 1, 4, 10–14, 16–20 and HA-ESI 109–115

Worker notes for the integrator. Rules: phase-2 frozen plan (`../../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c08…b3be`) with amendments A1–A4, under the phase-3 scope freeze (`../PLAN.md`, SHA-256 `312c2733…5cf2`, commit 4d8325e). No plan of my own; nothing outside `part_c/` edited. Branch `worktree-agent-a95a974d36126c9cb`.

## Outcome

- **All 19 volumes screened in full** (1,900 screen rows: every contents row plus 24 sub-reports or items without their own contents row). **Every report in the region was read and coded**: 248 coded reports (247 in the region; one, ESI 19 p. 95 *Survey of Frankish Buildings*, has its report reference outside but its one eligible feature, at Lifta, inside). Nothing in the region is left as `not read (time limit)`.
- **579 feature rows in the region**: dated in the window yes 135, no 222, unknown 222. By zone: Z1 3, Z2 16, Z3 39, Z4 521. By class (yes/no/unknown): tombs 134 (50/49/35), rock-cut installations 121 (17/37/67), channels 99 (9/56/34), cisterns 95 (14/37/44), caves 48 (14/12/22), pools 35 (7/18/10), ritual baths 22 (18/1/3), columbaria 11 (3/3/5), hoards 9 (3/6/0), dams 5 (0/3/2). Full tables: `summary.md` (generated).
- **Phase-1 screen candidates in these volumes: 202, all accounted for** (`candidates_checkoff.csv`): read and coded 144, outside the region 53, not a field report 3, held 1, not read because the pages are missing from the copy 1.
- **Tier-1 record:** the IAA notice on Kh. ‘Almit (HA-ESI 115, English p. 48*, Hebrew pp. 63–66; B. Har-Even; permit L-857) was extracted to `tier1_kh_almit_extraction.md` and committed alone (`d431dfd`) before any other use; it was then coded (`HAESI115-048-khirbat-almit`, `tier1_record` note), as phase 2 did for ESI 5 p. 1. No arrival item, chain file or MANIFEST prediction was opened. No other volume mentions ‘Almit (text search of all 19 volumes for "Almit" and "עלמית").
- **Held:** ESI 13 p. 64, *Qumran Caves* (J. Patrich; map ref. 1935/1310): citation and first lines only (lines 3848–3852); not in `reports.csv` or `features.csv`. Read normally because outside the held stretch: ESI 13 p. 61 (caves of Wadi Murrar and ‘Ein Abu Mahmud, north of Wadi Qumran), ESI 18 p. 84 and ESI 20 p. 134 (Horbat Qumran: channel and aqueduct graffito, not caves). No Tell es-Sultan north-strip text was met. The L-656 field file and IAA Archive cave records were not sought.
- No report in these volumes was coded in phase 1 or phase 2 (checked against phase-1 `reports.csv`; phase 2 read other volumes), so no crosswalk is needed.

## Sources and access

| What | Where | Record |
|---|---|---|
| 19 portal PDFs | owner's Mac, `~/Downloads/IAA portal volumes/` (narrow filename filter; nothing else in the folder opened) | SHA-256 of each equals `../partition.csv`; `data/local_sources.csv` |
| Text | `pdftotext` 22.02.0 `-raw` (reading text) and `-layout` (contents only) on the Mac; the reading-order file (`<VOL>.ordered.txt`) puts HA-ESI 109–115 Hebrew pages first and the English pages (bound back to front) in reading order | hashes of raw, layout and ordered text in `data/local_sources.csv`; texts stay on the Mac, not in the repository |
| Coded spans | lines of `<VOL>.ordered.txt` | `data/local_spans.csv`: SHA-256 of each whitespace-collapsed span; all 249 records' quotes (≤ 12 words, verbatim) found by `scripts/verify_spans.py` |
| Screen tables | made on the Mac by `scripts/screen_volume.py` and `scripts/locate_headings.py` | `data/screen/` (contents rows, page index, every map reference with conversion, heading screen, orphan references) |

Side effect on the owner's computer: a transfer folder `~/Downloads/IAA portal volumes/_part_c_screen_tables/` (tool copies, the plan parameters, screen tables, coding tarballs and span checks; no extracted full text). It can be deleted. Extracted texts are in the session's scratch area on the Mac (`~/mnt/outputs/partc_esi/`), not in any connected folder.

## Method

1. **Screen.** `screen_volume.py` builds the reading-order text, a page index, every "map ref." (and נ״צ) with OIG EPSG:28191 / NIG EPSG:2039 conversion (phase-1 rules: digits → unit, northing > 400 km NIG, < 300 km OIG; a plausibility check rejects southern-grid and garbled references) and the contents rows. `locate_headings.py` finds each contents title in the body (two passes, title plus first author; ESI 1 and 4 use their capital-letter headings), takes the span to the next heading, and decides: map reference zoned; else the gazetteer with the A3 variants on the title. In-region map references outside any heading span were listed as orphans (none in the region remained unexplained).
2. **Overrides** (`data/screen_overrides.csv`, 21 rows, each with a reason): spans whose in-region reference belongs to a following item (Tel Harasim, Nahal Shemesh, Horbat Tittora, Horbat Ha-Tarsi, Neve Shalom, ESI 18 East Talpiyot); misread or misprinted references located by name (Tiv‘on out; Umm Leisun, Gallicantu 2000, Qiryat ‘Anavim survey and HA-ESI 115 Mount Scopus East in, Z4); author-name gazetteer hits (Na‘ama, Ein-Gedi); Be’er Sheva‘ "Ramot" and Bet Lehem of Galilee out; three Dead Sea Scrolls project or conservation items as not field reports; the held Qumran Caves item; ESI 14 p. 90 missing.
3. **Reading and coding** per phase-2 plan §5–§6 and A4, zones Z1–Z3 first in each volume, then Z4. One row per report and class (or per site or feature map reference). Conventions applied: association with a dated complex dates the feature; "Hellenistic" or "Roman" alone = unknown; Late Hellenistic, Early Roman, Hasmonean, Herodian, Second Temple = yes; fill sherds alone = unknown; hedged datings follow the named period (A4); typological datings stated by the report = yes; partial overlap with the window = unknown; baptismal fonts and bathhouse tubs not coded; oil-press caves as rock-cut installations; stepped pools as ritual baths only when the report says miqveh or the stair is the main access; the excavator's function words are kept in `feature_subtype`; features cited only from earlier work not coded.
4. **Build.** `scripts/build_part_c.py` (phase-1 `geo.py`, phase-2 `common.py`, unchanged) converts, zones and measures distances, links each coded report to its screen row, matches every phase-1 candidate to a screen row (title words, then page; 8 matches by hand in `data/candidate_overrides.csv`) and writes `reports.csv`, `features.csv` (phase-2 columns exactly), `screen.csv`, `candidates_checkoff.csv`, `summary.md`, `summary.json`. Deterministic; `tests/test_part_c.py` checks both plan hashes, that `d431dfd` contains only the Tier-1 file, the schema, every span and quote, that the build reproduces the committed outputs, that every in-region screen row has a coded report, and that all 202 candidates are accounted for.

## Deviations and exploratory choices (logged; no rule changed)

- **Exploratory screen additions** (titles not in the gazetteer, first lines place them in Z3/Z4; labelled `screen_note` in `reports.csv`): ESI 4 p. 21 Deir Mukallik (Nahal Og), ESI 4 p. 9 Bet Besai (southeast of Beit Sahur), ESI 12 p. 49 Wadi el-Qilt map survey (spelling variant of the gazetteer's "Wadi el-Qelt").
- **Headings located by hand**: 24 items without their own contents row (ESI 1 and 4 sub-reports under JERUSALEM, News in Brief items, ‘En Gedi in ESI 12, the Kh. ‘Almit notice) and 12 contents rows not found by the script; each is noted in `screen.csv`.
- **Hebrew read where the English pages are missing from the copy**: HA-ESI 110 English pp. 58–59 (Tell el-Ful, St. George Street, start of Et-Tur) and HA-ESI 113 English pp. 80–83 (end of Old City Walls, City of David, most of Ketef Hinnom). These records quote the Hebrew text verbatim from the extraction (bidirectional marks removed for matching; hashes are of the unaltered text).
- **Found late**: HA-ESI 115 p. 74* *Jerusalem, Mount Scopus (East)* (garbled reference zoned to the coast by the script) was caught by the phase-1 candidate check-off and coded (one cistern row). The check-off is the only cross-check on the script's zoning of garbled references; other garbled references with no region name in the title would not be caught.
- **Duplicates by design**: the Gihon rock-cut pool and Channel II recur in ESI 20 p. 99 and HA-ESI 109 p. 77*, 110 p. 63*, 114 p. 77*, 115 p. 51* (one feature, five rows, all dated no); Lower and Upper Aqueduct rows are different segments.

## Not read or limited

- ESI 14 printed pp. 90–91 are missing from the PDF copy: *Jerusalem, Giv‘at Shapira (French Hill)* not read; *Jerusalem, et-Tur* read from its last page only (no map reference).
- ESI 1 PDF p. 50 (printed p. 43) *Jaba‘it* (heading JABATT, line 1811; hiding complex with Herodian finds near Mevo Shiloh, no map reference): outside by the screen rule (no region name). It may lie at the northern edge of Z3; listed here for the integrator, not coded.
- The contents parser misses a few rows (for example HA-ESI 113 *Haifa, Ha-Qishon Harbor*); the orphan map-reference list is the safety net for items in the region with a reference.
- HA-ESI 109–115 Hebrew-only items were screened by their English contents; the Hebrew sections were read only where noted above.

## Proposed changes for the integrator

1. Merge `reports.csv` and `features.csv` into the phase-3 tables; zone counts for Z4 are not comparable as densities (part D samples online T3 separately).
2. Add the held ESI 13 p. 64 *Qumran Caves* (Patrich) to the arrival register's held cave items, with the phase-2 held list.
3. Record the Kh. ‘Almit notice in HA-ESI 115 (extraction `part_c/tier1_kh_almit_extraction.md`, commit `d431dfd`) for comparison under `research/preregistration/arrivals/ARRIVAL_PROCEDURE.md`.
4. Note ESI 14 pp. 90–91 as missing from the portal copy (a request for the printed pages would complete *Giv‘at Shapira*).
5. Decide whether ESI 1 printed p. 43 *Jaba‘it* belongs in Z3 (needs a location source).
6. Update `../../phase2_2026-10-10/portal_downloads_2026-10-11.csv` `read_status` for the 19 part-C files to "read (phase 3 part C)".
