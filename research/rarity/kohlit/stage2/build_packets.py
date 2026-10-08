"""Koḥlit rarity count, Stage 2: build one evidence packet per unit for the coders.

A packet holds, for one unit, everything the coders may use from the five §5 sources:
  1. WBADB: the unit's own row and every WBADB row within 2 km, with distance, grid bearing,
     point precision and the position-rule-2 test already computed;
  2. the original survey entry named in Survey_Ref, where it is lawfully online
     (in practice: Finkelstein et al. 1997, *Highlands of Many Cultures*);
  3. SWP Memoir entries: those linked in Stage 1b, plus entries that name the unit;
  4. for excavated units, excerpts of the first publication listed in WBADB, if gathered;
  5. for oasis units, every Nigro et al. 2011 catalogue entry within 2 km, with geometry.

Packets quote copyrighted sources, so they stay outside the repository. The committed
manifest records each packet's SHA-256.

Usage:
    python3 -I build_packets.py WBADB.xlsx SWP_II.txt SWP_III.txt HIGHLANDS.pdf NIGRO.pdf S4_DIR OUT_DIR
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
KOHLIT = HERE.parent
sys.path.insert(0, str(KOHLIT))
import stage1_screen as s1a  # noqa: E402
import stage1b_swp as s1b    # noqa: E402

PROTOCOL = json.loads((HERE / "protocol_constants.json").read_text(encoding="utf-8"))
COVERAGE = json.loads((HERE / "coverage.json").read_text(encoding="utf-8"))

HIGHLANDS_SHA256 = "2074020593f986fdc2189448f74c3037b577fb0093bb35b658eadcf47085c16c"
NIGRO_SHA256 = "0c7fefdf676abb796c6cccf4f33dd6289c499d6a54249322e0b2ea672122af73"
HIGHLANDS_PAGE_OFFSET = 35          # PDF page = printed page + 35
PACKET_RADIUS_M = 2_000
SWP_MENTION_RADIUS_M = 15_000
SWP_MAX_ENTRIES = 10
SWP_TEXT_CHARS = 2_500
NIGRO_PRECISION_M = 30              # the catalogue says its seconds are "indicative" (1" is about 30 m)

PERIOD_COLS = s1a.W["periods"]["sensitivity_pre70"] + ["Byz", "EIs", "Med", "Ott"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def precision_m(x, y):
    """Coarsest rounding step that both grid values share (WBADB rounds many points to 100 m)."""
    for p in (1000, 500, 100, 50, 10):
        if int(round(x)) % p == 0 and int(round(y)) % p == 0:
            return p
    return 1


def bearing_deg(x0, y0, x1, y1):
    return (math.degrees(math.atan2(x1 - x0, y1 - y0)) + 360.0) % 360.0


def geometry(ux, uy, uprec, fx, fy, fprec):
    d = math.hypot(fx - ux, fy - uy)
    coarse = max(uprec, fprec)
    valid = d >= 3 * coarse
    return {"distance_m": round(d), "bearing_deg": round(bearing_deg(ux, uy, fx, fy), 1) if d > 0 else None,
            "precision_m": coarse, "bearing_valid": bool(valid)}


def clean(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    s = str(v).strip()
    return "" if s in ("-", "NDA", "nan") else s


def periods(row):
    out = []
    for c in PERIOD_COLS:
        v = row.get(c)
        try:
            if v is not None and not (isinstance(v, float) and math.isnan(v)) and int(v) > 0:
                out.append(c + ("(major)" if int(v) == 2 else ""))
        except (TypeError, ValueError):
            pass
    return out


def wbadb_record(row):
    return {
        "row_id": row["row_id"], "sheet": "Surveyed" if row["row_id"].startswith("S") else "Excavations",
        "name": clean(row.get("Site_Name")), "other_names": clean(row.get("Other_Names")),
        "x": int(row["X"]), "y": int(row["Y"]), "periods": periods(row),
        "major_periods": clean(row.get("Major_Periods")), "other_periods": clean(row.get("Other_Periods")),
        "components": "; ".join(t for t in (clean(row.get("Site_Components")), clean(row.get("More_Components"))) if t),
        "comments": "; ".join(t for t in (clean(row.get("Comments")), clean(row.get("More_Comments"))) if t),
        "survey_ref": clean(row.get("Survey_Ref")), "excavated": clean(row.get("Excavated")),
        "publication": clean(row.get("Publication_Bibliography")),
    }


# ---------- source 2: Highlands of Many Cultures ----------

def highlands_pages(survey_ref):
    """Printed pages of Finkelstein et al. 1997 named in a Survey_Ref, e.g. '... 1997: 840-841, 843; ...'."""
    m = re.search(r"Finkelstein et al\.? 1997:?\s*([\d\s,\-–]+)", survey_ref or "")
    if not m:
        return []
    pages = []
    for part in m.group(1).split(","):
        part = part.strip()
        if not part:
            continue
        if re.match(r"^\d+\s*[-–]\s*\d+$", part):
            a, b = [int(x) for x in re.split(r"[-–]", part)]
            pages.extend(range(a, b + 1))
        elif part.isdigit():
            pages.append(int(part))
    return pages


def highlands_text(pdf, printed_pages):
    out = []
    for p in printed_pages:
        n = p + HIGHLANDS_PAGE_OFFSET
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        out.append({"printed_page": p, "pdf_page": n, "text": txt.strip()})
    return out


# ---------- source 5: Nigro, Sala and Taha 2011 ----------

DMS = re.compile(r"(\d+)\s*°\s*(\d+)\s*['’′]\s*([\d.]+)\s*(?:\"|''|’’|″|”)")


def parse_nigro(pdf):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    a = txt.index("3.2. Catalogue\n")
    b = txt.index("4. Bibliography of the sites in the Jericho Oasis and its", a)
    lines = txt[a:b].split("\n")
    entries, cur = [], None
    page = 99
    for i, line in enumerate(lines):
        pm = re.match(r"^\s*(\d{2,3})\s{2,}\S.*ROSAPAT 07\s*$", line) or re.match(r"^\s*2011\s+.*\s(\d{2,3})\s*$", line)
        if pm:
            page = int(pm.group(1))
            continue
        m = re.match(r"^(\d{1,3})\)\s+(\S.*)$", line)
        if m and any("PADIS code" in l for l in lines[i + 1:i + 5]):
            if cur:
                entries.append(cur)
            cur = {"cat_no": int(m.group(1)), "name": m.group(2).strip(), "page": page, "text": line}
            continue
        if cur and len(cur["text"]) < 6000:
            cur["text"] += "\n" + line
    if cur:
        entries.append(cur)
    to_grid = Transformer.from_crs("EPSG:4326", "EPSG:28193", always_xy=True)
    for e in entries:
        e["text"] = re.sub(r"\n{3,}", "\n\n", e["text"]).strip()
        loc = re.search(r"Site location:\s*(.*(?:\n(?!\s*[A-Z][A-Za-z ]+:).*)?)", e["text"])
        e["location_words"] = re.sub(r"\s+", " ", loc.group(1)).strip() if loc else ""
        dms = DMS.findall(e["location_words"])
        if len(dms) >= 2:
            lat = int(dms[0][0]) + int(dms[0][1]) / 60 + float(dms[0][2]) / 3600
            lon = int(dms[1][0]) + int(dms[1][1]) / 60 + float(dms[1][2]) / 3600
            gx, gy = to_grid.transform(lon, lat)
            e["x"], e["y"] = round(gx), round(gy - 1_000_000)
        else:
            e["x"] = e["y"] = None
    return entries


# ---------- source 3: SWP Memoirs ----------

def swp_entries(f2, f3):
    for (vol, (_, digest)), path in zip(s1b.SWP_FILES.items(), (f2, f3)):
        if s1b.sha256(path) != digest:
            sys.exit(f"SWP {vol} text hash does not match the frozen value")
    entries = s1b.parse("II", Path(f2).read_text(encoding="utf-8", errors="replace")) + \
        s1b.parse("III", Path(f3).read_text(encoding="utf-8", errors="replace"))
    to_grid = Transformer.from_crs("EPSG:4326", "EPSG:28193", always_xy=True)
    for i, e in enumerate(entries):
        lat, lon = s1b.square_latlon(e["square"])
        gx, gy = to_grid.transform(lon, lat)
        e["gx"], e["gy"] = gx, gy - 1_000_000
        e["keys"] = s1b.name_keys(e["name"])
        e["uid"] = f"{e['vol']}-{i}"
        e["word_keys"] = {s1b.skeleton([w]) for w in re.findall(r"[A-Za-z]{4,}", s1b.strip_marks(e["text"]).lower())}
    return entries


def pick_swp(unit, ukeys, linked_names, entries):
    ux, uy = unit["x"], unit["y"]
    long_keys = {k for k in ukeys if len(k) >= 4}
    picked = []
    for e in entries:
        d = math.hypot(e["gx"] - ux, e["gy"] - uy)
        if d > SWP_MENTION_RADIUS_M:
            continue
        linked = (e["vol"], e["page"], e["name"], e["square"]) in linked_names
        named = bool(ukeys and e["keys"]) and s1b.name_match(ukeys, e["keys"]) >= s1b.MIN_SIMILARITY
        mentions = bool(long_keys & e["word_keys"])
        if linked or named or mentions:
            rank = 0 if linked else (1 if named else 2)
            picked.append((rank, d, e))
    picked.sort(key=lambda t: (t[0], t[1]))
    out = []
    for rank, d, e in picked[:SWP_MAX_ENTRIES]:
        out.append({"vol": e["vol"], "page": e["page"], "name": e["name"], "square": e["square"],
                    "how_found": ["linked in Stage 1b", "same name within 15 km", "text names the unit"][rank],
                    "square_centre_distance_m": round(d), "text": e["text"][:SWP_TEXT_CHARS]})
    return out


# ---------- main ----------

def coverage_class(survey_ref):
    ref = (survey_ref or "").strip()
    if not ref or ref.lower() == "nan":
        return "none"
    order = {"partial": 1, "full": 2}
    found = [cls for key, cls in COVERAGE["surveys"].items() if key in ref]
    return max(found, key=order.get) if found else COVERAGE["default_if_unlisted"]


def main(xlsx, f2, f3, highlands_pdf, nigro_pdf, s4_dir, out_dir):
    if s1a.sha256(Path(xlsx)) != s1a.WBADB_SHA256:
        sys.exit("WBADB hash does not match the frozen value")
    if sha256_file(highlands_pdf) != HIGHLANDS_SHA256:
        sys.exit("Highlands PDF hash does not match the frozen value")
    if sha256_file(nigro_pdf) != NIGRO_SHA256:
        sys.exit("Nigro 2011 PDF hash does not match the frozen value")
    out_dir = Path(out_dir)
    (out_dir / "packets").mkdir(parents=True, exist_ok=True)
    s4_dir = Path(s4_dir)

    book = pd.ExcelFile(xlsx)
    sur, exc = book.parse("Surveyed"), book.parse("Excavations")
    sur["row_id"] = "S" + sur["Index"].astype(str)
    exc["row_id"] = "E" + exc["Index"].astype(str)
    rows = pd.concat([sur, exc], ignore_index=True, sort=False)
    rows = rows[pd.to_numeric(rows["X"], errors="coerce").notna() & pd.to_numeric(rows["Y"], errors="coerce").notna()]
    rows["X"], rows["Y"] = rows["X"].astype(float), rows["Y"].astype(float)
    recs = [wbadb_record(r) for _, r in rows.iterrows()]
    by_id = {r["row_id"]: r for r in recs}

    with open(KOHLIT / "stage1a" / "stage1a_units.csv", newline="", encoding="utf-8") as f:
        u1a = {r["unit_id"]: r for r in csv.DictReader(f)}
    with open(KOHLIT / "stage1b" / "stage1b_units.csv", newline="", encoding="utf-8") as f:
        u1b = {r["unit_id"]: r for r in csv.DictReader(f)}
    linked = {}
    with open(KOHLIT / "stage1b" / "swp_entry_index.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            linked.setdefault(r["unit_id"], set()).add((r["vol"], int(r["page"]) if r["page"] else None,
                                                        r["swp_name"], r["square"]))

    swp = swp_entries(f2, f3)
    nigro = parse_nigro(nigro_pdf)
    nigro_by_no = {e["cat_no"]: e for e in nigro}

    stage2 = sorted(uid for uid, r in u1b.items() if r["stage1"] == "to Stage 2")
    manifest = []
    for uid in stage2:
        own = by_id[uid]
        a = u1a[uid]
        ux, uy = own["x"], own["y"]
        uprec = precision_m(ux, uy)
        unit = dict(own)
        unit.update({"precision_m": uprec, "main_set": a["main_set"] == "True", "in_R1": a["in_R1"] == "True",
                     "in_R2": a["in_R2"] == "True", "excavated": a["excavated"] == "True",
                     "coverage": coverage_class(own["survey_ref"]), "stage1a_hits": a["hits"],
                     "stage1b_swp_pool_words": u1b[uid]["swp_pool_words"]})

        near = []
        for r in recs:
            if r["row_id"] == uid:
                continue
            d = math.hypot(r["x"] - ux, r["y"] - uy)
            if d <= PACKET_RADIUS_M:
                g = geometry(ux, uy, uprec, r["x"], r["y"], precision_m(r["x"], r["y"]))
                near.append({**r, "geom": g})
        near.sort(key=lambda r: r["geom"]["distance_m"])

        ukeys = set(s1b.name_keys(own["name"]))
        for alt in re.split(r"[;,]", own["other_names"]):
            ukeys |= s1b.name_keys(alt)
        swp_sel = pick_swp(own, ukeys, linked.get(uid, set()), swp)

        s2 = {"survey_ref": own["survey_ref"], "status": "not accessed (not lawfully online to our knowledge)",
              "pages": []}
        pages = highlands_pages(own["survey_ref"])
        if pages:
            s2 = {"survey_ref": own["survey_ref"], "status": "read: Finkelstein et al. 1997 (open access, TAU)",
                  "pages": highlands_text(highlands_pdf, pages)}
        elif not own["survey_ref"]:
            s2["status"] = "no survey entry named in WBADB"

        s4 = {"status": "not excavated"}
        if unit["excavated"]:
            pub = own["publication"]
            first = pub.split(";")[0].strip() if pub else ""
            s4 = {"first_publication": first or None, "status": "none listed in WBADB" if not first else "not accessed"}
            d4 = s4_dir / uid
            if first and d4.is_dir():
                meta = json.loads((d4 / "meta.json").read_text(encoding="utf-8")) if (d4 / "meta.json").exists() else {}
                s4["status"] = meta.get("status", "not accessed")
                s4["access"] = meta.get("access", "")
                s4["excerpts"] = [p.read_text(encoding="utf-8") for p in sorted(d4.glob("excerpt*.txt"))]
                s4["plan_images"] = [str(p.resolve()) for p in sorted(d4.glob("*.png"))]

        nig = []
        for e in nigro:
            if e["x"] is None:
                continue
            d = math.hypot(e["x"] - ux, e["y"] - uy)
            if d <= PACKET_RADIUS_M:
                nig.append({"ref": f"N{e['cat_no']}", "cat_no": e["cat_no"], "name": e["name"], "page": e["page"],
                            "x": e["x"], "y": e["y"],
                            "geom": geometry(ux, uy, uprec, e["x"], e["y"], NIGRO_PRECISION_M), "text": e["text"]})
        in_oasis = bool(nig)
        if in_oasis:
            near_nos = {n["cat_no"] for n in nig}
            for e in nigro:          # entries placed only in words relative to a catalogue site within 2 km
                if e["x"] is None:
                    refs = {int(x) for x in re.findall(r"site n\.\s*(\d+)", e["location_words"])}
                    if refs & near_nos:
                        nig.append({"ref": f"N{e['cat_no']}", "cat_no": e["cat_no"], "name": e["name"],
                                    "page": e["page"], "x": None, "y": None, "geom": None, "text": e["text"]})
        nig.sort(key=lambda n: (n["geom"] is None, n["geom"]["distance_m"] if n["geom"] else 0))
        s5 = {"status": "in oasis: catalogue entries within 2 km" if in_oasis else "not in oasis (no catalogue entry within 2 km)",
              "entries": nig}

        packet = {"unit": unit, "source1_wbadb_within_2km": near, "source2_survey_entry": s2,
                  "source3_swp": swp_sel, "source4_first_publication": s4, "source5_nigro_2011": s5,
                  "built_with": {"script": "stage2/build_packets.py", "constants": PROTOCOL["version"]}}
        blob = json.dumps(packet, ensure_ascii=False, indent=1)
        (out_dir / "packets" / f"{uid}.json").write_text(blob + "\n", encoding="utf-8")
        manifest.append({"unit_id": uid, "name": own["name"], "main_set": unit["main_set"], "in_R2": unit["in_R2"],
                         "excavated": unit["excavated"], "coverage": unit["coverage"],
                         "n_wbadb_rows": len(near), "n_swp": len(swp_sel),
                         "source2": s2["status"].split(":")[0], "source4": s4["status"].split(":")[0],
                         "source5": "in oasis" if in_oasis else "not in oasis", "n_nigro": len(nig),
                         "packet_sha256": hashlib.sha256((blob + "\n").encode("utf-8")).hexdigest()})

    rng = random.Random(PROTOCOL["seed"])
    order = stage2[:]
    rng.shuffle(order)
    pos = {u: i for i, u in enumerate(order)}
    for m in manifest:
        m["coder_a_order"] = pos[m["unit_id"]]
    manifest.sort(key=lambda m: m["coder_a_order"])
    with open(out_dir / "packet_manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    print(json.dumps({"packets": len(manifest), "in_oasis": sum(m["source5"] == "in oasis" for m in manifest),
                      "highlands": sum(m["source2"] == "read" for m in manifest),
                      "excavated": sum(m["excavated"] for m in manifest),
                      "nigro_entries_parsed": len(nigro),
                      "nigro_with_coordinates": sum(e["x"] is not None for e in nigro)}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:8])
