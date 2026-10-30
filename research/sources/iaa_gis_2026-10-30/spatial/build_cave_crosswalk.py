"""Build the cave crosswalk: IAA CaveAtlas -> repository cave register -> de Vaux.

Usage:
    python3 build_cave_crosswalk.py [--atlas data/cave_atlas.csv]
                                    [--repo data/repo_caves.csv]
                                    [--out data/cave_crosswalk.csv]

The three registers are independent:

  IAA CaveAtlas        151 cave points with a Hebrew name, ITM grid, elevation
                       and an excavated flag. Names may carry a Q siglum
                       ("מערת קומראן Q11") or a de Vaux site number
                       ("מערת קומראן 24").
  Repository register  research/regional/caves_entry25/caves.csv, keyed by
                       cave_id (DJD3:8, A41:XI/19, ...). DJD3 rows carry the
                       de Vaux 1952 site number and, for some, coordinates.
  de Vaux 1952 points  research/history/devaux1952_cave_points; already the
                       source of the DJD3 coordinates, so not compared twice.

Matching is explicit: a Q siglum, an exact name alias, or a de Vaux site
number. Distance alone never creates a match; the nearest register row is
reported as a lead with confidence "none".
"""
import argparse
import csv
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent

# DJD III p. 6 states only four equivalences. Everything else is a reading.
SIGLUM_TO_DEVAUX = {"1Q": 14, "2Q": 19, "3Q": 8, "6Q": 26}

# Curated name aliases: IAA Hebrew name fragment -> exact repository cave_id.
# Each pair was checked against the register's own name/other_ids, not distance.
ALIASES = [
    ("מכלול התאומות", "REPO:TwinCave", "Twin Cave complex"),
    ("פכית שמן האפרסמון", "A41:X/35", "Balsam Oil Juglet Cave"),
    ("המרגלים-אביאור", "A41:VIII/9", "Large Caves Complex / Cave of the Spies"),
    ("מערת הסנדל", "A41:VIII/28", "Cave of the Sandal"),
    ("מערת הלוחם", "A41:III/13", "Cave of the Warrior"),
    ("מערת האגרות", "ASI:147-429", "Cave of the Letters"),
    ("מערת סלוודורה", "Z23:Salvadora", "Salvadora Cave"),
]

QRE = re.compile(r"(?<![0-9A-Za-z])Q\s?(\d{1,2})(?![0-9])")
DVRE = re.compile(r"קומראן\s+(\d{1,2})")


def haversine(a, b, c, d):
    r = 6_371_008.8
    p1, p2 = math.radians(a), math.radians(c)
    dp = p2 - p1
    dl = math.radians(d - b)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def siglum_token(q, text):
    """Exact Q-siglum match: 1Q must not match 11Q or 21Q."""
    return re.search(rf"(?<![0-9A-Za-z]){re.escape(q)}(?![0-9A-Za-z])", text) is not None


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atlas", default=str(ROOT / "data/cave_atlas.csv"))
    ap.add_argument("--repo", default=str(ROOT / "data/repo_caves.csv"))
    ap.add_argument("--out", default=str(ROOT / "data/cave_crosswalk.csv"))
    args = ap.parse_args()

    atlas = load(args.atlas)
    repo = load(args.repo)
    repo_by_id = {r["cave_id"]: r for r in repo}
    repo_geo = [r for r in repo if r["lat"] and r["lon"]]

    out = []
    for a in atlas:
        name = a["name_heb"]
        lat, lon = float(a["lat"]), float(a["lon"])

        q = None
        m = QRE.search(name)
        if m:
            q = f"{m.group(1)}Q"

        dv = None
        m2 = DVRE.search(name)
        if m2:
            dv = int(m2.group(1))
        elif q in SIGLUM_TO_DEVAUX:
            dv = SIGLUM_TO_DEVAUX[q]

        match = None
        match_type = "none"
        confidence = "none"
        note = ""

        # 1. Q siglum, explicit in the name.
        if q:
            hits = [r for r in repo
                    if siglum_token(q, r["cave_id"])
                    or siglum_token(q, r["name_number"])
                    or siglum_token(q, r["other_ids"])]
            if hits:
                hits.sort(key=lambda r: 0 if r["lat"] else 1)
                match = hits[0]
                match_type = "siglum"
                confidence = "high"
                note = f"name carries {q}"
                if "ליד" in name:
                    confidence = "medium"
                    note = f"name says the cave is *near* {q}, not that it is {q}"
            else:
                note = f"name carries {q}; no register row for it"

        # 2. de Vaux site number in the name.
        if match is None and dv is not None:
            row_id = f"DJD3:{dv}"
            if row_id in repo_by_id:
                match = repo_by_id[row_id]
                match_type = "devaux_number"
                confidence = "high"
                note = f"name carries de Vaux site {dv}"

        # 3. Wadi Murabba'at: numbered cave groups 1-4.
        if match is None and "מורבעאת" in name:
            m3 = re.search(r"מורבעאת\s+(\d)", name) or re.search(r"מערה\s+(\d)", name)
            target = f"Z23:Murabbaat-{m3.group(1)}" if m3 else "Z23:Murabbaat-1"
            if target in repo_by_id:
                match = repo_by_id[target]
                match_type = "alias"
                confidence = "high"
                note = f"named Murabba'at cave {m3.group(1) if m3 else 1}"

        # 4. Curated name alias, exact repository id.
        if match is None:
            for heb, cid, basis in ALIASES:
                if heb in name:
                    if cid in repo_by_id:
                        match = repo_by_id[cid]
                        match_type = "alias"
                        confidence = "high"
                        note = f"name alias: {basis}"
                    else:
                        note = f"name alias {basis}: register row {cid} missing"
                    break

        # Nearest register row, always reported, never a match.
        near = None
        for r in repo_geo:
            d = haversine(lat, lon, float(r["lat"]), float(r["lon"]))
            if near is None or d < near[1]:
                near = (r, d)

        offset = None
        if match is not None and match["lat"] and match["lon"]:
            offset = round(haversine(lat, lon, float(match["lat"]), float(match["lon"])))

        if match is not None and not match["lat"]:
            note = (note + "; register row has no coordinates").strip("; ")
        flag = ""
        if offset is not None and match["precision_m"]:
            try:
                if offset > float(match["precision_m"]):
                    flag = "beyond register precision"
            except ValueError:
                pass
        if offset is not None and offset > 1000:
            flag = "offset >1 km"
        if match is not None and match.get("coord_ok") == "no":
            flag = "register coordinate flagged inaccurate"
        if dv is not None and match is None:
            flag = "IAA has a point for a de Vaux site the register lacks"

        out.append({
            "iaa_objectid": a["objectid"],
            "iaa_name_heb": name,
            "iaa_itm_x": a["itm_x"],
            "iaa_itm_y": a["itm_y"],
            "iaa_lat": a["lat"],
            "iaa_lon": a["lon"],
            "iaa_elevation_m": a["elevation_m"],
            "iaa_excavated": a["excavated"],
            "q_siglum": q or "",
            "devaux_site": dv if dv is not None else "",
            "repo_cave_id": match["cave_id"] if match else "",
            "repo_name": match["name_number"] if match else "",
            "repo_lat": match["lat"] if match else "",
            "repo_lon": match["lon"] if match else "",
            "repo_precision_m": match["precision_m"] if match else "",
            "repo_coord_ok": match["coord_ok"] if match else "",
            "offset_m": offset if offset is not None else "",
            "offset_flag": flag,
            "match_type": match_type,
            "confidence": confidence,
            "note": note,
            "nearest_repo_cave_id": near[0]["cave_id"] if near else "",
            "nearest_repo_dist_m": round(near[1]) if near else "",
        })

    order = {"high": 0, "medium": 1, "none": 2}
    out.sort(key=lambda r: (order[r["confidence"]],
                            r["devaux_site"] if r["devaux_site"] != "" else 999,
                            r["iaa_name_heb"]))
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    matched = [r for r in out if r["match_type"] != "none"]
    summary = {
        "atlas_rows": len(out),
        "matched": len(matched),
        "matched_with_offset": sum(1 for r in matched if r["offset_m"] != ""),
        "siglum_matches": sum(1 for r in out if r["match_type"] == "siglum"),
        "devaux_number_matches": sum(1 for r in out if r["match_type"] == "devaux_number"),
        "alias_matches": sum(1 for r in out if r["match_type"] == "alias"),
        "unmatched": sum(1 for r in out if r["match_type"] == "none"),
        "matches": [
            {k: r[k] for k in ("iaa_name_heb", "q_siglum", "devaux_site",
                                "repo_cave_id", "offset_m", "match_type", "confidence")}
            for r in matched
        ],
    }
    with open(pathlib.Path(args.out).with_name("cave_crosswalk_summary.json"),
              "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
