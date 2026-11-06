# Round-2 review RR3: lanes B1c, B2, B3, B4 (15 cards), 6 Nov 2026

Method: `REVIEW_BRIEF.md` with the changes in `review2/REVIEW2_NOTE.md`. No AGENTS.md procedures were applied. For every card I re-opened the cited evidence for at least the strongest claim, compared it with the round-1 card and review it extends, and ran a cheap kill test where one was open. Images I read (ʿAtiqot 76 p. 217, HA 106 TOC, the JSP 10 Carmel crop, Naveh 1974 p. 57) stay private. One render is in `private2/RR3/`.

Round-1 files compared: `out/B1c`, `out/B2`, `out/B2b`, `out/B3`, `out/B4`, `out/B4b`; reviews R2 (B1c), R3 (B3), R4 (B2), R6 (B4), R7 (B4b), R8 (B2b). No card is a restatement of a round-1 card.

---

## B1c-1: BCE/CE era slips in 23 HA passages, English and Hebrew

- **Verdict:** SURVIVES (NEW TO THE LITERATURE). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - Text corpus (`scratch/R2/t/hadtext`):
    - EN 24875: "late Persian and early Hellenistic periods (fourth century CE".
    - EN 01380: "Iron Age II–III (eighth–seventh centuries CE".
    - EN 01707: "middle of the second century CE".
    - EN 26634: "Antiochus III (223–187 CE)".
    - HE 00001: "(המאה הי' לסה"נ)".
    - HE 25601: "(המאה הב' לסה"נ)". The same report correctly prints Antiochus III's dates "לפסה"נ".
    - HE 25888: "(1550–3300 לסה"נ)".
    - HE 26211: "המאות הג'–הז' לפסה"נ".
  - Bucket prints (23 Oct): EN `vol-133/26005` p. 1, "end of the Late Bronze Age (thirteenth century CE)", while the same report elsewhere has "thirteenth century BCE". HE `vol-131/25601`: "(המאה הב' לסה"נ)". Both slips are confirmed on the printed page.
- **Round-1 link:** extends B1c-1 (year) to a new field. It is new.
- **Literature/novelty:** no era audit in `out/`, `out2/` (all lanes), `review/` or the repo. The worker's web queries for errata found none.
- **Alternative tried:** the period name, not the era, might be the error. In every row I checked, the other language agrees with the period, and so does a second date in the same report.
- **Correction:** the title says "23 HA reports". The CSV holds **23 slips in 21 reports** (11 EN-only, 10 HE-only slips in 8 reports, 2 in both). "20 of the 23" counts slips.

## B1c-2: ʿAtiqot map references that fail their NIG/OIG twin or their Hebrew text (17 articles)

- **Verdict:** SURVIVES (NEW TO THE LITERATURE for 15 articles; NEW TO THE PROJECT for the ʿEn Yaʿal fix). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - ʿAtiqot 76 (1652). The English summary is printed p. 217, which I rendered from the bucket PDF (private). It reads "Area A (map ref. NIG 17773/76693; OIG 12773/16693)".
  - The Hebrew text layer gives "16693/12773, רי"י 21693/62773" and Area B "21695/62775 … 16695/12775 … כ-50 מ' מדרום-מזרח למעיין".
  - ʿAtiqot 82 (1633): "NIG 190768–815/551782–5, OIG 140768–815/151782–5". The OIG twin requires NIG 651782, and the same article gives "NIG 190820/651805" for the neighbouring schoolyard.
- **Kill test run:** the worker left the print check of p. 217 open. I ran it, and the print matches the text layer.
- **Literature/novelty:** the project's `part_e_atiqot/reading_r3/NOTES.md` C6 calls the ʿEn Yaʿal references unusable ("fit neither grid") and places the unit by name. So the error was known to the project. The resolution from the Hebrew is not.
- **Corrections:**
  1. ʿEn Yaʿal is not a pure axis swap in all three areas. For Areas C and B the English OIG "eastings" (17192, 17195) are also 500 units (5 km) larger than the Hebrew 16692, 16695. The summary is garbled more than the card says. The conclusion (Hebrew right, summary wrong) is unchanged.
  2. The same project note (C6) also flags ATQ59-021s, an English-summary/Hebrew conflict of about 17 km that is not among the card's 17. It shows the recall limit of the twin test. The project already holds that case.

## B1c-3: same excavation, two IAA publications, different places (Rimmonim, Aḥihud, ʿEn Ẓippori)

- **Verdict:** SURVIVES (NEW TO THE LITERATURE). **Confidence:** high (Rimmonim, Aḥihud); medium (ʿEn Ẓippori). **Cost:** cheap.
- **Evidence checked:**
  - ʿAtiqot 118 (2322), n. 2: "Permit No. A-3847; map ref. 212114/717412". The Introduction: "west of Zububa, about 4 km east of Tel Megiddo (Fig. 1)".
  - HA 09562: "Zububa (Permit No. A-3847; map ref. 220950/717350)".
  - ʿAtiqot 60 (1222): "NIG 2210/7174".
  - pyproj (EPSG:2039). The HA point is 35.220 E 32.550 N, about 1 km W/NW of Zububa and about 4.7 km SE of Tel Megiddo. The ʿAtiqot 118 point is 35.126 E, about 6.6 km SW of Megiddo and about 10 km W of Zububa.
  - Fig. 1's text layer has a "0 500m" scale bar with "Zububa" labelled beside the site. That is a second internal witness against 212114.
  - Aḥihud: HA 01268, "map ref. NIG 2110/7572; OIG 1610/2572", the "northwestern fringes of Moshav Ahihud". ʿAtiqot 83 (1704): "216069/757196". ʿEn Ẓippori: the identical impossible string "123740–88/175760–176200" is in both HA 26165 and ʿAtiqot 119 (2361).
- **Kill test:** reading Fig. 1 on the page image was not possible. The ʿAtiqot 118 PDF is 55 MB, over the size limit. The figure's text layer supports the card.
- **Correction:** report 01268 is in **HA 121** (2009), not HA 122.
- **Round-1 link:** B1c-3 was one content mismatch. This card is a new permit-keyed join, so it is new.

## B1c-4: ʿAkko, Ha-ʿAmal St: lead "amulet" assigned to R. Daniel, no reading published

- **Verdict:** WEAKENED (tag kept: NEW TO THE PROJECT). **Confidence:** high for the printed facts; low for the significance. **Cost:** moderate.
- **Evidence checked:**
  - HA 25582 and 26039 staff lists both read "R. Daniel (lead amulet)".
  - 26039: "The lead tablet (Fig. 13) was found rolled and bears indecipherable incisions".
  - 25582: "incised marks, which have not been deciphered yet".
- **Literature check:**
  - Web: `Robert W. Daniel lead amulet Akko OR Acre OR Ptolemais`. This found Daniel & Hollmann, *Magica Levantina* (Brill-Schöningh 2025).
  - Its DFG project page (gepris 285891763) lists only Caesarea (well of the Governor's Palace; Hendler coll.), Antioch/Daphne, and a *silver* IAA epilepsy amulet. No ʿAkko lead item. This supports "no published reading".
- **Why weakened:** the simplest reading is that the specialist named in the list saw the tablet and judged it indecipherable, and the final report prints that verdict. That is a null result, not an unpublished reading. The card's "loose end" stands only if the tablet was never unrolled.

## B2-1: "Qumran, Cave Q3" (L-399/1986) = 3Q, misplaced 2.95 km onto the shore plain

- **Verdict:** SURVIVES (NEW TO THE LITERATURE for the register/WBADB point; NEW TO THE PROJECT for WB:E756 = DJD3:8). **Confidence:** high (point); medium-high (identity). **Cost:** cheap.
- **Evidence checked:**
  - Workbook (`scratch/B2r2/dl/WBADB_data1.xlsx`, sha256 `3db734cdc1a7…`), License List: "L-399/1986-0 | 195500 | 127600 | Qumran, Cave Q3 | NDA" and "L-399/1986-0 | 193390 | 129490 | Cave 1 and Cave 2 | Joseph Patrich".
  - Excavations 756: "Cave Q-3", L-399/1986-0, "Vendyl Jones ('78)".
  - ESI 6 store p. 78: "In April 1986 an excavation was carried out in Cave Q3 … the cave in which the Copper Scroll was found … given the number 8".
  - caves.csv: WB:E756 at 195500/127600; DJD3:8 at 193486/129756. The distance is 2.95 km.
- **Alternative tried:** WB:E756 might be the 1988 juglet cave (X/35, also called "Q3", also dug with Jones's volunteers). It is not. WBADB already has that cave as Excavations 702 "Cave of the Balsam Oil Juglet … Cave 13 or Cave Q3", at 193800/130150, under L-640/1994, "Excavated in 1988". So the 1986 licence on 756 points to the 1986 dig, which ESI 6 says was 3Q.
- **Extra observation:** WBADB 713 "Cave 1 and Cave 2" (Patrich '86, L-399 + L-405) lies 280 m from the project's 3Q point. 3Q may already be represented there, which makes 756 a pure phantom.
- **ARGUMENT:** modest and correct. It changes no identification. Calling the geniza reading "the published basis" is fair to Patrich's own ESI text.

## B2-2: HA 106 prints SOA licence "837" for a March 1995 Qumran survey; ghost register entry; WBADB 255-character truncation

- **Verdict:** SURVIVES (NEW TO THE LITERATURE). **Confidence:** high (anachronism, ghost, truncation); low-medium (679/693). **Cost:** cheap.
- **Evidence checked:**
  - HA 106 TOC image (`scratch/B2r2/ha106_181.png`, printed p. 179): "חורבת קומרן (קמ"ט 837)". The same page has the period-typical "קמ"ט 530" and "573".
  - Store text p. 131: "1995", "19325/12620".
  - Register: L-837/1999-0 twice (Kh. Qumran, Porat, 193250/126200; Miẓpeh Jericho). L-679 and L-693/1994 "The Springs Area: Qumran and Feshkha", 193300/126300.
  - Excavations 754 licence field length = 255, the only one at that length (next longest 236), ending "L-9".
- **Caveat on one argument:** the "0 inversions" test (I reproduced it: 1,112 numbered entries, 0 inversions) is partly circular, because the card itself suggests the register's years were inferred from the numbers. The anachronism does not need it. HA 106 (1996) prints 837, while L-773 was in use in January 1997 (B2b, R8).

## B2-3: the 49 WBADB licence spreads reviewed; B2b errors already in the register; Carmel ITM digit swap

- **Verdict:** SURVIVES, one sub-point struck. Tags: NEW TO THE PROJECT (classification; the register as the source of the B2b errors); NEW TO THE LITERATURE (minor) for the Carmel swap only. **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - Register: "L-733/1995-0 … Ba'al Ḥaẓor … L-733/1995-0 … Mattityahu (north) … L-733/1995-1 … Mattityahu (northeast)".
  - "L-959/2002-0 | 181000 | 132100 | 177300/137300 | Kh. Abu Musarraḥ; North of Kh. Shuweikeh | Yuval Peleg; Naftali Aizik, Yuval Peleg".
  - JSP 9 store p. 146: "In March 2003 … (License No. 959) … north of Khirbet Shuweikeh (map ref. ITM 20310/69455…)".
  - The JSP 10 Carmel crop (private) reads "ITM 52974/21743; IOG 09274/16743".
- **New relative to round 1:** B2b's `join_jsp10_x_wbadb.csv` gives `itm_vs_iog_m = 0` for A14 Carmel, so round 1 missed the 9/2 swap.
- **Struck:** "licence 959 printed for two digs" as a misprint (NEW TO THE LITERATURE). The register files both digs under one L-959/2002-0 entry with Peleg on both. That is consistent with one licence covering two salvage jobs, a practice the card itself documents for other licences. Neither print is shown to be wrong.

## B2-4: JSP 9 × register; the Shaked (west) field tower's ITM built from a northing-first IOG

- **Verdict:** SURVIVES (NEW TO THE LITERATURE, minor). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - JSP 9 store p. 155: "Shaked (map ref. ITM 25990/66450; 1OG 20990/16450) … (License No, 869)".
  - Register: "L-869/1999-0 | 164500 | 209900 | Shaqed (west)".
  - Arithmetic: 20990 + 5000 = 25990 and 16450 + 50000 = 66450. The offsets were applied to the swapped pair, so the correct ITM is 21450/70990.
- The join (JSP 8/9 left undone in round 1) is new.

## B3-1: the SC 57 → SC 126 renumbering was printed in HA-ESI 126 (2014), which CIIP cites; 65 IIP records still say SC 57

- **Verdict:** SURVIVES. Leading tag KNOWN BUT UNDER-DISCUSSED; secondary NEW TO THE LITERATURE for the CIIP and IIP scope. **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - HA 12643 (EN corpus): "…in the direction of Subterranean Complex 57 (… Alpert and Stern 2007 (https://doi.org/10.69704/jhaesi.116.2004.499); to be referred to in subsequent publications as Subterranean Complex 126)".
  - CIIP IV.2 store p. 197, n. 50: "I. Stern - B. Alpert, HA-ESI 126, 2014 (…id=12643&mag_id=121, viewed: 24.5.2017)".
  - IIP raw GitHub `mare0001`, `mare0018b`, `mare0030`, `mare0064`: `<geogFeat type="locus">Subterranean Complex 57</geogFeat>`. I did not recount all 65.
- **Caveat (R3's question, only partly closed):** the corpus text is the current online version. It carries DOIs added years later, so the 2014 wording is not proven by this copy. A 2024 Wayback capture exists (`web.archive.org/web/20240311135129/…id=12643&mag_id=121`), but my fetch was refused, so it is untested. The future tense ("to be referred to in subsequent publications") and *Maresha IV*'s 2014 citation "Subterranean Complex 57 (126)" make an original 2014 wording likely.
- **Round-1 link:** this goes beyond B3-1, with a new witness, the CIIP citation and the IIP scope.

## B3-2: Agathocles weight identity (Maresha III 161 no. 3 = CIIP 3679 = *Maresha IV* no. 3); "two redatings"

- **Verdict:** WEAKENED (NEW TO THE PROJECT). Identity: high. Internal mismatch: not shown. **Cost:** needs new data (INR 17 Note C).
- **Evidence checked:**
  - HA 26380: "an inscribed lead weight (Korzakova 2010b:161, No. 3)".
  - CIIP store p. 383: "Bibl.: Korzakova, Maresha III 161 no. 3 (ed. pr.)" under the entry "cast in the same mold as nos. 3677 and 3678".
  - Together these restore B3-3's point (a) (R3 had weakened it). This part holds.
- **Why weakened:**
  - *Maresha IV* p. 26 (store p. 37) is footnote 8. It is about Maresha's abandonment date: "this date was temporarily revised … to SE 205 … However, Finkielsztejn later (2022:86–90) corrected his reading to 112/111 BCE".
  - p. 248 (store p. 259) gives the weight series "redated to the year 200 SE, i.e. 113/112 BCE … dating the conquest itself to 112/111 or 111/110".
  - So p. 26's 112/111 is p. 248's conquest date. This is the weight-year versus conquest-date distinction that the card itself names as the alternative. A loose wording, not two readings.
  - The HA 133 (2021) "c. 107/6 BCE" predates the 2022 paper. Finkielsztejn's own 2021 chapter in *Middle Maccabees* (n. 15, store p. 226) still has "the last series of lead weights, dated 108/107". That is chronology of opinion, not an inconsistency.

## B3-3: Avigad 1962 × IIP/Rahmani for the Karm esh-Sheikh ossuaries

- **Verdict:** SURVIVES (NEW TO THE PROJECT). **Confidence:** medium. **Cost:** moderate.
- **Evidence checked:**
  - Avigad p. 8 (Drive `1EbVF1Wpb04URiHc3VfVkVYjpH6k0HUas`, connector OCR): "Ossuary No. 8. Inscription in green chalk (?) written 5 times—3 times on front, twice on rear".
  - IIP `jeru0064`: six words, with commentary "The first line is inscribed on the chest's front side … the rest on the back side … The last line appears corrupted". So Rahmani/IIP has 3 on the front and 3 on the back, the sixth a corrupted "[Η]ω[ρ]α".
  - IIP `jeru0489` (Alexander son of Simon): empty `<height/>` and empty provenance/locus.
- **Note:** the difference is real but small. Rahmani's sixth instance is flagged as corrupt by IIP itself. Which reading is right is open, as the card says.

## B3-4: Naveh 1974 Hyrcania Aramaic inscription: omitted by Haber & Gutfeld 2024; Wikipedia dates it CE

- **Verdict:** WEAKENED. Tag: NEW TO THE LITERATURE (minor) for the omission only. The date conflict is reduced to a Wikipedia slip plus an IIP source-file label. **Confidence:** high (facts). **Cost:** needs new data (CIIP IV.1 nos. 3209–3214).
- **Evidence checked:**
  - Naveh p. 57 (page image, private): "מבחינת השיקול הפליאוגרפי יש להעדיף את המחצית הראשונה של המאה הא' לפסה"נ". He leaves open the end of the Hasmonean period or early Herod.
  - Wikipedia raw text, l. 86: "from the second or first century CE", ref CIIP IV/1 pp. 619–628.
  - IIP `kmir0003`: `<date notBefore="-0200" notAfter="-0001" …>2-1 c. CE</date>`.
  - `haber2024.txt`: 0 hits for "Naveh". The inscriptions it lists are Mader's Greek, the papyri, and the 2023 Greek, Kufic and plaster finds.
- **Why weakened:** IIP's encoded dates and its live page are BCE, and Naveh is BCE. No scholarly publication is shown to say CE. Unless CIIP IV.1 says CE, the "conflict" is a Wikipedia and label error, not a literature conflict.
- **ARGUMENT:** sound and modest ("neutral for 16/29/35").

## B4-1: Gerizim Cat. 346 "ΓΣ(?)" is a thunderbolt type (SC 2364); the real ΓΣ bronze is SC 2368; the date spread into tesserae and *Middle Maccabees*

- **Verdict:** SURVIVES (NEW TO THE LITERATURE; KNOWN BUT UNDER-DISCUSSED for the conditional reading). **Confidence:** high (printed facts, misattribution); medium (misreading). **Cost:** needs new data (SNG Israel 1 no. 2697; SC II p. 534).
- **Evidence checked:**
  - JSP 19 store p. 165: Cat. 344 "Winged thunderbolt … Ɵ P (= S.E. 199) … SC 2: 534, No. 2364.1"; Cat. 345 "Same, but date: Σ (= S.E. 200) … 2364.2".
  - Store p. 166: Cat. 346 "110/109(?) … Same, but date: ΓΣ(?) (= S.E. 203) SNG Israel 1: 352, No. 2697; Cf. SC 2: 534, No. 2364.2".
  - wildwinds BMC 24 (SC 2368): "Herakles … Athena … Date GS (110-109 BC) in exergue"; BMC 16 (SC 2364): "ΘΡΡ, winged thunderbolt".
  - *Middle Maccabees* store p. 429: "the temple city on Mount Gerizim and Samaria by 110 BCE, and Beit Shean/Scythopolis by 109 BCE (Finkielsztejn in this volume)".
  - Finkielsztejn's chapter, store pp. 216–235: 0 hits for Gerizim, Shechem or Samarit*.
- **Strengthened:** Finkielsztejn's text (store p. 226) says "The city of Samaria fell in 108 BCE" and Scythopolis "was conquered in 108 BCE". So the editors' 110 and 109 also misstate him for Samaria and Scythopolis, not only for Gerizim.
- **Small correction:** the card calls Finkielsztejn's Samaria horizon a "latest dated coin 112/111". What I read is "fell in 108 BCE" (n. 16 cites the Harvard registers). The 112/111 may be on another page, but I did not see it.
- **Kill test (still open):** a web search for `"Spaer 2697"` returned dealer pages that did not resolve. On wildwinds, SNG Israel orders the Antioch issues as 2680 (first-reign AR), 2687–2696 (thunderbolt AE), 2700 (second-reign AR) and 2708 (Herakles/Athena AE, 110–107). No. 2697 sits at the junction, so its position does not decide the question.

## B4-2: re-run of the hoard screens with the Gerizim hoards and the Vespasian cache

- **Verdict:** SURVIVES (NEW TO THE PROJECT). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - The repo's `hoards_full/results.json` contains 0.6808, which is the baseline the worker reproduced.
  - `hoards_full_rerun_summary.json` v1_plus3 main: n_known 81, n_unknown 99, D 0.6846, G3 30, G4 43.
  - `gerizim_hoards_coin_weights.csv`, silver: 129 coins (121 tetradrachms), Σ = 1,770.71 g. That matches the card.
  - README "What stays unknown" lists IGCH and CH as closed.
- **Note on the ARGUMENT:** "temple silver in a vessel, hidden in a wall under siege" is stronger than the sources. JSP 19 says "apparently hidden" and asks whether the vessel came from the treasury, and Bijovsky prints an alternative deposit date (c. 121–119) that is not tied to the siege. The verdict does not depend on this wording.

## B4-3: Lorber 2021's silver-hoard table: 9 hoards missing from `hoards.csv`; Nablus 1891 dated 21 years early

- **Verdict:** SURVIVES (NEW TO THE PROJECT). **Confidence:** high (join); medium (effect). **Cost:** cheap.
- **Evidence checked:**
  - *Middle Maccabees* store p. 349 prints the table: "Ramallah area, early 1992 (CH 8, 464) ca. 135 …; Hebron, 1976 (CH 3, 61) 131 …; Golan, 1932 (IGCH 1600) 128/127 …; Samaria, 1999 (CH 9, 534) 128/127 …; Idumea … July 2004 … 128/127".
  - `hoards.csv`: `chre7844` "HEBRON 1976" is dated 132–136 CE, a different hoard. `n02_nablus1891` is at −125 (Noe), and `t02X06` ʿAqrav at −110.
  - No Ramallah, Golan, Capernaum or Bethlehem (IGCH 1603) Hellenistic rows. `chre20987` Bethlehem 1993 is Trajanic.

---

## Summary table

| lane | card | short title | original tag | verdict | final tag | confidence | cost |
|---|---|---|---|---|---|---|---|
| B1c | 1 | HA BCE/CE era slips, EN and HE | NEW TO THE LITERATURE | SURVIVES (23 slips in 21 reports) | NEW TO THE LITERATURE | high | cheap |
| B1c | 2 | ʿAtiqot NIG/OIG and EN/HE conflicts, 17 articles | NEW TO THE LITERATURE / PROJECT | SURVIVES (ʿEn Yaʿal B/C also +5 km) | NEW TO THE LITERATURE / NEW TO THE PROJECT | high | cheap |
| B1c | 3 | HA × ʿAtiqot same dig: Rimmonim, Aḥihud, ʿEn Ẓippori | NEW TO THE LITERATURE | SURVIVES (Aḥihud is HA 121) | NEW TO THE LITERATURE | high | cheap |
| B1c | 4 | ʿAkko lead amulet, no reading | NEW TO THE PROJECT | WEAKENED | NEW TO THE PROJECT | low | moderate |
| B2 | 1 | Cave Q3 L-399/1986 = 3Q, misplaced 2.95 km | NEW TO THE LITERATURE / PROJECT | SURVIVES | NEW TO THE LITERATURE / NEW TO THE PROJECT | high | cheap |
| B2 | 2 | HA 106 licence 837 anachronism; ghost; truncation | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high | cheap |
| B2 | 3 | 49 licence spreads; register holds B2b errors; Carmel swap | NEW TO THE PROJECT / LITERATURE | SURVIVES (L-959 "misprint" struck) | NEW TO THE PROJECT (+ NEW TO THE LITERATURE minor, Carmel) | high | cheap |
| B2 | 4 | JSP 9 Shaked tower ITM from swapped IOG | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE (minor) | high | cheap |
| B3 | 1 | SC 57→126 printed in HA 2014; CIIP cites it; IIP 65 records | KBUD / NEW TO THE LITERATURE | SURVIVES (2014 wording not independently dated) | KNOWN BUT UNDER-DISCUSSED (+ NEW TO THE LITERATURE scope) | high | cheap |
| B3 | 2 | Agathocles weight identity; "two redatings" | NEW TO THE PROJECT | WEAKENED | NEW TO THE PROJECT | high (identity) / low (mismatch) | needs new data |
| B3 | 3 | Avigad 1962 × IIP/Rahmani ossuaries | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | medium | moderate |
| B3 | 4 | Naveh Hyrcania inscription omitted; CE date | NEW TO THE LITERATURE | WEAKENED | NEW TO THE LITERATURE (minor, omission only) | high (facts) | needs new data |
| B4 | 1 | Cat. 346 type ≠ ΓΣ type; 110/109 spread; *Middle Maccabees* misattribution | NEW TO THE LITERATURE / KBUD | SURVIVES (strengthened) | NEW TO THE LITERATURE | high / medium | needs new data |
| B4 | 2 | Hoard screens re-run with 3 rows | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high | cheap |
| B4 | 3 | Lorber 2021 table: 9 hoards missing; Nablus date | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high / medium | cheap |
