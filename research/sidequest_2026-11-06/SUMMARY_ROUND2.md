# Side-quest swarm, round 2 (6 November 2026): summary

**Why round 2.** On 6 Nov the owner removed `AGENTS.md` (PR #93, merged as bb612c3) and asked for the side-quest work to be done again without its procedures. Round 2 used the brief changes in `ROUND2.md`:
- no frozen protocols, held areas, exposure rules or blind readers;
- a budget of about 150 tool calls per lane;
- each lane builds on round 1 instead of repeating it;
- cards may argue scroll consequences, in a part labelled ARGUMENT.

Safety rules stayed the same: AI only, no change to the repository by workers, image licences, site protection and secrets. Round 1 is in `SUMMARY.md` and is unchanged.

**What ran.** 25 lane workers (A1–A6, B1a–c, B2–B6, C1a–c, C2–C4, D1–D3, E1, E2), then 6 reviewers (RR1–RR6, about 4 lanes each), who reopened the evidence and ran the kill tests that the workers had left. RR6 also reviewed the orchestrator's direct search for entry 24.

**Result.**
- 78 cards written. The reviewers **killed 1** (B5-4: not new), **merged 6** into round-1 cards (B1a-3, C2-3, D3-3, E1-3, E2-1, E2-3) and **weakened 16**.
- **71 distinct new cards survive:** 29 NEW TO THE LITERATURE, 37 NEW TO THE PROJECT, 5 KNOWN BUT UNDER-DISCUSSED (counted by the leading tag after review).
- Round 2 also **killed or corrected four round-1 cards**:
  - C1c-2: its DEM reading is killed (GLO-30 matches the official gauge to about ±1 m).
  - C1c-3: killed.
  - C1a-1: its antiquity reading is killed (the "ring" is a military trench position).
  - A1-1/A1b-2: segment 15 has 5 rivets on EDF's own films, which reverses R7's rejection.

**Where it is.**
- Lane branches `claude/sidequest-2026-11-06-r2-<lane>`, each with `research/sidequest_2026-11-06/round2/<LANE>/`.
- The summary branch holds all lanes under `round2/`, the reviews under `round2/review/` and this file.
- Private products are in `sidequest_2026-11-06_private_round2.zip`.

---

## Round-2 top 10

Ranking rule as in round 1: tag × confidence × cost, with variety of lanes and a preference for cards that touch the scroll or the project's data.

### 1. "Cave Q3" of licence L-399/1986, which is 3Q itself (the Copper Scroll cave), is placed 2.95 km SE of 3Q on the shore plain (B2-1)
- NEW TO THE LITERATURE (the point) / NEW TO THE PROJECT (the identity). High.
- The Staff Officer for Archaeology permit register in the original WBADB workbook (1,177 entries, never used before) and WBADB both put the 1986 dig at 195500/127600. ESI 6 pp. 68–69 says Cave Q3 = the 1952 cave no. 8 = 3Q, dug in April 1986.
- RR3 ruled out the balsam-juglet cave: WBADB lists it separately (L-640, 1988).
- **Project data:** `caves_entry25/caves.csv` row `WB:E756` counts this point as a separate cave.

### 2. *Maresha IV* (IAA Reports 76, 2025): all map references sit about 80 m NE of their complexes, which matches a WGS84 → Israel-grid conversion made without the datum shift (A6-1)
- NEW TO THE LITERATURE. High for the offset; medium for the mechanism.
- 30 of 31 references are off by a median +64 E / +48 N, against +66 / +41 for the omitted datum shift.
- The same team's earlier Hadashot references and Kloner's chapter 4 reference are right, and the Cana IAA 75 volume is clean as a control.
- RR2 recomputed the vector and found an independent check that needs no imagery.

### 3. ROSAPAT 07's coordinates are WBADB's decimal lat/lon fields, copied; four monuments are misplaced as a result (C1b-1)
- NEW TO THE LITERATURE. High; RR4 found the evidence stronger than the card said.
- 14 of 68 entries fall within 1.5 m of WBADB points; entries 50 and 36 match WBADB's own decimals to 1e-6°.
- This explains round 1's Hisham's Palace offset: it is the point of a sherd scatter, Bar-Adon site 59c.
- New mislocations: Beit Jabr et-Tahtani (363–507 m), Kh. Qaqun (685–735 m), the Monastery of the Towers (361–400 m, possibly listed twice).

### 4. Humbert & Gunneweg 2003 gives five NAA samples two or three incompatible chemical origins, including QUM 209, which carries Conclusion 1 (B6-1)
- NEW TO THE LITERATURE. High that the conflict is in print.
- Takes round-1 top-10 #1 further. QUM 209 is "Group I, khirbeh jug" on p. 19, "el-Jib-like, north of Cave 1" on p. 24 and "Arad–Beer Sheba" on p. 392. QUM 211, 215, 217 and 221 conflict in the same way.
- ARGUMENT (modest): it removes the only Negev-made object tied to the limestone caves (Cave 3 included). It favours no entry.

### 5. Gerizim's 110/109 BCE terminus rests on a winged-thunderbolt bronze (Cat. 346), the wrong type for that year; the date has spread to the tesserae and to *Middle Maccabees* (B4-1)
- NEW TO THE LITERATURE. High for the printed facts; medium that the coin is misread.
- Takes round-1 top-10 #10 further. The catalogue's own comparison is the 113/112 variety. Antioch's ΓΣ bronzes are a different type (SC 2368).
- RR3: Finkielsztejn's chapter never names Gerizim, and the editors also misstate him on Samaria and Scythopolis.
- The SNG Israel 2697 kill test is still open.

### 6. Qumran: the 2002 ERT "possible cave" is open to the surface through a neck under the WALL marker; the unlabelled second body is closed (C4-3); and at Ḥorbat Ha-Gardi a 2009 radar cavity under the sheikh's tomb was never tested (C4-1)
- Both NEW TO THE LITERATURE. RR5 reproduced the neck with its own colour classification.
- The 2024 Ha-Gardi final report cites Re'em 2011 twice but never mentions the 2009 survey.
- The register of 9 dug geophysical targets (C4-2) survives as a sourced table (WEAKENED).

### 7. Hadashot: nine reports print the wrong excavation year in both languages, and 14 citation labels give the wrong permit (B1b-1, B1b-2)
- NEW TO THE LITERATURE. High. The permit clock dates each to the month, and three have a third witness (e.g. Ṣur Bahir 27732 "Oct 2010", which HA 136 says was in 2013).
- Label examples: Kefar Uriyya A-9146 → A-6146; Ḥ. Manoaḥ A-9775 → A-7775.
- B1b-3: about 25% of excavation permits of 2005–2017 have no HA report (RR2's corrected figure). ARGUMENT: the project's "nothing recorded here" inferences built on HA miss about a quarter of digs.

### 8. ʿAtiqot: 17 articles' map references fail their own NIG/OIG twin or their Hebrew text, 7 of them by 40–450 km; and one dig placed in two places by two IAA publications (B1c-2, B1c-3)
- NEW TO THE LITERATURE. High. RR3 rendered ʿAtiqot 76 p. 217: the ʿEn Yaʿal burial cave is NIG 21695/62775, 52 m ESE of the spring. The project places it by name only.
- Naḥal Rimmonim (ʿAtiqot 118) is about 10 km west of its own text and of HA 09562.
- B1c-1: 23 BCE/CE slips in 21 HA reports. The Hebrew is wrong in about half, so it is not a safe reference.

### 9. The Herodium aqueduct: Mazar's grid for point 62 lands on a 766 m spur, and the project's water inventory puts both ends of the Artas–Herodium aqueduct and all ten Solomon's Pools rows on hill-top ruins 0.3–1.2 km from the installations (C3-2, C3-1)
- C3-2 is NEW TO THE LITERATURE (medium); C3-1 is NEW TO THE PROJECT (high).
- Corrected, the aqueduct falls about 16–31 m, not 111 m. The entry-21 bearing moves from 285° to 292° and still fails.

### 10. 3Q15: on EDF's own radiographs segment 15 has 5 rivets (text and plates say 4), the 2/3 sheet join had at least 7 positions, and segment 10's "huit rivets" is right (A1-1, A1-2)
- A1-1 NEW TO THE LITERATURE (provisional); A1-2 NEW TO THE PROJECT. RR1 checked the films and the 1988 frame of the segment 10 foot.
- On both joins, EDF's condition plates draw fewer rivets than its films show.

**Also notable:**
- **E1-1:** Eshel & Safrai date the Massekhet Kelim preface's AM 3331 to "373 BCE"; it is 431/430. The plaques are probably modern forgeries. This touches Milik's Carmel candidate for Koḥlit.
- **B2-2:** HA 106's licence "837" was not issued until 1999.
- **B6-2:** HF2019's oldest radiocarbon-dated linen is printed with another textile's number.
- **D3-1:** HCM 2016 Pl. 42/45 are titled "Locus 83-3" for L. 81.3 material, including scroll jar KhQ 1492.
- **A2-2:** four more negatives of the copper rolls in situ (EBAF 13781–83, PAM 41958).
- **C1c-1:** GLO-30 is within ±1 m of the gauge on the shore plains; this kills round 1's "+5 m".

---

## All surviving round-2 cards (71)

Each lane's `round2/<LANE>/FINDS.md` has the full card, and `round2/review/RR*.md` has the reviewer's notes and corrections.

| Lane-card | Short title | Leading tag | Verdict | Reviewer | Confidence | Cost |
|---|---|---|---|---|---|---|
| A1-1 | Seg 15: 5 rivets on EDF films; seg 16: 6 hole positions; >=7 at 2/3 join | NEW TO THE LITERATURE | SURVIVES | RR1 | high (5 discs/4 holes); medium (7 total) | cheap |
| A4-1 | Model elevations = Schick 1898 feet (2420 ft datum); OS floor 2.4 m higher | NEW TO THE LITERATURE | SURVIVES | RR1 | high | cheap |
| A6-1 | Maresha IV refs ~80 m NE datum shift | NEW TO THE LITERATURE | SURVIVES | RR2 | high / medium (mechanism) | cheap |
| A6-2 | Maresha SC 89/90 SC 169 SC 97 slips | NEW TO THE LITERATURE | SURVIVES | RR2 | high | cheap |
| B1b-1 | 9 both-language year errors (permit clock) | NEW TO THE LITERATURE | SURVIVES | RR2 | high | cheap |
| B1b-2 | DOI vs Fig. 1 permit-label errors | NEW TO THE LITERATURE | SURVIVES | RR2 | high | cheap |
| B1c-1 | HA BCE/CE era slips EN and HE | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B1c-2 | Atiqot NIG/OIG and EN/HE map-ref conflicts (17 articles) | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B1c-3 | HA x Atiqot same dig: Rimmonim, Ahihud, En Zippori | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B2-1 | Cave Q3 L-399/1986 = 3Q misplaced 2.95 km | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B2-2 | HA 106 licence 837 anachronism; ghost entry; 255-char truncation | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B2-4 | JSP 9 Shaked tower ITM built from swapped IOG | NEW TO THE LITERATURE | SURVIVES | RR3 | high | cheap |
| B4-1 | Cat. 346 thunderbolt type vs SC 2368; 110/109 spread; Middle Maccabees misattribution | NEW TO THE LITERATURE | SURVIVES | RR3 | high / medium | needs new data |
| B5-1 | Homoud = embassy counsellor; three Jordanian men | NEW TO THE LITERATURE | SURVIVES | RR4 | medium | needs new data |
| B6-1 | HG2003 NAA chemistry conflicts (QUM 209, 211, 215, 217, 221) | NEW TO THE LITERATURE | SURVIVES | RR4 | high (printed); low (which group) | cheap |
| B6-2 | HF2019 Gr11Q98/198/183 for IAA 577250 | NEW TO THE LITERATURE | SURVIVES | RR4 | high | cheap |
| C1a-2 | Qasr el-Khan: ASI point on trig 881T, Mandate ruin 330 m SSE | NEW TO THE LITERATURE | SURVIVES | RR4 | high (positions); low-medium (tower) | needs new data |
| C1b-1 | ROSAPAT coordinates copied from WBADB nodes; 4 misplacements | NEW TO THE LITERATURE | SURVIVES | RR4 | high | cheap |
| C1c-2 | IHS 1 Dec 1979 -400.14 m spike | NEW TO THE LITERATURE | SURVIVES | RR5 | medium-high | moderate |
| C3-2 | Mazar point 62 grid on 766 m spur | NEW TO THE LITERATURE | SURVIVES | RR5 | medium | cheap |
| C4-1 | Ha-Gardi 2009 cavity untested; omitted in 2024 report | NEW TO THE LITERATURE | SURVIVES | RR5 | high/low | moderate |
| C4-3 | Qumran ERT body 1 open to surface via neck; body 2 closed | NEW TO THE LITERATURE | SURVIVES | RR5 | high/low | cheap |
| D3-1 | HCM 2016 Pl. 42/45 "Locus 83-3" = 81-3 | NEW TO THE LITERATURE | SURVIVES | RR6 | high | cheap |
| D3-2 | Magen 2018 Fig. 9 scale bar "cm" | NEW TO THE LITERATURE | SURVIVES | RR6 | high | cheap |
| E1-1 | Eshel & Safrai AM 3331 = "373 BCE"; Kelim plaques forged? | NEW TO THE LITERATURE | SURVIVES | RR6 | high (arithmetic); medium (novelty) | cheap / moderate (Davila 2013) |
| E1-2 | Lahav Forest, Har Avihu, Oron B map refs | NEW TO THE LITERATURE | SURVIVES | RR6 | high | cheap |
| E1-4 | Khirbat ʿAmra W20-22 used twice | NEW TO THE LITERATURE | SURVIVES | RR6 | high (facts); low (importance) | cheap |
| E2-2 | Itiner-e x TIR join; Ein Gedi and Livias divergences | NEW TO THE LITERATURE | SURVIVES | RR6 | medium-high | cheap |
| B3-4 | Naveh Hyrcania inscription omitted in 2024 report; CE date | NEW TO THE LITERATURE | WEAKENED | RR3 | high (facts) | needs new data |
| A1-2 | Seg 10 eighth rivet at 0.97 (Q10G ring + 1988 domed head); omitted on plates | NEW TO THE PROJECT | SURVIVES | RR1 | high | cheap |
| A2-2 | EBAF 13781-83 + PAM 41958 in-situ copper roll negatives | NEW TO THE PROJECT | SURVIVES | RR1 | high (rows); medium (distinct exposures) | moderate |
| A2-3 | Lot 2 EBAF numbers out of year order; 9x12 inside 24x36 range | NEW TO THE PROJECT | SURVIVES | RR1 | high (facts); low (cause) | moderate |
| A2-4 | L123 east vs west of L122; 23-3-1955; caption/repertory locus conflicts | NEW TO THE PROJECT | SURVIVES | RR1 | high (a); medium-low (b) | cheap / moderate |
| A3-1 | Town-survey sheet corner V-E/V-F/VI-E/VI-F at the Citadel; 5 km origin | NEW TO THE PROJECT | SURVIVES | RR1 | high; medium (defined origin) | cheap |
| A3-2 | 1928 V-F silently adds Macalister-Duncan Ancient Wall & Tower; NLI 1925 set | NEW TO THE PROJECT | SURVIVES | RR1 | high | cheap |
| A3-3 | U1-U10 random null; U5 = ASI 102/480; five open | NEW TO THE PROJECT | SURVIVES | RR1 | medium; low | moderate |
| A4-2 | Void 3 = Schick St Helena cistern Z; model reproduces depth order | NEW TO THE PROJECT | SURVIVES | RR1 | high (Z); low (Y) | cheap |
| A5-4 | 1956 Crowfoot letter Murabbaat C14 | NEW TO THE PROJECT | SURVIVES | RR2 | high / low (GrN-943) | moderate |
| B1a-2 | 16 not-yet-deciphered inscriptions ledger | NEW TO THE PROJECT | SURVIVES | RR2 | medium | moderate |
| B2-3 | 49 licence spreads; register holds B2b errors; Carmel ITM swap | NEW TO THE PROJECT | SURVIVES | RR3 | high | cheap |
| B3-3 | Avigad 1962 x IIP/Rahmani ossuaries | NEW TO THE PROJECT | SURVIVES | RR3 | medium | moderate |
| B4-2 | Hoard screens re-run with Gerizim + Vespasian rows | NEW TO THE PROJECT | SURVIVES | RR3 | high | cheap |
| B4-3 | Lorber 2021 table: 9 hoards missing; Nablus 1891 date | NEW TO THE PROJECT | SURVIVES | RR3 | high / medium | cheap |
| B5-3 | Kuhn: Leverkusen reduction tests; no full text by Sept 1956 | NEW TO THE PROJECT | SURVIVES | RR4 | high (text); low (fragment) | cheap |
| B6-4 | Magen 2018 L17/L18, T1-T9, 37 graves | NEW TO THE PROJECT | SURVIVES | RR4 | high (facts); low (importance) | cheap |
| C1a-1 | Mishor ring = military trench position | NEW TO THE PROJECT | SURVIVES | RR4 | medium-high | moderate |
| C1c-1 | GLO-30 within ±1 m of IHS gauge; round-1 +5 m and C1c-3 killed | NEW TO THE PROJECT | SURVIVES | RR5 | high | cheap |
| C2-1 | Map 106 desert half unpublished; 54/62 SWP features unrecorded | NEW TO THE PROJECT | SURVIVES | RR5 | high | cheap |
| C2-2 | POM SWP displaced 0.3-0.8 km on Qumran-Feshkha strip | NEW TO THE PROJECT | SURVIVES | RR5 | medium | cheap |
| C3-1 | Herodium aqueduct + Solomon's Pools rows on hill-top ruins; drop 111 to ~30 m | NEW TO THE PROJECT | SURVIVES | RR5 | high | cheap |
| C3-3 | X/35 = Cave 13 grid in caves.csv 0.43-0.50 km from 3Q | NEW TO THE PROJECT | SURVIVES | RR5 | medium | moderate |
| D1-1 | ʿAtiqot 41 plans give facings (XI/18, XI/20, VIII/29) | NEW TO THE PROJECT | SURVIVES | RR6 | high | cheap |
| A1-3 | Seg 18 lines across corner fragment; stop at 17/18 cut; move undisclosed | NEW TO THE PROJECT | WEAKENED | RR1 | medium (fit); low (stop at cut) | moderate |
| A2-1 | EBAF 15747-15778 printed 1953 shows 1954-55 loci | NEW TO THE PROJECT | WEAKENED | RR1 | low | moderate |
| A5-2 | Kallia 1932 stylobate tall | NEW TO THE PROJECT | WEAKENED | RR2 | high (file) / low (unrecorded) | moderate |
| A5-3 | Hyrcania guide audio vs NEAEHL | NEW TO THE PROJECT | WEAKENED | RR2 | low | needs new data |
| B1a-1 | Moza sherd vs Tel Moza pre-firing group | NEW TO THE PROJECT | WEAKENED | RR2 | low | needs new data |
| B1c-4 | Akko lead amulet no reading | NEW TO THE PROJECT | WEAKENED | RR3 | low | moderate |
| B3-2 | Agathocles weight identity; two redatings | NEW TO THE PROJECT | WEAKENED | RR3 | high (identity) / low (mismatch) | needs new data |
| B6-3 | B6-2 rows settled; KhQ 1109/1112 swap | NEW TO THE PROJECT | WEAKENED | RR4 | high (readings); medium (swap direction) | cheap |
| C1a-3 | F014 affine LOO 290-970 m; local tie | NEW TO THE PROJECT | WEAKENED | RR4 | high | cheap |
| C1b-2 | SWP kokhim tomb at Ain ed Duk unrecorded | NEW TO THE PROJECT | WEAKENED | RR4 | medium (project); low (literature) | moderate |
| C4-2 | Register of 9 dug geophysical void targets | NEW TO THE PROJECT | WEAKENED | RR5 | medium/low | cheap |
| D1-2 | Four Tier-1 Koḥlit records read | NEW TO THE PROJECT | WEAKENED | RR6 | high | cheap |
| D1-3 | Tell Muhalhil ASI 1: no pool, no Hell./Rom. pottery | NEW TO THE PROJECT | WEAKENED | RR6 | high (record); low (consequence) | cheap |
| D2-1 | EDF 3e breaks predate 1988; seg 6 opened in treatment | NEW TO THE PROJECT | WEAKENED | RR6 | medium | cheap |
| A5-1 | Tryphon epitaph 592 calendrically impossible | KNOWN BUT UNDER-DISCUSSED | SURVIVES | RR2 | high (calc) / low (CIIP) | cheap |
| B1b-3 | 410 cited-but-unreported permits | KNOWN BUT UNDER-DISCUSSED | SURVIVES | RR2 | medium | moderate |
| B3-1 | SC 57->126 printed in HA 2014; CIIP cites it; IIP 65 records | KNOWN BUT UNDER-DISCUSSED | SURVIVES | RR3 | high | cheap |
| B5-2 | Kuhn ThLZ: Herbst 1953, no mirrors; Berlin Jan 1954 | KNOWN BUT UNDER-DISCUSSED | SURVIVES | RR4 | high | cheap |
| D2-2 | Flat-ground doors avoid W; decay on steep slopes | KNOWN BUT UNDER-DISCUSSED | WEAKENED | RR6 | medium | cheap |

## Killed and merged

- **Killed:** B5-4 (the openings dated to the day). Not new: the round-1 timeline, R1 and `atlas/app/atlas-history-data.ts` line 71 already have these dates.
- **Merged into round-1 cards:**
  - B1a-3 → B1a-3: the West Bank polygon test confirms R2's corrected pattern.
  - C2-3 → C2-3: Thomsen 1917 no. 379 already lists the Dabbus milestone.
  - D3-3 → D3b-1: the store copy is the IAA portal PDF of 13 Oct 2026.
  - E1-3 → E1-3: Crossref, 9,525 of 9,526 records.
  - E2-1 → E2-2: the Dabaritta road.
  - E2-3 → E2-1: terrain-matched null; a weak road preference can no longer be excluded, but E2-1 holds.

## Effects on round-1 cards

- **C1c-2:** the DEM half is killed. **C1c-3:** killed. Site 139a is at −373 m, so it was never in the lake.
- **C1a-1:** the antiquity reading is killed (a military trench position, Dec 1974 frame F017). Every round-1 C1a position was about 290 m too far north (C1a-3).
- **A1b-2 / R7:** segment 15 has 5 rivets on EDF's films; R7's rejection of r1 is reversed (A1-1).
- **A1d-3:** "huit rivets" is right; the eighth is at 0.97 (A1-2).
- **A3-2:** U5 is killed (= ASI 102/480); five of the ten labels are still open (A3-3).
- **B3-3:** the Agathocles weight's identity is restored (B3-2).
- **D3b-1:** the errors were in the IAA online PDF as of 13 Oct 2026 (D3-3).
- **B2b-1/2:** the errors are already in the SOA register itself (B2-3).

## Scroll-related ARGUMENT sections (none changes an identification)

- **Entry 24, Mughâret Ekteif (orchestrator note, WEAKENED by RR6):**
  - Route 1 crosses the lower Wadi Ekteif gorge loop; it was there by June 1974 and was widened later with fill over most of the gorge's north side.
  - Two zones on the north side survive and are the places to check on the ground.
  - The SWP description fits a stepped cistern access, which weakens Ekteif as entry 24's *tomb*. Only the route argument survives.
  - Position stays ±250–300 m. Files: `research/first_tests_2026-11-06/entry24_ekteif/HUNT_2026-11-06.md`.
- **Koḥlit (entries 4, 11, 15, 19, 60):**
  - E1-1 removes the only witness for Milik's Carmel candidate (if the plaques are forgeries).
  - D1-3: Tell Muhalhil's full ASI 1 entry has no pool and no Hellenistic or Roman pottery. RR6 weakened this, because ASI 109/5 has Roman–Byzantine "Tell Muhalhal" units about 1.5 km away.
  - D1-2: the "tombs at its mouth" relation is met by Kh. ʿAlmit as well, so it cannot pick a candidate.
- **Entry 25 / 3Q:** B2-1, 3Q's own 1986 record misplaced. C3-3: the juglet cave X/35 is 0.43–0.50 km NNE–NE of 3Q (NEW TO THE PROJECT after RR5).
- **Entries 16, 29, 35 (Hyrcania):** B3-4, Naveh's 1st-c. BCE inscription is missing from the 2024 report. Net effect neutral.
- **Entry 21:** C3-1, the corrected aqueduct still fails the bearing.
- **Hoard screens:** with the Gerizim hoards and the Vespasian cache added, the context screen goes from D 0.6808 to 0.6846 and stays DIFFERENT. The weight screen's predictions stand (B4-2).

## Corrections for the owner (project data)

- `research/regional/caves_entry25/caves.csv`: `WB:E756` ("Cave Q3", L-399/1986) is 3Q itself, misplaced 2.95 km; treat it as a duplicate of DJD3:8 (B2-1). X/35's grid is already in the file, so the `devaux1952_cave_points/README.md` line 136 note "no 1993-survey cave coordinates in the repo" is wrong (C3-3).
- `research/regional/caves_entry25/aspect.csv`: 33 of the 48 ʿAtiqot 41 caves whose record cites a plan are coded "no facing", but their plans and captions give a facing (XI/18, XI/20, VIII/29 shown) (D1-1). WBS:4143 (XI/19) carries the published misprint 19343/12391.
- `research/regional/water_systems/water.csv`: the Artas–Herodium aqueduct head and destination and all ten Solomon's Pools rows are 0.3–1.2 km off. Mazar's head grid reads 1678 1217 (C3-1).
- `maps_used.csv`: ASI Map 106 (Talpiyot) is not "comprehensive"; its desert half is unpublished (C2-1).
- Koḥlit chain: `next_links.md` says ʿAlmit is "not yet read", but it had been read (D1-2).
- The SWP layer from Palestine Open Maps is 0.3–0.8 km off along the Qumran–Feshkha strip (C2-2). Do not use it there without local controls.
- For HEXAGON F014, tie locally (Mandate 1:20,000 ink gives about ±40 m); every round-1 C1a position moves about 290 m south (C1a-3).

## Blocked inputs (round 2, short list)

- SNG Israel 1 and *Seleucid Coins* II (needed for the B4-1 kill test).
- The JSP 19 digital appendix.
- CIIP I.1 (both Drive copies stop at lemma 9) and CIIP IV.1 (stops at 2671).
- Brown 2005.
- Yadin 1957 (archive.org 403).
- The old IAA permit register (redirects).
- The current IAA online PDF of *Maresha IV* (Cloudflare).
- ʿAtiqot 118 Fig. 1 (55 MB).
- Davila 2013 and Schwartz 2021.
- The Basson 2009 Ha-Gardi report.
- Wayback fetches that waited for approval and got none (HA 12643 of 2014; the Hachlili necropolis PDF; PaleoJudaica 2011).
- Overpass mirrors (all timed out).

Each lane's FINDS.md lists the rest.
