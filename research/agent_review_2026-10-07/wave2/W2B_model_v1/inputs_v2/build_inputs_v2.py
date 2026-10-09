#!/usr/bin/env python3
"""Build the W2B v2 inputs: exact byte copies of the v1 inputs plus declared rows only.

    python3 -I build_inputs_v2.py [--check]

Additions (approved by the project owner; see research/models/search_effectiveness/README_v2.md):
  * places_v2.csv     + iv17_abu_saraj (Abu Saraj cave IV/17, cave-group reference, JERICHO region)
  * candidates_v2.csv + entry 60 at kh_qumran (project model M-QUMRAN, not a published Kohlit proposal)
                      + entry 25 at iv17_abu_saraj (Sion 2002, feature-level compatibility only)
  * grid_conversions_v2.csv + the IV/17 cave-group grid reference
Every other v2 file is a byte copy of its v1 file. The Old Israel Grid reference is converted with
W2B's own scripts/grid_convert.py oig() (EPSG:28191 -> WGS84, pyproj), imported by path and not edited.
`--check` rebuilds in memory and fails if any written file differs.

This is exploratory input work. It makes no identification claim.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W2B = HERE.parent
V1 = W2B / "inputs"
GRID_CONVERT = W2B / "scripts" / "grid_convert.py"

COPIES = ("entries", "name_groups", "kohlit_proposals")  # identical copies, suffix v1 -> v2

# --------------------------------------------------------------------------- declared additions
IV17_OIG = (190300, 144150)  # printed 19030/14415 (10 m units); Sion 2002 p. 61 Fig. 12; shared cave-group centre
IV17_SIGMA_KM = 0.3
METHOD = ('EPSG:28191 -> EPSG:4326 (pyproj, PROJ "Palestine 1923 to WGS 84 (1)"); '
          'identical to EPSG:28193 with N+1000 km')

# Control: an Old Israel Grid point with an independent WGS84 position near IV/17 (2.8 km).
CONTROL = dict(label="Tell es-Sultan, WBADB E334 anchor (research/assessments/kohlit_chain/chain.json M-SULTAN)",
               oig=(192150, 142050), ref_place="tell_es_sultan",
               ref_note="places_v1 tell_es_sultan (Wikidata Q2402267)")
# W2B's own first control (scripts/grid_convert.py CONTROLS), repeated as a second check.
CONTROL_W2B = dict(label="Qumran, Khirbet (NEAEHL table; W2B grid_convert.py CONTROLS[0])",
                   oig=(193620, 127720), ref_place="kh_qumran", ref_note="places_v1 kh_qumran (Pleiades 688011)")


def place_row(lat, lon):
    return {
        "place_id": "iv17_abu_saraj",
        "name": "Abu Saraj cave IV/17 (Cave of the Built Wall), Jebel Abu Saraj cliffs; cave-group reference",
        "lat": str(lat),
        "lon": str(lon),
        "sigma_km": f"{IV17_SIGMA_KM}",
        "mixture_of": "",
        "model_region": "JERICHO",
        "coords_in_places_json": "no",
        "precision_string": "~300 m (shared cave-group reference, not a mouth point)",
        "coord_note": ("Sion 2002, Atiqot 41 p. 61 Fig. 12 (IV/17 on pp. 63-64, Plan 5 p. 63): group reference "
                       "OIG 19030/14415, shared by several caves (research/assessments/entry25_iv17/README.md) "
                       "-> EPSG:28191->WGS84 with W2B scripts/grid_convert.py oig(). Control: WBADB E334 Tell es-Sultan "
                       "OIG 192150/142050 -> within 0.1 km of places_v1 tell_es_sultan. INFERENCE: sigma 0.3 km because "
                       "the group extent is not stated"),
        "components": "",
        "kind": "v2_candidate",
    }


CANDIDATE_ROWS = [
    {
        "entry": "60", "place_id": "kh_qumran", "status": "possible", "confidence": "weak", "order_derived": "no",
        "prior_override": "",
        "source": ("Project model, not a published Kohlit proposal: research/assessments/kohlit_chain/chain.json "
                   "M-QUMRAN; rarity count two of three (C2 caves north, WBADB S3835/E745 and S3824; C3 northern "
                   "cemetery, de Vaux 1973 pp. 57-58; C1 UNKNOWN)"),
        "conditional_on_reading": "xii10!=janoah", "kohlit_proposal": "no",
    },
    {
        "entry": "25", "place_id": "iv17_abu_saraj", "status": "possible", "confidence": "low", "order_derived": "no",
        "prior_override": "",
        "source": ("Sion 2002, Atiqot 41 pp. 61-64, Plan 5 p. 63 (IV/17: two openings, rock-cut pillar); "
                   "research/assessments/entry25_iv17 (feature-level compatibility; identification inconclusive)"),
        "conditional_on_reading": "", "kohlit_proposal": "no",
    },
]


def grid_row(lat, lon):
    return {
        "id": "iv17_abu_saraj_group", "label": "Abu Saraj cave group with IV/17 (Jebel Abu Saraj cliffs), shared reference",
        "oig_e": str(IV17_OIG[0]), "oig_n": str(IV17_OIG[1]), "grid_unit_m": "10",
        "lat": str(lat), "lon": str(lon), "method": METHOD,
        "source": ("Sion, Atiqot 41 (2002), Regions IV and VI, p. 61 Fig. 12 (Hebrew): group reference 19030/14415 shared "
                   "by several caves including IV/17 (registration/entry25_abu_saraj_features_2026-10-01.json)"),
    }


# --------------------------------------------------------------------------- helpers
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load_grid_convert():
    spec = importlib.util.spec_from_file_location("w2b_grid_convert", str(GRID_CONVERT))
    mod = importlib.util.module_from_spec(spec)
    keep = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # leave no cache in the W2B scripts folder
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


def header(raw):
    return next(csv.reader(io.StringIO(raw.decode("utf-8"))))


def append_rows(raw, rows):
    """v1 bytes unchanged, then the new rows in the same dialect (csv minimal quoting, CRLF)."""
    if not raw.endswith(b"\r\n"):
        raise SystemExit("v1 file does not end with CRLF; refusing to append")
    fields = header(raw)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\r\n")
    for r in rows:
        if set(r) != set(fields):
            raise SystemExit(f"row fields {sorted(r)} differ from header {fields}")
        w.writerow(r)
    return raw + buf.getvalue().encode("utf-8")


def round5(x):
    return round(x, 5)  # as W2B grid_convert.py writes grid_conversions.csv


def build():
    """Return {file name: bytes} for inputs_v2 and the additions record."""
    gc = load_grid_convert()
    with open(V1 / "places_v1.csv", encoding="utf-8") as f:
        places_v1 = {r["place_id"]: r for r in csv.DictReader(f)}
    lat, lon = gc.oig(*IV17_OIG)
    lat5, lon5 = round5(lat), round5(lon)

    # the conversion reproduces every W2B grid conversion (same function, same rounding)
    same = []
    with open(V1 / "grid_conversions.csv", encoding="utf-8") as f:
        grid_v1 = list(csv.DictReader(f))
    for r in grid_v1:
        la, lo = gc.oig(int(r["oig_e"]), int(r["oig_n"]))
        same.append(dict(id=r["id"], equal=(round(la, 5) == float(r["lat"]) and round(lo, 5) == float(r["lon"]))))
    if not all(s["equal"] for s in same):
        raise SystemExit(f"grid conversion does not reproduce W2B: {same}")

    controls = []
    for c in (CONTROL, CONTROL_W2B):
        la, lo = gc.oig(*c["oig"])
        p = places_v1[c["ref_place"]]
        d = gc.km(la, lo, float(p["lat"]), float(p["lon"]))
        controls.append(dict(label=c["label"], oig=list(c["oig"]), wgs84=[round5(la), round5(lo)],
                             reference=c["ref_note"], reference_wgs84=[float(p["lat"]), float(p["lon"])],
                             difference_km=round(d, 3)))
    if controls[0]["difference_km"] > 0.2:
        raise SystemExit(f"control check failed: {controls[0]}")

    dists = {pid: round(gc.km(lat5, lon5, float(places_v1[pid]["lat"]), float(places_v1[pid]["lon"])), 3)
             for pid in ("ain_duk", "doq", "tell_es_sultan", "nuweimeh", "kh_qumran")}

    out = {}
    raw = {}
    for stem in COPIES:
        raw[stem] = (V1 / f"{stem}_v1.csv").read_bytes()
        out[f"{stem}_v2.csv"] = raw[stem]
    raw["places"] = (V1 / "places_v1.csv").read_bytes()
    raw["candidates"] = (V1 / "candidates_v1.csv").read_bytes()
    raw["grid_conversions"] = (V1 / "grid_conversions.csv").read_bytes()
    prow = place_row(lat5, lon5)
    grow = grid_row(lat5, lon5)
    out["places_v2.csv"] = append_rows(raw["places"], [prow])
    out["candidates_v2.csv"] = append_rows(raw["candidates"], CANDIDATE_ROWS)
    out["grid_conversions_v2.csv"] = append_rows(raw["grid_conversions"], [grow])

    record = {
        "what": "W2B inputs v2 = v1 inputs plus the declared rows below; every other byte is copied from v1.",
        "date_utc": "2026-10-09",
        "readme": "research/models/search_effectiveness/README_v2.md",
        "generator": "inputs_v2/build_inputs_v2.py",
        "files": {},
        "declared_rows": {"places_v2.csv": [prow], "candidates_v2.csv": CANDIDATE_ROWS,
                          "grid_conversions_v2.csv": [grow]},
        "conversion": {
            "function": "scripts/grid_convert.py oig() (EPSG:28191 -> EPSG:4326), imported by path, unchanged",
            "iv17_group_oig": list(IV17_OIG), "iv17_group_wgs84": [lat5, lon5],
            "reproduces_w2b_grid_conversions": same,
            "controls": controls,
            "distance_km_from_iv17_group": dists,
        },
    }
    v1_names = {"entries": "entries_v1.csv", "name_groups": "name_groups_v1.csv",
                "kohlit_proposals": "kohlit_proposals_v1.csv", "places": "places_v1.csv",
                "candidates": "candidates_v1.csv", "grid_conversions": "grid_conversions.csv"}
    for stem, v1name in v1_names.items():
        v2name = f"{stem}_v2.csv"
        record["files"][v2name] = dict(
            from_v1=v1name, v1_sha256=sha256_bytes(raw[stem]), v2_sha256=sha256_bytes(out[v2name]),
            appended_rows=len(record["declared_rows"].get(v2name, [])))
    out["additions_v2.json"] = (json.dumps(record, indent=1, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify the written files instead of writing")
    a = ap.parse_args()
    out = build()
    if a.check:
        bad = [n for n, b in sorted(out.items()) if not (HERE / n).exists() or (HERE / n).read_bytes() != b]
        if bad:
            raise SystemExit(f"inputs_v2 differ from a fresh build: {bad}")
        print("inputs_v2 match a fresh build:", ", ".join(sorted(out)))
        return
    for n, b in sorted(out.items()):
        (HERE / n).write_bytes(b)
        print(f"wrote {n}  sha256 {sha256_bytes(b)}")
    rec = json.loads(out["additions_v2.json"])
    print("IV/17 group ->", rec["conversion"]["iv17_group_wgs84"], "controls:",
          [(c["label"].split(",")[0], c["difference_km"]) for c in rec["conversion"]["controls"]])


if __name__ == "__main__":
    main()
