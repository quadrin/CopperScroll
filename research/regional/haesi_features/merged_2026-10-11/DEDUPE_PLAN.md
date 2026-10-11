# HA-ESI merged inventory: frozen deduplication plan

Written 11 October 2026 by the merge worker, before any pair of reports or rows was compared. Committed alone; that commit is the freeze record. Later changes go in a separate amendment file; this file is not edited.

This is bookkeeping on an exploratory inventory. It makes no identification claim and changes no registered outcome. It does not re-code any row: classes, datings, quotes and coordinates stay as the phase readers coded them.

## 1. Inputs (read only; no phase file is changed)

| Phase | Reports | Feature rows |
|---|---|---|
| 1 (9 Oct) | `../reports.csv` | `../features.csv`, `../features_unlocated.csv` |
| 2 (10 Oct) | `../phase2_2026-10-10/reports.csv` | `../phase2_2026-10-10/features.csv` |
| 3 A, B, C, D (11 Oct) | `../phase3_2026-10-11/part_{a,b,c,d_online}/reports.csv` | `../phase3_2026-10-11/part_{a,b,c,d_online}/features.csv` |

Helper inputs: `../phase2_2026-10-10/PLAN.md` (zone boxes, gazetteer, eligible classes; JSON block), `../phase2_2026-10-10/phase1_zone_crosswalk.csv` (zones of located phase-1 rows), `../phase3_2026-10-11/part_b/already_coded_crosswalk.csv` (uncoded Hebrew headings whose English version was coded), and `research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv` (points of named places).

## 2. Row scope and the three counting levels

Every source row goes into `features_all.csv` once, with `phase`, `source_file`, `row_uid` (`<source_file>#<1-based data row>`), `report_group` and `site_id`.

A row is **counted** only if (a) its class is one of the ten phase-2 classes (`cistern`, `pool_reservoir`, `channel_aqueduct`, `dam`, `ritual_bath`, `cave_with_finds`, `tomb_burial_cave`, `columbarium_dovecote`, `rockcut_installation`, `hoard_cache`) and (b) it has a zone Z1–Z4 (§3). Phase-1 `wall_tower` rows are kept but never counted (phase 2 §5 made walls ineligible). Phase-1 rows keep their phase-1 class codes; phase 2 §5 lists the small differences (phase-1 pool rows may include dams, rock-cut rows may include columbaria, caves required finds). They are counted under their own codes and the number of counted phase-1 rows per class is reported separately so a reader can remove them.

Counts are given by class × zone × `dated_in_window` at three levels:

1. **Rows**: counted rows, as coded (duplicates included).
2. **Deduplicated reports**: units (report group, class, zone). A report group is one field campaign's report in whatever versions were coded (§4). Its dating for that class and zone is **yes** if any row of any version is yes; else **no** if any row is no; else **unknown**. So "yes" means at least one feature of the class that some version dates in the window in its own words; "no" means dated features of the class, none in the window; "unknown" means all undated. The three columns add up to the number of distinct report groups per class and zone.
3. **Distinct sites**: units (site, class, zone), with the same yes > no > unknown rule over all counted rows of the site (any report, any version). A site is a named place within a distance (§5). A site count is not a count of features on the ground.

Zone at level 2: the preferred version's zones for that class (§4.4); a row of another version in a zone the preferred version does not use for that class is moved to the preferred version's zone when that version has exactly one zone for the class, else it keeps its own; every such case is a conflict. Zone at level 3: the most common zone of the site's counted rows (ties: the earlier zone in the order Z1, Z2, Z3, Z4); a site with rows in two zones is a conflict.

## 3. Zones of rows that have none

Phase 2 and 3 rows keep their `region_zone`. Phase-1 rows get a zone by the phase-2 §2 rule, applied in this order, and `zone_source` records which step gave it:

1. Row latitude and longitude present: the first phase-2 zone box containing the point (the phase-2 `zone_of`, re-implemented in the standard library from the same JSON parameters); else `outside`. A test checks agreement with `phase1_zone_crosswalk.csv`.
2. No coordinates: the zone whose phase-2 gazetteer terms (English and Hebrew, phase-2 normalisation and word boundaries) match the report title (`site_name`), if exactly one zone matches (region-wide terms ignored).
3. Else, if `coordinate_source` names a place id (`name only (<place_id>)`, `feature site name (<place_id>)`): the zone of that place's point in `places_v2.csv`.
4. Else `unlocated`; the row is kept and not counted.

Part A rows whose report zone is `MULTI` keep their own row zones. A row zone of `outside` or `unlocated` is not counted.

## 4. Same report (report groups)

A report group is one field campaign's report, in all coded versions. Reports are grouped by union over the links below. Every coded report, with or without feature rows, belongs to exactly one group; a group of one member is a single report.

### 4.1 Definitions used by the link rules

- **Version series**: `HA` = Hebrew *Hadashot Arkheologiyot* (1961–1998); `ESI` = English *Excavations and Surveys in Israel* (1982–2000); `HA-ESI print` = report ids `HAESI<vol>-…` (portal volumes 109–115 and HA-ESI 138); `HA-ESI online` = report ids `HAESI-<n>`.
- **Year**: the `year` column (publication year as coded).
- **First page**: the first integer in `pages`.
- **Report position**: the report's own `lat`, `lon` in its `reports.csv`; its grid unit `u` (1, 10, 100 or 1000 m) from the digit count of the first number in `map_ref_as_given` (phase-1 `geo.py` digit rule: 3 digits = 1000 m, 4 = 100 m, 5 = 10 m, 6 = 1 m); if the unit cannot be read, `u` = 1000 m.
- **Position test**: both positions present and great-circle distance ≤ 250 m + √2 × (u₁ + u₂). The √2 × u term is the largest offset between the converted point (the grid cell's south-west corner, as `geo.py` converts truncated references) and any point of that cell.
- **Author test**: at least one shared surname skeleton. Parenthesised text is removed from the author field; the rest is split on `,` `;` `&` ` and ` `/`; the surname of each part is its last Latin-script word of three or more letters; the skeleton is its ASCII-folded lower-case form with these steps in order: `ph`→`f`, `tz`/`ts`→`z`, `ck`/`q`/`c`→`k`, `w`→`v`, remove `a e i o u y h`, collapse repeated letters. Skeletons shorter than two letters are not used.
- **Name keys** (Latin key and Hebrew key) as defined in §5.1, computed from the report title.
- **Name test**: the Latin keys are equal and non-empty, or the Hebrew keys are equal and non-empty.
- **Place test**: the position test if both reports have positions; otherwise the name test.

### 4.2 Link rules

- **R1 identical citation.** Same series, same volume, same first page and same Latin or Hebrew name key. (Catches a report coded twice in two phases.)
- **R2 Hebrew and English versions.** One report in `HA` and one in `ESI`, with ESI year − HA year between −1 and +6, the author test passing and the place test passing. Matching is one to one: all candidate pairs are sorted by (position test used before name test, |ESI year − HA year|, distance, report ids) and accepted in that order when neither report is already paired by R2. A report with more than one passing candidate is flagged `ambiguous` and listed for review (§4.3).
- **R3 printed and online.** One `HA-ESI print` report and one `HA-ESI online` report of the same volume number, with the author test and the place test passing; one to one as R2.
- **R4 same permit.** A shared permit on two reports in any series, with the place test passing. The permit field is split at `,` `;` `/` and ` and `; each part with a digit is a permit, written with letters and digits only, upper case (for example `A-5185` and `A- 5185` are one permit). A permit belongs to one field season.
- `ESI` and `HA-ESI print` reports are not treated as versions of each other (both English; the bilingual series replaced ESI), and `HA` and `HA-ESI print` are not either; such pairs join only by R1 or R4.

### 4.3 Review list and manual decisions

`pair_candidates.csv` lists every R1 and R4 pair, and every R2/R3 pair that meets the series and year conditions and passes at least two of the author, position and name tests (a missing position fails the position test), with each test's result and the outcome. These pairs are listed for review: R2/R3 pairs with a passing name test and year window whose author test fails (possible transliteration miss), or whose position test fails while the name and author tests pass (possible misprinted reference); and every `ambiguous` R2/R3 pair.

A manual decision (`data/manual_decisions.csv`: kind, the two ids, `same` or `different`, reason, basis) may only (a) accept or reject a listed review pair, judged from the coded fields (titles, authors, pages, years, positions, feature rows and quotes), or (b) apply a reader's explicit statement in the source NOTES that two reports are the same campaign or different excavations. Manual decisions override the automatic outcome for that pair and are labelled INFERENCE. They are exploratory (made after seeing the candidates). The phase-3 part B note's three ESI 15 pairs are decided under (b).

### 4.4 What is kept when versions disagree

- All rows of all versions stay in `features_all.csv`; nothing is deleted or re-coded.
- **Preferred version** (the fuller text as coded): the most counted rows; then the most distinct counted classes; then a map-reference position (smaller unit first); then the later year; then the smaller report id. Its title, position and zone represent the group.
- Level-2 classes are the union over versions (a class coded in only one version still counts; a conflict is recorded).
- Datings are combined by §2 (yes if any version dates the class in the window in its own words).
- **Conflicts** (`conflicts.csv`), one row each: a class coded in one version only; different dating summaries for a class; different zones for a class; positions failing the position test within an R2/R3/R4 group; stated `n_features` different for a class with one row per version; an R4 group whose author test fails.

## 5. Same site (sites)

Sites are built over feature rows (all rows get a `site_id`; only counted rows enter level 3). Links are joined by union.

### 5.1 Name keys

The row's name is `feature_site` when the row has its own location (`coordinate_source` begins with `feature`) and that name gives a non-empty key; otherwise the report title `site_name`.

From the name, a Latin text (Hebrew letters removed) and a Hebrew text (Latin letters removed) are made. Each is cut into segments at `,` `;` `:` `(` `)` `[` `]` `–` `—` `/` `|` and at ` - ` (hyphen with spaces). Each segment is normalised as phase 2 (`norm`: NFKD, marks removed, lower case, apostrophes ʿ ʾ ‘ ’ ' \` ´ ׳ ʽ ʻ removed, punctuation to spaces; also the maqaf ־ and the gershayim ״ to spaces); the drop phrases are removed, then tokens are split. Tokens with a digit, tokens of one letter and drop words are removed. A token is **distinctive** if it has at least three letters and is neither a drop word nor a generic word.

The key of a text is taken from the first segment that has a distinctive token: its distinctive tokens, sorted, de-duplicated, joined by spaces. If no segment has one, the key is the first segment whose remaining tokens (generic words kept) number two or more, joined in order (for example `lower aqueduct`, `old city`). Else the key is empty. A key that equals a phase-2 region-wide term after normalisation (Judean Desert, Dead Sea, Jordan Valley, Lower Jordan Valley, Samaria, and their Hebrew forms; key tokens compared as sorted sets) is treated as empty: a region is not a named site. Word lists are in §7.

### 5.2 Link rules

- **S1 located rows.** Two rows with coordinates are one site if the distance is ≤ 250 m + √2 × (u₁ + u₂) (`u` = `precision_m`; missing = 1000 m) and the name test passes (equal non-empty Latin keys or equal non-empty Hebrew keys). Pairs within the distance whose names cannot be compared (no script in common) are listed in `site_review.csv`.
- **S2 rows without coordinates.** Within one zone, rows without coordinates that have the same non-empty key (Latin or Hebrew) are one site. If the located rows of that zone with that key all belong to exactly one site, the rows without coordinates join it; if they belong to several, the rows without coordinates stay a separate site flagged `ambiguous_name`.
- **S3 same ASI or WBADB site.** Rows citing the same ASI or WBADB site number are one site. (No row in the inputs cites one; the rule is stated for later use.)
- **S4 same report.** Within a report group, all rows located by the report itself (not by a feature reference) are one site.
- **S5 manual.** `data/manual_decisions.csv` kind `site`: a reader's explicit statement in the source NOTES that two reports describe the same structure (phase-3 parts A, C, D), or a decision on a `site_review.csv` pair. Labelled INFERENCE; recorded with reason.
- Rows with an empty key and no coordinates join others only by S4 or S5.

Chaining is allowed (single linkage along one key). `sites.csv` reports each site's spread (largest distance between located rows) and flags spreads over 1 km.

## 6. Outputs

`features_all.csv` (phase-2 columns, then `phase`, `source_file`, `report_group`, `site_id`, then `row_uid`, `counted`, `count_zone`, `zone_source`, `not_counted_reason`, `version_role`); `report_groups.csv`; `sites.csv`; `conflicts.csv`; `pair_candidates.csv`; `site_review.csv`; `summary.json`; `README.md`; `scripts/build_merged.py` (standard library only; reads the parameters below from this file); `tests/`. Group ids are `RG:<smallest member report id>`; site ids are `S<number>`, numbered by the order of each site's first row in the input order of §1.

## 7. Parameters (machine-readable)

```json
{
  "distance_m": 250,
  "precision_factor": 1.4142135623730951,
  "missing_unit_m": 1000,
  "esi_minus_ha_years": [-1, 6],
  "spread_flag_m": 1000,
  "phase2_classes": ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds", "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"],
  "zones_order": ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"],
  "dating_order": ["yes", "no", "unknown"],
  "segment_separators": [",", ";", ":", "(", ")", "[", "]", "–", "—", "/", "|", " - "],
  "extra_space_chars": ["־", "״"],
  "drop_phrases_en": ["second temple", "first temple", "early roman", "late roman", "middle roman", "late hellenistic", "early islamic", "late islamic", "iron age", "bronze age", "early bronze", "middle bronze", "late bronze", "brief news", "burial caves", "burial cave"],
  "drop_words_en": ["jerusalem", "the", "of", "and", "in", "at", "near", "by", "on", "to", "from", "for", "with", "an", "its", "area", "areas", "site", "sites", "survey", "surveys", "surveyed", "excavation", "excavations", "excavated", "salvage", "trial", "rescue", "test", "brief", "news", "season", "seasons", "report", "reports", "preliminary", "final", "sounding", "soundings", "probe", "probes", "inspection", "inspections", "documentation", "development", "works", "work", "project", "map", "maps", "no", "number", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "several", "various", "new", "further", "additional", "other", "remains", "finds", "period", "periods", "hellenistic", "roman", "byzantine", "ottoman", "mamluk", "crusader", "umayyad", "abbasid", "islamic", "chalcolithic", "persian", "israelite", "herodian", "hasmonean"],
  "generic_words_en": ["old", "city", "quarter", "street", "st", "road", "way", "hill", "hills", "mount", "mt", "mountain", "valley", "wadi", "nahal", "nahr", "ein", "ain", "ayn", "kh", "khirbet", "khirbat", "kirbet", "horbat", "horvat", "hurvat", "tel", "tell", "tulul", "givat", "giv", "givaat", "har", "ramat", "beit", "bet", "beth", "bir", "deir", "dayr", "kafr", "kefar", "umm", "abu", "ras", "jebel", "jabal", "mughar", "mughara", "mearat", "qasr", "rujm", "north", "south", "east", "west", "northern", "southern", "eastern", "western", "northeast", "northwest", "southeast", "southwest", "central", "upper", "lower", "middle", "church", "monastery", "chapel", "synagogue", "mosque", "tomb", "tombs", "cave", "caves", "burial", "cemetery", "cistern", "cisterns", "pool", "pools", "reservoir", "aqueduct", "aqueducts", "channel", "channels", "conduit", "tunnel", "quarry", "quarries", "winepress", "winepresses", "press", "installation", "installations", "tower", "wall", "walls", "gate", "house", "houses", "building", "buildings", "farm", "farmstead", "farmhouse", "fort", "fortress", "village", "ruin", "ruins", "neighborhood", "neighbourhood", "compound", "center", "centre", "junction", "square", "park", "forest", "school", "hospital", "hotel", "garden", "gardens", "plaza", "parking", "lot", "slope", "slopes", "ridge", "spring", "springs", "camp", "settlement", "plot", "lane", "alley", "route", "highway", "interchange", "bridge", "railway", "line", "pipeline", "sewage", "water", "system", "ancient", "bath", "bathhouse", "miqveh", "estate", "complex", "structure", "structures"],
  "drop_phrases_he": ["בית שני", "הבית השני", "בית ראשון", "חדשות בקצרה"],
  "drop_words_he": ["ירושלים", "בירושלים", "סקר", "סקרים", "חפירות", "חפירה", "חפירת", "חדשות", "בקצרה", "הצלה", "ניסיון", "ניסיונית", "בדיקה", "בדיקות", "עונה", "העונה", "ליד", "בסביבות", "באזור", "איזור", "אזור", "של", "על", "עם", "את", "תקופת", "התקופה", "ראשונה", "שנייה", "שלישית", "רביעית", "חמישית", "שני", "שלושה", "חדש", "חדשה", "ממצאים", "שרידים", "ההלניסטית", "הרומית", "הביזנטית"],
  "generic_words_he": ["חורבת", "חירבת", "חרבת", "תל", "עין", "נחל", "ואדי", "הר", "גבעת", "רמת", "בית", "דיר", "כפר", "אום", "אבו", "ראס", "גבל", "קבר", "קברים", "קבורה", "מערה", "מערות", "מערת", "בור", "בורות", "ברכה", "ברכת", "אמה", "אמת", "המים", "מים", "מחצבה", "מחצבות", "גת", "גתות", "כנסייה", "כנסיית", "מנזר", "צפון", "דרום", "מזרח", "מערב", "צפונית", "דרומית", "מזרחית", "מערבית", "העיר", "עיר", "העתיקה", "רובע", "הרובע", "רחוב", "רח", "שכונת", "שכונה", "מתחם", "כביש", "דרך", "מעיין", "העליונה", "התחתונה", "עליון", "תחתון"]
}
```

## 8. Exposure before this freeze

Seen while planning: AGENTS.md; the lane rules; the phase-1, phase-2 and phase-3 READMEs; phase-2 AMENDMENTS and PLAN §2, §5, §6; phase-3 PLAN; the NOTES of parts A, B, C and D, which name some same-site or same-report cases (part B: three ESI 15 pairs, one of them "different excavations"; part D: Arzei Ha-Bira quarry, Lower Aqueduct at Umm Tuba, Tyropoeon drainage channel, HAESI-2306/25020, HAESI-16734/1875; part C: the Gihon pool and Channel II in five volumes; part A: Jason's Tomb, the En Gedi pool, HA72-028 with ESI02-057); the column headers of every input table; value counts of series, volume, zone, class, dating, location status, coordinate source, grid and precision; three random report rows per reports table and six random feature rows per features table (titles, authors, permits, map references); `geo.py` and the phase-2 `common.py`; and that no input row cites an ASI or WBADB site number. No pair of reports or rows was compared, sorted by name or matched before this freeze.
