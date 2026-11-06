# Side-quest A1, round 2: 3Q15 as a physical object (6 Nov 2026)

Lane A1, round 2. This pass builds on A1, A1b, A1c, A1d and reviews R1, R7 and R8. It runs the kill tests that round 1 left open: EDF's radiographs of segments 10, 15 and 16, and the 1988 recto frames of cut 10. It also closes or narrows the segment 18, 23, 17 and 21 items.

Sources:
- **EDF** = Brizemeure, Lacoudre & Puech 2006, store copy B `Brizemeure-Lacoudre-Puech-2006-Le-rouleau-de-cuivre-3Q15-STD-39ffb801`.
  - Annexe 4 (PDF p. 64) lists the films.
  - Pre-treatment radiographs are Pl. LIII–CIX (PDF pp. 343–399). Post-treatment (1997) radiographs are Pl. CCXII–CCLXVI (pp. 513 ff.).
  - Pages were rendered at 300 dpi to scratch. Every y value below is in pixels of that 300 dpi page.
- **USC/WSRP 1988 frames:** `usc:DSS_3Q15_CT10_RLT_T` and `usc:DSS_3Q15_CT15_RLT_T` (bucket). Verso previews come from `images/previews/original-scroll-remaining/`.
- **Height fraction** = (y − strip top) / (strip bottom − strip top), measured on the same image.
- No letters were read. Crops are in `private2/A1/` only.

Data: `rivet_positions_radiographs.csv` holds every disc, hole and frame feature: its page, y, strip extent and fraction, and what it matches.

---

FIND CARD
Title (one line): EDF's own radiographs show five rivets on segment 15, where its text and both plates say four, and six hole positions on segment 16, where its plate draws four. The sheet 2/3 join had at least 7 rivet positions.
Round-1 link: A1b-2 (R7: "at least 6" fails, 5 holds). This card runs kill test (a) of that card and reverses R7's rejection of r1.
Lane: A1
What is odd (2–4 sentences): EDF's text says segment 15 "porte quatre rivets", and Pl. CXL–CXLIII draw 4 (at 0.51, 0.60, 0.77, 0.93). On EDF's pre-treatment film 15 G (Pl. LXXXVI) and on its 1997 film Q15G (Pl. CCXLII), the left edge carries **five** dense discs, at **0.393 / 0.518 / 0.612 / 0.777 / 0.931** and **0.385 / 0.513 / 0.609 / 0.773 / 0.929**. The undrawn fifth disc is A1b's r2 (0.39 in the 1988 frame). On segment 16, the Q16D film (Pl. CCXLVII) shows four full holes on the rivet edge, at 0.383, 0.511, 0.607 and 0.768, plus two **half-holes where the piece edge breaks through a hole**, at 0.108 and 0.272. EDF's Pl. CXLIV draws only 0.13, 0.40, 0.61 and 0.77, and its text says "cinq trous".
- The four full holes repeat segment 15's rivet spacing (gaps 433/327/548 px against 431/328/573 px).
- The 0.11 half-hole matches the round hole that the 1988 frame shows on segment 15 at 0.13 (A1b r1, inside old adhesive). R7 rejected r1 because EDF's cleaned plate draws no rivet there. A hole with its rivet lost fits both the radiograph and the plate.
- Segment 15's 0.93 rivet has no partner hole on segment 16. EDF's text for segment 16 records "cassures récentes sans fragments correspondants" on the right (rivet) side.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- EDF PDF p. 376 (Pl. LXXXVI, "15 G"): discs at y 1511, 1942, 2270, 2843 and 3375, x ≈ 107–147; strip y 147–3615.
- EDF PDF p. 543 (Pl. CCXLII, "Q15G"): discs at y 1646, 2084, 2414, 2972 and 3508; strip y 329–3750.
- EDF PDF p. 548 (Pl. CCXLVII, "Q16D"): half-holes at y 603 and 1159; holes at 1538, 1971, 2298 and 2846 (x ≈ 1050–1200); strip y 235–3634; no hole near y 3396.
- Second witness: Pl. CCXLVIII (p. 549, also "Q16D") is a separate exposure of the same reassembled strip turned 180°. Its six features (y 3617, 3068, 2687, 2264, 1934, 1388) map onto Pl. CCXLVII with a constant offset of 335–342 px. Pl. CCXLVI (p. 547, "Q16G") repeats the four full holes (gaps 455/356/590 px, 1.07 × scale).
- EDF text: PDF p. 74 (seg 15 "quatre rivets"; seg 16 "cinq trous de rivets … cassures récentes sans fragments correspondants").
- 1988: `usc:DSS_3Q15_CT15_RLT_T` hole r1 at (1225, 1005) and head r2 at (1070, 2160), from A1b's `ct15_rivet_line.csv`. Crops: `private2/A1/e15.png`, `z16.png`, `z_up.png`, `cmp548_549.png`, `ct15_upper.png`.
- One more candidate, not counted: a dense half-disc at the broken edge at 0.44 on both segment 15 films (p. 376 y 1691; p. 543 y 1819). It may be folded edge metal.
Literature check (queries run, result, tag):
- Repo main and `branch_only`: grep for "Q15G", "Q16D", "LXXXVI", "CCXLVII", "CCXLVIII", "trous de rivets", "cassures récentes sans". The only hits are plate numbers in `tables/plate_check.csv` (Puech's text plates, unrelated) and base64 noise in an atlas HTML file. Swarm round 1 used no radiograph of segments 15–16 (R7 and R8 list them as unread).
- Web: "Copper Scroll 3Q15 rivets sheet join number of rivets radiographs EDF Brizemeure Lacoudre" returned only catalogue and review pages (EBAF news, BAR reviews, Orion). Nothing on rivet counts.
- Tag: **NEW TO THE LITERATURE** (provisional) for the count and the text/plate/film contradiction. The films themselves are published in EDF and uncommented.
Why it might matter:
- This is the rivet layout of the one join where the scroll broke into two rolls. EDF's "4 rivets / 5 holes" mismatch does not mean a lost rivet. Both of its plates undercount what its own films show.
- With holes at 0.11 and 0.27 on segment 16 and rivets at 0.39–0.93 on segment 15, the join had at least 7 positions at 3.4–4.8 cm pitch. That is the same build as the sheet 1/2 join (card 2: 8 rivets).
- The two half-holes show where segment 16 broke: through rivet holes, the weakest line. That fits A1d-2's dated breaks.
How to confirm or kill it (with data in hand, or what is missing): Done with data in hand, two films per segment. It is killed for the sixth position if 0.11 and 0.27 on segment 16 are pieces that EDF misplaced in reassembly. Both lie on loose pieces ("un nouveau fragment a été repositionné"). Their spacing (4.6 cm, 3.2 cm) fits the series, but that does not prove the placement. The pre-treatment segment 16 films (Pl. LXXXIX–XCII) show that edge only edge-on, because the strip was still curved. The original films or the full-resolution verso TIFFs (not held) would settle it.
Confidence: high (5 discs on segment 15; 4 full holes on segment 16 aligned with them); medium (the two half-holes as rivet positions, so 7 in all)
Touches the Copper Scroll? yes: the sheet 2/3 join, columns VIII|IX (manufacture). ARGUMENT: no bearing on any entry's location. It bears only on how the three sheets were joined.

---

FIND CARD
Title (one line): Segment 10's "huit rivets" is right. The eighth rivet is at the foot of the join (0.97), clear on EDF film Q10G and seen as a head in the 1988 recto frame. EDF's plates leave it out. R8's faint disc at 0.41 is a ninth round feature, less dense than the rivets.
Round-1 link: A1d-3 (R8: 7 certain + 1 probable at 0.41).
Lane: A1
What is odd (2–4 sentences): R8 read Q10C (Pl. CCXXXII) and 10 C (Pl. LXXIII) and proposed the 0.41 disc as the eighth rivet. On Q10G (Pl. CCXXXI), which has the same scale and offset as Q10C (five shared discs within 15 px), the foot of the overlap band shows **two ring-shaped discs like the other rivets**, at 0.884 and **0.969**. Q10C shows dense blobs at the same two heights (0.877, 0.969). The 0.97 position is drawn on no EDF plate (Pl. CXXVIII and CXXIX stop at 0.872). So the dense series is 0.056, 0.235, 0.368, 0.476, 0.592, 0.718, 0.877 and 0.969: **eight**, as the text says. The 1988 recto frame CT10_RLT has round domed heads on the overlap band at 0.061, 0.240, 0.364, 0.409, 0.483, 0.587, 0.703 (holes), 0.872 and 0.969. That is all eight, and the 0.41 feature as well, which in the radiographs is a faint grey, off-axis disc and not a dense one.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- EDF PDF p. 532 (Pl. CCXXXI, Q10G): ring discs at y 996, 1458, 1862, 2281, 3302 and **3604**.
- EDF PDF p. 533 (Pl. CCXXXII, Q10C): strip y 169–3713; discs at 366, 1001, 1472, 1857, 2267 (hole) and 2715 (hole); dense blobs at 3278 and 3604; faint grey disc at 1626.
- EDF PDF p. 363 (Pl. LXXIII, 10 C pre-treatment): discs at 967, 1449, 1833, 2244 and 2686, faint at 1602; the foot is overexposed.
- `usc:DSS_3Q15_CT10_RLT_T`, band x ≈ 1780–1850, strip y ≈ 430–4880 (read by eye): heads at y 700, 1500, 2050, 2250 (pink crust), 2580, 3040, 3560 (hole pair), 4310 and **4740**. Unmatched: an oval at 4100 and a dark hole at 4500 (lacuna?).
- Crops: `private2/A1/z10.png`, `z10b.png`, `ct10rlt_band2.png`.
- Pitch (× 29.5 cm): 5.3, 3.9, 3.2, 3.4, 3.7, 4.7, 2.7 cm. The top rivet is about 1.7 cm from the top edge and the bottom rivet about 0.9 cm from the foot.
Literature check (queries run, result, tag): Repo and branches: "Q10G", "CCXXXI" (only unrelated plate numbers in `tables/plate_check.csv`), "huit rivets" (only swarm round 1). Web query as for card 1: nothing on rivet counts. Tag: **NEW TO THE PROJECT** (the films are published in EDF). EDF's plates' omission of the foot rivet is **NEW TO THE LITERATURE** (provisional).
Why it might matter:
- It settles A1d-3: EDF's text and films agree, and the plates are the weaker record. The same holds on the sheet 2/3 join (card 1), so for rivets **EDF's plates undercount on both joins**.
- Anyone who measures join geometry from the plates loses the end rivets.
- Both joins now read as about 8 rivets at 3–5 cm pitch, with end rivets 1–2 cm from the edges. That is one way of making both joins.
How to confirm or kill it (with data in hand, or what is missing): It is killed if the 0.97 ring on Q10G is the adhesive or resin lump that EDF's revers plates hatch at the foot. The ring-and-centre form and the matching 1988 domed head argue against that. Check `usc:DSS_3Q15_CT10_RLB_T` and `RRT_T` at the foot of the band (in hand, not done). The 0.41 feature stays open: it is round on the recto in 1988 but of low density on the films. It could be an empty hole filled with corrosion, or a blister.
Confidence: high (8 dense positions on two films); medium (0.41 = rivet-related)
Touches the Copper Scroll? yes: the sheet 1/2 join, segment 10 (manufacture only; no bearing on entry locations).

---

FIND CARD
Title (one line): Segment 18's "cinq lignes parallèles gravées" run across a separate corner fragment and the main strip, but stop at the 17|18 saw edge. EDF moved that fragment without saying so in its text.
Round-1 link: A1d dead end (segment 18 lines below preview resolution) and A1b-3 / R7 (lines that cross a 1955 cut predate it).
Lane: A1
What is odd (2–4 sentences):
- On EDF's revers plate Pl. CLI (p. 443) the five red "Traces d'utilisation (?)" are horizontal lines 0.3–1 cm below the top edge, at the verso top left. They run continuously across a small square fragment outlined as a separate piece (thick border, notch) and on into the main strip, about 2.5 cm in all. The post-treatment Pl. CLIII (p. 445) redraws them the same way. In the Feb 1994 photograph (Pl. XLVII, p. 334) that corner piece lies **loose** beside the strip.
- The avers plates show the same corner outlined in blue: "cassure récente avec fragment correspondant" before treatment (Pl. CL), "Nouveaux positionnements" after (Pl. CLII). EDF's text records only "un fragment a été placé dans la zone inférieure gauche", which is the red-marked lower-left corner of Pl. CLII.
- The verso left edge of segment 18 is its recto right edge, the 17|18 cut. Segment 17's revers (Pl. CXLIX, p. 441) draws no lines at the matching top corner.
- So, unlike the segment 13|14 lines that R7 found crossing a cut, these lines do not show on the other side of their saw cut.
Evidence (exact sources: file path / page / figure / frame / coordinates): EDF PDF p. 443 (Pl. CLI) at 300 dpi, window x 880–1600 / y 780–1100. PDF p. 445 (Pl. CLIII), p. 442 (Pl. CL), p. 444 (Pl. CLII), p. 441 (Pl. CXLIX, seg 17 after treatment, avers and revers), p. 334 (Pl. XLVII), text PDF p. 75. 1988 verso preview UC15246020 (corner below resolution). Crops: `private2/A1/p443z.png`, `pl18.png`, `top17_18.png`.
Literature check (queries run, result, tag): Repo and branches: "cinq lignes", "lignes parallèles" (only swarm A1b/A1d). Web: not found beyond EDF. Tag: **NEW TO THE PROJECT** (EDF draws all of it). The fit of the corner fragment shown by the lines, and the move of that fragment missing from EDF's text, are **NEW TO THE LITERATURE** (provisional, minor).
Why it might matter: The lines give an independent fit for the loose corner fragment, as C8 did for segment 10 (A1d-1). They stop at the saw cut with no partner on segment 17. That weakens "époque fonctionnelle" for this set. The saw kerf was only 0.006 in. (about 0.15 mm), so lines that crossed the cut line before 1955 should continue on segment 17. They either ended right at the future cut line or were made after the sawing. The 1955 Araldite backing of the verso (hatched over this very corner) is a possible medium for modern scratches.
How to confirm or kill it (with data in hand, or what is missing): It is killed for "post-1955" if segment 17's verso top-right corner shows the lines on a photograph. Segment 17 is only 5.6 cm wide and EDF draws its edges simply, so the plate's silence is weak evidence. Check EDF Pl. XLVI (p. 333) at 600 dpi and the post-treatment verso photos (Pl. CCV, CCVI). The 1988 verso previews are too coarse. The full-resolution verso TIFFs are not held.
Confidence: medium (what the plates draw: lines across the fragment boundary, and the undisclosed move); low (the lines stop at the cut, so they are post-1955)
Touches the Copper Scroll? yes: segment 18 (small roll), surface marks (no bearing on entry locations).

---

## Dead ends
- Segment 23 cloth bands, 2 vs 3 (A1d): closed. Both the 1988 preview UC15246565 and EDF Pl. LII (p. 339) show **three** green bands: two on the upper piece, and a third short band across the junction onto the lower piece. EDF's "trois" is right. The USC catalogue text (and A1d) missed the third. `private2/A1/vz23.png`.
- Segment 17 transparent tape (upper part) and segment 21 paper label and tape (upper part): not resolvable on the 1988 previews (about 1000 px) or on EDF Pl. XLVI and L at 400 dpi. Both segments look the same in 1988 and 1994 at that scale. Not carded.
- Pre-treatment segment 16 films (Pl. LXXXIX–XCII, pp. 379–382): the rivet edge is curved and seen edge-on (a dense white band), so no holes can be counted. Only the 1997 films serve.
- Segment 15 upper left edge (0.11–0.27): in 1988 it is under old adhesive (`ct15_upper.png`); only r1 (0.13) shows. The edge is broken away on the radiographs, so no partners for segment 16's 0.27 half-hole.
- Automatic disc and hole thresholding on the book renders: unreliable (page white and film margins merge, and the ring rivets are not saturated). All positions were read on ruled crops and centroided by hand. The scripts are in `private2/A1/scripts/`.
- Full-resolution recto TIFFs for tool marks and layout beyond the rivet bands: not attempted (budget spent on the radiograph kill tests). The only frame work was the CT10 RLT rivet band and the CT15 RLT upper edge.

## Blocked inputs
- None new. The full-resolution 1988 verso TIFFs are still absent: the WSRP delivery is recto only (A1-2). EDF's original radiograph films are not held, so all readings are from the book's halftone prints (store copy B), rendered at 300 dpi.
