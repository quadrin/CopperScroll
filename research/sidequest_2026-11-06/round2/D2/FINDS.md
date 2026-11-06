# Side-quest D2, round 2 (reuse the failed runs' tools; inventories as datasets): finds, 6 November 2026

Worker: lane D2, round 2. Round-1 family: `out/D2/` (cards D2-1 weakened, D2-2 and D2-3 survive; review R6). Two round-1 open items were taken up:
- **A2's registration method on another photo pair.** Round 1 did not try it. I applied A2's two-stage ECC registration (blurred silhouette first, then sign-free gradient magnitude; `register.py` on `claude/novel-2026-10-31-A2`) to two new pairings:
  - the USC Dec 1988 recto frames against EDF's after-treatment photographs of all 21 held segments;
  - the 1956 Manchester column photographs in DJD III vol. II against the 1988 frames.
  I then read EDF's own "recent break" records against the result.
- **R6's weakening of D2-1** ("regardless of slope" fails on slopes of 8° or more). It is tested on the 75 built-door units on flat ground that round 1 had dropped.

Private products are in `/home/claude/swarm/private2/D2/`: the crops and panels made from USC, EDF and DJD images, the registration JSONs and the scripts. Public data:
- `reg_1988_vs_edf_after.csv` (registration statistics per segment);
- `edf_recent_breaks_vs_1988.csv` (verdicts by zone);
- `flat_ground_doors.json` (counts and permutation tests only, no coordinates).

---

FIND CARD
Title (one line): The 1988 USC frames show that the "cassures récentes" EDF found on segments 5, 6 and 8 (code 3e, "recent break without matching fragment") were already there by Dec 1988. At segment 6, lower right, the pieces were still in place in 1988 and in Feb 1994. The open lacunae there first appear in EDF's after-treatment photograph, and EDF's text does not mention them.
Lane: D2
Round-1 link: A1d-2 (seg 15/16 pieces whole in 1988, separate in 1994; bracket Dec 1988–Dec 1993). This card dates a different set of EDF breaks with a third image epoch (EDF's Feb 1994 before-treatment plates), and it uses A2's registration, which round-1 D2 did not attempt.
What is odd (2–4 sentences):
- EDF's condition report codes breaks "3e: cassure récente sans fragment correspondant" (annex, EDF PDF p. 90) and gives no date. Its code table carries the note "incertitude sur datation de certaines cassures/lacunes" (PDF p. 85, seg 20).
- With the 1988 frames registered to EDF's photographs, the 3e zones on three segments can be bracketed:
  - Seg 8, bottom-right corner: the break outline EDF draws in orange (Pl. CXXIV) is already in the Dec 1988 frame, with the same concave shape, and it is unchanged in Feb 1994 and after treatment.
  - Seg 5: the upper lacunae along the central crack are already open in 1988.
  - Seg 6, lower right: EDF marks this zone with thick orange 3e lines (Pl. CXX). In 1988 and in the Feb 1994 photograph (Pl. XII) the zone is a crack network with every piece in place. In the after-treatment photograph (Pl. CLXXI) it has open lacunae, a triangle about 0.6 cm across and a slot about 0.8 × 1.7 cm. EDF's after-treatment drawing (Pl. CXXI) shows them as lacunae with a "fragments déplacés" arrow. Its seg 6 treatment text (PDF p. 70) lists only the acetonitrile bath that "a également défait les anciens collages" and "remontage des fragments".
- So "récente" in EDF covers breaks older than Dec 1988, at least on segments 5, 6 and 8. At segment 6 the material that is missing now went missing during the 1994–96 treatment, not before it.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- EDF 2006 = store doc `Brizemeure-Lacoudre-Puech-2006-Le-rouleau-de-cuivre-3Q15-STD-39ffb801` (copy B), PDF pages:
  - condition texts: pp. 69 (seg 5), 70 (seg 6), 71 (seg 8);
  - code table p. 85; annex definitions p. 90;
  - relevés avant/après: Pl. CXVIII (p. 410), CXX/CXXI (pp. 412–413), CXXIV (p. 416);
  - Feb 1994 before-treatment rectos: Pl. XI, XII, XIV (pp. 295, 296, 298; plate n+6 = seg n);
  - after-treatment avers: Pl. CLXX, CLXXI, CLXXIII (pp. 465, 466, 468; plate CLXV+n = seg n);
  - seg 6 radiographs: Pl. LXII–LXIII (pp. 352–353).
- USC: `usc:DSS_3Q15_CT5_RCT_T`, `CT6_RCT_T` (full-res box 1557 4175 2132 5144), `CT8_RCT_T`.
- Zone verdicts: `out2/D2/edf_recent_breaks_vs_1988.csv`. Registration: `out2/D2/reg_1988_vs_edf_after.csv`:
  - 10 of 21 segments register at silhouette ECC ≥ 0.94 with plausible scale; the gradient stage is weak (0.25–0.75).
- Panels (private): `private2/D2/crops/s6_bottom_88_94_96.png`, `te1.png`, `z1.png`, `rel_s6_avant_apres.png`. Scripts: `private2/D2/scripts/reg_loss.py`, `three_epoch.py`, `azoom.py`.
Literature check (queries run, result, tag):
- Web: "Copper Scroll 3Q15 condition change 1988 Zuckerman photographs compared EDF 1994 conservation fragments damage Amman". Hits: Wikipedia, the BAR sidebar on the conservation, EBAF news, catalogue records. None compares the epochs.
- Corpus: "cassure récente" occurs only in A1b, A1d, R8 and round-2 A1 (segments 15–16 and 18).
- Method 8 (`research/first_tests_2026-10-24/README.md`) registered 1988 against Feb 1994 for segs 4–6 to 0.12–0.19 mm. It recorded no state changes, and its DJD 1956 leg stopped.
- Tag: **NEW TO THE PROJECT**. The dating of EDF's 3e breaks to before Dec 1988, and the treatment-stage opening at seg 6, are **NEW TO THE LITERATURE (provisional)**: EDF does not compare its state with the 1988 photographs (as A1d already noted), and its text is silent on seg 6.
Why it might matter:
- EDF's code 3e is the only per-segment damage register of 3Q15. This card shows that it does not separate pre-1988 damage from damage at the time of treatment. A1d-2 (segs 15/16), R8's "16 D2 … 22/12/93" and this card together show three periods of loss: before Dec 1988; Dec 1988–Feb 1994; during treatment.
- Any reading of letters at the lower right of seg 6 should use the 1988 or Feb 1994 photographs, not the post-1996 object or its after-treatment photograph.
How to confirm or kill it (with data in hand, or what is missing):
- Confirm: read seg 6 at full resolution in all three epochs (the USC TIFF is held; EDF Pl. XII and CLXXI are in the store).
- Kill: the "lacunae" after treatment are only gaps from re-gluing pieces that are still present but not jointed ("collage non jointif"). The after-relevé would then show those pieces in place, and it shows lacunae.
- Extend: run the same three-epoch reading on every 3e zone of the other 18 segments. Pl. n+6 (Feb 1994) exists for all of them; the panels are cheap to make with `three_epoch.py`.
- Missing: the 1956 leg. The DJD III vol. II copy in Drive (`1GzRnplCiUtwZYLg_bAMSM4IJuCsSs6ZS`, 4.8 MB) holds the column photographs as 887 × 1223 JPX images under a 1-bit mask, about 2 px/mm. Seg 8's 4 cm keyhole lacuna cannot be found or ruled out there, so a 600 dpi scan is still needed (Method 8 reached the same conclusion).
Confidence: medium (1988 ≈ Feb 1994 at the three zones; seg 6 opening after treatment); low (that nothing changed 1988–1994 elsewhere on these segments).
Touches the Copper Scroll? maybe. It concerns the physical object: which image epoch to trust at broken edges (seg 6 lower right).

---

FIND CARD
Title (one line): On flat ground, where terrain cannot set the direction, ASI built-structure doors still avoid the west (6 of 62 against 15.5 expected) and point ESE. On slopes of 8° or more the W deficit disappears. The door preference is a compass habit that gives way to topography on steep ground.
Lane: D2
Round-1 link: D2-1 (R6: WEAKENED; "regardless of slope" fails because coupling to slope rises with gradient, and on slopes ≥ 8° the compass residual is not significant).
What is odd (2–4 sentences):
- Round 1 dropped all points on slopes under 3° (at the 200 m scale), and R6's critique applied to the units that remained. The 75 dropped built units, single-facing and deduplicated, are the one group in which no terrain null is needed: aspect there is undefined.
- Null: each unit's facing is rotated by a random multiple of 90°. This keeps the surveyors' cardinal/intercardinal rounding.
- Flat units: N 15 / E 27 / S 24 / W 9 against 18.75 each. W low p = 0.002, E high p = 0.016; resultant 0.28 toward 118°, p = 0.002.
- Same group after R6's cleaning (removing units whose text mentions a kiln, cave, tomb, burial, kokh, arcosolium, loculi or niche): n = 62; N 14.5 / E 22 / S 19.5 / W 6; W p = 0.0009, E p = 0.03; resultant 110°, p = 0.007.
- Gentle 3–8° (clean, n = 78): W 5 against 19.5, p < 10⁻⁴.
- Steep ≥ 8° (clean, n = 40): E 15.5 against 10 (p = 0.025), W 7 against 10 (p = 0.15); resultant 70°, p = 0.10.
- So the west avoidance is strongest where the ground is flat and weakest on steep slopes, where R6 showed doors partly follow the downslope.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `out2/D2/flat_ground_doors.json` (counts and tests for 4 slope classes × cleaned or not).
- Units: round-1 `private/D2/data/facing_units_full.csv` (subj = built, n_dirs = 1, no dup_of; slope `slp3` = GLO-30 plane fit over 7×7 cells), with each unit's ASI URL in `out/D2/facing_units.csv`.
- Script: `private2/D2/scripts/flat_doors.py` (20,000 permutations, seeds 20261106 / 7).
- 42 of the 62 clean flat units lie north of 31° N.
Literature check (queries run, result, tag):
- Web: "doorway orientation east ancient buildings Israel survey prevailing wind topography statistical test Byzantine field towers". Only Faust 2001 (*OJA* 20(2), https://cris.haifa.ac.il/en/publications/doorway-orientation-settlement-planning-and-cosmology-in-ancient-/) and its popular summaries (https://www.thetorah.com/article/houses-oriented-towards-god-in-the-east, https://www.biblicalarchaeology.org/daily/ancient-cultures/daily-life-and-practice/israelite-cosmology-iron-age-houses/).
- No study separates flat from sloping ground.
- Repo: no analysis beyond round-1 D2.
- Tag: **KNOWN BUT UNDER-DISCUSSED**. The E preference is published. The flat-ground test and the slope-dependent decay are new.
Why it might matter:
- It answers R6's objection with the cleanest subset: the preference is not a by-product of terrain, because it is strongest where there is no terrain to follow.
- The decay on steep slopes is what a practical habit would produce (sun, or shelter from the prevailing westerlies) that gives way to the ground. A rule held for its own sake (Faust's cosmology) would not decay that way. That is an inference, not a test.
- The base rate for an "east-facing door" clause in a survey record is high on flat ground (E or S in about two thirds of cases).
How to confirm or kill it (with data in hand, or what is missing):
- Kill: a hand-read of the 62 flat units that loses the W deficit. Or a reporting bias, for example surveyors noting E doors more often; this could be tested by comparing records that describe a structure but give no door.
- Wind or sun: compare the coast (strong westerlies) with the Negev and the Jordan Valley, on period-coded units (structure-level period from the ASI finds field). The current n is too small.
Confidence: medium (statistics robust to cleaning; extraction automatic, 24/25 in the round-1 audit).
Touches the Copper Scroll? no.

---

## Dead ends

- **Silhouette differencing after the A2 registration** (`reg_loss.py`, lost/gain maps). Segments 13, 16, 18, 19 and 20 came out with "lost bottom bands" of 1,200–2,200 mm². These are a registration artefact: the vertical scale of 1.35–1.42 differs from the 1.24–1.26 of the well-fitting segments, and the letter rows show the offset. Edges are also unreliable because viewpoint and curvature differ. Only local reading by eye of aligned crops gives usable verdicts. Do not reuse the lost/gain totals.
- **Registration failures:** segs 2, 4, 7, 12, 14, 15, 17, 21 and 23 (cc < 0.94 or scale 2–3.8). The mask picked up charts or stands, and two-light cuts (4, 17, 21) were among them. Seg 9 has no USC frame.
- **Feb 1994 before-treatment plates (Pl. n+6) as the target:** the grey background broke my green-object mask (scale about 5). Hand crops worked. A proper mask is the next step for the extension.
- **Automatic detection of EDF's orange "recent break" lines on the 28 relevé-avant plates:** colours change from plate to plate (seg 1 foliation is orange; segs 2–3 draw recent breaks in yellow; seg 6 draws adhesive tape in orange). The 216 detected blobs are not reliable (`private2/D2/data/orange_marks.csv`).
- **EDF code table (PDF p. 85):** the text layer gives 19–24 values per row for 26 code columns, so the 3e/3f columns cannot be aligned. The per-segment texts were used instead.
- **DJD III vol. II 1956 leg:** 1-bit-masked low-resolution plates and white montage gaps between strips. Holes such as CT7's mid-right holes do show, but seg 8's keyhole lacuna can be neither found nor excluded. Same conclusion as Method 8 (24 Oct).
- **Seg 8 keyhole lacuna:** its upper part is wider in 1988 than in Feb 1994. A lifted flap in 1988, or a piece re-seated before 1994? Not decidable here.
- **Seg 18 lower-left "cassure récente":** inconclusive because of the scale artefact. Round-2 A1 covers the seg 18 corner from the relevés.
- **`water.csv` dims against capacity_m3:** only 28 rows have both. Solomon's Pools (118 × 71 × ~10 m → c. 85,000 m³, etc.) and the Qumran pools agree with the published capacities, so there was no size-distribution oddity to report.
- **Caves (`caves_entry25/aspect.csv`) as an orientation dataset:** not run. D1 round 2 shows that 33 of the 48 plan-bearing ʿAtiqot 41 caves are coded "no facing", so any statistic on aspect.csv is biased toward caves described in words. Cliff faces are also below GLO-30 resolution (C3 round 1). The 32 plans would need hand measurement first.
- **H's character model on CIIP and ostraca:** unchanged from round 1 (no Aramaic, weak on names). Not retried.

## Blocked inputs

- A 600 dpi scan of DJD III *Planches* (Pls. XLIX–LXXI) is not in the corpus. The Drive copy `1GzRnplCiUtwZYLg_bAMSM4IJuCsSs6ZS` (4.8 MB) holds the column photographs at about 2 px/mm under a 1-bit mask, so the 1956 epoch cannot be used for loss dating.
- Nothing else is blocked. The store PDF of EDF copy B, the USC COGs and the round-1 D2 private data were all readable.
