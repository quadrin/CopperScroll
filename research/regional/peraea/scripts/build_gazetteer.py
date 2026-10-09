#!/usr/bin/env python3
"""Build the Peraea gazetteer, feature table and source register (exploratory; no identification claim).

    python3 -I research/regional/peraea/scripts/build_gazetteer.py [--check]

Writes, next to this folder: gazetteer.csv, features.csv, sources.csv.
All values below were coded by hand from the sources listed in SOURCES (read 9 October 2026 UTC) under the
frozen plan.json. Palestine Grid references are converted with pyproj EPSG:28191 -> EPSG:4326, the transformer
of W2B scripts/grid_convert.py (imported by path, not edited). `--check` rebuilds in memory and compares.
Quotes are 12 words or fewer. Labels: EVIDENCE (a source states it), INFERENCE (our reasoning or a source's
explicit inference), TRADITION, CLAIM (a modern proposal not tested).
"""
import argparse
import csv
import importlib.util
import io
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # research/regional/peraea
REPO = ROOT.parents[2]
GRID_CONVERT = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1/scripts/grid_convert.py"
PLAN = ROOT / "plan.json"

DOA = "https://publication.doa.gov.jo/uploads/publications/"

# --------------------------------------------------------------------------------------------- sources
# id: (citation, url, sha256 of the file read, how read)
SOURCES = {
    "kokkinos2001": ("Kokkinos, N. 2001. A Reconnaissance Trip to Peraea (2-12 October 2000). ADAJ 45: 479-484 (with Auge, C., Note sur le tresor ... de Iraq al-Amir, pp. 483-484 in the same PDF)",
                     DOA + "40/ADAJ_2001_45-479-484.pdf", "9792c071736c2d64300452550f27ea41a180d78995b2950fd304e2271334d127", "OCR"),
    "salles2009": ("Frangie, D. and Salles, J.-F. 2009. Hasmoneans, Herodians and Arabs in the Jordan Valley: Disputes Over a Border? SHAJ 10: 137-152",
                   DOA + "25/SHAJ_10-137-152.pdf", "a13bd7ad975774e457418c7ac1bd9afa50edb72deeba265b7ab40599a5b4fa67", "text layer"),
    "salles2013": ("Frangie, D. and Salles, J.-F. 2013. Recherches a Umm Hadar, Wadi al-Kafrayn. SHAJ 11: 243-262",
                   DOA + "16/SHAJ_11-243-262.pdf", "d1025541c0b75d9d92870b69a8a59182187b05181b1f4c2559be0eac85925fc7", "OCR"),
    "ji2009": ("Ji, C.-H. C. 2009. Drawing the Borderline: the Nabatean, Hasmonean and Herodian Kingdoms in Central Jordan. SHAJ 10: 617-632",
               DOA + "25/SHAJ_10-617-632.pdf", "3c51a8f5b355ab23e89364cd1889edd2386ee21b7cbe13d044eba43b88530101", "text layer"),
    "jilee1998": ("Ji, C.-H. C. and Lee, J. K. 1998. Archaeological Survey and Settlement Patterns in the Region of Iraq al-Amir, 1996. ADAJ 42: 587-608",
                  DOA + "77/ADAJ_1998_42-587-608.pdf", "29e0872cb90f5140e566de42f2d4cc9913f6c27f91aea991534009c1cdacb691", "OCR"),
    "jilee1999": ("Ji, C.-H. C. and Lee, J. K. 1999. The 1998 Season of Archaeological Survey in the Regions of Iraq al-Amir and Wadi al-Kafrayn. ADAJ 43: 521-539",
                  DOA + "78/ADAJ_1999_43-521-539.pdf", "c3c8b2ec14ef9b81302c68d9965c3923630a0b265531edeeabee449a1524fbc3", "OCR"),
    "jilee2002": ("Ji, C.-H. C. and Lee, J. K. 2002. The Survey in the Regions of Iraq al-Amir and Wadi al-Kafrayn, 2000. ADAJ 46: 179-195",
                  DOA + "71/ADAJ_2002_46-179-196.pdf", "c59dfb901c199dcb33532fc9074b627ca6460d3692324f3c79f248f62c7c1c2a", "OCR"),
    "jilee2004": ("Ji, C.-H. C. and Lee, J. K. 2004. From the Tobiads to the Hasmoneans: the Hellenistic pottery, coins, and history in the regions of Iraq al-Amir and the Wadi Hisban. SHAJ 8: 177-188",
                  DOA + "23/SHAJ_8-177-188.pdf", "e0369e4f359d4dbf1946d65f8818e54dbdb216658d8b2ae5557e43cf660336b5", "OCR"),
    "strobel1974": ("Strobel, A. 1974. Observations about the Roman Installations at Mukawer. ADAJ 19: 101-127",
                    DOA + "47/ADAJ_1974_19-101-127.pdf", "73d775e9daa4c1b6f908a229cc2e687f048569c0e0c07254afe1e55eb2b0f403", "OCR"),
    "strobel1997": ("Strobel, A. 1997. Ancient Roads in the Roman District of South Peraea. SHAJ 6: 271-280",
                    DOA + "21/SHAJ_6-271-280.pdf", "b12c9b658793a5a4fb8a1362f4e60db44c2e6582765f5dc4bc54d872f3fb8131", "OCR"),
    "piccirillo1979": ("Piccirillo, M. 1979. First Excavation Campaign at Qal'at el-Mishnaqa-Meqawer (Madaba). ADAJ 23: 177-183",
                       DOA + "105/ADAJ_1979_23-177-183.pdf", "919217ee440b2ed947cb773e496fb4e5883a5ab91d932d8a7716967682d041f1", "OCR"),
    "loffreda1981": ("Loffreda, S. 1981. Preliminary Report on the Second Season of Excavations at Qal'at el-Mishnaqa - Machaerus. ADAJ 25: 85-94",
                     DOA + "125/ADAJ_1981_25-85-94.pdf", "3731473184dbb98870147f197b565f22772107dacd3755b0b4d440bd4e213ec3", "OCR"),
    "voros2016": ("Voros, G. 2016. Machaerus: Excavations and Surveys (2009-2012). SHAJ 12: 529-542",
                  DOA + "15/SHAJ%20XII-529-542.pdf", "1ba4cce267098bbea5d9c20f3130892a8edf5f1b033bab434779a3a21f70deb6", "text layer"),
    "voros2018": ("Voros, G. 2018. Machaerus Project: Preliminary Report on the 2016-2017 Archaeological Excavation Seasons. ADAJ 59: 435-454",
                  DOA + "43/ADAJ_2018_59-435-454.pdf", "6a40362fa64c589b9e850d9fdd4cc0c477c7e201a89c563ef47fbf034ad04b90", "text layer"),
    "clamer1989": ("Clamer, C. 1989. 'Ain ez-Zara Excavations 1986. ADAJ 33: 217-225",
                   DOA + "42/ADAJ_1989_33-217-225.pdf", "420d50f3a2ee372cf7c60a05afba901e2985643868712315e99397c99fc344ee", "OCR"),
    "khalil1996": ("Khalil, H. 1996. Archaeological Survey of the East Coast of the Dead Sea: Phase 1: Suwayma, az-Zara and Umm Sidra. ADAJ 40: 429-449",
                   DOA + "75/ADAJ_1996_40-429-449.pdf", "d43ee59cb1c797bde9079f90305fc3d7ffaca21301bcb1dd8b955a79e4c63447", "OCR"),
    "waheeb1998": ("Waheeb, M. 1998. Wadi al-Kharrar Archaeological Project (al-Maghtas). ADAJ 42: 635-638",
                   DOA + "77/ADAJ_1998_42-635-638.pdf", "b28bb165069cd801237f931cbfb8ce12cd30775c8c8d7b0d3016af0be6ee2816", "OCR"),
    "waheeb2001": ("Waheeb, M. 2001. Recent Discoveries East of the Jordan River: Wadi al-Kharrar Archaeological Project. ADAJ 45: 419-426",
                   DOA + "40/ADAJ_2001_45-419-426.pdf", "2342f53de1325444c4d87a7867cd155d7e9b7b4a61f42160d75160f5f86e82ff", "OCR"),
    "waheeb2001shaj": ("Waheeb, M. 2001. Wadi al-Kharrar Archaeological Project (al-Maghtas). SHAJ 7: 591-600",
                       DOA + "193/SHAJ_7--591-600.pdf", "7936bf8d6cd594f1c10e3d3908a90b2ca0ba7296e95d260021f89c010d50e85f", "OCR"),
    "abushmais2002": ("Abu Shmais, A. and Waheeb, M. 2002. Recent Discoveries in the Baptism Site: The Pottery. ADAJ 46: 561-582",
                      DOA + "71/ADAJ_2002_46-561-582.pdf", "c5887a863114c2ac74cf13cd46758e549e094936449154186bc1f6f18bbda083", "OCR"),
    "lapp1962": ("Lapp, P. W. 1962. The 1961 Excavations at 'Araq el-Emir. ADAJ 6-7: 80-89",
                 DOA + "54/ADAJ_1962_6_7-80-89.pdf", "801e6ddf25c46254bb96a3102eec04cf09616096382b829400eccc83b4bd8ecb", "OCR"),
    "horn1972": ("Horn, S. H. 1972. The 1971 Season of Excavations at Tell Hesban. ADAJ 17: 15-22",
                 DOA + "51/ADAJ_1972_17%20-15-22.pdf", "2e9b1a8e240979988b7a6161ba53628d857e8ab1e9ba75d6ecdc04ec25347000", "OCR"),
    "ferguson2013": ("Ferguson, J. 2013. Pottery, chronology and cultural succession at Tall Madaba in the Late Hellenistic and Early Roman periods. SHAJ 11: 431-445",
                     DOA + "16/SHAJ_11-431-445.pdf", "d11c168eeabbeeec62951fcd99be55958db6d33e1600c6677f04a8b9ebc1b9fd", "OCR"),
    "pola2013": ("Pola, T. et al. 2013. A Preliminary Report of the Tulul adh-Dhahab (Wadi az-Zarqa) Survey and Excavation Seasons 2005-2011. ADAJ 57: 81-96",
                 DOA + "26/ADAJ_2013_57-81-96.pdf", "2d93c3d7d7308302b7ff09aa244761d489d7377680ee2fc1309318fa98b99f0c", "text layer"),
    "collins2009": ("Collins, S. et al. 2009. Tall al-Hammam: Preliminary Report on Four Seasons of Excavation (2006-2009). ADAJ 53: 385-414",
                    DOA + "66/ADAJ_2009_53-385-414.pdf", "fb398208351e9103267898716eb4c4a37ef26fc11484742ff6192d0025f5af8f", "text layer"),
    "kafrayn2012": ("Papadopoulos, T. J. et al. 2012. Tall al-Kafrayn: Preliminary Report on the University of Ioannina Excavations: 2010 and 2011 Seasons. ADAJ 56: 363-380",
                    DOA + "44/ADAJ_2012_56-363-380.pdf", "9c193421020064fee8c302ef5e04de669547a7cc25dfa2cb74042daac163ea8c", "text layer"),
    "nimrin1990": ("McCreery, D. W. and Flanagan, J. W. 1990. First Preliminary Report of the 1989 Tell Nimrin Project. ADAJ 34: 131-152",
                   DOA + "64/ADAJ_1990_34-131-152.pdf", "762416ed360984c1d6a9c0358d278c72e922dbc015606074defd7f998a511a91", "OCR"),
    "nimrin1992": ("McCreery, D. W., Flanagan, J. W. et al. 1992. Preliminary Report of the 1990 Excavation at Tell Nimrin. ADAJ 36: 89-111",
                   DOA + "41/ADAJ_1992_36-89-111.pdf", "3d60902c8c3450cabb19947bb59f58b162cba46e098184901df1331acc283390", "OCR"),
    "bisheh1973": ("Bisheh, G. 1973. Rock-Cut Tombs at Rajib. ADAJ 18: 63-67",
                   DOA + "36/ADAJ_1973_18-63-67.pdf", "16228f5aea5a1ab13e27705cb2d5da47c45ce8873e377e508103cf0c8039159c", "OCR"),
    "hadidi1979": ("Hadidi, A. 1979. A Roman Family Tomb at es-Salt. ADAJ 23: 129-137",
                   DOA + "105/ADAJ_1979_23-129-137.pdf", "240af19769264986bed48c0b235612bfa34d86b6bfbfde3b31111e29fd14fdde", "OCR"),
    "aij1": ("ACOR. 2018. Archaeology in Jordan 1 (2016 and 2017 seasons), entire volume (Pella, S. Bourke, pp. 23-24; Khirbat al-Mukhayyat, D. Foran, p. 50; Machaerus, G. Voros, pp. 57-58)",
             "https://publications.acorjordan.org/download/aij-1-2017-2017-entire-volume/", "0c43eaad5db23076e8b89cff46c572e420fc71fc3f8e480f813f04c2a1cf41b4", "text layer"),
    "aij2": ("ACOR. 2020. Archaeology in Jordan 2 (2018 and 2019 seasons), entire volume (Gadara/Umm Qays Hinterland Survey, p. 19)",
             "https://publications.acorjordan.org/download/aij-2-2018-2019-entire-volume/", "e772a591ec197b4e3006c684b831512450675c79204802cd9d37157369989179", "text layer"),
    "josephus_war": ("Josephus, The Wars of the Jews, tr. W. Whiston (public domain), Project Gutenberg eBook 2850; cited Book.Chapter.Section (Whiston)",
                     "https://www.gutenberg.org/cache/epub/2850/pg2850.txt", "9a72663aefa6b22bb4398d5f878bb027c6b6de839e7cbe744a34240505fd8d20", "text"),
    "josephus_ant": ("Josephus, Antiquities of the Jews, tr. W. Whiston (public domain), Project Gutenberg eBook 2848; cited Book.Chapter.Section (Whiston)",
                     "https://www.gutenberg.org/cache/epub/2848/pg2848.txt", "bb2e32da8ba3adc109b7694e6a8f2f11570462af2bedd55798da70b754c6e440", "text"),
    "wikidata": ("Wikidata entity JSON (Special:EntityData) and English Wikipedia article coordinates, read 9 October 2026",
                 "https://www.wikidata.org/wiki/Special:EntityData/", "", "JSON/HTML"),
}

# ----------------------------------------------------------------------------------------------- sites
# coordinates: ("pg", E_km, N_km, citation) for a printed Palestine Grid reference, ("ll", lat, lon, citation) otherwise
SITES = [
    dict(site_id="machaerus", name="Machaerus (Qal'at al-Mishnaqa, Mukawir)", ancient_name="Machaerus",
         identification="EVIDENCE", identification_note="Excavated citadel, lower city and Roman siege works (Strobel 1974; Voros 2018)",
         coord=("ll", 31.56722, 35.62417, "English Wikipedia 'Machaerus' (Wikidata Q1549278) page coordinate; Wikidata P625 (31.56694, 35.63361, used by W2B) lies 0.9 km east, beside Mukawir village"),
         sigma_km=0.3, sigma_basis="citadel about 100 x 60 m plus a lower city of about 7 dunams (Loffreda 1981 p. 92); page coordinate precision about 0.1 km",
         occupation="Hasmonean (c. 90-57 BC), Herodian (c. 30 BC-36 AD), Early Roman garrison (44-71 AD)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="voros2018 p. 449; loffreda1981 p. 90",
         marker_text="Built by Alexander Jannaeus, rebuilt by Herod with reservoirs", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 7.6.2",
         marker_arch="Hasmonean and Herodian miqvaot; Hasmonean towers", marker_arch_label="EVIDENCE", marker_arch_cite="voros2018 pp. 445-449; loffreda1981 p. 90",
         peraea_proper="yes", peraea_basis="Josephus War 3.3.3 names Machaerus as the southern end of Peraea",
         status="documented", status_reason="occupation and markers both EVIDENCE"),
    dict(site_id="kh_ataruz", name="Khirbat 'Ataruz", ancient_name="",
         identification="n.a.", identification_note="",
         coord=("ll", 31.57442, 35.66475, "English Wikipedia 'Khirbat Ataruz' (Wikidata Q100233378) page coordinate"),
         sigma_km=0.3, sigma_basis="page coordinate; site extent not stated in the sources read",
         occupation="late Hellenistic - early Roman ceramic fills and building remains", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="ji2009 p. 624 (excavator's report)",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="underground ritual bath (miqveh) on the eastern slope", marker_arch_label="EVIDENCE", marker_arch_cite="ji2009 p. 624",
         peraea_proper="yes", peraea_basis="INFERENCE: inside the Machaerus-Pella latitude band, west of Philadelphia; Ji 2009 p. 620 notes the area may have been Nabataean at times",
         status="documented", status_reason="occupation and archaeological marker both EVIDENCE (excavator)"),
    dict(site_id="callirrhoe", name="'Ain az-Zara (Callirrhoe), Building A (Zara 4)", ancient_name="Callirrhoe",
         identification="INFERENCE", identification_note="Herodian spa identified with 'Ain az-Zara by the excavators (Strobel 1997; Clamer 1989); hot springs as in War 1.33.5",
         coord=("pg", 203.450, 111.750, "khalil1996 p. 436 (Zara 4, P.G. 111.750N; 203.450E)"),
         sigma_km=0.3, sigma_basis="printed grid reference to 1 m; oasis buildings spread over about 0.5 km",
         occupation="Early Roman (end 1st c. BC/beginning 1st c. AD to end 1st/beginning 2nd c. AD)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="clamer1989 p. 222",
         marker_text="Herod bathed in the hot baths at Callirrhoe", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 1.33.5",
         marker_arch="coins of the First Jewish Revolt in the deposits", marker_arch_label="EVIDENCE", marker_arch_cite="clamer1989 p. 223",
         peraea_proper="yes", peraea_basis="INFERENCE: east shore of the Dead Sea between Machaerus and Pella",
         status="documented", status_reason="occupation EVIDENCE; textual marker rests on the Callirrhoe identification, archaeological marker EVIDENCE"),
    dict(site_id="kh_al_mukhayyat", name="Khirbat al-Mukhayyat (town of Nebo)", ancient_name="Nebo (town)",
         identification="INFERENCE", identification_note="Town of Nebo identification by the excavators (AIJ 1 p. 50)",
         coord=("ll", 31.76778, 35.72528, "English Wikipedia 'Khirbet al-Mukhayyat' page coordinate (Wikidata Q6401771 gives 31.76667, 35.71667 at 0.017 deg precision)"),
         sigma_km=0.5, sigma_basis="page coordinate; Wikidata point 0.8 km away",
         occupation="Late Hellenistic (miqveh); Hasmonean and Herodian coins", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="aij1 p. 50; jilee2004 p. 182",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="plaster-lined stepped ritual bath (miqveh); coins of Alexander Jannaeus", marker_arch_label="EVIDENCE", marker_arch_cite="aij1 p. 50; jilee2004 p. 182",
         peraea_proper="yes", peraea_basis="INFERENCE: between Machaerus and Pella, west of Philadelphia",
         status="documented", status_reason="occupation and archaeological marker both EVIDENCE"),
    dict(site_id="madaba", name="Tall Madaba (Madaba)", ancient_name="Medaba",
         identification="EVIDENCE", identification_note="",
         coord=("ll", 31.71667, 35.80000, "English Wikipedia 'Madaba' page coordinate (town; Tall Madaba lies in the town centre)"),
         sigma_km=0.7, sigma_basis="town-level coordinate at 1-arcminute precision",
         occupation="Late Hellenistic Phases 6-5 (late 2nd c. BC to c. 63 BC)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="ferguson2013 p. 433",
         marker_text="Taken by John Hyrcanus; held by Jannaeus; ceded to Aretas", marker_text_label="EVIDENCE", marker_text_cite="josephus_ant 13.9.1; 13.15.4; 14.1.4",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: Ferguson 2013 p. 433 calls it part of the Judaean Peraea 129-63 BC",
         status="documented", status_reason="occupation and textual marker both EVIDENCE"),
    dict(site_id="tall_hisban", name="Tall Hisban", ancient_name="Esbus / Heshbon",
         identification="EVIDENCE", identification_note="",
         coord=("ll", 31.80083, 35.80889, "English Wikipedia 'Heshbon' (Wikidata Q1615584) page coordinate"),
         sigma_km=0.3, sigma_basis="page coordinate; tall a few hundred metres across",
         occupation="Stratum 15 late Hellenistic fort; Stratum 14 early Roman village", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="ji2009 p. 621; horn1972 p. 18",
         marker_text="Heshbon among Moabite cities held by the Jews; Hesebonitis settled by Herod", marker_text_label="EVIDENCE", marker_text_cite="josephus_ant 13.15.4; 15.8.5",
         marker_arch="Alexander Jannaeus coin on the fort's bedrock; rolling-stone tombs", marker_arch_label="EVIDENCE", marker_arch_cite="ji2009 pp. 621-622",
         peraea_proper="yes", peraea_basis="INFERENCE: between Machaerus and Pella, west of Philadelphia",
         status="documented", status_reason="occupation and markers EVIDENCE (reported by Ji 2009 from the excavation reports)"),
    dict(site_id="iraq_al_amir", name="'Iraq al-Amir (village and Qasr al-'Abd)", ancient_name="Tyre (Birta) of the Tobiads",
         identification="INFERENCE", identification_note="Josephus Ant. 12.4.11 describes Hyrcanus' castle 'Tyre'; identification with Qasr al-'Abd is standard but is an identification",
         coord=("ll", 31.91280, 35.75180, "English Wikipedia 'Qasr al-Abd' (Wikidata Q7267043) page coordinate"),
         sigma_km=0.6, sigma_basis="the excavated village lies about 0.5 km from the Qasr (Lapp 1962 p. 80)",
         occupation="Stratum IIIb late 2nd c. BC, used to about the mid-1st c. AD", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="lapp1962 p. 89",
         marker_text="Tobiad Hyrcanus' estate beyond Jordan (before the window)", marker_text_label="EVIDENCE", marker_text_cite="josephus_ant 12.4.11",
         marker_arch="coins of Alexander Jannaeus (village and gateway)", marker_arch_label="EVIDENCE", marker_arch_cite="jilee2004 p. 182 (citing Lapp 1983 and Dentzer et al. 1983)",
         peraea_proper="yes", peraea_basis="INFERENCE: between Machaerus and Pella, west of Philadelphia",
         status="documented", status_reason="occupation EVIDENCE; Hasmonean coins EVIDENCE (secondary report)"),
    dict(site_id="kh_as_sur", name="Khirbat as-Sur (Survey Site 67)", ancient_name="",
         identification="n.a.", identification_note="",
         coord=("pg", 217.5, 145.9, "jilee1998 p. 597 (Site 67, PG 217.5/145.9)"),
         sigma_km=0.3, sigma_basis="grid reference to 100 m; site about 200 x 400 m",
         occupation="Hellenistic-Byzantine fort; Hellenistic-early Roman coins and pottery", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="jilee2004 p. 181; jilee1998 p. 597",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="one Hasmonean coin of John Hyrcanus I (surface coin survey)", marker_arch_label="EVIDENCE", marker_arch_cite="jilee2004 p. 181",
         peraea_proper="yes", peraea_basis="INFERENCE: between Machaerus and Pella, west of Philadelphia",
         status="documented", status_reason="occupation and marker EVIDENCE; the marker is a single surface coin"),
    dict(site_id="umm_hadar", name="Umm Hadar / Rujm Umm Haddar (Survey Site 118)", ancient_name="",
         identification="n.a.", identification_note="",
         coord=("pg", 214.2, 141.2, "jilee1999 p. 532 (Site 118, PG 214.2/141.2)"),
         sigma_km=0.2, sigma_basis="grid reference to 100 m; fort 40.7 x 30.8 m",
         occupation="mid-2nd to mid-1st c. BC fort (Hasmonean ceramic tradition)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="salles2013 p. 252; salles2009 p. 150",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="Hasmonean coins (two of Hyrcanus II); Judaean four-handled jars", marker_arch_label="EVIDENCE", marker_arch_cite="salles2013 p. 255; jilee2004 p. 181; salles2009 p. 146",
         peraea_proper="yes", peraea_basis="INFERENCE: lower Wadi al-Kafrayn, between Machaerus and Pella",
         status="documented", status_reason="occupation and marker both EVIDENCE (excavation)"),
    dict(site_id="tall_barakat", name="Tall Barakat (Survey Site 178)", ancient_name="",
         identification="n.a.", identification_note="",
         coord=("pg", 213.87, 140.08, "jilee2002 p. 184 (Site 178, PG 213.87/140.08)"),
         sigma_km=0.2, sigma_basis="grid reference to 10 m; citadels a few hundred metres across",
         occupation="late Hellenistic-early Roman fortress (late 2nd-early 1st c. BC)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="jilee2002 p. 185",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="eight Hasmonean coins (Hyrcanus I or Jannaeus, Aristobulus, Jannaeus)", marker_arch_label="EVIDENCE", marker_arch_cite="jilee2004 p. 181",
         peraea_proper="yes", peraea_basis="INFERENCE: lower Wadi al-Kafrayn, between Machaerus and Pella",
         status="documented", status_reason="occupation (survey) and coin marker EVIDENCE"),
    dict(site_id="tulul_adh_dhahab_w", name="Tulul adh-Dhahab, western hill (Tall adh-Dhahab al-Gharbiya)", ancient_name="Amathus? / Essa?",
         identification="CLAIM", identification_note="Amathus proposed here by Thiel 2005 (via Pola 2013 p. 87); Kokkinos 2001 prefers Tall 'Ammata, Mittmann Tall al-Mughanni",
         coord=("pg", 214.9, 177.1, "pola2013 p. 82 (PG 2149.1771)"),
         sigma_km=0.3, sigma_basis="grid reference to 100 m; hill about 130 x 50 m; Wikidata 'Amathus' point (used by W2B) lies 0.1 km away",
         occupation="Hellenistic building erected 2nd-early 1st c. BC, burnt before the mid-1st c. BC", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="pola2013 pp. 92-95",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="latest coins are of Alexander Jannaeus (80/76 BC)", marker_arch_label="EVIDENCE", marker_arch_cite="pola2013 p. 94",
         peraea_proper="yes", peraea_basis="INFERENCE: Wadi az-Zarqa, between Machaerus and Pella; not a Decapolis city",
         status="documented", status_reason="occupation and coin marker EVIDENCE; the Amathus identification is not used"),
    dict(site_id="kharrar", name="Wadi al-Kharrar: Tall al-Kharrar (Elijah's Hill) and Site 7", ancient_name="Bethany beyond the Jordan (tradition)",
         identification="TRADITION", identification_note="John 1:28 place identified here by Byzantine pilgrims and the excavators",
         coord=("ll", 31.83722, 35.55028, "English Wikipedia 'Al-Maghtas' (Wikidata Q12193567) page coordinate (baptism area)"),
         sigma_km=1.5, sigma_basis="INFERENCE: Tall al-Kharrar lies about 2 km east of the river (Waheeb 1998 p. 636); the page point is the river-side baptism area",
         occupation="Pre and early Roman phase I (ca. 100 BC-AD 73)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="abushmais2002 pp. 562, 569",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="chalk stone cups (1st c. BC); Herodian lamps; coin of AD 9-11", marker_arch_label="EVIDENCE", marker_arch_cite="abushmais2002 pp. 562, 565, 569",
         peraea_proper="yes", peraea_basis="INFERENCE: east bank of the Jordan opposite Jericho",
         status="documented", status_reason="occupation and stone-vessel marker EVIDENCE; the Bethany identification is TRADITION and is not used"),
    dict(site_id="pella", name="Pella (Tabaqat Fahl)", ancient_name="Pella",
         identification="EVIDENCE", identification_note="Decapolis city",
         coord=("ll", 32.45000, 35.61667, "English Wikipedia 'Pella, Jordan' page coordinate (1-arcminute precision)"),
         sigma_km=0.7, sigma_basis="page precision",
         occupation="Late Hellenistic town house with Hasmonean-period (ca. 83/80 BC) destruction", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="aij1 p. 24",
         marker_text="Pella destroyed by the Jews for refusing Jewish customs", marker_text_label="EVIDENCE", marker_text_cite="josephus_ant 13.15.4",
         marker_arch="Hasmonean-period destruction layer", marker_arch_label="EVIDENCE", marker_arch_cite="aij1 p. 24",
         peraea_proper="no", peraea_basis="Decapolis city; Josephus War 3.3.3 uses it as Peraea's northern boundary",
         status="documented", status_reason="occupation and marker EVIDENCE; Decapolis city, outside Peraea proper"),
    dict(site_id="tell_er_rameh", name="Tell er-Rameh", ancient_name="Betharamphtha / Livias / Julias",
         identification="TRADITION", identification_note="Traditional Livias; Graves and Stripling (via Wikipedia) put the administrative centre at Tall el-Hammam",
         coord=("ll", 31.82556, 35.64444, "Wikidata Q85805483 P625"),
         sigma_km=0.3, sigma_basis="small tall; city extent unknown",
         occupation="'Early Roman' surface sherds", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="kokkinos2001 p. 480 (surface collection)",
         marker_text="Antipas walled Betharamphtha and renamed it Julias", marker_text_label="EVIDENCE", marker_text_cite="josephus_ant 18.2.1",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: Jordan valley east of Jericho",
         status="partial", status_reason="the textual marker applies only through the Livias identification (TRADITION)"),
    dict(site_id="tall_el_hammam", name="Tall el-Hammam (Field UA and lower tall)", ancient_name="Abila? / Livias? (proposals)",
         identification="CLAIM", identification_note="Abel-Shittim/Abila or Livias proposals (Collins 2009 n. 6; Wikipedia 'Livias')",
         coord=("ll", 31.84018, 35.67368, "Wikidata Q55634648 P625"),
         sigma_km=0.4, sigma_basis="tall proper 36 ha",
         occupation="Hellenistic and Early Roman pottery incl. a Herodian-style lamp (Field UA)", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="collins2009 p. 410",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: Jordan valley between Machaerus and Pella",
         status="partial", status_reason="no marker except proposed identifications (CLAIM)"),
    dict(site_id="kh_al_habbasa", name="Khirbat al-Habbasa (Survey Site 180)", ancient_name="Herodium II? (Kokkinos)",
         identification="CLAIM", identification_note="Kokkinos 2001 p. 479: 'may be identified with' the fortress Herodium II",
         coord=("pg", 214.43, 139.18, "jilee2002 p. 185 (Site 180, PG 214.43/139.18)"),
         sigma_km=0.2, sigma_basis="grid reference to 10 m",
         occupation="sparse late Hellenistic-early Roman pottery", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="jilee2002 p. 187",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: lower Wadi al-Kafrayn",
         status="partial", status_reason="no marker except a proposed identification (CLAIM); the 2001 coin survey found no Hellenistic coins (jilee2004 p. 181)"),
    dict(site_id="tall_ammata", name="Tall 'Ammata", ancient_name="Amathus? (Kokkinos)",
         identification="CLAIM", identification_note="Kokkinos 2001 p. 481: Amathus 'probable' here; alternatives Tulul adh-Dhahab, Tall al-Mughanni",
         coord=None,
         sigma_km=None, sigma_basis="no coordinate found in an open source read (JADIS 2018003; north bank of Wadi Rajib, Kokkinos 2001 p. 481)",
         occupation="Hellenistic and Early Roman surface sherds", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="kokkinos2001 p. 481 (surface)",
         marker_text="Amathus taken by Jannaeus; council seat under Gabinius", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 1.4.2; 1.8.5",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: Jordan valley between Machaerus and Pella",
         status="partial", status_reason="the textual marker applies only through the Amathus identification (CLAIM); no coordinate"),
    dict(site_id="tall_al_umayri", name="Tall al-'Umayri", ancient_name="",
         identification="n.a.", identification_note="",
         coord=("ll", 31.86861, 35.88806, "English Wikipedia 'Tall al-Umayri' (Wikidata Q12203045) page coordinate"),
         sigma_km=0.3, sigma_basis="page coordinate",
         occupation="late Hellenistic farming village", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="ji2009 p. 622 (citing Herr et al. 1999)",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="plaster-lined bath called a miqveh by Ji (not the excavators)", marker_arch_label="CLAIM", marker_arch_cite="ji2009 p. 622",
         peraea_proper="yes", peraea_basis="INFERENCE: west of Philadelphia; Ji 2009 places it in the Hasmonean-Herodian zone",
         status="partial", status_reason="the ritual-bath reading is Ji's, and its date is disputed (LH or ER)"),
    dict(site_id="tell_nimrin", name="Tell Nimrin", ancient_name="Bethennabris? (Beth Nimrah)",
         identification="INFERENCE", identification_note="Beth Nimrah/Bethennabris identification (Wikipedia 'Beth Nimrah')",
         coord=("ll", 31.90900, 35.63800, "English Wikipedia 'Beth Nimrah' (Wikidata Q4897428) page coordinate"),
         sigma_km=0.3, sigma_basis="page coordinate",
         occupation="Hellenistic and Roman surface sherds; Roman pits", occupation_window="overlaps", occupation_label="EVIDENCE",
         occupation_cite="nimrin1990 p. 136; nimrin1992 p. 98",
         marker_text="Bethennabris village in the Gadara campaign of AD 68", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 4.7.4",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: Jordan valley between Machaerus and Pella",
         status="partial", status_reason="occupation only 'Roman' undivided; marker depends on the identification (INFERENCE)"),
    dict(site_id="kh_sar", name="Khirbat Sar (Survey Site 210)", ancient_name="Herod's captured Nabataean fort? (Ji)",
         identification="CLAIM", identification_note="Ji 2009 p. 620 proposes the fort Herod took in 31 BC",
         coord=("pg", 228.60, 150.40, "jilee2002 p. 193 (Site 210, PG 228.60/150.40)"),
         sigma_km=0.2, sigma_basis="grid reference to 10 m",
         occupation="copious early Roman pottery; Hellenistic material", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="ji2009 p. 620",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE: west of Philadelphia",
         status="partial", status_reason="no marker except a proposed identification (CLAIM)"),
    dict(site_id="tall_jadur", name="Tall Jadur (near as-Salt)", ancient_name="Gadara/Gadora of Peraea?",
         identification="INFERENCE", identification_note="'best candidate' for Peraean Gadara (Ji 2009 p. 620; Kokkinos 2001 p. 480)",
         coord=None, sigma_km=None, sigma_basis="no coordinate found in an open source read",
         occupation="not recorded in the sources read", occupation_window="unknown", occupation_label="",
         occupation_cite="",
         marker_text="Gadara, 'the metropolis of Perea', taken by Vespasian", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 4.7.3",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE",
         status="partial", status_reason="identification INFERENCE; occupation UNKNOWN (silence is not absence); no coordinate"),
    dict(site_id="tall_al_kafrayn", name="Tall (Khirbat) al-Kafrayn", ancient_name="Abila of Peraea?",
         identification="INFERENCE", identification_note="Abila = Kh. al-Kafrayn (Kokkinos 2001 p. 480; Wikipedia 'Abila (Peraea)'); Zayadine prefers Tall al-Hammam (Salles 2009 p. 138 n. 1)",
         coord=("ll", 31.84972, 35.67861, "English Wikipedia 'Abila (Peraea)' (Wikidata Q2236536) page coordinate"),
         sigma_km=0.4, sigma_basis="page coordinate; large site",
         occupation="Iron Age excavated; 'no archaeological remains of the Hellenistic period' reported", occupation_window="unknown", occupation_label="EVIDENCE",
         occupation_cite="salles2009 p. 138 n. 1; kafrayn2012 pp. 363-380",
         marker_text="Abila taken by Placidus in AD 68", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 4.7.6",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE",
         status="partial", status_reason="identification INFERENCE; Roman occupation UNKNOWN in the sources read"),
    dict(site_id="gadara_umm_qais", name="Umm Qays (Gadara of the Decapolis)", ancient_name="Gadara",
         identification="EVIDENCE", identification_note="Decapolis city",
         coord=("ll", 32.65417, 35.68750, "English Wikipedia 'Umm Qais' (Wikidata Q131955) page coordinate"),
         sigma_km=0.5, sigma_basis="page coordinate",
         occupation="not read in the sources used (Hellenistic Gadara reports listed, not opened)", occupation_window="unknown", occupation_label="",
         occupation_cite="",
         marker_text="Jannaeus took Gadara", marker_text_label="EVIDENCE", marker_text_cite="josephus_war 1.4.2",
         marker_arch="a mikveh among quarries in the hinterland (undated)", marker_arch_label="EVIDENCE", marker_arch_cite="aij2 p. 19",
         peraea_proper="no", peraea_basis="Decapolis city",
         status="partial", status_reason="occupation in the window not read; hinterland mikveh undated"),
    dict(site_id="rajib_tombs", name="Rajib rock-cut tombs (east of Amman)", ancient_name="",
         identification="n.a.", identification_note="Not Ragaba: this Rajib lies by the Cave of the Seven Sleepers near Amman",
         coord=None, sigma_km=None, sigma_basis="no coordinate recorded",
         occupation="Tomb 1: Herodian lamps, 1st c. AD cooking pot; Tomb 2 2nd-3rd c. AD", occupation_window="yes", occupation_label="EVIDENCE",
         occupation_cite="bisheh1973 pp. 63-65",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="no", peraea_basis="Philadelphia territory (INFERENCE)",
         status="excluded", status_reason="no Jewish, Hasmonean or Herodian marker (Herodian-type lamps are not a plan marker)"),
    dict(site_id="es_salt_tomb", name="es-Salt Roman family tomb", ancient_name="",
         identification="n.a.", identification_note="",
         coord=None, sigma_km=None, sigma_basis="no coordinate recorded",
         occupation="Roman family tomb with a coin of Constantine I", occupation_window="no", occupation_label="EVIDENCE",
         occupation_cite="hadidi1979 pp. 129-137",
         marker_text="", marker_text_label="", marker_text_cite="",
         marker_arch="", marker_arch_label="", marker_arch_cite="",
         peraea_proper="yes", peraea_basis="INFERENCE",
         status="excluded", status_reason="dated after the window; no marker"),
]

# --------------------------------------------------------------------------------------------- features
# (site_id, feature_type, subtype as given, position as given, period as given, dated_in_window, label, cite, quote, notes)
FEATURES = [
    ("machaerus", "cistern", "Hasmonean cistern 15.5 m deep, 110 m3", "citadel, 7 m from the Hasmonean mikveh", "Hasmonean", "yes", "EVIDENCE", "voros2018 p. 449; voros2016 p. 535", "fully excavated a 15.5 meter deep Hasmonean cistern", "used in the Herodian period too (voros2016 p. 530)"),
    ("machaerus", "pool", "Hasmonean mikveh", "under the south-eastern Doric porticus corridor", "Hasmonean", "yes", "EVIDENCE", "voros2018 p. 447 (citing Corbo 1980: 368)", "the Franciscan Mission discovered a Hasmonean period mikveh", "filled by the Herodian builders"),
    ("machaerus", "cistern", "Herodian cistern 9.5 m deep, about 380 m3", "centre of the peristyle Doric royal courtyard", "Herodian", "yes", "EVIDENCE", "voros2018 p. 437; voros2016 p. 535", "the 9.5 meter deep Herodian cistern in the center of the peristyle", ""),
    ("machaerus", "pool", "small Herodian royal mikveh (1968)", "outside the walls of the royal bathhouse", "Herodian", "yes", "EVIDENCE", "voros2018 p. 445", "small ritual immersion bath", "vaulted roof in situ"),
    ("machaerus", "pool", "king-size royal mikveh with 12 steps (2016)", "northern wing of the palace, inside the Hasmonean-origin tower", "Herodian (c. 30 BC)", "yes", "EVIDENCE", "voros2018 pp. 446-447; aij1 p. 58", "the newly discovered king-size mikveh", "used as a kitchen after 44 AD"),
    ("machaerus", "cistern", "cistern 6 m deep beside the king-size mikveh ('otzar')", "just before the ritual bath", "Herodian", "yes", "EVIDENCE", "voros2018 p. 446", "a newly discovered six meter deep cistern", "no stairs"),
    ("machaerus", "pool", "small northern Herodian royal mikveh (2017)", "citadel, by the Early Roman surrounding wall", "Herodian (destroyed probably 36 AD)", "yes", "EVIDENCE", "voros2018 p. 446 (Fig. 14)", "the small northern Herodian royal mikveh in the citadel", ""),
    ("machaerus", "pool", "private domestic mikveh (1981)", "outside the citadel walls, in a house of the lower city", "Herodian lower city", "yes", "EVIDENCE", "voros2018 p. 445 (citing Corbo-Loffreda 1981: 284)", "in a house in the lower city of Machaerus", "excavators: ritual use 'cannot be excluded'"),
    ("machaerus", "pool", "overflowing plastered rainwater basins", "citadel water-harvesting system", "Herodian", "yes", "EVIDENCE", "voros2018 p. 446", "series of overflowing plastered rainwater basins", ""),
    ("machaerus", "pool", "plastered pool of the frigidarium", "royal bathhouse", "Herodian", "yes", "EVIDENCE", "voros2018 p. 452 (Fig. 26)", "the lower stratum in the plastered pool of the frigidarium", "non-ritual (Corbo 1979)"),
    ("machaerus", "tower", "fourth tower of the palace, converted into bath and cistern-reservoir", "northern wing, outside the Early Roman wall", "Hasmonean foundations; Herodian conversion", "yes", "EVIDENCE", "voros2018 p. 438", "a huge fortification tower, with Hasmonean foundations", ""),
    ("machaerus", "tower", "three towers on the crest", "crest of the mound", "Hasmonaean", "yes", "EVIDENCE", "loffreda1981 p. 90", "The three towers on the crest of the mound", "re-used in the Herodian period"),
    ("machaerus", "wall", "defensive wall G between towers 1 and 2", "south flank of the later Thermae", "Hasmonaean", "yes", "EVIDENCE", "loffreda1981 p. 90", "a massive defensive wall of the Hasmonaean fortress", ""),
    ("machaerus", "cistern", "white plastered structure, possibly a cistern", "locus 12 of the Praefurnium, against wall G", "Hasmonaean", "yes", "EVIDENCE", "loffreda1981 p. 90", "a white plastered Hasmonaean structure, possibly a water cistern", "function uncertain in the source"),
    ("machaerus", "tower", "tower n. 5", "northern slope of Jabal Mishnaqa", "Hasmonaean; resettled in the Herodian period", "yes", "EVIDENCE", "loffreda1981 p. 92", "definite proof that tower n.5 was built by the Hasmonaeans", "Hasmonaean coins in room 1"),
    ("machaerus", "cistern", "rock-cut water reservoir 8 m deep entered from tower n. 5 room 2", "northern slope, connected to tower n. 5", "Hasmonaean (by association with tower n. 5)", "yes", "EVIDENCE", "loffreda1981 p. 92", "connected to a huge rock-cut water reservoir, 8 m. deep", "the source says the entrance was masked and blocked in antiquity"),
    ("machaerus", "cistern", "numerous rock-cut water reservoirs", "eastern flank (proposed lower city)", "not dated", "undated", "EVIDENCE", "loffreda1981 p. 92", "numerous rock-cut water reservoirs still visible in this area", ""),
    ("machaerus", "wall", "walls B, C, D with towers n. 5-6", "eastern flank of Jabal Mishnaqa", "not dated (tower n. 5 Hasmonaean)", "undated", "EVIDENCE", "loffreda1981 p. 92", "protected by free standing walls and towers", ""),
    ("machaerus", "channel", "aqueduct on a 'bridge' from the plateau", "east side, between the plateau of Meqawer and the fortress hill", "not dated in the source", "undated", "EVIDENCE", "piccirillo1979 p. 180; strobel1974 p. 102", "It is the foundation of an aqueduct which collected the water", "Strobel infers it was demolished in the 72 AD siege (INFERENCE)"),
    ("machaerus", "cistern", "series of cisterns fed by the aqueduct", "northern slope of the fortress", "not dated in the source", "undated", "EVIDENCE", "piccirillo1979 p. 180", "the series of cisterns excavated on the northern slope", ""),
    ("machaerus", "wall", "Roman circumvallation 3.5 km long, 1.8-2 m wide", "around the hill", "72 AD", "yes", "EVIDENCE", "strobel1974 pp. 101, 120; voros2018 p. 450", "the Roman circumvallation, erected in 72 AD", "with camps and a siege ramp"),
    ("machaerus", "wall", "polygonal surrounding wall of the Early Roman garrison", "around the citadel", "Early Roman (ca. 44-71 AD)", "yes", "EVIDENCE", "voros2018 p. 437", "polygonal surrounding wall of the citadel is not from the Herodian period", ""),
    ("machaerus", "cave", "cave with a north-facing entrance", "beside the main Roman camp east of the fortress", "not dated", "undated", "EVIDENCE", "strobel1974 p. 120", "A cave nearby, the entrance of which faces North", "not investigated"),
    ("kh_ataruz", "pool", "underground ritual bath (miqveh)", "eastern slope", "late Hellenistic-early Roman context (Hasmonean-Herodian)", "yes", "EVIDENCE", "ji2009 p. 624", "underground ritual bath known as miqveh", "dated by context and type"),
    ("kh_al_mukhayyat", "pool", "plaster-lined stepped ritual bath (miqveh)", "western edge of Field C, by the Iron Age fortification wall", "Late Hellenistic", "yes", "EVIDENCE", "aij1 p. 50", "stepped ritual bath (or miqveh) dated to the Late Hellenistic period", "plaster installations around it"),
    ("tall_hisban", "wall", "late Hellenistic fort (Stratum 15)", "summit", "late Hellenistic", "yes", "EVIDENCE", "ji2009 p. 621", "Stratum 15 appears to have been a late Hellenistic military fort", "Jannaeus coin on the bedrock"),
    ("tall_hisban", "tomb", "tombs with rolling-stone doors and loculi", "Tall Hisban", "early Roman", "yes", "EVIDENCE", "ji2009 p. 621 (citing Waterhouse 1994, 1998)", "early Roman tombs with a rolling-stone door and interior individual loculi", ""),
    ("tall_hisban", "cistern", "unexcavated cistern, Square B.3", "Area B, shelf south of the acropolis", "early Roman (Stratum XII)", "yes", "EVIDENCE", "horn1972 p. 18", "An unexcavated cistern in Square B.3", ""),
    ("tall_hisban", "cave", "cave or cistern, Square B.4", "Area B, shelf south of the acropolis", "early Roman (Stratum XII)", "yes", "EVIDENCE", "horn1972 p. 18", "a partly excavated cave or cistern in Square B.4", ""),
    ("tall_hisban", "wall", "massive Wall B.1:17", "Area B", "possibly 1st c. AD (uncertain)", "undated", "EVIDENCE", "horn1972 p. 18", "Some evidence points to its construction in the 1st century A.D.", "the source leaves the date open"),
    ("tall_al_umayri", "pool", "plaster-lined bath (called a miqveh by Ji)", "Field A", "late Hellenistic or early Roman (disputed)", "yes", "EVIDENCE", "ji2009 p. 622", "plaster-lined bath of Field A", "the miqveh reading is Ji's (CLAIM)"),
    ("tall_al_umayri", "cave", "pits of the farming village", "southern summit", "late Hellenistic", "yes", "EVIDENCE", "ji2009 p. 622", "domestic buildings, semi-circular bins and several pits", ""),
    ("madaba", "wall", "late Hellenistic perimeter (fortification) wall", "Field B, inside the older city wall", "late Hellenistic (Phase 6, late 2nd c. BC)", "yes", "EVIDENCE", "ferguson2013 p. 433", "In the late Hellenistic period, a new perimeter wall was built", ""),
    ("madaba", "tower", "at least two towers", "Tall Madaba", "late Hellenistic", "yes", "EVIDENCE", "ji2009 p. 621 (citing Harrison et al. 2000)", "a series of walls, at least two towers", ""),
    ("iraq_al_amir", "wall", "village walls of Stratum IIIb", "north and east sides of the village", "late 2nd c. BC, used to mid-1st c. AD", "yes", "EVIDENCE", "lapp1962 p. 89", "major walls containing the city to the north and to the east", ""),
    ("iraq_al_amir", "channel", "aqueduct between the caves and the village", "between the inscribed caves and the village", "probably Hellenistic", "overlaps", "EVIDENCE", "lapp1962 p. 87", "An ancient (probably Hellenistic) aqueduct", "still in use in 1961"),
    ("iraq_al_amir", "cave", "caves with the Tobiah inscriptions", "cliffs about 220 m above the village", "not dated in this source", "undated", "EVIDENCE", "lapp1962 p. 80", "two famous inscriptions on cave entrances, naming Tobiah", "Josephus Ant. 12.4.11 describes Hyrcanus' caves"),
    ("iraq_al_amir", "cistern", "two plastered pits or cisterns", "outside the entrance of the Square Building", "construction date unclear; open in the 4th c. AD", "undated", "EVIDENCE", "lapp1962 p. 87", "Just outside the entrance were two pits or cisterns", ""),
    ("iraq_al_amir", "hoard", "Ptolemaic silver tetradrachm hoard (315 coins examined)", "found 1993 in a pipe trench at 'Iraq al-Amir", "3rd c. BC (latest 243/2 BC)", "no", "EVIDENCE", "kokkinos2001 p. 483 (Auge)", "un important trésor de monnaies d'argent ptolémaiques", "at least about a thousand coins reported"),
    ("kh_as_sur", "wall", "defence wall more than 2 m thick", "around the site", "Hellenistic-Byzantine fort", "overlaps", "EVIDENCE", "jilee1998 p. 597", "A massive defense wall which measures more than 2 m thick", ""),
    ("kh_as_sur", "cistern", "several large cisterns", "middle of the site", "not dated separately", "undated", "EVIDENCE", "jilee1998 p. 598", "several large cisterns located in the middle of this site", ""),
    ("umm_hadar", "cistern", "central cistern/well, 4.2 m internal diameter, >5 m deep", "centre of the courtyard", "fort period (mid-2nd to mid-1st c. BC)", "yes", "EVIDENCE", "salles2009 p. 145", "The well is the most massive construction of the site", "filled in one episode with the fort's debris"),
    ("umm_hadar", "channel", "basin about 1 x 1 m with a channel to the well", "north of the well", "fort period", "yes", "EVIDENCE", "salles2009 p. 145", "a nicely-built basin about 1 x 1m across and 0.6m deep", "possibly a decanting basin (source's question)"),
    ("umm_hadar", "tower", "north-western and north-eastern corner towers", "corners of the fort", "fort period", "yes", "EVIDENCE", "salles2009 p. 140", "the north-western tower, the north-eastern tower", ""),
    ("umm_hadar", "wall", "eastern curtain wall M20 with the main entrance", "east side of the fort", "fort period", "yes", "EVIDENCE", "salles2009 p. 144", "the main entrance pierced the eastern curtain wall, M20", ""),
    ("umm_hadar", "tomb", "graves cut into the courtyard floors", "courtyard of the ruined fort", "shortly after the fort's destruction", "yes", "EVIDENCE", "salles2013 p. 252", "ces tombes, creusées dans la cour", "dated only relative to the destruction (mid-late 1st c. BC)"),
    ("umm_hadar", "pool", "possible reservoir beside a run-off drainage (Umm Hadar 10)", "about 100 m west of the fort", "Hellenistic and Byzantine pottery", "overlaps", "EVIDENCE", "salles2009 p. 140 (quoting Waheeb 1997)", "a possible reservoir built beside the run-off water drainage", "not relocated in 2006-2008"),
    ("tall_barakat", "wall", "external defence walls of the upper citadel", "southern sides of the site", "late Hellenistic-early Roman", "yes", "EVIDENCE", "jilee2002 pp. 184-185", "The external defense walls measure approximately 1.5m thick", ""),
    ("tall_barakat", "tower", "towers of the lower citadel", "eastern terrace", "late Hellenistic-early Roman (late 2nd-early 1st c. BC)", "yes", "EVIDENCE", "jilee2002 pp. 184-185", "this lower citadel includes an enclosure wall, towers, cisterns, and aqueducts", "after Prag and Barnes 1996"),
    ("tall_barakat", "cistern", "cisterns of the lower citadel", "eastern terrace", "late Hellenistic-early Roman (late 2nd-early 1st c. BC)", "yes", "EVIDENCE", "jilee2002 pp. 184-185", "this lower citadel includes an enclosure wall, towers, cisterns, and aqueducts", "after Prag and Barnes 1996"),
    ("tall_barakat", "channel", "aqueducts of the lower citadel", "eastern terrace", "late Hellenistic-early Roman (late 2nd-early 1st c. BC)", "yes", "EVIDENCE", "jilee2002 pp. 184-185", "this lower citadel includes an enclosure wall, towers, cisterns, and aqueducts", "after Prag and Barnes 1996"),
    ("kh_al_habbasa", "cistern", "cisterns in the lower enclosure", "lower enclosure", "not dated separately (site LH-ER and LByz-EIsl)", "undated", "EVIDENCE", "jilee2002 p. 187", "ancient aqueducts which brought water to the cisterns in the lower enclosure", ""),
    ("kh_al_habbasa", "channel", "aqueducts from the plateau to the east", "east of the lower enclosure", "not dated separately", "undated", "EVIDENCE", "jilee2002 p. 187", "ancient aqueducts which brought water to the cisterns in the lower enclosure", ""),
    ("kh_al_habbasa", "wall", "main enclosure wall of the upper citadel", "upper citadel", "not dated separately", "undated", "EVIDENCE", "jilee2002 p. 187", "the line of a main enclosure wall", ""),
    ("kh_al_habbasa", "cistern", "large cisterns with a Roman fort", "hills east of Tall el-Hammam", "Roman", "overlaps", "EVIDENCE", "collins2009 p. 410", "Large cisterns and a fort (Roman) are present in the hills", ""),
    ("tulul_adh_dhahab_w", "wall", "defensive construction on the western slope", "between Terraces III and IV", "probably Hellenistic (source's inference)", "overlaps", "EVIDENCE", "pola2013 p. 88", "much more likely to have been constructed during the Hellenistic period", "foundation sherds Iron Age II"),
    ("tulul_adh_dhahab_w", "tower", "city-wall tower", "southern edge of Terrace II", "not dated (stones beneath dated 1305-978 BC)", "undated", "EVIDENCE", "pola2013 pp. 86-88", "A city wall tower at the southern edge of Terrace II", ""),
    ("tulul_adh_dhahab_w", "hoard", "small repository of inscribed lead sling bullets", "burnt layer on the stylobate, Square 92", "before the mid-1st c. BC destruction", "yes", "EVIDENCE", "pola2013 p. 93", "a small repository of which was found in the burnt layer", ""),
    ("callirrhoe", "pool", "Pool 338, plastered thermal pool fed by a hot spring", "Building A, north of Room 313, middle of the east wall", "Early Roman (silted up at the end of the period)", "yes", "EVIDENCE", "clamer1989 pp. 219, 221", "obviously represents a thermal bath or pool", "bottom not reached at 3.5 m"),
    ("callirrhoe", "channel", "plastered inlet and overflow channel of Pool 338", "walls W204 and W235", "Early Roman", "yes", "EVIDENCE", "clamer1989 p. 221", "a narrow channel for the overflow in its western wall", ""),
    ("callirrhoe", "pool", "swimming pool about 12 m long and 5 m deep with lower basins", "peristyle courtyard of the villa", "Herodian", "yes", "EVIDENCE", "strobel1997 pp. 271-272", "a swimming pool of about 12 m length and 5m depth", "may be the same structure as Pool 338 (not resolved)"),
    ("callirrhoe", "wall", "stone fence around the oasis", "around the oasis", "not dated in the source", "undated", "EVIDENCE", "strobel1997 p. 271", "once completely surrounded by a partially well-preserved stone fence", ""),
    ("callirrhoe", "wall", "harbour walls (Zara 21)", "shore about 0.3 km west of Building A", "not dated in the survey", "undated", "EVIDENCE", "khalil1996 p. 441", "Harbour with five or six long walls built with large limestone ashlars", "Strobel 1997 p. 271 describes harbour moles at the Herodian spa"),
    ("callirrhoe", "wall", "boulder wall 'Kanal' (Zara 5), 139.5 m", "upslope, above a stream course", "Roman (?)", "overlaps", "EVIDENCE", "khalil1996 p. 437", "A wall of comparatively large limestone boulders, two stones wide", ""),
    ("kharrar", "pool", "three pools with a drainage system", "around Tall al-Kharrar, mainly south", "early phase (site use early Roman to late Byzantine)", "overlaps", "EVIDENCE", "waheeb2001shaj p. 595", "three pools with the drainage system are attributable to this phase", "the source does not date the phase in years"),
    ("kharrar", "cistern", "three cisterns of Tall al-Kharrar", "slopes of the tall", "Roman (context of the aqueducts)", "overlaps", "EVIDENCE", "waheeb2001shaj pp. 592, 597", "especially the three cisterns of Tall al-Kharrar", ""),
    ("kharrar", "channel", "aqueducts from Wadi al-Kafrayn and ar-Ramah", "east and south of the tall", "Roman (implied)", "overlaps", "EVIDENCE", "waheeb2001shaj p. 597", "Through aqueducts from Wadi al-Kafrayn and ar-Ramah", ""),
    ("kharrar", "pool", "pools on both sides of the tall", "both sides of Tall al-Kharrar", "Roman", "overlaps", "EVIDENCE", "abushmais2002 p. 569", "no Roman structure except for the pools and paths", ""),
    ("kharrar", "pool", "large pool 15 x 24 m with staircase", "about 250 m east of the John the Baptist church", "Byzantine", "no", "EVIDENCE", "waheeb2001 pp. 423-424", "the Byzantines decided to build a large pool", "perhaps a natural pond in the Roman period (source's inference)"),
    ("kharrar", "cave", "two natural caves used as hermit cells", "Wadi al-Kharrar", "Byzantine use", "no", "EVIDENCE", "waheeb1998 p. 636", "two natural caves, which had been transformed into hermit grottas", "natural caves; earlier use not stated"),
    ("tall_el_hammam", "channel", "aqueduct about 165 m long", "from springs on the east side toward Field LR", "Roman", "overlaps", "EVIDENCE", "collins2009 p. 410", "approximately 165m of a Roman period aqueduct", ""),
    ("tell_er_rameh", "wall", "large dressed stones, possibly a fortification wall", "south of the tall, within 50-100 m", "not dated", "undated", "EVIDENCE", "kokkinos2001 p. 481", "seem to have belonged to a fortification wall", "Kokkinos links it to Antipas' wall (INFERENCE)"),
    ("gadara_umm_qais", "pool", "mikveh among quarries (hinterland survey)", "Gadara hinterland", "antiquity (not dated)", "undated", "EVIDENCE", "aij2 p. 19", "partially immovable remains (e.g., a mikveh)", "location within the survey area not given"),
    ("rajib_tombs", "tomb", "rock-cut tomb with thirteen loculi (Tomb 1)", "south of Abu Alanda and Rajib", "1st c. AD (Herodian lamps; cooking pot)", "yes", "EVIDENCE", "bisheh1973 pp. 63-64", "were thirteen loculi cut into the side walls", "site excluded from the gazetteer counts"),
    ("es_salt_tomb", "tomb", "Roman family tomb", "es-Salt", "Roman, with a coin of Constantine I", "no", "EVIDENCE", "hadidi1979 pp. 129-137", "A Roman Family Tomb at es-Salt", "title quoted; site excluded"),
]

GAZ_FIELDS = ["site_id", "name", "ancient_name", "identification_label", "identification_note", "lat", "lon", "coord_source",
              "sigma_km", "sigma_basis", "dist_to_river_km", "in_area", "peraea_proper", "peraea_basis",
              "occupation_as_given", "occupation_dated_in_window", "occupation_label", "occupation_citation",
              "marker_text", "marker_text_label", "marker_text_citation", "marker_arch", "marker_arch_label", "marker_arch_citation",
              "status", "status_reason", "n_features", "n_features_dated_in_window", "w2b_place_id"]
FEAT_FIELDS = ["feature_id", "site_id", "site_name", "lat", "lon", "coord_note", "feature_type", "feature_as_given",
               "position_as_given", "period_as_given", "dated_in_window", "evidence_label", "citation", "source_url",
               "quote", "notes"]
SRC_FIELDS = ["source_id", "citation", "url", "sha256", "read_mode"]
FEATURE_TYPES = ("pool", "cistern", "channel", "tomb", "cave", "tower", "wall", "hoard")
WINDOW_VALUES = ("yes", "overlaps", "no", "undated")


# ------------------------------------------------------------------------------------------- helpers
def load_transformer():
    spec = importlib.util.spec_from_file_location("w2b_grid_convert", str(GRID_CONVERT))
    mod = importlib.util.module_from_spec(spec)
    keep = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


def pg_to_wgs84(gc, e_km, n_km):
    lon, lat = gc.T191.transform(e_km * 1000.0, n_km * 1000.0)
    return round(lat, 5), round(lon, 5)


def dist_to_polyline_km(lat, lon, poly):
    """Shortest distance (km) from a point to a lat/lon polyline, local equirectangular projection."""
    lat0 = math.radians(lat)
    kx, ky = 111.32 * math.cos(lat0), 110.57

    def xy(a, b):
        return ((b - lon) * kx, (a - lat) * ky)
    best = float("inf")
    for (a1, b1), (a2, b2) in zip(poly, poly[1:]):
        x1, y1 = xy(a1, b1)
        x2, y2 = xy(a2, b2)
        dx, dy = x2 - x1, y2 - y1
        t = max(0.0, min(1.0, -(x1 * dx + y1 * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(x1 + t * dx, y1 + t * dy))
    return best


def river_lon_at(lat, poly):
    """Longitude of the river/shore line at a latitude (linear interpolation; None outside the polyline)."""
    pts = sorted(poly)
    for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
        if a1 <= lat <= a2:
            return b1 + (b2 - b1) * (lat - a1) / (a2 - a1)
    return None


def cite_url(cite):
    sid = cite.split()[0].rstrip(";,")
    return SOURCES[sid][1] if sid in SOURCES else ""


def to_csv(fields, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue().encode("utf-8")


def build():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    area = plan["area"]
    poly = [tuple(p) for p in area["river_shore_polyline_lat_lon"]]
    gc = load_transformer()
    feats_by_site = {}
    for f in FEATURES:
        feats_by_site.setdefault(f[0], []).append(f)
    gaz, coords = [], {}
    for s in SITES:
        if s["coord"] is None:
            lat = lon = None
            src = ""
        elif s["coord"][0] == "pg":
            lat, lon = pg_to_wgs84(gc, s["coord"][1], s["coord"][2])
            src = f"Palestine Grid {s['coord'][1]}/{s['coord'][2]} -> EPSG:28191 to WGS84 (pyproj); {s['coord'][3]}"
        else:
            lat, lon, src = s["coord"][1], s["coord"][2], s["coord"][3]
        coords[s["site_id"]] = (lat, lon)
        if lat is None:
            d, in_area = "", "unknown"
        else:
            d = dist_to_polyline_km(lat, lon, poly)
            rl = river_lon_at(lat, poly)
            east = rl is not None and lon > rl
            ok = area["lat_min"] <= lat <= area["lat_max"] and east and d <= area["east_limit_km"]
            d, in_area = f"{d:.1f}", ("yes" if ok else "no")
        fs = feats_by_site.get(s["site_id"], [])
        gaz.append(dict(
            site_id=s["site_id"], name=s["name"], ancient_name=s["ancient_name"],
            identification_label=s["identification"], identification_note=s["identification_note"],
            lat="" if lat is None else f"{lat:.5f}", lon="" if lon is None else f"{lon:.5f}", coord_source=src,
            sigma_km="" if s["sigma_km"] is None else f"{s['sigma_km']:.1f}", sigma_basis=s["sigma_basis"],
            dist_to_river_km=d, in_area=in_area, peraea_proper=s["peraea_proper"], peraea_basis=s["peraea_basis"],
            occupation_as_given=s["occupation"], occupation_dated_in_window=s["occupation_window"],
            occupation_label=s["occupation_label"], occupation_citation=s["occupation_cite"],
            marker_text=s["marker_text"], marker_text_label=s["marker_text_label"], marker_text_citation=s["marker_text_cite"],
            marker_arch=s["marker_arch"], marker_arch_label=s["marker_arch_label"], marker_arch_citation=s["marker_arch_cite"],
            status=s["status"], status_reason=s["status_reason"], n_features=str(len(fs)),
            n_features_dated_in_window=str(sum(1 for f in fs if f[5] == "yes")),
            w2b_place_id=("transjordan" if (s["status"] == "documented" and s["peraea_proper"] == "yes" and lat is not None) else ""),
        ))
    names = {s["site_id"]: s["name"] for s in SITES}
    feat_rows = []
    counter = {}
    for f in FEATURES:
        sid = f[0]
        counter[sid] = counter.get(sid, 0) + 1
        lat, lon = coords[sid]
        feat_rows.append(dict(
            feature_id=f"{sid}-{counter[sid]:02d}", site_id=sid, site_name=names[sid],
            lat="" if lat is None else f"{lat:.5f}", lon="" if lon is None else f"{lon:.5f}",
            coord_note="site point (no feature-level coordinate in the source)" if lat is not None else "no coordinate",
            feature_type=f[1], feature_as_given=f[2], position_as_given=f[3], period_as_given=f[4],
            dated_in_window=f[5], evidence_label=f[6], citation=f[7], source_url=cite_url(f[7]), quote=f[8], notes=f[9]))
    src_rows = [dict(source_id=k, citation=v[0], url=v[1], sha256=v[2], read_mode=v[3]) for k, v in sorted(SOURCES.items())]
    return {"gazetteer.csv": to_csv(GAZ_FIELDS, gaz), "features.csv": to_csv(FEAT_FIELDS, feat_rows),
            "sources.csv": to_csv(SRC_FIELDS, src_rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = build()
    if a.check:
        bad = [n for n, b in out.items() if not (ROOT / n).exists() or (ROOT / n).read_bytes() != b]
        if bad:
            raise SystemExit(f"differs from a fresh build: {bad}")
        print("gazetteer.csv, features.csv and sources.csv match a fresh build")
        return
    for n, b in sorted(out.items()):
        (ROOT / n).write_bytes(b)
        print("wrote", n)


if __name__ == "__main__":
    main()
