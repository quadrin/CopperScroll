#!/usr/bin/env python3
"""Regional chance control: probability that a random Hebrew-like core of the same pattern finds at least
one Palmer name scoring >= 0.75 inside a given region (tesseract records only, no double counting).

Regions (SWP grid squares, calibrated in data/grid_calibration.json, ~7 x 9 km per square):
  jericho_qumran : sheet XVIII squares Os, Ot, Ou, Ps, Pt, Pu, Qs, Qt (Jericho oasis, Wadi Qelt, NW Dead Sea, Qumran)
  judean_desert  : all of sheet XVIII plus XVII/XXI/XXII columns N-O (desert east of Jerusalem-Bethlehem-Tekoa)
  jerusalem      : sheet XVII squares Mt, Mu (Jerusalem and its immediate surroundings)
Run: NRAND=300 python3 -I chance_regional.py ROOTDIR   -> data/chance_regional.csv
"""
import csv, json, os, random, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toponym import heb_tokens, palmer_variants, score, heb_str, HEB_MAP

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data")
NRAND = int(os.environ.get("NRAND", "300"))
THRESH = 0.75
REGIONS = {
    "jericho_qumran": lambda sh, g: sh == "XVIII" and g in {"Os", "Ot", "Ou", "Ps", "Pt", "Pu", "Qs", "Qt"},
    "judean_desert": lambda sh, g: sh == "XVIII" or (sh in {"XVII", "XXI", "XXII"} and g[:1] in {"N", "O"}),
    "jerusalem": lambda sh, g: sh == "XVII" and g in {"Mt", "Mu"},
}

def main():
    rs = list(csv.DictReader(open(os.path.join(D, "palmer_names.csv"), encoding="utf-8")))
    pools = {k: [] for k in REGIONS}
    for r in rs:
        if r["source"] != "tess" or not r["name_raw"] or len(r["name_raw"]) > 80:
            continue
        V, _ = palmer_variants(r["name_raw"], r["gloss"], "tess")
        if not V:
            continue
        for k, f in REGIONS.items():
            if f(r["sheet"], r["grid"]):
                pools[k].append((r["name_raw"], r["sheet"], r["page"], r["grid"], [A for _, A in V]))
    print({k: len(v) for k, v in pools.items()})
    names = json.load(open(os.path.join(D, "scroll_names.json"), encoding="utf-8"))
    pool_freq = Counter()
    for ne in names:
        for v in ne["variants"]:
            for t, k in heb_tokens(v["core"]):
                if k == "strong":
                    pool_freq[t] += 1
    strong = [l for l in sorted(set(HEB_MAP.values())) if l not in ("'", "h", "w", "y")]
    tot = sum(pool_freq[l] for l in strong)
    rng = random.Random(7)
    def draw():
        if rng.random() < 0.5:
            x = rng.random() * tot
            for l in strong:
                x -= pool_freq[l]
                if x <= 0:
                    return l
        return rng.choice(strong)
    def best_in(H, pool):
        out = []
        for name, sh, pg, g, Vs in pool:
            s = max(score(H, list(A))[0] for A in Vs)
            if s >= THRESH:
                out.append((round(s, 3), name, sh, pg, g))
        return sorted(out, reverse=True)
    pat_cache = {}
    rows = []
    for ne in names:
        if ne["priority"] == 0:
            pass
        for v in ne["variants"]:
            H = heb_tokens(v["core"])
            pat = tuple(("S", "strong") if k == "strong" else (t, k) for t, k in H)
            if pat not in pat_cache:
                res = {k: 0 for k in REGIONS}
                for _ in range(NRAND):
                    Hr = [((draw() if k == "strong" else t), k) for t, k in pat]
                    for k, pool in pools.items():
                        for name, sh, pg, g, Vs in pool:
                            if max(score(Hr, list(A))[0] for A in Vs) >= THRESH:
                                res[k] += 1
                                break
                pat_cache[pat] = {k: res[k] / NRAND for k in res}
            row = dict(scroll_id=ne["id"], variant=v["core"], heb_skeleton=heb_str(H))
            for k, pool in pools.items():
                hits = best_in(H, pool)
                row[f"{k}_hits"] = len(hits)
                row[f"{k}_examples"] = "; ".join(f"{h[1]} ({h[2]} p.{h[3]} {h[4]}, {h[0]})" for h in hits[:4])
                row[f"{k}_p_random_any_hit"] = round(pat_cache[pat][k], 3)
            rows.append(row)
            print(ne["id"], v["core"], {k: (row[f"{k}_hits"], row[f"{k}_p_random_any_hit"]) for k in REGIONS}, flush=True)
    with open(os.path.join(D, "chance_regional.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    main()
