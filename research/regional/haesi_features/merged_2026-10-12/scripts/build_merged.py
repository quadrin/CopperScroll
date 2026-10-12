#!/usr/bin/env python3
"""Build the merged, deduplicated regional inventory over phases 1, 2, 3 A-D and 4 E-I.

Rules: ../merged_2026-10-11/DEDUPE_PLAN.md (frozen; JSON parameters read from it), ../merged_2026-10-11/AMENDMENTS.md (A1-A4)
and ../PLAN_EXTENSION.md (frozen phase-4 extension; JSON parameters read from it); AMENDMENTS.md in this lane if present.
Inputs are read only. Standard library only (zones re-implemented from the phase-2 PLAN.md JSON block).

Usage (from anywhere):
    python3 -I research/regional/haesi_features/merged_2026-10-12/scripts/build_merged.py [OUT_DIR] [--phases13]
OUT_DIR defaults to the lane folder (merged_2026-10-12/). --phases13 builds phases 1-3 only with the 88 frozen manual
decisions; it must reproduce ../merged_2026-10-11 (checked by the tests).
"""
import csv
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
HAESI = LANE.parent
REPO = HAESI.parents[2]
OLD = HAESI / "merged_2026-10-11"
PLAN = OLD / "DEDUPE_PLAN.md"
EXT = LANE / "PLAN_EXTENSION.md"
EXT_FREEZE_COMMIT = "f596618"
PHASE2_PLAN = HAESI / "phase2_2026-10-10" / "PLAN.md"
PLACES = REPO / "research" / "agent_review_2026-10-07" / "wave2" / "W2B_model_v1" / "inputs_v2" / "places_v2.csv"
PHASE1_XWALK = HAESI / "phase2_2026-10-10" / "phase1_zone_crosswalk.csv"
PARTB_XWALK = HAESI / "phase3_2026-10-11" / "part_b" / "already_coded_crosswalk.csv"
MANUAL = LANE / "data" / "manual_decisions.csv"
MANUAL_OLD = OLD / "data" / "manual_decisions.csv"
OLD_FEATURES = OLD / "features_all.csv"
OLD_GROUPS = OLD / "report_groups.csv"

FEATURE_SOURCES13 = [
    ("1", "features.csv"),
    ("1", "features_unlocated.csv"),
    ("2", "phase2_2026-10-10/features.csv"),
    ("3A", "phase3_2026-10-11/part_a/features.csv"),
    ("3B", "phase3_2026-10-11/part_b/features.csv"),
    ("3C", "phase3_2026-10-11/part_c/features.csv"),
    ("3D", "phase3_2026-10-11/part_d_online/features.csv"),
]
REPORT_SOURCES13 = [
    ("1", "reports.csv"),
    ("2", "phase2_2026-10-10/reports.csv"),
    ("3A", "phase3_2026-10-11/part_a/reports.csv"),
    ("3B", "phase3_2026-10-11/part_b/reports.csv"),
    ("3C", "phase3_2026-10-11/part_c/reports.csv"),
    ("3D", "phase3_2026-10-11/part_d_online/reports.csv"),
]
LEVELS = ("rows", "reports", "sites")


# ---------------------------------------------------------------- parameters

def json_block(path):
    t = Path(path).read_text(encoding="utf-8")
    m = re.search(r"```json\n(.*?)\n```", t, re.S)
    return json.loads(m.group(1))


P = json_block(PLAN)
PX = json_block(EXT)
P2 = json_block(PHASE2_PLAN)
CLASSES = P["phase2_classes"]
ZONES = P["zones_order"]
DATING = P["dating_order"]
FEATURE_SOURCES4 = [tuple(x) for x in PX["phase4_feature_sources"]]
# Amendment B3 (12 Oct 2026): the owner-supplied chapters coded after the extension froze.
FEATURE_SOURCES4 += [("4F", "phase4_2026-10-11/part_f_iaa_reports/reading_addendum_2026-10-12/features.csv")]
REPORT_SOURCES4 = [tuple(x) for x in PX["phase4_report_sources"]]
NEVER_COUNTED = PX["never_counted_sources"]
PHASE4 = set(p for p, _ in REPORT_SOURCES4)
FINAL_SERIES = set(PX["final_series"])
PRELIM_SERIES = set(PX["preliminary_series"])

# set by main(): which inputs are used
FEATURE_SOURCES = list(FEATURE_SOURCES13)
REPORT_SOURCES = list(REPORT_SOURCES13)

# ---------------------------------------------------------------- text helpers (phase-2 norm)

DROP_CHARS = "ʿʾ‘’'`´׳ʽʻ’"
SPACE_CHARS = "-–—,.;:()[]/\"״“”"


def norm(s):
    """Phase-2 common.norm, unchanged: returns ' tokens ' with single spaces."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for c in DROP_CHARS:
        s = s.replace(c, "")
    for c in SPACE_CHARS:
        s = s.replace(c, " ")
    return " " + " ".join(s.split()) + " "


def norm_key(s):
    """norm plus the plan's extra space characters (maqaf, gershayim)."""
    for c in P["extra_space_chars"]:
        s = s.replace(c, " ")
    return norm(s)


def is_hebrew(c):
    return "֐" <= c <= "׿"


def latin_text(s):
    return "".join(" " if is_hebrew(c) else c for c in s)


def hebrew_text(s):
    return "".join(" " if (c.isalpha() and not is_hebrew(c)) else c for c in s)


def segments(s):
    s = s.replace(" - ", "|")
    seps = [x for x in P["segment_separators"] if x != " - "]
    pat = "[" + re.escape("".join(seps)) + "]"
    return [x for x in re.split(pat, s) if x.strip()]


LISTS = {
    "lat": dict(phrases=[norm_key(x).strip() for x in P["drop_phrases_en"]],
                drop=set(norm_key(x).strip() for x in P["drop_words_en"]),
                generic=set(norm_key(x).strip() for x in P["generic_words_en"])),
    "heb": dict(phrases=[norm_key(x).strip() for x in P["drop_phrases_he"]],
                drop=set(norm_key(x).strip() for x in P["drop_words_he"]),
                generic=set(norm_key(x).strip() for x in P["generic_words_he"])),
}


def seg_tokens(seg, lists):
    s = norm_key(seg)
    for ph in lists["phrases"]:
        s = s.replace(" " + ph + " ", " ")
    toks = []
    for t in s.split():
        if any(ch.isdigit() for ch in t) or len(t) <= 1 or t in lists["drop"]:
            continue
        toks.append(t)
    return toks


# PLAN_EXTENSION §4.1: phase-4 names use the frozen lists plus the phase-4 additions (Latin script only)
LISTS4 = {
    "lat": dict(phrases=LISTS["lat"]["phrases"] + [norm_key(x).strip() for x in PX["phase4_drop_phrases_en"]],
                drop=LISTS["lat"]["drop"] | set(norm_key(x).strip() for x in PX["phase4_drop_words_en"]),
                generic=LISTS["lat"]["generic"] | set(norm_key(x).strip() for x in PX["phase4_generic_words_en"])),
    "heb": LISTS["heb"],
}


def raw_key(text, script, p4=False):
    lists = (LISTS4 if p4 else LISTS)[script]
    segs = [seg_tokens(x, lists) for x in segments(text)]
    for toks in segs:
        d = sorted(set(t for t in toks if len(t) >= 3 and t not in lists["generic"]))
        if d:
            return " ".join(d)
    for toks in segs:
        if len(toks) >= 2:
            return " ".join(toks)
    return ""


def region_keys(p4):
    rk = {"lat": set(), "heb": set()}
    for _t in P2["region_wide_terms"]["en"]:
        rk["lat"].add(" ".join(sorted(set(raw_key(_t, "lat", p4).split()))))
    for _t in P2["region_wide_terms"]["he"]:
        rk["heb"].add(" ".join(sorted(set(raw_key(_t, "heb", p4).split()))))
    return {k: set(x for x in v if x) for k, v in rk.items()}


REGION_KEYS = region_keys(False)
REGION_KEYS4 = region_keys(True)


def name_keys(name, p4=False):
    """(latin_key, hebrew_key) of a name, as DEDUPE_PLAN §5.1 (with the PLAN_EXTENSION §4.1 lists for phase-4 names)."""
    out = []
    rk = REGION_KEYS4 if p4 else REGION_KEYS
    for script, text in (("lat", latin_text(name)), ("heb", hebrew_text(name))):
        k = raw_key(text, script, p4)
        if k and " ".join(sorted(set(k.split()))) in rk[script]:
            k = ""
        out.append(k)
    return tuple(out)


def all_tokens(name, p4=False):
    """PLAN_EXTENSION §4.1: all tokens of every segment after drop phrases and drop words (generic kept), per script."""
    out = []
    for script, text in (("lat", latin_text(name)), ("heb", hebrew_text(name))):
        lists = (LISTS4 if p4 else LISTS)[script]
        s = set()
        for seg in segments(text):
            s.update(seg_tokens(seg, lists))
        out.append(frozenset(s))
    return tuple(out)


def name_test(ka, kb):
    return bool((ka[0] and ka[0] == kb[0]) or (ka[1] and ka[1] == kb[1]))


def n4_test(a, b):
    """PLAN_EXTENSION §4.1 N4: equal keys, or one report's key contained in all tokens of the other's name."""
    if name_test(a["keys"], b["keys"]):
        return True
    for i in (0, 1):
        for x, y in ((a, b), (b, a)):
            k = x["keys"][i]
            if k and set(k.split()) <= y["toks"][i]:
                return True
    return False


def comparable(ka, kb):
    return bool((ka[0] and kb[0]) or (ka[1] and kb[1]))


def fold_ascii(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def skeleton(word):
    w = word.lower()
    for a, b in (("ph", "f"), ("tz", "z"), ("ts", "z"), ("ck", "k"), ("q", "k"), ("c", "k"), ("w", "v")):
        w = w.replace(a, b)
    w = re.sub(r"[aeiouyh]", "", w)
    w = re.sub(r"(.)\1+", r"\1", w)
    return w


def author_skeletons(author):
    s = re.sub(r"\([^)]*\)", " ", author or "")
    s = fold_ascii(s)
    for c in DROP_CHARS:
        s = s.replace(c, "")
    parts = re.split(r",|;|&|/|\band\b", s, flags=re.I)
    out = set()
    for p in parts:
        words = [w for w in re.findall(r"[A-Za-z]+", p) if len(w) >= 3]
        if words:
            k = skeleton(words[-1])
            if len(k) >= 2:
                out.add(k)
    return out


PERMIT_DROP = [r"judea and samaria license no\.?", r"j&s license", r"license no\.?", r"license"]


YEAR_STRIP = re.compile(r"^\W*(%s)\s*-\s*(\d+)\s*/\s*(?:\d{2}|\d{4})\W*$" % "|".join(PX["permit_year_strip_prefixes"]), re.I)


def permits(field):
    """Amendment A1: phrase removal, split at , ; and ' and ', letters and digits only.
    PLAN_EXTENSION §4.1, done first: parenthesised text removed; 'A-<n>/<year>' read as 'A-<n>'."""
    s = re.sub(r"\([^)]*\)", " ", field or "")
    for pat in PERMIT_DROP:
        s = re.sub(pat, " ", s, flags=re.I)
    out = set()
    for part in re.split(r",|;|\band\b", s, flags=re.I):
        if any(ch.isdigit() for ch in part):
            m = YEAR_STRIP.match(part)
            if m:
                part = m.group(1) + m.group(2)
            out.add(re.sub(r"[^A-Za-z0-9]", "", part).upper())
    return out


# ---------------------------------------------------------------- geography

def km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km (R = 6371.0088 km), as phase-1 geo.km()."""
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def zone_of(lat, lon):
    """Phase-2 common.zone_of: first zone (frozen order) whose box contains the point."""
    for z in P2["zones_order"]:
        for la0, la1, lo0, lo1 in P2["zones"][z]:
            if la0 <= lat <= la1 and lo0 <= lon <= lo1:
                return z
    return None


GAZ = {}
for _z, _g in P2["gazetteer"].items():
    GAZ[_z] = sorted(set(norm(p).strip() for p in _g["en"] + _g["he"] if norm(p).strip()))


def title_zone(title):
    nt = norm(title)
    hits = [z for z, ps in GAZ.items() if any((" " + p + " ") in nt for p in ps)]
    return hits[0] if len(hits) == 1 else None


UNIT = {3: 1000, 4: 100, 5: 10, 6: 1}


def ref_unit(text):
    m = re.search(r"(\d{3,6})(?:\s*[–-]\s*\d+)?\s*[/.]\s*(\d{3,6})", text or "")
    if not m:
        return None
    return max(UNIT[len(m.group(1))], UNIT[len(m.group(2))])


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def tol_m(u1, u2):
    return P["distance_m"] + P["precision_factor"] * (u1 + u2)


# ---------------------------------------------------------------- io

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class UF:
    def __init__(self):
        self.p = {}

    def add(self, x):
        self.p.setdefault(x, x)

    def find(self, x):
        self.add(x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if rb < ra:
                ra, rb = rb, ra
            self.p[rb] = ra
        return ra != rb


def best(datings):
    for d in DATING:
        if d in datings:
            return d
    return "unknown"


# ---------------------------------------------------------------- load

def load_places():
    out = {}
    for r in read_csv(PLACES)[1]:
        if r["lat"] and r["lon"]:
            out[r["place_id"]] = (float(r["lat"]), float(r["lon"]))
    return out


def zone_for_phase1(lat, lon, title, coord_source, places):
    if lat is not None and lon is not None:
        return (zone_of(lat, lon) or "outside"), "map ref point (phase-2 boxes)"
    z = title_zone(title)
    if z:
        return z, "title gazetteer (phase-2 §2)"
    m = re.search(r"\(([a-z0-9_]+)\)", coord_source or "")
    if m and m.group(1) in places:
        la, lo = places[m.group(1)]
        return (zone_of(la, lo) or "outside"), "named place point (places_v2: %s)" % m.group(1)
    return "unlocated", "none"


def load_reports(places):
    reports = {}
    order = []
    for phase, rel in REPORT_SOURCES:
        _, rows = read_csv(HAESI / rel)
        for i, r in enumerate(rows, 1):
            rid = r["report_id"]
            assert rid not in reports, "duplicate report id %s" % rid
            lat, lon = fnum(r["lat"]), fnum(r["lon"])
            if phase == "1":
                zone, _ = zone_for_phase1(lat, lon, r["site_name"], r["coordinate_source"], places)
            else:
                zone = r.get("region_zone", "")
            ser = r["series"]
            p4 = phase in PHASE4
            if p4:
                ser = series_code(rid)
                vser = ser
            elif ser == "HA-ESI":
                vser = "HA-ESI online" if rid.startswith("HAESI-") else "HA-ESI print"
            else:
                vser = ser
            ym = re.search(r"\d{4}", r["year"] or "")
            pm = re.search(r"\d+", r["pages"] or "")
            unit = ref_unit(r.get("map_ref_used") or "") or ref_unit(r["map_ref_as_given"]) or P["missing_unit_m"]
            reports[rid] = dict(
                rid=rid, phase=phase, source_file=rel, row=r, series=ser, vseries=vser, volume=r["volume"].strip(),
                year=int(ym.group(0)) if ym else None, first_page=int(pm.group(0)) if pm else None,
                lat=lat, lon=lon, unit=unit if lat is not None else None, zone=zone,
                keys=name_keys(r["site_name"], p4), toks=all_tokens(r["site_name"], p4), p4=p4,
                authors=author_skeletons(r["author"]),
                permits=permits(r["permit"]), site_name=r["site_name"], author=r["author"],
                finds=p4 and ser == "ATQ" and is_finds(r), roundup=p4 and is_roundup(ser, r))
            order.append(rid)
    return reports, order


def series_code(rid):
    for pre, code in PX["series_by_id_prefix"]:
        if rid.startswith(pre):
            return code
    raise ValueError("no series code for %s" % rid)


FINDS_WORDS = set(norm(w).strip() for w in PX["finds_words"])


def is_finds(r):
    """PLAN_EXTENSION §4.1: finds or specialist report (ATQ)."""
    words = set(norm(r["site_name"] + " " + (r.get("toc_item") or "")).split())
    eos = (r["excavated_or_surveyed"] or "").lower()
    return bool(words & FINDS_WORDS) or "laboratory" in eos or "study" in eos


def is_roundup(ser, r):
    m = PX["roundup_markers"].get(ser)
    if not m:
        return False
    v = r.get(m["field"]) or ""
    if "contains" in m:
        return m["contains"] in v
    return v.startswith(m["startswith"])


def load_features(places, reports):
    fields2, _ = read_csv(HAESI / "phase2_2026-10-10/features.csv")
    rows = []
    for phase, rel in FEATURE_SOURCES:
        _, src = read_csv(HAESI / rel)
        for i, r in enumerate(src, 1):
            lat, lon = fnum(r["lat"]), fnum(r["lon"])
            if phase == "1":
                zone, zsrc = zone_for_phase1(lat, lon, r["site_name"], r["coordinate_source"], places)
            else:
                zone, zsrc = r["region_zone"], "source row"
            cls = r["feature_type"]
            p4 = phase in PHASE4
            if rel in NEVER_COUNTED:
                counted, reason = False, NEVER_COUNTED[rel]
            elif cls not in CLASSES:
                counted, reason = False, "class %s not eligible in phase 2" % cls
            elif zone not in ZONES:
                counted, reason = False, "zone %s" % zone
            else:
                counted, reason = True, ""
            cs = r["coordinate_source"] or ""
            name = r["site_name"]
            if cs.startswith("feature") and r["feature_site"].strip() and any(name_keys(r["feature_site"], p4)):
                name = r["feature_site"]
            prec = fnum(r["precision_m"])
            hm = re.match(r"(?:name only|feature site name) \(([a-z0-9_]+)\)", cs)
            hint = hm.group(1) if hm and hm.group(1) in places else ""
            rows.append(dict(
                uid="%s#%d" % (rel, i), phase=phase, source_file=rel, src=r, rid=r["report_id"],
                cls=cls, dating=r["dated_in_window"], zone=zone, zone_source=zsrc, counted=counted,
                reason=reason, lat=lat, lon=lon, unit=(prec if prec else P["missing_unit_m"]) if lat is not None else None,
                own_loc=cs.startswith("feature"), name=name, keys=name_keys(name, p4), hint=hint, p4=p4))
            assert r["report_id"] in reports, r["report_id"]
    return fields2, rows


def load_manual(path=MANUAL):
    if not Path(path).exists():
        return []
    return read_csv(path)[1]


# ---------------------------------------------------------------- report groups

def pair_tests(a, b):
    au = bool(a["authors"] & b["authors"])
    if a["lat"] is not None and b["lat"] is not None:
        d = km(a["lat"], a["lon"], b["lat"], b["lon"]) * 1000
        pos = d <= tol_m(a["unit"], b["unit"])
    else:
        d, pos = None, None
    nm = n4_test(a, b) if (a["p4"] or b["p4"]) else name_test(a["keys"], b["keys"])
    place = pos if pos is not None else nm
    return au, pos, nm, place, d


def permit_contra(a, b):
    return bool(a["permits"]) and bool(b["permits"]) and not (a["permits"] & b["permits"])


def derive_volume_map(reports, order):
    """Amendment A2: HA volume -> ESI volume, from the part-B crosswalk and unambiguous first-pass R2 links."""
    ev = defaultdict(Counter)
    src = defaultdict(Counter)
    if PARTB_XWALK.exists():
        for r in read_csv(PARTB_XWALK)[1]:
            rid = r["report_id"].strip()
            if rid in reports and reports[rid]["vseries"] == "ESI":
                ev[r["volume"].strip()][reports[rid]["volume"]] += 1
                src[(r["volume"].strip(), reports[rid]["volume"])]["part-B crosswalk"] += 1
    _, _, cands, _ = build_groups(reports, order, [], vmap=None, first_pass=True)
    for c in cands:
        if c["rule"] == "R2" and c["outcome"] == "linked":
            ha, esi = reports[c["report_a"]]["volume"], reports[c["report_b"]]["volume"]
            ev[ha][esi] += 1
            src[(ha, esi)]["first-pass unambiguous R2 link"] += 1
    vmap, rows = {}, []
    for ha in sorted(ev, key=lambda v: (int(re.match(r"\d+", v).group(0)), v)):
        mc = ev[ha].most_common()
        top = mc[0]
        ok = len(mc) == 1 or mc[1][1] < top[1]
        if ok:
            vmap[ha] = top[0]
        for esi, n in sorted(ev[ha].items(), key=lambda kv: (-kv[1], kv[0])):
            rows.append(dict(ha_volume=ha, esi_volume=esi, evidence_items=n,
                             evidence="; ".join("%s %d" % (k, v) for k, v in sorted(src[(ha, esi)].items())),
                             chosen="yes" if ok and esi == top[0] else "no"))
    return vmap, rows


def build_groups(reports, order, manual, vmap=None, first_pass=False):
    uf = UF()
    for rid in order:
        uf.add(rid)
    cands = []
    links = defaultdict(set)  # rid -> set of rules
    review = []
    mrep = {}
    for m in manual:
        if m["kind"] == "report":
            mrep[tuple(sorted((m["id_a"], m["id_b"])))] = m

    def rec(rule, a, b, tests, outcome, note=""):
        au, pos, nm, place, d = tests
        cands.append(dict(rule=rule, report_a=a["rid"], report_b=b["rid"], series_a=a["vseries"], series_b=b["vseries"],
                          year_a=a["year"] or "", year_b=b["year"] or "", author_test=yn(au),
                          position_test="" if pos is None else yn(pos), distance_m="" if d is None else "%.0f" % d,
                          name_test=yn(nm), place_test=yn(place), outcome=outcome, note=note))

    # R1 identical citation
    byc = defaultdict(list)
    for rid in order:
        r = reports[rid]
        if r["first_page"] is not None:
            byc[(r["series"], r["volume"], r["first_page"])].append(r)
    for _, lst in sorted(byc.items()):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                t = pair_tests(a, b)
                if a["p4"] or b["p4"]:
                    # amendment B1: R1 uses the frozen (equal-key) name test for phase-4 reports
                    nm_eq = name_test(a["keys"], b["keys"])
                    t = (t[0], t[1], nm_eq, t[1] if t[1] is not None else nm_eq, t[4])
                pk1 = tuple(sorted((a["rid"], b["rid"])))
                if t[2] and pk1 in mrep and mrep[pk1]["decision"] != "same":
                    rec("R1", a, b, t, "not linked (manual: %s)" % mrep[pk1]["decision"], "reviewed: " + mrep[pk1]["decision"])
                elif t[2] and t[0] and t[3]:
                    uf.union(a["rid"], b["rid"])
                    links[a["rid"]].add("R1")
                    links[b["rid"]].add("R1")
                    rec("R1", a, b, t, "linked")
                elif t[2]:
                    rec("R1", a, b, t, "not linked (author or place test failed, A3)")

    # R4 same permit
    byp = defaultdict(list)
    for rid in order:
        for p in sorted(reports[rid]["permits"]):
            byp[p].append(reports[rid])
    seen = set()
    for p, lst in sorted(byp.items()):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                key = (a["rid"], b["rid"])
                if key in seen:
                    continue
                seen.add(key)
                t = pair_tests(a, b)
                pk = tuple(sorted(key))
                if pk in mrep and mrep[pk]["decision"] != "same":
                    rec("R4", a, b, t, "not linked (manual: %s)" % mrep[pk]["decision"], "permit %s" % p)
                elif t[3]:
                    uf.union(a["rid"], b["rid"])
                    links[a["rid"]].add("R4")
                    links[b["rid"]].add("R4")
                    rec("R4", a, b, t, "linked", "permit %s" % p + ("" if t[0] else "; author test failed"))
                elif pk in mrep:
                    uf.union(a["rid"], b["rid"])
                    links[a["rid"]].add("R4 manual")
                    links[b["rid"]].add("R4 manual")
                    rec("R4", a, b, t, "linked (manual: same)", "permit %s; place test failed; reviewed: same" % p)
                else:
                    rec("R4", a, b, t, "not linked (place test failed)", "permit %s" % p)

    # R2 (HA x ESI) and R3 (print x online, same volume): one to one
    lo, hi = P["esi_minus_ha_years"]
    unmapped_pass = set()
    for rule, sa, sb in (("R2", "HA", "ESI"), ("R3", "HA-ESI print", "HA-ESI online")):
        A = [reports[x] for x in order if reports[x]["vseries"] == sa]
        B = [reports[x] for x in order if reports[x]["vseries"] == sb]
        eligible, listed = [], []
        for a in A:
            for b in B:
                pk = tuple(sorted((a["rid"], b["rid"])))
                man = mrep.get(pk)
                if rule == "R2":
                    if a["year"] is None or b["year"] is None or not (lo <= b["year"] - a["year"] <= hi):
                        if not (man and man["decision"] == "same"):
                            continue
                    unmapped = vmap is not None and a["volume"] not in vmap
                    if vmap is not None and not unmapped and vmap[a["volume"]] != b["volume"] and not (man and man["decision"] == "same"):
                        continue
                else:
                    unmapped = False
                    if a["volume"] != b["volume"]:
                        continue
                t = pair_tests(a, b)
                au, pos, nm, place, d = t
                npass = sum([au, bool(pos), nm])
                if npass >= 2 or man:
                    listed.append((a, b, t))
                if man:
                    continue
                if unmapped:
                    if au and place:
                        unmapped_pass.add(tuple(sorted((a["rid"], b["rid"]))))
                    continue
                if au and place:
                    dy = abs((b["year"] or 0) - (a["year"] or 0))
                    eligible.append(((0 if pos is not None else 1, dy, d if d is not None else 0.0, a["rid"], b["rid"]), a, b, t))
        nopt = Counter()
        for _, a, b, _ in eligible:
            nopt[a["rid"]] += 1
            nopt[b["rid"]] += 1
        paired = set()
        outcome = {}
        # manual 'same' first
        for a, b, t in listed:
            pk = tuple(sorted((a["rid"], b["rid"])))
            man = mrep.get(pk)
            if man and man["decision"] == "same":
                uf.union(a["rid"], b["rid"])
                links[a["rid"]].add(rule + " manual")
                links[b["rid"]].add(rule + " manual")
                paired.update((a["rid"], b["rid"]))
                outcome[pk] = "linked (manual: same)"
            elif man:
                outcome[pk] = "not linked (manual: %s)" % man["decision"]
        for key, a, b, t in sorted(eligible, key=lambda x: x[0]):
            pk = tuple(sorted((a["rid"], b["rid"])))
            if a["rid"] in paired or b["rid"] in paired:
                outcome[pk] = "not linked (one side already paired)"
                continue
            uf.union(a["rid"], b["rid"])
            links[a["rid"]].add(rule)
            links[b["rid"]].add(rule)
            paired.update((a["rid"], b["rid"]))
            outcome[pk] = "linked" + (" (ambiguous)" if nopt[a["rid"]] > 1 or nopt[b["rid"]] > 1 else "")
        for a, b, t in listed:
            pk = tuple(sorted((a["rid"], b["rid"])))
            au, pos, nm, place, d = t
            oc = outcome.get(pk)
            if oc is None:
                oc = "not linked"
            notes = []
            if nopt[a["rid"]] > 1 or nopt[b["rid"]] > 1:
                notes.append("ambiguous: %s has %d eligible, %s has %d" % (a["rid"], nopt[a["rid"]], b["rid"], nopt[b["rid"]]))
            rv = ""
            if pk in unmapped_pass:
                rv = "HA volume without English volume (A2)"
            elif nm and not au:
                rv = "author test failed"
            elif nm and au and pos is False:
                rv = "position test failed"
            elif "ambiguous" in oc or notes:
                rv = "ambiguous"
            if rv and pk not in mrep:
                notes.append("REVIEW: " + rv)
                review.append(pk)
            elif rv and pk in mrep:
                notes.append("reviewed: " + mrep[pk]["decision"])
            rec(rule, a, b, t, oc, "; ".join(notes))
    if not first_pass:
        phase4_rules(reports, order, uf, links, mrep, rec, review)
        # PLAN_EXTENSION §4.3: a manual 'same' is applied even when no rule lists the pair
        for pk, m in sorted(mrep.items()):
            if m["decision"] == "same" and pk[0] in reports and pk[1] in reports and uf.find(pk[0]) != uf.find(pk[1]):
                a, b = reports[pk[0]], reports[pk[1]]
                uf.union(pk[0], pk[1])
                links[pk[0]].add("manual")
                links[pk[1]].add("manual")
                rec("manual", a, b, pair_tests(a, b), "linked (manual: same)", "not listed by any rule")
    return uf, links, cands, review


def phase4_rules(reports, order, uf, links, mrep, rec, review):
    """PLAN_EXTENSION §4.2: R7, R5, R8, R6, in this order, after the frozen R1, R4, R2, R3."""

    def pk_of(a, b):
        return tuple(sorted((a["rid"], b["rid"])))

    def link(rule, a, b):
        uf.union(a["rid"], b["rid"])
        links[a["rid"]].add(rule)
        links[b["rid"]].add(rule)

    def evaluate(a, b, cand_fn, required):
        """Returns (tests, contra, cand, listed, failed-test names)."""
        t = pair_tests(a, b)
        au, pos, nm, place, d = t
        contra = permit_contra(a, b)
        ok = cand_fn(t)
        npass = sum([au, bool(pos), nm])
        man = mrep.get(pk_of(a, b))
        listed = ok or npass >= 2 or man is not None
        failed = [name for name, val in required(t) if not val]
        return t, contra, ok and not contra, listed, failed, man

    def finish(rule, a, b, t, contra, ok, failed, man, outcome=None, notes=()):
        notes = list(notes)
        if man is not None:
            oc = "linked (manual: same)" if man["decision"] == "same" else "not linked (manual: %s)" % man["decision"]
            notes.append("reviewed: " + man["decision"])
        elif outcome is not None:
            oc = outcome
        elif contra and not failed:
            oc = "not linked (permit contradiction)"
        elif not ok:
            oc = "not linked"
            if failed:
                notes.append("LISTED: %s failed" % " and ".join(failed))
        else:
            oc = "not linked"
        rec(rule, a, b, t, oc, "; ".join(notes))

    def apply_manual_same(rule, pairs):
        for a, b, ev in pairs:
            man = ev[5]
            if man is not None and man["decision"] == "same":
                link(rule + " manual", a, b)

    # ---- R7 IAAR volumes of one excavation
    iaar = [reports[x] for x in order if reports[x]["vseries"] == "IAAR"]
    req7 = lambda t: [("author test", t[0]), ("place test", t[3])]
    pairs = []
    for i in range(len(iaar)):
        for j in range(i + 1, len(iaar)):
            a, b = iaar[i], iaar[j]
            ev = evaluate(a, b, lambda t: t[0] and t[3], req7)
            if ev[3]:
                pairs.append((a, b, ev))
    apply_manual_same("R7", pairs)
    for a, b, ev in pairs:
        t, contra, ok, listed, failed, man = ev
        if man is None and ok:
            link("R7", a, b)
            finish("R7", a, b, t, contra, ok, failed, man, outcome="linked")
        else:
            finish("R7", a, b, t, contra, ok, failed, man)

    # ---- R5 ʿAtiqot finds report to its site report (same volume)
    atq = defaultdict(list)
    for x in order:
        if reports[x]["vseries"] == "ATQ":
            atq[reports[x]["volume"]].append(reports[x])
    req5 = lambda t: [("place test", t[3]), ("author and name tests", t[0] or t[2])]
    pairs = []
    for vol, lst in sorted(atq.items()):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                if not (a["finds"] or b["finds"]):
                    continue
                ev = evaluate(a, b, lambda t: t[3] and (t[0] or t[2]), req5)
                if ev[3]:
                    pairs.append((a, b, ev))
    apply_manual_same("R5", pairs)
    done = {}
    ambiguous = set()
    by_finds = defaultdict(list)  # finds rid -> [(site report, pair)]
    for a, b, ev in pairs:
        if not ev[2] and not (ev[5] is not None and ev[5]["decision"] == "same"):
            continue
        if ev[5] is not None and ev[5]["decision"] != "same":
            continue
        if a["finds"] and not b["finds"]:
            by_finds[a["rid"]].append((b, (a, b, ev)))
        elif b["finds"] and not a["finds"]:
            by_finds[b["rid"]].append((a, (a, b, ev)))
    for f in sorted(by_finds):
        groups = set(uf.find(s["rid"]) for s, _ in by_finds[f])
        if len(groups) == 1:
            for s, (a, b, ev) in by_finds[f]:
                if ev[5] is None:
                    link("R5", a, b)
                    done[pk_of(a, b)] = ("linked", [])
        else:
            ambiguous.add(f)
            for s, (a, b, ev) in by_finds[f]:
                if ev[5] is None:
                    done[pk_of(a, b)] = ("not linked", ["REVIEW: ambiguous (finds report with site-report candidates in %d groups)" % len(groups)])
                    review.append(pk_of(a, b))
    for a, b, ev in pairs:
        if a["finds"] and b["finds"] and ev[2] and ev[5] is None:
            if a["rid"] in ambiguous or b["rid"] in ambiguous:
                done[pk_of(a, b)] = ("not linked", ["REVIEW: ambiguous (finds report flagged in step 1)"])
                review.append(pk_of(a, b))
            else:
                link("R5", a, b)
                done[pk_of(a, b)] = ("linked", [])
    for a, b, ev in pairs:
        t, contra, ok, listed, failed, man = ev
        oc, notes = done.get(pk_of(a, b), (None, []))
        finish("R5", a, b, t, contra, ok, failed, man, outcome=oc, notes=notes)

    # ---- R8 QDAP / ADAJ round-up unit to full article (one to one)
    lo, hi = PX["article_minus_roundup_years"]
    req8 = lambda t: [("place test", t[3])]
    for ser in PX["roundup_series"]:
        A = [reports[x] for x in order if reports[x]["vseries"] == ser and reports[x]["roundup"]]
        B = [reports[x] for x in order if reports[x]["vseries"] == ser and not reports[x]["roundup"]]
        pairs = []
        for a in A:
            for b in B:
                if a["year"] is None or b["year"] is None or not (lo <= b["year"] - a["year"] <= hi):
                    if pk_of(a, b) not in mrep:
                        continue
                ev = evaluate(a, b, lambda t: t[3], req8)
                if ev[3]:
                    pairs.append((a, b, ev))
        apply_manual_same("R8", pairs)
        paired = set()
        for a, b, ev in pairs:
            if ev[5] is not None and ev[5]["decision"] == "same":
                paired.update((a["rid"], b["rid"]))
        eligible = []
        for a, b, ev in pairs:
            t = ev[0]
            if ev[2] and ev[5] is None:
                dy = abs(b["year"] - a["year"])
                eligible.append(((0 if t[1] is not None else 1, dy, t[4] if t[4] is not None else 0.0, a["rid"], b["rid"]), a, b, ev))
        nopt = Counter()
        for _, a, b, _ in eligible:
            nopt[a["rid"]] += 1
            nopt[b["rid"]] += 1
        res = {}
        for key, a, b, ev in sorted(eligible, key=lambda x: x[0]):
            amb = nopt[a["rid"]] > 1 or nopt[b["rid"]] > 1
            notes = []
            if amb:
                notes.append("REVIEW: ambiguous: %s has %d eligible, %s has %d" % (a["rid"], nopt[a["rid"]], b["rid"], nopt[b["rid"]]))
                review.append(pk_of(a, b))
            if a["rid"] in paired or b["rid"] in paired:
                res[pk_of(a, b)] = ("not linked (one side already paired)", notes)
                continue
            link("R8", a, b)
            paired.update((a["rid"], b["rid"]))
            res[pk_of(a, b)] = ("linked" + (" (ambiguous)" if amb else ""), notes)
        for a, b, ev in pairs:
            t, contra, ok, listed, failed, man = ev
            oc, notes = res.get(pk_of(a, b), (None, []))
            finish("R8", a, b, t, contra, ok, failed, man, outcome=oc, notes=notes)

    # ---- R6 final report (ATQ, IAAR) to preliminary report (HA, ESI, HA-ESI)
    lo, hi = PX["final_minus_preliminary_years"]
    finals = [reports[x] for x in order if reports[x]["vseries"] in FINAL_SERIES]
    prelims = [reports[x] for x in order if reports[x]["vseries"] in PRELIM_SERIES]
    req6 = lambda t: [("author test", t[0]), ("place test", t[3])]
    for f in finals:
        pairs = []
        for p in prelims:
            if f["year"] is None or p["year"] is None or not (lo <= f["year"] - p["year"] <= hi):
                if pk_of(f, p) not in mrep:
                    continue
            ev = evaluate(f, p, lambda t: t[0] and t[3], req6)
            if ev[3]:
                pairs.append((f, p, ev))
        apply_manual_same("R6", pairs)
        cand = [(f, p, ev) for f_, p, ev in pairs if (ev[2] and ev[5] is None) or (ev[5] is not None and ev[5]["decision"] == "same")]
        groups = set(uf.find(p["rid"]) for _, p, _ in cand)
        res = {}
        if len(groups) == 1:
            for _, p, ev in cand:
                if ev[5] is None:
                    link("R6", f, p)
                    res[pk_of(f, p)] = ("linked", [])
        elif len(groups) > 1:
            for _, p, ev in cand:
                if ev[5] is None:
                    res[pk_of(f, p)] = ("not linked", ["REVIEW: ambiguous (final report with preliminary candidates in %d groups)" % len(groups)])
                    review.append(pk_of(f, p))
        for a, b, ev in pairs:
            t, contra, ok, listed, failed, man = ev
            oc, notes = res.get(pk_of(a, b), (None, []))
            finish("R6", a, b, t, contra, ok, failed, man, outcome=oc, notes=notes)


def yn(x):
    return "yes" if x else "no"


# ---------------------------------------------------------------- main build

def cluster_sites(frows, manual, rows_by_rep, use_s2=True):
    """Site links S1, S4, S5 and (if use_s2) S2, as DEDUPE_PLAN §5 with amendment A4."""
    suf = UF()
    for fr in frows:
        suf.add(fr["uid"])
    rules_used = defaultdict(set)
    site_review = []
    loc = [fr for fr in frows if fr["lat"] is not None]
    # spatial hash for S1
    maxd = tol_m(P["missing_unit_m"], P["missing_unit_m"]) / 1000.0
    cell = maxd / 111.0
    grid = defaultdict(list)
    for fr in loc:
        grid[(int(math.floor(fr["lat"] / cell)), int(math.floor(fr["lon"] / cell)))].append(fr)
    idx = {fr["uid"]: i for i, fr in enumerate(frows)}
    for fr in loc:
        ci, cj = int(math.floor(fr["lat"] / cell)), int(math.floor(fr["lon"] / cell))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for o in grid.get((ci + di, cj + dj), []):
                    if idx[o["uid"]] <= idx[fr["uid"]]:
                        continue
                    d = km(fr["lat"], fr["lon"], o["lat"], o["lon"]) * 1000
                    if d > tol_m(fr["unit"], o["unit"]):
                        continue
                    if name_test(fr["keys"], o["keys"]):
                        if suf.union(fr["uid"], o["uid"]):
                            pass
                        rules_used[fr["uid"]].add("S1")
                        rules_used[o["uid"]].add("S1")
                    elif not comparable(fr["keys"], o["keys"]) and (any(fr["keys"]) and any(o["keys"])) and fr["rid"] != o["rid"]:
                        site_review.append((fr, o, d))
    # S4 same report group, rows located by the report itself
    byg = defaultdict(list)
    for fr in frows:
        if not fr["own_loc"]:
            byg[fr["report_group"]].append(fr)
    for g, lst in byg.items():
        for x in lst[1:]:
            suf.union(lst[0]["uid"], x["uid"])
            rules_used[x["uid"]].add("S4")
            rules_used[lst[0]["uid"]].add("S4")
    # S5 manual site decisions
    msite_applied = []
    for m in manual:
        if m["kind"] != "site":
            continue
        ra = [x for x in rows_by_rep[m["id_a"]] if (not m["class"] or x["cls"] == m["class"])]
        rb = [x for x in rows_by_rep[m["id_b"]] if (not m["class"] or x["cls"] == m["class"])]
        assert ra and rb, "manual site decision with no rows: %r" % m
        if m["decision"] == "same":
            for x in ra + rb:
                suf.union(ra[0]["uid"], x["uid"])
                rules_used[x["uid"]].add("S5")
            msite_applied.append(m)
    # S2 rows without coordinates
    if not use_s2:
        return suf, rules_used, site_review, set(), set()
    located_root = {}
    for script in (0, 1):
        tmp = defaultdict(set)
        for fr in loc:
            if fr["keys"][script]:
                tmp[(fr["zone"], fr["keys"][script])].add(suf.find(fr["uid"]))
        located_root[script] = tmp
    nol = [fr for fr in frows if fr["lat"] is None]
    ambiguous_rows = set()
    hint_split_rows = set()
    for script in (0, 1):
        byk = defaultdict(list)
        for fr in nol:
            if fr["keys"][script]:
                byk[(fr["zone"], fr["keys"][script])].append(fr)
        for k, lst in sorted(byk.items()):
            # amendment A4: split by the readers' named-place hint
            hints = sorted(set(fr["hint"] for fr in lst if fr["hint"]))
            if len(hints) <= 1:
                groups = [lst]
            else:
                groups = [[fr for fr in lst if fr["hint"] == h] for h in hints]
                groups.append([fr for fr in lst if not fr["hint"]])
                for fr in lst:
                    hint_split_rows.add(fr["uid"])
            for grp in groups:
                if not grp:
                    continue
                for x in grp[1:]:
                    suf.union(grp[0]["uid"], x["uid"])
                    rules_used[x["uid"]].add("S2")
                    rules_used[grp[0]["uid"]].add("S2")
                roots = located_root[script].get(k, set())
                roots = set(suf.find(r) for r in roots)
                if len(roots) == 1:
                    r0 = next(iter(roots))
                    for x in grp:
                        suf.union(r0, x["uid"])
                        rules_used[x["uid"]].add("S2")
                elif len(roots) > 1:
                    for x in grp:
                        ambiguous_rows.add(x["uid"])

    return suf, rules_used, site_review, ambiguous_rows, hint_split_rows


ZSHORT = {"Z1_GERIZIM": "Z1 Gerizim", "Z2_JORDAN_VALLEY": "Z2 Jordan Valley", "Z3_JUDEAN_DESERT": "Z3 Judean Desert",
          "Z4_JERUSALEM_HILLS": "Z4 Jerusalem hills"}
LEVEL_TITLE = {"rows": "Level 1, rows (as coded, duplicates included)",
               "reports": "Level 2, deduplicated reports (report group x class x zone)",
               "sites": "Level 3, distinct sites (site x class x zone)"}


def render_md(summary):
    """Generated tables: class x zone x dated_in_window at three levels. Cells are yes / no / unknown (all)."""
    out = ["# HA-ESI merged inventory: generated tables", "",
           "Generated by `scripts/build_merged.py`. Do not edit. Cells: yes / no / unknown (all), where yes, no and unknown are "
           "`dated_in_window`. Level 2 and 3 cells count units (report group or site) per class and zone; a unit's dating is yes if any "
           "of its rows is yes, else no if any is no, else unknown. A site count is not a count of features on the ground.", ""]

    def cell(d):
        return "%d / %d / %d (%d)" % (d["yes"], d["no"], d["unknown"], d["yes"] + d["no"] + d["unknown"])

    for lv in LEVELS:
        t = summary["counts"][lv]
        tot = summary["totals"][lv]
        out.append("## " + LEVEL_TITLE[lv])
        out.append("")
        out.append("| class | " + " | ".join(ZSHORT[z] for z in ZONES) + " | all zones |")
        out.append("|---|" + "---|" * (len(ZONES) + 1))
        for c in CLASSES:
            out.append("| %s | %s | %s |" % (c, " | ".join(cell(t[c][z]) for z in ZONES), cell(tot["by_class"][c])))
        out.append("| all classes | %s | %s |" % (" | ".join(cell(tot["by_zone"][z]) for z in ZONES), cell(tot["all_classes"])))
        out.append("")
    d = summary["distinct"]
    out.append("## Distinct units")
    out.append("")
    out.append("| measure | count |")
    out.append("|---|---|")
    for k in ("rows_all", "rows_counted", "reports_coded", "report_groups", "report_groups_multi", "report_groups_with_counted_rows",
              "sites", "sites_with_counted_rows", "sites_multi_report_group", "sites_counted_located", "sites_counted_name_only",
              "sites_spread_flagged", "sites_ambiguous_name"):
        out.append("| %s | %d |" % (k, d[k]))
    sens = summary["sensitivity_sites_without_S2"]
    out.append("| sites_with_counted_rows without S2 (upper bracket) | %d |" % sens["sites_with_counted_rows"])
    out.append("")
    out.append("Sites without S2, all classes: %s." % cell(sens["all_classes"]))
    out.append("")
    return "\n".join(out)


def main(out_dir=LANE, phases13=False):
    global FEATURE_SOURCES, REPORT_SOURCES
    if phases13:
        FEATURE_SOURCES, REPORT_SOURCES = list(FEATURE_SOURCES13), list(REPORT_SOURCES13)
    else:
        FEATURE_SOURCES = list(FEATURE_SOURCES13) + FEATURE_SOURCES4
        REPORT_SOURCES = list(REPORT_SOURCES13) + REPORT_SOURCES4
    out_dir = Path(out_dir)
    places = load_places()
    reports, order = load_reports(places)
    fields2, frows = load_features(places, reports)
    manual = load_manual(MANUAL_OLD if phases13 else MANUAL)
    vmap, vmap_rows = derive_volume_map(reports, order)
    uf, links, cands, review = build_groups(reports, order, manual, vmap=vmap)

    # groups
    members = defaultdict(list)
    for rid in order:
        members[uf.find(rid)].append(rid)
    rows_by_rep = defaultdict(list)
    for fr in frows:
        rows_by_rep[fr["rid"]].append(fr)

    def pref_key(rid):
        r = reports[rid]
        cr = [x for x in rows_by_rep[rid] if x["counted"]]
        return (-len(cr), -len(set(x["cls"] for x in cr)), 0 if r["lat"] is not None else 1,
                r["unit"] if r["unit"] is not None else 10 ** 9, -(r["year"] or 0), rid)

    gid_of, group_info = {}, {}
    conflicts = []
    for root, mem in members.items():
        mem = sorted(mem)
        gid = "RG:" + mem[0]
        pref = sorted(mem, key=pref_key)[0]
        for m in mem:
            gid_of[m] = gid
        group_info[gid] = dict(members=mem, pref=pref)

    # pairwise position conflicts inside multi-member groups
    for gid, g in sorted(group_info.items()):
        mem = g["members"]
        if len(mem) < 2:
            continue
        for i in range(len(mem)):
            for j in range(i + 1, len(mem)):
                a, b = reports[mem[i]], reports[mem[j]]
                if a["lat"] is not None and b["lat"] is not None:
                    d = km(a["lat"], a["lon"], b["lat"], b["lon"]) * 1000
                    if d > tol_m(a["unit"], b["unit"]):
                        conflicts.append(dict(level="report_group", unit_id=gid, type="position",
                                              members="%s;%s" % (a["rid"], b["rid"]), class_="",
                                              detail="%.0f m apart (tolerance %.0f m)" % (d, tol_m(a["unit"], b["unit"])),
                                              resolution="preferred version's position used (%s)" % g["pref"]))
                if "R4" in links[a["rid"]] and "R4" in links[b["rid"]] and not (a["authors"] & b["authors"]) and (a["permits"] & b["permits"]):
                    conflicts.append(dict(level="report_group", unit_id=gid, type="author", members="%s;%s" % (a["rid"], b["rid"]),
                                          class_="", detail="same permit, author test failed: %r / %r" % (a["author"], b["author"]),
                                          resolution="kept together (same permit)"))

    # level-2 units
    l2 = defaultdict(list)  # (gid, cls, zone) -> datings
    l2rows = defaultdict(list)  # (gid, cls, zone) -> rows
    for gid, g in sorted(group_info.items()):
        mem, pref = g["members"], g["pref"]
        crow = [x for m in mem for x in rows_by_rep[m] if x["counted"]]
        for fr in crow:
            fr["report_group"] = gid
        classes = sorted(set(x["cls"] for x in crow))
        for c in classes:
            rows_c = [x for x in crow if x["cls"] == c]
            zp = sorted(set(x["zone"] for x in rows_c if x["rid"] == pref))
            for x in rows_c:
                ez = x["zone"]
                if x["rid"] != pref and zp and ez not in zp:
                    if len(zp) == 1:
                        conflicts.append(dict(level="report_group", unit_id=gid, type="zone", members=x["rid"] + ";" + pref,
                                              class_=c, detail="%s row %s in %s; preferred %s in %s" % (x["rid"], x["uid"], ez, pref, zp[0]),
                                              resolution="row counted in the preferred version's zone"))
                        ez = zp[0]
                    else:
                        conflicts.append(dict(level="report_group", unit_id=gid, type="zone", members=x["rid"] + ";" + pref,
                                              class_=c, detail="%s row %s in %s; preferred %s in %s" % (x["rid"], x["uid"], ez, pref, "/".join(zp)),
                                              resolution="row keeps its own zone"))
                x["level2_zone"] = ez
                l2[(gid, c, ez)].append(x["dating"])
                l2rows[(gid, c, ez)].append(x)
            if len(mem) > 1:
                have = [m for m in mem if any(x["rid"] == m for x in rows_c)]
                lack = [m for m in mem if m not in have]
                if lack:
                    conflicts.append(dict(level="report_group", unit_id=gid, type="class_in_one_version", members=";".join(mem), class_=c,
                                          detail="coded in %s; not in %s" % ("/".join(have), "/".join(lack)),
                                          resolution="class counted (union of versions)"))
                summ = {m: best(set(x["dating"] for x in rows_c if x["rid"] == m)) for m in have}
                if len(set(summ.values())) > 1:
                    conflicts.append(dict(level="report_group", unit_id=gid, type="dating", members=";".join(have), class_=c,
                                          detail="; ".join("%s=%s" % (m, summ[m]) for m in have),
                                          resolution="combined %s (yes > no > unknown)" % best(set(summ.values()))))
                zs = {m: sorted(set(x["zone"] for x in rows_c if x["rid"] == m)) for m in have}
                if len(set(tuple(v) for v in zs.values())) > 1:
                    conflicts.append(dict(level="report_group", unit_id=gid, type="zone_versions", members=";".join(have), class_=c,
                                          detail="; ".join("%s=%s" % (m, "/".join(zs[m])) for m in have),
                                          resolution="see zone rows; preferred version's zone"))
                one = {m: [x for x in rows_c if x["rid"] == m] for m in have}
                if len(have) > 1 and all(len(v) == 1 for v in one.values()):
                    nf = {m: v[0]["src"]["n_features"].strip() for m, v in one.items()}
                    if all(nf.values()) and len(set(nf.values())) > 1:
                        conflicts.append(dict(level="report_group", unit_id=gid, type="n_features", members=";".join(have), class_=c,
                                              detail="; ".join("%s=%s" % (m, nf[m]) for m in have), resolution="rows kept as coded"))
    for fr in frows:
        fr.setdefault("report_group", gid_of[fr["rid"]])
        fr["report_group"] = gid_of[fr["rid"]]

    # ---------------- sites
    suf, rules_used, site_review, ambiguous_rows, hint_split_rows = cluster_sites(frows, manual, rows_by_rep)
    suf_no_s2 = cluster_sites(frows, manual, rows_by_rep, use_s2=False)[0]

    # site ids in input order
    sroot_rows = defaultdict(list)
    for fr in frows:
        sroot_rows[suf.find(fr["uid"])].append(fr)
    site_id_of_root = {}
    n = 0
    for fr in frows:
        r = suf.find(fr["uid"])
        if r not in site_id_of_root:
            n += 1
            site_id_of_root[r] = "S%04d" % n
    for fr in frows:
        fr["site_id"] = site_id_of_root[suf.find(fr["uid"])]

    sites = []
    l3 = defaultdict(list)
    l3rows = defaultdict(list)
    for root, lst in sroot_rows.items():
        sid = site_id_of_root[root]
        cl = [x for x in lst if x["counted"]]
        zc = Counter(x["zone"] for x in cl)
        if cl:
            top = max(zc.values())
            szone = [z for z in ZONES if zc.get(z) == top][0]
        else:
            szone = Counter(x["zone"] for x in lst).most_common(1)[0][0]
        if len(zc) > 1:
            conflicts.append(dict(level="site", unit_id=sid, type="site_zone", members=";".join(sorted(set(x["rid"] for x in cl))), class_="",
                                  detail="; ".join("%s=%d" % (z, zc[z]) for z in sorted(zc)), resolution="site counted in %s (most rows)" % szone))
        for x in cl:
            l3[(sid, x["cls"], szone)].append(x["dating"])
            l3rows[(sid, x["cls"], szone)].append(x)
        lr = [x for x in lst if x["lat"] is not None]
        spread = 0.0
        for i in range(len(lr)):
            for j in range(i + 1, len(lr)):
                spread = max(spread, km(lr[i]["lat"], lr[i]["lon"], lr[j]["lat"], lr[j]["lon"]) * 1000)
        rg = sorted(set(x["report_group"] for x in lst))
        lk = sorted(set(x["keys"][0] for x in lst if x["keys"][0]))
        hk = sorted(set(x["keys"][1] for x in lst if x["keys"][1]))
        units = defaultdict(list)
        for x in cl:
            units[x["cls"]].append(x["dating"])
        sites.append(dict(
            site_id=sid, n_rows=len(lst), n_rows_counted=len(cl), n_report_groups=len(rg), n_reports=len(set(x["rid"] for x in lst)),
            report_groups=";".join(rg), first_name=lst[0]["name"], latin_keys=" | ".join(lk), hebrew_keys=" | ".join(hk),
            located="yes" if lr else "no",
            lat="%.5f" % (sum(x["lat"] for x in lr) / len(lr)) if lr else "",
            lon="%.5f" % (sum(x["lon"] for x in lr) / len(lr)) if lr else "",
            spread_m="%.0f" % spread if lr else "", spread_flag="yes" if spread > P["spread_flag_m"] else "",
            zone=szone, zones_seen="/".join(sorted(set(x["zone"] for x in lst))),
            rules=";".join(sorted(set(r for x in lst for r in rules_used[x["uid"]]))),
            ambiguous_name="yes" if any(x["uid"] in ambiguous_rows for x in lst) else "",
            classes="; ".join("%s=%s" % (c, best(set(v))) for c, v in sorted(units.items()))))
    sites.sort(key=lambda s: s["site_id"])

    # sensitivity: sites without S2 (rows without coordinates joined only by S4/S5)
    alt_rows = defaultdict(list)
    for fr in frows:
        if fr["counted"]:
            alt_rows[suf_no_s2.find(fr["uid"])].append(fr)
    l3_alt = defaultdict(list)
    for root, lst in alt_rows.items():
        zc = Counter(x["zone"] for x in lst)
        top = max(zc.values())
        szone = [z for z in ZONES if zc.get(z) == top][0]
        for x in lst:
            l3_alt[(root, x["cls"], szone)].append(x["dating"])

    # ---------------- report_groups.csv
    partb_x = defaultdict(list)
    if PARTB_XWALK.exists():
        for r in read_csv(PARTB_XWALK)[1]:
            if r["report_id"]:
                for rid in re.split(r"[;,| ]+", r["report_id"]):
                    if rid:
                        partb_x[rid].append(r["screen_id"])
    rg_rows = []
    for gid, g in sorted(group_info.items()):
        mem, pref = g["members"], g["pref"]
        pr = reports[pref]
        allr = [x for m in mem for x in rows_by_rep[m]]
        units = sorted((c, z, best(set(d))) for (gg, c, z), d in l2.items() if gg == gid)
        rules = sorted(set(l for m in mem for l in links[m]))
        lat = pr["lat"]
        lon = pr["lon"]
        if lat is None:
            for m in mem:
                if reports[m]["lat"] is not None:
                    lat, lon = reports[m]["lat"], reports[m]["lon"]
                    break
        rg_rows.append(dict(
            report_group=gid, n_versions=len(mem), member_report_ids=";".join(mem),
            phases=";".join(reports[m]["phase"] for m in mem), version_series=";".join(reports[m]["vseries"] for m in mem),
            years=";".join(str(reports[m]["year"] or "") for m in mem), preferred_report_id=pref, link_rules=";".join(rules),
            ambiguous="", site_name=pr["site_name"], author=pr["author"],
            zone=pr["zone"], lat="" if lat is None else "%.5f" % lat, lon="" if lon is None else "%.5f" % lon,
            n_rows_all=len(allr), n_rows_counted=sum(1 for x in allr if x["counted"]),
            units="; ".join("%s@%s=%s" % u for u in units),
            site_ids=";".join(sorted(set(x["site_id"] for x in allr))),
            uncoded_versions=";".join(sorted(s for m in mem for s in partb_x.get(m, [])))))
    amb_ids = set()
    for c in cands:
        if "ambiguous" in c["outcome"] or "ambiguous" in c["note"]:
            amb_ids.update((c["report_a"], c["report_b"]))
    for r in rg_rows:
        if any(m in amb_ids for m in r["member_report_ids"].split(";")):
            r["ambiguous"] = "yes"
    nconf = Counter(c["unit_id"] for c in conflicts)
    for r in rg_rows:
        r["n_conflicts"] = nconf.get(r["report_group"], 0)

    # ---------------- features_all.csv
    vrole = {}
    for gid, g in group_info.items():
        for m in g["members"]:
            vrole[m] = "single" if len(g["members"]) == 1 else ("preferred" if m == g["pref"] else "alternate")
    extra = ["phase", "source_file", "report_group", "site_id", "row_uid", "counted", "count_zone", "zone_source",
             "not_counted_reason", "version_role", "level2_zone"]
    fa_rows = []
    for fr in frows:
        d = {k: fr["src"].get(k, "") for k in fields2}
        d.update(phase=fr["phase"], source_file=fr["source_file"], report_group=fr["report_group"], site_id=fr["site_id"],
                 row_uid=fr["uid"], counted=yn(fr["counted"]), count_zone=fr["zone"],
                 zone_source=fr["zone_source"], not_counted_reason=fr["reason"], version_role=vrole[fr["rid"]],
                 level2_zone=fr.get("level2_zone", "") if fr["counted"] else "")
        fa_rows.append(d)

    # ---------------- counts
    def table(units):
        t = {c: {z: {d: 0 for d in DATING} for z in ZONES} for c in CLASSES}
        for (c, z), dd in units:
            t[c][z][dd] += 1
        return t

    lvl_units = {
        "rows": [((x["cls"], x["zone"]), x["dating"]) for x in frows if x["counted"]],
        "reports": [((c, z), best(set(d))) for (g, c, z), d in sorted(l2.items())],
        "sites": [((c, z), best(set(d))) for (s, c, z), d in sorted(l3.items())],
    }
    counts = {lv: table(u) for lv, u in lvl_units.items()}
    alt_counts = table([((c, z), best(set(d))) for (s_, c, z), d in sorted(l3_alt.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0]))])

    def totals(t):
        by_class = {c: {d: sum(t[c][z][d] for z in ZONES) for d in DATING} for c in CLASSES}
        by_zone = {z: {d: sum(t[c][z][d] for c in CLASSES) for d in DATING} for z in ZONES}
        allc = {d: sum(by_class[c][d] for c in CLASSES) for d in DATING}
        for dct in list(by_class.values()) + list(by_zone.values()) + [allc]:
            dct["all"] = sum(dct[d] for d in DATING)
        return by_class, by_zone, allc

    summary = dict(
        what="HA-ESI merged inventory (phases 1, 2, 3A-D): counts by class x zone x dated_in_window at three levels",
        plan=dict(file="DEDUPE_PLAN.md", sha256=sha256_file(PLAN), freeze_commit="bf4320f", amendments="AMENDMENTS.md (A1)"),
        inputs={rel: dict(rows=sum(1 for x in frows if x["source_file"] == rel), sha256=sha256_file(HAESI / rel)) for _, rel in FEATURE_SOURCES},
        report_inputs={rel: dict(rows=sum(1 for r in reports.values() if r["source_file"] == rel), sha256=sha256_file(HAESI / rel)) for _, rel in REPORT_SOURCES},
        unit_definitions={
            "rows": "counted feature rows as coded (duplicates included)",
            "reports": "(report group, class, zone); dating yes if any row of any version is yes, else no if any no, else unknown",
            "sites": "(site, class, site zone); same yes > no > unknown rule over all counted rows at the site",
        },
        counts=counts,
    )
    tot = {}
    for lv in LEVELS:
        bc, bz, ac = totals(counts[lv])
        tot[lv] = dict(by_class=bc, by_zone=bz, all_classes=ac)
    summary["totals"] = tot
    counted_rows = [x for x in frows if x["counted"]]
    summary["distinct"] = dict(
        rows_all=len(frows), rows_counted=len(counted_rows),
        rows_not_counted=dict(Counter(x["reason"] for x in frows if not x["counted"])),
        reports_coded=len(reports), report_groups=len(group_info),
        report_groups_multi=sum(1 for g in group_info.values() if len(g["members"]) > 1),
        reports_in_multi_groups=sum(len(g["members"]) for g in group_info.values() if len(g["members"]) > 1),
        report_groups_with_counted_rows=len(set(x["report_group"] for x in counted_rows)),
        sites=len(sites), sites_with_counted_rows=sum(1 for s in sites if s["n_rows_counted"]),
        sites_multi_report_group=sum(1 for s in sites if s["n_rows_counted"] and s["n_report_groups"] > 1),
        sites_counted_located=sum(1 for s in sites if s["n_rows_counted"] and s["located"] == "yes"),
        sites_counted_name_only=sum(1 for s in sites if s["n_rows_counted"] and s["located"] == "no"),
        sites_spread_flagged=sum(1 for s in sites if s["spread_flag"]),
        sites_ambiguous_name=sum(1 for s in sites if s["ambiguous_name"]),
    )
    summary["groups_by_rule"] = dict(Counter(r for g in rg_rows if g["n_versions"] > 1 for r in [g["link_rules"]]))
    summary["phase1_counted_rows_by_class"] = dict(sorted(Counter(x["cls"] for x in counted_rows if x["phase"] == "1").items()))
    summary["conflicts_by_type"] = dict(sorted(Counter(c["type"] for c in conflicts).items()))
    summary["review"] = dict(report_pairs_listed=len(cands), report_pairs_open_review=len(review),
                             site_review_pairs=len(site_review),
                             manual_decisions=dict(Counter("%s/%s" % (m["kind"], m["decision"]) for m in manual)))
    summary["s3_external_site_ids"] = 0
    abc, abz, aac = totals(alt_counts)
    summary["sensitivity_sites_without_S2"] = dict(
        note="rows without coordinates joined only by S4 (same report group) and S5 (manual); an upper bracket on the site count",
        sites_with_counted_rows=len(alt_rows), by_class=abc, by_zone=abz, all_classes=aac)

    rg_extra, site_extra = [], []
    if not phases13:
        summary["what"] = ("Merged regional inventory (phases 1, 2, 3A-D, 4E-I): counts by class x zone x dated_in_window "
                           "at three levels")
        summary["plan"] = dict(file="../merged_2026-10-11/DEDUPE_PLAN.md", sha256=sha256_file(PLAN), freeze_commit="bf4320f",
                               amendments="../merged_2026-10-11/AMENDMENTS.md (A1-A4)",
                               extension=dict(file="PLAN_EXTENSION.md", sha256=sha256_file(EXT), freeze_commit=EXT_FREEZE_COMMIT),
                               extension_amendments=("AMENDMENTS.md" if (LANE / "AMENDMENTS.md").exists() else "none"))
        summary["phase4"] = phase4_contribution(reports, group_info, links, frows, sites, rg_rows, l2rows, l3rows, table, totals)
        rg_extra = ["phase4_members", "phase13_groups"]
        site_extra = ["phase4_rows", "phase13_sites"]

    # ---------------- write
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "features_all.csv", fields2 + extra, fa_rows)
    write_csv(out_dir / "report_groups.csv",
              ["report_group", "n_versions", "member_report_ids", "phases", "version_series", "years", "preferred_report_id",
               "link_rules", "ambiguous", "site_name", "author", "zone", "lat", "lon", "n_rows_all", "n_rows_counted", "units",
               "site_ids", "uncoded_versions", "n_conflicts"] + rg_extra, rg_rows)
    write_csv(out_dir / "sites.csv",
              ["site_id", "n_rows", "n_rows_counted", "n_report_groups", "n_reports", "report_groups", "first_name", "latin_keys",
               "hebrew_keys", "located", "lat", "lon", "spread_m", "spread_flag", "zone", "zones_seen", "rules", "ambiguous_name",
               "classes"] + site_extra, sites)
    conflicts.sort(key=lambda c: (c["level"], c["unit_id"], c["type"], c["class_"], c["members"], c["detail"]))
    for i, c in enumerate(conflicts, 1):
        c["conflict_id"] = "C%04d" % i
        c["class"] = c.pop("class_")
    write_csv(out_dir / "conflicts.csv", ["conflict_id", "level", "unit_id", "type", "class", "members", "detail", "resolution"], conflicts)
    cands.sort(key=lambda c: (c["rule"], c["report_a"], c["report_b"]))
    write_csv(out_dir / "pair_candidates.csv",
              ["rule", "report_a", "report_b", "series_a", "series_b", "year_a", "year_b", "author_test", "position_test",
               "distance_m", "name_test", "place_test", "outcome", "note"], cands)
    msite = {}
    for m in manual:
        if m["kind"] == "site":
            msite[tuple(sorted((m["id_a"], m["id_b"])))] = m["decision"]
    srows = []
    for a, b, d in site_review:
        srows.append(dict(row_a=a["uid"], row_b=b["uid"], report_a=a["rid"], report_b=b["rid"], site_a=a["site_id"], site_b=b["site_id"],
                          name_a=a["name"], name_b=b["name"], distance_m="%.0f" % d, same_site_now=yn(a["site_id"] == b["site_id"]),
                          manual_decision=msite.get(tuple(sorted((a["rid"], b["rid"]))), "")))
    srows.sort(key=lambda r: (r["report_a"], r["report_b"], r["row_a"], r["row_b"]))
    write_csv(out_dir / "site_review.csv", ["row_a", "row_b", "report_a", "report_b", "site_a", "site_b", "name_a", "name_b",
                                            "distance_m", "same_site_now", "manual_decision"], srows)
    md = render_md(summary)
    if not phases13:
        md = md.replace("# HA-ESI merged inventory: generated tables", "# Merged regional inventory, phases 1-4: generated tables", 1)
        md += "\n" + render_phase4_md(summary)
    (out_dir / "summary.md").write_text(md, encoding="utf-8")
    write_csv(out_dir / "ha_esi_volume_map.csv", ["ha_volume", "esi_volume", "evidence_items", "evidence", "chosen"], vmap_rows)
    summary["ha_esi_volume_map"] = vmap
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    return summary


def phase4_contribution(reports, group_info, links, frows, sites, rg_rows, l2rows, l3rows, table, totals):
    """PLAN_EXTENSION §6: phase-4-only, shared and phase 1-3-only units; joins of earlier groups and sites."""
    old_gid = {}
    for r in read_csv(OLD_GROUPS)[1]:
        for m in r["member_report_ids"].split(";"):
            old_gid[m] = r["report_group"]
    old_sid = {r["row_uid"]: r["site_id"] for r in read_csv(OLD_FEATURES)[1]}
    out = dict(old_inputs={"../merged_2026-10-11/report_groups.csv": sha256_file(OLD_GROUPS),
                           "../merged_2026-10-11/features_all.csv": sha256_file(OLD_FEATURES)})
    # report groups
    gid_rows = {r["report_group"]: r for r in rg_rows}
    p4_groups, joined_rules, bridging = [], Counter(), []
    for gid, g in sorted(group_info.items()):
        p4m = [m for m in g["members"] if reports[m]["p4"]]
        olds = sorted(set(old_gid[m] for m in g["members"] if not reports[m]["p4"]))
        gid_rows[gid]["phase4_members"] = ";".join(p4m)
        gid_rows[gid]["phase13_groups"] = ";".join(olds)
        if p4m:
            p4_groups.append(gid)
            if olds:
                joined_rules[";".join(sorted(set(l for m in p4m for l in links[m])))] += 1
        if len(olds) > 1:
            bridging.append(gid)
    out["report_groups_with_phase4"] = len(p4_groups)
    out["report_groups_phase4_only"] = sum(1 for g in p4_groups if not gid_rows[g]["phase13_groups"])
    out["report_groups_phase4_only_multi"] = sum(1 for g in p4_groups if not gid_rows[g]["phase13_groups"]
                                                 and int(gid_rows[g]["n_versions"]) > 1)
    out["report_groups_joined_to_phase13"] = sum(joined_rules.values())
    out["phase4_reports_joined_to_phase13"] = sum(len(gid_rows[g]["phase4_members"].split(";")) for g in p4_groups
                                                  if gid_rows[g]["phase13_groups"])
    out["joined_by_phase4_link_rules"] = dict(sorted(joined_rules.items()))
    out["phase13_groups_joined_together"] = {g: gid_rows[g]["phase13_groups"] for g in bridging}
    out["phase4_reports"] = sum(1 for r in reports.values() if r["p4"])
    # sites
    s_bridge = {}
    srow = defaultdict(list)
    for fr in frows:
        srow[fr["site_id"]].append(fr)
    for s in sites:
        lst = srow[s["site_id"]]
        olds = sorted(set(old_sid[x["uid"]] for x in lst if not x["p4"]))
        s["phase4_rows"] = sum(1 for x in lst if x["p4"])
        s["phase13_sites"] = ";".join(olds)
        if len(olds) > 1:
            s_bridge[s["site_id"]] = ";".join(olds)
    out["phase13_sites_joined_together"] = s_bridge
    cs = [s for s in sites if s["n_rows_counted"]]
    out["sites_counted_with_phase4_rows"] = sum(1 for s in cs if any(x["p4"] and x["counted"] for x in srow[s["site_id"]]))
    out["sites_counted_phase4_only"] = sum(1 for s in cs if not any((not x["p4"]) and x["counted"] for x in srow[s["site_id"]]))

    def split(units):
        st = {"phase4_only": [], "shared": [], "phase13_only": []}
        changed = []
        for (u, c, z), rows in sorted(units.items()):
            f = [x["p4"] for x in rows]
            d_all = best(set(x["dating"] for x in rows))
            if all(f):
                st["phase4_only"].append(((c, z), d_all))
            elif any(f):
                st["shared"].append(((c, z), d_all))
                d13 = best(set(x["dating"] for x in rows if not x["p4"]))
                if d13 != d_all:
                    changed.append("%s %s@%s: %s -> %s" % (u, c, z, d13, d_all))
            else:
                st["phase13_only"].append(((c, z), d_all))
        return st, changed

    res = {}
    rows_p4 = [((x["cls"], x["zone"]), x["dating"]) for x in frows if x["counted"] and x["p4"]]
    t = table(rows_p4)
    bc, bz, ac = totals(t)
    res["rows"] = dict(phase4=dict(counts=t, by_class=bc, by_zone=bz, all_classes=ac))
    for lv, units in (("reports", l2rows), ("sites", l3rows)):
        st, changed = split(units)
        res[lv] = {}
        for k, u in st.items():
            t = table(u)
            bc, bz, ac = totals(t)
            res[lv][k] = dict(counts=t, by_class=bc, by_zone=bz, all_classes=ac)
        res[lv]["shared_dating_changed_by_phase4"] = changed
    out["levels"] = res
    return out


def render_phase4_md(summary):
    p = summary["phase4"]
    out = ["# Phase-4 contribution (generated)", "",
           "Units whose counted rows are all phase-4 rows (phase 4 only), units with rows from both phases 1-3 and phase 4 "
           "(shared), and units without phase-4 rows. Cells: yes / no / unknown (all).", ""]

    def cell(d):
        return "%d / %d / %d (%d)" % (d["yes"], d["no"], d["unknown"], d["yes"] + d["no"] + d["unknown"])

    def tab(title, blk):
        out.append("## " + title)
        out.append("")
        out.append("| class | " + " | ".join(ZSHORT[z] for z in ZONES) + " | all zones |")
        out.append("|---|" + "---|" * (len(ZONES) + 1))
        for c in CLASSES:
            out.append("| %s | %s | %s |" % (c, " | ".join(cell(blk["counts"][c][z]) for z in ZONES), cell(blk["by_class"][c])))
        out.append("| all classes | %s | %s |" % (" | ".join(cell(blk["by_zone"][z]) for z in ZONES), cell(blk["all_classes"])))
        out.append("")

    lv = p["levels"]
    tab("Phase 4, level 1, rows (counted phase-4 rows)", lv["rows"]["phase4"])
    tab("Phase 4, level 2, phase-4-only report units", lv["reports"]["phase4_only"])
    tab("Phase 4, level 3, phase-4-only site units", lv["sites"]["phase4_only"])
    out.append("## Split of units")
    out.append("")
    out.append("| level | phase 4 only | shared | phases 1-3 only | shared units whose dating phase 4 changed |")
    out.append("|---|---|---|---|---|")
    for k in ("reports", "sites"):
        out.append("| %s | %s | %s | %s | %d |" % (k, cell(lv[k]["phase4_only"]["all_classes"]), cell(lv[k]["shared"]["all_classes"]),
                                                cell(lv[k]["phase13_only"]["all_classes"]), len(lv[k]["shared_dating_changed_by_phase4"])))
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    s = main(args[0] if args else LANE, phases13="--phases13" in sys.argv)
    d = s["distinct"]
    print("rows %d (counted %d); reports %d in %d groups (%d multi); sites %d (counted %d); conflicts %d" % (
        d["rows_all"], d["rows_counted"], d["reports_coded"], d["report_groups"], d["report_groups_multi"], d["sites"],
        d["sites_with_counted_rows"], sum(s["conflicts_by_type"].values())))
    print("review: %r" % s["review"])
