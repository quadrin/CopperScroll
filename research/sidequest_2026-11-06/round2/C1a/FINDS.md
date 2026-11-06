# Side-quest C1a, round 2: Jerusalem, Mishor Adummim and the desert plateau. Change across image epochs (6 Nov 2026)

Lane C1, area C1a. Round 2 under `ROUND2.md`: AGENTS procedures retired, so held-area guards were bypassed where they applied (`allow_protected=True`). About 105 tool calls.
Inputs used: HEXAGON D3C1208-400636F014 (25 Jun 1974), **D3C1209-200214F017 (1 Dec 1974; first use for this area)**, CORONA DS1101-2168DF040–042 (26 Sep 1967), the Palestine Open Maps 1:20,000 1940s sheets and RAF 1940s layer, Esri World Imagery, IAA ASI Map 109/4 online records (D2's cached JSON), WBADB, ESI 7–8, IAA Reports 66, and the project's Hirschfeld 1992 read notes.
Coordinates of unrecorded features are in `private2/C1a/PRIVATE_LOCATIONS2.md` only. Public text gives frame pixels, distances and recorded-site numbers.

Public data: `F014_4point_affine.json`, `f014_affine_controls_loo.csv`, `qasr_el_khan_records.csv`, `tools/` (`reg.py` hand-control panels on a common UTM grid, `p4.py`, `blend.py` Mandate-ink overlay at trial shifts, `dcrop.py`, `maps.py`, `nccraf.py`).

---

FIND CARD
Title (one line): The Mishor Adummim "ring" of 1974 is the closed perimeter trench of a military position: the 1 Dec 1974 frame shows traversed (zigzag) fire trenches and dug emplacements beside it, 330 m west of the Euthymius monastery
Lane: C1a
Round-1 link: C1a-1 (Mishor Adummim earthworks 1974, gone by 1978). This card runs its kill test and reports the result.
What is odd (2–4 sentences): Round 1 left the ring's nature open and asked for a second epoch. The December 1974 forward frame, never located for this area before, is much sharper here than the June frame. On it the ring's rim is a dug trench with a bright spoil edge and small regular bays. About 300–700 m to the east, traversed zigzag fire trenches run along the slopes and close a second loop of about 100 × 140 m. The round-1 "strips" are 6–8 deep rectangular pits with shadowed walls and bright ends, about 8–10 × 40–60 m each, which reads as vehicle emplacements or dugouts. Round 1's "compound" (F1d) is the Euthymius monastery itself. The cluster is a modern military position built against the monastery ruin, not an unrecorded antiquity.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- D3C1209-200214F017 tile b (1 Dec 1974). The ring is at about px (10310–10390, 14555–14655). The pits are at x 10120–10290, y 14320–14490. The two-walled rectangular structure (round-1 "bars", F1c) is at (10510–10580, 14600–14650). The Euthymius ruin is at (10680, 14630). The zigzag trenches and the second loop are at x 10900–11400, y 14000–15100. Private crops: `private2/C1a/f017b_ring.png`, `f017b_ringz.png` (2×), `f017b_zz.png` (1.5×), `f017b_east.png`.
- F014 (25 Jun 1974): the same ring, pits and bars (round-1 windows). The trench bays do not resolve there.
- F1d = Euthymius: on F014 the compound falls on the 1940s 1:20,000 block "Kh. el Khan el Ahmar" once the local tie is applied (card 3). That block lies within about 50 m of ASI 109/4 site 68 (Khirbet el-Khan el-Aḥmar, 56 × 61 m monastery) and of OSM "מנזר אותימיוס" (31.79225 N, 35.33629 E). Overlay: `private2/C1a/mish2_blend.png`.
- Corrected distances (positions private): ring → Euthymius 335 m (W, slightly N); ring → nearest WBADB record other than Euthymius (WBS:3165 = ASI 109/4/67) 530 m. R4's "18 WBADB records within 1.5 km" stands, but after the 290 m correction none is closer than Euthymius.
- Today (Esri): the ring, pits and bars are under the industrial buildings of Mishor Adummim. May 1978 F007 shows the ground graded (round 1).
Literature check (queries run, result, tag): corpus `pdf-search "Mishor Adummim"`. ESI 7–8 p. 121 (the 1987 Euthymius season; Meimaris's excavations 1976–78) says nothing about military works. Repo and `branch_only` grep for "Qasr el-Khan", "Mishor Adum", "zigzag", "trench" near Euthymius: none. Web: "Khan el-Ahmar Euthymius monastery army camp 1970s military trenches Mishor Adumim before industrial zone" found Wikipedia, CMHL, BibleWalks and the Malta 2014 thesis; none mentions a trench system at the monastery. Tag: **NEW TO THE PROJECT** (the military reading and the corrected geometry). I did not search Hebrew sources or IDF histories, so I do not claim NEW TO THE LITERATURE.
Why it might matter: (1) It closes C1a-1. The ring should not be carried as a candidate lost antiquity. (2) Traversed trenches and emplacements were dug within 100–400 m of a major Byzantine monastery before its 1976–79 excavations. That is a disturbance horizon that excavators of the outer monastery area (and of the destroyed Qasr el-Khan; card 2) may need. (3) For all lanes it shows what military earthworks look like on HEXAGON at 1 m: closed beaded rings and rectangular pits. These are the shapes most easily mistaken for enclosures.
How to confirm or kill it (with data in hand, or what is missing): (a) Who dug it and when, Jordanian (1948–67) or IDF (1967–74)? CORONA 26 Sep 1967 DF041 tile d covers the area (the Jerusalem–Jericho road is at x 11800–14600, y 4900–6950), but the frame is too soft at this spot to find an 80 m ring (dead end). The RAF 1:15,000 prints or an IDF/Mandate military map would settle it. (b) Kill condition: an excavation report or air photo that shows the ring as an ancient wall. Its crenellated trench rim with spoil on the inside argues against that.
Confidence: medium-high that it is a military trench work; high for the corrected position and for F1d = Euthymius
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): "Qasr el-Khan" is in two places: the 1940s 1:20,000 sheet prints the ruin 330 m SSE of where IAA ASI Map 109/4 site 67 (and WBADB WBS:3165) puts it, and the ASI point sits on the Mandate trig point 881T
Lane: C1a
Round-1 link: new (it comes from following R4's "read Sion 1994" request for C1a-1)
What is odd (2–4 sentences): Hirschfeld 1992 (p. 278 n. 37, citing Chitty 1932 p. 198) treats Qasr el-Khan as an outlying tower of the Euthymius monastery. He says it is "completely destroyed", appears on British Mandate maps, and has no descriptive source. IAA ASI 109/4 site 67 "Qasr el-Khan" is a Roman sherd-and-stone scatter, 30 × 30 m, "elevation 252 m (Trig. Point)", on a hilltop. Its point lies about 55 m from the Mandate trig point "881T 251.7", which is the source of the 252. The Mandate sheet's own ruin symbol "Qasr el Khān" (R. with a building) is about 330 m SSE of that point, south of the metalled road and about 290 m NW of Euthymius. So the survey record carries the name, but its location and finds belong to the trig hill. WBADB repeats the ASI site as WBS:3165 "Site." (Rom, Sion 1994) and drops the name.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ASI 109/4/67: IAA online record 10171 (https://survey.iaa.org.il/#/MapSurvey/68/site/10171), cached in `scratch/D2/asi/GetPolygonsSites_Eng__MapId-68.json` (point 31.79735 N, 35.33314 E = PG 181643/133853). D2's `asi_elevation_vs_glo30.csv` row 109/4,67 shows the printed 252 against GLO-30 240.6 m at the point.
- WBADB WBS:3165: `branch_only/sandbox__methods/.../wbadb_sites.csv`, 181600/133900, "Site.", Rom, "Sion 1994". About 60 m from ASI 67, so it is the same record.
- Mandate 1:20,000 (palopenmaps `pal20k-1940s`, z16): "Δ881T 251·7" about 55 m S of the ASI point. The ruin "Qasr el Khān" is printed south of the metalled road. Map-to-OSM agreement at the Euthymius block is within 50 m. Overlays: `private2/C1a/qek_trig.png` (F014 | Mandate | Esri at both points), `mish2_blend.png`.
- Hirschfeld 1992: project read note `research/sources/full_reads_2026-10-12/hirschfeld1992/observations.csv` row H1992-057 (p. 278, PDF 302).
- F014 and Dec 1974 F017 at the Mandate ruin position: no standing structure resolves at 1 m. One ~10 m dark patch lies within 60 m (Dec74 F017 b about (10420, 14395)). The ground is now under factories. The ASI 67 point is graded open ground north of the zone road.
- Sion 1994 identified (R4's open request): the ASI 109/4/69 bibliography gives "Sion O. 1994. The Roman–Byzantine Period on the Wadi Qelt Survey Map. In Erlich Z.H. and Eshel Y. (eds.), *Judea and Samaria Research Studies*, Vol. 3, 1993, pp. 221–232". So WBADB's many bare "Site." rows near Mishor Adummim are ASI Map 109/4 sites. The paper is not in the corpus.
- Two smaller slips on the same pair of sites:
  - ESI 7–8 (1988) p. 121 prints Khan el-Ahmar (Euthymius) at "map ref. 134/183". The site is at 1819/1333 (ASI 68; WBADB), which gives 133/182, so the printed reference is about 1.2 km off.
  - IAA Reports 66 (Givati II, Early Islamic) p. 360 puts "Khan el-Aḥmar and Qasr el-Khan, east of Nebi Musa" (after Har-el 1978:555). Both lie about 9 km **west** of Nebi Musa, on the Jerusalem side.
- Summary table: `out2/C1a/qasr_el_khan_records.csv`.
Literature check (queries run, result, tag): web "Qasr el-Khan" Euthymius tower Chitty and "Qasr el-Khan" OR "Qasr al-Khan" Khan el-Ahmar Mishor Adummim tower destroyed. Results: CMHL Euthymius nodes (no tower, no coordinates), Wikipedia, BibleWalks. Nothing places Qasr el-Khan or notes the ASI/Mandate split. Corpus `pdf-search "Qasr el"`: only CIIP and Givati II. Repo: only the Hirschfeld read note and D2's elevation row, neither noticing the position. Chitty 1932 (PEFQS) is not in the corpus. Tag: **NEW TO THE LITERATURE** (the two positions and the trig-point attachment; provisional, because Sion's 1994 paper and Chitty 1932 were not read). The ESI and Givati slips: NEW TO THE LITERATURE (small).
Why it might matter: Anyone looking for the remains of Euthymius's outer tower will use the ASI/WBADB point, which is the trig hill 330 m from the ruin the Mandate sheet prints. "Roman pottery at Qasr el-Khan" in the survey literature may describe a different spot from Chitty's tower. The ASI "hilltop, Trig. Point" wording and the 252 m value tie the record to the trig, not to the ruin symbol.
How to confirm or kill it (with data in hand, or what is missing): (1) Read Chitty 1932 p. 198 for the tower's distance and bearing from the monastery. It is consistent with the Mandate symbol if it says about 300 m NW, and with ASI 67 if it says about 600 m NNW. (2) Read Sion 1994 pp. 225–228 (not held) for how site 67 was located. (3) Check May 1978 F007 at the Mandate symbol position to date its loss (not done). Kill: if Chitty's tower is at the trig hill, the Mandate symbol is the misplaced one, and the card turns into a Mandate-map error.
Confidence: high (the positions and the trig coincidence); low-medium (which position is Chitty's tower)
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): No single affine can register HEXAGON F014 between Jerusalem and Jericho (leave-one-out errors 290–970 m); at Mishor Adummim the round-1 3-point fix is 290 m off, so features must be tied locally, and a Mandate-map ink overlay does that to about ±40 m
Lane: C1a
Round-1 link: C1a-2 (E-run F014 affine about 2 km off at Jerusalem; 3-point fix), extended
What is odd (2–4 sentences): Round 1 supplied a 3-point exact affine and warned that it was about 300 m off at Nebi Samwil. Adding a fourth independent control (Euthymius, tied through the Mandate sheet, ASI 109/4/68 and OSM) and fitting by least squares leaves residuals of 43–145 m on the controls themselves. Leaving each control out in turn gives errors of 290 m (Euthymius), 346 m (Dome), 628 m (Tell es-Sultan) and 973 m (Atarot). The misfit is mostly in northing, as expected from a panoramic camera with no sensor model. Automatic matching still fails even when it starts within 300 m at full resolution. Gradient NCC peaks were 0.05–0.16 against Esri at 8 grid nodes and at Nebi Samwil, Tell el-Ful and Augusta Victoria, and 0.05–0.10 against the RAF 1940s layer at Mishor.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `out2/C1a/F014_4point_affine.json`, `out2/C1a/f014_affine_controls_loo.csv`. The Euthymius control is F014 mosaic (121850, 18666) ↔ 31.79225 N, 35.33629 E.
- Local tie at Mishor Adummim: a feature's true position = round-1 3-point position + (−57 m E, −284 m N). It was derived from three independent agreements: the Euthymius block, the Wadi el-Haud double-dashed track on the pale linear feature, and trig 881T. Trial-shift overlays: `private2/C1a/mish_blend.png` (0,0 / −64,317 / −150,0) and `mish2_blend.png`.
- Consequence for round 1: every round-1 private position of cluster F1 was about 290 m too far north (corrected in `private2/C1a/PRIVATE_LOCATIONS2.md`). Round 1's statement that the 1974 strips "appear on the 1940s RAF layer" therefore fails. The RAF strips round 1 picked lie about 260 m from the corrected 1974 pits, at the edge of an RAF frame seam, so they are different features or the RAF layer is offset there. Nothing in the cluster is shown to be older than 1948.
- The December 1974 epoch, which round 1 could not find: D3C1209-200214F017 tile b covers Jerusalem (west edge) to the Jericho oasis (top right, x 18000–22000, y 2500–5500) and the north Dead Sea (bottom right). It is sharper than June F014 at Mishor Adummim: the trench bays resolve on it (card 1). Tie: Euthymius at tile-b px (10680, 14630). Near Mishor, offsets in metres map almost 1:1 to pixels (east = +x, north = −y; checked on ring–monastery distances, ±60 m).
Literature check (queries run, result, tag): repo and `branch_only` grep for `fwd_mosaic_px_to_utm`, `F014_3point`, "leave-one-out" with HEXAGON: only round-1 C1a/C1b/C1c and R4. The E run's NOTE says no camera model was fitted. Tag: **NEW TO THE PROJECT** (a method limit with numbers and a working local procedure).
Why it might matter: The entry 24 frozen test needs "a registered HEXAGON F014 window" to reopen. This card shows that a frame-wide affine cannot deliver one to better than a few hundred metres. A window must be tied on the spot, for example to Mandate 1:20,000 ink (tracks, trig points, ruins), which survives where modern imagery has changed everything. Any lane that used the round-1 3-point fix away from its three controls should expect errors of 300 m.
How to confirm or kill it (with data in hand, or what is missing): Run `tools/p4.py` and `tools/blend.py` at any recorded monument inside F014 and compare the 4-point prediction with the observed position. Kill: a camera-model fit (optical-bar panoramic) that brings the leave-one-out errors under 50 m with 6–10 hand ties. Nobody has done that yet.
Confidence: high
Touches the Copper Scroll? maybe (method: it sets the error any F014-based observation at a scroll candidate must carry, e.g. entry 24)

---

## Dead ends

- Automatic NCC (gradient and intensity, ±330–450 m search, full resolution, 3-point prior): F014 vs Esri at an 8-node 3 km grid and at three Jerusalem landmarks, and F014 vs RAF 1940s at Mishor. Peaks were 0.05–0.16 with no margin. Dropped; ties must be picked by hand.
- Hand ties by eye in Jerusalem suburbs (Nebi Samwil, Tell el-Ful, Augusta Victoria) at 300 m windows: built-up change since 1974 is too large to pick a point inside the 300 m prior error with confidence. The Dome (−8, −3 m NCC) was the only clean urban check.
- CORONA 26 Sep 1967: north-up. DF042 tile d holds the north Dead Sea, and DF041 tile d holds Jericho (x about 18500–19500, y 2200–4000) and Jerusalem (left edge). The Jerusalem–Jericho road was traced at x 11800–14600, y 4900–6950, but the frame is too soft and noisy here to find the 80 m ring. It does not answer whether the trenches predate the June 1967 war.
- Dec 1974 F017 frame-wide control: a crop at tile b (0–2600, 15000–17600) shows dense city blocks, but the Haram did not appear in it, and the Jericho crop did not show Tell es-Sultan clearly. Only the Euthymius tie is reported.
- Sion 1994 sites on Dec 1974 F017 at their WBADB grids (Sites C, D, E, F, G, H, J and WBS:3165): at ±60 m nothing unambiguous shows at C, D, E, G or J. At Site H ("two rectangular enclosures, 15 × 40 m", no period) dark elongated pits like the card 1 emplacements lie 60–110 m NW of the grid. Whether Sion's Site H is a military pit group is an open question, not tested (crop `private2/C1a/sion_sites.png`).
- Hirschfeld 1992 full text through the Drive connector: the text returned (120 k characters) is cut off before the notes (the last pages reached are in chapter 8), so note 37 is cited from the project's read note, not re-read.

## Blocked inputs

- Chitty 1932 (PEFQS, p. 198) and Sion 1994 (JSRS 3, pp. 221–232): not in the corpus (repo grep, bucket `pdf-search`).
- Drive `1u17e90YE2vQOg4d6CgXeXbPO0V2mw8J7` (Hirschfeld 1992, 29 MB): `read_file_content` returned a cut-off text (120 k characters, ending in chapter 8) without the notes.
- `palopenmaps.org/tiles/pal20k-1940s` at z17: tiles absent (blank). z16 used.
- Nominatim found no OSM node for Tell en-Nasbeh, Tel Gibeon, St George's (Wadi Qelt) or the Good Samaritan Inn under those English names.
