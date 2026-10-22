# Netzer, Meshel & Rosen-Ayalon 1978, *יריחו* (Yad Ben-Zvi), pp. 4–34: NLI library photos, screened reading (21 Oct 2026)

Source: *יריחו* (Jericho), Yad Yitzhak Ben-Zvi, Jerusalem 1978. Colophon: "© כל הזכויות שמורות ליד יצחק בן-צבי, ירושלים תשל"ח-1978". Design: Pati. NLI copy. Pencilled shelf mark on the title verso: **"S 79 A 499"**, and below it "E 113 a".

Contents (p. 3, read in full):

| Title | Author | Starts p. |
|---|---|---|
| הקדמה (Introduction) | – | 5 |
| מקורות (Sources) | – | 7 |
| ארמונות החורף של מלכי יהודה ביריחו – בסוף ימי הבית השני | Ehud Netzer | 12 |
| שני מיתקני ספורט בבקעת יריחו מן המאה הראשונה לפנה"ס | Ehud Netzer | 27 |
| המבצרים השולטים על יריחו וזיהויים | Zeev Meshel | 35 (protected, not opened) |
| נוסייב אל עוישירה | Ehud Netzer | 58 (not opened) |
| ח'רבת אל-מפג'ר | Miriam Rosen-Ayalon | 60 (protected, not opened) |

Photos: the 33 unprotected HEIC originals among IMG_0435–0470, taken on 21 Oct 2026 between 16:07 and 16:15. Each file's Drive ID, SHA-256, capture time and page are in [yericho1978_pp4-34_originals.csv](yericho1978_pp4-34_originals.csv). All 33 SHA-256 values were recomputed and match. The images are not in the repo.

## How this was done

1. A screened reader (a subagent) opened only this book's rows in `nli_photos/sorted.csv` that had an empty `protected` field. It did not open IMG_0446 or IMG_0450 (maps 1–2 sheet / map 2; "possible Sultan strip"), IMG_0465 (p. 35) or IMG_0471–0500 (Meshel and the Mafjar chapter).
2. Every page was OCR'd with `tesseract -l heb+eng`, using the `heb` model added for this pass. Hebrew OCR from these photos is poor, so **every number below was re-read by eye from a zoomed crop of the photo**.
3. The withholding rules were applied while reading. One passage and one name were withheld (see "Withheld").

## What the photos cover

| Part | Pages | Photos | Coverage |
|---|---|---|---|
| Cover, title, title verso, contents | – , 3 | IMG_0435–0437 | complete |
| Introduction | 4–5 | IMG_0438 | complete |
| Sources (Bible, Josephus, Strabo, etc.) | 6–11 | IMG_0439–0441 | complete, except the p. 7 passage withheld under rule 1 |
| Netzer, winter palaces | 12–19 | IMG_0442–0445 | complete text |
| Figures: map 1 (axonometric), map 3 (Pritchard 1951), map 5 legend and plan | 21, 23, 24–25 | IMG_0447–0449, 0451–0459 | complete. Map 2 on p. 22 is protected. |
| Map 4, Herodian palace reconstruction | 26 | IMG_0460 | complete |
| Netzer, hippodrome / theatre | 27–33 | IMG_0461–0464 | complete text and photos |
| Hippodrome comparison figure | 34 | IMG_0466–0470 | complete. p. 35 not opened. |

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = the reader's background knowledge, not from these pages.

### Netzer, "ארמונות החורף…" (pp. 12–19)

The chapter is a Hebrew translation of an article then forthcoming in *BASOR* (p. 12, n. *).

- EVIDENCE (p. 12): Tulul Abu el-ʿAlayiq lies "כ-2 ק"מ מדרום-מערב ליריחו", near the outlet of Wadi Qelt. Excavations began in "ינואר 1973". The site is called "מרכז ארמונות החורף של מלכי יהודה (החשמונאים האחרונים עד הורדוס וצאצאיו)".
- EVIDENCE (p. 12): the best evidence for the development of the oasis is the aqueduct remains. The aqueducts brought water from all the springs, near and far, to the Jericho valley. The springs named are ʿEn Duq, ʿEn Nuʿeima, the three Wadi Qelt springs, and the waters of ʿEn ʿAuja to the north-west. **One further spring name in the same list is withheld under rule 1.** Walls built alongside the aqueducts can still be followed for "קילומטרים רבים" without excavation.
- EVIDENCE (p. 12): the site was chosen for its distance from Jerusalem ("כ-20 ק"מ") and its slight elevation, and for the aqueducts. These were "surely built together with the palace".
- EVIDENCE (p. 13): the Hasmonean palace complex covers "כ-12 דונם". At its centre stood a central building "כ-48×52 מ'". Netzer considers Alexander Jannaeus "(103–76 לפנה"ס)" the most likely builder, pending further excavation. Under Herod the central building was buried under an artificial "platform" (the northern tell).
- EVIDENCE (p. 13): parts of the central building were exposed, mainly on the southern and eastern edges of the tell. They include "בור מים קטן (שהיה במקורו מקורה בקמרון חבית)" and a pair of pools, one stepped and one without steps. These "probably served as a miqveh", "the earliest miqveh yet excavated".
- EVIDENCE (p. 13): the large swimming pool east of the central building "ניזונה ישירות מאמת-המים אשר הביאה לכאן את מימי עין דיוק ועין נועימה". The aqueduct therefore dates by the palace's construction. It enters the pool on its west side, leaves on the east side and continues east to irrigate fields and gardens.
- EVIDENCE (p. 13): the pool's interior is "32.5" by "18" m and "close to 4 m" deep. A 6 m wide "platform" divides it in two. When full, the water covered the platform to "1.2–1.3 m". The descent into the pool is by a broad stair in the SW corner, where the water reached "3.5 m" depth.
- EVIDENCE (p. 14): large plastered and paved terraces surrounded the pool, covering "כ-2 דונם". South of the pool stood a building "(רוחבו כ-21 מ' ואורכו כ-17 מ')", taken to be a pavilion or reception hall overlooking Wadi Qelt.
- EVIDENCE (p. 14): Josephus's account of Aristobulus III drowning at Jericho (*Ant.* 15.3) is said to fit this palace, north of Wadi Qelt.
- EVIDENCE (p. 14): west of the pool lies a small complex with bathing installations and miqva'ot in three building phases. Two are Hasmonean and the last Herodian. The miqva'ot are linked to the needs of palace residents, "שהיו ברובם כוהנים ובחלקם אף כוהנים גדולים", purifying after bathing.
- EVIDENCE (p. 14): some miqva'ot contained concentrations of pottery and other vessels, mostly late Hasmonean, including fish plates and a "קרן השפע"-type vessel.
- EVIDENCE (p. 14): west of the central building is a further small complex built around a pool "8×8 מ'" ("שגם היא ברכת שחייה"), probably for the palace women. It belongs to one of the last Hasmonean stages.
- EVIDENCE (pp. 14–15): east of the complex there is a row of three storerooms, each "31.5" m long and "2.8" m wide. Their relation to the palace is unclear. They may have served the residents, or stored produce of the king's estates, perhaps balsam ("הצרי או האפרסמון").
- EVIDENCE (p. 15): there is a hoard of "20 מטבעות" of Mattathias Antigonus. The coins found mostly belong to Alexander Jannaeus. Antigonus is "המלך החשמונאי האחרון". In "37 לפנה"ס" Herod gained control, and for a time Cleopatra held the valley.
- EVIDENCE (p. 15): Pritchard's 1951 building, south of Wadi Qelt, is taken to be Herod's first palace (a villa used as a "gymnasium"). Wadi Qelt flows for weeks at a time in winter, along a straight stretch "(כ-300 מ')". Herod's second (expanded) palace spans both banks.
- EVIDENCE (pp. 15–17): the expanded palace uses *opus reticulatum* and *opus quadratum*, which Netzer links to Agrippa's visit "בשנת 15 לפנה"ס". It had four wings: three south of Wadi Qelt and one north (p. 16). The large hall of the north wing measures "29" × "19" m, about "540" m², with three rows of columns. The column spacing was "13" m. The hall resembles the Gymnasium hall "(חדר מס' 33)" but is "2.4" times larger (p. 16).
- EVIDENCE (pp. 17–18): there is a sunken garden south of Wadi Qelt (Kelso & Baramki), and a round building on the southern tell with an outer diameter above "16" m.
- EVIDENCE (p. 18): east of the monumental stair to the southern tell there is a huge pool, "כ-40 מ'" wide and "92 מ' (!)" long. It was probably for swimming and water games. Its axis deviates from the palace grid, apparently to fit the topography.
- EVIDENCE (pp. 18–19): Herod built a new, smaller central building on the "platform" over the Hasmonean central building. The Hasmonean pool was then surrounded by gardens, and its paved terraces were covered with earth.
- EVIDENCE (p. 19): the excavations do not support guard towers (Thrax and Taurus) on the two tells. The excavations at nearby Cypros in "1974" exposed Hasmonean remains under the Herodian fortress.
- EVIDENCE (p. 19): the water systems were "long-term" and developed gradually. The authors think they were neglected after the temple's destruction in "70" CE. Pliny is said to allude to a scorched-earth policy by the Zealots, especially in the balsam plantations. The site later became desert, except near Wadi Qelt until the early Muslim period. A 2nd-c. CE "בית אמידים" (wealthy house) was built on the ruins of the expanded palace, north of and near Wadi Qelt. The sentence continues on p. 20, which has no row in the photo index.
- INFERENCE: for entry 29, p. 13 is a primary statement that the Hasmonean swimming pool was fed directly by the ʿEn Duq / ʿEn Nuʿeima aqueduct, with inflow on the west and outflow on the east. It gives no position or level for those openings. This is consistent with the existing note that "the original inlets are lost". These pages describe a single swimming pool divided by a platform. They do not describe two "early Hasmonean pools" (the northern pool, about 18 × 13 m, of the atlas text). That pair comes from later work (Netzer 2001 / Trümper 2018), which these 1978 pages predate.
- INFERENCE: for entry 30, p. 14 calls the palace residents mostly priests, partly high priests, and links miqva'ot to them. This is Netzer's interpretation, not a find of a family name. Nothing names Haqqoz, a "cool room" or a cave.

### Figures (pp. 21–26)

- EVIDENCE: map 1 (p. 21) is an "שחזור אקסונומטרי של ארמון הורדוס ביריחו (הכין ושרטט א' נצר)". It shows Wadi Qelt with built wings on both banks, the sunken garden, the large pool and the round building on the tell.
- EVIDENCE: map 3 (p. 23) is a plan of Herod's first winter palace (the "gymnasium"), after J. A. Pritchard, *The Excavation at Herodian Jericho*, 1951. It has a metric scale bar.
- EVIDENCE: map 5 (pp. 24–25) is the "תכנית מכלול ארמון החשמונאים". The drawings were to be published with the *BASOR* article. Key:
  1. central building
  2. swimming pool
  3. pavilion
  4. terraces on both sides of the swimming pool
  5. colonnaded court (stoa)
  6. miqva'ot complex
  7. group of storerooms
  8. foundations of a Herodian villa (northern tell)
  9. and 10. "אמת-המים העוקפת" (the bypass aqueduct), shown as two dashed lines skirting the complex on the north and west
  11. ritual miqva'ot

  Areas E1–E4 are also marked SE of the complex. The plan has a scale bar and north arrow.
- EVIDENCE: map 4 (p. 26) is a "שחזור תכנית ארמון הורדוס המורחב ביריחו (הכין ושרטט א' נצר)". It labels "wadi Qelt" between the north wing and the southern units: 1 the round building, 2 the sunken garden and 3 the large pool.
- INFERENCE: map 5's items 9/10 make the aqueduct line visible in plan as a bypass around the Hasmonean complex. This 1978 drawing is schematic and has no levels.

### Netzer, "שני מיתקני ספורט…" (pp. 27–33)

The asterisk note says the chapter is reprinted from A. Zimri (ed.), *תרבות הגוף ביהדות*, Wingate Institute, 1977.

- EVIDENCE (p. 27): the Hasmonean palace had a central building "(בערך 45×70 מ')" on two storeys. This conflicts with p. 13's "48×52"; see the note below. A pool unit stood east of it, with an inner size of "18×32,5 מ'" and a water surface of "585 ממ"ר". American excavators (1950) had surveyed it as a "ברכת אגירה" (storage pool). Netzer argues it was a swimming pool for the residents, not storage. The pool was set in paved terraces covering about "1250 ממ"ר". A colonnade about "45 מ'" long ran north of it.
- EVIDENCE (pp. 28–30): this is the "hippodrome complex" at Tell es-Samarat. In late 1976 there were trial trenches with the Ministry of Education. The racecourse is "כ-315 מ'" × "כ-84 מ'". The theatre is "כ-70 מ'" in diameter, with tiers rising about "13 מ'". The raised building ("palatform") is about "70×70 מ'" and stands "10–13 מ'" above its surroundings. A column drum "בקוטר 65 ס"מ" was found. Spectator capacity is estimated at "3,000–4,000".
- EVIDENCE (p. 31): it is compared with the stadium at Sebaste (length "196 מ'", width "63 מ'").
- EVIDENCE (p. 34): the hippodrome figure has a handwritten caption: axonometric of the hippodrome complex, Jericho, 1:1000, with Sebaste below for comparison.

**Internal discrepancy:** p. 13 gives the Hasmonean central building as about 48 × 52 m, while p. 27 gives "בערך 45×70 מ'". Both were checked against crops.

### Introduction and sources (pp. 4–11)

- EVIDENCE (p. 4): the introduction names Kh. el-Mafjar and Tulul Abu el-ʿAlayiq as the prominent excavated sites in the plain. It speaks of fortresses guarding Jericho (Cypros, Doq …), large swimming pools and the hippodrome.
- EVIDENCE (p. 6): a photo caption reads "מטמון מטבעות של מתתיהו אנטיגונוס שנמצא בארמון החשמונאים ביריחו" (the Antigonus coin hoard). The page gives the Hebrew text of Josephus on Jericho, balsam and the palms.
- EVIDENCE (pp. 8–11): there are Hebrew translations of Josephus: Aristobulus III drowned in the pools (*Ant.* 15.3); the balsam (*Ant.* 14.4); Simon, Herod's slave, burns the Jericho palace (*War* 2.4 / *Ant.* 17.10); Archelaus rebuilds the palace and founds Archelais (*Ant.* 17.13; the water-diversion wording was not checked against a crop); and Strabo on Jericho (16.2.41).
- EVIDENCE: the pages say nothing on Kh. Qumran or ʿEin Feshkha.

## What these pages do NOT say

- They give no levels, inlet or outlet positions, pipe junctions or section drawings for any pool.
- They give no plan of the "two early Hasmonean pools" of the entry 29 test.
- They do not identify any house, "cool room" or cave, and do not name the Haqqoz family (entry 30).
- They do not discuss Qumran, ʿEin Feshkha or Doq beyond the one-word mention on p. 4.
- They do not describe the Cypros water system. That is in Meshel's chapter (pp. 35–57), which was not opened.

## Withheld

- **Rule 1, p. 7 (IMG_0439):** the Josephus passage (*War* 4) on the spring by the old city and the Elisha story. It was not read beyond identifying it.
- **Rule 1, p. 12 (IMG_0442):** one spring name in the list of aqueduct sources. Nothing else on that spring was read.
- No other page covered the SULTAN-1 strip. Maps 1–2 / map 2 (IMG_0446, IMG_0450) are protected and were not opened.
- Nothing fell under rules 2–4.

## Still missing

- p. 20 (if it exists: the photo of pp. 18–19 is followed directly by the p. 21 figure) and p. 22 (map 2, protected).
- Meshel, pp. 35–57 (protected). The Mafjar chapter is also protected.
- Notes to the hippodrome chapter (from p. 33; only the heading "הערות" is visible).
