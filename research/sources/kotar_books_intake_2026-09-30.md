# Three Kotar books: site leads and tests — 30 September 2026

## What they add

The strongest results are a correction to the evidence for Sekakah, several explicit Kidron canyon boundaries to test against entry 35, and a cave shortlist that separates early Roman material from later revolt evidence. The books also identify older shoreline measurements and photographs worth recovering. None identifies a Copper Scroll deposit or warrants a change to the current site ratings.

This is a targeted visual review of the supplied scans, not a full reading or transcription of all three books. The ZIPs contain 720 JPEG pages in total. Printed page numbers below were checked on the scans; image numbers refer to the locally extracted files. Original research notes and factual records are published here; book scans remain in the local research collection.

## Sources and coverage

| Source | Relevant material inspected | Local image sequence |
| --- | --- | --- |
| **P — פרח בר במדבר: מסע ומסה במדבר יהודה**, *Ariel* 186 (2009), [Kotar 99363677](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=99363677) | Roi Porat, Hanan Eshel, Uri Davidovich and Amos Frumkin, “מערות המפלט מימי מרד בר כוכבא במדבר יהודה — גילויים חדשים”: title and pp. 8–28, including distribution map and photographs | `perach/009.jpg` title; pp. 8–28 = `010.jpg`–`030.jpg` |
| **G — מדריך ישראל החדש, כרך 13: מדבר יהודה ובקעת ים המלח** (2001), chief editor Sefi Ben-Yosef, [Kotar 75901013](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=75901013) | Contents/index; site sections pp. 63, 79–86, 114–117, 128–129, 148, 176–177, 194–195 | Inspected printed pages correspond to image number +3; e.g. p. 176 = `guide13/179.jpg` |
| **D — ים המלח ומדבר יהודה 1900–1967** (1990), edited by Mordechai Naor, *Idan* series, Yad Ben-Zvi, [Kotar 84772311](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=84772311) | Tzipora Klein on shoreline changes, pp. 29–45; end of Magen Broshi's manuscript survey, pp. 203–206; Yehuda Ziv, “חקר מערות מדבר־יהודה”, pp. 207–220 | pp. 29–45 = `deadsea/035.jpg`–`051.jpg`; pp. 203–220 = `213.jpg`–`230.jpg`. Offset changes elsewhere in the book. |

The local accession and structured feature records are in [`kotar_book_leads_2026-09-30.json`](https://github.com/quadrin/CopperScroll/blob/main/registration/kotar_book_leads_2026-09-30.json). Paths there are for the current workspace; they are not downloadable copies of the books.

## 1. Sekakah: remove a circular name argument

**Source evidence:** G p. 176 explicitly explains that the modern Nahal Sekakah name comes from the proposed biblical settlement identification. It calls the Arabic stream Wadi Abu Shuʿla and gives competing settlement proposals, including Qumran and Khirbet Qumr Ismar. The stream eventually joins Nahal Qumran at source grid `1910.1272`.

**Inference:** a modern map label “Nahal Sekakah” is not independent attestation that the Copper Scroll's Sekakah was Qumran. It inherits an identification already under debate. This extends the [dependency audit of entries 20–23](https://github.com/quadrin/CopperScroll/blob/main/research/sites/qumran_cluster_dependency_audit_2026-09-30.md): a place name copied onto a modern stream must not be counted as a second witness.

The same section identifies useful physical features separately:

- **Bir el-Amara**, source grid `1831.1265`: large cistern with ancient stone troughs, G p. 176. The guide describes surviving features but does not give a secure construction or use phase for each trough.
- **Dam**, source grid `1837.1261`: dressed stone, diverting runoff into a built aqueduct on the south bank, G pp. 176–177. The continuation explicitly assigns it to **Hyrcania's northern water system**, dated broadly to Hasmonean and Herodian times, and gives a length of 1.2 km.
- **Stepped tunnel north of Hyrcania**, roughly 30 m deep, and a second blocked tunnel about 300 m away, G p. 177. The guide states that the function is uncertain and mentions comparison with Mithraic tunnels. That comparison is an interpretation, not proof of date or purpose.

The dam is a geographically specific feature lead, but it supplies Hyrcania in this account. It cannot be reassigned to Qumran merely because the modern stream carries the name Sekakah. The 1.2-km guide length also differs from Patrich's reported 1.95-km northern line in the existing notes. Determine measured endpoints and surviving versus reconstructed length before treating that difference as a contradiction.

## 2. Kidron: test canyon boundaries, retaining the textual alternatives

Entry 35, VIII 8–9, in the project's edition-based rendering, puts a cairn at the mouth of the Kidron gorge and specifies digging three cubits. The existing [reading notes](https://github.com/quadrin/CopperScroll/blob/main/text/readings.json) preserve three separate uncertainties:

- **יגר:** stone heap/cairn (Milik C77 p. 245; Puech 2015 pp. 72–73) versus a dam interpretation (Eshel, *Copper Scroll Studies*, pp. 101–102).
- **צוק:** gorge in Milik D28 p. 268 and Puech 2015 p. 73, versus “peak” in Lefkovits 2000 p. 262.
- **קדרון:** Kidron versus readings understood as pottery, recorded by Puech 2015 p. 73 nn. 299–300.

G pp. 194–195 describes successive canyon and basin sections rather than one continuous undifferentiated gorge. These are **guide anchors**, not deposit coordinates:

| Boundary | Source grid exactly as printed | Test |
| --- | --- | --- |
| Entry into the Mar Saba canyon section | `1808.1259` | Compare with the “before Mar Saba from Jerusalem” interpretation; this is a canyon entrance. |
| Southern end of that canyon, near the Small Lavra ridge | `1819.1227` | Test an outlet interpretation of “mouth”; it is not automatically the edition's chosen endpoint. |
| Transition into Hyrcania basin | `1839.1225` | Control the open-basin interval and reject models that silently treat it as canyon. |
| Start of the lower steep canyon | `1897.1213` | Separate the lower canyon's entrance from its outlet. |
| Kidron stream outlet, G p. 194 | `1925.1201` | Regional anchor for the eastern outlet model; not a surveyed cairn or the exact cliff-exit feature. |

G p. 195 also prints grave el-ʿAjami at `1882.1213`. Preserve that reading for map checking rather than moving it to make the described itinerary fit. Grid interpretation, feature assignment and source cartography need verification before conversion to WGS84.

**New spatial test:** compare the upper canyon entrance and outlet with the lower canyon entrance and outlet. For the cairn reading, seek an independently documented period stone heap beside an accessible path at each boundary. For the dam reading, seek the dated intake of Hyrcania's **southern Kidron** line; the Abu Shuʿla dam above belongs to the northern system in the guide. Keep the peak and pottery alternatives outside the Kidron-gorge model.

Three cubits would be about **1.34–1.58 m** under the project's working range of 0.445–0.525 m per cubit. This is a conditional digging depth, not a search radius. No particular heap, surface datum or excavation position is established. The guide narrows the comparison into explicit alternatives; entry 35's exact stretch remains unresolved (Q34).

## 3. Cave leads: dates, water and access before resemblance

P pp. 8–9 reports mapping/describing more than 400 caves, principally along the escarpment between Qumran and Ein Gedi. That is survey coverage, not 400 matched Copper Scroll candidates. The article distinguishes availability, size, access, water proximity and concealment. Most refuges were emergency adaptations; a subset had cut pools, plaster or other preparation.

| Feature lead | Evidence reported | Why follow it / what it cannot establish |
| --- | --- | --- |
| **Christmas cave, lower Kidron** — P pp. 22–23 | Relatively accessible entrance; second-year Bar Kokhba coin, two late Second Temple bronzes and two Hasmonean prutot; authors infer use in both revolts | Best immediate cave lead for checking early material in the already relevant Kidron sector. Mint dates do not date deposition. It is not reported as entry 35's cairn. |
| **Coin cave and neighboring Kidron caves** — P p. 22 | Bar-Adon excavations in 1970/1976; shepherd reuse; nearby caves with Agrippa I/Hadrian coins, Roman lamp and pottery | Recover cave numbers and original find contexts. Keep “in a neighboring cave” distinct from “in Coin cave.” |
| **Salvadora cave / photograph label 143** — P pp. 18–19 | Early Roman material; Bar-Adon's 1971 excavation described as unpublished in 2009; finds recovered from a rock fissure | Original field records could reveal fissure geometry and find context. A hiding fissure is a feature class, not a Copper Scroll identification. |
| **Te'enim complex** — P pp. 20–21 | Western cave: early Roman pottery and Herodian lamp fragment. Southern cave: spear placed in a narrow crack, interpreted as short Bar Kokhba use | Preserve separate cave identities and phases. Combining the early lamp and later spear into one deposit would manufacture a match. |
| **Romah complex and Naqb el-Mardeh** — P pp. 15–17 | Five caves; third-year Bar Kokhba coins and occupation material; aerial photograph marks paths and cave clusters | Stronger as an access/path comparison than as period evidence for the earlier scroll. Need survey plans and dated path evidence. |
| **Dinar cave** — P p. 18 | Easy access relative to neighboring cliff caves, small walls, third-year revolt coin and weapons; authors consider lookout/ambush use | Useful comparison showing that a coin-bearing cave need not be a prolonged refuge. No dated scroll-period installation demonstrated. |
| **Har Yishai / Cabar complexes** — P pp. 25–26 | Early Roman material together with later revolt evidence; plaster/retaining remains at some features | Separate installation dates from occupant dates and trace inherited Bar-Adon observations before claiming independent corroboration. |

The distribution map on P p. 11 is schematic, without adequate survey control for entrance coordinates. The photographs can identify terrain and source relationships; they do not justify precise map pins.

**Source dependence:** P p. 22 reproduces the Christmas cave entrance photograph from Allegro's *Search in the Desert* cover (1965). A visual match to that cover locates the same photographic witness; it is not an independent second observation. Likewise, “unpublished in 2009” is a historical access lead, not a claim that the excavation is still unpublished in 2026.

D pp. 208–209 and 213–216 describes both looted caves and substantial finds surviving in previously searched caves. Concealment, difficulty of access and earlier survey history therefore cannot be used alone to predict an intact deposit or total exhaustion. D p. 211's Cave 40 at ʿEd-Zefzefa also has a roofed rainwater cistern; its refuge context is later and must not be collapsed into a First Revolt feature.

**Recommended model:** extract cave identity, entrance/access route, internal water installations, find locus, and each dated occupation separately. Test route feasibility only after matching an actual entry's landmark terms. These regional leads have no assigned scroll-entry match yet.

## 4. Old landscape records: recover measurements, audit the reconstruction

Klein's chapter supplies concrete archival targets:

- **PEF/Masterman measurements, 1900–1913**, with a horizontal rock benchmark near Ein Feshkha; **H. Koppe's 1917 height calibration**, D p. 33.
- **Rujm el-Bahr**, shoreline/jetty photographs discussed across 1936–1970, D p. 38. Recover original dates, camera positions and elevation datum before fitting a shoreline.
- D p. 45 notes differing datum offsets. Datum differences that seem minor in a regional history can matter in a feature-level elevation comparison.

These are records of the **modern historical** landscape. They can help register older photographs and separate shoreline recession from changes to paths or structures. They do not directly give a first-century shoreline.

**Conflicting reconstruction:** D pp. 41–44 proposes a rise from roughly −400 to −330 m during Herod's reign, drawing on an aragonite-like band at Qumran and historical interpretation. The chapter also records de Vaux's alternative explanation of the white band as plaster/whitewash. The claimed date and water origin are not independent direct observations.

A later study, **Bookman, Enzel, Agnon and Stein (2004), GSA Bulletin 116:555–571, DOI 10.1130/B25286.1**, reports a late Holocene range of about **−390 to −415 m**, based on 46 radiocarbon ages. Its [university-hosted abstract](https://cris.huji.ac.il/en/publications/late-holocene-lake-levels-of-the-dead-sea/) was checked; the complete paper and individual first-century samples were not reviewed here. That reported range conflicts sharply with the older −330-m scenario. Exclude that scenario from the present location models; obtain the dated sample/elevation table before constructing a period shoreline envelope.

## 5. Next discriminating work

| Priority | Concrete work | Evidence that would change the assessment |
| --- | --- | --- |
| 1 | Recover Christmas/neighboring Kidron cave numbers, entrance plans and find loci; start from P pp. 22–23 and Bar-Adon's cited surveys | A named, positioned early Roman feature matching an entry; later finds alone do not pass the period test. |
| 2 | Register the four Kidron canyon-boundary alternatives against the source map and period routes | A dated cairn/heap or southern-aqueduct intake at a text-compatible boundary. A nearby Byzantine monastery does not date the landmark. |
| 3 | Compare the guide's Abu Shuʿla dam and 1.2-km line with Patrich's northern line and the supplied aqueduct volume | Common endpoints and construction phases; helps avoid conflating northern and southern systems. No equation to entry 21 without a separate textual and geographical argument. |
| 4 | Trace Salvadora 1971 and separate Te'enim cave records | Original fissure/cave plans plus early contexts; a repeated overview is not an independent confirmation. |
| 5 | Recover the PEF benchmark, Koppe calibration and original Rujm el-Bahr photographs; obtain Bookman et al.'s sample table | Controlled modern image registration and a dated ancient shoreline envelope with datum and uncertainty. |

LLMs can help align Hebrew/Arabic/English names, extract figure and archive references, and test mutually incompatible interpretations. Every proposed match should keep a visible chain: **entry reading → required feature → source observation → date → position → independent check**. Leave missing links empty. The structured records include explicit next tests rather than assigning unsupported identification scores.

## Effect on the atlas

Qumran entry 21 remains medium and conditional on Sekakah; Hyrcania remains possible/low; entry 35's precise Kidron stretch remains open. No cave entrance or hiding-place point is added to the map. The new raw guide grids are source locators awaiting verification, not WGS84 coordinates. This report corrects the evidence accounting and makes the next tests more specific.


## Additional contents and access check — 30 September 2026

The Kotar contents for this volume also list “מעיינות המרפא והמרחצאות באזור ים המלח” (Dead Sea healing springs and baths), beginning at printed p. 84. The reader reached a subscription/account gate at that page; its text and illustrations remain unread. The title supplies a possible water-source research lead, without evidence for a specific Scroll feature. The earlier cave article's coverage remains unchanged.
