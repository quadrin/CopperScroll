"""ʿAtiqot 41 Part 1 (Hebrew, IAA 2002): cave entries, coded by hand (PLAN.md section 4).

Source files and hashes: ../intake/atiqot41_intake.json. Printed pages: for each article the PDF page
index (cover = PDF p. 1) is mapped to the printed page by the page numbers printed on the pages.
Text is paraphrased by this worker; quotations are 12 words or fewer. Grid references are as printed (Old Israel Grid,
10 m units for 5+5 digits, 100 m units for 4+4 digits).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

ROWS, EXCL = [], []
LIN = "IAA 1993 northern Judean Desert cave survey (CNJD), Atiqot 41"

# ------------------------------------------------------------------ Region I
# Peleg and Hameiri, Region I (Wadi el-Makkuk and Wadi ed-Daliya), printed pp. 2-6 (PDF p = printed p).
# 19 caves surveyed (p. 3). Report uses only cardinal facing words (4-point). First read 04:09:41Z.
S1 = "A41 Region I (Peleg and Hameiri)"
T1 = "2026-10-11T04:09:41Z"
R(ROWS, "A41:I/1", num="1/I", src=f"{S1} p. 3", lineage=LIN, grid="18900/14590", cbasis="printed grid (shared by I/1-2)",
  period="no finds", exc="surveyed", read=T1, notes="Upper third of the cliff, north bank of Wadi Umm Sira; partly collapsed; perhaps three levels.")
R(ROWS, "A41:I/2", num="2/I", src=f"{S1} p. 3", lineage=LIN, grid="18900/14590", cbasis="printed grid (shared by I/1-2)",
  period="no finds", exc="surveyed", read=T1, notes="One narrow long space 6 x 2 m; lower third of the cliff.")
R(ROWS, "A41:I/3", num="3/I", src=f"{S1} p. 3", lineage=LIN, grid="18905/14575", n_open=1, open_basis="singular description",
  period="empty", exc="surveyed", read=T1, notes="A wide low opening (3.2 x 0.7 m) to one irregular space.")
R(ROWS, "A41:I/4", num="4/I 'Sickle Cave'", src=f"{S1} pp. 3-4", lineage=LIN, ftype="natural cave", grid="18910/14560",
  period="no archaeological finds (recent iron sickle on surface)", exc="excavated (L-619), to bedrock in most loci", read=T1,
  notes="Two levels; the two openings described are in the ceiling of the central space (interior), not exterior.")
R(ROWS, "A41:I/5", num="5/I", src=f"{S1} p. 4", lineage=LIN, ftype="natural cave", grid="18605/14855", n_open=1,
  open_basis="singular description", period="no finds", exc="surveyed", read=T1, notes="Large opening 5 x 4 m.")
R(ROWS, "A41:I/6", num="6/I", src=f"{S1} p. 4", lineage=LIN, ftype="natural cave", grid="18600/14790", cbasis="printed grid (shared by I/6-7)",
  period="empty", exc="surveyed", read=T1)
R(ROWS, "A41:I/7", num="7/I", src=f"{S1} p. 4", lineage=LIN, ftype="natural cave", grid="18600/14790", cbasis="printed grid (shared by I/6-7)",
  period="empty", exc="surveyed", read=T1)
R(ROWS, "A41:I/8", num="8/I", src=f"{S1} p. 4", lineage=LIN, grid="18870/14635", n_open=1, open_basis="singular description",
  period="no finds", exc="surveyed", read=T1, notes="Small opening 0.8 x 0.6 m.")
R(ROWS, "A41:I/9", num="9/I Mgharat Taybat el-Asm", src=f"{S1} p. 4", lineage=LIN, grid="18615/14885", n_open=1,
  open_basis="singular description", period="no finds", exc="surveyed", read=T1)
R(ROWS, "A41:I/10", num="10/I", src=f"{S1} pp. 4-5", lineage=LIN, grid="18585/14915", n_open=1, open_basis="singular description",
  terrace="yes", terrace_basis="an entrance space with collapsed ceiling and a levelled cultivation step in front of the cave (מדרגת עיבוד), together c. 20 x 5 m",
  period="non-indicative sherds", exc="surveyed", read=T1)
R(ROWS, "A41:I/14", num="14/I Shaqfan el-Azbat", src=f"{S1} pp. 4-6, Plan 1, Figs. 1-3", lineage=LIN, ftype="complex of spaces; natural cave",
  grid="18790/14945", n_open=1, open_basis="stated (its opening)", facings="cave:S", facing_basis="word in text", res=4,
  terrace="yes", terrace_basis="a fieldstone enclosure (courtyard, חצר) 11.2 x 8.5 m outside the cave, probably recent",
  plan="Plan 1 (p. 5)", period="Late Byzantine and Umayyad (6th-8th c. CE); not earlier", piw="no", exc="excavated (L-621), two test squares to bedrock",
  finds="pottery, glass, basalt grinding stone", read=T1,
  notes="Three adjacent openings: two small niches (east) and the cave (west); the cave's own opening faces south and was blocked by a wall.")
for n in (11, 12, 13):
    X(EXCL, f"A41:I/{n}", num=f"{n}/I", src=f"{S1} p. 4", ftype="cave", grid="18730-40/15150", reason="outside the box (N 151,500 > 150,000)", read=T1)
for n in (15, 16, 17, 18, 19):
    X(EXCL, f"A41:I/{n}", num=f"{n}/I", src=f"{S1} p. 6", ftype="cave", grid="18890/15400", reason="outside the box (N 154,000 > 150,000)", read=T1,
      notes="Group of five large and some smaller caves on Wadi el-Baqar; I/15 has a large step in front with Early Roman sherds; first-century cooking pots before I/15-16." if n == 15 else "")

# ------------------------------------------------------------------ Region II
# Hirschfeld and Riklin, Region II (upper Wadi el-Makkuk, Wadi es-Sikh), printed pp. 7-30 (printed = PDF + 6).
# 68 karst caves surveyed and re-examined (p. 10); Frumkin's earlier cave survey recorded 374 caves in the wadi (p. 10).
# Report uses intercardinal facing words (NE): 8-point. First read 04:10:36Z.
S2 = "A41 Region II (Hirschfeld and Riklin)"
T2 = "2026-10-11T04:10:36Z"
R(ROWS, "A41:II/1", num="1/II", src=f"{S2} p. 11, Plan 1, Fig. 3", lineage=LIN, grid="18040/14451", n_open=1, open_basis="singular description",
  res=8, plan="Plan 1 (p. 11)", period="Chalcolithic, Intermediate Bronze, Early Roman, Byzantine, one medieval sherd", piw="yes+other",
  exc="excavated (inner part, to bedrock c. 0.7 m)", finds="pottery", read=T2,
  notes="North cliff, 30 m above the channel; vertical shaft at the back to an upper level; a cultivation plot below the cliff south of the cave (not at the mouth).")
R(ROWS, "A41:II/2", num="2/II", src=f"{S2} p. 12; summary p. 29", lineage=LIN, grid="18045/14450", n_open=2, open_basis="stated number",
  res=8, north="decided", north_basis="the source names a north-eastern and a south-western opening (INFERENCE: the NE one is the northern member)",
  period="entry: no evidence of human activity in a limited test; summary (p. 29) lists 2/II among caves with Early Roman finds (conflict)",
  piw="", exc="sounded (limited test near both openings)", read=T2,
  notes="Two openings 8 m apart into two connected halls; SW opening 3.5 x 4-5 m, NE opening 3 x 2 m. No facing or pillar stated. The summary's '2/II on the north bank' may be a slip for 1/II.")
R(ROWS, "A41:II/3", num="3/II 'Wet Hole Cave' (Frumkin)", src=f"{S2} pp. 12-13, Plan 2, Figs. 4-5", lineage=LIN, grid="18065/14470",
  n_open=2, open_basis="stated number", res=8, plan="Plan 2 (p. 12), plan and section",
  pillar="no", pillar_basis="Plan 2 (whole cave, 0-4 m scale; viewed 05:24Z) shows no pillar and the text names none (PLAN 4.3 fail rule)",
  period="Chalcolithic (1 sherd), MB, Iron I (jewellery hoard), Early Roman (jars), Early Islamic; Islamic coin", piw="yes+other",
  exc="excavated (L-630; three loci to bedrock, max 1.5 m)", finds="pottery, stone vessel fragment, Iron I hoard, Islamic coin", read=T2,
  notes="Two openings in the south cliff, the lower c. 30 m above the channel; two levels; 40 m long.")
X(EXCL, "A41:II/4", num="4/II", src=f"{S2} p. 14", ftype="hermit cell (built)", reason="not a cave", read=T2)
X(EXCL, "A41:II/5", num="5/II", src=f"{S2} pp. 15-16", ftype="hermit cell (built)", reason="not a cave", read=T2)
R(ROWS, "A41:II/6", num="6/II", src=f"{S2} p. 17, Fig. 10", lineage=LIN, grid="18064/14497", n_open=1, open_basis="singular description", res=8,
  terrace="yes", terrace_basis="remains of a step (terrace) wall in front of the opening (קיר מדרגה), and a cultivation-terrace wall above the opening",
  period="Byzantine, Early Islamic, medieval", piw="no", exc="surveyed", read=T2,
  notes="Southernmost of four caves side by side in the north cliff; two burrows branch from the opening.")
R(ROWS, "A41:II/7", num="7/II", src=f"{S2} p. 17, Fig. 10", lineage=LIN, grid="18065/14498", n_open=1, open_basis="singular description", res=8,
  period="no finds", exc="surveyed", read=T2, notes="Two spaces on a north-south axis; opening 6.5 x 4 m.")
R(ROWS, "A41:II/8", num="8/II", src=f"{S2} p. 17, Fig. 10", lineage=LIN, ftype="cave (heading: cave and rock shelter)", grid="18066/14498",
  n_open=1, open_basis="singular description", res=8, period="Byzantine, Early Islamic, medieval", piw="no", exc="surveyed", read=T2,
  notes="A rock-cut flight of ten steps leads to the opening; entrance blocked in modern times.")
X(EXCL, "A41:II/9", num="9/II", src=f"{S2} p. 17", ftype="rock shelter", reason="not a cave (rock shelter)", grid="18067/14498", read=T2)
R(ROWS, "A41:II/10", num="10/II", src=f"{S2} pp. 17-18", lineage=LIN, grid="18079/14504", n_open=1, open_basis="singular description", res=8,
  period="non-indicative sherds", exc="surveyed", read=T2)
R(ROWS, "A41:II/11a", num="11/II (northern of the pair, 'Cave of the Martens', Frumkin)", src=f"{S2} p. 18, Plan 5, Figs. 11-12", lineage=LIN,
  grid="18082/14497", cbasis="printed grid (shared by the pair)", n_open=1, open_basis="singular description", res=8, plan="Plan 5 (p. 18)",
  period="Iron IIC, a few medieval sherds", piw="no", exc="excavated (L-631, per the Index)", read=T2,
  notes="A pair of caves side by side, not connected; a rock shelter in front narrowing to the opening.")
R(ROWS, "A41:II/11b", num="11/II (southern of the pair)", src=f"{S2} p. 18, Fig. 11", lineage=LIN, grid="18082/14497",
  cbasis="printed grid (shared by the pair)", res=8, period="", exc="surveyed", read=T2)
R(ROWS, "A41:II/12", num="12/II", src=f"{S2} pp. 18-19, Fig. 13", lineage=LIN, grid="18083/14499", n_open=1, open_basis="singular description", res=8,
  period="no finds", exc="surveyed", read=T2)
X(EXCL, "A41:II/13", num="13/II", src=f"{S2} p. 19", ftype="two cisterns", reason="not a cave", grid="18088/14500", read=T2)
X(EXCL, "A41:II/14", num="14/II", src=f"{S2} p. 20", ftype="tunnel/burrow (מחילה)", reason="not a cave by the source's type word", grid="18085/14510", read=T2)
X(EXCL, "A41:II/15", num="15/II", src=f"{S2} p. 20", ftype="niche (כוך)", reason="not a cave", grid="18095/14515", read=T2)
R(ROWS, "A41:II/16", num="16/II", src=f"{S2} p. 20", lineage=LIN, grid="18097/14510", n_open=1, open_basis="singular description", res=8,
  period="non-indicative sherds", exc="surveyed", read=T2, notes="A small blocked opening at the back of the hall is interior.")
X(EXCL, "A41:II/17", num="17/II", src=f"{S2} p. 20", ftype="agricultural terrace", reason="not a cave", read=T2)
R(ROWS, "A41:II/18", num="18/II", src=f"{S2} pp. 20-21", lineage=LIN, grid="18095/14508", n_open=1, open_basis="stated (the cave's opening)",
  facings="cave:NE", facing_basis="word in text", res=8, period="Byzantine", piw="no", exc="surveyed", read=T2,
  notes="Two levels; bell-shaped cistern beside the opening; a path retaining wall opposite the opening (not a terrace).")
R(ROWS, "A41:II/19", num="19/II", src=f"{S2} p. 21, Fig. 18", lineage=LIN, grid="19099/14501", coord_ok=False, where="east slope of the Khallet ed-Danabiya spur, upper Wadi el-Makkuk (Region II)", n_open=1, open_basis="singular description", res=8,
  period="Byzantine", piw="no", exc="surveyed", read=T2,
  notes="Grid printed 19099/14501, probably a slip for 18099/14501 (the cave is on the spur's east slope); coordinates flagged. A small rock-levelled platform in the upper level from which steps descend to 32/II; its relation to a mouth is not stated, so terrace is left unknown.")
for n in range(20, 32):
    R(ROWS, f"A41:II/{n}", num=f"{n}/II (one of twelve caves 20-31/II)", src=f"{S2} p. 21", lineage=LIN, grid="1809/1445-8",
      cbasis="group centre (20-31/II)", res=8, period="rock cuttings attributed to Byzantine monks (group statement)", piw="no",
      exc="surveyed (not systematically)", read=T2)
R(ROWS, "A41:II/32", num="32/II 'Church Cave'", src=f"{S2} pp. 21-22, Fig. 19", lineage=LIN, ftype="natural cave; 'actually a rock shelter'",
  grid="18075/14455", n_open=1, open_basis="stated (its wide opening)", facings="cave:S", facing_basis="word in text", res=8,
  period="Byzantine, Mamluk", piw="no", exc="excavated earlier (Goldfus 1984)", read=T2, c1="unknown",
  notes="The source calls it a natural cave and says it is in fact a rock shelter (PLAN 4.1(3)).")
for n in range(33, 42):
    R(ROWS, f"A41:II/{n}", num=f"{n}/II (one of nine caves 33-41/II)", src=f"{S2} p. 22", lineage=LIN, grid="1807/1443-5",
      cbasis="group centre (33-41/II)", res=8, period="Byzantine and medieval sherds near the openings (group statement)", piw="no",
      exc="surveyed (partly)", read=T2)
R(ROWS, "A41:II/42", num="42/II 'Steps Cave'", src=f"{S2} p. 22; summary p. 29", lineage=LIN, ftype="two-storey cave", grid="18095/14414", res=8,
  period="coins: Claudius/Antonius Felix 54 CE (outside the cave), Hadrian denarius 125-132 CE, Ayyubid 1250-1259; summary lists Early Roman", piw="yes+other",
  exc="surveyed", finds="three coins", read=T2,
  notes="Windows in the walls of both upper spaces; number of exterior openings not stated.")
X(EXCL, "A41:II/43", num="43/II", src=f"{S2} p. 22", ftype="hermit cell", reason="not a cave", read=T2)
X(EXCL, "A41:II/44", num="44/II", src=f"{S2} p. 23", ftype="retaining wall", reason="not a cave", read=T2)
X(EXCL, "A41:II/45", num="45/II", src=f"{S2} p. 23", ftype="agricultural plots", reason="not a cave", read=T2)
X(EXCL, "A41:II/46", num="46/II", src=f"{S2} p. 23", ftype="agricultural plots", reason="not a cave", read=T2)
R(ROWS, "A41:II/47", num="47/II", src=f"{S2} p. 23, Fig. 20", lineage=LIN, grid="18110/14453", res=8, period="Byzantine, Mamluk", piw="no",
  exc="surveyed", read=T2, notes="Three levels; six niches; upper hall reached by a rock-cut ramp.")
X(EXCL, "A41:II/48", num="48/II", src=f"{S2} p. 23", ftype="cistern", reason="not a cave", read=T2)
R(ROWS, "A41:II/49", num="49/II 'Spring Cave'", src=f"{S2} pp. 23-25, Plan 6, Figs. 21-23", lineage=LIN, grid="18120/14418",
  n_open=1, open_basis="stated (its opening, round, with a built dam wall)", res=8, plan="Plan 6 (p. 24)",
  period="Early Roman (pottery, pool plaster); pool perhaps a ritual bath of the Second Temple period (excavators' suggestion)", piw="yes",
  exc="excavated (L-632)", finds="pottery", read=T2)
R(ROWS, "A41:II/50", num="50/II", src=f"{S2} p. 25", lineage=LIN, grid="18108/14418", n_open=1, open_basis="singular description", res=8,
  period="non-indicative sherds", exc="surveyed", read=T2)
R(ROWS, "A41:II/51", num="51/II 'Lamp Cave'", src=f"{S2} pp. 25-26, Plan 7, Fig. 24", lineage=LIN, grid="18105/14418",
  n_open=1, open_basis="stated (a doorway set in the wall blocking the natural opening)", res=8, plan="Plan 7 (p. 25)",
  period="Iron IIC, Hellenistic (Hasmonean jar), Early Roman, Bar Kokhba-period lamp fragment, Mamluk coin", piw="yes+other",
  exc="excavated (L-633)", finds="pottery, lamp, coin", read=T2)
for n in range(52, 61):
    R(ROWS, f"A41:II/{n}", num=f"{n}/II (one of nine natural caves 52-60/II)", src=f"{S2} p. 26", lineage=LIN, ftype="natural cave",
      grid="1814/1442", cbasis="group centre (52-60/II)", res=8, period="no evidence of human presence (group statement)",
      exc="surveyed (hastily)", read=T2)
R(ROWS, "A41:II/61", num="61/II 'Terrace Cave' (heading: rock shelter)", src=f"{S2} pp. 26-28, Plan 8, Figs. 25-26", lineage=LIN,
  ftype="rock shelter (heading); cave (plan and figure captions)", grid="18163/14415", n_open=1, open_basis="singular description (its opening, walled)",
  res=8, terrace="yes", terrace_basis="nickname 'Terrace Cave' (מערת הטרסה) only; the text describes a built wall across the opening, not a terrace (weak)",
  plan="Plan 8 (p. 26)", period="Early Roman, Byzantine, Late Islamic; two 4th c. CE coins", piw="yes+other", exc="excavated (L-635)", read=T2, c1="unknown")
R(ROWS, "A41:II/62", num="62/II", src=f"{S2} p. 28", lineage=LIN, grid="18170/14425", cbasis="printed grid (shared by 62-63/II)", res=8,
  period="no finds", exc="surveyed (hastily)", read=T2)
R(ROWS, "A41:II/63", num="63/II", src=f"{S2} p. 28", lineage=LIN, grid="18170/14425", cbasis="printed grid (shared by 62-63/II)", res=8,
  period="no finds", exc="surveyed (hastily)", read=T2)
X(EXCL, "A41:II/64", num="64/II", src=f"{S2} p. 28", ftype="lime kiln", reason="not a cave", read=T2)
R(ROWS, "A41:II/65", num="65/II", src=f"{S2} p. 28", lineage=LIN, grid="18198/14434", res=8, period="no finds", exc="surveyed", read=T2)
X(EXCL, "A41:II/66", num="66/II", src=f"{S2} p. 28, Fig. 27", ftype="rock shelter", reason="not a cave (rock shelter)", grid="18195/14490", read=T2)
R(ROWS, "A41:II/67", num="67/II", src=f"{S2} p. 28", lineage=LIN, ftype="dwelling cave", grid="18200/14499", n_open=1, open_basis="singular description",
  res=8, terrace="yes", terrace_basis="a seating platform (bench?) of a row of stones in front of the opening (משטח ישיבה) (weak)",
  period="no finds; inhabited by a shepherd family in 1993", exc="surveyed (partly)", read=T2)
X(EXCL, "A41:II/68", num="68/II", src=f"{S2} pp. 28-29", ftype="agricultural terraces", reason="not a cave", read=T2)

# ------------------------------------------------------------------ Region III
# Barshad and Shaked, Region III (lower Wadi el-Makkuk), printed pp. 31-41 (PDF p. 4 = p. 34; text starts p. 33).
# 14 caves, niches and rock clefts examined (p. 33). No facing words used (4-point). First read 04:13:27Z.
S3 = "A41 Region III (Barshad and Shaked)"
T3 = "2026-10-11T04:13:27Z"
X(EXCL, "A41:III/1", num="1/III", src=f"{S3} p. 33", ftype="niche (כוך)", reason="not a cave", grid="18935/14520", read=T3)
X(EXCL, "A41:III/2", num="2/III", src=f"{S3} p. 33", ftype="rock shelter", reason="not a cave (rock shelter)", grid="18927/14520", read=T3)
R(ROWS, "A41:III/3", num="3/III", src=f"{S3} p. 34, Fig. 2", lineage=LIN, ftype="natural cave, enlarged by cutting", grid="18930/14530",
  n_open=2, open_basis="stated number (two levels, each with an opening in the cliff)", res=4,
  pillar="yes", pillar_kind="natural stone pillar (עמוד אבן טבעי), c. 1.9 m high", pillar_pos="at the entrance of the upper level",
  pillar_basis="text p. 34", north="undetermined", north_basis="the two openings are on two levels, one above the other; no relative northing given",
  period="Chalcolithic sherds; autonomous coin of Side, 3rd c. BCE; textiles, leather, rope, human bones", piw="no",
  exc="surveyed; permit L-627 issued in 1993 but not carried out (note); probably excavated earlier by Patrich and Arubas (unpublished, note 3)", finds="pottery, textiles, coin, human bones", read=T3,
  notes="The lower level's entrance room had an opening blocked by a built wall; 'evidence for further openings' in the lower hall could not all be checked (interior or exterior not stated). No plan published.")
X(EXCL, "A41:III/4", num="4/III", src=f"{S3} p. 35", ftype="natural crevice with a rock shelter in front", reason="not a cave", grid="18927/14520", read=T3)
R(ROWS, "A41:III/5", num="5/III", src=f"{S3} p. 35", lineage=LIN, grid="18930/14530", cbasis="no own grid; 10 m below III/3 (grid of III/3 used)", res=4,
  period="Chalcolithic pottery and many human bones in front and in spoil (earlier digging)", piw="no", exc="surveyed; earlier digging", read=T3,
  notes="One natural space 4.0 x 1.5 m.")
X(EXCL, "A41:III/6", num="6/III", src=f"{S3} p. 35", ftype="niche (כוך)", reason="not a cave", grid="18925/14520", read=T3)
R(ROWS, "A41:III/7", num="7/III", src=f"{S3} p. 35, Fig. 3", lineage=LIN, grid="18925/14505", res=4,
  period="Chalcolithic sherds, bead, mat, leather, textiles, resin, human burials", piw="no",
  exc="excavated earlier by Patrich and Arubas (unpublished); surveyed 1993; permit L-626 issued but not carried out (note)", read=T3,
  notes="Access by ropes or a natural chimney; a natural rock ledge 8 x 6 m in front leads to further spaces (a natural ledge is not a terrace, PLAN 4.3).")
R(ROWS, "A41:III/8", num="8/III", src=f"{S3} pp. 36-39, Plan 1, Figs. 4-7", lineage=LIN, ftype="natural cave, two storeys", grid="18925/14505",
  cbasis="group centre (8-11/III)", res=4, plan="Plan 1 (p. 37), plans and section",
  period="Chalcolithic, Hellenistic and Roman sherds; 9 coins of Alexander Jannaeus (103-76 BCE), coins of 218-222 CE and Severus Alexander", piw="yes+other",
  exc="excavated fully (L-625)", finds="pottery, 12 coins, lead weight, glass, beads, textiles", read=T3,
  notes="Caves 8-11/III are linked by a narrow path that widens to a ledge in front of each cave (natural).")
X(EXCL, "A41:III/9", num="9/III", src=f"{S3} p. 39", ftype="niche (כוך), natural", reason="not a cave", read=T3,
  notes="Jannaeus coin, human skeleton; a bell-shaped plastered cistern beside the path near its opening.")
X(EXCL, "A41:III/10", num="10/III", src=f"{S3} p. 39", ftype="niche (כוך)", reason="not a cave", read=T3)
R(ROWS, "A41:III/11", num="11/III (system of spaces)", src=f"{S3} pp. 39-40, Plan 2 (p. 39), Figs. 3-4", lineage=LIN,
  ftype="system of spaces (heading); 'cave' in the text and in the Fig. 3 caption", grid="18925/14505", cbasis="group centre (8-11/III)",
  n_open=2, open_basis="stated number (two narrow openings to the rock ledge)", res=4,
  pillar="yes", pillar_kind="rock pillar (עמוד סלע)", pillar_pos="between the two openings", pillar_basis="text p. 39; drawn in Plan 2",
  north="decided", north_basis="Plan 2 (north arrow, 0-3 m bar): the opening to L3/L4 lies c. 0.4 m north of the opening to the large space (A6 with approximate midpoints, INFERENCE)",
  north_case="unspecified (arrow)", plan="Plan 2 (p. 39)",
  period="Chalcolithic, Iron II and Hellenistic sherds; coins of Alexander Jannaeus, Lucius Verus(?) 161-169 CE; posthumous Alexander tetradrachm; papyrus scraps", piw="yes+other",
  exc="excavated (L-629; three days; cistern L5 emptied)", finds="pottery, coins, papyrus scraps, organic finds", read=T3,
  notes="The openings lead onto a wide natural rock ledge (L1), partly roofed, 'facing the cliff front' (not a compass facing). Plan 2: mouths crossed by thin double-line partitions; rock-cut jambs cannot be told from built ones, so the mouths are NOT MEASURABLE under A3 (C4 unknown). Exploratory note (not under the rule): the ledge front faces roughly SSW on Plan 2's arrow; the cave is on the north cliff of the wadi. Plan 2 may also show the large space open to the cliff edge (INFERENCE, uncertain).")
R(ROWS, "A41:III/12", num="12/III", src=f"{S3} p. 40", lineage=LIN, grid="", where="c. 12 m above the foot of the north cliff, lower Wadi el-Makkuk (Region III)",
  n_open=1, open_basis="singular description (entry through a natural crack)", res=4, period="empty", exc="surveyed", read=T3)
R(ROWS, "A41:III/13", num="13/III 'Cave of the Warrior'", src=f"{S3} p. 40 (refers to Schick 1998)", lineage=LIN, grid="",
  where="c. 12 m above the foot of the north cliff, lower Wadi el-Makkuk (Region III)", res=4,
  period="a fourth-millennium BCE burial (Schick 1998, title)", piw="no", exc="excavated (Schick 1998; not read here)", read=T3)
X(EXCL, "A41:III/14", num="14/III", src=f"{S3} p. 40", ftype="rock shelter", reason="not a cave (rock shelter)", grid="18915/14502", read=T3)

# ------------------------------------------------------------------ Regions IV and VI
# Sion, Regions IV and VI (Jebel Abu Saraj cliffs), printed pp. 43-84 (printed = PDF + 41; p. 45 has no text layer and
# was read from the page image: introduction only). 30 caves in Region IV and 29 in Region VI (p. 80).
# Report uses intercardinal facing words (IV/8 'south-east'): 8-point. First read 04:20:50Z (pp. 46-60, 65-84).
# Pages 61-64 (IV/9-IV/21) were opened by an earlier worker (atlas/research/atiqot41_iv11_iv17_review_2026-10-01.md);
# IV/11 and IV/17 are recorded in the repository; IV/1 and IV/8 coin finds are quoted in
# research/agent_review_2026-10-07/wave2/W2C_kohlit_archaeology/REPORT.txt.
S4 = "A41 Regions IV and VI (Sion)"
T4 = "2026-10-11T04:20:50Z"
PO = "page-opened-before"
R(ROWS, "A41:IV/1", num="IV/1", src=f"{S4} pp. 46-47, Plan 1, Fig. 1", lineage=LIN, ftype="natural cave", grid="19015/14440",
  cbasis="printed grid (shared by IV/1, IV/2 and niches)", n_open=2, open_basis="stated number (two openings lead into the cave)",
  facings="m_north:E", facing_basis="word in text: the northern opening 'is set in the eastern wall of the cave' (position word read as facing, INFERENCE; see AMENDMENT_1)",
  pillar="no", pillar_basis="Plan 1 (schematic plan of the whole cave, 0-3 m scale; viewed 05:24Z) shows no pillar and the text names none (PLAN 4.3 fail rule; schematic)",
  res=8, north="decided", north_basis="the source names a northern and a southern opening", plan="Plan 1 (p. 46 or 47)",
  period="two Jannaeus coins (survey); two Jannaeus and one Hasmonean coin (excavation); use dated to the 1st c. BCE", piw="yes",
  exc="excavated (L-655, M. Dadon)", finds="coins, non-indicative sherds, bones, leather", exposure="exposed-repo", read=T4,
  notes="Oval elongated cave 12.0 x 3.2 m. The southern opening (2.3 m) is the main entrance; a path leads from the northern opening to rock shelter IV/2. Repository exposure covers the coins only.")
X(EXCL, "A41:IV/2", num="IV/2", src=f"{S4} pp. 47-49, Plan 2", ftype="rock shelter", reason="not a cave (rock shelter)", grid="19015/14440", read=T4,
  notes="Opening faces south; late Hellenistic and Early Roman pottery; Ptolemaic coins.")
R(ROWS, "A41:IV/3", num="IV/3 'Ibex Cave'", src=f"{S4} p. 49, Figs. 2, 4", lineage=LIN, ftype="natural cave", grid="19025/14430",
  cbasis="group centre (IV/3-8)", n_open=1, open_basis="singular description", res=8, period="ibex bones; bronze arrowhead (no date stated in the entry)",
  exc="surveyed", read=T4)
R(ROWS, "A41:IV/4", num="IV/4 'Two-storey Cave'", src=f"{S4} p. 49, Fig. 2", lineage=LIN, ftype="natural cave, two storeys", grid="19025/14430",
  cbasis="group centre (IV/3-8)", res=8, period="Hellenistic jar sherds (upper storey); coin of Maurice Tiberius 590/1 CE (lower storey)", piw="partly",
  exc="surveyed; plundered", read=T4, notes="Upper storey reached only by rappel, lower storey through a natural niche; exterior openings not counted.")
R(ROWS, "A41:IV/5", num="IV/5 'Lamp Cave'", src=f"{S4} pp. 50-52, Figs. 2, 5-7", lineage=LIN, ftype="natural cave", grid="19025/14430",
  cbasis="group centre (IV/3-8)", n_open=1, open_basis="stated (its opening, as wide and high as the cave)", facings="cave:E", facing_basis="word in text",
  res=8, period="four Jannaeus coins and a Ptolemy II coin (survey); Jannaeus coins (excavation); bronze two-nozzled lamp; Persian and Hellenistic pottery",
  piw="yes+other", exc="excavated to bedrock (L-602, Sirkis, Nagar-Hilman and Flos)", finds="lamp, coins, cooking pots in situ, arrowhead", read=T4,
  notes="The excavation paragraph (axis N-S, opening faces east) is read as belonging to IV/5 (Fig. 7 caption 'Cave IV/5').")
R(ROWS, "A41:IV/6", num="IV/6 'Drachms Cave'", src=f"{S4} pp. 52-54, Figs. 2, 5, 8", lineage=LIN, ftype="natural cave (hewn opening and space)",
  grid="19025/14430", cbasis="group centre (IV/3-8)", n_open=1, open_basis="stated (a hewn opening in the wall of the ledge)", res=8,
  period="silver drachms (late 4th c. BCE), Yehud coins, Hellenistic bronze coins incl. a Jannaeus coin, a Bar Kokhba-type glass bowl; Hellenistic and perhaps Persian use",
  piw="yes+other", exc="excavated to bedrock (L-601, R. Avner); plundered", finds="coins, glass bowl", read=T4,
  notes="A natural rock ledge in front (not a terrace under PLAN 4.3).")
R(ROWS, "A41:IV/7", num="IV/7 'Crescent Cave'", src=f"{S4} pp. 54-59, Plan 3, Figs. 2, 5, 9-11", lineage=LIN, ftype="natural cave", grid="19025/14430",
  cbasis="group centre (IV/3-8)", n_open=1, open_basis="stated (the cave's opening)", facings="cave:E", facing_basis="word in text", res=8,
  plan="Plan 3 (p. 55)", period="Chalcolithic, EB I, late Hellenistic, Early Roman pottery; coins: Seleucid, Jannaeus, Herod I, 37 BCE-6 CE",
  piw="yes+other", exc="excavated (L-648, F. Ibrahim)", finds="pottery, coins, human bones, beads", read=T4,
  notes="The opening, narrowing upwards, was blocked across its width by a low wall.")
R(ROWS, "A41:IV/8", num="IV/8 'Hasmonean Cave'", src=f"{S4} pp. 59-60, Plan 4", lineage=LIN, ftype="natural cave", grid="19025/14430",
  cbasis="group centre (IV/3-8)", n_open=1, open_basis="stated (its opening)", facings="cave:SE", facing_basis="word in text", res=8,
  plan="Plan 4 (p. 60)", period="seven Hasmonean coins (John Hyrcanus I, Jannaeus, Mattathias Antigonus)", piw="yes",
  exc="excavated fully (L-649)", finds="coins, textiles", exposure="exposed-repo", read=T4, notes="Repository exposure covers the coins only.")
R(ROWS, "A41:IV/9", num="IV/9", src=f"{S4} p. 61, Fig. 12", lineage=LIN, ftype="natural cave", grid="19030/14415", cbasis="group centre (IV/9-19)",
  res=8, period="", exc="surveyed", exposure=PO, read=T4, notes="Rock step in front; niches along the north wall.")
R(ROWS, "A41:IV/10", num="IV/10", src=f"{S4} p. 61, Fig. 12", lineage=LIN, ftype="natural cave", grid="19030/14415", cbasis="group centre (IV/9-19)",
  n_open=1, open_basis="singular description (an opening in the north wall of a front niche)", res=8, period="no finds", exc="surveyed; plundered",
  exposure=PO, read=T4)
R(ROWS, "A41:IV/11", num="IV/11 'Cave of the Pillar'", src=f"{S4} pp. 61-62; Feig, A41 pp. 85-90, Plan 1", lineage=LIN, ftype="natural cave",
  grid="19030/14415", cbasis="group centre (IV/9-19)", n_open=1, open_basis="singular description (Feig: an opening in the singular)", res=8,
  pillar="yes", pillar_kind="natural below, rock-cut above, 2.5 m", pillar_pos="south-west end of the hall", pillar_basis="Feig p. 85 (repository notes)",
  terrace="yes", terrace_basis="an entrance forecourt L14, c. 3 x 5 m (Feig p. 85, repository notes)", plan="Feig Plan 1 (p. 85)",
  period="Iron Age; Hellenistic/Roman; coins: Mattathias Antigonus (Sion), two Hasmonean and two Elagabalus (Feig)", piw="yes+other",
  exc="excavated (Feig)", exposure="exposed-repo", read=T4,
  notes="Coded from the repository's reading of Feig (atlas/research/atiqot41_iv11_iv17_review_2026-10-01.md) and Sion p. 61; one of the four modelled caves.")
R(ROWS, "A41:IV/12", num="IV/12", src=f"{S4} p. 62, Fig. 12 (excavation: Wolff, Part 2, not read)", lineage=LIN, ftype="natural cave", grid="19030/14415",
  cbasis="group centre (IV/9-19)", res=8, period="coins: Ptolemy II, Jannaeus, Mattathias Antigonus (two), Herod I", piw="yes+other",
  exc="excavated (Wolff, Part 2; not read)", exposure=PO, read=T4)
R(ROWS, "A41:IV/13", num="IV/13 (cave; with a niche 7 m west)", src=f"{S4} p. 62, Fig. 12", lineage=LIN, ftype="natural cave and niche", grid="19030/14415",
  cbasis="group centre (IV/9-19)", n_open=1, open_basis="stated (the cave's opening)", res=8, period="no finds", exc="surveyed", exposure=PO, read=T4)
R(ROWS, "A41:IV/14", num="IV/14", src=f"{S4} p. 63, Fig. 12", lineage=LIN, ftype="natural cave", grid="19030/14415", cbasis="group centre (IV/9-19)",
  n_open=1, open_basis="singular description (opening as wide as the cave)", res=8, period="no finds", exc="surveyed", exposure=PO, read=T4)
R(ROWS, "A41:IV/15", num="IV/15", src=f"{S4} p. 63, Fig. 12", lineage=LIN, ftype="natural cave", grid="19030/14415", cbasis="group centre (IV/9-19)",
  n_open=1, open_basis="stated (the cave's oval opening)", res=8, period="no finds", exc="surveyed", exposure=PO, read=T4)
R(ROWS, "A41:IV/16", num="IV/16", src=f"{S4} p. 63, Fig. 12", lineage=LIN, ftype="natural cave", grid="19030/14415", cbasis="group centre (IV/9-19)",
  n_open=1, open_basis="singular description ('from the opening inwards')", res=8, period="no finds", exc="sounded (test pits)", exposure=PO, read=T4,
  notes="A rock shelter (7.5 m) in front of a rectangular space.")
R(ROWS, "A41:IV/17", num="IV/17 'Cave of the Built Wall'", src=f"{S4} pp. 63-64, Plan 5, Figs. 12-13", lineage=LIN, ftype="natural cave", grid="19030/14415",
  cbasis="group centre (IV/9-19)", n_open=2, open_basis="stated number", facings="plan", facing_basis="plan (Plan 5; repository endpoint picks)", res=8,
  north_case="unspecified (arrow)", pillar="yes", pillar_kind="rock-cut", pillar_pos="between the northern and southern spaces (and openings)",
  pillar_basis="text p. 63", north="decided", north_basis="text names a northern and a southern opening; A6 on Plan 5 midpoints gives c. 2.6 m",
  plan="Plan 5 (p. 63)", period="Hellenistic pottery; coins of Jannaeus and a Hasmonean; use from the first half of the 2nd to the first half of the 1st c. BCE (excavator)",
  piw="yes+other", exc="excavated (L-656, M. Dadon)", finds="three arrowheads, sandals, textiles, rope", exposure="exposed-repo", read=T4,
  notes="One of the four modelled caves. The southern opening is partly blocked by a built wall 2.4 m long.")
X(EXCL, "A41:IV/18", num="IV/18 'Dagger Niche'", src=f"{S4} p. 64, Fig. 14", ftype="niche (כוך)", reason="not a cave", exposure=PO, read=T4)
R(ROWS, "A41:IV/19", num="IV/19", src=f"{S4} p. 64, Fig. 12", lineage=LIN, ftype="natural cave", grid="19040/14400", n_open=1,
  open_basis="singular description ('from the opening inwards')", res=8, period="no finds; used by nomads", exc="surveyed", exposure=PO, read=T4)
R(ROWS, "A41:IV/20", num="IV/20", src=f"{S4} p. 64, Fig. 15", lineage=LIN, ftype="natural cave", grid="19020/14395", n_open=1,
  open_basis="singular description ('narrow at the entrance')", res=8, period="no finds", exc="surveyed", exposure=PO, read=T4)
R(ROWS, "A41:IV/21", num="IV/21", src=f"{S4} pp. 64-65, Fig. 15", lineage=LIN, ftype="natural cave", grid="19035/14395", n_open=2,
  open_basis="stated number: two openings, northern (1.8 m) and southern (1.2 m), lead from a roof-collapsed front vestibule (6 x 5 m) into the inner space (counted as entrances, INFERENCE)",
  res=8, north="decided", north_basis="the source names a northern and a southern opening", period="no finds", exc="surveyed", exposure=PO, read=T4,
  notes="Whether the two openings are exterior depends on the vestibule's former roof (collapsed today).")
for n, extra in ((22, dict(n_open=1, open_basis="stated (an opening shaped as a right triangle)", period="no finds")),
                 (23, dict(n_open=1, open_basis="stated (a square opening)", period="no finds")),
                 (24, dict(period="non-indicative sherds", exc="surveyed; plundered")),
                 (25, dict(n_open=1, open_basis="stated (an opening 1.5 x 1.7 m)", period="no ancient finds", exc="surveyed; plundered")),
                 (26, dict(n_open=1, open_basis="stated (a square opening)", period="non-indicative sherds", exc="surveyed; plundered"))):
    kw = dict(exc="surveyed")
    kw.update(extra)
    g = "19035/14395" if n in (22, 23) else "19040/14395"
    R(ROWS, f"A41:IV/{n}", num=f"IV/{n}", src=f"{S4} p. 65, Fig. 15", lineage=LIN, ftype="natural cave", grid=g,
      cbasis="printed grid (shared)", res=8, read=T4, **kw)
R(ROWS, "A41:IV/27", num="IV/27", src=f"{S4} p. 66, Fig. 16", lineage=LIN, ftype="natural cave", grid="19010/14390", n_open=1,
  open_basis="singular description (the cave's opening)", res=8, period="non-indicative sherds; used until recently", exc="surveyed", read=T4)
R(ROWS, "A41:IV/28", num="IV/28", src=f"{S4} p. 66, Figs. 15, 17", lineage=LIN, ftype="natural cave", grid="19010/14390", res=8,
  period="no finds", exc="surveyed", read=T4, notes="A rock shelter and a perpendicular inner space (30 x 15 m); stepped rock slope in front.")
R(ROWS, "A41:IV/29", num="IV/29", src=f"{S4} pp. 66-67, Fig. 17", lineage=LIN, ftype="natural cave", grid="19010/14380", cbasis="group centre (IV/29-30)",
  n_open=1, open_basis="stated (the cave's opening)", res=8, period="no finds", exc="sounded (test pit)", read=T4)
R(ROWS, "A41:IV/30", num="IV/30", src=f"{S4} p. 67, Fig. 17", lineage=LIN, ftype="natural cave", grid="19010/14380", cbasis="group centre (IV/29-30)",
  n_open=1, open_basis="stated (the cave's opening, in its ceiling)", res=8, period="no finds", exc="surveyed", read=T4,
  notes="'Perhaps there was another opening at the bottom, blocked by collapse' (uncertain; not counted).")
# Region VI
for n, extra in ((31, dict(n_open=1, open_basis="stated (a narrow low opening)", period="no finds", exc="surveyed; disturbed")),
                 (32, dict(n_open=1, open_basis="stated (a wide low opening)", period="no finds")),
                 (33, dict(n_open=1, open_basis="stated (a rectangular opening)", period="two non-indicative sherds, probably Byzantine", piw="no")),
                 (34, dict(n_open=1, open_basis="stated (the opening, walled on both sides)", period="no finds")),
                 (35, dict(n_open=1, open_basis="stated (the opening, walled on both sides)", period="no finds")),
                 (36, dict(n_open=1, open_basis="stated (the cave's opening)", facings="cave:E", facing_basis="word in text", period="no finds")),
                 (37, dict(n_open=1, open_basis="stated (the cave's opening)", period="no finds"))):
    kw = dict(exc="surveyed")
    kw.update(extra)
    R(ROWS, f"A41:VI/{n}", num=f"VI/{n}", src=f"{S4} pp. 67-68, Figs. 19-20", lineage=LIN, ftype="natural cave", grid="19065/14340",
      cbasis="group centre (VI/31-37)", res=8, read=T4, **kw)
R(ROWS, "A41:VI/38", num="VI/38 (cave and burrow)", src=f"{S4} p. 69, Fig. 21", lineage=LIN, ftype="natural cave", grid="19065/14340",
  cbasis="group centre (VI/38-45)", n_open=1, open_basis="singular description (its opening, 5 m high)", res=8, period="no finds", exc="surveyed", read=T4)
R(ROWS, "A41:VI/39", num="VI/39", src=f"{S4} p. 69, Fig. 21", lineage=LIN, ftype="natural cave", grid="19065/14340", cbasis="group centre (VI/38-45)",
  n_open=1, open_basis="stated (an opening 5 m wide)", res=8, period="no finds", exc="surveyed; plundered", read=T4)
R(ROWS, "A41:VI/40", num="VI/40", src=f"{S4} p. 69, Fig. 21", lineage=LIN, ftype="natural cave", grid="19065/14340", cbasis="group centre (VI/38-45)",
  n_open=1, open_basis="singular description ('from the opening inwards')", res=8, period="no finds; used as a fold", exc="surveyed", read=T4,
  notes="A natural rock step in front.")
R(ROWS, "A41:VI/41", num="VI/41", src=f"{S4} p. 69, Fig. 21", lineage=LIN, ftype="natural cave", grid="19065/14340", cbasis="group centre (VI/38-45)",
  n_open=1, open_basis="singular description (a wall blocked the opening)", res=8, period="Byzantine sherds in robbers' spoil", piw="no",
  exc="surveyed; plundered", read=T4)
X(EXCL, "A41:VI/42", num="VI/42", src=f"{S4} p. 70", ftype="natural pit (בור)", reason="not a cave", read=T4)
R(ROWS, "A41:VI/43", num="VI/43", src=f"{S4} pp. 70-71, Plan 6, Figs. 21-22, 24", lineage=LIN, ftype="natural cave", grid="19070/14320",
  n_open=4, open_basis="stated number (four openings, I-IV)", res=8, plan="Plan 6 (p. 71)",
  period="coins of John Hyrcanus I (129-105 BCE) and Side (3rd c. BCE); excavator: activity in the 3rd-2nd c. BCE", piw="yes+other",
  exc="excavated (central part)", finds="coins, bronze buckle, leather, textiles", read=T4,
  notes="A natural rock step (6 x 2 m) under a projecting rock roof in front of opening IV (natural; not a terrace).")
R(ROWS, "A41:VI/44", num="VI/44", src=f"{S4} p. 71, Fig. 21", lineage=LIN, ftype="natural cave", grid="19070/14320", res=8, period="no finds",
  exc="surveyed", read=T4)
R(ROWS, "A41:VI/45", num="VI/45", src=f"{S4} p. 71, Fig. 21", lineage=LIN, ftype="natural cave", grid="19070/14320", n_open=2,
  open_basis="stated number (two openings lead into the cave)", facings="m1:E;m2:W",
  facing_basis="word in text: the main opening 'in its eastern wall', the second 'in its western wall' (position words read as facing, INFERENCE; see AMENDMENT_1)",
  res=8, north="undetermined", north_basis="openings in the east and west walls; no northing stated", period="no finds", exc="surveyed", read=T4)
R(ROWS, "A41:VI/46", num="VI/46", src=f"{S4} pp. 71-75, Plan 7, Figs. 23-27", lineage=LIN, ftype="natural cave", grid="19090/14285",
  n_open=1, open_basis="plan: Plan 7 (p. 73, viewed 05:22Z) shows one mouth, crossed by the courtyard fence; the Fig. 25 caption's plural 'openings' is not borne out by the plan (INFERENCE)", res=8,
  pillar="yes", pillar_kind="seven natural rock pillars (עמודי סלע טבעיים)", pillar_pos="inside, dividing the cave into sub-spaces", pillar_basis="text p. 72",
  terrace="yes", terrace_basis="an open courtyard (4.0 x 3.5 m) in front, separated from the opening by a semicircular stone fence (Plan 7)",
  plan="Plan 7 (p. 72 or 73)", period="EB IB and EB II (pottery, textiles); coins of 323-317 BCE and 383 CE", piw="no",
  exc="excavated (L-652, four loci); plundered", finds="pottery, textiles, beads, coins", read=T4,
  notes="'From the opening' in the singular in the excavation text; plural in the Fig. 25 caption; Plan 7 used for the count (PLAN 4.3: plans used for counts). Near miss for both branches: pillars and a courtyard, but one mouth.")
R(ROWS, "A41:VI/47", num="VI/47 (cave; niches VI/48-49 below)", src=f"{S4} p. 75, Figs. 23-24, 29", lineage=LIN, ftype="natural cave", grid="19070/14320",
  n_open=3, open_basis="stated number (three small openings in its northern wall)", facings="m1:N;m2:N;m3:N",
  facing_basis="word in text: openings 'in its northern wall' (position word read as facing, INFERENCE)", res=8,
  period="one sherd (Roman?); cave and niches dated late 4th-late 5th c. CE by coins", piw="no", exc="surveyed; plundered", read=T4)
X(EXCL, "A41:VI/48", num="VI/48", src=f"{S4} p. 75", ftype="niche (כוך)", reason="not a cave", read=T4)
X(EXCL, "A41:VI/49", num="VI/49", src=f"{S4} p. 75", ftype="niche (כוך)", reason="not a cave", read=T4)
R(ROWS, "A41:VI/50", num="VI/50", src=f"{S4} p. 76, Fig. 24", lineage=LIN, ftype="natural cave, two levels", grid="19070/14320",
  cbasis="group centre (VI/46-59)", res=8, period="skull fragment in robbers' pits", exc="surveyed; plundered", read=T4)
R(ROWS, "A41:VI/51", num="VI/51", src=f"{S4} p. 76, Fig. 24", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=1, open_basis="stated (the cave's opening, 2 m)", res=8, period="a few bones from robbers' pits", exc="surveyed; plundered", read=T4)
R(ROWS, "A41:VI/52", num="VI/52 'Niche Cave'", src=f"{S4} pp. 76-79, Plan 8, Figs. 23-24, 30-35", lineage=LIN, ftype="natural cave enlarged by cutting",
  grid="19070/14320", n_open=5, open_basis="stated number (five openings: four on one level, one 3.5 m lower)", res=8, plan="Plan 8 (p. 76)",
  period="glass bowls of the period between the Great Revolt and the Bar Kokhba revolt; Early Roman sherds; Early Islamic textiles; medieval and modern coins",
  piw="yes+other", exc="excavated (L-653)", finds="glass, textiles, metal objects, two plastered cisterns", read=T4,
  notes="A natural rock step (1.5-2.0 m wide) in front of the cave, overlooking the area (natural; not a terrace).")
R(ROWS, "A41:VI/53", num="VI/53", src=f"{S4} p. 79, Fig. 36", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=2, open_basis="stated: a rectangular opening divided in two by a natural stone partition (eastern and western openings)", res=8,
  north="undetermined", north_basis="the two parts are called eastern and western", period="no finds (plundered)", exc="surveyed; plundered", read=T4,
  notes="Pillar coded unknown: the divider is called a natural stone partition (מחיצת אבן טבעית), not a pillar (PLAN 4.3 strict). A near miss for C2p.")
R(ROWS, "A41:VI/54", num="VI/54", src=f"{S4} p. 79, Fig. 36", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=1, open_basis="stated (the cave's oval opening)", res=8, period="no finds", exc="surveyed", read=T4)
R(ROWS, "A41:VI/55", num="VI/55", src=f"{S4} p. 80, Fig. 36", lineage=LIN, ftype="natural cave with limited cuttings", grid="19070/14320",
  cbasis="group centre (VI/46-59)", res=8, terrace="yes", terrace_basis="a fieldstone step wall in front supporting a narrow platform (רחבה, 5.5 x 1.5 m)",
  period="no finds", exc="surveyed", read=T4)
R(ROWS, "A41:VI/56", num="VI/56", src=f"{S4} p. 80, Fig. 36", lineage=LIN, ftype="natural cave with limited cuttings", grid="19070/14320",
  cbasis="group centre (VI/46-59)", n_open=1, open_basis="stated (a narrow tall opening)", res=8, period="no finds; recent nomads", exc="surveyed", read=T4,
  notes="Access by a path on a stone wall of 11 courses.")
R(ROWS, "A41:VI/57", num="VI/57", src=f"{S4} p. 80", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=1, open_basis="stated (the opening, 4 x 6 m)", res=8, period="no finds", exc="surveyed", read=T4)
R(ROWS, "A41:VI/58", num="VI/58", src=f"{S4} p. 80", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=1, open_basis="stated (natural opening walled, with a built doorway)", res=8, period="no finds; modern nomads", exc="surveyed", read=T4)
R(ROWS, "A41:VI/59", num="VI/59", src=f"{S4} p. 80", lineage=LIN, ftype="natural cave", grid="19070/14320", cbasis="group centre (VI/46-59)",
  n_open=1, open_basis="stated (the long side open to the cliff, 2.5 m)", res=8, period="no finds", exc="surveyed", read=T4)

# ------------------------------------------------------------------ Region V
# Aronshtam, Region V (Jebel Quruntul escarpment between Wadi Abu Saraj and Wadi Halq er-Rummana), printed pp. 91-104
# (Table 1, pp. 92-96; excavations pp. 97-103). Report uses NE/NW: 8-point. The pages were opened by an earlier worker
# (registration/atiqot41_region_v_extracted.md); entries recorded there are exposed-repo, the rest page-opened-before.
# Re-read here 04:30:20Z. Eisenberg's V/49 report (pp. 105-121) is coded from the repository's extraction.
S5 = "A41 Region V (Aronshtam), Table 1"
T5 = "2026-10-11T04:30:20Z"
G1 = "19005-30/14390-95"


def _v(n, num=None, grid=G1, cb="group box (V/1-11)", **kw):
    kw.setdefault("exposure", PO)
    kw.setdefault("exc", "surveyed")
    R(ROWS, f"A41:V/{n}", num=num or f"V/{n}", src=kw.pop("src", f"{S5} p. 92"), lineage=LIN, grid=grid, cbasis=cb, res=8, read=T5, **kw)


GH1 = "group of natural caves and burrows (V/1-11); no own type word"
_v(1, ftype=GH1, c1="unknown", period="no finds")
X(EXCL, "A41:V/2", num="V/2", src=f"{S5} p. 92", ftype="narrow niche (כוך)", reason="not a cave", exposure=PO, read=T5)
_v(3, ftype="natural space (חלל טבעי) in the group of caves and burrows", c1="unknown", period="no finds")
_v(4, ftype="large cave", n_open=1, open_basis="stated (its entrance is from the ceiling)", period="no finds")
_v(5, ftype=GH1 + "; not described", c1="unknown")
X(EXCL, "A41:V/6", num="V/6", src=f"{S5} p. 92", ftype="burrow (מחילה)", reason="not a cave by the source's type word", exposure=PO, read=T5)
_v(7, ftype="low cave", period="no finds")
_v(8, ftype=GH1 + "; not described", c1="unknown")
_v(9, ftype="cave", n_open=1, open_basis="stated (the opening, 3 x 1.5 m)", period="no finds")
X(EXCL, "A41:V/10", num="V/10", src=f"{S5} p. 92", ftype="niche (כוך)", reason="not a cave", exposure=PO, read=T5)
X(EXCL, "A41:V/11", num="V/11", src=f"{S5} p. 92", ftype="niche (כוך)", reason="not a cave", exposure=PO, read=T5)
G2, C2 = "19020-35/14385-90", "group box (V/12-21)"
_v(12, grid=G2, cb=C2, ftype="large cave", n_open=2, open_basis="stated number (two openings)", facings="m1:NE;m2:NW",
   facing_basis="word in text: one opening 'in the north-east', the other 'in the north-west' (position words read as facing, INFERENCE; see AMENDMENT_1)",
   north="undetermined", north_basis="both openings are on the north side; no relative northing", period="no finds")
_v(13, grid=G2, cb=C2, ftype="small cave with a chimney in its ceiling", period="no finds")
X(EXCL, "A41:V/14", num="V/14", src=f"{S5} p. 92", ftype="niches (five niches, V/14-15)", reason="not a cave", exposure=PO, read=T5)
X(EXCL, "A41:V/15", num="V/15", src=f"{S5} p. 92", ftype="niches (five niches, V/14-15)", reason="not a cave", exposure=PO, read=T5)
X(EXCL, "A41:V/16", num="V/16", src=f"{S5} p. 92", ftype="natural niche", reason="not a cave", exposure=PO, read=T5)
_v(17, grid=G2, cb=C2, ftype="a space (חלל) in the group of caves and niches", c1="unknown", period="no finds")
_v(18, grid=G2, cb=C2, ftype="cave", period="no finds")
_v(19, grid=G2, cb=C2, ftype="cave", n_open=2, open_basis="stated number (two openings: one in the east, one a chimney in the ceiling)",
   facings="m1:E;m2:up", facing_basis="word in text: 'one in the east' (position word read as facing, INFERENCE); the second is a roof chimney (no azimuth)",
   north="undetermined", north_basis="one lateral opening and one roof opening", period="no finds; full of collapse; robbing signs",
   exc="surveyed; plundered")
_v(20, grid=G2, cb=C2, ftype="small cave (perhaps a Byzantine monk's cell)", period="Byzantine sherds, a nail, wood", piw="no",
   notes="A built stone wall survives in front of the cave.")
_v(21, grid=G2, cb=C2, ftype="cave", period="a piece of resin")
G3, C3 = "19005-20/14385", "group box (V/22-27)"
_v(22, grid=G3, cb=C3, ftype="elongated space with a blocked chimney (group: natural caves)", period="no finds")
_v(23, grid=G3, cb=C3, ftype="small cave", period="a small piece of leather")
_v(24, grid=G3, cb=C3, ftype="cave", period="robbing signs", exc="surveyed; plundered")
_v(25, grid=G3, cb=C3, ftype="shallow cave", period="no finds")
_v(26, grid=G3, cb=C3, ftype="large high cave", n_open=1, open_basis="singular description (its opening is wide)",
   period="Chalcolithic and Hellenistic sherds in the collapse at its opening", piw="partly", exposure="exposed-repo", src=f"{S5} p. 93")
X(EXCL, "A41:V/27", num="V/27", src=f"{S5} p. 93", ftype="several shallow niches", reason="not a cave", exposure=PO, read=T5)
_v(28, grid="19035/14375", cb="printed grid (shared by V/28-29)", ftype="natural cave", period="a few Early Roman sherds", piw="yes",
   exposure="exposed-repo", src=f"{S5} p. 93, Figs. 1-2")
_v(29, grid="19035/14375", cb="printed grid (shared by V/28-29)", ftype="natural cave", period="three non-indicative sherds in front",
   exposure="exposed-repo", src=f"{S5} p. 93, Figs. 1-2")
G4, C4 = "19025-40/14355-70", "group box (V/30-47)"
GH4 = "group of caves, spaces and niches (V/30-47; 'all natural caves'); not described"
for n in (30,):
    _v(n, grid=G4, cb=C4, ftype="small cave", period="no evidence of ancient use (group statement)", src=f"{S5} p. 93")
for n in (31, 32, 36, 37, 42, 43, 44, 45, 47):
    _v(n, grid=G4, cb=C4, ftype=GH4, c1="unknown", period="no evidence of ancient use (group statement)", src=f"{S5} pp. 93-94")
X(EXCL, "A41:V/33", num="V/33", src=f"{S5} p. 93", ftype="several shallow niches and burrows", reason="not a cave", exposure=PO, read=T5)
_v(34, grid=G4, cb=C4, ftype="three natural spaces with adjacent openings", c1="unknown", period="no evidence of ancient use (group statement)",
   src=f"{S5} p. 93", notes="Three spaces with three openings; whether one cave or three is not stated.")
_v(35, grid=G4, cb=C4, ftype="natural cave", period="sherds in front, probably from higher up the cliff", src=f"{S5} p. 93")
_v(38, grid=G4, cb="no own grid; group box (V/30-47)", ftype="cave of three wings and three levels", src=f"{S5} pp. 91, 93, Figs. 1-2; Index p. 259",
   terrace="yes", terrace_basis="a courtyard enclosed by a wall in front of the cave (חצר מוקפת חומה)",
   period="medieval textiles (by the cross-reference on p. 101); excavation results to be published separately", piw="no",
   exc="excavated (L-597; results not published here)", exposure="exposed-repo", other_ids="1993 no. 38 (Index p. 259)")
X(EXCL, "A41:V/39", num="V/39", src=f"{S5} p. 94", ftype="three niches", reason="not a cave", exposure=PO, read=T5)
_v(40, grid=G4, cb=C4, ftype="cave with a large space", terrace="yes", terrace_basis="an agricultural terrace in front (מדרגה חקלאית; date unclear)",
   period="no evidence of ancient use (group statement)", src=f"{S5} p. 94")
_v(41, grid=G4, cb=C4, ftype="cave with a large space", period="no evidence of ancient use (group statement)", src=f"{S5} p. 94")
_v(46, grid=G4, cb=C4, ftype="cave with a large space (c. 12 m across)", period="no evidence of ancient use (group statement)", src=f"{S5} p. 94")
_v(48, grid="19040/14365", cb="printed grid", ftype="hewn cave (facade collapsed)", period="two non-indicative sherds; Eisenberg (p. 120): hewn in the Second Temple period (no evidence given)",
   piw="", exposure="exposed-repo", src=f"{S5} p. 94; Eisenberg p. 120", other_ids="1993 no. 39 (Index p. 259; also printed for V/51)",
   notes="A row of three rooms parallel to the cliff; a plastered cistern; no plan.")
_v(49, grid="19035/14370", cb="printed grid", ftype="natural cave", src=f"{S5} p. 94; Eisenberg pp. 105-121, Plan 1, Figs. 1-2",
   n_open=3, open_basis="stated: the eastern hall's entrance, and in the western hall an opening through the cliff wall and a window; 'additional openings' (Eisenberg p. 105)",
   facings="m1:N;m2:N", facing_basis="plan (Eisenberg Plan 1: both mouths on the north side; repository reading, exposed)",
   pillar="yes", pillar_kind="a wide pillar (עמוד רחב)", pillar_pos="centre of the cave, dividing it into two halls", pillar_basis="Aronshtam p. 94; Eisenberg Fig. 2",
   plan="Eisenberg Plan 1 (p. 106)", period="Chalcolithic, EB IB, 1st c. BCE to the Great Revolt, medieval", piw="yes+other",
   exc="excavated (L-604, Eisenberg); plundered", exposure="exposed-repo", other_ids="1993 no. 42 ('Quruntul Cave 42')",
   notes="A built wall blocked the opening; a near miss: pillar and two halls, but three openings facing north.")
_v(50, grid="19060/14350", cb="printed grid", ftype="natural cave", src=f"{S5} pp. 96-100, Plan 2, Figs. 9-10",
   n_open=3, open_basis="stated: opening A (1.8 m) and two smaller openings B and C to its south leading to niche E",
   facings="m1:E", facing_basis="word in text: opening A faces east; B and C not stated", pillar="yes",
   pillar_kind="rock pillar (עמוד סלע), c. 0.4 m across", pillar_pos="in the entrance of niche F (interior)", pillar_basis="text p. 97",
   plan="Plan 2 (p. 97)", period="EB, Iron I-II, late Hellenistic (perhaps a refuge), 7th-8th c. CE, 12th-14th c. CE; Byzantine 1085-1092 and Mamluk coins",
   piw="partly", exc="excavated (L-596, Aronshtam)", exposure="exposed-repo", other_ids="1993 no. 13 (Index p. 259)")
GH5 = "group of natural caves and niches (V/51-56)"
_v(51, grid="19040/14345", cb="group point (V/51-56)", ftype="cave (group of natural caves and niches)", n_open=1,
   open_basis="stated (the opening, a right triangle)", period="no evidence of ancient use (group statement)", src=f"{S5} p. 94",
   notes="A rock step in front (natural).", other_ids="1993 no. 39 (Index; also printed for V/48)")
X(EXCL, "A41:V/52", num="V/52", src=f"{S5} p. 94", ftype="small niche (perhaps a collapsed cave)", reason="not a cave", exposure=PO, read=T5)
X(EXCL, "A41:V/53", num="V/53", src=f"{S5} p. 94", ftype="niche", reason="not a cave", exposure=PO, read=T5)
_v(54, grid="19040/14345", cb="group point (V/51-56)", ftype="cave", n_open=1, open_basis="stated (the cave's opening, c. 2 m, blocked by a rock)",
   period="no evidence of ancient use (group statement)", src=f"{S5} p. 94")
_v(55, grid="19040/14345", cb="group point (V/51-56)", ftype="one high narrow cave space", period="no evidence of ancient use (group statement)",
   src=f"{S5} pp. 94-95, Figs. 1, 3")
_v(56, grid="19040/14345", cb="group point (V/51-56)", ftype="oval cave space", n_open=1, open_basis="singular description (its opening, Fig. 4)",
   period="no evidence of ancient use (group statement)", src=f"{S5} pp. 94-95, Fig. 4")
_v(57, grid="19073/14345", cb="printed grid", ftype="cave of the kokhim (loculi) type, used for burial; with three niches outside",
   n_open=1, open_basis="stated (the cave's opening)", facings="cave:E", facing_basis="word in text",
   period="no finds; a later wall with a doorway and an iron door hinge; used as a fold", src=f"{S5} pp. 94-95, Figs. 1, 5")
X(EXCL, "A41:V/58", num="V/58", src=f"{S5} p. 95", ftype="building at the foot of the cliff", reason="not a cave", grid="19075/14345", exposure=PO, read=T5)
_v(59, grid="19045/14340", cb="printed grid", ftype="hanging cave", n_open=1, open_basis="stated (its opening, 4.25 m, blocked by a wall)",
   period="1st c. BCE-1st c. CE; second phase 2nd-3rd c. CE; medieval textiles", piw="yes+other", exc="excavated (L-599, Y. Peleg)",
   src=f"{S5} pp. 100-103, Plan 3, Figs. 11-12", exposure="exposed-repo", other_ids="1993 no. 20 (Index p. 259)")
G6, C6 = "19060-70/14340", "group box (V/60-64)"
for n in (60, 61, 62):
    _v(n, grid=G6, cb=C6, ftype="natural cave with one irregular space (group statement; not described)",
       period="no evidence of ancient use (group statement)", src=f"{S5} p. 95")
_v(63, grid=G6, cb=C6, ftype="elongated cave hewn in the rock", n_open=1, open_basis="stated (the opening, built of dressed stones)",
   period="a nail", src=f"{S5} p. 95")
_v(64, grid=G6, cb=C6, ftype="cave made of three burrows", n_open=3, open_basis="stated: the openings of the three burrows (Fig. 6 caption)",
   plan="Plan 1 (p. 96)", period="animal bones, iron fragment, wood", src=f"{S5} p. 96, Plan 1, Fig. 6",
   notes="Burrow 3 does not connect with the inner space; the connected cave has two openings (INFERENCE).")
G7, C7 = "19060-70/14340", "group box (V/65-68)"
_v(65, grid=G7, cb=C7, ftype="natural cave (group statement; not described)", period="no evidence of human activity (group statement)", src=f"{S5} p. 96")
_v(66, grid=G7, cb=C7, ftype="cave of two spaces (perhaps niches)", n_open=1, open_basis="stated (one common wide opening)",
   period="no evidence of human activity (group statement)", src=f"{S5} p. 96")
_v(67, grid=G7, cb=C7, ftype="rather small cave", n_open=1, open_basis="singular description (its opening, Fig. 7)",
   period="no evidence of human activity (group statement)", src=f"{S5} p. 96, Fig. 7")
_v(68, grid="19075/14340", cb="printed grid", ftype="cave", n_open=1, open_basis="stated (its built opening)",
   period="no evidence of human activity (group statement); used as a fold", src=f"{S5} p. 96, Fig. 8")
X(EXCL, "A41:V/69", num="V/69", src=f"{S5} p. 96", ftype="elongated niche", reason="not a cave", exposure=PO, read=T5)

# ------------------------------------------------------------------ Region VII
# Abeles, Region VII (eastern escarpment of Jebel Quruntul), printed pp. 123-137 (PDF p. 3 = p. 125).
# 31 caves surveyed, 16 described (p. 125, note 1). Report uses SE: 8-point. First read 04:32:11Z.
# Pages 123, 125, 135-137 were opened by an earlier worker (registration/atiqot41_region_v_extracted.md section 5).
S7 = "A41 Region VII (Abeles)"
T7 = "2026-10-11T04:32:11Z"
R(ROWS, "A41:VII/1", num="VII/1 'Mafjar Cave'", src=f"{S7} pp. 125-134, Plan 1, Figs. 2-7", lineage=LIN, grid="19080/14215",
  n_open=1, open_basis="singular description (plaster 'near the opening')", res=8, plan="Plan 1 (p. 126)",
  period="Chalcolithic, MB II, Iron, Hellenistic and Roman pottery; Early Roman glass bowls (Bar Kokhba-period parallels); candlestick bottle late 1st-2nd c. CE; Persian and Hellenistic coins; Mamluk coin",
  piw="yes+other", exc="excavated (L-611), test pits to 0.3 m", finds="pottery, glass, ring, MB scarab, metal objects, coins, textiles",
  exposure=PO, read=T7, notes="Spaces A, B and C; access by ropes and ladder from a ledge 3 m below the opening.")
R(ROWS, "A41:VII/2", num="VII/2", src=f"{S7} p. 134", lineage=LIN, grid="19070/14215", n_open=1, open_basis="stated (its opening)",
  facings="cave:E", facing_basis="word in text", res=8, period="no finds", exc="surveyed", read=T7,
  notes="Ledges/benches levelled on both sides of the opening (not a terrace in front).")
R(ROWS, "A41:VII/3", num="VII/3 'Sack Cave'", src=f"{S7} pp. 134-135, Plan 2 ('north assumed'), Fig. 8", lineage=LIN, grid="19075/14215",
  n_open=2, open_basis="stated: the main opening, and above it a burrow (opening 0.5 x 0.6 m) that 'also leads into the cave' (counted, INFERENCE)",
  res=8, north="undetermined", north_basis="the burrow opens above the main opening (vertical arrangement)", north_case="assumed (Plan 2: 'north assumed')",
  pillar="no", pillar_basis="Plan 2 (whole cave, 0-2 m scale; viewed 05:24Z) shows no pillar and the text names none (PLAN 4.3 fail rule)",
  plan="Plan 2 (p. 134), north assumed", period="Roman pottery (Herodian parallel); armour scales; coins of Valerius Gratus (17-24 CE) and Nabataean (25-106 CE)",
  piw="yes", exc="excavated (L-624)", finds="pottery, glass, armour scales, ring, nail, coins, leather-lined basket", exposure="exposed-repo", read=T7)
X(EXCL, "A41:VII/4", num="VII/4", src=f"{S7} p. 135", ftype="burrow (מחילה)", reason="not a cave by the source's type word", grid="19070/14215", exposure=PO, read=T7)
X(EXCL, "A41:VII/5", num="VII/5", src=f"{S7} p. 135", ftype="burrow (מחילה)", reason="not a cave by the source's type word", grid="19075/14215", exposure=PO, read=T7)
R(ROWS, "A41:VII/6", num="VII/6", src=f"{S7} p. 135", lineage=LIN, grid="19075/14215", n_open=1, open_basis="stated (the cave's opening)",
  facings="cave:S", facing_basis="word in text", res=8, period="no finds", exc="surveyed", exposure=PO, read=T7)
R(ROWS, "A41:VII/7", num="VII/7", src=f"{S7} pp. 135-136", lineage=LIN, grid="19080/14220", n_open=1, open_basis="stated (the cave's opening)",
  facings="cave:SE", facing_basis="word in text", res=8, period="no finds; sheep pen", exc="surveyed", exposure=PO, read=T7)
R(ROWS, "A41:VII/8", num="VII/8", src=f"{S7} p. 136", lineage=LIN, grid="19085/14225", n_open=1, open_basis="singular description (a narrow burrow leads to the space)",
  res=8, period="no finds", exc="surveyed", exposure=PO, read=T7)
R(ROWS, "A41:VII/9", num="VII/9 (caves and burrows)", src=f"{S7} p. 136", lineage=LIN, kind="cluster", cluster=None, ftype="several cave openings (caves and burrows)",
  grid="19085/14225", res=8, period="bones, textiles, leather, rope (unprocessed; undated)", exc="surveyed", exposure=PO, read=T7,
  notes="Cluster record: 'several cave openings' on a ledge; count not stated.")
X(EXCL, "A41:VII/10", num="VII/10", src=f"{S7} p. 136", ftype="burrow (מחילה)", reason="not a cave by the source's type word", grid="19090/14225", exposure=PO, read=T7)
R(ROWS, "A41:VII/11", num="VII/11", src=f"{S7} p. 136", lineage=LIN, ftype="narrow long cave (heading: caves)", grid="19090/14245", n_open=1,
  open_basis="stated (the cave's opening, at the west end of its long south side)", res=8,
  terrace="yes", terrace_basis="a roofed platform (רחבה מקורה) in front, perhaps roofed in antiquity", period="no finds (test pits to rock)",
  exc="sounded (test pits)", exposure="exposed-repo", read=T7)
R(ROWS, "A41:VII/undescribed", num="VII: 15 undescribed caves (eight openings at c. 210 m north of VII/11 and seven more around the cliff)",
  src=f"{S7} pp. 125 (note 1), 136", lineage=LIN, kind="cluster", cluster=15, ftype="caves (surveyed, not described)", grid="19090/14240",
  cbasis="printed grid of the cliff north of VII/11", res=8, period="", exc="surveyed", read=T7,
  notes="31 caves surveyed, 16 described; INFERENCE: the 'eight openings and seven more caves' are the 15 undescribed caves.")
X(EXCL, "A41:VII/12", num="VII/12", src=f"{S7} p. 136", ftype="burrow (מחילה)", reason="not a cave by the source's type word", grid="19090/14235", exposure="exposed-repo", read=T7)
R(ROWS, "A41:VII/13", num="VII/13", src=f"{S7} p. 136", lineage=LIN, grid="19090/14245", n_open=1, open_basis="stated (its opening)",
  facings="cave:S", facing_basis="word in text", res=8, period="no finds", exc="surveyed", exposure=PO, read=T7)
R(ROWS, "A41:VII/14", num="VII/14", src=f"{S7} p. 136", lineage=LIN, grid="19085/14225", n_open=1, open_basis="stated (the cave's opening)",
  facings="cave:S", facing_basis="word in text", res=8, period="no finds", exc="sounded (to rock at one point)", exposure=PO, read=T7,
  notes="A vertical winding shaft 8 m deep joins two levels.")
R(ROWS, "A41:VII/15", num="VII/15", src=f"{S7} p. 136", lineage=LIN, grid="19095/14240", cbasis="printed grid (shared by VII/15-16)", res=8,
  period="no finds; used recently by the monks of Deir Quruntul (Arabic inscription on a lintel)", exc="excavated (no finds)", exposure="exposed-repo", read=T7)
R(ROWS, "A41:VII/16", num="VII/16", src=f"{S7} p. 136", lineage=LIN, grid="19095/14240", cbasis="printed grid (shared by VII/15-16)", res=8,
  period="no finds; used recently by the monks", exc="excavated (no finds)", exposure="exposed-repo", read=T7)

# ------------------------------------------------------------------ Region VIII
# Eshel and Zissu, Region VIII (cliff slopes of trig. point 86, Jebel Mughr el-Bas, 'Ketef Yeriho'), printed pp. 139-150;
# Table 1 pp. 142-148 (read from the page images: the text layer drops the table's number column). "More than fifty cave
# openings, niches and clefts" examined (p. 141). Eshel and Zissu, 'The Excavation of Cave VIII/9', pp. 151-? (file 12).
# No facing words used: 4-point. First read 04:33:04Z (Region VIII), 04:34:19Z (VIII/9 report).
S8 = "A41 Region VIII (Eshel and Zissu), Table 1"
T8 = "2026-10-11T04:33:04Z"
T8b = "2026-10-11T04:34:19Z"


def _e(n, grid, **kw):
    kw.setdefault("exc", "surveyed")
    R(ROWS, f"A41:VIII/{n}", num=kw.pop("num", f"VIII/{n}"), src=kw.pop("src", f"{S8} p. 142"), lineage=LIN, grid=grid, res=4,
      read=kw.pop("read", T8), **kw)


def _ex(n, ftype, grid="", page="145"):
    X(EXCL, f"A41:VIII/{n}", num=f"VIII/{n}", src=f"{S8} p. {page}", ftype=ftype, reason="not a cave", grid=grid, read=T8)


_e(1, "19113/14220", ftype="an oval opening to an irregular space (no type word)", c1="unknown", n_open=1, open_basis="stated (an oval opening)",
   period="no finds")
_e(2, "19093/14211", num="VIII/2 'Cave of the Crosses'", ftype="cave", n_open=1, open_basis="stated (the cave's opening, 5 x 2 m)",
   plan="Plan 1 (p. 142 table ref.)", period="Byzantine sherds; plaster decorated with crosses", piw="no",
   notes="First examined in 1979 by the Cave Research Center (Frumkin).")
_e(3, "19080/14220", ftype="two shallow spaces, probably connected (no type word)", c1="unknown", n_open=2,
   open_basis="stated: their openings (plural) are irregular; two spaces 'probably connected' (INFERENCE: one cavity with two openings)",
   period="no finds")
_ex(4, "natural niche", "19119/14221", "142")
_ex(5, "three natural niches", "19083/14209", "142")
_e(6, "19092/14209", num="VIII/6 'Chimneys Cave'", ftype="karstic cave", src=f"{S8} pp. 142, 148-149, Plan 5, Figs. 1-2",
   n_open=1, open_basis="stated (its opening, with a built fence)", plan="Plan 5 (p. 148)",
   period="Chalcolithic, Hellenistic and Early Roman sherds; coins of Ptolemy II and of Geba (129/30 CE); human bones", piw="yes+other",
   exc="excavated (under the survey permit, per the Index)", notes="Connected by karstic shafts to hall R of VIII/9.")
_e(7, "19095/14209", num="VIII/7 'Beam Cave'", ftype="natural space enlarged by cutting", src=f"{S8} pp. 142-143, Plan 2, Fig. 1",
   n_open=1, open_basis="singular description (the opening, blocked by a wall with a wooden beam; 'and the window?')", plan="Plan 2 (p. 143)",
   period="no finds")
_e(8, "19099/14220", ftype="natural oval cave", period="no finds")
R(ROWS, "A41:VIII/9", num="VIII/9 'Large Caves Complex' ('Spies' Caves', Frumkin)", src=f"{S8} p. 142; Eshel and Zissu, A41 pp. 151-? (Plans 1-2, Figs. 1-12)",
  lineage=LIN, ftype="complex of natural caves (halls B-H, R)", grid="19094/14208", n_open=None,
  open_basis="the openings are side by side at one level (paraphrase; plural, number not stated)", res=4,
  plan="Plan 2 (p. 152), plan and sections", period="Chalcolithic, EB, Hellenistic coin and papyri, Early Roman cooking pot, two Hadrian coins and papyri, Byzantine, medieval",
  piw="yes+other", exc="excavated (three areas)", finds="papyri, textiles, coins, human bones", read=T8b,
  notes="A wide natural step in front carries a path to Deir Quruntul (natural; not a terrace).")
R(ROWS, "A41:VIII/10", num="VIII/10 'Avior Cave'", src=f"{S8} p. 145; Eshel and Zissu, A41 p. 151", lineage=LIN, ftype="cave",
  grid="19094/14208", cbasis="printed as 'as VIII/9'", n_open=1, open_basis="singular description (the opening of cave VIII/10, Fig. 1 caption)", res=4,
  period="excavated 1986: papyri (one names Avior), 38 skeletons, a wooden comb like those dated to the end of the Bar Kokhba revolt, Chalcolithic and EB I pottery, glass",
  piw="yes+other", exc="excavated (1986)", read=T8b)
_ex(11, "horizontal natural cleft with two niches", "19119/14220")
_ex(12, "two natural niches", "19083/14206")
_ex(13, "vertical natural cleft")
_ex(14, "natural niche", "19095/14206")
_ex(15, "natural niche")
_e(16, "19096/14224", ftype="natural cave", src=f"{S8} p. 145", period="no finds")
_ex(17, "natural niche", "19078/14203")
_ex(18, "shallow natural niche", "19080/14202")
_ex(19, "horizontal natural cleft", "19081/14202")
_e(20, "19084/14203", ftype="shallow natural space (no type word)", c1="unknown", src=f"{S8} p. 145", period="no finds")
_ex(21, "three natural niches", "19083/14203")
_e(22, "19084/14202", ftype="not examined (access); listed in the table of caves", c1="unknown", src=f"{S8} p. 145", exc="not examined")
_e(23, "19085/14201", ftype="not examined (access); listed in the table of caves", c1="unknown", src=f"{S8} p. 145", exc="not examined")
_ex(24, "three natural niches", "19099/14205")
_ex(25, "horizontal natural cleft (a decorated medieval silver piece beside it)", "19100/14202")
_ex(26, "shallow natural niche (a Jannaeus coin below it)", "19102/14201")
_e(27, "19106/14203", num="VIII/27 'the balcony of the Cave of the Sandal'", ftype="natural cave, perhaps enlarged by cutting", src=f"{S8} pp. 146, 148, Fig. 3",
   n_open=1, open_basis="stated (an opening c. 2 m wide)", period="rope fragment, iron arrowhead; human bones of two individuals on the step in front (undated)",
   notes="A natural rock step in front (the source's 'balcony'); natural, so not a terrace under PLAN 4.3.")
_e(28, "19106/14203", num="VIII/28 'Cave of the Sandal'", ftype="cave", src=f"{S8} p. 146, Figs. 2-3 (refers to Eshel and Zissu 1999; DJD 38)",
   cbasis="printed as 'as VIII/27'", period="MB II and Early Roman metal objects (Part 2 title); documents and finds of the Bar Kokhba period (Eshel and Zissu 1999; Zissu 2023)",
   piw="yes+other", exc="excavated (reported elsewhere)", exposure="exposed-repo",
   notes="Opening count and facing not given in this record (relevant to chain link S2430-2).")
_e(29, "19109/14205", num="VIII/29 'Cave of the Prutah'", ftype="small cave", src=f"{S8} pp. 146, 149",
   n_open=2, open_basis="stated number: a northern opening (towards the step below VIII/28) and a southern opening (to the cliff)",
   north="decided", north_basis="the source names a northern and a southern opening",
   period="EB and Early Roman sherds; prutah of year 2 of the Great Revolt (67/8 CE)", piw="yes+other", exc="sounded (1.5 x 1.5 m test square)",
   exposure="exposed-repo", notes="No compass facing for either opening (relevant to chain link S2430-2).")
_e(30, "19076/14202", ftype="natural cave", src=f"{S8} p. 146", n_open=1, open_basis="stated (its oval opening)", period="no finds")
_ex(31, "elongated natural niche", "19067/14198", "146")
_ex(32, "two natural clefts", "19067/14196", "146")
_e(33, "19111/14183", ftype="cave", src=f"{S8} p. 147", n_open=1, open_basis="stated (the cave's opening, walled)", period="a little organic and modern material")
_e(34, "19106/14175", ftype="small natural cave", src=f"{S8} p. 147", period="no finds")
_e(35, "19103/14177", ftype="cave", src=f"{S8} p. 147", n_open=1, open_basis="stated (the cave's wide opening, narrowed by a modern wall)", period="modern finds")
_e(36, "19102/14172", ftype="natural irregular cave", src=f"{S8} p. 147", n_open=2, open_basis="stated number (it has two openings)", period="no finds")
_ex(37, "three vertical clefts with one common opening", "19106/14170", "147")
_e(38, "19102/14168", ftype="natural cave", src=f"{S8} p. 147", n_open=1, open_basis="stated (its wide opening)", period="no finds")
for n, g in ((39, "19101/14162"), (40, "19099/14162"), (41, "19097/14160"), (43, "19101/14157"), (44, "19086/14152")):
    _ex(n, "natural niche(s)", g, "147")
_ex(42, "shallow natural cell (0.5 m)", "19101/14102", "147")
_ex(45, "vertical natural cleft", "19089/14152", "147")
_e(46, "19084/14150", ftype="natural cave (lower of two)", src=f"{S8} pp. 147, 149 (Y11 in the excavation)",
   n_open=2, open_basis="stated number: a wide opening and a second narrow opening in its ceiling", period="a hand-made nail and coarse textile; no evidence of human presence",
   exc="sounded (test trench L53, L-600)")
_e(47, "19088/14151", ftype="natural cave", src=f"{S8} pp. 148, 150 (Y10 in the excavation)", n_open=2, open_basis="stated number (it has two openings)",
   period="two sherds, textiles, bones (animal activity)", exc="sounded (L50, L51)",
   notes="An almost level, nearly rectangular rock step below the opening (natural; not a terrace).")
_e(48, "19095/14149", ftype="natural cave", src=f"{S8} p. 148", n_open=1, open_basis="stated (an irregular opening)", period="no finds")
_ex(49, "natural niche with a round opening", "", "148")
_ex(50, "natural niche", "19094/14145", "148")

# ------------------------------------------------------------------ Region IX
# Weiss, Region IX (southern part of Jebel Quruntul, north of Wadi Qelt), printed pp. 169-172; Table 1 p. 171 (read from the
# page image). 22 rock shelters and caves examined; only IX/14 had ancient finds and was excavated (p. 171).
# No facing words: 4-point. First read 04:35:06Z. IX/9, IX/10, IX/17, IX/21 and IX/22 are named in the Kohlit chain
# (research/assessments/kohlit_chain/chain.json) as 'natural caves, no finds' (via WBADB): exposed-repo.
S9 = "A41 Region IX (Weiss), Table 1"
T9 = "2026-10-11T04:35:06Z"


def _w(n, grid, **kw):
    kw.setdefault("exc", "surveyed")
    kw.setdefault("period", "no finds")
    R(ROWS, f"A41:IX/{n}", num=f"IX/{n}", src=kw.pop("src", f"{S9} p. 171"), lineage=LIN, grid=grid, res=4, read=T9, **kw)


_w(1, "19090/14110", ftype="natural oval cave")
_w(2, "19086/14103", ftype="natural cave", period="a few non-indicative sherds")
X(EXCL, "A41:IX/3", num="IX/3", src=f"{S9} p. 171", ftype="rock shelter", reason="not a cave (rock shelter)", grid="19086/14105", read=T9)
X(EXCL, "A41:IX/4", num="IX/4", src=f"{S9} p. 171", ftype="natural niche", reason="not a cave", grid="19086/14085", read=T9)
_w(5, "19084/14083", ftype="burial cave (blocked; plan unclear)", period="several ossuary fragments outside the cave (no date stated)",
   exc="sounded (a section and a metal-detector check)")
X(EXCL, "A41:IX/6", num="IX/6", src=f"{S9} p. 171", ftype="natural niche", reason="not a cave", grid="19082/14081", read=T9)
_w(7, "19116/14079", ftype="natural cave")
_w(8, "19114/14071", ftype="hewn burial cave, deliberately blocked; remains of four burial kokhim", period="no finds")
X(EXCL, "A41:IX/9", num="IX/9", src=f"{S9} p. 171", ftype="natural niche (כוך טבעי), 1 x 1 m", reason="not a cave", grid="19112/14062",
  exposure="exposed-repo", read=T9, notes="The Kohlit chain lists IX/9 as a natural cave (from WBADB); the source's table calls it a natural niche.")
_w(10, "19110/14050", ftype="natural cave of two spaces (a burrow and a hall)", period="no finds (two test trenches)", exc="sounded (two test trenches)",
   exposure="exposed-repo")
_w(11, "19079/14045", ftype="natural cave")
X(EXCL, "A41:IX/12", num="IX/12", src=f"{S9} p. 171", ftype="natural rock shelter", reason="not a cave (rock shelter)", grid="19109/14023", read=T9)
X(EXCL, "A41:IX/13", num="IX/13", src=f"{S9} p. 171", ftype="rock shelter", reason="not a cave (rock shelter)", grid="19062/14032", read=T9)
_w(14, "19072/14017", ftype="natural cave", src=f"{S9} pp. 171-172, Plan 1", n_open=1, open_basis="stated (a wide opening leads to the cave)",
   plan="Plan 1 (p. 172)", period="non-indicative sherds; activity mainly MB II, a little Iron Age", piw="no", exc="excavated (one locus, under the survey permit)")
X(EXCL, "A41:IX/15", num="IX/15", src=f"{S9} p. 171", ftype="natural rock shelter", reason="not a cave (rock shelter)", grid="19039/14021", read=T9)
X(EXCL, "A41:IX/16", num="IX/16", src=f"{S9} p. 171", ftype="natural elongated niche", reason="not a cave", grid="19045/14023", read=T9)
_w(17, "19102/14023", ftype="natural shallow cave", exposure="exposed-repo")
X(EXCL, "A41:IX/18", num="IX/18", src=f"{S9} p. 171", ftype="natural rock shelter (a few non-indicative sherds)", reason="not a cave (rock shelter)", grid="19042/14009", read=T9)
X(EXCL, "A41:IX/19", num="IX/19", src=f"{S9} p. 171", ftype="natural elongated niche", reason="not a cave", grid="19074/14002", read=T9)
X(EXCL, "A41:IX/20", num="IX/20", src=f"{S9} p. 171", ftype="natural rock shelter with one space", reason="not a cave (rock shelter)", grid="19045/13987", read=T9)
_w(21, "19062/13980", ftype="natural shallow rectangular cave", exposure="exposed-repo")
_w(22, "19081/13992", ftype="natural shallow cave", exposure="exposed-repo")

# ------------------------------------------------------------------ Region X
# Yattah, Kam and Ben-Haim, Region X (fault escarpment south of Almog junction and west of Kalia, north of Nahal Qumran,
# between OIG northings 131.5 and 129.0), printed pp. 173-186; Table 1 pp. 175-178 (read from the page images).
# 'About 61 cave openings, all natural' (p. 175); 1952 caves could not be re-identified and were renumbered; Patrich's
# 1984-85 survey unpublished. No facing words: 4-point. First read 04:35:50Z.
# CAUTION (INFERENCE): on p. 176 the right-hand columns (opening size, type, notes) are printed one row below their
# cave: the names of X/35 and X/42, which the text and figure captions fix, stand in rows 36 and 43. Per-row sizes and
# notes on p. 176 are therefore not used; the grid column is used. On p. 178 the names of X/51, X/55, X/57, X/59 and X/60
# stand in their own rows; the first note on p. 178 ('two caves excavated by Vendyl Jones') stands in row 48 but WBADB
# S3703 names 'Two Caves X/47' (Kohlit Stage 2 packet E754), so it is assigned to X/47 with a flag.
S10 = "A41 Region X (Yattah, Kam and Ben-Haim), Table 1"
T10 = "2026-10-11T04:35:50Z"
GX = {5: "19204/13193", 6: "19212/13088", 7: "19208/13085", 8: "19205/13083", 9: "19395/13079", 10: "19399/13079",
      11: "19388/13082", 12: "19338/13053", 13: "19339/13078", 14: "19386/13064", 15: "19374/13085", 16: "19381/13066",
      17: "19309/13065", 18: "19310/13062", 19: "19311/13054", 20: "19313/13054", 21: "19322/13055", 22: "193218/130518",
      23: "19371/13083", 24: "19395/13064", 25: "19326/13044", 26: "19364/13085", 27: "19371/13064", 28: "19327/13039",
      29: "19315/13033", 30: "19325/13036", 31: "19363/13078", 32: "19359/13064", 33: "19375/13020", 34: "19375/13020",
      35: "19380/13015", 36: "19355/13071", 37: "19354/13070", 38: "19380/12995", 39: "19356/13062", 40: "19346/13073",
      41: "19340/13083", 42: "19337/13053", 43: "19335/12971", 44: "19341/12970", 45: "19334/13077", 46: "19373/13082",
      47: "19330/12954", 48: "19339/12949", 49: "19328/13059", 50: "19337/12937", 51: "19340/13050", 52: "19391/12942",
      53: "19382/12942", 54: "19374/12935", 55: "19327/13064", 56: "19326/13080", 57: "19325/13025", 58: "19393/12935",
      59: "19381/12935", 60: "19333/13071", 61: "19380/12910"}
CAVE_X = "cave opening in the table of caves ('about 61 cave openings, all natural', p. 175); no individual description"
for n in range(1, 5):
    X(EXCL, f"A41:X/{n}", num=f"X/{n}", src=f"{S10} p. 175", ftype="niche (כוך)", reason="not a cave",
      grid="19280/13122" if n == 1 else "", read=T10)
SPECIAL = {35, 42, 47, 51, 55, 57, 59, 60}
for n in range(5, 62):
    if n in SPECIAL:
        continue
    page = "175" if n <= 11 else ("176" if n <= 47 else "178")
    kw = {}
    if n in (44, 45):
        kw["notes"] = "The note 'three adjacent caves near the southern border of Region XI' is printed in row 45 on p. 176, where the columns are offset; it probably belongs to X/44 (N 129.70, nearer that border) (INFERENCE)."
    if n in (36, 37):
        kw["notes"] = "X/37 and X/42 have spoil heaps with many sherds, probably from Patrich's excavation (p. 175)." if n == 37 else "Fig. 4 shows the openings of X/35, X/36 and X/51."
    if n == 48:
        kw["notes"] = "Row 48 carries the note 'two caves excavated earlier by Vendyl Jones and surveyed now'; assigned to X/47 (see header)."
    R(ROWS, f"A41:X/{n}", num=f"X/{n}", src=f"{S10} p. {page}", lineage=LIN, ftype=CAVE_X, grid=GX[n], res=4,
      period="", exc="surveyed", read=T10, **kw)
R(ROWS, "A41:X/35", num="X/35 'Balsam Oil Juglet Cave' = Patrich and Arubas Cave 13 ('Q3')",
  src=f"{S10} pp. 176-182, Plan 1, Figs. 3-4, 9-11; Patrich and Arubas, IEJ 39 (1989) pp. 43-59 (repository: salvage records S13)",
  lineage=LIN + "; Patrich and Arubas 1988 excavation", ftype="natural cave", grid=GX[35],
  n_open=1, open_basis="singular description ('the opening of cave X/35', Fig. 9; Patrich and Arubas: one opening 5.5 x 1.8 m)",
  facings="cave:E", facing_basis="word in text: Patrich and Arubas p. 43, 'faces east' (repository salvage record S13; exposed)", res=4,
  plan="Plan 1 (p. 180)", period="Chalcolithic, Iron and Early Roman (Patrich and Arubas); 2nd c. CE lamps, a prutah of year 2 of the revolt (67 CE); Roman, Early Islamic and medieval textiles",
  piw="yes+other", exc="excavated (Patrich and Arubas 1988; L-640, 1993)", finds="juglet of oil (1988), lamps, coin, textiles, ropes",
  exposure="exposed-repo", read=T10, other_ids="Patrich and Arubas 1989 Cave 13 (Q3); perhaps 1952 cave 2 (Patrich and Arubas p. 44 n. 3, hedged)",
  notes="Identity with Patrich and Arubas Cave 13 is stated by the source (p. 180). The hedged identity with 1952 cave 2 is flagged, not merged.")
R(ROWS, "A41:X/42", num="X/42 'Rock Cave'", src=f"{S10} pp. 176, 182, Fig. 12", lineage=LIN, ftype="cave", grid=GX[42],
  n_open=1, open_basis="singular description (the ceiling collapse almost blocked the cave's opening)", res=4,
  period="a few non-indicative sherds (perhaps Roman); textile and leather; a modern coin", piw="partly",
  exc="excavated (L-639; trench to c. 2 m); earlier digging probably by Patrich", read=T10)
R(ROWS, "A41:X/47", num="X/47 (two caves dug by Vendyl Jones; assignment flagged)", src=f"{S10} pp. 176, 178 (note 2), Fig. 8; WBADB S3703 'Two Caves X/47'",
  lineage=LIN, kind="cluster", cluster=2, ftype="two caves excavated earlier by Vendyl Jones, surveyed in 1993", grid=GX[47], res=4,
  period="", exc="excavated by V. Jones (unpublished; 'exposed by him for many years', large spoil heap at its opening)", read=T10, exposure="exposed-repo",
  notes="INFERENCE: probably the Twin Cave / Jones's 'Cave of the Column' (salvage records S09, S15). The record names no Twin Cave, Bar-Adon or 1952 number, so it is not merged and is silent for Twin Cave under the aspect rule (A1). Printed in row 48 (p. 178); WBADB gives X/47.")
R(ROWS, "A41:X/51", num="X/51 'Hides Cave'", src=f"{S10} pp. 178, 182-183, Plan 2, Figs. 4, 13-15", lineage=LIN, ftype="cave", grid=GX[51],
  n_open=2, open_basis="stated number (the cave has two openings; the wide one 6 m)", res=4, plan="Plan 2 (p. 183)",
  period="processed hides incl. sandal parts and thin writing leather; non-indicative sherds; a trilobate bronze arrowhead 'of the Roman period', like Bar Kokhba arrowheads from the Cave of Letters",
  piw="partly", exc="excavated (L-637; trenches, not to bedrock)", finds="hides, leather, arrowhead, chain", read=T10,
  pillar_kind="Plan 2 draws a free-standing bedrock mass (c. 2.4 x 4 m) beside the wide opening, between it and a narrow gap to the south",
  pillar_basis="not coded: the text names no pillar and says collapses filled most of the cave; a drawn rock mass is not a reported pillar (strict reading; near miss, see AMENDMENT_1)",
  notes="Used recently as a hyena feeding station (bones at the opening). Entry was possible only through the wide opening (text). Fig. 13 shows the opening 'looking north'. Plan 2 viewed 05:25Z.")
R(ROWS, "A41:X/55", num="X/55 'Goats Cave' (heading: rock shelter)", src=f"{S10} pp. 178, 183, Figs. 16-17", lineage=LIN,
  ftype="rock shelter (heading); 'cave' in the table and nickname", grid=GX[55], res=4, period="no finds", exc="sounded (3 x 3 m test square outside)",
  c1="unknown", read=T10)
R(ROWS, "A41:X/57", num="X/57 'Threads Cave'", src=f"{S10} pp. 178, 183-184, Plan 3, Fig. 18", lineage=LIN, ftype="elongated cave", grid=GX[57],
  n_open=1, open_basis="stated (the opening, 4 x 1.5 m)", res=4, plan="Plan 3 (p. 184)",
  period="textiles, threads, ropes; a Byzantine coin of 402-408 CE near the opening; a spearhead", piw="no", exc="excavated (L-616; trench)", read=T10)
R(ROWS, "A41:X/59", num="X/59 'John's Cave'", src=f"{S10} pp. 178, 184-185, Fig. 19", lineage=LIN, ftype="cave: a triangular rock shelter leading to a smaller inner space",
  grid=GX[59], res=4, period="a few non-indicative, probably ancient sherds; organic finds; a modern hermit's belongings", exc="sounded (two test squares and a trench)",
  read=T10)
R(ROWS, "A41:X/60", num="X/60 'Button Cave'", src=f"{S10} pp. 178, 185, Plan 5, Fig. 20", lineage=LIN, ftype="cave (front collapsed)", grid=GX[60], res=4,
  plan="Plan 5 (p. 185)", period="Roman and Byzantine jars and jugs; human bones; used in the Roman period (authors)", piw="partly",
  exc="excavated (one day, Nahlieli and Lander)", read=T10, notes="Entered through a breach in the ceiling; the original plan of the front is unknown.")

# ------------------------------------------------------------------ Region XI
# Baruch, Mazor and Sandhaus, Region XI (fault escarpment above Horbat Qumran, from the stream below Jaufat Zabin, near
# grid line 129, to Nahal Qumran), printed pp. 187-198. 22 natural caves located (p. 189); earlier de Vaux and
# Patrich-Arubas caves could not be re-identified except XI/19 (= 1952 cave 19 = 2Q) and, hedged, XI/20 (= cave 20).
# Only 'east' is used as a facing word: 4-point. Pages 187, 189 and 195-198 were opened by an earlier worker
# (registration/atiqot41_region_v_extracted.md section 5). First read here 04:38:32Z.
S11 = "A41 Region XI (Baruch, Mazor and Sandhaus)"
T11 = "2026-10-11T04:38:32Z"
X(EXCL, "A41:XI/1", num="XI/1", src=f"{S11} p. 189, Fig. 1", ftype="rock shelter", reason="not a cave (rock shelter)", grid="19340/12930", exposure=PO, read=T11)
for n, kw in ((2, dict(n_open=1, open_basis="stated (its opening, 0.8 x 0.8 m)", period="no finds")),
              (3, dict(n_open=1, open_basis="stated (the opening, 0.9 x 2 m)", period="recent dung only")),
              (4, dict(n_open=1, open_basis="stated (the opening, 7 x 3 m)", period="non-indicative sherds", exc="sounded (1 x 1 m test square)")),
              (5, dict(n_open=1, open_basis="stated (its opening, 3 x 1.5 m)", period="an animal bone; otherwise sterile", exc="sounded (test pit)"))):
    kw.setdefault("exc", "surveyed")
    R(ROWS, f"A41:XI/{n}", num=f"XI/{n} (one of four caves XI/2-5)", src=f"{S11} p. 189", lineage=LIN, grid="19340/12920",
      cbasis="group centre (XI/2-5)", res=4, exposure=PO, read=T11, other_ids="WBADB S3770 'Four Caves XI/2-5' (Kohlit Stage 2 packet)", **kw)
R(ROWS, "A41:XI/6", num="XI/6 (cave and burrow)", src=f"{S11} pp. 189-190, Plan 1, Figs. 2-3", lineage=LIN, grid="19350/12900",
  n_open=1, open_basis="stated (the cave's opening, blocked by an arc-shaped wall)", res=4,
  terrace="yes", terrace_basis="a courtyard in front bounded by a fence of large fieldstones (c. 12 m) (חצר, תחומה בגדרה); pens with retaining walls (p. 189)",
  plan="Plan 1 (p. 190)", period="Early Roman jars: a 'scroll jar' rim (Hasmonean to Herodian) and a jar of the 1st c. CE", piw="yes",
  exc="excavated (L-644; two test squares)", read=T11)
R(ROWS, "A41:XI/7", num="XI/7", src=f"{S11} p. 191", lineage=LIN, grid="", where="lower cliff above Horbat Qumran, north of burrow XI/8 (Region XI)",
  ftype="cave of which only a rock shelter remains after the ceiling collapsed", c1="unknown", res=4,
  period="a few non-indicative sherds; animal bones", exc="surveyed", read=T11)
X(EXCL, "A41:XI/8", num="XI/8", src=f"{S11} p. 191", ftype="burrow (מחילה)", reason="not a cave by the source's type word", read=T11)
R(ROWS, "A41:XI/9", num="XI/9", src=f"{S11} p. 191, Fig. 4", lineage=LIN, grid="19350/12880", res=4,
  period="recent dung only", exc="surveyed", read=T11,
  notes="A small entrance hall; a narrow entrance in its back wall leads through a winding burrow to a large space (7 m2). Exterior openings not counted.")
R(ROWS, "A41:XI/10", num="XI/10", src=f"{S11} pp. 191-192, Plan 2, Figs. 5-7", lineage=LIN, ftype="natural cave in conglomerate", grid="19345/12875",
  n_open=1, open_basis="stated (its large wide opening)", facings="cave:E", facing_basis="word in text ('צופה מזרחה', looks east)", res=4,
  terrace="yes", terrace_basis="an ancient stone fence outside the cave, north and east (Figs. 5-6); pens with retaining walls in front (p. 189)",
  plan="Plan 2 (p. 191)", period="Chalcolithic (Wadi Rabah) and Early Roman (jarlet 1st c. BCE-1st c. CE; Second Temple bottle); 'perhaps a group of Essenes' (authors)",
  piw="yes+other", exc="excavated (L-660, Y. Zelinger)", read=T11,
  notes="Opposite Kibbutz Kalia, c. 0.5 km north of Horbat Qumran, at the foot of the cliff.")
R(ROWS, "A41:XI/11", num="XI/11", src=f"{S11} p. 192", lineage=LIN, grid="19348/12872", cbasis="group centre (XI/11-12)", res=4,
  period="no finds", exc="surveyed", read=T11, notes="Its opening is destroyed; dimensions not determinable.")
X(EXCL, "A41:XI/12", num="XI/12", src=f"{S11} p. 192", ftype="crevice (נקיק)", reason="not a cave", grid="19348/12872", read=T11)
R(ROWS, "A41:XI/13", num="XI/13", src=f"{S11} pp. 192-193, Plan 3, Fig. 8", lineage=LIN, grid="19340/12870", n_open=1,
  open_basis="singular description ('in the area of the opening')", res=4, plan="Plan 3 (p. 193)",
  period="Early Roman sherds incl. a bowl of a type common in the Hasmonean palace at Jericho; modern items", piw="yes",
  exc="excavated fully to sterile marl (L-642, per the Index)", read=T11, notes="Cutting marks on the walls.")
R(ROWS, "A41:XI/14", num="XI/14", src=f"{S11} p. 193, Plan 4", lineage=LIN, grid="19340/12870", n_open=1,
  open_basis="stated (its opening, wide and low)", res=4, plan="Plan 4", period="no finds", exc="sounded (test square at the opening, L-641)", read=T11)
R(ROWS, "A41:XI/15", num="XI/15", src=f"{S11} pp. 193-194, Fig. 9", lineage=LIN, grid="19348/12868", res=4,
  period="Early Roman sherds (cooking pot of the late 1st c. BCE-1st c. CE type); an EB jar", piw="yes+other",
  exc="sounded (test square, L-641); earlier digging (spoil in front)", read=T11, notes="Collapsed cave.")
R(ROWS, "A41:XI/16", num="XI/16", src=f"{S11} p. 194, Plan 5, Fig. 10", lineage=LIN, grid="19346/12860", n_open=1,
  open_basis="stated (a narrow tall opening)", res=4, plan="Plan 5 (p. 194)", period="Early Roman cooking pot; worked bone(?); textiles",
  piw="yes", exc="cleaned (a cut cell); earlier digging (spoil in front)", read=T11)
X(EXCL, "A41:XI/17", num="XI/17", src=f"{S11} p. 194", ftype="burrow (מחילה), no exact grid", reason="not a cave by the source's type word", read=T11)
R(ROWS, "A41:XI/18", num="XI/18", src=f"{S11} pp. 194-195, Plan 6, Figs. 11-12", lineage=LIN, grid="19345/12851", n_open=1,
  open_basis="stated (its opening, 1.2 x 0.7 m, blocked by collapse)", res=4, plan="Plan 6 (p. 194)",
  period="a Roman lid-bowl of the type used to cover 'scroll jars' (Hasmonean and Herodian parallels at Jericho)", piw="yes",
  exc="excavated fully to 0.7 m, not to bedrock (L-605, per the Index)", exposure=PO, read=T11,
  notes="Below cave Q2 excavated by de Vaux (XI/19). Named in the Kohlit chain (link QUMRAN-1) without its content.")
R(ROWS, "A41:XI/19", num="XI/19 = 1952 cave 19 = 2Q", src=f"{S11} pp. 195-196, Plan 7, Figs. 11, 13", lineage=LIN,
  ftype="large cave, two storeys", grid="19343/12391", coord_ok=False, where="centre of the lower fault cliff above Horbat Qumran (Region XI); Map XI near N 128.9", cbasis="printed grid (evidently a misprint: Map XI plots it near N 128.9; see notes)",
  n_open=1, open_basis="stated (the cave's opening leads to the lower storey)", res=4, plan="Plan 7 (p. 196)",
  period="Early Roman sherds from earlier spoil ('scroll jar', lid-bowl, cooking pot)", piw="yes", exc="excavated before (1952); niches and corridor cleaned (L-606)",
  exposure="exposed-repo", read=T11, other_ids="DJD3:19 (stated: identified from old photographs as Baillet-Milik-de Vaux cave 19)",
  notes="MERGE: same cave as DJD III site 19 (2Q), by the source's statement.")
R(ROWS, "A41:XI/20", num="XI/20 (perhaps 1952 cave 20)", src=f"{S11} pp. 196-197, Fig. 14", lineage=LIN, ftype="natural cave", grid="19335/12838",
  n_open=1, open_basis="stated (a wide high opening)", res=4,
  period="Early Roman sherds outside the opening; a 14th-c. Mamluk jug at a hearth in the opening", piw="yes+other",
  exc="excavated (L-606; not to bedrock)", exposure="exposed-repo", read=T11,
  other_ids="perhaps DJD3:20 ('it seems this cave should be identified with cave 20', hedged)",
  notes="Hedged identity with 1952 cave 20: flagged, not merged (PLAN 4.2).")
X(EXCL, "A41:XI/21", num="XI/21", src=f"{S11} p. 197", ftype="tumulus, oval structure, cairns and sherd scatter", reason="not a cave", grid="19360/12890", exposure=PO, read=T11)
X(EXCL, "A41:XI/22", num="XI/22", src=f"{S11} p. 198", ftype="built enclosure around a pit", reason="not a cave", grid="19350/12850", exposure="exposed-repo", read=T11)

# ------------------------------------------------------------------ Region XII (excavation reports only)
# Part 1 publishes no Region XII survey list, only five excavation reports (files 17-20): XII/49 (Ibrahim, pp. 201-?),
# XII/50 and XII/52-53 (Cohen and Israel, pp. 207-?), XII/56 (Ibrahim, pp. 215-216), XII/61 (Ibrahim and Hameiri,
# pp. 217-218). The other Region XII caves (numbers up to at least 61) are not described in Part 1 (coverage gap).
# File 18 uses only 'east' for openings: 4-point. First read 04:40:05Z.
S12 = "A41 Region XII"
T12 = "2026-10-11T04:40:05Z"
R(ROWS, "A41:XII/49", num="XII/49", src=f"{S12}: Ibrahim, 'The Excavation of Cave XII/49', pp. 201-202, Plan 1, Figs. 1-2", lineage=LIN,
  ftype="natural cave", grid="19288/12749", n_open=1, open_basis="singular description (the opening as wide as the cave, c. 11 m)", res=4,
  plan="Plan 1 (p. 201)", period="Iron II-III (many), Hellenistic, Roman and Byzantine sherds; textiles", piw="partly",
  exc="excavated (L-610; five test pits); surveyed and dug earlier by de Vaux (note 1)", read=T12, exposure="exposed-repo", other_ids="repository: tables/phase5_reports.csv gives the report title and a one-line period summary (abstract level); openings, pillar and facing first read here",
  notes="Upper third of the south cliff of Nahal Qumran, c. 30 m from the top of a dry fall.")
X(EXCL, "A41:XII/50", num="XII/50", src=f"{S12}: Cohen and Israel, pp. 207-208, Plan 1, Fig. 2", ftype="rock shelter (opening faces east)",
  reason="not a cave (rock shelter)", grid="191170/127416", read=T12)
R(ROWS, "A41:XII/52", num="XII/52", src=f"{S12}: Cohen and Israel, p. 208, Plan 2, Fig. 3", lineage=LIN, ftype="cave",
  grid="191170/127416", coord_ok=False, where="upper rock step of the fault escarpment south of Nahal Qumran, c. 10 m south of XII/50 (Region XII)", cbasis="printed grid of the upper step (shared with XII/50); the leading '191' is probably a misprint for '193' (central grid 19325/12710)",
  n_open=1, open_basis="stated (the entrance opening, 0.5 x 0.9 m); a natural roof chimney is not called an entrance",
  facings="cave:E", facing_basis="word in text", res=4, plan="Plan 2",
  period="non-indicative sherds incl. jars of the 1st c. CE and later; modern rubber baskets and a hoe (earlier digging by de Vaux or robbers)",
  piw="partly", exc="sounded (L52 to 0.8 m, not to bedrock; under the survey permit)", read=T12, exposure="exposed-repo", other_ids="repository: tables/phase5_reports.csv gives the report title and a one-line period summary (abstract level); openings, pillar and facing first read here")
R(ROWS, "A41:XII/53", num="XII/53", src=f"{S12}: Cohen and Israel, pp. 207-210, Plan 3 (p. 209), Figs. 1, 4-7", lineage=LIN,
  ftype="cave formed in terrestrial conglomerate", grid="19125/12725", coord_ok=False, where="middle rock step of the fault escarpment south of Nahal Qumran (Region XII; central grid 19325/12710)",
  cbasis="printed grid of the middle step; the leading '191' is probably a misprint for '193' (central grid 19325/12710)",
  n_open=2, open_basis="stated: the opening (4.5 m, as wide as the cave) was divided in two by a pillar (W2); its southern part was blocked by a large boulder (two openings, INFERENCE)",
  facings="cave:E", facing_basis="word in text: the central hall's opening 'faces east' (פונה מזרחה); plan measured as a sensitivity (plan_measurements.json)",
  res=4, north_case="unspecified (arrow)",
  pillar="yes", pillar_kind="built of conglomerate stones ('probably built to stabilise the opening'), W2; a second support W3 near the south-west wall",
  pillar_pos="in the opening, dividing it into a northern and a southern part", pillar_basis="text pp. 208-209; Plan 3 labels W2 and W3 'עמוד Pillar'; Fig. 4",
  north="decided", north_basis="the source names the southern part of the divided opening; A6 on Plan 3 gives c. 2.2 m (INFERENCE)",
  plan="Plan 3 (p. 209)", period="Early Islamic (layer 1), Early Roman (layer 2: jar rim, Herodium parallel), Pottery Neolithic (layer 3), PPNB (layer 4, Byblos points)",
  piw="yes+other", exc="excavated (L-608; areas A and B); earlier digging (de Vaux or robbers)", finds="pottery, flint points, matting, rope, seeds, bones",
  read=T12, exposure="exposed-repo",
  other_ids="repository: tables/phase5_reports.csv row 37 gives the report title and a one-line summary ('first used in the Neolithic, reused in the 1st century CE'); the opening, pillar, facing and northern-part details were first read here (04:40Z, after the freeze)",
  notes="Key row: a cave whose east-facing opening is divided into two by a pillar (built, date not stated). Fig. 4 is captioned 'looking south-west', i.e. into an opening that faces roughly north-east (INFERENCE). The phase of W2 is unknown; the Early Roman layer abuts W1, not W2. A resemblance to 1952 site 32 ('wide low E-facing entrance ... long narrow passage', Qumran-type pottery and Arab sherds) is noted as INFERENCE only; no identity is stated.")
R(ROWS, "A41:XII/56", num="XII/56", src=f"{S12}: Ibrahim, 'The Excavation of Cave XII/56', pp. 215-216, Plan 1, Fig. 1", lineage=LIN,
  ftype="very large natural cave", grid="19292/12690", n_open=1, open_basis="stated (its opening, 6 x 8 m)", facings="cave:E",
  facing_basis="word in text", res=4, plan="Plan 1 (p. 215)", period="very few Iron Age and late Hellenistic sherds; a Natufian lunate; flints; glass; textiles",
  piw="partly", exc="excavated (L-658; five squares to c. 0.5 m); plundered", read=T12,
  notes="c. 400 m south of Nahal Qumran at the foot of the upper fault cliff.")
R(ROWS, "A41:XII/61", num="XII/61", src=f"{S12}: Ibrahim and Hameiri, 'The Excavation of Cave XII/61', pp. 217-218, Plan 1, Figs. 1-4", lineage=LIN,
  ftype="natural cave (an entrance hall and two halls)", grid="19305/12760", n_open=1,
  open_basis="singular description (an entrance hall as wide as the opening; the two halls open from it)", res=4, plan="Plan 1 (p. 217)",
  period="Hellenistic, Byzantine and Mamluk sherds; leather", piw="partly", exc="excavated (L-647; four test pits); dug earlier, probably by de Vaux",
  read=T12, notes="North of the eastern fall of Nahal Qumran, c. 150 m west of Horbat Qumran.")

# ------------------------------------------------------------------ Region XIII
# Tal and Oron, Region XIII (fault escarpment south of Qumran to the Kidron, incl. Einot Tsukim/Ein Feshkha), printed
# pp. 219-227; Table 1 pp. 222-226 (read from the page images). Types defined p. 222: cave (opening narrower than the
# main space), shelter (opening wider), niche, other. Only 'east' for openings: 4-point. First read 04:43:10Z.
S13 = "A41 Region XIII (Tal and Oron), Table 1"
T13 = "2026-10-11T04:43:10Z"
R(ROWS, "A41:XIII/1", num="XIII/1 (group of caves)", src=f"{S13} p. 222", lineage=LIN, kind="cluster", cluster=None, ftype="caves (a group on a scree slope south of the Qumran site)",
  grid="19280/12555", res=4, period="no finds; all filled with alluvium", exc="surveyed", read=T13,
  notes="Cluster record; count not stated. The large cave has several rooms joined by natural burrows.")
R(ROWS, "A41:XIII/2", num="XIII/2 (survey C-7)", src=f"{S13} pp. 222-223, Plan 1, Figs. 1-2", lineage=LIN, ftype="cave", grid="19250/12550",
  n_open=1, open_basis="stated (the cave's triangular opening, 6 m high, 3 m at the base)", res=4,
  terrace="yes", terrace_basis="a step/terrace in front (15 m long, 5 m tread) supported by a built wall of medium and large fieldstones",
  plan="Plan 1 (p. 222), plan and section", period="Pottery Neolithic hearths (8th millennium BCE, radiocarbon); Chalcolithic, Iron, Hellenistic, Byzantine and Early Islamic sherds; unidentified coins",
  piw="partly", exc="excavated (stratigraphic section, L-614)", finds="flint spearheads, fan scraper, knife, rope, matting", read=T13,
  notes="A niche (C-7a) north of the cave, no finds.")
R(ROWS, "A41:XIII/3", num="XIII/3 (survey C-9)", src=f"{S13} p. 223", lineage=LIN, ftype="cave", grid="19250/12330", n_open=1,
  open_basis="stated (the opening, 4 x 3 m)", res=4, period="no finds", exc="surveyed", read=T13)
for n, t, g in ((4, "three pens", "19260/12310"), (5, "round structure", "19210/12275"), (6, "rock shelter (C-10)", "19245/12270"),
                (7, "rock shelter (C-8)", "19230/12200"), (9, "installation (a small 'dolmen')", "19180/12170"), (10, "hearths", "19180/12160"),
                (11, "rock shelters (C-14)", "19120/12140"), (12, "rock shelter (C-6)", "19110/12085"), (13, "five rock shelters (C-1-4), one with a built doorway and window", "19150/12140"),
                (15, "rock shelters and niches (C-13)", "19090/12140"), (17, "rock shelter (C-11) with low stone fences", "19200/12120")):
    X(EXCL, f"A41:XIII/{n}", num=f"XIII/{n}", src=f"{S13} pp. 223-226", ftype=t, reason="not a cave", grid=g, read=T13)
R(ROWS, "A41:XIII/8", num="XIII/8 (survey C-5)", src=f"{S13} pp. 224, 226-227 (excavation: Zelinger), Plan 2", lineage=LIN, ftype="cave", grid="19180/12180",
  n_open=1, open_basis="stated (the cave's opening, partly screened by a stone wall)", facings="cave:E", facing_basis="word in text ('הצופה מזרחה', facing east)",
  res=4, plan="Plan 2 (p. 227)", period="a few non-indicative sherds; recent textiles and ropes", exc="excavated fully (L-661)", read=T13,
  notes="c. 200 m west of the Einot Tsukim (Ein Feshkha) reserve, c. 200 m above the Dead Sea; a hearth near the opening.")
R(ROWS, "A41:XIII/14", num="XIII/14", src=f"{S13} p. 224", lineage=LIN, ftype="large cave whose ceiling collapsed; many niches around, their openings walled",
  grid="18980/15140", coord_ok=False, where="upper level of the cliff, at the bend of Nahal Kidron (Region XIII)", res=4, period="no finds", exc="surveyed", read=T13,
  notes="Printed grid N 151.4 is impossible for Region XIII (probably 18980/12140, the grid of XIII/16); the description nearly repeats XIII/16 (a possible double printing).")
R(ROWS, "A41:XIII/16", num="XIII/16 (survey C-12)", src=f"{S13} p. 226", lineage=LIN, ftype="large cave whose ceiling collapsed", grid="18980/12140", res=4,
  period="no finds", exc="surveyed (not carefully, because of the collapse)", read=T13,
  notes="North bank of Nahal Kidron, in conglomerate; many niches around with walled openings.")

# ------------------------------------------------------------------ Region XIV
# Dahari, Region XIV (fault escarpment from Nahal Kidron to Nahal Deragot), printed pp. 229-247 ('Operation Scroll',
# November 1993). Facing words include 'north-east' (XIV/2/17): 8-point. Pages 229-241 and 246 were opened by an
# earlier worker (registration/atiqot41_region_v_extracted.md section 5; W2B grid conversions for XIV/51, XIV/53).
# Pages 242-245 first read here 04:44:45Z.
S14 = "A41 Region XIV (Dahari)"
T14 = "2026-10-11T04:44:45Z"
for k, g, kw in (("marl-1", "19340/12765", dict(n_open=1, open_basis="stated (a small opening and one small space)", exc="excavated (no finds)",
                                                   notes="Next to de Vaux's cave 4 (4Q) (p. 231, Fig. 1); the source gives it no number.")),
                 ("marl-2", "", dict(exc="surveyed", notes="The source gives it no number or grid.")),
                 ("marl-3", "", dict(exc="surveyed", notes="The source gives it no number or grid."))):
    R(ROWS, f"A41:XIV/{k}", num=f"Region XIV marl cave near Horbat Qumran ({k})", src=f"{S14} p. 231, Fig. 1", lineage=LIN, ftype="cave in the marl",
      grid=g, where="Lisan marl near Horbat Qumran", res=8, period="no finds (all three empty)", exposure=PO, read=T14, **kw)
R(ROWS, "A41:XIV/1", num="XIV/1", src=f"{S14} p. 231", lineage=LIN, grid="19060/12070", res=8, period="empty", exc="surveyed", exposure="exposed-repo", read=T14,
  notes="Almost at the top of the south cliff of Nahal Kidron.")
R(ROWS, "A41:XIV/2/11", num="XIV/2/11 (niche in a small natural cave, Kidron (South) site)", src=f"{S14} pp. 231-234, Figs. 2, 4-5", lineage=LIN,
  ftype="niche (כוך) built in a small natural cave; listed among the site's 'caves' (p. 231)", grid="1909/1205", cbasis="site centre (XIV/2)", c1="unknown",
  n_open=1, open_basis="singular description (its opening, Fig. 4)", facings="cave:N", facing_basis="word in text ('the only niche facing north')", res=8,
  terrace="yes", terrace_basis="a built stone wall bounds a step whose tread served as a courtyard in front of the niche (Fig. 5)",
  period="Early Roman sherds; site built in the 1st c. CE, peak in the Great Revolt", piw="yes", exc="surveyed; plundered", exposure="exposed-repo", read=T14)
R(ROWS, "A41:XIV/2/17", num="XIV/2/17 (cave, Kidron (South) site)", src=f"{S14} pp. 231, 238", lineage=LIN, ftype="cave (the southernmost cave of the site)",
  grid="1909/1205", cbasis="site centre (XIV/2)", facings="cave:NE", facing_basis="word in text (its front faces north-east)", res=8,
  period="site XIV/2 built in the 1st c. CE, used to the Great Revolt (site-level statement); the cave itself full of alluvium", piw="yes",
  exc="surveyed", exposure=PO, read=T14, notes="A built retaining wall in front (two courses); not coded as a terrace (PLAN 4.3: no terrace word).")
X(EXCL, "A41:XIV/2", num="XIV/2 other units (niches, rooms, cells, courtyard)", src=f"{S14} pp. 231-239", ftype="niches and built structures of the Kidron (South) site",
  reason="not caves (the site's other 15 units)", grid="1909/1205", exposure="exposed-repo", read=T14)
R(ROWS, "A41:XIV/3", num="XIV/3 (cluster of 15 caves)", src=f"{S14} p. 241", lineage=LIN, kind="cluster", cluster=15,
  ftype="15 natural caves in the Lisan marl, joined by underground burrows", grid="1911/1204", res=8, period="no surface remains", exc="surveyed",
  exposure="exposed-repo", read=T14)
R(ROWS, "A41:XIV/4", num="XIV/4 (cluster of 20 caves)", src=f"{S14} pp. 241-242, Figs. 22-23", lineage=LIN, kind="cluster", cluster=20,
  ftype="20 small caves (c. 1.5 m long) in a vertical limestone cliff", grid="1908/1203", res=8, period="no finds (XIV/4/1-2 cleaned)", exc="surveyed",
  exposure="exposed-repo", read=T14, notes="A wall was built at the openings of XIV/4/1 and XIV/4/2.")
R(ROWS, "A41:XIV/4-south", num="XIV: five caves 200-450 m south of XIV/4 (unnumbered)", src=f"{S14} p. 242", lineage=LIN, kind="cluster", cluster=5,
  ftype="caves in the fault escarpment", grid="1907/1200", cbasis="group centre", res=8, period="no finds", exc="surveyed", read=T14)
X(EXCL, "A41:XIV/5", num="XIV/5", src=f"{S14} p. 242", ftype="burrow (מחילה)", reason="not a cave by the source's type word", grid="19065/11990", read=T14)
R(ROWS, "A41:XIV/6", num="XIV/6 'Amnon's Cave'", src=f"{S14} pp. 242-244, Plan 2, Figs. 24-27", lineage=LIN, grid="19060/11965",
  n_open=1, open_basis="stated (its small opening, narrowed by a built wall)", res=8, plan="Plan 2 (p. 243)",
  period="Neolithic and Chalcolithic (mat 5564-5387 BCE); cooking pots of the 1st c. CE; Early Islamic stamped handle", piw="yes+other",
  exc="excavated (Y. Sharvit); plundered", read=T14)
for n, g, kw in ((7, "19050/11950", dict(num="XIV/7 'Large Opening Cave'", n_open=1, open_basis="stated (a large opening)")),
                 (8, "19040/11940", dict(n_open=1, open_basis="stated (its crescent-shaped opening)")),
                 (9, "19035/11930", dict(n_open=1, open_basis="stated (its small opening; a retaining wall on its north side)")),
                 (10, "19040/11910", dict(n_open=1, open_basis="stated (a triangular opening)", period="a few Chalcolithic sherds", piw="no")),
                 (11, "19035/11900", dict(n_open=1, open_basis="stated (the cave's small opening)")),
                 (12, "19051/11890", dict(n_open=2, open_basis="stated number (the cave's two hidden openings)")),
                 (17, "19040/11865", dict(n_open=1, open_basis="singular description (its opening was hard to reach)", period="bird droppings only"))):
    kw.setdefault("period", "no finds")
    R(ROWS, f"A41:XIV/{n}", num=kw.pop("num", f"XIV/{n}"), src=f"{S14} pp. 244-245", lineage=LIN, grid=g, res=8, exc="surveyed", read=T14, **kw)
for k in ("a", "b"):
    R(ROWS, f"A41:XIV/13-16{k}", num=f"XIV/13-16: northern cave {k} (two caves and two niches)", src=f"{S14} p. 245", lineage=LIN,
      ftype="large branching cave on the north bank of an unnamed wadi", grid="1904/1187", cbasis="group centre (XIV/13-16)", res=8, period="no finds",
      exc="surveyed", read=T14, notes="The source numbers the group 13-16 without saying which numbers are the caves.")
X(EXCL, "A41:XIV/13-16n", num="XIV/13-16: two southern niches", src=f"{S14} p. 245", ftype="two small shallow niches", reason="not caves", grid="1904/1187", read=T14)
R(ROWS, "A41:XIV/18", num="XIV/18 'Coin Cave'", src=f"{S14} p. 245 (Bar-Adon 1989 pp. 30-32 cited)", lineage=LIN, ftype="cave", grid="1903/1185",
  cbasis="group centre (XIV/18-22)", res=8, period="finds of the Great Revolt from Bar-Adon's earlier excavation (as cited); none in 1993", piw="yes",
  exc="excavated earlier (Bar-Adon); surveyed 1993", read=T14)
X(EXCL, "A41:XIV/19-22", num="XIV/19-22", src=f"{S14} p. 245", ftype="four small niches", reason="not caves", grid="1903/1185", read=T14)
for n in range(23, 33):
    R(ROWS, f"A41:XIV/{n}", num=f"XIV/{n} (one of ten caves XIV/23-32)", src=f"{S14} p. 245", lineage=LIN, ftype="cave (most very small, hard to reach)",
      grid="1900/1181", cbasis="group centre (XIV/23-32)", res=8, period="no finds", exc="surveyed", read=T14)
R(ROWS, "A41:XIV/33", num="XIV/33", src=f"{S14} p. 245", lineage=LIN, ftype="cave, 'probably the largest along the fault escarpment of the Judean Desert'",
  grid="", where="foot of the upper step of the fault escarpment, between OIG northings 117 and 118 (Region XIV)",
  n_open=1, open_basis="stated (its arched opening)", facings="cave:S", facing_basis="word in text", res=8, period="no finds", exc="surveyed", read=T14,
  notes="Two storeys: an entrance storey c. 70 x 30 m and a hidden underground space below.")
X(EXCL, "A41:XIV/34-46", num="XIV/34-46", src=f"{S14} p. 245", ftype="rock shelters XIV/34 and XIV/46; niches XIV/35-45", reason="not caves", read=T14)
R(ROWS, "A41:XIV/47", num="XIV/47 'Square Opening Cave'", src=f"{S14} p. 245", lineage=LIN, grid="18920/11665", n_open=1, open_basis="stated (its square opening)",
  res=8, period="no finds", exc="surveyed", read=T14)
for n in (48, 49, 50):
    R(ROWS, f"A41:XIV/{n}", num=f"XIV/{n} (caves in Nahal Qane / Wadi el-Ghuweir)", src=f"{S14} pp. 245-246", lineage=LIN, ftype="small cave",
      grid="1890/1155", cbasis="group centre (XIV/48-50)", res=8, period="no finds", exc="surveyed", exposure=PO, read=T14,
      notes="The south-bank cave is printed 'XIV/30', evidently XIV/50." if n == 50 else "")
R(ROWS, "A41:XIV/51", num="XIV/51 (above the 'Ein el-Ghuweir site)", src=f"{S14} p. 246 (Bar-Adon 1989 p. 40 cited)", lineage=LIN, grid="18920/11505",
  res=8, period="pottery of the 8th and ?th centuries BCE (Bar-Adon, as cited); none in 1993", piw="no", exc="excavated earlier (Bar-Adon); re-examined 1993",
  exposure="exposed-repo", read=T14)
R(ROWS, "A41:XIV/52", num="XIV/52", src=f"{S14} p. 246", lineage=LIN, grid="18870/11460", n_open=1, open_basis="stated (its small opening, in its ceiling)",
  res=8, period="no finds (test trench)", exc="sounded", exposure=PO, read=T14)
for n in (53, 54):
    R(ROWS, f"A41:XIV/{n}", num=f"XIV/{n} (caves near the road in Nahal Samar)", src=f"{S14} p. 246 (Bar-Adon 1989 p. 49 cited)", lineage=LIN, ftype="cave",
      grid="1887/1129", cbasis="group centre (XIV/53-58)", res=8, period="", exc="surveyed earlier (Bar-Adon) and in 1993", exposure="exposed-repo", read=T14)
X(EXCL, "A41:XIV/55-58", num="XIV/55-58", src=f"{S14} p. 246", ftype="four shallow niches (two late Iron Age sherds in XIV/55)", reason="not caves", grid="18835/11300", exposure=PO, read=T14)
R(ROWS, "A41:XIV/59", num="XIV/59 (Nahal Tur)", src=f"{S14} p. 246", lineage=LIN, grid="18805/11165", n_open=1, open_basis="stated (its opening, hidden behind a boulder)",
  res=8, period="animal bones, porcupine quills", exc="surveyed", exposure=PO, read=T14)
R(ROWS, "A41:XIV/60", num="XIV/60 (Nahal Tur)", src=f"{S14} p. 246", lineage=LIN, grid="18775/11165", res=8, period="no finds", exc="surveyed", exposure=PO, read=T14)
R(ROWS, "A41:XIV/61", num="XIV/61 (Nahal Deragot)", src=f"{S14} p. 246", lineage=LIN, ftype="large cave", grid="18700/10960", res=8, period="no finds",
  exc="surveyed", exposure=PO, read=T14)

# ------------------------------------------------------------------ Region XV (excavation report only)
# Nahliel and Lander, 'The Excavation of Cave XV/3 in Nahal Hazezon', printed pp. 249-251 (map p. 249, Plan 1).
# Note 1 of the report: the Region XV survey (N. Negev) is not published in this volume (coverage gap).
# No facing words. First read 04:46:31Z.
S15 = "A41 Region XV (Nahliel and Lander)"
T15 = "2026-10-11T04:46:31Z"
R(ROWS, "A41:XV/3", num="XV/3 (Nahal Hazezon)", src=f"{S15} pp. 249-251, Plan 1", lineage=LIN, ftype="cave", grid="1853/1076",
  cbasis="printed approximate grid ('נ\"צ משוער')", n_open=None,
  open_basis="unknown: a wide opening (6 x c. 2 m) opens into two halls; 'a smaller opening' (1.5 x 3 m) leads to the southern hall, not said to be exterior",
  plan="Plan 1", period="two Roman coins and a sword of unclear date in the spoil in front (survey); 'probably a hiding cave' in the Roman period (authors); modern shepherds",
  piw="partly", exc="excavated (test squares L1-L3; no ancient finds in L2-L3)", read=T15,
  notes="West bank of upper Nahal Hazezon just above its 150 m deep canyon. The rest of Region XV is unpublished in Part 1.")
