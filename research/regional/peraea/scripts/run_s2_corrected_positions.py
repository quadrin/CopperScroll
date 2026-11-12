#!/usr/bin/env python3
"""S2_broad before and after the position amendment of 11 November 2026 (see PLAN_v3.md, Amendment).

    python3 -I -B research/regional/peraea/scripts/run_s2_corrected_positions.py [--check]

Runs the sensitivity variant S2_broad two times: with the gazetteer as frozen on 9 October 2026
(gazetteer_frozen_2026-10-09.csv) and with the amended gazetteer.csv. The amended run must reproduce
outputs_v3/results_v3.json. Also checks that the two files differ only in the rows of the three corrected
sites. Output: research/regional/peraea/exploratory/s2_corrected_positions_2026-11-11.json. No identification claim.
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
OLD = PERAEA / "gazetteer_frozen_2026-10-09.csv"
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


def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def broad(rows):
    return [r for r in rows if r["peraea_proper"] == "yes" and r["lat"] and r["status"] in ("documented", "partial")]


def compute():
    rv = load_run_v3()
    plan = rv.load_plan()
    rv.check_frozen(plan)
    cor = corrections()
    old, new = read(OLD), read(rv.GAZ)
    changed = sorted(o["site_id"] for o, n in zip(old, new) if o != n)
    if len(old) != len(new) or changed != sorted(cor):
        raise SystemExit(f"the two gazetteer files differ in other rows than the corrected sites: {changed}")
    for n in new:
        if n["site_id"] in cor:
            c = cor[n["site_id"]]
            if (float(n["lat"]), float(n["lon"])) != (float(c["corrected_lat"]), float(c["corrected_lon"])):
                raise SystemExit(f"gazetteer.csv does not have the corrected point of {n['site_id']}")
    d2 = rv.load_data(rv.IN_V2, "v2")
    v2 = rv.run(d2)
    rf = rv.run(rv.set_components(d2, rv.comps_of(broad(old))))
    rc = rv.run(rv.set_components(d2, rv.comps_of(broad(new))))
    kf, kc = rv.kohlit_report(rf, v2), rv.kohlit_report(rc, v2)
    ref = json.loads((rv.OUT_V3 / "results_v3.json").read_text(encoding="utf-8"))["kohlit"]["S2_broad"]
    repro = max(abs(kc["entries"][e]["P_transjordan"] - ref["entries"][e]["P_transjordan"]) for e in kc["entries"])
    repro = max(repro, abs(kc["kohlit_latent"]["P_transjordan"] - ref["kohlit_latent"]["P_transjordan"]))
    per_entry = {e: rv.tv(rc["post"][e], rf["post"][e]) for e in rf["order"]}
    worst = max(per_entry, key=per_entry.get)
    return dict(
        label="S2_broad with the gazetteer of 9 October 2026 (frozen) and with the amended gazetteer (corrected)",
        corrected_sites={k: dict(frozen=[float(v["frozen_lat"]), float(v["frozen_lon"])],
                                 corrected=[float(v["corrected_lat"]), float(v["corrected_lon"])],
                                 moved_m=int(v["distance_frozen_to_corrected_m"])) for k, v in sorted(cor.items())},
        s2_sites=[r["site_id"] for r in broad(new)],
        amended_S2_reproduces_results_v3_max_abs_diff=rv.rnd(repro),
        kohlit_latent_P_transjordan=dict(frozen=rv.rnd(kf["kohlit_latent"]["P_transjordan"]),
                                         corrected=rv.rnd(kc["kohlit_latent"]["P_transjordan"])),
        kohlit_entries_P_transjordan={e: dict(frozen=rv.rnd(kf["entries"][e]["P_transjordan"]),
                                              corrected=rv.rnd(kc["entries"][e]["P_transjordan"]))
                                      for e in kf["entries"]},
        logml=dict(frozen=rv.rnd(rf["logml"]), corrected=rv.rnd(rc["logml"])),
        max_total_variation_corrected_vs_frozen=dict(entry=worst, tv=rv.rnd(per_entry[worst])),
    )


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
