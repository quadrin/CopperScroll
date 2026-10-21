# Hyrcania and the Qumran aqueduct: NLI library photos, screened reading (21 Oct 2026)

Sources:

1. D. Amit, J. Patrich and Y. Hirschfeld (eds.), *The Aqueducts of Israel* (JRA Supplementary Series 46, Portsmouth RI 2002). NLI copy. Pencilled shelf marks on p. 4: "2° 2003 B 2825 copy 2" and "תז 786.5"; a third mark, "163.653", is struck through.
   - J. Patrich, "The aqueducts of Hyrcania–Kastellion", pp. 336–352 (contents p. 6 lists it at 336; Masada starts at 353).
   - Z. Ilan and D. Amit, "The aqueduct of Qumran", pp. 380–386. Fig. 1 is on p. 380; the title and text start on p. 381.
2. צבי אילן (ed.), *מדבר יהודה וים המלח: קובץ מאמרים לכנס הי"ט של החברה להגנת הטבע* (Society for the Protection of Nature, Ein Gedi field school). Typeset ("מערכת והבאה לדפוס") by Yossi Feldman and Lea Eckstein. Library copy with an oval library stamp (illegible) on the title page; no shelf mark visible in the photo.
   - Y. Feldman, "מערכת המים במצודת הורקניה", pp. 326–335. It is preceded by a list of Josephus passages on Hyrcania, pp. 325–326, with no author named.

Photos: 39 HEIC originals, IMG_0626–0654 (17:38–17:44) and IMG_0758–0767 (18:41–18:43), taken on 21 Oct 2026. Each file's Drive ID, SHA-256, capture time and page are in [originals.csv](originals.csv). The images are not in the repo.

## How this was done

1. A screened reader (subagent) chose from `nli_photos/sorted.csv` only the rows for these two books that had an empty `protected` field and were not marked `already_read`. The exception is IMG_0651, marked "already_read (part) / new". The reader converted the HEIC files and read every page by eye from rotated crops.
2. The protected rows were not opened. These are IMG_0659 and 0663 (Jericho maps), IMG_0670–0678 (Netzer & Garbrecht before p. 378) and IMG_0768–0770 (Meshel, Ilan vol. pp. 350–353).
3. Self-check:
   - English pages: OCR (`tesseract -l eng`). Every number below was matched against the OCR text or against a zoomed crop of the photo. The OCR misread the p. 342 dam as "47.5 m long, 45 m wide"; the crop reads 17.5 m and 4–5 m.
   - Hebrew pages: no Hebrew OCR model is installed, so each number was re-read from a zoomed crop.
4. Withholding rules were applied as briefed (see "Withheld").

## What the photos cover

| Chapter | Pages | Photos | Coverage |
|---|---|---|---|
| Front matter: abbreviations, site map, contents | 4–6 | IMG_0626–0628 | contents complete |
| Patrich, "The aqueducts of Hyrcania–Kastellion" | 336–352 | IMG_0629–0650, 0637 | **complete chapter**, all figures 1–28 |
| Ilan & Amit, "The aqueduct of Qumran" | 381–386 | IMG_0651–0654 | complete text. Fig. 1 on p. 380 was not re-opened (read 20 Oct). |
| Ilan vol.: title page | – | IMG_0758 | recto only; no verso or colophon photographed |
| Ilan vol.: Herodium plan (end of previous article); Hyrcania source list | 324–326 | IMG_0759–0760 | complete |
| Ilan vol.: Feldman, Hyrcania water system, with maps on pp. 329 and 330 | 326–335 | IMG_0760–0766 | **complete article** |
| Ilan vol.: Wright, "השרידים הארכיאולוגיים בחירבת מירד", first page | 335 | IMG_0766 | title and first paragraph only |
| Ilan vol.: pp. 348–349 | 348–349 | IMG_0767 | **Not Hyrcania.** It is A. F. Rainey, "מצור מכוור – עדויות ארכיאולוגיות" (Machaerus, from *Eretz-Israel* 10). It was identified, not extracted. |

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = background knowledge, not checked here.

### Front matter (2002)

- EVIDENCE: the site map on p. 4 marks Hyrcania and Dok as "desert palace-fortress" and Qumran as "palace/estate".
- EVIDENCE: contents (pp. [5]–6) lists Patrich at p. 336 and Ilan & Amit at p. 380; Netzer & Garbrecht starts at p. 366 and Hirschfeld (Ramat Hanadiv) at p. 387.

### Patrich 2002, Hyrcania (pp. 336–352)

**History and sources (p. 336)**
- EVIDENCE: the dates are founded under "Alexander Jannaeus (103-74 B.C.)" or John Hyrcanus; destroyed "in 57 by Gabinius"; besieged and taken "in 31 by Herod"; not mentioned after Herod; "In 492, St Sabas founded a monastery"; the monastery was deserted "in the middle of the 14th c."
- EVIDENCE: the remains represent three phases, Hasmonean, Herodian and Byzantine.
- EVIDENCE: Feldman (in 1971) was the first to trace the S aqueduct from the Qidron and to map the cisterns on the E and S slopes with the Survey Department. He showed that the N aqueduct starts at a dam in Wadi Abu Shula, not at Bir el-Amara.
  - n. 5 cites him as: Ilan (ed.), *The Judean desert and the Dead Sea* "(Nineteenth Congress … Tel-Aviv 1974) 316-35 [Hebrew]".
  - INFERENCE: the volume itself prints the article on pp. 326–335. The "316" in n. 5 is a typo.
- EVIDENCE: Patrich surveyed the aqueducts in 1983 for the Map of Deir Mar Saba (109/7). B. Levenstein drew the sections and plans (n. 6).

**Lengths and general route (pp. 336–337)**
- EVIDENCE: the N aqueduct is "the shorter and almost certainly the earlier". It is "1950 m long"; the S aqueduct is "about 9 km". Both are plastered with lime and fine gravel along their whole length.
- EVIDENCE: the channel of the S aqueduct is c. 50 cm wide.
- EVIDENCE: the two aqueducts join "about 750 m west of the fortress". The section c. 500 m west of the fortress crosses friable Hatrurim strata and is masonry-built.
- EVIDENCE: three saddles are crossed on thick supporting walls that act as "three bridges". The line follows the 240 m contour, then drops to the E saddle, which is "48 m lower than the peak of Hyrcania (248 m asl)".
- EVIDENCE: Fig. 1 (p. 337), "Map of the aqueducts to Hyrcania":
  - grid E 178–185 / N 123–126, with a north arrow;
  - points 1–48;
  - a legend for existing aqueduct, projected aqueduct, bridge, support wall over gully, dam, quarry, building and "cave for quarrying";
  - labels Jebel el-Muntar, W. Abu Shaaleh, Mar Saba and the Qidron.

**Phasing (pp. 337–338)**
- EVIDENCE: the lower courses of the E bridge (no. 48) are Hasmonean. At that height the four lower cisterns on the S slope could be filled from the N aqueduct. The Hasmonean bridge was "apparently destroyed" in 57 BC.
- EVIDENCE: Herod built the S aqueduct, raised the E bridge and cut new, higher cisterns on the S and E slopes.
- EVIDENCE: after abandonment the Herodian E bridge partly collapsed, so the Byzantine line could not fill the upper cisterns. The Byzantine works reactivated the N aqueduct, and a short stretch of the S aqueduct "from no. 42", without replastering.
- EVIDENCE: a Byzantine channel runs on the N face of the W bridge (no. 46) and at the head of the E bridge (no. 48). It runs lower than the earlier line and south of it (p. 338).

**S aqueduct, points 1–43 (pp. 338–343)**
- Start (p. 338), EVIDENCE: the line starts on the S bank of the Qidron and crosses to the N bank "after some 1300 m". No diversion dam, regulator or bridge was found at the start.
- Points 1–8, EVIDENCE:
  - pt 2: a wall 1.95 m wide in Wadi Abu el-Kilab;
  - pt 6: a square Byzantine cistern and a round structure with an external diameter of 3.4 m;
  - pt 8: bottom 50 cm (Figs. 2–4, sections at pts 8, 9 and 10).
- Points 9–15 (pp. 339–340), EVIDENCE:
  - pt 9: rock-cut, bottom c. 50 cm, sides 75 cm;
  - pt 11: c. 60 cm at the top and c. 35 cm at the bottom, height c. 75 cm. In the Byzantine period it was blocked, replastered and turned into a cistern, with a settling basin and a run-off dam above. Fig. 5 is a plan with sections.
  - pt 13: a supporting wall 1.3 m high (three courses);
  - pt 14: two drainage apertures; the wall is 2.75 m high above a 15 m drop;
  - pt 15: a wall up to 7 m high (Figs. 6–8).
- Points 16–29 (pp. 340–341), EVIDENCE:
  - pt 16: a wall with "three sluices";
  - pt 17: a rock-cut section c. 3 m long, 50 cm wide and c. 70 cm high;
  - pt 18: a wall 1.75 m wide, perhaps a branch, robbed for Great Laura hermitages;
  - pts 20 and 30: lime-mining caves;
  - pts 23–25: crossing of the vehicle road at a low saddle;
  - pt 29: first bridge, maximum height to the channel 7.5 m, base width 2.5 m. The channel is c. 1.0 m wide at the N end of the bridge and returns to c. 45 cm after 10 m. A guard structure measures 3.2 × 3.2 m.
- Points 33–35, EVIDENCE:
  - pt 33: channel 52 cm wide;
  - pt 34: second bridge, base 2.5 m thick, maximum height above the streambed 17 m (Fig. 9);
  - pt 35: bottom 48 cm, top 60 cm, sides 40–50 cm (Fig. 10).
- Points 36–42 (p. 342), EVIDENCE:
  - pt 36: a terrace wall up to 80 cm high diverting a stream;
  - pt 38: a wall c. 2.5 × 6 m, perhaps a flood-diversion dam (uncertain);
  - pt 40: third bridge, over Wadi el-Eidarawi. The surviving base is 3.6 m wide (2.5 m original plus a 1.1 m addition). The reconstructed bridge was 9 m high and 16 m long. On the N bank the supporting wall partly blocks a natural cave. Figs. 11–13 show pt 40.
  - pt 42: a dam diverting a stream into a secondary branch, "possibly" the Byzantine restart.
- pt 43 (p. 343), EVIDENCE: the junction lies near the W end of bridge 46 and is not visible. A castellum is inferred there; none is visible.

**N aqueduct (p. 343)**
- EVIDENCE, pt 44, the starting dam: "17.5 m long, 4-5 m wide". It lies diagonally across Wadi Abu Shula and diverts water to the S bank. One course is visible, at the edge of a waterfall c. 8 m high.
- EVIDENCE: a cross is cut c. 50 m from the dam, "near a black trail-mark painted on the rock", and a second cross lies further down. They may mean Byzantine re-use of an aqueduct "apparently first built in the Hasmonean period". No Byzantine repairs were seen.
- EVIDENCE, pt 45: a sondage c. 300 m from the dam found Second Temple-type plaster. The channel is "c.1 m" wide, about double the S aqueduct (Fig. 14).

**The three saddle bridges (pp. 343–348)**
- W bridge, pt 46, EVIDENCE:
  - the wall is 2.35–2.75 m thick, at a saddle at 240 m asl, c. 150 m long overall (Figs. 15–16);
  - a lime kiln lies downslope;
  - a Byzantine channel c. 40 cm wide, with reddish sherd-tempered plaster, runs on the N face, which shows that its water came from the Wadi Abu Shula (N) aqueduct.
- Central bridge, EVIDENCE: c. 50 m long; preserved 1.4 m above the surface at the centre; the E end is 2.3 m higher; the supporting wall was over 3.7 m high (pp. 344–345).
- E bridge, pt 48 (Figs. 17–21), EVIDENCE:
  - the saddle was narrowed by quarrying; the total length is 112 m (p. 346);
  - a few lower courses use Hasmonean header-and-stretcher masonry with drafted margins of 8–10 cm and bosses projecting 6 cm. The rest is Herodian, with minor Byzantine repairs.
  - The Herodian channel lay 1.20 m above the present W end and is not preserved. The original height to the channel base was "c.12.5 m". The present height is c. 6 m, base 2.5 m, top 1.45 m (p. 348).
  - Upper arches or a siphon are offered as possibilities.
  - Fig. 17 is an aerial view plus L. Ritmeyer's reconstruction (a reconstruction, not observed fabric).

**Pools (pp. 347–351)**
- EVIDENCE: "The pools to the north and south of the bridge were also created by the quarrying" (p. 347).
- EVIDENCE, N (double) pool, p. 348:
  - two basins separated by a partition 4.8–5.4 m wide;
  - the S basin is up to 2.6 m deep and the N basin up to 5 m;
  - the N pool measures "19 (S) x 15 (W) x 18.2 (N) x 16 m (E)";
  - three rows of rock-cut benches above it suggest a swimming pool. n. 9 compares Jericho: "Perhaps the pools at Hyrcania also date to the Hasmonean period".
  - Feldman's sondages found Second Temple lime-and-gravel plaster; crosses are engraved in places.
  - The pools were supplementary reservoirs; water was carried up to the summit by pack animals.
- EVIDENCE: a round pit NE of the N pool is 3.05 m in diameter and 4.3 m deep, purpose unknown (Fig. 23). Feldman found 3 lime kilns near the fortress. A footpath passes through the rock wall in a rock-cut passage (n. 10).
- EVIDENCE, S pool: a depression with a vertical rock-cut W side and no visible plaster (pp. 348, 351).
- EVIDENCE: "This area with the N pools served as a kind of moat" that cut the fortress off from the western ridge (p. 351).
- EVIDENCE: Fig. 22 (p. 349), "Map of the pools and cisterns around the fortress":
  - grid E 184 700–184 800 / N 125 000–125 200, scale 0–50 m;
  - labels: double pool, hewn benches, pit, southern pool, upper and lower channel, tunnel, cisterns lettered A–T, buried chapel K, ritual baths S, P and F.

**Cisterns (p. 351)**
- EVIDENCE: Patrich cites Feldman for "20 rock-cut cisterns and 2 built pools", with an estimated 20,000 m³:
  - 5 on the hilltop: K1, X, P, L and H. They are not aqueduct-fed; P is vaulted with steps, perhaps a miqveh. n. 11 reports 7th–9th c. papyri found in K1.
  - 8 on the upper S line;
  - 4 on the lower S line;
  - 3 on the E slope.
- EVIDENCE: cave K, "Feldman's 'cistern no.21'", is a Byzantine funerary chapel and probably not a cistern.
- EVIDENCE, by feeder line:
  - the lower S branch feeds J, E, O and N, "presumably Hasmonean";
  - the upper S branch feeds A, A1, M, B, C, D, F and G and ends in a plastered open pool;
  - the N branch of the upper aqueduct feeds S, R and T;
  - the Byzantine aqueduct fed only E and J.
- EVIDENCE: a second built pool with steps lies SW of cistern O (Fig. 24; n. 12, possibly a swimming pool).
- EVIDENCE, **point 49 (entry 16):** "Between cisterns A and N the aqueduct passes through a built tunnel". The free part measures "c.11.5 m in length, height 1.25 m, width 0.75 m". It has a barrel vault and a square opening at the N end; the S end "is blocked by débris" (Figs. 25a–b, p. 350).
- EVIDENCE: cistern S (Fig. 26, captioned "on NE slope") and cistern F (Figs. 27–28, "on the SE slope") are stepped, possibly ritual baths. F carries black crosses and Greek inscriptions from monastic use.
- EVIDENCE: in cistern C, by its steps, Feldman found Herodian lamps and jars and a Herodian coin (n. 13, citing Feldman p. 334). "No later vessels" were found, so the upper cisterns were not used after that period.

**Conclusion (p. 352)**
- EVIDENCE: the system is Hasmonean in origin and peaked under Herod. There are six bridges in all: three on the S aqueduct and three on the shared saddles. The bridges were the "Achilles' heel"; maintenance difficulties were "possibly … one factor in the abandonment of the fortress after the time of Herod".

### Ilan & Amit 2002, Qumran (pp. 381–386)

**Setting and survey (p. 381)**
- EVIDENCE: Qumran has 15 pools and ritual baths totalling "more than 11,000 m³" (citing Wood 1984). The aqueduct collected run-off rainwater.
- EVIDENCE: the aqueduct is "quite short (c.500 m)". The new survey and soundings were made "in 1980-82", on 7 Dec 1980 and 24 Jan 1982.
  - n. 4: de Vaux's 1955 survey, published in Humbert & Chambon 1994, shows "no major differences".

**Intake and dam (pp. 381–382)**
- EVIDENCE: the start is at the next-to-last large waterfall of Nahal Qumran, on a fault line. Basin no. 2 is enclosed by cliffs. Today the channel is first visible at no. 3, where a side gorge comes out on the N bank.
- EVIDENCE: there is "no doubt" that it originally drew most of its water from the main wadi, which drains the Buqeia. It also took cloudburst water from the side tributary (Masada is cited as a parallel).
- EVIDENCE: "No remains of an installation survive". Floods are said to have destroyed every built feature in the bed.
- EVIDENCE: "It seems that a dam was built (fig. 1 no. 4)" to close the basin. Water rose to the channel and was let out from "the N end of the dam".
  - n. 6: unlike the usual low diversion dams, "a more substantial dam must have been built" here because of the difference in levels.

**Branches, tunnels and the cliff stretch (pp. 382–383)**
- EVIDENCE: the rock-hewn channel runs ESE "for some 40 m" along the N bank and then splits:
  - no. 9 winds south;
  - no. 8 runs straight to a shaft and a "short tunnel (5.5 m long)" (no. 10, the west tunnel A). It rises toward the shaft. A tentative function is to drain run-off back west to the junction.
- EVIDENCE: "after another 40 m" comes a crag (no. 11), cut through by "a tunnel, 13.5 m long" (the east tunnel B; Figs. 2–4). The channel then turns NE and runs "c.130 m" along the foot of the scarp, where much of it is destroyed (no. 15).
- EVIDENCE: the channel is lined with white Second Temple-type plaster and is alternately rock-hewn and built on large-block walls (Fig. 5a–b). Cover slabs survive at nos. 12–13.
- EVIDENCE: "opposite Kh. Qumran" it turns at "approximately a right-angle (fig. 1 no. 16)".
- Figure captions:
  - Fig. 2, panorama: "A = the west tunnel, point 10; B = the east tunnel, point 11";
  - Fig. 3: "The east tunnel";
  - Fig. 4: "The E opening of the east tunnel";
  - Fig. 5a–b: built and rock-cut sections against the cliffs;
  - Fig. 6, p. 385: "The aqueduct on the plain";
  - Fig. 7, p. 386: Ritmeyer's reconstruction of the settlement and its water installations.

**Plain and settlement (p. 385)**
- EVIDENCE: the channel descends in a straight line "for more than 200 m". It turns slightly north and then southeast (no. 19) before reaching the settlement.
- EVIDENCE, **the entry-21 wording:** "At its last turn, a wall serving as a kind of low dam was built attached to the aqueduct, evidently in order to catch run-off". The sentence continues "…which descended from the slopes of the scarp and divert it into the aqueduct."
- EVIDENCE: on the plain it is a simple channel with a floor of river pebbles and side stones standing "c.15-20 cm" proud. At the settlement come a settling depression, a plastered chute, a partitioned distribution installation and a pebble-paved incline to the pools.

**Dating (p. 385, "The date of the system, and literary references")**
- EVIDENCE: "The first system may belong to the Iron Age fortress (8th-7th c. B.C.)". A round pool west of the Iron Age tower may have been fed by a channel that was later re-used as the aqueduct's base.
- EVIDENCE: Hasmonean settlers (dated "103-77 B.C.") "presumably built an aqueduct". However, "the aqueduct seen today dates to the final period (about the time of Herod Archelaus, 4 B.C.-A.D. 6)". This is possibly a reconstruction of a Hasmonean aqueduct.
  - n. 7: the authors agree with Magness, *DSD* 2.1 (1995) 58–65.
- EVIDENCE: the pools show two phases: the large S pool was half-filled with débris, and the later main channel runs over that fill.
- EVIDENCE: "The aqueduct and the dam at its inception may well be mentioned in a literary source." Kh. Qumran's Iron Age fortress is identified with Sekaka (Josh. 15:61), citing H. Eshel, *IEJ* 45 (1995).
- EVIDENCE (p. 386): the conclusion reads "The archaeological findings match this evidence well". The chapter is signed "(D.A.)". The scroll-related text is withheld (see below).

### Ilan (ed.), *מדבר יהודה וים המלח*: imprint and front matter

- EVIDENCE: the title page photo (IMG_0758) **prints no year**.
  - It names the editor (צבי אילן), the typesetting by Feldman and Eckstein, and the funders: Tamar regional council, KKL, the Ministry of Education (youth division), the Ministry of Tourism and the Information Centre.
  - The verso was not photographed (the facing leaf is blank). There is no colophon photo.
- EVIDENCE: the latest dates printed in the photographed pages are on the maps: "פברואר 1973" (map drawing, p. 329) and "February 1971" (Survey Department plan, p. 330).
- INFERENCE: the book appeared in 1973 or later. The photos cannot decide between 1973 (the sort label), 1974 (Patrich n. 5) and [1976] (the shelf list). The 19th SPNI congress date (BK, not checked) would settle it.
- EVIDENCE: the plan on p. 324 is not Hyrcania. Its legend reads ארמון-מבצר ההר, ארמון תחתון, מסלול מרוצים, מכלול הבריכה, הבנין המונומנטלי, label "לבית לחם". INFERENCE: it is Herodium, closing the previous article.
- EVIDENCE: pp. 325–326 give "לקט מקורות" for Hyrcania. It contains Josephus passages, two of them on Antipater's burial at Hyrcania (*War* I 33.7; *Ant.* 17.7.1, §187), and Strabo 16.2.40.

### Feldman, "מערכת המים במצודת הורקניה" (pp. 326–335)

**Survey and setting (pp. 326–327)**
- EVIDENCE: the survey began after July 1967, by the Ein Gedi field school. The site, "אל-מירד", covers 20 dunams. Earlier work: Wright, with "משלחת מגילת-הנחושת … באפריל 1960".
- EVIDENCE: the work had three stages: a youth camp on the survey for 10 days; digging in the cisterns for 7 days; and measuring, photography and checks for about 30 days.
- EVIDENCE: the hill rises "כדי 160 מ'" above the Buqeia and about 48 m above the saddle toward Jebel Muntar. Muntar is 524 m high; the Buqeia lies at +80 to −20 m and is 13 km long. The rock is in 4 formations (Bina, Menuha, Mishash, Hatrurim).

**History (p. 328)**
- EVIDENCE: coins found on the site are of John Hyrcanus and Alexander Jannaeus, plus "מטבע מימי הורדוס".
- EVIDENCE: "יש לשער שהמצודה נהרסה בימי מלחמות היהודים ברומאים, במאה הראשונה לספירה". This is stated as a supposition, with no evidence given.
  - INFERENCE: this differs from Patrich, who says the fortress was abandoned after Herod.
- EVIDENCE: the Kastellion monastery was founded in 492. The three periods are Hasmonean, Herodian and Byzantine.

**Inventory (pp. 328–331)**
- EVIDENCE: "24 בורות חצובים ובנויים", about 20,000 m³. They break down as "בריכות פתוחות וגדולות – 3" and "בורות חצובים ומקורים – 21".
- EVIDENCE, the three open pools:
  - (א1) the western pools are about 8,000 m³ (p. 328). Their first use was perhaps as quarries, then as a defensive barrier at the most exposed approach. Trial digs found plaster, although Wright had reported none.
  - (א2) a southern pool, built, at the lowest level, plastered, perhaps a bathing pool, with a later opening in its NW corner (p. 331).
  - (א3) an eastern pool at the E foot, full of alluvium. A channel led to it and pool plaster was found. Feldman suggests it served an army camped below the fortress (p. 331).
- EVIDENCE: the cisterns have up to 3 plaster renewals, with key-marks about 5 cm apart, and "3 בורות לשריפת סיד" (lime-burning pits). One cistern mouth had a plastered settling compartment; upward "פירים" (shafts) are unexplained. Cisterns F and S are small and stepped and were "כנראה" bathing cisterns (p. 331).
- EVIDENCE: the groups are 6 on the summit, 8 on the upper S row, 4 on the lower S row and 3 on the E side. The total is printed "סה"כ 12 בורות".
  - INFERENCE: 6 + 8 + 4 + 3 = 21, so "12" is a misprint for 21. Feldman counts 6 on the summit; Patrich, citing him, says 5.

**Water supply to the fortress (p. 332)**
- EVIDENCE: the surviving built aqueduct west of the fortress could feed only the open pools and the lower S row.
- EVIDENCE: it is "רק קטע משרידי אמה גדולה". Feldman reconstructs it as c. 170 m long and c. 16.78 m high.
- EVIDENCE: the eastern cisterns were fed by gravity along the upper row. The summit cisterns hold little silt, so they were filled "מכלי שני" (by carried vessels) and from roof run-off, as at Masada.

**Northern aqueduct (pp. 332–333)**
- EVIDENCE: it drains the ravine descending from Mt Muntar and is "אורכה כ-1951 מ'". It starts at "נ.צ. 1837 1261" and runs east; the N and S lines share a route from "נ.צ. 1844 1254".
- EVIDENCE: at 1837 1261 there is a dam "שאורכו 17.50 מ' ורוחבו 1.7–4.00 מ'". It is built "בצורת קשת" (curved) and not perpendicular to the flow.
- EVIDENCE: retaining walls reach about 3 m. Near the dam the channel section is 1.45 × 0.65 m.
- EVIDENCE: its purpose was to gather the ravine's run-off. The catchment is "כ-1.2 קמ"ר" (about 1.2 km²). The aqueduct is mentioned in B. Z. Luria's *גלילות במולדת*.

**Southern aqueduct (p. 333)**
- EVIDENCE: it was understood only from aerial photographs. A segment near Mar Saba is marked on the 1:50,000 map; at first it was taken for a monastic supply.
- EVIDENCE: the length is "כ-9 ק"מ". It crosses 6 ravines on retaining walls up to 18 m high.
- EVIDENCE: these walls are not dams; some have culverts ("גשרונים") so that water passes freely beneath.
- EVIDENCE: "השיפוע הממוצע של האמה הוא 2%" (the average gradient is 2%). The route keeps to the Turonian shoulder, is plastered throughout and has a smaller section than the N line.
- EVIDENCE: Kidron floods occur "3–12 פעמים בשנה" and last 2–24 hours (pp. 333–334).

**The three saddles (p. 334)**
- EVIDENCE, by grid reference:
  - 1844 1254: 90.00 m long, maximum height 7.00 m;
  - 1845 1253: 60.00 m long, maximum height 4.50 m;
  - 1846 1252: 170.00 m long, maximum height 16.78 m.
- EVIDENCE: the upper channel's retaining walls were later destroyed and rebuilt much lower, so it could feed only the lower and western pool rows.

**Dating (p. 334)**
- EVIDENCE: there were "לפחות 3 שלבי בנייה": Hasmonean, Herodian and the monastery's.
- EVIDENCE: the N aqueduct came first. Kidron water in the Hasmonean period is possible, "אך לכך אין לנו הוכחות". In the Herodian period the upper aqueduct worked and the upper row of cisterns was full.
- EVIDENCE: trial digs, especially in cistern C by its steps, found lamps, jars and other vessels "רובם מן התקופה ההרודיאנית" and "מטבע הרודיאני נאה". No later sherds were found, so the upper cisterns fell out of use.
- EVIDENCE: in the latest stage the high aqueducts were destroyed and only the N (Muntar) aqueduct was used again. The Kidron system did not operate (pp. 334–335).

**Maps**
- EVIDENCE: p. 329, "הורקניה / מפת תוואי אמת-המים":
  - grid E 179–185 / N 124–128, north arrow, contour interval 25 m;
  - "מיפוי לפי תצלומי אויר – מאי 1953"; drawn by ח. חמילניק, "פברואר 1973";
  - legend: 1 the aqueduct from the Muntar area; 2 the double, two-level aqueduct; 3 the bridge on the great aqueduct; 4 the aqueduct from Nahal Kidron; plus a ridge-line symbol.
- EVIDENCE: p. 330, "הורקניה / תרשים בורות המים סביב המצודה":
  - Survey Department, February 1971; scale 10–0–50 m; grid N 125 000–125 200;
  - labels: "Main Aqueduct", "Upper-Level Aqueduct", "Lower-Level Aqueduct", "Horkania Fort", cisterns A–T (with K1), and the double pool NW of the main aqueduct.
- INFERENCE: this is the base drawing behind Patrich's Fig. 22.

**Other (p. 335)**
- EVIDENCE: the acknowledgements name the Judea-Samaria archaeology staff officer, the IDF, the Border Police, the Survey Department (Musa, Chmelnik, Zion Shatrug, Israel Segal) and hydrologist Dan Marom.
- EVIDENCE: Wright's article follows on p. 335. Its note ** says the 1960 expedition was organised to check sites named in the Copper Scroll, dug in several places "וכמעט ולא העלתה דבר".

## Bearing on entries

- **Entry 16:**
  - EVIDENCE: point 49 in Patrich 2002 repeats the 1989 dimensions (11.5 m free length, 1.25 m high, 0.75 m wide, S end blocked). The 14/40/41-cubit test is unchanged.
  - INFERENCE: the guide's dam "1837.1261" is Feldman's printed reference for the N-aqueduct dam (p. 332).
  - INFERENCE: the guide's "1.2-km line" probably comes from Feldman's 1.2 km² *catchment*, not a length. Both Feldman and Patrich give c. 1950 m for the line.
  - EVIDENCE: Patrich's "black trail-mark painted on the rock" near the cross 50 m from the dam is a modern waymark.
- **Entry 20:**
  - EVIDENCE: dam no. 4 is reconstructed ("It seems that a dam was built"), and "No remains of an installation survive" (pp. 381–382). This is unchanged from 1989.
  - EVIDENCE: the authors' own "low dam" is a different wall, at the last turn (no. 19) by the settlement.
- **Entry 21:**
  - EVIDENCE: the 2002 text describes nos. 2, 3, 4, 8–13, 15, 16 and 19 exactly as the 1989 review does. INFERENCE: the 2002 and 1989 numbering agree.
  - EVIDENCE: the p. 385 sentence confirms Stacey's quotation word for word. But it places the low dam "At its last turn" (no. 19, by the settlement) and links it to no earlier channel or to no. 16.
  - EVIDENCE: "Herod Archelaus" is the authors' date for the visible aqueduct ("about the time of"), with a Hasmonean-reconstruction alternative.
  - EVIDENCE: Cargill's "Iron Age" citation is partly supported. p. 385 says only that the *first system may* be Iron Age.
- **Entry 29:**
  - EVIDENCE: there are now two independent measurements of the northern (double) pool group.
    - Patrich: N basin 19 × 15 × 18.2 × 16 m, up to 5 m deep; S basin up to 2.6 m deep; partition 4.8–5.4 m.
    - Feldman: the western open pools hold about 8,000 m³.
  - EVIDENCE: both report Second Temple plaster from Feldman's sondages. Patrich alone suggests the pools may be Hasmonean.
  - EVIDENCE: the Q49 count discrepancy has a source:
    - Feldman: 24 installations = 3 open pools + 21 cisterns (6/8/4/3; printed total "12");
    - Patrich, citing him: 20 cisterns + 2 built pools, with 5 on the summit.
  - EVIDENCE: Feldman supposes the fortress was destroyed in the 1st-century CE war, but offers no evidence. Patrich says it was abandoned after Herod.
- **Entry 31:** nothing in these pages.
- **Entry 32:** nothing in these pages.

No reading, identification or confidence level is changed by this record.

## What these pages do NOT say

- Ilan & Amit do not tie the p. 385 low dam to an "earlier channel" or to no. 16. They give no point-16 phasing.
- They report no surviving fabric of dam no. 4, and no grid reference or elevation for any Qumran point.
- Patrich gives no gradient for either aqueduct; Feldman's 2% is the only one. Patrich gives no grid reference for any numbered point. The positions come only from the Fig. 1 grid.
- Neither Patrich nor Feldman mentions the long rock-cut tunnels in the wadi cliffs that the owner visited on 20 Oct. The only tunnel either describes is point 49, a built, vaulted tunnel on the S slope.
- Neither reports finds later than Herodian from the upper cisterns, nor any dated activity between 4 BCE and the Byzantine period.
- The Ilan volume's photographed pages do not print its year.
- Ilan pp. 348–349 contain no Hyrcania map. The Hyrcania aqueduct maps are on pp. 329–330.

## Withheld

- Withheld under rule 4, p. 386: Fig. 8 and the adjoining text paragraph (scroll facsimile and reading).
- Nothing was withheld under rules 1, 2 or 3. No cave reports in the held areas, no SULTAN-1 or spring-house material and no Kh. ʿAlmit appear in these pages.

## Still missing

- 2002: p. 380, Fig. 1, was not re-opened. It was read on 20 Oct from IMG_0027–0029 (and IMG_0655). Patrich's notes 7–13 were read only where they bear on the findings above.
- Ilan vol.:
  - the title verso, colophon and contents pages, needed for the imprint year;
  - Wright's article after its first paragraph (pp. 335–?);
  - any page between 336 and 347.
- pp. 350–353 are protected (Meshel) and not opened. The Hyrcania aqueduct map asked for as "pp. 348–349" is in fact on p. 329, which was photographed and read.
- Patrich's chapter ends on p. 352; p. 353 begins Netzer's Masada chapter and was not read.
