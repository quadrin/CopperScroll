# Side-quest B3, round 2 (Epigraphy and names): finds, 6 Nov 2026

Round 2 builds on `out/B3/FINDS.md` (cards B3-1 to B3-3) and on R3's review of them. New inputs used here:
- the Hadashot text corpus (`hadashot/derived/hadtext_pdftotext.tgz`, English, vols 116–137): 38 reports mention Maresha;
- the IIP EpiDoc source (`github.com/Brown-University-Library/iip-texts`, HEAD 0b7dc83, 17 Jul 2024; 5,536 files);
- the Avigad 1962 page images in Drive folder `19KtN_mcIKYHpfg631Ps-IHtjeWh7d2Zm` (p01–p16, read through the connector's OCR);
- Naveh 1974 (Drive `10GXLYLzxPkDP_Q4MGT1JvkyIdfWsYdAW`);
- Haber & Gutfeld 2024 (Drive `1G0Ytg3tyh1JVCQVX1P6z4TqHEuU6AeTS`).

Page conventions:
- *Maresha IV* "pdf p." is the bucket page number (slug `Stern-2025-Maresha-IV-Subterranean-Complexes-IAA-Reports-76-db5921ab`).
- CIIP IV.2 "pdf p." is the bucket page number (slug `Ameling-et-al-eds-2018-Corpus-Inscriptionum-Iudaeae-Palaesti-75db1ea8`; printed = pdf + 746).

Data files in this folder:
- `sc57_sc126_witnesses.csv`
- `iip_records_sited_SC57.csv` (65 rows)
- `avigad1962_concordance.csv` (11 ossuaries)

---

FIND CARD
Title (one line): The SC 57 → SC 126 renumbering was printed in 2014, in the Hadashot report that CIIP IV.2 itself cites. Yet CIIP (2018) kept "SC 57" in 3504, 3511 and 3733, and IIP still files 65 records of the complex under "Subterranean Complex 57".
Lane: B3
Round-1 link: B3-1 (Heliodorus complex SC 126 not SC 57). This card adds the 2014 witness, CIIP's own use of it, a room-by-room proof that HA 119's "SC 57" is SC 126, and how far the error spread in IIP.
What is odd (2–4 sentences): Round 1 rested the renumbering on *Maresha IV* (2025) alone. R3 also doubted whether the "(126)" in the 2014 chapter title was added afterwards. But the excavators' own HA-ESI 126 report on SC 169 (Stern & Alpert, 26 Nov 2014) says SC 57 is "to be referred to in subsequent publications as Subterranean Complex 126" and then writes "Subterranean Complex 57 (126)". CIIP IV.2 cites that same report three times: Marisa introduction n. 50, viewed 24.5.2017; 3675 "fig. 2"; and 3737, which takes its ed. pr. from figs 6–7. The 3737 inscription is described in the sentences right after the renumbering. Even so, CIIP has 0 occurrences of "Complex 126", and the IIP source files give locus "Subterranean Complex 57" to all 65 records drawn from BAR S2652. Those are 38 Aramaic/Phoenician (Eshel), 15 Greek pottery (Ecker & Korzakova) and 12 amphora stamps (Finkielsztejn).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HA-ESI 126, report 12643, `en/vol-126/12643_maresha-subterranean-complex-169.txt` l. 83–90: "…in the direction of Subterranean Complex 57 (… to be referred to in subsequent publications as Subterranean Complex 126)" and "proximity to Subterranean Complex 57 (126)". Map ref. of SC 169: 190560/611070.
- HA-ESI 119, report 00499 (Alpert & Stern, 15 Mar 2007), `en/vol-119/00499_maresha-subterranean-complex-57.txt`. Its description matches *Maresha IV*'s SC 126 (pdf pp. 195–196) room by room:
  - four rooms;
  - Room 1: "a tunnel was quarried on the southern side" (*Maresha IV*: "blocked burrow on the southern side … towards SC 169"); it holds the Attic-Greek inscribed fragments, i.e. the stele;
  - Room 2: "small banister";
  - Room 4: round, "resembles a water cistern", 24 stairs and a banister, quarrying marks (*Maresha IV*: "circular staircase and a banister … final functions … quarries").
  Real SC 57 in *Maresha IV* (pdf p. 120) is a single round columbarium with a ceiling shaft. HA's Room 4 "has neither a shaft in the ceiling".
- CIIP IV.2, Marisa introduction n. 50 (pdf p. 197, printed 943). 3675 Findspot (pdf p. 378): "HA-ESI 126, 2014 fig. 2 [… id=12643 …, viewed 13.10.2016]". 3737 Bibl. (pdf p. 454): "HA-ESI 126, 2014 (… id=12643 …, viewed: 13.12.2016), figs. 6 (ph.), 7 (dr.) (ed. pr.)". SC 57 used in 3504 (pdf p. 203), 3511 (pdf p. 210: "Subterranean Complex 57. The complex is located about 100 m to the southeast of the Maresha acropolis … four rooms … Room 1") and 3733 (pdf p. 450).
- IIP: `epidoc-files/mare0001.xml` … `mare0064.xml` (incl. 0018a/b), `<geogFeat type="locus">Subterranean Complex 57</geogFeat>`. Sources IIP-658/659/660 = BAR S2652 pp. 71–75, 77–94, 95–101 (`data-keep/iip-zotero-export.xml`). List: `iip_records_sited_SC57.csv`.
- Map references for the same complex (published, protected national-park site): HA 119 E 190551 N 611000; *Maresha IV* "611031/190665" (northing first), i.e. E 190665 N 611031, 118 m apart (see Dead ends).
- Witness table: `sc57_sc126_witnesses.csv`.
Literature check (queries run, result, tag):
- Web queries: `"Subterranean Complex 126" Maresha Stern Alpert 2014 "Subterranean Complex 57" renumbered Heliodorus`, plus round 1's and R3's queries. They returned the BAR pages, Wikipedia, IIP and press, and nothing that flags 126.
- Repo (main + branch_only): "Complex 126" and "SC 126" give 0 hits (R3), and "12643" and "to be referred to" give 0 hits.
- Tag: **KNOWN BUT UNDER-DISCUSSED** for the renumbering, which the excavators published in 2014. **NEW TO THE LITERATURE** for the facts that CIIP cited the announcing report without adopting it, and that all 65 IIP SC-57 records are affected. I found no publication that says either.
Why it might matter: Anyone placing the stele, the Sohemus/Ilaeus altar, the Abselamus graffito or the 65 ostraca, stamps and inscribed sherds on the Maresha plan through CIIP or IIP lands on Macalister's columbarium. R3's caveat is removed: the number 126 does not rest on *Maresha IV* alone, and the 2014 date is confirmed by the excavators' own report.
How to confirm or kill it (with data in hand, or what is missing): Data in hand: open the two HA texts and *Maresha IV* pdf pp. 120 and 195–196. The kill test is the HA 119 plan (`Images//4099-1.jpg`, not in the text corpus) against *Maresha IV* Plan 2.126: if HA's four-room plan is not Plan 2.126, the identity fails. The plan image itself was not opened here. Missing: BAR S2652.
Confidence: high
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): The Agathocles weight from SC 97 is one object in three publications (Maresha III 161 no. 3 = CIIP 3679 = *Maresha IV* ch. 3 no. 3). *Maresha IV* gives its 2022 redating two different ways (SE 200 = 113/112 vs 112/111), and the director's own 2021 report still put the end of Maresha at c. 107/6 BCE.
Lane: B3
Round-1 link: B3-3 (Agathocles weight 205 vs 200; Sosibius 201), which R3 weakened.
What is odd (2–4 sentences): R3 weakened B3-3 because *Maresha IV* never names Agathocles, so the object's identity was only probable. HA 135 (Stern 2023) closes that gap. It cites the SC 97 "inscribed lead weight" as "Korzakova 2010b:161, No. 3", and CIIP 3679 (SC 97, courtyard east of Room 3) gives its ed. pr. as "Korzakova, Maresha III 161 no. 3". The dating is not stable inside one volume. *Maresha IV* printed p. 26 says Finkielsztejn (2022:86–90) "corrected his reading to 112/111 BCE", which equals SE 201, and adds that the latest sealing of the SC 89 archive is SE 201. Printed p. 248 says the same series was "redated to the year 200 SE, i.e. 113/112 BCE". Two years earlier, the same director's HA 133 report stated that "the terminus ante quem date for the abandonment of Maresha has been established as c. 107/6 BCE".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HA 135, report 26380 (Stern, 30 Aug 2023), `en/vol-135/26380_maresha-subterranean-complexes-97-and-99.txt` l. 67–68 and reference l. 114 ("Korzakova H.B. 2010b. Lead Weights", Maresha III, IAA Reports 45).
- CIIP IV.2 3679 Bibl. (pdf p. 383): "Korzakova, Maresha III 161 no. 3 (ed. pr.). – Finkielsztejn, ibid. 175f., 185-9, table 8,1 no. 3". CIIP 3675 Sosibius Bibl. (pdf p. 379): "Korzakova, Maresha III 163 no. 7". So both weights sit in one 2010 catalogue, with Finkielsztejn's table 8.1 as the chronology.
- *Maresha IV* pdf p. 37 (printed 26, Stern): SE 205 "temporarily revised … equivalent to 108/107 BCE. However, Finkielsztejn later (2022:86–90) corrected his reading to 112/111 BCE. This also corresponds with the date of the latest sealing (SE 201= 112/111 BCE) … in SC 89".
- *Maresha IV* pdf p. 259 (printed 248): "redated to the year 200 SE, i. e. 113/112 BCE … dating the conquest itself to 112/111 or 111/110".
- HA 133, report 26015 (Stern, 30 Jun 2021), l. 38–40 ("c. 107/6 BCE") and l. 121 ("after the Hellenistic period/107 BCE").
Literature check (queries run, result, tag):
- INR 17 (2022) page (lockwoodonlinejournals.com/index.php/inr/article/view/2838): paywalled, USD 20; the abstract names no years.
- Web search `Maresha lead weight agoranomos Sosibios OR Sosibius year 201 112/111 Hyrcanus conquest Finkielsztejn Agathokles`: only the INR abstract, Finkielsztejn 1998 and catalogue pages.
- Repo: no hit for "Korzakova" or "26380".
- Tag: **NEW TO THE PROJECT** (each statement is published; the join and the internal mismatch are not, as far as I can find).
Why it might matter: The identity is now certain, so B3-3's point (a) should be restored. On *Maresha IV*'s own p. 26 the latest dated objects are SE 201: the SC 89 sealing, and CIIP 3675 Sosibius from SC 169. That supports R3's reading that the "last series" wording on p. 248 is loose rather than a chronological conflict. The real open point is which numeral Finkielsztejn 2022 reads on the Agathocles moulds, 200 or 201, because the volume says both. Whoever cites "the last weights" for Hyrcanus' conquest of Maresha should cite Note C directly.
How to confirm or kill it (with data in hand, or what is missing): Missing: the full text of Finkielsztejn, INR 17 (2022), Note C, pp. 86–90. If it reads SE 201 on the Agathocles series, p. 248 is the slip; if it reads SE 200, p. 26 is. Maresha III (IAA Reports 45) is not in the corpus (Drive search "Maresha" in PDFs gives only HA reports). With it, table 8.1 would show the 2010 order of Agathocles and Sosibius.
Confidence: high (identity, and the two printed dates); medium (that it is a slip rather than a weight-date / conquest-date distinction)
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): Avigad 1962 × IIP × the CIIP index: the nine inscribed ossuaries of the Karm esh-Sheikh tomb, joined. Rahmani/IIP reads Horea six times where Avigad has five, ends Arristobola differently, and leaves Alexander's ossuary (the only one at the Hebrew University) without measurements or provenance.
Lane: B3
Round-1 link: round-1 dead end/blocked item (Avigad 1962 × CIIP I.1). CIIP I.1's lemma text is still blocked (see below), so this card uses the two witnesses that can be reached.
What is odd (2–4 sentences): Avigad states the following.
- Ossuary No. 9, Alexander son of Simon with the bilingual lid QRNYT, "is at present at the Hebrew University (Inv. No. 1965)"; the others went to the PAM (p. 4).
- Horea is written "5 times—3 times on front, twice on rear" (p. 8).
- Arristobola (a) is ΑΡΡΙΣΤΟΒΟ[ΛΑ] with "the last two letters faded" (p. 4).
- The boxes are 27–32 cm high (p. 4).
IIP's records for the tomb come from Rahmani's *Catalogue of Jewish Ossuaries* (IIP-119, pp. 101–104), which covers only State collections. In those records:
- Horea has six instances, the sixth a third line on the back read [Η]ω[ρ]α (jeru0064);
- Arristobola (a) is read Ἀρριστοβού[λα] (jeru0058);
- Aristobula's box is 25.5 cm high and Jacob's 37 cm (jeru0058, jeru0065);
- Alexander's ossuary is a separate, later record (jeru0489) entered from Avigad only, with no dimensions and an empty provenance element.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Avigad 1962 page images, Drive folder `19KtN_mcIKYHpfg631Ps-IHtjeWh7d2Zm`: p04 (`1kmwTjoWRAoW0M6iYuRES3nsDDN67HFEQ`: ossuaries, sizes, No. 9 at HU Inv. 1965, inscription 1), p05, p06, p07, p08 (`1EbVF1Wpb04URiHc3VfVkVYjpH6k0HUas`: Horea 5×), p09–p11 (Alexander, Jacob), p12 (conclusion).
- IIP `epidoc-files/jeru0058.xml`–`jeru0065.xml` (bibl IIP-119 = Rahmani, CJO) and `jeru0489.xml` (bibl IIP-689 = Avigad 1962, "insc 08").
- The CIIP index numbers 324–332 come from round 1 (Drive sheet `CIIP_CPJ_names`). Order: 324 Alexander, 325 Aristobula/Sorra, 326 Horea, 327 Jacob, 328 Mnaso, 329 Philiskos, 330 Sabatis/Damon, 331 Sara a–c, 332 Thaliarchos a–b.
- CIIP I.1 front matter (connector text, `scratch/B3/ciip1_1.txt`): Akeldama is nos. 288–311 and "Kidron Valley (Centre and South)" starts at p. 337. So 324–332 fall in the Centre/South Kidron chapter, which agrees with Avigad's "south of Silwan … south-western slope".
- Full join: `avigad1962_concordance.csv`.
Literature check (queries run, result, tag):
- Web: `Avigad 1962 IEJ 12 ossuaries Kidron "Philiskos" OR "Thaliarchos" Cyrene inscription` returned IIP jeru0489, BAS and catalogue pages; no comparison of the two readings.
- Repo: names Thaliarch*/Philisk*/Sabatis/Mnaso hit only the W2D Ilan lists; `registration/avigad1962_kidron_ossuaries_extracted.md` has no IIP or Rahmani join.
- Tag: **NEW TO THE PROJECT**. The readings are published by Avigad (1962) and Rahmani (1994); the differences are stated here for the first time as far as I can find. I could not check whether CIIP I.1 comments on them.
Why it might matter: CIIP I.1 nos. 324–332 will have had to choose between the two readings. The concordance gives the keys (Avigad ossuary and inscription numbers, CIIP number, IIP ID, CJO page) needed to check them as soon as the CIIP text is readable. It also explains why IIP has the "Alexander son of Simon" ossuary, the item most often linked to Simon of Cyrene (Mark 15:21), as a thin stand-alone record: the box was never in the State collection that Rahmani catalogued.
How to confirm or kill it (with data in hand, or what is missing): Data in hand: Avigad Fig. 10 / Pl. 3A (p08 and the plates p13–p16) against Rahmani's reading of the back of the Horea box. The 6th instance can be judged only on a photograph of the rear. Missing: CIIP I.1 nos. 324–332 (blocked), and the Rahmani CJO pages themselves (not in the corpus; IIP is a secondary witness to them).
Confidence: medium (that the readings differ: high; which reading is right: open)
Touches the Copper Scroll? no (Avigad's tomb was already checked against entry 56 in `registration/avigad1962_kidron_ossuaries_extracted.md`; nothing here changes that)

---

FIND CARD
Title (one line): The only Second-Temple inscription from Hyrcania (Naveh 1974; IAA 70-313) is missing from the 2024 excavators' survey of the site's inscriptions. Wikipedia, citing CIIP IV.1, dates it "second or first century CE", but Naveh dated it to the first half of the 1st century BCE.
Lane: B3
Round-1 link: new (round 1 listed CIIP IV.1 / Naveh as not attempted)
What is odd (2–4 sentences): Naveh published two fragments of a carefully cut monumental Aramaic inscription in Jewish script from Kh. el-Mird. Visitors had picked them up and handed them in (reg. no. 70–313). They have letters about 17 mm high and at least four lines, and read ]מנפא[ … ]חבל[ … ]א דכל[ … ]למרת אי[ … ]לנפשנא קדם הר[. Naveh restored "before Hyr[canus]" or "Hor[od]", suggested a tomb inscription of an important person, and recalled that Herod buried Antipater at Hyrcania. Palaeographically he preferred "the first half of the 1st c. BCE" (pp. 56–57). Haber & Gutfeld 2024 report the first season at Ḥorbat Hyrcania and list the site's inscriptions (Mader's Greek inscription, the 1952 papyri, the 2023 Greek and Kufic finds), but they never mention this one. Naveh is absent from their text and bibliography. Wikipedia's "Hyrcania (fortress)" cites CIIP IV.1 pp. 619–628 and dates the "two pieces of a Jewish monumental stone inscription" to "the second or first century CE". IIP's source file has the same CE wording in its date label ("2-1 c. CE") while encoding notBefore −0200 / notAfter −0001. IIP's live page shows "2-1 c. BCE".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Naveh, ʿAtiqot (Hebrew series) 7, 1974, pp. 56–57 and Pl. XV:8 (Drive `10GXLYLzxPkDP_Q4MGT1JvkyIdfWsYdAW`, PDF pp. 2–3): fragment sizes c. 12 and 22 cm (n. 2), letters c. 17 mm, line spacing c. 15 mm, dating paragraph on p. 57.
- Haber & Gutfeld 2024, *New Studies in the Archaeology of Jerusalem* 17 (Drive `1G0Ytg3tyh1JVCQVX1P6z4TqHEuU6AeTS`; text kept at `scratch/B3r2/haber2024.txt`): no "Naveh", "CIIP" or Aramaic stone inscription. The only Aramaic items are the Christian Palestinian Aramaic papyri.
- CIIP IV.1 contents (connector text): "LXXVIII. Hyrcania (Castellion, mod. Kh. el-Mird) nos. 3209-3214 … 619". The lemma text is blocked (see below).
- IIP `epidoc-files/kmir0003.xml` l. 79–80: `<date notBefore="-0200" notAfter="-0001" …>2-1 c. CE</date>`. Dimensions 13.5 × 6.7 × 5 cm, which match neither of Naveh's fragment heights (c. 12 and 22 cm). Bibliography: Naveh 1974 only. Live page https://search.inscriptionsisraelpalestine.org/inscriptions/kmir0003 shows "2-1 c. BCE".
- Wikipedia raw text, `Hyrcania_(fortress)`, fetched 6 Nov 2026 (`scratch/B3r2/hyrc_wiki.txt` l. 86), with the CIIP IV.1 citation.
Literature check (queries run, result, tag):
- Web queries: `Hyrcania Khirbet el-Mird Aramaic monumental inscription Naveh 1974 tomb Hasmonean "Hyrcania" inscription CIIP 3209`, and `"Hyrcania" Aramaic "monumental" inscription "Jewish script" … "first century BCE" … Naveh Mird`. Results: IIP, Wikipedia mirrors, and 2023 press on the Psalm inscription. Nothing notes the date conflict or the omission.
- Repo: Naveh 1974 appears only in the Drive indexes and one Koḥlit coding packet; no note uses it, and "second or first century CE" gives 0 hits.
- Tag: **NEW TO THE LITERATURE** for the date conflict between Naveh and Wikipedia/IIP and for the omission in the 2024 report. The source of the "CE" (CIIP IV.1 itself, or a slip by Wikipedia/IIP) is open.
Why it might matter: It is the only epigraphic trace of the Hasmonean/Herodian fortress, and the new excavation is the natural place for more fragments to turn up. Naveh himself said more fragments could settle the restoration. A CE date would wrongly make it evidence of Jewish monumental activity at Hyrcania in the 1st–2nd c. CE.
ARGUMENT (scroll consequence, kept apart from the evidence): Hyrcania is a low-rated candidate for entries 16, 29 and 35 (`tables/phase3_places.csv`: Eshel restores "to Hyrcania" in entry 16). The project's own note sets "in use 1st c. BCE; after Herod 'seems to have been abandoned' (Patrich)" against Eshel's 1st-c. CE garrison. If the Wikipedia/IIP-label date were believed, this inscription would count for Eshel's side. On Naveh's dating it does not; it adds nothing to the 1st-c. CE case. The word לנפשנא does not help entry 2 (נפש "monument", I 5) either: Naveh weighs the "nefesh = tomb marker" sense and prefers "for ourselves". Net effect: neutral for 16/29/35, with one possible false positive removed.
How to confirm or kill it (with data in hand, or what is missing): Missing: CIIP IV.1 pp. 619–630 (nos. 3209–3214). If CIIP dates the stone to the 2nd–1st c. CE, the conflict is between CIIP and Naveh, not a Wikipedia slip; if CIIP says BCE, Wikipedia and the IIP label are wrong. The IIP 13.5 cm height should be checked against CIIP's "Meas.".
Confidence: high (that the published dates conflict and that the 2024 report omits the stone); low (where the CE date started)
Touches the Copper Scroll? maybe (Hyrcania for entries 16, 29, 35; see ARGUMENT)

---

## Dead ends

- CIIP III and IV.2 × Hadashot (all 11 citations of HA-ESI 116+: 2255 Jaffa Eden Hotel, 2404 Ashqelon Refuse Pit 115, 3501/intro, 3511, 3675, 3733, 3735–3736 Maresha West, 3737, 3851 Beit Mirsim, 3894 Naḥal Peḥar). Findspots and contexts agree, apart from the SC 57 issue in card 1. HA 119 report 465 (Beit Mirsim) never mentions the stone of CIIP 3851; CIIP cites it for context only.
- *Maresha IV* vs Hadashot map references for the same complexes. *Maresha IV*'s eastings run 70–160 m east of the HA references:
  - SC 1: +106 m;
  - SC 89: +71 m against HA 133, +103 m against HA 120;
  - SC 126/57: +114 m;
  - SC 169: +111 m against HA 133, +158 m against HA 126.
  The northings agree within about 65 m. A correct Palestine-grid → ITM conversion accounts for only about 60 m E (pyproj EPSG:28193 → 2039), and HA prints NIG = OIG + 50/500 km. I dropped this as outside B3 (it is A6-3 / D3 ground) without settling which set is right. Also: HA 135 prints SC 97's reference as "19070/611260" (a 5-digit easting), and *Maresha IV*'s SC 99 easting 190665 equals SC 126's (R3 noted SC 99's two references 520 m apart).
- Finkielsztejn, INR 17 (2022) Note C: paywalled (USD 20); not read.
- Maresha III (IAA Reports 45, 2010; Korzakova's lead weights; Finkielsztejn's table 8.1): not in the corpus. A Drive search of PDFs titled "Maresha" finds only Hadashot reports.
- IIP kmir0003 "2-1 c. CE": the live site already shows BCE, so on its own it is only a source-file label slip. Kept in card 4 only as a possible origin of the Wikipedia date.
- Naḥal Peḥar CIIP 3894 ΒΗΤΟΜΟΡΣΥΚΩΝ (Paran: "Beth-mor [or Beth Morsy?]"): no corpus source settles the place name. Dropped.
- IIP as a second witness for CIIP I.1 readings: IIP carries no CIIP numbers for the Avigad tomb (jeru0058–0065, 0489), so it cannot stand in for the CIIP lemma text.

## Blocked inputs

- Drive `CIIP I.1 – Jerusalem 1-704 (compressed).pdf` (`1RNl4SwNvUF1XomCQ5N9Ze7WS4bMoGZb8`, 8.3 MB): `download_file_content` → "The connection to MCP server "Google_Drive" was closed because a message from the server was too large or could not be parsed" (same as round 1).
- Drive `CIIP I.1 – Jerusalem 1-704.pdf` (`126ct8RGvh91Nh4qHqHUWwqFsaqEus8R9`, 24.9 MB; first try in round 2): `read_file_content` returns 215,054 characters, front matter to lemma no. 9 (Theodotos) only, the same truncation as the compressed copy. Permissions: owner only, so there is no public download route. CIIP I.1 is not in the bucket page store, and De Gruyter lists every chapter as "Requires Authentication".
- Drive `CIIP IV.1 – Iudaea-Idumaea 2649-3324 (compressed).pdf` (`1gUPsePFJUkTWUwVzxVTRH8_gnsk7_u1h`, 20.5 MB): `read_file_content` returns 122,572 characters, reaching lemma 2671 only; Hyrcania (3209–3214, pp. 619–630) is not reached.
- INR 17 (2022) full text: paywall at lockwoodonlinejournals.com (article 2838).
- Wikipedia API revision query: "You are making too many requests to the API" (rate limit); the raw article text was fetched.

## Reproducibility

Scratch is `/home/claude/swarm/scratch/B3r2/`:
- kept: `zipb/context/` (text of Drive `CopperScroll_full_coverage_2026-10-14_ciip_index_b.zip`: CIIP IV.2 index and map-key pages only), `ciip4_1_head.txt`, `haber2024.txt`, `hyrc_wiki.txt`, `naveh/` (rendered Naveh pages; copyright: do not publish);
- deleted after use (about 250 MB), and can be rebuilt:
  - the Hadashot texts: `tar xzf /home/claude/swarm/scratch/R2/hadtext_pdftotext.tgz`;
  - the IIP clone: `git clone --depth 1 https://github.com/Brown-University-Library/iip-texts` (HEAD 0b7dc83 on 6 Nov 2026).
