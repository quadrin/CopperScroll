# Tier-1 record HA 28–29 (1969): extraction only

**What it is.** The facts that *Hadashot Arkheologiyot* 28–29 (1969) gives about features inside the phase-2 region, extracted by the phase-3 part-A reader before any coding from this volume. Extraction only: no comparison with any prediction was made. The reader did not open `research/preregistration/arrivals/items/`, the arrival `MANIFEST.md` predictions or `research/assessments/kohlit_chain/chain.json`, and did not search the repository for earlier notes on Tananir.

**Status.** Every report below was first read on 11 October 2026, after the phase-2 freeze (d0f8c7c) and the phase-3 scope freeze (4d8325e): `unexposed at freeze`, `tier1_record`. The integrator compares under `research/preregistration/arrivals/ARRIVAL_PROCEDURE.md`.

**Labels.** EVIDENCE = the volume says it (Hebrew quotes verbatim from the text layer, 12 words or fewer). INFERENCE = the reader's reasoning. Nothing here is a CLAIM of identification.

## Source

| item | value |
|---|---|
| Volume | Hadashot Arkheologiyot 28–29 (portal title "29–28"), 1969, Hebrew, typed; no table of contents; no map references anywhere in the volume |
| Portal | https://publications.iaa.org.il/ha_hebrew_series/64 (PDF https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1063&context=ha_hebrew_series) |
| Local file | owner's Mac, `~/Downloads/IAA portal volumes/IAA_HA_029-028_1969.pdf`, 23,784,617 bytes, 53 PDF pages |
| PDF SHA-256 | `8ded53fb9ed4d98ca0d4e287cbc757537a1b2a4d915cab5fc1501f472b834c28` (matches `../partition.csv`) |
| Text | `pdftotext -raw` (SHA-256 `a67db84ed531aaf1bd15cfce31fbce5f90b8987a00926aad0e3bfec84df119c9`) and `pdftotext -layout` (SHA-256 `631089ce5da3ec46d8522bf70706b72657fa84d6f729ae0cd879651bf25ae06f`), kept on the Mac outside the repository |
| Page numbers | printed page = PDF page − 1 (PDF page 1 is the portal cover) |
| Span hash rule | SHA-256 of raw-file lines a–b, bidi control characters removed, whitespace collapsed to single spaces, UTF-8 |

Text-layer caveat (INFERENCE): `pdftotext -raw` gives the Hebrew in logical order but reverses hyphenated compounds (for example raw "הביזאנטית-הרומית" is "הרומית-הביזאנטית" in the layout text) and moves some punctuation. Readings below were checked against the layout text where order or numbers mattered.

## 1. Kh. Tananir near Shechem (Z1_GERIZIM)

Printed pp. 39–40 (PDF pp. 40–41), raw lines 10510–10761, span SHA-256 `2c2404622661fe2fb3b76a68dd80e0e7732eca83d7a3435aa507dafb4cdede33`. Heading (letter-spaced in the original): "ח' תאנאניר ליד שכם". No author line; no map reference. Located by name only: the text places the site on the lower slopes of Mount Gerizim ("השוכנת בשיפולי הר גריזים"). Zone by name: Z1_GERIZIM (INFERENCE; the spelling "תאנאניר" is a variant of the gazetteer form "תנניר").

EVIDENCE:
- Work: an excavation in October 1968 within the expedition working at Tell Balata (ancient Shechem) on behalf of the American School(s) of Oriental Research in Jerusalem; directed by Dr R. Boling, with researchers and students of the Hebrew Union College, the Dominican Bible school and the British School of Archaeology in Jerusalem.
- The building excavated was first found in 1931 by the German expedition at Shechem and then defined as a temple; its plan, published a year later, drew the American expedition's attention for its resemblance to the Canaanite temple recently found at the Amman (Rabbath Ammon) airport. The excavation confirmed the plan's basic lines as published.
- Dating of the main building: finds on the floors and in the foundation trenches point to the Middle Canaanite (Middle Bronze) II B III period (printed "ב' III"; the first occurrence is garbled in the text layer) and confirm that the building had a cultic character.
- An earlier building lies under the north wall of the "square temple" ("המקדש הרבוע"). **Round pit/cistern:** "באחד משלושת חדריו נחשף בור עגול גדול" — in one of its three rooms a large round pit (בור), partly built of stones and plaster and partly cut in the sloping bedrock. More than half of the lower building has slid down the hillside. By the edge of the pit, a group of jars sealed by the collapse of the building. Jars and fragments of lamps and bowls at the bottom of the pit date the lower building also to Middle Canaanite II B III. No dimensions, depth or orientation are given for the pit. The text does not say whether the pit held water (INFERENCE: "בור" with plaster can be a cistern; the report gives no function).
- **Rock-cut plastered pool:** "נמצאה בריכה מלבנית חצובה בסלע וטוחה" — about 50 m west of the main building ("כ 50-מ' מערבה לבניין העיקרי") a rectangular pool, cut in the rock and plastered, and beside it a levelled rock surface ("משטח סלע מיושר"). No dimensions, depth, orientation or date are given for the pool itself.
- **Small round structure:** a small rounded building, already noted by the German expedition, located about 200 m west of the main building. No dimensions or date.
- The two structures (INFERENCE: the pool with its rock surface, and the round structure) were photographed and planned for excavation in a further season.
- Abundant ribbed sherds, stone tesserae ("קוביות אבן") and wall remains indicate building in the Roman–Byzantine period ("בתקופה הרומית-הביזאנטית" in the layout text). The text does not tie this dating to the pool or to the round structure (INFERENCE: the sentence follows their description but speaks of building on the site generally).
- Not given anywhere in the report: a map reference, any compass direction other than "west of the main building" and "under the north wall", any opening or entrance direction, any measurement other than the two distances (about 50 m and about 200 m west).

## 2. Jerusalem, survey in the village of Silwan (Z4_JERUSALEM_HILLS)

Printed pp. 26–28 (PDF pp. 27–29), raw lines 6989–7462, span SHA-256 `cef645d99ea23169898d0a56da109e5d6afb93d4533fde9e04d372dff2162565`. Heading "ירושלים / סקר בכפר השילוח". Survey by Dr D. Ussishkin (Tel Aviv University) with G. Barkay, for the Israel Exploration Society with the Jerusalem municipality and the National Parks Authority, summer (1968). No map reference; zone by name (Silwan).

EVIDENCE:
- Setting: the village houses stand on the slope east of the Kidron valley opposite the City of David; several near-vertical cliffs run along this slope. "בתקופת הבית הראשון נוצלו מצוקים אלו לחציבת מערות קברים" — in the First Temple period these cliffs were used for cutting tomb caves, probably for the nobles and officials of Judah; the tomb openings were set in the rock face.
- The tombs are empty and ruined today. Damage began in the Roman period; most damage occurred in the Byzantine period (probably 5th–6th centuries CE), when Christian monks lived in them and adapted each tomb as a dwelling.
- Later use: "מערות קברים הפכו לבורות מים בורות ביוב מחסנים ולולים" — after the village was built, tomb caves became water cisterns, sewage pits, storerooms and coops, and some are built into village houses. No dates for these conversions beyond "after the village was built".
- Three groups of tombs: gabled ceiling, flat ceiling, and monolithic. Gabled-ceiling tombs: on the long wall of the burial chamber a rectangular trough-shaped burial bench, with a ledge for a lid along its sides and a cut headrest at its bottom; in two tombs a double trough.
- Three monolithic tombs were surveyed (cut free on their outer sides as well and separated from the cliff):
  - The first, called "Tomb of Pharaoh's Daughter": flat roof today; the survey cleaned the roof and found that the pyramid that stood on it (shown earlier by Avigad) was rock-cut and was destroyed later when ashlars were quarried from it; the quarrying pattern is visible on the roof.
  - The second, with the inscription "...יהו אשר על הבית" (deciphered by Avigad): inside, originally two burial chambers.
  - The third, north of and near the "asher al ha-bayit" tomb, with a fragmentary Hebrew inscription on its facade (found years ago by Reifenberg). About 1.5 m from the village street; "קבור כיום מתחת לחצר ומשמש כבור מים" — buried today under a courtyard and used as a water cistern. Width about 5.25 m; present height about 4.23 m. In front, a rock-cut "plaza" with a step in its centre leading to the opening; another step runs round the facade and seems to continue along its sides. In the centre of the facade a deep niche containing the tomb opening, destroyed beyond recognition in the time of the monks. Above the niche a smoothed surface with the inscription and remains of a projecting cornice; legible fragments include "(זאת קברת)" and "...יהו"; formula and script resemble the "asher al ha-bayit" inscription.
- No orientation of any facade or opening is stated (INFERENCE: the cliffs face west, towards the City of David, from the slope east of the Kidron; the text does not say which way the openings face).

## 3. Jerusalem, "Cave of the Grapes" (מערת האשכולות) (Z4)

Printed p. 28 (PDF p. 29), raw lines 7463–7533, span SHA-256 `3a979abd4ba890fa8efffa3dc693a212677b9ad54cc7248e8b657879421e2b70`.

EVIDENCE: rediscovered about a year earlier, which changed building plans in north-east Jerusalem; exposed in November by the Department of Antiquities with the Ministry of Housing and Solel Boneh. "החזית שהיתה מכוסה באדמה נראית עתה בכל הדרה" — the facade, formerly covered with earth, is now visible, with the carvings at the bottom of the lintel. The interior was not cleaned at this stage. Plan to include it and the nearby caves in a public garden continuing the Sanhedriya garden. No date, dimensions or orientation given.

## 4. Jerusalem, caves in Shmuel ha-Navi Street (Z4)

Printed pp. 28–29 (PDF pp. 29–30), raw lines 7534–7727, span SHA-256 `59cd6974e87560d96e3262e5924e1ac16d386baf7970e9421b7789a8add7baaa`.

EVIDENCE:
- Tomb 1, corner of Shmuel ha-Navi and Yehezkel Streets, found by a tractor driver during foundation work and excavated with the district archaeologist: "זאת מערת כוכים מהטיפוס הנפוץ בסוף ימי הבית השני" — a kokhim cave of the type common at the end of the Second Temple period. "הממצא כלל 19 גלוסקמאות", some with the usual rosette decoration, one exceptional, painted red and blue. Other finds few: a spindle-shaped clay bottle, a juglet fragment and two coins of the procurators of the 50s of the 1st century CE. Part of the large cemetery extending from Mount Scopus towards Sanhedriya.
- Tomb system 2, found recently in the same street: three units; two entered by a side opening, each with two chambers; in one chamber a relatively high ceiling, a lower row of kokhim and arcosolia above them. The third unit has a vertical entrance from the courtyard into a pit closed with a rolling or blocking stone ("בור שנסתם בגולל"). "במקורן שימשו מערות אלו לקבורה בסוף ימי הבית השני"; later turned into dwellings; pottery almost all Early Arab. "הפתח בחצר שימש כבור מים בתקופה האחרונה" — the courtyard opening served as a water cistern in the last period; unclear whether it was earlier a burial entrance or was cut by the cave dwellers. No dimensions or orientation.

## 5. Abu Ghosh, Neolithic site, 1968 (Z4, name only)

Printed pp. 25–26 (PDF pp. 26–27), raw lines 6641–6988, span SHA-256 `bfd253913384d23f195db5adc91ddba3144cbf21bccbc8b1bcea80ab9421dee8`. Heading "אבו-ע'וש 1968" (variant spelling of the gazetteer's "אבו גוש"; INFERENCE).

EVIDENCE: second season, July, French Centre for Prehistoric Research in Jerusalem, directed by G. Dollfus and M. Lechevallier (centre headed by J. Perrot). Four rectangular stone houses in the upper level; trenches; a depression plastered with clay. "נחשפו שלושה שלדי אדם כולם בתנוחה מכווצת" — an adult under the floor of house 1 and two children in house 2. Settlement placed in the 7th millennium BCE, parallel to Pre-Pottery Neolithic B at Jericho. A large trench with Byzantine sherds cut one house. No feature in the window.

## 6. In-region reports with no feature of the eligible classes

- Jerusalem, conservation of the city walls (printed p. 29, PDF p. 30, raw lines 7734–7784, SHA-256 `3f087b0026d674d269bae807bebc1608b9f2eec15a998e8b0e0086958397760c`): north and west walls completed including the Shechem (Damascus) and New Gates; east wall to finish with the Lions' Gate. Walls only.
- Herodium (printed p. 36, PDF p. 37, raw lines 9517–9688, SHA-256 `2db353ecbdbf626fa2ce936777d57d47f0b889b40c9b32fcbca5e4e8d3b5019f`): conservation by the National Parks Authority under G. Foerster of the palace dug by V. Corbo 1963–1967 (east facade of the great peristyle, bath house, frigidarium and its dome); new architectural details in the east of the palace; finds: ostraca with short Hebrew and Greek inscriptions, coins, stone-vessel and glass fragments, many arrowheads and ballista stones. No cistern, pool, tomb or other eligible feature is described.

## 7. Borderline (outside the region by title; listed, not coded)

- Ai (et-Tell), 1968 season (printed pp. 38–39, PDF pp. 39–40, raw lines 10154–10509, SHA-256 `baf564e94a7a48acf0b5d419960a87ef7cb7b4a3eaad6cda3dc22ffede28c41b`): the title names Ai, which is not in the gazetteer (INFERENCE: et-Tell lies at about 31.92 N, 35.26 E, just outside the Z3 and Z4 boxes). The report adds that at Kh. Hudriya ("ח' חיודרייה") an industrial area of a Byzantine monastery was dug north-west of the church found in 1966, and "בואדי עוגיה שבעה קברים" — seven tombs of the Herodian to late Byzantine periods were found and cleaned in Wadi ʿAuja(?) ("עוגיה"). No map reference; the location of these tombs relative to the region boxes is unknown (INFERENCE). Not coded; listed for the integrator.

Other headings in the volume (Galilee, coast, Shephelah, Negev, Hebron hills — Kh. Hatta near Nuba, Eshtemoa, the Machpelah, Khallet el-Ful near Simiya, Emmaus — Samaria/Sebaste, Taanach, Sinai) are outside the region by title; they are listed in `screen.csv`.
