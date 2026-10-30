# 3Q15 disputed letters on the WSRP 1988 full-resolution colour crops (30 Oct 2026)

> **Image use.** WSRP 1988, private study copy (USC/WSRP colour drum scans). No image, crop, preview or annotated figure is in this repository; frames are cited by file name (crop names such as `I12_CT3__CT3_RCB` refer to frame DSS_3Q15_CT3_RCB_T). All readings below are **exploratory, image-checked (single reader, not blind to the editions)**; they are not confirmatory evidence. Columns XI–XII (CT19–CT23) were hashed only and never viewed.

**Status: first-pass, single-reader, exploratory reading.** These are manuscript-image observations (USC/WSRP 1988 drum scans, recto), not edition-based. However, they do not meet the plan's freeze/blind-reader standard (§3 step 2):

- Before any pixel was read, the reader had already seen the competing readings for every line. They are in the crops_log "purpose" field and in `wsrp_locate.md`/`wsrp_plan.md`, which were read first.
- The III 11–13 observation was written after the edition readings for entry 14 had been printed.
- The IX 10 row assignment was revised after the readings had been read.

No result below is confirmatory evidence for any identification.

## Files

- Blind log: (session workspace, not retained; not in the repository). Each section is timestamped. The hash chain is in `blind_hashlog.txt` (the final sha256 is `7d209aed…b3a859c9c6`). Each edition lookup came after the section hash for that line, except where marked NOT BLIND.
- Comparison notes: (session workspace).
- Scripts:
  - (session workspace) verifies the sha256 of each download against crops_log.
  - (session workspace), `grid.py` and `enh.py` make the views.
  - (session workspace) makes the figures.
- Figures (18 annotated JPEGs): (session workspace, not retained; not in the repository).
- Crops: 50 of the 104 crops were downloaded. Every one matched its crops_log `png_sha256`. The list with full hashes is in (session workspace).

**Transforms (all lines).** For each view:
1. A sub-window is cut from the crop PNG.
2. The L channel of CIELAB gets CLAHE (clip 2.0, 8×8 tiles; a few early I 12 views used clip 3).
3. A few early I 12/II 3 views also got an unsharp mask (σ 2, amount 1). It amplified corrosion texture and was dropped.
4. The view is resampled with Lanczos at ×0.55–2.6.
5. Colour views are untransformed apart from the resampling.

No rotation, registration warping or channel arithmetic was applied. Coordinates below are crop-PNG pixels [x, y]. The text runs right to left.

**Grades:** certain / probable / possible / illegible.

---

## I 12 (entry 4): the letter(s) before ק in ניקרת / נקרת / מקרת

**Crops used:**

| Crop | sha256 (first 16) | Role |
|---|---|---|
| I12_CT3__CT3_RCB | c01c77962583ea70 | main |
| I12_CT3__CT3_RCT | c71fc1348e614463 | |
| I12_CT3__CT3_RLB | c1b8f686f87d78c3 | |
| I12_CT3__CT3_RLT | 030b082e27305544 | |
| I12_CT3__CT3_RRB | 815e58d483797baa | |
| I12_CT3__CT3_RRT | 4c316209b8d7612a | |
| I12_CT2__CT2_RLB / RLT / RRB / RRT | d2b93edb… / b35cfa11… / 36464dcc… / 5c70e01d… | join check |
| I12_CT4__CT4_RB / RT | 983ee79e… / f51fad71… | line end |

**Registration.** On CT3 RCB, the row at y≈620–720 reads, right to left: roofed letter, ו, ב, ש, ו/ל. This fits "…חו בשולי" of I 11, which was taken from the neighbouring-line text. So the row at y≈860–1010 is I 12 (probable).

**Blind observation (CT3 RCB, right to left from the CT3 right edge at x≈985):**

1. **x≈870–960: one closed square letter with a flat base** (probable). On RRB/RRT a thin vertical runs up its right side and rises above the box top. It cannot be told whether this is the box's own wall or a separate narrow letter.
2. x≈740–850: a V-shaped head with a stem on the left that descends below the line. ק, possible.
3. x≈610–720: a square body with a long vertical descending below the line. Possible.
4. x≈470–600: an arched head with a corrosion pit. ר/ד/ת type, possible.
5. x≈330–420: roofed. Probable roofed letter.
6. x≈200–290: box. Probable box.
7. x≈90–170: box. Possible.

**Edition comparison.** Reading 2–7 as ק-ר-ת-ה-ט-ב fits ...קרת הטביל(ה), which every edition shares.

- **Letter 1 is a single closed box.** This **supports one closed letter (Puech 2006 מקרת; Lefkovits m-)**. It **contradicts a short נ + small י occupying this space (Milik, Wolters, Schiffman ניקרת)**, at "probable" strength.
- Eshel's נקרת also has one letter before ק, but a נ in this hand is open on the left, and the box looks closed.
- Caveats:
  - The box stands against the CT2/CT3 saw cut, and I 12 was not registered on CT2's left edge, so a letter there (a י or the נ) is not excluded.
  - The thin vertical on the box's right is unexplained.
- ר or ד in letter 3 (Lefkovits mqdt/mqrt): undecidable.
- Puech 2015's ה in the lacuna: not reached. It lies at the CT3/CT4 join and was not registered.

**Not recorded by any edition:** the thin overshooting vertical on the right of the box (RRB/RRT).

**Verdict:** supports מקרת over ניקרת at "probable" strength, conditional on nothing standing on CT2's left edge. Lefkovits' ד/ר and Puech's ה are undecidable.

**Effect on the repo entry (proposal only):** add to `e4-immersion` a WSRP-image note: "CT3 shows one closed box before ק (probable); נ+י not seen; CT2 edge unchecked."

**Figures:** I12_a_CT3RCB.jpg, I12_b_CT3RRB.jpg, I12_c_CT3RRT.jpg.

## II 3–4 (entry 7): בית ה?ד? and ΘΕ/ΞΕ

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| II3-4_CT6__CT6_RCB | 2bfc99c0640ab6f7 |
| II3-4_CT6__CT6_RCT | 9756240aab46c976 |
| II3-4_CT6__CT6_RLB | 88351b8fdce40b77 |
| II3-4_CT6__CT6_RLT | f5488b1cfb8a0093 |
| II3-4_CT6__CT6_RRB | 8a0d4fbba7c03e9b |
| II3-4_CT6__CT6_RRT | daa28efcee8402fe |
| II3-4_CT5__CT5_RCB | 49a240bbb1f8efc5 |
| II3-4_CT5__CT5_RCT | ee55cdba57b73f3f |
| II3-4_CT5__CT5_RLB | 2e09094c5741bc60 |
| II3-4_CT5__CT5_RLT | 9cc77ca224fa9f0c |

**Blind observation.**
- On CT6, from the cut inwards:
  - A cut letter (roof plus a vertical at the edge): illegible.
  - Then two roofed letters of identical form: a full right leg and a shorter, inset left leg whose top stops just below the roof (RRB/RRT).
  - Then a vertical, then a צ/ע-type letter.
- On CT5's left edge: a box (ב/מ), an arched letter (ת?), a roofed letter with a full right leg, and a dark box against the cut.
- At the II 4 line end there is a **closed oval ring with a medial bar**, the same in RCB, RCT, RLB and RLT. Beside it, under red stain, a possible Ε.

**Edition comparison.**
- **4th letter ה:** weakly supported (possible). It has the same form as the agreed ה of הישן next to it. This tends against Wolters / the text shown ח, and is consistent with Puech's המדה and Milik's המרה.
- **1st letter (ה/ח):** undecidable.
- **3rd letter (ד/ר):** undecidable. Only a vertical and part of a roof survive at the CT6 saw cut. A letter may be lost or doubled across the CT5/CT6 join, which was not registered.
- **ΘΕ:** **supports Θ (Milik, Puech, Lefkovits); contradicts ΞΕ (Ullendorff, Muchowski)**, which would show three free bars with no enclosing ring. This agrees with the plate check.

**Verdict:** Θ supported. 4th letter ה possible. 1st and 3rd letters undecidable.

**Effect (proposal only):** in `e7-the`, add the WSRP confirmation of the ring with a bar in four lightings. In `e7-house`, record that the 4th letter is ה-like on the WSRP images, which agrees with plate round 2, and leave the rest open.

**Figures:** II3_a_CT6RRB.jpg, II3_b_CT6RCB_theta.jpg, II3_c_CT5RLB.jpg.

## III 1 (entry 12): the gap after בח

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| III1_CT7__CT7_RCB | 9acb7fd6ab27f69d |
| III1_CT7__CT7_RCT | 1f901aa48b045b2c |
| III1_CT7__CT7_RLB | 0965c6c285007da0 |
| III1_CT7__CT7_RLT | 894d8b550be980d4 |

**Blind observation.**
- The gap is a **loss of metal**: a black backdrop or mount material shows through. **There is nothing to read inside it (certain).**
- At the gap's left (line-end) edge there is one letter cut by the break: a left wall and a rounded base turning right. ט/מ/ס type, possible. ב/ל are not supported.
- To its left are roofed letters, which fit תחת.
- The right side of the gap (the line start) is too damaged to read.

**Edition comparison.**
- The image confirms rounds 2–3 ("metal missing, no traces").
- Nothing confirms either restoration: Puech's ש(ל) ]דיאט or Lefkovits' נב]ט.
- The edge letter fits the final ט that both restorations need (possible). So the image cannot choose between them. Milik's "no letters" restoration is unaffected.

**Verdict:** undecidable between the restorations. The edge letter is weakly ט-compatible.

**Effect (proposal only):** in `e12-court`, note that the gap is a loss of metal on WSRP and that the edge letter is ט-like (possible). Keep ◦◦◦.

**Figures:** III1_a_CT7RLB.jpg, III1_b_CT7RCB.jpg.

## III 8 (entry 13): שבמל[ה/ח](ם)

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| III8_CT7__CT7_RCB | 8a26c69e04c8d96c |
| III8_CT7__CT7_RCT | b732d1d7a3faae7a |
| III8_CT7__CT7_RLB | edbeecdc7af8dc54 |
| III8_CT7__CT7_RLT | ad8500c93b586b18 |
| III8_CT8__CT8_RCB | 5afb5e3ed23c8e76 |
| III8_CT8__CT8_RCT | 60d9c1f75b2bb889 |
| III8_CT8__CT8_RLB | 14f9e4ef8c5f1b3e |
| III8_CT8__CT8_RLT | 4d1a1f1682672a4c |
| III8_CT8__CT8_RRB | bc2367c15abc8314 |
| III8_CT8__CT8_RRT | 28b543ecefb1d835 |

**Registration.** The III 7 Greek pair sits at CT7 RCB (530–700, 380–520). The CT8 row below it ends in X-shaped signs, which fits the ביאתא of III 9.

**Blind observation.**
- **On CT7**, the mid-line zone where the disputed word should stand is heavily corroded in all four lightings. I see a diagonal (ש/ל type) and, near CT7's left edge, a roofed letter plus a diagonal. The ה/ח left-leg gap is not resolved, and no closed ם can be seen.
- **On CT8**, the end of III 8 shows, right to left:
  - box, box;
  - a blister;
  - a head with an inner stroke (פ?);
  - two separate verticals;
  - a closed rectangle at the line end (final-ם-like, possible to probable).

**Edition comparison.**
- The CT8 row end should be בצפונו. The closed box at the very end is unexpected for a final ו. Either my row assignment is off by one, or the last letters are written close together. Unresolved.
- The disputed word itself: **undecidable** for ה/ח and for the final ם. It neither supports nor contradicts Puech 2015 שבמלה, Milik/Puech 2006 מלח, or the text-shown extra מ.

**Not recorded by any edition:** a closed box at the end of the CT8 row (if the row is III 8). This needs a line-registration check before it means anything.

**Effect (proposal only):** none to the reading. Add "WSRP CT7: word zone corroded, undecidable" to `e13-millo`.

**Figures:** III8_a_CT8RCB.jpg, III8_b_CT7RCB.jpg.

## III 11–13 (entry 14): NOT BLIND

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| III11-13_CT7__CT7_RCB | 2a480f552a1ebe06 |
| III11-13_CT8__CT8_RCB | e38ca6fcbbe07720 |
| III11-13_CT8__CT8_RLB | 2cd5fa5e30811171 |

The other lightings were not downloaded.

**Observation (exploratory).**
- **III 11**, the word under the blister: the zone is blistered with a chain of corrosion nodules. **Illegible.**
- **End of III 12 (CT8):** a closed box (מ, possible), then a through-hole.
- **Start of III 13 (CT7 right edge):** a letter with a roof, a right vertical and a left leg ending in a foot. ת, possible. ד is less likely because ד has no left leg.
- **Numeral zone of III 13 (CT8):** corroded. **Illegible.**

**Edition comparison.**
- (a) ה/ח + ם at III 11: undecidable.
- (b) The ת-like start of III 13 weakly favours **המ|ת (Milik 1960, Lefkovits, the text shown)** over **מ|דף (Milik 1962, Puech 2006/2015)**. This is non-blind, from one lighting only, with registration uncertain by ±1 line.
- (c) 13 or 14: undecidable.

**Effect (proposal only):** none until the line is re-read blind in all six lightings.

**Figures:** III12_a_CT8RCB.jpg, III13_b_CT7RCB.jpg.

## V 1–9 (entries 21–23)

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| V1-4_CT10__CT10_RCB | 68edea18ef8bf874 |
| V5-9_CT10__CT10_RCB | ec144e1daca8921b |

CT11 and the other CT10 lightings were not downloaded.

**Blind observation.**
- In the upper left half of CT10 there is a band of fine oblique striations with no engraved strokes (V1-4 crop, x≈330–580, y≈380–620). It may be the smooth lacuna or abraded letters.
- Lower rows carry red-stained letters, including roofed and box letters.
- No line registration was made against the text.

**Edition comparison.**
- The V 1–2 link word is a restoration in every edition. No trace supports ש[במערב], [הבאה ל], ש[ב] or של גי ה. The image is consistent with round 2's "no traces".
- V 8/9 שלומ|ו עד against שלום | ועד: not assessed.

**Verdict:** undecidable.

**Effect:** none.

**Figure:** V12_a_CT10RCB.jpg.

## IX 7 (entry 40): ים / דרום

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| IX7_CT17__CT17_RT | 3d782937ab5f0e6d |
| IX7_CT17__CT17_RB | b715a1f2c7aaf115 |
| IX7_CT16__CT16_RCB | e78c911217c646d3 |

**Blind observation.**
- On CT17 there is a **closed final-ם-like box** (probable) at RT (560–660, 410–510) and RB (490–600, 270–420).
- Between the box and the serrated saw cut lie about 1.5–2 letter widths of crusted, corroded surface. In that space there is **at most one vertical-like trace** (RT x≈860–880, possible), and **no ד/ר roof or head stroke** is seen.
- The CT16 left edge was not registered to IX 7.

**Edition comparison.**
- The image **leans to ים (Milik, Lefkovits)**: ם plus a possible single vertical.
- It **does not exclude דרום (Puech 2006)**, because of the corrosion and the unknown width of strip lost at the saw cut. Puech's ד and ר could have stood on CT16's left edge, which was not registered.
- This agrees with the plate check (Q14) and adds nothing decisive.

**Effect (proposal only):** add to `e40-direction`: "WSRP CT17 RT/RB: closed ם, ≤1 vertical before it, no ד/ר stroke seen; leans ים; saw-cut loss unquantified."

**Figures:** IX7_a_CT17RT.jpg, IX7_b_CT17RB.jpg.

## IX 10 (entry 41): בקומעה

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| IX10_CT16__CT16_RCB | b302eaf8e5f0b896 |
| IX10_CT16__CT16_RCT | 5690695062e94ac5 |
| IX10_CT16__CT16_RRB | 037628a25d1901bc |
| IX10_CT16__CT16_RRT | 88ddebc2bfd59fb5 |

**Blind observation.** I read the long row at RCB y≈380–520 as: ב, ק, ו, a diagonal plus a small vertical, a roofed letter, a box, a box. At the time I could not decide whether it was IX 10 or IX 11.

**After reading the text (not blind).** The sequence fits **IX 11 בקול המים** (ב-ק-ו-ל-ה-מ…). So this row is IX 11, not IX 10. This is a **registration finding**: both lines start ב-ק-ו, and the "extra vertical" seen here belongs to IX 11's ל. Anyone reading this frame must not take this row for IX 10.

The probable IX 10 is the upper row (RCB y≈80–300). It shows a ב at the right edge, then a ק-like letter and a vertical. Where the box (מ/ב) and ע should stand, the surface is striated corrosion with a crack through it. There is a possible closed box at RCB (1270–1330, 100–180).

**Verdict:** undecidable. There is a weak, non-blind lean to a closed box (Puech 2015 קומעה), as in plate round 2.

**Effect (proposal only):** add a caution to `e41-qomaah`: "on CT16 frames IX 11 (בקול) begins with the same ב-ק-ו; plate observations of an 'extra vertical' should be checked against IX 11."

**Figures:** IX10_a_CT16RCB.jpg, IX10_b_CT16RCT.jpg.

## X 15–16 (entry 49): the letter after ש-ל

**Crops used:**

| Crop | sha256 (first 16) |
|---|---|
| X15_CT18__CT18_RCB | 3d3748d96756fe6e |
| X15_CT18__CT18_RCT | 96352a081888b20b |

The flange-adjacent RLB/RLT/RRB/RRT crops and CT17 were not used.

**Blind observation.**
- Five rows were seen:
  - row a;
  - row b, four identical tall signs with closed rounded heads;
  - row c, which ends at the left in a roof bar with three hanging verticals;
  - row d, two box letters;
  - row e, an א-like sign.
- The bottom right is broken away.
- I could not isolate a ש-ל-? group.

**Edition comparison.**
- A tentative fit: row d = the ככ that ends X 16, and row e = ארבעת in X 17, which would make row c the end of X 15 (…רחיל תחת). This is not secure.
- No head-bar ר and no cursive waw was identified at a registered position.

**Verdict:** undecidable. Nothing for or against Siloam (Puech, Milik), Rachel (Lurie, Beyer, Wolters) or Jehu (Lefkovits).

**Effect:** none.

**Figure:** X15_a_CT18RCT.jpg.

---

## Summary of verdicts

| Line | Verdict |
|---|---|
| I 12 | One closed box before ק: supports מקרת (Puech 2006) / Lefkovits m- over ניקרת (probable); CT2 edge unchecked |
| II 3–4 | Θ supported, Ξ contradicted; 4th letter ה-like (possible); 1st and 3rd letters undecidable |
| III 1 | Metal loss with no traces (certain); edge letter ט-like (possible); restorations undecidable |
| III 8 | Undecidable (corrosion) |
| III 11–13 | III 11 illegible; ת-like start of III 13 weakly favours המ\|ת (non-blind); sum illegible |
| V 1–9 | Undecidable |
| IX 7 | Leans to ים; דרום not excluded |
| IX 10 | Undecidable; registration hazard with IX 11 found |
| X 15–16 | Undecidable |

**Next steps:**
- A truly blind second reader, with the candidate readings withheld, for I 12 and IX 7.
- Register I 12 on CT2's left edge and IX 7 on CT16's left edge.
- Download the remaining lightings for III 11–13, V (CT11) and X 15 (RLB/RLT and CT17).

## Exposure log

- **Drive, read:**
  - The listing of `crops/` (names and IDs).
  - 50 crop PNGs, one call per file ID, each verified against the crops_log sha256.
  - The local copy of crops_log.
- **Drive, written:** nothing.
- **Held material:** no CT19–CT23 file was named, requested or opened.
  - The CT16 RCB/RRB/RRT frames show out-of-focus curled flanges at the left. These were not examined. Per the locating note, CT16's neighbours (CT15/CT17) are not held.
  - The CT18 crops are clipped to the flat strip. No flange was examined.
- **Repo** (`the repository (read-only)`, read only):
  - AGENTS.md.
  - `data/scroll-text.js`, columns I–III and IX–X, lines named above. For column V only the line count was read.
  - `text/readings.json`, entries 4, 7, 12/12a, 13, 14, 21–23, 40, 41 and 49 only.
  - No grep was run. `research/preregistration/` was not opened. No XII 10, Yanun or Janoaḥ material was opened.
- **Claude project:** not read, not written.
- **Repo:** not written; no commit or push.

## Integrator note (main session, 30 Oct 2026)
- The main session viewed the annotated figures for I 12 (CT3 RCB, CLAHE) and II 4 (CT6 RCB, CLAHE).
  - II 4: a closed ring with a horizontal bar across its middle is visible, consistent with Θ.
  - I 12: a closed, box-like letter before ק is visible.
  - Both agree with the agent's grades ("probable" for I 12, Θ supported for II 4).
- All results are EXPLORATORY. The candidate readings were known before reading, and III 11–13 and the IX 10 row were examined after the editions had been opened.
- Blind observation log: `wsrp_letters/observations_blind.md`, with hashes in `blind_hashlog.txt`, in the 29 Oct session workspace. The 18 annotated JPEGs are in `out/wsrp_letters_figs/` there. The workspace is not permanent; rerunning the crops notebook can regenerate the source crops.
- Follow-ups: download and read CT11 for V 1–9; register the CT2 left edge for I 12; re-check plate readings of IX 10 against IX 11.
- Repo changes are proposed only; none has been applied.
