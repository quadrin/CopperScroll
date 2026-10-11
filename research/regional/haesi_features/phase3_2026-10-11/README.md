# HA-ESI phase 3: the downloaded portal volumes and the rest of the online Jerusalem tier

**What it is.** The rest of the IAA excavation-report inventory, read on 11 October 2026 under the phase-2 frozen plan, unchanged, with the scope frozen in [PLAN.md](PLAN.md) (commit 4d8325e). Four parts: HA 1961–1979 (A), HA 1980–1998 (B), ESI and HA-ESI volumes (C), online Jerusalem reports, tier T3 positions 81–662 (D).
**Main result.** 1,260 more reports coded and 2,582 feature rows in the region, 628 of them dated by the report to the window (Hasmonean to 135 CE). Every heading of all 101 downloaded volumes was screened, and every in-region report was read except two whose pages are missing from the portal copies. All 684 phase-1 screen candidates in these volumes are accounted for, and the online Jerusalem tier is finished.
**What stays unknown.** Rows are per report and class: repeated seasons at one site, and Hebrew and English versions of the same report (parts B and C), are not yet deduplicated, so these are not counts of features on the ground. Most rows are undated or only partly dated. Held cave reports (plan §7) were cited only. No count of the inventory changes a registered outcome.

All exploratory. No identification claim.

## Totals (`python3 -I summarize_phase3.py` → [summary_phase3.json](summary_phase3.json))

| Part | Reports coded | Feature rows in region | yes / no / unknown |
|---|---|---|---|
| A, HA 1961–1979 (50 volumes) | 251 | 364 | 152 / 91 / 121 |
| B, HA 1980–1998 (32 volumes) | 179 | 473 | 115 / 188 / 170 |
| C, ESI 1, 4, 10–20 and HA-ESI 109–115 (19 volumes) | 248 | 579 | 135 / 222 / 222 |
| D, online T3, positions 81–662 | 582 | 1,166 | 226 / 365 / 575 |
| **All** | **1,260** | **2,582** | **628 / 866 / 1,088** |

By class (rows): rock-cut installations 641, tombs 544, channels and aqueducts 425, cisterns 403, caves 229, pools and reservoirs 145, ritual baths 105, columbaria 36, hoards 34, dams 20.
By zone: Jerusalem hills (Z4) 2,375; Judean Desert (Z3) 128; Jordan Valley (Z2) 62; Gerizim (Z1) 17. The desert and valley zones remain thin because few reports exist there, not because they were skipped.

With phases 1 and 2 (73 and 274 reports), the IAA inventory now holds about 1,600 reports. What remains of the IAA journals is listed under "Not read".

## Protected and held material

- **HA 28–29 (Tier 1)** was extracted first, alone (commit aa17f58), by a reader who did not open any prediction: [part_a/tier1_HA28-29_extraction.md](part_a/tier1_HA28-29_extraction.md). **Kh. ʿAlmit** extractions: [part_b](part_b/tier1_kh_almit_extraction.md) (HA 88 pp. 18–19), [part_c](part_c/tier1_kh_almit_extraction.md) (HA-ESI 115), and two passing mentions in HA 26 ([part_a](part_a/tier1_kh_almit_extraction.md)). No arrival-register item file exists for either record (the arrival README's step 5, registering them before reading, was never done), so there are no registered outcomes to score. Any comparison with the Koḥlit chain models would be exploratory. Part A's HA 26 coding row named "Almit" before its extraction was committed (ordering deviation; no feature was coded from it).
- **Held cave reports** (Qumran cliffs and marl terrace, Jericho escarpment, Wadi Qelt gorge): cited with first lines only. Part B: HA90-039-1, HA93-065-2, HA99-045-2, HA100-055-1, HA104-080-1, HA106-129-1. Part C: ESI 13 p. 64 (Qumran Caves, Patrich). Part A: the HA 26 caves sub-section (item 7.1). Part B saw a few extra lines of four held reports while locating headings; none used (line ranges in [part_b/NOTES.md](part_b/NOTES.md)).
- **Tell es-Sultan north strip:** HA103-061-1 and HA 43 item 21 cited only; no row has `protected_strip = yes`. Part A displayed the four-line HA 43 notice in full before applying the strip check.

## Not read

- Pages missing from the portal copies: HA 94 pp. 38–39 (Mt. Ebal 1989, Z1); ESI 14 pp. 90–91 (Giv'at Shapira; et-Tur read from its last page only).
- About 30 image-only pages in part A (apparently plates, including possible survey maps in HA 26) and HA 41–42 p. 49.
- Two online "Extended report" PDFs (HAESI-25804, HAESI-26431) were coded from their online summaries only.
- HA 44 is not in the portal list.
- Edge cases left for a decision: Ein Arub (on the Z4 south edge, HA 27 and HA 48–49), Jabaʿit (ESI 1 p. 43, no map reference, possibly Z3), Kh. Hadatha (HA 6, excluded as el-Haditha near Lod: to check).

## Files

[PLAN.md](PLAN.md) · [partition.csv](partition.csv) · `part_a/`, `part_b/`, `part_c/`, `part_d_online/` (each: `reports.csv`, `features.csv` in the phase-2 column order, `screen.csv`, `candidates_checkoff.csv` for A–C, `NOTES.md`, scripts, tests) · [summarize_phase3.py](summarize_phase3.py), [summary_phase3.json](summary_phase3.json).

Working copies left on the owner's computer (not in the repository; safe to delete): `~/Downloads/IAA portal volumes/_derived_text_partB/` (part B's extracted text) and `~/Downloads/IAA portal volumes/_part_c_screen_tables/` (part C's transfer tables).

## Proposed, not applied

- Deduplicate by field campaign and across Hebrew/English versions before using any count (part B lists three to check against ESI 15).
- Add the held cave reports to the arrival register; decide Ein Arub, Jabaʿit and Kh. Hadatha.
- Archive the HA 26 plate pages if they are survey maps and the owner permits.
