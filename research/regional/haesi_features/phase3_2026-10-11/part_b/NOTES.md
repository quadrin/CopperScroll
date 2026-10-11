# HA-ESI phase 3, part B: HA Hebrew volumes 1980–1998

Reader: part-B worker, 11 October 2026. Rules: phase-3 scope freeze `../PLAN.md` (SHA-256 `312c2733…55cf2`, commit 4d8325e) and the phase-2 frozen plan `../../phase2_2026-10-10/PLAN.md` (SHA-256 `5b1a5c08…7b3be`) with amendments A1–A4, unchanged. Both hashes are checked by `tests/test_partb.py`. Nothing here changes a frozen parameter.

## What was read

All 32 part-B files of `../partition.csv` (HA 73 to HA 108), each as a whole volume. Files, SHA-256 (verified against the partition), portal item URLs, PDF page counts and table-of-contents pages are in `data/volumes.csv`.

| HA vol. | year | PDF pp. | headings | read | already coded (Eng.) | opened, not coded | held | automatic |
|---|---|---|---|---|---|---|---|---|
| 73 | 1980 | 47 | 32 | 1 | 0 | 0 | 0 | 31 |
| 74–75 | 1980 | 65 | 36 | 2 | 0 | 0 | 0 | 34 |
| 76 | 1981 | 49 | 30 | 1 | 5 | 1 | 0 | 23 |
| 77 | 1981 | 71 | 56 | 12 | 0 | 2 | 0 | 42 |
| 78–79 | 1982 | 107 | 75 | 16 | 0 | 0 | 0 | 59 |
| 80–81 | 1982 | 75 | 55 | 6 | 0 | 1 | 0 | 48 |
| 82 | 1983 | 85 | 54 | 1 | 13 | 4 | 0 | 36 |
| 83 | 1983 | 86 | 59 | 0 | 7 | 0 | 0 | 52 |
| 84 | 1984 | 75 | 47 | 0 | 11 | 1 | 0 | 35 |
| 85 | 1984 | 54 | 52 | 0 | 7 | 1 | 0 | 44 |
| 86 | 1985 | 50 | 75 | 7 | 0 | 3 | 0 | 65 |
| 87 | 1985 | 55 | 57 | 6 | 0 | 3 | 0 | 48 |
| 88 | 1986 | 42 | 43 | 0 | 8 | 8 | 0 | 27 |
| 89 | 1987 | 67 | 63 | 2 | 8 | 1 | 0 | 52 |
| 90 | 1987 | 68 | 50 | 0 | 7 | 5 | 1 | 37 |
| 91 | 1988 | 39 | 6 | 0 | 0 | 0 | 0 | 6 |
| 92 | 1988 | 83 | 67 | 1 | 8 | 3 | 0 | 55 |
| 93 | 1989 | 105 | 77 | 0 | 8 | 8 | 1 | 60 |
| 94 | 1989 | 77 | 75 | 2 | 6 | 4 | 0 | 62 |
| 95 | 1990 | 87 | 75 | 0 | 11 | 2 | 0 | 62 |
| 96 | 1991 | 66 | 41 | 4 | 0 | 4 | 0 | 33 |
| 97 | 1991 | 107 | 86 | 11 | 0 | 6 | 0 | 69 |
| 98 | 1992 | 60 | 7 | 0 | 0 | 0 | 0 | 7 |
| 99 | 1993 | 124 | 89 | 13 | 0 | 7 | 1 | 68 |
| 100 | 1993 | 133 | 90 | 18 | 0 | 8 | 1 | 63 |
| 101–102 | 1993 | 152 | 102 | 18 | 0 | 15 | 0 | 69 |
| 103 | 1995 | 140 | 98 | 1 | 20 | 7 | 0 | 70 |
| 104 | 1995 | 139 | 91 | 16 | 0 | 4 | 1 | 70 |
| 105 | 1996 | 38 | 1 | 0 | 0 | 0 | 0 | 1 |
| 106 | 1996 | 185 | 109 | 14 | 0 | 13 | 1 | 81 |
| 107 | 1997 | 169 | 120 | 17 | 0 | 14 | 0 | 89 |
| 108 | 1998 | 204 | 158 | 10 | 0 | 8 | 0 | 140 |

"Automatic" = outside region by the frozen screen rules, or a group heading whose children were screened. HA 91, 98 and 105 are Bet Sheʾan expedition volumes (outside the region). HA 94 lacks printed pp. 30–31, 38–39 and 46–47 in the portal copy (page numbers jump); see "Not read".

Totals (from `summary.md`, generated): 2,076 headings; 179 reports read and coded, all in the region (146 Z4, 24 Z3, 8 Z2, 1 Z1; 23 with no eligible feature); 473 feature rows (window yes 115, no 188, unknown 170); 119 headings already coded in phase 1 or 2 from their English versions (crosswalk with zones in `already_coded_crosswalk.csv`); 267 phase-1 screen candidates in these volumes, each checked off (`candidates_checkoff.csv`; none left "not found in the volume").

## Method (plan §3.3 on whole volumes)

1. Text: `pdftotext -layout` and `-raw` of each PDF on the owner's computer, one volume at a time; text kept outside the repository (session scratch). Line numbers in `text_lines` are 1-based global raw-file lines; `data/spans.csv` gives the SHA-256 of each coded span (whitespace collapsed, bidi marks removed) and confirms every quote is found verbatim (`scripts/verify_spans.py`: 179 records, 0 quotes not found).
2. Headings: every entry of the in-volume table of contents (`scripts/toc.py`; 11 hand fixes in `data/toc_fixes.csv`; 15 headings listed by hand in `data/headings_manual.csv` where the contents list is missing or unreadable). Screen id `HA<vol>-<printed page>-<k>` (`pNNN` = PDF page where the printed page was not located).
3. Automatic screen (`scripts/screen_partb.py` → `data/screen_auto.csv`, `data/refs_auto.csv`): map references on the heading's pages converted (OIG EPSG:28191, NIG EPSG:2039; phase-1 `geo.py`) and zoned with the frozen boxes; titles matched to the frozen gazetteer with the A3 variants. Flags decide only what must be opened.
4. Every flagged heading opened by hand (first lines) and decided in `data/decisions/*.csv`; every in-region report read and coded under plan §5–§6 (`data/coding/*.json`; quotes ≤12 words, verbatim from the raw text, OCR punctuation kept).
5. Completeness sweep (`scripts/body_headings.py`): 251 heading-like body lines matching the gazetteer; 60 not matching a contents heading, each reviewed (`data/body_heading_review.csv`, plus automatic classes for imprint lines and the bare group word "ירושלים"); result in `body_headings.csv`.
6. `scripts/build_partb.py` merges everything and writes the outputs; `tests/test_partb.py` re-runs it and compares byte for byte.

Report location (EVIDENCE of method): a report map reference → coordinates and zone (115 reports); otherwise the zone of the named place (63, "name only (zone)"); otherwise the zone of its first feature reference (1). Feature rows with their own reference are located separately (55 rows).

## Deviations and judgement calls

- **Screen misses caught by hand** (automatic decision was "outside"; read after the body sweep or hand check): HA100-073-1 Givʿat HaMatos (range reference not parsed, name not in gazetteer); HA108-136-1 Gihon Spring and HA108-138-1 Old-City wall (Jerusalem group heading missing from the HA 108 contents); HA106-173-2, the list of archive reports (pp. 173–175), whose Jerusalem, East Talpiyot entry has no map reference (coded as `HA106-175-east-talpiyot`, no finds). HA78-059-1 Ras et-Tawil is marked **EXPLORATORY ADDITION** in its decision: title not in the gazetteer and printed reference unreadable; the text places it south of Neve Yaʿaqov (Z4).
- Nine `HA<vol>-p000-1` rows are the contents-page running head (journal title) parsed as an item: "opened: not a site report".
- Hebrew reports whose English versions were coded in phase 1 or 2 were not re-coded (119). Hebrew reports whose English versions are in ESI 10–20 (part C) **were** coded here; the integrator should deduplicate (below).
- Phase-1 candidate check-off: matched by printed page ±1 and Hebrew title words; 18 matched by hand in `data/candidate_overrides.csv` (OCR-split title, a wrong portal page, archive-list entries, spelling variant). EVIDENCE: the four candidates of portal item 73 (HA 93) have the same text and pages as item 72 (HA 90) candidates #022, #031–#033; INFERENCE: the portal record of item 73 repeats the HA 90 contents; they are checked off against the HA 90 headings. Outcomes use the decision wording (read; already coded; outside region; held; not a site report; group heading with children screened).
- HA 106 H. Tittora (HA106-120-1): printed reference "205/14540" lost its leading digits; the same text gives 15205/14550 (outside).
- Edge zones checked against the boxes: Nahal Yoʾel 15880/12842 outside (lon 35.092); Rekhes Soreq 15971/12868 Z4 (lon 35.1016); Har Etan 160771/13080 Z4.

## Protected and held material

- **Tier 1, Kh. ʿAlmit**: the IAA notice in HA 88 pp. 18–19 (screen HA88-018-1) was extracted only, to `tier1_kh_almit_extraction.md`, committed alone first (18db6bd); it is not coded here (its English version is phase-2 `ESI05-001-kh-almit`).
- **Held cave reports** (citation and first lines only, not coded): HA90-039-1 Judean Desert and Samaria cave survey 1985–86 (Patrich); HA93-065-2 Judean Desert cave survey 1986–87; HA99-045-2 map of Wadi Qilt survey (map 109/4); HA100-055-1 Qumran caves (Patrich 1988); HA104-080-1 map of Qalya survey (109/5); HA106-129-1 H. Qumran survey (Porat 1995, marl terrace). Read normally because outside the held areas: HA100-052-1 Wadi Murrar, ʿEin Abu Mahmud caves (north of Wadi Qumran) and HA108-179-3 the Kh. Qumran aqueduct graffito (built site).
- **Exposure disclosures** (held text displayed beyond first lines while locating neighbouring headings; nothing from it was coded or used): HA 99 raw lines c. 16790–16810 (closing lines of the Wadi Qilt survey); HA 100 lines 24702–24704 (three words after the first line of the Qumran caves report); HA 104 lines 31645–31745 (opening) and 32270–32330 (a period-distribution paragraph) of the Qalya survey; HA 106 lines 47399–47470 (opening of H. Qumran). The body sweep also displayed two sub-heading lines of HA93-065-2 (Wadi Qelt; Naʿaran–Jericho cliff) and one caption line of HA90-039-1.
- **Tell es-Sultan**: the only heading is HA103-061-1 (Jericho, Tell es-Sultan), citation only, not opened; its English version is phase-1 `ESI15-068-jericho`. No part-B row carries `protected_strip = yes`.

## Not read

- HA94-038-1 **Mt. Ebal 1989** (Z1, printed p. 38): pages missing from the portal copy. Its English version is not among the phase-1/2 reports; possibly ESI 10 (part C). A complete copy of HA 94 pp. 38–39 is needed.
- The six held reports above.
- Nothing is `not read (time limit)`.

## Privacy and files

Only the 32 part-B PDFs in `~/Downloads/IAA portal volumes/` were listed (narrow filter), converted and staged. A derived-text archive was written next to them, `~/Downloads/IAA portal volumes/_derived_text_partB/partb_txt.tar.gz` (SHA-256 `d4feb74a9bf9989d917e8e17368c1bb337d4d2703e584c18704d595a7337d139`); it is not in the repository, and the owner may delete it (this session could not). The repository holds only coded rows, citations, coordinates with CRS, quotes ≤12 words and span hashes.

## Reproduce

From the repository root: `python3 -I research/regional/haesi_features/phase3_2026-10-11/part_b/scripts/build_partb.py` (needs no PDF or text); tests: `python3 -I -m unittest discover -s research/regional/haesi_features/phase3_2026-10-11/part_b/tests`. Re-screening or re-verifying spans needs the text directory: `scripts/screen_partb.py TEXTDIR`, `scripts/body_headings.py TEXTDIR`, `scripts/verify_spans.py TEXTDIR`.

## Proposed changes for the integrator

1. **Deduplicate** part-B Hebrew reports against part C's English versions (ESI 10–20) by site, permit number and season. Also check against phase-1/2 ESI 15: `HA100-072-east-talpiyot-lower-aqueduct` vs `ESI15-078-lower-aqueduct`; `HA101-084-arnona` vs `ESI15-080-arnona` (17107/12863); `HA100-063-binyane-haumma` vs `ESI15-072-binyane-haumma` (different excavations: keep both).
2. **Phase-1 accounting**: mark candidates `ha_hebrew_series_73#022`, `#031`–`#033` as duplicates of `ha_hebrew_series_72#…` (same HA 90 items) when counting the 651 phase-1 unread candidates.
3. **Screen limitation** to record with the phase-3 results: headings whose English title omits "Jerusalem" and that carry no parsable reference fall outside automatically; four such misses were caught by hand here, so other parts may have similar ones.
4. **Mt. Ebal 1989** (HA 94 pp. 38–39) needs another copy or its English version before Z1 coverage for 1989 is complete.
5. Held reports (six above) stay held under plan §7; reading them needs the integrator's decision and a reader not exposed to the reserved observations.
