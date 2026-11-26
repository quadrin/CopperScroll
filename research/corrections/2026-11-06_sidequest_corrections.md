# Corrections from the side-quest swarm, 6 November 2026

**Scope.** This branch applies or proposes corrections to the project's own files that the side-quest swarm documented and independent reviewers checked. Full cards and reviews: `research/sidequest_2026-11-06/` on branch `claude/sidequest-2026-11-06-summary` (`SUMMARY.md`, "Corrections for the owner"). Nothing here is an identification. No rating, outcome-ledger entry, PROGRESS_METRICS, ACTIVE_TEST decision or atlas datum is changed. No frozen table is edited.

## A. Proposed errata for frozen tables (no frozen file changed)

| File | What | Where |
|---|---|---|
| `research/regional/water_systems/` | 35 field-level errata. Coordinates: J15 Hisham's Palace 4.3 km off; J19 St Andrew placed to about 200 m; WBADB S4146 = Mar Saba counted twice. Wrong `dup_of` links (Hirschfeld 1983 read as 1985; Kloner [101] book numbers read as ASI-online sequence numbers). Lower Herodium flagged (value not in hand). ASI 109/4 sign note. | `ERRATA_2026-11-06.md`, `errata_2026-11-06.csv` |
| `research/comparanda/hoards_full/` | Three missing deposits: Gerizim silver hoard (the first `temple_related` = 1), Gerizim bronze hoard, Vespasian Coins Cave crack cache. Proposed in the catalogue's 48-column schema; derived columns left to `hoards_full.py`. | `ADDITIONS_2026-11-06.md`, `proposed_additions_2026-11-06.csv` |

The water lane cannot be rebuilt here: the WBADB file and the ASI cache are not in the repository. A rebuild, or a re-run of the hoard comparison, after seeing these items is a new exploratory model under AGENTS.md. The frozen results stand.

## B. Notes corrected in place (dated, original text kept)

| File | Correction | Card / review |
|---|---|---|
| `research/OPEN_QUESTIONS.md` (R07) | The "Current follow-up (8 October)" line still says Kallai 1972 pp. 172–173 are unread; the 19 October entry records them read. A dated note marks it superseded. | D1-3 / R5 |
| `research/assessments/entry29_jericho_pools/README.md` | (1) The Plans 14/15/23 "not located" rows predate the NLI photographs of 21 Oct; a dated note points to the later record. (2) "Meinardus 183–184 remains unread": the article (BSAC XVIII pp. 181–193 with plates) is in Drive `08 Working files/Unsorted source scans/`; a note gives the file IDs and what pp. 181, 183 and 184 say. | D1-3 / R5; A5-1, C1b-2 / R3, R4 |
| `research/sources/nli_photos_2026-10-21/avigad1954.md` | "IMG_0771.MOV was skipped" and "pp. 74–75 missing": the clip's frames 14 and 16 are pp. [74] and [75]. A note gives the Drive ID; transcription still to do (a Hebrew reader should check p. 74's measures). | A5-2 / R3 |
| `registration/avigad1962_kidron_ossuaries_extracted.md` | "Serial No. XXX" corrected to XXXI after the page image. | B3 (dead-end list; not separately reviewed) |

## C. Not changed here (owner's decision or outside `main`)

- **Run E (31 Oct) georeference of HEXAGON 1974 frame F014** (branch `claude/novel-2026-10-31-E`): about 2.2–2.4 km off at Jerusalem and about 520 m off at Tell es-Sultan. A 3-point correction is in `research/sidequest_2026-11-06/C1a/F014_3point_affine.json` (C1a-2 / R4). The run's branch is a finished record, so it is not edited.
- **Cave of Letters coding** ("no second metal deposit"): the metal-detector null reaches about 3.5 m, ERT debris about 6–7.5 m (C4-3 as weakened by R5). The coding should carry the depth limit.
- **Qumran plateau salvage record:** Hadashot 117 report 126 (Price) records the 2002 hand-dug shaft to 17 m that tested the 1990/1996 deep targets: natural stone lines (C4-1 / R5). The salvage records stop at S34–S36.
- **West Bank Hadashot coverage:** reports by the Staff Officer for Archaeology are almost absent from HA vols 117–128 (published 2005–2016), so a Hadashot silence at a West Bank place in those years is a publication gap, not a negative search (B1a-3 as corrected by R2).
- **Entry 24:** Mughâret Ekteif (SWP Memoirs III p. 220) now has a map position, about 2.4 km east of the project's `kuteif` point, with no record within 567 m (C2-1 / R4). Its position is in the private products only (site protection).
- **Kh. Abu Lahm (Q24 / entry 31):** Mandate card 8751's "4 km NE of ʿAin es-Sultan" is wrong; the ruin lies 2.2–3.2 km NW–NNW (D1-2 / R5).
- **Store tooling** (bucket, not the repository): `tools/hexview.py` should split `pages.jsonl` on `"\n"` only (it uses `splitlines()`, which breaks on U+2028), and `hexcog2.build_index` should skip `open-sources/` (its `manifest.json` has another format).
