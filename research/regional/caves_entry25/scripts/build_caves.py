#!/usr/bin/env python3
"""Build caves.csv and excluded.csv from the hand-coded modules (PLAN.md sections 4-5).

Run from anywhere:  python3 -I -B research/regional/caves_entry25/scripts/build_caves.py
Steps: load coded/*.py; apply stated-identity merges; add the Atiqot 41 Index crosswalk to other_ids; parse and
convert coordinates (EPSG:28191 -> EPSG:4326 and EPSG:2039, pyproj); test region membership (PLAN 2); flag possible
duplicates (PLAN 4.2: best points within 50 m across field campaigns, or the same proper name, listed in NAME_FLAGS);
write caves.csv, excluded.csv and duplicates.csv.
"""
import csv
import importlib
import json
import math
import re
import sys
from pathlib import Path

from pyproj import Transformer

LANE = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(LANE / "coded"))
sys.path.insert(0, str(LANE / "scripts"))
from coding import FIELDS, XFIELDS  # noqa: E402

MODULES = ["a41", "djd3", "esi", "zissu", "asi", "wbadb"]
BOX = (180000.0, 197000.0, 91000.0, 150000.0)
DUP_M = 50.0
OIG2WGS = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
OIG2ITM = Transformer.from_crs("EPSG:28191", "EPSG:2039", always_xy=True)
WGS2OIG = Transformer.from_crs("EPSG:4326", "EPSG:28191", always_xy=True)

# Same proper name (PLAN 4.2), across field campaigns. Each pair is flagged, never merged.
NAME_FLAGS = [
    ("Z23:PoolNahalDavid", "ASI:147-149", "same name: Cave of the Pool, Nahal David"),
    ("Z23:Horror", "ASI:147-417", "same name: Cave of Horror"),
    ("Z23:Letters", "ASI:147-429", "same name: Cave of (the) Letters"),
    ("Z23:Spear", "WB:S5247", "same name: Caves of the Spear"),
    ("Z23:Figs", "WB:S5600", "same name: Cave of (the) Figs"),
    ("Z23:HarYishai", "ASI:147-90", "same name: Har Yishai (cave)"),
    ("Z23:HarYishai", "ASI:147-91", "same name: Har Yishai (cave)"),
    ("A41:VIII/10", "WB:E333", "same name: Avi'or Cave"),
    ("A41:X/60", "WB:E680", "same name: Cave of the Button"),
    ("A41:IV/11", "WB:E707", "same name: 'Cave of the Pillar' (Atiqot 41 Index nickname of IV/11; WBADB record at Qumran)"),
    ("A41:II/49", "PAT:UMakkuk-5", "same name: Cave of the Spring (upper Wadi Makkuk)"),
    ("DJD3:8", "A41:X/35", "same label 'Q3' (ESI 6 for 1952 no. 8; Atiqot 41 p. 180 for Patrich and Arubas Cave 13)"),
    ("DJD3:8", "WB:E756", "same label 'Q3' / 'Q-3'"),
    ("A41:X/35", "WB:E756", "same label 'Q3' / 'Q-3'"),
]


def load():
    rows, excl, merge = [], [], {}
    for name in MODULES:
        m = importlib.import_module(name)
        for r in m.ROWS:
            r["module"] = name
        rows += m.ROWS
        excl += m.EXCL
        merge.update(getattr(m, "MERGE", {}))
    return rows, excl, merge


def apply_merges(rows, merge):
    by = {r["cave_id"]: r for r in rows}
    for src, dst in merge.items():
        s, d = by.get(src), by.get(dst)
        if s is None or d is None:
            raise SystemExit(f"merge {src} -> {dst}: missing row")
        for k in FIELDS:
            if k in ("cave_id", "notes", "source_records", "other_ids", "exposure", "first_read_utc", "lineage"):
                continue
            if d.get(k) in (None, "") and s.get(k) not in (None, ""):
                d[k] = s[k]
        d["source_records"] = f"{d['source_records']} || {s['source_records']}"
        d["other_ids"] = "; ".join(x for x in (d.get("other_ids"), f"merged record {src}", s.get("other_ids")) if x)
        d["lineage"] = f"{d['lineage']}; {s['lineage']}" if s["lineage"] not in d["lineage"] else d["lineage"]
        d["notes"] = "; ".join(x for x in (d.get("notes"), f"MERGED {src} (identity stated by a source)", s.get("notes")) if x)
        order = ["exposed-repo", "page-opened-before", "exposed-this-worker", "unexposed-at-freeze"]
        d["exposure"] = min((d["exposure"], s["exposure"]), key=order.index)
        if s.get("first_read_utc") and not d.get("first_read_utc"):
            d["first_read_utc"] = s["first_read_utc"]
    return [r for r in rows if r["cave_id"] not in merge]


def add_index(rows):
    idx = {}
    with open(LANE / "coded/a41_index_crosswalk.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            idx[r["pub_id"]] = r
    for r in rows:
        if not r["cave_id"].startswith("A41:"):
            continue
        base = re.sub(r"(?<=\d)[a-z]$", "", r["cave_id"])
        x = idx.get(base)
        if not x:
            continue
        bits = [f"1993 no. {x['no_1993']}" if x["no_1993"] else "", f"1993 code {x['code_1993']}" if x["code_1993"] else "",
                f"permit {x['permit']}" if x["permit"] else "", f"Index nickname '{x['nickname_en']}'" if x["nickname_en"] else ""]
        bits = [b for b in bits if b]
        if bits:
            r["other_ids"] = "; ".join(y for y in (r.get("other_ids"), "A41 Index: " + ", ".join(bits)) if y)


def parse_part(s):
    """One printed grid component -> (metres, unit_m). Handles 4, 5 and 6 digit forms and 'dddd-d' ranges."""
    s = s.strip()
    units = {4: 100.0, 5: 10.0, 6: 1.0}
    m = re.fullmatch(r"(\d{4,6})-(\d{1,3})", s)
    if m:
        first, tail = m.group(1), m.group(2)
        unit = units[len(first)]
        lo, hi = int(first), int(first[:-len(tail)] + tail)
        # a group range: the returned 'unit' is the full extent, so half of it is the half-range plus half a unit
        return (lo + hi) / 2 * unit, (hi - lo) * unit + unit
    if not s.isdigit() or len(s) not in units:
        raise ValueError(s)
    return int(s) * units[len(s)], units[len(s)]


def coords(r):
    g, crs = r["coord_printed"], r["crs_printed"]
    if not g:
        return None
    if crs == "WGS84":
        lat, lon = (float(v) for v in g.split("/"))
        x, y = WGS2OIG.transform(lon, lat)
        return x, y, None
    a, b = g.split("/")
    (x, ux), (y, uy) = parse_part(a), parse_part(b)
    return x, y, max(ux, uy) / 2.0


def build():
    rows, excl, merge = load()
    rows = apply_merges(rows, merge)
    add_index(rows)
    out = []
    for r in rows:
        c = coords(r)
        rec = dict(r)
        rec.update(x_oig="", y_oig="", lat="", lon="", itm_x="", itm_y="", in_region="", region_basis="", edge="")
        if c:
            x, y, half = c
            lon, lat = OIG2WGS.transform(x, y)
            ix, iy = OIG2ITM.transform(x, y)
            rec.update(x_oig=round(x, 1), y_oig=round(y, 1), lat=round(lat, 6), lon=round(lon, 6), itm_x=round(ix, 1), itm_y=round(iy, 1))
            if rec["precision_m"] in (None, ""):
                rec["precision_m"] = half
                rec["coord_basis"] = (rec["coord_basis"] + "; precision nominal (half the printed unit)") if half is not None else rec["coord_basis"]
        if c and r.get("coord_ok", True):
            x, y = c[0], c[1]
            inside = BOX[0] <= x <= BOX[1] and BOX[2] <= y <= BOX[3]
            p = float(rec["precision_m"] or 0)
            near = min(abs(x - BOX[0]), abs(x - BOX[1]), abs(y - BOX[2]), abs(y - BOX[3])) <= p
            rec["in_region"] = "yes" if inside else ("edge" if near else "no")
            rec["region_basis"] = "point"
            rec["edge"] = "edge" if near else ""
        else:
            rec["in_region"] = "yes"
            rec["region_basis"] = "by description" + (" (printed grid flagged as a misprint)" if c else "")
        out.append(rec)
    outside = [r["cave_id"] for r in out if r["in_region"] == "no"]
    if outside:
        raise SystemExit(f"rows outside the box: {outside}")
    flags = duplicates(out)
    for r in out:
        r["possible_duplicate_of"] = "; ".join(sorted(flags.get(r["cave_id"], [])))
    return out, excl


def campaign(r):
    return r["lineage"].split(";")[0].strip()


def duplicates(rows):
    pts = [(r["cave_id"], float(r["x_oig"]), float(r["y_oig"]), campaign(r)) for r in rows
           if r["x_oig"] != "" and r.get("coord_ok", True)]
    flags, pairs = {}, []
    for i in range(len(pts)):
        a = pts[i]
        for b in pts[i + 1:]:
            if a[3] == b[3]:
                continue
            d = math.hypot(a[1] - b[1], a[2] - b[2])
            if d <= DUP_M:
                flags.setdefault(a[0], set()).add(b[0])
                flags.setdefault(b[0], set()).add(a[0])
                pairs.append((a[0], b[0], f"{d:.0f} m"))
    ids = {r["cave_id"] for r in rows}
    for a, b, why in NAME_FLAGS:
        if a not in ids or b not in ids:
            raise SystemExit(f"name flag on a missing row: {a} {b}")
        flags.setdefault(a, set()).add(b)
        flags.setdefault(b, set()).add(a)
        pairs.append((a, b, why))
    with open(LANE / "duplicates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["row_a", "row_b", "basis"])
        w.writerows(sorted(pairs))
    return flags


OUT_FIELDS = ["cave_id", "name_number", "source_records", "other_ids", "lineage", "feature_type_source", "row_kind", "cluster_count",
              "coord_printed", "crs_printed", "x_oig", "y_oig", "lat", "lon", "itm_x", "itm_y", "precision_m", "coord_basis", "coord_ok",
              "in_region", "region_basis", "where_described", "n_openings", "openings_basis", "opening_facings", "facing_basis",
              "facing_resolution", "north_case", "pillar", "pillar_kind", "pillar_position", "pillar_basis", "terrace", "terrace_basis",
              "northern_member", "northern_basis", "published_plan", "period_stated", "period_in_window", "excavation_status", "finds",
              "c1_override", "exposure", "first_read_utc", "possible_duplicate_of", "module", "notes"]


def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    return v


def main():
    rows, excl = build()
    rows.sort(key=lambda r: (MODULES.index(r["module"]), r["cave_id"]))
    with open(LANE / "caves.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: cell(r.get(k)) for k in OUT_FIELDS})
    with open(LANE / "excluded.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=XFIELDS, lineterminator="\n")
        w.writeheader()
        for r in excl:
            w.writerow({k: cell(r.get(k)) for k in XFIELDS})
    print(f"caves.csv: {len(rows)} rows; excluded.csv: {len(excl)} records")


if __name__ == "__main__":
    main()
