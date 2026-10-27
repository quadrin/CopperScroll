"""EXPLORATORY (not in the rule): leads that also require the landmark constraint itself to pass."""
import os, sys
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S
LMK = {"7": {"E7.L"}, "22": {"E22.S", "E22.E"}, "25": {"E25.P"}, "26": {"E26.L"}, "30": {"E30.L"}, "38": {"E38.P"}}
rows, inv, lane = S.load()
for setting in ("strict", "lenient"):
    cbe = defaultdict(list)
    for x in inv:
        cbe[x["entry"]].append(S.Cave(x["cave_id"], rows[x["cave_id"]], lane.get(x["cave_id"], {}), setting))
    def count(assign):
        _, _, table = S.run(assign, cbe, S.ENTRIES)
        out = []
        for e, lm, cid, name, sc, st, combos in table:
            ok = [bn for bn, bsc in combos if (S.lead_status(bsc) or (False,))[0] and any(bsc.get(k) == "pass" for k in LMK[lm])]
            if ok:
                out.append((e, cid))
        return out
    real = count({e: e for e in S.ENTRIES})
    sw = [count(a) for a in S.derangements(S.ENTRIES, 10, 20261027)]
    p = (1 + sum(len(s) >= len(real) for s in sw)) / 11
    print(setting, "real", len(real), Counter(e for e, _ in real), real[:12], "swaps", [len(s) for s in sw], "p", round(p, 3))
