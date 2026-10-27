# Run 22 step 2-3: score 9 sites x 61 entries, and the shuffled control.
import json, random, sys, csv, os, statistics
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENT = json.load(open(os.path.join(BASE, "out/step1_entry_relations.json"), encoding="utf-8"))
INVJ = json.load(open(os.path.join(BASE, "out/site_inventory.json"), encoding="utf-8"))
SITES, INV, NAMES, SYN = INVJ["sites"], INVJ["inventory"], INVJ["names"], INVJ["synonyms"]
RANK = {"P": 2, "U": 1, "A": 0}
MI = {"strict": 0, "lenient": 1}

def best(vs):
    return max(vs, key=lambda x: RANK[x]) if vs else "U"

def lookup_F(t, site, mode):
    i = MI[mode]; vs = []
    for m in SYN.get(t, [t]):
        r = INV[site].get("F:" + m)
        vs.append(r[i] if r else "U")
    # P if any member P; A only if every member A; else U
    if "P" in vs: return "P"
    if all(x == "A" for x in vs): return "A"
    return "U"

def lookup_QS(code, site, mode):
    i = MI[mode]; parts = code.split(":"); subj = parts[1]
    vs = []
    for m in SYN.get(subj, [subj]):
        c = ":".join([parts[0], m] + parts[2:])
        r = INV[site].get(c)
        vs.append(r[i] if r else "U")
    if "P" in vs: return "P"
    if all(x == "A" for x in vs): return "A"
    return "U"

def resolve(code, lm):
    p = code.split(":")
    if p[0] in ("Q", "S"):
        p = [lm if (j >= 1 and x == "L") else x for j, x in enumerate(p)]
    return ":".join(p)

def verdict(code, site, mode):
    k = code.split(":")[0]
    if k == "F": return lookup_F(code[2:], site, mode)
    if k in ("Q", "S"): return lookup_QS(code, site, mode)
    if k == "N":
        n = code[2:]; return NAMES[n][site][MI[mode]] if n in NAMES else "U"
    if k == "R":
        r = INV[site].get(code); return r[MI[mode]] if r else "U"
    raise ValueError(code)

def score_entry(rels, lm, site, mode, anyreading):
    out = []
    for r in rels:
        c = resolve(r["code"], lm); v = verdict(c, site, mode)
        if anyreading and r.get("alt"):
            ca = resolve(r["alt"], lm); va = verdict(ca, site, mode)
            if RANK[va] > RANK[v]: v, c = va, ca + " (alt)"
        out.append((c, v))
    vs = [v for _, v in out]
    sat = all(v == "P" for v in vs); comp = "A" not in vs
    return out, sat, comp

MODES = [("strict", False), ("lenient", False), ("strict", True), ("lenient", True)]
def mname(m, a): return f"{m}-{'any' if a else 'base'}"

def run_real():
    res = {}
    for n, e in ENT.items():
        for s in SITES:
            for m, a in MODES:
                out, sat, comp = score_entry(e["relations"], e["landmark"], s, m, a)
                res[(n, s, mname(m, a))] = dict(rels=out, sat=sat, comp=comp,
                    npass=sum(v == "P" for _, v in out), nunk=sum(v == "U" for _, v in out), nfail=sum(v == "A" for _, v in out))
    return res

def synth(seed):
    rng = random.Random(seed)
    keys = list(ENT.keys())
    lms = [ENT[k]["landmark"] for k in keys]
    rest = [r for k in keys for r in ENT[k]["relations"][1:]]
    counts = [len(ENT[k]["relations"]) - 1 for k in keys]
    rng.shuffle(lms); rng.shuffle(rest)
    out = {}; i = 0
    for k, lm, c in zip(keys, lms, counts):
        rels = [dict(k="F", code="F:" + lm, subj=None, alt=None)] + rest[i:i + c]; i += c
        out[k] = dict(landmark=lm, relations=rels)
    return out

def count_sat(entries, mode, anyr, sites):
    sat = comp = 0
    for n, e in entries.items():
        for s in sites:
            _, st, cp = score_entry(e["relations"], e["landmark"], s, mode, anyr)
            sat += st; comp += cp
    return sat, comp

if __name__ == "__main__":
    nshuf = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed0 = 20261027
    res = run_real()
    insites = [s for s in SITES if s != "MAS"]
    allsites = list(SITES)
    summary = {}
    for m, a in MODES:
        mn = mname(m, a)
        for label, ss in [("in_region", insites), ("with_Masada", allsites)]:
            real_sat = sum(res[(n, s, mn)]["sat"] for n in ENT for s in ss)
            real_comp = sum(res[(n, s, mn)]["comp"] for n in ENT for s in ss)
            sh = [count_sat(synth(seed0 + i), m, a, ss) for i in range(nshuf)]
            ssat = [x[0] for x in sh]; scomp = [x[1] for x in sh]
            p_sat = (1 + sum(x >= real_sat for x in ssat)) / (nshuf + 1)
            p_comp = (1 + sum(x >= real_comp for x in scomp)) / (nshuf + 1)
            summary[f"{mn}|{label}"] = dict(real_satisfied=real_sat, shuffled_satisfied=ssat if nshuf <= 20 else None,
                shuf_sat_mean=statistics.mean(ssat), shuf_sat_min=min(ssat), shuf_sat_max=max(ssat),
                ratio=(real_sat / statistics.mean(ssat)) if statistics.mean(ssat) else None, p_satisfied=p_sat,
                real_compatible=real_comp, shuf_comp_mean=statistics.mean(scomp), shuf_comp_min=min(scomp), shuf_comp_max=max(scomp), p_compatible=p_comp)
    tag = f"n{nshuf}"
    json.dump(summary, open(os.path.join(BASE, f"out/control_summary_{tag}.json"), "w"), indent=1)
    # full matrix (only once)
    if nshuf == 10:
        with open(os.path.join(BASE, "out/pair_scores.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["entry", "site", "mode", "satisfied", "compatible", "n_pass", "n_unknown", "n_fail", "relations"])
            for (n, s, mn), r in res.items():
                w.writerow([n, s, mn, int(r["sat"]), int(r["comp"]), r["npass"], r["nunk"], r["nfail"],
                            "; ".join(f"{c}={v}" for c, v in r["rels"])])
        # synthetic entries of shuffle 1 for inspection
        json.dump(synth(seed0), open(os.path.join(BASE, "out/shuffle_seed20261027.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    for k, v in summary.items():
        print(k, {x: v[x] for x in ["real_satisfied", "shuf_sat_mean", "shuf_sat_min", "shuf_sat_max", "ratio", "p_satisfied", "real_compatible", "shuf_comp_mean", "p_compatible"]})
