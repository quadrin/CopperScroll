"""ASI online site records inside the box (PLAN.md S9), coded by hand.

Fetched 2026-10-11 05:05Z with scripts/intake/fetch_asi_box.py (cache outside the repository; manifest hashes are in
../intake/asi_manifest.csv) and flattened with scripts/intake/asi_extract.py; read 05:06:26Z onward.
Online sheets intersecting the box: 83/12 Wadi el-Makokh (Goldfus and Golani), 109/4 Wadi Qelt (Sion), 109/5 Kalia
(Sion), 109/7 Deir Mar Saba (Patrich), 147 'Ein Gedi (Hadas). Sheets 102, 106, 108/2 and 83/2 only touch the western
edge (E 180,000). Not online: 83/10, 83/13, 109/3, 109/8 (the Qumran-Feshkha shore), 109/9, 109/10, 109/11, 134.
Admission (PLAN 4.1): records (or described sub-units of records) that the source calls a cave. A record that only
names caves in passing, with neither count nor description, is listed in excluded.csv. Groups without a count are
cluster rows with cluster_count empty. Coordinates: the record's WGS84 site point unless a sub-unit has its own
printed map reference (Old Israel Grid, 10 m units, as printed in these records). Facing-word resolution is set per
sheet (A4): 109/4, 109/7 and 83/12 records use intercardinal words somewhere, so 8-point; 147 and 109/5 4-point.
Exposure: sites already in research/regional/asi_jerusalem/sites.csv (109/4 sites 7, 8; 109/5 site 108; 109/7 sites
35, 63, 70, 89, 96, 98) are 'exposed-repo'; the rest were first read here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

ROWS, EXCL = [], []
MERGE = {"PAT:Qilt-16": "ASI:109/4-7-Cell10", "PAT:Qilt-13": "ASI:109/4-7-Cplx7"}
T = "2026-10-11T05:06:26Z"
EXPOSED = {("109/4", 7), ("109/4", 8), ("109/5", 108), ("109/7", 35), ("109/7", 63), ("109/7", 70), ("109/7", 89), ("109/7", 96), ("109/7", 98)}
SHEET = {"109/5": ("Kalia", "Sion 2013", 4), "147": ("'Ein Gedi", "Hadas", 4), "109/4": ("Wadi Qelt", "Sion 2013", 8),
         "83/12": ("Wadi el-Makokh", "Goldfus and Golani", 8), "109/7": ("Deir Mar Saba", "Patrich", 8)}
PT = {}  # (sheet, site) -> (lat, lon) of the record's site point


def pt(sheet, site, lat, lon):
    PT[(sheet, site)] = (lat, lon)


def a(sheet, site, sub, num, *, grid="", crs=None, cbasis=None, kind="cave", cluster=None, c1=None, ftype="cave", **kw):
    name, auth, res = SHEET[sheet]
    if not grid:
        lat, lon = PT[(sheet, site)]
        grid, crs, cbasis = f"{lat}/{lon}", "WGS84", cbasis or "ASI site point (record's WGS84 point; site centre)"
    else:
        crs, cbasis = crs or "OIG", cbasis or "map reference printed for this unit in the record"
    cid = f"ASI:{sheet}-{site}" + (f"-{sub}" if sub else "")
    kw.setdefault("res", res)
    kw.setdefault("exc", "surveyed")
    R(ROWS, cid, num=num, src=f"ASI Map of {name} ({sheet}), {auth}, site {site} (survey.iaa.org.il online record)",
      lineage=f"Archaeological Survey of Israel, Map of {name} ({sheet})", ftype=ftype, kind=kind, cluster=cluster, grid=grid, crs=crs,
      cbasis=cbasis, c1=c1, exposure="exposed-repo" if (sheet, site) in EXPOSED else "unexposed-at-freeze", read=T, **kw)


def x(sheet, site, what, why):
    X(EXCL, f"ASI:{sheet}-{site}", num=f"ASI {sheet} site {site}", src=f"ASI Map of {SHEET[sheet][0]} ({sheet}), site {site}", ftype=what,
      reason=why, exposure="exposed-repo" if (sheet, site) in EXPOSED else "unexposed-at-freeze", read=T)


# ---------------------------------------------------------------- 109/5 Kalia
pt("109/5", 108, 31.76787, 35.45608)
for sub, g, dims in (("1", "", "h 2.5, depth 6, width 3 m; printed map ref '19310131100' (garbled; site point used)"),
                     ("1a", "", "c. 8 m W of Cave 1; h 4, depth 3.5, width 2 m"),
                     ("2", "19330/13070", "on the N side of the valley; h 6, depth 15, width 5 m"),
                     ("3", "19315/13040", "h 3.5, depth 7, width 2 m; devoid of finds"),
                     ("4", "19365/13010", "fairly large: h 6, width c. 10, length 35 m")):
    a("109/5", 108, f"Cave{sub}", f"Zahr Danab Ghayar Cave {sub} (ASI 109/5 site 108)", grid=g, period="no sherds in any of the caves", piw="", notes=dims)

# ---------------------------------------------------------------- 147 'Ein Gedi
for s, la, lo in ((50, 31.47459, 35.32083), (90, 31.47558, 35.39639), (91, 31.47531, 35.39597), (96, 31.47134, 35.31641), (111, 31.46682, 35.32903),
                  (118, 31.46745, 35.33640), (125, 31.47041, 35.35019), (127, 31.46915, 35.34913), (128, 31.46860, 35.35271), (149, 31.47309, 35.37429),
                  (180, 31.47279, 35.39586), (181, 31.47270, 35.39375), (182, 31.47216, 35.39081), (185, 31.47197, 35.39575), (187, 31.47152, 35.39586),
                  (195, 31.46909, 35.39322), (201, 31.46810, 35.39680), (213, 31.46504, 35.38964), (238, 31.45734, 35.34533), (272, 31.46243, 35.38479),
                  (285, 31.46008, 35.38531), (295, 31.45602, 35.38815), (296, 31.45593, 35.38878), (300, 31.46450, 35.38953), (331, 31.44741, 35.35478),
                  (365, 31.43841, 35.33478), (377, 31.44470, 35.35478), (412, 31.43435, 35.33572), (413, 31.43390, 35.33215), (414, 31.43390, 35.33267),
                  (415, 31.43300, 35.32951), (417, 31.43119, 35.33298), (429, 31.43298, 35.34540)):
    pt("147", s, la, lo)
G = "147"
a(G, 50, "", "Nahal Arugot large cave (ASI 147 site 50)", n_open=1, open_basis="singular description (walls and steps in the entrance to the cave)",
  plan="plan cited in the record (not online)", notes="Three chambers; the rear collapsed into a drainage tunnel.")
a(G, 90, "", "Har Yishay cave with Hebrew inscription (ASI 147 site 90)", ftype="natural cave, two storeys",
  period="Chalcolithic, Iron, Hellenistic, Roman, Byzantine; 8th-7th c. BCE inscription", piw="partly",
  notes="Stalactites and stalagmites; inscription in the eastern chamber of the upper level (Bar-Adon 1975).")
a(G, 91, "", "Har Yishay cave in a rock shelter (ASI 147 site 91)", ftype="cave inside a rock shelter",
  n_open=2, open_basis="stated: an entrance (3.5 x 3.5 m, 0.5 m high) and a second way into the hall by the channel south of the rock shelter",
  north="decided", north_basis="INFERENCE: the second way in is by a channel south of the rock shelter, so the rock-shelter entrance is the northern one",
  period="Early Bronze, Roman, Byzantine pottery", piw="partly",
  notes="An open area c. 6 x 6 m in front of the cave (not a terrace word; natural). The record gives no facing.")
a(G, 96, "", "two rock shelters including caves, Nahal Arugot (ASI 147 site 96)", kind="cluster", c1="unknown", ftype="rock shelters including caves",
  period="Early Bronze and Ottoman", piw="no")
a(G, 111, "", "cave in a bedrock notch with a shepherd's shelter (ASI 147 site 111)", notes="Cave 3 x 3 m.")
for sub, nb in (("a", dict(n_open=1, open_basis="singular description (a square opening 1 x 1 m)", notes="Hall 6 m diameter, 3 m high.")),
                ("b", dict(notes="8 m deep, 6 m wide, 2 m high.")),
                ("c", dict(n_open=1, open_basis="singular description (a millstone near its opening)", notes="7.5 m deep, 2.5 m wide, 1 m high."))):
    a(G, 118, sub, f"Nahal Arugot slope cave {sub} (ASI 147 site 118)", period="site finds: Upper Palaeolithic to EB flints; EB, Early Roman and Byzantine pottery",
      piw="yes+other", **nb)
a(G, 125, "", "'Ein Arugot cave in a bedrock notch (ASI 147 site 125)", n_open=1, open_basis="stated (opening 2.5 x 4 m; remains of a blocking wall)")
a(G, 127, "", "Nahal Arugot natural cave (ASI 147 site 127)", n_open=1, open_basis="stated (a large opening c. 12 x 20 m)",
  period="Iron Age and Roman pottery; seal impression", piw="partly")
a(G, 128, "", "Nahal Arugot natural cave (ASI 147 site 128)", period="Iron Age pottery", piw="no", notes="A niche at the eastern end.")
a(G, 149, "", "Cave of the Pool, Nahal David (ASI 147 site 149)", n_open=1, open_basis="singular description (a plastered pool in its opening)",
  period="Chalcolithic, Iron I and Roman pottery; Bar Kokhba arrowheads, coins, comb", piw="yes+other", exc="excavated (Avigad 1961-62)",
  notes="North bank of Nahal David; 30 m long.")
a(G, 180, "1", "Newe 'Ein Gedi cave 1 (ASI 147 site 180)", n_open=1, open_basis="singular description (an opening blocked by a wall)",
  period="Early Roman pottery", piw="yes", notes="4 x 4 m, 2 m high.")
a(G, 180, "2", "Newe 'Ein Gedi cave 2 (ASI 147 site 180)", grid="18765/09785", n_open=1, open_basis="stated (its opening 0.9 x 1.2 m)",
  terrace="yes", terrace_basis="a retaining wall built in front of it forms a horizontal surface c. 3 x 3 m (a built platform)",
  period="Early Roman and Byzantine pottery", piw="yes+other", notes="c. 20 m S of cave 1; partly rock-hewn.")
a(G, 181, "", "Newe 'Ein Gedi natural cave (ASI 147 site 181)", period="Roman and Byzantine pottery", piw="partly", notes="2 x 9 m, 9 m high; stalactites.")
a(G, 182, "", "Newe 'Ein Gedi natural cave (ASI 147 site 182)", n_open=1, open_basis="stated (an opening 2.5 m wide, 2 m high)",
  period="Roman-Byzantine pottery", piw="partly", notes="Divided into two sections, 7.3 m deep. Cites Eshel and Porat 2009.")
a(G, 185, "77/42", "Newe 'Ein Gedi rock-hewn burial cave 77/42 (ASI 147 site 185)", ftype="rock-hewn burial cave",
  terrace="yes", terrace_basis="a large courtyard to its east with built walls (N wall 11.3 m, E wall 14.4 m)", plan="plan cited in the record (not online)",
  period="Early Roman pottery (all three caves)", piw="yes")
a(G, 185, "77/43", "Newe 'Ein Gedi cave 77/43 (ASI 147 site 185)", n_open=1, open_basis="stated (the cave opening is large, 1.4 x 1.5 m)",
  period="Early Roman pottery (all three caves)", piw="yes", notes="c. 10 m N of 77/42; construction and plaster inside.")
a(G, 185, "77/44", "Newe 'Ein Gedi two-chamber cave 77/44 (ASI 147 site 185)", period="Early Roman pottery (all three caves)", piw="yes",
  notes="c. 5 m N of 77/42; a small niche facing south (a niche, not a mouth).")
a(G, 187, "", "Newe 'Ein Gedi blocked natural cave (ASI 147 site 187)", n_open=1, open_basis="stated (the cave opening 0.8 x 1.0 m)",
  period="Early Roman pottery", piw="yes")
a(G, 195, "", "burial caves in the northern cliff of Nahal David (ASI 147 site 195)", kind="cluster", ftype="group of burial caves",
  notes="Cites Avigad 1962: 156-158.")
a(G, 201, "", "Newe 'Ein Gedi two-level burial cave (ASI 147 site 201)", ftype="burial cave with six plastered loculi")
a(G, 213, "", "Newe 'Ein Gedi natural cave (ASI 147 site 213)", plan="plan cited in the record (not online)",
  period="Chalcolithic pottery; Persian-period jewellery (Eshel and Porat excavation)", piw="no", exc="excavated (Eshel and Porat)")
for sub, d in (("a", "c. 10 m long, 1.1 m high, 7 m deep; sooty ceiling"), ("b", "9 m long, 3 m high, 3 m deep"), ("c", "5 m long, 3 m deep, 1.5 m high; sooty ceiling")):
    a(G, 238, sub, f"Har Avishay wadi-cliff cave {sub} (ASI 147 site 238)", notes=d)
a(G, 272, "", "Newe 'Ein Gedi loculi cave with a nefesh (ASI 147 site 272)", ftype="loculi (burial) cave, two chambers", plan="plan cited in the record (not online)")
a(G, 285, "", "Newe 'Ein Gedi loculi burial cave with a courtyard (ASI 147 site 285)", ftype="burial cave with loculi",
  terrace="yes", terrace_basis="'in front of the cave is a courtyard'", period="Early Roman pottery, ossuary fragments, glass", piw="yes")
a(G, 295, "1", "Newe 'Ein Gedi burial cave with fifteen wooden coffins (ASI 147 site 295)", ftype="burial cave (ruinous)",
  period="Hellenistic (2nd-1st c. BCE)", piw="partly", exc="excavated (Hadas 1994)")
a(G, 295, "2", "Newe 'Ein Gedi burial cave (ASI 147 site 295)", grid="18680/09601", ftype="burial cave (ruinous)", period="Hellenistic pottery", piw="partly",
  exc="excavated (Hadas 1994)")
a(G, 295, "3", "Newe 'Ein Gedi burial cave, destroyed (ASI 147 site 295)", grid="18699/09600", ftype="burial cave (destroyed)",
  period="Hellenistic and Early Roman pottery", piw="yes+other", exc="excavated (Hadas 1994)")
a(G, 296, "", "Newe 'Ein Gedi burial cave with eight wooden coffins (ASI 147 site 296)", ftype="burial cave (ruinous)")
a(G, 300, "76/09", "Newe 'Ein Gedi burial cave 76/09 (ASI 147 site 300)", grid="18702/09689", ftype="rock-hewn burial cave", period="Early Roman pottery; ossuaries", piw="yes")
a(G, 300, "76/12", "Newe 'Ein Gedi natural cave used for burial 76/12 (ASI 147 site 300)", grid="18701/09612", ftype="natural cave used for burial",
  period="Early Roman pottery", piw="yes")
a(G, 331, "", "Nahal Avishay natural cave (ASI 147 site 331)", n_open=1, open_basis="stated (its opening, narrowed by a wall)",
  period="Early Bronze, Late Roman and Byzantine pottery", piw="no")
a(G, 365, "", "Nahal Hever cave with an internal wall (ASI 147 site 365)")
for sub in ("a", "b", "c", "d"):
    a(G, 377, sub, f"Ramat Hever small cave {sub} (ASI 147 site 377)", period="Ottoman pottery (site)", piw="no")
a(G, 412, "", "Nahal Hever cave with an internal sloping terrace (ASI 147 site 412)", grid="18199/09365", period="Roman, Byzantine, Ottoman pottery (site)",
  piw="partly", notes="Walls built inside it form a sloping terrace (inside the cave, not at the mouth: C2t not coded); meagre building remains in front.")
a(G, 413, "", "Gavei Hever two-chamber cave (ASI 147 site 413)", notes="Chambers 5 x 5 and c. 6 x 12 m; a 4 m tunnel.")
a(G, 414, "", "Nahal Hever karstic cave (ASI 147 site 414)", period="Chalcolithic/EB, Iron, Roman pottery", piw="partly")
a(G, 415, "1", "Nahal Hever cave with two halls (ASI 147 site 415)", n_open=1, open_basis="singular description (the cave opening leads to a hall)",
  period="Roman pottery", piw="partly", notes="Remains of construction in front of the cave.")
a(G, 415, "2", "Nahal Hever cave with a walled front (ASI 147 site 415)", grid="18120/09345", period="Roman and Byzantine pottery", piw="partly",
  notes="Its front is blocked by a wall with two windows (openings in a built wall: n_openings not coded).")
a(G, 417, "", "Cave of Horror, Nahal Hever (ASI 147 site 417)", period="Bar Kokhba Revolt finds: coins, glass, papyri, a scroll, skeletons", piw="yes",
  exc="excavated (Aharoni 1962)", notes="c. 65 m deep, south bank of Nahal Hever.")
a(G, 429, "", "Cave of the Letters, Nahal Hever (ASI 147 site 429)", period="Bar Kokhba Revolt finds and archives", piw="yes",
  exc="excavated (Aharoni 1961; Yadin 1961-62)", notes="Three halls, c. 150 m long, upper cliff of the N bank.")
for s, what in ((416, "Roman siege camp B above the Cave of Horror"), (418, "charcoal kiln"), (419, "graves"), (420, "campsite and kilns"), (421, "campsite"),
                (422, "building and stone circle"), (423, "campsite"), (424, "campsite"), (425, "campsite"), (426, "sherd scatter and cairn"),
                (427, "Roman army camp A above the Cave of the Letters"), (428, "campsite"), (437, "stone circle"), (442, "campsite"), (443, "granary"),
                (444, "graves"), (445, "campsites")):
    x(G, s, what, "not a cave (the site name refers to a nearby cave)")
X(EXCL, "ASI:147-300-76/13", num="ASI 147 site 300, unit 76/13", src="ASI Map of 'Ein Gedi (147), site 300", ftype="tomb, a single rock-hewn chamber",
  reason="not a cave by the source's type word (tomb)", grid="18705/09695", read=T)

# ---------------------------------------------------------------- 109/4 Wadi Qelt
for s, la, lo in ((7, 31.84910, 35.41985), (8, 31.84415, 35.41191), (13, 31.84153, 35.35010), (23, 31.82755, 35.34691), (29, 31.82394, 35.35060),
                  (31, 31.81762, 35.35693), (43, 31.81627, 35.35904), (63, 31.80588, 35.37223), (104, 31.77840, 35.34842), (105, 31.77343, 35.35475),
                  (107, 31.77925, 35.38759), (108, 31.77925, 35.38802), (110, 31.77654, 35.39223), (111, 31.77609, 35.39329), (112, 31.77609, 35.39435),
                  (114, 31.76580, 35.32518)):
    pt("109/4", s, la, lo)
Q = "109/4"
CHOZ = dict(period="Byzantine pottery (site); monastic cells, some inhabited into the 20th c.", piw="no",
            plan="plans and figures cited in the record (not online)")
CELLS = {
    1: dict(open_basis="unknown: the front is blocked by a built wall with windows and an opening fixed in it (openings in a built wall)",
            notes="c. 400 m E of St George's; 3.5 x 10 m; reached by a ladder; cistern in the eastern wall."),
    2: dict(n_open=2, open_basis="stated: 'the cell has two openings'; the western one is blocked by a built wall",
            notes="Westernmost cell of the laura; floor on several levels. The second opening is not located beyond 'western', so the northern member is undetermined."),
    3: dict(notes="Plastered floor, partly mosaic; a small fenced plot (vegetable garden) in front, 3.5 x 5 m (not a terrace word)."),
    4: dict(n_open=1, open_basis="singular description (its opening is arched)", terrace="yes",
            terrace_basis="a built open surface (1.6 x 4.0 m) in front of the cell (paraphrase; a built platform)"),
    5: dict(n_open=1, open_basis="singular description (a level opening at 0.4 m)"),
    6: dict(num="Choziba Chapel 6 (cave at the base of the chapel)", ftype="cave at the base of a chapel (complex of buildings)",
            notes="A gate built of stone and two niches; rebuilt 1879."),
    8: dict(n_open=5, open_basis="stated: 'five openings of different sizes'", notes="4 x 15 m; burial use (bones on benches)."),
    9: dict(notes="Curved built facade 3.5 m high with a tall window in the west."),
    10: dict(terrace="yes", terrace_basis="a courtyard reached by a staircase, and a balcony 4 x 5 m in front of the living quarters",
             pillar_kind="modern columns (two W, three E) carrying a corrugated-metal roof over the balcony", pillar_pos="on the balcony",
             pillar_basis="modern roof supports (A9-type phase problem); not coded", other_ids="Patrich 1987 cell No. 16 (stated by the record)",
             notes="Inhabited by the monk Paul in the late 1960s. MERGE of Patrich survey Qilt cave No. 16 (identity stated)."),
    11: dict(terrace="yes", terrace_basis="'utilizes a natural terrace enclosed by stone-built fences'; includes a balcony and garden",
             notes="60 sq m; chapel, living quarters, cistern."),
    12: dict(n_open=1, open_basis="singular description (a tabun near the opening of the cell)"),
    13: dict(notes="Two triangular cells; six niches."),
    15: dict(notes="Exposed and partly destroyed; an oven and two rooms; on the southern bank."),
    16: dict(terrace="yes", terrace_basis="a 3 m terrace or vegetable garden built in front of the cell (paraphrase)"),
}
for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16):
    kw = dict(CHOZ) | dict(CELLS.get(n, {}))
    num = kw.pop("num", f"Choziba Cell {n} (cell in a natural cave)")
    ftype = kw.pop("ftype", "monastic cell built in a natural cave ('the cells were constructed in natural caves')")
    a(Q, 7, f"Cell{n}", num, ftype=ftype, **kw)
a(Q, 7, "Cplx7", "Choziba Complex 7 (stronghold-like complex in the cliff)", ftype="complex of rooms and cisterns in the cliff side (within the cells built in caves)",
  other_ids="Patrich 1987 Complex 13 (stated by the record)", notes="Reached by 34 steps and a ladder; Greek inscription. MERGE of Patrich survey Qilt cave No. 13 (identity stated).",
  **CHOZ)
a(Q, 7, "Cplx14", "Choziba Complex 14 (a series of natural caves; cells A, D-G)", kind="cluster", ftype="series of natural caves adapted for dwelling, ten rooms",
  notes="Eight openings A-H in the facade; cells B and C are separate rows.", **CHOZ)
for c in ("B", "C"):
    a(Q, 7, f"Cplx14{c}", f"Choziba Complex 14, cell {c}", ftype="cell in a natural cave (Complex 14)",
      n_open=2, open_basis="stated: cells B and C 'have two openings'; the western is blocked by a wall with a window",
      notes="Horseshoe-shaped, 3.5 x 3.5 m; south side of Nahal Perat. Only a western opening is located, so the northern member is undetermined.", **CHOZ)
a(Q, 8, "base", "St George's monastery: natural cave at the base of the church", ftype="natural cave (the monastery is built around it)",
  period="active monastery since the Byzantine period", piw="no")
a(Q, 8, "Elijah", "St George's monastery: Church of Elijah inside a cave (upper level)", ftype="cave containing a church", period="monastery (Byzantine onward)", piw="no")
a(Q, 8, "skulls", "St George's monastery: burial cave with dozens of skulls (east of the monastery)", ftype="burial cave", period="monastery (Byzantine onward)", piw="no")
a(Q, 13, "", "'Ein el-Fewwar cells incorporated in natural caves (ASI 109/4 site 13)", kind="cluster", c1="unknown",
  ftype="more than ten cells, built, some incorporated in natural caves", period="Byzantine and Ottoman pottery", piw="no")
DH = dict(period="Roman, Byzantine, medieval, Ottoman pottery (site)", piw="partly")
a(Q, 23, "1", "Damnat el-Hartiya Cave 1", ftype="cave hewn in limestone", n_open=1, open_basis="stated (an opening 3.6 m high, 3.3 m wide)", **DH)
a(Q, 23, "2", "Damnat el-Hartiya Cave 2", n_open=1, open_basis="stated (its opening is 2.5 m high)", **DH)
a(Q, 23, "3", "Damnat el-Hartiya Cave 3", terrace="yes", terrace_basis="a courtyard bounded by a stone fence in front of caves 3 and 4 (paraphrase)",
  notes="1.8 m above the courtyard.", **DH)
a(Q, 23, "4", "Damnat el-Hartiya Cave 4", n_open=1, open_basis="singular description ('the opening faces north')", facings="cave:N", facing_basis="word in text",
  terrace="yes", terrace_basis="a courtyard bounded by a stone fence in front of caves 3 and 4 (paraphrase)", **DH)
a(Q, 23, "5", "Damnat el-Hartiya Cave 5", n_open=1, open_basis="singular description ('the opening faces east')", facings="cave:E", facing_basis="word in text", **DH)
SH = dict(period="three medieval sherds; modern pottery (site)", piw="no")
a(Q, 29, "1", "Sha'ab el-Haseena Cave 1", n_open=1, open_basis="stated (the opening is 4.1 m wide)", notes="Joined to Cave 2 by a corridor.", **SH)
a(Q, 29, "2", "Sha'ab el-Haseena Cave 2", n_open=1, open_basis="stated (the opening is 7.6 m wide)", notes="5 m higher than Cave 1.", **SH)
a(Q, 29, "3", "Sha'ab el-Haseena Cave 3", terrace="yes", terrace_basis="a stone terrace four courses high forms a small courtyard outside the cave (paraphrase)", **SH)
a(Q, 29, "4", "Sha'ab el-Haseena Enclosure 4 (rock shelter with two crannies)", c1="unknown", ftype="'enclosure': a rock shelter with two crannies", **SH)
a(Q, 29, "5", "Sha'ab el-Haseena Enclosure 5", ftype="'enclosure' under a fold of flint layers (called 'the cave' in the text)",
  n_open=1, open_basis="singular description (2.1 m high at the entrance)", notes="A wall enclosing a 9 m corridor outside the cave.", **SH)
a(Q, 31, "", "Ma'ale Adumim (1) natural cave with a walled front (ASI 109/4 site 31)", ftype="natural cave (concrete floor)",
  open_basis="unknown: the opening is closed by a modern wall with six small windows", period="Roman pottery (site); modern Jordanian wall", piw="partly",
  notes="A chimney leads to a closed dome-like cavity. A Herodian palace was excavated c. 50 m NE (Peleg 2005).")
a(Q, 43, "", "caves blocked with stone fences south of Khan el-Hatrura (ASI 109/4 site 43)", kind="cluster", ftype="caves blocked with stone fences, within 50 m S of the khan",
  period="site: Roman (end of the Second Temple period), Byzantine, Crusader, Mamluk, Ottoman; caves undated", piw="")
a(Q, 63, "", "Tabaq Qatif (1) rock-hewn cave (ASI 109/4 site 63)", ftype="rock-hewn cave at the base of a natural cave",
  n_open=1, open_basis="singular description (the part closest to the opening collapsed)", notes="Two rooms, 10 x 15 and 8 x 12 m; partly plastered; in use.")
a(Q, 104, "", "Qubur el-Ma'adara (6) rock-hewn cave (ASI 109/4 site 104)", ftype="rock-hewn cave",
  n_open=1, open_basis="stated (the opening 1.1 x 1.5 m, built and blocked by a wall)",
  notes="Four steps lead to the opening 'fixed in the eastern corner of the cave' (a position in a corner; not coded as a facing).")
a(Q, 105, "", "Qubur el-Ma'adara (7) cave dwelling (ASI 109/4 site 105)", ftype="cave dwelling",
  n_open=1, open_basis="singular description (blocked by a wall with a door)", facings="cave:NW", facing_basis="word in text ('the opening faces northwest')")
a(Q, 107, "church", "Deir Mukallik (St Theoctistus) church cave (ASI 109/4 site 107, part D)", ftype="cave of three levels containing a church",
  n_open=3, open_basis="at least three: the main entrance corridor (Unit 1), 'two openings to the cliff' in the eastern part (one S of Unit 10, one skylight-like at Unit 9); Unit 5 'open to the east'",
  plan="Sion and Riklin 1993 (cited; not read)", period="Byzantine monastery (founded 411 CE); frescoes", piw="no",
  notes="An 'entrance' (Unit 6) to the northern part is also named. A burial cave below and a cave above are separate rows.")
a(Q, 107, "burial", "Deir Mukallik church cave: burial cave on the lower level (ASI 109/4 site 107)", ftype="rock-hewn plastered burial cave",
  n_open=1, open_basis="singular description ('the only source of light is from the entrance')",
  pillar="yes", pillar_kind="a dressed column incorporated in the natural side of the cave", pillar_pos="in the wall facade between the entrance vault and the small chamber",
  pillar_basis="record text (Sion and Riklin 1993, as summarised)", period="human bones; Byzantine monastery context", piw="no")
a(Q, 107, "upper", "Deir Mukallik church cave: cave on the upper level (ASI 109/4 site 107)", ftype="natural cave (7.5 x 10.5 m) reached by a chimney from Unit 2",
  period="Byzantine monastery context", piw="no")
a(Q, 108, "", "Deir Mukallik Cave (ASI 109/4 site 108)", ftype="cave", other_ids="Patrich: the anchorite cave of Sabas (record cites Patrich 1989: 8-9)",
  notes="North bank of Nahal Og above a 10 m cliff; beam sockets. ESI 6 p. 68 puts Patrich's proposed Sabas cave (Nahal Og Cave 1) on the south bank west of the monastery: same identification, bank discrepancy; flagged, not merged.")
a(Q, 110, "", "Nahal Og (13) natural cave (ASI 109/4 site 110)", n_open=1, open_basis="stated (a circular opening 4 m high)", notes="18 m long; upper part of the southern cliff.")
a(Q, 111, "", "Nahal Og (14) natural cave (ASI 109/4 site 111)", n_open=1, open_basis="singular description (a wall built in the cave opening)",
  notes="Reached by a natural cranny 18 m long.")
a(Q, 112, "", "Nahal Og (15) natural cave (ASI 109/4 site 112)", n_open=1, open_basis="stated (an entrance 20 m long and 8 m wide)",
  notes="A retaining wall in the SE corner of the entrance; approachable only from the east.")
a(Q, 114, "", "Zahr Shamis (2) rock-hewn cave (ASI 109/4 site 114)", ftype="rock-hewn cave with a rectangular facade", period="Roman and Byzantine pottery", piw="partly",
  notes="Hewn in the western side of a small ravine (no facing word).")
x(Q, 84, "cisterns; caves named in passing ('the slope above the caves')", "caves mentioned only in passing (no count or description)")

# ---------------------------------------------------------------- 83/12 Wadi el-Makokh (Benjamin survey numbers in brackets)
for s, la, lo in ((6, 31.89521, 35.32323), (11, 31.91596, 35.32114), (20, 31.91414, 35.33382), (24, 31.91685, 35.33065), (35, 31.93850, 35.32857),
                  (42, 31.89926, 35.34015), (49, 31.93126, 35.34653), (57, 31.91953, 35.35603), (69, 31.92358, 35.36450), (70, 31.92629, 35.36027),
                  (76, 31.90913, 35.37822)):
    pt("83/12", s, la, lo)
M = "83/12"
KD = dict(period="site: Chalcolithic/EB, Iron II, Roman, Byzantine (majority), medieval, Ottoman", piw="partly")
a(M, 6, "church", "Khallat ed-Dinnabiya laura: church in a large cave [327]", ftype="large cave containing a church (laura)", **KD)
a(M, 6, "caves", "Khallat ed-Dinnabiya laura: caves with rock-cut windows [327]", kind="cluster", ftype="caves with rock-cut windows, niches, crosses, benches and built walls", **KD)
a(M, 11, "", "cave with rock-cut niches [332]", period="Byzantine, Ottoman (eight sherds)", piw="no")
a(M, 20, "", "el-Munya rock-cut cave [341]", ftype="rock-cut cave (part of a farmhouse site)", period="site: MB, Iron II, Byzantine, Early Islamic, medieval, Ottoman", piw="no")
a(M, 24, "", "cave with remains of building activity [345]", period="medieval and Ottoman single sherds", piw="no")
a(M, 35, "", "rock-cut dwelling cave [356]", period="no identifiable sherds", piw="")
a(M, 42, "", "natural cave with traces of plaster [363]", period="site: Iron II (87%), Hellenistic, Roman, Byzantine, Ottoman", piw="partly")
a(M, 49, "", "'Alali el-Benat anchorite cave [370]", ftype="anchorite cave", period="Byzantine sherds", piw="no")
a(M, 57, "", "cave with two entrances [378]", n_open=2, open_basis="stated: 'cave with two entrances'",
  period="1968 survey: Iron II, one Hellenistic, two Roman, two Ottoman sherds", piw="partly",
  notes="No positions, facings, pillar or terrace are given (the record is one line).")
a(M, 69, "", "complex of caves [390]", kind="cluster", period="1968 survey: a few Roman sherds", piw="partly")
a(M, 70, "", "cave with pillars, vaults and natural niches [391]", pillar="yes", pillar_kind="'pillars' (kind not stated)", pillar_pos="not stated",
  pillar_basis="record text: 'Cave with pillars, vaults and natural niches; built stairs'", period="1968 survey: a rope-decorated sherd; one Iron II sherd", piw="no")
a(M, 76, "", "cave at a building site [397]", period="site: Iron II; Byzantine(?)", piw="no")

# ---------------------------------------------------------------- 109/7 Deir Mar Saba
for s, la, lo in ((17, 31.74726, 35.36949), (35, 31.74153, 35.40589), (63, 31.72473, 35.35995), (70, 31.71877, 35.36522), (89, 31.70986, 35.35149),
                  (96, 31.70582, 35.33028), (98, 31.71015, 35.33145)):
    pt("109/7", s, la, lo)
S = "109/7"
a(S, 17, "C8", "Laura of Jeremias: wide cave above Complex 8 (ASI 109/7 site 17)", ftype="wide cave (2 m deep)", period="Byzantine laura (founded 531 CE)", piw="no")
a(S, 17, "C9", "Laura of Jeremias: cave near Cell 9 (ASI 109/7 site 17)", ftype="cave (store-space?)", n_open=1,
  open_basis="singular description (at the cave entrance, 1.8 m high, scanty remains of wall)", period="Byzantine laura", piw="no")
a(S, 17, "C10", "Laura of Jeremias: cave beside Cell 10 (ASI 109/7 site 17)", ftype="cave closed by a well-preserved wall",
  open_basis="unknown: closed by a built wall with an entrance and a low window",
  terrace="yes", terrace_basis="'small stone-built terrace (20 sq m) at edge of ledge' beside the cell and cave (position relative to the cave mouth not exact)",
  period="Byzantine laura", piw="no")
a(S, 35, "", "Magharat Abu Tabaq (reservoir cave of the Iron Age fortress)", ftype="deep cave used as the fortress reservoir",
  n_open=1, open_basis="stated (steps descend from the cave opening, 4 m wide, 2.5 m high; ashlar jambs flank the entrance)",
  period="site: Iron IIb-c (majority), Hellenistic, Roman, Byzantine (scanty)", piw="partly", notes="Cut into the N slope of the hill; c. 35 m deep.")
SP = dict(period="Monastery of the Cave (Spelaion), founded 508 CE; Byzantine", piw="no")
a(S, 63, "Sabas", "'Cave of Sabas', Monastery of the Cave (Spelaion), Bir el-Qattar", ftype="large cave converted into a chapel",
  n_open=2, open_basis="stated: its opening (5.5 m wide, with a parapet on a retaining wall) and a steep rock-cut tunnel entered from the cliff face 4 m below the cave floor",
  pillar_kind="a stucco-moulded Corinthian capital on the rock face near the lower tunnel entrance (decoration, not a standing column)",
  pillar_basis="not coded (no pillar or column stands in the cave)",
  north_case="", notes="10 m deep, 4 m wide; N cliffs of Nahal Sekhakha. The two openings are one above the other (vertical), so the northern member is undetermined.", **SP)
a(S, 63, "dwelling", "Spelaion: dwelling cave under Bir el-Qattar", ftype="dwelling cave (3.2 x 7.4 m)", **SP)
a(S, 63, "Ecave", "Spelaion: small east cave closed off by a wall", ftype="small cave (2.2 m deep, 3.6 m wide)", **SP)
a(S, 63, "Lres", "Spelaion: cave holding the L-shaped reservoir", ftype="cave containing a reservoir (3.2 x 10 m)", **SP)
a(S, 63, "tower", "Spelaion: natural cave holding the cistern under the tower", ftype="natural cave with a cistern built inside", **SP)
a(S, 63, "Sres", "Spelaion: Byzantine reservoir in a cave south of the monastery", grid="18418/12577", ftype="cave closed off by two walls, used as a reservoir", **SP)
a(S, 70, "", "Hyrcania: oval Byzantine burial cave with frescoes", ftype="burial cave (eight cists; frescoed hermits)", period="Byzantine (frescoes 6th-12th c.)", piw="no")
a(S, 89, "", "Wadi el-Makari: two clusters of caves and rock shelters", kind="cluster", c1="unknown", ftype="caves and rock shelters (Bedouin sheepfolds)",
  period="site: Iron II, Roman, Mamluk", piw="partly")
a(S, 96, "", "Nahal Qidron (Mar Saba road): reservoir in a cave", ftype="cave holding a stone-lined plastered reservoir, its opening closed by a thick wall")
ML = dict(period="Great Laura of Sabas (483 CE) and later", piw="no")
LAURA = [
    ("7", "18131/12426", "Complex 7: anchorite cell (rock shelter with a wide opening; typed 'natural cave prepared for habitation')", dict(c1="unknown", grid_basis="approx. 30 m N of Complex 8")),
    ("8", "18132/12423", "Complex 8: natural cave on the upper level", dict(notes="Wide opening; lower structure on a narrow terrace below (not coded: the terrace is on the lower level, not at the cave mouth).")),
    ("14", "18150/12410", "Complex 14: cave fronted by a dwelling structure", dict(n_open=1, open_basis="stated (cave opening 3 m wide)")),
    ("19", "", "Complex 19: wide-mouthed cave above the complex", dict(n_open=1, open_basis="singular description (wide-mouthed)")),
    ("24L", "18160/12388", "Complex 24: large lower cave (grain store)", dict(n_open=1, open_basis="singular description (opening blocked by a wall)")),
    ("24U", "18160/12388", "Complex 24: small cave on the upper level", {}),
    ("26", "", "Complex 26: cave closed off by a wall (Bedouin store)", {}),
    ("27", "18156/12384", "Complex 27: cave on the fifth level behind the chapel", dict(n_open=1, open_basis="singular description (cave entrance closed off by a wall)",
        pillar="yes", pillar_kind="built supportive pillar (0.45 m wide) in the later raising of the blocking wall", pillar_pos="at the cave entrance",
        pillar_basis="record text; later phase (A9-type caution)")),
    ("31", "18150/12360", "Complex 31: Theoktistos ('God-made') church inside a cave, Mar Saba monastery", {}),
    ("32N", "18161/12376", "Complex 32: northern cell in a natural cave", {}),
    ("32S", "18161/12376", "Complex 32: southern cell in a natural cave", {}),
    ("33N", "18164/12373", "Complex 33: northern cave (chapel)", dict(notes="Closed by a wall of small stones; entrance threshold in situ; mosaic.")),
    ("33C", "18164/12373", "Complex 33: central cave (dwelling)", dict(n_open=1, open_basis="stated (entrance 4.3 m wide, 1.7 m high)")),
    ("33S", "18164/12373", "Complex 33: third cave (dwelling)", {}),
    ("34L", "18149/12352", "Complex 34: dwelling cave on the lower level", dict(open_basis="unknown: an entrance in the wall closing the cave from the E, and windows",
        notes="Three square pillars linked by arches support the wall closing the upper level (outside the overhang; not coded as in-cave pillars).")),
    ("34U", "18149/12352", "Complex 34: cave on the upper level closed by a wall with windows", {}),
    ("35", "18149/12351", "Complex 35: store-space in a natural cave beside the Hesychasterion of Sabas", {}),
    ("37", "18157/12350", "Complex 37: 'Cave of St Sabas'", dict(open_basis="unknown: its (widened) opening, a former upper opening now closed by a grill, and access from a lower cave through the floor",
        notes="In a vertical cleft in the E cliffs; prayer niche in the E of the cave.")),
    ("37lower", "18157/12350", "Complex 37: lower cave below the 'Cave of St Sabas'", dict(n_open=1, open_basis="singular description (closed by a cement wall with a metal door)")),
    ("39", "18139/12338", "Complex 39: 'Cave of Xenophon'", dict(terrace="yes", terrace_basis="an open forecourt (1.5 x 5.5 m) and an antechamber facing the cave, with a courtyard to N, on a shelf",
        notes="On the W cliffs; 20 m above the wadi bed.")),
    ("43", "18156/12333", "Complex 43: 'Complex of Johannes, son of Xenophon' (typed cave plus cell on a shelf)", {}),
    ("45", "18150/12328", "Complex 45: 'Arcadius' Tower' (complex in a wide cave)", {}),
    ("48", "18158/12325", "Complex 48: cave with a dwelling cell, near a rock pillar", dict(
        pillar="yes", pillar_kind="rock pillar", pillar_pos="at the cave opening: the entry passage runs beside it and two walls west of it close off the rest of the opening",
        pillar_basis="record text ('passageway ... near rock pillar'; 'two walls to W of pillar close off cave opening')",
        open_basis="unknown: an entry passage by the pillar; a window(?) in the N wall and an entrance(?) in the W wall of the closing walls (hedged)",
        notes="High in the SW cliffs of Nahal Qidron, 250 m SE of Complex 45; a tower and a constructed space (antechamber or verandah?) front the cave (no terrace word).")),
]
for sub, g, num, extra in LAURA:
    extra = dict(extra)
    extra.pop("grid_basis", None)
    kw = dict(ML) | extra
    a(S, 98, f"C{sub}", f"Mar Saba Great Laura {num}", grid=g, ftype=kw.pop("ftype", "cave prepared for habitation (laura complex)"), **kw)
X(EXCL, "ASI:109/7-98-C19group", num="Mar Saba Great Laura Complex 19: 'remains in caves'", src="ASI Map of Deir Mar Saba (109/7), site 98",
  ftype="caves named in passing", reason="caves mentioned only in passing (no count or description)", exposure="exposed-repo", read=T)
for s, what in ((2, "storage caves of the Jahlin Bedouin named in passing"), (58, "Bedouin storage caves to N named in passing"),
                (62, "aqueduct wall closing in a natural cave (named in passing)")):
    x(S, s, what, "caves mentioned only in passing (no count or description)")
