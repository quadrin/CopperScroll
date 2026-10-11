#!/usr/bin/env python3
"""HA-ESI phase 3, part C: build the part-C tables from the hand coding and the heading screen.

Reads (part_c/data): coding_*.json (one file per volume), local_sources.csv, local_spans.csv,
        screen/<VOL>.screen.csv (made on the owner's computer by screen_volume.py and locate_headings.py),
        screen_overrides.csv, candidate_overrides.csv; phase-1 ../../data/screen_candidates.csv;
        the frozen phase-2 plan (PLAN.md JSON block) and the phase-1/phase-2 helpers, unchanged.
Writes (part_c): reports.csv and features.csv (phase-2 column order), screen.csv, candidates_checkoff.csv,
        summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_c/scripts/build_part_c.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
PART = HERE.parent
DATA = PART / "data"
PHASE3 = PART.parent
LANE = PHASE3.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; also puts the phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402  (phase-1 build: region boxes, W2B paths, field lists)

CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
SCREEN_FIELDS = ["vol", "series", "volume", "year", "heading_line", "ordered_page", "toc_page", "title", "authors",
                 "located", "n_maprefs", "first_mapref", "first_zone", "first_latlon", "zones_in_span", "title_hits",
                 "script_decision", "final_decision", "status", "coded_report_ids", "note"]
CHECK_FIELDS = ["item_key", "screen", "volume_title", "phase1_pages", "toc_text", "groups", "matched_terms", "vol",
                "matched_heading_line", "matched_toc_page", "matched_title", "match_basis", "status", "report_ids", "note"]
VOLS = ["ESI01", "ESI04", "ESI10", "ESI11", "ESI12", "ESI13", "ESI14", "ESI16", "ESI17", "ESI18", "ESI19", "ESI20",
        "HAESI109", "HAESI110", "HAESI111", "HAESI112", "HAESI113", "HAESI114", "HAESI115"]
# phase-1 screen_candidates.csv volume titles -> part-C volume keys
CAND_VOL = {"Excavations and Surveys in Israel %d" % n: "ESI%02d" % n for n in (1, 4, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20)}
CAND_VOL.update({"Ḥadashot Arkheologiyot חדשות ארכיאולוגיות %d" % n: "HAESI%d" % n for n in range(109, 116)})


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def fmt(x, nd):
    return "" if x is None or x == "" else ("%.*f" % (nd, x))


def vol_of(report_id):
    return report_id.split("-", 1)[0]


def first_page(report_id):
    return int(report_id.split("-")[1])


def ranges(spec):
    return [tuple(int(x) for x in r.split("-")) for r in spec.split(";")]


def load_coding():
    reps = []
    for p in sorted(DATA.glob("coding_*.json")):
        vol = p.stem.split("_", 1)[1]
        for r in json.loads(p.read_text(encoding="utf-8")):
            assert vol_of(r["report_id"]) == vol, (p.name, r["report_id"])
            reps.append(r)
    reps.sort(key=lambda r: r["report_id"])
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def locate_ref(ref, places, params):
    r = geo.parse_ref(ref)
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside",
                swapped=r["swapped"])


def tokens(s):
    return [t for t in common.norm(s).split() if t not in ("jerusalem", "the", "of", "and", "survey", "a")]


def build_reports(reps, params, places, entries_by_place, bx, sources, spans):
    features, reports, outside_feats = [], [], []
    for rep in reps:
        if rep.get("held"):
            continue  # held cave report: citation and first lines only (screen.csv), not a coded report
        vol = vol_of(rep["report_id"])
        src = sources[vol]
        url = src["portal_item_url"]
        access = "owner's Mac local PDF '%s' (SHA-256 %s), pdftotext -raw, reading-order text" % (
            src["local_file_name"], src["pdf_sha256"])
        sp = spans[rep["report_id"]]
        assert sp["text_lines"] == rep["text_lines"], rep["report_id"]
        assert not sp["quotes_not_found"], rep["report_id"]
        text_file = "%s.ordered.txt (outside the repository)" % vol
        pages = "%d%s" % (first_page(rep["report_id"]), "*" if rep["series"] == "HA-ESI" else "")
        exposure = rep.get("exposure") or "unexposed at freeze"
        if rep.get("map_ref") and not rep.get("map_ref_unusable"):
            loc = locate_ref(rep["map_ref"], places, params)
            src_txt = "map ref"
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[],
                       zone=rep.get("name_zone") or "unlocated", swapped=False)
            src_txt = "name only" + (" (%s)" % rep["name_place"] if rep.get("name_place") else "")
            if rep.get("map_ref_unusable"):
                src_txt += "; printed map reference unusable"
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else (rep.get("name_place", ""), None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(rep["title"]).strip(), rep, bx)
        if d:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else "beyond 5 km")
        elif rep.get("name_place"):
            status = "name only"
        else:
            status = "name only (zone)" if rep.get("name_zone") else "unlocated"
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rep["report_id"], f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rep["report_id"], f["window"])
            assert len(f["quote"].split()) <= 12, (rep["report_id"], f["quote"])
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src_txt, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate_ref(f["map_ref"], places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) or (fdist is None and fnear) else ""
            row = dict(report_id=rep["report_id"], url=url, series=rep["series"], volume=rep["volume"], year=rep["year"],
                       pages=pages, site_name=rep["title"], author=rep.get("author", ""),
                       permit=rep.get("permit", ""), map_ref_as_given=f.get("map_ref") or rep.get("map_ref", ""),
                       map_ref_used="", grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"],
                       precision_m=fl["unit"], lat=fmt(fl["lat"], 5), lon=fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen="S-LOC",
                       region_zone=fl["zone"], dist_to_nearest_place_km=fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=exposure)
            (frows if fl["zone"] in ZONES else outside_feats).append(row)
        features.extend(frows)
        notes = [rep.get("notes", "")]
        if rep.get("tier1_record"):
            notes.append("TIER-1 RECORD: " + rep["tier1_record"])
        if rep.get("screen_note"):
            notes.append(rep["screen_note"])
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=rep["series"], volume=rep["volume"],
                            year=rep["year"], pages=pages, site_name=rep["title"], author=rep.get("author", ""),
                            permit=rep.get("permit", ""), screen="S-LOC", toc_item="", map_ref_as_given=rep.get("map_ref", ""),
                            map_ref_used="", grid=loc["grid"], crs_used=loc["crs"], lat=fmt(loc["lat"], 5),
                            lon=fmt(loc["lon"], 5), coordinate_source=src_txt, nearest_place=nearest,
                            distance_km=fmt(dist, 3), places_within_2km=";".join(w2), places_within_5km=";".join(w5),
                            regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=text_file, text_lines=rep["text_lines"], text_sha256=sp["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"),
                            location_note=rep.get("location_note", ""), notes="; ".join(x for x in notes if x),
                            region_zone=loc["zone"], dist_to_nearest_place_km=fmt(dist, 3), exposure_at_freeze=exposure,
                            tier="S-LOC (whole volume)"))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])
    return features, reports, outside_feats


def generic_decision(d):
    if d.startswith("map ref not converted; name screen: no match"):
        return "outside region (no region name; map ref not converted)"
    if d.startswith("heading not located in body; name screen: no match"):
        return "outside region (no region name; heading not located in the body)"
    if d.startswith("no map ref; title names no region place"):
        return "outside region (no map ref; no region name)"
    if d.startswith("outside region"):
        return d
    return ""


def build_screen(reps, sources):
    overrides = {}
    for o in read_csv(DATA / "screen_overrides.csv"):
        key = (o["vol"], o["heading_line"]) if o["heading_line"] else (o["vol"], "", o["toc_page"], o["title"])
        overrides[key] = o
    used_over = set()
    rows = []
    for vol in VOLS:
        for r in read_csv(DATA / "screen" / ("%s.screen.csv" % vol)):
            r["script_decision"] = r.pop("decision")
            rows.append(r)
    by_vol = defaultdict(list)
    for r in rows:
        by_vol[r["vol"]].append(r)
    links = defaultdict(list)
    added = []
    for rep in reps:
        vol = vol_of(rep["report_id"])
        starts = [a for a, b in ranges(rep["text_lines"])]
        # the coded span may begin a line or two before the script's heading line (title split over two lines)
        hit = [r for r in by_vol[vol] if r["heading_line"]
               and any(a <= int(r["heading_line"]) <= min(b, a + 3) for a, b in ranges(rep["text_lines"]))]
        how = "heading line"
        if not hit:
            rt = tokens(rep["title"])
            hit = [r for r in by_vol[vol] if not r["heading_line"] and r["toc_page"].isdigit()
                   and int(r["toc_page"]) == first_page(rep["report_id"])
                   and (tokens(r["title"])[:2] == rt[:2] or (tokens(r["title"]) and set(tokens(r["title"])) <= set(rt)))]
            how = "contents row (heading located by hand)"
        if hit:
            r = hit[0]
            links[id(r)].append(rep)
            if how != "heading line":
                r.setdefault("_note", []).append("heading located by hand at line %d" % starts[0])
        else:
            src = sources[vol]
            nr = dict(vol=vol, series=rep["series"], volume=rep["volume"], year=rep["year"], heading_line=str(starts[0]),
                      ordered_page="", toc_page=str(first_page(rep["report_id"])), title=rep["title"],
                      authors=rep.get("author", ""), located="by hand (not a contents row)", n_maprefs="",
                      first_mapref=rep.get("map_ref", ""), first_zone="", first_latlon="", zones_in_span="",
                      title_hits="", script_decision="(not in the script screen)")
            nr["_note"] = ["item without its own contents row (sub-report, News in Brief item or exploratory addition)"]
            if rep.get("screen_note"):
                nr["_note"].append(rep["screen_note"])
            links[id(nr)].append(rep)
            added.append(nr)
            assert src
    rows.extend(added)
    out, problems = [], []
    for r in rows:
        key1 = (r["vol"], r["heading_line"])
        key2 = (r["vol"], "", r["toc_page"], r["title"])
        o = overrides.get(key1) if r["heading_line"] else None
        o = o or overrides.get(key2)
        recs = links.get(id(r), [])
        note = list(r.get("_note", []))
        held = [x for x in recs if x.get("held")]
        coded = [x for x in recs if not x.get("held")]
        if o:
            used_over.add((o["vol"], o["heading_line"], o["toc_page"], o["title"]))
            final = o["final_decision"]
            note.append(o["reason"])
        elif coded:
            sd = r["script_decision"]
            if sd.startswith("in region"):
                final = sd
            elif "name match Z" in sd or "name screen: Z" in sd:
                final = "in region (by name)"
            else:
                final = "in region (located by hand)"
        else:
            final = generic_decision(r["script_decision"])
        if held:
            status = "held: citation and first lines only"
        elif coded:
            status = "read and coded"
        elif final.startswith("not read"):
            status = final
        elif final.startswith(("in region", "part in region")) or not final:
            problems.append("%s %s p.%s %s | %s" % (r["vol"], r["heading_line"], r["toc_page"], r["title"], r["script_decision"]))
            status = "PROBLEM"
        else:
            status = "not coded (%s)" % final.split(" (")[0]
        src = sources[r["vol"]]
        out.append(dict(r, series=src["series"], volume=src["volume"], year=src["year"], final_decision=final,
                        status=status, coded_report_ids=";".join(x["report_id"] for x in recs), note="; ".join(note)))
    missing = set((o["vol"], o["heading_line"], o["toc_page"], o["title"]) for o in overrides.values()) - used_over
    assert not missing, "unused screen overrides: %s" % sorted(missing)
    assert not problems, "screen rows in the region without a coded report:\n" + "\n".join(problems)
    out.sort(key=lambda r: (VOLS.index(r["vol"]), int(r["heading_line"]) if r["heading_line"] else 10 ** 9,
                            int(r["toc_page"]) if r["toc_page"].isdigit() else 0, r["title"]))
    return out


def build_checkoff(screen):
    cands = [c for c in read_csv(LANE / "data" / "screen_candidates.csv") if c["volume_title"] in CAND_VOL]
    over = {o["item_key"]: o for o in read_csv(DATA / "candidate_overrides.csv")}
    by_vol = defaultdict(list)
    for s in screen:
        by_vol[s["vol"]].append(s)

    def score(c, s):
        ct = set(tokens(c["toc_text"]))
        st = tokens(s["title"])
        st = [t for t in st if not re.match(r"^[a-z]?\d", t)]  # drop permit numbers and years
        if not st:
            return 0.0
        return sum(1 for t in st if t in ct) / len(st)

    def page(s):
        return int(s["toc_page"]) if s["toc_page"].isdigit() else None

    # pass 1: unambiguous matches give each volume's page offset between the phase-1 list and the contents
    offs = defaultdict(list)
    for c in cands:
        vol = CAND_VOL[c["volume_title"]]
        sc = sorted(((score(c, s), i) for i, s in enumerate(by_vol[vol])), reverse=True)
        if sc and sc[0][0] >= 0.99 and (len(sc) == 1 or sc[1][0] < 0.6) and c["pages"].isdigit():
            p = page(by_vol[vol][sc[0][1]])
            if p is not None:
                offs[vol].append(p - int(c["pages"]))
    off = {v: median(o) for v, o in offs.items()}
    rows = []
    for c in cands:
        vol = CAND_VOL[c["volume_title"]]
        cp = int(c["pages"]) if c["pages"].isdigit() else None
        best, basis = None, ""
        if c["item_key"] in over:
            o = over[c["item_key"]]
            if o["heading_line"] or o["toc_page"]:
                m = [s for s in by_vol[vol] if (o["heading_line"] and s["heading_line"] == o["heading_line"])
                     or (not o["heading_line"] and s["toc_page"] == o["toc_page"] and s["title"] == o["title"])]
                assert len(m) == 1, (c["item_key"], len(m))
                best = m[0]
            basis = "by hand: " + o["note"]
        else:
            # every heading whose title words (minus 'Jerusalem', articles, permit numbers) are mostly in the
            # phase-1 contents text; several -> the one nearest the phase-1 page after the volume's median offset
            cand = []
            ct = set(tokens(c["toc_text"]))
            for s in by_vol[vol]:
                sc = score(c, s)
                if sc < 0.6:
                    continue
                ov = len(ct & set(tokens(s["title"])))
                p = page(s)
                pd = abs(p - (cp + off.get(vol, 0))) if (p is not None and cp is not None) else 999
                cand.append((-ov, pd, -sc, s["heading_line"] or "", s))
            cand.sort(key=lambda x: x[:4])
            if cand:
                best = cand[0][4]
                basis = "title words %.2f; %d heading(s) matched; page %s vs phase-1 %s (volume offset %+g)" % (
                    -cand[0][2], len(cand), best["toc_page"], c["pages"], off.get(vol, 0))
        if best is None:
            status, rid = ("not found in the volume" if not basis else over[c["item_key"]]["status"]), ""
        else:
            status, rid = best["status"], best["coded_report_ids"]
        rows.append(dict(item_key=c["item_key"], screen=c["screen"], volume_title=c["volume_title"], phase1_pages=c["pages"],
                         toc_text=c["toc_text"], groups=c["groups"], matched_terms=c["matched_terms"], vol=vol,
                         matched_heading_line=best["heading_line"] if best else "", matched_toc_page=best["toc_page"] if best else "",
                         matched_title=best["title"] if best else "", match_basis=basis, status=status, report_ids=rid,
                         note=best["final_decision"] if best else ""))
    rows.sort(key=lambda r: (VOLS.index(r["vol"]), r["item_key"]))
    return rows


def summarize(features, reports, outside_feats, screen, checkoff):
    md = ["# HA-ESI phase 3, part C: summary tables (generated by scripts/build_part_c.py; do not edit)\n"]
    in_reg = [r for r in reports if r["region_zone"] in ZONES]
    md.append("Reports read and coded: %d; in the region %d; outside or unlocated %d." % (
        len(reports), len(in_reg), len(reports) - len(in_reg)))
    md.append("Reports in the region with no eligible feature: %d.\n" % sum(1 for r in in_reg if r["n_feature_rows"] == 0))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). Rows outside the region (feature map ref): %d.\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"], len(outside_feats)))
    md.append("## Feature rows by class and zone (rows: yes / no / unknown)\n")
    md.append("| class | " + " | ".join(ZONES) + " | all |")
    md.append("|---|" + "---|" * (len(ZONES) + 1))
    tab = defaultdict(Counter)
    for f in features:
        tab[(f["feature_type"], f["region_zone"])][f["dated_in_window"]] += 1
        tab[(f["feature_type"], "all")][f["dated_in_window"]] += 1
    js_tab = {}
    for c in CLASSES:
        cells = []
        for z in ZONES + ["all"]:
            k = tab[(c, z)]
            n = sum(k.values())
            cells.append("%d (%d/%d/%d)" % (n, k["yes"], k["no"], k["unknown"]) if n else "0")
            js_tab["%s|%s" % (c, z)] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %s |" % (c, " | ".join(cells)))
    zt = Counter(f["region_zone"] for f in features)
    md.append("| all classes | " + " | ".join(str(zt[z]) for z in ZONES) + " | %d |" % len(features))
    md.append("\n## Reports by volume and zone\n")
    md.append("| volume | headings screened | " + " | ".join(ZONES) + " | other | feature rows |")
    md.append("|---|---|" + "---|" * (len(ZONES) + 2))
    js_vol = {}
    for v in VOLS:
        rr = [r for r in reports if vol_of(r["report_id"]) == v]
        nh = sum(1 for s in screen if s["vol"] == v)
        zc = Counter(r["region_zone"] for r in rr)
        nf = sum(int(r["n_feature_rows"]) for r in rr)
        md.append("| %s | %d | %s | %d | %d |" % (v, nh, " | ".join(str(zc[z]) for z in ZONES),
                                                sum(n for z, n in zc.items() if z not in ZONES), nf))
        js_vol[v] = dict(headings=nh, reports=len(rr), zones={z: zc[z] for z in ZONES}, feature_rows=nf)
    st = Counter(s["status"] for s in screen)
    md.append("\n## Screen status (all headings)\n")
    md.append("| status | rows |")
    md.append("|---|---|")
    for k in sorted(st):
        md.append("| %s | %d |" % (k, st[k]))
    ck = Counter(r["status"] for r in checkoff)
    md.append("\n## Phase-1 screen candidates in the part-C volumes (%d)\n" % len(checkoff))
    md.append("| status | candidates |")
    md.append("|---|---|")
    for k in sorted(ck):
        md.append("| %s | %d |" % (k, ck[k]))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | zone | nearest place (km) | class | subtype | period as given |")
    md.append("|---|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s | %s |" % (f["report_id"], f["region_zone"],
                      ("%s (%s)" % (f["nearest_place"], f["distance_km"])) if f["distance_km"] else (f["nearest_place"] or "name only"),
                      f["feature_type"], f["feature_subtype"].replace("|", "/"), f["period_as_given"].replace("|", "/")))
    js = dict(reports=len(reports), reports_in_region=len(in_reg), feature_rows=len(features), window=dict(wt),
              class_zone=js_tab, rows_by_zone={z: zt[z] for z in ZONES}, outside_feature_rows=len(outside_feats),
              volumes=js_vol, screen_status=dict(st), headings_screened=len(screen), candidates=dict(ck))
    return dict(md="\n".join(md) + "\n", json=js)


def main(out_dir=PART):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((LANE / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    sources = {r["text_file"]: r for r in read_csv(DATA / "local_sources.csv")}
    spans = {r["report_id"]: r for r in read_csv(DATA / "local_spans.csv")}
    reps = load_coding()
    assert set(spans) == {r["report_id"] for r in reps}, "local_spans.csv and coding disagree"
    features, reports, outside_feats = build_reports(reps, params, places, entries_by_place, bx, sources, spans)
    screen = build_screen(reps, sources)
    checkoff = build_checkoff(screen)
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "screen.csv", SCREEN_FIELDS, screen)
    write_csv(out_dir / "candidates_checkoff.csv", CHECK_FIELDS, checkoff)
    summ = summarize(features, reports, outside_feats, screen, checkoff)
    (out_dir / "summary.json").write_text(json.dumps(summ["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "summary.md").write_text(summ["md"], encoding="utf-8")
    print("reports %d (in region %d), feature rows %d (outside region %d), screen rows %d, candidates %d" % (
        len(reports), sum(1 for r in reports if r["region_zone"] in ZONES), len(features), len(outside_feats),
        len(screen), len(checkoff)))


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
