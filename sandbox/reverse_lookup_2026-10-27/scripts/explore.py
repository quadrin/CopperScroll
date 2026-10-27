# Exploratory follow-ups (not part of the rule): name-blind fit, multi-relation entries.
import sys, os, json, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S
insites = [s for s in S.SITES if s != "MAS"]
def nameblind(rels):
    return [r for r in rels if r["code"].split(":")[0] not in ("N",)]
def count(entries, mode, anyr, sites, minrel=1, blind=False):
    n = 0; pairs = []
    for k, e in entries.items():
        rels = nameblind(e["relations"]) if blind else e["relations"]
        if len(rels) < minrel: continue
        for s in sites:
            _, st, _ = S.score_entry(rels, e["landmark"], s, mode, anyr)
            if st: n += 1; pairs.append((k, s))
    return n, pairs
out = {}
for mode, anyr in [("strict", False), ("lenient", False)]:
    for label, minrel, blind in [("min3rel", 3, False), ("nameblind_all", 1, True), ("nameblind_min3", 3, True)]:
        real, pairs = count(S.ENT, mode, anyr, insites, minrel, blind)
        sh = [count(S.synth(20261027 + i), mode, anyr, insites, minrel, blind)[0] for i in range(1000)]
        p = (1 + sum(x >= real for x in sh)) / 1001
        out[f"{mode}|{label}"] = dict(real=real, shuf_mean=statistics.mean(sh), shuf_min=min(sh), shuf_max=max(sh), p=p, pairs=pairs)
        print(mode, label, real, round(statistics.mean(sh), 2), min(sh), max(sh), round(p, 3), pairs)
json.dump(out, open(os.path.join(S.BASE, "out/explore.json"), "w"), indent=1)
