"""DJD III (de Vaux 1962, Part I) cliff sites, marl caves and later caves; RB 60 (1953) map points (PLAN.md S1-S3).

All content comes from repository notes read before the freeze (exposure 'exposed-repo'):
research/history/djd3_text_cave_list_extracted.md (DJD III pp. 3-17, 26-34) and
research/history/devaux1952_cave_points/devaux1952_cave_points.csv (RB 60 pl. XX digitised; 1 sigma c. 30 m).
Reed, BASOR 135 (1954) 8-13 (Downloads PDF, SHA-256 d9be5b19...; already read for salvage record S01) adds no cave:
its 39 'caves and crevices' are the same lineage; its 'Cave No. 14 ... a very shallow crevice' matches DJD site 15,
not 14 (= 1Q), a numbering discrepancy noted, not used.
Facing words in DJD III include NE and SE, so every DJD III word is read at 8-point resolution (A4).
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

REPO = Path(__file__).resolve().parents[4]
PTS = {}
with open(REPO / "research/history/devaux1952_cave_points/devaux1952_cave_points.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        PTS[r["point"]] = f"{r['oig_x']}/{r['oig_y']}"

ROWS, EXCL = [], []
# MERGE: rows of this module that are the same cave as a row of another module, by the source's own statement.
MERGE = {"DJD3:19": "A41:XI/19"}

LIN52 = "1952 Qumran Caves Expedition (de Vaux and Reed)"
SRC = "DJD III (de Vaux 1962) pp. 6-13 (repo extraction)"
EXPO = "exposed-repo"
PTNOTE = "RB 60 pl. XX point digitised (devaux1952_cave_points.csv; 1 sigma c. 30 m, c. 60 m at 95%)"
NOPT = "Qumran cliff between Hajar el-Asba and Ras Feshkha (1952 survey band, DJD III p. 4); no digitised point"


def d(num, *, src_pages, n_open=None, open_basis="", facings="", period="", piw="", hab="", notes="", terrace=None,
      terrace_basis="", other_ids="", exc="sounded or excavated in 1952 (method per site not stated, DJD III p. 6)",
      finds="", c1=None, ftype="cave"):
    key = str(num)
    grid = PTS.get(key, "")
    R(ROWS, f"DJD3:{key}", num=f"1952 site {key}", src=f"{SRC}; site {key}, {src_pages}", lineage=LIN52, ftype=ftype,
      grid=grid, prec=30 if grid else None, cbasis=PTNOTE if grid else "", where="" if grid else NOPT,
      n_open=n_open, open_basis=open_basis, facings=facings, facing_basis="word in text" if facings else "",
      res=8, terrace=terrace, terrace_basis=terrace_basis, period=period, piw=piw, exc=exc, finds=finds,
      exposure=EXPO, other_ids=other_ids, c1=c1,
      notes=("; ".join(x for x in (f"habitability: {hab}" if hab else "", notes) if x)))


d(1, src_pages="p. 6", period="Qumran-type sherds", piw="yes", hab="yes", exc="excavated to bedrock (ash 0.75 m to the rock)",
  notes="Large cave, open chamber c. 6 x 5 m, 3.5 m high, plus a lower inner chamber.")
d(3, src_pages="p. 7", period="Qumran-type pottery; flints 'much older'", piw="yes+other", hab="no",
  open_basis="unknown: found through a small low opening that drained seepage; the entrance layout cannot be established",
  exc="surface collection (finds at or just below the surface)")
d(4, src_pages="p. 7", n_open=1, open_basis="singular description (a wide entrance c. 4 x 1.5 m)", facings="cave:S",
  period="mostly Arab sherds; a few possibly Qumran type", piw="partly", hab="doubtful")
d(5, src_pages="p. 7", n_open=1, open_basis="singular description (opening to the E; two storeys)", facings="cave:E",
  period="very few sherds, none certainly Qumran", piw="", hab="no",
  notes="Text: directly above the roof of cave 8 (3Q); no digitised point (the map label 5 is plotted NW of 8, a map-text mismatch).")
d(6, src_pages="p. 7", n_open=1, open_basis="singular description (a wide opening)", facings="cave:S",
  period="Arab; Iron II(?) sherds; nothing of Qumran type", piw="no", hab="yes")
d(7, src_pages="p. 7", n_open=1, open_basis="singular description (opening E)", facings="cave:E",
  period="lid and jar fragments of Qumran type", piw="yes", hab="no", notes="Very small cave, 2 x 1.5 m.")
d(8, src_pages="pp. 7-8, 14-15, 33-34, 201; ESI 6 (1987/88) pp. 68-70, fig. 29 (Patrich 1986 excavation)",
  open_basis="unknown: the original entrance is unknown (ceiling collapsed)", period="Qumran; 'Herodian' lamp (level II); Chalcolithic sherds (ESI 6)",
  piw="yes+other", hab="doubtful", exc="excavated (1952, 12 days); re-excavated April 1986 to the floor (Patrich, ESI 6 pp. 68-69)",
  finds="c. 35 jars, 26 lids, jugs, lamp, texts, the two copper rolls",
  other_ids="3Q; 'Cave Q3' (ESI 6 p. 68, stating it was no. 8 in 1952)",
  notes="The Copper Scroll cave. MERGE of the ESI 6 record (identity stated by ESI 6). A41 p. 180 applies the label 'Q3' to Patrich and Arubas Cave 13 (X/35): label conflict, flagged.")
d(10, src_pages="p. 7", n_open=1, open_basis="singular description (a wide entrance)", period="2 Qumran-type jars", piw="yes", hab="yes")
d(11, src_pages="p. 7", n_open=1, open_basis="singular description (a wide entrance)", facings="cave:SE",
  period="uncertain sherds, nothing of Qumran type", piw="", hab="yes")
d(13, src_pages="p. 8", period="Iron II sherds; nothing of Qumran type", piw="no", hab="yes", notes="Large cave high in the cliff, SW of 12.")
d(14, src_pages="p. 9 (refers to DJD I pp. 8-17)", period="", piw="", other_ids="1Q",
  exc="search for the original entrance outline (1952); excavated 1949 (DJD I, not read)",
  notes="1Q. DJD I, which describes the cave, was not read in this lane.")
d(18, src_pages="p. 9", n_open=1, open_basis="singular description (a large cave opening N)", facings="cave:N",
  period="4 Qumran-type jars", piw="yes", hab="doubtful")
d(19, src_pages="p. 9", facings="cave:NE", open_basis="", period="Qumran", piw="yes", hab="doubtful", other_ids="2Q; A41 XI/19",
  exc="emptied by clandestine digging; pottery from the spoil (1952)",
  notes="Two storeys of chambers or recesses opening NE. MERGED into A41:XI/19 (identity stated by Atiqot 41 p. 195).")
d(20, src_pages="p. 9", n_open=1, open_basis="singular description (cave opening S)", facings="cave:S",
  period="uncertain sherds; nothing of Qumran type", piw="", hab="doubtful", notes="Almost completely filled with debris.")
d(22, src_pages="p. 10", period="base of a Qumran-type jar", piw="yes", hab="no", notes="Very small cave, 1 m wide, 2 m deep.")
d(23, src_pages="p. 10", n_open=1, open_basis="singular description (a wide entrance)", period="Byzantine and Arab sherds", piw="no",
  hab="yes", notes="A low wall built in front of the entrance (not coded as a terrace: no terrace word).")
d(25, src_pages="p. 10", period="few sherds; nothing of Qumran type", piw="", hab="yes", notes="Cave 3 m wide, 2 m high.")
d(26, src_pages="pp. 10, 26", period="Qumran-type jar and bowl", piw="yes", hab="doubtful", other_ids="6Q",
  exc="emptied by Bedouin; spoil sifted (1952)", notes="Small cave at the mouth of the Wadi Qumran gorge, below the aqueduct.")
d(27, src_pages="p. 10", terrace="yes", terrace_basis="'a rectangular porch 4 x 6 m' (word 'porche'; position relative to the mouth not stated)",
  period="Iron II; perhaps Qumran", piw="partly", hab="yes", exc="sounded (earlier Bedouin soundings)")
d(28, src_pages="p. 11", n_open=1, open_basis="singular description (a shaft leads to the chamber)", period="Qumran-type jars and lid", piw="yes",
  hab="no", notes="Above no. 29.")
d(29, src_pages="p. 11", n_open=1, open_basis="singular description (entered by a tunnel 2 m long)", period="Qumran-type jars and lids", piw="yes",
  hab="no", notes="De Vaux's candidate for an anciently violated deposit (p. 34).")
d(31, src_pages="p. 11", n_open=1, open_basis="singular description (a rectangular opening)", period="Qumran-type bowls and jars", piw="yes", hab="yes")
d(32, src_pages="p. 11", n_open=1, open_basis="singular description (a wide low entrance)", facings="cave:E",
  period="Qumran-type jars and lid; Arab sherds", piw="yes+other", hab="doubtful", notes="At the foot of the cliff; ends in a long narrow passage.")
d(33, src_pages="p. 11", n_open=2, open_basis="stated: a wide low opening and a 'window' (fenêtre) to the N",
  facings="m1:E;m2:N", period="a few Roman sherds apparently later than Qumran (perhaps Second Revolt, p. 16)", piw="partly", hab="yes",
  notes="Cube-shaped cave. The window's position relative to the opening is not given, so the northern member is undetermined. 'To the N' is read as a facing (AMENDMENT_1, coding note 1).")
d(34, src_pages="p. 11", period="Roman sherds a little later than Qumran; possibly level III", piw="partly", hab="yes",
  notes="Entered down a slope; connects with a lower cave still used by shepherds.")
d(36, src_pages="p. 12", n_open=1, open_basis="singular description (a large cave opening NE)", facings="cave:NE",
  period="Roman sherds, apparently later than Qumran", piw="partly", hab="yes")
d(37, src_pages="p. 12", terrace="yes", terrace_basis="a platform 10 m N-S x 5 m E-W leads to the great chamber ('plate-forme')",
  period="Qumran-type sherds; Chalcolithic (1953)", piw="yes+other", hab="yes", exc="surface collection in two small side caves",
  notes="'The largest of the caves'; great chamber c. 13 m high; side chambers; a tunnel W to another chamber 18 m deep. Exterior openings not counted.")
d(38, src_pages="p. 12", n_open=1, open_basis="singular description (a high triangular entrance)", period="Roman sherds later than Qumran; Arab",
  piw="partly", hab="yes", notes="W of and above Ain Feshkha.")
d(39, src_pages="p. 12; Reed 1954 p. 13", n_open=1, open_basis="singular description (opening 3 m wide, 2.5 m high)", facings="cave:NE",
  period="Qumran-type jars and lids; Iron II lamp", piw="yes+other", hab="yes", exc="dug earlier by Bedouin; examined 1952",
  notes="Depth 8 m (DJD III; Reed 1954 also gives c. 8 m deep, 3 m wide, 2.5 m high).")
d(40, src_pages="p. 12", period="Qumran-type jar", piw="yes", hab="yes", notes="'Smaller than 39 but similar' (not used to infer openings).")
for k, desc, per, piw, nb in (
        ("A", "a low cave with a low entrance (1956)", "Iron II sherds; Qumran-type sherds", "yes+other", dict(n_open=1, open_basis="singular description (a low entrance)")),
        ("B", "a low cave whose front has collapsed (1956)", "Qumran; Iron II; mostly Chalcolithic", "yes+other", {})):
    R(ROWS, f"DJD3:{k}", num=f"1956 cave {k}", src=f"{SRC}; p. 13", lineage="1956 re-examination of the Qumran cliff (de Vaux)", ftype="cave",
      where="north flank of the ravine that has 3Q on its south flank, a little higher and further east (DJD III p. 13)", res=8,
      period=per, piw=piw, exc="excavated 1956 (A 21-24.3; B 21-22.3)", exposure=EXPO, notes=desc, **nb)

MARL = "1955 Qumran marl-terrace prospection (de Vaux; Hassan Awad's team)"
for k, note in (("7Q", ""), ("8Q", ""), ("9Q", ""), ("10Q", "Yielded only an ostracon (DJD III p. 34 n. 1).")):
    R(ROWS, f"DJD3:{k}", num=k, src=f"DJD III pp. 27-31 (repo extraction: existence and pottery codes only)", lineage=MARL, ftype="cave in the marl terrace",
      where="marl terrace by Kh. Qumran (DJD III p. 27)", res=8, period="Qumran pottery (fig. 6)", piw="yes", exc="excavated 1955", exposure=EXPO,
      notes=("The repository extraction does not record the descriptions of pp. 27-31. " + note).strip())
R(ROWS, "DJD3:oval", num="unfinished oval artificial cave between 4Q and 5Q", src="DJD III p. 27 (repo extraction)", lineage=MARL,
  ftype="unfinished, unused artificial cave", where="marl terrace between 4Q and 5Q (DJD III p. 27)", res=8, period="unused", piw="",
  exc="found 1955", exposure=EXPO)
R(ROWS, "DJD3:5Q", num="5Q", src="DJD III p. 26 (repo extraction: chapter title only)", lineage="1952 (5Q found by de Vaux's team, Sept. 1952; BK)",
  ftype="cave", where="by Kh. Qumran (DJD III ch. II)", res=8, period="Qumran (manuscript cave)", piw="yes", exc="", exposure=EXPO,
  notes="Chapter II was not extracted; only its existence is in the repository.")
R(ROWS, "DJD3:4Q", num="4Q", src="DJD III pp. 4, 32 (named only)", lineage="1952 (found by Bedouin, Sept. 1952)", ftype="cave (marl terrace)",
  where="marl terrace at Kh. Qumran (DJD III p. 4)", res=8, period="Qumran (manuscript cave)", piw="yes", exc="", exposure=EXPO,
  notes="Named only; DJD VI, which describes it, is not an inventoried source.")
R(ROWS, "DJD3:11Q", num="11Q", src="DJD III pp. 4, 32 (named only)", lineage="1956 (found by Bedouin, Jan. 1956)", ftype="cave with a blocked entrance (p. 4)",
  where="Qumran cliff north of 3Q (DJD III p. 13 context)", n_open=1, open_basis="singular description ('a cave with a blocked entrance', p. 4)", res=8,
  period="Qumran (manuscript cave)", piw="yes", exc="", exposure=EXPO, notes="Named only; no description in the inventoried sources.")

for k, t, why in (("2", "pottery deposit under fallen rocks", "not a cave (pottery heap)"), ("9", "rock crevice closed by a dry-stone wall", "not a cave (crevice)"),
                  ("12", "rock shelter c. 5 m wide", "not a cave (rock shelter)"), ("15", "rock hollow open to the N (cleft)", "not a cave (cleft)"),
                  ("16", "expedition camp", "not a find site"), ("17", "very high crevice", "not a cave (crevice)"),
                  ("21", "rock fissure", "not a cave (cleft)"), ("24", "rock shelter", "not a cave (rock shelter)"),
                  ("30", "rock hollow 1 m wide (cleft)", "not a cave (cleft)"), ("35", "ruins of a rectangular building", "not a cave (building)"),
                  ("X-1", "surface find on a path", "not a cave"), ("X-2", "surface find, findspot not recorded", "not a cave")):
    X(EXCL, f"DJD3:{k}", num=f"1952 site {k}", src=f"{SRC}", ftype=t, reason=why, grid=PTS.get(k, ""), exposure=EXPO,
      notes="Patrich and Arubas 1989 p. 44 n. 3 hedge their Cave 13 (= A41 X/35) with 1952 no. 2." if k == "2" else "")
