# IAA Discover / Hadashot scrape — cave-survey seed data

Scraped **2026-10-30** for the ICRC / MALHAM (Israel Cave Research Center) work.
The three supplied URLs resolved to one report, one landing page and one
permission-restricted survey record.

## Sources and what came back

| # | URL | Result |
|---|-----|--------|
| 1 | `hadashot.iaa.org.il/report_detail_eng.aspx?id=26324&mag_id=135` | Public. Nahal Hever final report (HA-ESI 135, 2023) — full text + 2 figures. |
| 2 | `discover.iaa.org.il/?entity_index=0` | Public landing page only. Counts: 6,139,011 records, 972,426 artifacts, 3,091,299 images, 17,275 3D models, 2,058 researchers. The catalogue itself is a JS/ArcGIS SPA with no server-rendered content. |
| 3 | `discover.iaa.org.il/?...&entityId=4477322&entityType=survey` | **Blocked.** The SPA ignores the deep link and shows `0 of 0`; the record endpoint returns HTTP **403** `You do not have permission to view this survey.` Survey 4477322 is also absent from the public `/api/surveys` index (3,709 records), so its title cannot be recovered from public data. |

Because record 4477322 is gated, the dataset below covers the **public**
Judean Desert / cave survey records instead — including the survey that the
Hadashot report belongs to (`EXP-42382`, “סקר מערות במצוקי מדבר יהודה
[2017–2024]”, permits S-800/2017 … S-1295/2024).

## API notes

The SPA is backed by a plain, unauthenticated JSON API:

```
GET  /api/surveys                 # 3,709 survey stubs
GET  /api/api/SurveyPage/<id>     # full record — note doubled /api
GET  /api/entity-types            # 18 entity type ids
GET  /api/regions                 # region polygons
```

`/api/api/...` is not a typo: the frontend's `E_backendUrl` is already `/api`,
and `SurveyPage` is appended to it. `POST /api/query` exists but returned empty
result sets for guest sessions, so the scrape filters the full survey list
client-side instead.

Full records expose: survey id/name (he/en), type and subtype, years,
responsible person, permit numbers (`S-800/2017` style), excavator and
institution groups, and the survey polygon as WKT in Israel TM grid
(EPSG:2039). Guest access suffices for all 57 records collected here.

## Files

```
scrape_iaa.py                 survey scraper (no dependencies)
scrape_hadashot.py            report scraper (bs4)
data/surveys.json             57 records, full detail where public
data/survey_licenses.csv      80 rows, one per permit
data/manifest.json            per-record HTTP status + run metadata
data/homepage.json            landing-page counts
data/hadashot/26324_nahal-hever.md    report text
data/hadashot/figures/        fig01.jpg (cave entrances), fig02.jpg (plan/sections)
```

## Dataset shape

- 57 surveys match cave (`מערה/מערות/מערת`, `cave`) or Judean Desert terms.
- 49 flagged `is_cave`, 15 flagged `is_judean_desert` (overlap expected).
- 57/57 detail fetches returned HTTP 200; 58 distinct permit ids.

Judean Desert records include:

- `EXP-1149` — Aharoni's 1953–1957 Judean Desert survey/excavations (4 permits)
- `EXP-5232` — 1960 Judean Desert caves expedition
- `EXP-4421` — 1985–1986 Judaean Desert caves survey (Patrich)
- `EXP-42382` — 2017–2024 cliff caves survey (Sion/Klein/Ganor, 8 permits)
- `EXP-51562`, `EXP-51902`, `EXP-52625` — seasons 7–9 (2024–2026)
- four `YAZ-S-*` records — undated survey stubs with no permits

## Caveats

- **Record 4477322 is not public.** Do not assume it is the 2017–2024 survey;
  the only link is the shared free-text query “מדבר יהודה”.
- The `EXP-42382` polygon in the API is a coarse bounding box
  (`226000–237000 E, 580000–599000 N`), unlike the season records which carry
  real traced polygons. Treat it as a placeholder, not a survey extent.
- Four `YAZ-S-*` survey stubs have no permits, years or responsible person.
- Names are reproduced as recorded, including typos in the English fields
  (“survay”, “Exx&survey”).
- Figures and report text remain © Israel Antiquities Authority; this is a
  working research copy, not a redistribution.
