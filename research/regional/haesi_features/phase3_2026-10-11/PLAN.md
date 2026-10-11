# HA-ESI phase 3: scope freeze (reading the downloaded portal volumes and the rest of the online Jerusalem tier)

Written 11 October 2026 (Los Angeles) by the integrator, before any portal volume or further online report was read. Committed alone; its commit is the freeze record.

## What phase 3 is

Phase 3 continues the phase-2 inventory under the **phase-2 frozen plan, unchanged**: `../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be` (commit d0f8c7c), with its amendments A1–A4 as recorded in `../phase2_2026-10-10/AMENDMENTS.md`. Region and zones (§2), gazetteer (§4), eligible feature classes (§5), coding rules and output columns (§6), protected and held material (§7) and decision wording (§8) apply as written. Nothing here changes them.

What phase 3 adds is access, not rules:

1. **Downloaded portal volumes.** On 11 October 2026, with the owner's approval, 101 portal volumes (HA 1961–1998, ESI 1–20, HA-ESI 109–115) were saved to the owner's computer, `~/Downloads/IAA portal volumes/`, with sizes and SHA-256 in `../phase2_2026-10-10/portal_downloads_2026-10-11.csv`. Each volume is read with the phase-2 local-PDF method (plan §3.3, S-LOC): text extracted with `pdftotext` (layout and raw) on the owner's computer; **every report heading in the whole volume is screened**; a heading's map reference is converted and zoned; without one, its title or heading is matched to the gazetteer (with the A3 name variants); **every report in the region is read and coded**. Reports already coded in phase 1 or phase 2 are not re-coded; they get a zone in a crosswalk file. Phase-1 screen candidates (`../data/screen_candidates.csv`) that fall in a volume are checked off explicitly (read, outside region, or not found in the volume), so that the 651 phase-1 unread candidates are each accounted for.
2. **The rest of the online Jerusalem tier.** Online tier T3 (titles beginning "Jerusalem") continues from position 81 of 662, in the frozen order (ascending SHA-256 of the report id), through the owner's Chrome as plan §3.1 and §3.4 require: one tab, one page at a time, at least 3 seconds between page loads, no scripted bulk fetching, no downloads; any check asking for a click or a CAPTCHA stops the route.

The stop rule (plan §3.5) applies: whatever is not read when a part must stop is listed with its position or volume and page as `not read (time limit)`.

## Parts (one worker each; the integrator merges)

| Part | What it reads | Folder |
|---|---|---|
| A | HA Hebrew series, volumes dated 1961–1979 (50 files, listed in `partition.csv`), including HA 28–29 | `part_a/` |
| B | HA Hebrew series, volumes dated 1980–1998 (32 files) | `part_b/` |
| C | ESI 1, 4, 10–14, 16–20 and HA-ESI 109–115 (19 files) | `part_c/` |
| D | Online tier T3, positions 81–662 | `part_d_online/` |

IAA Reports 7 (Jericho cemetery) and IAA Reports 1 (Akeldama) are read by the tombs lane (`research/regional/tombs/`) under that lane's own plan, not here.

Each part writes `reports.csv`, `features.csv` (phase-2 column order exactly), `screen.csv` (every heading or title screened, with decision and reason), `candidates_checkoff.csv` (parts A–C: each phase-1 candidate in its volumes and what happened to it), and `NOTES.md` (what was read, page ranges, deviations, not read). Report ids for portal volumes: `<SERIES><vol>-<first page>-<slug>`, as phase 2 used for local volumes (for example `ESI05-058-ketef-yeriho`).

## Protected material (restating plan §7; no change)

- **Held cave reports** (Qumran cliffs and marl terrace from Wadi Qumran to ʿEin Feshkha; Jericho escarpment from Jebel Qarantal to Wadi Nuweiʿimeh and ʿAin Duk; Wadi Qelt gorge): listed with citation and first lines only, not read.
- **HA 28–29** (Tier 1): extraction only, by part A, before any other use: the reader does not open the arrival item files or `research/assessments/kohlit_chain/chain.json`. Facts go to `part_a/tier1_HA28-29_extraction.md` with page numbers; the integrator compares under `research/preregistration/arrivals/ARRIVAL_PROCEDURE.md`. The same applies to any IAA notice on Kh. ʿAlmit found in any volume (`tier1_kh_almit_extraction.md` in that part).
- **Tell es-Sultan north strip**: citation only, `protected_strip = yes`.
- The L-656 field file and IAA Archive cave records are not sought.

## Exposure before this freeze

The integrator has seen the phase-2 README, PLAN, AMENDMENTS, the column headers and summary counts, the download manifest (file names, sizes, hashes), and, while checking that the downloads were text PDFs, the `pdftotext` output of page 5 of HA 36, HA 5, HA 103 and ESI 18 (a few lines each: a survey note on Tel Ḥushniyya, a Tel heading, a blank page, and the ESI 18 contents list). No report in the region was read.
