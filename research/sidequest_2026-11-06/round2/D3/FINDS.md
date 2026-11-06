# Side-quest D3, round 2: errors in published sources (6 Nov 2026)

Lane D3 (round-1 family: `out/D3/`, `out/D3b/`; reviews R2, R8). Round 2 took the three items round 1 left open: (a) plate and figure cross-references in the volumes whose captions D3b could not read by machine (HCM 2016, JSP 8, ROSAPAT 07, Humbert–Fidanzio 2019); (b) scale bars and north arrows, which nobody had checked; (c) the *Maresha IV* store copy against the IAA online PDF. It did not repeat A6 (Maresha IV datum shift), B1b/B1c (HA and ʿAtiqot references) or C3.

Two things round 1 got wrong in its method and that change the picture:
- D3b's reference regex was case-sensitive (`Figs?\.`), so it missed lowercase "fig." references. HCM 2016 has 444 of them in Humbert's essay and ROSAPAT 07 has 77. Both are now checked.
- HCM 2016's plates are captioned "Planche N", and ROSAPAT's "Pl. [Roman numeral]". Both are in the text layer. D3b's "no caption text layer" was a regex miss for these two volumes. It holds only for JSP 8, whose text layer is draft OCR of phone photographs.

Data (all in this folder):
- `hcm2016_plate_title_vs_position.csv`: 47 Humbert pottery plates, plate title against the Position column.
- `hcm2016_lamp_plate_labels.csv`: 155 lamp-plate labels paired with the catalogue.
- `north_arrow_scale_checks.csv`: 19 plans from 3 volumes.
- `scripts.md`: the scripts.

No images or crops are published. Page renders and Esri crops were viewed in scratch only and have been deleted.

---

FIND CARD
Title (one line): HCM 2016 (*Khirbet Qumrân et Aïn Feshkha III A*) captions Planches 42 and 45 "Locus 83-3", and its List of Plates repeats it, but every object on them is from L. 81 level 3. The objects include the scroll-type jar KhQ 1492.
Lane: D3
Round-1 link: extends D3b dead end "HCM 2016 … cannot be checked by machine" (new result)
What is odd (2–4 sentences): The locus 81 plate run reads Pl. 39 "Locus 81-1", Pl. 40–41 "81-2", **Pl. 42 "Locus 83-3"**, Pl. 43–44 "81-3", **Pl. 45 "Locus 83-3, photographies de poteries"**, Pl. 46 "81-4 et 7". On Pl. 42 all 8 catalogue rows have Position "81.3" and dates 16–20/3/54, with no archive remark naming L. 83. Those dates are the dates Humbert's own stratigraphic table gives for 81.3 ("3C, atelier, 15-20/3/54", p. 284). Pl. 45 shows only objects from Pl. 43 and 44 ("Planche 43, 5", "43, 6", "44, 7", "44, 8"), and both of those plates are titled "Locus 81-3". Locus 83 is a real and different locus (the small stepped basin next to L. 91), so the caption sends the objects to the wrong room. The same volume's lamp catalogue (Młynarczyk) gives KhQ 1391, item 4 on Pl. 42, as "Found: Loc. 81, 'upper'; Cf. Qumran 1, 317".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Store doc `Humbert-Chambon-Mynarczyk-eds-2016-Khirbet-Qumran-et-Ain-Fes-31a119b3`. PDF p. 288 = Pl. 42. I read the page image at 70 dpi: the title "Locus 83-3, poterie et catalogue, éch. ¼" sits over a table of KhQ 1498, 1492 ("jarre type à manuscrit"), 1407, 1391 (lampe), 1486, 1493, 1488 and 1490, all "81.3".
- PDF p. 291 = Pl. 45. PDF p. 533, the List of Plates: "Planche 42 : Locus 83-3 … 288"; "Planche 45 : Locus 83-3, photographies de poteries … 291".
- PDF p. 284: stratigraphic table of L. 81. PDF p. 281: the text assigns de Vaux's L. 88 pottery to "l'installation 81.3".
- PDF p. 471–472: lamp catalogue no. 44, KhQ 1391.
- Full plate audit in `hcm2016_plate_title_vs_position.csv`. Of 47 plates with tables, 38 have title = position. On 4 the title gives the archive locus that the Remarks column names: Pl. 35 (title L. 68; three rows are Position 73.x, Remarks "L. 73") and Pl. 68, 70 and 83 (Remarks "L. 98", "L. 93", "L. 131"). That is Humbert's stated reassignment and is consistent. Pl. 42 is the only plate whose title locus appears neither in its Position column nor in its Remarks column.
Literature check (queries run, result, tag):
- Web: "Khirbet Qumrân et Aïn Feshkha IIIA 2016 Humbert Chambon Młynarczyk review planches locus 81 errata". No erratum found. Hits were the publisher pages and the 2024 English translation (NTOA.SA 5b, "179 figures and 113 plates"). The Vandenhoeck & Ruprecht reading sample, `content.e-bookshelf.de/media/reading/L-22498334-6fcc33c08f.pdf`, stops before the List of Plates, so I could not tell whether the translation corrects the caption.
- Repo main and `branch_only`: "83-3", "KhQ 1492" and "Locus 83-3" have no relevant hits (only number substrings in unrelated CSVs). Round-1 and round-2 B6 cards do not mention it.
- Tag: **NEW TO THE LITERATURE** (minor; provisional until the 2024 English edition is checked).
Why it might matter: Pl. 42 is one of the few published plates that draws and photographs a complete scroll-type jar (KhQ 1492) from the "atelier" level 81.3. Anyone who counts scroll jars by locus from the plate captions or the List of Plates will put it in L. 83, a water installation, and not in the L. 81 workshop. The caption is wrong in two places and in the volume's own index.
How to confirm or kill it (with data in hand, or what is missing): Open PDF p. 288, 291 and 533 (2 minutes). The card is killed if de Vaux's 1954 register (Humbert–Chambon 1994, *Qumran 1*, pp. 317–318) lists KhQ 1492/1498 under L. 83. Młynarczyk's citation of *Qumran 1* p. 317 for KhQ 1391 as L. 81 argues against that, and Humbert's text never mentions L. 83 in the L. 81 chapter. Missing: the *Qumran 1* pages (the Drive photo set of 3 Nov was not read for them) and the 2024 English edition.
Confidence: high (that the caption contradicts the plate's own table and its neighbours); medium (that no corrected edition exists)
Touches the Copper Scroll? no (Qumran site pottery; no bearing on any scroll entry)

Side results of the same audit (not carded; in the CSVs):
- **Lamp catalogue against lamp plates (Pl. 95–113): clean.** I paired the 155 number labels on the plates with the registration labels by optimal assignment of label positions (`pdftotext -bbox`). All 155 agree with Młynarczyk's catalogue (148 parsed entries) except two artefacts of the method: no. 30 is two pieces, and nos. 192/193 sit next to each other. No. 8 prints its joined pieces in the other order ("5109 + 5094").
- **Humbert's 268 lowercase "fig." references and 80 "Planche" references: clean.** All 176 figure captions exist. The locus-token check flagged 12; all are multi-locus captions.
- **Cross-chapter locus conflicts.** KhQ 1141 and KhQ 1169 are "Loc. 45 South" in Młynarczyk (p. 476) but Position 84.1 and 84.4 on Humbert's Locus 84 plate (p. 227, Remarks "45 sup." / "45 sud dans la cendre"). Humbert reassigns de Vaux's "45 sud" to L. 84 and the lamp chapter does not follow him. This is a disagreement of interpretation inside one volume, not a misprint.
- **Planche 39 is unclear.** The title is "Locus 81-1" and the drawing carries the label "81.1", but all 8 table rows have Position "88.1" (de Vaux's L. 88). Not carded.

---

FIND CARD
Title (one line): The general plan of Qumran in Magen & Peleg 2018 (Fig. 9) has a scale bar labelled "0 10 20 cm". The plan is at metre scale. The 12 detailed plans and their north arrows check out against each other and against imagery.
Lane: D3
Round-1 link: new (first scale-bar and north-arrow audit in the swarm)
What is odd (2–4 sentences): The only overall plan of the site in the Magen & Peleg site description (Fig. 9) has its graphic scale lettered "0 10 20" with the unit "cm". Read literally, the plan would show a site about 1.5 m across. Measured with that bar, pool L91 is 16.9 units long overall. The same pool is 17.2 m overall on the authors' detailed Fig. 98, and the text gives it as 15.60 × 4.40 m inside. So the bar is right in metres and only the unit is misprinted. Every other plan in the chapter (Figs. 16, 24, 31, 38, 41, 57, 71, 98, 100, 102, 104, 107) is lettered "m".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Store doc `Magen-2018-Qumran-site-description-chapter-of-Back-to-Qumran-927bd2d8` (a JSTOR download dated 28 Sep 2026), PDF p. 3 = Fig. 9, printed [11]. At 150 dpi the bar ticks are at x ≈ 964 and 1129 px (165 px = "20 cm"). L91 on Fig. 9 runs from about (655, 860) to (620, 995).
- Fig. 98 = PDF p. 76: 0–5 m bar = 146 px at 100 dpi; L91 inner 460 px = 15.75 m. Text: PDF p. 77 "L91, measuring 15.60×4.40 m".
- North-arrow audit, in `north_arrow_scale_checks.csv`. The arrow angle was measured by `arrow.py` (tip and tail of the largest dark component). The tool has a −5.2° bias on this arrow style, which I calibrated on 9 north-up arrows (range −4.6 to −5.9). Wall angles were measured by Hough fits (`lines.py`) on the north-up Figs. 9 and 41: the N–S walls of L71 and L91 bear 19–21°, and the L56/58 axis bears 106–108°.
  - The three rotated plans agree with the north-up plans: Fig. 98 (L91) within 4.3°, Fig. 100 (L56/58) −4.8°, Fig. 107 (L71) −1.6°.
  - An Esri World Imagery z18 view of the site (fetched 6 Nov, scratch only) shows the main building's walls rotated about 12–19° clockwise. That fits the plans; at 0.5 m per pixel it is a coarse check.
Literature check (queries run, result, tag): Repo main and `branch_only`: no note on Magen 2018 scale bars or north arrows. The project's only Magen 2018 plate note is the L17/L18 caption slip on `sandbox/methods`. I did not run a web search for so minor a slip. Tag: **NEW TO THE LITERATURE** (trivial typographic error; the audit result itself is new to the project).
Why it might matter: A small slip, but it sits on the figure that people reproduce and georeference as "the" plan of the site. The audit result matters more. The Magen 2018 plans are consistent in scale and north to about 5°, so they are safe to register against each other and against the 1953 RAF and HEXAGON frames that other lanes use.
How to confirm or kill it (with data in hand, or what is missing): Look at PDF p. 3, bottom right (1 minute). It is killed only if the printed JSP volume differs from the JSTOR chapter PDF. Not checked: Magen & Peleg's earlier publications of the same plan (JSP 6, 2007; Galor et al. 2006).
Confidence: high
Touches the Copper Scroll? no (unless the plan is used to georeference Qumran features; the scale itself is correct)

---

FIND CARD
Title (one line): The *Maresha IV* store copy is the IAA Publications Portal's own full-volume PDF. So D3b's 10 wrong figure pointers are in the IAA's online edition. The live portal cannot be fetched (Cloudflare challenge), so a re-issue after 13 Oct 2026 cannot be ruled out.
Lane: D3
Round-1 link: D3b-1 (*Maresha IV* wrong figure pointers); this runs its open kill test as far as the data allow
What is odd (2–4 sentences): D3b-1 and R8 left one way to kill the card open: the IAA's online PDF might differ from the store copy. Page 1 of the store copy is the bepress Digital Commons cover sheet that the IAA portal adds to every download. It reads "Israel Antiquities Authority Publications Portal … 8-2025 … DOI: https://doi.org/10.69704/iaaRepV000.1996.82 … https://publications.iaa.org.il/iaareports/82". So the store copy is the portal's full-volume file, not a pre-print or author copy. Its source file was uploaded to Drive on 13 Oct 2026 (the full-volume file is 71,974,017 bytes, sha256 91710daa…). So the errors were in the IAA's online edition at some time between August and 13 October 2026.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `gs://copper-scroll-cog-1030/pdf/Stern-2025-Maresha-IV-Subterranean-Complexes-IAA-Reports-76-db5921ab/p0001.pdf` (612 × 792 pt cover sheet; the book pages are 595 × 765 pt). `manifest.json`: src_bytes 71974017, src_sha256 91710daa4ce82384b5d9ab07d527efcf4a4b0771379df3794420f75a0b3d4998.
- Drive file `14GuLQZbp5DER3u-ARMnwZoLKZrb1Kt80`, createdTime 2026-10-13T15:03:59Z.
- Online per-chapter files are listed by AWOL (1 Sep 2025): `https://publications.iaa.org.il/cgi/viewcontent.cgi?filename=N&article=1081&context=iaareports&type=additional` (N = 0–8). On 6 Nov 2026 these return HTTP 403 with a Cloudflare "Just a moment..." challenge. Robots.txt does not disallow `viewcontent.cgi`, but I did not try to get past the challenge.
- Wayback `available` API: no snapshot of any chapter file.
- Also checked, Plan 1.3.1 (PDF p. 16). After the page is turned 90° clockwise, its north arrow points up. That matches A6's SIFT registration of the same plan to Esri imagery (rotation −0.10°), so the arrow is correct. The plan has no scale bar (A6's fit gives 0.530 m per px at 220 dpi).
Literature check (queries run, result, tag): web: `"Maresha IV" Subterranean Complexes IAA Reports 76 pdf` found the author's academia.edu page and the Haifa/ÖAW/AWOL notices, with no erratum or "revised" notice. Tag: as D3b-1 (**NEW TO THE LITERATURE**). This card only strengthens it.
Why it might matter: It turns D3b-1's "store copy" caveat into "the IAA's own published PDF". An erratum request (for the owner, not the swarm) can cite the portal DOI.
How to confirm or kill it (with data in hand, or what is missing): A human with a browser can download chapter 1, 2, 6 and 7 from the portal and check PDF pp. 28, 90, 133, 164, 170, 228, 300, 346 and 358. The card is killed if the current files differ. Missing: any copy of the portal files later than 13 Oct 2026.
Confidence: high (provenance); unknown (current state of the portal)
Touches the Copper Scroll? no

---

## Dead ends
- **JSP 8 plate and figure checks.** The store text layer is draft OCR of phone photos ("JSP 8 | 30-31 | IMG_1607 | draft OCR"). Captions are garbled ("Fig, 52. Confi, …"), so 217 of 323 "unresolved" figure references are OCR damage, not errors. A real check needs the Drive HEIC photos, one by one (161 photos); not done in this budget.
- **ROSAPAT 07.** The "unresolved Pl. 227–267" of round 1 are running page headers ("2011 Plates 227"), not references. The volume's 85 plates are captioned "Pl. [Roman] - …" but the text never cites them. 56 lowercase "(fig. N.N)" and "(map N)" references all resolve, and the subjects agree (spot-read). Map 13 is never cited (trivial).
- **Humbert–Fidanzio 2019 (11Q).** All 47 unresolved Pl. references and 8 unresolved Fig. references are external: PAM plate numbers, Yadin's *Temple Scroll* plates, and comparanda in footnotes. "Figs. 47-48" is a joint caption. Internal references resolve.
- **HCM 2016 lamp plates** have no scale bar or scale statement, and the drawings are at varying scales (only the catalogue gives dimensions). There is nothing to test, so this is not an error.
- **Galor (Humbert–Gunneweg 2003) north arrows.** Figs. 9, 10 and 11 agree with the site's wall orientation within 4°. Figs. 12 and 13 read 6–11° more westerly than the L68/L69 walls on Magen's Fig. 104 imply. That is within my by-eye accuracy on long spear-shaped arrows, so not carded.
- **Galor Fig. 7 against Magen for L91.** Galor's flat pool is 11.9 × 4.9 m and Magen's 15.60 m. The difference is naming: Galor gives the stepped end to L85, and Magen counts it in L91. Total lengths agree (about 15.3 against 15.6 m). The scale bars are consistent.
- **Magen Fig. 100 L56 length.** 8.2–8.4 m to W609 against the text's 9.30 m; the width matches (3.57 against 3.55 m). The likely cause is the measuring convention (W609 is 0.7 m thick). Dropped.
- **HCM Młynarczyk "Loc. 130-3A" against Humbert "130.2".** "3A" and "2B" are grid squares (Remarks column "A3", "B2") written in reverse order, not levels. No conflict.
- **Imagery truth for north arrows.** Esri z19 is "Map data not yet available" at Qumran. z18 (0.51 m per px) is too coarse for a Hough fit of the walls, so I estimated by eye (12–19° clockwise).

## Blocked inputs
- `https://publications.iaa.org.il/cgi/viewcontent.cgi?filename={0,1,2,6,7}&article=1081&context=iaareports&type=additional` and `…?article=1081&context=iaareports`: HTTP 403, Cloudflare challenge page ("Just a moment..."), 6 Nov 2026. Not circumvented.
- Wayback Machine: no snapshots of those URLs (`archive.org/wayback/available` returns an empty result). The CDX query was "Blocked by egress policy".
- Esri World Imagery z19 tiles over Qumran (x 313783–313787, y 213352–213356): the server returns placeholder "Map data not yet available" tiles.
- 2024 English translation of HCM 2016 (NTOA.SA 5b): not held. The publisher's reading sample (26 pp.) ends before the List of Plates.

## Reproducibility
- Text layers: round-1 `scratch/D3b/txt/{HCM2016,ROS07,HF2019,JSP8,MAG2018,HG2003}.json`.
- Lamp-plate pairing: `hcm_hung.py` (needs `pdftotext -bbox` on store pages p0453 … p0517).
- Plate titles: inline script output in `hcm2016_plate_title_vs_position.csv`.
- Arrows and walls: `arrow.py` and `lines.py` on `hexview.py pdf-page … --dpi 150` renders of Magen PDF pp. 3, 8, 15, 21, 27, 30, 44, 56, 76, 78, 80, 82, 84 and HG2003 pp. 328, 330–332.
