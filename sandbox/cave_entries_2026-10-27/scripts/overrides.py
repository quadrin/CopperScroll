"""Hand coding of the text-dependent constraints (step 3), fixed after reading flags_auto.json and
cave_texts.json and BEFORE score.py was run. Every pass needs a statement in the source; default is unknown.

Keys: cave_id -> dict of flags. Values: True (pass, strict), "lenient" (pass only in the lenient setting).
Flags:
  building      E7.L / L7: built structure at or attached to the cave
  three         E7.R: >=3 ledges, levels, terraces or stone courses
  fissure       E22.F: crevice / cleft / fissure / crack
  vessels       E22.I part 1: vessels (pottery vessels, jars, jugs, bowls, lamps)
  written       E22.I part 2: written material (texts, papyri, ostracon, inscription)
  jar, scroll   E25.I: a jar AND a scroll (scroll fragments / wrappers count, as fixed in step 1)
  heap          E26.L / L26: cairn, stone heap or boulder at the mouth / corner / front
  coins         E26.I (talents) and E38.I (staters): coins or a metal hoard
  silver        E30.I: silver in any form
  gold_bars     E7.I: gold or metal bars / ingots
  spring        E38.P / L38: the record places the cave at a spring
  removal       descriptor only: signs of removal / plunder / blocked or sealed openings
"""

SRC_DJD = "DJD III (repo extraction research/history/djd3_text_cave_list_extracted.md)"

O = {
    # --- DJD III cliff sites (site table pp. 6-13; jar table p. 14; lid table p. 15) ---
    "DJD3:8": dict(vessels=True, jar=True, written=True, scroll=True, removal=False,
                   basis="3Q: c. 35 jars, 26 lids, jugs, lamp; skin texts (Baillet pp. 94-104) and the copper rolls (pp. 7-8, 201)"),
    "A41:XI/19": dict(vessels=True, jar=True, written=True, scroll=True, removal=True,
                      basis="2Q = site 19: c. 8 jars, lid, 3 bowls; texts Baillet pp. 48-93; emptied by the Bedouin (DJD III pp. 3, 9)"),
    "DJD3:26": dict(vessels=True, jar=True, written=True, scroll=True, removal=True,
                    basis="6Q = site 26: jar t9 and bowl; texts Baillet pp. 105-41; emptied by the Bedouin (DJD III pp. 15, 26)"),
    "DJD3:10Q": dict(vessels=True, written=True, basis="10Q: Qumran pottery (fig. 6, 10Q3) and an ostracon only (DJD III p. 34 n. 1)"),
    "DJD3:7Q": dict(vessels=True, written=True, basis="7Q: pottery fig. 6 (7Q2-7Q6); manuscript cave (DJD III p. 34 n. 1)"),
    "DJD3:8Q": dict(vessels=True, written=True, basis="8Q: pottery fig. 6 (8Q7-8Q14); manuscript cave (DJD III p. 34 n. 1; 8Q phylactery figs. 8-12)"),
    "DJD3:9Q": dict(written=True, basis="9Q: manuscript cave (DJD III p. 34 n. 1); no 9Q piece in fig. 6"),
    "DJD3:5Q": dict(written=True, basis="5Q: manuscript cave (DJD III p. 34 n. 1)"),
    "DJD3:4Q": dict(written=True, basis="4Q: manuscript cave (DJD III p. 34 n. 1)"),
    "DJD3:11Q": dict(written=True, removal=True, basis="11Q: manuscript cave with a blocked entrance (DJD III pp. 4, 34 n. 1)"),
    "DJD3:14": dict(written=True, basis="1Q: manuscript cave (DJD III p. 34 n. 1); DJD I not read"),
    "DJD3:29": dict(vessels=True, jar=True, removal=True,
                    basis="site 29: c. 13 jars, 17 lids; de Vaux's candidate for an anciently violated deposit (p. 34)"),
    "DJD3:12": dict(vessels=True, jar=True, basis="site 12 (rock shelter): 5 jars, lids, bowl, mat"),
    "DJD3:17": dict(vessels=True, jar=True, fissure=True, removal=True,
                    basis="site 17: crevice; jars, bowls, pot, lamp; posts stored or hidden (pp. 16-17, 34)"),
    "DJD3:9": dict(vessels=True, fissure=True, removal=True, basis="site 9: crevice closed by a dry-stone wall; Herodian lamp, juglet"),
    "DJD3:15": dict(vessels=True, jar=True, fissure=True, basis="site 15: cleft; jar t10 with its bowl-lid"),
    "DJD3:21": dict(vessels=True, jar=True, fissure=True, basis="site 21: rock fissure; 4 jars washed in"),
    "DJD3:30": dict(vessels=True, jar=True, fissure=True, basis="site 30: cleft; Qumran jar"),
    "DJD3:3": dict(vessels=True, jar=True, basis="site 3: jars, lids, cooking pot, goblet; bronze ring"),
    "DJD3:39": dict(vessels=True, jar=True, removal=True, basis="site 39: jars, lids, bowl; Bedouin holes (p. 12)"),
    "DJD3:1": dict(vessels=True, jar=True, basis="site 1: Qumran jar and lid"),
    "DJD3:7": dict(vessels=True, jar=True, basis="site 7: lid and jar"),
    "DJD3:10": dict(vessels=True, jar=True, basis="site 10: 2 jars"),
    "DJD3:18": dict(vessels=True, jar=True, basis="site 18: 4 jars"),
    "DJD3:22": dict(vessels=True, jar=True, basis="site 22: jar base"),
    "DJD3:28": dict(vessels=True, jar=True, basis="site 28: jars and lids"),
    "DJD3:31": dict(vessels=True, jar=True, basis="site 31: bowls and jars"),
    "DJD3:32": dict(vessels=True, jar=True, basis="site 32: jars and lid"),
    "DJD3:40": dict(vessels=True, jar=True, basis="site 40: jar"),
    "DJD3:37": dict(vessels=True, basis="site 37: bowl and goblet bases"),
    "DJD3:23": dict(basis="site 23: low wall in front of the entrance (a wall, not a building)"),
    # --- Atiqot 41 / lane rows ---
    "A41:XII/53": dict(heap=True, vessels=True, jar=True, scroll=True, removal=True,
                       basis="Atiqot 41 pp. 207-210 (lane coding): southern part of the opening blocked by a large boulder; "
                             "2017 re-excavation (Gutfeld, IAA 'Operation Scroll'; NBC News 8 Feb 2017; JPost 2022 'Cave 53', earlier dug by Israel and Cohen): "
                             "broken storage jars and lids, scroll wrappings (leather, string), a blank parchment piece, pickaxe heads (looting)"),
    "A41:III/11": dict(vessels=True, written=True, coins=True, basis="pottery, coins, papyrus scraps"),
    "A41:VIII/9": dict(vessels=True, written=True, coins=True, basis="papyri, Early Roman cooking pot, coins"),
    "A41:VIII/10": dict(vessels=True, written=True, basis="Avior cave: papyri, pottery, glass"),
    "WB:E333": dict(written=True, coins=True, basis="Avi'or Cave: Bar Kokhba papyri; coins"),
    "A41:VIII/28": dict(written=True, basis="documents of the Bar Kokhba period (Eshel and Zissu 1999)"),
    "Z23:KetefJericho": dict(written=True, basis="First Revolt papyri (Zissu)"),
    "PAT:UMakkuk-1": dict(three=True, written=True, basis="three levels; Greek and Arabic inscriptions"),
    "A41:VII/15": dict(written=True, basis="Arabic inscription on a lintel"),
    "A41:V/38": dict(three=True, basis="cave of three wings and three levels; courtyard enclosed by a wall"),
    "A41:VI/56": dict(three=True, basis="access by a path on a stone wall of 11 courses"),
    "A41:I/1": dict(three="lenient", basis="'perhaps three levels'"),
    "PAT:UMakkuk-7": dict(three="lenient", removal=True, basis="chambers on several levels, once closed by stone walls"),
    "ASI:109/4-7-Cell2": dict(three="lenient", building=True, basis="floor on several levels; monastic cell built in a cave"),
    "A41:III/12": dict(fissure=True, basis="entry through a natural crack"),
    "PAT:UMakkuk-5": dict(fissure=True, spring=True, removal=True,
                          basis="'Cave of the Spring': a fissure whose opening is blocked by a masonry wall; a plastered reservoir collects a small spring; traces of digging and sieving"),
    "A41:III/4": dict(fissure=True, basis="natural crevice"), "A41:VIII/11": dict(fissure=True, basis="cleft"),
    "A41:VIII/19": dict(fissure=True, basis="cleft"), "A41:VIII/25": dict(fissure=True, silver=True, basis="cleft; a decorated medieval silver piece beside it"),
    "A41:VIII/32": dict(fissure=True, basis="two clefts"), "A41:VIII/37": dict(fissure=True, basis="three clefts"),
    "A41:VIII/45": dict(fissure=True, basis="cleft"), "A41:XI/12": dict(fissure=True, basis="crevice"),
    "A41:IV/6": dict(coins=True, silver=True, vessels=True, removal=True, basis="silver drachms, Yehud and Hellenistic coins, glass bowl; plundered"),
    "PAT:LMakkuk-2": dict(coins=True, silver=True, basis="a silver Islamic coin at its foot"),
    "A41:III/8": dict(coins=True, basis="12 coins (9 Jannaeus)"), "A41:III/3": dict(coins=True, removal=True, basis="coin of Side; blocked opening"),
    "A41:IV/1": dict(coins=True, basis="Jannaeus and Hasmonean coins"), "A41:IV/5": dict(coins=True, vessels=True, basis="coins, lamp, cooking pots in situ"),
    "A41:IV/7": dict(coins=True, vessels=True, removal=True, basis="coins, pottery; opening blocked by a low wall"),
    "A41:IV/8": dict(coins=True, basis="seven Hasmonean coins"), "A41:IV/11": dict(coins=True, basis="Hasmonean coins"),
    "A41:IV/12": dict(coins=True, basis="coins Ptolemy II to Herod I"), "A41:IV/17": dict(coins=True, removal=True, basis="coins; southern opening partly blocked by a built wall"),
    "A41:VI/43": dict(coins=True, basis="coins of John Hyrcanus I"), "A41:VI/46": dict(coins=True, vessels=True, basis="pottery, coins"),
    "A41:VI/47": dict(coins=True, basis="coins (4th-5th c. CE)"), "A41:VII/1": dict(coins=True, vessels=True, basis="pottery, glass, coins"),
    "A41:VII/3": dict(coins=True, vessels=True, basis="pottery, coins of Valerius Gratus"), "A41:VIII/6": dict(coins=True, basis="coins"),
    "A41:X/35": dict(coins=True, vessels=True, basis="juglet of oil, lamps, prutah of year 2"), "A41:X/57": dict(coins=True, basis="Byzantine coin"),
    "A41:XIII/2": dict(coins=True, basis="unidentified coins"), "A41:V/50": dict(coins=True, basis="Byzantine and Mamluk coins"),
    "WB:E762": dict(coins=True, vessels=True, basis="Early Roman pottery, coins, nails"),
    "A41:XI/6": dict(vessels=True, jar=True, basis="'scroll jar' rim and a 1st c. CE jar"),
    "A41:XI/10": dict(vessels=True, jar=True, basis="jarlet, Second Temple bottle"),
    "A41:XII/52": dict(vessels=True, jar=True, removal=True, basis="jars of the 1st c. CE; earlier digging"),
    "A41:X/60": dict(vessels=True, jar=True, basis="Roman and Byzantine jars and jugs"),
    "A41:XI/18": dict(vessels=True, basis="Roman lid-bowl"),
    "PAT:UMakkuk-6": dict(vessels=True, jar=True, basis="Roman jar fragment"),
    "PAT:Qilt-20": dict(vessels=True, basis="jug fragments, Roman lamp"),
    "PAT:LMakkuk-5": dict(vessels=True, basis="Roman sherds and broken stone vessels"),
    # buildings at caves (lane rows; ASI-Jerusalem rows are handled by class co-occurrence, lenient)
    "ASI:83/12-76": dict(building=True, basis="'cave at a building site'"),
    "ASI:109/4-7-Cell6": dict(building=True, basis="cave at the base of a chapel (complex of buildings)"),
}
for n in (1, 3, 4, 5, 8, 9, 10, 11, 12, 13, 15, 16):
    O.setdefault(f"ASI:109/4-7-Cell{n}", {}).update(building=True, basis="monastic cell built in a natural cave (Choziba laura, ASI 109/4)")
