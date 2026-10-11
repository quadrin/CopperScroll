# HA-ESI phase 2: frozen plan (regional inventory of the scroll's feature kinds)

Written 11 October 2026 UTC (10 October Los Angeles) by the IAA-reports lane, before any new report was read. Exploratory. No identification claim. No registered outcome, ledger count or test changes. Labels: EVIDENCE (what a report says), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record).

This plan replaces nothing in phase 1 (`../search_plan.json`, frozen 9 October). Phase-1 files are not edited.

## 1. Question

How many features of the scroll's kinds do the IAA excavation reports (HA, ESI, HA-ESI) record in a fixed region, whatever their distance to a proposed place, and how many are dated by the report to the window (Hasmonean to 135 CE)? The value is the denominator: rows per class, zone and dating status. Unread reports stay listed as unread; silence is never absence.

## 2. Region (fixed)

CRS of the boxes: WGS84 (EPSG:4326), decimal degrees. Map references are converted as in phase 1 (`../scripts/geo.py`): Old Israel Grid with EPSG:28191, New Israel Grid with EPSG:2039; digit and grid rules unchanged. A point is assigned to the first zone that contains it, in this order:

| Zone | Name | Box (lat; lon) |
|---|---|---|
| Z1_GERIZIM | Mount Gerizim, Shechem and its eastern hinterland to Kh. Yanun | 32.14–32.26; 35.19–35.37 |
| Z2_JORDAN_VALLEY | Jordan Valley from Phasaelis and Jericho to the Dead Sea's north end | 31.76–32.06; 35.40–35.60 |
| Z4_JERUSALEM_HILLS | Jerusalem and the Judean hills to Bethlehem, Herodium and Tekoa | 31.62–31.90; 35.10–35.27 |
| Z3_JUDEAN_DESERT | Judean Desert, escarpment and western Dead Sea shore | 31.20–31.92; 35.27–35.60, plus 31.92–32.06; 35.30–35.60 (both minus Z2) |

Boxes are INFERENCE (approximate physiographic limits). The western shore and the Jordan form the practical east limit (HA-ESI does not cover Jordan). A point outside all boxes is outside the region. A report without a map reference is placed in the zone its title names (gazetteer, §4), with `coordinate_source = name only` and no distance; an ambiguous name without a map reference stays unlocated and is listed, not coded.

## 3. Sources and access routes (in this order of work)

1. **Online screen (S-ON).** hadashot.iaa.org.il, read through the owner's Chrome as a person would: one tab, one page at a time, at least 3 seconds between page loads, no scripted fetching, no parallel tabs, no downloads. The per-volume report lists (`reports_eng.aspx?id=…`, volumes 116–137, 2004–2025) and the Extended Reports list are screened in full against the gazetteer (§4). A Cloudflare or other check that asks for a click or a CAPTCHA stops this route; it is reported, never solved.
2. **Portal test.** One portal volume PDF (publications.iaa.org.il) is opened in Chrome to see whether its text can be read in the browser. Nothing is saved to disk. If it cannot be read, `portal_pdfs_needed.csv` lists every portal volume (series, volume, exact PDF URL, size, number of phase-1 screened candidates, priority by region hits) and the route stops. If it can be read, HA 28–29 is read first (Tier-1 record, §8), then the phase-1 candidates in the region (`../dropped.csv`, tier P1) oldest first, after reading tier T1 online.
3. **Local PDFs (S-LOC)** on the owner's Mac (`~/Downloads`, narrow filter; research files only): ESI 2, 3, 5, 6, 7–8, 9, 15; HA 40, 45, 59–60. Duplicate files are compared by SHA-256 and only one copy is used. Text is extracted with `pdftotext` (layout and raw). Every report heading in each whole volume is screened: its map reference is converted and zoned; without one, its title is matched to the gazetteer. Every report in the region is read, except reports already read in phase 1, which are not re-coded but get a zone in `phase1_zone_crosswalk.csv`.
4. **Online reading.** Candidates from S-ON are opened and read one page at a time in this tier order: T1 = titles placed in Z1, Z2 or Z3, or matching a region-wide term ("Judean Desert", "Dead Sea", "Jordan Valley", "Samaria" with a zone name); T2 = Z4 titles that do not begin with "Jerusalem"; T3 = Z4 titles that begin with "Jerusalem". Within a tier the reading order is ascending SHA-256 of the report id string (for example `sha256("5432")`), so that any part read before the stop is a pseudo-random sample of its tier. Nothing is reordered after a result is seen.
5. **Stop rule.** Work stops when the session must end. Everything screened but not read is listed with its tier and order position as `not read (time limit)`.

What the online pages give: the report id, volume, year, title, author(s), permit, map reference and text. The text read is the main report body as shown in the page; its SHA-256 is computed over that text with whitespace collapsed to single spaces (UTF-8). No figure, plan or photograph is opened or stored; figure captions in the text may be read.

## 4. Gazetteer for title screens (frozen)

Titles and names are normalised as in phase 1 (NFKD, marks removed, lower case; ʿ ʾ ‘ ’ ' ` ´ ׳ removed; hyphens, dashes, commas, full stops and parentheses become spaces; spaces collapsed). A term matches with a word boundary on both sides. A title matching any term is a candidate. Its zone is fixed by the report's map reference once read; a candidate whose map reference falls outside the region is dropped with that reason. The lists are in the JSON block below (`gazetteer`).

## 5. Eligible feature classes

A report is coded if it lies in the region and records, as found, exposed, documented, surveyed or inspected in the reported work, at least one feature of these classes. Features cited only from earlier work are not coded (noted). Codes reuse phase-1 values where the meaning is the same.

| Code | Includes | Phase-1 difference |
|---|---|---|
| cistern | cistern, bell-shaped or water pit, plastered pit for water | same |
| pool_reservoir | pool, reservoir, open water basin, water tank | phase 1 also put dams here; phase 2 codes dams as `dam` |
| channel_aqueduct | channel, conduit, aqueduct, pipe line, water tunnel, drain, sewer | same |
| dam | dam, check dam, diversion or barrage wall across a stream | new; phase-1 rows with dams are under pool_reservoir |
| ritual_bath | stepped pool or miqveh, whatever the excavator's function label (subtype records the label) | same code, stepped pools added explicitly |
| cave_with_finds | any non-burial cave or underground cavity the report records as a feature (natural or artificial; refuge cave, hiding complex, storage cave), with or without stated finds | phase 1 required finds |
| tomb_burial_cave | tomb, burial cave, grave, cist or shaft grave, kokhim or arcosolia, ossuary or sarcophagus burial, cemetery, funerary monument (nefesh, pyramid or built tomb monument) | monuments added explicitly |
| columbarium_dovecote | columbarium, dovecote, rock-cut niche wall for pigeons | new; phase 1 put columbaria under rockcut_installation |
| rockcut_installation | rock-cut installation, winepress, oil press, quarry, cupmark, rock-cut basin, pit or shaft not used as cistern | same |
| hoard_cache | hoard, cache, hidden vessels or deposit, purposely concealed group of objects | same |

Walls, towers, forts and buildings are not eligible in phase 2 (phase 1 coded `wall_tower`). A feature named in the report as a part of a building (for example a plastered pool in a bathhouse) is coded under its class.

Class to scroll terms (INFERENCE from `tables/landmark_lexicon_index.csv`, Puech entry numbers; meaning confidence there): cistern ← בור (3 6 8 9 10 15 45), שית/שיח (13 18 19 43 60), שוחה (57); pool_reservoir ← ברכה (11 16), אשיח (22 29 46 55), ים basin (47), מזקא (9 45), שקת (49); channel_aqueduct and dam ← אמה conduit (4 16 21 29 33), ביב (42 59), זרב (40), חריץ (23), יציאת המים (32 49); ritual_bath ← מקרת הטבילה (4), מעלות (1 6 57); cave_with_finds ← מערה (7 25 26 30 56); tomb_burial_cave ← קבר (14 24 51 53 54 60), יגר (20 28 35), נפש (2), יד (48), כוך and בית המשכב (56), משכן (27); columbarium_dovecote ← שובך (38 44); rockcut_installation ← no single term (צריח 8 36 37 39 40 47; שן הסלע 10; INFERENCE only); hoard_cache ← the deposits themselves. **Reading dependence:** columbarium_dovecote bears on entries 38 and 44 only under the dovecote meaning (Puech 2015, Høgenhaven 2020); Milik reads a regular opening of a cave or rock face, Lefkovits a tower, Schiffman a drain (`text/readings.json` e38-dovecote, e44-dovecote). Under Milik's meaning entries 38 and 44 point to cave_with_finds or rockcut_installation instead. No entry clause (direction, distance, relation) is scored in this lane; the rows serve entry lanes as denominators.

## 6. Coding rules (as phase 1 unless stated)

- One row per (report, feature class), or per (report, site, class) when a survey report gives separate sites with their own map references. `n_features` is the stated number, else blank.
- `period_as_given`: the report's words for the feature's date. `dated_in_window`: **yes** only if the report dates the feature itself to the Hasmonean, Herodian, Early Roman, Late Hellenistic (= Hasmonean), Second Temple or Bar Kokhba period, the 1st c. BCE, the 1st c. CE or up to 135 CE, or says it was in use then; **no** if dated only outside the window; **unknown** if undated, dated only by the site's general periods, or by a range that only partly overlaps (Hellenistic, Roman, Middle Roman, Hellenistic–Roman, Early Roman–Byzantine).
- `quote`: verbatim, 12 words or fewer, from the text read.
- `excavated_or_surveyed`: excavated, excavated (salvage), surveyed, inspected.
- `region_zone` from §2; `dist_to_nearest_place_km` to the nearest point place of `places_v2.csv` (mixtures and transjordan excluded), from the converted map reference only.
- `feature_subtype`: the report's own word for the feature (for example "dam", "stepped pool", "miqveh", "hiding complex", "nefesh").
- `exposure_at_freeze`: `unexposed at freeze` for every report first read after this freeze; `read in phase 1` for phase-1 reports.
- Labels: observed remains, the excavator's function label and reconstruction are kept apart in the quote and subtype; our zone and class assignments are INFERENCE.

Output columns: `features.csv` has exactly the phase-1 `features.csv` columns, in the same order, then `region_zone`, `dist_to_nearest_place_km`, `feature_subtype`, `exposure_at_freeze`. `reports.csv` has the phase-1 `reports.csv` columns, then `region_zone`, `dist_to_nearest_place_km`, `exposure_at_freeze`, `tier`. Looks rows, if made, use the phase-1 `looks_haesi.csv` schema and rule (relation `HAESI-COVER`, all detection numbers null).

## 7. Protected and held material

- **Tell es-Sultan north strip.** A text that describes the strip from the north foot of Tell es-Sultan to about 250 m north is recorded with `protected_strip = yes` and only its citation; it is exposed text and not unseen evidence. No image is opened.
- **Held cave reports.** Exposure at planning: the item file `research/preregistration/arrivals/items/iaa-archive-cave-records.md` was opened while planning and its first prediction (Kh. Qumran opening facing) was seen. This lane therefore cannot be a blind reader for cave records in that item's area. Cave-survey or cave-excavation reports (any series) whose caves lie in the Qumran cliffs and marl terrace (Wadi Qumran to ʿEin Feshkha), the Jericho escarpment from Jebel Qarantal to Wadi Nuweiʿimeh and ʿAin Duk, or the Wadi Qelt gorge are **held**: listed with citation, not read, left to the arrival procedure. Excavation reports of built sites there (for example Kh. Qumran itself) are read normally.
- **Tier-1 records** (arrival register README step 5): HA 28–29 (Tananir) and the IAA notices on Kh. ʿAlmit are read only after this freeze, with extraction only: the reader does not open `research/assessments/kohlit_chain/chain.json` predictions or the arrival item files for them. Facts are extracted with page or report id; the integrator compares. They are marked `unexposed at freeze` and flagged `tier1_record` in notes. The ʿAtiqot 41 cave entries, Zertal vol. 4 site 194 and Highlands pp. 700–702 are not in this lane and are not sought.
- The L-656 field file and IAA Archive cave records are not sought.

## 8. Decision wording

Results are counts: "k rows of class c in zone z (yes y / no n / unknown u)", with the number of reports read and the number screened but unread per tier. A class count is a count of rows in the read corpus, not of features on the ground (several seasons can report one feature; same-feature notes are kept). No count is a rarity result for an entry, and nothing here identifies a place.

## 9. Exposure before this freeze

Seen while planning: phase-1 README, search_plan.json, corpus.csv, the first rows of screen_candidates.csv, reports.csv, features.csv, dropped.csv and unread_online_candidates.csv; phase-1 coding format (two HA 59–60 reports); kohlit_chain next_links.md (link list, relations, record names; no predictions); arrival README step 5 and ARRIVAL_PROCEDURE; the first 40 lines of the iaa-archive-cave-records item (one prediction, §7); the landmark lexicon, the dovecote readings and translation lines IX 1, IX 17, X 1. On hadashot.iaa.org.il: the home navigation, the search page (search types, the seven Area strips), the structure of map strip 5 (239 report links; no title read) and the volume list (volume numbers and page ids only). Local PDFs: file names, sizes, SHA-256, page counts and text-layer character counts; text extracted on the Mac but not read. No report, title list or table of contents beyond phase 1 had been read.

## 10. Parameters (machine-readable)

```json
{
  "zones_order": ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z4_JERUSALEM_HILLS", "Z3_JUDEAN_DESERT"],
  "zones": {
    "Z1_GERIZIM": [[32.14, 32.26, 35.19, 35.37]],
    "Z2_JORDAN_VALLEY": [[31.76, 32.06, 35.40, 35.60]],
    "Z4_JERUSALEM_HILLS": [[31.62, 31.90, 35.10, 35.27]],
    "Z3_JUDEAN_DESERT": [[31.20, 31.92, 35.27, 35.60], [31.92, 32.06, 35.30, 35.60]]
  },
  "box_format": "[lat_min, lat_max, lon_min, lon_max], inclusive",
  "classes": ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds", "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"],
  "tiers": {"T1": "Z1, Z2, Z3 or region-wide term", "T2": "Z4, title not beginning 'jerusalem'", "T3": "Z4, title beginning 'jerusalem'"},
  "order_within_tier": "ascending sha256(report_id string)",
  "region_wide_terms": {"en": ["judean desert", "dead sea", "jordan valley", "lower jordan valley", "samaria"], "he": ["מדבר יהודה", "ים המלח", "בקעת הירדן", "שומרון"]},
  "gazetteer": {
    "Z1_GERIZIM": {
      "en": ["gerizim", "har gerizim", "mount gerizim", "nablus", "shechem", "sekhem", "neapolis", "flavia neapolis", "balata", "tell balata", "tel balata", "askar", "tananir", "luza", "qiryat luza", "kiryat luza", "har berakha", "har bracha", "elon more", "elon moreh", "itamar", "yizhar", "yitzhar", "huwwara", "hawara", "burin", "rujeib", "kafr qallil", "ebal", "har eval", "mount ebal", "sychar", "josephs tomb", "joseph s tomb", "awarta", "beit furik", "yanun", "janoah", "aqraba", "gidonim", "asira", "beit iba", "zawata", "madama"],
      "he": ["גריזים", "הר גריזים", "שכם", "נאפוליס", "נבלוס", "בלאטה", "תל בלאטה", "עסכר", "תנניר", "לוזה", "קרית לוזה", "הר ברכה", "אלון מורה", "איתמר", "יצהר", "חווארה", "בורין", "עיבל", "הר עיבל", "קבר יוסף", "עוורתא", "ינון", "ינוח", "עקרבה", "גדעונים"]
    },
    "Z2_JORDAN_VALLEY": {
      "en": ["jericho", "yeriho", "tell es sultan", "tel es sultan", "ein es sultan", "en es sultan", "elisha", "tulul abu el alayiq", "tulul abu alayiq", "abu el alayiq", "naaran", "nueima", "nuweima", "nuweimeh", "nueimah", "ein duk", "en duk", "ain duk", "duyuk", "quruntul", "qarantal", "mount of temptation", "tell el qos", "cypros", "kypros", "tell el aqaba", "hisham", "mafjar", "tell es samrat", "samrat", "fasayil", "phasaelis", "pezael", "petzael", "tomer", "gilgal", "netiv ha gedud", "niran", "yitav", "naama", "auja", "el auja", "mevoot yeriho", "vered yeriho", "beit ha arava", "bet ha arava", "beit haarava", "qasr el yahud", "qasr al yahud", "hajla", "deir hajla", "beth hogla", "nebi musa", "nabi musa", "muhalhil", "almog", "jordan river", "baptism site", "allenby"],
      "he": ["יריחו", "תל א סולטאן", "תל אל סולטאן", "עין א סולטאן", "מעיין אלישע", "תולול אבו אל עלאיק", "נערן", "נועימה", "עין דוק", "קרנטל", "הר הפיתוי", "קיפרוס", "מפג'ר", "הישאם", "פצאל", "תומר", "גלגל", "נתיב הגדוד", "נירן", "ייטב", "נעמה", "עוג'ה", "מבואות יריחו", "ורד יריחו", "בית הערבה", "קאסר אל יהוד", "חגלה", "נבי מוסא", "מוחלחל", "אלמוג", "פסאיל"]
    },
    "Z3_JUDEAN_DESERT": {
      "en": ["qumran", "feshkha", "fashkha", "enot zuqim", "einot zuqim", "einot zukim", "ghuweir", "turaba", "turabeh", "mizpe shalem", "mezoke deragot", "metzoke dragot", "mizpe deragot", "deragot", "dragot", "darga", "murabbaat", "kalya", "qalya", "en gedi", "ein gedi", "nahal arugot", "nahal david", "nahal hever", "nahal mishmar", "nahal zeelim", "nahal tzeelim", "masada", "mezada", "en boqeq", "en bokek", "nahal boqeq", "nahal hazezon", "nahal qidron", "nahal kidron", "mar saba", "wadi en nar", "hyrcania", "hyrkania", "horqania", "kh mird", "el mird", "buqeia", "buqeiah", "sekakah", "kh es samra", "abu tabaq", "el maqari", "nahal og", "wadi qelt", "wadi el qelt", "nahal perat", "ein prat", "en prat", "ein fara", "ein qelt", "ein fawwar", "choziba", "st george", "mizpe yeriho", "kfar adumim", "kefar adummim", "nofei prat", "maale adummim", "maale adumim", "mishor adummim", "mishor adumim", "kedar", "khan el ahmar", "khan al ahmar", "euthymius", "martyrius", "samiya", "samieh", "marjama", "kafr malik", "kokhav ha shahar", "kokhav hashahar", "rimmonim", "mughayyir", "mukhmas", "mikhmas", "michmash", "nahal mikhmas", "wadi suweinit", "nahal teqoa", "nahal tekoa", "natuf", "khareitun", "chariton", "umm qatafa", "ketef jericho", "ketef yeriho", "cave of letters", "cave of horror", "nokdim", "almit"],
      "he": ["קומראן", "קמראן", "פשחה", "עינות צוקים", "ע'ויר", "טורבה", "מצפה שלם", "מצוקי דרגות", "דרגה", "מורבעאת", "קליה", "עין גדי", "נחל ערוגות", "נחל דוד", "נחל חבר", "נחל משמר", "נחל צאלים", "מצדה", "עין בוקק", "נחל קדרון", "מר סבא", "הורקניה", "מירד", "בוקיעה", "סככה", "נחל אוג", "ואדי קלט", "נחל פרת", "עין פרת", "עין קלט", "עין פוואר", "קוזיבה", "מצפה יריחו", "כפר אדומים", "נופי פרת", "מעלה אדומים", "מישור אדומים", "קדר", "ח'אן אל אחמר", "סמיה", "מרג'מה", "כפר מאלכ", "כוכב השחר", "רימונים", "מע'ייר", "מכמש", "נחל מכמש", "נחל תקוע", "נטוף", "חריטון", "כתף יריחו", "נוקדים", "עלמית"]
    },
    "Z4_JERUSALEM_HILLS": {
      "en": ["jerusalem", "yerushalayim", "bethlehem", "bet lehem", "beit lehem", "beit jala", "bet jala", "beit sahur", "bet sahur", "herodium", "herodion", "tekoa", "teqoa", "tuqu", "artas", "solomons pools", "solomon s pools", "el khader", "al khadr", "efrat", "efrata", "har gilo", "gilo", "har homa", "ramat rahel", "sur bahir", "umm tuba", "beit safafa", "ein kerem", "en kerem", "moza", "motza", "mevasseret", "mevasseret ziyyon", "abu ghosh", "qiryat yearim", "kiryat yearim", "qiryat anavim", "maale ha hamisha", "maale hahamisha", "har adar", "beit surik", "givat zeev", "nebi samwil", "nabi samwil", "nabi samuel", "bir nabala", "qalandiya", "atarot", "jaba", "geva binyamin", "hizma", "anata", "anatot", "almon", "pisgat zeev", "neve yaaqov", "beit hanina", "shufat", "shuafat", "french hill", "ramot", "ramat shlomo", "tell el ful", "tel el ful", "givat shaul", "beit zayit", "zova", "tzova", "sataf", "ramallah", "el bireh", "al bira", "beitunia", "psagot", "beit horon", "bet horon", "beit ur", "mar elias", "el azariya", "al eizariya", "bethany", "abu dis", "sawahra", "jabal mukabbir", "jebel mukabbir", "ras el amud", "silwan", "siloam", "mount of olives", "mount scopus", "isawiya", "issawiya", "kfar ezyon", "kefar ezyon", "alon shevut", "neve daniel", "rosh zurim", "beit fajjar", "nahal refaim", "emeq refaim", "manahat", "malha", "walaja", "battir", "betar", "betar illit", "husan", "wadi fukin", "nahalin", "kh el yahud"],
      "he": ["ירושלים", "בית לחם", "בית ג'אלא", "בית סאחור", "הרודיון", "הרודיום", "תקוע", "ארטאס", "בריכות שלמה", "אל ח'דר", "אפרת", "הר גילה", "גילה", "הר חומה", "רמת רחל", "צור באהר", "אום טובא", "בית צפאפא", "עין כרם", "מוצא", "מבשרת ציון", "אבו גוש", "קרית יערים", "קרית ענבים", "מעלה החמישה", "הר אדר", "בית סוריכ", "גבעת זאב", "נבי סמואל", "ביר נבאלה", "קלנדיה", "עטרות", "ג'בע", "גבע בנימין", "חיזמא", "ענאתא", "ענתות", "עלמון", "פסגת זאב", "נווה יעקב", "בית חנינא", "שועפט", "הגבעה הצרפתית", "רמות", "רמת שלמה", "תל אל פול", "גבעת שאול", "בית זית", "צובה", "סטף", "רמאללה", "אל בירה", "ביתוניא", "פסגות", "בית חורון", "בית עור", "אל עיזריה", "אבו דיס", "סוואחרה", "ג'בל מוכבר", "ראס אל עמוד", "סילואן", "השילוח", "הר הזיתים", "הר הצופים", "עיסאויה", "כפר עציון", "אלון שבות", "נווה דניאל", "בית פג'אר", "נחל רפאים", "עמק רפאים", "מנחת", "מלחה", "ולג'ה", "בתיר", "ביתר", "חוסאן", "נחאלין"]
    }
  },
  "held_cave_areas": ["Qumran cliffs and marl terrace, Wadi Qumran to Ein Feshkha", "Jericho escarpment, Jebel Qarantal to Wadi Nuweimeh and Ain Duk", "Wadi Qelt gorge"],
  "tier1_records": ["HA 28-29 (Tananir)", "IAA notices on Kh. Almit"],
  "in_window": "Hasmonean to 135 CE, stated by the source; partly overlapping = unknown"
}
```
