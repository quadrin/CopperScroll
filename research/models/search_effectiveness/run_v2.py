#!/usr/bin/env python3
"""Run the W2B joint placement model (K2 default) with the two v2 candidates, and rerun the
search-effectiveness layer on the v2 inputs.

    python3 -I research/models/search_effectiveness/run_v2.py [--tables] [--skip-repro]

Steps, as frozen in PLAN_v2.md:
  R0  reproduce outputs_fixed/ from the unchanged v1 inputs with this runner (stops on a mismatch);
      reproduce results.json with the layer wrapper
  R1  decomposition A (v1) / B (place only) / C (+ entry 25) / D (+ entry 60) / E (v2)
  R2  label sensitivity of the two new rows; R3 sigma of the new place
  R4  the 15 check_order_kernel.py configurations on v1 and v2
  R5  the search-effectiveness layer (run_analysis.analyse, imported and not edited) on v2

W2B code (joint_model_v1.py) and the layer code (search_model.py, run_analysis.py) are imported and
never changed. Outputs: results_v2.json here; tables under W2B_model_v1/outputs_v2/.
The W2B model needs numpy; this file adds no other dependency.
"""
import argparse
import copy
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import search_model as sm  # noqa: E402
import run_analysis as ra  # noqa: E402

W2B = sm.W2B
REPO = sm.REPO
IN_V1 = W2B / "inputs"
IN_V2 = W2B / "inputs_v2"
OUT_V2 = W2B / "outputs_v2"
OUT_FIXED = W2B / "outputs_fixed"
T06_REF = W2B.parent.parent / "wave1" / "T06_joint_model" / "outputs" / "posterior_M3_joint_fitted.csv"
PLAN_V2 = HERE / "PLAN_v2.md"
LOOKS_V2 = HERE / "looks_v2.csv"
RESULTS_V2 = HERE / "results_v2.json"

KOHLIT = ("4", "11", "15", "19", "60")
PROPOSALS = ("tell_es_sultan", "ein_samiya", "muhalhil", "beit_kahil", "kuhlah", "carmel_siah", "mount_zion",
             "transjordan", "ein_ghuweir", "ein_feshkha")
NEW_PLACE = "iv17_abu_saraj"
ROW25 = ("25", NEW_PLACE)
ROW60 = ("60", "kh_qumran")
NEW_ROWS = (ROW25, ROW60)
STORE_MIN = 1e-3

JM = sm.load_jm()


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rnd(x):
    return ra.rnd(x, 8)


# ============================================================================ plan
def load_plan_v2():
    return sm.load_plan(PLAN_V2)


def check_frozen_v2(plan):
    got = {}
    for rel in plan["frozen_inputs_sha256"]:
        p = (W2B / rel) if rel.startswith("inputs_v2/") else (HERE / rel)
        got[rel] = sha256(p)
    if got != plan["frozen_inputs_sha256"]:
        bad = sorted(k for k in got if got[k] != plan["frozen_inputs_sha256"][k])
        raise SystemExit(f"frozen v2 inputs changed: {bad}")
    return got


# ============================================================================ R0: the v2 runner on W2B inputs
KERNEL_GRID = [(t, g) for t, g in (("sinkhorn", 0), ("fixed", 0), ("fixed", 5))]
KERNEL_SETTINGS = ((0., 0., 0., ()), (0., 0., .995, ()), (.9, 0., .995, ()), (.9, .4, .995, ()),
                   (0., 0., .8, ("documented", "likely")))


def load_data(inputs_dir, suffix):
    return JM.Data(str(inputs_dir), suffix)


def kernel_rows(inputs_dir, suffix, extra=False):
    """The 15 bounded runs of scripts/check_order_kernel.py for one input set (same order, same columns).
    With extra=True, three columns are added for the v2 candidates."""
    d = load_data(inputs_dir, suffix)
    rows = []
    for transition, grid in KERNEL_GRID:
        for rho, wa, wl, excl in KERNEL_SETTINGS:
            cfg = JM.cfg_with(transition=transition, grid_km=grid, grid_mass=10.,
                              rho=rho, w_A=wa, w_L=wl, exclude_order_derived=excl)
            m = JM.Model(d, cfg)
            r = m.run()
            p = r["post"][r["order"].index("60")]
            T = m.transition(wl)
            rp = m.region_probs(p)
            row = dict(inputs=suffix, transition=transition, grid_km=grid,
                       rho=rho, w_A=wa, w_L=wl, excluded="|".join(excl),
                       logml=float(r["logml"]),
                       P_tell_es_sultan=float(p[m.idx["tell_es_sultan"]]),
                       P_north_32_05=float(sum(p[i] for i, s in enumerate(m.states)
                                               if float(m.W[i] @ m.A[:, 0]) > 32.05)),
                       R_north=rp["NORTH"], R_background=rp.get("BG", 0.),
                       max_row_sum_error=float(np.max(np.abs(T.sum(1) - 1))),
                       stationarity_drift=float(np.max(np.abs(m.pi @ T - m.pi))))
            if extra:
                p25 = r["post"][r["order"].index("25")]
                row.update(P60_kh_qumran=float(p[m.idx["kh_qumran"]]),
                           P25_iv17_abu_saraj=float(p25[m.idx[NEW_PLACE]]) if NEW_PLACE in m.idx else 0.0,
                           P25_kh_qumran=float(p25[m.idx["kh_qumran"]]))
            rows.append(row)
    return rows


def v0_check_text(inputs_dir):
    """scripts/analysis_v1.py v0check(), as text (json.dump with indent=1, no final newline)."""
    d0 = load_data(inputs_dir, "v0")
    m = JM.Model(d0, JM.cfg_with(w_A=0.4, w_L=0.995, lam=2.0, rho=0.9, kohlit_scheme=None, transition="sinkhorn"))
    r = m.run()
    with open(T06_REF, encoding="utf-8") as f:
        ref = {row["entry"]: row for row in csv.DictReader(f)}
    pos = {e: i for i, e in enumerate(r["order"])}
    mx = max(abs(v - float(ref[e]["R_" + k])) for e in r["order"] for k, v in m.region_probs(r["post"][pos[e]]).items())
    out = dict(logml=round(r["logml"], 4), T06_M3_logml=8.6831, max_abs_region_diff=mx)
    return json.dumps(out, indent=1)


def layer_analyse(inputs_dir, suffix, looks_path):
    """run_analysis.analyse() on another input set and looks table, without editing the layer.

    analyse() reads <sm.INPUTS>/*_v1.csv and sm.load_looks(). We point sm.INPUTS at a temporary folder
    holding byte copies of the chosen input files under the names analyse() expects, and bind
    sm.load_looks to the chosen looks table. The PLAN.md scenarios and reading sets are used unchanged;
    only the looks hash that analyse() checks is set to the table actually used."""
    plan = copy.deepcopy(sm.load_plan())
    looks_path = Path(looks_path)
    saved = (sm.INPUTS, sm.LOOKS, sm.load_looks)
    orig_load = sm.load_looks
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for stem in ("entries", "places", "candidates", "name_groups", "kohlit_proposals"):
            shutil.copyfile(Path(inputs_dir) / f"{stem}_{suffix}.csv", tmp / f"{stem}_v1.csv")
        try:
            sm.INPUTS = tmp
            sm.LOOKS = looks_path
            sm.load_looks = lambda path=None: orig_load(path or looks_path)
            plan["frozen_inputs_sha256"]["looks.csv"] = sha256(looks_path)
            res = ra.analyse(plan)
        finally:
            sm.INPUTS, sm.LOOKS, sm.load_looks = saved
    return res


def compare_kernel_csv(a_path, b_path):
    """Row-by-row comparison of two kernel_sensitivity.csv files: byte-equal rows and largest differences."""
    with open(a_path, encoding="utf-8") as f:
        a = list(csv.DictReader(f))
    with open(b_path, encoding="utf-8") as f:
        b = list(csv.DictReader(f))
    same_rows, max_abs, max_rel = 0, 0.0, 0.0
    if len(a) != len(b) or (a and list(a[0]) != list(b[0])):
        return dict(rows=len(a), rows_byte_equal=0, structure_equal=False, max_abs_diff=None, max_rel_diff=None)
    for r, s in zip(a, b):
        same_rows += r == s
        for k in r:
            if r[k] == s[k]:
                continue
            try:
                x, y = float(r[k]), float(s[k])
            except ValueError:
                return dict(rows=len(a), rows_byte_equal=same_rows, structure_equal=False, max_abs_diff=None,
                            max_rel_diff=None)
            max_abs = max(max_abs, abs(x - y))
            if abs(x) > 1e-10:
                max_rel = max(max_rel, abs(x - y) / abs(x))
    return dict(rows=len(a), rows_byte_equal=same_rows, structure_equal=True, max_abs_diff=max_abs, max_rel_diff=max_rel)


def reproduce(out_dir, tol=1e-12):
    """R0. Write the reproduced outputs_fixed files to out_dir and compare them with outputs_fixed/ and with
    a fresh run of W2B's own scripts/check_order_kernel.py on this machine (written to a temporary folder)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = kernel_rows(IN_V1, "v0") + kernel_rows(IN_V1, "v1")
    JM.write_csv(out_dir / "kernel_sensitivity.csv", rows)
    (out_dir / "v0_reproduction_check.json").write_text(v0_check_text(IN_V1))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, "-I", "-B", str(W2B / "scripts" / "check_order_kernel.py"), "--out", tmp],
                       check=True, capture_output=True)
        rerun_equal = (Path(tmp) / "kernel_sensitivity.csv").read_bytes() == (out_dir / "kernel_sensitivity.csv").read_bytes()
    recorded = json.loads((OUT_FIXED / "kernel_validation.json").read_text())["input_and_code_sha256"]
    current = {rel: sha256(W2B / rel) for rel in recorded}
    layer_equal = (json.dumps(layer_analyse(IN_V1, "v1", sm.LOOKS), sort_keys=True, ensure_ascii=False) ==
                   json.dumps(json.loads((HERE / "results.json").read_text(encoding="utf-8")), sort_keys=True,
                              ensure_ascii=False))
    cmp_fixed = compare_kernel_csv(OUT_FIXED / "kernel_sensitivity.csv", out_dir / "kernel_sensitivity.csv")
    check = dict(
        runner="research/models/search_effectiveness/run_v2.py kernel_rows() and v0_check_text() on W2B inputs/ (v0, v1)",
        kernel_sensitivity_csv_byte_equal=(out_dir / "kernel_sensitivity.csv").read_bytes() ==
        (OUT_FIXED / "kernel_sensitivity.csv").read_bytes(),
        kernel_sensitivity_vs_outputs_fixed=cmp_fixed,
        kernel_sensitivity_within_tolerance=bool(cmp_fixed["structure_equal"] and cmp_fixed["max_abs_diff"] <= tol),
        tolerance_abs=tol,
        kernel_sensitivity_byte_equal_to_w2b_script_rerun_here=rerun_equal,
        v0_reproduction_check_json_byte_equal=(out_dir / "v0_reproduction_check.json").read_bytes() ==
        (OUT_FIXED / "v0_reproduction_check.json").read_bytes(),
        kernel_sensitivity_sha256=sha256(out_dir / "kernel_sensitivity.csv"),
        layer_wrapper_on_v1_equals_results_json=layer_equal,
        kernel_validation_recorded_vs_current_sha256={
            rel: dict(recorded=recorded[rel], current=current[rel], equal=recorded[rel] == current[rel])
            for rel in sorted(recorded)},
        numpy_version=np.__version__,
        note=("kernel_validation.json stores SHA-256 values of the files used for outputs_fixed; the comparison "
              "says which committed files still carry those exact bytes. The numbers are compared directly above."),
    )
    (out_dir / "check.json").write_text(json.dumps(check, indent=1, sort_keys=True) + "\n")
    return check


def r0_passed(chk):
    """Stop rule used by main(). PLAN_v2 R0 asked for byte equality with outputs_fixed; see README_v2 for why
    round-off differences are accepted when W2B's own script gives the same bytes on this machine."""
    return bool(chk["kernel_sensitivity_within_tolerance"] and chk["kernel_sensitivity_byte_equal_to_w2b_script_rerun_here"]
                and chk["v0_reproduction_check_json_byte_equal"] and chk["layer_wrapper_on_v1_equals_results_json"])


# ============================================================================ R1-R3: K2-default runs
def variant(data, drop=(), relabel=None, sigma=None):
    d = copy.deepcopy(data)
    d.cands = [r for r in d.cands if (r["entry"], r["place_id"]) not in set(drop)]
    for key, (status, conf) in (relabel or {}).items():
        hit = [r for r in d.cands if (r["entry"], r["place_id"]) == key]
        if len(hit) != 1:
            raise ValueError(f"relabel target {key} not found once")
        hit[0]["status"], hit[0]["confidence"] = status, conf
    if sigma is not None:
        d.place[NEW_PLACE]["sigma_km"] = str(sigma)
    return d


def run_default(data):
    m = JM.Model(data, JM.cfg_with())
    r = m.run()
    post = {e: {s: float(r["post"][i][k]) for k, s in enumerate(m.states)} for i, e in enumerate(r["order"])}
    regions = {e: {g: float(v) for g, v in m.region_probs(r["post"][i]).items()} for i, e in enumerate(r["order"])}
    z = {g: {s: float(v) for s, v in zp.items()} for g, zp in r["zpost"].items()}
    return dict(post=post, regions=regions, zpost=z, logml=float(r["logml"]), states=list(m.states),
                order=list(r["order"]), title=dict(data.title))


def tv(p, q):
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def top(p, n=8):
    return [[s, v] for s, v in sorted(p.items(), key=lambda x: (-x[1], x[0]))[:n]]


def entry_summary(run, e, places):
    p = run["post"][e]
    return dict(P={s: p.get(s, 0.0) for s in places}, top=top(p), regions=run["regions"][e])


def sens_summary(run, base_E, base_A, e_new, place):
    entries = sorted(set(KOHLIT) | {"25"}, key=lambda x: run["order"].index(x))
    others = [(tv(run["post"][e], base_E["post"][e]), e) for e in run["order"] if e not in entries]
    o = max(others, key=lambda x: (x[0], x[1]))
    return dict(P_new=run["post"][e_new].get(place, 0.0),
                tv_vs_E={e: tv(run["post"][e], base_E["post"][e]) for e in entries},
                tv_vs_A={e: tv(run["post"][e], base_A["post"][e]) for e in entries},
                most_moved_other_vs_E=dict(entry=o[1], tv=o[0]))


def model_runs(plan):
    A_data = load_data(IN_V1, "v1")
    E_data = load_data(IN_V2, "v2")
    sets = dict(A=A_data, B=variant(E_data, drop=NEW_ROWS), C=variant(E_data, drop=(ROW60,)),
                D=variant(E_data, drop=(ROW25,)), E=E_data)
    runs = {k: run_default(v) for k, v in sets.items()}
    A, E = runs["A"], runs["E"]
    order = A["order"]
    thr = plan["tv_report_threshold"]

    tv_table = {e: {k: tv(runs[k]["post"][e], A["post"][e]) for k in "BCDE"} for e in order}
    watch = ["kh_qumran", NEW_PLACE, "U_JERICHO", "U_QUMRAN"]
    focus = {}
    for e in ("25", "60"):
        focus[e] = {k: entry_summary(runs[k], e, watch + (list(PROPOSALS) if e == "60" else [])) for k in "ABCDE"}
    kohlit = {}
    for e in KOHLIT:
        kohlit[e] = {k: dict(P={s: runs[k]["post"][e].get(s, 0.0) for s in PROPOSALS + ("kh_qumran", "U_QUMRAN", "U_JER", "U_JERICHO")},
                             regions=runs[k]["regions"][e], tv_vs_A=(0.0 if k == "A" else tv_table[e][k]))
                     for k in "ABCDE"}
    zlat = {k: top(runs[k]["zpost"].get("Kohlit", {}), 12) for k in "ABCDE"}
    over = sorted([e for e in order if tv_table[e]["E"] > thr], key=lambda e: -tv_table[e]["E"])
    changed = {e: dict(title=A["title"][e], tv=tv_table[e],
                       top_change_E_minus_A=[[s, E["post"][e].get(s, 0.0) - A["post"][e].get(s, 0.0)]
                                             for s in sorted(set(E["post"][e]) | set(A["post"][e]),
                                                             key=lambda s: (-abs(E["post"][e].get(s, 0.0) - A["post"][e].get(s, 0.0)), s))[:5]])
               for e in over}

    # R2 labels
    labels = {}
    for key_s, steps in plan["label_steps"].items():
        e, place = key_s.split("|")
        key = (e, place)
        res = {}
        for step, (status, conf) in steps.items():
            run = E if step == "main" else run_default(variant(E_data, relabel={key: (status, conf)}))
            item = sens_summary(run, E, A, e, place)
            item.update(label=[status, conf])
            res[step] = item
        labels[key_s] = res
    # R3 sigma
    sig = {}
    for s in plan["sigma_km"]["sensitivity"]:
        run = run_default(variant(E_data, sigma=s))
        sig[str(s)] = sens_summary(run, E, A, "25", NEW_PLACE)
    sig[str(plan["sigma_km"]["main"])] = sens_summary(E, E, A, "25", NEW_PLACE)

    # stored posteriors (A and E), states at or above STORE_MIN in either
    stored = {}
    for e in order:
        keep = sorted(s for s in set(E["post"][e]) | set(A["post"][e])
                      if max(E["post"][e].get(s, 0.0), A["post"][e].get(s, 0.0)) >= STORE_MIN)
        stored[e] = {s: [A["post"][e].get(s, 0.0), E["post"][e].get(s, 0.0)] for s in keep}

    return dict(
        logml={k: runs[k]["logml"] for k in "ABCDE"},
        n_states={k: len(runs[k]["states"]) for k in "ABCDE"},
        tv_vs_A=tv_table, entries_over_threshold=over, changed_entries=changed,
        focus=focus, kohlit=kohlit, kohlit_latent_top=zlat,
        label_sensitivity=labels, sigma_sensitivity=sig,
        posterior_A_E_stored=stored, title=A["title"], order=order)


# ============================================================================ R5: layer summaries
def layer_summary(res, ref=None):
    dc = {d["look_id"]: d for d in res["double_counting"]}
    rep = [d for d in res["double_counting"] if d["factor_added"] is not None]
    out = dict(
        double_counting={k: dc[k] for k in ("L42", "L43", "L44")},
        reported_rows_adding_a_factor=[d["look_id"] for d in rep if d["factor_added"] != 1.0],
        reported_rows=len(rep),
        reported_status_counts={},
        factors_below_1=[f for f in res["factors"] if f["factor"] < 1],
        tv_vs_S4={rname: {e: res["entries"][e]["by_reading"][rname]["tv_vs_S4"]
                          for e in list(KOHLIT) + ["25"] if e in res["entries"]}
                  for rname in sorted(res["plan"]["reading_sets"])},
        entries_changed_S0={rname: sorted([e for e, rec in res["entries"].items()
                                           if rec["by_reading"][rname]["tv_vs_S4"]["S0"] >= 1e-4],
                                          key=lambda x: -res["entries"][x]["by_reading"][rname]["tv_vs_S4"]["S0"])
                            for rname in sorted(res["plan"]["reading_sets"])},
        S0_minus_S4_top={e: res["entries"][e]["by_reading"]["R-P"].get("S0_minus_S4_top", [])[:5] for e in KOHLIT},
        probes=[dict(probe_id=p["probe_id"], entry=p["entry"], place=p["place"], P_now=p["P_now"],
                     dP_05=p["by_pd"]["0.5"]["delta_P"], dP_09=p["by_pd"]["0.9"]["delta_P"],
                     top_other_09=p["by_pd"]["0.9"]["top_other_entries"][0]) for p in res["probes"]],
        unsearched_all_entries_mean=res["unsearched_mass"]["all_entries_mean"],
        logml=res["meta"]["logml"],
    )
    for d in rep:
        s = d["status"].split(":")[0]
        out["reported_status_counts"][s] = out["reported_status_counts"].get(s, 0) + 1
    if ref is not None:
        rdc = {d["look_id"]: d for d in ref["double_counting"]}
        out["double_counting_status_changed_vs_v1"] = {k: [rdc[k]["status"], dc[k]["status"]]
                                                       for k in sorted(dc) if rdc[k]["status"] != dc[k]["status"]}
        out["factors_identical_to_v1"] = ([(f["reading_set"], f["scenario"], f["entry"], f["place"], f["factor"])
                                           for f in ref["factors"]] ==
                                          [(f["reading_set"], f["scenario"], f["entry"], f["place"], f["factor"])
                                           for f in res["factors"]])
        out["tv_vs_S4_v1"] = {rname: {e: ref["entries"][e]["by_reading"][rname]["tv_vs_S4"] for e in list(KOHLIT) + ["25"]}
                              for rname in sorted(ref["plan"]["reading_sets"])}
        out["probes_v1"] = [dict(probe_id=p["probe_id"], P_now=p["P_now"], dP_09=p["by_pd"]["0.9"]["delta_P"])
                            for p in ref["probes"]]
    return out


def layer_runs():
    ref = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    a = layer_analyse(IN_V2, "v2", sm.LOOKS)
    b = layer_analyse(IN_V2, "v2", LOOKS_V2)
    return dict(v2_inputs_looks_csv=layer_summary(a, ref), v2_inputs_looks_v2_csv=layer_summary(b, ref))


# ============================================================================ main
def analyse(plan, with_kernel=True, with_layer=True):
    check_frozen_v2(plan)
    out = dict(meta=dict(
        plan_v2_sha256=sha256(PLAN_V2), frozen_inputs_sha256=check_frozen_v2(plan),
        model_code_sha256=sha256(sm.MODEL_PATH), run_v2_sha256=sha256(Path(__file__)),
        layer_code_sha256={"search_model.py": sha256(HERE / "search_model.py"),
                           "run_analysis.py": sha256(HERE / "run_analysis.py")},
        model_cfg="joint_model_v1.cfg_with() defaults: transition 'fixed' (K2), kohlit_scheme None, rho 0.9, "
                  "w_A 0.4, w_L 0.995, XII 10 milik_puech"))
    out["model"] = model_runs(plan)
    if with_kernel:
        out["kernel_grid"] = kernel_rows(IN_V1, "v1", extra=True) + kernel_rows(IN_V2, "v2", extra=True)
    if with_layer:
        out["layer"] = layer_runs()
    return rnd(out)


def write_tables(res):
    OUT_V2.mkdir(parents=True, exist_ok=True)
    m = res["model"]
    rows = [dict(entry=e, title=m["title"][e], **{f"tv_{k}_vs_A": m["tv_vs_A"][e][k] for k in "BCDE"}) for e in m["order"]]
    JM.write_csv(OUT_V2 / "entry_tv_v2.csv", rows)
    rows = [dict(entry=e, state=s, P_v1=v[0], P_v2=v[1]) for e in m["order"] for s, v in m["posterior_A_E_stored"][e].items()]
    JM.write_csv(OUT_V2 / "posteriors_v1_v2.csv", rows)
    if "kernel_grid" in res:
        JM.write_csv(OUT_V2 / "kernel_sensitivity_v2.csv", res["kernel_grid"])


def tables(res):
    m = res["model"]
    L = []
    L.append("### Decomposition (K2 default): P(new state) and TV against v1\n")
    L.append("| Set | P(25 at iv17) | P(25 at kh_qumran) | P(25 at U_JERICHO) | P(60 at kh_qumran) | P(60 at tell_es_sultan) | TV 25 | TV 60 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for k in "ABCDE":
        f25, f60 = m["focus"]["25"][k]["P"], m["focus"]["60"][k]["P"]
        t25 = 0.0 if k == "A" else m["tv_vs_A"]["25"][k]
        t60 = 0.0 if k == "A" else m["tv_vs_A"]["60"][k]
        L.append(f"| {k} | {f25[NEW_PLACE]:.4f} | {f25['kh_qumran']:.4f} | {f25['U_JERICHO']:.4f} | {f60['kh_qumran']:.4f} | "
                 f"{f60['tell_es_sultan']:.4f} | {t25:.4f} | {t60:.4f} |")
    L.append("\n### Koḥlit group: P(kh_qumran), P(QUMRAN region), TV against v1\n")
    L.append("| Entry | P(kh_qumran) v1 | v2 | QUMRAN v1 | v2 | JERICHO v1 | v2 | TV B | TV C | TV D | TV E |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for e in KOHLIT:
        a, b = m["kohlit"][e]["A"], m["kohlit"][e]["E"]
        t = m["tv_vs_A"][e]
        L.append(f"| {e} | {a['P']['kh_qumran']:.4f} | {b['P']['kh_qumran']:.4f} | {a['regions']['QUMRAN']:.4f} | "
                 f"{b['regions']['QUMRAN']:.4f} | {a['regions']['JERICHO']:.4f} | {b['regions']['JERICHO']:.4f} | "
                 f"{t['B']:.4f} | {t['C']:.4f} | {t['D']:.4f} | {t['E']:.4f} |")
    L.append("\n### Entries with TV(v1, v2) > 0.01\n")
    L.append("| Entry | Title | TV B | TV C | TV D | TV E | Largest change (E − A) |")
    L.append("|---|---|---|---|---|---|---|")
    for e in m["entries_over_threshold"]:
        c = m["changed_entries"][e]
        s, d = c["top_change_E_minus_A"][0]
        L.append(f"| {e} | {c['title']} | {c['tv']['B']:.4f} | {c['tv']['C']:.4f} | {c['tv']['D']:.4f} | {c['tv']['E']:.4f} | {s} {d:+.4f} |")
    L.append("\n### Label sensitivity\n")
    L.append("| Row | Step | Label | P(new state) | TV 25 vs E | TV 60 vs E | max TV Koḥlit 4–19 vs E | Most moved other (vs E) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for key, steps in m["label_sensitivity"].items():
        for step, it in steps.items():
            k4 = max(it["tv_vs_E"][e] for e in ("4", "11", "15", "19"))
            o = it["most_moved_other_vs_E"]
            L.append(f"| {key} | {step} | {'/'.join(it['label'])} | {it['P_new']:.4f} | {it['tv_vs_E']['25']:.4f} | "
                     f"{it['tv_vs_E']['60']:.4f} | {k4:.4f} | {o['entry']} ({o['tv']:.4f}) |")
    L.append("\n### Sigma of iv17_abu_saraj\n")
    L.append("| sigma km | P(25 at iv17) | TV 25 vs E |")
    L.append("|---|---|---|")
    for s, it in sorted(m["sigma_sensitivity"].items(), key=lambda x: float(x[0])):
        L.append(f"| {s} | {it['P_new']:.4f} | {it['tv_vs_E']['25']:.4f} |")
    L.append("\n### Koḥlit latent, top states (A and E)\n")
    for k in "AE":
        L.append(f"- {k}: " + ", ".join(f"{s} {v:.3f}" for s, v in m["kohlit_latent_top"][k][:8]))
    if "kernel_grid" in res:
        L.append("\n### Kernel grid (entry 60 and 25)\n")
        L.append("| inputs | transition | grid | rho | w_A | w_L | excl | P60 tell | P60 kh_qumran | P25 iv17 | P25 kh_qumran |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in res["kernel_grid"]:
            L.append(f"| {r['inputs']} | {r['transition']} | {r['grid_km']} | {r['rho']} | {r['w_A']} | {r['w_L']} | {r['excluded']} | "
                     f"{r['P_tell_es_sultan']:.4f} | {r['P60_kh_qumran']:.4f} | {r['P25_iv17_abu_saraj']:.4f} | {r['P25_kh_qumran']:.4f} |")
    if "layer" in res:
        for name, ly in res["layer"].items():
            L.append(f"\n### Layer on {name}\n")
            for k, d in ly["double_counting"].items():
                L.append(f"- {k} ({d['entry']}, {d['place']}): {d['status']}; factor added {d['factor_added']}")
            L.append(f"- reported rows adding a factor: {ly['reported_rows_adding_a_factor'] or 'none'}; "
                     f"factors identical to v1: {ly['factors_identical_to_v1']}")
            L.append(f"- reported-row statuses: {ly['reported_status_counts']}")
            L.append(f"- status changes against v1: {ly['double_counting_status_changed_vs_v1']}")
            L.append("\n| Entry | TV S0 vs S4, v1 | v2 | S1 v1 | S1 v2 |")
            L.append("|---|---|---|---|---|")
            for e in list(KOHLIT) + ["25"]:
                a, b = ly["tv_vs_S4_v1"]["R-P"][e], ly["tv_vs_S4"]["R-P"][e]
                L.append(f"| {e} | {a['S0']:.4f} | {b['S0']:.4f} | {a['S1']:.4f} | {b['S1']:.4f} |")
            L.append("\n| Probe | Entry | Place | P now v1 | v2 | dP at 0.9 v1 | v2 |")
            L.append("|---|---|---|---|---|---|---|")
            p1 = {p["probe_id"]: p for p in ly["probes_v1"]}
            for p in ly["probes"]:
                q = p1[p["probe_id"]]
                L.append(f"| {p['probe_id']} | {p['entry']} | {p['place']} | {q['P_now']:.4f} | {p['P_now']:.4f} | "
                         f"{q['dP_09']:+.4f} | {p['dP_09']:+.4f} |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", action="store_true")
    ap.add_argument("--skip-repro", action="store_true", help="skip R0 (already recorded in outputs_v2/repro_v1)")
    a = ap.parse_args()
    plan = load_plan_v2()
    check_frozen_v2(plan)
    if not a.skip_repro:
        chk = reproduce(OUT_V2 / "repro_v1")
        print("R0:", {k: chk[k] for k in ("kernel_sensitivity_csv_byte_equal", "kernel_sensitivity_vs_outputs_fixed",
                                          "kernel_sensitivity_byte_equal_to_w2b_script_rerun_here",
                                          "v0_reproduction_check_json_byte_equal",
                                          "layer_wrapper_on_v1_equals_results_json")}, file=sys.stderr)
        if not r0_passed(chk):
            raise SystemExit("R0 failed: the v2 runner does not reproduce outputs_fixed/ or results.json; stopping")
    res = analyse(plan)
    RESULTS_V2.write_text(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    write_tables(res)
    if a.tables:
        print(tables(res))
    print(f"wrote {RESULTS_V2}", file=sys.stderr)


if __name__ == "__main__":
    main()
