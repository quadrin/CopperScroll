#!/usr/bin/env python3
"""Screen every Guerin site heading ('each site description as he heads it') of one volume.

Input: the heading list built in the scratch folder from the archive.org OCR (gue entries.json: headings,
paragraph ranges, printed pages only) and data/gue_fixes.csv (hand fixes: sub-headings, non-entries, OCR names).
Output: data/screen_gue_<vol>.csv (committed; names, pages, decisions; no body text).

Guerin gives no map reference, so placement is by name only (plan section 2): the frozen phase-2 gazetteer,
with the recorded spelling variants (data/name_variants.csv, source GUE). A heading matching no term, or terms
in more than one zone, stays unlocated and is listed (not read). Region-wide terms do not place.

Usage: screen_gue.py entries.json VOL(J1|J2|J3|S1) out.csv
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
from screen_swp import FIELDS, tier_of  # noqa: E402

FIXES = PART / "data" / "gue_fixes.csv"


def load_fixes():
    out = {}
    if FIXES.exists():
        with open(FIXES, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out.setdefault((r["vol"], r["key"]), []).append(r)
    return out


def screen(entries, vol):
    fixes = load_fixes()
    merged = []
    for e in entries:
        name = names.clean_name(e["name_raw"])
        key = names.slug(name)
        acts = {f["action"]: f for f in fixes.get((vol, key), []) + fixes.get((vol, "%s@%s" % (key, e["page_first"])), [])}
        if "subsection" in acts and merged:
            merged[-1]["p1"] = e["p1"]
            merged[-1]["page_last"] = e["page_last"]
            merged[-1]["n_paras"] += e["n_paras"]
            merged[-1].setdefault("subsections", []).append(name)
            continue
        e = dict(e, name=name, key=key, note=[])
        if "name" in acts:
            e["name"] = acts["name"]["value"]
            e["note"].append("name fixed: " + acts["name"]["reason"])
        if "noentry" in acts:
            e["noentry"] = acts["noentry"]["reason"]
        merged.append(e)
    rows = []
    for e in merged:
        hits = {z: h for z, h in names.gaz_hits(e["name"]).items() if z != "REGION_WIDE"}
        rw = names.gaz_hits(e["name"]).get("REGION_WIDE", [])
        hit_txt = "; ".join("%s: %s" % (z, ",".join(h)) for z, h in sorted(hits.items()))
        zone, basis = "", ""
        if e.get("noentry"):
            decision = "no description (%s)" % e["noentry"]
        elif len(hits) == 1:
            zone, basis, decision = list(hits)[0], "name (gazetteer)", "candidate"
        elif len(hits) > 1:
            decision = "unlocated: name matches several zones"
        else:
            decision = "unlocated: no gazetteer match"
        page = e["page_first"]
        uid = "GUE-%s-%s-%s" % (vol, ("%03d" % page) if page is not None else "nopage", names.slug(e["name"]))
        tier = ""
        if decision == "candidate":
            tier = tier_of([zone])
            if zone == "Z4_JERUSALEM_HILLS" and names.slug(e["name"]).startswith("jerusalem"):
                tier = "T3"
        note = list(e["note"])
        if rw:
            note.append("region-wide term in the name: " + ",".join(rw))
        if e.get("subsections"):
            note.append("sub-headings merged: " + "; ".join(e["subsections"]))
        if e.get("chapter"):
            note.append("chapter: " + " ".join(e["chapter"].split())[:40])
        rows.append(dict(unit_id=uid, vol=vol, sheet=vol, name_as_printed=" ".join(e["name_raw"].split()),
                         name=e["name"], square="", square_status="none (Guerin gives no map reference)",
                         zones_seen="", gazetteer_hits=hit_txt, zone=zone, location_basis=basis, page_first=page,
                         page_last=e["page_last"], n_paras=e["n_paras"], decision=decision, tier=tier,
                         order_position_in_tier="", sha256_unit_id=hashlib.sha256(uid.encode()).hexdigest(),
                         note="; ".join(note), p0=e["p0"], p1=e["p1"]))
    ids = [r["unit_id"] for r in rows]
    dup = {u for u in ids if ids.count(u) > 1}
    seen = {}
    for r in rows:
        if r["unit_id"] in dup:
            seen[r["unit_id"]] = seen.get(r["unit_id"], 0) + 1
            r["unit_id"] += "-%d" % seen[r["unit_id"]]
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
