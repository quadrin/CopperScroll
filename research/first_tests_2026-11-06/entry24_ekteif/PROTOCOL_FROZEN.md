# Entry 24 and Mughâret Ekteif: frozen protocol (6 November 2026)

Written by Claude for the owner's request "Do #2 and #3 now" (6 Nov 2026), item #2. Rules: [AGENTS.md](../../../AGENTS.md), section "Tests that can fail". This file is committed, with its SHA-256 in the commit message, **before** any reserved observation is opened.

## 1. Question and stopping point

- **Question.** Does the stepped, sloping rock-cut excavation that the Survey of Western Palestine (SWP) calls Mughâret Ekteif (Memoirs III, 1883, p. 220) survive as a visible cut at the place where SWP sheet XVIII prints the label "Mght. Ekteif"? And can it be the "tomb in the Kippa ravine, on the way from Jericho to Secacah" of entry 24 (column V, lines 12–14)?
- **Conclusion that could change.** The project holds this feature only at SWP-square level (`features_zone_unresolved.csv`, row SWP3-220-mugharet-ekteif, "zone unresolved"). The entry 24 rating asks for "a dated record of the stepped chamber". A visible cut at a known point gives a field target. A clear absence where similar features are visible narrows the claim to "subterranean or destroyed".
- **Evidence now.** SWP text (p. 220) and sheet XVIII; Mandate 1:20,000 sheet 19-13 (no cave symbol); side-quest card C2-1 (6 Nov) gives the sheet position (±250 m), which is held privately. No survey since 1873 records the feature. Bar-Adon 1972 sites 80–83 (ASI 1 pp. 117–119) are already EXPOSED (held-area screen of 29 Oct).
- **Deliverable and stop.** One blind reading of modern (and, if registrable, 1974) satellite windows, scored once under the rules below. Then a result file with one of the three AGENTS outcomes for each claim. No further sourcing in this pass.

## 2. Text basis (edition-based, not checked on the manuscript for this test)

- V 12: בקבר שבנחל הכפא "in the tomb that is in the ravine of the Kippa". Milik (DJD III, D12, p. 264) and Puech (2015, p. 59) place it in Wadi Kuteif / Ekteif. The meaning of Kippa ("rock" or "vault/cavern") is disputed.
- V 13: בביאה מירחו לסככא "on the way in from Jericho to Secacah" (Puech: "certain"; Milik, Beyer, Lefkovits agree). Allegro 1960 reads no Jericho ("the eastern entrance"; via Puech 2015 p. 59 n. 232).
- V 14: "dig seven cubits: 32 talents". No observation available here can test the depth.
- Retained text branches: **T1** = Jericho→Secacah route (majority reading); **T2** = Allegro (no route clause).

## 3. Claim A: the feature is visible at the sheet position (branch-level position claim)

**Claim A.** On imagery, inside a circle of 300 m radius round the private C2 point (pick uncertainty 250 m plus tile registration about 50–100 m), there is a straight cut feature of the size the SWP describes ("slopes downward at a gradient about 1 by 2 for 120 feet", with cut steps).

**Registered alternatives.** (a1) The excavation is roofed or choked and is not visible from above. (a2) It was destroyed (road works, quarrying, military works). (a3) The SWP label is more than 300 m from the feature.

**Window centre.** The private point in `center_PRIVATE.json` (outside the repo). SHA-256 of that file: `d4ad1b49e5f11cfea5eb4ceaaeeebd01bcbea640f95b4a3008f45ae20eeb9548`. The point is not published, because the feature is unrecorded and unprotected.

**Windows.** Each window is 600 m × 600 m, north up, UTM 36N, 0.5 m per pixel (1200 × 1200 px).
- **T (target):** centred on the private point.
- **C1–C8 (controls):** centres 1.5 km from the target at bearings 0°, 45°, 90°, 135°, 180°, 225°, 270° and 315°. They are placed by this rule only; nothing was viewed to choose them. They give the base rate of features that meet the criterion in the same desert terrain.
- **P (positive control):** centred on Kh. Qumran (Pleiades 688011; 31.74183 N, 35.45941 E), where an open rock-cut aqueduct channel and large stepped, cut installations are known. It tests whether the reader can see cut features of this size on this imagery.

**Epochs.**
- **E1 (required):** Esri World Imagery, zoom 18 (the maximum here; C1b found that z19 has no data near Jericho).
- **E2 (optional):** HEXAGON KH-9, 25 June 1974, the F015 tile that covers the target. It is used only if a registration reaches RMS ≤ 60 m on at least 3 check points that are all more than 2 km from the target, and if the registration work uses only overviews at 8 m per pixel or coarser near the target. If not, E2 is left out and the omission is recorded. All 10 windows are then cut from E2 by the same rule as E1.

**Blind reading.** A separate agent (the reader) gets the windows with neutral names (W01–W10 per epoch). The order is shuffled with a seed equal to the first 8 hex digits of this file's SHA-256, read as an integer. The reader is told nothing about the scroll, the hypothesis, the place or which window is the target. The reader must not search the web or any repository. For each window and epoch, the reader records:
1. Usability: `usable`, `partly usable` or `unusable` (cloud, blur, saturation), and the fraction of the central circle (radius 300 m = 600 px) that is built over, paved, cultivated or freshly disturbed (0, <25 %, 25–50 %, >50 %).
2. The main drainage line(s) in the window, as pixel polylines.
3. Every **qualifying feature**: a straight or nearly straight linear feature 15–60 m long (30–120 px) and 1–6 m wide, with roughly parallel edges, that ends at both ends and is not part of a road, track, wall, terrace, field edge or channel that continues beyond it, and is not a natural gully (a gully branches, narrows toward its head or follows the drainage). For each feature: the two end points in pixels and a grade, `probable` or `possible`.

The reader's output file is hashed and recorded before unblinding. Only `probable` features count in the scoring.

**Scoring (mechanical, after unblinding).** A window is **positive** if, on any available epoch, it has at least one probable feature whose midpoint is within 600 px (300 m) of the window centre. A window is **eligible** if on at least one epoch it is `usable` or `partly usable` and its central circle is ≤ 50 % built over or disturbed. Let c = the number of eligible positive controls among C1–C8, and n = the number of eligible controls.

**Decision rule for Claim A (in this order).**
1. **Not identifiable from available evidence** if P is not positive (the method does not show known cut features), or T is not eligible, or n < 6, or c ≥ 3.
2. **Supported relative to the registered alternatives** if T is positive, c ≤ 2, and at least one probable feature in T lies on the north side of the reader's main drainage line (SWP: "in the north side of the valley"). If the reader marked no drainage line in T, this condition is unknown and the result is not identifiable.
3. **Rejected** (for the version "a visible open cut within 300 m") if T is not positive and c ≤ 2. This does not reject the existence of the excavation: alternatives a1–a3 survive.
4. If T is positive with c ≤ 2 but all of T's probable features are on the south side of the drainage line, the result is **rejected**.

**Registered unseen prediction (P1).** T is positive and the qualifying feature is on the north side of the drainage line, with c ≤ 2. Success is outcome 2 above; failure is outcome 3 or 4.

## 4. Claim B: Mughâret Ekteif is the entry 24 tomb

**Candidates and controls (fixed now).** The tombs lane, branch 24-J (`research/regional/tombs/README.md`, 11–12 Oct), already scored tombs in wadis on the Jericho→Secacah approach: Jericho Hills F and G (F4, F7 strictly dated to the window), ʿAqabat Jabr South ASI 109/5/62 (lenient), St George / Choziba (any date), ASI 109/7/19 (Wadi Khashna mounds, "graves?") and WBADB E508 (Wadi Ekteif pit graves, Early Islamic). Status-unknown alternatives: any unrecorded chamber in the same wadis. These are the registered alternatives. No new inventory is built in this pass.

**Route component (exploratory: all positions are already exposed).** Corridor = 3 km on each side of the straight line (the 24-J rule) from each Jericho origin {Tell es-Sultan 31.8717 N 35.4446 E; Tulul Abu el-ʿAlayiq 31.85187 N 35.43624 E} to each Secacah branch {Kh. Qumran 31.74183 N 35.45941 E; Kh. Abu Ṭabaq WBS:3867 31.742661 N 35.41281 E; Karm es-Samra / el-ʿAjaz WBS:4115 31.716811 N 35.391652 E; Kh. el-Maqari WBS:4167 31.69942 N 35.38149 E}. The distance from the private point to each line is computed and reported as in or out.

**Decision rule for Claim B.**
- **Supported** needs discrimination against the controls on kind (a tomb) and date (window), plus P1 success. No available observation gives the kind or the date of the excavation, and the controls include window-dated tombs. **So Claim B cannot be supported by this test, whatever P1 shows.** This is stated before the reading.
- **Rejected** needs a contradiction across all retained branches. Branch T2 (Allegro) has no route clause, so the route component cannot reject Claim B. A rejection would need evidence that the excavation is not a tomb or is not of the window, and no such evidence is available.
- **Therefore Claim B closes as "not identifiable from available evidence".** Reopening condition: a dated plan or finds from the excavation (field visit, or an unread survey file that records it), or a new reading of V 12–13.

## 5. Exposure audit (done before freezing)

- **This coordinator** has not opened any imagery or map at the target or control centres. The private point was read from the C2 CSV.
- **C2 (6 Nov)** viewed SWP sheet XVIII and Mandate 1:20,000 sheet 19-13 at a 2 km × 1.6 km window round the target (maps only; no imagery). These maps are EXPOSED and were used only to set the window centre and the side of the valley.
- **Other side-quest lanes.** A search of every tile URL logged by the swarm found no Esri, 1940s-aerial or HEXAGON tile within 900 m of the target. C1b's 1945/Esri windows are 4–8 km north. C1c's Esri strip (z15, 4 m per pixel) ends at 31.785 N, about 1.4 km south; it includes parts of the southern control windows C4–C6 at 4 m per pixel only. The 1945 Great Britain Army mosaic in the store does not reach the target.
- **Project main.** The HEXAGON method test (23–24 Oct) looked at Qumran (window P). No main-branch file gives the target position.
- **Owner and atlas users.** Not auditable. If the owner has looked at the north side of lower Wadi Ekteif on any imagery, he should say so; the result would then be marked as possibly exposed.
- **Held area.** The target and controls C1–C8 lie in held area H1 of the owner's 25 October rule (E ≥ 189.0, N 130.5–152.0, old Palestine grid). This test uses that imagery as its reserved observation. After this test, the ten windows are **EXPOSED** for any later test.

## 6. What is published

Public: this protocol, the reader's scores (pixel positions in each 600 m window, which do not give a ground position without the private centre), the outcome and, for each route line, only "in" or "out" of the 3 km corridor (exact distances together could locate the point). Private (`/home/claude/swarm/private/E24/`, delivered as a download): the centre, the window images and any ground positions.
