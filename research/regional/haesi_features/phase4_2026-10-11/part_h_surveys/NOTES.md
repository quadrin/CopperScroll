# Part H notes: nineteenth-century surveys (SWP Memoirs III and II, Guérin Judée I)

Worker notes for phase 4, part H (frozen scope `../PLAN.md`, row H; rules of the phase-2 plan `../../phase2_2026-10-10/PLAN.md` with amendments A1–A4). Session of 2026-10-11. Branch `worktree-agent-a09887456b1215731`, not pushed.

## What was read

| Source | archive.org id | Section screened | Headings screened | Read |
|---|---|---|---|---|
| SWP Memoirs III, Judaea (1883), Sheets XVII–XXVI | `surveyofwesternp03conduoft` | Section B (archaeology) of each sheet; the appendix not screened | 1,058 | every candidate (163 coded, 3 held) |
| SWP Memoirs II, Samaria (1882), Sheets IX–XVI | `surveyofwesternp02conduoft` | Section B of each sheet | 677 | every candidate (15) |
| Guérin, *Judée* I (1868) | `descriptiongeogr01guer` | every site heading of the volume | 82 | every candidate (22) |
| Guérin, *Judée* II, *Judée* III, *Samarie* I | `descriptiongeogr02guer`, `03guer`, `04guer` | — | 0 | not read (time limit) |

All archive.org requests returned HTTP 200 (OCR files `_hocr_searchtext.txt.gz`, `_hocr_pageindex.json.gz`, `_djvu.txt`, item metadata); requests were at least 3 s apart. No request was blocked. OCR text stayed in the scratch folder.

Printed pages come from the running heads of the hOCR page index, chained between anchors. In SWP III, leaves 136–137 are a duplicate scan (dropped) and a few leaves carry plates; in SWP II, leaves 457–464 repeat pp. 409–416 and pp. 401–408 are missing from the scan (no entry there could be screened).

## Method in brief

- **Units.** One SWP site entry (heading in Section B with its square) or one Guérin site heading = one unit. Unit ids `SWP<vol>-<page>-<slug>` and `GUE-J1-<page>-<slug>`. Sub-headings that describe parts of one site were merged into the parent (`data/swp_fixes.csv`, `data/gue_fixes.csv`, each with a reason).
- **Placement.** SWP reference squares were turned into zones with an affine fit of the SWP grid on repository coordinates (`data/swp_grid_calibration.csv`, `scripts/swp_grid.py`). A square counts as clear only if the whole square, widened by 0.25 square (about 2.3 km) on every side, lies in one phase-2 zone or wholly outside the region. Otherwise the name was tried against the frozen phase-2 gazetteer within the zones the square touches. Guérin gives no map references, so his headings are placed by name only (`coordinate_source = name only`). Sheets wholly outside the region (SWP III XIX, XX, XXIII, XXIV; SWP II IX, X, XIII, XVI) are out by sheet. Region-wide terms never place.
- **Order.** T1 → T2 → T3 as phase 2 defines them, ascending SHA-256 of the unit id within a tier. Each screen was committed before its reading began (commits `c00fe61`, `6c11592`, `1ddb417`).
- **Coding.** Classes, in-window rule and columns as phase 2. `excavated_or_surveyed` is `surveyed` (SWP) or `inspected` (Guérin). `dated_in_window` is `unknown` unless the author dates the feature itself; A4 applied (hedged dates follow the named period; modern → no; site-level dating only → unknown). Each feature row carries a label in `feature_subtype`: observed remains or author's function label. `period_as_given` keeps the author's words.

## Deviations and choices (exploratory)

- **D1 (held text read in error).** While checking the section structure of SWP III, the 'Ain ed Duk entry (p. 190; `surveyofwesternp03conduoft_djvu.txt` lines 9957–9964: a kokim tomb chamber and caves near the spring, Jericho escarpment) was displayed in full before the hold check. Reading stopped there. It is recorded in `held.csv` and not coded. The same page sample also showed Beit Jubr et Tahtani and Bir Abu Shualeh before the order was frozen; neither is held, and both were coded only at their frozen positions.
- **Kilia (SWP II)** was read without a separate first-line check; it lies well outside the held stretch.
- **Calibration groups.** SWP II uses a fit on vol. II and III points together; SWP III keeps its own vol. III fit, so its frozen screen did not change (checked byte for byte after each change).
- **Zone-split squares.** 119 read units lie in squares that are wholly in the region but straddle two zones (Z2|Z3 or Z3|Z4) and match no gazetteer term in either. They were read and coded, and their 94 rows are kept apart in `features_zone_unresolved.csv` (same columns, compound zone). The integrator decides whether to use them.
- **Squares split by the region boundary.** 360 SWP entries (160 in III, 200 in II) lie in squares that cross the region boundary and match no gazetteer term. They are listed as unlocated and were not read.
- **Spelling variants.** `data/name_variants.csv` maps SWP and Guérin spellings to gazetteer terms (for example *Kolounieh* → *moza*). These are exploratory choices with reasons.
- **Long Guérin units.** Units of more than 60 paragraphs (Bethlehem, Souba, Neby-Samouil, A'in Karim, Kiriet el-Anab p. 62, Beth-Horon lower, Beit-Hanina) were read by keyword location: every paragraph containing a French feature word (citerne, piscine, birket, aqueduc, grotte, caverne, tombeau, sépulcre, pressoir, taillé/creusé dans le roc, etc.; list in the reader script) was read in full, plus the opening paragraphs. `reports.csv` (`text_lines`) gives the scope of each. A feature described without any keyword would be missed.
- **SWP Section A** (topography, water) was not screened: site entries are in Section B.
- **Mogheifir** (SWP III): the cistern's dating was changed from `no` to `unknown` before the tables were built, because the date given belongs to the site, not the cistern (A4).
- **Missed headings found while reading** (not in the screen; nothing coded from them): SWP III Tell Abu Zelef (O s, p. 221; no feature), 'Alaly el Benat (p. 62, inside 'Ain Yalo); SWP II Kh. et Tuweiyil (O p, p. 395), Jett (J l, p. 193); Guérin I Cha'fath (p. 395, inside Beit-Hanina; its pool is coded under Beit-Hanina, same zone Z4 through the gazetteer term *shufat*) and Kharbata (p. 347, inside Beit-A'our el-Fouka; cisterns and "tombeaux antiques" shown to Guérin; no gazetteer match, not coded). The SWP III Mukhmas entry breaks mid-sentence in the OCR.
- **Guérin unlocated headings of note.** These match no gazetteer term and stay unlocated under the rule, though some may lie in Z4: El-Djib (Gibeon, p. 385), Lifta (p. 252), Tombeau de Rachel (p. 224), Aqueduc (p. 236), Désert de Saint-Jean (p. 102), Couvent de Sainte-Croix (p. 77), Merhaïr ez-Zenanir (p. 262), Biddou (p. 362). Full list in `screen.csv`.

## Held and protected

`held.csv` holds six records: 'Ain ed Duk (D1, whole entry), Jebel Kuruntul with its sub-heading "Chapels and Caves" (whole entry, held from the first line), Tell es-Sultan paragraph 6 (north strip, `protected_strip = yes`, citation only), Deir el Kelt paragraphs 1 and 76 (cliff text held by caution; the built monastery was read), and Kh. ʿAlmit (Tier-1, extraction only, `tier1_kh_almit_extraction.md`).

## Not read

- Guérin *Judée* II, *Judée* III, *Samarie* I: not read (time limit). No screen was made, so no tier positions exist for them. Judée III probably covers the Jericho area and the country north-east of Jerusalem (ʿAlmit, Quruntul, Wadi Qelt); the cave holds would apply there.
- 360 SWP entries in squares split by the region boundary, 27 SWP entries with no usable square and no name match, 56 Guérin headings with no gazetteer match: unlocated, not read.

## Figures worth archiving (not stored)

SWP Memoirs III: Deir el Kelt plan; Kh. Murussus plan; Kh. el Burj plan; Jisr ed Deir plan and elevation; Kusr Hajlah plan; Bir Beit Bassa tomb plan and section (p. 87); Mugharet Masa plan and PEF photograph 177; Telilia plan; Kh. Tekua font drawing; Masada plan and PEF photographs 286–288; El Bireh plan and photographs 105–106; Neby Samwil plans; Herodium plan; Kubbet Rahil photograph 250; Kuryet el Enab photograph 153; Tell es-Sultan plate "Aqueducts near Jericho"; Tellul Abu el 'Aleik sections. SWP Memoirs II: Gerizim plans and PEF photographs 88, 89, 91, 126, 127, 220; Nablus photograph 94. Page numbers other than those given need checking in the scan before archiving.

## Proposed changes for the integrator

1. Add the 22 Guérin and 178 SWP units to the merged inventory from `features.csv`; decide separately on `features_zone_unresolved.csv` (94 rows whose zone is certain only as Z2|Z3 or Z3|Z4).
2. A georeferenced SWP gazetteer (for example the PEF name lists keyed to the 1:63,360 map) would place the 360 entries in squares split by the region boundary and resolve the zone-split rows.
3. Add gazetteer terms for el-Jib (Gibeon), Lifta, Kharbata and Shu'fat variants, then re-screen the Guérin unlocated headings as a new exploratory pass.
4. Guérin *Judée* II–III and *Samarie* I remain for a later session, starting with *Judée* III (ʿAlmit extraction; Jericho area holds apply).
