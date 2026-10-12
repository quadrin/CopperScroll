# Phase 4, part E (ʿAtiqot 42–121): working notes

Worker session of 11 October 2026 (Los Angeles; fetches logged in UTC on 12 October). Rules: phase-2 frozen plan (`../../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c08…b3be`) with amendments A1–A4, under the phase-4 scope freeze (`../PLAN.md`, commit b002e03, SHA-256 `5428c4cc…2da`). `arrival.py check` returned `manifest: ok (29 files)` at the start.

## What was done

1. **Volume pages.** All 80 volume pages (`/atiqot/vol42/iss1/` to `/vol121/iss1/`) were fetched with curl from the workspace, at least 4 s apart. Every one returned HTTP 200. `scripts/parse_volumes.py` turned them into `data/atiqot_articles.csv`: 1,357 listings with title, authors, landing URL, PDF URL and PDF size.
2. **Title screen.** Every title was matched to the phase-2 gazetteer with the A1 normalisation and the A3 variants (`scripts/screen_lib.py`, which reuses phase-2 `common.py`). Hebrew titles: only 3 portal titles contain Hebrew script (pointing marks inside English words); Hebrew-language articles are listed under English titles, which were screened. 234 titles matched.
3. **Manual screen (exploratory).** I then read all 1,357 titles by eye, as phase 2 (A2) and phase 3 did. `data/screen_manual.csv` lists every manual action with its reason: 32 gazetteer hits dropped as plainly outside the region by title (A3 practice), 30 titles added because they name an in-region place in a form the gazetteer misses, and 25 titles sent to a landing-page location check because the place was unknown to me or the title named no place.
4. **Landing pages.** The 256 candidate landing pages were fetched, at least 4 s apart, all HTTP 200. `scripts/extract_landing.py` keeps only the keywords, whether there is an abstract, and the SHA-256 of the abstract (`data/landing_meta.csv`). No landing page gives a map reference.
5. **Portal location map.** The journal's `images.kml` (one request) gives a point for 277 articles. Its points are the portal's, not the article's. They were used only to place three location-check articles and to cross-check zones (`data/kml_points.csv`, WGS84 lon/lat as published). Placemarks of ʿAtiqot 41 were dropped by the script before anything was written or shown; there were none in the file.
6. **Placement.** `scripts/make_decisions.py` records the decision for every landing page (`data/landing_decisions.csv`). `scripts/build_part_e.py` writes `screen.csv`, `held.csv`, `pdfs_needed.csv` and `summary.json`.

No PDF or `viewcontent` URL was requested by any script or by hand. No article body was read.

## Deviations and choices (exploratory)

- **Manual screen.** The by-eye additions and location checks are exploratory, as A2 in phase 2. They carry `screen = S-MAN (manual, exploratory)`.
- **Normalisation gaps found.** Two forms escape the A1 normalisation: the possessive "Jerusalem’s" (normalised to "jerusalems"; 4 titles) and the modifier-letter apostrophe U+02BC in "Refaʼim" (1 title, 116.14). "Jerusalemin" (120.6) is a portal typo. All six were added by the manual screen. I did not change `screen_lib.py` or the gazetteer.
- **Spellings outside the gazetteer.** ‘Aujah (gazetteer: auja), ‘En ‘Aneva (not in the gazetteer), Qidron Valley, Tyropoeon Valley, Wilson’s Arch, Tel Arza, Western Wall Tunnels, Khirbat Ka‘kul, Khirbat ‘Adasa/‘Addasa and Khirbat Umm Leisun (companions of Jerusalem-titled articles).
- **‘En ‘Aneva (42.33)** is placed in Z3 by name, using the place's map reference in phase-2 row ESI02-029 (OIG 18225/08435). It is the only zone taken from another record.
- **Namesakes and polities.** "Latin Kingdom of Jerusalem" (110.19) and "Kingdom of Jerusalem" (112.10) name a polity, not a place. Both are country-wide syntheses and were dropped.
- **"Samaria".** The JSON parameters list "samaria" as a region-wide term without the prose's "with a zone name". I applied the JSON. 114.3 (southern Samaria, "desert fringes") stays in T1 as region-wide. 119.8 (Western Samaria) and 120.4 (Poriyya, northern Jordan Valley) were dropped as outside the region on their abstracts.
- **Laboratory studies at Qumran.** 110.9 (inkwell residues, Dead Sea Scrolls) and 116.8 (tefillin skins, Judean Desert) are region-wide T1. The portal map puts both at Kh. Qumran. Their first lines describe artefacts, not a cave, so they are not held. They are flagged in the notes: the reader applies the held check at the first line.
- **Page numbers.** Pages come only from the page note that the portal prints in many titles. The landing pages' `bepress_citation_firstpage` equals the portal item number, not a printed page (checked in the tests), so it is not used. Where no page is shown, the unit id uses the item number: `ATQ<vol>-i<item>-<slug>`. A starred page (Hebrew or English-summary pagination) gets the suffix `s`, as in `ATQ84-065s-…`. Pages are zero-padded to three digits, as in the phase-2 and phase-3 ids. The ids are fixed now and are not changed after reading; printed pages go in the page columns.
- **Duplicate listings.** 21 articles are listed twice on their volume page (vols 53, 57, 65), with the same title and pages but different PDF records. Each is screened once; the second listing is marked `duplicate listing`.
- **Unlocated candidates.** 9 candidates could not be placed from the title, landing page or portal map. They are listed as tier `U`, after T3, because only the PDF can give the map reference. This tier is my addition, so that they are not lost; plan §2 says an unlocated unit is listed, not coded.
- **Article kind.** `pdfs_needed.csv` has a column `article_kind` ("excavation, survey or site study" or "finds or specialist study"). It is a rough INFERENCE from title words, for the owner's information only. It does not change the frozen order.
- **First request.** The very first volume page (vol. 42) was fetched with the user agent "Mozilla/5.0". I fetched it again 3 s later with curl's default agent and used that copy. Every other request used curl's default agent. Nothing was blocked, so no check was worked around.

## Exposure in this pass

- Seen: all 1,357 portal titles and author lines; for the 256 candidates, the keywords and the first sentence of the abstract (where there was one). I read the full abstract for 7 location checks only: 52.55, 56.6, 70.10, 71.9, 101.3, 112.6 and 114.3. None of them is a cave in a held area.
- The abstract of 119.3 (‘Aujah aqueducts) mentions Wadi Qelt. It concerns aqueducts (built features), which are read normally. Its full text was not opened.
- These units are still "unexposed at freeze" when read later. The freeze was before this pass, and nothing here was evidence for a registered test.

## Protected and held

- **ʿAtiqot 41:** not fetched or screened (the volume range starts at 42; the KML filter drops vol. 41).
- **Held cave areas:** no title, keywords or abstract first line placed a cave article in the Qumran cliffs and marl terrace, the Jericho escarpment or the Wadi Qelt gorge. `held.csv` has its header only.
- **Kh. ʿAlmit:** no title, keyword or landing page names it. No Tier-1 extraction file is needed for this pass.
- **Tell es-Sultan north strip:** no title or landing page names Tell es-Sultan. Nothing is flagged `protected_strip`.
- Not sought: Kochavi 1972, the L-656 file and the IAA Archive cave records.

## Not read

Nothing in this part has been read yet. Reading waits for the owner's approval of the PDF list. Every candidate in `pdfs_needed.csv` is `not read (awaiting PDF download)`, with its tier and order.

## Figures to archive later

None seen; no article was opened.

## Proposed changes for the integrator

- No change to shared status files from this part, since nothing was read.
- If the screen is reused for other series: add U+02BC (ʼ) to the A1 drop list, and match the possessive ’s. That would be a new amendment, not a silent change.
- Owner request, one line: "ʿAtiqot 42–121: approve the download of 237 article PDFs (T1 17, T2 208, T3 3, U 9; about 463 MB) listed in `part_e_atiqot/pdfs_needed.csv`."
