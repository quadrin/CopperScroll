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
- **Place and feature are the commonest weak links**: P limits 63 rows and F 56 (alone or with others), against D 24 and R 23. 32 candidates rest on no place evidence at all, only entry order or landscape.
- **U:** 72 untested, 18 not unique (a documented rival meets the same tested subset), 1 conditionally excluded (Siloam, entry 49: the ledger's two L103 exclusions).
- **Former "medium" ratings:** 14 are weak and 5 are none — 9 East Gate (F 0: no cistern within 18 m), 17 Buqeia (D 0), 18 ʿAṣla (F 0), 35 Mar Saba (F 0), 59 Kh. Ibziq (F 0: no conduit).
- **Highest sums** (each still weak): 16 Hyrcania and 29 Jericho palaces (R1 P3 F2 D2: only the restored word is weak), 57 Gerizim (R3 P3 F1 D1), 58 Beth Shean (R3 P2 F1 D2).

## Later changes

- **16 October 2026** (Perlego reads, [findings log](../../logs/findings_log.md#16-october-2026--perlego-reads-folded-in-eleven-books)): D rises from 1 to 2 for 51 and 53 at the south wall and for 51 at the SE corner. *The Southern Wall* (Baruch & Reich 2023) records a stratified Herodian stratum in Areas A–B (Tables 4.1–4.2 pp. 68, 80). No label changes; D now limits 25 rows, not 26. Entry 1's F and D basis now records the Early Roman houses and stepped cistern in Wadi Nuʿeima (Taha 2020 pp. 277–278); its levels do not change. Each changed row has a `review` note.
- **16 October 2026, later** (Lefkovits 2000 read from the owner's copy, [extraction](../../../registration/lefkovits2000_items3_5_7_extracted.md)): R rises from 2 to 3 for entry 3 (both candidates; all three editions read the court of the peristyle, the cistern and the upper entrance, p. 64) and from 1 to 2 for entry 5 (Puech and Lefkovits read samekh, the staircase; Milik dissents, pp. 90–93). Entry 7 keeps R 1; Lefkovits reads חמדה but calls every letter ambiguous (p. 110). No label changes; R now limits 23 rows, not 24. Entry 29's `decisive_next` now points to Plan 14, after Netzer 2001 pp. 74–84 were read ([extraction](../../../registration/netzer2001_pp74-84_extracted.md)).
- **16 October 2026, later still:** a new candidate for entry 27, the Givati monumental building (jer_givati), added at the owner's request as the dwelling-reading candidate (Unearthing Jerusalem ch. 13). Rated R 2, P 0, F 1, D 2, untested; label none. There are now 92 candidates plus entry 41: 47 none, 45 weak.
- **16 October 2026, JSTOR reads** ([Bethesda extraction](../../../registration/bethesda_jstor_2026-10-16_extracted.md); [Siloam extraction](../../../registration/siloam_jstor_2026-10-16_extracted.md); [Guil 2017](../../../registration/guil2017_siloam_extracted.md); [Bull, BASOR 190](../../../registration/bull_tell_er_ras_1965_1968_extracted.md)): F rises from 0 to 1 for entry 56 at Bethesda. Von Wahlde 2009 p. 128 reports a central cistern and grottoes with steps east of the twin pools, dated by coins to 68 CE, but no threshold or west entrance. The label stays none (P 0); F now limits 56 rows, not 57. Entry 55's D basis adds the pools' dates. Entries 49 and 57 keep their levels; their `decisive_next` now names the two Siloam channel junctions and BASOR 190.
- **17 October 2026** (Amit 1989 read from the owner's copy, [extraction](../../../registration/amit1989_doq_extracted.md)): D rises from 1 to 2 for 31 Doq. Herodian rooms were excavated on the fortress's north-east spur (Netzer 1982, reported by Amit), and the Hasmonean water system stayed in use. The label stays weak (R 1). Calibration example 31 in RUBRIC.md records the earlier value. Also: Duprez 1970 read for 55 and 56 (no level change).

## Files

- [ratings.json](ratings.json) — one row per candidate, with the anchor words, a basis and repository sources for each part, the observation that would most change the weakest part (`decisive_next`), and the raters' flags.
- [ratings.csv](ratings.csv) — the same, flat.
- [record_conflicts.md](record_conflicts.md) — 79 places where the atlas text or a table disagreed with a newer or more specific record, each resolved on 15 October: 51 corrected, 1 clarified, 15 not a conflict or needing no change, 12 left for owner decisions (candidate lists, statuses, confidence labels, one ledger question).
- `atlas/app/atlas-components.json` — the compact copy the atlas reads.

Rebuild after editing `ratings.json`: `python3 tools/build_evidence_components.py` (`--check` fails if an output is stale or a row is missing).

## Method

Five raters each took a block of entries (1–12a, 13–28, 29–37, 38–48, 49–60) from one brief, citing repository files for every level; background knowledge could only lower a level. All three calibration examples in the rubric came back with the same values. The 1,095 citations name 88 repository files; all exist. Five were checked against their text (feature constraints line 26, findings F12.4 and F11.3, the L103 ledger records, Phase 5 assessments line 4).

Integrator review, for consistency across raters (each change is noted in the row's basis and `review` field):

- **P = 0 where the entry names no place** (the rubric's level 0), in 13 rows the raters had put at 1 for an order-derived location: 3 (both), 12, 12a (both), 16 Tell es-Sultan, 23, 25 Qumran, 26, 27 (both), 28, 33. Also 40 ʿAin en-Naṭuf: the name read (Horon) points to Beth-Horon.
- **P = 3 under a restored name**, as the raters did for Beth-Horon (40), when the restored name is independently located: 16 Hyrcania, 29 Jericho (three candidates). The restoration is rated under R. 29 Hyrcania stays 1: its restored name is Kidron, tied to Hyrcania by one editor.
- **R = 1, not 0, for 12 and 12a**: the court name is lost but restored by each edition.
- **R may differ between candidates of one entry** when they rely on different words: 35 Hyrcania needs the minority sense "dam" (R 1), Mar Saba the agreed letters (R 2). The rubric's sentence that R repeats per entry is superseded on this point.
