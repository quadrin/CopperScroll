# Regional inventory phase 4: scope freeze (ʿAtiqot, IAA Reports, QDAP, nineteenth-century surveys, ADAJ)

The integrator wrote this on 11 October 2026 (Los Angeles), before any title list, article or survey entry from these sources was read. It is committed alone, and that commit is the freeze record.

## What phase 4 is

Phase 4 extends the regional inventory of the scroll's feature kinds to five more source groups. It runs under the **phase-2 frozen plan, unchanged**:

- the plan is `../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be` (commit d0f8c7c);
- amendments A1–A4 apply as recorded in `../phase2_2026-10-10/AMENDMENTS.md`, and the A3 name variants are used as in phase 3.

The following apply as written, and nothing here changes them:

- region and zones (§2), including the rule for placing a text with no map reference by name;
- the gazetteer (§4) and the eligible feature classes (§5);
- the coding rules, the in-window rule, labels and output columns (§6);
- protected and held material (§7) and the decision wording (§8).

Phase 4 adds access routes and report-unit definitions only. All of it is exploratory, it makes no identification claim, and no registered result can change from it.

## Parts, sources and access routes

One worker runs each part, and the integrator merges them. Each part's rules:

- **Screening.** Every title, heading or site entry in its source is screened against the gazetteer, or placed by map reference where the source gives one.
- **Reading.** Every in-region unit is read and coded. Reading order is tier T1, then T2, then T3, as phase-2 plan §3.4 defines the tiers. Within a tier, units go in ascending SHA-256 of the unit id.
- **Stop rule.** The phase-2 stop rule (§3.5) applies. Whatever is not read is listed as `not read (time limit)` with its tier and position.
- **No figures stored.** No figure, plate, plan or photograph is stored in this phase. Figures worth archiving are listed in the part's `NOTES.md` for a later, rights-checked archiving pass.

| Part | Source | Units and ids | Access route |
|---|---|---|---|
| E | ʿAtiqot vols 42–121 (2002–2026), IAA portal | One article = one unit, `ATQ<vol>-<first page>-<slug>`. A survey article with separate sites that have their own map references gives one row per site and class, as in plan §6 | **Screen:** fetch the 80 volume pages (`publications.iaa.org.il/atiqot/vol<N>/iss1/`) from the workspace, one at a time, at least 3 s apart; article landing pages only for title candidates. **Read:** the PDF endpoints refuse scripts and must not be worked around. The candidate PDFs are downloaded in the owner's Chrome only after he approves the list, then read on his Mac with `pdftotext`. Until then the part delivers the screen and the candidate list |
| F | IAA Reports nos. 2–6 and 8–78, IAA portal | A monograph's report on one site = one unit, `IAAR<no>-<slug>`. Chapters on separate sites are separate units | As part E. IAA Reports 1 and 7 were already read by the tombs lane and are not re-read |
| G | QDAP vols 1–14 (1931–1950), archive.org collection `pub_quarterly-department-of-antiquities-palestine` | One article, or one site paragraph in a round-up such as "Excavations in Palestine", = one unit, `QDAP<vol>-<page>-<slug>` | archive.org OCR text (`_djvu.txt`) of the open issue items, fetched from the workspace. Page numbers are taken from the text or the page images |
| H | *Survey of Western Palestine*, Memoirs II (Samaria, 1882) and III (Judaea, 1883); then Guérin, *Judée* I–III and *Samarie* I | One site entry = one unit, `SWP<vol>-<page>-<slug>` or `GUE-<J1..J3,S1>-<page>-<slug>` | archive.org OCR text: SWP `surveyofwesternp02conduoft`, `surveyofwesternp03conduoft`; Guérin `descriptiongeogr01guer`–`04guer`. Order: SWP III, SWP II, Guérin Judée I–III, Samarie I. The stop rule applies between and within volumes |
| I | ADAJ, Jordan Department of Antiquities portal | One article or field report = one unit, `ADAJ<vol>-<first page>-<slug>` | PDFs listed on `publication.doa.gov.jo` (Publication Type ADAJ), fetched from the workspace one at a time, at least 3 s apart. Volumes 1–12 (1951–1967, West Bank years) first, then later volumes |

**Location for sources without map references:**

- **H:** if an entry carries an SWP sheet and square, the zone comes from that sheet. Otherwise it is placed by name, with the gazetteer and `places_v2.csv`, under plan §2 (`coordinate_source = name only`). An entry whose name is ambiguous stays unlocated and is listed.
- **G and I:** an old report with a Palestine Grid reference is converted with EPSG:28191, as for the Old Israel Grid in phase 1.

**Excavated or surveyed:** nineteenth-century survey entries are coded `surveyed`, or `inspected` where the text says so.

## Protected and held material

Phase-2 plan §7, restated with the cases these sources raise. None of this is new rules.

- **Held cave areas** are the Qumran cliffs and marl terrace, the Jericho escarpment (Jebel Qarantal to Wadi Nuweiʿimeh and ʿAin Duk) and the Wadi Qelt gorge. A report or survey entry on a cave in a held area is listed with its citation and first line only, and is not read. This applies in every part, including SWP and Guérin descriptions of the Quruntul hermit caves and the Wadi Qelt caves. Built sites there are read normally, for example Kh. Qumran, the Jericho palaces and the Wadi Qelt aqueducts.
- **Tell es-Sultan north strip.** A text describing the strip is recorded as `protected_strip = yes`, with its citation only.
- **Kh. ʿAlmit.** Any text on Kh. ʿAlmit is handled under the Tier-1 extraction rule. The reader extracts facts with page numbers to `tier1_kh_almit_extraction.md` in the part folder, and does not open the arrival item files or `research/assessments/kohlit_chain/chain.json`.
- **ʿAtiqot 41** (Tier 1 cave entries) is excluded whole: not screened, not read.
- **Not sought:** Kochavi 1972 (registered arrival item `kochavi-1972`), the L-656 file and the IAA Archive cave records.
- **Drive and Downloads.** On the owner's Mac a part opens only the files it downloaded under this plan, in `~/Downloads/IAA portal volumes/phase4/`. Nothing else in `~/Downloads` is listed or opened. The owner's Drive library is not used in phase 4.

## Outputs

Each part writes the following, using the phase-2 columns in the same order:

- `reports.csv`, `features.csv` and `screen.csv` (every unit screened, with its decision and reason);
- `held.csv` (held or protected units, citation only);
- `NOTES.md` (what was read, page ranges, deviations, not read, figures to archive later);
- tests that check the column order, the zone rule and that no held unit was coded.

Parts E and F also write `pdfs_needed.csv` (unit, exact PDF URL, tier, order), so the integrator can ask the owner.

Rows are not deduplicated against phases 1–3 in this phase. The merge (`../merged_2026-10-11/`) is extended later under its own plan.

## Exposure before this freeze

While checking access, the integrator saw:

- **ʿAtiqot:** the all-issues page (volume numbers and links only); the vol. 100 page (link counts only, no titles read); one landing page (fetched to find the PDF link pattern; no title or text read); and one PDF request, refused with 403.
- **Other portals:** the IAA Reports series page (fetched, size only); the DoA ADAJ search page (the newest file names); the EAP1544 vol. I manifest (fetched, size only); the size of the SWP Memoirs III OCR text (not read); and `robots.txt`.
- **Earlier today:** two link-checking workers saw QDAP and IEJ contents pages and the IEJ 1961–62 article titles. No entry, article body or site description from these sources has been read for the project.
