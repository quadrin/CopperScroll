# Evidence components

Rated 15 October 2026 (Los Angeles). Every atlas candidate is rated on five parts of its case — reading (R), place (P), feature (F), date (D), each 0–3, and uniqueness (U) — under the [rubric](RUBRIC.md), which was committed before any rating (`6200ece`). The weakest of R, P, F and D sets the label. The ratings replace the atlas's single low/medium label in the atlas view.

This is a description of the evidence. It identifies nothing and excludes nothing; the [outcome ledger](../../progress/outcome_ledger.json) is unchanged.

## Result

91 candidates, plus entry 41 (no candidate):

| Label | Candidates |
|---|---|
| strong | 0 |
| partial | 0 |
| weak | 45 |
| none | 46 |

- **No candidate has every part at 2 or better.** No feature is rated 3 (all described elements present) and no date is rated 3 (the feature itself dated in the window). 15 candidates have a specific recorded feature (F 2).
- **Place and feature are the commonest weak links**: P limits 62 rows and F 57 (alone or with others), against D 26 and R 24. 32 candidates rest on no place evidence at all, only entry order or landscape.
- **U:** 72 untested, 18 not unique (a documented rival meets the same tested subset), 1 conditionally excluded (Siloam, entry 49: the ledger's two L103 exclusions).
- **Former "medium" ratings:** 14 are weak and 5 are none — 9 East Gate (F 0: no cistern within 18 m), 17 Buqeia (D 0), 18 ʿAṣla (F 0), 35 Mar Saba (F 0), 59 Kh. Ibziq (F 0: no conduit).
- **Highest sums** (each still weak): 16 Hyrcania and 29 Jericho palaces (R1 P3 F2 D2: only the restored word is weak), 57 Gerizim (R3 P3 F1 D1), 58 Beth Shean (R3 P2 F1 D2).

## Files

- [ratings.json](ratings.json) — one row per candidate, with the anchor words, a basis and repository sources for each part, the observation that would most change the weakest part (`decisive_next`), and the raters' flags.
- [ratings.csv](ratings.csv) — the same, flat.
- [record_conflicts.md](record_conflicts.md) — 79 places where the atlas text or a table disagrees with a newer or more specific record (uncorrected).
- `atlas/app/atlas-components.json` — the compact copy the atlas reads.

Rebuild after editing `ratings.json`: `python3 tools/build_evidence_components.py` (`--check` fails if an output is stale or a row is missing).

## Method

Five raters each took a block of entries (1–12a, 13–28, 29–37, 38–48, 49–60) from one brief, citing repository files for every level; background knowledge could only lower a level. All three calibration examples in the rubric came back with the same values. The 1,095 citations name 88 repository files; all exist. Five were checked against their text (feature constraints line 26, findings F12.4 and F11.3, the L103 ledger records, Phase 5 assessments line 4).

Integrator review, for consistency across raters (each change is noted in the row's basis and `review` field):

- **P = 0 where the entry names no place** (the rubric's level 0), in 13 rows the raters had put at 1 for an order-derived location: 3 (both), 12, 12a (both), 16 Tell es-Sultan, 23, 25 Qumran, 26, 27 (both), 28, 33. Also 40 ʿAin en-Naṭuf: the name read (Horon) points to Beth-Horon.
- **P = 3 under a restored name**, as the raters did for Beth-Horon (40), when the restored name is independently located: 16 Hyrcania, 29 Jericho (three candidates). The restoration is rated under R. 29 Hyrcania stays 1: its restored name is Kidron, tied to Hyrcania by one editor.
- **R = 1, not 0, for 12 and 12a**: the court name is lost but restored by each edition.
- **R may differ between candidates of one entry** when they rely on different words: 35 Hyrcania needs the minority sense "dam" (R 1), Mar Saba the agreed letters (R 2). The rubric's sentence that R repeats per entry is superseded on this point.
