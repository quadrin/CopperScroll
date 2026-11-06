# Side-quest round 2, lane B1a (Hadashot at scale, part a: finds mentioned once and never published; unique or unexplained installations), 6 Nov 2026

Worker B1a, round 2. Round 1 covered only HA-ESI vols 116–122. This round used **all** vols 116–137 (4,667 EN reports). Inputs:
- the pdftotext corpus (R2's extraction `scratch/R2/t/hadtext/`, from bucket `hadashot/derived/hadtext_pdftotext.tgz`);
- the ʿAtiqot 41–121 text corpus (bucket `atiqot/text/`, 1,420 files);
- bucket HA PDFs `hadashot/pdf/en/vol-NNN/` (figures read from the PDFs, none fetched from the IAA site);
- ʿAtiqot PDF `atiqot/pdf/vol-110/iss-1/1078_*`;
- the NEAEHL 5 page store (`hexview.py`);
- D3's `refs_raw.json`;
- Natural Earth 10 m admin-0 polygons.

Scripts are in `scripts/`. Data:
- `ha_unread_inscriptions_followup.csv`;
- `ha_westbank_polygon_by_volume.csv` and `ha_westbank_polygon_deep.csv`;
- `ha_uniqueness_claims_all_vols.csv` (319 sentences);
- `ha_pending_study_sentences_all_vols.csv` (109 sentences).

---

FIND CARD
Title (one line): The "Second Temple" Hebrew sherd incised before firing from Thiede & Lass's Moẓa dig (HA 117, id 147) fits Tel Moẓa's Iron Age group of jar inscriptions incised before firing. The publication of that group (ʿAtiqot 110, 2023) counts four and does not mention it.
Lane: B1a
Round-1 link: B1a-1 (Moẓa unread inscription). This card adds a second witness and a testable re-dating.
What is odd (2–4 sentences): In round 1 the sherd was an isolated "Second Temple" oddity. It is not isolated. Sindel & Misgav (ʿAtiqot 110, 2023) publish two jar inscriptions in ancient Hebrew script, "engraved … in the fresh clay prior to firing", from fills at the foot of Tel Moẓa. With Vainstub's two from the tell (excavated 2003, published 2009), they treat these as a closed group: "all four inscriptions" were "engraved on the vessels prior to firing", 7th c. BCE, a "new category of ownership inscription, found so far only in Moẓa". Thiede's sherd has the same rare technical trait and comes from the same site, two years earlier (A-3472, 2001). Its fill is about 0.3–0.4 km from the tell excavations. The next-door 2024 dig (Moẓa Area J, id 26581, 215550/633255) found redeposited Iron Age II finds, including a warrior figurine, as well as Early Roman ones. The 2023 article does not cite Thiede, Lass, HA 117 or the sherd. No source located here has linked them. The only stated date ("Second Temple") comes from a report published after Thiede's death that names no epigrapher. The Hebrew body text calls the inscription "blurred".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HA: `hadtext/en/vol-117/00147_mo-z-a.txt`, the L7 paragraph and caption 5 (`Images//3472-5.jpg`; private copy `/home/claude/swarm/private/B1a/moza_HAESI117_id147_fig5_IAA.jpg`). It prints map ref NIG 21550–70/63320–30.
- ʿAtiqot: `atiqot/text/vol-110/iss-1/1078_from-nasas-to-semakhyahu-two-new-engraved-inscriptions-from.txt`, abstract and pp. 24–29: "all inscribed on jars before firing"; "found at the tell in 2003"; Figs. 2–3 (PDF pp. 7–8). The reference list has no Thiede.
- NEAEHL 5, Moẓa entry (store `Stern-ed-1993-2008-…-1b9b4740`):
  - p. 423: Thiede & Lass dug 2000–2003 "west of the Crusader building". The tell's stratigraphy has Iron IIC (7th–early 6th c. BCE) and then Hellenistic, with no Early Roman stratum on the spur.
  - p. 425: the two Hebrew inscriptions "lspn bn nss and [ln]ss lsmkyh[w]".
- Distances, from the printed map refs:
  - Thiede (≈215600/633250) to Tel Moẓa (id 10582, 215478–667/633510–784): ≈0.4 km.
  - Thiede to the Byzantine farmstead directly south of Sindel's 2021 trench (id 25536, 215696–712/633505–18): ≈0.28 km.
  - Thiede to Area J (id 26581): ≈0.05 km.
Literature check (queries run, result, tag):
- Corpus: of the 17 Moẓa reports in HA (`scripts/ctx.py`), none but 147 mentions the sherd. ʿAtiqot 41–121: only art. 1078 deals with Moẓa inscriptions, and it does not cite it.
- Repo main and branch_only: no "Sindel", "Semakhyahu" or "Nasas". Thiede appears only in the haesi_features coding.
- Web queries:
  - "\"Moza\" OR \"Motza\" Thiede Lass excavation inscribed sherd ostracon Hebrew \"before firing\"": only the 2023 article (cris.huji.ac.il) and unrelated items came back.
  - "Thiede \"Zeitschrift für Antikes Christentum\" 2004 Emmaus Moza Ostrakon": Wikipedia and Emmaus pages only.
  - academia.edu/31136736 (BAIAS 23 scan): the body cannot be read through WebFetch.
- Tag: **NEW TO THE LITERATURE** (the link and the re-dating question). The sherd itself is NEW TO THE PROJECT (round 1).
Why it might matter: If the sherd is Iron Age, it is a fifth member of a group that the 2023 authors call unique to Moẓa, and their formula and scribe analysis (three scribes, "routine procedure") gets another test case. If it is truly Second Temple, it is a rare example of the technique in that period. In either case it needs an epigrapher, which it never had.
ARGUMENT (kept apart from the evidence): The strongest point is the prior. Hebrew inscribed before firing is the signature of Tel Moẓa's Iron Age II workshop. The site's Iron Age material is redeposited downslope, and Iron Age II finds were redeposited at Area J next door. The "Second Temple" label is unsupported, and it fits the excavators' Emmaus agenda. My non-expert look at the photo: deep, angular grooves, including a zigzag (W-like) group at the top. This fits engraved paleo-Hebrew letter forms and does not exclude Jewish script. I make no claim about the reading.
How to confirm or kill it (with data in hand, or what is missing): Compare IAA photo 3472-5 with ʿAtiqot 110 Figs. 2–3 and Vainstub 2009 Fig. 5.11 (IAA Reports 39; not in the store). Points to check: letter forms, groove profile, and fabric (are all on jar handles?). The card dies if an epigrapher reads the sherd in Jewish (square) script, or if BAIAS 23 (2005) or CIIP IV.1 already reads it as Second Temple. A full kill needs the object (IAA stores, excavation A-3472, L7).
Confidence: high that the link is unmade in print (as far as searched); low–medium that the sherd is Iron Age.
Touches the Copper Scroll? no.

---

FIND CARD
Title (one line): A ledger of 16 HA-ESI reports (2004–2025) that announce an inscription as "not (yet) deciphered". Four were read later (one 14 years on, in ʿAtiqot 117), and about ten still have no reading in later HA reports, ʿAtiqot 41–121 or the web checks run. They include a Latin milestone on the Lod–Neapolis road (dug 2005) and a rolled lead "curse tablet" from ʿAkko (dug 2003).
Lane: B1a
Round-1 link: new. Round 1 swept only vols 116–122, and B1c's "will be published" sweep only vols 130–137 (12 hits, no follow-up check).
What is odd (2–4 sentences): I swept every EN report for an inscription noun near "not (yet) deciphered / undeciphered / indecipherable / illegible / enigmatic / still being studied", without coins or stamped handles (`scripts/unread.py`). Then I checked each hit for a later reading: in later HA reports at the same site, in ʿAtiqot 41–121 (site and object proximity search, `scripts/atqchk.py`), and on the web.
- Read later:
  - ʿAvedat Nabataean tabula ansata. HA 123 (2011) "not yet been deciphered"; dug 1999; published by Pogorelsky & Abudraham, ʿAtiqot 117 (2025), 26 years after the dig.
  - Shivta Latin metal seal. HA 132 (2020); Eck & Tepper, SCI 40 (2021).
  - ʿUyun Umm el-ʿAzam Syriac/Aramaic. CMHL entry.
  - ʿAkko marble fragment with Hebrew letters. Unread in the HA 131 preliminary (2019); three letters read by Misgav in the HA 133 final (2021).
  - Probably published: the Hazor 2006 cuneiform tablet (title match only).
- Still unread (no reading located):
  - Rantis (NW) milestone with a Latin inscription (HA 123, dug May 2005 on the Lod–Neapolis Roman road).
  - ʿAkko, Ha-ʿAmal St rolled lead tablet. "Indecipherable incisions" in both the preliminary and the final; the final likens it to curse tablets.
  - Tel Dor (NE): Greek inscription on a dressed stone inside an unfinished shaft (dug 2017).
  - Jerusalem, 2 St George St: Greek inscription under plaster on Pillar 14 (dug 2011).
  - Shuʿfat survey: Latin tabula ansata, three lines of three letters, over a burial cave (2011).
  - Ḥorbat Zerifin: jar lid with Arabic, on a lid type "unknown from other sites".
  - Ẓippori marble slab with Greek letters.
  - East Talpiyot: three letters in a kokh.
  - Maʿagan Mikhael B: stringer with Greek letters and "Allah".
  - Newe Yam: hieroglyphic Seshat stone, known only from press reports.
Evidence (exact sources: file path / page / figure / frame / coordinates): `ha_unread_inscriptions_followup.csv`, one row per object, with the HA wording, excavation year, later-HA check, ʿAtiqot hit and web result. Key texts:
- `hadtext/en/vol-123/01826_rantis-northwest.txt` (Table 1, basket 106 "an inscription"; Fig. 7 = `Images//4407-7.jpg`);
- `en/vol-133/26039_akko-ha-amal-street.txt` (Fig. 13; "Similar tablets, identified as curse tablets") and `en/vol-131/25582_akko.txt`;
- `en/vol-133/26023_tel-dor-northeast.txt` (Square 39 paragraph, shaft L134);
- `en/vol-130/25393_jerusalem-the-old-city.txt`;
- `en/vol-124/02194_jerusalem-shufa-t-survey.txt` (Fig. 6);
- positive controls: `atiqot/text/vol-117/iss-1/2255_a-new-nabataean-funerary-inscription-from-avedat.txt` and the reference "Eck W. and Tepper Y. 2021 … SCI 40:145–150" in `atiqot/text/vol-110/iss-1/1083_not-a-signet-ring-of-pontius-pilatus.txt`.

I read the IAA figures of the Rantis milestone (4407-7) and the Shuʿfat lintel (S-316-6) from the bucket PDFs. At web resolution neither can be read, so I attempted no reading. The images were not copied out.
Literature check (queries run, result, tag):
- Web queries:
  - "Rantis Roman milestones Latin inscription excavation Elisha 2011 Antipatris Gophna road milestone" (packhum, JRS milestone of AD 69, IIP Caesarea: none is Rantis);
  - "\"רנתיס\" \"אבני מיל\" OR \"אבן מיל\" כתובת לטינית" (nothing on Rantis);
  - "Akko Acre lead curse tablet rolled defixio found excavation Tepper Ha-Amal Street" (nothing on ʿAkko);
  - "Tel Dor northeast mausoleum Roman shaft Greek inscription stone Golan Ratzlaff excavation 2019" (only the HA record on Brandeis scholarworks);
  - "Newe Yam underwater Seshat hieroglyphic inscription stone 2021 Sharvit Egyptian" (press 2020 only: ancient-origins, ABC);
  - "Hazor cuneiform tablet 2006 season …" (Horowitz & Oshima, "Two Late Bronze Age Tablets from Hazor", keibi KEI00011148).
- Repo: Rantis appears only in toponym and HA title lists; none of these objects is coded.
- Tag: **NEW TO THE PROJECT** (the follow-up ledger). Each object is already published by HA as unread, so the claim is about follow-up, not existence.
Why it might matter:
- The Rantis milestone is the strongest single item. A legible Roman milestone gives an emperor and a date for the road phase at the place where the report says the Lod–Neapolis road bypasses the Antipatris swamps. The report also says the stones were reused in post-Roman maintenance. It has sat unread for 20 years after the dig.
- The ʿAkko lead tablet would be one of very few curse tablets from Ptolemais.
- As a dataset, the ledger shows that HA "not yet deciphered" is an end state as often as a stage. Only 4–5 of 16 were followed up, and one of those took 26 years from dig to reading.
How to confirm or kill it (with data in hand, or what is missing):
- Kill a row by finding its reading. Corpora not in the store: CIIP I and IV.1, IIP, the Fischer–Isaac–Roll milestone corpus (*Roman Roads in Judaea* II, 1996, which predates the dig), and SEG 2018–2025.
- For Rantis, check Isaac & Roll's later milestone notes and *Scripta Classica Israelica*.
- For ʿAkko, check the ʿAkko volumes and SEG.
- The search was by keyword. It misses unread inscriptions described without these words; Moẓa ("enigmatic") was caught only because "enigmatic" was in the list.
Confidence: medium (the per-row "no reading located" is limited by which corpora the web reaches); high for the positive-control rows.
Touches the Copper Scroll? no.

---

FIND CARD
Title (one line): Round 1's untested kill test, run: a West Bank polygon test that ignores report text confirms R2's corrected pattern. HA-ESI vols 117–128 (2005–2016) hold only 4 field reports more than 3 km inside the West Bank, out of 2,907 with a usable map reference (0.14%). Vols 129–136 hold 17 of 1,301 (1.3%), and vol. 116 holds 4 of 72.
Lane: B1a
Round-1 link: B1a-3 (SOA gap), as corrected by R2 (WEAKENED: gap = vols 117–128; return from vols 129–130).
What is odd (2–4 sentences): Round 1 and R2 both counted SOA reports by text markers. A marker count misses reports that print no permit, and a misprinted coordinate does not affect it. This test uses only the printed map reference. It is converted from NIG/OIG to WGS84 (pyproj, EPSG:2039) and tested against the Natural Earth 10 m "Palestine" (PSX) polygon. I dropped points within 3 km of the polygon edge, because the polygon is coarse and many Green Line sites (Jatt, Ibthan, Shaʿar Efrayim) fall on it. I also dropped a Jerusalem box. I removed by hand the rows D3 already flags as map-reference errors (244, 631, 638, 682, 980, 997, 8518, 24845) and municipal Jerusalem (758, 686, 1510, 1612, 1801). The genuine deep West Bank reports per volume are then:
- 116: 4;
- 117: 1 (Qumran Plateau);
- 118–121: 0;
- 122: 1 (Emanuel Cave);
- 123–124: 0;
- 125: 1 (Naḥal Tirẓa);
- 126–127: 0;
- 128: 1 (Tel Ḥevron);
- 129: 2 (ʿEn Perat, ʿEli);
- 130: 2 (Efrat cemetery, Shaqed NW);
- 131: 0;
- 132: 4 (two Qumran, Naḥal Ḥaẓaẓon, Givʿat Zeʾev);
- 133: 2;
- 134: 0;
- 135: 3;
- 136: 4;
- 137: 0.

The text-free method reproduces R2's corrected break, at about one tenth of the later rate, and it finds no hidden cluster of West Bank reports that the marker counts missed.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `ha_westbank_polygon_by_volume.csv` (all PSX hits per volume, including edge points);
- `ha_westbank_polygon_deep.csv` (more than 3 km inside, with ids and titles; coordinates not reproduced);
- script `scripts/gl.py` (inputs: `/home/claude/swarm/scratch/D3/refs_raw.json`, `baseline/reports_metadata.csv`, `ne_10m_admin_0_countries.geojson` from github.com/nvkelso/natural-earth-vector);
- 4,403 EN reports parsed, 34 unparsable.
Literature check (queries run, result, tag): As for round-1 B1a-3 and R2 (no published statement found of an HA policy on Judea & Samaria reports). Tag unchanged: **NEW TO THE PROJECT** (probably known to specialists).
Why it might matter: It removes the main objection to the round-1 card, that the marker method could miss SOA reports. The gap is real in publication years 2005–2016. Following R2, it is not a gap in excavation years: excavations of 2005–2014 surface in vols 129–130.
ARGUMENT (Copper Scroll consequence): The project's HA-based negative evidence is weak for any West Bank candidate area for excavations still unpublished in 2025. Those areas include Qumran and Feshkha, Jericho, the Buqeiʿa, Nebi Musa, Ibziq and the Kidron/Hyrcania desert. Examples are the "silence" in `haesi_features` and the 24 Oct hoard follow-up. Across 2004–2025, HA holds only 25 deep-West Bank field reports, and 8 of them are in the Qumran/Ḥaẓaẓon/es-Samra/Mazin corridor (vols 117, 132, 135, 136). Before 2020, the online HA corpus is essentially blind east of the Green Line. A negative result there should carry little weight against a scroll candidate, unless it is backed by JSP volumes, the SOA archive or WBADB. This lowers the value of HA silence; it does not favour any particular candidate.
How to confirm or kill it (with data in hand, or what is missing): Replace Natural Earth with the official 1949 armistice line (not in the store) and drop the 3 km buffer. The card dies if the near-edge band (`by_volume` file) holds many genuine West Bank field reports in vols 117–128. On inspection it is dominated by Green Line villages inside Israel.
Confidence: high (for the corrected pattern).
Touches the Copper Scroll? maybe (it weakens HA negative evidence at West Bank candidate places; see ARGUMENT).

---

## Dead ends

- Garden Tomb glass cylinder seal (round-1 B1a-2), three further web searches:
  - "Ornan glass cylinder seal \"Garden Tomb\" …"
  - "Ornan \"Sin of Harran\" crescent standard seals …"
  - Hebrew "\"גן הקבר\" חותם גלילי זכוכית זלינגר"

  No publication was found. One lead is untested: Koch 2018, "New Light on the Glyptic Finds from Late Iron Age Jerusalem and Judah" (in *New Studies in the Archaeology of Jerusalem* 12, ed. Uziel, Gadot, Zelinger et al.). It is the likeliest place the seal was catalogued, and it is not in the store. Status is unchanged from round 1.
- Moẓa BAIAS 23 (academia.edu/31136736) through WebFetch: the body is still unreadable (CamScanner scan); see card 1.
- Corpus-wide "first / unique / no parallel" sweep (319 sentences in 279 reports, `ha_uniqueness_claims_all_vols.csv`). I checked six claims against the corpus or a final report:
  - Be'er Sheva North "first Second Temple underground complexes in the Be'er Sheva Valley" (26275): not contradicted. The nearest candidate, Railway Line 25705, is Hellenistic.
  - Yafo Magen Avraham "no parallels for this installation" (23799, HA 127, 2015): the ʿAtiqot 100 (2020) final calls it a composite winepress and cites a parallel at Tel Ḥefer published in 2009. The literature already corrected it.
  - Nofekh/Ramla Arabic zir handles, Rahat, Yeroḥam, Ḥorbat Zerifin lids: not testable from the corpus.
- Join of HA uniqueness and unclear-function claims to ʿAtiqot finals by permit (`scripts/join.py`, 54 claims in 43 reports): too noisy. My ʿAtiqot permit index also matches page and figure numbers. The only clean case is Yafo, above.
- Khirbat el-Qut "hoard of Bar Kokhba-period coins discovered nearby (E. Kogan-Zehavi, pers. comm.)" (26229; B1c open lead):
  - none of the 49 Kogan-Zehavi HA reports mentions it;
  - web "Ramat Beit Shemesh hoard Bar Kokhba coins Kogan-Zehavi": the MFA hoard is Naḥal Shalva/Qiryat Gat, already published;
  - the JPost 120-coin hoard is the Frumkin–Zissu–Eshel cave "near Betar, within the Green Line", which is not an IAA find.

  Still open. It was not carded because nothing beyond the pers. comm. exists.
- Ḥorbat Zerifin "c. 10 jar lids of a type unknown from other sites" (814): no other HA report describes such lids. Not testable further.
- Pending-study sweep (109 sentences, `ha_pending_study_sentences_all_vols.csv`): apart from the inscriptions in card 2, the hits are illegible coins, "in preparation" used in its ordinary sense, and pers. comm. citations.
- Polygon by-product: the deep West Bank false positives 24845 (Moẓa Taḥtit, northing 663184 for 633184), 682, 244, 631, 638, 8518 and 997 are map-reference misprints or EN/HE conflicts. All are already listed in `out/D3/FINDS.md` and `ha_mapref_errors.csv`. They are left to B1b and B1c.

## Blocked inputs

- `https://www.academia.edu/31136736` (BAIAS 23, Thiede–Lass–Lewis 2005): WebFetch returns only the citation and "Scanned by CamScanner"; the body cannot be read.
- Vainstub 2009 (IAA Reports 39, *Salvage Excavations at Tel Moẓa*) and Koch 2018 (NSAJR 12): not in Drive or the bucket page store (`hexview.py pdfs` shows neither).
- CIIP I and IV.1: not in the store (CIIP IV.2 and III only).
- No official Green Line polygon in the repo or the store. I used Natural Earth 10 m PSX (coarse) instead, with a 3 km buffer.
