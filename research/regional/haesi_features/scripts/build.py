#!/usr/bin/env python3
"""Build the HA-ESI feature tables from the hand coding in data/coding_*.json.

Writes (to the output folder, default: this module's parent folder):
  features.csv, features_unlocated.csv, reports.csv, dropped.csv, looks_haesi.csv, summary.md, summary.json

Run from the repository root:
  python3 -I research/regional/haesi_features/scripts/build.py [--out DIR]
Standard library plus pyproj (as the W2B model). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import geo  # noqa: E402

REPO = HERE.parents[3]
W2B_IN = REPO / "research" / "agent_review_2026-10-07" / "wave2" / "W2B_model_v1" / "inputs_v2"
LOOKS_REF = REPO / "research" / "models" / "search_effectiveness" / "looks.csv"
PLAN = ROOT / "search_plan.json"
DATA = ROOT / "data"

TYPES = ["cistern", "pool_reservoir", "channel_aqueduct", "ritual_bath", "rockcut_installation",
         "tomb_burial_cave", "cave_with_finds", "wall_tower", "hoard_cache"]
P1_PLACES = {"tell_es_sultan", "ein_samiya", "kh_yanun", "muhalhil", "beit_kahil", "kuhlah", "carmel_siah", "mount_zion",
             "ein_ghuweir", "ein_feshkha", "iv17_abu_saraj", "nuweimeh", "ain_duk", "doq", "jericho_palaces", "jericho_area",
             "tell_el_qos", "choziba", "kuteif", "jordan_ford", "asla", "kh_qumran", "wadi_qumran", "buqeia", "gerizim", "jer_siloam"}
P2_PLACES = {"mar_saba", "hyrcania", "natuf", "tekoa_herodium", "beth_shean", "ibziq", "beth_horon", "kh_salhab"}
KIDRON = ["jer_kidron_mon", "jer_kidron_east", "jer_gethsemane", "jer_bir_ayyub", "mar_saba"]
SILOAM_TERMS = {"siloam", "silwan", "city of david", "ir david", "gihon", "ophel", "shiloah", "השילוח", "שילוח", "עיר דוד",
                "סילואן", "גיחון", "עופל", "הר ציון", "mount zion"}
KIDRON_TERMS = {"kidron", "qidron", "wadi en nar", "nahal qidron", "nahal kidron", "קדרון", "נחל קדרון", "ואדי א נאר"}
P1_GROUPS = {"JERICHO_ALL", "QUMRAN_ALL", "ein_samiya", "kh_yanun", "beit_kahil", "kuhlah", "carmel_siah", "buqeia",
             "gerizim", "R_JD_CLIFFS", "R_WADI_QELT"}
P2_GROUPS = {"mar_saba", "hyrcania", "natuf", "tekoa_herodium", "beth_shean", "ibziq", "beth_horon", "kh_salhab"}

FEATURE_FIELDS = ["report_id", "url", "series", "volume", "year", "pages", "site_name", "author", "permit",
                  "map_ref_as_given", "map_ref_used", "grid", "crs_used", "easting_m", "northing_m", "precision_m",
                  "lat", "lon", "coordinate_source", "feature_site", "nearest_place", "distance_km",
                  "places_within_2km", "places_within_5km", "regions", "feature_type", "n_features",
                  "period_as_given", "dated_in_window", "excavated_or_surveyed", "quote", "relevance",
                  "candidate_entries", "protected_strip", "screen"]
REPORT_FIELDS = ["report_id", "url", "access", "series", "volume", "year", "pages", "site_name", "author", "permit",
                 "screen", "toc_item", "map_ref_as_given", "map_ref_used", "grid", "crs_used", "lat", "lon",
                 "coordinate_source", "nearest_place", "distance_km", "places_within_2km", "places_within_5km",
                 "regions", "location_status", "excavated_or_surveyed", "area_depth_stated", "n_feature_rows",
                 "feature_types", "text_file", "text_lines", "text_sha256", "protected_strip", "location_note", "notes"]
DROP_FIELDS = ["candidate_id", "screen", "series", "volume", "year", "pages", "toc_text", "groups", "tier", "reason", "detail", "url"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def load_coding():
    reps = []
    for p in sorted(DATA.glob("coding_*.json")):
        reps.extend(json.loads(p.read_text(encoding="utf-8")))
    reps.sort(key=lambda r: r["report_id"])
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def boxes(plan):
    return {k: (v["lat"], v["lon"]) for k, v in plan["regions"].items() if isinstance(v, dict) and "lat" in v}


def regions_for(lat, lon, dists, title_norm, rep, bx):
    regs = set()
    if lat is not None:
        for k, (la, lo) in bx.items():
            if la[0] <= lat <= la[1] and lo[0] <= lon <= lo[1]:
                regs.add(k)
        d = dict((p, k) for k, p in dists)
        if any(d.get(p, 99) <= 2.0 for p in KIDRON):
            regs.add("R_KIDRON")
        if d.get("jer_siloam", 99) <= 1.0:
            regs.add("R_SILOAM_COD")
    if any(t in title_norm for t in SILOAM_TERMS if t not in ("הר ציון", "mount zion")):
        regs.add("R_SILOAM_COD")
    if any(t in title_norm for t in KIDRON_TERMS):
        regs.add("R_KIDRON")
    if rep.get("region_by_title"):
        regs.add(rep["region_by_title"])
    if "R_JD_CLIFFS" in regs and not (rep.get("region_by_title") == "R_JD_CLIFFS"):
        # box alone is not enough: cliff and cave reports only (plan)
        if not any(f["type"] == "cave_with_finds" for f in rep["features"]):
            regs.discard("R_JD_CLIFFS")
    return sorted(regs)


def locate(rep, places):
    """Return location dict for a report."""
    ref = rep.get("map_ref_used") or rep.get("map_ref")
    out = dict(grid="", crs_used="", e="", n="", unit="", lat=None, lon=None, source="", dists=[])
    if ref:
        r = geo.parse_ref(ref, rep.get("grid_label", ""))
        lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
        out.update(grid=r["grid"], crs_used="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                   unit=r["unit_m"], lat=lat, lon=lon,
                   source="map ref" + (" (order corrected; see location_note)" if rep.get("map_ref_used") or r["swapped"] else ""),
                   dists=geo.distances(lat, lon, places))
    elif rep.get("name_place"):
        p = next(p for p in places if p["place_id"] == rep["name_place"])
        out.update(lat=None, lon=None, source="name only (%s)" % rep["name_place"])
    return out


def fmt(x, nd):
    return "" if x is None or x == "" else ("%.*f" % (nd, x))


def tier_of_candidate(groups, terms):
    g = set(filter(None, groups.split(";")))
    t = set(filter(None, terms.split(";")))
    if g & P1_GROUPS or (("JER_ALL" in g) and (t & SILOAM_TERMS)):
        return "P1"
    if g & P2_GROUPS or (t & KIDRON_TERMS):
        return "P2"
    return "P3"


def author_only(toc_text, terms):
    """True if every matched term occurs only in the last ' , ' segment and that segment is an author field.

    Hebrew names may carry a one- or two-letter prefix (screen S2), so the title part is tested with the
    prefix-tolerant matcher. A last segment that starts with '(' belongs to the title.
    """
    import screen_toc as st
    parts = toc_text.split(" , ")
    if len(parts) < 2 or parts[-1].strip().startswith("("):
        return False
    title = st.norm(" , ".join(parts[:-1]))
    saved = st.S2
    st.S2 = True
    try:
        found = st.hits(title, [t for t in terms.split(";") if t])
    finally:
        st.S2 = saved
    return not found


def main(out_dir=ROOT):
    out_dir = Path(out_dir)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    bx = boxes(plan)
    places = geo.load_places(W2B_IN / "places_v2.csv")
    pmeta = {p["place_id"]: p for p in places}
    cands = read_csv(W2B_IN / "candidates_v2.csv")
    entries_by_place = defaultdict(list)
    for c in cands:
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))

    import screen_toc as st
    reps = load_coding()
    features, feat_unloc, reports, dropped, looks = [], [], [], [], []
    read_items = set()
    for rep in reps:
        if rep.get("toc_item"):
            read_items.add(rep["toc_item"])
        loc = locate(rep, places)
        dists = loc["dists"]
        nearest, dist = (dists[0][1], dists[0][0]) if dists else (rep.get("name_place", ""), None)
        w2 = [p for k, p in dists if k <= 2.0]
        w5 = [p for k, p in dists if k <= 5.0]
        if not dists and rep.get("name_place"):
            w2 = w5 = []
        title_norm = st.norm(rep["title"])
        regs = regions_for(loc["lat"], loc["lon"], dists, title_norm, rep, bx)
        if dists:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else ("beyond 5 km, in region" if regs else "beyond 5 km"))
        elif rep.get("name_place"):
            status = "name only"
        elif regs:
            status = "region by title only"
        else:
            status = "unlocated"
        in_scope = status in ("within 2 km", "2-5 km", "beyond 5 km, in region", "name only", "region by title only")
        frows = []
        for f in rep["features"]:
            fplace = f.get("place", None)
            row = dict(report_id=rep["report_id"], url=rep["item_url"], series=rep["series"], volume=rep["volume"],
                       year=rep["year"], pages=rep["pages"], site_name=rep["title"], author=rep["author"],
                       permit=rep.get("permit", ""), map_ref_as_given=rep.get("map_ref", ""),
                       map_ref_used=rep.get("map_ref_used", ""), grid=loc["grid"], crs_used=loc["crs_used"],
                       easting_m=loc["e"], northing_m=loc["n"], precision_m=loc["unit"],
                       lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5), coordinate_source=loc["source"],
                       feature_site=f.get("site", ""), nearest_place=nearest, distance_km=fmt(dist, 3),
                       places_within_2km=";".join(w2), places_within_5km=";".join(w5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance=f.get("rel", ""), protected_strip=rep.get("protected_strip", "no"),
                       screen=rep["screen"])
            if fplace is not None:  # multi-site report: the feature carries its own site
                row.update(coordinate_source=("feature site name (%s)" % fplace) if fplace else "region by title only",
                           nearest_place=fplace, distance_km="", places_within_2km="", places_within_5km="", lat="", lon="")
            place_for_entries = row["nearest_place"] if (dists and dist <= 2.0) or fplace or rep.get("name_place") else ""
            if fplace is not None:
                place_for_entries = fplace
            row["candidate_entries"] = ";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else ""
            assert f["type"] in TYPES, f["type"]
            assert f["window"] in ("yes", "no", "unknown"), f["window"]
            frows.append(row)
        if in_scope:
            features.extend(frows)
        else:
            feat_unloc.extend(frows)
            dropped.append(dict(candidate_id=rep["report_id"], screen=rep["screen"], series=rep["series"], volume=rep["volume"],
                                year=rep["year"], pages=rep["pages"], toc_text=rep["title"], groups="", tier="",
                                reason="read, not coded: " + ("no map reference and the title names no listed place" if status == "unlocated" else status),
                                detail=("features listed in features_unlocated.csv" if frows else "no coded feature") + ("; nearest %s at %s km" % (nearest, fmt(dist, 3)) if dists else ""),
                                url=rep["item_url"]))
        reports.append(dict(report_id=rep["report_id"], url=rep["item_url"], access=rep["access"], series=rep["series"],
                            volume=rep["volume"], year=rep["year"], pages=rep["pages"], site_name=rep["title"],
                            author=rep["author"], permit=rep.get("permit", ""), screen=rep["screen"],
                            toc_item=rep.get("toc_item", ""), map_ref_as_given=rep.get("map_ref", ""),
                            map_ref_used=rep.get("map_ref_used", ""), grid=loc["grid"], crs_used=loc["crs_used"],
                            lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5), coordinate_source=loc["source"],
                            nearest_place=nearest, distance_km=fmt(dist, 3), places_within_2km=";".join(w2),
                            places_within_5km=";".join(w5), regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows) if in_scope else 0,
                            feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=rep["text_file"], text_lines=rep.get("text_lines", ""), text_sha256=rep["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"), location_note=rep.get("location_note", ""),
                            notes=rep.get("notes", "")))
        # looks: places covered by this report
        covered = []
        if dists:
            for k, p in dists:
                if k <= max(pmeta[p]["sigma_km"], 0.3) + loc["unit"] / 1000.0:
                    covered.append((p, "map ref, %s km (cover radius %.2f km)" % (fmt(k, 3), max(pmeta[p]["sigma_km"], 0.3) + loc["unit"] / 1000.0)))
        elif rep.get("name_place"):
            covered.append((rep["name_place"], "title names the place; no map reference"))
        for f in rep["features"]:
            if f.get("place") and f["place"] not in [c[0] for c in covered]:
                covered.append((f["place"], "feature site named in the text (%s); no map reference" % f.get("site", "")))
        for p, how in covered:
            # features at p: those whose own site is p, plus report-level features when p is the report's location
            here = [f for f in rep["features"] if f.get("place") == p or ("place" not in f and not how.startswith("feature site"))]
            res = "reported" if here else "silent"
            kinds = ";".join("%s(%s)" % (f["type"], f["window"]) for f in here)
            for e in entries_by_place.get(p, []):
                looks.append(dict(entry_id=e, place_id=p, report=rep, how=how, result=res, kinds=kinds))
    # dropped: screen candidates not read
    rules = json.loads((DATA / "drop_rules.json").read_text(encoding="utf-8"))
    corpus = {r["item_key"]: r for r in read_csv(DATA / "corpus.csv")}
    screen = read_csv(DATA / "screen_candidates.csv")
    rid_by_item = {rep["toc_item"]: rep["report_id"] for rep in reps if rep.get("toc_item")}
    for c in screen:
        if c["item_key"] in read_items:
            continue
        vol = c["item_key"].split("#")[0] if "#" in c["item_key"] else "ha-esi_138"
        tier = tier_of_candidate(c["groups"], c["matched_terms"])
        par = rules.get("parallel_volumes", {}).get(vol)
        twins = [x for x in screen if par and x["item_key"].startswith(par + "#") and x["pages"] == c["pages"]] if par else []
        if twins and all(x["item_key"] in read_items for x in twins):
            reason, detail = "duplicate", "Hebrew version of read report(s) " + ";".join(sorted(rid_by_item[x["item_key"]] for x in twins))
        elif author_only(c["toc_text"], c["matched_terms"]):
            reason, detail = "screen false positive", "the matched name occurs only in the author field"
        elif c["item_key"] in rules["pages_absent"]:
            reason, detail = "not read: pages absent", rules["pages_absent"][c["item_key"]]
        elif vol in rules["readable_items"]:
            reason, detail = "not read: other", rules["readable_items"][vol]
        else:
            st_ = corpus.get(vol, {}).get("status", "not read: source not reachable")
            reason, detail = "not read (source not reachable)", st_
        dropped.append(dict(candidate_id=c["item_key"], screen=c["screen"], series=c["series"], volume=c["volume_title"],
                            year=c["year"], pages=c["pages"], toc_text=c["toc_text"], groups=c["groups"], tier=tier,
                            reason=reason, detail=detail, url=corpus.get(vol, {}).get("item_url", c["pdf_url"])))
    dropped.sort(key=lambda r: (r["reason"], r["tier"], r["candidate_id"]))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"]))
    feat_unloc.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"]))
    reports.sort(key=lambda r: r["report_id"])

    # looks table in the schema of looks.csv
    with open(LOOKS_REF, newline="", encoding="utf-8") as f:
        look_fields = next(csv.reader(f))
    looks.sort(key=lambda x: (x["report"]["report_id"], x["place_id"], int("".join(ch for ch in x["entry_id"] if ch.isdigit())), x["entry_id"]))
    lrows = []
    for i, lk in enumerate(looks, 1):
        rep = lk["report"]
        rec = "%s, %s %s (%s) %s, ‘%s’" % (rep["author"], rep["series"], rep["volume"], rep["year"],
                                                    ("p. " + rep["pages"]) if rep["series"] != "HA-ESI" else rep["pages"], rep["title"])
        area = rep.get("area_depth", "")
        lrows.append({
            "look_id": "H%03d" % i, "entry_id": lk["entry_id"], "place_id": lk["place_id"], "relation_id": "HAESI-COVER",
            "required_feature": "any HA-ESI coded feature type at the place (search_plan.json feature_types)",
            "reading_condition": "", "placement_relevant": "yes", "record": rec,
            "record_key": "%s %s %s" % (rep["series"], rep["volume"], rep["pages"]), "record_id": rep["report_id"],
            "lineage": "HA-ESI %s%s" % (rep["report_id"], (" (permit %s)" % rep["permit"]) if rep.get("permit") else ""),
            "looked_at": "%s; %s%s" % (rep["excavated_or_surveyed"], lk["how"], ("; stated area/depth: " + area) if area else ""),
            "coverage": "", "coverage_basis": "UNKNOWN: the report gives no target-area fraction" + ("; it states " + area if area else ""),
            "p_recognise": "", "p_recognise_basis": "UNKNOWN: not estimated here",
            "p_report": "", "p_report_basis": "UNKNOWN: not estimated here",
            "p_survive": "", "p_survive_basis": "UNKNOWN: not estimated here",
            "result": lk["result"], "result_basis": "EVIDENCE",
            "satisfies_requirement": "unknown", "counted_via": "",
            "project_use": "research/regional/haesi_features/features.csv",
            "notes": ("coded types (dated_in_window): " + lk["kinds"]) if lk["kinds"] else "no coded feature type at this place in this report",
        })
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "features_unlocated.csv", FEATURE_FIELDS, feat_unloc)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "dropped.csv", DROP_FIELDS, dropped)
    write_csv(out_dir / "looks_haesi.csv", look_fields, lrows)
    summary = summarize(features, reports, dropped, lrows, places)
    (out_dir / "summary.json").write_text(json.dumps(summary["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "summary.md").write_text(summary["md"], encoding="utf-8")
    print("features %d, unlocated features %d, reports %d, dropped %d, looks %d" % (len(features), len(feat_unloc), len(reports), len(dropped), len(lrows)))


def summarize(features, reports, dropped, lrows, places):
    pids = [p["place_id"] for p in places]
    # per place: features at that place (2 km by map ref, name only, feature site)
    by_place = defaultdict(Counter)
    win_place = defaultdict(Counter)
    for f in features:
        targets = set()
        if f["distance_km"]:
            targets = set(filter(None, f["places_within_2km"].split(";")))
        elif f["nearest_place"]:
            targets = {f["nearest_place"]}
        for p in targets:
            by_place[p][f["feature_type"]] += 1
            win_place[p][f["dated_in_window"]] += 1
    rep_place2, rep_place5 = Counter(), Counter()
    for r in reports:
        if r["location_status"] == "name only":
            rep_place2[r["nearest_place"]] += 1
            rep_place5[r["nearest_place"]] += 1
        for p in filter(None, r["places_within_2km"].split(";")):
            rep_place2[p] += 1
        for p in filter(None, r["places_within_5km"].split(";")):
            rep_place5[p] += 1
    feat_sites = defaultdict(set)
    for f in features:
        if f["coordinate_source"].startswith("feature site name") and f["nearest_place"]:
            feat_sites[f["nearest_place"]].add(f["report_id"])
    for p, s in feat_sites.items():
        rep_place2[p] += len(s)
        rep_place5[p] += len(s)
    lines = []
    lines.append("| place_id | reports within 2 km (incl. name-only) | reports within 5 km | feature rows (2 km) | dated in window: yes / no / unknown | feature types (rows) |")
    lines.append("|---|---|---|---|---|---|")
    silent = []
    for p in pids:
        if rep_place5[p] == 0:
            silent.append(p)
            continue
        c = by_place[p]
        lines.append("| %s | %d | %d | %d | %d / %d / %d | %s |" % (
            p, rep_place2[p], rep_place5[p], sum(c.values()), win_place[p]["yes"], win_place[p]["no"], win_place[p]["unknown"],
            ", ".join("%s %d" % (t, c[t]) for t in TYPES if c[t]) or "none"))
    type_tot = Counter(f["feature_type"] for f in features)
    win_tot = Counter(f["dated_in_window"] for f in features)
    reason_tot = Counter(d["reason"] for d in dropped)
    tier_unread = Counter((d["tier"]) for d in dropped if d["reason"].startswith("not read"))
    md = []
    md.append("# Summary tables (generated by scripts/build.py; do not edit)\n")
    md.append("Reports read: %d. Located within 5 km of a place, by name, or in a region: %d. Feature rows: %d (yes %d, no %d, unknown %d).\n" % (
        len(reports), sum(1 for r in reports if r["location_status"] not in ("beyond 5 km", "unlocated")), len(features),
        win_tot["yes"], win_tot["no"], win_tot["unknown"]))
    md.append("## Features per place (places with at least one report within 5 km)\n")
    md.extend(lines)
    md.append("\n## Feature rows by type\n")
    md.append("| feature_type | rows | dated in window (yes) |")
    md.append("|---|---|---|")
    for t in TYPES:
        md.append("| %s | %d | %d |" % (t, type_tot[t], sum(1 for f in features if f["feature_type"] == t and f["dated_in_window"] == "yes")))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | place (nearest or named) | distance_km | feature_type | period_as_given |")
    md.append("|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s |" % (f["report_id"], f["nearest_place"] or f["regions"], f["distance_km"] or "name or region", f["feature_type"], f["period_as_given"]))
    md.append("\n## Places with no read HA-ESI report within 5 km (silence, not absence)\n")
    md.append(", ".join(silent) + "\n")
    md.append("\n## Candidates not coded, by reason\n")
    md.append("| reason | rows |")
    md.append("|---|---|")
    for k in sorted(reason_tot):
        md.append("| %s | %d |" % (k, reason_tot[k]))
    md.append("\nUnread screen candidates by tier: " + ", ".join("%s %d" % (k, tier_unread[k]) for k in sorted(tier_unread)) + ".\n")
    md.append("\n## looks_haesi.csv\n")
    md.append("Rows: %d (reported %d, silent %d); places: %d; entries: %d.\n" % (
        len(lrows), sum(1 for r in lrows if r["result"] == "reported"), sum(1 for r in lrows if r["result"] == "silent"),
        len({r["place_id"] for r in lrows}), len({r["entry_id"] for r in lrows})))
    js = dict(reports=len(reports), features=len(features), window=dict(win_tot), types=dict(type_tot),
              reports_within_2km={p: rep_place2[p] for p in pids if rep_place2[p]},
              reports_within_5km={p: rep_place5[p] for p in pids if rep_place5[p]},
              silent_places=silent, dropped_by_reason=dict(reason_tot), unread_by_tier=dict(tier_unread),
              looks=len(lrows))
    return dict(md="\n".join(md) + "\n", json=js)


if __name__ == "__main__":
    out = ROOT
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
