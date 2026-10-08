#!/usr/bin/env python3
"""Score every Palmer (SWP 1881) name against every Copper Scroll name variant.

Run: python3 -I run_match.py ROOTDIR
Inputs : data/palmer_names.csv (parse_palmer.py), data/scroll_names.json, data/positive_controls.json,
         data/grid_anchors.json
Outputs: data/candidates_all.csv, data/candidates_ranked.csv, data/chance_control.csv,
         data/positive_controls_result.csv, data/grid_calibration.json
"""
import csv, json, math, os, random, sys, re
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toponym import heb_tokens, palmer_variants, score, ar_str, heb_str, HEB_MAP

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data")
PRIORITY = {"XIV", "XV", "XVII", "XVIII", "XXI", "XXII"}
THRESH = 0.75

def load_records():
    rs = list(csv.DictReader(open(os.path.join(D, "palmer_names.csv"), encoding="utf-8")))
    out = []
    for k, r in enumerate(rs):
        if not r["name_raw"] or len(r["name_raw"]) > 80:
            continue
        V, gen = palmer_variants(r["name_raw"], r["gloss"], r["source"])
        if not V:
            continue
        r["rid"] = k
        r["variants"] = V
        r["generic"] = " ".join(gen)
        out.append(r)
    return out

# ---------- grid calibration: SWP squares (column letter, row letter) -> lat/lon -------------
def grid_idx(g):
    return ord(g[0]) - ord("A"), ord(g[1]) - ord("a")

def calibrate(records):
    anchors = json.load(open(os.path.join(D, "grid_anchors.json"), encoding="utf-8"))
    pts = []
    for a in anchors:
        pts.append((grid_idx(a["grid"]), a["lat"], a["lon"], a["name"]))
    # least squares lon = a0 + a1*(col+0.5); lat = b0 + b1*(row+0.5)
    def fit(xs, ys):
        n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        b = sxy / sxx; a = my - b * mx
        res = [y - (a + b * x) for x, y in zip(xs, ys)]
        return a, b, math.sqrt(sum(r * r for r in res) / max(1, n - 2)), res
    cols = [p[0][0] + 0.5 for p in pts]; rows = [p[0][1] + 0.5 for p in pts]
    a0, a1, se_lon, rl = fit(cols, [p[2] for p in pts])
    b0, b1, se_lat, rb = fit(rows, [p[1] for p in pts])
    cal = dict(lon=(a0, a1, se_lon), lat=(b0, b1, se_lat),
               anchors=[dict(name=p[3], grid=chr(65 + p[0][0]) + chr(97 + p[0][1]), lat=p[1], lon=p[2],
                             res_lat_km=round(rb[i] * 111, 1), res_lon_km=round(rl[i] * 94.6, 1))
                        for i, p in enumerate(pts)],
               square_km=dict(ew=round(abs(a1) * 94.6, 1), ns=round(abs(b1) * 111, 1)))
    json.dump(cal, open(os.path.join(D, "grid_calibration.json"), "w"), indent=1)
    return cal

def grid_latlon(g, cal):
    if not g or len(g) != 2:
        return None, None
    c, r = grid_idx(g)
    a0, a1, _ = cal["lon"]; b0, b1, _ = cal["lat"]
    return round(b0 + b1 * (r + 0.5), 4), round(a0 + a1 * (c + 0.5), 4)

# ---------------------------------------------------------------------------------------------
def best_match(H, rec):
    best = None
    for lab, A in rec["variants"]:
        s, c, path = score(H, list(A))
        if best is None or s > best[0]:
            best = (s, c, path, lab, A)
    return best

def known_flag(name_entry, A):
    sk = "".join({"3": "ʿ"}.get(a, a.lower()) for a in A)
    for k in name_entry.get("known_ar", []):
        kk = k.lower().replace("'", "ʿ")
        if kk and kk in sk:
            return True
    return False

def main():
    random.seed(20261006)
    recs = load_records()
    print("records with comparable specific names:", len(recs))
    cal = calibrate(recs)
    print("grid calibration:", cal["square_km"], "lat se", cal["lat"][2], "lon se", cal["lon"][2])
    names = json.load(open(os.path.join(D, "scroll_names.json"), encoding="utf-8"))
    rows = []
    for ne in names:
        for v in ne["variants"]:
            H = heb_tokens(v["core"])
            if not H:
                continue
            for r in recs:
                b = best_match(H, r)
                if b[0] >= 0.6:
                    lat, lon = grid_latlon(r["grid"], cal)
                    rows.append(dict(scroll_id=ne["id"], scroll_name=ne["name"], entries=ne["entries"],
                                     variant=v["core"], variant_who=v["who"], heb_skeleton=heb_str(H),
                                     score=round(b[0], 3), cost=round(b[1], 2), rule_path=" ".join(b[2]),
                                     palmer_name=r["name_raw"], matched_part=b[3], ar_skeleton=ar_str(b[4]),
                                     gloss=re.sub(r"\s+", " ", r["gloss"])[:160], sheet=r["sheet"], page=r["page"],
                                     grid=r["grid"], approx_lat=lat, approx_lon=lon, ocr_source=r["source"],
                                     priority_sheet=r["sheet"] in PRIORITY,
                                     known_match=known_flag(ne, b[4]), scroll_priority=ne["priority"]))
    rows.sort(key=lambda x: (-x["score"], x["scroll_id"]))
    keys = list(rows[0].keys())
    with open(os.path.join(D, "candidates_all.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    # de-duplicate the two OCR sources: one row per (scroll_id, sheet, page, grid, ar_skeleton)
    seen, ranked = set(), []
    for x in rows:
        key = (x["scroll_id"], x["sheet"], x["grid"], x["ar_skeleton"])
        if key in seen:
            continue
        seen.add(key); ranked.append(x)
    with open(os.path.join(D, "candidates_ranked.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(ranked)
    print("candidate rows >=0.6:", len(rows), "deduped:", len(ranked))

    # ------------------ positive controls (method sensitivity) ------------------
    pcs = json.load(open(os.path.join(D, "positive_controls.json"), encoding="utf-8"))
    pri = [r for r in recs if r["sheet"] in PRIORITY]
    pc_rows = []
    for pc in pcs:
        H = heb_tokens(pc["core"])
        V, _ = palmer_variants(pc["arabic"], "", "tess")
        tb = max((score(H, list(A)) + (lab, A) for lab, A in V), key=lambda x: x[0]) if V else (0, 0, [], "", ())
        true_s = tb[0]
        comp = 0
        for r in pri:
            b_ = best_match(H, r)
            if b_[0] >= true_s - 1e-9 and b_[0] >= 0.6:
                comp += 1
        n_above = sum(1 for r in pri if best_match(H, r)[0] >= THRESH)
        in_ocr = any(ar_str(A) == ar_str(tb[4]) for r in pri for _, A in r["variants"]) if V else False
        pc_rows.append(dict(name=pc["name"], hebrew=pc["core"], heb_skeleton=heb_str(H), arabic=pc["arabic"],
                            ar_skeleton=ar_str(tb[4]), true_score=round(true_s, 3), rule_path=" ".join(tb[2]),
                            records_scoring_ge_true=comp, records_ge_075=n_above, skeleton_present_in_ocr=in_ocr))
    with open(os.path.join(D, "positive_controls_result.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(pc_rows[0].keys())); w.writeheader(); w.writerows(pc_rows)
    print("positive controls:", len(pc_rows), "| >=0.75:", sum(1 for p in pc_rows if p["true_score"] >= THRESH),
          "| >=0.9:", sum(1 for p in pc_rows if p["true_score"] >= 0.9))

    if os.environ.get("SKIP_CHANCE"):
        return
    # ------------------ chance control ------------------
    # random Hebrew-like cores with the same strong/weak pattern as each scroll variant;
    # consonants drawn 50/50 from (a) the pooled consonant frequency of scroll + control names,
    # (b) uniform over the 22 letters.
    pool = Counter()
    for ne in names:
        for v in ne["variants"]:
            for t, k in heb_tokens(v["core"]):
                pool[t] += 1
    for pc in pcs:
        for t, k in heb_tokens(pc["core"]):
            pool[t] += 1
    letters = sorted(set(HEB_MAP.values()))
    strong_letters = [l for l in letters if l not in ("'", "h", "w", "y")]
    tot = sum(pool[l] for l in strong_letters)
    def draw():
        if random.random() < 0.5:
            x = random.random() * tot
            for l in strong_letters:
                x -= pool[l]
                if x <= 0:
                    return l
        return random.choice(strong_letters)
    # unique Arabic variant skeletons on priority sheets (dedupe for speed); weight by record count
    sk_count = Counter()
    for r in pri:
        seen_r = set()
        for lab, A in r["variants"]:
            seen_r.add(A)
        for A in seen_r:
            sk_count[A] += 0  # placeholder to keep keys
        r["_sks"] = seen_r
    uniq = sorted({A for r in pri for A in r["_sks"]})
    print("unique Arabic skeletons on priority sheets:", len(uniq))
    NRAND = int(os.environ.get("NRAND", "60"))
    cc_rows = []
    cache_obs = {}
    for ne in names:
        for v in ne["variants"]:
            H = heb_tokens(v["core"])
            # observed: number of priority-sheet records with best score >= THRESH
            sk_best = {A: score(H, list(A))[0] for A in uniq}
            obs = sum(1 for r in pri if max(sk_best[A] for A in r["_sks"]) >= THRESH)
            obs_best = max(sk_best.values())
            rand_hits, rand_best = [], []
            for t in range(NRAND):
                Hr = [(draw() if k != "weak" else t0, k) for (t0, k) in H]
                skb = {A: score(Hr, list(A))[0] for A in uniq}
                rand_hits.append(sum(1 for r in pri if max(skb[A] for A in r["_sks"]) >= THRESH))
                rand_best.append(max(skb.values()))
            mean = sum(rand_hits) / NRAND
            sd = math.sqrt(sum((x - mean) ** 2 for x in rand_hits) / max(1, NRAND - 1))
            p_hits = (1 + sum(1 for x in rand_hits if x >= obs)) / (NRAND + 1)
            p_best = (1 + sum(1 for x in rand_best if x >= obs_best)) / (NRAND + 1)
            p_any = sum(1 for x in rand_hits if x >= 1) / NRAND
            cc_rows.append(dict(scroll_id=ne["id"], variant=v["core"], heb_skeleton=heb_str(H),
                                n_strong=sum(1 for _, k in H if k == "strong"),
                                observed_hits_ge075=obs, observed_best=round(obs_best, 3),
                                random_mean_hits=round(mean, 2), random_sd=round(sd, 2),
                                random_p95=sorted(rand_hits)[int(0.95 * (NRAND - 1))],
                                p_random_hits_ge_observed=round(p_hits, 3),
                                p_random_best_ge_observed=round(p_best, 3),
                                share_random_with_any_hit=round(p_any, 3)))
            print(ne["id"], v["core"], "obs", obs, "rand mean", round(mean, 2), "p", round(p_hits, 3), flush=True)
    with open(os.path.join(D, "chance_control.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cc_rows[0].keys())); w.writeheader(); w.writerows(cc_rows)

if __name__ == "__main__":
    main()
