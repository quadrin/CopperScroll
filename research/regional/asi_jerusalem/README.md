# ASI survey records near the project's places

**What it is.** The Archaeological Survey of Israel (ASI) site records near the project's 48 placeable places, read from the IAA's open survey database and coded for features, periods and distances. They include Kloner's three *Survey of Jerusalem* volumes and the Judean Desert maps of Patrich (Mar Saba), Sion (Wadi Qelt, Kalia) and Hirschfeld (Herodium).\
**Main result.** 1,258 records from 17 maps lie within 3 km of a place, and 211 lie within 1 km of a Jerusalem place. In those 211, the records' own sentences date 182 feature mentions at 70 sites fully in the window. Almost all are Herodian tombs and caves. Only six water features at four sites are dated fully in the window. The looks table has 133 rows: 71 reported and 62 silent. Ten rows have a stated coverage, and none has a detection rate.\
**What stays unknown.** No ASI record lies inside the Old City walls, so the Temple enclosure, Bethesda and the walled Tyropoeon have no ASI coverage. The online records give no printed page numbers and no detection rates. No online sheet covers Tell es-Sultan, Kh. Qumran, ʿEin Feshkha or ʿEin el-Ghuweir.

Exploratory, 9 October 2026 (UTC). No identification claim. No registered result, outcome count or closed test changes. Labels: EVIDENCE (what a record says), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record).

## Plan freeze

- plan.json SHA-256: `19f91bc5f29aa58bbc954bb525ab72c26239ca222c170ed45043bab5a858f230`
- Frozen: 2026-10-09T22:17:17Z (UTC), before any site was coded.
- plan_amendment_1.json SHA-256: `8510259e6775e1a4ef888d4ec1fb42dbbd46de5a3b7e43d7786e314d825d4414`
- Frozen: 2026-10-09T22:22:11Z (UTC), before any site was coded. Reason: the server is slow (fetch order only).
- plan_amendment_2_posthoc.json SHA-256: `35c08513dcdbf16bdd60fe8329efa4c773d0d52c1867f8e10130dd0a9ceb3c90`
- Written: 2026-10-09T22:36:30Z (UTC), AFTER a first build was inspected. It is a post-hoc Hebrew check in a separate file. The frozen columns stay as they are.

Exposure before the freeze is listed in plan.json. Correction: amendment 1 says four Map 22 records had been fetched; the first run had fetched seven (Map 22 sites 1–7) before it was stopped. Only the field names of two records were printed.

Changes after the first build, none of which changes a class, a date or a look: a feature found only in the record's "Finds" term list is quoted as that one term, not as a 12-word window of the list; the raw "Finds" list is not stored in sites.csv; seven early responses were added to the source manifest.

**Post-freeze deviation: quotes cut back (9 October, at the integrator's request).** Reason: to limit aggregate reproduction of the ASI descriptions. The first build held 4,890 feature quotes (up to 21 per record) and 1,258 site quotes; each was 12 words or fewer, but together they could rebuild much of the copyrighted text. The plan files were not changed; only the build was. Now:
- features.csv has an empty `quote` column. `matched_text` keeps the single matched term, and `citation` points to the record.
- sites.csv has at most one quote per record (the first 12 words or fewer of the description), and only for the 315 records within 1 km of a place. The other 943 records have an empty quote.
- coverage_statements.csv keeps its 15 short quotes from the map introductions; looks_asi.csv repeats them in its basis columns.
- Result: 315 site quotes, 3,754 quoted words in sites.csv; 0 feature quotes. No class, date, distance or look changed.
- The quotes in the "Results by place" section below were taken from the records while coding. They are 12 words or fewer each.

## Files

| File | What it holds |
|---|---|
| access.md | What was tried, the data services, failed links, what a person would need to open |
| plan.json, plan_amendment_1.json | Frozen rules |
| plan_amendment_2_posthoc.json | Post-hoc Hebrew word rule (exploratory) |
| coverage_statements.csv | Coverage and detection statements from each map's introduction, with quotes of 12 words or fewer |
| sites.csv | One row per ASI record within 3 km of a place (1,258); a quote only for the 315 within 1 km |
| features.csv | One row per (record, feature class) (4,890); matched term, no quote |
| place_summary.csv | Counts per place within 1 km and 3 km |
| looks_asi.csv | Looks in the column schema of `research/models/search_effectiveness/looks.csv` (133) |
| maps_used.csv | The 18 selected maps, sheet bounds, record counts, introduction hashes |
| hebrew_check_v2.csv | Post-hoc Hebrew classes per record |
| sources_manifest.csv | URL, HTTP status, size, SHA-256 and fetch time of all 457 responses read |
| scripts/ | `fetch_asi.py` (download to a cache outside the repository), `build_asi.py` (tables), `asi_common.py` |
| tests/ | unittest |

No description text, page image, plan or map scan is stored. Quotes are 12 words or fewer, and only sites.csv (315 records) and coverage_statements.csv carry them.

## How the tables were built

- Source: the IAA survey database at survey.iaa.org.il, through the JSON services that its own page calls (access.md). Kloner's volumes give a full English translation of the Hebrew text (Kloner's preface in the Map 101 introduction). The Benjamin survey's English text is a summary; the Hebrew is fuller (Map 102 introduction).
- Maps: every online map whose sheet lies within 3 km of a placeable place (18 maps). Map 64 (Bet Yosef) has no record within 3 km.
- Sites: records within 3 km of any placeable place. The full record (GetSiteDesc2) was fetched for all 315 records within 1 km of a place, and for 3 more. The other 940 records use the database GeoJSON point and text.
- Coordinates (W2B conventions): the record's New Israel Grid value, read as northing and easting (the larger number is the northing), converted EPSG:2039 → EPSG:4326 with pyproj `Transformer.from_crs(..., always_xy=True)`. Distances are haversine with R = 6371.0088 km, as in W2B `scripts/grid_convert.py`. Check: the converted point lies 9.2–10.4 m (median 9.8 m) from the record's own WGS-84 value in all 318 records. INFERENCE: the database uses a different datum shift; 10 m does not matter at the 1 km scale. Records without a fetched record use the database point and carry that same offset.
- Feature classes: 30 keyword classes (plan.json). Names follow the project's landmark classes (T02 `entry_features.csv`) where one exists. A class is coded when its word occurs in the name, additional names, "Finds" term list, description or finds note. Bibliography is excluded.
- Periods: recorded as given. A feature is "dated in window" only when a period label stands in the same description sentence as the feature word: `yes` if every label is in the window (Hasmonean, Herodian, Early Roman, first century BCE or CE, Bar Kokhba), `partly` if some label overlaps it (Hellenistic, Roman, Second Temple, Middle Roman), `no` if all labels fall outside, `unknown` if none. Site pottery and the record's "Period" list never date a feature; they set `site_finds_in_window` only.

## Results by place

Distances are from the place point in `places_v2.csv`. Site numbers are "map/site". Dates are as the record gives them.

### Jerusalem (Kloner, Survey of Jerusalem; Maps 102, 105, 106)

| place | records ≤1 km | ≤3 km | features dated yes / partly (≤1 km) |
|---|---|---|---|
| jer_temple | 57 | 432 | 38 / 40 |
| jer_east_gate | 52 | 433 | 41 / 41 |
| jer_se_corner | 50 | 411 | 44 / 40 |
| jer_south_wall | 53 | 406 | 48 / 44 |
| jer_tyropoeon | 59 | 426 | 38 / 45 |
| jer_bethesda | 53 | 450 | 44 / 45 |
| jer_kidron_mon | 46 | 409 | 50 / 44 |
| jer_kidron_east | 45 | 385 | 52 / 43 |
| jer_gethsemane | 45 | 431 | 40 / 40 |
| jer_siloam | 50 | 367 | 66 / 33 |
| jer_bir_ayyub | 64 | 355 | 75 / 31 |
| jer_tombs_kings | 38 | 421 | 33 / 20 |
| mount_zion | 59 | 378 | 50 / 40 |
| jer_baqa | 17 | 284 | 17 / 11 |
| ramat_rahel | 22 | 156 | 9 / 18 |
| tell_el_ful | 25 | 230 | 10 / 5 |

(`place_summary.csv` holds the exact counts per class.)

- **The walled Old City: jer_temple, jer_east_gate, jer_se_corner, jer_south_wall, jer_tyropoeon, jer_bethesda.** EVIDENCE: no Map 102 record lies inside the walls. INFERENCE: the survey did not inventory the walled city; no introduction read here says so. The nearest records lie just outside: 102/409 Gate of Mercy, a "Second Temple period residential quarter"; 102/414 ʿOfel, "Rock-hewn miqva’ot of the Second Temple period"; 102/417 City of David, a plastered cistern "containing Herodian potsherds" and miqvaʾot; 102/345 Lions' Gate (Finds term "Ritual bath"; a channel of Crusader to Ottoman date). The Bethesda pools, the Temple Mount cisterns and the Golden Gate itself have no record. Every "reported" look at these six places rests on records outside the walls.
- **jer_siloam (entry 49).** No record describes the Siloam pool or the Siloam tunnel itself. 102/485 City of David (south), 0.13 km: "Probably retaining walls related to the Siloam pool"; Period list Hasmonean, Herodian, Second Temple period. 102/416 City of David, 0.30 km: the tel "above the source of the Gihon spring"; no feature date. 102/417 and 102/418 hold conduits of Herodian to Ottoman date.
- **jer_bir_ayyub (entries 34, 45, 47).** 102/486 ʿEn Rogel lies 10 m from the place point: "Ancient well in Nahal Qidron"; Finds term "Well"; no period. No record within 1 km is coded basin (entry 47 basin: silent in Maps 102 and 106). The Ge Ben Hinnom tombs (102/481–484, 0.16–0.38 km) carry Second Temple and Herodian dates.
- **jer_kidron_mon (entries 2, 36, 48, 51).** 102/410, 0.05 km: "Herodian-period nefesh (monument)" (Absalom's Tomb) before the Cave of Jehoshaphat. 102/411, 0.06 km: the Tomb of Bene Ḥezir and the "Tomb of Zachariah"; Period list Hasmonean; the description gives no feature date. 102/412, 413 and 415: rock-hewn "Herodian (?)" burial caves; 102/413's Finds list includes "Miqveh".
- **jer_kidron_east (entries 52–54, 56).** 102/420 Kefar Ha-Shilloah (Silwan), 0.04 km: 48 Iron Age II monuments and burial caves. The record adds kokhim "apparently from the Herodian period", but the frozen sentence rule codes the tomb class "no" (Iron Age), because the record splits that clause into its own sentence. This is a known miss of the rule.
- **jer_gethsemane.** 102/407 (Mount of Olives; Period list Herodian, Crusader), 102/406 Tomb of the Virgin (conduit, Roman and Byzantine), 102/424 Dominus Flevit cemetery (Hasmonean and Herodian caves).
- **jer_tombs_kings (entry 27).** 102/320, 0.01 km: the Tombs of the Kings, "Tomb of Queen Helene of Adiabene"; "two cisterns in its floor served as miqva'ot". Period list Herodian, Roman, Late Roman, Byzantine. 102/330 Nablus Road, 0.36 km: pools, a cistern and conduits in a sentence dated "first century CE".
- **mount_zion (Koḥlit proposal; entries 4, 11, 15, 19, 60).** 102/405, 0.04 km: the south spur of the Upper City, miqvaʾot and fortifications. 102/402, 0.19 km: an Iron Age II burial cave and the aqueduct "leading from Solomon’s Pools to the Temple Mount". 102/478, 0.34 km: St Peter in Gallicantu, "Rock-hewn miqva’ot of the Second Temple period". 102/399 Birket es-Sultan (reservoir; Late Roman, Byzantine, Second Temple).
- **jer_baqa (entries 36, 37).** 17 records within 1 km, from Maps 102 and 106: Herodian burial caves (102/461–463, 106/6, 106/8) and 106/4 Naḥal Aẓal, a conduit in a sentence of Hasmonean to Ottoman dates.
- **ramat_rahel (entry 46).** 106/95 Ḥ. Ẓewaḥa (additional names "Ramat Raḥel, Kh. Ṣaliḥ"), 0.22 km: a fort, a columbarium, "reservoirs and five ritual baths"; Period list Iron Age II to Early Arab, including Hasmonean and Herodian. Its reservoir and pool rows are "partly" in window. 106/96, 0.32 km: a Herodian burial complex.
- **tell_el_ful (entry 43).** 102/79 Giv'at Sha'ul (= Tell el Ful), 0.07 km: the tel; Period list from Middle Bronze II to Mamluk, including Hasmonean and Herodian. No pit is dated in the window.
- **jer_shaveh** has no coordinates and gets no row.

Water features dated fully in the window within 1 km of a Jerusalem place (all six): 102/330 cistern, pool and conduit ("first century CE"; jer_tombs_kings 0.36 km); 102/460 conduit (Hasmonean; mount_zion 0.56 km, jer_bir_ayyub 0.64 km); 102/464 conduit ("Hasmonean or Herodian"; mount_zion 0.74 km); 102/241 reservoir (Herodian; jer_tombs_kings 0.92 km). INFERENCE: in 102/241 the date belongs to a burial cave in the same sentence, not to the reservoirs. So the rule can attach a date to the wrong feature.

### Judean Desert (Patrich, Map 109/7; Sion, Maps 109/4 and 109/5)

- **mar_saba (entry 35).** Nine records within 1 km. 109/7/96–98 hold the plastered cisterns, reservoirs and conduits of the laura and of Deir Maqtal el-Ghuweir. Where a Period list is given, it is Byzantine or later. No feature is dated in the window.
- **hyrcania (entries 16, 29, 35).** 109/7/70 Hyrcania, 0.09 km: "Remains of Hasmonean fortress on summit" (fortress: yes); "Some twenty cisterns and reservoirs"; the conduit sentence is Byzantine. 109/7/69 Naḥal Sekhakha, 0.16 km: a bridge with "the Herodian channel on top of the bridge" (conduit: yes); four lower courses "are Hasmonean". 109/7/67 and 109/7/90 hold conduits "partly" in window.
- **buqeia (entries 1, 17).** Six records within 1 km. 109/7/91, 0.33 km: an Iron Age II casemate fortress. No feature is dated in the window. The place has σ 2.5 km, so 1 km samples a small part of it.
- **muhalhil (Koḥlit proposal; proxy point at Nebi Musa).** Two records within 1 km, both tombs (109/5/96 Sitna ʿAisha; 109/5/95). EVIDENCE: Sion's Kalia map records "Tell Muhalhal (1)" to "(9)" (109/5/83–87, 97–100) 1.0–1.9 km from the proxy point: stone fences, enclosures, building bases and stone heaps. None has a Period list in the database. This bears on looks L05, L22 and probes P03 and P04 of the search-effectiveness model (Bar-Adon 1972).
- **asla (entry 18).** Six records within 1 km (caves, conduits); none dated.
- **kuteif (entry 24).** Four records within 1 km: stone groups, a guard tower (109/4/66) and a compound. No tomb.

### South (Hirschfeld, Map 108/2)

- **natuf (entries 38, 40).** 108/2/17 Kh. Khureitun "Identified as Monastery of Chariton", 108/2/26 the "Hanging Cave" and 108/2/27: cisterns, a pool, conduits and the spring. Dates are Byzantine. No dovecote is coded within 1 km (entry 38: silent, coverage 1.0).
- **tekoa_herodium (entries 39, 42–45).** No record within 1 km of the sector point; 26 within 3 km. The place has σ 4 km.

### Jericho area (Maps 109/4, 109/5, 83/12)

- **choziba (entry 32).** 109/4/8 St George's monastery, 0.01 km (tomb, cave); 109/4/20 Manzal Jabr, a reservoir and conduit; 109/4/17–18, channels called "modern". Entry 32's landmark (an outlet) is not a lookable class, so it has no look row.
- **jericho_palaces (entry 29).** 109/5/14 Tell el-ʿAlaiq (6), "Kind of site: Hasmonean palaces"; 109/5/12, pools (Period list Early Bronze Age, Early Roman); 109/5/16 Birkat Musa, "A reservoir measuring 146 × 175 m". The Kalia records put most dates in the Period list, not in the sentences, so most of their features are "unknown" by the frozen rule.
- **ain_duk (entries 1, 17, 29, 31)** and **iv17_abu_saraj (entry 25).** Two records within 1 km of ʿAin Duk: 83/12/103 ʿEin en-Nueimeh [424], "Traces of walls. Neolithic sherds", and 83/12/104. 83/12/103 is the only record within 1 km of IV/17 (0.66 km). The Abu Saraj cliff lies just east of the online Map 83/12 sheet. No ASI record here names IV/17 or describes a cave mouth. These are not the IAA Archive cave records of the arrival register, and the frozen Entry 25 / IV/17 rules were not applied to them.
- **doq, tell_es_sultan, tell_el_qos, jericho_area, jordan_ford, nuweimeh.** No record within 1 km. The Map of Jericho is not online. 18 records lie 2–3 km from Tell es-Sultan in Maps 83/12 and 109/5. None lies within 1 km, so no record describes the protected strip north of the tell (`protected_zone_nearby` is "no" for every row).

### Other regions

- **beth_horon (entry 40).** 83/1/48 Beit Ur el-Fauqa [143], 0.01 km: the same record that `registration/entry40_sources_extracted.md` read on 29 September. Its dates use "Rom", which is "partly" in window.
- **carmel_siah** (Map 22, 19 records within 1 km), **beth_shean** (Map 63, 11), **kuhlah** (Map 140, 8). No feature is dated fully in the window.

## Places with no ASI record within 1 km

tell_es_sultan, tell_el_qos, jericho_area, jordan_ford, nuweimeh, doq, tekoa_herodium, kh_qumran, wadi_qumran, ein_feshkha, ein_ghuweir, gerizim, ibziq, kh_salhab, kh_yanun, ein_samiya, beit_kahil. jer_shaveh and transjordan have no coordinates.

- No online sheet lies within 3 km of ein_feshkha, ein_ghuweir, gerizim, ibziq, kh_salhab, kh_yanun, ein_samiya or beit_kahil.
- Kh. Qumran and Wadi Qumran lie 2.3–2.4 km south of the Kalia sheet (109/5), the nearest online sheet. Map 109/5 holds two records within 3 km of Kh. Qumran and one within 3 km of Wadi Qumran.
- Tell es-Sultan, Tell el-Qos, the Jericho oasis point, the Jordan ford, Wadi Nuweiʿimeh and Jebel Qarantal lie in or near the Map of Jericho, which is not online.
- tekoa_herodium lies inside the Herodium sheet, but no record lies within 1 km of its point.

## The looks table

`looks_asi.csv` uses the exact columns of `research/models/search_effectiveness/looks.csv`. One row per (candidate pair in `candidates_v2.csv`, lookable landmark class of the entry in T02 `entry_features.csv`, map whose sheet lies within 1 km of the place). "Reported" means at least one record of that map within 1 km is coded in the crosswalk class. "Silent" means none is. No row codes an explicit absence.

- 133 rows: 71 reported, 62 silent. Every reported row has `satisfies_requirement` = unknown.
- Coverage is filled (1.0) only where the introduction states a full-area survey and the place's 1 km circle lies inside that sheet: nine Herodium rows (natuf, tekoa_herodium) and one Kalia row (asla). All other coverage values are null, with the introduction's words in `coverage_basis`.
- `p_recognise`, `p_report` and `p_survive` are null in every row. Four introductions limit detection in words: Kloner's teams "were often unable to locate and record all" remains (Maps 105, 106); Sion's Kalia survey says "small sites, for various reasons were not recorded"; Hirschfeld investigated "Some of the many caves and rock shelters located in the area"; the Benjamin survey finds it "conceivable that additional small sites will yet be discovered".
- Each map is its own lineage. Map 102 mixes two field surveys (Kloner's and the Benjamin survey of Dinur and Feig). The Jerusalem records also compile earlier publications and excavations, so they are not independent of the excavation reports the project already uses (Kloner, Map 101 introduction).
- INFERENCE: with every detection number null, these rows add no factor in the search model (its rule: any null number makes the factor 1).

## Open questions this bears on

- R06 (entry 49, Siloam): the ASI has no record of the Siloam pool or tunnel themselves; 102/485 and 102/416–418 are the nearest records. Nothing here tests the L103 junction.
- R07 (Koḥlit, Achor, Sekakah): the Tell Muhalhal records 109/5/83–100 near the muhalhil proxy; Buqeia records in Map 109/7; no online sheet covers Tell es-Sultan or Wadi Nuweiʿimeh.
- R03 (entry 32, Choziba): Map 109/4 records at St George's; none is a dated outlet or wall.
- R04 (entry 40, Beth-Horon): 83/1/48 [143] is the record already read; nothing new.
- R02 (entry 25, IV/17): no cave record near Abu Saraj in the online maps.
- The Jerusalem entries without an R number (entries 2, 27, 34, 45–48, 51–56): the records above give a dated inventory for the Kidron, Siloam, Bir Ayyub and Tombs of the Kings areas, and show that the walled city is not covered.

## Known limits of the frozen rules (measured)

- Keyword noise: "H. " initials code 18 rows as settlement_ruin; "Tel"/"Tell" in names codes 55 rows as mound; "Solomon's Pools" codes a pool at 102/460; "well-constructed" codes spring_well at 109/7/69; OCR errors such as "rniqva’ot" (102/418) miss a pool.
- The period rule needs the label in the same sentence. Abbreviation full stops split sentences (102/420). The Benjamin abbreviation "R" (Roman) is not in the lists; "Rom" is. Twelve rows carry the lowercase word "iron" as a period label.
- The frozen Hebrew check over-reports: "בור" matches inside "קבורה" (burial), "מער" inside "מערב" (west). Frozen `heb_only_classes` flags 465 cisterns and 273 caves. The post-hoc whole-word rule (hebrew_check_v2.csv) flags 205 cisterns and 10 caves. INFERENCE: most remaining Hebrew "בור" are standing pits in tombs ("בור עמידה") or winepress vats ("בור איגום"), not cisterns. Neither Hebrew flag changes features.csv or looks_asi.csv.
- 940 of 1,258 records (all beyond 1 km of every place) were coded from the database GeoJSON text, without the record's "Finds" and "Period" fields.

## Run and test

From the repository root:

```
python3 -I research/regional/asi_jerusalem/scripts/fetch_asi.py CACHE_DIR      # fetch (slow: 10–40 s per record)
python3 -I research/regional/asi_jerusalem/scripts/build_asi.py CACHE_DIR      # rebuild the tables
ASI_CACHE=CACHE_DIR python3 -I -m unittest discover -s research/regional/asi_jerusalem/tests -v
```

The tests check the plan hashes against this README, the CSV schemas (looks_asi.csv against looks.csv), quote length (12 words or fewer), the quote limits of the post-freeze deviation (no feature quotes; site quotes only within 1 km), the period and grid rules, and, with the cache, that two builds are byte-identical and equal to the committed tables and that every coverage quote occurs in its introduction. Without ASI_CACHE the two cache tests are skipped. All ten pass with the worker's cache (9 October).

## Failed links

- https://www.antiquities.org.il/survey/new/default_en.aspx: HTTP 301 to https://www.iaa.org.il/ (the old survey site is gone).
- https://zenon.dainst.org/Record/000052795, /000050598, /000207352 (catalogue records of Kloner's volumes): bot wall, "Access Denied".
- `Service_Eng.aspx/GetMapNameAndId` without `typed`: HTTP 500.
