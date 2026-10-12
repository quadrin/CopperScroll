#!/usr/bin/env python3
"""Build the part-E (ʿAtiqot 42-121) screen, held list and PDF list from the committed data files.

Inputs (all in ../data, committed):
  atiqot_articles.csv     one row per article listing on the 80 volume pages (parse_volumes.py)
  screen_manual.csv       manual screen actions: drop_title (A3-style), add (name variant), check (location unknown)
  landing_meta.csv        first/last page, keywords, abstract hash from the fetched landing pages (extract_landing.py)
  kml_points.csv          portal location-map points (images.kml) for articles of vols 42-121
  landing_decisions.csv   placement decision for every fetched landing page (zone, basis, held, notes)
Outputs (part folder): screen.csv, held.csv, pdfs_needed.csv, summary.json. reports.csv and features.csv are
left with the phase-2 headers only (no article body read in this pass).
Deterministic; standard library only (phase-2 common.py for the frozen plan parameters and zones).

  python3 -I build_part_e.py
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen_lib as L  # noqa: E402

PART = L.PART
DATA = PART / "data"
ZONES_T1 = {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT"}

SCREEN_FIELDS = ["unit_id", "volume", "year", "item_no", "title", "authors", "first_page", "last_page",
                 "page_source", "language", "landing_url", "pdf_url", "pdf_size", "screen", "title_hits",
                 "manual_action", "manual_reason", "landing_fetched", "keywords", "kml_lat", "kml_lon", "kml_zone",
                 "zone", "zone_basis", "tier", "order_position_in_tier", "decision", "reason", "held",
                 "tier1_kh_almit", "protected_strip", "duplicate_of"]
HELD_FIELDS = ["unit_id", "volume", "year", "first_page", "last_page", "title", "authors", "landing_url",
               "first_line_seen", "held_area", "held", "tier1_kh_almit", "protected_strip", "note"]
PDF_FIELDS = ["tier", "order_position_in_tier", "unit_id", "title", "authors", "volume", "year", "first_page",
              "last_page", "pages", "landing_url", "pdf_url", "pdf_size", "zone", "zone_basis", "article_kind",
              "flag", "sha256_unit_id"]


def read(name):
    p = DATA / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def tier_of(zone, title, region_wide):
    if zone in ZONES_T1 or (region_wide and zone.startswith("REGION_WIDE")):
        return "T1"
    if zone == "Z4_JERUSALEM_HILLS":
        return "T3" if L.common.norm(title).strip().startswith("jerusalem") else "T2"
    return ""


def build():
    params = L.common.plan_params()
    pats = L.patterns(params)
    man = {(r["volume"], r["item_no"]): r for r in read("screen_manual.csv")}
    meta = {(r["volume"], r["item_no"]): r for r in read("landing_meta.csv")}
    kml = {(r["volume"], r["item_no"]): r for r in read("kml_points.csv")}
    dec = {(r["volume"], r["item_no"]): r for r in read("landing_decisions.csv")}

    rows, first_listing = [], {}
    for x in read("atiqot_articles.csv"):
        k = (x["volume"], x["item_no"])
        title, note, fp, lp, lang = L.split_title(x["title"])
        # Pages come only from the page note in the portal title. The landing pages' bepress_citation_firstpage
        # equals the portal item number, not a printed page (checked in tests), so it is not used.
        page_source = "page note in the portal title" if fp else "not shown on the portal (unit id uses item number)"
        m = meta.get(k)
        uid = L.unit_id(x["volume"], fp, x["item_no"], title)
        h = L.hits(x["title"], pats)
        mm = man.get(k, {})
        r = dict(x)
        r.update({"unit_id": uid, "title": x["title"], "first_page": fp, "last_page": lp, "page_source": page_source,
                  "language": lang or ("Hebrew" if "(Hebrew" in x["title"] else ""),
                  "title_hits": L.fmt_hits(h), "manual_action": mm.get("action", ""),
                  "manual_reason": mm.get("reason", ""), "landing_fetched": "yes" if m else "no",
                  "keywords": m["keywords"] if m else "", "held": "no", "tier1_kh_almit": "no",
                  "protected_strip": "no"})
        kp = kml.get(k)
        if kp:
            r["kml_lat"], r["kml_lon"] = kp["lat"], kp["lon"]
            r["kml_zone"] = L.common.zone_of(float(kp["lat"]), float(kp["lon"]), params) or "outside"
        r["screen"] = "S-GAZ" if h else ("S-MAN (manual, exploratory)" if mm.get("action") in ("add", "check") else "")
        if uid in first_listing:
            r.update({"decision": "duplicate listing", "duplicate_of": first_listing[uid],
                      "reason": "same article listed twice on the volume page (same title and pages); screened once"})
            r["unit_id"] = uid + "~i%s" % x["item_no"]
            rows.append(r)
            continue
        first_listing[uid] = "%s.%s" % k
        if mm.get("action") == "drop_title":
            r.update({"decision": "dropped: outside region by title (A3)", "reason": mm["reason"]})
        elif not h and not mm:
            r.update({"decision": "not a candidate", "reason": "no gazetteer term or A3 variant in the title; not added by the manual screen"})
        else:
            d = dec.get(k)
            if not d:
                r.update({"decision": "candidate: landing page not fetched", "reason": "no landing-page decision recorded"})
            else:
                r.update({"zone": d["zone"], "zone_basis": d["zone_basis"], "reason": d["note"],
                          "held": d.get("held", "no") or "no", "tier1_kh_almit": d.get("tier1_kh_almit", "no") or "no",
                          "protected_strip": d.get("protected_strip", "no") or "no",
                          "article_kind": d.get("article_kind", "")})
                if d["decision"] == "out":
                    r["decision"] = "dropped: outside region (landing page)"
                elif d["decision"] == "unlocated":
                    r["decision"] = "candidate: unlocated (PDF needed for the map reference)"
                    r["tier"] = "U"
                elif d["decision"] == "held":
                    r["decision"] = "held (citation and first line only)"
                else:
                    r["decision"] = "candidate: in region (PDF needed)"
                    r["tier"] = tier_of(d["zone"], title, "REGION_WIDE" in h)
                    if not r["tier"]:
                        raise SystemExit("no tier for %s" % uid)
        rows.append(r)

    # Order within tier: ascending SHA-256 of the unit id (plan section 3.4).
    for t in ("T1", "T2", "T3", "U"):
        ts = sorted((r for r in rows if r.get("tier") == t), key=lambda r: L.sha_order(r["unit_id"]))
        for n, r in enumerate(ts, 1):
            r["order_position_in_tier"] = str(n)
    return rows


def size_mb(s):
    n, u = s.split()
    return float(n.replace(",", "")) * {"KB": 1 / 1024, "MB": 1.0, "GB": 1024.0}[u]


def kind(title):
    t = L.common.norm(title)
    finds = ["coins", "glass", "pottery", "flint", "fauna", "faunal", "skeletal", "anthropological", "petrographic",
             "mollus", "animal", "bones", "seal", "scarab", "inscription", "lamps", "radiocarbon", "residue",
             "beads", "metal", "ceramic", "chalkstone", "graffiti", "stamp", "amulet", "pendant", "tag", "mold",
             "jar handles", "juglets", "dendroarch", "threads", "wood", "seeds", "fish"]
    if any((" " + w) in t for w in finds) and not any(w in t for w in [" excavation", " remains", " burial cave", " survey", " tomb", " quarry", " aqueduct", " pool", " cave "]):
        return "finds or specialist study (INFERENCE from title)"
    return "excavation, survey or site study (INFERENCE from title)"


def main():
    rows = build()
    write(PART / "screen.csv", SCREEN_FIELDS, rows)
    held = [r for r in rows if r.get("held") == "yes" or r.get("tier1_kh_almit") == "yes" or r.get("protected_strip") == "yes"]
    for r in held:
        d = {x["volume"] + "." + x["item_no"]: x for x in read("landing_decisions.csv")}.get(r["volume"] + "." + r["item_no"], {})
        r["first_line_seen"] = d.get("first_line_seen", "")
        r["held_area"] = d.get("held_area", "")
        r["note"] = d.get("note", "")
    write(PART / "held.csv", HELD_FIELDS, held)
    pdfs = []
    for r in rows:
        if r.get("tier") in ("T1", "T2", "T3", "U"):
            flags = []
            if r["held"] == "yes":
                flags.append("held")
            if r["tier1_kh_almit"] == "yes":
                flags.append("tier1_kh_almit")
            if r["protected_strip"] == "yes":
                flags.append("protected_strip")
            n = L.page_count(r["first_page"], r["last_page"])
            pdfs.append(dict(r, pages=n or "", flag=";".join(flags), article_kind=r.get("article_kind") or kind(r["title"]),
                             sha256_unit_id=L.sha_order(r["unit_id"])))
    order = {"T1": 0, "T2": 1, "T3": 2, "U": 3}
    pdfs.sort(key=lambda r: (order[r["tier"]], int(r["order_position_in_tier"])))
    write(PART / "pdfs_needed.csv", PDF_FIELDS, pdfs)

    dec = Counter(r["decision"] for r in rows)
    tiers = {}
    for t in ("T1", "T2", "T3", "U"):
        ps = [p for p in pdfs if p["tier"] == t]
        known = [int(p["pages"]) for p in ps if p["pages"]]
        tiers[t] = {"pdfs": len(ps), "with_page_range": len(known), "pages_known_total": sum(known),
                    "pdf_size_mb_total": round(sum(size_mb(p["pdf_size"]) for p in ps), 1)}
    zones = Counter((r.get("tier", ""), r.get("zone", "")) for r in pdfs)
    summary = {
        "volumes_screened": len({r["volume"] for r in rows}),
        "listings_screened": len(rows),
        "articles_screened": sum(1 for r in rows if r["decision"] != "duplicate listing"),
        "decisions": dict(sorted(dec.items())),
        "gazetteer_candidates": sum(1 for r in rows if r["screen"] == "S-GAZ"),
        "manual_screen_rows": sum(1 for r in rows if r["screen"].startswith("S-MAN")),
        "landing_pages_fetched": sum(1 for r in rows if r["landing_fetched"] == "yes"),
        "pdfs_needed": len(pdfs),
        "pdfs_by_tier": tiers,
        "pdfs_by_tier_zone": {"%s|%s" % k: v for k, v in sorted(zones.items())},
        "held": sum(1 for r in rows if r["held"] == "yes"),
        "tier1_kh_almit": sum(1 for r in rows if r["tier1_kh_almit"] == "yes"),
        "protected_strip": sum(1 for r in rows if r["protected_strip"] == "yes"),
        "reports_rows": 0,
        "features_rows": 0,
    }
    (PART / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(main(), indent=1, ensure_ascii=False))
