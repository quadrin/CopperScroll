#!/usr/bin/env python3
"""Run the W2B joint placement model (K2 default) on the v3 inputs (documented Peraea places for the
Goranson `transjordan` proposal), as frozen in research/regional/peraea/PLAN_v3.md.

    python3 -I -B research/regional/peraea/scripts/run_v3.py [--tables] [--no-write]

Steps: R0 reproduction of v2 (stops on failure); R1 primary V3-P; R2 sensitivity S1-S6.
W2B joint_model_v1.py and inputs_v3/build_inputs_v3.py are imported by path and never changed.
Writes W2B_model_v1/outputs_v3/ (tables and results_v3.json). Needs numpy (and pyproj through the gazetteer
builder only for tests). Exploratory; no identification claim.
"""
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PERAEA = HERE.parent
REPO = PERAEA.parents[2]
W2B = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1"
IN_V2 = W2B / "inputs_v2"
IN_V3 = W2B / "inputs_v3"
OUT_V3 = W2B / "outputs_v3"
OUT_V2 = W2B / "outputs_v2"
PLAN_V3 = PERAEA / "PLAN_v3.md"
GAZ = PERAEA / "gazetteer.csv"

KOHLIT = ("4", "11", "15", "19", "60")
TJ = "transjordan"
STORE_MIN = 1e-3
TV_THRESHOLD = 0.01
# the 15 bounded runs of W2B scripts/check_order_kernel.py (same constants as research/models/search_effectiveness/run_v2.py)
KERNEL_GRID = (("sinkhorn", 0), ("fixed", 0), ("fixed", 5))
KERNEL_SETTINGS = ((0., 0., 0., ()), (0., 0., .995, ()), (.9, 0., .995, ()), (.9, .4, .995, ()),
                   (0., 0., .8, ("documented", "likely")))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    keep = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


JM = load_module("w2b_joint_model_v1", W2B / "scripts/joint_model_v1.py")
BV3 = load_module("w2b_build_inputs_v3", IN_V3 / "build_inputs_v3.py")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_plan():
    text = PLAN_V3.read_text(encoding="utf-8")
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    return json.loads(m.group(1))


def check_frozen(plan):
    bad = [rel for rel, h in plan["frozen_inputs_sha256"].items() if sha256(REPO / rel) != h]
    if bad:
        raise SystemExit(f"frozen v3 inputs changed: {bad}")


def rnd(x, n=8):
    if isinstance(x, float):
        return round(x, n)
    if isinstance(x, dict):
        return {k: rnd(v, n) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rnd(v, n) for v in x]
    return x


# --------------------------------------------------------------------------------------------- model runs
def load_data(inputs_dir, suffix):
    return JM.Data(str(inputs_dir), suffix)


def run(data, **cfg):
    m = JM.Model(data, JM.cfg_with(**cfg))
    r = m.run()
    post = {e: {s: float(r["post"][i][k]) for k, s in enumerate(m.states)} for i, e in enumerate(r["order"])}
    regions = {e: {g: float(v) for g, v in m.region_probs(r["post"][i]).items()} for i, e in enumerate(r["order"])}
    z = {g: {s: float(v) for s, v in zp.items()} for g, zp in r["zpost"].items()}
    return dict(post=post, regions=regions, zpost=z, logml=float(r["logml"]), order=list(r["order"]),
                title=dict(data.title), n_states=len(m.states))


def tv(p, q):
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in set(p) | set(q))


def top(p, n=8):
    return [[s, v] for s, v in sorted(p.items(), key=lambda x: (-x[1], x[0]))[:n]]


def tj_mass(run_, e, extra=()):
    """P(entry at transjordan or at any of the added per-site places), P(region TRANSJ), P(U_TRANSJ)."""
    p = run_["post"][e]
    return dict(P_transjordan=p.get(TJ, 0.0) + sum(p.get(s, 0.0) for s in extra),
                P_region_TRANSJ=run_["regions"][e].get("TRANSJ", 0.0), P_U_TRANSJ=p.get("U_TRANSJ", 0.0))


# --------------------------------------------------------------------------------------------- variants
def gaz_rows():
    with open(GAZ, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def comps_of(rows, sigma_floor=0.0):
    return [(float(r["lat"]), float(r["lon"]), max(float(r["sigma_km"]), sigma_floor)) for r in rows]


def set_components(data, comps):
    d = copy.deepcopy(data)
    d.place[TJ]["components"] = "|".join(f"{a:.5f}:{b:.5f}:{s:g}" for a, b, s in comps)
    return d


def km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def cluster_components(rows, link_km):
    """Single-linkage clusters within link_km; one component per cluster (mean position;
    sigma = max(member sigma, largest member distance from the mean)). Clusters ordered by first member."""
    pts = comps_of(rows)
    n = len(pts)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            if km(pts[i][0], pts[i][1], pts[j][0], pts[j][1]) <= link_km:
                parent[find(j)] = find(i)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    out, members = [], []
    for root in sorted(groups, key=lambda r: min(groups[r])):
        idx = groups[root]
        la = sum(pts[i][0] for i in idx) / len(idx)
        lo = sum(pts[i][1] for i in idx) / len(idx)
        sg = max(max(pts[i][2] for i in idx), max(km(la, lo, pts[i][0], pts[i][1]) for i in idx))
        out.append((round(la, 5), round(lo, 5), round(sg, 3)))
        members.append([rows[i]["site_id"] for i in idx])
    return out, members


def split_variant(data_v2, rows, total_odds):
    """S4: one place per documented site (region TRANSJ); transjordan candidate rows replaced by per-site rows
    with prior_override = total_odds / n; the transjordan place is kept with no candidate rows."""
    d = copy.deepcopy(data_v2)
    tj_rows = [r for r in d.cands if r["place_id"] == TJ]
    d.cands = [r for r in d.cands if r["place_id"] != TJ]
    n = len(rows)
    new_ids = []
    template = d.place[TJ]
    for g in rows:
        pid = "peraea_" + g["site_id"]
        new_ids.append(pid)
        p = {k: "" for k in template}
        p.update(place_id=pid, name=g["name"], lat=g["lat"], lon=g["lon"], sigma_km=g["sigma_km"], mixture_of="",
                 model_region="TRANSJ", coords_in_places_json="no", precision_string="gazetteer sigma",
                 coord_note="v3 S4 split variant", components="", kind="peraea_v3")
        d.places.append(p)
        d.place[pid] = p
        for r in tj_rows:
            c = dict(r)
            c.update(place_id=pid, prior_override=repr(total_odds / n))
            d.cands.append(c)
    return d, new_ids


# --------------------------------------------------------------------------------------------- report helpers
def kohlit_report(run_, ref_v2, ref_v3=None, extra=()):
    out = {}
    for e in KOHLIT:
        rec = tj_mass(run_, e, extra)
        rec["tv_vs_v2"] = tv(run_["post"][e], ref_v2["post"][e])
        if ref_v3 is not None:
            rec["tv_vs_V3P"] = tv(run_["post"][e], ref_v3["post"][e])
        rec["top"] = top(run_["post"][e])
        out[e] = rec
    z = run_["zpost"].get("Kohlit", {})
    latent = dict(P_transjordan=z.get(TJ, 0.0) + sum(z.get(s, 0.0) for s in extra), P_U_TRANSJ=z.get("U_TRANSJ", 0.0),
                  top=top(z, 10))
    return dict(entries=out, kohlit_latent=latent, logml=run_["logml"], n_states=run_["n_states"])


def kernel_rows(data, label):
    rows = []
    for transition, grid in KERNEL_GRID:
        for rho, wa, wl, excl in KERNEL_SETTINGS:
            cfg = dict(transition=transition, grid_km=grid, grid_mass=10., rho=rho, w_A=wa, w_L=wl,
                       exclude_order_derived=excl)
            m = JM.Model(data, JM.cfg_with(**cfg))
            r = m.run()
            p = r["post"][r["order"].index("60")]
            rp = m.region_probs(p)
            rows.append(dict(inputs=label, transition=transition, grid_km=grid, rho=rho, w_A=wa, w_L=wl,
                             excluded="|".join(excl), logml=float(r["logml"]),
                             P60_transjordan=float(p[m.idx[TJ]]), P60_region_TRANSJ=float(rp["TRANSJ"]),
                             P60_tell_es_sultan=float(p[m.idx["tell_es_sultan"]]),
                             P60_kh_qumran=float(p[m.idx["kh_qumran"]])))
    return rows


# --------------------------------------------------------------------------------------------- R0
def reproduce_v2(v2_run):
    off = BV3.build(off=True)
    off_equal = {n: off[n] == (IN_V2 / n.replace("_v3.csv", "_v2.csv")).read_bytes() for n in sorted(off)}
    with open(OUT_V2 / "posteriors_v1_v2.csv", encoding="utf-8") as f:
        ref = list(csv.DictReader(f))
    max_diff, worst = 0.0, None
    for r in ref:
        got = v2_run["post"][r["entry"]].get(r["state"], 0.0)
        d = abs(got - float(r["P_v2"]))
        if d > max_diff:
            max_diff, worst = d, (r["entry"], r["state"])
    p60q = v2_run["post"]["60"]["kh_qumran"]
    p25 = v2_run["post"]["25"]["iv17_abu_saraj"]
    return dict(switch_off_byte_equal_to_inputs_v2=off_equal, posteriors_rows_compared=len(ref),
                posteriors_max_abs_diff=max_diff, posteriors_worst=worst,
                P60_kh_qumran=p60q, P25_iv17_abu_saraj=p25,
                P60_kh_qumran_4dp_ok=round(p60q, 4) == 0.0325, P25_iv17_4dp_ok=round(p25, 4) == 0.1802,
                numpy_version=np.__version__)


def r0_ok(chk, tol):
    return (all(chk["switch_off_byte_equal_to_inputs_v2"].values()) and chk["posteriors_max_abs_diff"] <= tol
            and chk["P60_kh_qumran_4dp_ok"] and chk["P25_iv17_4dp_ok"])


# --------------------------------------------------------------------------------------------- main analysis
def analyse(plan, with_kernel=True):
    check_frozen(plan)
    sens = plan["sensitivity"]
    d2 = load_data(IN_V2, "v2")
    d3 = load_data(IN_V3, "v3")
    v2 = run(d2)
    chk = reproduce_v2(v2)
    if not r0_ok(chk, plan["r0_tolerance_abs"]):
        return dict(r0=chk, stopped=True)
    v3 = run(d3)
    gz = gaz_rows()
    prim = [r for r in gz if r["w2b_place_id"] == TJ]
    broad = [r for r in gz if r["peraea_proper"] == "yes" and r["lat"] and r["status"] in ("documented", "partial")]
    s1_comps, s1_members = cluster_components(prim, sens["cluster_km"])
    variants = {
        "S1_cluster": (set_components(d2, s1_comps), ()),
        "S2_broad": (set_components(d2, comps_of(broad)), ()),
        "S3_sigma5": (set_components(d2, comps_of(prim, sens["sigma_floor_km"])), ()),
    }
    s4_data, s4_ids = split_variant(d2, prim, sens["split_total_odds"])
    variants["S4_split"] = (s4_data, tuple(s4_ids))
    runs = {k: run(v[0]) for k, v in variants.items()}

    order = v2["order"]
    tv_table = {e: {"V3P": tv(v3["post"][e], v2["post"][e]),
                    **{k: tv(runs[k]["post"][e], v2["post"][e]) for k in runs}} for e in order}
    over = sorted([e for e in order if tv_table[e]["V3P"] > TV_THRESHOLD], key=lambda e: -tv_table[e]["V3P"])
    changed = {}
    for e in over:
        diffs = sorted(set(v3["post"][e]) | set(v2["post"][e]),
                       key=lambda s: (-abs(v3["post"][e].get(s, 0.0) - v2["post"][e].get(s, 0.0)), s))[:5]
        changed[e] = dict(title=v2["title"][e], tv=tv_table[e]["V3P"],
                          top_change=[[s, v3["post"][e].get(s, 0.0) - v2["post"][e].get(s, 0.0)] for s in diffs])

    res = dict(
        meta=dict(plan_v3_sha256=sha256(PLAN_V3), run_v3_sha256=sha256(Path(__file__)),
                  model_code_sha256=sha256(W2B / "scripts/joint_model_v1.py"),
                  model_cfg="joint_model_v1.cfg_with() defaults: transition fixed (K2), rho 0.9, w_A 0.4, w_L 0.995, XII 10 milik_puech",
                  v3_components=d3.place[TJ]["components"], v2_components=d2.place[TJ]["components"],
                  s1_clusters=s1_members, s1_components=s1_comps, s2_sites=[r["site_id"] for r in broad],
                  s4_places=list(s4_ids)),
        r0=chk,
        kohlit=dict(v2=kohlit_report(v2, v2), V3P=kohlit_report(v3, v2),
                    **{k: kohlit_report(runs[k], v2, v3, variants[k][1]) for k in runs}),
        entry_60_regions=dict(v2=v2["regions"]["60"], V3P=v3["regions"]["60"],
                              **{k: runs[k]["regions"]["60"] for k in runs}),
        tv_vs_v2=tv_table, entries_over_threshold=over, changed_entries=changed,
        mean_tv_all_entries={k: sum(tv_table[e][k] for e in order) / len(order) for k in tv_table[order[0]]},
        logml=dict(v2=v2["logml"], V3P=v3["logml"], **{k: runs[k]["logml"] for k in runs}),
    )
    # S6: Janoah reading
    j2 = run(d2, readings=dict(kohlit15=True, solomon23=True, xii10="janoah"))
    j3 = run(d3, readings=dict(kohlit15=True, solomon23=True, xii10="janoah"))
    res["S6_janoah"] = {e: dict(v2=tj_mass(j2, e), V3P=tj_mass(j3, e), tv=tv(j3["post"][e], j2["post"][e]))
                        for e in ("4", "11", "15", "19", "60")}
    res["S6_janoah_latent"] = dict(v2=j2["zpost"].get("Kohlit", {}).get(TJ, 0.0), V3P=j3["zpost"].get("Kohlit", {}).get(TJ, 0.0))
    # stored posteriors
    stored = {}
    for e in order:
        keep = sorted(s for s in set(v2["post"][e]) | set(v3["post"][e])
                      if max(v2["post"][e].get(s, 0.0), v3["post"][e].get(s, 0.0)) >= STORE_MIN)
        stored[e] = {s: [v2["post"][e].get(s, 0.0), v3["post"][e].get(s, 0.0)] for s in keep}
    res["posterior_v2_v3_stored"] = stored
    res["titles"] = v2["title"]
    res["order"] = order
    if with_kernel:
        res["kernel_grid"] = kernel_rows(d2, "v2") + kernel_rows(d3, "v3")
    return rnd(res)


def write_csv(path, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_outputs(res):
    OUT_V3.mkdir(parents=True, exist_ok=True)
    (OUT_V3 / "repro_v2").mkdir(exist_ok=True)
    (OUT_V3 / "repro_v2" / "check.json").write_text(json.dumps(res["r0"], indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if res.get("stopped"):
        return
    (OUT_V3 / "results_v3.json").write_text(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT_V3 / "posteriors_v2_v3.csv",
              [dict(entry=e, state=s, P_v2=v[0], P_v3=v[1]) for e in res["order"] for s, v in res["posterior_v2_v3_stored"][e].items()])
    write_csv(OUT_V3 / "entry_tv_v3.csv",
              [dict(entry=e, title=res["titles"][e], **{f"tv_{k}_vs_v2": v for k, v in res["tv_vs_v2"][e].items()}) for e in res["order"]])
    rows = []
    for var, rep in res["kohlit"].items():
        for e, rec in rep["entries"].items():
            rows.append(dict(variant=var, entry=e, P_transjordan=rec["P_transjordan"], P_region_TRANSJ=rec["P_region_TRANSJ"],
                             P_U_TRANSJ=rec["P_U_TRANSJ"], tv_vs_v2=rec["tv_vs_v2"], tv_vs_V3P=rec.get("tv_vs_V3P", ""),
                             top3="; ".join(f"{s} {p:.4f}" for s, p in rec["top"][:3])))
        lat = rep["kohlit_latent"]
        rows.append(dict(variant=var, entry="latent", P_transjordan=lat["P_transjordan"], P_region_TRANSJ="",
                         P_U_TRANSJ=lat["P_U_TRANSJ"], tv_vs_v2="", tv_vs_V3P="",
                         top3="; ".join(f"{s} {p:.4f}" for s, p in lat["top"][:3])))
    write_csv(OUT_V3 / "kohlit_v3.csv", rows)
    if "kernel_grid" in res:
        write_csv(OUT_V3 / "kernel_grid_v3.csv", res["kernel_grid"])


def tables(res):
    L = []
    if res.get("stopped"):
        return "R0 failed: " + json.dumps(res["r0"])
    L.append("| Variant | Entry | P(transjordan) | P(TRANSJ) | P(U_TRANSJ) | TV vs v2 | top 3 |")
    L.append("|---|---|---|---|---|---|---|")
    for var, rep in res["kohlit"].items():
        for e, rec in rep["entries"].items():
            L.append(f"| {var} | {e} | {rec['P_transjordan']:.4f} | {rec['P_region_TRANSJ']:.4f} | {rec['P_U_TRANSJ']:.4f} | "
                     f"{rec['tv_vs_v2']:.4f} | " + "; ".join(f"{s} {p:.3f}" for s, p in rec["top"][:3]) + " |")
        lat = rep["kohlit_latent"]
        L.append(f"| {var} | latent | {lat['P_transjordan']:.4f} | | {lat['P_U_TRANSJ']:.4f} | | " +
                 "; ".join(f"{s} {p:.3f}" for s, p in lat["top"][:3]) + " |")
    L.append("\nEntries with TV(v2, V3P) > 0.01: " + ", ".join(f"{e} ({res['tv_vs_v2'][e]['V3P']:.4f})" for e in res["entries_over_threshold"]))
    L.append("Mean TV over all entries: " + ", ".join(f"{k} {v:.4f}" for k, v in res["mean_tv_all_entries"].items()))
    L.append("logml: " + ", ".join(f"{k} {v:.4f}" for k, v in res["logml"].items()))
    L.append("\nS6 Janoah: " + "; ".join(f"{e}: v2 {v['v2']['P_transjordan']:.4f} -> V3P {v['V3P']['P_transjordan']:.4f} (TV {v['tv']:.4f})"
                                        for e, v in res["S6_janoah"].items()))
    if "kernel_grid" in res:
        L.append("\n| inputs | transition | grid | rho | w_A | w_L | excl | P60 transjordan | P60 TRANSJ | P60 tell | P60 qumran |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in res["kernel_grid"]:
            L.append(f"| {r['inputs']} | {r['transition']} | {r['grid_km']} | {r['rho']} | {r['w_A']} | {r['w_L']} | {r['excluded']} | "
                     f"{r['P60_transjordan']:.4f} | {r['P60_region_TRANSJ']:.4f} | {r['P60_tell_es_sultan']:.4f} | {r['P60_kh_qumran']:.4f} |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--no-kernel", action="store_true")
    a = ap.parse_args()
    plan = load_plan()
    res = analyse(plan, with_kernel=not a.no_kernel)
    if not a.no_write:
        write_outputs(res)
    if res.get("stopped"):
        raise SystemExit("R0 failed: the v3 runner does not reproduce v2; stopping (see outputs_v3/repro_v2/check.json)")
    if a.tables:
        print(tables(res))


if __name__ == "__main__":
    main()
