"""Add the West Bank and East Jerusalem Archaeological Database (WBADB) to lane J's unified
feature table as a fifth inventory.

Source: R. Greenberg and A. Keinan, West Bank and East Jerusalem Archaeological Database
(Tel Aviv University / Emek Shaveh, 2009), the database behind *Israeli Archaeological
Activity in the West Bank 1967-2007: A Sourcebook* (Jerusalem: Ostracon, 2009).
Public file: https://www.tau.ac.il/humanities/abraham/publications/archaeological.xls
No licence is stated. The raw file is not stored in the repository; this script fetches it
and checks its hash.

usage: python3 build_inventory_v2.py [path/to/archaeological.xls]
"""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

HERE = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
URL = "https://www.tau.ac.il/humanities/abraham/publications/archaeological.xls"
SHA256 = "1f1638756ea589b4f7548b5433072335f9407885323563f327d87b6d460bca53"
UA = "Mozilla/5.0 (compatible; CopperScroll research intake)"
J_TABLE = REPO / "sandbox/landscape_map_2026-10-31/inputs/features_unified.csv"  # lane J, 7b58cf0

# Component words -> lane J classes (one site can carry several classes)
CLASS_RX = {
    "cistern": r"cistern",
    "pool_reservoir": r"\bpools?\b|reservoir|birk",
    "channel_aqueduct": r"aqueduct|channel|conduit",
    "tomb": r"tomb|burial|grave|cemetery|kokh|ossuar",
    "cave": r"\bcaves?\b",
    "dam": r"\bdams?\b",
    "rockcut": r"rock-?cut|rock-?hewn|winepress|wine press|oil press|\bpress|installation|quarr|cupmark",
    "steps_ritual_bath": r"miqv|mikv|ritual bath|stepped",
    "fortress": r"\bfort\b|fortress|fortif|\btower",
    "dovecote": r"columbar|dovecot",
}
ZONES = [  # lane J boxes, first match wins
    ("Z1_GERIZIM", [(32.14, 32.26, 35.19, 35.37)]),
    ("Z2_JORDAN_VALLEY", [(31.76, 32.06, 35.40, 35.60)]),
    ("Z4_JERUSALEM_HILLS", [(31.62, 31.90, 35.10, 35.27)]),
    ("Z3_JUDEAN_DESERT", [(31.20, 31.92, 35.27, 35.60), (31.92, 32.06, 35.30, 35.60)]),
]


def zone_of(la, lo):
    if np.isnan(la):
        return "UNZONED"
    for z, boxes in ZONES:
        for a, b, c, d in boxes:
            if a <= la <= b and c <= lo <= d:
                return z
    return "OUT"


def fetch(path=None):
    if path is None:
        req = urllib.request.Request(URL, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=120).read()
    else:
        data = Path(path).read_bytes()
    h = hashlib.sha256(data).hexdigest()
    if h != SHA256:
        raise SystemExit(f"hash mismatch: {h} (expected {SHA256}); the published file has changed")
    return data


def clean(x):
    s = " ".join(str(x).split()) if isinstance(x, str) else ""
    return "" if s in ("-", "nan") else s


def main():
    raw = fetch(sys.argv[1] if len(sys.argv) > 1 else None)
    tmp = HERE / "data/_archaeological.xls"
    tmp.write_bytes(raw)
    sheets = pd.read_excel(tmp, sheet_name=None)
    tmp.unlink()
    t = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)  # Old Israel Grid (Palestine 1923)
    rows = []
    for sheet, tag in (("Surveyed", "S"), ("Excavations", "E")):
        d = sheets[sheet]
        x = pd.to_numeric(d.X, errors="coerce").values
        y = pd.to_numeric(d.Y, errors="coerce").values
        lon, lat = t.transform(x, y)
        for i, r in enumerate(d.itertuples(index=False)):
            comp = "; ".join(c for c in (clean(getattr(r, "Site_Components", "")),
                                          clean(getattr(r, "More_Components", ""))) if c)
            txt = (comp + " " + clean(getattr(r, "Comments", ""))).lower()
            cls = [k for k, p in CLASS_RX.items() if re.search(p, txt)]
            rows.append(dict(
                wb_id=f"WB{tag}:{int(r.Index)}", sheet=sheet, site_name=clean(r.Site_Name),
                other_names=clean(r.Other_Names), oig_x=x[i], oig_y=y[i],
                lat=round(float(lat[i]), 6) if np.isfinite(lat[i]) else np.nan,
                lon=round(float(lon[i]), 6) if np.isfinite(lon[i]) else np.nan,
                survey_ref=clean(getattr(r, "Survey_Ref", "")),
                site_no=clean(getattr(r, "Survey_Site_Number", getattr(r, "Site_No", ""))),
                license=clean(getattr(r, "License", getattr(r, "License_No", ""))),
                major_periods=clean(r.Major_Periods), other_periods=clean(r.Other_Periods),
                hel=int(getattr(r, "Hel", 0) or 0), rom=int(getattr(r, "Rom", 0) or 0),
                components=comp, classes=";".join(cls)))
    wb = pd.DataFrame(rows)
    wb["zone"] = [zone_of(a, b) for a, b in zip(wb.lat, wb.lon)]
    wb.to_csv(HERE / "data/wbadb_sites.csv", index=False)

    # inventory v2: lane J rows + one WBADB row per (site, class), in lane J's schema
    j = pd.read_csv(J_TABLE)
    add = []
    for r in wb.itertuples():
        for c in [c for c in r.classes.split(";") if c]:
            add.append(dict(fid=f"{r.wb_id}:{c}", inventory="WBADB_" + ("S" if r.sheet == "Surveyed" else "E"),
                            cls=c, lat=r.lat, lon=r.lon, zone=r.zone, name_place="",
                            period_text=" ".join(p for p in (r.major_periods, r.other_periods) if p),
                            sid="", stratum=f"{c}|{r.zone}"))
    v2 = pd.concat([j, pd.DataFrame(add)], ignore_index=True)
    v2.to_csv(HERE / "data/features_unified_v2.csv", index=False)
    print("WBADB sites", len(wb), "| with a class", int((wb.classes != "").sum()),
          "| added rows", len(add), "| v2 rows", len(v2))
    print(wb.zone.value_counts().to_dict())


if __name__ == "__main__":
    main()
