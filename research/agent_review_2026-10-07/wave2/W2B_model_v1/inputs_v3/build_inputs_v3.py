#!/usr/bin/env python3
"""Build the W2B v3 inputs: inputs_v2 plus documented Peraea places for Goranson's Transjordan proposal.

    python3 -I -B build_inputs_v3.py [--check] [--off]

Rule (frozen in research/regional/peraea/PLAN_v3.md before any v3 run):
  the single place `transjordan` (two 15-km components at Machaerus and Amathus) keeps its place_id, region
  TRANSJ and every candidate row; only its `components` (and the two text fields that describe them) are
  replaced by an equal-weight mixture over the gazetteer sites with status `documented`, peraea_proper `yes`
  and a coordinate (research/regional/peraea/gazetteer.csv, column w2b_place_id = transjordan). Each site is
  one component lat:lon:sigma_km with its gazetteer sigma.
  grid_conversions_v3.csv appends the Palestine Grid conversions used by those sites.
  Every other v3 file is a byte copy of its v2 file.

`--off` builds with the change switched off; the result must be byte-identical to inputs_v2 (tested).
`--check` rebuilds in memory and fails if a written file differs. Exploratory; no identification claim.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
W2B = HERE.parent
V2 = W2B / "inputs_v2"
REPO = W2B.parents[3]
GAZ = REPO / "research/regional/peraea/gazetteer.csv"

COPIES = ("entries", "name_groups", "kohlit_proposals", "candidates")
TARGET = "transjordan"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read_rows(raw):
    return list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))


def write_rows(rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\r\n").writerows(rows)
    return buf.getvalue().encode("utf-8")


def peraea_sites(gaz_path=GAZ):
    with open(gaz_path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["w2b_place_id"] == TARGET]
    for r in rows:
        if not (r["status"] == "documented" and r["peraea_proper"] == "yes" and r["lat"] and r["lon"] and r["sigma_km"]):
            raise SystemExit(f"gazetteer row {r['site_id']} does not meet the v3 rule")
    return rows


def components_string(sites):
    return "|".join(f"{float(s['lat']):.5f}:{float(s['lon']):.5f}:{float(s['sigma_km']):g}" for s in sites)


def build(off=False, gaz_path=GAZ):
    out = {}
    raws = {stem: (V2 / f"{stem}_v2.csv").read_bytes() for stem in COPIES + ("places",)}
    raws["grid_conversions"] = (V2 / "grid_conversions_v2.csv").read_bytes()
    for stem in COPIES:
        out[f"{stem}_v3.csv"] = raws[stem]
    if off:
        out["places_v3.csv"] = raws["places"]
        out["grid_conversions_v3.csv"] = raws["grid_conversions"]
        return out
    sites = peraea_sites(gaz_path)
    rows = read_rows(raws["places"])
    head = rows[0]
    ix = {k: i for i, k in enumerate(head)}
    hit = [r for r in rows[1:] if r[ix["place_id"]] == TARGET]
    if len(hit) != 1:
        raise SystemExit("transjordan row not found exactly once")
    r = hit[0]
    old = list(r)
    r[ix["components"]] = components_string(sites)
    r[ix["precision_string"]] = f"mixture of {len(sites)} documented Peraea sites (gazetteer sigma each)"
    r[ix["coord_note"]] = ("v3: equal-weight mixture over the documented Second Temple sites of Peraea in "
                           "research/regional/peraea/gazetteer.csv (status documented, peraea_proper yes): "
                           + ", ".join(s["site_id"] for s in sites)
                           + ". Goranson names no site; this is a modelling proxy, not an identification")
    changed = [head[i] for i in range(len(head)) if old[i] != r[i]]
    if sorted(changed) != sorted(["components", "precision_string", "coord_note"]):
        raise SystemExit(f"unexpected changed fields: {changed}")
    out["places_v3.csv"] = write_rows(rows)
    g = read_rows(raws["grid_conversions"])
    gh = g[0]
    for s in sites:
        src = s["coord_source"]
        if not src.startswith("Palestine Grid "):
            continue
        e_txt, n_txt = src.split()[2].rstrip(";").split("/")
        e_km, n_km = float(e_txt), float(n_txt)
        decimals = max(len(t.split(".")[1]) if "." in t else 0 for t in (e_txt, n_txt))
        unit = {0: "1000", 1: "100", 2: "10", 3: "1"}[decimals]
        rec = dict(id=f"peraea_{s['site_id']}", label=s["name"], oig_e=str(int(round(e_km * 1000))),
                   oig_n=str(int(round(n_km * 1000))), grid_unit_m=unit, lat=s["lat"], lon=s["lon"],
                   method="EPSG:28191 -> EPSG:4326 (pyproj, W2B grid_convert.T191); Palestine Grid east of the Jordan",
                   source=src.split("; ", 1)[1] if "; " in src else src)
        g.append([rec[k] for k in gh])
    out["grid_conversions_v3.csv"] = write_rows(g)
    return out


def record(out, off_out, gaz_path=GAZ):
    sites = peraea_sites(gaz_path)
    files = {}
    for name, b in sorted(out.items()):
        v2name = name.replace("_v3.csv", "_v2.csv")
        files[name] = dict(from_v2=v2name, v2_sha256=sha256_bytes((V2 / v2name).read_bytes()),
                           v3_sha256=sha256_bytes(b), byte_copy=(b == (V2 / v2name).read_bytes()))
    return {
        "what": "W2B inputs v3 = inputs_v2 with the transjordan components replaced by documented Peraea sites",
        "date_utc": "2026-10-09",
        "plan": "research/regional/peraea/PLAN_v3.md",
        "generator": "inputs_v3/build_inputs_v3.py",
        "gazetteer_sha256": sha256_bytes(Path(gaz_path).read_bytes()),
        "sites": [dict(site_id=s["site_id"], lat=s["lat"], lon=s["lon"], sigma_km=s["sigma_km"]) for s in sites],
        "components": components_string(sites),
        "switch_off_equals_v2": all(off_out[n] == (V2 / n.replace("_v3.csv", "_v2.csv")).read_bytes() for n in off_out),
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--off", action="store_true", help="print whether the switched-off build equals inputs_v2")
    a = ap.parse_args()
    out = build()
    off_out = build(off=True)
    out["additions_v3.json"] = (json.dumps(record(out, off_out), indent=1, sort_keys=True) + "\n").encode("utf-8")
    if a.off:
        same = {n: off_out[n] == (V2 / n.replace("_v3.csv", "_v2.csv")).read_bytes() for n in sorted(off_out)}
        print("switched off == inputs_v2:", same)
        if not all(same.values()):
            raise SystemExit(1)
        return
    if a.check:
        bad = [n for n, b in sorted(out.items()) if not (HERE / n).exists() or (HERE / n).read_bytes() != b]
        if bad:
            raise SystemExit(f"inputs_v3 differ from a fresh build: {bad}")
        print("inputs_v3 match a fresh build:", ", ".join(sorted(out)))
        return
    for n, b in sorted(out.items()):
        (HERE / n).write_bytes(b)
        print(f"wrote {n}  sha256 {sha256_bytes(b)}")


if __name__ == "__main__":
    main()
