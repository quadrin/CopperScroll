# Round-2 review RR5: lanes C1c, C2, C3, C4 (6 Nov 2026)

Reviewer RR5. Batch: `out2/C1c` (2 cards), `out2/C2` (3), `out2/C3` (3), `out2/C4` (3), 11 cards in all. For each card I checked the round-1 file (`out/<LANE>/FINDS.md`) and the round-1 reviews (R4 for C1c/C2, R5 for C3/C4). I reopened the cited evidence for at least the strongest claim and ran the cheap kill tests listed below. AGENTS.md procedures were not applied (REVIEW2_NOTE). No lane folder, repo, Drive or git was changed. Private check images are in `/home/claude/swarm/private2/RR5/` (SWP tile check at Qumran, TIR detail, ERT crop). No coordinates of unrecorded features appear here.

---

## C1c, card 1: GLO-30 agrees with the official gauge to within about ±1 m on the shore plains; the round-1 "+5 m" came from a June 1974 line picked too far landward

**Verdict: SURVIVES.** Tag kept: NEW TO THE PROJECT (gauge series, the GLO-30 test, the corrected 1974 line); KNOWN BUT UNDER-DISCUSSED for the wadi-mouth deficits. Confidence: high (plains agreement; C1c-3 killed); medium (picking rather than registration). Cost: cheap.

**Round-1 link.** This is the kill test of round-1 C1c-2 (R4: "needs an IHS gauge value") plus new data (the IHS series, 11 Landsat dates). It is not a restatement. It kills the DEM half of C1c-2 and all of C1c-3.

**Evidence checked**
- I recomputed the per-date medians from `landsat_waterlines_1980_2010.csv` with the card's filter (N 3481.0–3507.5 km, slope < 0.08). All 11 values match `glo30_vs_gauge_by_date.csv` to 0.01 m (+0.39, −1.01, +0.22, −0.28, +0.54, +0.73, +0.92, +3.03, −0.80, +0.15, +0.18).
- `hexagon1974_vs_mss1975_waterline.csv`: the median MSS 1975 minus HEXAGON 1974 offset is 89 m over 29 transects. My quartiles are 24 / 89 / 174 m; the card gives an IQR of 40–172 m, a small difference. A lake fall of about 0.5 m between June 1974 and June 1975 moves the line about 15–20 m on 3 % slopes, so it does not explain 89 m.
- I downloaded the IHS series again through the CKAN API (`datastore_search`, resource 823479b4…): 695 rows. All match `deadsea_level_ihs.csv`.
- Site 139a: I sampled GLO-30 (`scratch/C1c2/glo30_N31E035.tif`) at the private WBADB point: **−373.6 m**, against the card's −373.0. The point lies far above any lake level of the last two centuries, so C1c-3 is dead.

**Literature check.** A grep of repo main and `branch_only` for "data.gov.il", "Hydrological Service" and "823479b4" finds only Survey of Israel orthophoto notes. The project holds no gauge series.

**Alternatives tried.** Vertical datum (EGM2008 against the Israeli levelling datum) is under 1 m. A Landsat geolocation bias would have to be one-sided on every date, which is unlikely, as the card says. The 1999 +3.0 m outlier is still unexplained.

**ARGUMENT.** "Near-physical picture of where that shore ran" overstates a little. It is true only if the modelled 1st-century level (−395 to −400 m) is right, and that ±2.5 m range alone moves the line by about 80 m on 3 % slopes. The claim that no rating changes is correct.

## C1c, card 2: the 1 Dec 1979 gauge value (−400.14 m) is a one-month spike, probably a slip for −401.14

**Verdict: SURVIVES** (supporting numbers corrected). Tag kept: NEW TO THE LITERATURE (tentative). Confidence: medium-high that the value is wrong; low for the correct value. Cost: moderate (IHS yearbook).

**Evidence checked**
- The API rows read `_id` 659 01/10/1979 −400.99, 658 01/11/1979 −401.08, **657 01/12/1979 −400.14**, 656 01/01/1980 −400.63. Confirmed.
- I recomputed the series statistics from the API download:
  - The +0.94 m rise and the −0.49 m fall are the largest rise and the largest fall in the whole series. Confirmed.
  - The next largest fall is **−0.32 m** (28 Jun → 24 Jul 1995), not −0.37 m.
  - The other Dec→Jan changes (38, not 49; the readings are irregular) run from **−0.20 to +0.44 m**, not −0.16 to +0.26.
  - The other Nov→Dec changes run from **−0.18 to +0.06 m**, not −0.27 to +0.01.

  None of these corrections touches the core.
- Caveat the card leaves out: a one-month rise of +0.89 m did happen in the flood winter of Jan–Feb 1992. So the rise alone is possible. The **reversal** is what cannot be physical: a fall of half a metre in one winter month, against about 0.1–0.2 m of winter evaporation. Read as −401.14, the value gives a smooth series.

**Literature check.** Web search `Dead Sea level monthly 1979 1980 "-401.14" OR "-400.14"` found only the USGS OF 78-176 report and PANGAEA items, with no tabulated 1979 value. No erratum was found.

## C2, card 1: the desert half of ASI Map 106 (Talpiyot) is a published-record hole; Hirschfeld's 115-site survey was published only for the municipal strip

**Verdict: SURVIVES.** Tag kept: NEW TO THE PROJECT. Confidence: high. Cost: cheap.

**Round-1 link.** New area, and it explains the gap. It is not a restatement of C2-2.

**Evidence checked**
- ESI 3 (1984), store page index 69–70: "One hundred fifteen sites were recorded on this map". The breakdown (15 undated, 12 Bronze Age cairns, 17 Iron Age, 11 Second Temple, 40 Byzantine with 12 monastic, 20 winepresses) is confirmed verbatim.
- Kloner's online intro (`GetMapIntro?mapId=53`, GET, fetched today): "Y Hirschfeld surveyed the area of the Map of Talpiyot, part of it included within the municipal boundaries". Confirmed.
- The ASI online dump for map 53: all 144 sites lie at PG E 170.0–174.9, and none lies east of E 175. Confirmed.
- WBADB, E 175–180: **5 rows in N 120–129** (Kh. Jinjas, Theodosius, el-Burj, the two el-Maʿaṣia forts) and 7 rows in N 120–130. The card says 7 for N 120–129, a minor slip.
- The project file `asi_jerusalem/coverage_statements.csv` calls Map 106 "comprehensive (no explicit full-area statement)". `maps_used.csv` gives the sheet's full extent (lon 35.21–35.316) and ties it to places including `mar_saba` and `tekoa_herodium`. This supports the card's point that the project reads the block as covered.
- Kill test re-run: I took the 62 private feature positions and computed the nearest record over WBADB, all ASI online dumps and `water.csv`. **7** lie within 500 m, 42 are more than 1 km away, and the median is 1.38 km. The card gives 8, 42 and 1.28 km using more layers. Consistent.

**Literature check.** Web search for Hirschfeld "Map of Talpiyot"/"Map of Talpiot" found the CMHL bibliography entries for the preliminary notes only (ESI 2: 58–59; HA 82 (1983): 50–52). These are a third preliminary note, not a site gazetteer. No site-level publication was found.

**ARGUMENT.** It is measured: it turns silence into "unpublished" and moves no candidate. It does not overstate.

## C2, card 2: the georeferenced SWP (POM `pal63k-1880`) is displaced 0.3–0.8 km on the Qumran–ʿAin Feshkha strip

**Verdict: SURVIVES, TAG CHANGED** to NEW TO THE PROJECT. The provisional NEW TO THE LITERATURE applies only if the native sheet shows the same offsets. Confidence: medium. Cost: cheap (native sheet on Drive 07).

**Evidence checked.** I fetched POM z15 tiles around Kh. Qumran myself and marked the true position (31.7408 N, 35.4589 E). Private image: `private2/RR5/qumran_swp_check.png`.
- The SWP ruin circle "Kh. Kumrân" is drawn about **335 m NNW** of the true ruin.
- On the sheet the true point falls *south* of the SWP's Wady Kumrân line, on the wrong bank.

So a displacement of several hundred metres is confirmed. My bearing (NNW) differs from the card's "WNW" for this control. I did not recheck the Feshkha or Tannur label anchors.

**Why the tag changes.** The card cannot say whether the offset comes from the 1873–74 drawing or from POM's rubber-sheeting. A local fault in a third-party web georeference is a project-level fact. Levin et al. (ICC 2015) give only an overall RMSE of 74.4 m in what is online, with no regional breakdown (checked), so nothing published contradicts or anticipates the card.

## C2, card 3: Thomsen 1917 already lists the Dabbus el-ʿAbd milestone (no. 379) and treats both SWP roads; TIR omits the Buqeia road

**Verdict: MERGE into round-1 C2-3** (as its correction). Final tag: KNOWN BUT UNDER-DISCUSSED. Confidence: high. Cost: cheap.

**Evidence checked** (local archive.org OCR, `scratch/C2r2/dl_thomsen/thomsen.txt`):
- Lines 5047–5049: "379. Etwa 2½ km östlich von talʿat ed-damm ein Mst (genannt dabbus el-ʿabd) Inschrift unbekannt. PEF Mem. III S. 188". Confirmed.
- Lines 4817–4820: "Zweifelhaft als R[ömer]str[aße] ist die Verbindung zwischen beitin und eriha über ras et-tawil und durch das wadi abu retmeh". Confirmed.
- Lines 5050–5059 (road XL): "aber wohl erst byzantinische Anlage. Mst fehlen" (OCR "bj^zantinische … yht telileii"). Confirmed.
- TIR: I viewed the repo `tir-north-hyrcania-detail.png`. The only line through Ras el-Baquq–Hyrcania is the blue double aqueduct, and no red road is drawn. Consistent with the card.

**Why MERGE.** This is the kill test that round-1 C2-3 named. It is correct, and it demotes the milestone half of C2-3 (the stone is catalogued, only not in any digital dataset). It is a correction, not a separate find. It should replace C2-3's milestone sentence, and C2-3 keeps the Itiner-e/TIR omission.

## C3, card 1: the water inventory puts the Herodium aqueduct head, its destination and ten Solomon's Pools rows on hill-top ruins 0.3–1.2 km away; the drop of 111 m shrinks to about 30 m

**Verdict: SURVIVES.** Tag kept: NEW TO THE PROJECT. Confidence: high. Cost: cheap.

**Round-1 link.** It overlaps round-1 C3-2 (WBS:4287 = fortress grid) and the round-1 dead end, which already called the Artas and Solomon's Pools fallback points "terrain-impossible". R5 left "pool more than 350 m away" unverified. The new parts:
- the pool distance is measured;
- Mazar's head grid is legible;
- the Solomon's Pools offsets are quantified;
- the gradient consequence is worked out.

That is enough to count as more than a restatement.

**Evidence checked**
- `water.csv`: `LIT-MAZ-HERODIUM-AQ`, `-ARTAS-SPR` and `-ARTAS-DAM` sit at 31.6797/35.18593 (350 m), with the note "grid ref partly illegible". The `-HERODIUM-POOL` and `LIT-NET01-LH-*` rows sit on S4287 at 31.666169/35.240763. The ten `LIT-MAZ-SOL-*` rows sit at 31.68511/35.17960. All confirmed.
- I fetched the OSM nodes myself (api.openstreetmap.org): pool 8803075026 at 31.66869/35.23901, summit 431633653, Artas Spring 2935013947 at 31.68875/35.18567.
- My distances: S4287 to pool **325 m**; WBE:833 to pool **548 m**; summit to pool 433 m; project head to Mazar 1678/1217 **906 m**; OSM spring to Mazar grid 162 m. GLO-30 gives: project head 843 m, Mazar head 678 m, S4287 722 m, pool 655 m. These match the card to within a few metres. The drop becomes about 121 m against 16–31 m.
- The 30 Oct sweep note (line 94 area) has "Urtas spring (map ref. 1678 1217)". Confirmed, so `water.csv` is stale against the project's own reading.
- Note: 325 m is *inside* the 350 m label of the LIT rows and outside the 100 m label of the WBADB rows. The card says this correctly.

## C3, card 2: Mazar's grid for Herodium-aqueduct point 62 (1697 1221) is on a 766 m spur, 75–95 m above the channel

**Verdict: SURVIVES.** Tag kept: NEW TO THE LITERATURE (minor erratum). Confidence: medium. Cost: cheap (Mandate 1:20,000 contours).

**Evidence checked**
- JRA 46 text layer, p. 124: "62 (map ref, 1697 1221)". Confirmed.
- I converted the grid (EPSG:28191) and sampled GLO-30. At 169700/122100 the height is **770 m**. Every cell in a 100 m grid from E 169.5 to 169.8 is 712–775 m.
- Cells that suit a channel at 670–695 m lie at E 168.7–169.1 on N 122.0–122.1 (for example 169000/122100: 681 m). This fits the card's reading of Fig. 1 and the "1690/1691" misprint.
- Mazar's end point 1726/1198 gives 674 m, against "c. 670". Confirmed.

**Alternatives.** A tunnel is excluded by Mazar's "built section". An E/N swap is excluded, because the head uses the same order. I did not run the Fig. 1 scaling myself.

## C3, card 3: the juglet cave (P&A Cave 13 = ʿAtiqot 41 X/35) has a 1993 grid in `caves.csv` never joined to 3Q; 0.43–0.50 km NNE–NE of point 8

**Verdict: SURVIVES, TAG CHANGED** to NEW TO THE PROJECT only. The provisional NEW TO THE LITERATURE for the "clash" is dropped. Confidence: medium. Cost: moderate.

**Evidence checked**
- `caves.csv` row `A41:X/35` gives "19380/13015" and "= Patrich and Arubas Cave 13 ('Q3')". `DJD3:8` gives 193486/129756. Distance **503.8 m at 38.6°**. Confirmed.
- `devaux1952_cave_points/README.md`: "I found no 1993-survey cave coordinates in the repo, so there was nothing to match". Confirmed, and the statement is wrong, because the repo's own `caves.csv` holds the grid. That is the core of the card, and it holds.

**Why the NEW TO THE LITERATURE part is dropped.** The 130 m westward correction rests on two assumptions:
- that the OSM track is P&A's 1988 "track";
- that a 1993 grid printed to 10 m is accurate to better than about 100 m.

Hand-held GPS under Selective Availability (1993), or a map-derived grid, gives errors of the order of 100 m. So the "clash" between the printed easting and the excavators' description is within plausible positioning error.

The Region X "eastward bias" ARGUMENT is labelled as such, but it is speculative. It should not weaken F's predicate until positions are checked on imagery.

## C4, card 1: Ḥorbat Ha-Gardi, a 2009 GPR/EM "large subterranean cavity" under Sheikh Gharbawi's tomb, untested; the 2024 final report omits the survey

**Verdict: SURVIVES.** Tag kept: NEW TO THE LITERATURE (small). Confidence: high (published and omitted); low (meaning). Cost: moderate (Basson's report).

**Evidence checked** (Hadashot text, `scratch/R2/t/hadtext/`):
- `en/vol-123/01712_h-orbat-ha-gardi.txt` lines 264–289: "beneath the tomb of Sheikh Gharbawi there is a large subterranean cavity, whose eastern part is cut by a deep modern trench". Confirmed. So is the line "three and even four secondary compounds".
- `en/vol-136/26469_h-orbat-ha-gardi.txt` (565 lines): no match for geophys, radar, GPR, cavit, subterr, Basson or 2009. In the Hebrew version the only חלל hit is "חלל החדר" (the room's space).
- Decisive detail: the 2024 report **cites Re'em 2011 twice** (lines 44, 73), for the 2006 excavation, but never its geophysics. So the omission is not an oversight of the source.

**Literature check.** Web search ("Horbat Ha-Gardi Maccabees tomb Sheikh Gharbawi cavity radar Re'em") found only the press pieces the worker had already read (Fox, Live Science, JPost, BAR, artnet, bibleplaces). None mentions the cavity.

## C4, card 2: a register of 9 published geophysical void targets later dug; in Lisan marl only the shallow cliff target was real

**Verdict: WEAKENED, TAG CHANGED** to NEW TO THE PROJECT. Confidence: medium for the per-case facts; low for the depth and substrate conclusion. Cost: cheap.

**Evidence checked.** Gezer, HA 121 report 1294: "The survey detected one distinct anomaly … No signs of quarrying or other human activity … the geophysical survey was not at all suitable for the rock structure". Confirmed. I read rows G01–G17 of the register.

**What fails**
- **The depth split does not hold in the marl.** The four marl cases are:
  - G01 (16 m): failed;
  - G02 (probe to about 3 m, below a 1.2 m floor): failed, but not "deep";
  - G03 (0.5–1 m): real;
  - G04 (0.5–1 m, a shallow cliff target): failed.

  So shallow marl targets are 1 of 2. Depth is not what separates success from failure. "The deep plateau targets failed" rests on G01 alone.
- **"Both tested targets deeper than 3 m were not archaeological"** is n = 2 (G01, G06).
- **The classes are mixed.** The register counts cisterns and entrances (Sepphoris), known aqueduct shafts (Bet ha-ʿEmeq) and objects in rubble (Cave of Letters) as "void targets". So the 4/1/4 tally is not a rate.
- **Tag.** A compilation of nine cases from this corpus is a useful project table, not a literature finding.

**ARGUMENT (a) overstates.** "Belong to the class that has failed every time it was tested" means n = 1–2. G13–G14 are also coded "Lisan marl", but the line ran "over dump", so the upper bodies may sit in fill. Point (c) of the card admits the small n, but the title and (a) do not.

**What survives.** The register itself (G01–G17, sourced) and the observation that the corpus's deep marl "cavity" targets have never been confirmed.

## C4, card 3: the 2002 Qumran ERT "possible cave" is not closed; at 100–180 Ω·m it rises to the surface through a neck under the WALL marker at about 41 m; body 2 is closed

**Verdict: SURVIVES.** Tag kept: NEW TO THE LITERATURE (a reading of a published figure). Confidence: high (in the figure); low (meaning). Cost: cheap.

**Kill test run independently.** I downloaded the Drive figure (`1iT4sAYZ-…`, 976 × 730) and wrote my own nearest-colour classification on the colour bar (row 588, px 380–586, 50–240 Ω·m). I used 4-connected labelling with seeds at 35 m / 6 m (body 1) and 59 m / 7 m (body 2).

| threshold | body 1 top | body 1 extent along line | body 2 top |
|---|---|---|---|
| 100 Ω·m | 0.0 m | 28.6–44.3 m | 4.2 m |
| 150 Ω·m | 0.0 m | 29.7–43.7 m | 5.8 m |
| 180 Ω·m | 0.1 m | 30.0–41.5 m | — |
| 200 Ω·m | 3.7 m (core 30.2–39.4 m) | | |

This reproduces the card's numbers. The neck is also visible by eye under the WALL marker at about 41 m (private crop `private2/RR5/ert_crop.png`).

**Caveat (the card names it).** Smoothness-constrained inversion and contour rendering commonly smear a resistive near-surface footing downwards, so reading (d) is at least as likely as a shaft. The result undercuts "sealed cave". It does not establish any of the other readings.

---

## Summary table

| lane | card | short title | original tag | verdict | final tag | confidence | cost |
|---|---|---|---|---|---|---|---|
| C1c | 1 | GLO-30 within ±1 m of the IHS gauge; round-1 +5 m and C1c-3 killed | NEW TO THE PROJECT / KBUD | SURVIVES | NEW TO THE PROJECT (wadi mouths KBUD) | high | cheap |
| C1c | 2 | IHS 1 Dec 1979 −400.14 m spike | NEW TO THE LITERATURE (tentative) | SURVIVES (stats corrected) | NEW TO THE LITERATURE (tentative) | medium-high | moderate |
| C2 | 1 | Map 106 desert half: Hirschfeld's 115 sites unpublished; 54/62 SWP features unrecorded | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high | cheap |
| C2 | 2 | POM SWP displaced 0.3–0.8 km on Qumran–Feshkha strip | NEW TO THE LITERATURE (prov.) | SURVIVES, TAG CHANGED | NEW TO THE PROJECT | medium | cheap |
| C2 | 3 | Thomsen 1917 no. 379 Dabbus milestone; roads judged in 1917; TIR omits | KBUD | MERGE (into round-1 C2-3) | KBUD | high | cheap |
| C3 | 1 | Herodium aqueduct head/dest + Solomon's Pools rows on hill-top ruins; drop 111 → ~30 m | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high | cheap |
| C3 | 2 | Mazar point 62 grid on 766 m spur (misprint) | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | medium | cheap |
| C3 | 3 | X/35 = Cave 13 grid in caves.csv, 0.43–0.50 km from 3Q | NEW TO THE PROJECT / NTL (prov.) | SURVIVES, TAG CHANGED | NEW TO THE PROJECT | medium | moderate |
| C4 | 1 | Ḥ. Ha-Gardi 2009 cavity untested; omitted by 2024 report | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high / low | moderate |
| C4 | 2 | Register of 9 dug geophysical void targets; marl deep targets fail | NEW TO THE PROJECT / NTL | WEAKENED, TAG CHANGED | NEW TO THE PROJECT | medium / low | cheap |
| C4 | 3 | Qumran ERT body 1 open to surface via neck; body 2 closed | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high / low | cheap |
