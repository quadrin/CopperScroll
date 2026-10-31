#!/usr/bin/env python3
"""Lane I2 matcher. Lane I's frozen matcher (I/scripts/medieval_match.py) is imported and used UNCHANGED for:
T01 scorer and sound rules, THRESH 0.75, SLACK_KM 5, NRAND 200, SEED 20261030, rendering rules M1-M9
(name_skeletons), feature classes and position rule (eligible, name_area), random-core construction (rand_core),
consonant pool, group definitions, pass marks, and lane I's data/name_constraints.json (read from lane I's folder).
Additions (lane I2 protocol, fixed before matching):
 HS  Hebrew-script names (any Hebrew letter in the string) are mapped to the scorer's Arabic-token alphabet by
     heb_record_skeletons() below (rules HS1-HS6). Latin-script strings use lane I name_skeletons() unchanged.
 K1  Khitrowo records (seg kh_*): each Latin string is also scored with every 'f' that is followed by a letter
     replaced by 's' (OCR of the long s); both forms are kept.
 D1  Huetteroth records (seg hutt_*): before lane I name_skeletons(), DMG letters are rewritten
     (š->sh, ġ->gh, ḫ->kh, ṯ->th, ḏ->dh, ž->j; OCR '$'->sh), an OCR '7' or '*' or '£' directly before a letter at
     word start -> "'" (ʿayn), other non-letter OCR noise removed, and DMG generic words are removed
     (DMG_GENERIC below), in addition to lane I's GENERIC list.
 T1  Tomb sub-test and tomb controls: the Jewish source of this layer is Kaftor va-Ferach (seg 'kaftor'); lane I
     used Adler/Carmoly/Benjamin. Same TOMB feature class and areas.
 P   Pooled layer = all three sources (primary result). Per-source counts (kaftor, khitrowo, hutteroth) are
     descriptive only; they reuse the same random cores (same seeds), restricted to that source's records.
Usage: NRAND=200 python3 -I medieval_match_i2.py I2_DIR LANE_I_DIR T01_DIR W2B_INPUTS_DIR [--dry]
"""
import sys, os, csv, json, re, unicodedata, random
from collections import defaultdict, Counter
from multiprocessing import Pool
I2, LANEI, T01, W2B = sys.argv[1:5]
DRY = "--dry" in sys.argv
_argv = sys.argv
sys.argv = [os.path.join(LANEI, "scripts", "medieval_match.py"), LANEI, T01, W2B]
sys.path.insert(0, os.path.join(LANEI, "scripts"))
import medieval_match as mm          # lane I module, unchanged (its main() is not run)
sys.argv = _argv
from toponym import heb_tokens, score, heb_str, HEB_MAP

# ---------------- HS: Hebrew-script record names -> scorer tokens ----------------
# HS1 strip niqqud/cantillation; geresh (׳ ' `) after ג ח ד ת ט צ ע כ marks an Arabic letter (HS2).
# HS2 letter map (record side, scorer Arabic-token alphabet of T01 lat_tokens):
#     א dropped (vowel letter / hamza; lat_tokens drops vowels); ב b; ג g; ג׳ j; ד d; ד׳ D; ה h (final ה -> E, A3);
#     ו w; ז z; ח h; ח׳ X; ט t; ט׳ D; י y; כ ך k; כ׳ X; ל l; מ ם m; נ ן n; ס s; ע 3; ע׳ G; פ ף f; צ ץ s; צ׳ D;
#     ק k; ר r; ש S; ת t; ת׳ T.
# HS3 words split on space, maqaf, hyphen, slash; Hebrew generic words (HEB_GENERIC) removed; every remaining word
#     and the whole remaining phrase are compared (as lane I M2), max 6 sequences.
# HS4 a word beginning with the article ה (len >= 3 letters after it) also gets a variant without it; a word
#     beginning with Arabic article אל (len >= 2 after it) also gets a variant without it.
# HS5 adjacent identical tokens collapse (A4), as lat_tokens.
# HS7 vowel letters: a single ו or י that is not the first letter of the word is a vowel letter (plene spelling) and
#     is dropped, as lat_tokens drops Latin vowels; a doubled וו / יי is the consonant w / y (one token).
# HS6 Latin-script parts of other_names go through lane I rules; the extractor's 'translit' field is NOT scored.
HMAP = {"א": "", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "w", "ז": "z", "ח": "h", "ט": "t", "י": "y", "כ": "k",
        "ך": "k", "ל": "l", "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "3", "פ": "f", "ף": "f", "צ": "s",
        "ץ": "s", "ק": "k", "ר": "r", "ש": "S", "ת": "t"}
HGER = {"ג": "j", "ד": "D", "ח": "X", "ט": "D", "כ": "X", "ע": "G", "צ": "D", "ץ": "D", "ת": "T"}
HEB_GENERIC = set("""עין עיין עינות באר בארות בור בורות מעין מעיין מעינות נחל נחלי עמק עמקי בקעה בקעת הר הרי הרים גבעת גבעה
תל תלי מערת מערה מערות קבר קברי קברות קבורת ציון כפר מגדל ברכת ברכה בריכת בריכה נהר נהרות ים מדבר ואדי גבל ג׳בל ביר
חרבת חרבה ח׳רבת ח׳רבה כרבת דיר ראס אבו אם אום אל של את על אצל בין עיר כרך מקום שער שערי דרך שדה שדות ארץ גבול מערב מזרח
צפון דרום מערבי מזרחי צפוני דרומי עליון עליונה תחתון תחתונה גדול גדולה קטן קטנה ישן חדש הוא היא הם אשר שהוא שהיא היום עתה
עכשיו נקרא נקראת נקראים שקורין שקורים קורין קורים שנקרא הנקרא הנקראת והוא רבי ר׳ רבנו הנביא הקדוש הצדיק
אבן סלע מצודת מבצר חומת חומה מגדל עד מן""".split())
HEB_LET = re.compile(r"[א-ת]")
def heb_word_tokens(w):
    w = "".join(c for c in unicodedata.normalize("NFKD", w) if not unicodedata.combining(c))
    toks = []
    i = 0
    first = True
    while i < len(w):
        c = w[i]
        g = i + 1 < len(w) and w[i + 1] in "׳'`’"
        if c in "וי" and not first:  # HS7
            if i + 1 < len(w) and w[i + 1] == c:
                toks.append(HMAP[c]); i += 2
            else:
                i += 1
            continue
        if c in HMAP:
            first = False
            t = HGER.get(c) if (g and c in HGER) else HMAP[c]
            if t:
                toks.append(t)
            i += 2 if g else 1
        else:
            i += 1
    if len(toks) >= 2 and toks[-1] == "h" and w.rstrip("׳'`’")[-1:] == "ה":
        toks[-1] = "E"
    out = []
    for t in toks:
        if out and out[-1] == t:
            continue
        out.append(t)
    return out
def heb_word_variants(w):
    vs = [w]
    if w.startswith("ה") and len(HEB_LET.findall(w)) >= 4:
        vs.append(w[1:])
    if w.startswith("אל") and len(HEB_LET.findall(w)) >= 4:
        vs.append(w[2:])
    return vs
def heb_record_skeletons(raw):
    s = re.sub(r"[\[\]\(\)\"״.,;:!?]", " ", raw or "")
    toks = [t for t in re.split(r"[\s\-־/]+", s) if HEB_LET.search(t)]
    toks = [t for t in toks if t.strip("׳'") not in HEB_GENERIC and len(HEB_LET.findall(t)) >= 2]
    if not toks:
        return set()
    seqs = [toks] + ([[t] for t in toks] if len(toks) > 1 else [])
    sk = set()
    for ws in seqs[:6]:
        combos = [[]]
        for w in ws:
            combos = [c + [v] for c in combos for v in heb_word_variants(w)][:16]
        for c in combos:
            A = []
            for v in c:
                A += heb_word_tokens(v)
            # A4 across word joins
            B = []
            for t in A:
                if B and B[-1] == t:
                    continue
                B.append(t)
            if B:
                sk.add(tuple(B))
    return sk
# ---------------- D1: DMG (Huetteroth) ----------------
DMG_GENERIC = set("""hirbat hirbet khirbat hirba mazra mazraa mazraat mazra'a mazra'at kafr kefr fawqa fauqa fawqani tahta tahtani
sufla ulya kabira kabir sagira saghira qibliyya qibli sarqiyya sharqi garbi gharbi wa dir nazd qarya nahiya maqam nabi sayh shaykh
ard yali hali gawr ghawr tayifat urban""".split())
def dmg_prepare(s):
    s = s.replace("š", "sh").replace("Š", "Sh").replace("ġ", "gh").replace("ḫ", "kh").replace("Ḫ", "Kh").replace("ṯ", "th")
    s = s.replace("ḏ", "dh").replace("ž", "j").replace("$", "sh")
    s = re.sub(r"(?:(?<=\s)|^)[7*£#®]+(?=[A-Za-zÀ-ÿ])", "'", s)
    s = re.sub(r"[^\w'’ʿʾ\- ]|\d", " ", s)
    words = [w for w in re.split(r"[ \-]+", s) if w and mm.strip_dia(w).lower().replace("’", "'").strip("'") not in DMG_GENERIC]
    return " ".join(words)
def latin_skeletons(part, seg):
    forms = [part]
    if seg.startswith("hutt"):
        forms = [dmg_prepare(part)]
    if seg.startswith("kh_"):
        forms.append(re.sub(r"f(?=[a-zéèêàâîôûç])", "s", part))
    sk = set()
    for f in forms:
        sk |= mm.name_skeletons(f)
    return sk
def rec_skeletons(rec):
    sk = set()
    for part in [rec["name_as_printed"]] + (rec["other_names"] or "").split("|"):
        if HEB_LET.search(part or ""):
            sk |= heb_record_skeletons(part)
        else:
            sk |= latin_skeletons(part, rec["seg"])
    return sk
def source_of(seg):
    return "kaftor" if seg == "kaftor" else ("khitrowo" if seg.startswith("kh_") else "hutteroth")
# ---------------- random job returning hit ids (same construction as lane I job) ----------------
def job_ids(args):
    key, variants, rec_ids, seed, pool = args
    rng = random.Random(seed)
    allhits = set()
    for v in variants:
        H = heb_tokens(v)
        pat = [(("S", "strong") if k == "strong" else (t, k)) for t, k in H]
        Hr = mm.rand_core(pat, rng, pool)
        allhits |= set(mm.hits_for(Hr, rec_ids))
    return key, sorted(allhits)
def main():
    recs = [r for r in csv.DictReader(open(os.path.join(I2, "data", "records_i2_placed.csv"), encoding="utf-8")) if r["primary_layer"] == "True"]
    nc = json.load(open(os.path.join(LANEI, "data", "name_constraints.json"), encoding="utf-8"))
    names = {n["id"]: n for n in json.load(open(os.path.join(T01, "data", "scroll_names.json"), encoding="utf-8"))}
    places = {r["place_id"]: r for r in csv.DictReader(open(os.path.join(W2B, "places_v3.csv"), encoding="utf-8"))}
    cand = defaultdict(set)
    for r in csv.DictReader(open(os.path.join(W2B, "candidates_v3.csv"), encoding="utf-8")):
        cand[r["entry"]].add(r["place_id"])
    recsk = [rec_skeletons(r) for r in recs]
    src = [source_of(r["seg"]) for r in recs]
    print("primary-layer records:", len(recs), Counter(src), "with a comparable name:", sum(1 for s in recsk if s),
          "unique skeletons:", len({a for s in recsk for a in s}))
    groups = {}
    for nid in nc["test_names"] + nc["known_survival_names"]:
        pts, regs = mm.name_area(nid, names, places, cand)
        ids = [i for i, r in enumerate(recs) if recsk[i] and mm.eligible(r, nc["names"][nid]["classes"], pts, regs, nc)]
        groups[nid] = dict(variants=[v["core"] for v in names[nid]["variants"]], ids=ids, biblical=nc["names"][nid]["biblical"],
                           kind="test" if nid in nc["test_names"] else "known")
    for pc in nc["positive_controls_medieval"]:
        pts = [(pc["lat"], pc["lon"], pc["sigma_km"])]
        ids = [i for i, r in enumerate(recs) if recsk[i] and mm.eligible(r, ["ANY"], pts, set(), nc)]
        groups["PC:" + pc["name"]] = dict(variants=[pc["core"]], ids=ids, kind="pc")
    tomb_src = ("kaftor",)  # T1
    for tc in nc["tomb_controls"]:
        pts = [(tc["lat"], tc["lon"], tc["sigma_km"])]
        ids = [i for i, r in enumerate(recs) if recsk[i] and r["seg"].startswith(tomb_src) and mm.eligible(r, ["TOMB"], pts, set(), nc)]
        groups["TC:" + tc["name"]] = dict(variants=[tc["core"]], ids=ids, kind="tc")
    for nid in nc["tomb_names"]:
        pts, regs = mm.name_area(nid, names, places, cand)
        ids = [i for i, r in enumerate(recs) if recsk[i] and r["seg"].startswith(tomb_src) and mm.eligible(r, ["TOMB"], pts, regs, nc)]
        groups["TOMB:" + nid] = dict(variants=[v["core"] for v in names[nid]["variants"]], ids=ids, kind="tomb",
                                      biblical=nc["names"][nid]["biblical"])
    for k, g in groups.items():
        print(f"{k:45s} kind={g['kind']:5s} eligible_records={len(g['ids'])} " +
              " ".join(f"{s}={sum(1 for i in g['ids'] if src[i] == s)}" for s in ("kaftor", "khitrowo", "hutteroth")))
    if DRY:
        return
    mm.init(None, recsk)
    pool = Counter()
    for nid in names:
        for v in names[nid]["variants"]:
            for t, k in heb_tokens(v["core"]):
                if k == "strong":
                    pool[t] += 1
    for l in [l for l in sorted(set(HEB_MAP.values())) if l not in ("'", "h", "w", "y")]:
        pool.setdefault(l, 0)
    obs, detail = {}, []
    for k, g in groups.items():
        hs = set()
        for v in g["variants"]:
            H = heb_tokens(v)
            for i in mm.hits_for(H, g["ids"]):
                hs.add(i)
                best = max((score(H, list(A)) for A in recsk[i]), key=lambda x: x[0])
                r = recs[i]
                detail.append(dict(group=k, variant=v, heb=heb_str(H), score=round(best[0], 3), rule_path=" ".join(best[2]),
                                   source=src[i], rec_id=r["rec_id"], name_as_printed=r["name_as_printed"], translit=r.get("translit", ""),
                                   other_names=r["other_names"], feature_type=r["feature_type"], region=r["region"],
                                   anchor_id=r["anchor_id"], placement=r["placement_basis"], text=r["text"], year=r["year_used"],
                                   page=r["page"], lines=r["lines"], position_phrase=r["position_phrase"]))
        obs[k] = hs
    jobs = []
    for gi, (k, g) in enumerate(groups.items()):
        if g["kind"] in ("test", "known", "tomb"):
            for t in range(mm.NRAND):
                jobs.append((k, g["variants"], g["ids"], mm.SEED + 100000 * gi + t, dict(pool)))
    with Pool(2, initializer=mm.init, initargs=(None, recsk)) as P:
        res = P.map(job_ids, jobs, chunksize=8)
    rnd = defaultdict(list)
    for k, ids in res:
        rnd[k].append(ids)
    SUBS = {"pooled": None, "kaftor": "kaftor", "khitrowo": "khitrowo", "hutteroth": "hutteroth"}
    def cnt(ids, sub):
        return len(ids) if sub is None else sum(1 for i in ids if src[i] == sub)
    D = os.path.join(I2, "results"); os.makedirs(D, exist_ok=True)
    rows, summary = [], {}
    for sname, sub in SUBS.items():
        for k, g in groups.items():
            o = cnt(obs[k], sub)
            row = dict(subset=sname, group=k, kind=g["kind"], biblical=g.get("biblical", ""), variants=" ".join(g["variants"]),
                       eligible_records=cnt(g["ids"], sub), observed_records=o)
            if k in rnd:
                r = [cnt(x, sub) for x in rnd[k]]
                n = len(r)
                row.update(random_mean=round(sum(r) / n, 3), random_p99=sorted(r)[int(0.99 * (n - 1))],
                           share_random_ge1=round(sum(1 for x in r if x >= 1) / n, 3),
                           p=round((1 + sum(1 for x in r if x >= o)) / (n + 1), 4), n_random=n)
            rows.append(row)
        def total(keys):
            T = sum(cnt(obs[k], sub) for k in keys)
            sims = [sum(cnt(rnd[k][j], sub) for k in keys) for j in range(mm.NRAND)]
            p99 = sorted(sims)[int(0.99 * (mm.NRAND - 1))]
            p = (1 + sum(1 for s in sims if s >= T)) / (mm.NRAND + 1)
            return dict(observed=T, random_mean=round(sum(sims) / mm.NRAND, 2), random_p99=p99, p=round(p, 4), pass_=T > p99)
        test = [k for k, g in groups.items() if g["kind"] == "test"]
        nonbib = [k for k in test if not groups[k]["biblical"]]
        tomb = [k for k, g in groups.items() if g["kind"] == "tomb"]
        summary[sname] = dict(primary_all_test_names=total(test), secondary_nonbiblical=total(nonbib), tomb_subtest=total(tomb),
                              positive_controls_found=[k for k, g in groups.items() if g["kind"] == "pc" and cnt(obs[k], sub) > 0],
                              positive_controls_missed=[k for k, g in groups.items() if g["kind"] == "pc" and cnt(obs[k], sub) == 0],
                              tomb_controls_found=[k for k, g in groups.items() if g["kind"] == "tc" and cnt(obs[k], sub) > 0],
                              tomb_controls_missed=[k for k, g in groups.items() if g["kind"] == "tc" and cnt(obs[k], sub) == 0],
                              records=len(recs) if sub is None else sum(1 for s in src if s == sub))
    summary["params"] = dict(nrand=mm.NRAND, seed=mm.SEED, thresh=mm.THRESH, slack_km=mm.SLACK_KM)
    with open(os.path.join(D, "group_results.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) + [c for c in ("random_mean", "random_p99", "share_random_ge1", "p", "n_random") if c not in rows[0]])
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(D, "conjunctive_matches.csv"), "w", newline="", encoding="utf-8") as fh:
        if detail:
            w = csv.DictWriter(fh, fieldnames=list(detail[0])); w.writeheader(); w.writerows(detail)
    json.dump(summary, open(os.path.join(D, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))
if __name__ == "__main__":
    main()
