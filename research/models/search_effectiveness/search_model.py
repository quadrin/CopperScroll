#!/usr/bin/env python3
"""Search-effectiveness layer over the W2B joint placement model (K2 default).

The W2B model (joint_model_v1.py) is imported by path and never edited. This layer turns
"someone looked here and recorded nothing" into a likelihood factor on an entry's place states:

    pd = coverage * p_recognise * p_report * p_survive        (any null -> no factor)
    factor = 1 - pd                                           (silent or explicit_absence rows)

Rows of one field lineage count once (largest pd). Lineages multiply. A target (entry, place,
relation) with a reported row that fully satisfies the requirement takes no silence factor.
Factors multiply the model's tempered likelihood rows through `Model.run(L_override=...)`.
With every factor equal to 1 the W2B outputs are reproduced exactly (see tests).

Run with python3 -I. The W2B model needs numpy; this file uses numpy only for the vectors it
passes to that model.
"""
import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
W2B = REPO / "research" / "agent_review_2026-10-07" / "wave2" / "W2B_model_v1"
MODEL_PATH = W2B / "scripts" / "joint_model_v1.py"
INPUTS = W2B / "inputs"
LOOKS = HERE / "looks.csv"
NEXT = HERE / "next_records.csv"
PLAN = HERE / "PLAN.md"

NUM_FIELDS = ("coverage", "p_recognise", "p_report", "p_survive")
RESULTS = ("reported", "silent", "explicit_absence")
NEGATIVE = ("silent", "explicit_absence")
SATISFIES = ("yes", "partly", "no", "unknown", "")


# ----------------------------------------------------------------------------- loading
def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_jm(path=MODEL_PATH):
    """Import the W2B model module by path (read-only use)."""
    spec = importlib.util.spec_from_file_location("w2b_joint_model_v1", str(path))
    mod = importlib.util.module_from_spec(spec)
    keep = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # leave no cache in the W2B folder
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


def load_plan(path=PLAN):
    """Return the frozen JSON parameter block of PLAN.md."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not m:
        raise ValueError("PLAN.md has no ```json block")
    return json.loads(m.group(1))


def _num(v):
    v = (v or "").strip()
    if v == "" or v.lower() in ("null", "none", "na"):
        return None
    x = float(v)
    if not 0.0 <= x <= 1.0:
        raise ValueError(f"probability out of range: {v}")
    return x


def load_looks(path=LOOKS):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for f in NUM_FIELDS:
            r[f] = _num(r.get(f))
        r["placement_relevant"] = (r.get("placement_relevant") or "yes").strip()
    return rows


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_looks(rows, entries, states):
    """Raise ValueError on a malformed looks table. `entries` and `states` are sets of ids."""
    seen = set()
    errs = []
    for r in rows:
        lid = r.get("look_id", "")
        if lid in seen:
            errs.append(f"{lid}: duplicate look_id")
        seen.add(lid)
        if r["entry_id"] not in entries:
            errs.append(f"{lid}: unknown entry {r['entry_id']}")
        if r["place_id"] not in states:
            errs.append(f"{lid}: unknown place state {r['place_id']}")
        if r["result"] not in RESULTS:
            errs.append(f"{lid}: bad result {r['result']}")
        if r.get("satisfies_requirement", "") not in SATISFIES:
            errs.append(f"{lid}: bad satisfies_requirement")
        if r["placement_relevant"] not in ("yes", "no"):
            errs.append(f"{lid}: bad placement_relevant")
        if not r.get("record", "").strip():
            errs.append(f"{lid}: record citation missing")
        if not r.get("relation_id", "").strip():
            errs.append(f"{lid}: relation_id missing")
        for f in NUM_FIELDS:
            basis = (r.get(f + "_basis") or "").strip()
            if r[f] is not None and not basis.startswith(("EVIDENCE", "INFERENCE")):
                errs.append(f"{lid}: {f} has a number but no EVIDENCE/INFERENCE basis")
            if r[f] is None and basis and not basis.startswith(("UNKNOWN", "EVIDENCE", "INFERENCE")):
                errs.append(f"{lid}: {f} is null and its basis has no UNKNOWN/EVIDENCE/INFERENCE label")
        for cond in filter(None, (r.get("reading_condition") or "").split(";")):
            if "=" not in cond:
                errs.append(f"{lid}: bad reading_condition {cond}")
    if errs:
        raise ValueError("; ".join(errs))


# ----------------------------------------------------------------------------- the likelihood
def condition_ok(cond, readings):
    for c in filter(None, (cond or "").split(";")):
        k, v = c.split("=", 1)
        if readings.get(k.strip()) != v.strip():
            return False
    return True


def row_pd(row, scenario):
    """Detection probability of one row under a scenario, or None when any factor is unknown."""
    if row["result"] not in NEGATIVE or row["placement_relevant"] != "yes":
        return None
    if scenario.get("zero"):
        return 0.0
    vals = {f: row[f] for f in NUM_FIELDS}
    for f, cap in (scenario.get("caps") or {}).items():
        if row["result"] in cap["results"] and vals[f] is not None:
            vals[f] = min(vals[f], float(cap["value"]))
    if any(v is None for v in vals.values()):
        return None
    pd = 1.0
    for f in NUM_FIELDS:
        pd *= vals[f]
    return pd


def target_key(row):
    return (row["entry_id"], row["place_id"], row["relation_id"])


def target_factors(rows, scenario, readings, extra=()):
    """Per (entry, place, relation) target: factor, combined pd and the rows behind it.

    `extra` holds synthetic (key, lineage, pd) looks used by the probe analysis."""
    active = [r for r in rows if r["placement_relevant"] == "yes" and condition_ok(r.get("reading_condition"), readings)]
    by = {}
    for r in active:
        by.setdefault(target_key(r), []).append(r)
    for key, _lin, _pd in extra:
        by.setdefault(key, [])
    out = {}
    for key in sorted(by):
        rs = by[key]
        dominated = any(r["result"] == "reported" and r.get("satisfies_requirement") == "yes" for r in rs)
        lin = {}
        used = []
        for r in rs:
            p = row_pd(r, scenario)
            if p is None:
                continue
            used.append(r["look_id"])
            lin[r["lineage"]] = max(lin.get(r["lineage"], 0.0), p)
        for k2, lineage, p in extra:
            if k2 == key:
                lin[lineage] = max(lin.get(lineage, 0.0), float(p))
                used.append("probe:" + lineage)
        factor = 1.0
        if not dominated:
            for lineage in sorted(lin):
                factor *= (1.0 - lin[lineage])
        out[key] = dict(factor=factor, pd=1.0 - factor, dominated=dominated,
                        rows=sorted(r["look_id"] for r in rs), used=sorted(used))
    return out


def entry_vectors(model, targets):
    """Multiply target factors into one vector per entry (states not looked at keep factor 1)."""
    vec = {}
    for (e, place, _rel), t in targets.items():
        if t["factor"] == 1.0:
            continue
        v = vec.setdefault(e, np.ones(model.S))
        v[model.idx[place]] *= t["factor"]
    return vec


# ----------------------------------------------------------------------------- running the W2B model
def tempered_likelihoods(model, order=None):
    """The likelihood matrix exactly as Model.run builds it (evidence rows, then name-group tempering)."""
    order = order or model.d.order
    ev = model.evidence(order)
    G = model.groups(order, ev)
    L = np.array([ev[e][0] for e in order])
    if G and model.c["temper"]:
        ng = {}
        for g in G:
            for p in g["pos"]:
                ng[p] = max(ng.get(p, 1), len(g["pos"]))
        for p, k in ng.items():
            L[p] = L[p] ** (1.0 / k)
    return order, L


def run(model, vectors=None, force_override=False):
    """Run the W2B model with search factors. Factors are applied after tempering and are not tempered:
    each row is a separate record about a separate required feature."""
    vectors = vectors or {}
    if not vectors and not force_override:
        return model.run()
    order, L = tempered_likelihoods(model)
    over = {}
    for i, e in enumerate(order):
        if e in vectors:
            over[e] = L[i] * vectors[e]
        elif force_override:
            over[e] = L[i] * 1.0
    return model.run(L_override=over)


def model_readings(reading_set):
    """W2B cfg readings for a reading set (other keys gate looks rows only)."""
    return dict(kohlit15=reading_set.get("kohlit15") == "yes", solomon23=True,
                xii10=reading_set.get("xii10", "milik_puech"))


def build_model(jm, data, reading_set):
    rd = model_readings(reading_set)
    default = jm.DEFAULT["readings"]
    if rd == dict(default):
        cfg = jm.cfg_with()
    else:
        cfg = jm.cfg_with(readings=rd)
    return jm.Model(data, cfg)


def tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())
