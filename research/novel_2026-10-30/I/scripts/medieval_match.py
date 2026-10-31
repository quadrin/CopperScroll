#!/usr/bin/env python3
"""Lane I frozen matcher: scroll names vs medieval place records (1100-1600), conjunction of
   name score >= 0.75 (T01 scorer + rules M1-M9 below)  AND  feature class allowed for the scroll name
   AND  position inside the scroll name's candidate area.
Usage: NRAND=200 python3 -I medieval_match.py LANE_DIR T01_DIR W2B_INPUTS_DIR [--dry]
--dry: build inputs, print counts, score nothing (used before the freeze).

Medieval rendering rules (applied to each name string before T01 lat_tokens):
 M1 lower-case; strip diacritics; drop possessive 's; brackets removed.
 M2 generic words (English, French, Latin, German, Arabic topographic) and articles/prepositions are removed;
    every remaining word and the whole remaining phrase are compared (as T01 palmer_variants).
 M3 'ph' -> f; 'qu' -> k; 'x' -> ks; 'dj' -> j; 'sch' -> sh; 'tz' -> ts; 'ck' -> k; 'w' -> w.
 M4 'c' before e/i/y -> s OR k (variants); other 'c' (not in 'ch') -> k.
 M5 'ch' -> kh OR k OR sh (variants: Latin/German/English vs French).
 M6 'th' -> t OR th (variants).
 M7 word-initial 'j' -> j OR y (Latin/German/English J for yod); 'g' before e/i -> g OR j.
 M8 'y' not next to a vowel -> i (vowel); 'ou','oo' -> u; 'ee' -> i.
 M9 word-initial 'beth','bet','beit','bayt','beth-' prefix: variant with the prefix removed.
 Variants are capped at 16 per word (first 16 in a fixed order).
Position rule: record placed (lat, lon, radius) -> distance to the nearest candidate place of any scroll
 entry that uses the name (W2B candidates_v3 + places_v3) <= radius + place sigma + SLACK_KM (5 km).
 Candidate places without coordinates use the region mapping. Unplaced record -> its region code must be in the
 name's mapped region set.
"""
import sys, os, csv, json, re, math, random, unicodedata
from collections import defaultdict, Counter
from multiprocessing import Pool

LANE, T01, W2B = sys.argv[1:4]
DRY = "--dry" in sys.argv
sys.path.insert(0, os.path.join(T01, "scripts"))
from toponym import heb_tokens, score, lat_tokens, HEB_MAP, heb_str

THRESH = 0.75
SLACK_KM = 5.0
NRAND = int(os.environ.get("NRAND", "200"))
SEED = 20261030
REGMAP = {"JER": {"JER"}, "JERICHO": {"JJV"}, "QUMRAN": {"JJV", "DES"}, "DESERT": {"DES"}, "SOUTH": {"DES", "JER"},
          "NORTH": {"GER"}, "TRANSJ": {"PER"}, "SAMDES": {"DES", "GER"}, "WEST": set(), "HEBNEG": set(), "CARMEL": set()}
GENERIC = set("""the of a an and in on at to by near from st saint sainte san santa s
de du des la le les l d au aux et en sur pres a dans
der die das von zu zum zur
fountain fount fontaine fons fonte spring source well wells puits pool pools piscine piscina cistern citerne lake
brook torrent stream river fleuve riviere rivulet water waters aqueduct conduit canal channel
valley vale vallee vallis val wadi wady glen ravine gorge
mount mountain mountains mont montagne mons hill hills colline height heights ridge rock rocks roche pierre stone
tomb tombs tombeau tombeaux sepulchre sepulcher sepulchres sepulcre sepulture grave graves monument mausoleum cave caves caverne grotto grotte spelunca
church churches eglise ecclesia chapel chapelle oratory monastery monastere abbey abbaye convent couvent laura lavra cell cells hermitage
mosque masjid jami mosquee shrine maqam makam mazar kubbet qubbat
town city ville cite civitas village villa casale casal castle chateau castellum castrum fort fortress tower tour turris
gate gates porte porta door bab road way chemin via field fields champ campus garden jardin hortus plain plaine desert wilderness
house maison domus place lieu sea mer mare lake
ain ayn bir wadi jebel jabal tell tall khirbet khirbat kh ras deir dayr kasr qasr birket birkat nahr umm abu ibn ben bar bin beni bani
el al ad ed es esh et en er ez an ar as at az
holy sacred great little greater lesser upper lower old new east west north south eastern western northern southern blessed
lord our lady virgin mary prophet patriarch king queen""".split())
VOWELS = set("aeiou")

def strip_dia(s):
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))

def word_variants(w):
    """M3-M9 on one lower-case ascii word -> list of Palmer-style strings."""
    w = w.replace("ph", "f").replace("qu", "k").replace("dj", "j").replace("sch", "sh").replace("tz", "ts").replace("ck", "k").replace("x", "ks")
    w = w.replace("ou", "u").replace("oo", "u").replace("ee", "i")
    # M8 y as vowel when not next to a vowel
    w = "".join("i" if (c == "y" and not ((i > 0 and w[i - 1] in VOWELS) or (i + 1 < len(w) and w[i + 1] in VOWELS))) else c
                for i, c in enumerate(w))
    outs = [""]
    i = 0
    while i < len(w):
        c = w[i]; nx = w[i + 1] if i + 1 < len(w) else ""
        if c == "c" and nx == "h":
            opts = ["kh", "k", "sh"]; i += 2
        elif c == "t" and nx == "h":
            opts = ["t", "th"]; i += 2
        elif c == "c":
            opts = ["s", "k"] if nx in ("e", "i", "y") else ["k"]; i += 1
        elif c == "j" and i == 0:
            opts = ["j", "y"]; i += 1
        elif c == "g" and nx in ("e", "i"):
            opts = ["g", "j"]; i += 1
        else:
            opts = [c]; i += 1
        outs = [o + p for o in outs for p in opts][:16]
    res = []
    for o in outs:
        res.append(o)
        m = re.match(r"^(beth|beit|bayt|bet)(?=[^aeiou])(.+)$", o)  # M9
        if m and len(m.group(2)) >= 2:
            res.append(m.group(2))
    seen = []
    for r in res:
        if r not in seen:
            seen.append(r)
    return seen[:16]

def name_skeletons(raw):
    s = strip_dia(raw or "").lower()
    s = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", s)
    s = re.sub(r"'s\b|’s\b", " ", s)
    s = s.replace("’", "'").replace("‘", "'").replace("ʿ", "'").replace("ʾ", "'")
    s = re.sub(r"[^a-z' \-]", " ", s)
    toks = [t.strip("'") for t in re.split(r"[ \-]+", s) if t.strip("'")]
    toks = [t for t in toks if t not in GENERIC and len(t) >= 2]
    if not toks:
        return set()
    sk = set()
    seqs = [toks] + ([[t] for t in toks] if len(toks) > 1 else [])
    for ws in seqs[:6]:
        vlists = [word_variants(t) for t in ws]
        combos = [[]]
        for vl in vlists:
            combos = [c + [v] for c in combos for v in vl][:16]
        for c in combos:
            A = []
            for v in c:
                A += lat_tokens(v)
            if A:
                sk.add(tuple(A))
    return sk

def hav(a, b, c, d):
    p = math.pi / 180
    x = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))

def load():
    recs = list(csv.DictReader(open(os.path.join(LANE, "data", "medieval_records_placed.csv"), encoding="utf-8")))
    recs = [r for r in recs if r["primary_layer"] == "True"]
    nc = json.load(open(os.path.join(LANE, "data", "name_constraints.json"), encoding="utf-8"))
    names = {n["id"]: n for n in json.load(open(os.path.join(T01, "data", "scroll_names.json"), encoding="utf-8"))}
    places = {r["place_id"]: r for r in csv.DictReader(open(os.path.join(W2B, "places_v3.csv"), encoding="utf-8"))}
    cand = defaultdict(set)
    for r in csv.DictReader(open(os.path.join(W2B, "candidates_v3.csv"), encoding="utf-8")):
        cand[r["entry"]].add(r["place_id"])
    return recs, nc, names, places, cand

def name_area(nid, names, places, cand):
    ents = [e.strip() for e in names[nid]["entries"].split(",")]
    pts, regs = [], set()
    for e in ents:
        for pid in cand.get(e, ()):
            p = places[pid]
            regs |= REGMAP.get(p["model_region"], set())
            if p["lat"] and p["lon"]:
                pts.append((float(p["lat"]), float(p["lon"]), float(p["sigma_km"] or 0)))
    return pts, regs

def eligible(rec, classes, pts, regs, nc):
    ft = rec["feature_type"]
    ok = False
    for c in classes:
        cl = nc["classes"][c]
        if "*" in cl or ft in cl:
            ok = True
    if not ok:
        return False
    if rec["lat"]:
        la, lo, rad = float(rec["lat"]), float(rec["lon"]), float(rec["radius_km"])
        if any(hav(la, lo, a, b) <= rad + s + SLACK_KM for a, b, s in pts):
            return True
        return False
    return rec["region"] in regs

def rec_skeletons(rec):
    sk = set()
    for part in [rec["name_as_printed"]] + (rec["other_names"] or "").split("|"):
        sk |= name_skeletons(part)
    return sk

G_SK = None; G_RECS = None
def init(sk, recsk):
    global G_SK, G_RECS
    G_SK, G_RECS = sk, recsk

def hits_for(H, rec_ids):
    cache = {}
    out = []
    for i in rec_ids:
        best = 0.0
        for A in G_RECS[i]:
            if A not in cache:
                cache[A] = score(H, list(A))[0]
            if cache[A] > best:
                best = cache[A]
        if best >= THRESH:
            out.append(i)
    return out

def rand_core(pattern, rng, pool):
    strong = sorted(pool); tot = sum(pool.values())
    def draw():
        if rng.random() < 0.5:
            x = rng.random() * tot
            for l in strong:
                x -= pool[l]
                if x <= 0:
                    return l
        return rng.choice(strong)
    return [((draw() if k == "strong" else t), k) for t, k in pattern]

def job(args):
    key, variants, rec_ids, seed, pool = args
    rng = random.Random(seed)
    allhits = set()
    for v in variants:
        H = heb_tokens(v)
        pat = [(("S", "strong") if k == "strong" else (t, k)) for t, k in H]
        Hr = rand_core(pat, rng, pool)
        allhits |= set(hits_for(Hr, rec_ids))
    return key, len(allhits)

def main():
    recs, nc, names, places, cand = load()
    recsk = [rec_skeletons(r) for r in recs]
    nsk = sum(1 for s in recsk if s)
    print("primary-layer records:", len(recs), "with a comparable name:", nsk, "unique skeletons:", len({a for s in recsk for a in s}))
    groups = {}
    for nid in nc["test_names"] + nc["known_survival_names"]:
        pts, regs = name_area(nid, names, places, cand)
        classes = nc["names"][nid]["classes"]
        ids = [i for i, r in enumerate(recs) if recsk[i] and eligible(r, classes, pts, regs, nc)]
        groups[nid] = dict(variants=[v["core"] for v in names[nid]["variants"]], ids=ids, regs=sorted(regs), npts=len(pts),
                           biblical=nc["names"][nid]["biblical"], kind="test" if nid in nc["test_names"] else "known")
    # positive controls and tomb controls: area = control point; feature class ANY (controls) / TOMB (tomb controls)
    for pc in nc["positive_controls_medieval"]:
        pts = [(pc["lat"], pc["lon"], pc["sigma_km"])]
        ids = [i for i, r in enumerate(recs) if recsk[i] and eligible(r, ["ANY"], pts, set(), nc)]
        groups["PC:" + pc["name"]] = dict(variants=[pc["core"]], ids=ids, kind="pc")
    tomb_src = ("adler_", "carmoly_", "benjamin_")
    for tc in nc["tomb_controls"]:
        pts = [(tc["lat"], tc["lon"], tc["sigma_km"])]
        ids = [i for i, r in enumerate(recs) if recsk[i] and r["seg"].startswith(tomb_src) and eligible(r, ["TOMB"], pts, set(), nc)]
        groups["TC:" + tc["name"]] = dict(variants=[tc["core"]], ids=ids, kind="tc")
    for nid in nc["tomb_names"]:
        pts, regs = name_area(nid, names, places, cand)
        ids = [i for i, r in enumerate(recs) if recsk[i] and r["seg"].startswith(tomb_src) and eligible(r, ["TOMB"], pts, regs, nc)]
        groups["TOMB:" + nid] = dict(variants=[v["core"] for v in names[nid]["variants"]], ids=ids, kind="tomb",
                                      biblical=nc["names"][nid]["biblical"])
    for k, g in groups.items():
        print(f"{k:45s} kind={g['kind']:5s} eligible_records={len(g['ids'])}")
    if DRY:
        return
    init(None, recsk)
    pool = Counter()
    for nid in names:
        for v in names[nid]["variants"]:
            for t, k in heb_tokens(v["core"]):
                if k == "strong":
                    pool[t] += 1
    for l in [l for l in sorted(set(HEB_MAP.values())) if l not in ("'", "h", "w", "y")]:
        pool.setdefault(l, 0)
    out = {}
    detail = []
    for k, g in groups.items():
        hs = set()
        for v in g["variants"]:
            H = heb_tokens(v)
            for i in hits_for(H, g["ids"]):
                hs.add(i)
                best = max((score(H, list(A)) for A in recsk[i]), key=lambda x: x[0])
                r = recs[i]
                detail.append(dict(group=k, variant=v, heb=heb_str(H), score=round(best[0], 3), rule_path=" ".join(best[2]),
                                   rec_id=r["rec_id"], name_as_printed=r["name_as_printed"], other_names=r["other_names"],
                                   feature_type=r["feature_type"], region=r["region"], anchor_id=r["anchor_id"],
                                   placement=r["placement_basis"], text=r["text"], year=r["year_used"], page=r["page"],
                                   lines=r["lines"], position_phrase=r["position_phrase"]))
        out[k] = dict(g, obs=len(hs))
    jobs = []
    for gi, (k, g) in enumerate(groups.items()):
        if g["kind"] in ("test", "known", "tomb"):
            for t in range(NRAND):
                jobs.append((k, g["variants"], g["ids"], SEED + 100000 * gi + t, dict(pool)))
    with Pool(2, initializer=init, initargs=(None, recsk)) as P:
        res = P.map(job, jobs, chunksize=8)
    rnd = defaultdict(list)
    for k, n in res:
        rnd[k].append(n)
    rows = []
    for k, g in out.items():
        r = rnd.get(k)
        row = dict(group=k, kind=g["kind"], biblical=g.get("biblical", ""), variants=" ".join(g["variants"]),
                   eligible_records=len(g["ids"]), observed_records=g["obs"])
        if r:
            n = len(r)
            row.update(random_mean=round(sum(r) / n, 3), random_p99=sorted(r)[int(0.99 * (n - 1))],
                       share_random_ge1=round(sum(1 for x in r if x >= 1) / n, 3),
                       p=round((1 + sum(1 for x in r if x >= g["obs"])) / (n + 1), 4), n_random=n)
        rows.append(row)
    # global statistics
    def total(keys):
        T = sum(out[k]["obs"] for k in keys)
        sims = [sum(rnd[k][j] for k in keys) for j in range(NRAND)]
        p99 = sorted(sims)[int(0.99 * (NRAND - 1))]
        p = (1 + sum(1 for s in sims if s >= T)) / (NRAND + 1)
        return dict(observed=T, random_mean=round(sum(sims) / NRAND, 2), random_p99=p99, p=round(p, 4), pass_=T > p99)
    test = [k for k, g in out.items() if g["kind"] == "test"]
    nonbib = [k for k in test if not out[k]["biblical"]]
    tomb = [k for k, g in out.items() if g["kind"] == "tomb"]
    summary = dict(primary_all_test_names=total(test), secondary_nonbiblical=total(nonbib), tomb_subtest=total(tomb),
                   positive_controls_found=[k for k, g in out.items() if g["kind"] == "pc" and g["obs"] > 0],
                   positive_controls_missed=[k for k, g in out.items() if g["kind"] == "pc" and g["obs"] == 0],
                   tomb_controls_found=[k for k, g in out.items() if g["kind"] == "tc" and g["obs"] > 0],
                   tomb_controls_missed=[k for k, g in out.items() if g["kind"] == "tc" and g["obs"] == 0],
                   nrand=NRAND, seed=SEED, thresh=THRESH, slack_km=SLACK_KM, records=len(recs))
    D = os.path.join(LANE, "results"); os.makedirs(D, exist_ok=True)
    with open(os.path.join(D, "group_results.csv"), "w", newline="", encoding="utf-8") as fh:
        keys = sorted({k for r in rows for k in r}, key=lambda x: list(rows[0]).index(x) if x in rows[0] else 99)
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    with open(os.path.join(D, "conjunctive_matches.csv"), "w", newline="", encoding="utf-8") as fh:
        if detail:
            w = csv.DictWriter(fh, fieldnames=list(detail[0])); w.writeheader(); w.writerows(detail)
    json.dump(summary, open(os.path.join(D, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()
