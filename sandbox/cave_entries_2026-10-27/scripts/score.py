"""Steps 3-4 of run 10: score entry x cave pairs, find leads, run the landmark-swap control.

Run: python3 -I score.py   (after build_inventory.py and flags.py)
"""
import csv, itertools, json, math, os, random, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from overrides import O  # noqa: E402

OUT = os.path.join(HERE, "..", "out")
LANE = "/home/claude/copperscroll/research/regional/caves_entry25"

PLACES = {  # lat, lon, sigma_m (places.csv / places_v2)
    "jer_temple": (31.77825, 35.23534, 150), "kh_qumran": (31.74183, 35.45941, 100),
    "abu_saraj_iv17": (31.89009, 35.42477, 300), "jericho_area": (31.85611, 35.46306, 3000),
    "tell_el_qos": (31.8551, 35.4656, 200), "natuf": (31.64436, 35.23543, 700),
}
# Window-period buildings (Milik 'vicinity' branch) and those with a bath (Puech 'cool room').
BUILDINGS = {"jericho_palaces": (31.85187, 35.43624, 300, True), "kh_qumran": (31.74183, 35.45941, 100, False),
             "ein_feshkha": (31.71444, 35.45333, 500, False), "jer_temple": (31.77825, 35.23534, 150, False),
             "hyrcania": (31.719, 35.366, 200, False)}
SPRINGS = {"natuf": (31.64436, 35.23543, 700), "ain_duk": (31.8976, 35.4177, 300), "tell_es_sultan": (31.8717, 35.4446, 150),
           "ein_feshkha": (31.71444, 35.45333, 500), "jer_siloam": (31.77008, 35.23616, 300), "jer_bir_ayyub": (31.7672, 35.23599, 100)}
ENTRY_PLACES = {"7": ["jer_temple"], "22": ["kh_qumran"], "25": ["kh_qumran", "abu_saraj_iv17"], "26": ["kh_qumran"],
                "30": ["jericho_area", "tell_el_qos"], "38": ["natuf"]}
ENTRIES = ["7", "22", "25", "26", "30", "38"]
GENERIC = {"E7.C", "E25.C1", "E26.X", "E38.C"}
ITEMS = {"E7.I", "E22.I", "E25.I", "E26.I", "E30.I", "E38.I"}
DEPTH = {"E25.D", "E26.D", "E30.D", "E38.D"}


def dist(a, b):
    la1, lo1 = map(math.radians, a[:2]); la2, lo2 = map(math.radians, b[:2])
    return 6371000.0 * math.hypot((lo2 - lo1) * math.cos((la1 + la2) / 2), la2 - la1)


def bearing(a, b):
    la1, lo1 = map(math.radians, a[:2]); la2, lo2 = map(math.radians, b[:2])
    return (math.degrees(math.atan2((lo2 - lo1) * math.cos((la1 + la2) / 2), la2 - la1)) + 360) % 360


def within(d, s, R):
    if d + s <= R:
        return "pass"
    if d - s > R:
        return "fail"
    return "unknown"


def east_of(ref, cave, sc):
    d = dist(ref, cave); s = ref[2] + sc
    if d <= s:
        return "unknown"
    b = bearing(ref, cave); h = math.degrees(math.atan2(s, d))
    n = max(2, int(2 * h / 0.25) + 1)
    ins = [45 <= ((b - h + 2 * h * i / (n - 1)) % 360) <= 135 for i in range(n)]
    if all(ins):
        return "pass"
    if not any(ins):
        return "fail"
    return "unknown"


def load():
    rows = {r["cave_id"]: r for r in json.load(open(os.path.join(OUT, "all_rows.json"), encoding="utf-8"))}
    inv = list(csv.DictReader(open(os.path.join(OUT, "inventory.csv"), encoding="utf-8")))
    lane = defaultdict(dict)
    for fn in ("scores.csv", "iaa_scores.csv", "phase4_scores.csv"):
        for s in csv.DictReader(open(os.path.join(LANE, fn), encoding="utf-8")):
            if s["ruleset"] == "primary":
                lane[s["cave_id"]][(s["branch"], s["orientation"])] = s
    return rows, inv, lane


V = {"match": "pass", "fail": "fail", "unknown": "unknown"}


class Cave:
    def __init__(self, cid, row, lane, setting):
        self.id, self.r, self.lane, self.setting = cid, row, lane, setting
        self.p = (float(row["lat"]), float(row["lon"]))
        self.s = float(row.get("precision_m") or 100)
        self.asi = row["_src"] == "asi_jerusalem"
        self.kind = row["_kind"]
        self.o = O.get(cid, {})
        self.cls = set((row.get("asi_classes") or "").split(";")) if self.asi else set()

    def flag(self, k, asi_class=None):
        v = self.o.get(k)
        if v is True:
            return "pass"
        if v == "lenient" or (self.asi and asi_class and asi_class in self.cls):
            return "pass" if self.setting == "lenient" else "unknown"
        return "unknown"

    def generic(self):
        if self.kind == "fissure":
            return "unknown"
        return "pass"

    def lane_c(self, branch, level, c):
        s = self.lane.get((branch, level))
        if not s:
            return "pass" if (c == "c1" and not self.kind == "fissure") else "unknown"
        return V[s[c]]

    def j7(self):
        if self.asi:
            v = self.r.get("asi_cave_dated_in_window", "")
            if v == "yes":
                return "pass"
            if v == "partly" and self.setting == "lenient":
                return "pass"
            if v == "no" and self.setting == "survey_fail":
                return "fail"
            return "unknown"
        if self.kind == "fissure":
            # DJD III fissures: Qumran-type / Herodian finds (extraction); A41 clefts: no period recorded
            return "pass" if self.id in ("DJD3:9", "DJD3:15", "DJD3:17", "DJD3:21", "DJD3:30") else "unknown"
        v = self.r.get("period_in_window", "")
        ex = (self.r.get("excavation_status", "") or "").lower()
        if v.startswith("yes"):
            return "pass"
        if v == "partly":
            return "pass" if self.setting == "lenient" else "unknown"
        if v == "no":
            if self.setting == "survey_fail" or "excavat" in ex or "sound" in ex:
                return "fail"
            return "unknown"
        return "unknown"


# ---------- landmark bundles (each returns {branch_name: {constraint: score}}) ----------

def L7(c, ref):
    return {"-": {"E7.L": c.flag("building", "building")}}


def L22(c, ref):
    out = {}
    for name, R in (("S500", 500), ("S2km", 2000)):
        out[name] = {"E22.S": within(dist(ref, c.p), c.s + ref[2], R), "E22.E": east_of(ref, c.p, c.s)}
    return out


def L25(c, ref):
    return {"PILLAR": {"E25.P": c.lane_c("B-PILLAR", "cave", "c2")}, "TERRACE": {"E25.P": c.lane_c("B-TERRACE", "cave", "c2")}}


def L26(c, ref):
    return {"-": {"E26.L": c.flag("heap", "cairn")}}


def L30(c, ref):
    res = {}
    for name, R, need_bath in (("Puech100", 100, True), ("Milik500", 500, False)):
        best = "unknown"
        for b in BUILDINGS.values():
            if need_bath and not b[3]:
                continue
            v = within(dist(b, c.p), c.s + b[2], R)
            if v == "pass":
                best = "pass"; break
        res[name] = {"E30.L": best}
    return res


def L38(c, ref):
    if c.o.get("spring") is True:
        return {"-": {"E38.P": "pass"}}
    v = within(dist(ref, c.p), c.s + ref[2], 50)  # fail if > 500 m: handled below
    d = dist(ref, c.p)
    if d - c.s - ref[2] > 500:
        v = "fail"
    elif v != "pass":
        v = "pass" if (c.asi and "spring_well" in c.cls and c.setting == "lenient") else "unknown"
    return {"-": {"E38.P": v}}


LANDMARK = {"7": L7, "22": L22, "25": L25, "26": L26, "30": L30, "38": L38}


def landmark_ref(lm_entry, c, own_entry):
    """Reference point for a positional landmark of entry lm_entry applied to cave c of own_entry."""
    if lm_entry == "22":
        pl = min(ENTRY_PLACES[own_entry], key=lambda k: dist(PLACES[k], c.p))
        return PLACES[pl]
    if lm_entry == "38":
        if own_entry == "38":
            return SPRINGS["natuf"]
        return min(SPRINGS.values(), key=lambda s: dist(s, c.p))
    return None


# ---------- non-landmark constraints of each entry ----------

def body(e, c):
    """Returns {branch: {constraint: score}}."""
    if e == "7":
        return {"-": {"E7.C": c.generic(), "E7.R": c.flag("three"), "E7.I": c.flag("gold_bars")}}
    if e == "22":
        f = "pass" if c.kind == "fissure" else c.flag("fissure")
        it = "pass" if (c.flag("vessels") == "pass" and c.flag("written", "inscription") == "pass") else "unknown"
        return {"-": {"E22.F": f, "E22.I": it}}
    if e == "25":
        out = {}
        for br in ("B-PILLAR", "B-TERRACE"):
            for lv in ("cave", "both-mouths"):
                out[f"{br}/{lv}"] = {"E25.C1": c.lane_c(br, lv, "c1"), "E25.2": c.lane_c(br, lv, "c3"),
                                      "E25.E": c.lane_c(br, lv, "c4"), "E25.N": c.lane_c(br, lv, "c5"),
                                      "E25.D": "unknown",
                                      "E25.I": "pass" if (c.flag("jar") == "pass" and c.flag("scroll") == "pass") else "unknown"}
        return out
    if e == "26":
        return {"F-cave": {"E26.F": c.lane_c("B-PILLAR", "cave", "c4"), "E26.X": c.generic(), "E26.D": "unknown", "E26.I": c.flag("coins")},
                "F-landmark": {"E26.F": "unknown", "E26.X": c.generic(), "E26.D": "unknown", "E26.I": c.flag("coins")}}
    if e == "30":
        return {"-": {"E30.D": "unknown", "E30.I": c.flag("silver")}}
    if e == "38":
        return {"-": {"E38.C": c.generic(), "E38.D": "unknown", "E38.I": c.flag("coins")}}


def lead_status(sc, items_specific=False):
    vals = sc.items()
    if any(v == "fail" for k, v in vals):
        return None
    npass = [k for k, v in vals if v == "pass" and k != "J7"]
    spec = [k for k in npass if k not in GENERIC and k not in DEPTH and (items_specific or k not in ITEMS)]
    prim = len(npass) >= 2 and len(spec) >= 1
    strict = len(spec) >= 2
    return prim, strict


def score_pair(e, lm, c, own_entry):
    """Entry e's body with landmark bundle of entry lm, on cave c of inventory own_entry."""
    ref = landmark_ref(lm, c, own_entry)
    lmb = LANDMARK[lm](c, ref)
    bd = body(e, c)
    j7 = c.j7()
    combos = []
    for (bn, bsc), (ln, lsc) in itertools.product(bd.items(), lmb.items()):
        sc = dict(bsc); sc.update(lsc); sc["J7"] = j7
        combos.append((f"{bn}|{ln}", sc))
    return combos


def best(combos, items_specific=False):
    """Best branch combination: lead(primary) > lead(strict) ordering; else fewest fails, most passes."""
    def key(item):
        name, sc = item
        st = lead_status(sc, items_specific)
        nf = sum(v == "fail" for v in sc.values()); npas = sum(v == "pass" for v in sc.values())
        return ((st[1] if st else False), (st[0] if st else False), -nf, npas)
    return max(combos, key=key)


def run(assign, caves_by_entry, entries, items_specific=False):
    """assign: entry -> landmark entry. Returns lead lists."""
    leads_p, leads_s, table = [], [], []
    for e in entries:
        for c in caves_by_entry[e]:
            combos = score_pair(e, assign[e], c, e)
            name, sc = best(combos, items_specific)
            st = lead_status(sc, items_specific)
            table.append((e, assign[e], c.id, name, sc, st, combos))
            if st and st[0]:
                leads_p.append((e, c.id))
            if st and st[1]:
                leads_s.append((e, c.id))
    return leads_p, leads_s, table


def derangements(entries, n, seed):
    rng = random.Random(seed); out = []
    while len(out) < n:
        p = entries[:]; rng.shuffle(p)
        if all(a != b for a, b in zip(entries, p)):
            out.append(dict(zip(entries, p)))
    return out


def main():
    rows, inv, lane = load()
    results = {}
    for setting in ("strict", "lenient", "survey_fail"):
        caves_by_entry = defaultdict(list)
        for x in inv:
            r = rows[x["cave_id"]]
            caves_by_entry[x["entry"]].append(Cave(x["cave_id"], r, lane.get(x["cave_id"], {}), setting))
        for label, entries in (("six", ENTRIES), ("five", [e for e in ENTRIES if e != "38"])):
            ident = {e: e for e in entries}
            for items_spec in (False, True):
                lp, ls, table = run(ident, caves_by_entry, entries, items_spec)
                swaps = derangements(entries, 10, 20261027)
                sw = []
                for a in swaps:
                    sp, ss, _ = run(a, caves_by_entry, entries, items_spec)
                    sw.append({"assign": a, "n_primary": len(sp), "n_strict": len(ss), "leads_primary": sp, "leads_strict": ss,
                               "entries_with_lead": len({e for e, _ in sp}),
                               "per_entry_primary": dict(Counter(e for e, _ in sp)), "per_entry_strict": dict(Counter(e for e, _ in ss))})
                key = f"{setting}|{label}|items_specific={items_spec}"
                pp = (1 + sum(s["n_primary"] >= len(lp) for s in sw)) / 11
                ps = (1 + sum(s["n_strict"] >= len(ls) for s in sw)) / 11
                ne = len({e for e, _ in lp})
                pe = (1 + sum(s["entries_with_lead"] >= ne for s in sw)) / 11
                results[key] = {"per_entry_primary": dict(Counter(e for e, _ in lp)), "per_entry_strict": dict(Counter(e for e, _ in ls)),
                                "real_primary": lp, "real_strict": ls, "n_real_primary": len(lp), "n_real_strict": len(ls),
                                "entries_with_lead": ne, "p_primary": round(pp, 3), "p_strict": round(ps, 3), "p_entries": round(pe, 3),
                                "swaps": sw}
                if setting == "strict" and label == "six" and not items_spec:
                    write_table(table, "pairs_strict.csv")
                if setting == "lenient" and label == "six" and not items_spec:
                    write_table(table, "pairs_lenient.csv")
    # all-pairs alternative (every entry x every inventory cave; real landmarks)
    for setting in ("strict", "lenient"):
        allc = {}
        for x in inv:
            allc.setdefault(x["cave_id"], Cave(x["cave_id"], rows[x["cave_id"]], lane.get(x["cave_id"], {}), setting))
        lp = []
        for e in ENTRIES:
            for c in allc.values():
                own = e  # positional landmarks resolved to the entry's own candidate places
                name, sc = best(score_pair(e, e, c, own))
                st = lead_status(sc)
                if st and st[0]:
                    lp.append((e, c.id, name))
        results[f"allpairs|{setting}"] = {"n": len(lp), "leads": lp}
    json.dump(results, open(os.path.join(OUT, "results.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k, v in results.items():
        if k.startswith("allpairs"):
            print(k, v["n"], v["leads"][:40])
        else:
            print(k, "real P/S:", v["n_real_primary"], v["n_real_strict"], "entries", v["entries_with_lead"],
                  "swaps P:", [s["n_primary"] for s in v["swaps"]], "S:", [s["n_strict"] for s in v["swaps"]],
                  "p:", v["p_primary"], v["p_strict"], v["p_entries"])


def write_table(table, fn):
    cols = ["entry", "landmark", "cave_id", "best_branch", "lead_primary", "lead_strict", "n_pass", "n_fail", "n_unknown", "fails", "passes", "scores"]
    with open(os.path.join(OUT, fn), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for e, lm, cid, name, sc, st, _ in table:
            w.writerow([e, lm, cid, name, bool(st and st[0]), bool(st and st[1]),
                        sum(v == "pass" for v in sc.values()), sum(v == "fail" for v in sc.values()), sum(v == "unknown" for v in sc.values()),
                        ";".join(k for k, v in sc.items() if v == "fail"), ";".join(k for k, v in sc.items() if v == "pass"),
                        json.dumps(sc)])
    with open(os.path.join(OUT, fn.replace(".csv", "_all_branches.csv")), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["entry", "landmark", "cave_id", "branch", "lead_primary", "lead_strict", "fails", "passes", "scores"])
        for e, lm, cid, name, sc, st, combos in table:
            for bn, bsc in combos:
                bs = lead_status(bsc)
                w.writerow([e, lm, cid, bn, bool(bs and bs[0]), bool(bs and bs[1]), ";".join(k for k, v in bsc.items() if v == "fail"),
                            ";".join(k for k, v in bsc.items() if v == "pass"), json.dumps(bsc)])


if __name__ == "__main__":
    main()
