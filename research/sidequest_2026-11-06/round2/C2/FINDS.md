# Side-quest C2, round 2: named features on old maps (SWP sheets XVII/XVIII/XXI edges, the Qumran–Feshkha strip, and the desert east of Bethlehem), 6 Nov 2026

Round 1 read SWP sheet XVIII north of N 124 only. Round 2 does three things.
- It extends the map–record join south and west: SWP sheet XVIII south of N 124 (Mar Saba, Kidron, the shore down to ʿEin et-Turaba), and the eastern edges of sheets XVII and XXI (E 172–180, N 119–129).
- It tests how well the georeferenced SWP layer is registered across the region. Round 1 assumed about 100 m everywhere.
- It runs the kill tests that round 1 left open on card C2-3 (Thomsen 1917 and the TIR roads).

The orchestrator is handling Mughâret Ekteif, so this round skips it. The one exception is the registration figure near it (card 2), because the orchestrator can use that.

Record index used here: `/home/claude/swarm/private2/C2/scripts/records.py`. It joins:
- WBADB (6,950 rows), with B2b's correction applied to WBS:1910 and WBS:2931;
- the full IAA ASI online dump that lane D2 fetched (`scratch/D2/asi/`, 8,941 points in the region). Round 1 used it only through `water.csv`/`caves.csv`;
- `water.csv`, `caves.csv`, `tombs.csv`, the HA/ESI `sites.csv` and the Mandate `features.csv`.

Public data in this folder (none of the files gives coordinates of unrecorded features):
- `swp18_features_vs_records_corrected.csv`: round 1's 23 picks, re-joined (see "Corrections to round 1").
- `talpiyot_hole_swp_features.csv`: 62 SWP-named point features in the Map 106 block, each with its class and the distance to its nearest record. It has no positions.
- `swp_pom_registration_checks.csv`: 16 control readings (recorded sites only).
- `swp_shoreline_vs_glo30_m394.csv`: the SWP shoreline against the −394 m contour of GLO-30, every 250 m of northing.

Private: `/home/claude/swarm/private2/C2/`. It holds the feature positions (`hole_features_PRIVATE.csv`), the overlay views `v_*.png` (SWP z15, all record layers drawn), the control contact sheets, the SWP/1940s pairs, the TIR crops and the scripts.

---

FIND CARD
Title (one line): The desert half of ASI Map 106 (Talpiyot) is a published-record hole. Hirschfeld surveyed the whole sheet in 1981–84 and recorded 115 sites, but only the Jerusalem municipal strip was published site by site. In the hole, 54 of the 62 point features that the SWP names (caves, ruins, a vaulted reservoir, cisterns) have no record within 500 m.
Lane: C2
Round-1 link: new (it extends C2-2 to a new area and explains the gap it found)
What is odd (2–4 sentences):
- The project's record layers (WBADB, the ASI online dump, water, caves, tombs, HA/ESI) are dense on every side of a block of about 70 km²: Jerusalem (Map 102) to the north, Mar Saba (109/7, east of E 180) to the east, Herodium (108/2, south of N 120) to the south.
- Inside the block they are almost empty. All 144 ASI online sites of Map 106 lie at E 170–175, and the HA reports with map references in the block (2004–2025) all lie west of E 175. East of E 175, between N 120 and N 129, WBADB holds 7 rows.
- The SWP draws 62 named point features in the block, over E 173–180 / N 119.9–128.9 (all of the empty part except its westernmost km, E 172–173). The median distance from a feature to the nearest record is 1.28 km. Only 8 lie within 500 m, and 42 are more than 1 km away. For comparison, 14 of round 1's 23 sheet XVIII picks lie within 500 m.
- The cause is in print. ESI 3 (1984) says Hirschfeld surveyed the whole Talpiot sheet (E 170–180 / N 120–130) for the ASI and recorded 115 sites: 12 Bronze Age cairns, 17 Iron Age sites, 11 Second Temple sites, 40 Byzantine sites (12 monastic), 20 winepresses and 15 undated sites. The Map 106 volume (Kloner, *Survey of Jerusalem: The Southern Sector*) says Hirschfeld "surveyed the area of the Map of Talpiyot, part of it included within the municipal boundaries", and it publishes only the municipal part.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ESI 2 (1983) pp. 58–59 and ESI 3 (1984) pp. 62–63, "Judean Desert, Survey (Map 106)": bucket docs `ESI-02-1983-…-427304df` page index 65–66 and `ESI-03-1984-…-5e17a652` pages 69–70.
- Kloner's online introduction to Map 106: `survey.iaa.org.il/aspxService/Service_Eng.aspx/GetMapIntro?mapId=53`, fetched 6 Nov 2026. It contains the sentence about Hirschfeld and the municipal boundary.
- Sheet extents and site spreads come from `scratch/D2/asi/GetPolygonsSites_Eng__MapId-53.json` and `research/regional/asi_jerusalem/maps_used.csv`.
- The 1-km record-density grid was computed inline from `records.py` (count of all layers except the Mandate layer per 1-km PG square, E 170–194 / N 110–144). The block shows as empty cells.
- The 62 SWP features: `talpiyot_hole_swp_features.csv`. Among them:
  - Kh. el-Makhrûm with "Caves". The Memoirs III entry (Sheet XVII, Nu) reads "Foundations, caves, and cisterns, apparently Byzantine work".
  - Mughâret Dâûd.
  - Kh. Jokhdhum (Memoirs XVII Nu).
  - Kabr Ghunnâm.
  - Kh. el-Haradân (Memoirs XVII Nu).
  - Mughâir er-Retaghbîr and two other unnamed "Cave(s)" labels.
  - "Bkt. el Jûba (Caves)" (Memoirs XVII Nu: a vaulted tank 104 × 53 ft and 29 ft deep, with vaults outside it). It lies 427 m from the Theodosius row WBS:4098 and has no record of its own.
  - Sheikh Saʿd "Caves".
  - Kh. er-Rilkah? "Caves".
  - 45 named or unnamed cisterns ("Bir", "B.").
- WBADB carries only three of Hirschfeld's Map 106 sites, all named in the ESI notes: WBS:3781 (the Iron Age fort, map ref. 1791/1291), WBS:3962 (Kh. Jinjas laura, 1797/1268) and WBS:4116 (el-Burj, 1795/1249). The project's HA/ESI layer codes the same ESI notes (`haesi_features/phase2_2026-10-10/reports.csv`, ids ESI02-058, ESI03-062).
- Positions are in `private2/C2/hole_features_PRIVATE.csv`, and the views are `v_173_119.png`, `v_173_124.png` and `v_178_124.png`.
- Registration here is good. Herodium reads at 15 m, Kh. el-Muntar at 100 m and the Theodosius area agrees (card 2). So the distances are not a registration artefact.
Literature check (queries run, result, tag):
- Corpus: `hexview pdf-search "Map 106"` gives the two ESI notes and nothing else. Repo grep for "Map 106", "Talpiot map", "115 sites" and "one hundred fifteen" finds only the ESI notes coded as features. `asi_jerusalem/maps_used.csv` and `coverage_statements.csv` call Map 106 "comprehensive (no explicit full-area statement)", which is the Kloner wording for the municipal survey.
- Web: "archaeological survey Talpiyot map 106 Hirschfeld … unpublished". It finds only the HUJI bibliography entry for ESI 2 (https://dig.corps-cmhl.huji.ac.il/biblio/judean-desert-survey-map-map-106). No final publication of the desert part turned up.
- Name grep of all record layers for Makhr, Jokh, Ghunn, Daʾud, Dhahir, Ikhdash, Hanjal, Kukwedh, Keiakb, Ameiy, Haradan and Retaghbir: no hits.
- Tag: **NEW TO THE PROJECT**. That Hirschfeld's survey exists and its desert part is unpublished is known to specialists (the ESI notes, Kloner's preface). That the project treats the sheet as "comprehensive", the size of the hole, and the SWP feature list are not in any project file.
Why it might matter:
- Every "no record here" result, density or denominator built from WBADB/ASI (caves, tombs, water installations, Koḥlit rarity, the 1 km landscape map) counts this block as empty when it is merely unpublished.
- The block holds the middle Kidron (Wadi en-Nar) between Deir Ibn ʿObeid/Theodosius and the Mar Saba gorge.
- ARGUMENT (Copper Scroll): the project's place `mar_saba` ("Kidron gorge at Deir Mar Saba", tied to entry 35, medium) lies about 1–2 km east of the hole. Several candidates are described as running "downstream of Bir Ayyub" along the Kidron (`phase3_places.csv`, `jer_bir_ayyub`). For any entry whose reading follows the Kidron below Jerusalem, a missing feature on the stretch from about E 175 to E 180 is uninformative, not negative. This weakens no candidate and strengthens none. It removes a silent negative from any test that used the layers over this stretch.
How to confirm or kill it (with data in hand, or what is missing):
- Confirmed with data in hand: the ESI notes, Kloner's intro, and the empty grid cells.
- To kill it, find a site-level publication of Hirschfeld's desert sites. Candidates: an ASI volume or online map for the eastern 106 sheet, Hirschfeld's 1990s Judean Desert monasteries gazetteer (12 monastic sites), or the archive files of the Staff Officer for Archaeology. Only the monastery subset is likely to be in Hirschfeld's monastery books, and they are not in the corpus.
- The 1940s 1:20,000 sheet 17-12 could add a second witness for each SWP feature (not done here).
Confidence: high (that the hole and its cause exist); medium (each feature's label-anchor position, ±250 m)
Touches the Copper Scroll? maybe. It turns the project's silence along the middle Kidron into "not published", which matters for Kidron-following readings (entries tied to `jer_bir_ayyub` and `mar_saba`).

---

FIND CARD
Title (one line): The georeferenced SWP sheet (Palestine Open Maps `pal63k-1880`) is accurate to 0–160 m from Herodium to Jericho and Nebi Musa, but it is displaced 0.3–0.8 km west and north along the Qumran–ʿAin Feshkha strip. There the SWP cliff, springs and Kh. Qumran plot inland of their true places, and dry-land sites plot in the 1880 sea.
Lane: C2
Round-1 link: C2-1 / C2-2 (they assumed a uniform ~100 m registration; R4 asked for a re-pick)
What is odd (2–4 sentences):
- Recorded sites were read on SWP crops centred on their true positions (16 controls) and on SWP | 1940s pairs.
- Inland and on the Jericho plain the SWP symbol lands within 160 m of the truth: Herodium 15 m, Rujm el-Bahr under 30 m, Kh. el-Muntar 100 m, Hyrcania 130 m, Deir Hajla 150 m, Nebi Musa shrine 160 m, Maqam er-Raʿi 120 m.
- Between Kh. Qumran and Ras Feshkha it does not:
  - Kh. Qumran's ruin circle lies 375 m WNW of WBE:748;
  - the ʿAin et-Tannur and ʿAin Feshkha labels lie 400 m and about 800 m W–NW of the 1940s springs;
  - the foot of the Jurat el-Beid cliff at N 126 is drawn 500 m west of the 1940s cliff;
  - the WBADB point for the ʿAin Feshkha building, and the Qasr el-Yahud fortress at Wadi Mazin, both plot in the SWP's 1880 sea.
- ʿAin et-Turabe is 330 m off. The published accuracy of the SWP is an RMSE of 74.4 m on triangulation points (Levin et al., ICC 2015).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `swp_pom_registration_checks.csv` lists each control, its reference source, the offset read and the crop it was read from.
- Crops: `private2/C2/controls_swp.png`, `controls2_swp.png` (1.6 km windows with 250 m and 500 m rings), `pair_qumran.png` and `pair_nebimusa.png` (SWP z15 | 1940s z16, 500 m grid), and `m_188_119.png` / `v_188_119.png` (1940s and SWP at E 188–193 / N 119–124).
- The shoreline profile is in `swp_shoreline_vs_glo30_m394.csv`. The SWP sea edge is found by colour and compared with the GLO-30 −394 m contour (the sheet prints the 1870s level as −1,292 ft). They agree within about ±400 m on most of the coast. The −0.9 to −1.0 km gaps sit at the Kidron mouth (N 119.5–120.5) and at N 128.5, where fan-delta growth since 1875 can explain them. The profile therefore does not prove a drawing error. The point controls carry the result.
Literature check (queries run, result, tag):
- Web: "Survey of Western Palestine map accuracy Dead Sea western shore Feshkha positional error georeferenced". It found Levin et al., "Assessing the accuracy of historical maps – the Survey of Western Palestine as a case study" (ICC 2015; https://icaci.org/files/documents/ICC_proceedings/ICC2015/papers/19/195.html): RMSE 74.4 m, with no regional pattern reported in the abstract.
- Repo: `research/regional/mandate_maps/swp_comparison.csv` compares label points 277–602 m apart in the Jericho area only. It reports no control-point registration.
- Tag: **NEW TO THE LITERATURE** (provisional) for the local 0.3–0.8 km displacement on the Qumran–Feshkha strip. I could not tell whether it comes from the 1873–74 drawing or from POM's rubber-sheeting.
Why it might matter:
- Any "no record within X m" test, or any reading of an SWP label as a position, is unsafe on this strip below about 800 m. That covers the Feshkha springs, the Qumran plateau cliff and the Ras Feshkha–Kidron shore.
- Round 1's seven SWP-only features are all in the zone of good registration: Wadi Qelt, Nebi Musa and the Jericho plain, each within about 2 km of a ≤160 m control. Their verdicts stand.
- For the orchestrator's Ekteif work: the nearest controls (the Nebi Musa shrine 1.4 km SW, 160 m; Maqam er-Raʿi, 120 m) suggest a local error of about 150 m. That is smaller than the ±250–300 m used.
How to confirm or kill it (with data in hand, or what is missing):
- Re-read the strip controls on the native SWP sheet scan (Drive 07 `SWP 1-63360 (1880)`) against its printed graticule. If the native sheet agrees with the truth, POM's georeference is at fault. If it shows the same offsets, the 1870s drawing is.
- Add 5–10 more controls on the strip (ʿAin el-Ghuweir, Kh. Mazin, the Qumran aqueduct) from the 1940s sheet.
- It dies if a re-read of the symbol, not the label, at ʿAin Feshkha and ʿAin et-Tannur gives offsets below 200 m.
Confidence: medium (Qumran, the cliff and Qasr el-Yahud are read on symbols or lines; Feshkha and Tannur are label anchors)
Touches the Copper Scroll? maybe. The Qumran–Feshkha strip is where several Secacah/Qumran readings sit; positions taken from SWP labels there carry an error of up to about 0.8 km.

---

FIND CARD
Title (one line): Round 1's C2-3 kill test, run. Thomsen 1917 already lists the "Dabbus el-ʿAbd" Roman milestone (no. 379, inscription unknown, from SWP only), and it treats both of the SWP roads that Itiner-e omits: the Bethel–Jericho road it calls doubtful, the Buqeia road probably Byzantine. TIR (Roll's roads) also omits the Buqeia road.
Lane: C2
Round-1 link: C2-3 (Itiner-e omits two SWP roads; the Dabbus milestone is in no dataset)
What is odd (2–4 sentences):
- Round 1 named Thomsen 1917 as the kill test and did not run it. Thomsen, *Die römischen Meilensteine der Provinzen Syria, Arabia und Palaestina*, catalogues no. 379: "Etwa 2½ km östlich von talʿat ed-damm ein Mst (genannt dabbus el-ʿabd), Inschrift unbekannt. PEF Mem. III S. 188, vgl. englische Karte Sheet XVIII".
- Under road XXXV he writes that the link between Beitin and Jericho "über ras et-tawil und durch das wadi abu retmeh" is "zweifelhaft als Römerstraße".
- Under road XL he reports the claim (PEF Mem. III p. 58) that the road by Bir Umm el-Fus to the Buqeia is Roman. He judges it "wohl erst byzantinische Anlage" and notes "Mst fehlen".
- So the milestone is catalogued (with no position and no reading), and both road questions were already raised in 1917. Only the Itiner-e omission is new.
- The TIR North sheet (Roll's roads, 1993) also draws no road through the Buqeia or past Hyrcania (`tir-north-qumran-jericho.png`). So Itiner-e follows TIR here.
- The 1940s 1:20,000 sheet prints five purple "(Stone)" labels along the modern road near Talʿat ed-Damm. None lies within 480 m of the SWP "R.M.S." The nearest are 480 m and 670 m away, against a local registration of about 150 m. So the 1940s map gives no second witness that the column was still standing.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Thomsen 1917 full text: `https://archive.org/download/bub_gb_xbdOAAAAMAAJ/bub_gb_xbdOAAAAMAAJ_djvu.txt` (local copy `scratch/C2r2/dl_thomsen/thomsen.txt`): no. 379 at lines 5047–5049, road XL at lines 4994–5058, road XXXV at lines 4803–4816.
- TIR: repo `research/assets/plans/tir-michigan/north/tir-north-qumran-jericho.png` (rotated 90°; private upright copy `private2/C2/tir_qj.png`).
- 1940s "(Stone)" labels: `private2/C2/pair_dabbus.png`. The R.M.S. position stays private (round 1).
Literature check (queries run, result, tag):
- Web: "Dabbus el-Abd" milestone, no relevant hit. "Roman milestones Jerusalem Jericho road Talat ed-Damm … Thomsen 1917", no later catalogue entry with coordinates.
- Repo grep "thomsen": it is cited only in the TIR gazetteer follow-up and in survey readings, never no. 379.
- Tag: **KNOWN BUT UNDER-DISCUSSED** (unchanged). The milestone half of C2-3 must be restated: it is in Thomsen 1917 but in no digital dataset (Itiner-e, WBADB, ASI). The roads are discussed in 1917, and only the Itiner-e and TIR omission is current.
Why it might matter: route and road-proximity tests built on Itiner-e or TIR inherit the same gap. The gap is a choice (the roads were judged not Roman), not an oversight. Any use of the Buqeia road in a scroll route model has to be argued as a Byzantine or older track, not as a Roman road.
How to confirm or kill it (with data in hand, or what is missing): read the later milestone corpora (Roll's Israel Milestone Committee lists; Fischer, Isaac & Roll 1996 covers only Jaffa–Jerusalem) for a Talʿat ed-Damm stone with a reading. Neither is in the corpus. On the 1940s question, the 1940s RAF aerials layer at POM could show the column. Not done.
Confidence: high (the Thomsen entries and the TIR omission)
Touches the Copper Scroll? maybe (only through route models).

---

## Corrections to round 1 (C2)

- **ʿAtiqot 41 points (B2b card 3).** After WBS:1910 and WBS:2931 are put back at their ʿAtiqot grids (19114/14071 and 19386/13064), no distance in the round-1 table depends on them. The false "1174 m WBADB:WBS:2931" third-nearest record of Mekûr es-Sidri is gone; its nearest record stays at 614 m (WBS:3091).
- **Adding the full ASI online dump** changes these nearest distances:
  - Rujm Haleiseh: 880 → 549 m (ASI 109/4/94, a road with retaining walls);
  - Nuseib en-Nuwârah: 1,277 → 933 m;
  - Joreif Ghuzal cave: 525 → 381 m (ASI 109/5/88, a monastic cell, which supports round 1's dead-end identification);
  - R.M.S. Dabbus: 465 → 409 m.
- **All seven round-1 features are still more than 500 m from any record.** The table is `swp18_features_vs_records_corrected.csv`.
- **Registration.** Round 1's 500 m threshold holds for all seven (card 2). Do not reuse it on the Qumran–Feshkha strip.
- **C2-3.** The milestone is in Thomsen 1917, no. 379 (card 3).

## Dead ends
- Shoreline test (SWP sea edge against the GLO-30 −394 m contour, 96–131.5 km N): they agree within about ±400 m. The two 1 km gaps sit at wadi mouths, so fan growth and drawing error cannot be told apart. The profile was kept as data and not used as a card.
- South of Mar Saba (E 178–193, N 109–119; views `v_178_114`, `v_183_114`, `v_188_119`): few SWP labels. The shore cliffs are dense with Dahari and Tal & Oron (ʿAtiqot 41) points, which GLO-30 puts at −100 to −385 m, on the cliffs and not in the sea. Unrecorded SWP items there are mostly cisterns. There are three cave labels (Mughâir Abu Zeid, Mughâir el-Mu…, "Caves" in Wadi Jorfân) with nearest records at 400–790 m: too weak for a card. Five views (`v_173_109`, `v_173_114`, `v_178_109`, `v_183_109`, `v_188_109`) were made but not read.
- The WBADB/ʿAtiqot Region XIII points that plot "in the 1880 sea" on the SWP are a registration effect (card 2), not grid errors: GLO-30 heights of −100 to −330 m put them on the cliff.
- Mughâret el-Jai: Memoirs III pp. 137–138 itself says the label is "written rather too far west". The cave is recorded (WBS:2562, a monastic complex). The label position was not checked.
- Memoirs III Sheet XXII Section B has only 4 entries (around ʿEin Gedi). The desert south of Mar Saba has almost no Memoirs descriptions, so its SWP names are map-only.
- 1940s "(Stone)" labels near Talʿat ed-Damm: not at the R.M.S. (card 3).
- Fitting a square grid to the Memoirs letter squares (by name-matching) gave columns about 10 km wide. Name matching alone is too noisy to place entries. Not used.

## Blocked inputs
- Thomsen 1917 is not in the corpus; I used the archive.org text, which is OCR with errors (for example "dabbus el-ahä^^" for el-ʿabd). The ZDPV volume search on archive.org returned nothing.
- Hirschfeld's site-level records for the eastern Map 106 are not in the corpus, ASI online or WBADB (card 1).
- Roll's later milestone lists are not in the corpus. Search: `hexview pdf-search` "Dabbus", no hit (round 1).
- TIR: only the repository crops were read. The native North sheet (`north/restore_native.py`, 23 parts) was not rebuilt, so the Wadi Abu Retmeh stretch north of Jericho was not checked on TIR.

## Seed / reproducibility
- Scripts are in `/home/claude/swarm/private2/C2/scripts/`:
  - `records.py`: the record index, including the B2b fix and the ASI dump;
  - `redo_r1.py`: re-joins the round-1 table;
  - `ov2.py` / `batch.py`: SWP views with all layers drawn;
  - `contact2.py`: control crops;
  - `pair.py`: SWP | 1940s pairs;
  - `shore.py`: the shoreline profile;
  - `parse_memoirs.py` / `fitgrid.py`: Memoirs III Section B parser (638 entries, sheets XVII, XVIII, XXI, XXII).
- `ov2.py`, `contact2.py`, `pair.py`, `shore.py`, `redo_r1.py` and `fitgrid.py` import from the round-1 scripts, which they expect at `/home/claude/swarm/scratch/C2/scripts/`. They have not been copied to `private2`, so rerunning these tools needs both folders.
- Pixel to PG for the 5 km views: E = E0 + x/304.4 km, N = N1 − y/306.6 km.
- Tiles fetched 6 Nov 2026 from palopenmaps.org.
