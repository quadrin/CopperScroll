# Side-quest B6, round 2: the Qumran final reports as data (6 Nov 2026)

Abbreviations follow round 1 (`out/B6/FINDS.md`).
- **HG2003** = Humbert & Gunneweg 2003, *KhQ II*. Store `Humbert-and-Gunneweg-eds-2003-…-7c3a264b`; printed page = PDF page − 30.
- **HC1994** = Humbert & Chambon 1994. Owner's page photos in Drive `1_aCKbwjJKK2WzZdFD3zZm1JD5fMeT0Qe`.
- **HCM2016** = *KhQ III A*. Store `…-31a119b3`; printed page = PDF page.
- **HF2019** = Humbert & Fidanzio 2019, *KhQ IV A, Qumran Cave 11Q*. Store `Humbert-and-Fidanzio-editors-2019-…-10ddfb6b`; printed page = PDF page − 25. It is a born-digital e-book, so its text layer is reliable.
- **M2018** = Magen & Peleg 2018, *Back to Qumran*, "Site description" chapter. Store `Magen-2018-…-927bd2d8`; JSTOR CC BY-NC copy. Printed pages are given in brackets.

Data in this folder:
- `naa2003_chemistry_conflicts.csv`: 6 samples, each given incompatible chemical results.
- `hf2019_inventory_number_conflicts.csv`: 4 objects with wrong or several inventory numbers.
- `register_rows_settled.csv`: 3 open rows of round-1 B6-2, settled.

Private (owner's HC1994 photos): `private2/B6/HC1994_p312_L61_objects_1109_1139_crop.jpg` and `HC1994_p348_tombe16_crop.jpg`.

---

FIND CARD
Title (one line): In HG2003, the two NAA chapters give the same samples two or three incompatible chemical origins (QUM 209, 211, 215, 217, 221, and the Feshkha inkwell). Conclusion 1 rests on one of them.
Lane: B6
Round-1 link: B6-1 (top-10 #1), taken further. B6-1 moved QUM 209's *find spot*; this card shows that the *chemistry* the conclusion uses is not stable either. Also extends B6-2.
What is odd (2–4 sentences): The pottery chapter (Gunneweg & Balla, pp.11–64) and the inscriptions chapter (same authors, pp.389–395) report results for the same QUM samples, and they disagree with each other and within themselves.
- **QUM 209** has three origins: (a) p.19, a "jug found in the khirbeh" that belongs "to Chemical Group I [local Qumran] as we have shown", although it is in no Group I table; (b) p.24, "found north of Cave 1", similar to "Arabic pottery analyzed from el-Jib"; (c) p.392, it "matches chemically … Arad-Beer Sheba local ware", which is the basis of conclusion 1 on p.393.
- **QUM 211** (Feshkha 255A) is in the Jericho Group III list on p.392. On the same page it is "the inkwell, QUM 211 (Feshkha 255A)" with an Arad–Beer Sheba–Qitmit origin, and p.24 also gives it Arad–Beer Sheba. Lemaire (p.380) describes it as a combed pithos sherd with a Greek prayer, "provenance inconnue". The Feshkha inkwell is a different sample, QUM 193 (AF 15), which pp.13 and 32 call "locally made at Qumran".
- **QUM 215** is called a khirbeh jug in Group I (p.19) and el-Jib-like (pp.24, 392). It is Lemaire's 4QA, a painted sherd from Cave 4, September 1952 (p.372, "Provenance INAA: El-Jib ?").
- **QUM 217** is one of the "nine [Jericho] jugs" and, in the next sentence, belongs to Group I (p.19).
- **QUM 221** (inkwell, L129): p.13 says it "did not match any of the pottery that we have analyzed so far"; p.32 says it matches Arad–Qitmit–Beer Sheba pottery analysed at Bonn.

The Arad–Beer Sheba result is thus attached at different places to 209, 211, 221 (and 148). For QUM 209, only the p.392 version agrees with Lemaire's "Provenance INAA: Arad-Beershéba" (p.369).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HG2003 pottery chapter: p.13 (PDF 43) on the inkwells; p.19 (PDF 49, "Jugs" paragraph, checked on the rendered page image); Table 5 p.19 (S-211 Feshkha and S-217 in the jugs column); p.24 (PDF 54) "Outliers"; p.32 (PDF 62) on QUM 221; App. I p.36 (PDF 66) and App. II p.41 (PDF 71).
- HG2003 inscriptions chapter: Table 1 p.390 (PDF 420), whose category column says "Settlement" for QUM 209 and "Cave" for QUM 215; group lists p.391 (PDF 421); p.392 (PDF 422) Group III and "Outliers"; p.393 (PDF 423) conclusion 1.
- Lemaire: p.349 (PDF 379, KhQ 682, no INAA line); p.364 (PDF 394, KhQ 2507, Hébron-Motsa, which agrees with Group II on p.391); p.369 (PDF 399, KhQ 2575); p.372 (PDF 402, 4QA); p.380 (PDF 410, Fesh. 255A).
- Row-by-row: `out2/B6/naa2003_chemistry_conflicts.csv`.
Literature check (queries run, result, tag):
- Web: `Gunneweg Balla 2003 neutron activation Qumran inconsistencies review "Khirbet Qumrân et 'Aïn Feshkha II"`; `Qumran inkwell neutron activation "Arad" OR "Qitmit" Gunneweg inkwell Feshkha provenance contradictory`; `Michniewicz Krzyśko Qumran pottery provenance critique Gunneweg Balla neutron activation errors`. These returned only Orion bibliography entries for the chapters and for later Gunneweg papers ([Orion 53933](https://orion-bibliography.huji.ac.il/node/53933), [Orion 61657](https://orion-bibliography.huji.ac.il/node/61657), [Orion 62516](https://orion-bibliography.huji.ac.il/node/62516)). No erratum or review that lists these conflicts was found.
- Store: `pdf-search "QUM 209"`, `"Beer Sheba"`, `"north of Cave 1"` across all 103 PDFs give hits only in HG2003. Wagemakers 2014 (Gunneweg's chapter) has none.
- Project: "QUM 211", "QUM 215", "QUM 217", "QUM 221", "QUM 193" appear only in round-1 `out/B6/locus_finds.csv`; `registration/qumranII2003_extracted.md` has nothing on the NAA.
- Later Gunneweg papers (Holistic Qumran 2010, Bio- and Material Cultures 2006) were not read; they are not in the store.
- Tag: **NEW TO THE LITERATURE**.
Why it might matter: Gunneweg & Balla's provenance groups are the published basis for statements such as "Qumran pottery made in Jericho", "the Feshkha inkwell is a Qumran product" and "the Cave 1 sherd came from the Beer Sheba region". For five samples the volume supports two or more answers. Anyone reusing the tables (as Lemaire did, by copying a provenance line into each entry) inherits whichever version they copied.
How to confirm or kill it (with data in hand, or what is missing):
- All quotes are in the text layer, and p.19 was checked on the rendered page image. The other pages can be re-rendered with `hexview.py pdf-page … <PDF page>`.
- Kill it for a sample if the published PCA/cluster figures (not in the text layer; pp.20–23 plates) put it in one group unambiguously. That would show which statement is the slip, but not remove the contradiction in print.
- Final settlement needs the Budapest element data (not in the corpus).
Confidence: high (the contradictions are printed); low for which group is right.
Touches the Copper Scroll? maybe. ARGUMENT (kept apart from the evidence): Conclusion 1 sets a "limestone natural caves" group (1, 2, 3, 11: no inscribed pottery) against marl caves, and uses QUM 209 as its one positive datum near Cave 1. With 209 moved to L30 (B6-1) and its chemistry given three ways, no Negev-made object is tied to the limestone caves, Cave 3 included. This removes a weak argument from the cave–settlement debate. It does not favour any 3Q15 entry identification.

---

FIND CARD
Title (one line): HF2019 (Cave 11Q final report) prints the oldest radiocarbon-dated linen, the string bundle IAA 577250, as "Gr11Q98", a number its own catalogue gives to a different textile. The index calls it Gr11Q198, and the authors' accepted manuscript calls it Gr11Q183.
Lane: B6
Round-1 link: new (round 1 did not use HF2019).
What is odd (2–4 sentences): Sample 1 of the 2015–16 Groningen series (GrA-65493, 2160 ± 30 BP, 2σ 358–108 BC) is the oldest Cave 11Q linen. Taylor et al. use it to argue that 11Q is not only a "young cave" (pp.155–156). Ch. 6 calls it "Gr11Q98" in the text, the Fig. 1 caption and Table 1, with IAA 577250.
- In ch. 4, Table 1 (textiles, p.108) gives **Gr11Q98 = IAA 577242**, a bleached tabby fragment 12 × 11.5 cm.
- Ch. 4 Table 3 (strings, p.112) prints IAA 577250 as Gr11Q98.
- The Index of Materials (p.284) and the List of Figures (p.xxiv, "Calibration curve for 11Q linen string, Gr11Q198") give **Gr11Q198 = 577250**.
- The King's College accepted manuscript of ch. 6 calls the same object **"Gr11Q183, IAA 577250"**. In print, Gr11Q183 is "988", a group of textile fragments (Table 1 no. 154, p.111).

The same dropped leading "1" affects three more strings in Table 3 and the ch. 4 text: 179 → 79, 197 → 97, 199 → 99. Each collides with a textile in Table 1. For example, pp.104 and 116 say "Gr11Q79 and Gr11Q99 … have a little string tied to the textile corner", but Table 1 gives Gr11Q79 as a "cut textile", while the knotted cord is Gr11Q179 = 814859.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HF2019 PDF pp.173 (printed 148: sample list), 175 (150: Fig. 1 text), 176 (151: Table 1), 180 (155: 2σ discussion).
- Ch. 4 Table 1: PDF 133 (p.108) rows 50, 68–70; PDF 136 (p.111) rows 150, 154. Ch. 4 Table 3: PDF 137 (p.112) rows 19–22. Ch. 4 text: PDF 129–130 (pp.104–105) and 141 (p.116).
- Index: PDF 308–309 (pp.283–284). List of Figures: PDF 25.
- Accepted manuscript: https://core.ac.uk/download/518763676.pdf (cover: "Final author's version (accepted by publisher, after peer review)"). It was read through WebFetch (model summary with quotes): "Bundle of strings (Gr11Q183, IAA 577250)…". The other five samples keep the same numbers as in print.
- Table: `out2/B6/hf2019_inventory_number_conflicts.csv`.
Literature check (queries run, result, tag):
- Web: `"Gr11Q98" OR "Gr11Q198" radiocarbon linen string Cave 11Q`. This found only the ch. 6 manuscript (core.ac.uk), which uses a third number, and catalogue entries ([OEAW record](https://www.oeaw.ac.at/resources/Record/993584707204498/TOC), [V&R preview](https://www.vandenhoeck-ruprecht-verlage.com/downloads/productPreviewFiles/LP_978-3-525-56469-1.pdf)). No correction was found.
- Project: "Gr11Q" gives 0 hits on main and branch_only.
- Tag: **NEW TO THE LITERATURE**.
Why it might matter: HF2019 introduced the Gr11Q system to give every 11Q object one unambiguous number (Introduction, p.10). For the volume's key early-dated linen, the system now points to three objects. Anyone resampling "Gr11Q98" at the IAA by inventory number would get the wrong textile. The IAA number 577250 is the only stable key. The same check should be run on the Fidanzio–Humbert 2016 cave inventory (not in the corpus).
How to confirm or kill it (with data in hand, or what is missing): Data in hand; the checks are text lookups of a born-digital PDF. The remaining question is which Gr number the IAA storeroom label carries. That needs the IAA Organic Materials Unit records (not in the corpus; no request made).
Confidence: high
Touches the Copper Scroll? no (Cave 11Q, not 3Q).

---

FIND CARD
Title (one line): Three open rows of round-1 B6-2 settled with de Vaux's lists and HCM2016. KhQ 1139 is a bowl-type pot of L61 (so NAA App. III is right and App. I/II are wrong), and HC1994 and HCM2016 swap the types of KhQ 1109 and 1112.
Lane: B6
Round-1 link: B6-2 (top-10 #5), finishing its "still open" list.
What is odd (2–4 sentences):
- **KhQ 1286** (QUM 107) is "gobelet" in HC1994 (L65 list) and in HCM2016's L65 catalogue, so NAA App. II's "potter's wheel" is wrong. The next number, 1287, is a "tuyau".
- **KhQ 1270** is not in HC1994's L62 list; it is in L65 ("grand bol"; HCM2016 "grand gobelet"). So App. II's L62 row is wrong.
- **KhQ 1139**: the page photo reads "1109 : jatte … 1112 : couvercle de jarre … 1139 : pot type 1109". So 1139 is a jatte-type vessel from L61. That matches App. III ("Bowl L.61") against App. I/II ("Ovoid lid with handle, L.58").
- New: HCM2016's L61 catalogue, which says its descriptions come "d'après de Vaux", gives **1109 = "couvercle de jarre"** and **1112 = "bol"**. That is the reverse of HC1994, so one of the two volumes has swapped these entries.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HC1994 pp.312–313 = owner's photo IMG_2985 (Drive `1401BKvEtIwrC5Pt1jql0lK7T9mACvrbq`), read from the photo. Private crop: `private2/B6/HC1994_p312_L61_objects_1109_1139_crop.jpg`.
- HCM2016 p.178 (L61 catalogue nos. 12 and 24) and p.219 (L65 catalogue nos. 3 and 4).
- `out2/B6/register_rows_settled.csv`.
Literature check (queries run, result, tag): Same queries as round-1 B6-2, plus a search of the HCM2016 text for 1109/1112/1139. No erratum found. Tag: **NEW TO THE PROJECT** for the settled rows (they complete a NEW TO THE LITERATURE card). The 1109/1112 swap is **NEW TO THE LITERATURE** (minor).
Why it might matter: It closes B6-2 except for KhQ 16/6, and it shows that App. III is not uniformly the worst of the three appendices. The 1109/1112 swap affects any count of lids against bowls in L61, a room of HCM2016's south-east workshop argument.
How to confirm or kill it (with data in hand, or what is missing): The HCM2016 drawings of L61 (Pl. 7, p.179) show whether no. 24 (1109) is drawn as a lid. One page render (`pdf-page …31a119b3 179`) would decide the swap. This was not done for budget.
Confidence: high (readings); medium (which volume swapped 1109/1112).
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): Magen & Peleg 2018 reuse de Vaux's numbers for other things: pools "L17" and "L18" in three captions are L117/L118, and the 2002 graves "T1–T9" duplicate de Vaux's T1–T9. Their "37 graves in the central cemetery" also counts de Vaux's two north-cemetery tombs.
Lane: B6
Round-1 link: new (round 1 did not cross-check M2018).
What is odd (2–4 sentences): Captions Fig. 59 [55] ("pools L17 and L18"), Fig. 95 ("pool L17") and Fig. 96 ("pool L18") [83] name the pools by the round cistern. The text calls them "pools L117 and L118" [82]–[83]. De Vaux's (and Magen's own, [28], [31]–[32]) L17 is a small room and L18 a corridor in the main building. Magen numbers his 2002 graves T1–T9 [99]–[100], in the same series as de Vaux's T1–T9, and on [99] "Tomb 1" means de Vaux's southern-cemetery T1 two sentences before "Grave T1" means his own. "De Vaux uncovered … 37 graves in the central cemetery, and an additional 4 in the southern" [95]: but HC1994 lists de Vaux's Tombe 9 = "Tombe A, cimetière nord" and Tombe 10 = "Tombe B, cimetière nord", so only 35 of T1–T37 are in the central cemetery.
Evidence (exact sources: file path / page / figure / frame / coordinates): M2018 store PDF pp.46 [55], 73–74 [82]–[83], 19 [28], 22–23 [31]–[32], 86 [95], 90–91 [99]–[100]. HC1994 tomb notes (OCR `scratch/B6/h1994_ocr.txt`, "Tombe 9 (Tombe A, cimetière nord)", "Tombe 10 (Tombe B, cimetière nord)"; album captions 449–451).
Literature check (queries run, result, tag): Not searched on the web separately. The collisions are visible only by setting the chapter against de Vaux's lists. Project: "L117" and "Magen" together give no hit on this point. Tag: **NEW TO THE PROJECT** (minor; probably never printed, but too small to claim more).
Why it might matter: The project indexes Qumran features by locus. "L17/L18" from Magen's captions would land on the wrong room. A "T1–T9" citation is ambiguous without the author's name.
How to confirm or kill it (with data in hand, or what is missing): Data in hand. For "L17/L18", kill it if Magen's plan (Fig. 57, labels "M17 … M15") shows that his own "M" numbers are meant; then the captions mix two systems, which is the same problem.
Confidence: high (facts); low (importance)
Touches the Copper Scroll? no

---

## Dead ends

- **M2018 against HC1994 on what de Vaux found.** All of these agree with HC1994:
  - The L13 chimney coins (HC1994 coins 760–762 "sous la cheminée", Agrippa I; 765–767 in jar 764).
  - The L120 silver hoards (HC1994: found "en creusant sous le sol supérieur"; 223 + 185 + 153).
  - Tombs 32 and 33 (bronze ring and beads; two earrings).
  - "Tomb 16 contained two individuals": checked on photo IMG_3004, p.348, "première tombe de Qumrân qui contient deux individus".
  - No card.
- **HF2019 radiocarbon arithmetic.** The two averages are consistent: 200 ± 40 is the weighted mean of 190 ± 50 and 210 ± 60, and 220 ± 30 includes 240 ± 30. The IntCal13 ranges look plausible. Small slips, not carded:
  - p.150 says "Samples 8, 9 and 10" for the Gr11Q9 strings; Table 1 numbers them 8, 10, 11.
  - The Gr11Q9 deposition date varies across the volume: foreword "18th or 19th century"; ch. 6 p.155 "17th or 18th centuries"; Taylor p.139 47.7% in 1724–1815.
- **HF2019 diary and HC1994 on the 1956 tombs 32–37.** The dates match to within a day (diary 8–11 March; HC1994 T33–35 "9–10-3-1956", T36 "10 et 11-3"). Not a find.
- **The B6-1 propagation test in later Gunneweg work.** Wagemakers 2014 (store) has no QUM 209 / Beer Sheba hit. Holistic Qumran 2010 and Bio- and Material Cultures 2006 are not in the store.
- **KhQ 16 vs KhQ 6 (QUM 262, B6-2 row C11).** Still unresolved: neither number is in the HCM2016 text layer, and the HC1994 L-list for the 1951 objects was not read.
- **HC1994 "536" and "351" duplicates** (round-1 lead). Not reached for budget.

## Blocked inputs

- Mizzi 2017 review and de Vaux 1973: still not in the store (`hexview.py pdfs Mizzi` / `pdfs Vaux` → nothing). Not searched on Drive again.
- Fidanzio & Humbert 2016, "Finds from the Qumran Caves" (de Vaux's cave inventory, in Fidanzio ed. 2016, *The Caves of Qumran*): `hexview.py pdfs` lists no copy. A Drive copy of *The Caves of Qumran* is named in brief §2.1 (folder 01) but was not opened (budget).
- `grep` in this shell is a wrapper that silently returns nothing on piped input and on paths under `/home/claude/swarm/scratch`; use `command grep -a`.
