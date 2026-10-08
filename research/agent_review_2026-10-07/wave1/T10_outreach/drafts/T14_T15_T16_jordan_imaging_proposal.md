# T14 + T15 + T16 — Imaging and analysis proposal to the Jordan Museum and the Department of Antiquities of Jordan

Status: DRAFT ONLY. Nothing has been sent. Requires the project owner's approval, and ideally a Jordanian institutional partner as co-applicant before submission.

## 0. Routing (official public contacts)

| Body | Route | Source |
|---|---|---|
| The Jordan Museum (holds and displays the 23 segments) | info@jordanmuseum.jo (the site states it "is going through re-development") | https://jordanmuseum.jo/en (EVIDENCE) |
| Department of Antiquities of Jordan (DoA) | Info-DoA@DOA.GOV.JO; hotline 06-4336464 (as printed on the home page); P.O. Box 88, Amman 11118; Jabal Amman, Third Circle, Abdul Moneim Rifai St., Bldg 21 (fax number is on the contact page; its digit grouping is garbled by right-to-left display, so copy it from the page) | https://doa.gov.jo/Ar/Pages/اتصل_بنا and https://doa.gov.jo/ (EVIDENCE) |
| DoA research-project submission page (excavation/survey permits; may or may not cover object studies) | https://doa.gov.jo/AR/ListDetails/الخدمات_والتصاريح/1141/3 ("تقديم مشروع البحث") and archaeological works instructions https://doa.gov.jo/Ar/Pages/تعليمات_الأعمال_الآثرية | https://doa.gov.jo/ (EVIDENCE that the pages exist; whether object studies use this route is UNKNOWN) |

Suggested sequence: a short letter of enquiry to both bodies (below), asking which office handles scientific study of museum objects and what the application format is; then a full application in that format, in Arabic and English. INFERENCE (high): an application co-signed by a Jordanian university or conservation partner, with Jordanian staff as co-investigators and data co-owners, is more likely to succeed than a foreign project acting alone.

## 1. Background facts the proposal relies on

- The scroll was cut into 23 strips at Manchester in 1955–56 by H. Wright Baker (UML catalogue GB 133 TPA/1/132, https://archiveshub.jisc.ac.uk/data/gb133-tpa/tpa/1/132). EVIDENCE.
- 1994–96: EDF's laboratory stabilised the 23 segments; "At every stage in the process numerous X-rays and digital photographs were taken"; "A plaster imprint was made of each segment to enable the production of flat replicas through electrolysis" (G. J. Brooke, "The Conservation of the Copper Scroll", *BAR* 32:5, 2006, sidebar, https://library.biblicalarchaeology.org/sidebar/the-conservation-of-the-copper-scroll/). The same sidebar refers to an unpublished 1977 study of the scroll's deterioration by Andrew Oddy. EVIDENCE.
- Four electroplated copies were made from the plaster reproduction and "donated to the Amman Museum, the Louvre Museum, the École Biblique et Archéologique Française de Jérusalem and the ÉDF Foundation"; the work included "silicone stamping of each of the curved segments" and "X-ray photographs carried out by ÉDF-Valectra" (ÉBAF news, 15 Feb 2024, https://www.ebaf.edu/?p=28351). EVIDENCE.
- Published technical accounts: R. Bertholon, N. Lacoudre and J. Vasquez, "The conservation and restoration of the Copper Scroll from Qumran", in Brooke and Davies (eds), *Copper Scroll Studies* (2002); D. Brizemeure, N. Lacoudre and É. Puech, *Le Rouleau de cuivre de la grotte 3 de Qumrân (3Q15): expertise, restauration, épigraphie* (Brill, 2006). EVIDENCE that these exist (chapter list; BAR review by P. K. McCarter, Sept/Oct 2007, https://library.biblicalarchaeology.org/department/reviews-copper-scroll-conservation/). **Their metallurgical results were not read in this pass** (paywalled).
- Composition: a secondary source (Wikipedia, "Copper Scroll") states the metal is "copper mixed with about 1 percent tin" and that "no metallic copper remained in the strips". Its underlying reference could not be resolved in this pass. Treat as UNVERIFIED until checked against Wright Baker 1956, Bertholon et al. 2002 or Brizemeure et al. 2006.
- Facsimile Editions (London) scanned the three EDF electroformed plates in 3D, not the originals, and notes that "EDF-Valectra only reproduced the front of the three plates" (https://facsimile-editions.com/cs/). EVIDENCE. So no published 3D data of the original segments was found.
- The Wikimedia Commons photographs (2018–2026, CC BY-SA 4.0) show the strips displayed in a glass case at the Jordan Museum (file descriptions, see `data/commons_copper_scroll_images.csv`). EVIDENCE.
- Lead-isotope analysis of 3Q15: none found in the sources checked. INFERENCE (low–medium confidence; searches were limited and the 2006 "expertise" volume was not read).

## 2. What we ask for

### Work package 1 (T14) — non-invasive surface documentation of all 23 segments and the museum's EDF copy

- **Reflectance Transformation Imaging (RTI)** of the recto and verso of each segment and of each column of the Amman EDF copy: highlight-RTI with ~40–60 light positions (or a portable dome), cross-polarised reference images, colour target and scale. RTI is routinely used to reveal incised and low-relief marks by relighting (e.g. Riris and Corteletti 2015, *Internet Archaeology* 38, §3.3, used polynomial texture maps to read the superimposition of rock engravings: https://intarch.ac.uk/journal/issue38/7/3-3.html).
- **3D surface capture**: structured-light or photogrammetric models of every segment (target lateral sampling ≤ 50 µm; depth noise ≤ 10–20 µm), with calibrated scale. These give curvature-based renderings and virtual flattening, and measured groove depths where Tov reported ΚΕΝ and "seventeen" as "written 2 mm below the writing surface of the preceding words" (L. Tov in *Copper Scroll Studies*, p. 289, as recorded in the project's `phase4_summary.md`).
- **Micro-3D** (focus-variation or confocal microscopy, ~1–5 µm) only at the ~20 regions of interest listed in WP2.
- Conditions: all work in the museum, under museum conservators' supervision, with LED light filtered for UV/IR, no contact, and case opening only under the museum's procedures. Estimated handling time: about 1–2 hours per segment for RTI and 3D; 10–15 working days in total.
- Deliverables to the museum and DoA: all raw images and models, processed RTI files, a metadata record per capture (date, operator, light positions, calibration), and a report. Licensing and any publication are decided by the DoA and the museum (see §4).

### Work package 2 (T15) — stroke-order analysis where Greek and Hebrew grooves meet

Target loci (edition line references): the seven Greek letter groups at I 4 (ΚΕΝ), I 12 (ΧΑΓ), II 2 (ΗΝ), II 4 (ΘΕ), II 9 (ΔΙ), III 7 (ΤΡ/ΤΡΙ) and IV 2 ({Ι}ΣΚ) (`phase4_greek_letters.csv`), and any place where these grooves cross or touch a Hebrew stroke, a numeral or a correction. The project's earlier review of the 1988 photographs found no authenticated crossing and records the number of actual crossings as unknown, not zero (`phase4_summary.md`, "USC 1988 registration and lighting review").

Method:
1. Register each locus on the 3D model and RTI using the adjacent Hebrew (no target box is drawn from edition layout alone).
2. At each candidate junction, record which groove's walls and raised burr are interrupted by the other. In punched or chased metal, the later tool mark deforms or displaces the burr of the earlier one. Compare with experimental crossings punched into modern copper (with permission, test pieces only) to fix the criteria before looking at the scroll.
3. Score each junction as earlier / later / indeterminate, by two analysts independently, with the criteria and decision rule written down in advance.
Precedents: microscopic study of the order of intersecting incisions on engraved objects (F. d'Errico, "A new model and its implications for the origin of writing: the La Marche antler revisited", *Cambridge Archaeological Journal* 5(2), 1995 — bibliographic detail from Cambridge Core search listing); PTM-based superimposition (Riris and Corteletti 2015, above); an SPIE paper on determining the sequence of line crossings using 3D measurement (SPIE vol. 5954, paper 59540V, 2005, doi:10.1117/12.623117 — title only seen in a search listing; content not accessible).
Limits stated up front: corrosion, EDF consolidation and the 1955–56 cutting may have destroyed the evidence at some or all junctions; an "indeterminate" result is expected at many loci.

### Work package 3 (T16, optional) — composition and lead isotopes

- **Step 1, non-invasive:** portable XRF spot readings on surfaces the conservators select (corrosion surface only; the result describes corrosion products, not the original alloy).
- **Step 2, only if the DoA approves:** micro-sampling (≤ 1 mg) for lead-isotope ratios (MC-ICP-MS) and trace elements, from already detached fragments, saw debris or conservation residues if any were retained in 1955–56 or 1994–96, or else from a damaged edge the conservators choose. We recognise that this is **invasive**, may be refused, and that the metal is reported to be heavily mineralised (see §1). We ask first whether retained fragments exist.
- Question addressed: whether the copper's ore source is consistent with Levantine/Arabah sources or with imported metal; this bears on where the sheets were made, not on what the text means.

## 3. What the analysis would answer (and what it would not)

- Disputed letters: the plate check (30 lines) found that printed reproductions decide few cases; RTI and 3D give lighting-independent stroke geometry for re-reading by a blind panel (T13). It will not by itself choose between readings.
- Greek letters: a dated stroke order at even one crossing would show whether a Greek group was cut before or after the adjacent Hebrew. It will not tell us what the letters mean.
- Metal: ore-source compatibility only.

## 4. Data ownership, licensing and credit (proposal terms)

- All data belong to the DoA / Jordan Museum. The project receives a copy for the stated research only.
- Proposed licence for any public release: CC BY-NC 4.0 or another licence the DoA chooses; release timing set by the DoA. Jordanian staff are co-authors on any publication from the data.
- Training: on-site training in RTI and 3D capture for museum staff, with equipment left on loan or donated if funding allows.

## 5. Rough budget (INFERENCE; to be replaced by real quotes)

| Item | Range (USD) |
|---|---|
| RTI kit (camera, lenses, lights, spheres, targets) or dome hire | 5,000–25,000 |
| 3D scanner hire or service, 2–3 weeks | 10,000–40,000 |
| Micro-3D microscopy (portable instrument hire or lab time) | 5,000–20,000 |
| Travel, subsistence, insurance, team of 2–3 for 3 weeks | 15,000–30,000 |
| Processing, storage, publication | 5,000–15,000 |
| Optional pXRF / lead isotopes (lab fees, if approved) | 3,000–10,000 |
| **Total** | **≈ 45,000–140,000** |

## 6. Draft letter of enquiry (English; to be translated into Arabic)

To: The Director General, Department of Antiquities of Jordan; The Director, The Jordan Museum
Subject: Enquiry about a non-invasive imaging study of the Copper Scroll (3Q15)

Your Excellency, Dear Director,

I am writing on behalf of an independent research project on the Copper Scroll from Qumran Cave 3, which is held in the Jordan Museum. Scholars still disagree about a number of letters in the scroll, and about seven small groups of Greek letters engraved at the ends of entries in its first four columns. These questions can now be studied with non-contact imaging methods that were not available when the scroll was conserved by Électricité de France in 1994–96.

We would like to ask whether the Department and the Museum would consider an application for:
1. reflectance transformation imaging (photographs taken under many lighting angles) and 3D surface scanning of the 23 segments and of the Museum's electroformed copy, carried out in the Museum under the supervision of the Museum's conservators, with no contact with the metal;
2. close study of the places where the Greek letters meet Hebrew letters, to see which was engraved first;
3. optionally, and only if the Department considers it acceptable, a study of the metal's composition. This could begin with non-invasive measurements. Any sampling would be invasive, so we would first ask whether fragments detached during the 1955–56 cutting or the 1990s conservation were kept.

All images and data would belong to the Department and the Museum, which would decide on any publication and licence. We would propose that Museum and Department staff take part as co-investigators and co-authors, and we would offer training in the imaging methods.

Could you tell us which office handles applications for the scientific study of museum objects, and what form the application should take? We would be glad to send a full proposal with methods, schedule and budget, in Arabic and English.

With respect and thanks,
[Name], on behalf of the Copper Scroll research project
[Institutional partner, if any]
[Contact details]
