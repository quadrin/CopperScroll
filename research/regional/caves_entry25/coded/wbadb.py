"""WBADB rows added under PLAN.md 4.2 (S10): cave rows inside the box that cite no inventoried source.

Workbook: WBADB_data1.xlsx from https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx, SHA-256
3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b (checked 2026-10-11 05:13:34Z; not committed).
Selection: scripts/intake/wbadb_extract.py (461 cave-word rows in the box; 412 cite an inventoried source and serve
as crosswalks only; 49 cite none and were read by hand 05:14Z onward). X/Y: Old Israel Grid metres (EPSG:28191).
Precision: WBADB X/Y are often rounded to 50 or 100 m; precision is set to half the rounding unit (nominal).
Rows citing Bar-Adon 1989 (S7) beyond its Twin Cave chapter (hermits' caves in Wadi Murrar, a cave in Wadi Mazin,
caves west of 'Ein et-Turabe) are not added (PLAN 4.2), which leaves a coverage gap noted in the README.
The two sheets record some sites twice (Surveyed and Excavations); such pairs are one row here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

ROWS, EXCL = [], []
MERGE = {}
T = "2026-10-11T05:14:00Z"
SRC = "WBADB (Greenberg and Keinan 2009), WBADB_data1.xlsx"


def prec(x, y):
    xi, yi = int(x), int(y)
    if xi % 100 == 0 and yi % 100 == 0:
        return 50
    if xi % 50 == 0 and yi % 50 == 0:
        return 25
    return 5


def w(key, sheet_idx, num, x, y, lineage, *, kind="cave", cluster=None, ref="", **kw):
    R(ROWS, f"WB:{key}", num=num, src=f"{SRC}, {sheet_idx}" + (f"; survey ref. {ref}" if ref else ""), lineage=lineage, kind=kind,
      cluster=cluster, grid=f"{int(x):06d}/{int(y):06d}", crs="OIG", prec=prec(x, y), cbasis="WBADB X/Y (Old Israel Grid metres; site point)",
      exposure=kw.pop("exposure", "unexposed-at-freeze"), read=T, **kw)


BA = "Bar-Adon 1968 emergency survey (Bar-Adon 1972), via WBADB"
PE = "Bar-Ilan University / Israel Cave Research Center refuge-cave surveys 2001-2004 (Porat, Eshel), via WBADB"
w("S1798", "Surveyed 1798", "Kh. Umm 'Azbe: caves at a ruin (Bar-Adon 1972 site 32)", 194000, 149700, BA, kind="cluster", ref="Bar-Adon 1972, Site 32",
  ftype="ruin with structural remains and caves", period="Roman, Ottoman (site)", piw="partly")
w("S2298", "Surveyed 2298 and Excavations 323", "Tell el-Jurn: Roman burial cave (Shantur 1972)", 193600, 142400,
  "Shantur 1972 excavation (HA 43), via WBADB", ftype="Roman burial cave near the synagogue (site point of Tell el-Jurn)",
  period="Roman burial cave", piw="partly", exc="excavated (1972, Shantur)", notes="Recorded as 'nearby' to the synagogue; the cave has no point of its own.")
w("S2800", "Surveyed 2800", "deep cave in a fenced area (Dinur and Feig 1993 no. 1)", 180400, 136950, "Benjamin survey, Map of Jerusalem (Dinur and Feig 1993), via WBADB",
  ref="Dinur and Feig 1993: 423, No. 1", period="Iron II, Byzantine, Ottoman (site)", piw="no")
w("S2950", "Surveyed 2950", "cave near ancient terraces (Dinur and Feig 1993 no. 2)", 180100, 135900, "Benjamin survey, Map of Jerusalem (Dinur and Feig 1993), via WBADB",
  ref="Dinur and Feig 1993: 423, No. 2", notes="'Cave nearby' only.")
w("S4216", "Surveyed 4216", "The Christmas Cave (Nahal Qidron)", 189887, 121095, PE, ref="Porat et al. 2007: 233-245",
  period="Chalcolithic; Early and Late Roman; Byzantine; Islamic; coins, Roman pottery, textiles", piw="yes+other",
  exc="excavated by Allegro 1961; surveyed 2001 (L-921)", notes="Discovered by J. M. Allegro in 1960 (WBADB comment).")
w("S4222", "Surveyed 4222", "village with caves (Bar-Adon 1972 site 114)", 191000, 120800, BA, kind="cluster", ref="Bar-Adon 1972, Site 114",
  ftype="houses, caves and paths (a village)", period="Iron Age, Roman-Byzantine", piw="partly")
w("S4225", "Surveyed 4225", "three caves fronted by terraces (Bar-Adon 1972 site 113)", 190700, 120700, BA, kind="cluster", cluster=3, ref="Bar-Adon 1972, Site 113",
  terrace="yes", terrace_basis="'Three caves, fronted by terraces' (covers every member)", period="Iron Age, Roman-Byzantine, Late Byzantine, Islamic", piw="partly")
w("S4312", "Surveyed 4312", "Cave 751 (Nahal Qidron)", 190381, 118730, PE, ref="Porat et al. 2007: 252", period="Roman pottery; metal items", piw="partly",
  notes="Previously surveyed by Bar-Adon (No. 2), unpublished.")
w("S4313", "Surveyed 4313", "Cave 752 (Nahal Qidron)", 190366, 118719, PE, ref="Porat et al. 2007: 248-250", period="Chalcolithic; Early Roman; two Roman coins", piw="yes+other",
  notes="Previously surveyed by Bar-Adon (No. 3), unpublished.")
w("S4319", "Surveyed 4319", "Cave 753: two adjacent caves (Nahal Qidron)", 190337, 118655, PE, kind="cluster", cluster=2, ref="Porat et al. 2007: 251-252",
  period="Roman pottery; olive pits", piw="partly", notes="Previously surveyed by Bar-Adon (No. 5), unpublished.")
for sub, d in (("1", "cave with a stone threshold and a niche"), ("2", "another cave with three halls and a niche")):
    w(f"S4391-{sub}", "Surveyed 4391", f"Bar-Adon 1972 site 128a: {d}", 189570, 117250, BA, ref="Bar-Adon 1972, Site 128a", period="Iron Age, Roman, Byzantine (site)", piw="partly")
for sub, d in (("1", "large cave with an entrance hall and another hall"), ("2", "another cave")):
    w(f"S4404-{sub}", "Surveyed 4404", f"Bar-Adon 1972 site 128b: {d}", 189480, 117150, BA, ref="Bar-Adon 1972, Site 128b", period="Roman (site)", piw="partly")
w("S4809", "Surveyed 4809", "cave with niches and tunnels (Bar-Adon 1972 site 157)", 185600, 109800, BA, ref="Bar-Adon 1972, Site 157")
w("S4824", "Surveyed 4824", "Kh. el-Kuseir hermit's cave", 180200, 109600, "Hirschfeld survey (Hirschfeld 1985, site 123), via WBADB", ref="Hirschfeld 1985, Site 123",
  ftype="hermit's cave with a chapel", period="Byzantine", piw="no")
w("S4929", "Surveyed 4929", "five caves with sheepfolds in front (Bar-Adon 1972 site 164b)", 187820, 108600, BA, kind="cluster", cluster=5, ref="Bar-Adon 1972, Site 164b",
  period="Roman", piw="partly", exc="dug by Bedouin")
w("S5127", "Surveyed 5127", "The Cave of the Denarius", 187370, 106500, PE, ref="Porat and Eshel 2003: 169-173",
  ftype="Bar Kokhba refuge cave", period="Bar Kokhba denarius; iron javelin", piw="yes")
w("S5247", "Surveyed 5247 and Excavations 904", "The Caves of the Spear (complex of five refuge caves)", 186530, 104950, PE, kind="cluster", cluster=5,
  ref="Porat and Eshel 2003: 165-169", period="Chalcolithic; Hellenistic; Early Roman; Bar Kokhba (coins, arrowheads, spear, lamp)", piw="yes+other",
  exc="excavated (Eshel and Porat)")
w("S5600", "Surveyed 5600", "Cave of Figs (two caves)", 186600, 100900, PE, kind="cluster", cluster=2, ref="Porat et al. 2004: 83-90",
  period="Chalcolithic; Early Roman javelin and Herodian lamp; Late Roman", piw="yes+other")
w("S5710", "Surveyed 5710", "Mugharat Mukhras Delal", 180500, 98600, "unattributed survey record, via WBADB", period="Chalcolithic finds", piw="no")
w("S5741", "Surveyed 5741", "'Cave of the Nails'", 182320, 97610, PE, ref="Porat et al. 2004", period="Bar Kokhba (Rom2); nails", piw="yes")
w("S5751", "Surveyed 5751", "Caves 344 (two caves)", 183020, 97370, PE, kind="cluster", cluster=2, ref="Porat et al. 2006: 115-120",
  period="Early Roman; Chalcolithic, Iron Age, Mamluk", piw="yes+other", exc="surveyed; extensive looting")
w("S5764", "Surveyed 5764", "Four Caves (scroll fragments)", 182860, 97080, PE, kind="cluster", cluster=4, ref="Porat et al. 2004",
  period="Bar Kokhba pottery; Hebrew scroll fragments", piw="yes")
w("S5765", "Surveyed 5765", "Caves 348 (cave complex, four caves surveyed)", 182860, 97080, PE, kind="cluster", cluster=4, ref="Porat et al. 2006: 120-124",
  period="Chalcolithic; Bar Kokhba coins, lamp, scroll fragments", piw="yes+other", exc="surveyed; extensive looting",
  notes="Same point as Surveyed 5764 'Four Caves'; identity not stated (flagged by distance).")
w("E247", "Excavations 247", "cave in Jebel Quruntul (Hameiri and Peleg)", 185800, 149100, "IAA 1993 northern Judean Desert cave survey (permit list), via WBADB",
  notes="No components or bibliography in WBADB; excavators are the Atiqot 41 Region I authors.")
w("E253", "Excavations 253", "Wady Dar el-Jerir: cave with natural pillars and vaults", 184200, 148150, "Bar-Adon 1968 survey team trial excavation, via WBADB",
  pillar="yes", pillar_kind="natural pillars", pillar_pos="not stated", pillar_basis="WBADB components: 'Cave with natural pillars and vaults; stairs'",
  period="Iron II, Roman, Islamic, Ottoman", piw="partly", exc="trial excavation (Bar-Adon survey team)",
  notes="INFERENCE: the same description as ASI 83/12 site 70 [391] ('cave with pillars, vaults and natural niches; built stairs', 1968 survey sherds).")
w("E293", "Excavations 293", "cave in Jebel Quruntul (Hameiri and Peleg)", 189900, 144300, "IAA 1993 northern Judean Desert cave survey (permit list), via WBADB",
  notes="No components or bibliography in WBADB.")
w("E325", "Excavations 325", "'Cave No. 20' (Darawsheh and Solomon)", 190900, 142400, "excavation permit record, via WBADB", notes="No components or bibliography in WBADB.")
w("E333", "Excavations 333", "Avi'or Cave", 190940, 142080, "Eshel 1986 and Eshel and Zissu 1993 excavations, via WBADB",
  period="Bar Kokhba papyri; coins Hellenistic to Mamluk; 38 skeletons", piw="yes+other", exc="excavated (Eshel 1986; Eshel and Zissu 1993)")
w("E519", "Excavations 519", "Wadi Murrar, 'Ein Abu Mahmud caves", 195700, 133500, "Judean Desert Caves survey (Yadin and Patrich; Patrich and Arubas), via WBADB", kind="cluster",
  period="6th-7th c. caves", piw="no", notes="WBADB gives conflicting points (IAA database: Kh. Qumran; HA: 1957/1335).")
w("E572", "Excavations 572", "Mishor Adummim cave with doorjambs and courtyard", 181000, 132100, "Peleg excavation (HA-ESI 112, 2000), via WBADB",
  terrace="yes", terrace_basis="'enclosed courtyard'", period="Early Roman; Mamluk", piw="yes+other", exc="excavated (Peleg)")
w("E680", "Excavations 680", "Cave of the Button (Itah and Kam)", 193330, 130710, "IAA 1993 northern Judean Desert cave survey (permit list), via WBADB",
  period="Roman, Byzantine", piw="partly", notes="No bibliography in WBADB; the name and excavators are those of A41 X/60.")
for k in ("A", "B"):
    w(f"E706-{k}", "Excavations 706", f"Cave {k} of 'Caves A and B' (Itah and Kam)", 193600, 129600, "IAA 1993 northern Judean Desert cave survey (permit list), via WBADB",
      notes="No components or bibliography in WBADB.")
w("E707", "Excavations 707", "'Cave of the Pillar' (Qumran cliff)", 193500, 129600, "excavation record without data (NDA), via WBADB",
  notes="No excavator or bibliography. INFERENCE: probably Jones's 'Cave of the Column' work (the Twin Cave is WBADB Excavations 715 at 193700/129300, c. 360 m away).")
w("E711", "Excavations 711", "Cave 24 in Qumran (Patrich survey numbering)", 193650, 129500, "Hebrew University Judean Desert cave survey (Patrich), via WBADB",
  period="PPNB arrowhead; Roman lamp; Nabataean vessel; textiles", piw="partly", exc="excavated (Patrich 1997)", ref="Patrich 1994b: 90")
w("E755", "Excavations 755", "Cave Q-5 (Hizmi)", 193550, 127650, "excavation permit record, via WBADB")
w("E756", "Excavations 756", "Cave Q-3 (Jones 1978)", 195500, 127600, "V. Jones 1978 excavation, via WBADB",
  notes="Label 'Q-3' as for the Copper Scroll cave in ESI 6 and for X/35 in Atiqot 41 (flagged by label). The printed point lies on the plain east of Qumran (doubtful).")
w("E760", "Excavations 760", "Cave Q-9 (Patrich)", 193650, 127550, "Hebrew University Judean Desert cave survey (Patrich), via WBADB",
  period="Roman pottery", piw="partly", notes="ESI 13 (1995): 64 gives 1935/1310 (not inventoried).")
w("E761", "Excavations 761", "Cave Q-4 (Hizmi and Richardson)", 193450, 127550, "excavation permit record, via WBADB",
  notes="INFERENCE: the point is at Kh. Qumran; perhaps 4Q (not stated).")
w("E762", "Excavations 762", "caves north of Kh. Qumran (Broshi and Eshel 1996)", 193500, 127500, "Broshi and Eshel 1996 excavation, via WBADB", kind="cluster",
  period="Early Roman pottery, coins, nails", piw="yes", exc="excavated (Broshi and Eshel 1996)")
w("E876", "Excavations 876", "Muraba'at cave (permit record)", 185000, 111200, "excavation permit record, via WBADB", notes="No data in WBADB.")
w("E891", "Excavations 891", "Cave A-1 (Nahlieli and Lender)", 185300, 107600, "IAA 1993 cave survey, Region XV excavation, via WBADB",
  period="Roman coins, sword, pottery", piw="partly", notes="Same excavators and point as A41 XV/3 (Index code A1).")
w("E906", "Excavations 906", "Harasim Cave", 186000, 104000, "excavation permit record, via WBADB", notes="No data in WBADB.")
w("E931", "Excavations 931", "'Le'nahem Avdi' Cave", 183350, 97450, "Bar-Adon excavation; Porat et al. 2006, via WBADB",
  period="Chalcolithic, Iron II and Bar Kokhba pottery; seal impression 'Le'nahem Avdi'", piw="yes+other",
  notes="INFERENCE: the seal impression identifies it with ASI 147 site 127 (Nahal Arugot natural cave; seal impression), c. 140 m away; not flagged (no stated identity).")
for idx, what, why in (("Surveyed 5230", "cairns and camp sites", "not a cave (matched 'Cave Research Center')"),
                       ("Surveyed 5255", "rectangular structure", "not a cave (matched 'Cave Research Center')"),
                       ("Excavations 787", "Monastery of the Cave (Spelaion)", "a monastery record; its caves are coded from ASI 109/7 site 63"),
                       ("Excavations 921", "Kh. Muqaddam", "not a cave (comment names the Twin Cave licence)")):
    X(EXCL, "WB:" + idx.replace(" ", ""), num=f"WBADB {idx}", src=SRC, ftype=what, reason=why, read=T)
