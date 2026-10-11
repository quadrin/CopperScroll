#!/usr/bin/env python3
"""Hidden deposits, 200 BCE to 135 CE: a fuller catalogue, the precedent's comparison re-run on it,
and two descriptive comparisons (stated depths; placement relative to a named landmark), as frozen
in PLAN.md.

The statistic, runs, coding functions and decision wording are imported unchanged from
research/comparanda/concealment_contexts/concealment.py after its SHA-256 is checked. The scroll
coding is read in place from that folder's scroll_contexts.csv, also hash-checked.

Standard library only. Deterministic. Run from the repository root with python3 -I:

  python3 -I research/comparanda/hoards_full/hoards_full.py build   # recompute derived columns of hoards.csv
  python3 -I research/comparanda/hoards_full/hoards_full.py run     # write results.json and RESULTS.md
  python3 -I research/comparanda/hoards_full/hoards_full.py check   # verify hashes, derived columns, results
"""
import ast
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(RESEARCH)
PREC_DIR = os.path.join(RESEARCH, "comparanda", "concealment_contexts")

PLAN_SHA256 = "1f0a90a932b98ee7e6c0549b6550ae54048e2ed727ac6bf1aa0a85441ee0362c"
FROZEN = {
    os.path.join(PREC_DIR, "PLAN.md"): "6d797192bffdb92473237347a6fbe59a93593eca6bd7fc32e3f54acc647369d1",
    os.path.join(PREC_DIR, "concealment.py"): "976b59b1dcd8ccb60cb4a127da80ca7e12de9bbb53f8fdf78c3a476d8771b265",
    os.path.join(PREC_DIR, "scroll_contexts.csv"): "c9547bb28dc93aed3d6256148d5bb7211b7403e91da922c4aa82c2be1949ae50",
    os.path.join(PREC_DIR, "comparanda.csv"): "2e1f970ede7e974aa76f0fa0d8e495d0026872be93722e6d6392d3b4f5c0d542",
    os.path.join(RESEARCH, "schematics", "searches", "search_04_depths.py"):
        "71e39b3dd9f9812ba16fe59cd7e695ba8c58802dd95577c0ee5fe9de72bd059b",
    os.path.join(RESEARCH, "agent_review_2026-10-07", "wave1", "T02_hoard_match", "hoards.json"):
        "e5972e7f486ed7bac1e5db424f9174a855895f7f02b40e03b04f4069baa3e4d8",
}
PREC_RESULTS = os.path.join(PREC_DIR, "results.json")
PREC_RESULTS_SHA256 = "88dd29004763e7770942e60cd00560ccd589a234473234d3d9fb59e68c9ef862"
TRANSLATION = os.path.join(REPO, "text", "translation_en.json")

WINDOW_CAT = (-200, 135)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_frozen():
    bad = [p for p, h in FROZEN.items() if sha256(p) != h]
    if bad:
        raise SystemExit("frozen input changed: " + ", ".join(os.path.relpath(p, REPO) for p in bad))
    if sha256(os.path.join(HERE, "PLAN.md")) != PLAN_SHA256:
        raise SystemExit("PLAN.md hash does not match the frozen hash")


def load_precedent():
    check_frozen()
    spec = importlib.util.spec_from_file_location("concealment_precedent", os.path.join(PREC_DIR, "concealment.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_precedent()

PREC_INPUT = list(C.COMP_INPUT)
NEW_INPUT = ["origin", "first_read", "unexposed_at_freeze", "object_class", "temple_related", "depth_m",
             "depth_datum", "depth_text", "landmark", "landmark_text", "discovery_year", "terminus_text",
             "sources_pages", "recode_reason", "prec_setting", "prec_placement", "prec_include", "prec_date"]
INPUT = PREC_INPUT + NEW_INPUT
DERIVED = list(C.COMP_DERIVED) + ["in_window_catalogue", "window_status", "landmark_strict"]
FIELDS = INPUT + DERIVED

ORIGINS = ["precedent", "t02", "new"]
OBJECT_CLASSES = ["coins", "metal_objects", "coins_and_metal", "documents", "sacred_objects", "mixed"]
DEPTH_DATUMS = ["present_surface", "ancient_floor", "feature_top", "unstated"]
LANDMARK_CLASSES = ["corner", "step", "pillar", "threshold", "gate", "wall_face"]

# PLAN 10, scroll expressions (case-insensitive)
SCROLL_RE = {
    "corner": r"\bcorners?\b",
    "step": r"\b(steps?|stairs?|stairway|staircase)\b",
    "pillar": r"\b(pillars?|columns?)\b",
    "threshold": r"\b(thresholds?|doors?|doorways?|entrances?)\b|as you go in|as you enter|on entering",
    "gate": r"\bgates?\b|\bgateway\b",
    "wall_face": r"\bwalls?\b",
}
SCROLL_THRESHOLD_STRICT = r"\b(thresholds?|doors?|doorways?)\b"
COMP_THRESHOLD_STRICT = r"threshold|door"


# ---------------------------------------------------------------- io and derivation
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def csv_bytes(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    return buf.getvalue().encode("utf-8")


def window_status(r):
    try:
        a = float(r["date_from"])
        b = float(r["date_to"]) if r["date_to"] != "" else a
    except ValueError:
        return "unknown"
    lo, hi = WINDOW_CAT
    if lo <= a and b <= hi:
        return "inside"
    if b < lo or a > hi:
        return "outside"
    return "partial"


def landmark_classes(r):
    v = r.get("landmark", "")
    return [x for x in v.split(";") if x in LANDMARK_CLASSES]


def landmark_strict(r):
    cls = landmark_classes(r)
    if "threshold" in cls and not re.search(COMP_THRESHOLD_STRICT, r.get("landmark_text", ""), re.I):
        cls = [c for c in cls if c != "threshold"]
    if cls:
        return ";".join(cls)
    return "none_stated" if r.get("landmark", "") else ""


def derive(rows):
    out = []
    for r in rows:
        r = {k: r.get(k, "") for k in INPUT}
        fc = C.fine_category(r["setting"], r["placement"])
        g = C.coarse_group(r["setting"])
        r.update(context_category=fc, context_label=C.FINE_LABELS[fc], coarse_group=g or "",
                 in_window_main=int(C.in_window(r, C.WINDOW_MAIN)), in_window_sens=int(C.in_window(r, C.WINDOW_SENS)),
                 in_region_main=int(C.in_region_main(r)), in_region_judaea=int(C.in_region_judaea(r)),
                 in_window_catalogue=int(C.in_window(r, WINDOW_CAT)), window_status=window_status(r),
                 landmark_strict=landmark_strict(r))
        out.append(r)
    return out


def built_bytes():
    return csv_bytes(derive(read_csv(os.path.join(HERE, "hoards.csv"))), FIELDS)


def validate(rows):
    ids = set()
    for r in rows:
        if r["id"] in ids:
            raise ValueError(f"duplicate id {r['id']}")
        ids.add(r["id"])
        if r["setting"] not in C.SETTINGS or r["placement"] not in C.PLACEMENTS:
            raise ValueError(f"{r['id']}: bad setting/placement")
        if r["how_found"] not in C.HOW_FOUND:
            raise ValueError(f"{r['id']}: bad how_found")
        if r["origin"] not in ORIGINS or r["first_read"] not in ("before_freeze", "after_freeze"):
            raise ValueError(f"{r['id']}: bad origin/first_read")
        if r["object_class"] not in OBJECT_CLASSES:
            raise ValueError(f"{r['id']}: bad object_class")
        if r["depth_datum"] and r["depth_datum"] not in DEPTH_DATUMS:
            raise ValueError(f"{r['id']}: bad depth_datum")
        if (r["depth_m"] == "") != (r["depth_datum"] == ""):
            raise ValueError(f"{r['id']}: depth_m and depth_datum must be given together")
        if r["landmark"]:
            parts = r["landmark"].split(";")
            if parts != ["none_stated"] and not all(p in LANDMARK_CLASSES for p in parts):
                raise ValueError(f"{r['id']}: bad landmark {r['landmark']}")
        if r["include"] == "1" and r["setting"] == "unknown" and r["landmark"]:
            raise ValueError(f"{r['id']}: landmark coded for an unknown context")
        for k in ("landmark_text", "depth_text", "context_reported"):
            for q in re.findall(r"[\"“']([^\"”']{3,})[\"”']", r[k]):
                if len(q.split()) > 12:
                    raise ValueError(f"{r['id']}: quote longer than 12 words in {k}")
    return True


# ---------------------------------------------------------------- comparison runs (precedent, unchanged)
def precedent_summary(runs, bias):
    main_v = runs["main"]["verdict"]
    changed = [k for k in runs if k != "main" and runs[k]["verdict"] != main_v]
    reporting_sensitive = (bias["B1_excavated_vs_not"]["verdict"] == "DIFFERENT" or
                           bias["B2a_scroll_vs_excavated"]["verdict"] != bias["B2b_scroll_vs_not_excavated"]["verdict"])
    return {"main_verdict": main_v, "robust": not changed, "runs_changing_verdict": changed,
            "reporting_sensitive": reporting_sensitive}


def restore_precedent_coding(rows):
    out = []
    for r in rows:
        r = dict(r)
        if r["recode_reason"]:
            if r["prec_setting"]:
                r["setting"] = r["prec_setting"]
            if r["prec_placement"]:
                r["placement"] = r["prec_placement"]
            if r["prec_include"]:
                r["include"] = r["prec_include"]
            if r["prec_date"]:
                a, b = r["prec_date"].split("..")
                r["date_from"], r["date_to"] = a, b
        out.append(r)
    return out


EXTRA_RUNS = [
    ("x1_catalogue_window", "Catalogue window 200 BCE-135 CE instead of 150 BCE-135 CE",
     lambda rows: rows, {"window": WINDOW_CAT}),
    ("x2_new_rows_only", "Main run on rows first catalogued in this lane (origin new or t02)",
     lambda rows: [r for r in rows if r["origin"] in ("new", "t02")], {}),
    ("x3_precedent_coding", "Main run with the precedent's coding restored for recoded rows",
     restore_precedent_coding, {}),
    ("x4_after_freeze_only", "Main run on rows first read after this lane's freeze",
     lambda rows: [r for r in rows if r["first_read"] == "after_freeze"], {}),
]
def _without_new_qumran(rows):
    return [r for r in rows if not (r["origin"] == "new" and "qumran_cave" in r["flags"])]


EXPLORATORY_RUNS = [
    ("e1_without_new_qumran_caves",
     "EXPLORATORY (chosen after coding): main run without the Qumran caves 2Q-12Q added here",
     _without_new_qumran, {}),
    ("e2_s1_window_without_new_qumran_caves",
     "EXPLORATORY (chosen after coding): run s1 (63 BCE-70 CE) without the Qumran caves 2Q-12Q added here",
     _without_new_qumran, {"window": C.WINDOW_SENS}),
]


def run_set(rows, scroll, spec):
    out = {}
    for key, label, filt, opts in spec:
        r = C.run_one(filt(rows), scroll, opts)
        r["label"] = label
        out[key] = r
    return out


# ---------------------------------------------------------------- PLAN 9: depths
def scroll_digs():
    path = os.path.join(RESEARCH, "schematics", "searches", "search_04_depths.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    digs, cubits = None, None
    for n in tree.body:
        if isinstance(n, ast.Assign):
            t = n.targets[0]
            if isinstance(t, ast.Name) and t.id == "DIGS":
                digs = ast.literal_eval(n.value)
            if isinstance(t, ast.Tuple) and [e.id for e in t.elts] == ["CUBIT", "CUBIT_LO", "CUBIT_HI"]:
                cubits = ast.literal_eval(n.value)
    return digs, {"short": cubits[1], "working": cubits[0], "royal": cubits[2]}


def describe(values):
    v = sorted(values)
    n = len(v)
    if n == 0:
        return {"n": 0}
    d = {"n": n, "min": round(v[0], 3), "median": round(statistics.median(v), 3), "max": round(v[-1], 3)}
    if n >= 4:
        q = statistics.quantiles(v, n=4, method="inclusive")
        d["q1"], d["q3"] = round(q[0], 3), round(q[2], 3)
    for t in (0.5, 1, 2, 3):
        d[f"share_deeper_than_{t}m"] = round(sum(1 for x in v if x > t) / n, 3)
    return d


def depth_comparison(rows):
    digs, cubits = scroll_digs()
    elig = [r for r in rows if str(r["include"]) == "1" and C.in_region_main(r) and C.in_window(r, WINDOW_CAT)]
    with_d = [r for r in elig if r["depth_m"] != ""]
    out = {"scroll_phrases": len(digs), "cubit_branches_m": cubits,
           "scroll_restored_or_corrupt_entries": [e for e, _, _, note in digs if note],
           "comparanda_eligible_catalogue_window": len(elig), "comparanda_with_stated_depth": len(with_d),
           "comparanda_without_stated_depth": len(elig) - len(with_d),
           "comparanda_rows": [{"id": r["id"], "depth_m": float(r["depth_m"]), "datum": r["depth_datum"],
                                "text": r["depth_text"]} for r in with_d]}

    def comp_set(sel):
        vals = [float(r["depth_m"]) for r in sel]
        if len(vals) < 5:
            return {"n": len(vals), "note": "too few stated depths to describe",
                    "rows": [r["id"] for r in sel]}
        return describe(vals)

    sets = {
        "all": with_d,
        "main_window": [r for r in with_d if C.in_window(r, C.WINDOW_MAIN)],
        "surface_and_floor_only": [r for r in with_d if r["depth_datum"] in ("present_surface", "ancient_floor")],
    }
    for dt in DEPTH_DATUMS:
        sets[f"datum_{dt}"] = [r for r in with_d if r["depth_datum"] == dt]
    out["comparanda"] = {k: comp_set(v) for k, v in sets.items()}
    comp_vals = [float(r["depth_m"]) for r in with_d]
    out["scroll"] = {}
    for variant, keep in (("all_phrases", lambda d: True), ("without_restored_or_corrupt", lambda d: not d[3])):
        for bname, cub in cubits.items():
            sv = [n * cub for d in digs if keep(d) for n in [d[1]]]
            desc = describe(sv)
            if comp_vals:
                desc["share_scroll_deeper_than_comparanda_max"] = round(sum(1 for x in sv if x > max(comp_vals)) / len(sv), 3)
                desc["share_comparanda_shallower_than_scroll_min"] = round(
                    sum(1 for x in comp_vals if x < min(sv)) / len(comp_vals), 3)
            out["scroll"][f"{variant}:{bname}"] = desc
    return out


# ---------------------------------------------------------------- PLAN 10: landmarks
def scroll_entry_texts(scroll):
    tr = json.load(open(TRANSLATION, encoding="utf-8"))
    keys = list(tr)
    pos = {k: i for i, k in enumerate(keys)}
    out = {}
    for r in scroll:
        m = re.match(r"([IVX]+):(\d+)(?:\s*[–-]\s*([IVX]+):(\d+))?$", r["col_line"].strip())
        a = f"{m.group(1)} {m.group(2)}"
        b = f"{m.group(3)} {m.group(4)}" if m.group(3) else a
        txt = " ".join(tr[k] for k in keys[pos[a]:pos[b] + 1])
        out[r["entry"]] = re.sub(r"\{\{([^|}]*)\|[^}]*\}\}", r"\1", txt)
    return out


def scroll_landmarks(text, strict=False):
    hits = []
    for cls, rx in SCROLL_RE.items():
        if cls == "threshold" and strict:
            rx = SCROLL_THRESHOLD_STRICT
        if re.search(rx, text, re.I):
            hits.append(cls)
    return hits


def tally(items, n):
    """items: list of (id, [classes]); n: denominator."""
    out = {"n": n, "any": sum(1 for _, c in items if c)}
    out["share_any"] = round(out["any"] / n, 3) if n else None
    for cls in LANDMARK_CLASSES:
        out[cls] = sum(1 for _, c in items if cls in c)
    out["hits"] = {i: c for i, c in items if c}
    return out


def landmark_comparison(rows, scroll):
    res = {"scroll": {}, "comparanda": {}}
    texts = scroll_entry_texts(scroll)
    for variant, strict in (("main", False), ("strict", True)):
        res["scroll"][f"primary_deposit:{variant}"] = tally(
            [(r["entry"], scroll_landmarks(r["primary_deposit"], strict)) for r in scroll], len(scroll))
        res["scroll"][f"translation:{variant}"] = tally(
            [(r["entry"], scroll_landmarks(texts[r["entry"]], strict)) for r in scroll], len(scroll))

    def comp(units, strict):
        items = []
        for u in units:
            v = landmark_strict(u) if strict else u["landmark"]
            items.append((u["id"], [x for x in v.split(";") if x in LANDMARK_CLASSES]))
        return items

    sets = {
        "a_all_units_main": C.comparanda_units(rows),
        "b_known_context_main": [u for u in C.comparanda_units(rows) if C.coarse_group(u["setting"])],
        "c_all_units_catalogue_window": C.comparanda_units(rows, window=WINDOW_CAT),
        "c_known_context_catalogue_window": [u for u in C.comparanda_units(rows, window=WINDOW_CAT)
                                             if C.coarse_group(u["setting"])],
    }
    for k, units in sets.items():
        for variant, strict in (("main", False), ("strict", True)):
            res["comparanda"][f"{k}:{variant}"] = tally(comp(units, strict), len(units))
    return res


# ---------------------------------------------------------------- catalogue summary
def count(rows, key, order=None):
    d = {}
    for r in rows:
        d[r[key]] = d.get(r[key], 0) + 1
    if order:
        return {k: d.get(k, 0) for k in order if d.get(k, 0)} | {k: v for k, v in sorted(d.items()) if k not in order}
    return dict(sorted(d.items()))


def catalogue_summary(rows):
    elig = [r for r in rows if r["include"] == "1"]
    reg = [r for r in elig if C.in_region_main(r)]
    cat = [r for r in reg if C.in_window(r, WINDOW_CAT)]
    main = [r for r in reg if C.in_window(r, C.WINDOW_MAIN)]
    return {
        "rows": len(rows), "excluded_by_definition": len(rows) - len(elig), "eligible": len(elig),
        "eligible_in_region": len(reg), "eligible_in_catalogue_window": len(cat),
        "eligible_in_main_window": len(main),
        "catalogue_window_by_origin": count(cat, "origin", ORIGINS),
        "catalogue_window_by_object_class": count(cat, "object_class", OBJECT_CLASSES),
        "catalogue_window_by_how_found": count(cat, "how_found", C.HOW_FOUND),
        "catalogue_window_by_window_status": count(cat, "window_status", ["inside", "partial", "outside"]),
        "catalogue_window_by_setting": count(cat, "setting", C.SETTINGS),
        "catalogue_window_known_context": sum(1 for r in cat if r["setting"] != "unknown"),
        "catalogue_window_with_stated_depth": sum(1 for r in cat if r["depth_m"] != ""),
        "temple_related": sum(1 for r in cat if r["temple_related"] == "1"),
        "recoded_precedent_rows": [r["id"] for r in rows if r["recode_reason"]],
        "unexposed_at_freeze_rows": [r["id"] for r in rows if r["unexposed_at_freeze"] == "1"],
        "new_rows": [r["id"] for r in rows if r["origin"] == "new"],
        "excluded": [{"id": r["id"], "reason": r["exclusion_reason"]} for r in rows if r["include"] != "1"],
        "eligible_outside_catalogue_window": [r["id"] for r in reg if not C.in_window(r, WINDOW_CAT)],
    }


def delta(runs):
    with open(PREC_RESULTS, "rb") as f:
        b = f.read()
    if hashlib.sha256(b).hexdigest() != PREC_RESULTS_SHA256:
        raise SystemExit("precedent results.json changed")
    prec = json.loads(b.decode("utf-8"))["runs"]["main"]
    here = runs["main"]
    return {"precedent": {"counts_comparanda": prec["counts_b"], "n_known": prec["n_b"],
                          "n_unknown": prec["n_comparanda_unknown"], "D": prec["D"], "p": prec["p"],
                          "verdict": prec["verdict"]},
            "here": {"counts_comparanda": here["counts_b"], "n_known": here["n_b"],
                     "n_unknown": here["n_comparanda_unknown"], "D": here["D"], "p": here["p"],
                     "verdict": here["verdict"]},
            "change_by_group": {g: here["counts_b"].get(g, 0) - prec["counts_b"].get(g, 0)
                                for g in C.COARSE_ORDER}}


def analyse():
    rows = derive(read_csv(os.path.join(HERE, "hoards.csv")))
    validate(rows)
    scroll = read_csv(os.path.join(PREC_DIR, "scroll_contexts.csv"))
    runs = {}
    for key, label, opts in C.RUNS:
        r = C.run_one(rows, scroll, opts)
        r["label"] = label
        runs[key] = r
    bias = C.bias_checks(rows, scroll)
    summary = precedent_summary(runs, bias)
    main_units = C.comparanda_units(rows)
    new_in_main = [u["id"] for u in main_units if u["origin"] != "precedent"]
    return {
        "plan_sha256": PLAN_SHA256,
        "frozen_inputs": {os.path.relpath(p, REPO): h for p, h in FROZEN.items()},
        "settings": {"seed": C.SEED, "n_perm": C.N_PERM, "n_boot": C.N_BOOT, "alpha": C.ALPHA,
                     "D_threshold": C.D_THRESHOLD, "min_known_comparanda": C.MIN_KNOWN,
                     "window_main": list(C.WINDOW_MAIN), "window_sens": list(C.WINDOW_SENS),
                     "window_catalogue": list(WINDOW_CAT)},
        "catalogue": catalogue_summary(rows),
        "runs": runs,
        "bias": bias,
        "summary": summary,
        "extra_runs": run_set(rows, scroll, EXTRA_RUNS),
        "exploratory_runs": run_set(rows, scroll, EXPLORATORY_RUNS),
        "delta_vs_precedent": delta(runs) | {"new_units_in_main_run": new_in_main},
        "depth": depth_comparison(rows),
        "landmark": landmark_comparison(rows, scroll),
    }


# ---------------------------------------------------------------- report
def fmt_counts(res, order, labels):
    return [f"| {c} {labels[c]} | {res['counts_a'][c]} | {res['counts_b'][c]} |" for c in order if c in res["counts_a"]]


def run_rows(runs):
    L = ["| run | scroll n | comparanda n (known) | comparanda unknown | chi2 | p | D | D 95% CI | verdict |",
         "|---|---|---|---|---|---|---|---|---|"]
    for k, r in runs.items():
        ci = f"{r['D_ci95'][0]}-{r['D_ci95'][1]}" if r["D_ci95"] else "-"
        L.append(f"| {k} | {r['n_a']} | {r['n_b']} | {r['n_comparanda_unknown']} | {r['chi2']} | {r['p']} | "
                 f"{r['D']} | {ci} | {r['verdict']} |")
    return L


def report(res):
    s = res["summary"]
    cat = res["catalogue"]
    d = res["delta_vs_precedent"]
    L = ["# Hidden deposits, 200 BCE to 135 CE: results", "",
         "Generated by `hoards_full.py run`. Plan: PLAN.md, SHA-256 `" + res["plan_sha256"] + "`.",
         "Labels: every count is INFERENCE (my coding of reported contexts); the reported contexts are EVIDENCE.", "",
         f"Main verdict (precedent rules, fuller catalogue): **{s['main_verdict']}**. Precedent: "
         f"**{d['precedent']['verdict']}** (D = {d['precedent']['D']}). Here: D = {d['here']['D']}, p = {d['here']['p']}.",
         f"Robust across the precedent's one-factor runs: **{'yes' if s['robust'] else 'no'}**"
         + (f" (changed by: {', '.join(s['runs_changing_verdict'])})" if s["runs_changing_verdict"] else "") + ".",
         f"Reporting-sensitive (precedent PLAN 12): **{'yes' if s['reporting_sensitive'] else 'no'}**.", "",
         "## Catalogue", "",
         f"- Rows: {cat['rows']}; excluded by definition: {cat['excluded_by_definition']}; eligible: {cat['eligible']}.",
         f"- Eligible in region: {cat['eligible_in_region']}; in the catalogue window (200 BCE-135 CE): "
         f"{cat['eligible_in_catalogue_window']}; in the main window (150 BCE-135 CE): {cat['eligible_in_main_window']}.",
         f"- Catalogue window, by origin: {cat['catalogue_window_by_origin']}.",
         f"- By object class: {cat['catalogue_window_by_object_class']}.",
         f"- By how found: {cat['catalogue_window_by_how_found']}.",
         f"- By setting: {cat['catalogue_window_by_setting']}; known context: {cat['catalogue_window_known_context']}.",
         f"- With a stated depth: {cat['catalogue_window_with_stated_depth']}. Temple-related by a source read: {cat['temple_related']}.",
         f"- Recoded precedent rows: {', '.join(cat['recoded_precedent_rows']) or 'none'}. "
         f"Rows unexposed at freeze: {', '.join(cat['unexposed_at_freeze_rows']) or 'none'}.",
         f"- New rows ({len(cat['new_rows'])}): {', '.join(cat['new_rows'])}.", "",
         "## Precedent runs on the fuller catalogue", ""]
    L += run_rows(res["runs"])
    L += ["", "## Main run: counts by coarse group, with the change from the precedent", "",
          "| group | scroll | comparanda here | precedent | change |", "|---|---|---|---|---|"]
    m = res["runs"]["main"]
    for g in C.COARSE_ORDER:
        if g in m["counts_a"]:
            L.append(f"| {g} {C.COARSE_LABELS[g]} | {m['counts_a'][g]} | {m['counts_b'][g]} | "
                     f"{d['precedent']['counts_comparanda'].get(g, 0)} | {d['change_by_group'][g]:+d} |")
    L += ["", f"Known-context comparanda units: {d['here']['n_known']} (precedent {d['precedent']['n_known']}); "
          f"unknown: {d['here']['n_unknown']} (precedent {d['precedent']['n_unknown']}).",
          f"Units not in the precedent that enter the main run: {', '.join(d['new_units_in_main_run']) or 'none'}.", "",
          "Adjusted standardised residuals, scroll row:", "", "| group | residual |", "|---|---|"]
    for c, v in m["residuals_a"].items():
        L.append(f"| {c} {C.COARSE_LABELS[c]} | {v} |")
    L += ["", "## Fine categories (run s9)", "", "| category | scroll | comparanda |", "|---|---|---|"]
    L += fmt_counts(res["runs"]["s9_fine"], C.FINE_ORDER, C.FINE_LABELS)
    b = res["bias"]
    L += ["", "## Reporting-bias check", "", "| check | group a n | group b n | p | D | verdict |", "|---|---|---|---|---|---|"]
    for k in ("B1_excavated_vs_not", "B2a_scroll_vs_excavated", "B2b_scroll_vs_not_excavated"):
        r = b[k]
        L.append(f"| {k} | {r['n_a']} | {r['n_b']} | {r['p']} | {r['D']} | {r['verdict']} |")
    L += ["", "| how found | units | unknown context | share |", "|---|---|---|---|"]
    for h, v in b["B3_unknown_share_by_how_found"].items():
        L.append(f"| {h} | {v['units']} | {v['unknown_context']} | {v['share_unknown']} |")
    L += ["", "## Additional runs fixed in PLAN 11 (not part of the robustness rule)", ""]
    L += run_rows(res["extra_runs"])
    L += ["", "## Exploratory runs (chosen after coding; they test nothing)", ""]
    L += run_rows(res["exploratory_runs"])
    dep = res["depth"]
    L += ["", "## Depths (PLAN 9; descriptive, no verdict)", "",
          f"Comparanda eligible in the catalogue window and region: {dep['comparanda_eligible_catalogue_window']}; "
          f"with a stated depth: {dep['comparanda_with_stated_depth']}; without: {dep['comparanda_without_stated_depth']}.", "",
          "| row | depth m | datum | wording |", "|---|---|---|---|"]
    for r in dep["comparanda_rows"]:
        L.append(f"| {r['id']} | {r['depth_m']} | {r['datum']} | {r['text']} |")
    L += ["", "| set | n | min | q1 | median | q3 | max | >0.5 m | >1 m | >2 m | >3 m | note |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def drow(name, x):
        if "note" in x:
            return f"| {name} | {x['n']} | | | | | | | | | | {x['note']}: {', '.join(x['rows'])} |"
        return (f"| {name} | {x['n']} | {x.get('min', '')} | {x.get('q1', '')} | {x.get('median', '')} | {x.get('q3', '')} | "
                f"{x.get('max', '')} | {x.get('share_deeper_than_0.5m', '')} | {x.get('share_deeper_than_1m', '')} | "
                f"{x.get('share_deeper_than_2m', '')} | {x.get('share_deeper_than_3m', '')} | |")
    for k, x in dep["comparanda"].items():
        L.append(drow("comparanda " + k, x))
    for k, x in dep["scroll"].items():
        L.append(drow("scroll " + k, x))
    L += ["", "Share of scroll depths deeper than the deepest stated comparandum, and share of comparanda shallower "
          "than the scroll's shallowest depth:", "", "| scroll set : cubit | scroll > comparanda max | comparanda < scroll min |",
          "|---|---|---|"]
    for k, x in dep["scroll"].items():
        L.append(f"| {k} | {x.get('share_scroll_deeper_than_comparanda_max')} | {x.get('share_comparanda_shallower_than_scroll_min')} |")
    lm = res["landmark"]
    L += ["", "## Placement relative to a named landmark (PLAN 10; descriptive, no verdict)", "",
          "| set | n | any | share | corner | step | pillar | threshold | gate | wall face |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for side in ("scroll", "comparanda"):
        for k, x in lm[side].items():
            L.append(f"| {side} {k} | {x['n']} | {x['any']} | {x['share_any']} | {x['corner']} | {x['step']} | "
                     f"{x['pillar']} | {x['threshold']} | {x['gate']} | {x['wall_face']} |")
    L += ["", "Hits, scroll (primary_deposit, main): " + "; ".join(
        f"{e} {'/'.join(c)}" for e, c in lm["scroll"]["primary_deposit:main"]["hits"].items()) + ".",
          "", "Hits, comparanda (catalogue window, all units, main): " + "; ".join(
        f"{i} {'/'.join(c)}" for i, c in lm["comparanda"]["c_all_units_catalogue_window:main"]["hits"].items()) + ".", ""]
    L += ["## Excluded rows", ""]
    for e in cat["excluded"]:
        L.append(f"- {e['id']}: {e['reason']}")
    L += ["", "Eligible but outside the catalogue window: " + (", ".join(cat["eligible_outside_catalogue_window"]) or "none") + ".", ""]
    return "\n".join(L) + "\n"


def results_bytes(res):
    return (json.dumps(res, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "check"
    check_frozen()
    if cmd == "build":
        b = built_bytes()
        with open(os.path.join(HERE, "hoards.csv"), "wb") as f:
            f.write(b)
        print("built")
    elif cmd == "run":
        res = analyse()
        with open(os.path.join(HERE, "results.json"), "wb") as f:
            f.write(results_bytes(res))
        with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as f:
            f.write(report(res))
        print(json.dumps(res["summary"]))
    elif cmd == "check":
        with open(os.path.join(HERE, "hoards.csv"), "rb") as f:
            if f.read() != built_bytes():
                raise SystemExit("hoards.csv derived columns are stale; run build")
        res = analyse()
        with open(os.path.join(HERE, "results.json"), "rb") as f:
            if f.read() != results_bytes(res):
                raise SystemExit("results.json differs from a fresh run")
        with open(os.path.join(HERE, "RESULTS.md"), "r", encoding="utf-8") as f:
            if f.read() != report(res):
                raise SystemExit("RESULTS.md differs from a fresh run")
        print("ok")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
