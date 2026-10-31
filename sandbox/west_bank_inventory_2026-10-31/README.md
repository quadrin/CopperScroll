# West Bank inventory: WBADB added as a fifth inventory, 31 Oct 2026

Owner request, 31 Oct 2026 09:43 America/Los_Angeles: "yes go for these" (add the West Bank database as a fifth inventory, with attribution). Exploratory sandbox data. Nothing here changes ratings, the ledger, ACTIVE_TEST or atlas data.

## Source and attribution

**West Bank and East Jerusalem Archaeological Database (WBADB).**
- Raphael Greenberg and Adi Keinan, Tel Aviv University and Emek Shaveh, 2009.
- It is the database behind R. Greenberg and A. Keinan, *Israeli Archaeological Activity in the West Bank 1967–2007: A Sourcebook* (Jerusalem: Ostracon, 2009).
- Project page: https://www.tau.ac.il/humanities/abraham/archaeological-database.html

**Public file.** https://www.tau.ac.il/humanities/abraham/publications/archaeological.xls, downloaded 31 Oct 2026.
- SHA-256: 1f1638756ea589b4f7548b5433072335f9407885323563f327d87b6d460bca53.
- Sheets:
  - Surveyed: 5,980 sites.
  - Excavations: 970 sites.
  - License List: 1,181 permits issued by the Staff Officer for Archaeology, 1968–2007.

**Licence.** None is stated. The raw file is not in this repository; `scripts/build_inventory_v2.py` fetches it and checks the hash. The derived table keeps facts only: names, grid references, periods, component lists, survey references and licence numbers.

## Files

| File | Rows | What it is |
|---|---|---|
| `data/wbadb_sites.csv` | 6,950 | Both site sheets, with Old Israel Grid and WGS84 coordinates, periods (Hellenistic and Roman flags), component list and parsed classes |
| `data/features_unified_v2.csv` | 16,383 | Lane J's unified table (7,366 rows, `claude/novel-2026-10-30-J` 7b58cf0), plus one row per WBADB site and class (9,017 rows, `inventory` = `WBADB_S` or `WBADB_E`) |
| `scripts/build_inventory_v2.py` | — | Rebuilds both tables from the public file |

**Coordinates.** Converted from the Old Israel Grid with EPSG:28191, the convention of the W2B grid conversions. A check against the project's place points:
- Kh. Qumran 76 m, Hyrcania 74 m, Tell es-Sultan 72 m, Mt Gerizim 67 m, ʿEin Feshkha 266 m.
- Survey points mark site centres, not features.

**Classes.** Parsed automatically from the component text, with the same ten classes as lane J. The patterns are in the script. "Installation", "press" and "cupmark" count as rockcut, which makes that class broad. The parse is not hand-checked.

## Effect, measured against the 1940s map features

This check is exploratory. Benchmark B of run 26 has now been seen against this file, so it can no longer serve as an unseen check.

| Same-class record near a 1940s mapped feature | Lane J only | With WBADB |
|---|---|---|
| In the same 300 m cell | 0.27 | 0.36 |
| Within 300 m | 0.36 | 0.57 |
| Within 1 km | 0.52 | 0.82 |
| Desert windows, within 1 km | 0.42 | 0.92 |

Of 3,463 WBADB sites inside the run 26 study cells, 1,301 (38 %) have no lane J record within 300 m. That includes 532 in the Judean Desert and 147 around Gerizim, where lane J has 6 records.

## Limits

- The data end in 2007.
- Components are listed per site, not positioned.
- Surveys overlap one another and the cave survey. Duplicates do not change cell presence, but they raise other-class richness counts.
- Post-2007 work by the Civil Administration (for example the 2017–18 Qumran cave licences) is not included.
