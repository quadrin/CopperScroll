#!/usr/bin/env python3
"""Screen every SWP Memoirs site entry (Section B, archaeology) of one volume.

Input: the entry list built in the scratch folder from the archive.org OCR (entries.json: headings,
squares, paragraph ranges and printed pages only), data/swp_fixes.csv (hand fixes of OCR headings).
Output: data/screen_swp<vol>.csv (committed; names, squares, pages, decisions; no body text).

Placement (plan section 2 and phase-4 PLAN part H): the zone comes from the SWP square where the
whole square (widened by swp_grid.MARGIN) lies in one zone or wholly outside the region; otherwise
from the frozen gazetteer by name (with the recorded spelling variants); otherwise an in-region
square split between zones gives 'zone unresolved' (read, coded to features_zone_unresolved.csv),
and a square split by the region boundary gives 'unlocated' (listed, not read).

Usage: screen_swp.py entries.json VOL out.csv
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
sys.path.insert(0, str(HERE))
import names  # noqa: E402
import swp_grid  # noqa: E402

FIXES = PART / "data" / "swp_fixes.csv"
FIELDS = ["unit_id", "vol", "sheet", "name_as_printed", "name", "square", "square_status", "zones_seen",
          "gazetteer_hits", "zone", "location_basis", "page_first", "page_last", "n_paras", "decision",
          "tier", "order_position_in_tier", "sha256_unit_id", "note"]
# valid square ranges per sheet (columns, rows) as printed in the headings of each sheet (OCR outliers excluded)
SHEET_RANGE = {
    "XVII": ("JKLMN", "stu"), "XVIII": ("MNOP", "rstu"), "XIX": ("BCDE", "uvwx"), "XX": ("DEFGHIJ", "uvwx"),
    "XXI": ("IJKLM", "uvwx"), "XXII": ("NO", "vwx"), "XXIII": ("CDE", "x"), "XXIV": ("DEFGHIJ", "xyz"),
    "XXV": ("IJKLM", "xyz"), "XXVI": ("NO", "yz"),
    "XI": ("IJKLMN", "nop"), "XII": ("NOPQ", "nop"), "XIV": ("JKLMN", "pqr"), "XV": ("NOPQ", "pqr"),
}
SHEETS_OUTSIDE = {"XIX", "XX", "XXIII", "XXIV"}  # every valid square of these sheets is outside the region


def load_fixes():
    out = {}
    if FIXES.exists():
        with open(FIXES, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out.setdefault((r["vol"], r["sheet"], r["key"]), []).append(r)
    return out


def tier_of(zones):
    if any(z in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT") for z in zones):
        return "T1"
    if zones:
        return "T2"  # no SWP or Guerin heading begins with 'Jerusalem' (T3)
    return ""


def screen(entries, vol, coef=None):
    coef = coef or swp_grid.fit()
    fixes = load_fixes()
    rows = []
    merged = []
    for e in entries:
        raw = e["name_raw"]
        name = names.clean_name(raw)
        key = names.slug(name)
        fx = fixes.get((str(vol), e["sheet"], key), [])
        acts = {f["action"]: f for f in fx}
        if "subsection" in acts:
            if merged:
                merged[-1]["p1"] = e["p1"]
                merged[-1]["page_last"] = e["page_last"]
                merged[-1]["n_paras"] += e["n_paras"]
                merged[-1].setdefault("subsections", []).append(name)
            continue
        e = dict(e, name=name, key=key, note=[])
        if "name" in acts:
            e["name"] = acts["name"]["value"]
            e["note"].append("name fixed: " + acts["name"]["reason"])
        if "square" in acts:
            e["square"] = acts["square"]["value"]
            e["note"].append("square fixed: " + acts["square"]["reason"])
        if "noentry" in acts:
            e["noentry"] = acts["noentry"]["reason"]
        merged.append(e)
    for e in merged:
        sq = e["square"]
        sheet = e["sheet"]
        rng = SHEET_RANGE.get(sheet)
        status, seen, zone, basis = "none", [], "", ""
        if sq:
            if rng and (sq[0] not in rng[0] or sq[1] not in rng[1]):
                status = "invalid (OCR)"
            else:
                z, status, seen = swp_grid.square_zone(sq, coef)
                if status == "clear":
                    zone = z or "OUTSIDE"
                    basis = "SWP square"
        hits = names.gaz_hits(e["name"])
        hit_txt = "; ".join("%s: %s" % (z, ",".join(h)) for z, h in sorted(hits.items()))
        decision = ""
        if e.get("noentry"):
            decision = "no description (%s)" % e["noentry"]
        elif zone == "OUTSIDE":
            decision = "out: square outside region"
        elif zone:
            decision = "candidate"
        elif sheet in SHEETS_OUTSIDE:
            zone, basis, decision = "OUTSIDE", "SWP sheet", "out: sheet outside region"
        else:
            # mixed, invalid or no square
            hz = sorted(hits)
            if status == "mixed":
                hz = [z for z in hz if z in seen]
            if len(hz) == 1:
                zone, basis, decision = hz[0], "name (gazetteer)", "candidate"
            elif len(hz) > 1:
                decision = "unlocated: name matches several zones"
            elif status == "mixed" and "OUTSIDE" not in seen:
                zone, basis, decision = "|".join(seen), "SWP square (zone split)", "candidate (zone unresolved)"
            elif status == "mixed":
                decision = "unlocated: square split by the region boundary"
            elif sheet in SHEETS_OUTSIDE:
                zone, basis, decision = "OUTSIDE", "SWP sheet", "out: sheet outside region"
            else:
                decision = "unlocated: no usable square, no gazetteer match"
        page = e["page_first"]
        uid = "SWP%s-%s-%s" % (vol, ("%03d" % page) if page is not None else "nopage", names.slug(e["name"]))
        zones = [z for z in zone.split("|") if z.startswith("Z")] if zone else []
        note = list(e["note"])
        if e.get("subsections"):
            note.append("subsections merged: " + "; ".join(e["subsections"]))
        rows.append(dict(unit_id=uid, vol=vol, sheet=sheet, name_as_printed=" ".join(e["name_raw"].split()),
                         name=e["name"], square=sq, square_status=status, zones_seen="|".join(seen),
                         gazetteer_hits=hit_txt, zone=zone, location_basis=basis, page_first=page,
                         page_last=e["page_last"], n_paras=e["n_paras"], decision=decision,
                         tier=tier_of(zones) if decision.startswith("candidate") else "",
                         order_position_in_tier="", sha256_unit_id=hashlib.sha256(uid.encode()).hexdigest(),
                         note="; ".join(note), p0=e["p0"], p1=e["p1"]))
    ids = [r["unit_id"] for r in rows]
    dup = {u for u in ids if ids.count(u) > 1}
    for r in rows:
        if r["unit_id"] in dup:
            r["unit_id"] += "-%s" % (r["square"].lower() or "x")
            r["sha256_unit_id"] = hashlib.sha256(r["unit_id"].encode()).hexdigest()
    for tier in ("T1", "T2", "T3"):
        q = sorted((r for r in rows if r["tier"] == tier), key=lambda r: r["sha256_unit_id"])
        for k, r in enumerate(q, 1):
            r["order_position_in_tier"] = k
    return rows


def main(entries_json, vol, out):
    d = json.load(open(entries_json, encoding="utf-8"))
    rows = screen(d["entries"], vol)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS + ["p0", "p1"], lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    from collections import Counter
    print(Counter(r["decision"] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
