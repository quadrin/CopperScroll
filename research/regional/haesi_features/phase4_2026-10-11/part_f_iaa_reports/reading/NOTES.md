# Notes: part F reading pass (reader r4), 11–12 October 2026

## Exposure

- Before reading I opened these:
  - the phase-4 and phase-2 plans and amendments, and the part-F screen files;
  - the phase-3 part C build and coding as a model;
  - the merged inventory's rows for these sites, opened only to write the duplicate notes below, after the coding was done.
- No arrival item, `chain.json` or held text was opened.
- `arrival.py check`: manifest ok.
- `exposure_at_freeze = unexposed at freeze` for all 12 units.

## What was read (printed pages)

| Unit | Read | Text |
|---|---|---|
| IAAR39 Tel Moẓa | pp. 1–7, 9–60 (Chapters 1–2) | text layer; 21 image-only pages by OCR |
| IAAR3 Manaḥat | pp. 1–36 (Introduction, Chapters 1–3); Chapters 4–5 scanned | OCR (no text layer); PDF ends at p. 69 |
| IAAR19 Abu Ghosh | pp. 1–21 (Chapters 1–3), 77–85 (Chapter 9) | text layer; 8 pages by OCR |
| IAAR69 Kathisma | pp. vii–ix, 1–116 (Preface, Chapters 1–3) | text layer; 3 plan pages by OCR |
| IAAR12 Efrata | pp. 3–41 (Introduction, Chapters 1–3); Chapter 4 scanned | OCR (no text layer); PDF ends in Chapter 4 (p. 77) |
| IAAR67 Western Wall Plaza III | pp. ix–xx, 3–23 (Foreword, Chapter 1) | text layer |
| IAAR66/2 Giv‘ati II, part 2 | pp. 271–374 (Chapter 12), 590–594 (Chapter 16) | text layer |
| IAAR66/3 Giv‘ati II, part 3 | pp. 749–751 (Chapter 21) | text layer |
| IAAR63 Western Wall Plaza I | pp. ix–x, 1–2, 17–115 (Chapters 2–3), 165–169 (Chapter 6) | text layer; 1 page by OCR |
| IAAR64 Western Wall Plaza II | pp. 283–284 (Chapter 6) | text layer |
| IAAR52 Giv‘ati I | pp. 1–62 (Chapters 1–2) | text layer; 20 image-only pages by OCR |
| IAAR66/1 Giv‘ati II, part 1 | pp. 1–70 (Chapters 1–2) | text layer; 1 page by OCR |

In every volume, the finds chapters were searched for hoards, caches and deposits:

- search terms: hoard, cache, favissa, genizah, concealed, hidden, intentional or foundation deposit;
- only the passages found were read.

## Deviations and choices (exploratory)

These choices were made while reading. The plans do not settle them. None changes a frozen rule.

1. **Long chapters.** The long chapters were not read line by line. Each passage naming an eligible feature was read in full; every other passage was skimmed by a keyword-in-context pass. The chapters are:
   - Kathisma Chapters 2–3;
   - Western Wall Plaza I Chapter 3;
   - Giv‘ati II Chapters 2 and 12.

   A feature named only with a word outside the search list could be missed.
2. **Pits and silos.** These were coded as `rockcut_installation` under plan §5, "pit or shaft not used as cistern":
   - storage silos, refuse pits and stone-lined sewage pits, whether earth-dug or built;
   - one built shaft (Giv‘ati I L728).

   The subtype says when they are not rock-cut. The rows are:
   - Tel Moẓa silos and pits;
   - Abu Ghosh Pit 102;
   - Giv‘ati II part 2 pits;
   - Giv‘ati I Stratum I pits and Shaft 728.

   The precedent is HA67-050, where built silos were coded with rock-cut ones. The integrator may prefer to keep only rock-cut pits (see the proposals below).
3. **Up to 135 CE.** Two Aelia Capitolina features were coded `yes` under the in-window rule's "up to 135 CE":
   - the Cardo quarrying in Western Wall Plaza III, dated to the "first third of the second century CE";
   - the Cardo drainage channels in Western Wall Plaza I, "before 130 CE".

   Both are post-70 Roman works. Western Wall Plaza I dates the same Cardo quarrying "Roman period or earlier", which is coded `unknown` there. Each volume is coded as its own text says.
4. **Hedged dates (A4).** Cistern 6170, which "probably originated in the Second Temple period", is coded `yes`. Quarry 9588 is dated differently in two volumes:
   - Western Wall Plaza III: "tentatively attributed to the Early Roman period", coded `yes` together with Quarry 8170;
   - Western Wall Plaza I: "First and/or Second Temple period", partial overlap, coded `unknown`.
5. **Class follows the label.** The Giv‘ati underground reservoir with Shafts 1339 and 1391A is named differently in two parts of the same volume:
   - part 1 calls it an "underground water reservoir" (`pool_reservoir`);
   - part 2 calls it "Cistern 1391" (`cistern`).

   It is the same feature. The subtype records the label.
6. **Caches.** These were coded as `hoard_cache`:
   - the Efrata tumulus vessel group ("probably intentionally placed—perhaps an offering");
   - the Kathisma favissa;
   - the bone-waste cache placed in a wall niche (Giv‘ati II part 2);
   - two astragali groups in refuse pits that the specialist calls "caches" (Giv‘ati II part 3).

   The last is a label only: the groups lay in refuse pits.
7. **Western Wall Plaza rooms.** Rooms L402 and L404, "hewn out like caves" in the cliff, were coded `cave_with_finds` (`unknown`), following HAESI-1219, which coded the same rooms.
8. **Map references.**
   - Where a range is printed, the first values are used (`geo.parse_ref`).
   - Efrata's reference is printed "1645 1175" without a slash; it is used as 1645/1175, and both are recorded.
   - Western Wall Plaza II and III and the three Giv‘ati II parts print no reference. They are placed by name, although sister volumes print one for the same site (IAAR63 and IAAR52). The reference was not copied across.
9. **Manaḥat miqweh.** It is coded from the Chapter 3 statement that Area 600 contains a miqweh 300 m south of the site, dated `unknown`. Chapter 14, which describes it, is not in the PDF. ESI 7–8 (`ESI07-117-manahat`) describes it as "in a cave".
10. **Efrata winepresses.** The two Byzantine winepresses are coded from the Introduction and Chapter 2. Appendix 1, which describes them, is not in the PDF.

## Same feature in two volumes of this batch

Rows are not deduplicated in this phase. Same-feature notes:

| Feature | Rows |
|---|---|
| Quarries 8170 and 9588 | IAAR63 and IAAR67 |
| Foundation-deposit coin hoard L4253 | IAAR63 and IAAR64 |
| Giv‘ati reservoir or Cistern 1391 (Shafts 1339, 1391A) | IAAR66p1 (`pool_reservoir`) and IAAR66p2 (`cistern`) |
| Abbasid pits | named in IAAR66p1 and IAAR52; coded in IAAR66p2 and, for Area M1 Stratum I, IAAR52 |

## Probable duplicates with `../../../merged_2026-10-11/` (HA-ESI and ESI reports of the same excavations)

The merged files were not changed. Each pair is INFERENCE from site, season, description and locus numbers.

**Jerusalem volumes (T3)**

| This pass | Merged row(s) | Same feature(s) |
|---|---|---|
| IAAR63 cistern `yes` (Cistern 6170) | HAESI-1219 cistern `yes` (hewn bell-shaped cistern re-roofed with slabs); HAESI-25927 cistern `no` (hewn cistern roofed with slabs on arches) | Cistern 6170; the two HA-ESI reports date it differently |
| IAAR63 ritual_bath `yes` (2022, 2050) | HAESI-1219 ritual_bath `yes`; HAESI-25927 ritual_bath `yes` (L2022) | Miqveh 2022 and Installation 2050 |
| IAAR63 channel `yes` (Low-Level Aqueduct L116) | HAESI-1219 channel `yes`; HAESI-1285 channel `unknown`; HAESI-25927 channels `yes`/`unknown`/`no` (aqueduct, deepening, Ottoman pipe) | the aqueduct section L116 |
| IAAR63 channel `yes` (Cardo drainage, before 130 CE) | HAESI-1219 channel `unknown` (drainage system below the cardo) | Channels 536, 8178, 8068, 547; dating differs |
| IAAR63 cistern `no` (300, 712, …) | HAESI-1219 cistern `unknown` (hewn cisterns under the western sidewalk) and cistern `no` | Cisterns 300 and 712 |
| IAAR63 rockcut `yes` (5336, Quarry 8170); IAAR67 rockcut `yes` (8170, 9588) | HAESI-1219 rockcut `yes` (quarry on the low terrace) | Quarry 8170 |
| IAAR63 rockcut `unknown` (9588 …); IAAR67 rockcut `yes` | HAESI-18755 rockcut `unknown` (quarry below W958) | Quarry 9588 |
| IAAR67 rockcut `no` (Iron Age quarry) | HAESI-1219 rockcut `no` (stepped quarries with severance channels) | the Iron Age quarry edge |
| IAAR63 rockcut `unknown` (L318 …) | HAESI-25927 rockcut `no` (rounded plastered installation with settling pit) | probably L318 |
| IAAR63 cave_with_finds `unknown` (L402, L404) | HAESI-1219 cave_with_finds `unknown` (hewn subterranean chambers, L402) | Rooms L402 and L404 |
| IAAR63 and IAAR64 hoard_cache `no` (minimi foundation deposit) | none found in merged | |
| IAAR52 cistern, ritual_bath, pool_reservoir `yes` (702, 704, 719, 714) | HAESI-873 cistern, ritual_bath, pool_reservoir `yes` (2008 report: built cistern, two miqwa'ot, bathtub) | the Stratum VII annex of Building 760 |
| IAAR52 channel `no` (601, 676 …) | HAESI-873 channel `no` (2 rows) | the drainage channels |
| IAAR66p1 hoard_cache `no` (264 solidi) | HAESI-1377 hoard_cache `no` | the Heraclius hoard |
| IAAR66p1 pool_reservoir `no`; IAAR66p2 cistern `no` (Cistern 1391) | HAESI-1377 pool_reservoir `no` (two underground plastered reservoirs); HAESI-5432 cistern `no` (cisterns of the Abbasid settlement) | probably the same reservoirs and cisterns |
| IAAR66p1 ritual_bath `yes` (miqveh under Reservoir 6388) | possibly HAESI-25886 cistern `no` ("the large miqveh converted into a water cistern") | uncertain: HAESI-25886 is a later season (2021 report) |
| IAAR66p1 channel `no` | HAESI-1377 channel `no` (roof gutter, pipe, plastered channels) | in part |

Not duplicated by my rows:

- HAESI-250 (the 2003–2005 Shukron–Reich season);
- HAESI-25405, 25886, 26089, 26474 and HAESI138-004 (Giv‘ati seasons after the volumes' scope);
- HAESI-25120, 25221 and 26195 (Western Wall Tunnels);
- HAESI-15729 (Western Wall Foundations).

**T2 volumes (noted for completeness)**

| This pass | Merged row(s) |
|---|---|
| IAAR39 Tel Moẓa | HAESI-169 (2005): spring tunnel, pools, oval rock-cutting in Area E, all coded `unknown` there; ESI15-083 (1993 season); HAESI115-055 (2003) |
| IAAR19 Abu Ghosh | ESI19-070 and HA107-099 (the 1995 season: burial pit L118) |
| IAAR69 Kathisma | ESI20-101, HA108-139, HAESI113-089 (channels in the church walls, conduit L147); HAESI-106 (2000 season: Channels 627/628, Bir Qadismu) |
| IAAR3 Manaḥat | ESI07-117 (1987–1988: ritual bath in a cave, burial in a building) |
| IAAR12 Efrata | no merged row from the 1979 excavation. ESI09-157 and HAESI-25417 are other excavations at Efrat |

## Figures to archive later (not stored)

| Volume | Figures (printed page) |
|---|---|
| IAAR39 | Fig. 2.1 topographic map with areas (p. 9); Fig. 2.49 Area F spring (p. 57); Plan 2.18 Area F plan and sections (pp. 58–59); Tables 2.3, 2.5 silo tables (pp. 15–16, 27) |
| IAAR3 | Fig. 1.1 map (p. 3); Plan 3.1 excavation areas (opening of Chapter 3); Fig. 3.4 Pit L121 (p. 16); Fig. 3.25 cupmark (p. 26) |
| IAAR19 | Fig. 1.2 location of areas (p. 2); Plan 3.1 general plan (p. 14); Plan 3.4 Burial T134 (p. 17); Fig. 3.4 floor and grave L118 (p. 19) |
| IAAR69 | Fig. 1.1 location (p. 1); Fig. 1.3 Bir Qadismu (p. 3); Plan 1.1 excavation areas (p. 7); Figs. 2.14–2.15 clay pipe to the cupmark (p. 33); Fig. 2.34 favissa (p. 48); Plan 3.4 Bir Qadismu (p. 110); Fig. 3.18 Reservoir 810 (p. 114) |
| IAAR12 | Plan 1 map (p. 3); Plan 2 topographic map (p. 5); Fig. 1 aerial view (p. 7); Plan 5 cemetery plan (p. 18); cave plans and sections (Chapters 3–4) |
| IAAR67 | Plans 1–6 (pp. xv–xx); Plan 1.1 and sections, quarries (pp. 4–6); Figs. 1.7–1.10 Quarries 8170, 9588 (pp. 11–14) |
| IAAR63 | Plan 1.1 Old City location (p. 1); Plan 2.1 Second Temple-period remains and sections (pp. 19–21); Figs. 2.1–2.7 (Cistern 6170, Miqveh 2022, Low-Level Aqueduct, quarries; pp. 18–26); Figs. 3.12–3.21 drainage channels (pp. 45–49); Figs. 3.53–3.55 Cistern 300 (p. 79) |
| IAAR52 | Figs. 1.1–1.3 location (pp. 2–3); Figs. 2.37–2.41 Stratum VII water installations (pp. 27–29); Plan 2.18 schematic plan and sections (pp. 55–61) |
| IAAR66p1 | Plan 2.30 schematic plan and sections; Figs. 2.39–2.40 Reservoir 6388 (p. 37); Figs. 2.45–2.48 gold hoard in situ (pp. 49–50) |
| IAAR66p2 | Plan 12.17 Phase IIB layout (Chapter 12); Plan 12.29 Open Square 1377 with the cistern shafts (p. 332); Figs. 12.14–12.29 pits (pp. 288–298); Figs. 12.46–12.48 Cistern 3587 (p. 317) |
| IAAR66p3 | Fig. 21.7 astragali caches (Chapter 21, near p. 750) |

## Proposed changes for the integrator

1. **Pits.** Decide whether earth-dug and built storage, refuse and sewage pits and silos count as `rockcut_installation` (choice 2). If not, drop or reclassify these rows:
   - Tel Moẓa rockcut `no`;
   - Abu Ghosh rockcut `no`;
   - Giv‘ati II part 2 rockcut `no`;
   - Giv‘ati I rockcut `no` (Stratum I pits).

   Giv‘ati I Shaft 728 (`yes`) is built, not rock-cut.
2. **Post-70 features dated up to 135 CE.** Decide whether the in-window `yes` should cover these Aelia Capitolina works:
   - IAAR67 Cardo quarrying, "first third of the second century CE";
   - IAAR63 Cardo drainage, "before 130 CE".

   If the plan's "up to 135 CE" is meant only for Bar Kokhba-era Judaean contexts, an amendment is needed. It would be exploratory.
3. **Duplicates.** Add the same-feature pairs above to the merge's dedupe pass, especially:
   - IAAR63 and IAAR67 against HAESI-1219, 1285, 18755 and 25927;
   - IAAR52 against HAESI-873;
   - IAAR66p1 against HAESI-1377.
4. **Missing chapters.** Ask the owner for the two chapter PDFs listed under Sources in `README.md`: Manaḥat Chapter 14, The Miqweh, and Efrata Appendix 1, Byzantine Winepresses. They would date the Manaḥat miqweh and describe the Efrata winepresses.
5. **Class label for one feature.** Consider one class label for the Giv‘ati reservoir, Cistern 1391, across IAAR66p1 and IAAR66p2 (choice 5).
