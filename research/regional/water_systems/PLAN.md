# Water-systems lane: frozen plan (10 October 2026 UTC)

Exploratory regional inventory and count. It makes no identification claim, changes no registered outcome and does not reopen the closed entry 29 result (`research/assessments/entry29_jericho_pools/`). Labels: EVIDENCE (the source says it), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record). Unknown stays unknown (null), never zero. Rules of `AGENTS.md` and the lane rules apply.

## 1. Question

Within a fixed region, how many recorded ancient water installations satisfy each clause of the scroll's water entries 21, 22, 29, 32, 42, 45 and 46, how many fail and how many are unknown? Each result is reported as "k match, f fail, m unknown, of N", per entry, per reading branch and per source lineage. Entries 11 and 60 are counted elsewhere (`research/rarity/kohlit/`) and are not repeated.

## 2. Region (fixed before any record is coded)

- **Box:** WGS 84 (EPSG:4326) latitude 31.600–31.900 N, longitude 35.120–35.560 E, land west of the Jordan River and the Dead Sea shore only.
- Corners in the Israeli Transverse Mercator (EPSG:2039), easting/northing: SW 211443/611968, SE 253200/612019, NW 211469/645233, NE 253091/645285. In the Old Israel (Palestine 1923) Grid (EPSG:28191), as WBADB uses it: SW 161442/111966, SE 203199/112017, NW 161468/145231, NE 203090/145283.
- **Membership:** a row is in the region if its point (rules in §6) lies inside the box. A literature row without its own coordinates takes its site's point (§6).
- **Why this box.** It holds every place the lane brief names: the Jericho oasis and Naʿaran springs (north edge 31.90), Qumran, ʿEin Feshkha and ʿEin el-Ghuweir (south edge 31.60), Wadi Qelt with its springs, Hyrcania and the Buqeiʿa, Mar Saba, Herodium, Artas and Solomon's Pools, Jerusalem with its aqueducts, Ramat Raḥel and ʿEin Kerem (west edge 35.12), to the Jordan (east). Its edges are straight lines, not drawn round any candidate. The ʿArrub and upper Wadi Biyar aqueduct sources, Alexandrion, Phasaelis, Masada and ʿEin Gedi lie outside or on the edge; rows outside the box are not counted.
- **Uncovered:** the east bank of the Jordan (no source in the list covers it).

## 3. Sources (fixed list; nothing else enters a count)

Each source is its own **lineage**. Counts are reported per lineage and merged (§9).

1. **WBADB** (Greenberg & Keinan 2009), `WBADB_data1.xlsx`, SHA-256 `3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b` (the file is not committed). Both sheets. Text fields read: Site_Name, Other_Names, Site_Components, More_Components, Comments, More_Comments. Points: X/Y as EPSG:28191.
2. **ASI online maps** whose sheets meet the box and are online (checked 10 October): 101 Ein Kerem, 102 Jerusalem, 105 Bet Lehem, 106 Talpiot, 83/1 Ramallah, 83/2 El Bira, 83/12 Wadi el-Makokh, 108/2 Herodium, 109/4 Wadi Qelt, 109/5 Kalia, 109/7 Deir Mar Saba. One English GeoJSON call per map (`Service_Eng.aspx/GetPolygonsSites`), cached outside the repo, one request per 1.2 s, method as in `research/regional/asi_jerusalem/access.md`. Text fields read: name, additional names, description and finds, as present in the GeoJSON. Points: the GeoJSON WGS 84 point. Not online and so not covered: 83/13 (Jericho), 83/14, 108/1, 109/6, 109/8 (Qumran–Feshkha shore), 109/9, 109/10.
3. **HA-ESI lane rows**: `research/regional/haesi_features/features.csv` rows of type cistern, channel_aqueduct, pool_reservoir or ritual_bath whose point is in the box. Reused as coded there; not re-read.
4. **Literature** (hand-coded, one row per installation the source describes, or one aggregate row where the source aggregates). Only the listed pages:
   - a. Garbrecht & Peleg 1994, *BA* 57.3 pp. 161–170 (repo extraction `registration/garbrecht_peleg1994_extracted.md`; PDF in the owner's Downloads for checks).
   - b. Amit, Hirschfeld & Patrich (eds) 1989, *Ancient Aqueducts in the Land of Israel* (Hebrew), printed pages: Mazar, Jerusalem aqueducts survey pp. 169–195; Amit, Doq pp. 223–228; Meshel & Amit, Cypros pp. 229–242; Patrich, Hyrcania pp. 243–260; Netzer, Jericho estate pp. 273–281; Ilan & Amit, Qumran pp. 283–288; Hirschfeld, Martyrius irrigation gardens pp. 299–304; Hirschfeld, Chariton water supply pp. 305–312. Copy: owner's Downloads, SHA-256 `2330e0b31590057b26ffebdb56852e40ed78bf32b5e0b7453d293a1278abab15` (354 pp., no text layer; viewer page = printed + 13). Pages already extracted in the repo are read from those extracts.
   - c. Netzer's Jericho reports: the 28 records and 21 coverage notices of the entry 29 regional inventory (`research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.csv` and `.json`), reused as coded there; Netzer, "The Hasmonean and Herodian Winter Palaces at Jericho" (16-page PDF, all pages); Netzer 2001, *The Palaces of the Hasmoneans and Herod the Great*, only its passages on Jericho, Cypros, Doq, Hyrcania and Herodium water installations, found by a text search for pool, reservoir, aqueduct, cistern, channel, dam; Netzer 2001, *Hasmonean and Herodian Palaces at Jericho* I (final report), only its table of contents and the sections whose headings name pools or water installations, for installations not already in the 28 records.
   - d. Qumran: Magen & Peleg 2018 site description (repo extraction `registration/magen2018_extracted.md`, PDF for checks); Magen & Peleg 2007, *Back to Qumran* (JSP 18), its water-system section only; Galor, "Qumran's Plastered Pools: A New Perspective" (30-page PDF, all pages); repo extractions `registration/qumranII2003_extracted.md`, `registration/humbert_english_extracted.md`, `registration/qumran_waterworks_originals_2026-10-01.json`.
   - e. "The Desert Forts of Judea in Second Temple Times" (1975; 14-page PDF, all pages).
   - f. Repo notes already in the repository on Hyrcania (`registration/hyrcania_patrich1989_extracted.md`), Doq (`research/measurements/cycle11/doq_records.md`, `cycle8/doq_completed.md`), Wadi Qelt and Choziba (`research/sites/feature_investigation.md`), Siloam and Jerusalem pools (`research/measurements/cycle15/siloam_bathing.md` and the Siloam cycle notes), Ramat Raḥel and ʿEin Kerem (phase 2/5 summaries, findings log), Herodium (any repo note found by a grep for Herodium/Herodion with a water word). A note counts only for installations it describes with a page or figure of an original source.
5. **Not in the count:** the SWP *Memoirs* (grid squares of about 7 × 9 km are too coarse for clause positions; not read for this lane), the English *Aqueducts of Israel* (2002; interlibrary loan), DAAHL (blocked earlier), and any source not listed. The ʿAtiqot 41 cave entries, HA 28–29, Zertal vol. 4 site 194, *Highlands* pp. 700–702 and the IAA notices on Kh. ʿAlmit are protected Tier 1 records and are not read. WBADB and ASI summary rows are not those records; any WBADB/ASI row on Kh. ʿAlmit is flagged "first read after freeze".

## 4. Eligibility and installation types

A row is one installation record: one source record (WBADB row, ASI record, HA-ESI row, literature installation) and one type. A survey record naming several types gives one row per type. A row whose source gives a plural with no count is an **aggregate** (count null).

Types and the English words that code them in survey text (whole words, any case, plurals allowed):

| type | words |
|---|---|
| aqueduct | aqueduct, conduit, water channel, channel, canal, water tunnel, siphon, water pipe, pipeline |
| dam | dam, weir, barrage, dike, dyke |
| reservoir_pool | pool, reservoir, birka, birke, birkeh, birket, birkat, open tank |
| cistern | cistern, water hole |
| well | well (not "well-" compounds, "as well", "well known") |
| spring | spring, spring-house; a name beginning ʿEin, ʿAin, ʿEn, Ein, Ain or En followed by a space |
| basin_tank | basin, tank, trough, settling tank |
| outlet | outlet, sluice, spillway, overflow, inlet, intake |
| waterfall | waterfall, cascade |
| water_system | water system, water installation(s), waterworks |

**Exclusions (survey text):** channel, basin, tank and trough are not coded in a sentence that names a wine press, winepress, oil press, olive press, press or treading floor; "swimming pool" is not coded; a pool word inside the phrase "from/to/towards/leading … Solomon's Pools" is not coded as a pool of that record unless the record's own name contains Solomon or Birak/Birket Suleiman (disclosure: the ASI lane reported this noise at ASI 102/460). Ritual baths (miqveh, miqva'ot, ritual bath) are not a type of this lane; a stepped installation enters only if the source also calls it a pool, reservoir or cistern.

Literature rows use the same types, assigned by the coder from the source's own words.

## 5. Clauses, branches and codes (fixed from the readings before any record is coded)

Readings from `text/readings.json` and `tables/entry_concordance.csv` (Puech 21–46 = Lefkovits 21–46 = Milik 23–48). Each clause is coded MATCH, FAIL or UNKNOWN per row. **Silence is never FAIL**; FAIL needs a positive statement in the source that contradicts the clause. A clause that every installation trivially satisfies, or that names an unlocated place, is recorded as "not scored" and counts nothing.

**Survey text (WBADB, ASI).** A clause word counts only in the same sentence as the row's feature word (sentences split at full stops and semicolons). Words: great = great, large, big, huge, main, largest, enormous; northern = north, northern; plaster = plaster, plastered; entrance = step(s), stair(s), staircase, stepped, entrance, doorway; head = head, intake, begins, starts, source; marker = stone, boulder (S-stone), pool, basin, reservoir (S-pool), either or dam, structure (S-any), and only in a sentence that also has a head word; bend = bend, turn, curve, elbow; wall = wall, row of stones, retaining wall, course; fissure = fissure, crack, cleft, crevice; four sides = rectangular, square, quadrangular, oblong, or two dimensions "a × b" / "a by b"; not four sides = round, circular, oval, bell-shaped, pear-shaped, irregular, triangular. Literature rows are coded by the coder from the source's words and plans under the same definitions.

**Common clause, all entries: date.** `date_code`: `in` if a period label attached to the installation (literature: the source's dating of that installation; survey text: a label in the same sentence as the feature word) is in the window, Hasmonean to 135 CE (Hasmonean, Herodian, Early Roman, Late Second Temple, first century BCE or CE, Bar Kokhba, or a named builder/ruler of 167 BCE–135 CE); `in_hedged` the same with "possibly/probably/apparently/perhaps/may"; `partly` for labels overlapping the window (Hellenistic, Late Hellenistic, Roman, Middle Roman, Second Temple, second century BCE or CE); `out` if all labels are outside (Bronze, Iron, Persian, Late Roman, Byzantine and later, modern); `undated`. Site-level periods (WBADB flags, ASI period lists, site pottery) never date an installation; they go to `site_period_in_window` only. **Main rule:** `out` FAILs; all other codes pass. **Dated-only rule:** only `in` or `in_hedged` pass. **Strict-dated:** only `in`. The count "installations dated in the window" = rows with `in` or `in_hedged` (hedged reported separately).

### Entry 21 (V 1–4): head of the water conduit [ ] Sekakah, from the north, under the great [stone]
Eligible: aqueduct rows (a dam or intake row that a source makes the head of an aqueduct is coded on that aqueduct and not counted twice).
- **H (head):** MATCH if the source records the conduit's head, intake or upstream start (location or description). Otherwise UNKNOWN. Never FAIL.
- **Marker branches** (letters: only הגדולא survives): **S-stone** (Milik, Puech: [האבן]): MATCH if a stone or boulder is recorded at the head; **S-pool** (Allegro: "the pool"): MATCH if a pool, basin or reservoir is recorded at the head; **S-any**: MATCH if any built or natural feature (stone, dam, pool, basin, structure) is recorded at the head; **S-open** (no noun): no extra clause.
- **Direction branches** (מן הצפון, Lefkovits pp. 187–188, two senses): **N-side** (the deposit is on the north side of the head): under S-stone, S-pool and S-any the marker must be recorded on the north side of the head (315°–45°); a marker with no stated side is UNKNOWN; S-open adds nothing. **F-flow** (the water comes from the north): the marker clause applies without a side, and MATCH if the source states that the conduit comes from the north, or the head lies 315°–45° from the conduit's destination; FAIL if the source states another direction of origin, or head and destination are both located and the bearing lies outside 315°–45° (with the position rule of §6); otherwise UNKNOWN.
- **Branch combinations reported:** {S-stone, S-pool, S-any, S-open} × {N-side, F-flow}: eight. Headline "conduit heads with a stone or feature on the north" = S-stone × N-side and S-any × N-side.
- **Place (Sekakah)**: reported as a conditional column. **Q** (Puech: Kh. Qumran; Milik: Wadi Qumran): MATCH if the conduit leads to Kh. Qumran or lies in Wadi Qumran or the Buqeiʿa; otherwise FAIL under Q. **Any**: not scored.
- Depth (three cubits, restored): not scored.

### Entry 22 (V 5–7): the fissure in Sekakah, east of the reservoir of Solomon
Eligible: reservoir_pool rows. Sensitivity: reservoir_pool plus cistern rows.
- **Name:** MATCH if a source names the installation Solomon's (Solomon's Pool(s), Birak Suleiman) or identifies it with Josephus's "Pool of Solomon" (CLAIM). Otherwise UNKNOWN. Never FAIL.
- **Fissure east:** MATCH if a fissure, crack, cleft or crevice is recorded 45°–135° from the reservoir within 500 m (sensitivity 1 km), or the source says east of it. Otherwise UNKNOWN.
- **Place:** Q as in entry 21 (conditional column).

### Entry 29 (VII 3–7): the conduit of Qi◦[ ], the great northern reservoir, on its four sides
Eligible: reservoir_pool rows. Sensitivity: plus cistern rows. Only the counting below; the 24 cubits are recorded (dimensions column) but not tested.
- **Conduit:** MATCH if a conduit, channel or aqueduct feeds or joins the reservoir; FAIL if the source states its only supply is something else (a spring rising in it, direct runoff without a channel); otherwise UNKNOWN.
- **Great:** MATCH if the source calls it great, large, big, main or largest, or it is the largest by stated dimensions or capacity of two or more reservoirs of its site complex (one site in one source); FAIL if two or more reservoirs of the site complex have stated dimensions or capacities and it is not the largest; otherwise UNKNOWN.
- **Northern:** MATCH if the source calls it northern or places it north of its site, or the source's plan makes it the northernmost of two or more reservoirs of the site complex; FAIL if the plan places another reservoir of the site complex north of it; otherwise UNKNOWN.
- **Four sides:** MATCH if the source gives a rectangular, square or quadrangular plan, or length and width; FAIL if round, circular, oval, bell- or pear-shaped, triangular or irregular; otherwise UNKNOWN.
- **Qi◦ branches (conditional columns):** **Q-any** (Puech "collection of the waters"; Milik qy[ṣyṣ]): no place clause. **Q-Kidron** (Eshel): MATCH if the conduit draws on Wadi en-Nar / Nahal Qidron. **Q-Cypros** (Eshel): MATCH if the reservoir is at Cypros or its conduit leads there. **Q-Jericho** (Puech's restoration "of Jericho(?)"): MATCH if the reservoir lies in the Jericho oasis (Tell es-Sultan, Tulul Abu el-ʿAlayiq, Naʿaran, Doq, Cypros foot, Kh. el-Mafjar). Each branch is FAIL for rows with a located position elsewhere.

### Entry 32 (VII 14–16): the mouth of the water outlet of Kozeba, as far as the טור
Eligible: spring, aqueduct and outlet rows.
- **Outlet branches:** **O-spring** (a spring head): spring rows MATCH; **O-built** (a channel exit, junction or aqueduct head; Eshel: the head of a Qelt aqueduct): aqueduct rows with H = MATCH, and outlet rows, MATCH. A row of another type is not eligible in that branch.
- **Place branches:** **K-Qelt** (Kozeba = Wadi Qelt: Milik 1962 D20, Puech 2015 p. 67, Eshel): MATCH if the source names Wadi Qelt (Qelt, Kelt, Qilt, Nahal Perat/Prat) or a Qelt spring (ʿEin Fara/Perat, ʿEin Fawwar, ʿEin Qelt) or Choziba / St George / Deir el-Qelt for the row's place or supply; FAIL if the row is located and the source names another wadi for it; otherwise UNKNOWN. **K-Buz** (Lefkovits הבוזבא): place unlocated: not scored.
- **טור branches:** **T-wall** (Milik: retaining wall; Puech: wall courses/parapet): MATCH if a wall, row of stones, retaining wall or built course is recorded at the outlet; otherwise UNKNOWN. **T-mountain / T-rock** (Puech alternative; Eshel הסור): not scored.
- Count "outlets at a named wadi": eligible rows whose source names the wadi they lie in (any wadi), and the K-Qelt subset.

### Entry 42 (IX 11–13): the קול המים near לכפת ביב
Eligible: waterfall rows (branch **W-fall**: Puech, Høgenhaven), dam and reservoir_pool rows (branch **W-dam**: Puech's qyl reading).
- **Bend (Puech לכפת ביב):** MATCH if the source puts the row at or beside a bend, turn or curve of a conduit, or a coded conduit bend lies within 250 m (sensitivity 1 km); otherwise UNKNOWN.
- **Milik כפר נבו:** a village not located: not scored.
- East / distance (מזרח / מרחב): not scored.

### Entry 45 (X 3–4): the cistern גר of the channels watered from the great wadi
Branches: **C-plaster** (Puech בור גר, "(re)plastered cistern"): eligible cistern rows; clauses plaster, channels, wadi, great wadi. **C-open** (Lefkovits, same letters, sense obscure): cistern rows; clauses channels, wadi, great wadi. **M-well** (Milik, wheel-well): well rows; clauses channels, wadi, great wadi.
- **Plaster:** MATCH if plaster is recorded; FAIL if recorded as unplastered; otherwise UNKNOWN.
- **Channels:** MATCH if a channel, conduit or aqueduct is recorded feeding it; FAIL if the source states another feed only (roof or surface runoff directly, groundwater); otherwise UNKNOWN. In survey text the feed must be stated by a feed phrase in the same sentence (a verb such as fed, filled, supplied, diverted, led, conveyed, carried, brought, drained, joined to "channel/conduit/aqueduct/canal" and to the cistern), not by co-occurrence alone.
- **Wadi:** MATCH if the feeding channel draws on a wadi, stream bed or flood water; FAIL if the source states that the channel collects slope runoff or spring water instead; otherwise UNKNOWN.
- **Great wadi:** **G-strict**: MATCH if the source calls the wadi great, large or main, or the wadi is one of the region's trunk wadis that run from the Judean watershed to the rift, fixed here by name: Wadi Qelt (Nahal Perat), Wadi en-Nar / Kidron (Nahal Qidron), Wadi Mukallik (Nahal Og), Wadi Darajeh with its upper reach Wadi Khureitun (Nahal Darga / Teqoa), Wadi Nuʿeima. FAIL if the named wadi is another wadi. UNKNOWN if unnamed. (INFERENCE: the list rests on general map knowledge of the drainage, written before any row was coded.) **G-loose**: any wadi passes.
- "In its floor": not scored.

### Entry 46 (X 5–7): the reservoir in Beth ha-Kerem, as you go in, on its left
Eligible: reservoir_pool rows. Sensitivity: plus cistern rows.
- **Place branches:** **B-RamatRahel** (Aharoni; Milik 1962 p. 268; Lefkovits p. 333): MATCH within 1 km (sensitivity 2 km) of `ramat_rahel` in `places_v2.csv` (31.73999 N, 35.21899 E); FAIL if located beyond. **B-EinKerem** (Conder, SWP III p. 20): MATCH within 1 km (sensitivity 2 km) of Ein Karem, Wikidata Q1022487 P625 (31.766728 N, 35.161996 E; looked up 10 October before any row was coded); FAIL beyond. **B-any:** not scored.
- **Entrance ("as you go in"):** MATCH if the source records a way in: steps, a stair, a doorway or an entrance; otherwise UNKNOWN.
- "On its left", ten cubits / feet: not scored.

## 6. Positions, distances and bearings

- Survey rows: the record's point (WBADB X/Y via EPSG:28191 → EPSG:4326 with pyproj, `always_xy=True`; ASI GeoJSON WGS 84). Precision: WBADB 100 m if both X and Y are multiples of 100, else 10 m; ASI 50 m; HA-ESI its `precision_m`.
- Literature rows: (1) coordinates or a grid reference the source gives; (2) else the point of the WBADB or ASI record of the same named site, with precision that record's precision plus 250 m; (3) else the `places_v2.csv` point and its sigma; (4) else null (not in the box test; listed separately as "unplaced").
- Distances: haversine, R = 6371.0088 km. Bearings: grid north from the first point. A bearing or a "near" distance is computed only if the separation is at least 3 × the coarser precision; otherwise the clause is UNKNOWN unless the source states the relation in words. The source's own words and plans take precedence over computed bearings.

## 7. Deduplication and site complexes

- **WBADB ↔ ASI:** a WBADB row and an ASI record are the same site if the WBADB `Survey_Ref` cites "Kloner …, Site [MAP] N", "Patrich …, Site N" (ASI 109/7) or "Hirschfeld …, Site N" (ASI 108/2) and the ASI record is MAP site N; or, otherwise, both points lie within 300 m and the name skeletons match (kohlit stage 1b rule: consonant skeleton, difflib ratio ≥ 0.85). In a merged count the ASI record represents the site and the WBADB row is marked `dup_of`.
- **Literature ↔ survey:** the coder links each literature row to its site key. Survey rows of the same type whose site name matches the site key and whose point lies within 1 km are `superseded_by` the literature site in the merged count.
- **Across literature sources:** rows that the sources identify as the same installation share a `group_id`. Group clause: MATCH if any member MATCHes and none FAILs; FAIL if any FAILs and none MATCHes; CONFLICT (counted in m and listed) if both; else UNKNOWN.
- Corroboration is not added up: a group counts once.

## 8. Outputs

- `water.csv`: one row per installation record and type: id, lineage, source, locator (page, figure or record id), name, site_key, type, aggregate count, lat, lon, CRS, precision_m, coordinate source, feed, feed_wadi, dimensions as given, shape, plaster, entrance, great/north words, head recorded, head marker and side, flow-from, bend, wall at outlet, fissure, Solomon name, period as given, date_code, site_period_in_window, excavated, dup_of, superseded_by, group_id, quote (literature only, 12 words or fewer), SHA-256 of the text span read.
- `scores.csv`: one row per eligible row × entry × branch, with each clause code and the overall code.
- `counts.csv`: N, k, f, m per entry × branch × lineage (WBADB, ASI, HA-ESI, literature, merged) × date rule (main, dated-only), plus the headline counts of the brief: conduit heads with a stone or feature on the north (entry 21); reservoirs described or planned as great, as northern, and as either (entry 29 clauses); cisterns fed by channels from a great wadi (entry 45, C-open × G-strict, and G-loose); outlets at a named wadi and at Wadi Qelt (entry 32); installations dated in the window (all types).
- A survey record is its own site complex; with one reservoir in it, the relative clauses "great" and "northern" can only MATCH on words.
- `README.md`, `scripts/`, `tests/`, `sources_read.csv` (what was read, pages, hashes, access), and the blocked list with exact URLs.
- **Overall code of a row in a branch:** MATCH if every scored clause MATCHes and the date passes; FAIL if any scored clause or the date FAILs; otherwise UNKNOWN.

## 9. Decision wording (fixed now)

- Each count reads "k match, f fail, m unknown, of N" for the stated entry, branch, lineage and date rule. **Main headline:** merged lineage, main date rule.
- **k ≥ 5** in a branch: the clause combination is common in the recorded region; a fit at any one site carries little weight on its own.
- **k small and m small:** the combination is uncommon in the recorded region.
- **m ≫ k:** rarity is not measurable from the available record.
- **k = 0:** existing candidate fits rest on evidence or tolerances outside this inventory; this is not a rejection.
- **Never follows:** an identification (no discrimination test and no unseen prediction is run here; the candidates are exposed), anything about a deposit, anything outside the box, rarity on the ground rather than in the record.

## 10. Exposure before this freeze

- **Repository (before this lane):** WBADB rows with pool words region-wide (kohlit stage 1, 518 rows); ASI records within 3 km of the 48 places, including all Jerusalem, Hyrcania, Mar Saba, Choziba, Jericho-palace, Ramat Raḥel and Buqeiʿa records (asi_jerusalem lane); 73 HA-ESI reports (haesi_features lane); Garbrecht & Peleg 1994 in full; the 1989 volume's Doq, Cypros, Hyrcania, Jericho-estate, Qumran, Alexandrion and Porath chapters; Netzer 1983/1989/2001 and 2006 passages and the 28-record entry 29 inventory; ROSAPAT 2011; SWP III Jericho waterworks; Magen & Peleg 2018; Humbert & Chambon; Reeder & Jol 2006; Stacey 2007; Eshel 2002; Puech 2006/2015; Lefkovits 2000; Milik 1962; the Siloam, Ramat Raḥel, Herodium and Wadi Qelt notes.
- **This worker, before writing this plan:** `AGENTS.md`, `LANE_RULES.md`, `research/ACTIVE_TEST.md`; the kohlit README and pre-registration; the ASI lane README and access note; the entry 29 inventory note (all of it); `registration/garbrecht_peleg1994_extracted.md` (all of it); `text/readings.json` and the concordance rows for the seven entries; the lexicon and feature-constraint rows for them; the schematics README; the WBADB column list and the count of its rows in the box by `Survey_Ref` form (no component or comment text); the ASI map list and sheet grid (no site record); the contents leaves of the 1989 volume (OCR of repo extract pp. 4–5); page counts and hashes of the Downloads PDFs (no text); the HA-ESI type vocabulary; the Wikidata coordinate of Ein Karem; the arrival register check (`manifest: ok`).
- Because nearly all candidate installations are exposed, every count here is exploratory.

## 11. Amendments

Any change after this commit goes in a separate file `PLAN_AMENDMENT_n.md`, labelled with the reason and with what had been seen. Choices made after seeing records are exploratory and labelled.
