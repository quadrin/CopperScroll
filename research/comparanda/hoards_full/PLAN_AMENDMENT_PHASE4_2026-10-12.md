# Plan amendment: the merged regional inventory (phases 1–4) as an exploratory view (12 October 2026)

Written 12 October 2026 (UTC) by the phase-4 fold worker for this lane, before any `hoard_cache` row of the merged inventory was read, mapped to this lane, coded or compared with `hoards.csv`. `PLAN.md` (SHA-256 `1f0a90a9…0362c`, commit be266e2) is not edited. Its frozen results (`results.json`, `RESULTS.md`, `hoards.csv`) are not changed.

**Status: exploratory.** The frozen plan read the phase-1 HA-ESI table only (R1: two hoard rows, both out of window, none added). Using the merged inventory is a source extension made after the frozen results were seen. It never changes the frozen headline (main run DIFFERENT, D = 0.6808, 78 known-context units of 177). The results are a separate view beside it. No identification claim follows. No registered outcome changes. Every inventory row is already in the repository (exposed); none is unseen evidence.

## 0. This lane had no IAA amendment

Unlike the tombs, caves, columbaria and water-systems lanes, this lane never wrote `PLAN_AMENDMENT_IAA_2026-10-11.md` and never mapped the phase 1–3 inventory (`merged_2026-10-11`). So this amendment does both at once, on `merged_2026-10-12`. It reports two layers, so that the phase-4 part can be read alone:

- **view A:** the frozen catalogue plus the units from phase 1–3 rows (what an IAA fold would have added);
- **view B:** view A plus the units from phase-4 rows (`phase` starting with 4).
- **Phase-4 increment** = B − A.

The method is the IAA-view method of the other lanes (tombs §2–§7, caves and columbaria §4 for rows without coordinates), adapted to this lane's frozen rules (PLAN 4, 7, 8, 9, 10, 11). There is no earlier name-only rule of this lane to reuse; §4 below adopts the caves/columbaria rule.

## 1. What had been seen when this was written

- This lane's PLAN.md, README.md, RESULTS.md (all), the function list and lines 1–192 of `hoards_full.py`, the first 80 lines of its test file, the header and value counts of `hoards.csv` (object type, container, country, include, how found, `judaea_by_name`, origin, first read, depth datum, landmark) and two of its rows (chre5386, n_givati_rings).
- The precedent's PLAN.md (all) and `concealment.py` lines 100–140 and 255–375.
- The rules `FOLD4_RULES.md` and `PHASE4_RULES.md`; the tombs IAA amendment (all); the lines of the caves, columbaria and water-systems IAA amendments that state their rules for rows without coordinates; lines 60–100 of the caves `iaa_view.py`; the header of `places_v2.csv`.
- `merged_2026-10-12/README.md` (all), including the class × zone × dating tables: `hoard_cache` 77 counted rows (22 yes / 51 no / 4 unknown); phase 4: 29 rows (6 / 21 / 2), 21 phase-4-only report units, 15 phase-4-only site units.
- `phase4_2026-10-11/README.md` (all). It names, among in-window QDAP rows, "the Silwan shekel hoard (findspot from a dealer)", and lists "Awarta and ʿUrif hoards" among known cross-source duplicates.
- The integrator's task message names phase-4 hoard rows: the Murabbaʿat Ptolemaic hoard (ʿAtiqot 112), the Silwan shekel hoard (QDAP), ADAJ hoards (Awarta, ʿUrif and others) and IAA Reports deposits. This lane's README already cites ʿAtiqot 112 (Murabbaʿat Cave II, abstract) and has a row for it.
- Value counts of `hoard_cache` rows in `features_all.csv` by phase: rows (1: 2, 2: 12, 3A: 10, 3B: 6, 3C: 9, 3D: 9, 4E: 8, 4F: 7, 4G: 2, 4I: 12), and by phase × series, counted, `dated_in_window`, zone, `excavated_or_surveyed`, `version_role`, and presence of `lat`. Value counts of `coordinate_source` patterns and `n_features` over all classes.
- **Not seen:** any `hoard_cache` row's site name, subtype, quote, period, coordinates, pages or report id, in any phase; any phase-4 reader's NOTES; any part's feature table.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-12/features_all.csv` and `report_groups.csv`, `sites.csv` (commit 7cac03b); SHA-256 recorded in the output and checked by the tests.
- Only what the inventory coding states is used: `report_id`, `series`, `volume`, `year`, `pages`, `site_name`, `lat`, `lon`, `coordinate_source`, `feature_type`, `feature_subtype`, `quote`, `n_features`, `period_as_given`, `dated_in_window`, `excavated_or_surveyed`, `protected_strip`, `phase`, `report_group`, `site_id`, `row_uid`, `counted`, `count_zone`, `version_role`. No report is re-read. A phase-4 reader's NOTES may be read after this freeze only for a reader statement that two rows are one deposit (§6).
- The frozen catalogue: `hoards.csv` as committed (204 rows), used unchanged.

## 3. Rows, units and protected material

- **Class.** Counted rows with `feature_type = hoard_cache`. No other class.
- **Versions.** Tombs §4, unchanged: rows of the preferred or single version of a report group are units; rows of an alternate version are units only when no preferred or single row of that group has this class.
- **Unit.** One inventory row = one cluster (`cluster_id` = `row_uid`). For run s7 (rows), a row with a numeric `n_features` = k > 1 is expanded to k rows with the same cluster id; otherwise one row.
- **Protected.**
  - A row with `protected_strip = yes`, or whose site name, subtype or quote names Tell es-Sultan, is excluded (`exclusion_reason = protected: Tell es-Sultan`) and nothing else is coded from it.
  - A row whose site name, subtype or quote names Kh. ʿAlmit (`almit`, `ʿalmit`, `'almit`) is excluded the same way and compared with nothing.
  - **Held cave areas.** A row whose text has a cave word (§5) and whose text names a held area (Qumran, Feshkha/Fashkha, Qarantal/Quruntul/Kuruntul, Nuweiʿimeh/Nueima, ʿAin Duk/Duq/Dyuk, Qelt/Kelt) is excluded (`protected: held cave area`) and listed by row id only. The phase-4 readers gave held caves no feature row, so none is expected; any found is reported.

## 4. Region, positions and rows without coordinates

- **Main region (precedent §4).** Every counted row lies in a zone Z1–Z4, all inside Israel, the Palestinian Territories or Jordan. `country` is written "southern Levant (inventory zone Zn)" and is coded inside the main region. Coordinates are not needed for this.
- **Sensitivity region (boxes J and V).** A row with `lat`/`lon` is tested against the boxes. A row without coordinates is placed at its reader's place id (`name only (<id>)`, `feature site name (<id>)` and the other `(<id>)` forms) from `places_v2.csv`, if that place has a point (the caves/columbaria rule); `judaea_by_name` = 1 if that point lies in a box, else 0. A row with neither is outside the sensitivity region (precedent §4: "Israel" or "Palestine" alone is outside).
- Positions serve only these tests and the duplicate test (§6).

## 5. Coding (precedent §3, §5, §8; this lane's PLAN 8–10), from the coding fields only

**Text** = `feature_subtype` + ". " + `quote` (lower case). The site name is used only for protected and held tests and the duplicate test. Every regex hit below is checked by hand against the coding fields (§7).

- **Date (precedent §3; midpoint rule).** From `period_as_given`, in this order:
  1. Explicit years: every number followed by BCE/BC (negative) or CE/AD (or preceded by AD); `date_from` = min, `date_to` = max.
  2. Otherwise centuries: "Nth century BCE" → −100N … −100(N−1)−1; "Nth century CE" or "Nth century" alone → 100(N−1)+1 … 100N. Early/late/mid qualifiers are ignored.
  3. Otherwise named periods, union of all matched (from = min, to = max): Iron Age −1200…−586; Persian −539…−332; Ptolemaic −301…−200; Seleucid −200…−141; Hellenistic −332…−37; Late Hellenistic or Hasmonean −141…−37; Herodian −37…70; Early Roman −63…135; Second Temple −141…70 (the phase-2 reading of the term as late Second Temple); First Revolt or Great Revolt 66…70; Bar Kokhba or Second Revolt 132…135; Roman (alone) −63…324; Middle Roman 70…250; Late Roman 250…363; Byzantine 324…638; Early Islamic, Umayyad 638…750; Abbasid 750…969; Fatimid 969…1099; Crusader 1099…1291; Ayyubid 1187…1260; Mamluk 1260…1516; Ottoman 1516…1917; Mandate or British 1917…1948.
  4. Otherwise, if `dated_in_window = yes`: −141…135 (the phase-2 window), flagged `date from dated_in_window`.
  5. Otherwise no date: excluded and listed (precedent §3).
- **Eligibility (precedent §5).** The reader coded a hoard or cache. Excluded on the text: `single coin|one coin|a single` (single coin); `grave goods|funerary offering|with the (deceased|body|skeleton)|in the coffin` (grave goods); `foundation deposit` (excavator's classification); `votive` (votive); `(mint|workshop) (debris|waste)` (workshop debris). Otherwise included.
- **Object class.** documents: `scroll|document|papyr|manuscript`; coins: `coin|shekel|tetradrachm|didrachm|denar|prut|drachm|sela|obol`; metal: `jewel|gold|silver|bronze vessel|vessels|weapon|sword|tool|ingot|bullion|ring|earring|bracelet`. Two or more → `coins_and_metal` (coins and metal) or `mixed`; none → `coins` if the word hoard is in the text, else `mixed`. `object_type` = the subtype as given.
- **Setting (precedent 8.1).** Patterns, all recorded: cistern `cisterns?`; pool_reservoir `pool|reservoir|miqw?e|miqva|mikve|ritual bath|basin|spring`; channel `channel|aqueduct|conduit|drain|outlet`; tomb `tomb|burial cave|kokh|loculus|loculi|mausoleum|funerary`; cave `cave|rock shelter|crevice|fissure|hiding complex|refuge`; structure `house|room|courtyard|shop|street|building|fort|casemate|tower|storeroom|store room|columbarium|dovecote|underground chamber|bathhouse|palace|synagogue|villa|farmhouse|church|monastery|structure|wall|floor|niche|threshold|doorway|pillar|column|locus|installation|silo`; ruin_heap `ruin|heap|cairn|mound|collapse|debris`; open_ground `field|open ground|open area|slope|road|quarry|garden|terrace`. Precedence (precedent: the water installation, tomb or cave is the setting): cistern > pool_reservoir > channel > tomb > cave > structure > ruin_heap > open_ground; no hit → unknown.
- **Placement (precedent 8.2, its order).** under_stone_threshold `under (a |the )?(large |flat )?(stone|slab|threshold|doorway|door|step|steps|paving)`; wall_cavity `niche|in(side)? (a |the )?wall|between (the )?(wall )?stones|crack|door-?frame`; pillar `pillar|column`; under_floor `(under|beneath|below|in|into) (a |the )?(\w+ )?floor|between (the )?floors|pit|buried`; container_buried: setting open_ground and a container; corner `corner`; upper_storey `upper (storey|story|floor)`; floor_surface `on (a |the )?floor|scattered|ash`; else not_stated.
- **Container.** `jar|jug|juglet|pot|vessel|box|chest|purse|bag|pouch|cloth|bundle|lamp|flask|bowl` → the matched word.
- **How found (precedent 8.5).** looting_recovered `dealer|market|looted|loot|confiscat|seized|antiquities trade|robbers?`; else chance `chance|accident|farmer|shepherd|resident|bulldozer|by workers`; else `excavated…` or `…surveyed` in `excavated_or_surveyed` → excavation; else unknown.
- **Depth (PLAN 9).** `(\d+(?:\.\d+)?)\s*(?:[-–]|to)?\s*(\d+(?:\.\d+)?)?\s*(m|cm)\b` within the text, with `depth|deep|below|beneath|under` in the same text; range → midpoint; cm → m. Datum: `below (the )?(present |modern )?(surface|ground)` → present_surface; `below (the )?floor` → ancient_floor; `below (the )?(top|mouth|opening)` → feature_top; else unstated. A height above a floor is not a depth.
- **Landmark (PLAN 10).** This lane's comparanda expressions (corner, step, pillar, threshold, gate, wall_face as in PLAN 10 and `hoards_full.py`) on the text. `none_stated` when the setting is known and nothing hits; empty when the setting is unknown. Strict variant as frozen.
- **Temple-related.** `temple` in the text → 1, else 0.
- `origin` = `iaa_p13` (phase 1–3 row) or `iaa_p4` (phase-4 row); `first_read` = `after_freeze`; `unexposed_at_freeze` = 0; `sources_pages` = series, volume, year, pages and report id; `discovery_year` empty (the inventory gives the report year, not the find year).

## 6. Duplicates (PLAN 7, adapted)

PLAN 7 needs a find year, a coin count or a closing date. The inventory gives none of these as fields. So:

- **Candidates against `hoards.csv`** (all 204 rows, eligible or not): an inventory unit and a catalogue row are a candidate pair if (a) both have coordinates and lie within 1.0 km, or (b) their normalised site names share a name token (lower case, diacritics and ʿ ʾ ' removed, generic words dropped: kh, khirbet, khirbat, horbat, hurvat, tel, tell, wadi, nahal, ein, en, ain, el, al, the, of, site, cave, area, street, st, quarter, a, b, c, and numbers), and their date ranges overlap or either is unknown.
- **Candidates among inventory units:** units in different report groups with the same `site_id` and overlapping or unknown dates.
- **Decision by hand** for each candidate pair, from the coded fields only (both sides: site, date, object type, counts in subtype or quote, discovery year, source and pages), plus any reader statement in a phase-4 NOTES file or `notes` that the two are one deposit: `same`, `different` or `undetermined`, with a one-line reason, in `data/phase4_dedupe_decisions.csv`.
- **Rule.** A unit decided `same` as a catalogue row is not added (the catalogue row is kept unchanged). Main view: `undetermined` is treated as `same` (not added). Sensitivity: `undetermined` counted as new. Among inventory units, the unit of the earlier phase, then the lower `row_uid`, is kept.

## 7. Manual check (the IAA-view rule)

Each regex code of §5 (setting, placement, depth, landmark, exclusion on eligibility) is read against the coding fields, in `data/phase4_manual_check.csv`. The check may confirm a code, choose another setting or placement **that the patterns also proposed**, or set it back to unknown / not_stated / empty, with a reason. It may not add a code no pattern proposed. It may exclude a row only on an explicit precedent §5 ground stated in the coding fields (quoted). The number of changes is reported.

## 8. Runs and outputs

- `scripts/phase4_view.py` (standard library; imports `hoards_full.py`, which hash-checks the precedent) builds the units, applies §3–§7, and runs the precedent's ten runs, its bias checks, and this lane's x1 and x3 runs, unchanged (seed, permutations, bootstrap, decision wording), on: the frozen catalogue (must reproduce `results.json`), view A and view B; plus view B with `undetermined` counted (sensitivity). Runs x2 and x4 (new rows only) are run on the inventory units alone. The depth and landmark descriptions of PLAN 9 and 10 are recomputed for views A and B.
- Outputs: `phase4_view_2026-10-12.csv` (one line per inventory hoard row: ids, phase, protected or held status, version selection, coded fields, duplicate decision, in view A / B), `phase4_scores.csv` (per view × run: n, known, unknown, D, CI, p, verdict, and coarse-group counts), `phase4_summary.json`. It never writes `hoards.csv`, `results.json` or `RESULTS.md`.
- **Tests:** this amendment's SHA-256 (recorded in the code); the frozen catalogue run reproduces the committed `results.json` runs; the frozen files are unchanged; the view rebuilds byte-identically; no excluded protected or held row is in a view.

## 9. Reporting

As the frozen README: the verdict word with D, p and known/unknown counts, per view and run, beside the frozen run; which new units enter which coarse group, landmark class and depth list, with source unit id and printed page; the units that stay unknown or are excluded, with reasons. A change in a verdict word in a view is exploratory and is not a result of the frozen plan.
