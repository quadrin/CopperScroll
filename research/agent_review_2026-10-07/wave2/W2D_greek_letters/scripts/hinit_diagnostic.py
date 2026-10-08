#!/usr/bin/env python3
"""Post-hoc diagnostic (NOT pre-registered): distribution of W if the 7 groups really were the
opening letters (lengths 3,3,2,2,2,2,2) of 7 Jewish persons drawn at random (bearer-weighted) from Ilan I.
usage: hinit_diagnostic.py initials_names_hand.csv OUT.json"""
import csv, sys, random, json, collections
random.seed(7)
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
tab = collections.Counter(); tot = 0
for r in rows:
    w = int(r["weight"]); ops = r["u1_openings"].split()
    if not ops: continue
    tot += w
    prefs = set(o[:L] for o in ops for L in (1, 2, 3) if len(o) >= L)
    for p in prefs: tab[p] += w
obs = sum(tab[g] for g in ["ΚΕΝ", "ΧΑΓ", "ΗΝ", "ΘΕ", "ΔΙ", "ΤΡ", "ΣΚ"]) / tot
names = [(r["canonical"], int(r["weight"])) for r in rows if r["canonical"]]
pop = [n for n, w in names]; wts = [w for n, w in names]
Ws = []
for _ in range(100000):
    gs = [random.choices(pop, weights=wts)[0][:L] for L in (3, 3, 2, 2, 2, 2, 2)]
    Ws.append(sum(tab[g] for g in gs) / tot)
Ws.sort()
res = {"W_obs_u1_hand": obs, "W_hinit_mean": sum(Ws)/len(Ws), "W_hinit_median": Ws[len(Ws)//2],
       "W_hinit_p01": Ws[len(Ws)//100], "P_W_le_obs_under_Hinit": sum(1 for w in Ws if w <= obs)/len(Ws)}
print(res); json.dump(res, open(sys.argv[2], "w"), indent=1)
