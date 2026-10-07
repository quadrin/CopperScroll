#!/usr/bin/env python3
"""Write the W2-A Koḥlit dossier tables (CSV + JSON) from hand-transcribed data.
Every row carries its source pages. Run: python3 -I write_tables.py OUTDIR"""
import csv, json, sys, os
OUT = sys.argv[1]

# Page conventions used below:
#  Lefkovits 2000 = book page (PDF page = book + 21)
#  Puech 2006 = printed page of vol. 1 (PDF page = printed + 26 in the 706-page scan)
#  Puech 2015 = printed page (PDF = printed + 11)
#  DJD III = printed page (PDF = printed + 20)
#  CSS = Copper Scroll Studies (2002/2004), printed page (PDF = printed + 17)
#  Zissu 2001 = PEQ 133, printed page
#  Allegro 1960 = The Treasure of the Copper Scroll, 1st ed. (2023 Routledge reprint epub, print pagination)

proposals = [
 dict(id="P01", proponent="J.M. Allegro, unpublished 'Provisional Translation and Notes' (MS, c. 1956)",
      sources="Lefkovits 2000 p. 73 (siglum Allegro-pr, defined p. xiii)",
      site="none; reads I 9 as 'In the tell of Kḥlt'", coords="none",
      textual_basis="כחלת only at I 9; the other three cases read בחלה 'in a hole'",
      name_argument="כחלת 'may be the same as' כוחלית of b. Qid. 66a",
      features="none", criticisms="superseded by Allegro's own 1960 book",
      uses_bQid66a="yes (earliest link to b. Qid. 66a found in this search)", uses_hyssop="not reported",
      access="secondary (Lefkovits)", label="EVIDENCE (as reported by Lefkovits)"),
 dict(id="P02", proponent="J.M. Allegro 1960 (Treasure of the Copper Scroll, 1st ed.)",
      sources="Allegro 1960 pp. 33, 35, 39, 55; nn. 17-18 pp. 136-137; nn. 313-316 p. 170",
      site="no Koḥlit at all: I 9 'In the trough (?) of the Place of the Basin (?)' in the Temple (bathhouse under the Môqēd chamber); XII 10 'the Pit (Shîth) adjoining', the Šîth 'under the Altar itself' (n. 315)",
      coords="none", textual_basis="I 9 bḥl šl bḥlh; II 13, IV 1 (restored), IV 11-12 and XII 10 bḥlh 'in a hole'; XII 10 second word škynh 'neighbouring' (n. 314)",
      name_argument="none (no toponym)", features="Temple installations", criticisms="Milik 1962; Puech 2006 pp. 181, 185, 187, 206 (kḥlt and taw certain)",
      uses_bQid66a="no (not in the 1960 book)", uses_hyssop="no", access="direct (epub)", label="EVIDENCE"),
 dict(id="P03", proponent="J.M. Allegro 1964 (rev. ed.)",
      sources="Lefkovits 2000 p. 73 (Allegro rev. pp. 21-23, 25); Zissu 2001 p. 148; Wolters, CSS p. 317 n. 19",
      site="not established from the sources read", coords="none",
      textual_basis="KHLT at I 9 ('mound of KHLT'), II 13, IV 11; XII 10 still 'in a hole'",
      name_argument="not reported", features="not reported", criticisms="-",
      uses_bQid66a="unknown", uses_hyssop="unknown", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P04", proponent="J.T. Milik 1959-1962 (RB 66; ADAJ 4-5; DJD III)",
      sources="DJD III pp. 234 (B 19g), 240 (C 20, C 22), 241 (C 38), 274-275 (D 71-75), 280-281 (E 3-4), 285-289, 298-299; ADAJ 4-5 (1960) pp. 139-142 (translation only; no Koḥlit note found in the commentary pp. 143-155, OCR); Zissu p. 147 cites Milik, RB 66 (1959) 567-75",
      site="ʿEin Koḥel = Wadi ʿEin es-Siah spring ('Fons Eliae'), west slope of Mount Carmel; 'caverne de l'immersion' = ʿAin Umm el-Farag; pit/cave near el-Farag on the north slope of the valley",
      coords="none published (refs: SWP I pp. 268 f., 302; von Mülinen ZDPV 31 (1908) 15-19, pl. II)",
      textual_basis="כחלת at I 9, II 13, IV 11-12, XII 10 (4×); IV 1 read שב[..]קה (no Koḥlit); XII 10 שבצח 'smooth rock'",
      name_argument="Beirut marble plaque (photocopy from Starcky) prefacing Massekhet Kelim names a spring 'ʿEn Koḥel' in a deep valley with good water, a high mountain to its east with a blocked door at the top; Milik emends Massekhet Kelim's עין כתל to עין כחל and takes כחלת as the adjective 'kohlit' agreeing with an implied ʿAin (DJD pp. 234, 274-275)",
      features="hill by the spring with a turning door (I 9) = the plaque's mountain and blocked door; pool east of the spring (II 13); pit north-east of the spring (IV 11); narrow, horizontal cave north of Koḥlit (XII 10); treasure judged legendary (E 3-4)",
      criticisms="Dupont-Sommer 1961 pp. 382, 390-91 (Milik in error; עין כתל apparently in Babylon; tl = mound, not hill) via Lefkovits p. 74; Bardtke 1968 via Zissu p. 147; Zissu p. 147 (plaque preface 'suspect', in no other edition); Puech 2006 p. 175 n. 49 and p. 181 ('on peut douter'; 'vraisemblablement pas un site dans le Carmel')",
      uses_bQid66a="cited only to dismiss it: 'essais d'identification peu satisfaisants (כוחלית שבמדבר de bQiddušin 66a; Beit Kahil ...; H. Kuhlah ...)' (DJD p. 274)",
      uses_hyssop="no (not found in DJD III text)", access="direct (DJD III text; ADAJ OCR)", label="EVIDENCE"),
 dict(id="P05", proponent="(pre-1962 attempts, unnamed by Milik) Beit Kahil and Kh. Kuḥlah",
      sources="DJD III p. 274 (D 71); Lefkovits p. 74 lists them under Milik as 'possible identifications'; Zissu p. 148 says Milik 'proposed' them; Lurie via Lefkovits p. 74; Puech 2006 p. 181",
      site="Beit Kahil (WNW of Hebron); H. Kuḥlah / Kh. Quḥlet (NE of Beersheba); Lurie adds ʿEin Kuḥleh (Negev) and ʿEin el-Kuḥleh near Avdat",
      coords="none in sources read", textual_basis="כחלת as toponym", name_argument="Arabic name likeness only",
      features="none claimed", criticisms="Milik calls them unsatisfactory; Puech uses them only to show the name is not unique",
      uses_bQid66a="listed alongside b. Qid. 66a by Milik", uses_hyssop="no", access="direct (DJD) + secondary",
      label="EVIDENCE; Zissu's attribution to Milik as his proposal is not supported by DJD p. 274 (INFERENCE, high)"),
 dict(id="P06", proponent="B.Z. Lurie 1963 (Megillat ha-Neḥoshet, Hebrew)",
      sources="Lurie pp. 61-62 n. 1, 65, 73, 83, 126 via Lefkovits p. 74 and Zissu p. 148; Puech 2006 p. 181 n. 103",
      site="Tell Muḥalḥil near Nebi Musa (northern Judaean desert)",
      coords="none in sources read (Bar-Adon 1972 site 83 would carry a grid; not accessed)",
      textual_basis="כחלת in all four cases; 'in the Tell of כוחלית'", name_argument="phonetic likeness; also lists Beit Kaḥil, Kh. Kuḥleh, ʿEin Kuḥleh, ʿEin el-Kuḥleh",
      features="a tell", criticisms="Zissu p. 148: Bar-Adon's 1968 survey (Bar-Adon 1972 p. 118, site 83) found only a small structure 3.5 × 2.5 m; 'the only connection ... is the phonetic similarity'",
      uses_bQid66a="yes (refers to the Talmudic Koḥalit in the desert, per Zissu p. 148)", uses_hyssop="not reported", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P07", proponent="B. Pixner 1983 (RevQ 11: 323-65)",
      sources="Pixner pp. 337, 343 n. 6, 346, 348 n. 20, 358 via Lefkovits pp. 74, 426; Zissu pp. 148-149; Bar-Ilan, CSS pp. 204-205; Puech 2006 p. 181 n. 103, 2015 p. 53",
      site="Tell Koḥlit = site of the Greek Orthodox cemetery on Mount Zion, Jerusalem (entry 4); a second Koḥlit at Sekakah = Kh. Qumran; a third in 'Ṣehab', land of Damascus = Tell Shihab near the Yarmuk (entry 60)",
      coords="none in sources read", textual_basis="כחלת a technical term for a monastic centre; XII 10 שבצהב 'in Ṣehab'",
      name_argument="none (term, not toponym)", features="Essene quarter", criticisms="Goranson 1992/2002 (CSS pp. 227-228); Zissu p. 149 ('influenced by his concern to follow the trail of the Essenes in Jerusalem'); Bar-Ilan CSS p. 205; Eshel CSS p. 106 n. 35; Puech 2006/2015",
      uses_bQid66a="not reported", uses_hyssop="not reported", access="secondary (Pixner 1983 not available)", label="EVIDENCE (as reported)"),
 dict(id="P08", proponent="K. Beyer 1984/1994 (Die aramäischen Texte vom Toten Meer [+ Ergänzungsband])",
      sources="Beyer pp. 224-233 via Lefkovits pp. 74, 426; Goranson, CSS p. 228 n. 4; Puech 2006 p. 181 n. 104, p. 206 n. 506; Puech 2015 p. 112 n. 506",
      site="no Koḥlit (כחלת = 'schwarzes Objekt'); entry 60 placed at Janoaḥ, 'Ynḥ 10 km SE of Gerizim'",
      coords="none (Yanun: Notley-Safrai 2005 p. 104 grid 18440/17230)", textual_basis="XII 10 שבינח; כחלת common noun",
      name_argument="-", features="-", criticisms="Goranson CSS p. 228 ('seems unlikely'); Puech 2006 p. 181 and n. 104",
      uses_bQid66a="no", uses_hyssop="no", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P09", proponent="S. Goranson 1992 (JJS 43: 282-87), 1996 paper, 2002 (CSS pp. 226-232)",
      sources="CSS pp. 226-228 (direct); JJS 1992 p. 287 via Zissu p. 147, Lefkovits p. 75 n. 12, Puech 2006 p. 175 n. 49",
      site="a district ('kohlit'), 'most plausibly identified as an area east of the Jordan River'; no site named",
      coords="none", textual_basis="accepts Lefkovits's possible fifth instance at IV 1 (CSS p. 228)",
      name_argument="b. Qid. 66a: Jannaeus 'returned from conquering 60 towns in kohlit' (CSS p. 227)",
      features="none (district); argues a tell inside a 'kohlit' rules out Pixner's monastery reading",
      criticisms="Puech 1997 p. 184 n. 62; Puech 2006 p. 175 n. 49 ('rien ne prouve que Koḥlit doive être compris comme un district'); Bar-Ilan CSS p. 205 (a district would not help the person hiding)",
      uses_bQid66a="yes (central)", uses_hyssop="Zissu p. 147 attributes the hyssop+baraita 'region' inference to Goranson 1992 p. 287 (not verified: JJS 1992 not read)",
      access="direct (2002) + secondary (1992)", label="EVIDENCE"),
 dict(id="P10", proponent="É. Puech 1997 (RevQ 18: 184-85 n. 62), 2002 (CSS pp. 82-83 n. 62), 2006, 2015",
      sources="Puech 2006 pp. 175 n. 49, 181 and nn. 101-105, 186-187, 206, 216; Puech 2015 pp. 13-15 n. 49, 31 nn. 101-105, 39, 52-53, 111-113; CSS p. 82 n. 62",
      site="Tell es-Sultan (old Jericho), north of Hasmonaean-Herodian Jericho, 'à titre d'hypothèse'",
      coords="none published by Puech (repo gazetteer: 31.8717 N, 35.4446 E, ~150 m)",
      textual_basis="כחלת 5× (I 9, II 13, IV 1 restored שב[צפון כ]חלת, IV 11-12, XII 10); XII 10 שכנה 'qui se trouve' and second צפון = 'hidden'",
      name_argument="none: the tell could bear a name distinct from the oasis-city (cf. Tell es-Sultan/Jericho, Dhibon/Qarḥoh, Jerusalem/Ophel/Zion); the name is not unique (Beit Kaḥil etc.)",
      features="tell (4); pool to the east (11) ~ the very abundant spring at the foot of the tell (2 Kgs 2:19-22); great cistern to the north (15, his restoration); underground chamber to the north (19) and (60) with tombs hiding the entrance; Qumran-type graves on the north side of the tell (Kenyon 1981 pp. 173-174, not verified here); large irrigation works; sequence 'Valley of Achor north of Jericho'; Elisha-Elijah link to the Carmel legend; 'blue' could mean an indigo-working place (n. 105)",
      criticisms="Zissu 2001 p. 149 (circumstantial; no convincing link to b. Qid. 66a or Hyrcanus's campaigns; Jericho was in Hyrcanus's territory from the start; the name Jericho persisted at the site); wave-1 T06 order model; this dossier: the 'cistern to the north' rests on Puech's own restoration of the direction (2006 pp. 186-187)",
      uses_bQid66a="yes, addressed: Hyrcanus took 'villes' in Idumaea (2006; 'Samaria and Idumaea' in 2002); 'Tell es-Sultan est encore dans le désert, mais le toponyme peut ne pas être unique'",
      uses_hyssop="no (not found)", access="direct", label="EVIDENCE"),
 dict(id="P11", proponent="J.K. Lefkovits 1993 (diss.), 2000",
      sources="Lefkovits 2000 pp. 73-76, 135, 154-156, 179-180, 425-432, 451; Goranson CSS p. 228 (citing diss. pp. 183-87)",
      site="no site; 'the Scroll ... also indicates that Kaḥelet was near Jericho' (p. 428), with Janoaḥ (Ephraim, Kh. Yanun) to its north; also entertains Transjordan (p. 75)",
      coords="none", textual_basis="כחלת 4× + restored 5th at IV 1 (שב[כ]חלת, from diss. 1993); XII 10 שבינח 'in Janoaḥ'",
      name_argument="'Kaḥelet may well be the same as' כוחלית of b. Qid. 66a (p. 74); root כחל 'to colour azure' (p. 75); Koḥalit hyssop probably named after the place (p. 75); Rashi: a district in the wilderness; Jastrow: = Nophah (Num 21:30), Transjordan",
      features="Kaḥelet had more than one pit ('eastern deep pit', p. 179)", criticisms="Puech 2006 p. 186 nn. 190-191 and p. 206 (IV 1 details; Janoaḥ 'impossible')",
      uses_bQid66a="yes", uses_hyssop="yes (m. Par. 11:7 quoted; m. Neg. 14:6; Sifre on Num. 19:6; b. Suk. 13a; b. Ḥul. 62b, p. 75 n. 13)",
      access="direct", label="EVIDENCE"),
 dict(id="P12", proponent="B. Zissu 2001 (PEQ 133: 145-158; also JSRS 10 (2001) 119-136, Hebrew, not read)",
      sources="Zissu 2001 pp. 145-158 (direct)",
      site="ʿEin Samiya valley, desert of Samaria (Kh. Samiya as the Second Temple settlement; Kh. el-Marjama as the tell)",
      coords="'map ref. 181/155, Israel grid' (p. 150) ≈ 31.988 N, 35.327 E (my EPSG:28191 conversion, ~100 m datum uncertainty); Kh. Yanun 18425/17385, Yanun 18370/17245 (p. 149)",
      textual_basis="Lefkovits's 'the pit at Janoaḥ, north of Kaḥelet' (XII 10) - 'obligatory' in Baker's and Milik's facsimiles, not allowed by Allegro's (p. 149); counts Kaḥelet 4× (5 with Lefkovits)",
      name_argument="Wadi Kuḥeila, draining into the valley (Mandate 1:20,000 sheet 15-18 El Mughaiyir, 1941), preserves kḥl; Janoaḥ = Yanun (Onom. 108:20, 12 miles E of Neapolis) lies ~17 km north",
      features="tell Kh. el-Marjama (>30 dunams, Bronze/Iron fortified city, Hellenistic-Byzantine occupation); ʿEin Samiya spring (~300 m³/h) with canals and pools; rock-cut pool by aqueducts near the tell (Kallai) and a reservoir (Zohar 1980); many natural and rock-cut caves; Kh. Samiya with Roman-Byzantine kokhim tombs (Lyon 1908; Yeivin 1970-71; Baramki 1942 Tomb 1 with Early Roman lamp and ossuary fragments); Dhahr Mirzbaneh MB I cemeteries; el-Qasr monastery with cistern; possible 'Koḥalit hyssop' cultivation; n. 2: Avigad's 'yyn kḥl' jar might name Kh. el-Marjama",
      criticisms="Puech 2006 p. 175 n. 49, p. 181 n. 103, p. 206 n. 506 (depends on Janoaḥ, which 'n'est pas à retenir'/'is impossible'; unconvincing in the sequence of names; Koḥlit is 5×, Sokokah 4×, not 4 and 5)",
      uses_bQid66a="yes (central; dated to John Hyrcanus after M. Stern 1995)", uses_hyssop="yes (m. Neg. 14:6; m. Par. 11:7; 'Sifre, Deuteronomy 19, 6' - recte Sifre Numbers on Num 19:6, §124)",
      access="direct", label="EVIDENCE"),
 dict(id="P13", proponent="H. Eshel 2002 (CSS pp. 92-107)",
      sources="CSS p. 106 and n. 35", site="unidentified ('little is known about Kohlit other than it was located in the desert')",
      coords="none", textual_basis="I 9 read with an aqueduct ('its opening is at the edge of the aqueduct on the north')",
      name_argument="b. Qid. 66a", features="an aqueduct at Koḥlit", criticisms="-",
      uses_bQid66a="yes", uses_hyssop="no", access="direct",
      label="EVIDENCE; cites Zissu and adds 'there is an aqueduct at ʿEin Samiya' (Puech 2006 p. 181 n. 103 counts Eshel as following Zissu)"),
 dict(id="P14", proponent="M. Bar-Ilan 2002 (CSS pp. 198-209)", sources="CSS pp. 204-205",
      site="a specific place, unidentified ('not necessarily the place mentioned in b. Qid. 66a')", coords="none",
      textual_basis="Kahlit 4× (items 4, 11, 19, 60)", name_argument="-", features="-",
      criticisms="-", uses_bQid66a="mentions, non-committal", uses_hyssop="no", access="direct", label="EVIDENCE"),
 dict(id="P15", proponent="B. Thiering 2002 (CSS pp. 276-287)", sources="CSS pp. 285-287",
      site="'the Blue': the southern of two rooms at the SE corner of the courtyard at Kh. Qumran (loc. 101/102), a vestry; entry 60's graves = a grave at the NE corner of the esplanade (loc. 96)",
      coords="Kh. Qumran", textual_basis="kohlit 4× (1.9, 2.13, 4.11, 12.10)", name_argument="kḥl 'blue' (Ezek 23:40)",
      features="rooms, aqueduct, 'dipping hole'", criticisms="Puech 2006 p. 175 n. 49 notes it without comment", uses_bQid66a="no", uses_hyssop="no", access="direct", label="EVIDENCE"),
 dict(id="P16", proponent="Tübinger Bibelatlas (TAVO) B V 18 (Mittmann & Schmitt eds., 2001)",
      sources="via Puech 2006 p. 175 n. 49; Puech 2015 p. 14", site="between ʿAin el-Ghuweir and ʿAin et-Turabe, western Dead Sea shore",
      coords="sheet not inspected", textual_basis="-", name_argument="-", features="-",
      criticisms="Puech: 'il n'y a manifestement pas de tell ni surabondance d'eau douce'", uses_bQid66a="unknown", uses_hyssop="unknown", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P17", proponent="ʿAin Feshkha (proposer not identified)", sources="Puech 2006 p. 175 n. 49 and p. 181 n. 105",
      site="ʿAin Feshkha", coords="-", textual_basis="-", name_argument="'blue' = indigo working at ʿAin Feshkha (M. Bélis) is mentioned by Puech for the meaning of kḥlt",
      features="spring, installations", criticisms="Puech: excluded, no tell; Koḥlit 5× vs Sokokah 4×", uses_bQid66a="-", uses_hyssop="-", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P18", proponent="Talmud commentators on b. Qid. 66a (not 3Q15 proposals)",
      sources="Lefkovits 2000 p. 75 and n. 18", site="Rashi: a district in the wilderness; Jastrow: = Nophah (Num 21:30), Transjordan; Kohut: כחלית a metathesis for Cilicia",
      coords="-", textual_basis="-", name_argument="-", features="-", criticisms="-", uses_bQid66a="yes", uses_hyssop="-", access="secondary", label="EVIDENCE (as reported)"),
 dict(id="P19", proponent="J. Høgenhaven 2016, 2020", sources="wave-1 T03 kohlit_proposals.csv (DTT 79 (2016) p. 72 n. 22; 2020 p. 89); not re-verified here",
      site="Tell es-Sultan as one option; 2020 only if Achor = Wadi Nuweiʿimeh", coords="-", textual_basis="XII 10 'by the smooth rock' (Milik)",
      name_argument="-", features="-", criticisms="-", uses_bQid66a="unknown", uses_hyssop="unknown", access="via wave 1", label="UNVERIFIED here"),
]

xii10 = [
 dict(edition="Allegro, provisional MS (c. 1956)", reading="שכינה / שכונה", gloss="'In the Shith of the Sanctuary ([or] settlement), in the North, in the hole...'; revised MS: 'In the pit ([or] foundation) nearby'", argument="שכינה 'divine presence', i.e. the sanctuary; the yod 'a small stroke at the top of the nun'", source="Lefkovits 2000 p. 425"),
 dict(edition="Milik, original reading (BA 19 (1956) 62-63; SVT 4 (1957) 22)", reading="שכנה", gloss="'In the pit nearby, towards the north in a hole opening toward the north near the graves'", argument="adjective 'nearby'; כחלת read as בחלה 'hole'", source="Lefkovits 2000 pp. 425-426 and n. 2; Wolters, CSS p. 320 n. 27"),
 dict(edition="Allegro 1960", reading="שכינה (škynh)", gloss="'In the Pit (Shîth) adjoining on the north, in a hole opening northwards'", argument="šekēnah 'neighbouring' (f.); Šîth under the Altar", source="Allegro 1960 pp. 55, 170 nn. 313-316"),
 dict(edition="Milik 1959/1960", reading="(Smooth Rock, i.e. צחיח-type reading)", gloss="'At the tunnel in the Smooth Rock to the north of Kohlit, which opens towards the north'", argument="-", source="ADAJ 4-5 (1960) p. 142 (OCR)"),
 dict(edition="Milik 1962 (DJD III)", reading="שבצח", gloss="'Dans la galerie du Rocher Lisse au nord de Koḥlit, qui s'ouvre vers le nord'", argument="צחיח סלע (Ezek 24:7; 26:4, 14), shining smooth rock, 'si la lecture est bonne'; reading note: 'צח, malgré la tête très petite du ṣadé, semble préférable à ינח où les deux premières lettres seraient en ligature, comparable à celle de la l. 9'", source="DJD III pp. 240 (C 22), 234 (B 19h), 298-299"),
 dict(edition="Lurie 1963", reading="שכינה (follows Allegro)", gloss="'In the nearby pit (or cave) in the north of Koḥalit'", argument="-", source="Lefkovits 2000 p. 426; Puech 2006 p. 206 n. 503"),
 dict(edition="Pixner 1983", reading="שבצהב", gloss="'In the underground passage that is in Ṣehab north of Koḥlit'", argument="Ṣehab = Tell Shihab near the Yarmuk", source="Lefkovits 2000 p. 426; Puech 2006 p. 206 n. 504"),
 dict(edition="Beyer 1984/1994", reading="שבינח", gloss="'In the cavity, which is in Janoaḥ ... in the north there is a kaḥolet (black object)'", argument="Ynḥ 10 km SE of Gerizim = ינוח of Josh 16:6-7", source="Lefkovits 2000 p. 426; Puech 2006 p. 206 n. 506"),
 dict(edition="Lefkovits 1993 (diss. vol. 2 pp. 925-931) and 2000", reading="שבינח (defective for שבינוח)", gloss="'In the deep pit which is in Janoah, in the north of Kaḥelet, its entrance is hidden'", argument="the symbol after bet is 'either a ligature of yod plus nun or a ṣade, followed by a he/ḥet/taw'; Janoah of Josh 16:6-7 is listed with Upper Beth-horon and Jericho; Ephraim (Kh. Yanun) rather than Galilee; alternatives listed: Jonah/dove, Noah, marsh (ṣade), Ṣehab, Ṣiaḥ, Ṣaḥ, dry land, Shebna", source="Lefkovits 2000 pp. 425-432; drawings p. 451"),
 dict(edition="García Martínez 1994; García Martínez & Tigchelaar", reading="(conflicting reports)", gloss="-", argument="Lefkovits p. 426: García Martínez 'agrees with Pixner'; Puech 2006 n. 506 lists García Martínez & Tigchelaar with the šbynḥ readers", source="Lefkovits 2000 p. 426; Puech 2006 p. 206 n. 506"),
 dict(edition="Vermes", reading="follows Milik", gloss="-", argument="-", source="Lefkovits 2000 p. 426"),
 dict(edition="Muchowski 1993", reading="שבצח (follows Milik; transcribed 'Cach')", gloss="-", argument="-", source="Puech 2006 p. 206 n. 502"),
 dict(edition="Wise 1996", reading="(not rendered)", gloss="'In the dry well that is at the north of Kohlit'", argument="-", source="Lefkovits 2000 p. 426"),
 dict(edition="Wilmot (Wilmot & Wise 2002 p. 310)", reading="{שבצח} deleted as partial dittography of שבצפון", gloss="-", argument="-", source="Lefkovits 2000 p. 427; Puech 2006 p. 206 n. 505"),
 dict(edition="Wolters (1990, 1992, 1996 ed.; CSS 2002)", reading="שכנה ('so my edition') = Shekinah; or nun preceded by waw/yod", gloss="'In the cavern of the Presence on the north of Koḥlit'", argument="examined the original in Amman in 1991: no horizontal cross-stroke; the short vertical 'may be an accidental scratch or discoloration'; 'certainly not a ṣade'; 'either a nun alone ... or a nun preceded by a waw or yod'", source="Wolters, CSS pp. 319-320; Lefkovits 2000 p. 426"),
 dict(edition="Puech 1997 and 2002", reading="שבנה", gloss="-", argument="'neither ṣade nor yod can be inserted'", source="Puech, CSS p. 78; Puech 2006 p. 206 n. 507"),
 dict(edition="Puech 2006 / 2015", reading="שכנה (preferred) or שבנה", gloss="'Dans la fosse qui se trouve au nord de Koḥlit, son ouverture est cachée avec des tombeaux à son entrée'", argument="the right-hand stroke touches the next and is a double strike of the burin; 'De yod inséré il n'y a point, encore moins de ṣade'; šknh = qal fem. perfect of kwn 'qui se trouve' (rare in Hebrew, attested in Phoenician-Punic), or haplography for š(b)knh 'at the base' (cf. VI 7), or šbnh 'which was built'/'of Shebna'", source="Puech 2006 pp. 206, 216; Puech 2015 pp. 111-113"),
 dict(edition="Bedman 2000", reading="adopts Puech 1997", gloss="-", argument="-", source="Puech 2006 p. 206 n. 507"),
 dict(edition="Zissu 2001", reading="Janoaḥ (follows Lefkovits)", gloss="'the pit at Janoaḥ north of Kaḥelet'", argument="'obligatory when one examines carefully the copies of Wright-Baker and Milik; Allegro's copy is slightly different here, and does not allow the reading Janoaḥ'", source="Zissu 2001 p. 149"),
]

counts = [
 ("Allegro provisional MS (c. 1956)", "I 9 only", "1", "Lefkovits p. 73"),
 ("Milik original (1956-57)", "XII 10 read בחלה 'hole'", "-", "Lefkovits pp. 425-426"),
 ("Allegro 1960", "none (all read bḥlh / bḥl šl bḥlh)", "0", "Allegro 1960 pp. 33, 35, 39, 55"),
 ("Milik 1960 (ADAJ) and 1962 (DJD)", "I 9, II 13, IV 11-12, XII 10 (Milik nos. 4, 12, 21, 64); IV 1 read שב[..]קה", "4", "DJD III p. 285 ('revient quatre fois'); ADAJ pp. 139-142"),
 ("Lurie 1963", "the four cases", "4", "Lefkovits p. 74; Zissu p. 148"),
 ("Allegro 1964 rev.", "I 9, II 13, IV 11; XII 10 still 'hole'", "3", "Lefkovits p. 73; Zissu p. 148"),
 ("Pixner 1983", "four, as different places", "4", "Lefkovits p. 74; Bar-Ilan CSS p. 205"),
 ("Beyer 1984/1994", "none (common noun 'black object')", "0", "Lefkovits p. 74"),
 ("Lefkovits 1993/2000", "I 9, II 13, IV 1 (restored שב[כ]חלת), IV 11-12, XII 10", "4 + 1 restored", "Lefkovits pp. 73, 154-156"),
 ("Wise 1996", "follows Lefkovits at IV 1 ('[that is in Ko]hlit')", "5", "Lefkovits p. 155"),
 ("Wolters 1996 / 2002", "1.9, 2.13, 4.11-12, 12.10", "4", "Wolters, CSS p. 317"),
 ("Puech 1996 paper, 1997, 2002, 2006, 2015", "I 9, II 13, IV 1 (restored שב[צפון כ]חלת), IV 11-12, XII 10; also places (16) at Koḥlit", "5", "Puech 2006 pp. 175 n. 49, 186-187, 206; Lefkovits p. 155 n. 10 (Puech's 1996 Manchester paper)"),
 ("Zissu 2001", "four, 'or five if we accept Lefkovits'", "4 (5)", "Zissu p. 146"),
 ("Goranson 2002", "accepts Lefkovits's IV 1 as plausible", "5", "CSS p. 228"),
 ("Bar-Ilan 2002", "items 4, 11, 19, 60", "4", "CSS p. 204"),
 ("Thiering 2002", "1.9, 2.13, 4.11 + final item", "4", "CSS p. 285"),
 ("CopperScroll atlas (repo)", "entries 4, 11, 15, 19, 60", "5", "shared/entries.md"),
]

rabbinic = [
 dict(ref="b. Qiddushin 66a", text="מעשה בינאי המלך שהלך לכוחלית שבמדבר, וכיבש שם ששים כרכים", spelling="כוחלית", edition="Sefaria, William Davidson vocalized (nikkud stripped here)", url="https://www.sefaria.org/Kiddushin.66a", cited_by="Allegro MS (via Lefkovits p. 73); Milik DJD p. 274 (dismissed); Lurie; Goranson; Lefkovits p. 75; Zissu pp. 146-147; Eshel CSS p. 106 n. 35; Bar-Ilan CSS p. 205; Puech 2006 pp. 175 n. 49, 181"),
 dict(ref="m. Negaim 14:6", text="מצות אזוב, לא אזוב יון, לא אזוב כוחלי, לא אזוב רומי, לא אזוב מדברית", spelling="כוחלי", edition="Sefaria, Torat Emet 357", url="https://www.sefaria.org/Mishnah_Negaim.14.6", cited_by="Zissu p. 147; Lefkovits p. 75 n. 13"),
 dict(ref="m. Parah 11:7", text="אזוב יון, אזוב כוחלית, אזוב רומי, אזוב מדברי, פסול", spelling="כוחלית", edition="Sefaria, Torat Emet 357", url="https://www.sefaria.org/Mishnah_Parah.11.7", cited_by="Zissu p. 147; Lefkovits p. 75"),
 dict(ref="Sifre Numbers (Bamidbar) §124 on Num 19:6", text="אזוב. ולא אזוב יון, ולא אזוב כוחלית, ולא אזוב מדברית, ולא אזוב רומית", spelling="כוחלית", edition="Sefaria, Wikisource text", url="https://www.sefaria.org/Sifrei_Bamidbar.124", cited_by="Lefkovits p. 75 n. 13 ('Sifri on Num. 19:6'); Zissu p. 147 cites it as 'Sifre, Deuteronomy 19, 6' (mis-citation)"),
 dict(ref="b. Sukkah 13a", text="אזוב, ולא אזוב יון, ולא אזוב כוחלי, ולא אזוב מדברי, ולא אזוב רומי", spelling="כוחלי", edition="Sefaria, William Davidson vocalized", url="https://www.sefaria.org/Sukkah.13a", cited_by="Lefkovits p. 75 n. 13"),
 dict(ref="b. Ḥullin 62b", text="״אזוב״, ולא אזוב יון, ולא אזוב כוחלי, ולא אזוב רומי, ולא מדברי", spelling="כוחלי", edition="Sefaria, William Davidson vocalized", url="https://www.sefaria.org/Chullin.62b", cited_by="Lefkovits p. 75 n. 13"),
]

def wcsv(name, rows, fields=None):
    path = os.path.join(OUT, name)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        if fields is None: fields = list(rows[0].keys())
        w = csv.writer(f); w.writerow(fields)
        for r in rows: w.writerow([r[k] for k in fields] if isinstance(r, dict) else list(r))
    print('wrote', path, len(rows))

wcsv('kohlit_proposals.csv', proposals)
wcsv('xii10_readings.csv', xii10)
wcsv('kohlit_counts_by_edition.csv', counts, ['edition', 'kohlit_lines', 'count', 'source'])
wcsv('kohalit_rabbinic_passages.csv', rabbinic)
json.dump(dict(proposals=proposals, xii10=xii10, counts=[dict(zip(['edition','kohlit_lines','count','source'], c)) for c in counts], rabbinic=rabbinic),
          open(os.path.join(OUT, 'kohlit_dossier.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote kohlit_dossier.json')
