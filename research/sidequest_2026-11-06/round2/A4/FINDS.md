# Side-quest A4, round 2: the Holy Sepulchre underground 3D model (6 Nov 2026)

**Input:** `GrabeskircheUntergrund.glb` (bucket `models/grabeskirche-untergrund/`, 517,017,896 B, the same object as in round 1). The model is by Holger Siegel, University of Wuppertal, DOI 10.57899/bkf2-pv55, licence CC BY-NC-SA 4.0; the source-plan textures are excluded from reuse. The repository record is unchanged since 2026-06-01 (`lastModified`), with no new version. **No texture was extracted or viewed.** All model numbers below come from the bedrock mesh (node 12, 5,966,136 vertices, world transform as in round 1) or from the plane positions in the glTF JSON. Data derived from the mesh are CC BY-NC-SA 4.0 (attribution: Siegel 2026, DOI above).

**Historical witnesses used (all public domain, Internet Archive full text plus one page image):** Schick, "The site of the Church of the Holy Sepulchre at Jerusalem", *PEF Quarterly Statement* 1898 pp. 145–155 (item `palestine-exploration-quarterly_1898`); Schick, "Recent discoveries in Jerusalem", *QS* July 1889 pp. 111–113 (`…_1889-07`); Conder's rock-level table and text, *QS* April 1880 (`…_1880-04`); Warren & Conder, *SWP Jerusalem* (1884) pp. 274–275, 282 and 288 (`surveyofwesternp00warruoft`; p. 282 checked on the page image); Warren, *Recovery of Jerusalem* (1871) p. 209 (`recoveryofjerusa00wilsuoft`). The Mandate check uses Albright 1:2,000 sheet VI-F (Drive 07, `25-27-6-F.pdf`, file `1iT8Ji5U4cCU_j8pbJtPUyt7w1aIHOIHx`, SHA-256 `676b8402…d131`), read for spot heights only. No image is reproduced.

**Data files here:** `datum_witnesses.csv` (13 rows: printed level, the matching model value, the difference and how well the location is known); `cistern_depth_order.csv` (Schick's cisterns X/Y/Z against the model cavities). Private: `/home/claude/swarm/private2/A4/` holds three mesh-only contour renders with the source-plane footprints outlined (no textures).

---

FIND CARD
Title (one line): The model's "metres above sea level" are Schick's 1898 feet. The root datum is his printed "datum line … 2,420 feet", and three of his printed cistern levels reproduce to within 0.5 m. The PEF/Ordnance Survey levels put the church floor 2.4 m higher (2,480 ft), and the 1927 Mandate 1:2,000 street level at the parvis entrance is 1.2 m above the model floor.
Lane: A4
Round-1 link: A4-2 (its kill test "get one published m-asl level and test the 753.53 m datum" is now run), plus the open "154" point of A4-1.
What is odd (2–4 sentences): Round 1 found the root node `---NULL_8.2°_2420ft_73761.6cm_üMM---` but could not say where 2,420 ft came from. Schick's 1898 notes to his plans and sections say "the datum line being taken at 2,420 feet above the Mediterranean". The mesh honours his other absolute numbers: his deepest cistern X ("2,408 feet") is the mesh's global minimum at 734.49 m (2,409.7 ft), and his cisterns "under the church and behind the belfry" that "come down to the level of 2,444 feet" bottom out at 744.55–745.93 m (2,442.7–2,447.3 ft). The PEF's own levels on the Ordnance Survey datum disagree at the church. They give the Calvary chapel floor as 2,494 ft ("Checked 1882"), the rock at Calvary as 2,495 ft and "15 feet above the floor of the church", and so a floor of 2,480 ft (755.9 m). Schick's own "flooring of Calvary … 14 feet higher than the general flooring" gives the same 2,480 ft. The model puts the church floor (the Corbo/G&T plan planes) at 753.53 m (2,472.2 ft) and the Calvary summit at 758.31 m (2,487.9 ft). So the floor is 2.37 m low and the summit 2.17 m low, while the Calvary height above the floor (4.78 m, 15.7 ft) agrees with the PEF figure.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **Schick 1898:**
  - QS 1898 p. 153: the datum sentence; X, Y, Z and the 2,444 ft level are on pp. 153–154.
  - p. 145: Calvary flooring 14 ft above the church floor.
- **PEF/OS levels:**
  - SWP Jerusalem p. 282, nos. 187–192: Tomb of Nicodemus 2485 (C); above the Chapel of Adam 2495 (C), with the note "Floor of the Calvary Chapel, 2494. Checked 1882"; north of the Latin Chapel 2479 (C); NW corner of the south courtyard 2473, 7 ft below surface (S); in front of the Convent of Abraham 2458, 18 ft (S); west door 2495, 8 ft (S), "Top of ridge".
  - SWP p. 288, for the floor arithmetic.
  - p. 275: the S rows are Schick's 1873 observations, "relied on within 2 or 3 feet".
  - QS 1880: the same table, with Calvary still 2490 and "about 10 feet above the floor".
- **Model:** summit at model (−71.8, −25.2). The X void is at (83.2, −88.2); the 2,444 ft group is round-1 `mesh_enclosed_voids.csv` rows near Corbo pl. 17, 46, 52, 60 and 64 and G&T fig. 41. All values are in `datum_witnesses.csv`.
- **Mandate check (Albright VI-F, 1927):**
  - Haram raised platform 742.8, 742.2 and 741.9 m; lower court 737.9, 736.7 and 736.4 m.
  - The OS gives the floor of the Dome of the Rock at 2,435 ft (742.2 m; the rock "rises 5 feet above the floor", crest 2,440, SWP pp. 114–115) and the "general level of the Sanctuary" at 2,420 ft (737.6 m; SWP pp. 176–177).
  - So the OS and Mandate datums agree to about 0.3–0.6 m.
  - At the church, the Mandate sheet's only nearby spot heights are 754.7 m on the street at the south-east entry to the parvis and 757.1 m at the north-east corner block.
Literature check (queries run, result, tag): repo main and `branch_only` grep for "datum line", "2,495", "2,494", "2,408", "Helena's Cistern", "PEQ 1898" and "754.7". The hits are unrelated numbers in HA, atlas and benchmark files. No project note reads Schick 1898 or the SWP church rows. Web: "Schick 1898 'datum line' 2,420 feet Holy Sepulchre rock levels Conder Calvary 2,495" returns only the model's repository page and unrelated PEF items. Nothing has been published on the model. Tag: **NEW TO THE LITERATURE** for the model–source comparison. Schick's and Conder's numbers are themselves published, so that part is **KNOWN BUT UNDER-DISCUSSED**: no publication found sets Schick's 1898 church levels against the OS levels.
Why it might matter: anyone who reads the model's elevations as modern metres is reading Schick's level system. It reproduces Schick's printed cistern levels, but at the church core it sits 1.2–2.4 m below two independent level systems (OS 1864–82 and Mandate 1927) that agree with each other on the Haram. Where the error lies (Schick's 1898 sections, or how the modeller placed Corbo's ±0.00 at +15.914 m above the datum line) cannot be told without the section sheets. Either way, the model's absolute levels carry about ±2 m of uncertainty. Its relative levels (Calvary height, cistern order) hold up. Side point (extends A4-1): R5 found an Open Jerusalem item "Notes to the Plan and Sections of the ground of the Church of the Holy Sepulchre (Part II), [1898]". Its title matches part II of the QS 1898 article, whose datum sentence the model follows. So PEF/SCHICK/154 is probably that text, which would explain why no plane carries it. Not proven: no PEF number was found online.
How to confirm or kill it (with data in hand, or what is missing): (1) Read the church-floor level that Schick prints on his own 1898 section plates. The QS 1898 plates "Sections shewing rock levels" are in the public-domain scan (`palestine-exploration-quarterly_1898`, plates facing pp. 148 and 152; the OCR is unreadable). If they show the floor at about 52 ft above the datum line, the 2.4 m gap is between Schick and the OS, not the modeller's. If they show about 60 ft, the modeller misplaced the plan planes. (2) Find a modern m-asl level for the parvis or the Calvary chapel, for example in the Survey of Israel 1:1,250 Old City sheets or the NTUA Aedicule survey. Kill it if Schick's plates and a modern level both put the church floor near 753.5 m. In that case the OS's 2,480 ft is the outlier. The Mandate street level of 754.7 m beside a parvis that is entered by steps would allow that.
Confidence: high (the datum's provenance and the three Schick matches); medium (the 1.2–2.4 m conflict, which rests on PEF values that are well located and Mandate spot heights 5–10 m off the floor).
Touches the Copper Scroll? no. The model's value as a set of Jerusalem cistern levels (round-1 note) now carries a ±2 m absolute caveat.

---

FIND CARD
Title (one line): Round-1 "void 3" is Schick's "St. Helena's Cistern, Z". The model reproduces Schick's whole 1898 cistern depth order (X deepest at 2,408 ft, then Y and Z, then the cisterns under the church at 2,444 ft), and it models his rock-hewn Z as roofed rock and his masonry-vaulted Y as an open pit.
Lane: A4
Round-1 link: A4-3 (R5 weakened it: a Schick 203 section crosses void 3, and the cameras `GreatCistern.*` exist; the cavity's identity and its source were left open).
What is odd (2–4 sentences): Schick 1898 ranks the cisterns by depth. X, in the east, goes "down to the deepest level of all", 2,408 ft. Next come "the newly restored large Cistern of the Greeks, Y, and the one called St. Helena's Cistern, Z (one north and one south of the ancient Basilica)". Those "under the church and behind the belfry come down to the level of 2,444 feet". The mesh's four deepest cavity groups fall in exactly that order and place:
- X is an enclosed void east of Khan ez-Zeit, floor 734.49 m = 2,409.7 ft.
- Y is an open pit south of the basilica by Abraham's convent, floor 737.30 m = 2,419.0 ft.
- Z is round-1 void 3, north of the basilica, floor 740.21 m = 2,428.5 ft.
- The group under the church has floors of 2,442.7–2,447.3 ft.
Schick 1889 also says Z is "in the greater part hewn in the rock", and that Y is vaulted on 18 piers with walls probably of masonry ("possibly a portion may be scarped rock, but I doubt it"). The mesh matches: rock lies over Z (rock top 756.8 m above a 740.2 m floor), but Y has no rock roof (rock surface = floor, 737.3 m).
Evidence (exact sources: file path / page / figure / frame / coordinates): QS 1898 pp. 153–154. QS July 1889 pp. 111–112: Y is 102 ft E–W × 34 ft 6 in, 34 ft deep at the west and 50 ft 6 in at the east below the new shop floor, with the bottom falling east. QS 1889 p. 112: the Bordeaux Pilgrim's two cisterns, "the south one … the large cistern … the north one that of 'Helena', so called, under the Coptic Convent". Model: `cistern_depth_order.csv`. Cavity search: vertices with min-elevation < 741.5 m on a 0.5 m grid, labelled components. Round-1 `mesh_enclosed_voids.csv` row 3 (void 3: ceiling plan 18.0 × 12.4 m, ceiling about 752.6 m, floor 740.2–740.6 m).
Literature check (queries run, result, tag): repo and `branch_only` grep for "Helena's Cistern", "St. Helena's Cistern" and "2,408": no hits. Round 1's web searches for the dimensions of the Coptic "cistern of St Helena" found no measurements. Archive.org full texts of Warren 1876, Wilson & Warren 1871, SWP Jerusalem 1884 and C. W. Wilson 1906 have no dimensions for the Coptic cistern either. Tag: **NEW TO THE PROJECT** (the identification and the order test). The model–Schick agreement is **NEW TO THE LITERATURE** only because nothing has been published on the model.
Why it might matter: this closes A4-3. Void 3 is neither undocumented nor an artefact; it is Schick's Z, modelled to his depth ranking. It also gives a quantitative test of how faithfully the modeller followed Schick in three dimensions. That agreement makes the absolute-level conflict in card 1 more likely to come from Schick's level system than from careless modelling. Y is modelled as part of a broad open low area east of Abraham's convent, not as a 31 × 10.5 m box. That fits Schick's statement that the ground between Y and the Russian cistern "is nothing else but débris and earth", but it means the model cannot be used to measure Y.
How to confirm or kill it (with data in hand, or what is missing): (1) If the shop floor over Y is about 2,470 ft (Schick's Russian pavement level, QS 1888 Jan., "about 2,470 feet"), then Y's east-end bottom at 50 ft 6 in down is 2,419.5 ft. That matches the model's 2,419.0 ft, but the shop-floor level is not printed, so this is only consistent. (2) Read Z's plan and level on the QS 1898 section plates (lines I–J and K–L pass the Coptic convent; the OCR shows "COPTIC CONVENT" and "CISTERN" on the plate facing p. 152). Kill the identification if those plates put St Helena's cistern elsewhere than north of the basilica's east end.
Confidence: high (the order and the rock/masonry match); medium (that void 3 = Z rather than another Coptic cistern next to it).
Touches the Copper Scroll? no.

---

## Dead ends
- Sapienza/Custodia excavation reports (June 2023, July 2023, Aug 2024, Custodia website): no depth or level figures, so no test of the model's Rotunda rock (model: rock at about 753.3 m, roughly flush with the floor).
- Web search for a modern m-asl level of the Calvary chapel or the church floor: nothing usable.
- Measuring Schick's Y (102 × 34.5 ft) in the mesh: the pit merges into a 1,300–2,100 m² low area at any threshold above 738.2 m; only an 8 × 7 m sump below 738.2 m is separable.
- PEF rock rows 187, 189, 190, 191 and 192 against the mesh: the locations are known only to about 10 m and the ground is steep. Belfry (no. 190): model about 2,469 ft vs 2,473 ft. Abraham (no. 191): model about 2,451 ft vs 2,458 ft. These are recorded in the CSV but not used as evidence.
- Dimensions of the Coptic St Helena cistern in Warren 1876, Recovery 1871, SWP Jerusalem 1884 and Wilson 1906: none given.
- "PEF/SCHICK/154" web search: no catalogue entry that gives the number.
- Repository: no new version of the model (lastModified 2026-06-01).

## Blocked inputs
- `gs://copper-scroll-cog-1030/reading/iaa_mandate/2026-11-02/IAA_19623_ATQ_199a_Holy_Sepulchre_Nativity_survey_correspondence_native_638_scans.pdf` (145,432,675 B, 638 scans, no text layer): not opened. It is over the store's whole-object download rule, and it is in lane but would need OCR of hundreds of pages. It may hold the Mandate structural survey's levels for the church and is the best next input for card 1.
- The QS 1898 section plates (facing pp. 148 and 152): the scan is public, but the Internet Archive OCR of the plates is unreadable, and the page images were not read in this pass.
- Corbo 1981 and Gibson & Taylor 1994: still not in the corpus (their ±0.00 definition is unverified).

## Seed / reproducibility
- Mesh: node 12, accessor 1 (POSITION) and 2 (NORMAL), world matrix as in round 1. Grid 0.5 m, origin x −164, z −141. "top" = max y of vertices with normal_y > 0.3; "low" = min y of all vertices per cell. Code: `/home/claude/swarm/scratch/A4/code2/` (`grid.py`, `topgrid.py`, `q.py`, `pit.py`, `zoom.py`).
- Albright VI-F frame and lon/lat: `out/A3/albright_sheet_georef.csv`. Spot heights were read by eye from crops of the 5,723 × 6,036 JPEG (church about px 1,180/4,050; Haram about px 3,926/4,261). The crops were deleted.
- Feet to metres: × 0.3048.
