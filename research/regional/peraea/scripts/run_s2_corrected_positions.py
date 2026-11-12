#!/usr/bin/env python3
"""Exploratory variant, added after the frozen v3 run (PLAN_v3.md: 'Anything added later is labelled a new
exploratory variant'): S2_broad with three corrected site positions.

    python3 -I -B research/regional/peraea/scripts/run_s2_corrected_positions.py [--check]

The frozen files (gazetteer.csv, build_gazetteer.py, PLAN_v3.md, outputs_v3/) are not changed. The corrections
are read from gazetteer_position_corrections_2026-11-11.csv and applied in memory to the rows of the frozen
gazetteer. Only the sensitivity variant S2_broad uses the three sites (their w2b_place_id is empty), so only
S2_broad is run again: one time with the frozen positions (must reproduce outputs_v3/results_v3.json) and one
time with the corrected positions. sigma_km is not changed.
Output: research/regional/peraea/exploratory/s2_corrected_positions_2026-11-11.json. No identification claim.
"""
import argparse
import csv
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERAEA = HERE.parent
COR = PERAEA / "gazetteer_position_corrections_2026-11-11.csv"
OUT = PERAEA / "exploratory" / "s2_corrected_positions_2026-11-11.json"


def load_run_v3():
    spec = importlib.util.spec_from_file_location("run_v3", HERE / "run_v3.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["run_v3"] = mod
    spec.loader.exec_module(mod)
    return mod


def corrections():
    with open(COR, encoding="utf-8") as f:
        return {r["site_id"]: r for r in csv.DictReader(f)}


def broad_rows(rv, cor=None):
    rows = [dict(r) for r in rv.gaz_rows()
            if r["peraea_proper"] == "yes" and r["lat"] and r["status"] in ("documented", "partial")]
    if cor:
        for r in rows:
            if r["site_id"] in cor:
                r["lat"], r["lon"] = cor[r["site_id"]]["corrected_lat"], cor[r["site_id"]]["corrected_lon"]
    return rows


def compute():
    rv = load_run_v3()
    plan = rv.load_plan()
    rv.check_frozen(plan)
    cor = corrections()
    d2 = rv.load_data(rv.IN_V2, "v2")
    v2 = rv.run(d2)
    frozen_rows, corrected_rows = broad_rows(rv), broad_rows(rv, cor)
    missing = sorted(set(cor) - {r["site_id"] for r in frozen_rows})
    if missing:
        raise SystemExit(f"corrected sites are not in S2_broad: {missing}")
    rf = rv.run(rv.set_components(d2, rv.comps_of(frozen_rows)))
    rc = rv.run(rv.set_components(d2, rv.comps_of(corrected_rows)))
    kf, kc = rv.kohlit_report(rf, v2), rv.kohlit_report(rc, v2)
    ref = json.loads((rv.OUT_V3 / "results_v3.json").read_text(encoding="utf-8"))["kohlit"]["S2_broad"]
    repro = max(abs(kf["entries"][e]["P_transjordan"] - ref["entries"][e]["P_transjordan"]) for e in kf["entries"])
    repro = max(repro, abs(kf["kohlit_latent"]["P_transjordan"] - ref["kohlit_latent"]["P_transjordan"]))
    per_entry = {e: rv.tv(rc["post"][e], rf["post"][e]) for e in rf["order"]}
    worst = max(per_entry, key=per_entry.get)
    res = dict(
        label="exploratory, added 2026-11-11 after the frozen v3 run; not a part of PLAN_v3",
        corrected_sites={k: dict(frozen=[float(v["frozen_lat"]), float(v["frozen_lon"])],
                                 corrected=[float(v["corrected_lat"]), float(v["corrected_lon"])],
                                 moved_m=int(v["distance_frozen_to_corrected_m"])) for k, v in sorted(cor.items())},
        s2_sites=[r["site_id"] for r in frozen_rows],
        frozen_S2_reproduces_results_v3_max_abs_diff=rv.rnd(repro),
        kohlit_latent_P_transjordan=dict(frozen=rv.rnd(kf["kohlit_latent"]["P_transjordan"]),
                                         corrected=rv.rnd(kc["kohlit_latent"]["P_transjordan"])),
        kohlit_entries_P_transjordan={e: dict(frozen=rv.rnd(kf["entries"][e]["P_transjordan"]),
                                              corrected=rv.rnd(kc["entries"][e]["P_transjordan"]))
                                      for e in kf["entries"]},
        logml=dict(frozen=rv.rnd(rf["logml"]), corrected=rv.rnd(rc["logml"])),
        max_total_variation_corrected_vs_frozen=dict(entry=worst, tv=rv.rnd(per_entry[worst])),
    )
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="compute again and compare with the committed file")
    a = ap.parse_args()
    text = json.dumps(compute(), indent=1, sort_keys=True) + "\n"
    if a.check:
        if OUT.read_text(encoding="utf-8") != text:
            raise SystemExit("exploratory/s2_corrected_positions_2026-11-11.json does not match a fresh run")
        print("exploratory/s2_corrected_positions_2026-11-11.json matches a fresh run")
        return
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
