"""Zissu 2023 (PLAN.md S11): named caves inside the box not otherwise inventoried.

Source: registration/zissu2023_extracted.md (repository extraction of Zissu, 'Kings, Hermits and Refugees in the
Judean Desert', in Sion et al. eds., New Studies in the Archaeology of the Judean Desert, IAA 2023, pp. 185-215;
exposed before the freeze). The chapter gives no coordinates, plans, entrance counts or facings for any cave, so
every clause beyond C1 is unknown. Caves named there that are already inventoried (Avi'or Cave = A41 VIII/10,
Cave of the Sandal = A41 VIII/28, the Qumran caves) are not added again.
Murabba'at count: Reed, BASOR 135 (1954) p. 8 ('the clearing of four large caves in Wadi Murabba'at').
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from coding import R, X  # noqa: E402

ROWS, EXCL = [], []
MERGE = {}
SRC = "Zissu 2023 (repo extraction registration/zissu2023_extracted.md)"
LIN = "named refuge caves (Zissu 2023 synthesis; original campaigns not inventoried here)"
EX = "exposed-repo"


def z(key, num, *, where, page, kind="cave", cluster=None, period="Bar Kokhba refuge (Zissu)", piw="yes", notes="", src=None):
    R(ROWS, f"Z23:{key}", num=num, src=src or f"{SRC}, item at p. {page}", lineage=LIN, kind=kind, cluster=cluster,
      where=where, period=period, piw=piw, exc="excavated (per the literature Zissu cites; not inventoried here)", exposure=EX, notes=notes)


z("KetefJericho", "Caves of Ketef Jericho", kind="cluster", where="cliff west of Jericho (Zissu p. 205)", page="205, 207",
  period="First Revolt papyri; Bar Kokhba refuge", notes="Openings 'obvious to anyone looking westward from Jericho' (Zissu); count not given.")
z("JerichoRidge", "Caves on the Jericho Ridge", kind="cluster", where="Jericho area (Zissu p. 207)", page="207",
  notes="Count not given; probably overlaps Ketef Jericho and the Atiqot 41 Jebel Quruntul regions (no crosswalk).")
for n in (1, 2, 3, 4):
    z(f"Murabbaat-{n}", f"Wadi Murabba'at (Nahal Darga) cave No. {n}", where="Wadi Murabba'at / Nahal Darga (inside the box by description)",
      page="194, 204, 208-209", period="First Revolt and Bar Kokhba documents (Zissu)", piw="yes",
      src=f"{SRC}, item 10 (pp. 194, 204, 208-209); Reed 1954 p. 8 (four large caves cleared in 1952)",
      notes="Cave No. 1 had a plaster-lined water pool (Zissu p. 208)." if n == 1 else "Count of four from Reed 1954 p. 8; DJD II (Benoit, Milik and de Vaux 1961) not read.")
z("PoolNahalDavid", "Cave of the Pool, Nahal David", where="Nahal David, 'En Gedi", page="205-208", period="prutah of year 2 of the First Revolt; Bar Kokhba",
  notes="Plaster-lined pool; arrowheads in the roof (Zissu).")
z("HarYishai", "Har Yishai Cave", where="'En Gedi area", page="207")
z("Salvadora", "Salvadora Cave", where="north of 'En Gedi", page="207", period="probable 'En Gedi refuge (Zissu)", piw="partly")
z("Figs", "Cave of the Figs", where="north of 'En Gedi", page="207", period="probable 'En Gedi refuge (Zissu)", piw="partly")
z("Spear", "Caves of the Spear", kind="cluster", where="north of 'En Gedi", page="207", period="probable 'En Gedi refuge (Zissu)", piw="partly")
z("Letters", "Cave of Letters, Nahal Hever", where="Nahal Hever (north bank)", page="205-209", period="First Revolt prutah; Bar Kokhba documents",
  notes="Arrowheads in the roof; Roman siege camp above (Zissu).")
z("Horror", "Cave of Horror, Nahal Hever", where="Nahal Hever (south bank)", page="207-209", notes="Roman siege camp above; human remains (Zissu).")

for k, what, why in (
        ("Tetradrachm", "Cave of the Tetradrachm, upper channel of Nahal Hever", "upper Nahal Hever lies west of the box's E 180,000 edge; not placeable inside"),
        ("Mishmar-Zeelim-Harduf", "caves of Nahal Mishmar, Nahal Ze'elim and Nahal Harduf", "south of N 091,000 (PLAN section 2)"),
        ("Rashash", "caves in Wadi er-Rashash", "north of the box"), ("Naasaneh", "'Araq en-Na'asaneh, Wadi Daliyeh", "north of the box"),
        ("Teqoa", "caves of Nahal Teqoa and el-Masia Cave", "Herodium region, west of the box"),
        ("Pheretae", "caves of the Pheretae ravine", "identified with Wadi Fara / 'Ein Fara (ESI 3 p. 61), west of the box"),
        ("HidingWestJericho", "hiding caves between west of Jericho and the Benjamin hills", "general category without count or locality")):
    X(EXCL, f"Z23:{k}", num=what, src=SRC, ftype="caves", reason=why, exposure=EX)
