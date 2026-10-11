"""ESI cave-survey and cave-excavation reports inside the box (PLAN.md S5), and the repository's modelled caves (S7, S8, S14).

S5 scan (title/heading scan of the text layers of ESI 2, 3, 5, 6, 7-8, 9 and 15, owner's Downloads copies; run
2026-10-11 04:58Z). Reports whose title names a cave survey or cave excavation: ESI 2 none in the box; ESI 3 pp. 61-62
'Judean Desert, Secret Passages and Caves' (Patrich, first season: Wadi Suweinit, Ein Fara, Qasr er-Rawabi, all west of
E 180,000, so outside the box); ESI 5 none; ESI 6 pp. 66-70 'Judean Desert, Survey of Caves 1985/1986' (Patrich);
ESI 7-8 pp. 92-95 'Judean Desert, Cave Survey 1986/1987' (Agur, Arobes and Patrich) and p. 117 'Makkuk Cave' (Eshel);
ESI 9 and ESI 15 none in the box. ESI 4 (second season, ESI 4:21) is not in the owner's library (not read).
Reports without a cave title (Hirschfeld's monastery surveys, the Mar Saba map, 'En Gedi map) are outside S5 as frozen.

Facing words: ESI 6 and 7-8 give none for any cave opening (a niche 'facing east' in upper Makkuk Cave 1 is a niche).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

ROWS, EXCL = [], []
MERGE = {}

LINP = "Hebrew University Judean Desert cave survey (Patrich), 1983-1987"
E6 = "ESI 6 (1987/88) pp. 66-70, Patrich, 'Judean Desert, Survey of Caves 1985/1986'"
E78 = "ESI 7-8 (1988/89) pp. 92-95, Agur, Arobes and Patrich, 'Judean Desert, Cave Survey 1986/1987'"
PO = "page-opened-before"
UX = "unexposed-at-freeze"
T6 = "2026-10-11T04:58:36Z"

# --- Wadi Qilt: 20 caves recorded and numbered (ESI 7-8 p. 92), including the Choziba monastic cells.
QILT_WHERE = "Wadi Qilt below St George's monastery (Choziba), mainly the north bank, within c. 2 km east of the monastery (ESI 6 p. 66)"
QILT = {
    1: dict(period="Byzantine pottery; a plastered cistern", piw="no"),
    9: dict(period="Byzantine monastic complex (mosaic near the altar; restored 1897)", piw="no", ftype="cave used as a monastic cell (complex No. 9)"),
    13: dict(period="Byzantine monastic complex; mosaic with a Greek inscription", piw="no", ftype="cave used as a monastic cell (complex No. 13)"),
    14: dict(period="Roman-Byzantine sherds; inhabited by a monk into the 20th century", piw="partly", notes="High in the cliff above the burial complex."),
    16: dict(period="monastic cell inhabited up to modern times", piw="", ftype="cave used as a monastic cell (complex No. 16)"),
    18: dict(period="monastic cell inhabited up to modern times", piw="", ftype="cave used as a monastic cell (complex No. 18)"),
    20: dict(n_open=1, open_basis="singular description (the cave's mouth, enlarged by the collapse of a thin rock wall)",
             period="jug fragments; an almost intact round Roman lamp of the 2nd c. CE", piw="partly",
             notes="c. 8 x 2.5 m; plastered cistern at the west end; a trimmed forked tree trunk below the mouth (an ancient ladder?)."),
}
for n in range(1, 21):
    kw = dict(QILT.get(n, {}))
    ftype = kw.pop("ftype", "cave")
    notes = kw.pop("notes", "")
    R(ROWS, f"PAT:Qilt-{n}", num=f"Wadi Qilt cave No. {n} (Patrich survey)", src=f"{E6} p. 66; {E78} p. 92", lineage=LINP, ftype=ftype,
      where=QILT_WHERE, exc="surveyed", exposure=PO if n in (9, 13, 16, 18) else UX, read=T6,
      notes=("Of the 20 numbered caves, five are Roman-period and the rest monastic retreats (ESI 7-8 p. 92). " + notes).strip(), **kw)

# --- Upper Wadi Makkuk: eight caves (ESI 6 p. 67).
UM_WHERE = "upper and eastern Wadi Makkuk, away from the Khallat ed-Danabiya monastery (ESI 6 p. 67)"
UM = {
    1: dict(period="Greek inscription and cross; Arabic inscription", piw="", notes="Easternmost; three levels. An inscribed niche faces east (a niche, not the cave mouth)."),
    5: dict(num="upper Wadi Makkuk cave No. 5 'Cave of the Spring'", n_open=1, open_basis="singular description (a fissure whose opening is blocked by a masonry wall c. 2 m high)",
            period="a large quantity of Roman sherds", piw="partly", notes="A plastered reservoir behind the wall collects a small spring; traces of digging and sieving."),
    6: dict(period="Roman jar fragment; rock drawings of c. ten gazelles", piw="partly"),
    7: dict(period="", piw="", notes="The most developed: chambers on several levels, once closed by stone walls."),
}
for n in range(1, 9):
    kw = dict(UM.get(n, {}))
    num = kw.pop("num", f"upper Wadi Makkuk cave No. {n} (Patrich survey)")
    kw.setdefault("notes", "Some of the eight caves gave Roman sherds (unassigned).")
    R(ROWS, f"PAT:UMakkuk-{n}", num=num, src=f"{E6} p. 67", lineage=LINP, where=UM_WHERE, exc="surveyed", exposure=UX, read=T6, **kw)

# --- Lower Wadi Makkuk: six caves (ESI 6 p. 67); five excavated in 1987 (ESI 7-8 pp. 93-95).
LM_WHERE = "lower Wadi Makkuk (ESI 6 p. 67; ESI 7-8 p. 93)"
LM = {
    1: dict(src=f"{E6} p. 67; {E78} pp. 93-94", n_open=1, open_basis="singular description (a skimpy wall closed the entrance)",
            pillar_kind="a 'prominent rock column' on the ledge in front of the cave", pillar_pos="on the natural ledge in front of the cave, outside it",
            pillar_basis="ESI 7-8 p. 93; outside the cave, so not coded under PLAN 4.3 (C2p unknown); see AMENDMENT_1 near misses",
            period="Late Chalcolithic burials (at least 35 persons); Roman finds from the front part and the lower ledge", piw="partly",
            exc="excavated (1987); plundered", finds="human remains, trepanned skulls, beads, textiles, ropes",
            notes="c. 6 m deep; two natural burial tunnels descend from its right side; reached from the west along a steep slide. "
                  "A niche c. 10 m away held a Roman-type sandal (late 1st or early 2nd c. CE). INFERENCE: resembles A41 III/3 (natural stone pillar at the upper entrance; Chalcolithic; human bones; 'probably excavated earlier by Patrich and Arubas'); no identity is stated, so no flag."),
    2: dict(src=f"{E6} p. 67", period="a silver Islamic coin at its foot", piw="no"),
    3: dict(src=f"{E6} p. 67; {E78} p. 94", period="Chalcolithic secondary burials in baskets; a few EB sherds; a few Roman sherds in the front", piw="partly",
            exc="excavated (1987); plundered", notes="Reached by a natural chimney and a 30 m rope ladder via a large cave sharing a common ledge ('balcony') with it; two branches. "
                                                     "A natural ledge is not a terrace (PLAN 4.3). INFERENCE: resembles A41 III/7 (access by ropes or a chimney; ledge 8 x 6 m)."),
    4: dict(src=f"{E6} p. 67", period="Chalcolithic stone macehead fragment", piw="no"),
    5: dict(src=f"{E78} p. 94", period="numerous Roman sherds and broken stone vessels", piw="partly", exc="excavated (1987)",
            notes="Broad and high-ceilinged; a narrowing tunnel at a high level in its depths."),
    6: dict(src=f"{E6} p. 67; {E78} pp. 94-95", period="Chalcolithic copper implements, baskets, mat, ropes, axe", piw="no", exc="excavated (1987)",
            notes="Abuts the left side of Cave 5, in a 25 m cliff; c. 7 x 5 m."),
}
for n in range(1, 7):
    kw = dict(LM[n])
    src = kw.pop("src")
    kw.setdefault("exc", "surveyed")
    R(ROWS, f"PAT:LMakkuk-{n}", num=f"lower Wadi Makkuk cave No. {n} (Patrich survey)", src=src, lineage=LINP, where=LM_WHERE,
      exposure=UX, read=T6, **kw)
X(EXCL, "PAT:LMakkuk-niche", num="niche next to lower Wadi Makkuk Cave 1", src=f"{E78} p. 95", ftype="niche, entrance blocked by a masonry wall; Roman-type sandal",
  reason="not a cave (niche)", exposure=UX, read=T6, notes="The authors allow that it may once have been part of a cave.")

# --- Na'aran - Jericho cliff: 30 caves identified and numbered (ESI 7-8 p. 93).
NJ_WHERE = "the c. 3.5 km cliff between Na'aran and Jericho, from Wadi Makkuk to the Qarantal monastery (ESI 7-8 p. 92)"
for n in range(1, 31):
    extra = {}
    if n == 22:
        extra = dict(period="a gilded clay disk with a lily; a few Late Byzantine or Early Arab sherds", piw="no")
    R(ROWS, f"PAT:NJ-{n}", num=f"Na'aran-Jericho cliff cave No. {n} (Patrich survey)", src=f"{E78} p. 93", lineage=LINP, where=NJ_WHERE,
      exc="surveyed", exposure=UX, read=T6,
      notes="The cliff overlaps Atiqot 41 Regions IV-VIII; no crosswalk to the 1993 numbers is published, so overlap cannot be resolved (counted in N_rows and N_min).",
      **extra)

# --- Nahal Og (Wadi Mukallik): one cave recorded with rock-cutting (ESI 6 p. 68, fig. 28).
R(ROWS, "PAT:Og-1", num="Nahal Og (Wadi Mukallik) Cave No. 1", src=f"{E6} p. 68, fig. 28 (plan and section)", lineage=LINP,
  ftype="cave with rock-cutting and levelling", where="south bank of Nahal Og, west of the Deir Mukallik (St Theoktistus) monastery (ESI 6 p. 68)",
  plan="ESI 6 fig. 28 (plan and section; not measured: PLAN 4.3 triage)", period="Byzantine sherds at its foot; a Roman-period wooden comb",
  piw="partly", exc="surveyed", exposure=UX, read=T6, notes="Proposed as St Sabas's retreat of 469-474 CE.")

for k, where, why in (("Wuheita", "Wadi Wuheita", "locality not placeable inside the box from the record"),
                      ("Auja", "Wadi el-Auja (six caves)", "Wadi el-Auja lies at or north of the box's northern edge (N 150,000); not placeable inside"),
                      ("Shiban", "Wadi Shiban (rock-cut caves on both banks)", "locality not placeable inside the box from the record")):
    X(EXCL, f"PAT:{k}", num=f"Patrich survey caves, {where}", src=f"{E6} p. 67", ftype="caves", reason=why, exposure=UX, read=T6)

# --- Makkuk Cave (ESI 7-8 p. 117).
R(ROWS, "ESI78:MakkukCave", num="Makkuk Cave (SPNI Cave Research Center 1984)", src="ESI 7-8 (1988/89) p. 117, Eshel, 'Makkuk Cave'",
  lineage="SPNI Cave Research Center discovery (1984); Eshel sounding", ftype="karst cave, c. 520 m long", grid="1825/1448",
  period="scanty Chalcolithic; MB I; especially Bar Kokhba period (store jars, glass juglet, Roman lamp)", piw="yes+other",
  exc="sounded (H. Eshel); plundered (front part)", exposure=UX, read=T6,
  notes="North bank of Wadi Makkuk; several large halls in the front part. Exterior openings not described.")

# --- The repository's modelled caves not otherwise coded (S7, S8, S14). IV/11 and IV/17 are coded in a41.py.
R(ROWS, "REPO:TwinCave", num="Twin Cave (Me'arat ha-Te'omim; Jones's 'Cave of the Column')",
  src="Bar-Adon, Atiqot Hebrew Series 9 (1989) ch. B pp. [15]-17, fig. B1 (via registration/entry25_twin_cave_features_2026-10-01.json); ESI 6 pp. 69-70 (fourth season 1986)",
  lineage="Bar-Adon / Jones excavations 1971-1986", ftype="cave (two units)", grid="1937/1293", cbasis="published cave locator (printed grid)",
  n_open=2, open_basis="stated: two openings (mouths) of a northern and a southern unit", facings="m_north:E;m_south:E",
  facing_basis="word in text: both mouths east, toward the Dead Sea (Bar-Adon, via the repository)", res=4,
  pillar="yes", pillar_kind="thick rock pillar (natural character is a source-reader inference)", pillar_pos="separating the northern and southern units",
  pillar_basis="Bar-Adon p. 16 (via the repository)", north="decided", north_basis="the source names northern and southern units with their openings",
  plan="none (exterior photograph only, fig. B1)",
  period="1st c. BCE-1st c. CE parallels; a Bar Kokhba-era comparative vessel date; mixed-period pottery including Roman", piw="yes+other",
  exc="excavated (seasons 1971, 1977, 1982, 1986; the 1986 season found nothing indicative)", exposure="exposed-repo",
  other_ids="Bar-Adon 'Twin Cave'; Jones 'Cave of the Column'; WBADB rec. 709 (site centre 193700/129300, via repo)",
  notes="One of the four modelled caves; every record is exposed (exploratory, A10). Browning 1996 p. 76: the two openings do not reach the same cavity (via salvage record S15). "
        "A41 X/47 ('two caves dug by Vendyl Jones', c. 470 m away at its printed grid) is not merged (no stated identity).")
R(ROWS, "REPO:JonesNorth", num="Jones's 'North Entrance to the Cave of the Column' (1992 dig)",
  src="salvage record S14 (Browning, BA 59 (1996) p. 77; Amar, DSD 5 (1998) pp. 1-3; via repo)", lineage="V. Jones, unlicensed 1992 dig (CLAIM)",
  ftype="a smaller cave slightly north of the Cave of the Column, at about the same level (CLAIM)",
  where="slightly north of the Twin Cave / Cave of the Column, Qumran cliff (Browning p. 77, via repo)",
  period="claimed Temple incense (red material) in a rock-lined pit; no dated finds published", piw="",
  exc="dug without a licence (1992); stopped by the Antiquities Authority", exposure="exposed-repo",
  notes="CLAIM row: no plan, opening count or facing is published; identified by Jones from a reading of 3Q15 VI 3-5. One of the four modelled caves.")
