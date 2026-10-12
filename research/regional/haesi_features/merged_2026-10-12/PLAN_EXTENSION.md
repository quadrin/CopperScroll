# Merged regional inventory, phases 1–4: frozen plan extension

Written 11 October 2026 by the phase-4 merge worker, before any pair of phase-4 reports or rows was compared with another report or row. Committed alone; that commit is the freeze record. Later changes go in `AMENDMENTS.md` in this folder; this file is not edited.

This is bookkeeping on an exploratory inventory. It makes no identification claim and changes no registered outcome. No row is re-coded: classes, datings, quotes and coordinates stay as the phase readers coded them.

## 1. What is adopted unchanged

- `../merged_2026-10-11/DEDUPE_PLAN.md` (commit bf4320f, SHA-256 `ff13b357ae37c558bf5cebba0db01541cc0d17db0d2b12e1c7b8fe0710be676f`), with its JSON parameters, read by the build from that file.
- `../merged_2026-10-11/AMENDMENTS.md` A1–A4 (SHA-256 `2ace5f1bd7c953fd32895d71cbf4a1815aa9b8d59b8dffe23045c71a26f3e723`).
- The 88 manual decisions of `../merged_2026-10-11/data/manual_decisions.csv` (SHA-256 `0bc4be61a5d3de93c7cf038c98c711f7a83fbd0772791b98751a3fd1c74089bb`), copied unchanged as the first 88 data rows of `data/manual_decisions.csv` here.
- For any pair of two phase 1–3 reports or rows, every rule, word list and decision applies exactly as frozen. Run on the phase 1–3 inputs alone, the build must reproduce the `merged_2026-10-11` report groups, sites and counts (a test checks this).
- The counting levels (§2), the zone rules (§3), the preferred-version and conflict rules (§4.4), the site rules S1–S5 (§5.2) and the outputs (§6) are unchanged.

A phase 1–3 report group or site can still change in one way only: two of them are joined through a phase-4 report or row that links to both (union is transitive). Every such join is listed in `report_groups.csv` and `sites.csv` and summarised in the README.

## 2. Phase-4 inputs (read only)

| Phase code | Reports | Feature rows |
|---|---|---|
| 4E ʿAtiqot | `../phase4_2026-10-11/part_e_atiqot/reading_r{1,2,3}/reports.csv` | `…/reading_r{1,2,3}/features.csv` |
| 4F IAA Reports | `../phase4_2026-10-11/part_f_iaa_reports/reading/reports.csv` | `…/reading/features.csv` |
| 4G QDAP | `../phase4_2026-10-11/part_g_qdap/reports.csv` | `…/part_g_qdap/features.csv` |
| 4H SWP, Guérin | `../phase4_2026-10-11/part_h_surveys/reports.csv` | `…/part_h_surveys/features.csv`, then `…/features_zone_unresolved.csv` |
| 4I ADAJ | `../phase4_2026-10-11/part_i_adaj/reports.csv` | `…/part_i_adaj/features.csv` |

The screen-level `reports.csv` and `features.csv` directly under `part_e_atiqot/` and `part_f_iaa_reports/` hold headers only and are not inputs. Input order (for row uids and site numbering) is phases 1–3 as frozen, then the table order above.

Rows of `features_zone_unresolved.csv` carry two zones (`Z2…|Z3…` or `Z3…|Z4…`). They get report groups and sites like any row and are **never counted** (`not_counted_reason = zone split (two zones)`).

## 3. Series, versions and ids

Each phase-4 report gets a series code from its report-id prefix: `ATQ` (ʿAtiqot), `IAAR` (IAA Reports), `QDAP`, `ADAJ`, `SWP` (Survey of Western Palestine Memoirs) and `GUE` (Guérin). The series code is the report's version series. The frozen R1 compares series codes, so ʿAtiqot rows coded as `Atiqot` and `'Atiqot` are one series.

Version rules:

- **ATQ.** One article is one report. A Hebrew article with an English summary in the same PDF is one unit, not two versions. ATQ articles join each other only by R1, R4, R5 (§4.2) or a manual decision.
- **IAAR.** Volumes and part-volumes of one monograph series on one excavation (for example nos. 63, 64, 67; nos. 52 and 66/1–3) join by R4 or R7.
- **ATQ and IAAR** are *final* series; `HA`, `ESI`, `HA-ESI print` and `HA-ESI online` are *preliminary* series. A final report joins a preliminary report by R4 or R6.
- **QDAP and ADAJ.** A round-up unit (QDAP: author field contains `round-up`; ADAJ: `screen` begins `ADAJ round-up heading`) joins a full article of the same series by R8. Two round-up units, or two full articles, join only by R1, R4 or a manual decision: seasons of one excavation stay separate report groups, as in phases 1–3, and meet at the site level.
- **SWP and GUE** are independent surveys (different observers and years). They are never versions of each other or of any other report; their rows meet other rows only at the site level.
- ATQ or IAAR with QDAP or ADAJ, and QDAP with ADAJ: only R1, R4 or a manual decision.

## 4. Added link rules for reports

### 4.1 Definitions

- **Phase-4 name keys.** For the name of a phase-4 report or row, the frozen key function (§5.1) is used with these additions: the phase-4 drop phrases and drop words and the phase-4 generic words of §7 are added to the frozen lists. Keys of phase 1–3 names are computed exactly as frozen.
- **N4 name test**, used for any pair in which at least one report is a phase-4 report: the frozen name test passes, or the non-empty Latin key of one report is a subset (as a set of tokens) of all Latin tokens of the other report's name (every segment, after drop phrases and drop words are removed, generic words kept); the same for Hebrew keys. For pairs of two phase 1–3 reports the frozen name test is used.
- **Place test** for a pair with a phase-4 report: the frozen position test if both positions are present, else the N4 name test.
- **Permits** (R4 and the contradiction check): the frozen A1 parsing, with two additions, done first: parenthesised text is removed from the permit field; and a part of the form `A-<number>/<year>` (year of two or four digits) is read as `A-<number>`, because IAA `A-` permit numbers run on across years and the HA-ESI reports print them without the year. Other prefixes (`S-`, `G-`, `B-`) keep the year.
- **Permit contradiction**: both reports have at least one permit and share none. R5–R8 never link a pair with a permit contradiction; such pairs are listed with outcome `not linked (permit contradiction)`.
- **Finds or specialist report**: an ATQ report whose `site_name` or `toc_item` contains (after the frozen `norm`) one of the finds words of §7 as a whole word, or whose `excavated_or_surveyed` contains `laboratory` or `study`. Every other ATQ report is a *site report*.
- **Current group**: the union-find group after the rules applied so far, in the order of §4.2.

### 4.2 Rules, applied in this order after the frozen R1, R4, R2, R3

- **R7 IAAR volumes of one excavation.** Two IAAR reports with the author test and the place test passing and no permit contradiction are linked.
- **R5 ʿAtiqot finds report to its site report.** Candidates are pairs of ATQ reports in the same volume, at least one of them a finds report, with the place test passing, no permit contradiction, and the author test or the N4 name test passing.
  1. For each finds report, its candidate site reports are taken. If they lie in exactly one current group, the finds report is linked to them. If they lie in two or more groups, the pairs are flagged `REVIEW: ambiguous` and nothing is linked automatically.
  2. Then pairs of two finds reports that are candidates are linked, unless either finds report was flagged ambiguous in step 1 (then `REVIEW: ambiguous`).
- **R8 QDAP or ADAJ round-up to full article.** One round-up unit and one full article of the same series, with the place test passing, no permit contradiction and article year − round-up year between −1 and +4. One to one, as the frozen R2: candidate pairs sorted by (position test used before name test, |year difference|, distance, report ids) and accepted when neither report is already paired by R8; a report with more than one candidate is flagged `ambiguous` (`REVIEW: ambiguous` when the accepted pair is one of several).
- **R6 final to preliminary report.** One ATQ or IAAR report and one report of a preliminary series, with the author test and the place test passing, no permit contradiction (§4.1: so the fallback is used only when at least one of the two records no permit; where both record permits, only R4 links them), and final year − preliminary year between −2 and +40. For each final report, its passing preliminary reports are taken. If they lie in exactly one current group, the final report is linked to all of them (a final report may cover several seasons, and several finals may join one preliminary report). If they lie in two or more groups, the pairs are flagged `REVIEW: ambiguous` and nothing is linked automatically.

### 4.3 Listing, review and manual decisions

- `pair_candidates.csv` lists every R5–R8 candidate pair, and every pair that meets a rule's series, volume and year conditions and passes at least two of the author, position and N4 name tests (a missing position fails), with each test and the outcome.
- `REVIEW: ambiguous` pairs must be closed by a manual decision (the build test fails while one is open), as in the frozen §4.3.
- Pairs that fail one required test but pass the other two are marked `LISTED: <test> failed` and are **not linked** unless a manual decision says `same`. They need no decision; their number is reported in the README as a possible over-count (a campaign counted twice).
- Manual decisions keep the frozen form and limits (§4.3): (a) closing or deciding a listed pair from the coded fields; (b) applying a phase reader's explicit statement in the source NOTES (or in a `notes` field of the reader's own tables) that two reports are the same campaign (kind `report`) or describe the same structure (kind `site`, rule S5). A reader's "probably", "possibly" or "uncertain" is not an explicit statement and is not applied. Every added decision is labelled INFERENCE and exploratory (made after seeing the candidates), with its reason and basis (the NOTES file and section, or the review list).
- A manual `same` for a report pair is applied even when no rule lists the pair; a manual `different` on a pair the rules would link prevents that link (for R4 as frozen; for R5–R8 likewise).

## 5. Sites

S1–S5 and amendment A4 are unchanged. Phase-4 rows enter them with their own coordinates, precision, zone and phase-4 name keys (§4.1). S2 joins rows without coordinates by key within one zone; for rows in `features_zone_unresolved.csv` the zone is the compound value, so they join only each other by S2. S4 (all report-located rows of one report group are one site) applies to the groups formed by §4.

## 6. Counts and the phase-4 contribution

Counts are by class × zone × `dated_in_window` at the three frozen levels, over phases 1–4. The phase-4 contribution is reported separately:

- **Level 1:** counted phase-4 rows.
- **Level 2:** a unit (report group, class, zone) is **phase-4 only** if all its counted rows are phase-4 rows; **shared** if it has rows from phases 1–3 and from phase 4; **phase 1–3 only** otherwise. For shared units, the README states how many have a dating summary different from the summary of their phase 1–3 rows alone. A phase-4 report group is **joined to earlier reports** if its group contains a phase 1–3 report; the README counts these by link rule.
- **Level 3:** the same three-way split for units (site, class, zone).
- The no-S2 bracket for sites is given for the whole inventory, as frozen.

## 7. Parameters (machine-readable)

```json
{
  "phase4_report_sources": [
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r1/reports.csv"],
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r2/reports.csv"],
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r3/reports.csv"],
    ["4F", "phase4_2026-10-11/part_f_iaa_reports/reading/reports.csv"],
    ["4G", "phase4_2026-10-11/part_g_qdap/reports.csv"],
    ["4H", "phase4_2026-10-11/part_h_surveys/reports.csv"],
    ["4I", "phase4_2026-10-11/part_i_adaj/reports.csv"]
  ],
  "phase4_feature_sources": [
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r1/features.csv"],
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r2/features.csv"],
    ["4E", "phase4_2026-10-11/part_e_atiqot/reading_r3/features.csv"],
    ["4F", "phase4_2026-10-11/part_f_iaa_reports/reading/features.csv"],
    ["4G", "phase4_2026-10-11/part_g_qdap/features.csv"],
    ["4H", "phase4_2026-10-11/part_h_surveys/features.csv"],
    ["4H", "phase4_2026-10-11/part_h_surveys/features_zone_unresolved.csv"],
    ["4I", "phase4_2026-10-11/part_i_adaj/features.csv"]
  ],
  "never_counted_sources": {"phase4_2026-10-11/part_h_surveys/features_zone_unresolved.csv": "zone split (two zones)"},
  "series_by_id_prefix": [["ATQ", "ATQ"], ["IAAR", "IAAR"], ["QDAP", "QDAP"], ["ADAJ", "ADAJ"], ["SWP", "SWP"], ["GUE-", "GUE"]],
  "final_series": ["ATQ", "IAAR"],
  "preliminary_series": ["HA", "ESI", "HA-ESI print", "HA-ESI online"],
  "final_minus_preliminary_years": [-2, 40],
  "article_minus_roundup_years": [-1, 4],
  "roundup_series": ["QDAP", "ADAJ"],
  "roundup_markers": {"QDAP": {"field": "author", "contains": "round-up"}, "ADAJ": {"field": "screen", "startswith": "ADAJ round-up heading"}},
  "permit_year_strip_prefixes": ["A"],
  "finds_words": ["coin", "coins", "numismatic", "hoard", "pottery", "ceramic", "ceramics", "glass", "vessel", "vessels", "lamp", "lamps", "find", "finds", "bone", "bones", "faunal", "fauna", "animal", "skeletal", "human", "anthropological", "osteological", "inscription", "inscriptions", "inscribed", "epigraphic", "ostracon", "ostraca", "graffiti", "papyri", "papyrus", "seal", "seals", "sealings", "bulla", "bullae", "scarab", "scarabs", "stamp", "stamped", "impression", "impressions", "bead", "beads", "jewelry", "jewellery", "metal", "metals", "objects", "artifacts", "artefacts", "figurine", "figurines", "sculpture", "mold", "mould", "radiocarbon", "plaster", "analysis", "analyses", "wood", "charcoal", "charred", "seeds", "fruits", "botanical", "archaeobotanical", "insects", "fish", "shells", "textile", "textiles", "leather", "skins", "inkwells", "assemblage", "assemblages"],
  "phase4_drop_phrases_en": ["english summary", "hebrew summary", "recent discoveries", "department of antiquities", "second half", "first half"],
  "phase4_drop_words_en": ["hebrew", "english", "arabic", "summary", "greek", "discoveries", "recent", "palestine", "jordan", "trans", "district", "government", "archaeological", "historical", "contribution", "contributions", "study", "analysis", "analyses", "evidence", "note", "notes", "list", "volume", "part", "ii", "iii", "iv", "late", "later", "early", "earlier", "intermediate", "medieval", "century", "centuries", "bce", "ce", "stratum", "strata", "levels", "coins", "coin", "pottery", "ceramic", "glass", "vessel", "vessels", "lamps", "skeletal", "human", "faunal", "inscription", "inscriptions", "fragments", "artifacts", "assemblage", "metal", "lead", "seal", "stamp", "scarab", "sculpture", "mosaic", "radiocarbon", "restoration", "production", "agricultural", "domestic", "worship", "planning", "custody", "chance", "small", "another", "between", "against", "during", "under", "below", "beneath", "outside", "side", "front", "face", "foot", "end", "main", "field", "expeditions", "grounds", "land", "group", "hoard", "chamber", "shaft", "courtyard", "cut", "stone", "oil", "esh", "les", "des", "aux", "sur", "une", "dans", "pres"],
  "phase4_generic_words_en": ["khurbet", "khurbat", "kharbet", "kharbat", "wady", "kusr", "kasr", "mugharet", "mugharat", "birket", "corner", "rock"]
}
```

## 8. Exposure before this freeze

Seen while planning (11 October 2026, Los Angeles):

- `AGENTS.md`; the phase-4 worker rules (`PHASE4_RULES.md`, scratchpad); `../merged_2026-10-11/` `DEDUPE_PLAN.md`, `AMENDMENTS.md`, `README.md`, `scripts/build_merged.py`, `tests/test_merged.py` and the first five lines of `data/manual_decisions.csv`; `../phase4_2026-10-11/README.md` and `PLAN.md`.
- Headers of every phase-4 input table (all equal the phase-2 columns); that report ids are unique across phases 1–4 (a uniqueness check, no comparison of content).
- Value counts per phase-4 table: series, year, access, `excavated_or_surveyed`, `location_status`, `region_zone`, grid, CRS, volume, permit and map-reference formats with digits masked, `coordinate_source` with the place id masked, report-id patterns, feature class, dating, row zone, precision; `toc_item` (first 40 characters, digits masked; for reader r2 these are article titles), `screen`, the four commonest authors, page formats, tier. Permit formats of phases 1–3 by series, digits masked.
- Latin key tokens that occur in three or more phase-4 reports (frequency list of words, used to choose the §7 word lists; no name was compared with another name), and counts of the readers' place hints in phase-4 rows (11 place ids).
- NOTES of the phase-4 readers: part E r3 "Same feature in more than one row"; part F reading "Same feature in two volumes of this batch", "Probable duplicates with merged_2026-10-11" and "Proposed changes"; the "Deviations and choices" and "Proposed changes" sections of part E r1, r2 and r3; the "Proposed changes" of parts G, H and I; and a keyword search (`same`, `duplicate`, `repeat`, `dedup`) over the NOTES and READMEs of parts E–I. These name many same-feature and same-excavation pairs (for example IAAR63/64/67 with HAESI-1219, 1285, 18755, 25927; IAAR52 with HAESI-873; IAAR66p1 with HAESI-1377; ATQ88 Cave 900; ATQ119 Channel 515; QDAP Citadel, Mefjer, Nasbeh; ADAJ Awarta and ʿUrif hoards). The keyword search also displayed the readers' own records of deviations G-D1 and H-D1, which quote a few words of held Jericho text and describe the held ʿAin ed Duk entry; no held source text was opened and nothing is coded from it.
- No pair of reports or rows was compared, sorted by name, or matched before this freeze, and no rule above was tried on the data.
