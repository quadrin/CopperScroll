# Side-quest A1: cuts 12–15 and the 5 Nov TIFF set as an object (6 Nov 2026)

Lane A1. Inputs used: Drive folder "3Q15 Copper Scroll (Unzipped Files)" (`1K_Q5rKzL3dUwkb9saX4oiWbno9ayCiR4`, listed by metadata only); bucket `usc/` COGs (cuts 10 and 16 viewed in windows); Brizemeure–Lacoudre–Puech 2006, the bucket copy `Brizemeure-Lacoudre-Puech-2006-Le-rouleau-de-cuivre-3Q15-STD-39ffb801` (copy B, called "EDF 2006" below); Lefkovits 2000 (bucket); Manchester TPA-1-132 cutting correspondence (Drive `1QYCHkEFl7bzCdXFGrgkE7ZRG8Rk97TTv`); the project's USC public catalogue `research/sources/usc_copper_scroll_images/index.csv` (main). No letters were read. All crops are in `private/A1/` only.

Data files in this folder (no image content):
- `drive_cuts12-15_listing.csv`: the 22 cut 12–15 TIFFs in Drive (name, file ID, bytes, modified time, code).
- `frame_inventory_1988.csv`: for each cut, the USC catalogue's 1988 frames (recto/verso, colour/b&w, fragments) against the TIFFs delivered to Drive or the bucket.
- `cut_marks_1955_record.csv`: for each segment, EDF 2006's dimensions, its transcription of the 1955 white-ink cut marks, fragment and rivet counts and changes, plus the marks that the USC catalogue's text says the 1988 verso photographs show.

---

FIND CARD
Title (one line): The 1955 Manchester cut-mark labels (letters F→A × numbers 1–12, segments 2–15 only) are published only in EDF 2006, and its transcription has an impossible range (segment 14 "A5 à A4") and other gaps. The 1988 verso photographs, which show the marks before EDF repainted them, are missing from the TIFF delivery.
Lane: A1
What is odd (2–4 sentences): EDF 2006 says that each segment's "repères de la découpe" were written on it in white ink in 1955, and that EDF copied them onto the reverse in black ink. For segment 2 to segment 15 it gives one range each: F2–F7, F8–F12, E2–E4, E4–E8, E9–D3 ?, D4–D8 ?, D9–D12, C1–C7, C8–C12, B1–B6, B7–B11, B12–A4, **A5 à A4**, A8–A12 ?. Segments 1 and 16–23 have only their numbers. The labels count down from F (outer, column I) to A (inner, column VIII) in steps of 12. That fits the large roll only, which was cut second. (The TPA letter of 19 Oct 1955 says one scroll was "completely opened" by then, and that "the second scroll" has convolutions "much closer together".) Four things in the sequence do not fit:
1. Segment 14's "A5 à A4" cannot be right. It sits between segment 13 (ends A4) and segment 15 (starts A8), so it should read A5–A7.
2. E1 appears nowhere (segment 3 ends at F12, segment 4 starts at E2).
3. E4 is given for both segment 4 and segment 5. No other neighbouring pair shares a mark.
4. Three ranges carry "?" (segments 6, 7, 15).

The USC catalogue's text for the 1988 verso photographs (taken before EDF) names marks that agree with EDF wherever both exist: cut 2 F5, F6; cut 5 E6–E8; cut 7 D5, D6; cut 9 C3–C6, with C1, C2 on a small loose square at lower left; cut 11 B3, B5, B6; cut 12 B7–B9; cut 13 "A", "A2". For cuts 6, 14 and 15, the three uncertain ranges, it only says "small painted marks" without reading them. Those three photographs would settle the three uncertain ranges.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- EDF 2006, ch. II §2.2.1–2.2.23 "Traitement du segment n° …", bucket copy B, PDF pp. 67–79 (book pp. 43–55). Segment 14 is on PDF p. 73, "(A5 à A4)". Segment 6 is on PDF p. 70, "(E9 à D3 ?)". §6.2.1 and §6.2.9 (PDF pp. 57–58) describe how the marks were recorded on Mylar and copied back onto the segments. Extracted text: `scratch/A1/puech_cr.txt`.
- TPA-1-132 (Drive `1QYCHkEFl7bzCdXFGrgkE7ZRG8Rk97TTv`): Wright Baker to Lankester Harding, 19 Oct 1955 (first scroll "completely opened … on 4 days"; second scroll's "convolutions … much closer together"); 6 Mar 1956 (each strip "generally extending around about half the circumference"; saw 1 in. diameter, 0.006 in. wide).
- 1988 verso photographs in the USC catalogue: `research/sources/usc_copper_scroll_images/index.csv` on main. Relevant rows: "3Q15 Cut 2 Verso right, color" (2A3BF1S6Y6B23), "Cut 5 Verso, color" (2A3BF1S6Y6HJG), "Cut 7 Verso, color" (2A3BF1S6Y6TL0), "Cut 9 Verso, color" (2A3BF1S6Y8O63), "Cut 11 Verso" (2A3BF1S6OH2S1), "Cut 12 Verso" (2A3BF1S6OJ6KW), "Cut 13 Verso, color" (2A3BF1S6OJJ77), "Cut 14 Verso" (2A3BF1S6OHS97 / 2A3BF1S6OK9W5), "Cut 15 Verso" (2A3BF1S6OU291 / 2A3BF1S6ORRDD), "Cut 6 Verso" (2A3BF1S6YV4OE / 2A3BF1S6YVE0Y).
- Summary table: `cut_marks_1955_record.csv`.
Literature check (queries run, result, tag):
- Bucket full-text: `pdf-search "repères"`, `"rivet"` (EDF 2006), `"rivet"` (Lefkovits 2000). Lefkovits pp. 446–447 maps cuts to columns but does not mention the labels.
- Repository: `git grep` on main for "repères|cutting mark|white ink|E9 à D3" found nothing. The only USC catalogue text that mentions the labels is the AI preview descriptions, and no note discusses them.
- Web: "Copper Scroll Wright Baker 1955 cutting reference marks letters segments" found nothing specific. The Orion entry "Professor Henry Wright Baker: The Copper Scroll and his Career" (orion-bibliography.huji.ac.il/node/64320) has not been read.
- Tag: **NEW TO THE PROJECT** for the label scheme (published in EDF 2006). **NEW TO THE LITERATURE** for the internal errors (A5–A4, missing E1, doubled E4), unless the Orion paper or DJD III (Wright Baker, pp. 203–210) has them.
Why it might matter: These labels are the only surviving record that ties each saw cut to a position on a convolution of the large roll. With them, the segments could be put back into an unrolled geometry independently of the text: which segment lay on which turn, and where the turn boundaries fall (F/E between segments 3 and 4, E/D inside segment 6, D/C at the 8|9 cut, C/B at the 10|11 cut, B/A inside segment 13). That is relevant to column-boundary and saw-loss questions. The segment 14 error also affects anyone who uses EDF to re-derive cut positions.
One unexplained point (not resolved): EDF widths divided by the number of marks a segment spans *grow* inward. Segment 4 is about 1.4 cm per mark, segment 10 about 1.7, segment 15 about 2.4, while segments 2–3 are about 1.1. That is the reverse of what 12 equal angular marks per turn on a tightening coil would give. So either the marks were not equally spaced or "Largeur" is not an arc measure.
How to confirm or kill it (with data in hand, or what is missing): Read the white labels on the 1988 verso photographs of cuts 4, 6, 13, 14 and 15. The colour verso TIFFs are **not** in the 5 Nov Drive set or the bucket (see card 2). The public preview links in `remaining_preview_manifest.csv` have expired (HTTP 403), and `private-media/` is encrypted. The owner could re-fetch the five previews from USC Digital Library, or ask WSRP for the verso TIFFs. Also check DJD III pp. 203–210 (Wright Baker) and the EDF Mylar "relevé". It is killed if the segment 14 labels physically read A5…A4, for example if the cut was relabelled.
Confidence: high (that the inconsistencies exist in the published transcription); medium (that the labels are per-turn positions, F outer to A inner)
Touches the Copper Scroll? yes (the physical cutting record of the large roll, segments 2–15, columns I–VIII)

---

FIND CARD
Title (one line): The 115-TIFF "complete" set is exactly the 1988 colour **recto** set minus cuts 1 and 9. No verso frame (24 colour, 24 b&w) was delivered, and edge-light ("RE") frames exist only for cuts 15 and 16, the two segments on either side of the broken sheet 2/3 rivet join.
Lane: A1
What is odd (2–4 sentences): Across the 23 cuts, the USC catalogue lists 120 colour recto views, 2 colour recto "fragments" views (cut 10, cut 16), 24 colour verso views, 1 colour verso-fragments view, and b&w twins of each. The Drive set holds 115 TIFFs (= 93 in the bucket + 22 for cuts 12–15). That is exactly 120 + 2 − 1 (cut 1) − 6 (cut 9). So nothing is missing at random: *every* verso image is missing, and those are the photographs that carry the 1955 cut labels and show the rivets from the back (cut 10 verso: "three small round holes in a vertical line"). Light codes: cut 13 has no right view (RR*) and cut 14 has no centre view (RC*). The catalogue agrees (4 recto views each), so these were never shot and were not lost in transfer. The edge-light frames RET/REB exist only for cuts 15 and 16. EDF records 4 rivets on segment 15's left edge and 5 rivet holes on segment 16's right edge, and Lefkovits (p. 446) puts the sheet 2/3 join, where the roll broke, between columns VIII and IX. So in 1988 extra edge-lit views were made of exactly the two faces of the broken join. The Drive copies of cuts 12–15 are dated 3 Nov (all others 29 Oct). They are the only copies anywhere in Drive: a search for `DSS_3Q15_CT13`/`CT14` returns only this folder.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `frame_inventory_1988.csv`, built from `research/sources/usc_copper_scroll_images/index.csv` (294 rows of type "original scroll cut segment (1988 film photo, scanned)"), bucket `index.json` (93 `usc:` items) and `drive_cuts12-15_listing.csv`.
- Special frames: `usc:DSS_3Q15_CT10_FRS_T` (cut 10 recto fragments), `usc:DSS_3Q15_CT16_RFR_T` (cut 16 recto fragments), `usc:DSS_3Q15_CT16_RET_T`/`REB_T`, Drive `DSS_3Q15_CT15_RET_T.tif` (1JYBvhN6G_8qIo6nb4EeRcJqB0QhK5_EU) and `…CT15_REB_T.tif` (1Ui_tFVQuJX9I8sERtBMA7iaXUsIFgI1V). Cut 23's extra codes RBC/RTC/RCS are in the bucket.
- Rivets: EDF 2006 PDF p. 74 (segment 15: "quatre rivets sur son bord gauche"; segment 16: "cinq trous de rivets sur son bord droit"); PDF p. 71 (segment 10: "deux plaques soudées … par huit rivets"). Lefkovits 2000 PDF p. 467 (book p. 446).
- Cut 12–15 bytes ≈ 8-bit RGB uncompressed, so 14.4–22.9 Mpx (CT15_RCB is the largest at 68.7 MB, about 22.9 Mpx, against 33–52 MB for the bucket frames).
Literature check (queries run, result, tag): The project's "already done" list says the verso *previews* exist (Method 7). I found no note that (a) the TIFF delivery has no verso at all, (b) the delivered set equals colour-recto-minus-1-and-9, or (c) the RE frames belong only to the join segments. I searched the baseline summaries and the C2/C3/A2 branch notes for FRS/RFR/RE[TB]/verso and found nothing. The USC catalogue describes the cut 16 edge flap ("perhaps adhering metal from the neighbouring turn"), so that observation is **not** new. Tag: **NEW TO THE PROJECT**.
Why it might matter: Any physical-object study of rivets, joins, cut labels or the backs of the strips cannot be done from the 115 TIFFs. The project's high-resolution set is blind to the face that carries the manufacturing and cutting evidence. It also changes the remedy for cuts 12–15: the owner should run `hexcog2.py … extras` for the 22 Drive TIFFs, *and* request the 24 colour verso TIFFs (plus the cut 16 verso-fragments view) from WSRP.
How to confirm or kill it (with data in hand, or what is missing): Confirm by checking the WSRP delivery note, or by asking WSRP whether verso TIFFs exist at 1988 scan resolution. It is killed if the 4.5 GB 3Q15 zip in Drive 06 holds verso TIFFs (not checked: the zip is over the connector limit). Check the zip's file list in Colab with `unzip -l`.
Confidence: high (inventory arithmetic); medium (that RE = edge views made because of the rivet join; this is inferred from which cuts have them)
Touches the Copper Scroll? yes (the image base for every physical study of the scroll)

---

FIND CARD
Title (one line): WSRP 1988 frame CT10_FRS records "Seven fragments from lower right edge of 'Cut 10'", placed and matched on 12/9/88 by Ken and Bruce Zuckerman. EDF later reports 11 fragments and re-placing one fragment in exactly that zone. Together the two records give the only before/after record of the cut 10 lower-right edge, beside the sheet 1/2 rivet join.
Lane: A1
What is odd (2–4 sentences): Frame `usc:DSS_3Q15_CT10_FRS_T` is not a view of a strip. It shows a padded box with loose pieces and handwritten cards: "Seven fragments from lower right edge of 'Cut 10' of Copper Scroll – placed in position for future conservation" / "Placed and matched 12/9/88 by Ken + Bruce Zuckerman (who photographed them in place)" / "KEEP LEVEL! MOVE CAREFULLY – LOOSE FRAGMENTS". In the box are a long chain of pieces fitted end to end, with cracks between them, and a separate triangular piece. EDF 2006 (segment 10) counts 11 fragments, two plates still joined by 8 rivets, and one change: "un fragment a été replacé correctement dans la zone inférieure droite". Likewise `CT16_RFR` shows 5 loose pieces of cut 16 (one with a small round hole), and EDF segment 16 has "un nouveau fragment a été repositionné et l'emplacement d'un autre modifié" and 5 rivet holes, against 4 rivets on segment 15. A 5th hole with no matching rivet, and a loose cut 16 piece with a hole, can be checked against each other.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `usc:DSS_3Q15_CT10_FRS_T` (2613×4231). Cards at about x 600–1900, y 2600–4200; fragment box at about x 700–2100, y 1200–2600.
- `usc:DSS_3Q15_CT16_RFR_T` (2613×3646). Pieces, as full-res bounding boxes from a threshold of the 1/4 overview: x 1512–2092 / y 1028–3248 (large piece with hole[s]); x 836–1156 / y 536–1476 and x 908–1192 / y 1472–1940 (blade-like piece, broken); x 964–1116 / y 2256–2648; x 268–364 / y 780–912.
- Cut 10 join: an overlap band in `CT10_RLT` and `CT10_RLB` at about x 1650–1950 for the whole strip height, with round domed features (rivet-head candidates) by eye at about y 700, 1500, 2000, 2250, 2560, 3070, 3560, 3950, 4310, 4700 (RLT). That is 8–10 candidates against EDF's 8, and not checked across lightings.
- EDF 2006 PDF p. 71 (segment 10), p. 74 (segments 15–16). Crops: `private/A1/frs10_label.png`, `frs10_box.png`, `c10rlt_seam.png`, `c10rlb_seam.png`, `mont16.png`, `c16_flaps.png`.
Literature check (queries run, result, tag): Web "Zuckerman 1988 Copper Scroll Amman photography loose fragments 'cut 10'" found nothing. The repository has the USC catalogue rows ("Cut 10 Recto fragments": "long, narrow vertical piece made of several fragments fitted end to end") but no link to the EDF record, the date or the card text. Tag: **NEW TO THE PROJECT** (the link between the two records); the 1988 matching date and card are probably **NEW TO THE LITERATURE** (not found in EDF 2006's history of earlier treatments).
Why it might matter: Changes to segments 10 and 16 between the 1988 photographs and the EDF (1994–96) remounting decide which images are valid for edge letters and rivet positions at both sheet joins. It also gives an independent count of the cut 10 lower-right pieces (7 loose in 1988), to set against EDF's segment total.
How to confirm or kill it (with data in hand, or what is missing): Overlay CT10_FRS on CT10_RCB/RRB (lower right) to see whether the 7 pieces were in place or missing in the strip frames (data in hand, not done for budget reasons). Compare against EDF plates CXXVIII–CXXIX and CCXXX–CCXXXII (segment 10) and CXLIV–CXLVII (segment 16) in the bucket copy. Count the rivet heads in cut 10 with a frozen rule across all 6 lightings. Cut 15's left edge (4 rivets) is blocked until cuts 12–15 are in the bucket.
Confidence: high (the frame content and the two records); low (the rivet-head count from frames)
Touches the Copper Scroll? yes (segments 10 and 16, sheet joins 1/2 and 2/3)

---

## Dead ends
- Pulling cut 12–15 TIFFs through the Drive connector: not tried (46–69 MB each, over the ~25 MB limit). Listed by metadata only.
- Full-Drive-folder paging to diff all 115 names: the connector returns pages of 5–25 with heavy metadata. Instead I checked by count (115 = 93 + 22), by the odd codes (FRS, RFR, RBC, RCS, RTC all present in Drive) and against the catalogue. No frame is in the bucket and missing from Drive.
- Rivet counting on cut 10 by eye (RLT, RLB): 8–10 round domed candidates along the overlap band. Not separable from corrosion blisters without a frozen cross-lighting rule, so not carded as a count.
- Cut 16 right-edge flap (RET/REB/RLB/RLT): a raised, curled, yellow-olive layer along the full right edge with embossed relief and one clear round hole at about (1575, 2030) in RET. The flap is out of focus in RET. Already described in the USC catalogue ("perhaps adhering metal from the neighbouring turn"), so it is not new.
- Ruling, guide lines and layout dots: not attempted. C2 found that line-band periodicity fails on most frames (8 of 24 accepted). Guide-line detection would need the same row-profile approach on the same unreliable surface.
- Frame orientation: some R?T/RR* frames appear rotated 180° against RL* (grey scale and flap side swap in cuts 10 and 16). Not verified systematically; `hexview --north-up` exists. Noted only.
- USC verso previews for cuts 13–15 (to read the 1955 labels): the signed CloudFront URLs in `remaining_preview_manifest.csv` have expired (HTTP 403).

## Side observation (not carded; outside the object brief)
- EDF 2006, PDF p. 29 (book p. 5), §1.1: "Le 20 mars 1952, dans la grotte dite n° 8 … découvre deux rouleaux de cuivre", and again "La grotte n° 8 est située …". The rolls are from Cave 3 (3Q15). Cave 8 was found in 1957. This looks like an uncorrected error in the geological introduction; not checked against the erratum or copy A.

## Blocked inputs
- Drive `1K_Q5rKzL3dUwkb9saX4oiWbno9ayCiR4/DSS_3Q15_CT12_* / CT13_* / CT14_* / CT15_*.tif` (22 files, 43–69 MB): over the connector size limit, and not in bucket `usc/`. Remedy: the owner runs `hexcog2.py … extras` (Colab cell 4c) on this folder to add the 22 COGs. Until then cut 15's left-edge rivets (EDF: 4) and the cut 12–15 strips cannot be examined.
- 1988 verso TIFFs (24 colour + cut 16 verso-fragments): absent from Drive 5 Nov folder and bucket. USC preview URLs return HTTP 403 (expired signatures). `private-media/wsrp-1988/` is encrypted (not opened, per brief).
- DJD III vol. I (Drive `1knLGD17tvjrKvu6pMFkhYMsu6nj8l6G7`, 26.7 MB): over the limit and not in the bucket PDFs. Wright Baker's DJD III notes (pp. 203–210) on the cut labels were not checked.
- Drive 06 4.5 GB 3Q15 zip: not listable through the connector (size).

## Seed / reproducibility
- Strip panels: `scratch/A1/strip.py ITEM X0 X1 Y0 Y1 SCALE NPARTS OUT` (uses `hexview.box`). Fragment counts: threshold of the mean RGB above 45 on a 1/4 overview, 2 iterations of binary opening, components over 150 px.
- EDF text extraction: `hexview.py pdf-text Brizemeure-…-39ffb801 <page>` for pp. 66–88.
