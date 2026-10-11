# Regional tomb inventory: frozen plan

Lane: every recorded Second Temple period tomb in two fixed regions, scored against the scroll's tomb entries 14, 24, 27, 48, 51, 52, 53, 54 and 56. Written 11 October 2026 UTC (10 October Los Angeles), before any tomb record was fetched or coded.

This is an **exploratory regional inventory and count**. It makes no identification claim and changes no registered outcome, closed result or outcome-ledger count. Its product is a denominator: for each entry and reading branch, how many recorded tombs satisfy each clause, how many fail, how many are unknown. Rarity identifies nothing by itself. A landmark match says nothing about a deposit.

Labels: EVIDENCE (a source says it), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record). Unknown stays unknown (null), never zero.

The machine-readable rules are in the JSON block at the end of this file. The scripts read that block from this file, so the rules cannot drift from the frozen text.

## 1. Exposure before the freeze

Seen before this plan was written (so nothing below is unseen evidence, and none of it can serve as a confirmatory test):

- **Text.** `text/translation_en.json` lines III 11–13, V 12–14, VI 11–13, X 12–14, XI 1–XII 3; `text/readings.json` ids e14-*, e24-*, e27-*, e48-*, e51-* to e56-*; `tables/entry_concordance.csv`; `tables/landmark_lexicon_index.csv`; `tables/feature_constraints.csv` (entry 24 row).
- **ASI lane outputs** (`research/regional/asi_jerusalem/README.md`, read in full): records 102/410 (Absalom's tomb, "Herodian-period nefesh", Cave of Jehoshaphat), 102/411 (Bene Ḥezir and "Tomb of Zachariah"; Period list Hasmonean), 102/412, 413, 415 (rock-cut burial caves, "Herodian (?)"; 413 has a miqveh in its Finds list), 102/420 (Silwan: Iron Age monuments with kokhim "apparently from the Herodian period"), 102/424 (Dominus Flevit, Hasmonean and Herodian caves), 102/320 (Tombs of the Kings, "Tomb of Queen Helene of Adiabene"), 102/481–484 (Ge Ben Hinnom tombs, Second Temple and Herodian), 106/6, 106/8, 102/461–463 (Herodian burial caves near Baqʿa), 106/96 (Herodian burial complex near Ramat Raḥel), 109/5/95–96 (tombs at Sitna ʿAisha), 109/4/8 (St George's monastery: tomb, cave), and at Wadi Kuteif four records within 1 km, none a tomb (109/4/66 a guard tower). Its access notes (`access.md`). No record description beyond these README quotes was read.
- **Kidron work.** `research/schematics/searches/search_11_kidron_monuments.py` (first 200 lines): Allegro's 1959–63 dig at the base of Zechariah's monument (courtyard, a chamber once cut into the pedestal, a conduit), his "Zadok" tomb south of it ("very nearly under the pillar"), his reading of the courtyard as Zadok's garden, and the project candidates for entries 48, 51, 52, 54 (Kidron, Silwan slope, Gethsemane).
- **Jericho.** `research/agent_review_2026-10-07/followup/C_kenyon_jericho_II_and_kh_yanun.md` §A–C: Kenyon *Jericho* II (1965), Roman tombs G2, G3, G5, G81, H23, K23, J41 and 14 graves (G66–68, G80, G84, J5, J6, J16, J22–25, P4, Q1), the grave-arcosolium group matched to Qumran Period II, D9, N.S.1 and P29. `research/rarity/kohlit/README.md`: WBADB row S2446 (Jericho's Roman cemetery, Rom), E754 (Kh. Qumran), S4546 (ʿEin el-Ghuweir), E334 (Tell es-Sultan).
- **HA-ESI lane** (`research/regional/haesi_features/README.md`, first 60 lines): tomb rows exist near Jerusalem places and Ramat Raḥel; graves at ʿEin el-Ghuweir. No row read.
- **Other.** `research/sources/burial_primary_followup_2026-10-01.md` (Maresha and Bet Guvrin; outside both regions). `research/ACTIVE_TEST.md`. The arrival register README (no item concerns these tombs).
- **Background knowledge, not read from a source in this session** (listed because it could steer choices): the Bene Ḥezir inscription names priests of the Ḥezir family, including a "son of ʿOved" (Obed); a later inscription on Absalom's monument names Zechariah; a sarcophagus from the Tombs of the Kings bears an inscription with the word for "queen"; Josephus places Helena's monuments, with three pyramids, north of Jerusalem; Jason's Tomb (Reḥavia) has a pyramid and a single-column porch; the Goliath family tomb at Jericho has inscriptions; the Qumran cemetery has about 1,100 shaft graves; Kloner and Zissu's typology of Jerusalem tombs (kokhim, arcosolia, courtyards, façades).
- **Source structure only, no records:** the WBADB column list (sheets Surveyed and Excavations; fields Site_Name, Other_Names, Site_Components, More_Components, Comments, More_Comments, Major_Periods, Other_Periods and period flags Hel, Rom); the IAA Reports 7 landing page (chapter list of Hachlili and Killebrew 1999); the IAA Reports index.

Consequence: any match at the Kidron monuments, the Tombs of the Kings, Bene Ḥezir, Jason's Tomb, the Kenyon Roman tombs, the Qumran cemetery or Jericho's cemetery is **exposed** and is reported as such.

## 2. Regions (CRS and boundary)

All coordinates are WGS 84 (EPSG:4326), decimal degrees. Distances are haversine with R = 6371.0088 km (as in W2B `scripts/grid_convert.py` and the ASI lane). Reference points are taken from `research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv`.

- **Region A, the Jerusalem necropolis:** every point within **5.0 km** of `jer_temple` (31.77825, 35.23534). Sensitivity: 3.0 km. Results are also given in bands 0–1, 1–2, 2–3, 3–5 km. Known coverage gap: the ASI has no record inside the Old City walls (ASI lane), so tombs there are not inventoried.
- **Region B1, the Jericho cemetery zone:** every point within **4.0 km** of `tell_es_sultan` (31.8717, 35.4446) or of `jericho_palaces` (31.85187, 35.43624).
- **Region B2, the Jericho–Qumran road zone (entry 24):** every point within **3.0 km** of the great-circle segment from `jericho_palaces` to `kh_qumran` (31.74183, 35.45941). Sensitivity: 5.0 km. The distance to the segment is computed on a local equirectangular projection centred on the segment midpoint (error well under 10 m at this scale).
- **Region B** = B1 ∪ B2. Secacah is taken as Kh. Qumran, as the lane brief fixes. The Buqeiʿa alternative (Kh. es-Samrah) is **not** inventoried; that is a stated limit.

INFERENCE for the widths: the course of the ancient Jericho–Qumran road between the plain and the cliff foot is unknown, so 3 km covers the plain west of the shore and the cliff foot; 5 km adds the lower wadis. 4 km around the two Jericho points covers the town, the palaces and the cemetery hills to the west and north. 5 km around the Temple Mount covers the ring of tombs on all sides; 3 km is the tight alternative.

Source coordinates: ASI units use the WGS 84 point of the database GeoJSON (the ASI lane measured a 9–10 m offset from the converted New Israel Grid value; not material here). WBADB X/Y are Old Israel Grid without the 1,000,000 m false northing (kohlit README); they are converted with pyproj from EPSG:28193 after adding 1,000,000 m to Y. HAESI rows keep the lat/lon of the HA-ESI lane. Kenyon tombs: see below.

Position uncertainty: ASI points ±0.05 km (the database point and the converted grid value differ by about 10 m); WBADB points ±0.1 km (grid to 50 m and site extent); HA-ESI rows use the HA-ESI lane's precision; Kenyon tombs have no grid value and get the Tell es-Sultan point ±1.2 km (INFERENCE from the area offsets in the repo note). **A location clause is unknown when the tolerance lies inside the position uncertainty** (|d − tolerance| ≤ uncertainty).

## 3. Sources to inventory and eligibility

| Code | Source | Region | How read |
|---|---|---|---|
| ASI | Archaeological Survey of Israel, online maps. Kloner's *Survey of Jerusalem* (Maps 101, 102, 105, 106) and every other online map whose sheet intersects Region A or Region B (with the 5 km sensitivity corridor) | A, B | One `GetPolygonsSites` GeoJSON call per map (English service), cached in the scratch folder, method of `research/regional/asi_jerusalem/access.md`, at most one request per second |
| WBADB | West Bank Archaeological Database, `WBADB_data1.xlsx`, SHA-256 `3db734cd…ea5b` (both sheets) | A, B | Script |
| HAESI | `research/regional/haesi_features/features.csv` and `features_unlocated.csv` rows already coded by that lane | A, B | Reuse; not re-read |
| KEN | Kenyon *Jericho* II (1965), ch. 6 (Bennett), as extracted in the repo note C §A | B1 | Reuse of the repo extraction; not re-read |
| HK | Hachlili and Killebrew 1999, *Jericho: The Jewish Cemetery of the Second Temple Period* (IAA Reports 7) | B1 | Try the IAA publisher; if it is behind a bot check, record as blocked and do not bypass |
| KZ | Kloner and Zissu 2007, *The Necropolis of Jerusalem in the Second Temple Period* | A | Try open routes (Internet Archive, Google Books, the owner's Drive and Downloads); if not openly readable, record as blocked with catalogue and loan routes |
| AV | Avigad 1954, *Ancient Monuments in the Kidron Valley* | A | Same as KZ |
| A64 | `research/history/allegro1964_treasure_2nd_ed_extracted.md` (repo extraction) | A | Exploratory enrichment only (§6) |

**Eligibility (a tomb unit).** A record is a tomb unit if its name, description or finds text (ASI), or its name, other names, components or comments (WBADB), or its feature type and quote (HAESI) contains a TOMB term (JSON `tomb_terms`), and its point lies inside Region A or B. A unit is the record as the source gives it: one tomb, a group of tombs or a cemetery. Units holding several tombs are flagged (`multi_tomb_record`). Sheikh's tombs and other later shrines are kept as units and fall out on the date test.

**Duplicates across lineages.** ASI is the primary lineage in Region A; WBADB is the primary lineage in Region B outside the ASI sheets. A unit from another lineage within **0.15 km** of a unit of the primary lineage, or with the same normalised name within 0.5 km, is flagged `possible_duplicate_of` and left out of the union count. Each lineage is also counted on its own.

## 4. Dating

The window is the Hasmonean period to 135 CE.

- **Strict (`dated_in_window`)**: `yes` if a WINDOW label (JSON `period_window`) stands in the same sentence as a TOMB term; otherwise `partly` if a PARTLY label (JSON `period_partly`) does; otherwise `no` if only OUTSIDE labels (JSON `period_outside`) do; otherwise `unknown`. For WBADB, the "sentence" is the tomb row's period text (Major_Periods and Other_Periods); the Hel and Rom flags alone give `partly`. For HAESI, the lane's own `dated_in_window` is kept. For KEN, the repo extraction's dating of that tomb.
- **Lenient (`dated_lenient`)**: `yes` if strict is yes, or "Second Temple" stands in a sentence with a TOMB term, or a WINDOW label occurs anywhere in the unit's text.
- Labels are matched longest first, and a matched label masks the shorter labels inside it (so "Late Roman" is not also read as "Roman", nor "Early Roman" as "Roman").
- Per the lane rules, `partly` counts as unknown, never as in window. The headline denominator is the strict `yes` set; the lenient set and the any-date set are sensitivities.

## 5. Coding the features

Each unit's English text is split into sentences (split at ". ", "! ", "? "). Terms match whole words, case-insensitive, plurals allowed. Values are `yes` or `unknown`; `no` only where a rule below names an explicit negative.

| Code | Feature | `yes` when | `no` when |
|---|---|---|---|
| F1 | Above-ground monument (nefesh, pyramid, tholos, monolith, mausoleum, built tomb) | a MONUMENT term | never |
| F2 | Columned porch or façade | one sentence has a PORCH term and a COLUMN term | never |
| F3 | Inside pillar | one sentence has a COLUMN term and an INTERIOR term and no PORCH term | never |
| F4 | Inscription | an INSCRIPTION term | never |
| F5 | Named inscription | a sentence with an INSCRIPTION term also has a NAME_CUE | never |
| F6 | Garden context (ancient) | "garden" in a sentence with a WINDOW label (any "garden" is kept as `garden_mention`) | never |
| F7 | Entrance or façade orientation | a sentence with an OPENING term and direction words; the set of directions found | — |
| F7w | West-facing entrance or façade | F7 includes W, NW or SW | F7 found directions and none is westerly |
| F8 | Road zone | in B2 (3 km; sensitivity 5 km) | outside |
| F10 | More than one chamber | a number of two or more before chamber/room/hall, or "several chambers" | "single chamber", "one chamber", "a single room" |
| F11 | Kokhim | a KOKH term | never |
| F12 | Ossuaries | an OSSUARY term | never |
| F13 | Bone repository or pit | a REPOSITORY term | never |
| F14 | Large slab or closing stone | a SLAB term | never |
| F16 | Cistern | "cistern" | never |
| F17 | Channel | a CHANNEL term | never |
| F19 | Wadi setting | a WADI term in the name or text | never |
| F20 | Communal versus family (INFERENCE) | communal `yes` if a GRAVE_FIELD term and no FAMILY_TYPE term | communal `no` if a FAMILY_TYPE term (chamber tomb with kokhim, arcosolia or benches) and no GRAVE_FIELD term |
| F21 | Unfinished or unused | an UNUSED term | never |
| N* | Names | `name_zadok`, `name_absalom`, `name_queen`, `name_obed`, `name_jericho`: the NAME term anywhere in the unit's name or text; `*_in_inscription` if in a sentence with an INSCRIPTION term | never |

**Circularity rule.** A name assigned by a Copper Scroll interpreter (for example Allegro's "Zadok" tomb) does not count. If the unit's text mentions the Copper Scroll, its name codes are set to unknown.

**Manual check.** Every unit coded `yes` for F1, F2, F3, F5, F6, F7w or any name is read by the coder and either confirmed or set back to unknown with a stated reason (for example "monument" meaning a modern memorial). Raw and checked counts are both reported. No other value is changed by hand.

## 6. Enrichment from the repo's Kidron work (exploratory)

Allegro 1964's observations at the Kidron monuments (A64) are attached to the matching ASI unit in separate `enrich_*` columns. They are not used in the headline counts, because no other unit gets a second source of the same kind. Results with enrichment are a labelled sensitivity.

## 7. Entries, reading branches and clauses

Clauses come from the readings first. Every branch is scored on Region A, Region B and A ∪ B; the **headline region** is named per branch. Overall result per unit and branch: `match` if every clause is `yes`; `fail` if any clause is `no`; otherwise `unknown`. Depths and cubits are not scored (no excavation is tested here). "On the east/north/west side" names where to dig, and every tomb has such sides, so it is not a clause (the count of units with a recorded west-facing feature is reported anyway).

Location clauses (geometric):
- `L_south_corner`: within 0.5 km of `jer_south_wall` (31.77594, 35.23661), the south wall where the Royal Stoa stood (sensitivity 1.0 km). `no` beyond.
- `L_millo`: within 0.5 km of `jer_south_wall` (Milik: by the Temple esplanade; Puech: the Millo, north end of the City of David). `no` beyond.
- `L_temple`: within 0.35 km of `jer_temple` (inside the enclosure: half-diagonal about 0.29 km plus the point's uncertainty). `no` beyond.
- `L_road`: in B2 (3 km; sensitivity 5 km). `no` outside.
- `L_east_road`: within 2.0 km of `wadi_qumran` (31.74111, 35.45056). `no` beyond.
- `L_jericho`: in B1 → `yes`; elsewhere `yes` if `name_jericho`, else unknown (a Jericho family's tomb could lie elsewhere).
- `L_name_only`: a location given only by an unlocated name: unknown for every unit.

| Branch | Readings (source) | Clauses | Headline region |
|---|---|---|---|
| 14-M62 | Milik 1962: by the Temple esplanade; a slab over a bone pit | L_millo, F13 | A |
| 14-P06 | Puech 2006: the Millo; under the slab(?) | L_millo, F14 | A |
| 14-NAME | Text shown, Lefkovits, Milik 1960, Puech 2002 ("salt"), Puech 2015 ("embankment", "trap"): ha-Melaḥ as an unlocated name; "the dead" or an unscorable object | L_name_only | A ∪ B |
| 24-J | Milik, Puech 2015, Beyer, Lefkovits: tomb in the Wadi of the Kippa, on the way from Jericho to Secacah | L_road, F19 | B |
| 24-A | Allegro: the eastern road (entrance) to Secacah; Kippa = Wadi Qumran (his identification) | L_east_road, F19 | B |
| 27-T | Puech 2015 "mausoleum"; project "resting place": the queen's tomb | name_queen | A ∪ B |
| 27-D | משכן as a dwelling or enclosure (atlas "residence") | non-funerary: not scored | — |
| 48-Y | Puech 2006, Milik, Høgenhaven: Absalom's monument | F1, name_absalom | A |
| 48-L | Lefkovits: the Place of Absalom | name_absalom | A |
| 51-S | Milik 1962, Puech 2015: below the southern corner of the stoa, in Zadok's tomb, under the pillar of the exedra | L_south_corner, name_zadok, F2x | A |
| 51-O | Lefkovits: below the corner of the ossuary, in Zadok's tomb, under the pillar of the exedra | F12, name_zadok, F2x | A |
| 51-J | Pixner: ṣdyq "the Just" (an emendation), with the stoa | L_south_corner, F2x | A |
| 52-M | Milik: the family plot at the top of the rock facing west, opposite Zadok's garden, under the great slab, in its water channel | F7w, F6, F14, F17 | A |
| 52-P | Puech, Beyer: the scarp ... under the great slab at its base | non-funerary landmark: not scored (proxy F7w + F14 reported) | — |
| 52-L | Lefkovits: the ruin ... spiral staircase | non-funerary landmark: not scored | — |
| 53-P | Puech 2006/2015: the tomb under the colonnades (Temple galleries) | L_temple | A |
| 53-K | Letters shown (rock "knife"); Milik's comparison with the altar ledge | L_name_only | A |
| 54-P | Puech 2006: the tomb of the common people of Jericho | F20 communal, L_jericho | B |
| 54-L | Lefkovits: the tomb of the sons of Obed, the Jerichoite | F20 family (communal `no`), name_obed, L_jericho | A ∪ B |
| 54-M | Milik: the tomb of the sons of [a partly read name], the Jerichoite | F20 family, F5, L_jericho | A ∪ B |
| 54-W | Wolters, text shown: the tomb of the common people, ritually pure ("my pure things are in it") | F20 communal, F21 (INFERENCE: a tomb never used is not impure) | A |
| 56-P | Puech 2006, 2015: entrance of the [ledge] of the western burial chamber; entrance from the west; under the threshold of the burial niche | F10, F7w, F11 | A |
| 56-M | Milik: three items; entrance from the west; under the threshold of the cistern | F10, F7w, F16 | A |
| 56-L | Lefkovits: the alley ...; entrance from the city | non-funerary: not scored | — |

F2x (exedra with a pillar) is `yes` if F2 is yes, or if one sentence has a PORCH term and "pillar"; otherwise unknown. Restored words (the ledge at XI 16, the cave at XI 17) give no clause. Clauses that depend on one reading only are listed in their branch alone.

## 8. Output tables

- `tombs.csv`: one row per unit: unit_id, source, record id, page or record locator, name, lat, lon, CRS, position uncertainty, region flags and distances, multi_tomb_record, every feature code above with the matched terms (single terms, no description text), period terms as given, dated_in_window, dated_lenient, possible_duplicate_of, manual check result, exposure flag.
- `scores.csv`: one row per unit and branch: each clause value and the overall result.
- `scores_summary.csv`: per branch, region and date set: N, k match, f fail, m unknown, and per clause k/f/m.
- `features_summary.csv`: per region and date set: N and the counts of units with F1, F2, F3, F4, F5, F6, F7w, F8, in window.
- `sources_access.csv`: every source and link tried, with status.

No description text, page image or PDF is stored. Quotes are 12 words or fewer and only in the README.

## 9. Decision wording

For each branch and region: "k match, f fail, m unknown, of N". If k = 0 and f = 0, the branch is **not discriminable from this inventory**. If k > 0, the matches are listed with their exposure status; a match is a candidate in a denominator, not an identification. Coverage gaps (the walled city, the unread Jericho cemetery report, the Benjamin survey's English summaries, the Buqeiʿa) are stated beside each count. No result here changes an outcome, a candidate confidence or the atlas.

## 10. Frozen rules (machine-readable)

```json
{
  "plan_version": 1,
  "crs": "EPSG:4326",
  "earth_radius_km": 6371.0088,
  "points": {
    "jer_temple": [31.77825, 35.23534],
    "jer_south_wall": [31.77594, 35.23661],
    "tell_es_sultan": [31.8717, 35.4446],
    "jericho_palaces": [31.85187, 35.43624],
    "kh_qumran": [31.74183, 35.45941],
    "wadi_qumran": [31.74111, 35.45056]
  },
  "regions": {
    "A_radius_km": 5.0, "A_sensitivity_radius_km": 3.0, "A_bands_km": [1, 2, 3, 5],
    "B1_radius_km": 4.0,
    "B2_halfwidth_km": 3.0, "B2_sensitivity_halfwidth_km": 5.0
  },
  "tolerances_km": {
    "L_south_corner": 0.5, "L_south_corner_sensitivity": 1.0,
    "L_millo": 0.5, "L_temple": 0.35, "L_east_road": 2.0
  },
  "position_uncertainty_km": {"ASI": 0.05, "WBADB": 0.1, "KEN": 1.2, "HAESI_default": 0.1},
  "duplicate_km": 0.15, "duplicate_same_name_km": 0.5,
  "tomb_terms": ["tomb", "burial", "burials", "kokh", "kokhim", "kokim", "loculus", "loculi", "arcosolium", "arcosolia", "ossuary", "ossuaries", "sarcophagus", "sarcophagi", "nefesh", "nephesh", "sepulchre", "sepulcher", "sepulchral", "mausoleum", "necropolis", "cemetery", "cemeteries", "grave", "graves", "burial cave", "burial caves", "shaft grave", "cist grave", "funerary", "interment"],
  "period_window": ["Hasmonean", "Herodian", "Early Roman", "first century BCE", "first century CE", "first century BC", "first century AD", "1st century BCE", "1st century CE", "1st century BC", "1st century AD", "first century", "1st century", "Bar Kokhba", "Bar Kochba", "Second Revolt", "First Revolt", "Late Second Temple", "Qumran Period II"],
  "period_partly": ["Hellenistic", "Late Hellenistic", "Roman", "Second Temple", "Middle Roman", "Hellenistic-Roman", "Hel", "Rom", "second century CE", "2nd century CE", "second century BCE", "2nd century BCE"],
  "period_outside": ["Chalcolithic", "Bronze", "Early Bronze", "Middle Bronze", "Late Bronze", "Intermediate Bronze", "Iron", "Iron Age", "Persian", "Byzantine", "Late Roman", "Early Arab", "Early Islamic", "Umayyad", "Abbasid", "Crusader", "Ayyubid", "Mamluk", "Ottoman", "Medieval", "Neolithic", "modern"],
  "monument_terms": ["nefesh", "nephesh", "nefashot", "pyramid", "pyramidal", "tholos", "monolith", "monolithic", "mausoleum", "funerary monument", "burial monument", "built tomb", "tower tomb", "conical roof", "monument"],
  "porch_terms": ["porch", "portico", "vestibule", "exedra", "loggia", "facade", "façade", "entrance hall", "in antis", "distyle", "propylaeum"],
  "column_terms": ["column", "columns", "pillar", "pillars", "pilaster", "pilasters", "capital", "capitals", "in antis", "distyle", "colonnade"],
  "interior_terms": ["chamber", "chambers", "hall", "room", "ceiling", "inside", "interior", "central", "centre", "center"],
  "inscription_terms": ["inscription", "inscriptions", "inscribed", "epitaph", "graffito", "graffiti", "dipinto"],
  "name_cues": ["name", "names", "named", "son of", "sons of", "daughter of", "wife of", "family of", "priest", "priests", "of the family"],
  "opening_terms": ["entrance", "entrances", "opening", "openings", "facade", "façade", "doorway", "door", "portal", "porch", "faces", "facing", "opens", "entered"],
  "direction_terms": {
    "N": ["north", "northern", "northward", "northwards"],
    "S": ["south", "southern", "southward", "southwards"],
    "E": ["east", "eastern", "eastward", "eastwards"],
    "W": ["west", "western", "westward", "westwards"],
    "NE": ["northeast", "north-east", "northeastern", "north-eastern"],
    "NW": ["northwest", "north-west", "northwestern", "north-western"],
    "SE": ["southeast", "south-east", "southeastern", "south-eastern"],
    "SW": ["southwest", "south-west", "southwestern", "south-western"]
  },
  "westerly": ["W", "NW", "SW"],
  "chamber_number_words": {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "several": 2, "many": 2},
  "chamber_nouns": ["chambers", "rooms", "halls", "burial chambers", "burial rooms"],
  "single_chamber_phrases": ["single chamber", "one chamber", "single room", "one room", "single burial chamber", "one burial chamber", "a single room", "a single chamber"],
  "kokh_terms": ["kokh", "kokhim", "kokim", "loculus", "loculi"],
  "ossuary_terms": ["ossuary", "ossuaries"],
  "repository_terms": ["repository", "repositories", "bone pit", "bone pits", "charnel", "bone repository", "collecting pit", "pit for bones"],
  "slab_terms": ["slab", "slabs", "rolling stone", "blocking stone", "closing stone", "sealing stone", "stone door", "blocking slab", "cover stone", "covering stone"],
  "channel_terms": ["channel", "channels", "conduit", "conduits"],
  "wadi_terms": ["wadi", "wady", "nahal", "naḥal", "valley", "ravine", "streambed", "stream bed", "gorge"],
  "grave_field_terms": ["graves", "grave", "cemetery", "cemeteries", "shaft grave", "shaft graves", "cist grave", "cist graves", "pit grave", "pit graves", "trench grave", "trench graves", "field of graves", "burial ground"],
  "family_type_terms": ["kokh", "kokhim", "kokim", "loculus", "loculi", "arcosolium", "arcosolia", "bench", "benches", "burial chamber", "burial chambers", "burial cave", "burial caves"],
  "unused_terms": ["unfinished", "unused", "never used", "not completed", "incomplete"],
  "names": {
    "zadok": ["Zadok", "Zadoq", "Sadok", "Ṣadoq", "Tsadok"],
    "absalom": ["Absalom", "Avshalom", "Abshalom"],
    "queen": ["queen", "Helena", "Helene", "Adiabene", "malkata", "malkatah", "malkat"],
    "obed": ["Obed", "Oved", "ʿOved", "'Oved", "Ovad"],
    "jericho": ["Jericho", "Yeriho", "Jerichoite"]
  },
  "scroll_mention_terms": ["Copper Scroll", "3Q15"],
  "branches": {
    "14-M62": {"clauses": ["L_millo", "F13"], "headline": "A"},
    "14-P06": {"clauses": ["L_millo", "F14"], "headline": "A"},
    "14-NAME": {"clauses": ["L_name_only"], "headline": "AB"},
    "24-J": {"clauses": ["L_road", "F19"], "headline": "B"},
    "24-A": {"clauses": ["L_east_road", "F19"], "headline": "B"},
    "27-T": {"clauses": ["name_queen"], "headline": "AB"},
    "27-D": {"clauses": null, "headline": null, "note": "non-funerary: not scored"},
    "48-Y": {"clauses": ["F1", "name_absalom"], "headline": "A"},
    "48-L": {"clauses": ["name_absalom"], "headline": "A"},
    "51-S": {"clauses": ["L_south_corner", "name_zadok", "F2x"], "headline": "A"},
    "51-O": {"clauses": ["F12", "name_zadok", "F2x"], "headline": "A"},
    "51-J": {"clauses": ["L_south_corner", "F2x"], "headline": "A"},
    "52-M": {"clauses": ["F7w", "F6", "F14", "F17"], "headline": "A"},
    "52-P": {"clauses": null, "headline": null, "note": "non-funerary landmark: not scored; proxy F7w+F14 reported"},
    "52-L": {"clauses": null, "headline": null, "note": "non-funerary landmark: not scored"},
    "53-P": {"clauses": ["L_temple"], "headline": "A"},
    "53-K": {"clauses": ["L_name_only"], "headline": "A"},
    "54-P": {"clauses": ["F20_communal", "L_jericho"], "headline": "B"},
    "54-L": {"clauses": ["F20_family", "name_obed", "L_jericho"], "headline": "AB"},
    "54-M": {"clauses": ["F20_family", "F5", "L_jericho"], "headline": "AB"},
    "54-W": {"clauses": ["F20_communal", "F21"], "headline": "A"},
    "56-P": {"clauses": ["F10", "F7w", "F11"], "headline": "A"},
    "56-M": {"clauses": ["F10", "F7w", "F16"], "headline": "A"},
    "56-L": {"clauses": null, "headline": null, "note": "non-funerary: not scored"}
  },
  "date_sets": ["strict", "lenient", "any"]
}
```
