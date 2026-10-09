#!/usr/bin/env python3
"""Concealment contexts: compare the Copper Scroll's hiding places with recorded
concealments in the southern Levant, 150 BCE - 135 CE, as frozen in PLAN.md.

Standard library only. Deterministic. Run with python3 -I.

  python3 -I concealment.py build   # recompute derived columns in both CSVs (idempotent)
  python3 -I concealment.py run     # write results.json and RESULTS.md
  python3 -I concealment.py check   # verify plan hash, derived columns and results bytes
"""
import csv
import hashlib
import io
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN_SHA256 = "6d797192bffdb92473237347a6fbe59a93593eca6bd7fc32e3f54acc647369d1"
SEED = 20261009
N_PERM = 20000
N_BOOT = 2000
ALPHA = 0.05
D_THRESHOLD = 0.25
MIN_KNOWN = 30

WINDOW_MAIN = (-150, 135)
WINDOW_SENS = (-63, 70)
BOX_J = ((31.20, 32.05), (35.00, 35.60))
BOX_V = ((31.70, 32.55), (35.45, 35.70))

SETTINGS = ["cistern", "pool_reservoir", "channel", "water_pit", "tomb", "cave", "structure",
            "ruin_heap", "open_ground", "unknown"]
PLACEMENTS = ["under_stone_threshold", "wall_cavity", "pillar", "under_floor", "container_buried",
              "corner", "upper_storey", "floor_surface", "not_stated"]
HOW_FOUND = ["excavation", "chance", "looting_recovered", "unknown"]

FINE_LABELS = {
    "C01": "cistern", "C02": "pool/reservoir", "C03": "channel/aqueduct/conduit",
    "C04": "tomb or burial cave", "C05": "natural cave or shelter", "C06": "wall cavity",
    "C07": "under floor", "C08": "under a stone or threshold", "C09": "jar buried in ground",
    "C10": "near a column/pillar", "C11": "field or open ground", "C12": "ruin or heap",
    "C13": "other (known)", "C14": "structure, placement not stated", "UNK": "unknown",
}
FINE_ORDER = [f"C{i:02d}" for i in range(1, 15)]
COARSE_LABELS = {"G1": "water installation", "G2": "tomb", "G3": "cave", "G4": "structure",
                 "G5": "open air"}
COARSE_ORDER = ["G1", "G2", "G3", "G4", "G5"]

COMP_INPUT = ["id", "site", "lat", "lon", "country", "date_from", "date_to", "object_type", "container",
              "setting", "placement", "context_reported", "how_found", "source", "cluster_id", "include",
              "exclusion_reason", "flags", "judaea_by_name", "t02_id"]
COMP_DERIVED = ["context_category", "context_label", "coarse_group", "in_window_main", "in_window_sens",
                "in_region_main", "in_region_judaea"]
BRANCHES = ["P", "Pu", "M", "L"]
SCROLL_INPUT = ["entry", "col_line", "object_type", "hebrew_terms", "lexicon_terms", "t02_landmarks",
                "primary_deposit", "secondary_deposits", "setting_P", "placement_P", "container_P",
                "setting_Pu", "placement_Pu", "container_Pu", "ref_Pu", "note_Pu",
                "setting_M", "placement_M", "container_M", "ref_M", "note_M",
                "setting_L", "placement_L", "container_L", "ref_L", "note_L", "notes"]
SCROLL_DERIVED = [f"{k}_{b}" for b in BRANCHES for k in ("fine", "coarse")]
SCROLL_DOCUMENTS_ONLY = {"60"}


# ---------------------------------------------------------------- coding functions
def fine_category(setting, placement, pit_unknown=False):
    """PLAN 8.3: fine category from setting and placement."""
    if setting not in SETTINGS or placement not in PLACEMENTS:
        raise ValueError(f"bad coding {setting!r} {placement!r}")
    if setting == "water_pit":
        return "UNK" if pit_unknown else "C01"
    direct = {"cistern": "C01", "pool_reservoir": "C02", "channel": "C03", "tomb": "C04", "cave": "C05"}
    if setting in direct:
        return direct[setting]
    if setting == "unknown":
        return "UNK"
    if setting == "structure":
        return {"wall_cavity": "C06", "under_floor": "C07", "container_buried": "C07",
                "under_stone_threshold": "C08", "pillar": "C10", "corner": "C13",
                "upper_storey": "C13", "floor_surface": "C13", "not_stated": "C14"}[placement]
    if setting == "ruin_heap":
        return "C08" if placement == "under_stone_threshold" else "C12"
    # open_ground
    if placement == "container_buried":
        return "C09"
    if placement == "under_stone_threshold":
        return "C08"
    return "C11"


def coarse_group(setting, pit_unknown=False):
    """PLAN 8.4: coarse group from setting; None for unknown."""
    if setting == "water_pit":
        return None if pit_unknown else "G1"
    return {"cistern": "G1", "pool_reservoir": "G1", "channel": "G1", "tomb": "G2", "cave": "G3",
            "structure": "G4", "ruin_heap": "G5", "open_ground": "G5", "unknown": None}[setting]


def midpoint(row):
    try:
        a = float(row["date_from"])
        b = float(row["date_to"]) if row["date_to"] != "" else a
    except ValueError:
        return None
    return (a + b) / 2.0


def in_window(row, window):
    m = midpoint(row)
    return m is not None and window[0] <= m <= window[1]


def in_region_main(row):
    return any(k in row["country"] for k in ("Israel", "Palestinian", "Jordan", "Golan"))


def in_region_judaea(row):
    try:
        lat, lon = float(row["lat"]), float(row["lon"])
    except ValueError:
        return row["judaea_by_name"] == "1"
    for (la, lo) in (BOX_J, BOX_V):
        if la[0] <= lat <= la[1] and lo[0] <= lon <= lo[1]:
            return True
    return False


# ---------------------------------------------------------------- io
def read_csv(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def csv_bytes(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    return buf.getvalue().encode("utf-8")


def derive_comparanda(rows):
    out = []
    for r in rows:
        r = {k: r.get(k, "") for k in COMP_INPUT}
        fc = fine_category(r["setting"], r["placement"])
        g = coarse_group(r["setting"])
        r.update(context_category=fc, context_label=FINE_LABELS[fc], coarse_group=g or "",
                 in_window_main=int(in_window(r, WINDOW_MAIN)), in_window_sens=int(in_window(r, WINDOW_SENS)),
                 in_region_main=int(in_region_main(r)), in_region_judaea=int(in_region_judaea(r)))
        out.append(r)
    return out


def derive_scroll(rows):
    out = []
    for r in rows:
        r = {k: r.get(k, "") for k in SCROLL_INPUT}
        for b in BRANCHES:
            r[f"fine_{b}"] = fine_category(r[f"setting_{b}"], r[f"placement_{b}"])
            r[f"coarse_{b}"] = coarse_group(r[f"setting_{b}"]) or ""
        out.append(r)
    return out


def built_bytes():
    comp = derive_comparanda(read_csv("comparanda.csv"))
    scr = derive_scroll(read_csv("scroll_contexts.csv"))
    return (csv_bytes(comp, COMP_INPUT + COMP_DERIVED), csv_bytes(scr, SCROLL_INPUT + SCROLL_DERIVED))


# ---------------------------------------------------------------- statistics
def chi_square(labels_a, labels_b, cats):
    na, nb = len(labels_a), len(labels_b)
    n = na + nb
    ca = [0] * len(cats)
    cb = [0] * len(cats)
    idx = {c: i for i, c in enumerate(cats)}
    for x in labels_a:
        ca[idx[x]] += 1
    for x in labels_b:
        cb[idx[x]] += 1
    stat = 0.0
    for i in range(len(cats)):
        col = ca[i] + cb[i]
        if col == 0:
            continue
        ea = na * col / n
        eb = nb * col / n
        stat += (ca[i] - ea) ** 2 / ea + (cb[i] - eb) ** 2 / eb
    return stat


def dissimilarity(labels_a, labels_b, cats):
    na, nb = len(labels_a), len(labels_b)
    return 0.5 * sum(abs(labels_a.count(c) / na - labels_b.count(c) / nb) for c in cats)


def residuals(labels_a, labels_b, cats):
    na, nb = len(labels_a), len(labels_b)
    n = na + nb
    out = {}
    for c in cats:
        oa = labels_a.count(c)
        col = oa + labels_b.count(c)
        e = na * col / n
        var = e * (1 - na / n) * (1 - col / n)
        out[c] = round((oa - e) / math.sqrt(var), 3) if var > 0 else None
    return out


def compare(labels_a, labels_b, order):
    """labels_a = scroll (or first group), labels_b = comparanda (or second group)."""
    present = [c for c in order if c in labels_a or c in labels_b]
    res = {"n_a": len(labels_a), "n_b": len(labels_b),
           "counts_a": {c: labels_a.count(c) for c in present},
           "counts_b": {c: labels_b.count(c) for c in present}}
    if len(labels_a) == 0 or len(labels_b) == 0 or len(present) < 2:
        res.update(chi2=None, p=None, D=None, D_ci95=None, residuals_a=None)
        return res
    obs = chi_square(labels_a, labels_b, present)
    pooled = list(labels_a) + list(labels_b)
    rng = random.Random(SEED)
    ge = 0
    na = len(labels_a)
    for _ in range(N_PERM):
        rng.shuffle(pooled)
        if chi_square(pooled[:na], pooled[na:], present) >= obs - 1e-12:
            ge += 1
    p = (1 + ge) / (N_PERM + 1)
    d = dissimilarity(labels_a, labels_b, present)
    rng = random.Random(SEED)
    boots = []
    for _ in range(N_BOOT):
        a = rng.choices(labels_a, k=len(labels_a))
        b = rng.choices(labels_b, k=len(labels_b))
        boots.append(dissimilarity(a, b, present))
    boots.sort()
    lo, hi = boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT) - 1]
    res.update(chi2=round(obs, 4), p=round(p, 5), D=round(d, 4), D_ci95=[round(lo, 4), round(hi, 4)],
               residuals_a=residuals(labels_a, labels_b, present))
    return res


def verdict(res, n_known_comparanda):
    if n_known_comparanda < MIN_KNOWN:
        return "NOT TESTABLE"
    if res["p"] is None:
        return "NOT TESTABLE"
    if res["p"] < ALPHA and res["D"] >= D_THRESHOLD:
        return "DIFFERENT"
    if res["p"] >= ALPHA and res["D"] < D_THRESHOLD:
        return "SIMILAR"
    return "INCONCLUSIVE"


# ---------------------------------------------------------------- selections
def comparanda_units(rows, window=WINDOW_MAIN, judaea=False, unit="cluster", metal_only=False):
    sel = []
    for r in rows:
        if str(r["include"]) != "1":
            continue
        if not in_window(r, window) or not in_region_main(r):
            continue
        if judaea and not in_region_judaea(r):
            continue
        if metal_only and r["object_type"].startswith("documents"):
            continue
        sel.append(r)
    if unit == "rows":
        units = [dict(r) for r in sel]
    else:
        groups = {}
        order = []
        for r in sel:
            k = r["cluster_id"]
            if k not in groups:
                groups[k] = []
                order.append(k)
            groups[k].append(r)
        units = []
        for k in order:
            g = groups[k]
            cats = [fine_category(x["setting"], x["placement"]) for x in g]
            best = max(cats, key=lambda c: (cats.count(c), -cats.index(c)))
            units.append(dict(g[cats.index(best)]))
    return units


def comp_labels(units, level):
    out = []
    for u in units:
        if level == "coarse":
            g = coarse_group(u["setting"])
            if g:
                out.append(g)
        else:
            f = fine_category(u["setting"], u["placement"])
            if f != "UNK":
                out.append(f)
    return out


def scroll_labels(rows, branch="P", level="coarse", pit_unknown=False, metal_only=False):
    out = []
    for r in rows:
        if metal_only and r["entry"] in SCROLL_DOCUMENTS_ONLY:
            continue
        s, p = r[f"setting_{branch}"], r[f"placement_{branch}"]
        if level == "coarse":
            g = coarse_group(s, pit_unknown)
            if g:
                out.append(g)
        else:
            f = fine_category(s, p, pit_unknown)
            if f != "UNK":
                out.append(f)
    return out


RUNS = [
    ("main", "Main: branch P, 150 BCE-135 CE, southern Levant, clusters, all types, coarse", {}),
    ("s1_window", "Window 63 BCE-70 CE", {"window": WINDOW_SENS}),
    ("s2_region", "Region: Judaea and the Jordan valley", {"judaea": True}),
    ("s3_branch_Pu", "Scroll branch Pu (Puech 2006/2015)", {"branch": "Pu"}),
    ("s4_branch_M", "Scroll branch M (Milik 1960/1962)", {"branch": "M"}),
    ("s5_branch_L", "Scroll branch L (Lefkovits 2000)", {"branch": "L"}),
    ("s6_pit_unknown", "Scroll pits (שית/שיח/שוחה/שיא) set to unknown", {"pit_unknown": True}),
    ("s7_rows", "Comparanda counted as rows, not clusters", {"unit": "rows"}),
    ("s8_metal_only", "Coins and metal only (documents dropped on both sides)", {"metal_only": True}),
    ("s9_fine", "Fine categories C01-C14 (secondary test)", {"level": "fine"}),
]


def run_one(comp_rows, scroll_rows, opts):
    level = opts.get("level", "coarse")
    units = comparanda_units(comp_rows, window=opts.get("window", WINDOW_MAIN), judaea=opts.get("judaea", False),
                             unit=opts.get("unit", "cluster"), metal_only=opts.get("metal_only", False))
    cl = comp_labels(units, level)
    sl = scroll_labels(scroll_rows, branch=opts.get("branch", "P"), level=level,
                       pit_unknown=opts.get("pit_unknown", False), metal_only=opts.get("metal_only", False))
    order = COARSE_ORDER if level == "coarse" else FINE_ORDER
    res = compare(sl, cl, order)
    res["n_comparanda_units_total"] = len(units)
    res["n_comparanda_unknown"] = len(units) - len(cl)
    res["verdict"] = verdict(res, len(cl))
    return res


def bias_checks(comp_rows, scroll_rows):
    units = comparanda_units(comp_rows)
    exc = [u for u in units if u["how_found"] == "excavation"]
    non = [u for u in units if u["how_found"] in ("chance", "looting_recovered")]
    out = {}
    b1 = compare(comp_labels(exc, "coarse"), comp_labels(non, "coarse"), COARSE_ORDER)
    b1["verdict"] = verdict(b1, b1["n_a"] + b1["n_b"])
    b1["note"] = "group a = excavated, group b = chance plus looting_recovered"
    out["B1_excavated_vs_not"] = b1
    sl = scroll_labels(scroll_rows)
    for key, grp in (("B2a_scroll_vs_excavated", exc), ("B2b_scroll_vs_not_excavated", non)):
        r = compare(sl, comp_labels(grp, "coarse"), COARSE_ORDER)
        r["verdict"] = verdict(r, r["n_b"])
        out[key] = r
    b3 = {}
    for h in HOW_FOUND:
        g = [u for u in units if u["how_found"] == h]
        unk = sum(1 for u in g if coarse_group(u["setting"]) is None)
        b3[h] = {"units": len(g), "unknown_context": unk,
                 "share_unknown": round(unk / len(g), 3) if g else None}
    out["B3_unknown_share_by_how_found"] = b3
    return out


def analyse():
    comp = read_csv("comparanda.csv")
    scr = read_csv("scroll_contexts.csv")
    runs = {}
    for key, label, opts in RUNS:
        r = run_one(comp, scr, opts)
        r["label"] = label
        runs[key] = r
    bias = bias_checks(comp, scr)
    main_v = runs["main"]["verdict"]
    changed = [k for k in runs if k != "main" and runs[k]["verdict"] != main_v]
    reporting_sensitive = (bias["B1_excavated_vs_not"]["verdict"] == "DIFFERENT" or
                           bias["B2a_scroll_vs_excavated"]["verdict"] != bias["B2b_scroll_vs_not_excavated"]["verdict"])
    excluded = [{"id": r["id"], "reason": r["exclusion_reason"]} for r in comp if str(r["include"]) != "1"]
    out_window = [r["id"] for r in comp if str(r["include"]) == "1" and not in_window(r, WINDOW_MAIN)]
    return {
        "plan_sha256": PLAN_SHA256,
        "settings": {"seed": SEED, "n_perm": N_PERM, "n_boot": N_BOOT, "alpha": ALPHA,
                     "D_threshold": D_THRESHOLD, "min_known_comparanda": MIN_KNOWN},
        "runs": runs,
        "bias": bias,
        "summary": {"main_verdict": main_v,
                    "robust": not changed, "runs_changing_verdict": changed,
                    "reporting_sensitive": reporting_sensitive},
        "comparanda_rows": len(comp),
        "comparanda_excluded": excluded,
        "comparanda_outside_main_window": out_window,
    }


# ---------------------------------------------------------------- report
def fmt_counts(res, order, labels):
    rows = []
    for c in order:
        if c in res["counts_a"]:
            rows.append(f"| {c} {labels[c]} | {res['counts_a'][c]} | {res['counts_b'][c]} |")
    return rows


def report(results):
    L = ["# Concealment contexts: results", "",
         "Generated by `concealment.py run`. Plan: PLAN.md, SHA-256 `" + results["plan_sha256"] + "`.",
         "Labels: every count below is INFERENCE (my coding of reported contexts); the reported contexts are EVIDENCE.", ""]
    s = results["summary"]
    L += [f"Main verdict: **{s['main_verdict']}**. Robust across one-factor runs: **{'yes' if s['robust'] else 'no'}**"
          + (f" (changed by: {', '.join(s['runs_changing_verdict'])})" if s["runs_changing_verdict"] else "") + ".",
          f"Reporting-sensitive (PLAN 12): **{'yes' if s['reporting_sensitive'] else 'no'}**.", ""]
    L += ["## Runs", "", "| run | scroll n | comparanda n (known) | comparanda unknown | chi2 | p | D | D 95% CI | verdict |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, r in results["runs"].items():
        ci = f"{r['D_ci95'][0]}-{r['D_ci95'][1]}" if r["D_ci95"] else "-"
        L.append(f"| {k} | {r['n_a']} | {r['n_b']} | {r['n_comparanda_unknown']} | {r['chi2']} | {r['p']} | {r['D']} | {ci} | {r['verdict']} |")
    L += ["", "## Main run: counts by coarse group", "", "| group | scroll | comparanda |", "|---|---|---|"]
    L += fmt_counts(results["runs"]["main"], COARSE_ORDER, COARSE_LABELS)
    L += ["", "Adjusted standardised residuals, scroll row (positive = more common in the scroll than expected):", ""]
    L += ["| group | residual |", "|---|---|"]
    for c, v in results["runs"]["main"]["residuals_a"].items():
        L.append(f"| {c} {COARSE_LABELS[c]} | {v} |")
    L += ["", "## Fine categories (run s9)", "", "| category | scroll | comparanda |", "|---|---|---|"]
    L += fmt_counts(results["runs"]["s9_fine"], FINE_ORDER, FINE_LABELS)
    b = results["bias"]
    L += ["", "## Reporting-bias check", "",
          "| check | group a n | group b n | p | D | verdict |", "|---|---|---|---|---|---|"]
    for k in ("B1_excavated_vs_not", "B2a_scroll_vs_excavated", "B2b_scroll_vs_not_excavated"):
        r = b[k]
        L.append(f"| {k} | {r['n_a']} | {r['n_b']} | {r['p']} | {r['D']} | {r['verdict']} |")
    L += ["", "B1 counts (a = excavated, b = chance or looting recovered):", "", "| group | excavated | not excavated |", "|---|---|---|"]
    L += fmt_counts(b["B1_excavated_vs_not"], COARSE_ORDER, COARSE_LABELS)
    L += ["", "B3: share of comparanda units with unknown context, by how found:", "",
          "| how found | units | unknown context | share |", "|---|---|---|---|"]
    for h, v in b["B3_unknown_share_by_how_found"].items():
        L.append(f"| {h} | {v['units']} | {v['unknown_context']} | {v['share_unknown']} |")
    L += ["", f"Comparanda rows: {results['comparanda_rows']}; excluded by definition: {len(results['comparanda_excluded'])}; "
          f"eligible but outside the main window: {', '.join(results['comparanda_outside_main_window']) or 'none'}.", ""]
    return "\n".join(L) + "\n"


def plan_hash():
    with open(os.path.join(HERE, "PLAN.md"), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def results_bytes(results):
    return (json.dumps(results, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "check"
    if plan_hash() != PLAN_SHA256:
        raise SystemExit("PLAN.md hash does not match the frozen hash")
    if cmd == "build":
        cb, sb = built_bytes()
        with open(os.path.join(HERE, "comparanda.csv"), "wb") as f:
            f.write(cb)
        with open(os.path.join(HERE, "scroll_contexts.csv"), "wb") as f:
            f.write(sb)
        print("built")
    elif cmd == "run":
        res = analyse()
        with open(os.path.join(HERE, "results.json"), "wb") as f:
            f.write(results_bytes(res))
        with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as f:
            f.write(report(res))
        print(json.dumps(res["summary"]))
    elif cmd == "check":
        cb, sb = built_bytes()
        for name, b in (("comparanda.csv", cb), ("scroll_contexts.csv", sb)):
            with open(os.path.join(HERE, name), "rb") as f:
                if f.read() != b:
                    raise SystemExit(f"{name} derived columns are stale; run build")
        res = analyse()
        with open(os.path.join(HERE, "results.json"), "rb") as f:
            if f.read() != results_bytes(res):
                raise SystemExit("results.json differs from a fresh run")
        print("ok")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
