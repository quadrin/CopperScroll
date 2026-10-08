#!/usr/bin/env python3
"""Build the T02 hoard/cache database (hoards.json, hoards.csv).

Every record cites its source(s).  CHRE = Coin Hoards of the Roman Empire database
(https://chre.ashmus.ox.ac.uk/hoard/<id>), fetched 6 Oct 2026; CHRE quotes the primary
publications given in 'source'.  Masses: 'measured' only where a publication gives the weight;
otherwise 'nominal' = coin count x nominal weight (shekel/tetradrachm 14.2 g, half-shekel/didrachm
7.1 g, denarius/drachm 3.4 g) -> an INFERENCE range, flagged as such.

Fields
 scope: 'in' (in region & period, scored), 'edge' (period OK, region marginal, scored but flagged),
        'out_region' (period OK, outside the scroll's region: comparanda only, not scored),
        'out_period' (outside c. 200 BCE-136 CE: listed only), 'self' (Cave 3 itself: not scored)
 prec_km: radius of uncertainty of the coordinate (site 0.2; generic-town 2-3; dealer attribution >=1)
 findspot: landmark classes (same vocabulary as entry_features: cistern, pool, reservoir, basin,
        conduit, outlet, spring, pit, tomb, monument, cave, fissure, chamber, dovecote, court,
        building, fortress, steps, threshold, corner, pillar, stone, wall, rock, mound, ruin, cairn,
        valley, field, road, street, natural, unknown)
 cues: position cues (corner, north/south/east/west, under_stone, threshold, floor, wall, ...)
 container: jar | pot | juglet | box | moneybox | bag | basket | lamp | bowl | none
 contents: silver_coins | gold_coins | bronze_coins | metal_vessels | scrolls | jewelry | silver_bullion | mint_debitage
 tpq: terminal (latest) coin year = terminus post quem for deposition (negative = BCE)
"""
import csv
import json
import os

OUT = "agent_review/wave1/T02_hoard_match"
C = "https://chre.ashmus.ox.ac.uk/hoard/"

H = []


def add(**k):
    k.setdefault("cues", [])
    k.setdefault("depth_m", None)
    k.setdefault("mass_g", None)
    k.setdefault("mass_basis", "")
    k.setdefault("notes", "")
    k.setdefault("macro", "")
    H.append(k)


# ---------------- Qumran / NW Dead Sea ----------------
for hid, nm, chre, n, cont, cdesc, fs, cues, sitec, mass in [
    ("H01", "Kh. Qumran L120 hoard A (1955)", 7692, 223, "pot",
     "small wide-mouthed pot stopped with palm fibre (de Vaux 1956: 567)", ["building", "threshold"],
     ["threshold", "floor"],
     "L120, to the right of the door on entering; two pots buried between the floors of Period Ib and II", (1583, 3167)),
    ("H02", "Kh. Qumran L120 hoard B (1955)", 18786, 185, "pot",
     "small wide-mouthed pot stopped with palm fibre (de Vaux 1956: 567)", ["building", "threshold"],
     ["threshold", "floor"],
     "same as A: right of the door, between Period Ib and II floors", (1314, 2627)),
    ("H03", "Kh. Qumran L120 hoard C (1955)", 18785, 153, "juglet",
     "jug (Ariel 2018: 'juglet') with a hole pierced in the belly to insert coins", ["building", "wall"],
     ["north", "wall", "floor"], "L120, against the north wall", (536, 1086)),
]:
    add(id=hid, name=nm, site="Khirbet Qumran", scope="in", lat=31.741119, lon=35.459027, prec_km=0.2,
        coord_src=f"CHRE {chre}", provenance="excavated (de Vaux 1955)", year_found=1955,
        tpq=-8, date_text="latest coins 9/8 BCE (Tyrian yr 118); deposition date disputed (Ariel 2018: after 9/8 BCE, possible foundation deposit; Lonnqvist 2007 argues later)",
        contents=["silver_coins"], contents_text=f"{n} silver coins (Tyrian shekels and half-shekels, Seleucid tetradrachms, a few Roman denarii)",
        count=n, mass_g=list(mass), mass_basis="nominal range (INFERENCE)", container=cont, container_text=cdesc,
        findspot=fs, cues=cues, findspot_text=sitec,
        source=f"CHRE {C}{chre}; de Vaux, RB 63 (1956) 567-568; Sharabani, RB 87 (1980) 274-284; Lonnqvist 2007 (Amman lots); Ariel 2018, 'Coins from the Renewed Excavations at Qumran', in Magen & Peleg, Back to Qumran (JSP 18) p. 404 (https://www.academia.edu/37004128); IAA exhibit text https://ibiblio.org/expo/deadsea.scrolls.exhibit/Community/coins.html",
        notes="Three vessels, 561 coins in total. Leonard (Orion list, 23 Dec 1999, https://orion.huji.ac.il/orion/archives/1999b/msg00642.html) states this hoard 'cannot be identified with any treasure listed in the Copper Scroll'.")
add(id="H04", name="Kh. Qumran L29 bowl group (1953)", site="Khirbet Qumran", scope="in", lat=31.741, lon=35.459, prec_km=0.2,
    coord_src="CHRE 18784", provenance="excavated", year_found=1953, tpq=134, date_text="CHRE terminal 134-135 CE",
    contents=["unknown_coins"], contents_text="10 coins in the bottom of a bowl", count=10, container="bowl", container_text="bowl",
    findspot=["fortress", "threshold"], cues=["threshold"], findspot_text="L29, entrance of the fortified tower", source=f"CHRE {C}18784")
add(id="H05", name="Kh. Qumran L83 hoard (1954-56)", site="Khirbet Qumran", scope="in", lat=31.741, lon=35.459, prec_km=0.2,
    coord_src="CHRE 8124", provenance="excavated", year_found=1955, tpq=68, date_text="26 bronze, First Revolt year 2 (67/68 CE)",
    contents=["bronze_coins"], contents_text="26 bronze coins of the First Revolt", count=26, container="none", container_text="not stated",
    findspot=["unknown"], findspot_text="Locus 83 (CHRE context: natural feature)", source=f"CHRE {C}8124; de Vaux, RB 63 (1956) 566")
add(id="H06", name="Qumran 1958 hoard", site="Khirbet Qumran (attribution)", scope="in", lat=31.741, lon=35.459, prec_km=1.0,
    coord_src="CHRE 8120", provenance="reported (Kadman 1967 no. 30)", year_found=1958, tpq=69, date_text="68-72 bronze coins of the First Revolt",
    contents=["bronze_coins"], contents_text="68-72 bronze coins", count=70, container="none", container_text="not stated",
    findspot=["unknown"], findspot_text="context uncertain", source=f"CHRE {C}8120; Kadman 1967 no. 30")
add(id="H07", name="'Feshka-Qumran' Agrippa I hoard", site="Qumran / Ein Feshkha", scope="in", lat=31.741, lon=35.459, prec_km=2.0,
    coord_src="CHRE 8122", provenance="reported (de Vaux 1961, Kadman 1967 no. 33)", year_found=None, tpq=44, date_text="18 bronze of Agrippa I (41-44 CE)",
    contents=["bronze_coins"], contents_text="18 bronze coins of Agrippa I", count=18, container="none", container_text="not stated",
    findspot=["unknown"], findspot_text="not stated", source=f"CHRE {C}8122; Kadman 1967 no. 33")
add(id="H08", name="Ein Feshkha cave silver hoard (1953)", site="cave near Ein Feshkha", scope="in", lat=31.724, lon=35.458, prec_km=2.0,
    coord_src="CHRE 7586 (location 'uncertain')", provenance="reported 1953", year_found=1953, tpq=117,
    date_text="1st c. BCE to 2nd c. CE; CHRE terminal 117-138 CE",
    contents=["silver_coins"], contents_text="at least 277 silver coins; denominations not clear from report", count=277,
    mass_g=[942, 3933], mass_basis="nominal range (INFERENCE)", container="none", container_text="not stated",
    findspot=["cave"], findspot_text="'in a cave somewhere in the neighbourhood of Feshkha (the exact location is uncertain)'",
    source=f"CHRE {C}7586 citing 'Ain Feshkha' (no author, 1953) p. 89")
add(id="H09", name="Qumran Cave 1 scroll jars", site="Qumran Cave 1", scope="in", lat=31.7418, lon=35.4594, prec_km=1.5,
    coord_src="anchor = Kh. Qumran atlas point; Cave 1 lies in the cliffs north of the site (distance not verified here)",
    provenance="Bedouin find 1947; excavated 1949 (Harding, de Vaux)", year_found=1947, tpq=68,
    date_text="jars of the Qumran type; deposition commonly placed before 68 CE (not re-verified here)",
    contents=["scrolls"], contents_text="scrolls; 'fragments of about seventy scrolls ... and pieces of fifty pottery jars and covers' (DJD I); Bedouin removed scrolls from a covered jar",
    count=None, container="jar", container_text="cylindrical jars with lids",
    findspot=["cave"], findspot_text="cave in the cliffs; openings/orientation not verified in this pass",
    source="DJD I (1955) as quoted by B. Nongbri, https://brentnongbri.com/2020/04/25/qumran-cave-1-questions-part-3-is-cave-1-really-cave-1/ ; Trever 1965 (Untold Story of Qumran)")
add(id="H10", name="Qumran Cave 3 (Copper Scroll cave)", site="Qumran Cave 3", scope="self", lat=None, lon=None, prec_km=None,
    coord_src="", provenance="excavated 1952", year_found=1952, tpq=None, date_text="",
    contents=["scrolls"], contents_text="the Copper Scroll, jars, leather fragments of ~14 texts", count=None, container="jar", container_text="jars",
    findspot=["cave"], findspot_text="cave north of Qumran", source="https://virtualqumran.huji.ac.il/tour/VTCaves.htm", notes="the scroll's own cache; not scored")

# ---------------- Jericho / lower Jordan valley ----------------
add(id="H11", name="Jericho 1973 (Tulul Abu el-Alayiq) Antigonus hoard", site="Hasmonean-Herodian palaces, Jericho", scope="in",
    lat=31.8533, lon=35.4375, prec_km=0.2, coord_src="CHRE 7828", provenance="excavated (Netzer)", year_found=1973, tpq=-37,
    date_text="20 large bronzes of Mattathias Antigonus (40-37 BCE)", contents=["bronze_coins"], contents_text="20 bronze coins", count=20,
    container="none", container_text="not stated", findspot=["court", "pool_adjacent"],
    findspot_text="garden fill west of the swimming pool, Locus A(B)22 (Netzer 1975: 92)",
    source=f"CHRE {C}7828; Meshorer 2004 in Netzer, Hasmonean and Herodian Palaces at Jericho II pp. 287-312; CH II no. 128")
add(id="H12", name="Jericho 1950-51 (NT Jericho / Kh. en-Nitla) hoard", site="New Testament Jericho", scope="in",
    lat=31.857, lon=35.461, prec_km=0.5, coord_src="CHRE 7832", provenance="excavated (Kelso & Baramki)", year_found=1950, tpq=86,
    date_text="15 bronzes, Herod Archelaus to 86 CE", contents=["bronze_coins"], contents_text="15 bronze coins", count=15,
    container="none", container_text="not stated", findspot=["building", "threshold"], cues=["threshold"],
    findspot_text="'under the doorway of the great room at the west end of the facade' (Kelso 1950: 20)",
    source=f"CHRE {C}7832; Kelso & Baramki, AASOR 29-30 (1955); CH II no. 138")
add(id="H13", name="Jericho 1874 shekel hoard", site="Jericho (attribution)", scope="in", lat=31.861, lon=35.462, prec_km=2.0,
    coord_src="CHRE 8082 (town-level)", provenance="19th-c. find, no excavation record", year_found=1874, tpq=69,
    date_text="shekels of years 1-4 of the First Revolt (to 69/70 CE)",
    contents=["silver_coins", "jewelry"], contents_text="c. 100 First Revolt shekels + gold seal with gem engraved with wheat ears", count=100,
    mass_g=[710, 1420], mass_basis="nominal range (INFERENCE)", container="jar",
    container_text="earthen pot with a lead seal (CHRE)", findspot=["unknown"], findspot_text="not recorded",
    source=f"CHRE {C}8082; Noe 1937 no. 513; Kadman 1960 p. 81; Kadman 1967 no. 23; Leonard 2000")
add(id="H14", name="'Near Jericho' 1980 silver hoard (trade)", site="near Jericho (dealer)", scope="in", lat=31.857, lon=35.461, prec_km=5.0,
    coord_src="CHRE 20985 (town-level)", provenance="trade information (A. Spaer)", year_found=1980, tpq=117,
    date_text="Nero to Hadrian; 1 Bar Kokhba bronze", contents=["silver_coins"], contents_text="52 silver + 1 bronze", count=53,
    mass_g=[177, 738], mass_basis="nominal range (INFERENCE)", container="none", container_text="not stated", findspot=["unknown"],
    findspot_text="unknown", source=f"CHRE {C}20985; CH VII no. 234")
add(id="H15", name="Cave of the Sandal (Ketef Jericho) coin clusters A-C", site="Ketef Jericho cliffs W of Jericho", scope="in",
    lat=31.8734, lon=35.4313, prec_km=0.5, coord_src="CHRE 8052/8053 (precision not stated)", provenance="excavated (IAA Operation Scroll 1993)",
    year_found=1993, tpq=124, date_text="Vitellius to Hadrian; deposited in Bar Kokhba revolt (132-136 CE)",
    contents=["silver_coins", "bronze_coins"], contents_text="26 coins in three clusters (6 countermarked bronzes; 7 silver; 13 silver+bronze)", count=26,
    mass_g=[30, 120], mass_basis="nominal range (INFERENCE)", container="none", container_text="not stated", findspot=["cave"],
    findspot_text="cave entrance in a vertical cliff c. 8 m above a terrace; small room, tunnel, main hall",
    source=f"CHRE {C}8052, {C}8053, {C}8054; Eshel & Zissu, ESI/HA 1995 pp. 295-298; Eshel & Zissu 1999 pp. 73-77")
add(id="H16", name="Wadi ed-Daliyeh, 'Iraq an-Na'asana cave denarii", site="Wadi ed-Daliyeh", scope="in", lat=31.99446, lon=35.40715, prec_km=0.3,
    coord_src="CHRE 7818", provenance="excavated/recorded 1980", year_found=1980, tpq=129, date_text="16 denarii 98/99-128/129 CE",
    contents=["silver_coins"], contents_text="16 denarii", count=16, mass_g=[54, 54], mass_basis="nominal (INFERENCE)", container="none",
    container_text="not stated", findspot=["cave"], findspot_text="multi-chambered cave c. 310 m long, N slope of Wadi ed-Daliyeh",
    source=f"CHRE {C}7818; Damati & Erlich 1981; Erlich & Damati 1998 pp. 71-76")
add(id="H17", name="Kh. el-Beiyudat Agrippa I coin piles", site="Kh. el-Beiyudat (Jordan valley N of Jericho)", scope="in",
    lat=31.96388, lon=35.46928, prec_km=0.3, coord_src="CHRE 9040", provenance="excavated, unprocessed", year_found=None, tpq=44,
    date_text="Agrippa I (41-44 CE)", contents=["bronze_coins"], contents_text="'piles of Agrippa I coins', not processed", count=None,
    container="none", container_text="", findspot=["unknown"], findspot_text="", source=f"CHRE {C}9040")
add(id="H18", name="Nahal Tirzah / Alexandrion road Jannaeus hoard (2024)", site="Jordan valley near Nahal Tirzah", scope="edge",
    lat=None, lon=None, prec_km=None, macro="jordan_valley", coord_src="no coordinates published in the source read",
    provenance="excavated (Univ. of Haifa)", year_found=2024, tpq=-76, date_text="c. 160 prutot of Alexander Jannaeus (mostly year 25)",
    contents=["bronze_coins"], contents_text="c. 160 bronze prutot", count=160, container="bag", container_text="perishable (leather pouch?) inferred by excavators",
    findspot=["building", "wall"], findspot_text="next to a collapsed wall in the food-preparation area of a building",
    source="https://www.numismaticnews.net/world-coins/a-miracle-hoard-2100-year-old-coins-unearthed-in-jordan-valley-during-hanukkah")
add(id="H19", name="Jericho Hasmonean-era shekel hoard (200+, latest 103/2 BCE)", site="Jericho (attribution)", scope="in",
    lat=31.856, lon=35.463, prec_km=3.0, coord_src="atlas 'jericho_area' point (town-level)", provenance="UNVERIFIED: mentioned only by R. D. Leonard (Orion list 28 Dec 1999) citing IGCH",
    year_found=None, tpq=-103, date_text="latest coin 103/2 BCE (per Leonard)", contents=["silver_coins"], contents_text="200+ shekels (per Leonard)",
    count=200, mass_g=[1420, 2840], mass_basis="nominal range (INFERENCE)", container="none", container_text="not stated",
    findspot=["unknown"], findspot_text="unknown", source="https://orion.huji.ac.il/orion/archives/1999b/msg00671.html (IGCH entry not accessed: coinhoards.org blocked by robots for this tool)")

# ---------------- Judean desert ----------------
add(id="H20", name="Murabba'at Cave II Ptolemaic hoard", site="Wadi Murabba'at (Nahal Darga), Cave II", scope="in",
    lat=31.588, lon=35.373, prec_km=2.0, coord_src="CHRE 7690 point for Wadi Murabba'at (wadi-level)", provenance="excavated (IAA, May 2022)",
    year_found=2022, tpq=-171, date_text="15 tetradrachms of Ptolemy VI, 176/5-171/0 BCE; hidden c. 170 BCE",
    contents=["silver_coins"], contents_text="15 silver tetradrachms + purple wool cloth; one coin incised 'Shalmai'", count=15,
    mass_g=[213, 213], mass_basis="nominal 14.2 g (INFERENCE)", container="box", container_text="lathe-turned wooden box (pyxis) with lid",
    findspot=["cave", "fissure"], findspot_text="crack in the cave wall / crevice near a shaft leading to inner cavities",
    source="Klein, Bijovsky, Ganor et al., 'Atiqot 112 (2023) 53-92 (https://cris.biu.ac.il/en/publications/a-hoard-of-ptolemaic-coins-found-in-murabbaat-cave-ii-in-the-jude-2/); https://www.archaeology.wiki/blog/2022/12/19/evidence-for-the-maccabean-revolt-against-the-greek-seleucid-kingdom/")
add(id="H21", name="Wadi Murabba'at silver hoard (purchased 1952)", site="Wadi Murabba'at (attribution)", scope="in", lat=31.588, lon=35.373, prec_km=3.0,
    coord_src="CHRE 7690", provenance="purchased in Jerusalem 1952", year_found=1952, tpq=119, date_text="down to 122 CE",
    contents=["silver_coins"], contents_text="227+ silver: 119 Nabataean denarii, 14 Antioch tetradrachms, Trajanic Arabian drachms etc., 51 imperial denarii",
    count=227, mass_g=[974, 974], mass_basis="nominal sum (INFERENCE)", container="none", container_text="not stated", findspot=["unknown"],
    findspot_text="", source=f"CHRE {C}7690; Milik & Seyrig, RN 1958; Mildenberg 1984 no. 5")
add(id="H22", name="Cave of Letters bronze vessel cache", site="Nahal Hever, Cave of Letters", scope="in", lat=31.4326, lon=35.3429, prec_km=0.2,
    coord_src="Wikipedia 'Cave of Letters'", provenance="excavated (Yadin 1960)", year_found=1960, tpq=132,
    date_text="Bar Kokhba war (132-135 CE)", contents=["metal_vessels"], contents_text="19 bronze objects: patera, jugs, incense shovels (Roman, images defaced); separate cache of keys",
    count=19, container="basket", container_text="basket", findspot=["cave"], cues=["threshold"],
    findspot_text="'a basket of bronze vessels and incense shovels' found at the cave entrance (Wikipedia); the cave 'has two openings, three halls and some crevices'",
    source="https://www.jewishvirtuallibrary.org/judean-desert-caves (Encyclopaedia Judaica 2007); https://en.wikipedia.org/wiki/Cave_of_Letters; Freund 2000, in Schiffman/Tov/VanderKam (eds), DSS Fifty Years after Their Discovery pp. 644-660 (https://orion-bibliography.huji.ac.il/node/53475)",
    notes="PRIOR CLAIM: R. Freund identified the Cave of Letters with entry 25's 'cave of the pillar with two openings' (J Weekly 12 Nov 2004, https://jweekly.com/2004/11/12/archaeologists-search-for-historical-clues-in-ancient-israeli-hideout/); described there as not accepted by colleagues.")
for hid, nm, chre, lat, lon, n, cnt, cont, ctext, fs, cues, depth, ftext, tpq, mass in [
    ("H23", "Cave of Horror Bar Kokhba coins", 8463, 31.42981, 35.34786, 4, ["unknown_coins"], "none", "", ["cave"], [], None, "Cave of Horror (Nahal Hever S bank)", 132, None),
    ("H24", "Har Yishai cave hoard (En Gedi)", 8472, 31.45223, 35.38480, 8, ["bronze_coins"], "bag", "leather purse", ["cave"], ["floor"], 0.4,
     "beaten-earth floor at 40 cm depth, with two Greek papyri", 132, None),
    ("H25", "Zabar cave hoard (En Gedi)", 8474, 31.466, 35.388, 9, ["silver_coins"], "bag", "cloth purse", ["cave"], ["under_stone"], 0.2,
     "centre of the cave, under a large stone apparently placed on purpose, depth c. 20 cm (Porat et al.)", 132, [31, 128]),
]:
    add(id=hid, name=nm, site="En Gedi / Nahal Hever caves", scope="in", lat=lat, lon=lon, prec_km=0.3, coord_src=f"CHRE {chre}",
        provenance="excavated", year_found=None, tpq=tpq, date_text="Second Revolt (132-136 CE)", contents=cnt,
        contents_text=f"{n} coins", count=n, mass_g=mass, mass_basis="nominal range (INFERENCE)" if mass else "", container=cont, container_text=ctext,
        findspot=fs, cues=cues, depth_m=depth, findspot_text=ftext, source=f"CHRE {C}{chre}; Porat, Eshel & Frumkin 2006/2007")
add(id="H26", name="En Gedi 1964 A lamp hoard", site="Tel Goren, En Gedi", scope="in", lat=31.451, lon=35.384, prec_km=0.3, coord_src="CHRE 7495",
    provenance="excavated", year_found=1964, tpq=59, date_text="139 bronze, 42-59 CE", contents=["bronze_coins"], contents_text="139 bronze coins in a lamp",
    count=139, container="lamp", container_text="Herodian lamp plugged with a pebble", findspot=["building", "wall"], cues=["wall"],
    findspot_text="niche in the plastered wall of a house (Building 236)", source=f"CHRE {C}7495; Meshorer 1976; CH III no. 86")
add(id="H27", name="En Gedi 1964 B bathhouse door-frame deposit", site="En Gedi bathhouse", scope="in", lat=31.451, lon=35.384, prec_km=0.3, coord_src="CHRE 7496",
    provenance="excavated", year_found=1964, tpq=117, date_text="6 bronze, 70/81-117/118 CE", contents=["bronze_coins"], contents_text="6 bronze coins",
    count=6, container="none", container_text="", findspot=["building", "threshold"], cues=["threshold"],
    findspot_text="hollow of a door frame in the tepidarium", source=f"CHRE {C}7496; Ariel 2007 p. 423")
add(id="H28", name="Herodion 1967 Bar Kokhba bronze hoard", site="Herodium", scope="in", lat=31.667, lon=35.243, prec_km=0.2, coord_src="CHRE 7631",
    provenance="excavated (Corbo)", year_found=1967, tpq=134, date_text="831 Bar Kokhba bronzes", contents=["bronze_coins"], contents_text="831 bronze coins",
    count=831, container="none", container_text="", findspot=["fortress", "building", "corner"], cues=["corner"], findspot_text="corner of Room 30",
    source=f"CHRE {C}7631; Spijkerman 1972; Mildenberg 1984 no. 13")
add(id="H29", name="Herodion 1969 First Revolt bronzes", site="Herodium", scope="in", lat=31.66576, lon=35.24158, prec_km=0.2, coord_src="CHRE 8044",
    provenance="excavated (Foerster)", year_found=1969, tpq=69, date_text="19 'year four' bronzes", contents=["bronze_coins"], contents_text="19 bronze coins",
    count=19, container="none", container_text="", findspot=["fortress", "threshold"], cues=["threshold"], findspot_text="ashes in an entrance room leading to a corridor",
    source=f"CHRE {C}8044; Ahipaz et al. 2017 pp. 127-129")
add(id="H30", name="Masada 1965 A (casemate 1039) shekels", site="Masada", scope="in", lat=31.3175, lon=35.3539, prec_km=0.2, coord_src="CHRE 7698",
    provenance="excavated (Yadin)", year_found=1965, tpq=72, date_text="17 shekels yrs 2-5 + 2 silver flans", contents=["silver_coins", "silver_bullion"],
    contents_text="17 shekels; 2 unstruck flans; defaced Tyrian shekel used as bullion", count=19, mass_g=[240, 270], mass_basis="nominal (INFERENCE)",
    container="none", container_text="", findspot=["fortress", "wall"], cues=["wall"],
    findspot_text="scattered on the floor of casemate 1039 near the synagogue with scroll pieces; probably hidden in the wall (Meshorer 1989: 74-76)",
    source=f"CHRE {C}7698; Meshorer 1989 (Masada I) pp. 74-76")
add(id="H31", name="Masada 1965 B (Building IX) silver", site="Masada", scope="in", lat=31.3175, lon=35.3539, prec_km=0.2, coord_src="CHRE 7697",
    provenance="excavated (Yadin)", year_found=1965, tpq=69, date_text="37 silver, yrs 1-3", contents=["silver_coins"], contents_text="37 silver coins",
    count=37, mass_g=[263, 525], mass_basis="nominal range (INFERENCE)", container="bag", container_text="cloth bag (traces)",
    findspot=["fortress", "building"], cues=["floor"], findspot_text="buried under the floor of Building IX, L336",
    source=f"CHRE {C}7697; Meshorer 1989 pp. 73-74")
add(id="H32", name="Masada 1963-65 A (bronze cupping vessel)", site="Masada", scope="in", lat=31.3175, lon=35.3539, prec_km=0.2, coord_src="CHRE 8167",
    provenance="excavated", year_found=1964, tpq=70, date_text="6 shekels + 6 half-shekels", contents=["silver_coins"], contents_text="12 silver coins",
    count=12, mass_g=[128, 128], mass_basis="nominal (INFERENCE)", container="box", container_text="bronze cupping vessel used as pyxis",
    findspot=["fortress"], findspot_text="L365", source=f"CHRE {C}8167; Meshorer 1989 p. 74")
add(id="H33", name="Masada 1963-65 B garrison tetradrachms", site="Masada", scope="in", lat=31.3158, lon=35.3534, prec_km=0.2, coord_src="CHRE 7281",
    provenance="excavated", year_found=1964, tpq=107, date_text="13 tetradrachms to 107-110 CE", contents=["silver_coins"], contents_text="13 tetradrachms",
    count=13, mass_g=[185, 185], mass_basis="nominal (INFERENCE)", container="none", container_text="", findspot=["fortress"], findspot_text="L157",
    source=f"CHRE {C}7281; Meshorer 1989 p. 77")
add(id="H34", name="'Judaean Desert' Bar Kokhba hoard (Ta'amira find)", site="northern Judean desert between Hebron and Dead Sea", scope="in",
    lat=31.515, lon=35.274, prec_km=10.0, coord_src="CHRE 7604 (area)", provenance="Bedouin find, 1962 report", year_found=1962, tpq=132,
    date_text="Bar Kokhba", contents=["silver_coins", "bronze_coins"], contents_text="4 tetradrachms, 20+ denarii, many bronzes", count=24,
    container="none", container_text="", findspot=["unknown"], findspot_text="", source=f"CHRE {C}7604")
add(id="H35", name="'Ain 'Arub hiding-complex cave prutot", site="al-Arroub", scope="edge", lat=31.62312, lon=35.13672, prec_km=0.3, coord_src="CHRE 8492",
    provenance="excavated", year_found=1975, tpq=69, date_text="8 prutot yrs 2-3", contents=["bronze_coins"], contents_text="8 prutot", count=8,
    container="none", container_text="", findspot=["cave"], findspot_text="Area D, L14", source=f"CHRE {C}8492; Tsafrir & Zissu 2002")

# ---------------- Jerusalem and environs ----------------
add(id="H36", name="Ramat Rahel Tyrian shekel hoard (2008)", site="Ramat Rahel, southern columbarium", scope="in",
    lat=31.740128, lon=35.217542, prec_km=0.1, coord_src="CHRE 7288", provenance="excavated (Lipschits, Oeming, Gadot)", year_found=2008, tpq=-10,
    date_text="15 Tyrian shekels 38/37-11/10 BCE; deposited on or after 11/10 BCE (press reports of 70 CE are superseded by the publication)",
    contents=["silver_coins"], contents_text="15 Tyrian shekels, unworn; total 204.54 g (avg 13.63 g)", count=15, mass_g=[204.54, 204.54], mass_basis="measured (Farhi et al. 2010)",
    container="pot", container_text="small cooking pot, lid = broken base of a jug/juglet",
    findspot=["dovecote", "chamber", "corner"], cues=["corner", "south", "west"],
    findspot_text="niche in the SW corner of the main hall of the southern (subterranean) columbarium, c. 0.5 m above the chalk floor and 3.5 m below the access shaft",
    source=f"CHRE {C}7288; Farhi, Davidovich, Gadot & Lipschits, INJ 17 (2010) 59-76, esp. 61-62 (https://www.academia.edu/6801386/); Buijtendorp, INR 8 (2013) 25-30; Heidelberg press release https://www.uni-heidelberg.de/presse/news08/pm595e.html",
    notes="Interpreted by the excavators as possibly a Temple-tax payment for 30 men (half-shekel each).")
add(id="H37", name="Siloam bronze-pyxis shekel hoard", site="Silwan (dealer attribution)", scope="in", lat=31.770162, lon=35.236066, prec_km=1.0,
    coord_src="CHRE 8000 (dealer attribution)", provenance="acquired by Reifenberg Oct 1940; no archaeological data", year_found=1940, tpq=67,
    date_text="Tyrian shekels 126/5 BCE onward + Jewish shekels years 1-2; hidden c. 67/68 CE (Reifenberg 1945: 85)",
    contents=["silver_coins"], contents_text="at least 12 Tyrian shekels + First Revolt shekels", count=12, mass_g=[170, None], mass_basis="lower bound, nominal (INFERENCE)",
    container="box", container_text="bronze pyxis with lid, diam. 7.5 cm, h. 9 cm", findspot=["unknown"],
    findspot_text="'no reason to doubt the statement of the dealer that the pyxis ... was actually found at or near Silwan' (Reifenberg 1945: 83)",
    source=f"CHRE {C}8000; Reifenberg 1945 'A Hoard of Tyrian and Jewish Shekels'; Kadman 1960 p. 82; Leonard 2000")
add(id="H38", name="'St Stephen's Gate' shekel hoard (1935)", site="outside Lions' (St Stephen's) Gate or Ophel (rumour)", scope="in",
    lat=31.781, lon=35.237, prec_km=0.8, coord_src="CHRE 7541 (rumoured findspot)", provenance="market, three Jerusalem dealers", year_found=1935, tpq=68,
    date_text="258 BCE - 68/69 CE", contents=["silver_coins"], contents_text="c. 160 silver shekels rumoured; 64 Jewish shekels + 25 non-Jewish coins examined by Hill",
    count=160, mass_g=[1136, 2272], mass_basis="nominal range (INFERENCE)", container="none", container_text="not stated", findspot=["unknown"],
    findspot_text="believed found outside St Stephen's Gate during road construction, or at Ophel (Hill 1938: 78)",
    source=f"CHRE {C}7541; Hill 1938; Kadman 1960 p. 81; Leonard 2000")
add(id="H39", name="Jewish Quarter 1975 shekels in a small pool", site="Jewish Quarter (Upper City)", scope="in", lat=31.775, lon=35.233, prec_km=0.3,
    coord_src="CHRE 7609 (quarter-level)", provenance="excavated (Avigad)", year_found=1975, tpq=69, date_text="shekels and half-shekels years 1-4",
    contents=["silver_coins"], contents_text="13 silver shekels and half-shekels", count=13, mass_g=[92, 185], mass_basis="nominal range (INFERENCE)",
    container="none", container_text="not stated", findspot=["pool", "building"], findspot_text="'in a small pool of a building'",
    source=f"CHRE {C}7609; Avigad, Discovering Jerusalem (1983) pp. 195-196; Leonard 2000")
add(id="H40", name="Dominus Flevit shekel hoard", site="Mount of Olives (Dominus Flevit)", scope="in", lat=31.777984, lon=35.241899, prec_km=0.2,
    coord_src="CHRE 7605", provenance="excavated (Franciscan, Spijkerman 1961)", year_found=1961, tpq=70, date_text="First Revolt years 1-5; hidden July/Aug 70 CE (Spijkerman)",
    contents=["silver_coins"], contents_text="16 silver: 10 shekels, half-shekels etc.", count=16, mass_g=[113, 227], mass_basis="nominal range (INFERENCE)",
    container="lamp", container_text="found near a Herodian lamp (possibly a marker; unclear if container)", findspot=["tomb"],
    findspot_text="slope of the Mount of Olives; CHRE context 'burial'", source=f"CHRE {C}7605; Spijkerman 1961 pp. 25-32; Kadman 1967 no. 31")
add(id="H41", name="Meqor Hayim burial-cave coins", site="Meqor Hayim, SW Jerusalem", scope="in", lat=31.754, lon=35.212, prec_km=0.3, coord_src="CHRE 7603",
    provenance="excavated", year_found=1980, tpq=70, date_text="3 tetradrachms + 3 bronzes, 40-70 and 70-106 CE",
    contents=["silver_coins", "bronze_coins"], contents_text="3 silver tetradrachms + 3 bronze", count=6, mass_g=[43, 43], mass_basis="nominal (INFERENCE)",
    container="none", container_text="", findspot=["tomb", "chamber"], findspot_text="burial chamber (kokh) of a nine-kokhim cave",
    source=f"CHRE {C}7603; Tzaferis & Berman 1982 pp. 70-73; Kloner 2000 p. 79")
add(id="H42", name="Mount Scopus (Hebrew University grounds) tetradrachms", site="Mount Scopus", scope="in", lat=31.793062, lon=35.244936, prec_km=0.5,
    coord_src="CHRE 8035", provenance="found 1940s (Sukenik 1949)", year_found=None, tpq=-29, date_text="142-29 BCE",
    contents=["silver_coins"], contents_text="11 tetradrachms (2 Demetrius II, 9 Tyrian)", count=11, mass_g=[156, 156], mass_basis="nominal (INFERENCE)",
    container="none", container_text="", findspot=["natural"], findspot_text="CHRE context: natural feature",
    source=f"CHRE {C}8035; Sukenik 1949; IGCH 1628; Ariel 1982 pp. 304, 311-313")
add(id="H43", name="'Hebrew University hoard'", site="Jerusalem (generic)", scope="in", lat=31.768, lon=35.214, prec_km=3.0, coord_src="CHRE 9023 (generic)",
    provenance="reported (S. Ben-Dor)", year_found=None, tpq=70, date_text="c. 70 CE", contents=["silver_coins"], contents_text="5 Tyrian + 2 Revolt shekels",
    count=7, mass_g=[99, 99], mass_basis="nominal (INFERENCE)", container="none", container_text="", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}9023; Ariel 1982")
for hid, nm, chre, lat, lon, n, ctext, tpq, src, mass in [
    ("H44", "'Jerusalem (North)' 47 shekels", 7901, 31.805, 35.222, 47, "47 First Revolt shekels (1 yr1, 31 yr2, 15 yr3)", 69, "CH VII no. 151", [667, 667]),
    ("H45", "'Jerusalem 1889' revolt silver", 8091, 31.768, 35.214, 120, "120-500 silver coins of both revolts", 136, "Noe 1937 no. 514; Kadman 1967 no. 24", [852, 7100]),
    ("H46", "'Jerusalem 1974' revolt shekels", 7841, 31.778, 35.232, None, "First Revolt shekels (number not given)", 70, "CH III no. 88", None),
    ("H47", "'Jerusalem 1914' hoard", 8092, 31.768, 35.214, 2, "2+ silver and bronze provincial coins", 70, "Noe 1937 no. 515", None),
]:
    add(id=hid, name=nm, site="Jerusalem (no findspot)", scope="in", lat=lat, lon=lon, prec_km=3.0, coord_src=f"CHRE {chre} (generic)",
        provenance="reported/market", year_found=None, tpq=tpq, date_text="", contents=["silver_coins"], contents_text=ctext, count=n,
        mass_g=mass, mass_basis="nominal range (INFERENCE)" if mass else "", container="none", container_text="", findspot=["unknown"],
        findspot_text="no findspot", source=f"CHRE {C}{chre}; {src}")
add(id="H48", name="Robinson's Arch vault-room hoard A (1975)", site="SW corner of Temple Mount", scope="in", lat=31.776, lon=35.234, prec_km=0.1,
    coord_src="CHRE 7695", provenance="excavated (Mazar)", year_found=1975, tpq=69, date_text="34 burnt bronzes, First Revolt",
    contents=["bronze_coins", "metal_vessels"], contents_text="34 bronze coins with an intact cooking pot and a bronze juglet with chain", count=34,
    container="pot", container_text="cooking pot; bronze juglet with chain", findspot=["building"], cues=["floor"],
    findspot_text="on the floor of the Herodian vault room L6098, SE part of Robinson's Arch", source=f"CHRE {C}7695; Bijovsky 2009 pp. 74, 77-79")
add(id="H49", name="Robinson's Arch hoard B (1975)", site="SW corner of Temple Mount", scope="in", lat=31.775, lon=35.235, prec_km=0.1,
    coord_src="CHRE 7696", provenance="excavated", year_found=1975, tpq=69, date_text="13 burnt bronzes", contents=["bronze_coins"], contents_text="13 bronze coins",
    count=13, container="none", container_text="", findspot=["street"], findspot_text="L6095 between Herodian street and vault room L6032",
    source=f"CHRE {C}7696; Bijovsky 2009 p. 74")
add(id="H50", name="Western Wall shops prutah hoard", site="Herodian street along the Western Wall", scope="in", lat=31.776955, lon=35.234865, prec_km=0.1,
    coord_src="CHRE 7703", provenance="excavated (Reich & Billig)", year_found=1994, tpq=69, date_text="192 coins, mostly Revolt yrs 2-4",
    contents=["bronze_coins"], contents_text="192 bronze coins", count=192, container="none", container_text="", findspot=["building", "threshold", "wall"],
    cues=["threshold", "wall"], findspot_text="scattered on the threshold of a shop and the street; probably hidden in the wall",
    source=f"CHRE {C}7703; Reich & Billig 1998 p. 90; Bijovsky 2009 p. 74")
add(id="H51", name="Ophel cave Revolt bronzes (2018)", site="cave near the Temple Mount (Ophel)", scope="in", lat=31.775, lon=35.237, prec_km=0.2,
    coord_src="CHRE 12464", provenance="excavated (Hebrew Univ.)", year_found=2018, tpq=70, date_text="mostly year 4 (69/70 CE)", contents=["bronze_coins"],
    contents_text="bronze coins (number unclear)", count=None, container="none", container_text="", findspot=["cave"], findspot_text="7 x 14 m cave used as refuge",
    source=f"CHRE {C}12464; Borschel-Dan, Times of Israel 2018")
add(id="H52", name="Citadel mint debitage (1970)", site="Jerusalem Citadel", scope="in", lat=31.776, lon=35.228, prec_km=0.1, coord_src="CHRE 7659",
    provenance="excavated", year_found=1970, tpq=-4, date_text="125-4 BCE", contents=["bronze_coins", "mint_debitage"], contents_text="10 coins + 61 debitage fragments; flan mould",
    count=71, container="none", container_text="", findspot=["building"], findspot_text="industrial building", source=f"CHRE {C}7659; Schauer 2010 pp. 99-108")
add(id="H53", name="Tell el-Ful columbarium Nero bronzes", site="Tell el-Ful (Giv'at Sha'ul)", scope="in", lat=31.823260, lon=35.230791, prec_km=0.1,
    coord_src="CHRE 7601", provenance="excavated (Baruch)", year_found=2000, tpq=68, date_text="7 bronzes of Nero, 67-68 CE", contents=["bronze_coins"],
    contents_text="7 bronze coins", count=7, container="none", container_text="", findspot=["dovecote", "chamber"],
    findspot_text="blockage of a corridor of a large hewn columbarium on the SE slope of the mound (Ariel et al. 2014: 149)",
    source=f"CHRE {C}7601; Baruch 2000 p. 63; Ariel, Baruch & Zilberbod 2014 pp. 149-152")
add(id="H54", name="Mandelbaum Gate quarry hoard", site="Jerusalem, Mandelbaum Gate", scope="in", lat=31.786, lon=35.227, prec_km=0.1, coord_src="CHRE 7732",
    provenance="excavated", year_found=None, tpq=68, date_text="4 Nero bronzes", contents=["bronze_coins"], contents_text="4 bronze coins", count=4,
    container="none", container_text="", findspot=["field"], findspot_text="under quarry chips", source=f"CHRE {C}7732; Ariel et al. 2014 pp. 152-154")
add(id="H55", name="Shu'afat hoards 2005-2006 (four small bronze groups)", site="Shu'afat", scope="in", lat=31.814, lon=35.234, prec_km=1.0, coord_src="CHRE 7724/7728-7730",
    provenance="excavated", year_found=2006, tpq=72, date_text="72/73-138 CE", contents=["bronze_coins"], contents_text="8-30 bronzes each", count=None,
    container="none", container_text="", findspot=["unknown"], findspot_text="", source=f"CHRE {C}7724, {C}7728, {C}7729, {C}7730")
add(id="H56", name="Bethany stone-mug hoard (market)", site="Bethany (dubious)", scope="in", lat=31.771657, lon=35.255901, prec_km=3.0, coord_src="CHRE 9039",
    provenance="purchased; Butcher doubts provenance", year_found=1949, tpq=98, date_text="Domitian-Trajan", contents=["bronze_coins"], contents_text="14 Antiochene bronzes",
    count=14, container="jar", container_text="stone mug", findspot=["unknown"], findspot_text="", source=f"CHRE {C}9039; Saller 1957 p. 336")
add(id="H57", name="Bir ed-Duwali room-floor hoard", site="Bir ed-Duwali (Beitunia)", scope="edge", lat=31.882917, lon=35.140563, prec_km=0.2, coord_src="CHRE 9041",
    provenance="excavated", year_found=None, tpq=66, date_text="c. 100 First Revolt coins", contents=["bronze_coins"], contents_text="c. 100 coins", count=100,
    container="none", container_text="", findspot=["building"], cues=["floor"], findspot_text="floor of a room, Area D", source=f"CHRE {C}9041; Hizmi 2011 pp. 88-94")
add(id="H58", name="Bir Zeit 1890 jar of Year 3 silver", site="Bir Zeit", scope="edge", lat=31.959, lon=35.182, prec_km=2.0, coord_src="CHRE 8116",
    provenance="reported", year_found=1890, tpq=69, date_text="year 3", contents=["silver_coins"], contents_text="7 silver coins", count=7,
    mass_g=[50, 99], mass_basis="nominal range (INFERENCE)", container="jar", container_text="earthenware jar", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}8116; Kadman 1960 p. 82 n. 14a")
add(id="H59", name="Bir Zeit 1940 shekel hoard", site="Bir Zeit", scope="edge", lat=31.959, lon=35.182, prec_km=2.0, coord_src="CHRE 8117",
    provenance="reported", year_found=1940, tpq=69, date_text="49 Tyrian shekels 11/12-60/61 CE + Revolt shekels yrs 1-3", contents=["silver_coins"],
    contents_text="54 silver shekels", count=54, mass_g=[767, 767], mass_basis="nominal (INFERENCE)", container="none", container_text="",
    findspot=["unknown"], findspot_text="", source=f"CHRE {C}8117; Kadman 1960 p. 82")
add(id="H60", name="Horbat Mazruq (el-Mazruq) money-box hoard (2014)", site="near Abu Ghosh / Kiryat Ye'arim", scope="edge", lat=31.806, lon=35.109, prec_km=0.3,
    coord_src="CHRE 8132 (CHRE 18771 gives 31.8013, 35.1719 for the same find)", provenance="excavated (IAA, Route 1)", year_found=2014, tpq=70,
    date_text="114 bronzes of year 4 (69/70 CE)", contents=["bronze_coins"], contents_text="114 bronze coins", count=114, container="moneybox",
    container_text="ceramic money box", findspot=["building", "corner"], cues=["corner"],
    findspot_text="corner of a room, perhaps in a wall niche or buried in the floor",
    source=f"CHRE {C}8132, {C}18771; https://embassies.gov.il/atlanta/NewsAndEvents/Pages/Hoard-of-coins-from-Great-Revolt-discovered-5-Aug-2014.aspx; Marco & Betzer 2016")
add(id="H61", name="'Reuben Hecht hoard' (Bethlehem vicinity)", site="near Bethlehem (dealer)", scope="in", lat=31.705, lon=35.202, prec_km=5.0, coord_src="CHRE 8168",
    provenance="market (late 1960s)", year_found=1968, tpq=67, date_text="ends with First Revolt shekels", contents=["silver_coins"], contents_text="c. 30 shekels originally (15 known)",
    count=30, mass_g=[213, 426], mass_basis="nominal range (INFERENCE)", container="none", container_text="", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}8168; Meshorer 1985")
add(id="H62", name="Te'omim Cave hoard B", site="Te'omim Cave, western Jerusalem hills", scope="edge", lat=31.726234, lon=35.020295, prec_km=0.2,
    coord_src="CHRE 7595", provenance="excavated (Zissu et al.)", year_found=2009, tpq=132, date_text="Bar Kokhba", contents=["silver_coins", "bronze_coins"],
    contents_text="9 silver + 1 bronze", count=10, mass_g=[31, 128], mass_basis="nominal range (INFERENCE)", container="none", container_text="",
    findspot=["cave", "fissure"], findspot_text="in a crack between fallen ceiling rocks next to hoard A (in a rock hole)",
    source=f"CHRE {C}7595; Zissu, Porat, Langford & Frumkin 2011; Zissu & Hendin 2012 pp. 221-222")

# ---------------- Samaria ----------------
add(id="H63", name="'Nablus' Tyrian tetradrachm hoard (1930/1935-36)", site="Nablus (attribution; town at the foot of Mt Gerizim)", scope="in",
    lat=32.20082, lon=35.27326, prec_km=3.0, coord_src="NO coordinates in CHRE; anchored to atlas Gerizim point with 3 km radius (INFERENCE)",
    provenance="reported", year_found=1930, tpq=-1, date_text="2nd-1st c. BCE", contents=["silver_coins"], contents_text="86+ Tyrian tetradrachms (IGCH 1629/1630 possibly one hoard)",
    count=86, mass_g=[1221, 1221], mass_basis="nominal, lower bound (INFERENCE)", container="none", container_text="", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}8036; IGCH 1629, 1630; Kadman 1967 nos. 12-13; Leonard 2000 p. 685")
add(id="H64", name="Sebastia 1910 hoard", site="Samaria-Sebaste", scope="in", lat=32.2771, lon=35.1884, prec_km=0.3, coord_src="CHRE 8097",
    provenance="excavated (Harvard)", year_found=1910, tpq=-74, date_text="after 74 BCE", contents=["silver_coins", "bronze_coins"],
    contents_text="1 tetradrachm + 22 bronze coins of Tyre", count=23, mass_g=[14, 14], mass_basis="nominal (INFERENCE)", container="none", container_text="",
    findspot=["unknown"], findspot_text="", source=f"CHRE {C}8097; Harvard Excavations at Samaria I pp. 52, 253, 261, 264")

# ---------------- out-of-region comparanda (not scored) ----------------
add(id="X01", name="'Isfiya (Mt Carmel) hoard 1960", site="'Isfiya", scope="out_region", lat=32.721, lon=35.059, prec_km=1.0, coord_src="CHRE 7657",
    provenance="farmers' find", year_found=1960, tpq=52, date_text="Tyrian silver 41/40 BCE-52/53 CE",
    contents=["silver_coins"], contents_text="3,850 Tyrian tetradrachms, 110 drachms, 275 Roman denarii (c. 4,500 total)", count=4560,
    mass_g=[55600, 56100], mass_basis="nominal (INFERENCE); Leonard 1999 quoted 7.8 kg = 0.366 talent, which is inconsistent with this count",
    container="pot", container_text="pot", findspot=["unknown"], findspot_text="below the surface near the ancient synagogue",
    source=f"CHRE {C}7657; Kadman 1960, 1961, 1962; CH I no. 118; https://orion.huji.ac.il/orion/archives/1999b/msg00557.html")
add(id="X02", name="'Northern Israel' Tyrian shekels (trade)", site="unknown, N Israel", scope="out_region", lat=None, lon=None, prec_km=None, coord_src="",
    provenance="trade", year_found=None, tpq=40, date_text="year 166 (40/41 CE)", contents=["silver_coins"], contents_text="100+ Tyrian shekels", count=100,
    container="none", container_text="", findspot=["unknown"], findspot_text="", source=f"CHRE {C}7955; CH VIII no. 551")
add(id="X03", name="'Israel 1991' and 'Israel 1997 B' Tyrian shekel hoards (trade)", site="unknown", scope="out_region", lat=None, lon=None, prec_km=None,
    coord_src="", provenance="trade (info D. Hendin via Leonard 2000)", year_found=1991, tpq=66, date_text="to c. 66-70 CE", contents=["silver_coins"],
    contents_text="500+ and 500-800 Tyrian shekels", count=800, container="none", container_text="", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}9151, {C}9152; Leonard 2000 p. 686")
add(id="X04", name="Gamla street hoard", site="Gamla (Golan)", scope="out_region", lat=32.9028, lon=35.7406, prec_km=0.2, coord_src="CHRE 7592",
    provenance="excavated", year_found=None, tpq=60, date_text="lost Oct 67 CE", contents=["silver_coins"], contents_text="20 Tyrian shekels + 7 Nero tetradrachms",
    count=27, container="juglet", container_text="small juglet", findspot=["street"], findspot_text="street before an olive press", source=f"CHRE {C}7592; Syon 2014 p. 126")
add(id="X05", name="Modi'in 2016 Hasmonean-estate hoard", site="Modi'in", scope="out_region", lat=None, lon=None, prec_km=None, coord_src="",
    provenance="excavated (IAA)", year_found=2016, tpq=-126, date_text="135-126 BCE", contents=["silver_coins"], contents_text="16 Tyrian silver shekels/half-shekels",
    count=16, container="none", container_text="", findspot=["fissure", "wall"], findspot_text="rock crevice against a wall",
    source="https://www.jewishnews.co.uk/rare-cache-of-silver-coins-from-over-2000-years-ago-discovered-in-israel/ ; https://www.coinworld.com/news/world-coins/silver-coin-hoard-found-in-israel.html")
add(id="X06", name="Horvat 'Aqrav (Upper Galilee) Tyrian silver hoard", site="Upper Galilee", scope="out_region", lat=None, lon=None, prec_km=None, coord_src="",
    provenance="found 1970", year_found=1970, tpq=-110, date_text="buried c. 110 BCE", contents=["silver_coins"], contents_text="20 documented coins (<half the find)",
    count=20, container="none", container_text="", findspot=["unknown"], findspot_text="", source="Syon, INR 9 (2014) 29-37 (https://lockwoodonlinejournals.com/index.php/inr/article/view/2708)")
add(id="X07", name="Nahal Shalva gold-and-silver hoard", site="Qiryat Gat region", scope="out_region", lat=31.565, lon=34.794, prec_km=0.5, coord_src="CHRE 7617",
    provenance="excavated (IAA 2012)", year_found=2012, tpq=117, date_text="Bar Kokhba", contents=["gold_coins", "silver_coins", "jewelry"],
    contents_text="4 aurei, 132 silver, jewellery", count=136, container="bag", container_text="cloth (linen traces)", findspot=["pit", "court"],
    findspot_text="pit in a courtyard", source=f"CHRE {C}7617")
add(id="X08", name="Hebron-hills Bar Kokhba silver hoards (El Fawar, Duma, Idna, Yatta etc.)", site="S Judean hills", scope="out_region", lat=None, lon=None,
    prec_km=None, coord_src="", provenance="mostly market", year_found=None, tpq=132, date_text="132-136 CE", contents=["silver_coins"],
    contents_text="e.g. El Fawar c. 2,500; Duma c. 1,200", count=2500, container="none", container_text="", findspot=["unknown"], findspot_text="",
    source=f"CHRE {C}8501, {C}8499, {C}8464, {C}7959 (Mildenberg 1984)")

# ---------------- out of period (listed only) ----------------
add(id="P01", name="Nahal Mishmar 'Cave of the Treasure'", site="Nahal Mishmar", scope="out_period", lat=None, lon=None, prec_km=None, coord_src="",
    provenance="excavated (Bar-Adon 1961)", year_found=1961, tpq=None, date_text="Chalcolithic (4th millennium BCE)", contents=["metal_vessels"],
    contents_text="429 objects (416 copper): maceheads, wands, 'crowns'", count=429, container="basket", container_text="wrapped in a mat",
    findspot=["cave", "fissure"], findspot_text="niche in the cave", source="https://www.jewishvirtuallibrary.org/judean-desert-caves (container/niche detail not verified here)")
add(id="P02", name="Givati parking lot Byzantine gold (2008)", site="City of David, Jerusalem", scope="out_period", lat=None, lon=None, prec_km=None, coord_src="",
    provenance="excavated (IAA)", year_found=2008, tpq=613, date_text="early 7th c. CE", contents=["gold_coins"], contents_text="264 gold coins", count=264,
    container="none", container_text="", findspot=["building"], findspot_text="", source="https://embassies.gov.il/MFA/IsraelExperience/history/Pages/Byzantine-coins-found- in-Jerusalem-excavations-22-Dec-2008.aspx")
add(id="P03", name="Beth Shean 1950 and 1958 hoards", site="Beth Shean", scope="out_period", lat=32.497, lon=35.497, prec_km=0.5, coord_src="CHRE 7621/8140",
    provenance="reported", year_found=1950, tpq=253, date_text="3rd and 5th c. CE", contents=["bronze_coins"], contents_text="414 and 12 coins", count=426,
    container="juglet", container_text="juglet (1950)", findspot=["court"], findspot_text="courtyard 151 room 4 (1950)", source=f"CHRE {C}7621, {C}8140; Kadman 1967 nos. 49, 61")
add(id="P04", name="Ramat Rahel Byzantine coin deposits (2008)", site="Ramat Rahel", scope="out_period", lat=31.7401, lon=35.2175, prec_km=0.1, coord_src="",
    provenance="excavated", year_found=2008, tpq=400, date_text="4th-5th c. CE", contents=["bronze_coins"], contents_text="380 + 70 coins", count=450,
    container="none", container_text="", findspot=["building"], findspot_text="stone floor near the shekel hoard", source="https://www.uni-heidelberg.de/presse/news08/pm595e.html")


def main():
    json.dump(H, open(os.path.join(OUT, "hoards.json"), "w"), ensure_ascii=False, indent=1)
    cols = ["id", "name", "site", "scope", "lat", "lon", "prec_km", "coord_src", "provenance", "year_found", "tpq", "date_text",
            "contents", "contents_text", "count", "mass_g", "mass_basis", "container", "container_text", "findspot", "cues", "depth_m",
            "findspot_text", "source", "notes"]
    with open(os.path.join(OUT, "hoards.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for h in H:
            w.writerow([";".join(map(str, h[c])) if isinstance(h.get(c), list) else h.get(c) for c in cols])
    from collections import Counter
    print(len(H), "records", Counter(h["scope"] for h in H))


if __name__ == "__main__":
    main()
