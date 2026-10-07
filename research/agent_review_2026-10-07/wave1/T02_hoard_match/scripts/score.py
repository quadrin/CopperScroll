#!/usr/bin/env python3
"""Score hoard records against Copper Scroll entries using the pre-stated rules in
../scoring_rules.json.  Inputs: ../hoards.json, ../entry_features.json.  Outputs in ../ :
scores_all.csv, top_pairs.csv, best_per_record.csv, best_per_entry.csv, null_test.json,
quantity_check.csv.  Run: python3 -I score.py
"""
import csv
import json
import math
import os
import random
import re

OUT = "agent_review/wave1/T02_hoard_match"

ANCHORS = {"jer_shaveh": (31.77825, 35.23534, 3.0), "tekoa_herodium": (31.666, 35.242, 4.0),
           "jordan_ford": (31.85611, 35.46306, 5.0)}
ENTRY_OVERRIDES = {"32": {"add_contents": ["unspecified_amount"]}, "56": {"add_contents": ["unspecified_amount"]},
                   "34": {"depth": 17}, "14": {"depth": 3}, "39": {"depth": 8.5}}
PRIMARY_EXCLUDE = {"threshold", "corner", "wall", "pillar", "steps", "stone", "unknown", "floor"}
GENERIC = {"building", "court", "natural", "valley", "field"}
FAMILIES = {
    "water": {"cistern", "pit", "pool", "reservoir", "basin", "conduit", "outlet", "spring", "pool_adjacent"},
    "underground": {"cave", "fissure", "chamber", "dovecote", "pit"},
    "burial": {"tomb", "monument"},
    "built": {"court", "building", "fortress", "street"},
    "open": {"cairn", "valley", "field", "road", "mound", "ruin", "rock", "natural"},
}
STRUCT = {"corner", "under_stone", "threshold", "floor", "wall", "upper_storey", "pillar", "steps"}
DIRS = {"north", "south", "east", "west"}
CUBIT_M = 0.5
TALENT_KG = 21.3
KARSH_G = (71.0, 142.0)


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def prec_km(s):
    if not s:
        return None
    m = re.search(r"area\s*~\s*([\d.]+)\s*km", s)
    if m:
        return float(m.group(1)) / 2
    m = re.search(r"~\s*([\d.]+)\s*(m|km)", s)
    if m:
        v = float(m.group(1))
        return v / 1000 if m.group(2) == "m" else v
    return None


def cand_points(e):
    pts = []
    for c in e["candidates"]:
        if c["lat"] is not None:
            pts.append((c["lat"], c["lon"], prec_km(c["precision"]) or 0.25, c["placeId"], c.get("region")))
        elif c["placeId"] in ANCHORS:
            la, lo, r = ANCHORS[c["placeId"]]
            pts.append((la, lo, r, c["placeId"] + "(anchor)", c.get("region")))
    return pts


def score_R(h, e, loc=None):
    lat, lon, rp = loc if loc else (h["lat"], h["lon"], h["prec_km"])
    pts = cand_points(e)
    if not pts:
        return 0, None
    if lat is None:
        jer = any(c.get("region") == "jericho" for c in e["candidates"])
        return (1 if jer else 0), None
    best, bestd = 0, None
    for la, lo, cp, pid, _ in pts:
        d = hav((lat, lon), (la, lo))
        if d <= max(0.25, cp) + rp and rp <= 0.5:
            r = 3
        elif d <= 3 + cp + rp:
            r = 2
        elif d <= 20 + cp + rp:
            r = 1
        else:
            r = 0
        if r > best or (r == best and (bestd is None or d < bestd[0])):
            best, bestd = r, (round(d, 2), pid)
    return best, bestd


def score_L(h, e):
    hp = set(h["findspot"]) - PRIMARY_EXCLUDE
    ep = set(e["landmarks"]) - PRIMARY_EXCLUDE
    shared = hp & ep
    if shared - GENERIC:
        return 2
    if shared:
        return 1
    for fam in FAMILIES.values():
        if hp & fam and ep & fam:
            return 1
    return 0


def score_C(h, e):
    ec = set(e["containers"])
    rc = h["container"]
    if not ec or rc in ("none", "", None):
        return 0
    exact = {"chest": "box", "jar": "jar", "pot": "pot", "juglet": "juglet"}
    if any(exact[c] == rc for c in ec):
        return 2
    if rc in ("jar", "pot", "juglet", "moneybox", "box", "bowl", "lamp", "basket"):
        return 1
    return 0


def score_K(h, e):
    ek = set(e["contents"])
    rk = set(h["contents"])
    s = 0
    silver = bool(rk & {"silver_coins", "silver_bullion"})
    gold = bool(rk & {"gold_coins"})
    if "silver" in ek and silver: s = max(s, 2)
    if "gold" in ek and gold: s = max(s, 2)
    if "vessels" in ek and "metal_vessels" in rk: s = max(s, 2)
    if "scroll_or_record" in ek and "scrolls" in rk: s = max(s, 2)
    if "staters" in ek and "silver_coins" in rk: s = max(s, 2)
    if "ingots" in ek and "silver_bullion" in rk: s = max(s, 1)
    if "unspecified_amount" in ek and (silver or gold): s = max(s, 1)
    return s


def score_P(h, e):
    rc, ec = set(h.get("cues", [])), set(e["position_cues"])
    p = 0
    if rc & ec & STRUCT:
        p = 1
        if rc & ec & DIRS:
            p += 1
    if h.get("depth_m") and e.get("depth_cubits"):
        ratio = h["depth_m"] / (e["depth_cubits"] * CUBIT_M)
        if 0.67 <= ratio <= 1.5:
            p += 1
    return min(p, 2)


def score_D(h):
    return 1 if (h.get("tpq") is not None and h["tpq"] <= 70) else 0


def score_pair(h, e, loc=None):
    R, rd = score_R(h, e, loc)
    L, Cc, K, P, D = score_L(h, e), score_C(h, e), score_K(h, e), score_P(h, e), score_D(h)
    return {"R": R, "L": L, "C": Cc, "K": K, "P": P, "D": D, "S": R + L + Cc + K + P + D, "nearest": rd}


def worth(s):
    return s["S"] >= 9 and s["R"] == 3 and s["L"] >= 1 and (s["C"] == 2 or s["K"] == 2) and s["D"] == 1


def entry_mass(e):
    a = e.get("amount_talents_as_translated")
    if not a:
        return None
    uf = e["unit_form"]
    if uf == "abbr":
        return {"reading": "karsh", "g_low": a * KARSH_G[0], "g_high": a * KARSH_G[1], "talent_g": a * TALENT_KG * 1000}
    if uf in ("full", "none"):
        return {"reading": "talent", "g_low": a * TALENT_KG * 1000, "g_high": a * TALENT_KG * 1000, "talent_g": a * TALENT_KG * 1000}
    return {"reading": "mixed", "g_low": a * KARSH_G[0], "g_high": a * TALENT_KG * 1000, "talent_g": a * TALENT_KG * 1000}


def main():
    hoards = json.load(open(os.path.join(OUT, "hoards.json")))
    entries = json.load(open(os.path.join(OUT, "entry_features.json")))
    for e in entries:
        ov = ENTRY_OVERRIDES.get(e["entry"], {})
        e["contents"] = sorted(set(e["contents"]) | set(ov.get("add_contents", [])))
        if "depth" in ov:
            e["depth_cubits"] = ov["depth"]
    scored = [h for h in hoards if h["scope"] in ("in", "edge")]
    rows = []
    for h in scored:
        for e in entries:
            s = score_pair(h, e)
            rows.append({"record": h["id"], "record_name": h["name"], "entry": e["entry"], "entry_title": e["title"], **s,
                         "worth_testing": worth(s)})
    cols = ["record", "record_name", "entry", "entry_title", "R", "L", "C", "K", "P", "D", "S", "worth_testing", "nearest"]
    with open(os.path.join(OUT, "scores_all.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # quantity check for pairs S>=6
    hmap = {h["id"]: h for h in hoards}
    emap = {e["entry"]: e for e in entries}
    top = sorted([r for r in rows if r["S"] >= 6], key=lambda r: (-r["S"], r["record"], r["entry"]))
    qrows = []
    for r in top:
        h, e = hmap[r["record"]], emap[r["entry"]]
        em = entry_mass(e)
        hm = h.get("mass_g")
        mid = None
        if hm and hm[0]:
            mid = (hm[0] + (hm[1] or hm[0])) / 2
        ratio_lo = ratio_hi = None
        compat = ""
        if em and mid:
            ratio_lo, ratio_hi = mid / em["g_high"], mid / em["g_low"]
            compat = "yes" if (ratio_hi >= 1 / 3 and ratio_lo <= 3) else "no"
        qrows.append({**{k: r[k] for k in ("record", "record_name", "entry", "entry_title", "S", "R", "L", "C", "K", "P", "D", "worth_testing")},
                      "entry_amount": e.get("amount_talents_as_translated"), "unit_form": e["unit_form"],
                      "entry_mass_reading": em["reading"] if em else "", "entry_mass_g_range": f"{em['g_low']:.0f}-{em['g_high']:.0f}" if em else "",
                      "record_mass_g_mid": round(mid) if mid else "", "ratio_range": f"{ratio_lo:.3g}-{ratio_hi:.3g}" if ratio_lo else "",
                      "quantity_compatible_x3": compat, "nearest_candidate": r["nearest"]})
    with open(os.path.join(OUT, "top_pairs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(qrows[0].keys()))
        w.writeheader()
        w.writerows(qrows)
    # best per record / entry
    by_rec = {}
    for r in rows:
        by_rec.setdefault(r["record"], []).append(r)
    bpr = []
    for rid, rs in by_rec.items():
        rs.sort(key=lambda r: -r["S"])
        best = rs[0]["S"]
        ties = [r["entry"] for r in rs if r["S"] == best]
        second = next((r["S"] for r in rs if r["S"] < best), None)
        bpr.append({"record": rid, "name": hmap[rid]["name"], "best_S": best, "n_entries_at_best": len(ties),
                    "entries_at_best": " ".join(ties[:12]), "second_best_S": second, "scope": hmap[rid]["scope"]})
    bpr.sort(key=lambda r: (-r["best_S"], r["n_entries_at_best"]))
    with open(os.path.join(OUT, "best_per_record.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(bpr[0].keys()))
        w.writeheader()
        w.writerows(bpr)
    by_ent = {}
    for r in rows:
        by_ent.setdefault(r["entry"], []).append(r)
    bpe = []
    for e in entries:
        rs = sorted(by_ent[e["entry"]], key=lambda r: -r["S"])
        best = rs[0]["S"]
        ties = [r["record"] for r in rs if r["S"] == best]
        bpe.append({"entry": e["entry"], "title": e["title"], "best_S": best, "records_at_best": " ".join(ties[:10]),
                    "best_components": f"R{rs[0]['R']} L{rs[0]['L']} C{rs[0]['C']} K{rs[0]['K']} P{rs[0]['P']} D{rs[0]['D']}"})
    with open(os.path.join(OUT, "best_per_entry.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(bpe[0].keys()))
        w.writeheader()
        w.writerows(bpe)
    # null model
    obs7 = sum(r["S"] >= 7 for r in rows)
    obsmax = max(r["S"] for r in rows)
    obsworth = sum(r["worth_testing"] for r in rows)
    obs_R3_contentpairs = sum(1 for r in rows if r["R"] == 3 and (r["C"] + r["K"] + r["L"]) >= 4)
    locs = [(h["lat"], h["lon"], h["prec_km"]) for h in scored]
    rng = random.Random(20261006)
    N = 2000
    ge7, gemax, geworth, geR3 = 0, 0, 0, 0
    dist7 = []
    for _ in range(N):
        perm = locs[:]
        rng.shuffle(perm)
        c7 = cmax = cw = cr3 = 0
        for h, loc in zip(scored, perm):
            for e in entries:
                s = score_pair(h, e, loc)
                if s["S"] >= 7: c7 += 1
                if s["S"] > cmax: cmax = s["S"]
                if worth(s): cw += 1
                if s["R"] == 3 and (s["C"] + s["K"] + s["L"]) >= 4: cr3 += 1
        dist7.append(c7)
        ge7 += c7 >= obs7
        gemax += cmax >= obsmax
        geworth += cw >= obsworth
        geR3 += cr3 >= obs_R3_contentpairs
    dist7.sort()
    res = {"n_records_scored": len(scored), "n_entries": len(entries), "n_pairs": len(rows),
           "observed": {"pairs_S_ge_7": obs7, "max_S": obsmax, "worth_testing_pairs": obsworth,
                        "pairs_R3_and_L+C+K>=4": obs_R3_contentpairs},
           "null_permutations": N,
           "p_values": {"pairs_S_ge_7": (ge7 + 1) / (N + 1), "max_S": (gemax + 1) / (N + 1),
                        "worth_testing_pairs": (geworth + 1) / (N + 1), "pairs_R3_and_L+C+K>=4": (geR3 + 1) / (N + 1)},
           "null_pairs_S_ge_7_median": dist7[N // 2], "null_pairs_S_ge_7_95pct": dist7[int(N * 0.95)]}
    json.dump(res, open(os.path.join(OUT, "null_test.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    print("score distribution:", {s: sum(r["S"] == s for r in rows) for s in range(13)})


if __name__ == "__main__":
    main()
