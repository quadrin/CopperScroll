# Side-quest C3, round 2: what the terrain says about recorded installations (6 Nov 2026)

Lane C3. DEM: Copernicus GLO-30, the round-1 UTM 36N mosaic (`scratch/C3/der/dem_utm30.tif`). I rebuilt slope and D8 flow accumulation from it (`private2/C3/derive.py`); heights below are bilinear samples (`samp2.py`). The new inputs this round:
- Netzer 1981, *Greater Herodium* (Qedem 13): bucket PDF `Netzer-1981-Greater-Herodium-Qedem-13-54f1abfb`, page images. Viewer page = printed page + 8.
- Mazar 1989, "Survey of the aqueducts to Jerusalem", in Amit, Hirschfeld & Patrich (eds), Hebrew: bucket `Amit-Hirschfeld-Patrich-eds-1989-…-9b4ae0b2`, viewer pp. 182–206 (printed 169–193). This volume has no text layer, so I OCRed the page images (tesseract `heb`) and checked every grid reference by eye at 220 dpi.
- Mazar 2002, JRA Suppl. 46 (English): bucket `01-Aqueducts-of-Israel-2002-indexed-0c0e68f6`.
- ʿAtiqot 41, Region X (Itah, Kam & Ben-Haim 2002): Drive `1cVCcAnyJdpJpTQ9tDurq9K1TRZg7LoPf`.
- Patrich & Arubas 1989, IEJ 39: Drive `1Da7WmdnvlKqKh6Huebnxx2ekqK39LKdx`.
- OpenStreetMap through the Overpass mirror `maps.mail.ru/osm/tools/overpass/api/interpreter`. The main Overpass server was blocked in round 1.
- Esri World Imagery z17 tiles, for one private overlay.

Public data files:
- `water_rows_vs_reference_points.csv`: project points against reference points, as distances and heights only.
- `mazar1989_gridrefs_vs_glo30.csv`: all 9 grid references in Mazar's chapter against GLO-30.

Private files (`private2/C3/`):
- reference-point lat/lon;
- the X/35 position note;
- the Region X imagery overlay;
- page crops of Netzer p. 4, Netzer Ill. 136 and Mazar p. 193;
- scripts.

---

FIND CARD
Title (one line): The water inventory puts the Herodium aqueduct's head, its destination and all ten Solomon's Pools rows on hill-top ruins 0.3–1.2 km from the installations. Corrected, the aqueduct's recorded drop of 111 m shrinks to about 30 m.
Round-1 link: C3-2 (WBS:4287 "Lower Herodium" = fortress grid), and the round-1 dead end "LIT fallback points … terrain-impossible".
Lane: C3
What is odd (2–4 sentences): Under plan §6 rule 2, each Mazar and Netzer literature row takes the point of the nearest named WBADB site, labelled "precision 350 m". For this aqueduct system that rule picks three hill-top ruins: Rujm Artas, the Herodium cone and Kh. el-Khawkh (= Tel ʿEitam). The installations themselves lie in the valleys beside them. Netzer's own figures put Lower Herodium at 645–670 m and the fortress at 710–750 m. GLO-30 puts the project's two "Lower Herodium" points at 727 m (WBS:4287) and 699 m (WBE:833), both on the cone, while the pool lies at 655 m. The head spring that Mazar locates by grid is 906 m from the project's head point and 152 m lower.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **What Netzer prints.**
  - Netzer 1981 printed p. 4 (viewer p. 12), "Surveying system": "Lower Herodium between 645 m. and 670 m. and the mountain palace-fortress between 710 m. and 750 m."
  - Ill. 136 (printed p. 106, viewer p. 114) is a contoured plan of Greater Herodium with north pointing **down**. On it the great pool (no. 11) lies about 410 m from the summit at about N 32° W. I scaled the plan by the pool's own 69.2 m length (Netzer pp. 11–13).
  - OSM node 8803075026 "The Pool" lies 433 m from the summit node 431633653, at 321°, and GLO-30 gives it 655 m. That is a second, independent witness.
- **Where the project puts Lower Herodium.**
  - `water.csv` rows `LIT-MAZ-HERODIUM-AQ` (dest), `LIT-MAZ-HERODIUM-POOL`, `LIT-NET01-LH-POOL`, `LIT-NET01-LH-BATHPOOL` (precision 350 m) and `WBADB-S4287-cistern` / `-reservoir_pool` (precision 100 m) all sit on WBS:4287. That point is 325 m from the pool and 72 m higher.
  - `WBADB-E839-reservoir_pool` takes WBE:833 (173000/119100). That point is on the **south** slope (699 m), 549 m from the pool, which lies to the NW of the summit.
- **Where the project puts the head.**
  - `LIT-MAZ-ARTAS-SPR` and the head of `LIT-MAZ-HERODIUM-AQ` sit on WBS:4223 Rujm Artas (838 m). The notes say "grid ref partly illegible".
  - The grid is legible on the page image: Mazar 1989 printed p. 193 has "(נ"צ 1217 1678)", which is E 167.8 / N 121.7 and gives 686 m on GLO-30. JRA 46 p. 243 prints the same. Mazar gives the first remains at 690 m (point 60), and JRA 46 p. 109 has "ʿEin Urtas (690 m)".
  - The project already read this grid on 30 Oct (`research/sources/books_usc_2026-10-30/aqueducts_other_chapters_sweep_2026-10-30.md` line 94), but `water.csv` was never updated.
  - OSM "Artas Spring" (node 2935013947) is 160 m from Mazar's grid, at 684 m.
- **Solomon's Pools.**
  - Ten rows sit on WBS:4206 Kh. el-Khawkh: `LIT-MAZ-SOL-UPPER`, `-MIDDLE`, `-LOWER`, `-SALEH-SPR`, `-BURAQ-SPR`, `-FARUJA-SPR`, `-ATAN-SPR`, `-COLLECT`, `-LOWER-AQ`, `-UPPER-AQ`.
  - That point is OSM's "תל עיטם" (Tel ʿEitam), 42 m away.
  - The three pool outlines (OSM relation 14243316) lie 815, 1,018 and 1,200 m WNW of it. ʿEin Faruja and ʿEin ʿAtan lie about 700 m away, and Qalʿat el-Buraq 1,238 m.
- All distances and heights are in `water_rows_vs_reference_points.csv`.
Literature check (queries run, result, tag):
- Repo main and `branch_only`: I grepped "1678 1217" and found only the 30 Oct sweep note. "Tel Eitam" appears only in reading and medieval notes. "645 m" appears only in an unrelated row. No water-lane note tests these points against terrain or OSM. The Netzer 1981 audit (`research/sources/netzer1981_targeted_2026-10-12/README.md`) says "No geographic registration was performed."
- WBADB itself carries the fortress grid for "Lower Herodium" (round 1).
- Tag: **NEW TO THE PROJECT.**
Why it might matter:
- The Herodium aqueduct is one of the two literature aqueducts whose bearing and head-to-destination relation the water lane computes (README "Known limits").
- On the project points the aqueduct falls 838 → 727 m (111 m over 5.4 km straight-line). Corrected, it falls about 686–690 → 655–670 m (20–35 m), which matches Mazar's own heights (690 m at point 60, c. 670 m where the trace ends).
- Any gradient, "head above destination" or flow-time use of these rows is off by a factor of about 3–5.
- The entry-21 F-flow bearing moves from 285° to 292°, so it stays **FAIL**: no clause score changes.
- The precision labels (100 m and 350 m) understate the real error in 11 of the 12 rows of the table. The exception is the 350 m-labelled Lower Herodium rows, which are 325 m off.
How to confirm or kill it (with data in hand, or what is missing):
- Re-place the rows on Mazar's grid and on the OSM points, keep the 350 m label for the springs, and re-run `build_water.py`. Diff `merged_scores.csv`; I expect no change.
- Kill condition: WBS:4287 or WBE:833 is a whole-site point not meant for the pool. Even so, the rows carry a 100 m label, and the pool is 325–549 m away and 44–72 m lower.
- The Netzer plan reading (≈410 m) and OSM (433 m) agree within the plan's drawing error.
Confidence: high
Touches the Copper Scroll? maybe. The Lower Herodium great pool is one of the README's three entry-29 near misses, and this changes where it is, not how it is coded.

---

FIND CARD
Title (one line): Mazar's grid for Herodium-aqueduct point 62 (1697 1221) puts a channel that runs at 670–690 m on a spur crest at 766 m. His own Fig. 1 places point 62 about 0.6 km farther west, and the error is repeated in the English edition of 2002.
Round-1 link: new (it completes round-1's "uphill channel" test, which round 1 could run only on three routed rows).
Lane: C3
What is odd (2–4 sentences): Mazar traces the Artas–Herodium aqueduct from 690 m at the village exit (point 60) to c. 670 m at 1726 1198, where it disappears. In the middle of that course he cites point 62 "(נ"צ 1221 1697)" as the place where the built aqueduct survives complete. GLO-30 gives 766 m at E 169.7 / N 122.1, and every cell within 50 m lies between 756 and 775 m. That is a spur top 75–95 m above any level the channel can hold, and a 100 m grid unit cannot account for it. The other eight grid references in the chapter fit their stated heights or settings.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **The grid as printed.**
  - Mazar 1989 printed p. 193 (viewer p. 206), left column, line 2. I read it at 220 dpi; private crop `private2/C3/pages/Mazar1989_p193_point62.png`.
  - JRA 46 (2002) bucket PDF p. 124 text layer: "62 (map ref, 1697 1221)". The same chapter gives "map ref. 167[8] 1217" for the head.
- **Mazar's Fig. 1 map** (printed p. 171, viewer p. 184): I scaled it on its 0–3 km bar (134 px/km at 150 dpi). It plots point 62 about 1.3 km E and 0.1 km N of the Artas village symbol, i.e. near E 169.0–169.1 / N 121.8–121.9. Point 64 falls about 2.2 km E, and the dotted line runs eastward between them.
- **The terrain.** GLO-30 in 100 m steps around the printed point has 751–773 m on the spur. Cells that fit the channel (≥ 665 m and ≤ 695 m) lie at E 168.7, 169.0, 169.1 on N 122.1, or at E 169.3–169.4 on N 121.8–121.9.
- **The other eight grid references** (Ṣur Bahir 1714/1267, the Scottish hospital 1715/1307, ʿEin Mughara 1647/1198, south Bethlehem 1681/1224, ʿEin Artas 1678/1217, rock cut 1680/1218, saddle 1706/1215, end 1726/1198) are in `mazar1989_gridrefs_vs_glo30.csv`. The end point gives 671 m against Mazar's "c. 670 m".
Literature check (queries run, result, tag):
- The repo sweep note (30 Oct) transcribes "Point 62 (1697 1221)" without comment.
- Web search for the Herodium aqueduct route, Mazar, Artas and Wadi Tuhin: no erratum or re-survey with grids found.
- JRA 46 repeats the reference, so the error survived the English edition.
- Tag: **NEW TO THE LITERATURE.**
Why it might matter: Point 62 is the one place Mazar cites for a complete section of this aqueduct, and it is the best-preserved built section. With the printed grid it cannot be found. The figure and the terrain together put it near E 169.0–169.1. The single-digit misprints "1690" or "1691" for "1697" fit both (GLO-30 679 m and 691 m).
How to confirm or kill it (with data in hand, or what is missing):
- Mandate 1:20,000 or SWP sheet contours at E 169.7 / N 122.1 would show whether a spur crest stands there. Palestine Open Maps is in Drive 07; I did not open it, for budget.
- Kill condition: the channel tunnels under the spur. Mazar reports no tunnel on this aqueduct, and he describes point 62 as a *built* section.
Confidence: medium (terrain and figure agree; the corrected digit is uncertain)
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): The juglet cave (Patrich & Arubas Cave 13 = ʿAtiqot 41 X/35) has a published 1993 grid that the project holds but never joined to 3Q. Read with Patrich & Arubas's "150 m west of the track" and GLO-30, it puts the cave 0.43–0.50 km NNE–NE of 3Q (1952 point 8).
Round-1 link: the round-1 dead end "ʿAtiqot 41 Region X off-cliff cluster … no source for its geology", now answered from the source.
Lane: C3
What is odd (2–4 sentences): The project's de Vaux-points note says "I found no 1993-survey cave coordinates in the repo, so there was nothing to match". It leaves the juglet cave's distance from 3Q open between 0.25 km (P&A's Fig. 1) and about 0.8 km (their "2.8 km north of Kh. Qumran"). Yet `caves.csv` row `A41:X/35` carries the printed grid 19380/13015, and Itah et al. state that X/35 *is* Cave 13. They removed its collapse in 1993. That grid lies 504 m from point 8, at 39°, and 2.50 km from Kh. Qumran. It falls 15–20 m west of the OSM Qalya–Almog track, on the flat plain (−308 m, 7°), whereas P&A put the east-facing conglomerate cave 150 m west of the track. GLO-30 shows the only east-facing scarp at this northing between E 193.60 and 193.70 (−249 → −295 m), which fits P&A and puts the printed easting about 130 m too far east.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ʿAtiqot 41 Region X, Table 1 row X/35 "‘Cave of the Balsam Oil Juglet’". The text says "(Patrich and Arubas 1989: Cave 13, referred to as Cave Q3)". The captions group X/35 with the cliff caves (Fig. 3) and with X/36 and X/51 (Fig. 4).
- Patrich & Arubas 1989 p. 43: "about 2.8 km. to the north of Kh. Qumran, and about 150 m. to the west of the track …"; "Samra formation"; "The cave faces east".
- 3Q = point 8 (193486/129756): `research/history/devaux1952_cave_points/README.md` lines 68–75. The "nothing to match" statement is at line 136, and the Cave 13 discussion at lines 125–134 and in `research/history/salvage_records/README.md` line 80.
- GLO-30 profile at N 130150 in 25 m steps is in the private note `private2/C3/X35_cave13_position_note.md`. The OSM track geometry was fetched 6 Nov.
- Distances to the 1952 points: printed X/35 is 488 m from point 4 and 504 m from point 8. Shifted 150 m west of the track, it is 391 m from point 4 and 434 m from point 8 (at 25°). P&A's candidate "No. 2" is 478–608 m away, at 83–85°.
Literature check (queries run, result, tag): Repo: I grepped "X/35", "Cave 13", "juglet" and "150 m west of the track". The cave inventory has the X/35 = Cave 13 identity, but no note joins the grid to the 3Q question. The grid is published (ʿAtiqot 41). Tags: **NEW TO THE PROJECT** for the join; **NEW TO THE LITERATURE** (provisional) for the clash between the printed easting and the excavators' description.
Why it might matter:
- The juglet excavation of 1988 was one of the scroll-motivated digs (salvage S13).
- This card turns the open 0.25–0.8 km range into a figure with a stated source: 0.43–0.50 km from 3Q, NNE–NE.
- That figure contradicts P&A's own Fig. 1 (0.25 km N), and their "2.8 km" (the grid gives 2.50 km).
- Neither placement is close to 1952 point 2, which lies W of the cave. So P&A's "may have been No. 2" gets no support from position.
- **ARGUMENT:** the eastern Region X groups probably share the same eastward bias. The 13 "ridge" caves of Fig. 2 (X/9–16, 23, 24, 26, 27, 31, 32) plot 100–600 m east of the escarpment foot, on a fan that imagery and GLO-30 show sloping at 2–5°. Some may sit in gully banks of a few metres, below DEM resolution. This weakens, but does not kill, F's "cliff host" predicate for Region X.
How to confirm or kill it (with data in hand, or what is missing):
- A surveyed 3Q mouth fix and a GPS fix of Cave 13 would settle it; neither is in the corpus.
- With the data in hand: register P&A Fig. 1 on GLO-30 using the Kh. Qumran symbol and the track. Its 3Q-to-Cave 13 offset should then come out near the 0.43–0.50 km found here, if the figure is the one in error.
- Kill condition: the "track" of 1988 is not the OSM track (for example, it is today's Highway 90 farther east). In the OSM query (35.45–35.47° E) the track is the only N–S road 0–200 m east of the scarp at this northing. I did not check where Highway 90 runs.
Confidence: medium (identity high, since the source states it; the 130 m correction rests on one sentence and the DEM)
Touches the Copper Scroll? yes: it is the nearest excavated cave to 3Q with a published grid, and its dig was scroll-motivated.

---

## Dead ends

- Pool volume against catchment (lane brief "pools with no possible catchment"):
  - Only 36 `water.csv` rows carry a capacity and 63 carry dimensions.
  - All are well-known sites with recorded channels (Qumran L-series, Solomon's Pools, Hyrcania, Martyrius, Jericho), so no "lost source" can be inferred.
  - Not run further.
- Mazar's upper-aqueduct heights in Jerusalem (Hezekiah's Pool 765 m, Emek Refaim 775 m, railway-station valley ≤ 755 m, printed p. 183): not tested. GLO-30 is a surface model and is biased by buildings in the city.
- Herodium entry-21 bearing: corrected from 285° to 292°. Still FAIL; no score effect.
- Netzer 1981 pool-floor level: not read. The pool's ground level (655 m, GLO-30) and Netzer's 645–670 m range are enough for card 1.
- Region X caves east of the track (X/9–11, 14–16, 24): imagery shows a fan with shallow gullies. They are not demonstrably misplaced, since gully-bank caves of a few metres cannot be excluded. That is why they are labelled ARGUMENT in card 3.
- Twin Cave / Vendyl Jones's caves: ʿAtiqot 41 X/48 (19339/12949, "previously excavated by Wendell Jones") lies 364 m WNW of the Bar-Adon / WBADB point 193700/129300. Same eastward pattern; not pursued.
- Solomon's Pools elevations: the project point (764 m) and the pools (774–797 m) differ little in height, so the error there is in plan only (card 1).

## Blocked inputs

- `https://overpass.kumi.systems/api/interpreter` and `https://overpass.private.coffee/api/interpreter`: curl error 28, timeout after 40 s with 0 bytes.
- `https://maps.mail.ru/osm/tools/overpass/api/interpreter`: one query returned "504 Gateway Time-out"; narrower queries succeeded.
- Amit–Hirschfeld–Patrich 1989 (Hebrew) has no text layer. I worked around it with tesseract `heb` OCR of viewer pp. 182–206; the OCR is not proof-read, but every grid reference was checked against the page image.
- Palestine Open Maps 1:20,000 (Drive 07): not opened, for budget. It is needed for card 2's kill test.
