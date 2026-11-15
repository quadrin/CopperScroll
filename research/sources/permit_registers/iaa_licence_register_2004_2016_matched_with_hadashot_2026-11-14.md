# IAA excavation licence register 2004–2016 matched with Hadashot: 3,840 permits, 2,351 with their own report; 202 permits in the project area have no report of their own — 14 November 2026

## Result first

- The register that the owner saved from the Wayback Machine (Google Sheet "IAA Excavation Licence Register 2004–2016 (Wayback archive)", 12 November) is now **one table of 3,840 permits** (English pages 2004–2015, Hebrew pages 2004–2016).
- Each permit was looked for in the text of the 4,667 Hadashot reports (English and Hebrew, `hadashot/derived/hadtext_pdftotext.tgz`):
  - **report**: the permit is in the report's own opening statement ("Permit No. …", "הרשאה מס' …"): **2,351** (61 %).
  - **cited only**: the permit is in other reports only, as a reference to an earlier dig: **390** (10 %).
  - **none**: in no report: **1,099** (29 %).
- By permit type: A (IAA salvage) 69 % with a report; G (licensed academic) 96 %; S (survey) 24 %; B (other bodies) 9 %.
- **Project area** (centre within 10 km of an atlas place, or a Jerusalem site name with no position): **202 permits without their own report** (160 none, 42 cited only). 35 are within 2 km of an atlas place. All are in Jerusalem and round Tell el-Ful. The register has no permits at Jericho, Qumran or in Samaria: those are Staff Officer for Archaeology licences, which are in the WBADB register (1,177 entries, work pass 2 of 9 November).
- **Water works among them, with no Hadashot report of their own:**

| Permit | Year | Site (Hebrew title of the register, translated) | Excavators |
|---|---|---|---|
| A-4077, A-4359 | 2004, 2005 | Spring House expedition (Kefar ha-Shiloaḥ) | Reich, Shukron |
| A-4709, A-5082 | 2006, 2007 | City of David, Spring House | Reich, Shukron |
| A-4720, A-5029, A-5339 | 2006–2008 | Siloam Pool | Reich, Shukron |
| A-5760, A-5850, A-5852 | 2009–2010 | City of David, drainage channel from the Yovel complex (to the Givati car park) | Reich, Shukron |
| A-6827 | 2013 | Old City, Western Wall excavations (drainage channel) | Shukron |
| A-6692 | 2013 | City of David, Jeremiah's Cistern | Uziel |
| A-6828 | 2012 | Mar Elias (Har Homa – the aqueduct) | Be'eri |
| A-6805 | 2013 | Jewish Quarter, link between the Cardo and the Ḥurva synagogue | Gutfeld, Geva |
| A-6046 | 2010 | Christian Quarter, Tanners' Street | Lavi |

- "No Hadashot report" does **not** mean "unpublished". The Reich–Shukron work at the spring and the pool is published in other journals and books. The table says only that Hadashot has no report of its own for these permits; the project's notes on Siloam must say which publication covers each permit.

## Method

1. The 28 tabs were joined on the permit number. Rows that repeat a permit were dropped; English and Hebrew rows of the same permit were joined. Result: 3,840 permits.
2. Permits in the report text: pattern letter–number (A, B, G, S, L). The report's own permits are the numbers within 90 characters after the first "Permit/License/הרשאה/רישיון" in the first 2,500 characters; every other number is a citation.
3. Positions: the report's map reference ("map ref." or "NIG", 4–6 digits, read as Israel grid; 13 old reports as Palestine grid) for 4,464 reports. A permit without a report gets a position only if earlier permits with the same site name have reports that lie within 1 km of each other (434 permits). General names such as "Jerusalem" get no position.
4. Atlas places: the 59 rows of `sites.csv` of the atlas input.

## Checks

- 15 random matches of "report" in the project area: the permit is the report's own in all 15.
- 8 random "cited only" permits: all 8 are references to earlier digs in another report.
- In 40 random type A permits with no match from the English opening alone, 12 were in the Hebrew opening or elsewhere; the method now reads the Hebrew text too.

## Limits

- The 2011 and 2012 tabs are short (49 and 119 permits against 310–390 in other years); the Wayback captures of those years are partial.
- A permit printed without its hyphen (for example "A4183") is not found.
- Map references in Hadashot have known errors (side quests B1b, B1c): about 1 % of reports have a wrong grid.
- Positions from a site name are approximate (up to 1 km).
- Reports in ʿAtiqot or other journals are not matched; a permit with no Hadashot report can have a full publication elsewhere.
- No status, rating or candidate depends on this table.

## Not done

- For each water-works permit above, the publication that covers it (the Siloam notes of the repository list the Reich–Shukron papers).
- The WBADB (Staff Officer) register against Hadashot in the same way, for Jericho, Qumran and Samaria.

## Where the files are

- Drive, beside the register sheet: `licence_register_2004_2016_matched_to_hadashot.csv` (3,840 rows: permit, year, type, status, site in English and Hebrew, excavators, Hadashot report ids — own and citing — position, its source, nearest atlas place and distance) and `project_area_permits_without_own_hadashot_report.csv` (202 rows).
- Session: `/home/claude/cs/lic/`.

No rating or candidate was changed.
