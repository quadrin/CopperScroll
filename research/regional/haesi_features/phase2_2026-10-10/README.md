# HA-ESI phase 2: regional inventory of the scroll's feature kinds

**What it is.** An exploratory count, from the IAA's own excavation reports (HA, ESI, HA-ESI), of every reported cistern, pool, channel, dam, stepped pool, cave, tomb, columbarium, rock-cut installation and hoard in a fixed region (Gerizim–Shechem, the Jordan Valley from Phasaelis to the Dead Sea, the Judean Desert, and Jerusalem with the hills to Bethlehem and Herodium), whatever its distance to a proposed scroll place. No identification claim; no outcome or test changes.

**Main result.** __N_REPORTS__ reports read and coded (95 from ten local PDF volumes, __N_ONLINE__ online HA-ESI reports) give __N_ROWS__ feature rows in the region; __N_YES__ rows are dated by the report to the window (Hasmonean–135 CE), __N_NO__ only outside it, __N_UNK__ unknown. Tombs (__N_TOMB__), rock-cut installations (__N_ROCK__), caves (__N_CAVE__), channels (__N_CHAN__) and cisterns (__N_CIST__) dominate; most rows come from the Jerusalem hills (Z4, __N_Z4__) and the Judean Desert (Z3, __N_Z3__). The online title screen is complete (4,667 titles, 798 candidates); tiers T1 (desert, Jordan Valley, Gerizim) and T2 (Jerusalem hills outside the city) were read in full, T3 (titles beginning "Jerusalem,") only as a pseudo-random sample (__N_T3READ__ of 662).

**What stays unknown.** Every row is a row in the read corpus, not a count of features on the ground: several seasons can report one feature, and unread reports are silent, not empty. Not read: __N_T3UNREAD__ T3 Jerusalem reports, all portal-only volumes (HA 1–107, ESI 1–19 and HA-ESI 108–115 except the ten local copies; listed with exact PDF URLs in `portal_pdfs_needed.csv`), including the Tier-1 record HA 28–29, and the cave reports held for the arrival procedure. Region boxes are approximate (INFERENCE), so a few reports at the edges (Abu Ghosh west, ‘En Boqeq) fall just outside.

## Freeze record

- Plan: `PLAN.md`, committed alone as `d0f8c7c` ("Freeze HA-ESI phase 2 plan"), 2026-10-11T04:06:41Z (UTC).
- PLAN.md SHA-256: `5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be` (checked by `tests/test_phase2.py`).
- Changes after the freeze are in `AMENDMENTS.md` (A1–A3, exploratory) with one deviation (D1: two held-area cave passages read before the hold was checked; both now marked exposed). The frozen plan is not edited.
- Exposure: every report coded here was first read after the freeze (`exposure_at_freeze = unexposed at freeze`), except ESI 5 p. 110 (Wadi Nueima), which the repository had read before (`research/assessments/entry29_jericho_pools/`). Phase-1 reports are not re-coded (see `phase1_zone_crosswalk.csv`).
- Tier-1 records (arrival register, step 5): the Kh. ‘Almit notice in ESI 5 p. 1 was read after the freeze, extraction only (`ESI05-001-kh-almit`, `tier1_record` note in `reports.csv`); no chain file or arrival item was opened. HA 28–29 (Tananir) was not read (portal PDF not readable in the browser; see Blocked).

## Sources and access

| Source | Route | Coverage | Not read |
|---|---|---|---|
| ESI 2, 3, 5, 6, 7–8 (whole volumes); ESI 9 and 15 (items not read in phase 1); HA 40, 45, 59–60 (screened) | Owner's Mac, `~/Downloads` (narrow filter), `pdftotext -raw` on the Mac; text kept outside the repository; SHA-256 of each PDF and text file in `data/local_sources.csv`, of each coded span in `data/local_spans.csv` | Every report heading screened by map reference or name; every in-region report read and coded (95 records) | Held cave sections (below); HA 45 printed pp. 20–25 missing from the copy |
| HA-ESI online, volumes 116–137 (2004–2025) | Owner's Chrome, one tab, one page at a time, ≥3 s between loads, no downloads, no bot checks met | All 22 volume lists read and hashed (`data/online_lists.csv`, 4,667 titles in `data/online_titles.csv`); 798 candidates; T1 48 and T2 88 handled in full; T3 sample | T3 positions after the stop (`online_screen.csv`, status `not read (time limit)`) |
| IAA publications portal PDFs (HA, ESI, HA-ESI 1999–2003) | One PDF opened in Chrome as the plan's test; the viewer showed the cover but the page-text tool read no text | None | All portal-only volumes; listed with URLs, sizes and priority in `portal_pdfs_needed.csv` (111 rows: priority A 50, B 35, C 16, local copy 10) |

Every online report's main text (title block, body, references and captions as shown) was hashed in the browser (SHA-256 of the whitespace-collapsed text) and the hash is in `reports.csv` (`text_sha256`). Local spans are hashed the same way over the listed lines of the `pdftotext -raw` file. Quotes are 12 words or fewer and were checked against the local spans (all found) or copied from the page text.

## Method

1. Region, zones, classes, in-window rule, tiers and reading order were fixed in `PLAN.md` before any new report was read.
2. Online screen: every title in the 22 volume lists was matched to the frozen gazetteer (S-ON1) and, by eye, to names the gazetteer lacked (S-ON2, amendment A2). Tiers: T1 = Z1–Z3 or region-wide names; T2 = Z4 names not beginning "Jerusalem,"; T3 = "Jerusalem, …". Reading order within a tier is ascending SHA-256 of the report id, so any read part is a pseudo-random sample of its tier. Sixteen titles naming places outside the region (Yafo or Ramla "Jerusalem Boulevard", Bet Lehem Ha-Gelilit, Horbat Betar, etc.) were dropped by title (A3).
3. Each candidate was opened in turn. Its map reference was converted (OIG EPSG:28191, NIG EPSG:2039; phase-1 `geo.py`) and zoned; reports whose reference fell outside every box were recorded as `opened: map ref outside region` and not coded. Cave reports in the held areas (Qumran cliffs and marl terrace, Jericho escarpment, Wadi Qelt gorge) were opened to their first lines only and held.
4. Coding: one row per report and class (or per site when a survey gives separate sites or map references); `quote` ≤ 12 words; `period_as_given` in the report's words; `dated_in_window` yes only when the report dates the feature (or its use) inside the window. Typological datings stated by the report (for example "a type of tomb … dating to the mid-Second Temple period") were coded yes; fill sherds alone were coded unknown. Features cited only from earlier work were not coded and are named in `notes`.
5. `scripts/build_phase2.py` converts, zones and measures distances (to the nearest point place in `places_v2.csv`), and writes all tables. It is deterministic; `tests/test_phase2.py` rebuilds and compares.

## Results

Full tables: `summary.md` (generated). Headline (rows; yes / no / unknown):

__RESULTS_TABLE__

Notable in-window rows (EVIDENCE, report's dating; no identification is implied): the Cave of the Pool in Nahal David with its plastered stepped pool and feeder groove (HAESI-198, -1173, -5384); refuge caves of the Bar Kokhba period in Nahal Hever (HAESI-25608) and Nahal ‘Arugot (HAESI-25101); a Second Temple tomb with a bronze-vessel hoard in the cliff at ‘En Gedi, entrance marked by a stone and an incised X (HAESI-1594); the ‘En Shulamit aqueduct (HAESI-1671); a deliberately buried, covered Early Roman cooking pot at Waladje (HAESI-2081); the Colonia (Moza) water systems, stepped pool and cistern of the late 1st–early 2nd century CE (HAESI-25953, -26581); and the Wadi Suweinit hiding complex with a stepped ritual bath (ESI02-107).

Phase-1 rows by zone (not re-coded; phase-1 classes): see `phase1_zone_crosswalk.csv` and `summary.md`.

## Blocked and held

Blocked (owner action needed):
- Portal PDFs: in-browser reading failed (test URL https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1001&context=ha_hebrew_series, HA 2–3: cover visible, no text layer through the page-text tool). Nothing was downloaded. All volumes needed are in `portal_pdfs_needed.csv` with exact PDF URLs and sizes; priority A first. The Tier-1 record **HA 28–29 (Tananir)** is https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1063&context=ha_hebrew_series (22.7 MB, portal item https://publications.iaa.org.il/ha_hebrew_series/64).

Held for the arrival procedure (not read beyond the first lines; listed with citation):
- HA-ESI 129 (2017), ʽEn Perat, burial cave, J&S License 2-3-2014 — https://hadashot.iaa.org.il/report_detail_eng.aspx?id=25219
- HA-ESI 132 (2020), ‘Enot Qumran (West), Cave A4-026 — https://hadashot.iaa.org.il/report_detail_eng.aspx?id=25868
- HA-ESI 117 (2005), Qumran Plateau (southern plateau of Kh. Qumran; held as a precaution) — https://hadashot.iaa.org.il/report_detail_eng.aspx?id=126
- HA-ESI 132 (2020), Kh. Qumran, marl plain north of the site (dwelling caves) — https://hadashot.iaa.org.il/report_detail_eng.aspx?id=25871
- ESI 6 (1988) pp. 66–68, "Judean Desert, Survey of Caves 1985/86" (Qumran caves) — local PDF, not read.
- ESI 7–8 (1990) pp. 92–93, "Judean Desert, Cave Survey 1986/87", including Na‘aran–Jericho cliff — local PDF, not read.
- ESI 7–8 (1990) pp. 95–97, Pharan and ‘Ein el-Fawwar sections of the monastery survey (Wadi Qelt) — local PDF, not read.

## Files

- `PLAN.md` (frozen), `AMENDMENTS.md`, `README.md`.
- `features.csv` (phase-1 columns + `region_zone`, `dist_to_nearest_place_km`, `feature_subtype`, `exposure_at_freeze`); `reports.csv` (phase-1 columns + `region_zone`, `dist_to_nearest_place_km`, `exposure_at_freeze`, `tier`).
- `online_screen.csv`: all 798 online candidates with tier, order position and status (read, opened outside region, held, dropped by title, not read).
- `portal_pdfs_needed.csv`: portal volumes not read, with PDF URLs, sizes, phase-1 candidate counts and priority.
- `phase1_zone_crosswalk.csv`: phase-1 report and feature rows with a phase-2 zone.
- `looks_haesi_phase2.csv`: looks rows in the phase-1 schema (relation `HAESI-COVER`, detection numbers null).
- `summary.md`, `summary.json`: generated tables.
- `data/`: coding (`coding_local_*.json`, `coding_online.json`), title lists and hashes, screen amendment, statuses, local source and span hashes.
- `scripts/`: `common.py`, `screen_online.py`, `portal_needed.py`, `build_phase2.py`. `tests/test_phase2.py`.

Run: `python3 -I research/regional/haesi_features/phase2_2026-10-10/scripts/build_phase2.py` then `python3 -I -m unittest discover -s research/regional/haesi_features/phase2_2026-10-10/tests`.

## Proposed changes for the integrator

- Owner: download the portal PDFs in `portal_pdfs_needed.csv` (priority A first, including HA 28–29) to `~/Downloads`; a later session can read them on the Mac as done here.
- Arrival register: add the seven held cave items above (four online, three local sections) as arrival items; record deviation D1 (ESI 3 pp. 61–62 ‘Ein Far‘a section and ESI 5 p. 58 Ketef Yeriho cave read before the hold was checked; no opening direction in either) against the IAA-archive cave-records item.
- Tier-1 record Kh. ‘Almit: extraction from ESI 5 p. 1 is in `reports.csv` (`ESI05-001-kh-almit`) for the integrator's comparison.
- Entry lanes may use `features.csv` as a denominator by class and zone; rows are reports' rows, not unique features (Cave of the Pool and Moza appear in several seasons).
- `research/sources/drive_index.md`: the owner's Mac holds local copies of ESI 2, 3, 5, 6, 7–8, 9, 15 and HA 40, 45, 59–60 (hashes in `data/local_sources.csv`); consider adding them to the Drive index.
