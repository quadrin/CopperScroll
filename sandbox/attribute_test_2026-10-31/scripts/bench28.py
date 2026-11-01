"""Run 28 benchmark D, gate and reported checks (RULE.md). Written 31 Oct 2026 before any consolidated describer
file or concordance existed.

usage: python3 bench28.py gate     -> out/bench_items.csv, out/bench_scores.csv, out/alpha.json, out/gate.json
       python3 bench28.py checks   -> out/checks.json (+ per-check score files)

Inputs:
  inventory  ../attribute_inventory_2026-10-31/out/atq41_consolidated_v2.csv (whole features = key without '.')
  describers out/<src>_consolidated.csv for src in djd3, ben93, ba72 (consolidate28.py; sub-feature rows kept)
  concordance keyed/concordance.csv (agreed rows plus third reading)
  1952 points research/history/devaux1952_cave_points/devaux1952_cave_points.csv

Interpretations fixed here, before data (also in FORK_LOG.md):
  * A describer "whole feature" is a row with no parent, or whose parent is not itself in an item class group
    (a cave keyed as a sub-feature of a survey *site* is a whole feature; a chamber of a cave is not).
  * Concordance refs and describer keys are compared after normalisation: upper case, spaces removed, leading
    SITE/CAVE/NO./# removed. A ref also matches a describer row whose key is ref + '.' + suffix only if no row
    has key == ref (then every such child in an item class group shares the truth set).
  * A describer item is excluded when any concordance row linking it is marked copied = yes.
  * Grids: two groups of 4-6 digits; E first. If E/N falls outside the survey extent (E 175-200, N 115-160 km)
    and N/E falls inside, N/E is used and flagged.
"""
import csv
import json
import random
import re
import sys
from pathlib import Path

import numpy as np
from scipy.stats import binom

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model28 import (ATTRS, INV, ITEM_GROUPS, NONCLASS, RUN, Model, attrs_of, expected_coverage, fit_alpha,  # noqa: E402
                     group, read_csv, set_size, training_pairs)

DESCRIBERS = ["djd3", "ben93", "ba72"]
SEEN_BEN93 = {"327", "332", "355", "363", "370", "372", "378", "386", "387", "390", "391"}
POINTS = RUN.parents[1] / "research/history/devaux1952_cave_points/devaux1952_cave_points.csv"


def norm_ref(s):
    s = (s or "").upper().replace(" ", "")
    s = re.sub(r"^(SITE|CAVE|NOS?\.?|#)+", "", s)
    return s.strip(".:,")


def norm_atq(k):
    k = (k or "").upper().replace(" ", "")
    k = re.sub(r"^(CAVE|ATQ41:)", "", k)
    m = re.match(r"^(\d+[A-Z]?)/([IVX]+)$", k)
    if m:
        k = f"{m.group(2)}/{m.group(1)}"
    return k


def parse_grid(g):
    nums = re.findall(r"\d{4,6}", (g or "").replace(".", ""))
    if len(nums) < 2:
        return None
    a, b = nums[0], nums[1]
    def km(x):
        return int(x) * {4: 0.1, 5: 0.01, 6: 0.001}[len(x)]
    e, n = km(a), km(b)
    ok = lambda e_, n_: 175 <= e_ <= 200 and 115 <= n_ <= 160
    if ok(e, n):
        return e, n, len(a), ""
    if ok(n, e):
        return n, e, len(a), "swapped N/E"
    return None


def inventory(path=INV / "out/atq41_consolidated_v2.csv"):
    rows = [r for r in read_csv(path) if "." not in r["key"]]
    cands = [attrs_of(r) for r in rows]
    pos = []
    for r in rows:
        try:
            pos.append((float(r["E_km"]), float(r["N_km"])))
        except (TypeError, ValueError):
            pos.append(None)
    return rows, cands, pos


def describer_rows():
    out = []
    for src in DESCRIBERS:
        p = RUN / f"out/{src}_consolidated.csv"
        if not p.exists():
            continue
        rows = read_csv(p)
        by = {r["key"]: r for r in rows}
        for r in rows:
            par = r.get("parent_id", "")
            if par and par in by and group(by[par]["feature_class"]) in ITEM_GROUPS:
                continue  # a part of a cave or water feature, not a whole feature
            out.append(dict(r, src=src))
    return out


def concordance():
    p = RUN / "keyed/concordance.csv"
    return read_csv(p) if p.exists() else []


def build_items(inv_rows, cands, pos, truth_mode="primary"):
    keyidx = {r["key"]: i for i, r in enumerate(inv_rows)}
    pts = {}
    if POINTS.exists():
        for r in read_csv(POINTS):
            try:
                pts[str(int(float(r["point"])))] = (float(r["pal_e_km"]), float(r["pal_n_km"]))
            except (KeyError, ValueError):
                pass
    drows = describer_rows()
    conc = concordance()
    keys_by_src = {}
    for r in drows:
        keys_by_src.setdefault(r["src"], set()).add(norm_ref(r["key"]))
    links, copied = {}, set()
    for c in conc:
        src = c.get("describer", "").strip()
        if src not in DESCRIBERS or c.get("ref_type", "").strip() not in ("site_number", "cave_number"):
            continue
        ref = norm_ref(c.get("describer_ref"))
        targets = [r for r in drows if r["src"] == src and (norm_ref(r["key"]) == ref or
                   (ref not in keys_by_src.get(src, set()) and norm_ref(r["key"]).startswith(ref + ".")))]
        atq = [keyidx[k] for k in (norm_atq(x) for x in c.get("atq41_keys", "").split(";")) if k in keyidx]
        for t in targets:
            tid = (src, t["key"])
            if c.get("copied", "").strip().lower() == "yes":
                copied.add(tid)
            elif atq:
                links.setdefault(tid, set()).update(atq)
    items, dropped = [], {"class": 0, "no_attr": 0, "no_truth": 0, "copied": 0}
    for r in drows:
        tid = (r["src"], r["key"])
        clue = attrs_of(r)
        if clue["cls"] not in ITEM_GROUPS:
            dropped["class"] += 1
            continue
        if all(clue[a] is None for a in NONCLASS):
            dropped["no_attr"] += 1
            continue
        if tid in copied:
            dropped["copied"] += 1
            continue
        truth, basis, flag = [], "", ""
        if truth_mode == "primary" and tid in links:
            truth, basis = sorted(links[tid]), "concordance"
        else:
            xy, rad = None, None
            if r["src"] == "djd3":
                xy = pts.get(norm_ref(r["key"]).split(".")[0])
                rad = 0.15
            else:
                g = parse_grid(r.get("grid_printed"))
                if g:
                    xy, rad, flag = (g[0], g[1]), (0.15 if g[2] >= 5 else 0.30), g[3]
            if xy:
                truth = [j for j, p in enumerate(pos) if p and cands[j]["cls"] == clue["cls"] and
                         ((p[0] - xy[0]) ** 2 + (p[1] - xy[1]) ** 2) ** 0.5 <= rad]
                basis = "location"
        if not truth:
            dropped["no_truth"] += 1
            continue
        items.append({"id": f"{r['src']}:{r['key']}", "src": r["src"], "key": r["key"],
                      "group": f"{r['src']}:{r['key'].split('.')[0]}", "clue": clue, "truth": truth,
                      "basis": basis, "grid_flag": flag})
    return items, dropped


def folds(items, seed=2828):
    groups = sorted({it["group"] for it in items})
    random.Random(seed).shuffle(groups)
    f = {g: (i % 2) + 1 for i, g in enumerate(groups)}
    for it in items:
        it["fold"] = f[it["group"]]


def fit(model, train, attrs):
    alpha, post = {}, {}
    for a in attrs:
        alpha[a], w = fit_alpha(training_pairs(model, train, a))
        post[a] = w
    return alpha, post


def score(model, items, prefix=""):
    """Cross-fitted scores: each fold scored with alpha from the other fold."""
    out, alphas = [], {}
    for k in (1, 2):
        train = [it for it in items if it["fold"] != k]
        a_attr, _ = fit(model, train, ATTRS)
        a_cls, _ = fit(model, train, ["cls"])
        alphas[f"fold{k}"] = {"attributes": a_attr, "class_only": a_cls, "n_train": len(train)}
        for it in (x for x in items if x["fold"] == k):
            row = {"id": it["id"], "src": it.get("src", ""), "group": it["group"], "fold": k, "n_truth": len(it["truth"]),
                   "basis": it.get("basis", "")}
            prior = len(it["truth"]) / model.N
            for name, attrs, alpha in (("attr", ATTRS, a_attr), ("cls", ["cls"], a_cls)):
                post = model.posterior(it["clue"], alpha, attrs)
                pt = float(post[it["truth"]].sum())
                row[f"log10bf_{name}"] = float(np.log10(max(pt, 1e-300) / prior))
                row[f"cov50_{name}"] = expected_coverage(post, it["truth"], 0.5)
                row[f"cov90_{name}"] = expected_coverage(post, it["truth"], 0.9)
                row[f"rank_{name}"] = int(1 + (post > post[it["truth"]].max() * (1 + 1e-12)).sum())
                row[f"size90_{name}"] = set_size(post, 0.9)
            row["gain"] = row["log10bf_attr"] - row["log10bf_cls"]
            row["attrs_known"] = ";".join(a for a in ATTRS if it["clue"][a] is not None)
            out.append(row)
    return out, alphas


def boot(rows, field, seed=2829, n=4000):
    groups = sorted({r["group"] for r in rows})
    by = {g: [r[field] for r in rows if r["group"] == g] for g in groups}
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n):
        pick = rng.integers(0, len(groups), len(groups))
        vals = [v for i in pick for v in by[groups[i]]]
        means.append(np.mean(vals))
    return float(np.mean([r[field] for r in rows])), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summary(rows):
    N = len(rows)
    s = {"N": N}
    for name in ("attr", "cls"):
        for lvl, p in ((50, 0.5), (90, 0.9)):
            cov = float(np.mean([r[f"cov{lvl}_{name}"] for r in rows])) if N else None
            lo, hi = (binom.ppf(0.025, N, p) / N, binom.ppf(0.975, N, p) / N) if N else (None, None)
            s[f"cov{lvl}_{name}"] = cov
            s[f"cov{lvl}_accept"] = [lo, hi]
        if N:
            s[f"log10bf_{name}"] = boot(rows, f"log10bf_{name}")
            s[f"median_rank_{name}"] = float(np.median([r[f"rank_{name}"] for r in rows]))
            s[f"median_size90_{name}"] = float(np.median([r[f"size90_{name}"] for r in rows]))
    if N:
        s["gain"] = boot(rows, "gain")
    return s


def write(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def gate():
    inv_rows, cands, pos = inventory()
    model = Model(cands)
    items, dropped = build_items(inv_rows, cands, pos)
    folds(items)
    write(RUN / "out/bench_items.csv", [{"id": it["id"], "fold": it["fold"], "basis": it["basis"], "grid_flag": it["grid_flag"],
                                          "truth": ";".join(inv_rows[j]["key"] for j in it["truth"]),
                                          **{a: (";".join("/".join(sorted(s)) for s in v) if a == "dirs" and v else v)
                                             for a, v in it["clue"].items()}} for it in items])
    res = {"candidates": model.N, "items": len(items), "dropped": dropped,
           "by_source": {s: sum(it["src"] == s for it in items) for s in DESCRIBERS},
           "by_basis": {b: sum(it["basis"] == b for it in items) for b in ("concordance", "location")}}
    if len(items) < 30:
        res.update(status="STOP: fewer than 30 items; not identifiable from available evidence; scroll not scored")
        json.dump(res, open(RUN / "out/gate.json", "w"), indent=1)
        print(json.dumps(res, indent=1))
        return
    rows, alphas = score(model, items)
    write(RUN / "out/bench_scores.csv", rows)
    full_attr, post_attr = fit(model, items, ATTRS)
    json.dump({"cross_fit": alphas, "all_items": full_attr,
               "posterior_all_items": {a: [round(float(x), 6) for x in w] for a, w in post_attr.items()}},
              open(RUN / "out/alpha.json", "w"), indent=1)
    s = summary(rows)
    g1 = all(s[f"cov{l}_accept"][0] <= s[f"cov{l}_attr"] <= s[f"cov{l}_accept"][1] for l in (50, 90))
    g2 = s["log10bf_attr"][0] > 0 and s["log10bf_attr"][1] > 0
    g3 = s["gain"][0] > 0 and s["gain"][1] > 0
    res.update(summary=s, G1=g1, G2=g2, G3=g3, status="PASS" if (g1 and g2 and g3) else "FAIL: scroll not scored")
    json.dump(res, open(RUN / "out/gate.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


def checks():
    out = {}
    inv_rows, cands, pos = inventory()
    model = Model(cands)
    # 3. truth by location only
    items, dropped = build_items(inv_rows, cands, pos, truth_mode="location")
    folds(items)
    rows, _ = score(model, items) if len(items) >= 4 else ([], {})
    write(RUN / "out/check3_location_scores.csv", rows)
    out["3_location_only"] = {"items": len(items), "dropped": dropped, "summary": summary(rows)}
    # 4. exposure sensitivity: drop ben93 items from seen sites and from the Makkukh cave list
    items, _ = build_items(inv_rows, cands, pos)
    folds(items)
    def seen(it):
        if it["src"] != "ben93":
            return False
        site = it["key"].split(".")[0]
        return site in SEEN_BEN93 or not (site.isdigit() and 322 <= int(site) <= 428)
    keep = [it for it in items if not seen(it)]
    rows, _ = score(model, keep) if len(keep) >= 4 else ([], {})
    out["4_exposure_sensitivity"] = {"items": len(keep), "summary": summary(rows)}
    # 5. alpha posteriors on all benchmark items, and q distributions
    full, post = fit(model, items, ATTRS)
    out["5_alpha_all_items"] = {a: {"mean": full[a], "n_pairs": len(training_pairs(model, items, a)),
                                    "ci95": _ci(post[a])} for a in ATTRS}
    out["5_q_by_attr"] = {a: sorted({round(model.q(a, it["clue"][a]), 4) for it in items if it["clue"][a] is not None})
                          for a in ATTRS}
    # 1. same team, other medium: plan readings as clues against the text-only inventory
    out["1_plans_vs_text"] = _plans_check()
    # 2. Kh. Qumran: Magen & Peleg loci against IIIA (walls excluded)
    out["2_mp18_vs_qum3a"] = _qumran_check()
    json.dump(out, open(RUN / "out/checks.json", "w"), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float)[:6000])


def _ci(w):
    from model28 import ALPHA_GRID
    c = np.cumsum(w)
    return [float(ALPHA_GRID[np.searchsorted(c, 0.025)]), float(ALPHA_GRID[min(np.searchsorted(c, 0.975), len(c) - 1)])]


def _plans_check():
    sys.path.insert(0, str(INV / "scripts"))
    import plan_merge as pm
    A, B = pm.load("A"), pm.load("B")
    C = {(r["key"], r["field"]): r["C_value"].strip() for r in read_csv(INV / "keyed/atq41plans_C_adjudication.csv")}
    rows = [r for r in read_csv(INV / "out/atq41_consolidated.csv") if "." not in r["key"]]
    cands = [attrs_of(r) for r in rows]
    model = Model(cands)
    idx = {r["key"]: i for i, r in enumerate(rows)}
    items = []
    for k in sorted(set(A) | set(B)):
        if k not in idx:
            continue
        a, b = A.get(k, {}), B.get(k, {})
        vals = {}
        for f in ("n_openings_plan", "opening_dirs_plan", "n_pillars_plan", "n_steps_plan"):
            va, vb = a.get(f, ""), b.get(f, "")
            if (k, f) in C:
                vals[f] = C[(k, f)]
            elif va and vb:
                vals[f] = va if (va == vb or (f == "opening_dirs_plan" and pm.dirs_agree(va, vb))) else ""
            else:
                vals[f] = va or vb
        clue = attrs_of({"feature_class": rows[idx[k]]["feature_class"], **vals}, f_open="n_openings_plan",
                        f_dirs="opening_dirs_plan", f_pil="n_pillars_plan", f_steps="n_steps_plan")
        if clue["cls"] is None or all(clue[x] is None for x in NONCLASS):
            continue
        items.append({"id": f"plan:{k}", "group": f"plan:{k}", "clue": clue, "truth": [idx[k]]})
    folds(items)
    srows, _ = score(model, items) if len(items) >= 4 else ([], {})
    write(RUN / "out/check1_plans_scores.csv", srows)
    return {"items": len(items), "candidates": model.N, "summary": summary(srows)}


def _qumran_check():
    q = [r for r in read_csv(INV / "out/qum3a_consolidated.csv") if "." not in r["key"] and r["feature_class"] != "wall"]
    cands = [attrs_of(r) for r in q]
    model = Model(cands)
    idx = {r["key"]: i for i, r in enumerate(q)}
    items = []
    for r in read_csv(INV / "out/mp18_consolidated.csv"):
        k = r["key"]
        if "." in k or not re.match(r"^L\d+[A-Z]?$", k) or k not in idx:
            continue
        clue = attrs_of(r)
        if clue["cls"] is None or all(clue[x] is None for x in NONCLASS):
            continue
        items.append({"id": f"mp18:{k}", "group": f"mp18:{k}", "clue": clue, "truth": [idx[k]]})
    folds(items)
    srows, _ = score(model, items) if len(items) >= 4 else ([], {})
    write(RUN / "out/check2_qumran_scores.csv", srows)
    return {"items": len(items), "candidates": model.N, "summary": summary(srows)}


if __name__ == "__main__":
    {"gate": gate, "checks": checks}[sys.argv[1]]()
