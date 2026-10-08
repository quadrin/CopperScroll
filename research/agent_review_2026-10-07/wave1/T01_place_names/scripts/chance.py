#!/usr/bin/env python3
"""Chance control: how many Palmer names would a random Hebrew consonant string 'match'?

Pool: tesseract-OCR records on the priority sheets (XIV, XV, XVII, XVIII, XXI, XXII), one OCR source only
so that no name is counted twice. For every scroll-name variant we record the observed number of
records with score >= 0.75 and the best score. Random cores keep the variant's pattern (number and
position of strong consonants, weak letters and feminine -t unchanged) and draw each strong consonant
50/50 from the pooled consonant frequency of scroll + control names, or uniformly from the 18 strong
Hebrew consonants. NRAND random cores per distinct pattern.

Run: NRAND=100 python3 -I chance.py ROOTDIR
Output: data/chance_control.csv, data/chance_random_by_pattern.json
"""
import csv, json, math, os, random, sys
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toponym import heb_tokens, palmer_variants, score, heb_str, HEB_MAP

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data")
PRIORITY = {"XIV", "XV", "XVII", "XVIII", "XXI", "XXII"}
THRESH = 0.75
NRAND = int(os.environ.get("NRAND", "100"))

def load_pool():
    rs = list(csv.DictReader(open(os.path.join(D, "palmer_names.csv"), encoding="utf-8")))
    recs = []
    for r in rs:
        if r["source"] != "tess" or r["sheet"] not in PRIORITY or not r["name_raw"] or len(r["name_raw"]) > 80:
            continue
        V, _ = palmer_variants(r["name_raw"], r["gloss"], "tess")
        if V:
            recs.append(frozenset(A for _, A in V))
    uniq = sorted({A for s in recs for A in s})
    idx = {A: i for i, A in enumerate(uniq)}
    rec_idx = [[idx[A] for A in s] for s in recs]
    return uniq, rec_idx

UNIQ, REC_IDX = load_pool()

def hits_for(H):
    sk = [score(H, list(A))[0] for A in UNIQ]
    best_per_rec = [max(sk[i] for i in ri) for ri in REC_IDX]
    return sum(1 for b in best_per_rec if b >= THRESH), max(sk)

def rand_job(args):
    pattern, seed, pool_freq = args
    rng = random.Random(seed)
    strong = sorted(pool_freq)
    tot = sum(pool_freq.values())
    def draw():
        if rng.random() < 0.5:
            x = rng.random() * tot
            for l in strong:
                x -= pool_freq[l]
                if x <= 0:
                    return l
        return rng.choice(strong)
    H = [((draw() if k in ("strong",) else t), k) for t, k in pattern]
    return hits_for(H)

def main():
    names = json.load(open(os.path.join(D, "scroll_names.json"), encoding="utf-8"))
    pcs = json.load(open(os.path.join(D, "positive_controls.json"), encoding="utf-8"))
    pool = Counter()
    for ne in names:
        for v in ne["variants"]:
            for t, k in heb_tokens(v["core"]):
                if k == "strong":
                    pool[t] += 1
    for pc in pcs:
        for t, k in heb_tokens(pc["core"]):
            if k == "strong":
                pool[t] += 1
    strong_letters = [l for l in sorted(set(HEB_MAP.values())) if l not in ("'", "h", "w", "y")]
    for l in strong_letters:
        pool.setdefault(l, 0)
    variants = []
    for ne in names:
        for v in ne["variants"]:
            H = heb_tokens(v["core"])
            # pattern: strong positions randomised, weak letters / fem -t kept
            pat = tuple(("S", "strong") if k == "strong" else (t, k) for t, k in H)
            variants.append((ne, v, H, pat))
    patterns = sorted({p for *_, p in variants})
    print("pool records:", len(REC_IDX), "unique skeletons:", len(UNIQ), "patterns:", len(patterns), flush=True)
    jobs = []
    for pi, p in enumerate(patterns):
        for t in range(NRAND):
            jobs.append((p, 1000 * pi + t, dict(pool)))
    with Pool(2) as P:
        res = P.map(rand_job, jobs, chunksize=4)
    by_pat = {}
    for (p, _, _), r in zip(jobs, res):
        by_pat.setdefault(p, []).append(r)
    json.dump({json.dumps(p): v for p, v in by_pat.items()},
              open(os.path.join(D, "chance_random_by_pattern.json"), "w"))
    rows = []
    for ne, v, H, pat in variants:
        obs, obs_best = hits_for(H)
        rh = [x[0] for x in by_pat[pat]]
        rb = [x[1] for x in by_pat[pat]]
        n = len(rh)
        mean = sum(rh) / n
        sd = math.sqrt(sum((x - mean) ** 2 for x in rh) / max(1, n - 1))
        rows.append(dict(scroll_id=ne["id"], variant=v["core"], variant_who=v["who"], heb_skeleton=heb_str(H),
                         n_strong=sum(1 for _, k in H if k == "strong"),
                         observed_hits_ge075=obs, observed_best=round(obs_best, 3),
                         random_mean_hits=round(mean, 2), random_sd=round(sd, 2),
                         random_p95_hits=sorted(rh)[int(0.95 * (n - 1))],
                         p_random_hits_ge_observed=round((1 + sum(1 for x in rh if x >= obs)) / (n + 1), 3),
                         share_random_best_ge_075=round(sum(1 for x in rb if x >= THRESH) / n, 3),
                         share_random_best_ge_090=round(sum(1 for x in rb if x >= 0.9) / n, 3),
                         n_random=n, pool_records=len(REC_IDX)))
    with open(os.path.join(D, "chance_control.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for r in rows:
        print(r["scroll_id"], r["variant"], r["observed_hits_ge075"], r["random_mean_hits"], r["p_random_hits_ge_observed"],
              r["share_random_best_ge_075"], flush=True)

if __name__ == "__main__":
    main()
