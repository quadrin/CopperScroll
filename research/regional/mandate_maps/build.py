"""Build the coded tables of the Mandate 1:20,000 map regression.

    python3 -I research/regional/mandate_maps/build.py

Inputs (this folder): plan.json, windows.json, items_base.csv, g1_picks.csv, g2_controls.csv,
name_readings.csv, landscape_change.csv (optional), and the W2B gazetteer places_v2.csv.
Outputs (this folder): georef_check.json, georef_check.csv, features.csv, names.csv,
swp_comparison.csv, summary.json. Deterministic; standard library and pyproj only.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PLACES = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv"
_spec = importlib.util.spec_from_file_location("mm_lib", HERE / "mm_lib.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

FEATURE_CLASSES = ["spring", "cistern", "well", "well_or_cistern", "pool", "aqueduct", "ruin", "tomb", "cave",
                   "quarry", "road", "built_up", "mill", "tell", "shrine", "monastery_church", "other",
                   "symbol_unidentified"]
NAME_CLASSES = FEATURE_CLASSES + ["wadi", "landform", "locality"]
ACCEPTED_G1 = {"ok", "manual"}
# SWP sheet XVIII rows of places_v2 and the 1:20,000 item that prints the same name (or None)
SWP_PAIRS = [("buqeia", "B01", "SWP label 'Kh. es Sumrah' -> 1:20,000 'Karm es Samra (El ʿAjaz)' with R. square"),
             ("nuweimeh", "U01", "SWP 'Wady en Nueiameh' lower-course label -> 'W. en Nuʿeima' label"),
             ("ain_duk", "N02", "SWP 'Ain ed Duk' -> 'ʿEin ed Duyūk' spring dot"),
             ("tell_el_qos", None, "SWP 'Tell el Kos': no such name printed in the 1:20,000 window"),
             ("kuteif", "K01", "SWP 'Wady Ekteif' label -> 'W. Quteif' label"),
             ("asla", "A06", "SWP 'Jofet el Asla' hill label -> 'Jaufat el ʿAsla' label")]


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def r1(x):
    return "" if x is None else f"{x:.1f}"


def g1_residuals(picks):
    out = []
    for p in picks:
        if p["status"] not in ACCEPTED_G1:
            continue
        e, n = L.to_grid(float(p["tile_lat"]), float(p["tile_lon"]))
        E, N = float(p["grid_e"]), float(p["grid_n"])
        edge = (E % 10000 == 0) or (N % 10000 == 0)
        de, dn, d = L.residual((e, n), (E, N))
        out.append({**p, "tile_e": e, "tile_n": n, "dE": de, "dN": dn, "d": d, "sheet_edge": edge})
    return out


def corrections(g1, windows):
    """Per (window, sheet): a similarity fit tile->grid if >= 3 accepted interior picks there, else the sheet mean shift."""
    by_sheet = {}
    for r in g1:
        if not r["sheet_edge"]:
            by_sheet.setdefault(r["sheet"], []).append(r)
    sheet_mean = {s: (sum(r["dE"] for r in rs) / len(rs), sum(r["dN"] for r in rs) / len(rs)) for s, rs in by_sheet.items()}
    fits = {}
    for wname in windows:
        for s, rs in by_sheet.items():
            here = [r for r in rs if r["window"] == wname]
            if len(here) >= 3:
                fits[(wname, s)] = L.fit_similarity([(r["tile_e"], r["tile_n"]) for r in here],
                                                    [(float(r["grid_e"]), float(r["grid_n"])) for r in here])
    return sheet_mean, fits


def correct(window, e, n, sheet_mean, fits):
    s = L.sheet_of(e, n)
    if (window, s) in fits:
        ce, cn = L.apply_similarity(fits[(window, s)], (e, n))
        return ce, cn, s, f"window similarity fit to {window} grid picks"
    if s in sheet_mean:
        me, mn = sheet_mean[s]
        return e - me, n - mn, s, "sheet mean G1 shift"
    return e, n, s, "uncorrected (no G1 pick on this sheet)"


def main():
    plan = json.loads((HERE / "plan.json").read_text(encoding="utf-8"))
    roots = plan["toponym_flags"]["roots"]
    windows = json.loads((HERE / "windows.json").read_text(encoding="utf-8"))
    places = {r["place_id"]: r for r in read_csv(PLACES)}
    items = read_csv(HERE / "items_base.csv")
    picks = read_csv(HERE / "g1_picks.csv")
    controls = read_csv(HERE / "g2_controls.csv")
    readings = {r["name_as_printed"]: r["arabic_script_inferred"] for r in read_csv(HERE / "name_readings.csv")}
    lc_path = HERE / "landscape_change.csv"
    landscape = {r["item_id"]: r for r in read_csv(lc_path)} if lc_path.exists() else {}

    # G1
    g1 = g1_residuals(picks)
    sheet_mean, fits = corrections(g1, windows)
    g1_by_sheet = {}
    for r in g1:
        if not r["sheet_edge"]:
            g1_by_sheet.setdefault(r["sheet"], []).append((r["dE"], r["dN"]))
    counts = {}
    for p in picks:
        counts.setdefault(p["sheet"], {}).setdefault(p["status"], 0)
        counts[p["sheet"]][p["status"]] += 1

    # items: corrected positions
    pos = {}
    for it in items:
        e, n = L.to_grid(float(it["tile_lat"]), float(it["tile_lon"]))
        ce, cn, s, how = correct(it["window"], e, n, sheet_mean, fits)
        lat, lon = L.to_wgs(ce, cn)
        pos[it["item_id"]] = {"tile_e": e, "tile_n": n, "e": ce, "n": cn, "sheet": s, "correction": how, "lat": lat, "lon": lon}

    # G2
    g2 = []
    for c in controls:
        p = pos[c["item_id"]]
        re_, rn = L.to_grid(float(c["ref_lat"]), float(c["ref_lon"]))
        d0 = L.residual((p["tile_e"], p["tile_n"]), (re_, rn))
        d1 = L.residual((p["e"], p["n"]), (re_, rn))
        g2.append({**c, "sheet": p["sheet"], "published_dE": d0[0], "published_dN": d0[1], "published_d": d0[2],
                   "corrected_dE": d1[0], "corrected_dN": d1[1], "corrected_d": d1[2]})
    model = [r for r in g2 if r["used_for_error_model"] == "yes"]
    pooled = L.summary([(r["corrected_dE"], r["corrected_dN"]) for r in model])
    rms_by_sheet = {}
    for s in sorted({r["sheet"] for r in model}):
        v = [(r["corrected_dE"], r["corrected_dN"]) for r in model if r["sheet"] == s]
        if len(v) >= 2:
            rms_by_sheet[s] = L.summary(v)["rms_m"]

    def sheet_rms(s):
        return rms_by_sheet.get(s, pooled["rms_m"])

    # georef_check outputs
    sheets = sorted(set(counts) | set(g1_by_sheet))
    check = {"operation": L.operation_names(), "accepted_g1_status": sorted(ACCEPTED_G1),
             "note": "dE, dN = position on the published tiles (or after correction) minus the reference, in EPSG:28191 metres. Sheet-edge grid lines are excluded from G1 summaries.",
             "g1_by_sheet": {}, "g2_rows": [], "g2_error_model": {"pooled": pooled, "rms_by_sheet_m": rms_by_sheet},
             "g2_published_by_kind": {}}
    rows_csv = []
    for s in sheets:
        sm = L.summary(g1_by_sheet.get(s, []))
        check["g1_by_sheet"][s] = {"pick_counts": counts.get(s, {}), **sm}
        rows_csv.append({"check": "G1_grid", "sheet": s, "n": sm.get("n", 0), "mean_dE_m": r1(sm.get("mean_dE_m")),
                         "mean_dN_m": r1(sm.get("mean_dN_m")), "median_m": r1(sm.get("median_m")), "max_m": r1(sm.get("max_m")),
                         "rms_about_mean_m": r1(sm.get("rms_about_mean_m")), "reference": "nominal Palestine grid intersections"})
    for kind in sorted({r["kind"] for r in g2}):
        v = [(r["published_dE"], r["published_dN"]) for r in g2 if r["kind"] == kind]
        check["g2_published_by_kind"][kind] = L.summary(v)
    for r in g2:
        check["g2_rows"].append({k: (round(r[k], 1) if isinstance(r[k], float) else r[k]) for k in
                                 ("control_id", "kind", "item_id", "sheet", "ref_sigma_m", "published_dE", "published_dN",
                                  "published_d", "corrected_dE", "corrected_dN", "corrected_d", "used_for_error_model")})
        rows_csv.append({"check": "G2_" + r["kind"], "sheet": r["sheet"], "n": 1, "control_id": r["control_id"],
                         "item_id": r["item_id"], "published_d_m": r1(r["published_d"]), "corrected_d_m": r1(r["corrected_d"]),
                         "ref_sigma_m": r["ref_sigma_m"], "reference": r["reference"]})
    (HERE / "georef_check.json").write_text(json.dumps(check, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_csv(HERE / "georef_check.csv", rows_csv,
              ["check", "sheet", "n", "control_id", "item_id", "mean_dE_m", "mean_dN_m", "median_m", "max_m",
               "rms_about_mean_m", "published_d_m", "corrected_d_m", "ref_sigma_m", "reference"])

    # features and names
    feats, names = [], []
    for it in items:
        p = pos[it["item_id"]]
        w = windows[it["window"]]
        dists = []
        for pid in w["places"]:
            pl = places[pid]
            pe, pn = L.to_grid(float(pl["lat"]), float(pl["lon"]))
            dists.append((math.hypot(p["e"] - pe, p["n"] - pn), pid))
        dist, pid = min(dists)
        pick = float(it["pick_error_m"])
        err = math.hypot(pick, sheet_rms(p["sheet"]))
        lc = landscape.get(it["item_id"], {})
        protected = it["window"] == "T_jericho" and (191745.7 <= p["tile_e"] <= 192595.7) and (142066.9 <= p["tile_n"] <= 142746.9)
        base = {"item_id": it["item_id"], "window": it["window"], "place_id": pid, "distance_to_place_m": f"{dist:.0f}",
                "sheet": p["sheet"], "feature_class": it["feature_class"], "anchor_kind": it["anchor_kind"],
                "lat": f"{p['lat']:.6f}", "lon": f"{p['lon']:.6f}", "grid_e": f"{p['e']:.0f}", "grid_n": f"{p['n']:.0f}",
                "pick_error_m": f"{pick:.0f}", "sheet_rms_m": f"{sheet_rms(p['sheet']):.0f}", "position_error_m": f"{err:.0f}",
                "correction": p["correction"], "tile_lat": it["tile_lat"], "tile_lon": it["tile_lon"],
                "protected_zone": "yes (viewed after the fit was saved; registration rejected)" if protected else "no",
                "evidence_kind": "EVIDENCE (printed on the 1940s map)", "notes": it["notes"]}
        if it["feature_class"] in FEATURE_CLASSES:
            feats.append({**base, "label_as_printed": it["name_as_printed"],
                          "period_as_source": "not given (map)", "period_in_window": "unknown (map)",
                          "state_2025": lc.get("state_2025", "not_checked"), "state_basis": lc.get("basis", "")})
        if it["name_as_printed"] and not it["name_as_printed"].endswith("(trig)") and it["feature_class"] in NAME_CLASSES:
            flags = L.root_flags(it["name_as_printed"], roots)
            ctx = L.context_flag(it["name_as_printed"], it["window"])
            names.append({**base, "name_as_printed": it["name_as_printed"],
                          "name_translit": L.expand_translit(it["name_as_printed"]),
                          "arabic_script_inferred": readings.get(it["name_as_printed"], ""),
                          "flag_roots": ";".join(flags), "flag_context": "context" if ctx else "",
                          "flag_label": "INFERENCE (root or context match only; no identification claim)" if (flags or ctx) else ""})
    fcols = ["item_id", "window", "place_id", "distance_to_place_m", "sheet", "feature_class", "label_as_printed",
             "anchor_kind", "lat", "lon", "grid_e", "grid_n", "pick_error_m", "sheet_rms_m", "position_error_m",
             "period_as_source", "period_in_window", "state_2025", "state_basis", "protected_zone", "evidence_kind",
             "correction", "tile_lat", "tile_lon", "notes"]
    ncols = ["item_id", "window", "place_id", "distance_to_place_m", "sheet", "name_as_printed", "name_translit",
             "arabic_script_inferred", "feature_class", "anchor_kind", "lat", "lon", "grid_e", "grid_n", "pick_error_m",
             "sheet_rms_m", "position_error_m", "flag_roots", "flag_context", "flag_label", "protected_zone", "correction", "notes"]
    write_csv(HERE / "features.csv", feats, fcols)
    write_csv(HERE / "names.csv", names, ncols)

    # SWP sheet XVIII comparison
    swp = []
    for pid, item, note in SWP_PAIRS:
        pl = places[pid]
        se, sn = L.to_grid(float(pl["lat"]), float(pl["lon"]))
        row = {"place_id": pid, "swp_position": f"{float(pl['lat']):.5f}, {float(pl['lon']):.5f}",
               "swp_coord_note": pl["coord_note"], "swp_sigma_km": pl["sigma_km"], "item_id": item or "", "note": note}
        if item:
            p = pos[item]
            de, dn, d = L.residual((p["e"], p["n"]), (se, sn))
            row.update({"mandate_position": f"{p['lat']:.5f}, {p['lon']:.5f}", "dE_m": f"{de:.0f}", "dN_m": f"{dn:.0f}",
                        "distance_m": f"{d:.0f}",
                        "within_swp_sigma": "yes" if d <= float(pl["sigma_km"]) * 1000 else "no"})
        swp.append(row)
    write_csv(HERE / "swp_comparison.csv", swp,
              ["place_id", "item_id", "swp_position", "swp_sigma_km", "mandate_position", "dE_m", "dN_m", "distance_m",
               "within_swp_sigma", "note", "swp_coord_note"])

    flagged = [n for n in names if n["flag_roots"] or n["flag_context"]]
    summary = {"items": len(items), "features": len(feats), "names": len(names),
               "features_by_class": {c: sum(1 for f in feats if f["feature_class"] == c) for c in FEATURE_CLASSES},
               "flagged_names": [{"item_id": n["item_id"], "name": n["name_as_printed"], "roots": n["flag_roots"],
                                  "context": n["flag_context"]} for n in flagged],
               "state_2025_counts": {s: sum(1 for f in feats if f["state_2025"] == s) for s in
                                     sorted({f["state_2025"] for f in feats})},
               "g2_pooled_rms_m": round(pooled["rms_m"], 1), "g2_rms_by_sheet_m": {k: round(v, 1) for k, v in rms_by_sheet.items()},
               "windows_with_similarity_fit": sorted(f"{w}:{s}" for w, s in fits)}
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("items", "features", "names", "g2_pooled_rms_m", "g2_rms_by_sheet_m")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
