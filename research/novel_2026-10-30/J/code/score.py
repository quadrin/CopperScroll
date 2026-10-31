"""Lane J confirmatory scoring: landscape date for the Copper Scroll list.

Usage: python3 score.py [--selftest]
--selftest replaces every coded interval with a random fake interval (seed 1) so the code
can be checked without looking at the real result. --planttest adds a fake 60-70 CE signal
to 30% of eligible features (power check on fake data). The confirmatory run uses no flag.
"""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

J = Path(__file__).resolve().parents[1]
SEED = 20261030
NPERM = 10000
ALPHA = 0.05
RULES = ("persist", "attested", "persist_sitefinds")

# name, evaluation year (negative = BCE), interval, boundary source key (see PROTOCOL_FROZEN.md §4)
SCENARIOS = [
    ("HAS", -88, (-140, -37), "Hasmonean rule, Simon to Herod's capture of Jerusalem"),
    ("HER", -20, (-37, -4), "reign of Herod the Great"),
    ("ERP", 36, (6, 65), "Early Roman before the revolt (Judaea a province to the revolt)"),
    ("REV1", 68, (66, 70), "First Revolt"),
    ("INT", 101, (71, 131), "between the revolts"),
    ("BK", 134, (132, 135), "Bar Kokhba revolt"),
    ("LR", 230, (136, 324), "Late Roman (legend)"),
    ("BYZ", 482, (324, 640), "Byzantine (legend)"),
]
USE_KINDS_BY_RULE = {"persist": {"feature", "other"}, "attested": {"feature", "other"},
                     "persist_sitefinds": {"feature", "other", "site", "finds"}}


def existence(start, end, eev, kind, t, rule):
    """Existence at year t, vectorised. int8: 1 yes, 0 no, -1 undated (bounds decide).
    Dated row = kind in the rule's dated kinds and a start year.
    persist / persist_sitefinds: yes if start <= t and not (end_event == yes and t > end); else no.
    attested: yes if start <= t <= end; else no.
    Row with an end year only: no if end_event == yes and t > end, else undated.
    Every other row is undated (-1)."""
    kinds = list(USE_KINDS_BY_RULE[rule])
    out = np.full(len(start), -1, np.int8)
    dated = np.isin(kind, kinds) & ~np.isnan(start)
    e_ = np.where(np.isnan(end), np.inf, end)
    if rule == "attested":
        yes = dated & (start <= t) & (t <= e_)
    else:
        yes = dated & (start <= t) & ~((eev == "yes") & (t > e_))
    out[dated] = 0
    out[yes] = 1
    only_end = np.isin(kind, kinds) & np.isnan(start) & ~np.isnan(end)
    out[only_end & (eev == "yes") & (t > e_)] = 0
    return out


def stats(exist_bool, pe, pf, nE, npairs_e):
    """S1: number of entries with >=1 eligible feature in existence.
    S2: mean over entries of the share of the entry's eligible features in existence."""
    hit = exist_bool[pf].astype(np.float64)
    k = np.bincount(pe, weights=hit, minlength=nE)
    return int((k > 0).sum()), float((k / npairs_e).mean())


def main(selftest=False, plant=False):
    f = pd.read_csv(J / "data/features_unified.csv", dtype=str)
    c = pd.read_csv(J / "period_coding/coded_intervals.csv", dtype=str)
    f = f.merge(c[["sid", "start", "end", "start_event", "end_event", "kind"]], on="sid", how="left")
    f["kind"] = f.kind.fillna("empty")
    for col in ("start_event", "end_event"):
        f[col] = f[col].fillna("no")
    f["start"] = pd.to_numeric(f.start, errors="coerce")
    f["end"] = pd.to_numeric(f.end, errors="coerce")
    if selftest:
        r = np.random.default_rng(1)
        f["start"] = r.integers(-1200, 1500, len(f)).astype(float)
        f["end"] = f.start + r.integers(10, 600, len(f))
        f["kind"] = np.where(r.random(len(f)) < 0.4, "feature", "undated")
        f["end_event"] = np.where(r.random(len(f)) < 0.1, "yes", "no")
    el = pd.read_csv(J / "data/eligibility.csv", dtype=str)
    if plant:
        # power check on fake data: features eligible for an entry get 60-70 CE, end event; all others random
        r = np.random.default_rng(2)
        f["start"] = r.integers(-1200, 1500, len(f)).astype(float)
        f["end"] = f.start + r.integers(10, 600, len(f))
        f["end_event"] = "no"
        f["kind"] = np.where(r.random(len(f)) < 0.4, "feature", "undated")
        m = f.fid.isin(el.fid) & (r.random(len(f)) < 0.3)
        f.loc[m, ["start", "end", "end_event", "kind"]] = [60.0, 70.0, "yes", "feature"]
    fid_idx = {k: i for i, k in enumerate(f.fid)}
    entries = sorted(el.entry.unique(), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    e_idx = {k: i for i, k in enumerate(entries)}
    pe = el.entry.map(e_idx).values
    pf = el.fid.map(fid_idx).values
    nE = len(entries)
    # only features eligible for at least one entry need to be scored, but permutation is over all
    # features of each stratum (class|zone), so the null draws from the regional background.
    strata = f.stratum.values
    groups = [np.where(strata == s)[0] for s in pd.unique(strata)]
    S, E, EE, K = f.start.values, f.end.values, f.end_event.values, f.kind.values
    dated_share = {}
    rng = np.random.default_rng(SEED)
    perms = np.empty((NPERM, len(f)), np.int32)
    base = np.arange(len(f))
    for p in range(NPERM):
        idx = base.copy()
        for g in groups:
            idx[g] = g[rng.permutation(len(g))]
        perms[p] = idx
    npairs_e = np.bincount(pe, minlength=nE).astype(np.float64)
    results = {}
    for rule in RULES:
        ex = {sc[0]: existence(S, E, EE, K, sc[1], rule) for sc in SCENARIOS}
        for bound in ("best", "worst"):
            o1, o2, n1, n2 = {}, {}, {}, {}
            for name, t, _, _ in SCENARIOS:
                x = ex[name]
                xb = (x == 1) | ((x == -1) & (bound == "best"))
                o1[name], o2[name] = stats(xb, pe, pf, nE, npairs_e)
                nn = np.array([stats(xb[perms[p]], pe, pf, nE, npairs_e) for p in range(NPERM)])
                n1[name], n2[name] = nn[:, 0], nn[:, 1]
            results[(rule, bound, "S1")] = (o1, n1)
            results[(rule, bound, "S2")] = (o2, n2)
            dated_share[(rule, bound)] = {name: float((ex[name][pf] != -1).mean()) for name, *_ in SCENARIOS}
    # secondary (descriptive): dated-only feature-weighted share per entry
    out_rows, summary = [], {}
    names = [s[0] for s in SCENARIOS]
    for (rule, bound, stat), (obs, null) in results.items():
        z = {}
        for n in names:
            mu, sd = null[n].mean(), null[n].std(ddof=1)
            zn = (obs[n] - mu) / sd if sd > 0 else 0.0
            zp = (null[n] - mu) / sd if sd > 0 else np.zeros(NPERM)
            z[n] = (zn, zp)
            p = (1 + int((null[n] >= obs[n]).sum())) / (1 + NPERM)
            out_rows.append(dict(stat=stat, rule=rule, bound=bound, scenario=n, eval_year=dict((s[0], s[1]) for s in SCENARIOS)[n],
                                 observed=round(obs[n], 5), null_mean=round(mu, 5), null_sd=round(sd, 5), z=round(zn, 3), p_upper=round(p, 5),
                                 n_entries_scored=nE))
        win = max(names, key=lambda n: z[n][0])
        diffs = {}
        for r_ in names:
            if r_ == win:
                continue
            d_obs = z[win][0] - z[r_][0]
            d_perm = z[win][1] - z[r_][1]
            diffs[r_] = dict(d_obs=round(float(d_obs), 3), p=round((1 + int((d_perm >= d_obs).sum())) / (1 + NPERM), 5))
        pw = [r for r in out_rows if r["stat"] == stat and r["rule"] == rule and r["bound"] == bound and r["scenario"] == win][0]["p_upper"]
        beats_null = pw <= ALPHA / len(names)
        beats_all = all(v["p"] <= ALPHA for v in diffs.values())
        summary[f"{stat}|{rule}|{bound}"] = dict(winner=win, winner_z=round(float(z[win][0]), 3), winner_p=pw,
                                           beats_null=bool(beats_null), beats_all_others=bool(beats_all), diffs=diffs)
    def passes(stat, rule="persist"):
        pr = [summary[f"{stat}|{rule}|best"], summary[f"{stat}|{rule}|worst"]]
        ok = (pr[0]["winner"] == pr[1]["winner"]) and all(x["beats_null"] and x["beats_all_others"] for x in pr)
        return ok, (pr[0]["winner"] if ok else None)
    s1_ok, s1_win = passes("S1")
    s2_ok, s2_win = passes("S2")
    outcome = "obtained" if s1_ok else ("partly" if s2_ok else "not obtained")
    res = dict(selftest=selftest, planttest=plant, seed=SEED, nperm=NPERM, alpha=ALPHA, scenarios=SCENARIOS,
               n_features=int(len(f)), n_entries_with_eligible=nE, entries=entries,
               n_pairs=int(len(el)), summary=summary,
               dated_share_of_pairs={f"{k[0]}|{k[1]}": v for k, v in dated_share.items()},
               decision=dict(primary_rule="persist", S1_passes=bool(s1_ok), S1_winner=s1_win,
                             S2_passes=bool(s2_ok), S2_winner=s2_win, outcome=outcome))
    tag = "_SELFTEST" if selftest else ("_PLANTTEST" if plant else "")
    pd.DataFrame(out_rows).to_csv(J / f"scenario_counts{tag}.csv", index=False)
    (J / ("data/devtests/" if tag else "") / f"confirmatory_result{tag}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res["decision"]), json.dumps({k: (v["winner"], v["winner_p"], v["beats_all_others"]) for k, v in summary.items()}, indent=0))


if __name__ == "__main__":
    main(selftest="--selftest" in sys.argv, plant="--planttest" in sys.argv)
