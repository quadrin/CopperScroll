# Phase 4, part E: ʿAtiqot vols 42–121 (2002–2026), screen and PDF list

**What it is.** A screen of every article title in ʿAtiqot 42–121 on the IAA portal against the frozen phase-2 gazetteer, with the candidates placed in a zone and tier from their landing pages. Exploratory; no identification claim.
**Main result.** 1,357 listings (1,336 articles) were screened. 237 PDFs are needed: T1 17, T2 208, T3 3, and 9 unlocated (U). No article body was read, so `reports.csv` and `features.csv` have headers only.
**What stays unknown.** Every feature count for this source. Reading waits for the owner's approval of the PDF downloads; the portal PDF endpoints refuse scripts and are not worked around.

## Sources and access

- Volume pages `https://publications.iaa.org.il/atiqot/vol<N>/iss1/` for N = 42–121 (80 pages), fetched with curl from the workspace, at least 4 s apart, all HTTP 200.
- Landing pages of the 256 candidates (`…/atiqot/vol<N>/iss1/<item>`), same route and pacing, all HTTP 200.
- The portal location map `https://publications.iaa.org.il/atiqot/images.kml` (one request).
- Every request is in `data/fetch_log.csv`.
- **Not read:** all 237 article PDFs in `pdfs_needed.csv`. Status: not read (awaiting the owner's approval of the downloads). No PDF or `viewcontent` URL was requested.
- ʿAtiqot 41 is excluded whole and was not fetched.

## Method

- Every title was screened with the phase-2 gazetteer, A1 normalisation and A3 variants (`scripts/screen_lib.py`, reusing phase-2 `common.py`).
- All titles were then read by eye (exploratory, as A2): 30 added, 25 sent to a location check, 32 gazetteer hits dropped as plainly outside the region by title (`data/screen_manual.csv`).
- Landing pages gave keywords and abstract first lines. No landing page gives a map reference. Zones come from the title (plan §2), the abstract, or, for three articles, the portal map point (`data/landing_decisions.csv`).
- Tiers follow plan §3.4: T1 = Z1, Z2, Z3 or a region-wide term; T2 = Z4, title not beginning "Jerusalem"; T3 = Z4, title beginning "Jerusalem". Within a tier the order is ascending SHA-256 of the unit id. Tier U (unlocated) is my addition and comes last.
- Unit ids: `ATQ<vol>-<first page>-<slug>`. Where the portal shows no page, the item number stands in (`ATQ<vol>-i<item>-<slug>`).
- Choices and deviations are in `NOTES.md`.

## Results

Screen decisions (`screen.csv`, 1,357 listings):

| Decision | Listings |
|---|---|
| not a candidate (no gazetteer term, not added by eye) | 1,048 |
| duplicate listing of the same article | 21 |
| dropped: outside region by title (A3) | 32 |
| dropped: outside region (landing page) | 19 |
| candidate: in region (PDF needed) | 228 |
| candidate: unlocated (PDF needed for the map reference) | 9 |

PDFs needed (`pdfs_needed.csv`):

| Tier | PDFs | Zones | With page range | Pages known | Portal PDF size |
|---|---|---|---|---|---|
| T1 | 17 | Z3 13, Z2 1, region-wide 3 | 1 | 14 | 36.8 MB |
| T2 | 208 | Z4 208 | 130 | 1,847 | 387.6 MB |
| T3 | 3 | Z4 3 | 2 | 91 | 14.1 MB |
| U | 9 | unlocated | 6 | 166 | 24.9 MB |

That is 237 PDFs and about 463 MB. Page ranges are known for 139 of them (2,118 pages). At the same average, the whole list would be roughly 3,600 pages (INFERENCE).

By the title alone (rough INFERENCE, column `article_kind`), 179 are excavation, survey or site studies and 58 are finds or specialist studies.

Feature rows by class and zone (yes / no / unknown): none. No article was read.

## Protected and held

- 0 held. No title, keyword or abstract first line placed a cave article in a held cave area. `held.csv` has its header only.
- No Kh. ʿAlmit article and no Tell es-Sultan north-strip text was found in titles or landing pages.
- 110.9 and 116.8 are laboratory studies of Dead Sea Scrolls material that the portal map places at Kh. Qumran. Their first lines describe artefacts, not a cave. They stay in T1, and the reader repeats the held check at the first line.

## Blocked

Nothing was blocked. PDF endpoints were not requested. The integrator's earlier test PDF request was refused with 403 (`../PLAN.md`, exposure section).

## Files

- `screen.csv`: every listing, with decision, reason, zone, tier and order.
- `pdfs_needed.csv`: unit id, title, authors, landing and exact PDF URL, zone, tier, order, flag, SHA-256 of the unit id.
- `held.csv`: held or protected units (none).
- `reports.csv`, `features.csv`: phase-2 headers only.
- `summary.json`: the counts above.
- `NOTES.md`: steps, choices, exposure, proposed owner request.
- `data/`: parsed article list, manual screen, landing metadata (keywords, abstract hash), portal map points, landing decisions, fetch log.
- `scripts/`: `parse_volumes.py`, `screen_lib.py`, `landing_list.py`, `extract_landing.py`, `make_decisions.py`, `build_part_e.py`, `fetch_log.py`.
- `tests/test_part_e.py`. Run from the repository root: `python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/tests`.

Counts for the tests: 1357 listings, 237 PDFs, 0 held.
