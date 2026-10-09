#!/usr/bin/env python3
"""Run the frozen search-effectiveness analysis and write results.json.

    python3 -I research/models/search_effectiveness/run_analysis.py [--out results.json] [--tables]

The script stops if looks.csv or next_records.csv differ from the SHA-256 values frozen in PLAN.md.
"""
import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import search_model as sm  # noqa: E402

KOHLIT = ("4", "11", "15", "19", "60")
STORE_MIN = 1e-3  # states below this in every scenario are not stored in results.json


def rnd(x, nd):
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        v = round(x, nd)
        return 0.0 if v == 0 else v
    if isinstance(x, dict):
        return {str(k): rnd(v, nd) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rnd(v, nd) for v in x]
    return x


def check_frozen(plan):
    want = plan["frozen_inputs_sha256"]
    got = {"looks.csv": sm.sha256(sm.LOOKS), "next_records.csv": sm.sha256(sm.NEXT)}
    if want != got:
        raise SystemExit(f"frozen inputs changed: PLAN {want} vs files {got}")
    return got


def candidate_odds(model, cands, readings):
    """Evidence odds per (entry, place) as Model.evidence weights candidate rows (default scheme;
    readings use the model's own condition syntax)."""
    c = model.c
    out = {}
    for r in cands:
        cond = r.get("conditional_on_reading", "")
        if not _model_cond_ok(cond, c["readings"]):
            continue
        if r.get("prior_override"):
            o = float(r["prior_override"])
        else:
            p = c["conf_p"][r["confidence"]]
            o = p / (1 - p) * c["status_mult"][r["status"]]
        out[(r["entry"], r["place_id"])] = out.get((r["entry"], r["place_id"]), 0.0) + o
    return out


def _model_cond_ok(cond, readings):
    if not cond:
        return True
    if "!=" in cond:
        k, v = cond.split("!=")
        return readings.get(k) != v
    if "=" in cond:
        k, v = cond.split("=")
        return readings.get(k) == v
    return bool(readings.get(cond, True))


def reading_set_for(cond, plan):
    """Main reading set unless the row's condition needs another one (first match in plan order)."""
    sets = plan["reading_sets"]
    main = plan["main_reading_set"]
    if sm.condition_ok(cond, sets[main]):
        return main
    for name in sorted(sets):
        if sm.condition_ok(cond, sets[name]):
            return name
    return None


def analyse(plan):
    jm = sm.load_jm()
    data = jm.Data(str(sm.INPUTS), "v1")
    looks = sm.load_looks()
    nexts = sm.load_csv(sm.NEXT)
    cands = sm.load_csv(sm.INPUTS / "candidates_v1.csv")
    nd = plan["rounding_decimals"]
    scen = plan["scenarios"]
    snames = sorted(scen)
    main = plan["main_reading_set"]

    models, posts, logml, targets = {}, {}, {}, {}
    for rname, rset in sorted(plan["reading_sets"].items()):
        m = sm.build_model(jm, data, rset)
        models[rname] = m
        sm.validate_looks(looks, set(data.order), set(m.states))
        for s in snames:
            t = sm.target_factors(looks, scen[s], rset)
            res = sm.run(m, sm.entry_vectors(m, t))
            posts[(rname, s)] = res["post"]
            logml[(rname, s)] = float(res["logml"])
            targets[(rname, s)] = t
    m0 = models[main]
    order = list(m0.d.order)
    states = list(m0.states)
    pos = {e: i for i, e in enumerate(order)}
    title = data.title

    # ------------------------------------------------------------------ per-entry posteriors and changes
    entries = {}
    for rname in sorted(plan["reading_sets"]):
        for e in order:
            i = pos[e]
            base = posts[(rname, "S4")][i]
            tvs = {s: sm.tv(posts[(rname, s)][i], base) for s in snames if s != "S4"}
            rec = entries.setdefault(e, dict(title=title[e], by_reading={}))
            item = dict(tv_vs_S4=tvs)
            changed = max(tvs.values()) > 1e-9
            keep = [k for k, st in enumerate(states)
                    if max(posts[(rname, s)][i][k] for s in snames) >= STORE_MIN]
            if rname == main and not changed:
                # every scenario equals S4 (the W2B K2 default) for this entry
                item["posterior_all_scenarios"] = {states[k]: float(base[k]) for k in keep}
            if changed and (rname == main or e in KOHLIT):
                item["posterior"] = {states[k]: {s: float(posts[(rname, s)][i][k]) for s in snames} for k in keep}
            if changed:
                d0 = posts[(rname, "S0")][i] - base
                top = sorted(range(len(states)), key=lambda k: (-abs(d0[k]), states[k]))[:8]
                item["S0_minus_S4_top"] = [dict(state=states[k], S4=float(base[k]), S0=float(posts[(rname, 'S0')][i][k]),
                                                delta=float(d0[k])) for k in top]
                item["region_S0_minus_S4"] = {r: float(v) for r, v in sorted(
                    {r: models[rname].region_probs(posts[(rname, "S0")][i])[r] - models[rname].region_probs(base)[r]
                     for r in models[rname].region_probs(base)}.items())}
            rec["by_reading"][rname] = item

    # ------------------------------------------------------------------ drivers: leave one target out (S0)
    drivers = {}
    for rname, rset in sorted(plan["reading_sets"].items()):
        m = models[rname]
        t0 = targets[(rname, "S0")]
        for key, t in sorted(t0.items()):
            if t["factor"] == 1.0:
                continue
            rest = {k: v for k, v in t0.items() if k != key}
            res = sm.run(m, sm.entry_vectors(m, rest))
            eff = {e: sm.tv(posts[(rname, "S0")][pos[e]], res["post"][pos[e]]) for e in order}
            top = sorted(((v, e) for e, v in eff.items() if v > 1e-9), key=lambda x: (-x[0], x[1]))[:10]
            drivers.setdefault(rname, []).append(dict(
                entry=key[0], place=key[1], relation=key[2], factor=t["factor"], rows=t["used"],
                effect_tv_by_entry={e: v for v, e in top}))

    # ------------------------------------------------------------------ factors table (all reading sets, scenarios)
    factors = []
    for (rname, s), tt in sorted(targets.items()):
        for key, t in sorted(tt.items()):
            if t["factor"] != 1.0 or t["dominated"]:
                factors.append(dict(reading_set=rname, scenario=s, entry=key[0], place=key[1], relation=key[2],
                                    factor=t["factor"], pd=t["pd"], dominated=t["dominated"], rows=t["used"]))

    # ------------------------------------------------------------------ unsearched mass per region (main, S0)
    thr = plan["unsearched_pd_threshold"]
    t0 = targets[(main, "S0")]
    vec0 = sm.entry_vectors(m0, t0)
    reported_states = {}
    for r in looks:
        if r["result"] == "reported" and r["placement_relevant"] == "yes" and \
                sm.condition_ok(r.get("reading_condition"), plan["reading_sets"][main]) and \
                r.get("satisfies_requirement") in ("yes", "partly"):
            reported_states.setdefault(r["entry_id"], set()).add(r["place_id"])
    unsearched = {}
    agg = {}
    for e in order:
        p = posts[(main, "S0")][pos[e]]
        v = vec0.get(e)
        per = {}
        for k, st in enumerate(states):
            reg = m0.region_of[st]
            pdc = 0.0 if v is None else 1.0 - float(v[k])
            a = per.setdefault(reg, dict(mass=0.0, unsearched=0.0, searched=0.0, with_reported_feature=0.0))
            a["mass"] += float(p[k])
            if pdc < thr:
                a["unsearched"] += float(p[k])
            else:
                a["searched"] += float(p[k])
            if st in reported_states.get(e, ()):
                a["with_reported_feature"] += float(p[k])
        unsearched[e] = per
        for reg, a in per.items():
            g = agg.setdefault(reg, dict(mass=0.0, unsearched=0.0, searched=0.0, with_reported_feature=0.0))
            for k2 in g:
                g[k2] += a[k2] / len(order)
    searched_states = sorted({(k[0], k[1]) for k, t in t0.items() if t["pd"] >= thr})

    # ------------------------------------------------------------------ phantom coverage
    phantom = []
    for r in looks:
        if r["result"] not in sm.NEGATIVE or not r.get("project_use", "").strip():
            continue
        rname = reading_set_for(r.get("reading_condition"), plan) or main
        pd_row = sm.row_pd(r, scen["S0"]) if r["placement_relevant"] == "yes" else None
        tgt = targets[(rname, "S0")].get(sm.target_key(r))
        pd_t = tgt["pd"] if (tgt and r["placement_relevant"] == "yes") else None
        if pd_row is not None and pd_row >= plan["phantom_pd_threshold"]:
            continue
        nulls = [f for f in sm.NUM_FIELDS if r[f] is None]
        zeros = [f for f in sm.NUM_FIELDS if r[f] == 0.0]
        phantom.append(dict(look_id=r["look_id"], entry=r["entry_id"], place=r["place_id"], relation=r["relation_id"],
                            record=r["record"], result=r["result"], pd_row=pd_row, pd_target=pd_t,
                            null_fields=nulls, zero_fields=zeros, placement_relevant=r["placement_relevant"],
                            project_use=r["project_use"], reading_set=rname))

    # ------------------------------------------------------------------ double counting against candidates_v1
    odds_by_set = {rn: candidate_odds(models[rn], cands, models[rn].c["readings"]) for rn in models}
    via_target = {}
    for r in looks:
        if r["result"] == "reported" and r.get("counted_via", "").strip():
            via_target.setdefault(sm.target_key(r), []).append(r["look_id"])
    srcs = {}
    for c in cands:
        srcs.setdefault((c["entry"], c["place_id"]), []).append(c["source"])
    dc = []
    for r in looks:
        key = (r["entry_id"], r["place_id"])
        has = key in srcs
        if r["result"] == "reported":
            auto = has and any(r["record_key"].lower() in s.lower() for s in srcs[key] if r["record_key"])
            if auto:
                status = "counted: candidates_v1 source cites this record"
            elif r.get("counted_via", "").strip() and has:
                status = "counted via the proposal: the proposer used this feature"
            elif has and sm.target_key(r) in via_target:
                status = ("counted via the proposal (same target): the proposer used this feature class here; "
                          "see " + ", ".join(via_target[sm.target_key(r)]))
            elif has:
                status = "not counted: candidate row exists; its source does not use this record"
            else:
                status = "no candidate row: positive evidence unused by the model"
            dc.append(dict(look_id=r["look_id"], entry=r["entry_id"], place=r["place_id"], record=r["record"],
                           satisfies=r.get("satisfies_requirement", ""), candidate_row=has, status=status,
                           counted_via=r.get("counted_via", ""), factor_added=1.0))
        else:
            odds = odds_by_set[reading_set_for(r.get("reading_condition"), plan) or main]
            if not has:
                status = "no candidate row"
            else:
                peers = sorted(v for (e2, _p), v in odds.items() if e2 == r["entry_id"])
                mine = odds.get(key)
                same = sum(1 for v in peers if mine is not None and abs(v - mine) < 1e-12)
                status = (f"odds not lowered for this look: {mine:.4f}, shared by {same} of {len(peers)} "
                          f"candidates of entry {r['entry_id']}" if mine is not None else "candidate inactive in this reading")
            dc.append(dict(look_id=r["look_id"], entry=r["entry_id"], place=r["place_id"], record=r["record"],
                           satisfies="", candidate_row=has, status=status, counted_via="", factor_added=None))

    # ------------------------------------------------------------------ probes: one more record, silent
    probes = []
    access_rank = {a: i for i, a in enumerate(plan["access_order"])}
    for n in nexts:
        rname = reading_set_for(n.get("reading_condition"), plan)
        m = models[rname]
        rset = plan["reading_sets"][rname]
        i = pos[n["entry_id"]]
        k = m.idx[n["place_id"]]
        base = posts[(rname, "S0")]
        key = (n["entry_id"], n["place_id"], n["relation_id"])
        t_now = targets[(rname, "S0")].get(key)
        pd_now = t_now["pd"] if t_now else 0.0
        item = dict(probe_id=n["probe_id"], entry=n["entry_id"], place=n["place_id"], relation=n["relation_id"],
                    record=n["record"], record_id=n["record_id"], access=n["access"],
                    can_contradict=n["can_contradict"], reading_set=rname, pd_now=pd_now,
                    dominated_now=bool(t_now and t_now["dominated"]), P_now=float(base[i][k]), by_pd={})
        for pdv in plan["probe_pd"]:
            t = sm.target_factors(looks, scen["S0"], rset, extra=[(key, "probe", pdv)])
            res = sm.run(m, sm.entry_vectors(m, t))
            post = res["post"]
            other = sorted(((sm.tv(post[j], base[j]), order[j]) for j in range(len(order)) if j != i),
                           key=lambda x: (-x[0], x[1]))[:3]
            item["by_pd"][str(pdv)] = dict(P_after=float(post[i][k]), delta_P=float(post[i][k] - base[i][k]),
                                           tv_entry=sm.tv(post[i], base[i]), delta_pd=pdv - pd_now if not item["dominated_now"] else 0.0,
                                           top_other_entries=[dict(entry=e2, tv=v) for v, e2 in other])
        probes.append(item)
    p0 = str(plan["probe_pd"][0])
    probes.sort(key=lambda x: (access_rank.get(x["access"], 99), -abs(x["by_pd"][p0]["delta_P"]), x["probe_id"]))

    # ------------------------------------------------------------------ summary of the table
    from collections import Counter
    act = [r for r in looks if r["placement_relevant"] == "yes"]
    num_rows = [r["look_id"] for r in looks if r["result"] in sm.NEGATIVE and sm.row_pd(r, scen["S0"]) is not None]
    summary = dict(rows=len(looks), by_result=dict(Counter(r["result"] for r in looks)),
                   placement_rows=len(act), entries=sorted({r["entry_id"] for r in looks}, key=lambda x: pos[x]),
                   places=sorted({r["place_id"] for r in looks}),
                   negative_rows_with_numeric_pd_S0=num_rows,
                   negative_rows=sum(1 for r in looks if r["result"] in sm.NEGATIVE),
                   entries_without_rows=[e for e in order if e not in {r["entry_id"] for r in looks}])

    meta = dict(plan_sha256=sm.sha256(sm.PLAN), frozen=check_frozen(plan),
                model_code_sha256=sm.sha256(sm.MODEL_PATH),
                model_inputs_sha256={p.name: sm.sha256(p) for p in sorted(sm.INPUTS.glob("*_v1.csv"))},
                search_model_sha256=sm.sha256(HERE / "search_model.py"),
                model_cfg="joint_model_v1.cfg_with() defaults: transition 'fixed' (K2), kohlit_scheme None, "
                          "rho 0.9, w_A 0.4, w_L 0.995; readings per reading set",
                states=len(states), entries=len(order),
                logml={f"{r}/{s}": v for (r, s), v in sorted(logml.items())})
    meta["stored_posterior_min"] = STORE_MIN
    out = dict(meta=meta, plan=plan, looks_summary=summary, factors=factors, entries=entries, drivers=drivers,
               unsearched_mass=dict(threshold=thr, reading_set=main, scenario="S0", all_entries_mean=agg,
                                    by_entry={e: unsearched[e] for e in order},
                                    states_with_pd_at_or_above_threshold=[list(x) for x in searched_states]),
               phantom_coverage=phantom, double_counting=dc, probes=probes)
    return rnd(out, nd)


def tables(res):
    """Markdown tables for the README (printed, not written)."""
    lines = []
    main = res["plan"]["main_reading_set"]
    lines.append("### Factors below 1\n")
    lines.append("| Reading set | Scenario | Entry | Place | Factor | Rows |")
    lines.append("|---|---|---|---|---|---|")
    for f in res["factors"]:
        if f["factor"] < 1:
            lines.append(f"| {f['reading_set']} | {f['scenario']} | {f['entry']} | {f['place']} | {f['factor']:.3f} | {', '.join(f['rows'])} |")
    lines.append("\n### Entries that change (TV distance from S4)\n")
    for rname in sorted(res["plan"]["reading_sets"]):
        lines.append(f"\nReading set {rname}:\n")
        lines.append("| Entry | Title | S0 | S1 | S2 | S3 |")
        lines.append("|---|---|---|---|---|---|")
        for e, rec in res["entries"].items():
            it = rec["by_reading"][rname]
            t = it["tv_vs_S4"]
            if max(t.values()) >= 1e-4:
                lines.append(f"| {e} | {rec['title']} | {t['S0']:.4f} | {t['S1']:.4f} | {t['S2']:.4f} | {t['S3']:.4f} |")
    lines.append(f"\n### Largest place changes, {main} S0 minus S4\n")
    lines.append("| Entry | State | S4 | S0 | S0 - S4 |")
    lines.append("|---|---|---|---|---|")
    for e, rec in res["entries"].items():
        it = rec["by_reading"][main]
        for row in it.get("S0_minus_S4_top", [])[:4]:
            if abs(row["delta"]) >= 1e-3:
                lines.append(f"| {e} | {row['state']} | {row['S4']:.4f} | {row['S0']:.4f} | {row['delta']:+.4f} |")
    lines.append("\n### Unsearched mass (pd < 0.2), mean over all entries, main reading set, S0\n")
    lines.append("| Region | Mass | Unsearched | Searched | On states with a reported feature |")
    lines.append("|---|---|---|---|---|")
    for reg, a in sorted(res["unsearched_mass"]["all_entries_mean"].items()):
        lines.append(f"| {reg} | {a['mass']:.4f} | {a['unsearched']:.4f} | {a['searched']:.4f} | {a['with_reported_feature']:.4f} |")
    lines.append("\n### Unsearched mass, Kohlit entries (main reading set, S0)\n")
    lines.append("| Entry | Total searched mass | Unsearched in JERICHO | Unsearched in SAMDES | Unsearched in QUMRAN |")
    lines.append("|---|---|---|---|---|")
    for e in ("4", "11", "15", "19", "60"):
        per = res["unsearched_mass"]["by_entry"][e]
        s = sum(a["searched"] for a in per.values())
        lines.append(f"| {e} | {s:.4f} | {per['JERICHO']['unsearched']:.4f} | {per['SAMDES']['unsearched']:.4f} | {per['QUMRAN']['unsearched']:.4f} |")
    lines.append("\n### Phantom coverage\n")
    lines.append("| Look | Entry | Place | Record | pd (S0) | Null fields | Zero fields |")
    lines.append("|---|---|---|---|---|---|---|")
    for p in res["phantom_coverage"]:
        pd = "null" if p["pd_row"] is None else f"{p['pd_row']:.2f}"
        lines.append(f"| {p['look_id']} | {p['entry']} | {p['place']} | {p['record']} | {pd} | {', '.join(p['null_fields']) or '-'} | {', '.join(p['zero_fields']) or '-'} |")
    lines.append("\n### Double counting (reported rows)\n")
    lines.append("| Look | Entry | Place | Status |")
    lines.append("|---|---|---|---|")
    for d in res["double_counting"]:
        lines.append(f"| {d['look_id']} | {d['entry']} | {d['place']} | {d['status']} |")
    lines.append("\n### Probes: one more silent record\n")
    pv = [str(x) for x in res["plan"]["probe_pd"]]
    lines.append(f"| Probe | Entry | Place | Record | Access | Can contradict | P now | dP at pd {pv[0]} | dP at pd {pv[1]} | Most moved other entry (pd {pv[1]}) |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for p in res["probes"]:
        a, b = p["by_pd"][pv[0]], p["by_pd"][pv[1]]
        oth = b["top_other_entries"][0]
        lines.append(f"| {p['probe_id']} | {p['entry']} | {p['place']} | {p['record']} | {p['access']} | {p['can_contradict']} | "
                     f"{p['P_now']:.4f} | {a['delta_P']:+.4f} | {b['delta_P']:+.4f} | {oth['entry']} (TV {oth['tv']:.4f}) |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "results.json")
    ap.add_argument("--tables", action="store_true", help="print README tables")
    a = ap.parse_args()
    plan = sm.load_plan()
    check_frozen(plan)
    res = analyse(plan)
    a.out.write_text(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    if a.tables:
        print(tables(res))
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
