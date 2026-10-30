# WSRP 1988 3Q15 crops: follow-ups on V 1–9, I 12 on CT2, and IX 10 vs IX 11 (30 Oct 2026)

> **Image use.** WSRP 1988, private study copy (USC/WSRP colour drum scans). No image, crop, preview or annotated figure is in this repository; frames are cited by file name (crop names such as `I12_CT3__CT3_RCB` refer to frame DSS_3Q15_CT3_RCB_T). All readings below are **exploratory, image-checked (single reader, not blind to the editions)**; they are not confirmatory evidence. Columns XI–XII (CT19–CT23) were hashed only and never viewed.

**Status: EXPLORATORY, single reader.** The reader knew the competing readings from the crop "purpose" fields and the 29–30 Oct report before any pixel was read. Only the CT11 (column V) observation was logged before the edition text was opened in this session. The I 12 (CT2) and IX 10/11 work is non-blind. Nothing here is confirmatory evidence for any reading or identification.

## Files
- Blind/working log: (session workspace, not retained; not in the repository).
  - The hash chain is in (session workspace):
    - V section: `538a4687…bba20703`, 06:43:44Z, logged before the V text was opened.
    - Non-blind sections: `5cb7792d…f045bbcf`, 07:22:33Z.
- V comparison notes: (session workspace).
- Crop hashes: (session workspace) (full sha256).
- Scripts:
  - (session workspace) (grid views).
  - (session workspace) (figures).
  - (session workspace), which prints ETCBC text and refuses columns XI–XII.
- Figures (11 annotated JPEGs): (session workspace, not retained; not in the repository).

**Downloads.** Thirteen new crops came from Drive. Twelve were the CT11 V1-4/V5-9 crops in all six lightings, plus V5-9_CT10_RLB.
- Each was checked against the crops_log `png_sha256`; all were OK.
- After the integrator's note about moved cache files, all 63 local copies in `wsrp_letters/dl/` were re-hashed against crops_log. There were 0 mismatches.

**Transforms, all views.**
1. Cut a sub-window from the crop PNG.
2. Apply CLAHE (clip 2.0, 8×8 tiles) to the L channel of CIELAB.
3. Resample with Lanczos at ×0.4–2.2. Colour views get no other change.
4. The CT11 RCB V1-4/V5-9 crops (both x 512–2036 full-res) and the CT10 RCB and CT16 RCB pairs were stitched on full-res y with no warping.
5. No rotation, registration warping or channel arithmetic was applied.

Coordinates are crop-PNG pixels [x, y], and the text runs right to left. Grades are certain / probable / possible / illegible.

---

## Task 1: Column V (V 1–9) on CT11 and the CT10/CT11 junction

**Crops used** (sha256, first 16 characters):

| Crop | V1-4_CT11 | V5-9_CT11 |
|---|---|---|
| RCB | 52fee03780b34649 | d2fd94d4f9e990b5 |
| RCT | 67ff2f8a4f70ae54 | 22dc2273373fc9ef |
| RLB | d509289d3c281663 | ef7ef789cdee3c77 |
| RLT | 102a11a9fd200d2d | 96c127b4377f849a |
| RRB | 3b06f4f9e437a88a | 293a0e04f142cd2a |
| RRT | e57da7320a60eb62 | d612be9b7ece47a9 |

Junction check: V1-4_CT10_RCB 68edea18ef8bf874, V5-9_CT10_RCB ec144e1daca8921b, V5-9_CT10_RLB ee4d9e65ea2d4b5d.

**Blind observation** (summary; the full letter-by-letter record is in `blind_log.md`).
- CT11 carries the left (line-end) parts of column V. Its left edge is broken in a step shape, with a wider loss at the top: on RCB, metal is missing left of x≈940 at row a, and left of x≈600–700 lower down.
- Nine inscribed rows (a–i) are visible.
- **Row d** (V1-4 RCB y≈1300–1480) is the only distinctive feature:
  - two boxes (x≈920–1260);
  - then a comb of parallel unit strokes with rounded tops and no roof or base (x≈600–860).
  - The comb shows ≥5 strokes (certain) and possibly 6. Its leftmost stroke stands at the break.
  - It appears in all six lightings. The stroke-ridge profile gives 6 maxima on RCB, 5 on RRB and 6 on RLB.
- **Row h, line-end side** (V5-9 RCB x≈40–700): corroded and blistered, illegible.
- **Row h, small red-brown outlined mark** (≈650–720, 1440–1540): it lies on the patina and is probably modern, not engraved.
- **Junction:** CT11's right edge is frayed. CT10's left side has a long crack and a detached plate. No letter could be followed across the cut, and the rows were not registered across it.

**Comparison** (non-blind, after the hash). The ETCBC text was used, with readings.json entries 21–23 and plate_check row V 9.

| Point | Observation vs editions | Verdict |
|---|---|---|
| Registration | Rows a–i = V 1–9 (probable). Row d = V 4 "…ש כסף ככ" + numeral. Row c starts its CT11 part with an א-type sign + box, which fits אמות (V 3). | Probable |
| V 1–2 link word (ש[במערב] Puech / [הבאה ל] Lefkovits-Beyer-Eshel / ש[ב] Milik / של גי ה text shown) | The word stands at the end of V 1. At row a, the metal is physically lost left of RCB x≈940. The lacuna is a **loss of metal**, not abraded letters (probable). No trace survives. | Undecidable. No restoration can be tested on WSRP |
| V 2 [האבן] | Line-end letters at x≈680–940 (a box at the break, a tall vertical) are not legible enough | Undecidable |
| V 3 depth (3, Puech; 3/5/6, Lefkovits) | The numeral word falls on lost metal at the left break | Undecidable. This confirms it is a restoration |
| V 4 sum (not in the brief; translation shown: 7) | ככ + ≥5 unit strokes, 6 possible, cut by the break | Compatible with 7 only if 1–2 strokes were lost at the break. Not decisive. **Not recorded by any edition note in the repo:** the stroke group runs into the broken edge |
| V 8/9 שלומ\|ו עד vs שלום \| ועד (Q41) | The V 8 line end (CT11 row h, left side) is corroded. On CT10, the V 9 line start sits at the crack/strip join (RCB x≈520–690) and is illegible in RCB and RLB | **Undecidable**, as in plate check Q41 |
| V 9 הרגם / הרגב | The word was not isolated with confidence | Undecidable |

**Proposed repo changes (proposals only).**
- `e21-link`: "WSRP 1988 CT11: the end of V 1 is lost metal (step-shaped break); no letter trace; restorations untestable on the metal images."
- `e21-depth`: "WSRP CT11: the V 3 depth word lies on lost metal."
- `e23-shallum`: "WSRP CT10/CT11: V 8 end corroded, V 9 start illegible at the CT10 crack; undecidable."
- Optional: the V 4 numeral note in the row above.

**New crops needed:** none for V on CT11; the six lightings cover the strip. If the V 9 start matters, cut CT10 RLT and RCT at the left edge as a band: CT10_RCT [908, 2600, 1500, 3300] and CT10_RLT [980, 2600, 1560, 3300]. These are uncropped lightings of the same zone; expect little gain.

## Task 2: I 12 on CT2's left edge

**Crops and previews used.**
- Crops: I12_CT2_RLB d2b93edbb28c49fa, RLT b35cfa11d31666a7, RRB 36464dccac94f917, RRT 5c70e01d56707a70, and I12_CT3_RCB c01c77962583ea70.
- q4 previews: CT2 RLB/RLT/RRB and CT3 RCB/RLB, the local copies from the locating pass.
- **Not blind:** I 9–13 were printed before the CT2 row was examined closely.

**Coverage.** The existing CT2 crops span the whole strip width. CT2 RLB's strip at q4 is x 268–484, which is full-res 1072–1936; the crop is 1060–1960. So the CT2 left edge at I 12 **is** in the crops, and no new crop is needed for coverage.

**Registration (inference, ±1 row).** I 12 lies at:
- CT2 RLB crop y≈650–860 (full-res y≈3930–4140);
- RLT y≈850–1010;
- RRB y≈840–1000;
- RRT y≈820–980.

**Reading of that row, right to left (RLB/RLT).**
1. A corroded line-start zone with a dark pit.
2. A closed box (probable).
3. Two V-shaped diagonal groups, ש-type (possible ×2).
4. A long left-leaning diagonal (ע possible).
5. The CT2 left-edge zone (RLB x≈40–250; RLT x≈80–330; RRB x≈60–250): a crusted surface, a curved crack and pits. **No letter can be isolated in any of the four lightings (illegible).**

This sequence fits **אמות שש ע[ד]** (I 12 begins "אמות שש עד"). On that reading, the ד of עד and possibly one more letter stood in the illegible edge zone of about 200 px (≈2 letter widths).

**Verdict.**
- The earlier CT3 "one closed box before ק" observation stands.
- **What stood at CT2's left edge is illegible.** One more letter (the נ of ניקרת/נקרת, or a י) could have stood there, or in the strip lost at the saw cut, and the images cannot exclude it.
- So the earlier verdict "supports מקרת at 'probable', conditional on CT2" **must be downgraded.** The CT3 image is compatible with מקרת (Puech 2006) / m- (Lefkovits). The images do not exclude נ/ני standing before it across the cut.
- Overall: undecidable, with a weak lean to one closed letter immediately before ק.

**Proposed repo change:** `e4-immersion`: "WSRP CT3: one closed box immediately before ק (probable). CT2 left edge at I 12 (after אמות שש ע-) is crusted and illegible in 4 lightings; a preceding נ/י across the cut is not excluded. Undecidable." This replaces the 30 Oct proposal.

**New crop boxes.** None are needed for coverage. To check the row count, one taller band would let I 9–13 line starts be counted from I 9 בתל:
- CT2_RLB [1060, 2300, 1960, 4400];
- CT2_RLT [976, 2400, 1956, 4600].

The CT2/CT3 saw-cut loss itself cannot be recovered from any crop.

## Task 3: IX 10 vs IX 11 on CT16

**Sources used.**
- Crops: IX10_CT16_RCB b302eaf8e5f0b896, RCT 5690695062e94ac5, RRB 037628a25d1901bc, RRT 88ddebc2bfd59fb5, and IX7_CT16_RCB e78c911217c646d3 (stitched rows above).
- DJD III plates volume (repo `research/assets/plans/djdIII1962/plates-volume.pdf`, sha256 b7a52c275ad42a33…). PDF p. 76 is pl. LXIV, the hand copy of col. IX; p. 77 is pl. LXV, the photograph of col. IX. Both were rendered at 300 dpi.
- Repo: `tables/plate_check.csv` IX rows, `research/text/plate_check.md` (round-2 table), `research/text/edition_confusions/variants.csv` V0439–V0459, and readings.json entries 40–43.
- **Not blind.**

**Row positions** (the earlier IX 11 finding is confirmed).
- Stitched CT16 RCB, full-res y; the IX 10 crop starts at y 2520 (IX7 crop 1720–2480, gap 2480–2520):

| Line | RCB crop y | Full-res y | Ends near |
|---|---|---|---|
| IX 10 | ≈80–300 | ≈2600–2820 | x≈1500 at right |
| IX 11 | ≈380–540 | ≈2900–3060 | |

- Short IX 9 (ככ + numerals): its line start lies in the corroded zone just above, at full-res y≈2440–2560, partly in the inter-crop gap. It was not resolved letter by letter.
- In RCT, IX 10 is at y≈240–440 and IX 11 at y≈540–700.
- Basis: IX 11's sequence ב-ק-ו-ל-ה-מ fits the lower row. IX 10's left half on CT16 shows ה, ע-type, a box (כ?) and a loop (ס?), which fit בקומעה כסף.

**Key observation.** One long vertical runs from IX 10 letter-top height down into the IX 11 row:
- at RCB x≈1260–1295, y≈110–400, and RCT x≈1290–1330, y≈240–560;
- seen in RCB, RCT and RRT (probable as one continuous stroke).

**Milik's hand copy (DJD III pl. LXIV)** draws the same feature: one long stroke from the ו-area of IX 10 down to IX 11, between ק and ל (figure IX_c). That stroke is the **ascender of IX 11's ל (בקול)**, which rises into the IX 10 row between its ו and its box letter.

**Consequences for published and project observations.**
- **Plate round 2's "second vertical with a knob (ו/ז) between ו and מ"** in IX 10 (P53; readings.json e41 "extra vertical … unresolved") is very probably this IX 11 lamed ascender, not an IX 10 letter. Grade: probable. It sits exactly where the WSRP stroke and Milik's copy put the ascender.
- The 30 Oct pass read the IX 11 row as IX 10 and saw an "extra vertical" beside a diagonal. That was IX 11's own ל, a different stroke from the one above.
- **Milik (hand copy):** he draws the stroke as continuous with IX 11 and does not count it as an IX 10 letter. There is no conflict.
- **Allegro / Luria (בקימעה):** a י/ו question at the same letter slot (variants V0439, V0443), not an extra letter. The ascender may have influenced a י reading; this is untested.
- **Puech (קומעה) and Lefkovits/Beyer/Pixner/GMT (קובעה):** neither reports an extra letter. Their dispute is ב vs מ at the box.
- **Wolters 1992 and the others' "כסף מנה חרם"** (V0447–V0453, with Puech's מנחה רב):
  - This word division concerns the far-left part of IX 10. On CT16 the IX 10 row shows only up to about כסף before the strip's left zone; מנה/מנחה would lie at the CT16 left edge (curled flange, not examined) or on CT17.
  - The IX 11 letters at that position (הקרובין לכפת) do not resemble מנה חרם. Row confusion is therefore an **unlikely** source for that division (inference).
  - Wolters is known here only via Puech and the repo's 2026-10-19 check; his own text was not reopened.
- No primary text of Milik, Allegro, Puech or Lefkovits commentary was opened in this pass; the statements above rest on the repo's variant table and plate-check records.

**Re-read of the true IX 10 disputed span (entry 41)** (CT16 RCB/RCT/RRB/RRT, non-blind):
- ב (probable);
- a ק-like head (possible);
- ו (possible);
- the lamed ascender from IX 11;
- a box zone (RCB x≈1060–1250) crossed by fine oblique striations and a crack; its top-right corner and base are visible, so a closed box is possible. The left wall is not resolved, so מ vs ב cannot be decided;
- ע-type diagonal (possible);
- ה (probable).

**Verdict:**
- The ב/מ letter is undecidable; there is a weak lean to a closed box, as in plate round 2.
- **The "extra vertical" is resolved as IX 11's ל ascender (probable).** This removes the unexplained letter and favours the five-letter word ב-ק-ו-[box]-ע-ה.

**Proposed repo changes (proposals only).**
- `e41-qomaah` note: replace "an extra vertical (ו/ז) between ו and מ is unresolved" with "the extra vertical is the ascender of IX 11's ל (בקול), which rises into IX 10. It is continuous across the rows on WSRP CT16 RCB/RCT/RRT and drawn so in Milik's DJD III pl. LXIV copy (exploratory, 30 Oct 2026)."
- In `tables/plate_check.csv`, R2-P53 comment: add the same note.
- e41-silver: no change.

**New crop boxes needed.**
- For כסף מנה חרם at the left end of IX 10, the CT17 right edge at IX 10–11 height is not in any crop: IX7_CT17 covers y 1680–2400 and X15_CT17 covers y 3120–4224.
  - CT17_RB [920, 2300, 1848, 3200];
  - CT17_RT [968, 2100, 1992, 3300].
  - RT's y offset is −200, as in the IX 7 boxes; check it with the q4 preview before cutting.
  - CT17 is not a held segment. Exclude any curled flange as before.
- To resolve IX 9's start: CT16 RCB [628, 2380, 2400, 2640], which closes the 2480–2520 gap.

---

## Summary

| Task | Result (exploratory) |
|---|---|
| V 1–9 (CT11) | V 1 link word and V 3 depth lie on lost metal (restorations untestable). V 4 ככ + ≥5 unit strokes (6 possible) at the break. V 8/9 division and הרגם/הרגב undecidable. No letter registration across the CT10/CT11 junction |
| I 12 on CT2 | Row registered as אמות שש ע[ד] (probable, non-blind). CT2 left edge illegible in 4 lightings. The earlier מקרת "probable" is downgraded to undecidable (weak lean). No new crop needed for coverage |
| IX 10 vs IX 11 | Rows confirmed (IX 10 upper, IX 11 lower). The plate-check "extra vertical" in IX 10 is IX 11's ל ascender (probable; WSRP + Milik pl. LXIV). ב/מ still undecidable (weak lean מ). מנה חרם needs a CT17 crop (box given) |

## Exposure log
- **Drive, read:** 13 crop PNGs, downloaded by file ID from `ids.json`: 12 CT11 V-crops and V5-9_CT10_RLB. No listing was made, crops_log was not re-read from Drive, and nothing was written.
- **Local (from earlier passes):** q4 previews of CT2, CT3 and CT16 (CT16 right half only); the local crops_log copy; earlier dl/ crops.
- **Held material:** no CT19–CT23 file was named, requested or opened. No column XI–XII image, plate or commentary was opened:
  - `pt.py` asserts columns 1–10;
  - the readings.json filter was entries 21–23 and 40–44, and IX lines only;
  - the plates PDF was rendered for pp. 76–77 only (col. IX).
- **Other exclusions:** no XII 10 material and nothing on Yanun/Janoaḥ; the repo grep excluded such terms. The curled flanges at the CT16 left edge and CT10/CT11 edges were not examined, and views were cropped to the flat strip.
- **Repo** (`the repository (read-only)`, read-only):
  - Read: AGENTS.md (head); `data/scroll-text.js` cols I, IV, V and IX (selected lines); `text/readings.json` (entries 21–23 and IX 1–17 records, entries 38–44); `text/translation_en.json` V 1–14; `tables/plate_check.csv` (I 12, IX rows); `tables/entry_concordance.csv` (V rows); `registration/plate_check/round2–3/key.json` (IX 10 records only); `research/text/plate_check.md` (lines 205–222 and grep hits); `research/text/edition_confusions/variants.csv` (IX 10–11 rows); the wolters1996 check (lines 55–70); the djdIII1962 README and plates PDF pp. 76–77.
  - All greps used `--exclude-dir=preregistration`; `research/preregistration/` was never opened.
  - Nothing was written; no commit or push.
- **Claude project and Drive:** not written.

## Integrator note (main session, 30 Oct 2026)
- The main session viewed the figure IX_a_CT16RCB_rows.jpg (CT16 RCB, CLAHE). One long vertical stroke runs from the upper row (IX 10) down into the lower row (IX 11), as described.
- All results are EXPLORATORY. Only column V was logged blind.
- The I 12 verdict in [wsrp_letters_2026-10-30.md](wsrp_letters_2026-10-30.md) ("probable" מקרת) is superseded by this note: undecidable, with a weak lean to one closed letter.
- A new crop is needed for the כסף מנה חרם division (far left of IX 10): CT17_RB [920,2300,1848,3200] and CT17_RT [968,2100,1992,3300].
- Proposed edits to readings.json and plate_check.csv (e4, e21, e23, e41) are not applied.
