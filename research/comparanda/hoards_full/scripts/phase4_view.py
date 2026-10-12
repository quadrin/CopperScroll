#!/usr/bin/env python3
"""Exploratory view: the merged regional inventory (phases 1-4) folded into the hoards_full catalogue,
as frozen in PLAN_AMENDMENT_PHASE4_2026-10-12.md (commit f2b42ac).

The frozen catalogue (hoards.csv), its results and the precedent's statistic are used unchanged:
hoards_full.py is imported (it hash-checks the precedent and PLAN.md) and the precedent's run_one,
bias_checks and coding functions do every comparison.

Standard library only. Deterministic. From the repository root:

  python3 -I -B research/comparanda/hoards_full/scripts/phase4_view.py candidates  # list review items
  python3 -I -B research/comparanda/hoards_full/scripts/phase4_view.py run         # write outputs
  python3 -I -B research/comparanda/hoards_full/scripts/phase4_view.py check       # rebuild and compare
"""
import csv
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
RESEARCH = os.path.dirname(os.path.dirname(LANE))
REPO = os.path.dirname(RESEARCH)
MERGED = os.path.join(RESEARCH, "regional", "haesi_features", "merged_2026-10-12")
PLACES = os.path.join(RESEARCH, "agent_review_2026-10-07", "wave2", "W2B_model_v1", "inputs_v2", "places_v2.csv")
DATA = os.path.join(LANE, "data")

AMENDMENT = os.path.join(LANE, "PLAN_AMENDMENT_PHASE4_2026-10-12.md")
AMENDMENT_SHA256 = "ba1f690c9a556290895b119f23464201f0ac736ddee4f98bb42c5daca98b5f2d"
AMENDMENT_COMMIT = "f2b42ac"
# merged_2026-10-12/features_all.csv at commit 7cac03b (amendment §2)
FEATURES_ALL_SHA256 = "940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d"
# the frozen lane outputs, which this view must never change
FROZEN_LANE_SHA256 = {
    "hoards.csv": "211bef3cee9fece1de0afbfc26cb549af923380de043a8c2df757fa7342d5eb1",
    "results.json": "b4858caf9c09e58a44f99ea5d3f4b6e6ab9e62c7f8d7e797167d5a33ffbcc05c",
    "RESULTS.md": "c0936672901b14cac567f483ca072d111f176f38fe2a6e59a61eea31b9f43aa5",
}

OUT_VIEW = os.path.join(LANE, "phase4_view_2026-10-12.csv")
OUT_SCORES = os.path.join(LANE, "phase4_scores.csv")
OUT_SUMMARY = os.path.join(LANE, "phase4_summary.json")
MANUAL = os.path.join(DATA, "phase4_manual_check.csv")
DEDUPE = os.path.join(DATA, "phase4_dedupe_decisions.csv")


def _load_lane():
    spec = importlib.util.spec_from_file_location("hoards_full", os.path.join(LANE, "hoards_full.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load_lane()   # checks PLAN.md and the precedent's frozen inputs on import
C = H.C


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_amendment():
    if sha256(AMENDMENT) != AMENDMENT_SHA256:
        raise SystemExit("PLAN_AMENDMENT_PHASE4_2026-10-12.md hash does not match the frozen hash")
    if sha256(os.path.join(MERGED, "features_all.csv")) != FEATURES_ALL_SHA256:
        raise SystemExit("merged_2026-10-12/features_all.csv changed")
    for name, h in FROZEN_LANE_SHA256.items():
        if sha256(os.path.join(LANE, name)) != h:
            raise SystemExit(f"frozen lane file {name} changed")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def csv_bytes(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    return buf.getvalue().encode("utf-8")


# ---------------------------------------------------------------- amendment §3: rows and protection
CAVE_WORD = r"\b(caves?|rock shelters?|crevices?|fissures?|hiding complex(es)?|refuge)\b"
HELD_AREA = r"qumran|feshkha|fashkha|qarantal|quruntul|kuruntul|nuwei|nueima|nuei|\bduk\b|\bduq\b|dyuk|qelt|kelt"


def text_of(r):
    return (r["feature_subtype"] + ". " + r["quote"]).lower()


def protected_reason(r):
    allt = (r["site_name"] + " " + r["feature_subtype"] + " " + r["quote"]).lower()
    if r["protected_strip"] == "yes" or re.search(r"sultan", allt):
        return "protected: Tell es-Sultan"
    if re.search(r"almit", allt):
        return "protected: Kh. Almit (compared with nothing)"
    if re.search(CAVE_WORD, allt) and re.search(HELD_AREA, allt):
        return "protected: held cave area"
    return ""


def hoard_rows():
    rows = read_csv(os.path.join(MERGED, "features_all.csv"))
    return [r for r in rows if r["counted"] == "yes" and r["feature_type"] == "hoard_cache"]


def version_selected(rows):
    """Tombs §4: preferred or single version; an alternate only if its group has no preferred/single row."""
    by = {}
    for r in rows:
        by.setdefault(r["report_group"], []).append(r)
    sel = set()
    for g, rs in by.items():
        pref = [r for r in rs if r["version_role"] in ("single", "preferred")]
        for r in (pref if pref else rs):
            sel.add(r["row_uid"])
    return sel


# ---------------------------------------------------------------- amendment §5: coding
PERIODS = [  # (pattern, from, to)
    (r"iron age", -1200, -586), (r"persian", -539, -332), (r"ptolemaic", -301, -200),
    (r"seleucid", -200, -141), (r"late hellenistic|hasmonean", -141, -37), (r"hellenistic", -332, -37),
    (r"herodian", -37, 70), (r"early roman", -63, 135), (r"second temple", -141, 70),
    (r"first revolt|great revolt", 66, 70), (r"bar kokhba|bar kochba|bar-kokhba|second revolt", 132, 135),
    (r"middle roman", 70, 250), (r"late roman", 250, 363), (r"byzantine", 324, 638),
    (r"early islamic|umayyad", 638, 750), (r"abbasid", 750, 969), (r"fatimid", 969, 1099),
    (r"crusader", 1099, 1291), (r"ayyubid", 1187, 1260), (r"mamluk", 1260, 1516), (r"ottoman", 1516, 1917),
    (r"mandate|british", 1917, 1948),
]
ROMAN_ALONE = (r"\broman\b", -63, 324)
ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8}


def parse_date(period, dated_in_window):
    p = period.lower()
    # Implementation clarifications (README, phase-4 section): "612/3" is the year 612/613; in "a-b ERA"
    # and "Nth-Mth centuries ERA" the era applies to both ends.
    p = re.sub(r"(\d{1,4})/(\d{1,4})", r"\1", p)
    era_rx = r"(bce|bc|b\.c\.e?\.?|ce|c\.e\.|ad|a\.d\.)"
    years = []
    for m in re.finditer(r"(\d{1,4})\s*[-–]\s*(\d{1,4})\s*" + era_rx, p):
        sign = -1 if m.group(3).startswith("b") else 1
        years += [sign * int(m.group(1)), sign * int(m.group(2))]
    for m in re.finditer(r"(\d{1,4})\s*" + era_rx, p):
        y = int(m.group(1))
        years.append(-y if m.group(2).startswith("b") else y)
    for m in re.finditer(r"\b(ad|a\.d\.)\s*(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?", p):
        years.append(int(m.group(2)))
        if m.group(3):
            years.append(int(m.group(3)))
    if years:
        return min(years), max(years), "explicit years"
    cents = []
    cent_rx = r"(?:centuries|century|cent\.?|c\.)"
    for m in re.finditer(r"\b(\d{1,2})(?:st|nd|rd|th)?\s*[-–]\s*(\d{1,2})(?:st|nd|rd|th)?\s*" + cent_rx +
                         r"\s*(bce|bc|ce|ad)?", p):
        for n in (int(m.group(1)), int(m.group(2))):
            era = m.group(3) or ""
            cents.append((-100 * n, -100 * (n - 1) - 1) if era.startswith("b") else (100 * (n - 1) + 1, 100 * n))
    for m in re.finditer(r"\b(\d{1,2})(?:st|nd|rd|th)?\s*" + cent_rx + r"\s*(bce|bc|ce|ad)?|"
                         r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth)\s+" + cent_rx +
                         r"\s*(bce|bc|ce|ad)?", p):
        n = int(m.group(1)) if m.group(1) else ORD[m.group(3)]
        era = m.group(2) or m.group(4) or ""
        if era.startswith("b"):
            cents.append((-100 * n, -100 * (n - 1) - 1))
        else:
            cents.append((100 * (n - 1) + 1, 100 * n))
    if cents:
        return min(a for a, _ in cents), max(b for _, b in cents), "centuries"
    hits = []
    rest = p
    for rx, a, b in PERIODS:
        if re.search(rx, rest):
            hits.append((a, b))
            rest = re.sub(rx, " ", rest)
    if re.search(ROMAN_ALONE[0], rest):
        hits.append(ROMAN_ALONE[1:])
    if hits:
        return min(a for a, _ in hits), max(b for _, b in hits), "named periods"
    if dated_in_window == "yes":
        return -141, 135, "date from dated_in_window"
    return None, None, "no date"


ELIG_EXCL = [
    (r"single coin|one coin|a single", "single coin"),
    (r"grave goods|funerary offering|with the (deceased|body|skeleton)|in the coffin", "grave goods"),
    (r"foundation deposit", "foundation deposit (excavator's classification)"),
    (r"votive", "votive offering"),
    (r"(mint|workshop) (debris|waste)", "mint or workshop debris"),
]
OBJ = {
    "documents": r"scroll|document|papyr|manuscript",
    "coins": r"coin|shekel|tetradrachm|didrachm|denar|prut|drachm|sela|obol",
    "metal": r"jewel|gold|silver|bronze vessel|vessels|weapon|sword|tool|ingot|bullion|\bring|earring|bracelet",
}
SETTING_RX = [
    ("cistern", r"cisterns?"),
    ("pool_reservoir", r"pool|reservoir|miqw?e|miqva|mikve|ritual bath|basin|spring"),
    ("channel", r"channel|aqueduct|conduit|drain|outlet"),
    ("tomb", r"tomb|burial cave|kokh|loculus|loculi|mausoleum|funerary"),
    ("cave", r"cave|rock shelter|crevice|fissure|hiding complex|refuge"),
    ("structure", r"house|room|courtyard|shop|street|building|fort|casemate|tower|storeroom|store room|columbarium|"
                  r"dovecote|underground chamber|bathhouse|palace|synagogue|villa|farmhouse|church|monastery|"
                  r"structure|wall|floor|niche|threshold|doorway|pillar|column|locus|installation|silo"),
    ("ruin_heap", r"ruin|heap|cairn|mound|collapse|debris"),
    ("open_ground", r"field|open ground|open area|slope|road|quarry|garden|terrace"),
]
PLACEMENT_RX = [
    ("under_stone_threshold", r"under (a |the )?(large |flat )?(stone|slab|threshold|doorway|door|step|steps|paving)"),
    ("wall_cavity", r"niche|in(side)? (a |the )?wall|between (the )?(wall )?stones|crack|door-?frame"),
    ("pillar", r"pillar|column"),
    ("under_floor", r"(under|beneath|below|in|into) (a |the )?(\w+ )?floor|between (the )?floors|pit|buried"),
    ("container_buried", None),
    ("corner", r"corner"),
    ("upper_storey", r"upper (storey|story|floor)"),
    ("floor_surface", r"on (a |the )?floor|scattered|ash"),
]
CONTAINER_RX = r"\b(jar|jug|juglet|pot|vessel|box|chest|purse|bag|pouch|cloth|bundle|lamp|flask|bowl)s?\b"
LOOT_RX = r"dealer|market|looted|loot|confiscat|seized|antiquities trade|robbers?"
CHANCE_RX = r"chance|accident|farmer|shepherd|resident|bulldozer|by workers"
DEPTH_RX = r"(\d+(?:\.\d+)?)\s*(?:[-–]|to)?\s*(\d+(?:\.\d+)?)?\s*(m|cm)\b"
DEPTH_CUE = r"depth|deep|below|beneath|under"


def propose(r):
    """All regex proposals for one inventory row (amendment §5)."""
    t = text_of(r)
    p = {}
    a, b, basis = parse_date(r["period_as_given"], r["dated_in_window"])
    p["date_from"], p["date_to"], p["date_basis"] = a, b, basis
    p["elig_excl"] = [lab for rx, lab in ELIG_EXCL if re.search(rx, t)]
    objs = [k for k, rx in OBJ.items() if re.search(rx, t)]
    if len(objs) >= 2:
        p["object_class"] = "coins_and_metal" if set(objs) == {"coins", "metal"} else "mixed"
    elif objs:
        p["object_class"] = {"documents": "documents", "coins": "coins", "metal": "metal_objects"}[objs[0]]
    else:
        p["object_class"] = "coins" if re.search(r"hoard", t) else "mixed"
    p["settings"] = [s for s, rx in SETTING_RX if re.search(rx, t)]
    m = re.search(CONTAINER_RX, t)
    p["container"] = m.group(1) if m else ""
    setting = p["settings"][0] if p["settings"] else "unknown"
    pl = []
    for name, rx in PLACEMENT_RX:
        if name == "container_buried":
            if setting == "open_ground" and p["container"]:
                pl.append(name)
        elif re.search(rx, t):
            pl.append(name)
    p["placements"] = pl
    es = r["excavated_or_surveyed"].lower()
    if re.search(LOOT_RX, t):
        p["how_found"] = "looting_recovered"
    elif re.search(CHANCE_RX, t):
        p["how_found"] = "chance"
    elif es.startswith("excavated") or "surveyed" in es:
        p["how_found"] = "excavation"
    else:
        p["how_found"] = "unknown"
    p["depth_m"], p["depth_datum"], p["depth_text"] = "", "", ""
    md = re.search(DEPTH_RX, t)
    if md and re.search(DEPTH_CUE, t):
        x = float(md.group(1))
        y = float(md.group(2)) if md.group(2) else x
        v = (x + y) / 2 / (100 if md.group(3) == "cm" else 1)
        if re.search(r"below (the )?(present |modern )?(surface|ground)", t):
            dt = "present_surface"
        elif re.search(r"below (the )?floor", t):
            dt = "ancient_floor"
        elif re.search(r"below (the )?(top|mouth|opening)", t):
            dt = "feature_top"
        else:
            dt = "unstated"
        p["depth_m"], p["depth_datum"], p["depth_text"] = f"{v:g}", dt, r["quote"]
    p["landmarks"] = [c for c in H.LANDMARK_CLASSES if re.search(H.SCROLL_RE[c], t, re.I)]
    p["temple_related"] = "1" if "temple" in t else "0"
    return p


# ---------------------------------------------------------------- amendment §7: manual check
MANUAL_FIELDS = ["row_uid", "field", "proposed", "checked", "reason"]


def manual_items(r, p):
    """The review items the amendment requires for one row: (field, proposed value)."""
    items = []
    if p["elig_excl"]:
        items.append(("exclusion", ";".join(p["elig_excl"])))
    items.append(("setting", ";".join(p["settings"]) or "unknown"))
    if p["placements"]:
        items.append(("placement", ";".join(p["placements"])))
    if p["depth_m"]:
        items.append(("depth", f"{p['depth_m']}|{p['depth_datum']}"))
    if p["landmarks"]:
        items.append(("landmark", ";".join(p["landmarks"])))
    return items


def load_manual():
    if not os.path.exists(MANUAL):
        return {}
    return {(m["row_uid"], m["field"]): m for m in read_csv(MANUAL)}


def apply_manual(r, p, manual, strict=True):
    """Return final codes. The check can confirm, choose another proposed value, or set back; never add."""
    out = {}
    missing = []

    def get(field, proposed):
        m = manual.get((r["row_uid"], field))
        if m is None:
            missing.append(field)
            return None
        if m["proposed"] != proposed:
            raise SystemExit(f"manual check for {r['row_uid']} {field} was made on a different proposal")
        return m

    # exclusion on eligibility
    excl = ""
    if p["elig_excl"]:
        m = get("exclusion", ";".join(p["elig_excl"]))
        if m is None or m["checked"] == "exclude":
            excl = ";".join(p["elig_excl"])
    else:
        m = manual.get((r["row_uid"], "exclusion_by_hand"))
        if m and m["checked"] == "exclude":
            excl = m["reason"]
    out["exclusion"] = excl
    # setting
    m = get("setting", ";".join(p["settings"]) or "unknown")
    setting = p["settings"][0] if p["settings"] else "unknown"
    if m is not None:
        if m["checked"] not in p["settings"] + ["unknown"]:
            raise SystemExit(f"{r['row_uid']}: checked setting {m['checked']} was not proposed")
        setting = m["checked"]
    out["setting"] = setting
    # placement
    placement = "not_stated"
    if p["placements"]:
        m = get("placement", ";".join(p["placements"]))
        placement = p["placements"][0]
        if m is not None:
            if m["checked"] not in p["placements"] + ["not_stated"]:
                raise SystemExit(f"{r['row_uid']}: checked placement {m['checked']} was not proposed")
            placement = m["checked"]
    if setting == "unknown":
        placement = "not_stated"
    out["placement"] = placement
    # depth
    out["depth_m"], out["depth_datum"], out["depth_text"] = "", "", ""
    if p["depth_m"]:
        m = get("depth", f"{p['depth_m']}|{p['depth_datum']}")
        if m is None or m["checked"] == "confirm":
            out["depth_m"], out["depth_datum"], out["depth_text"] = p["depth_m"], p["depth_datum"], p["depth_text"]
    # landmark
    lm = []
    if p["landmarks"]:
        m = get("landmark", ";".join(p["landmarks"]))
        lm = list(p["landmarks"])
        if m is not None:
            keep = [x for x in m["checked"].split(";") if x]
            if any(x not in p["landmarks"] + ["none_stated"] for x in keep):
                raise SystemExit(f"{r['row_uid']}: checked landmark adds a class")
            lm = [x for x in keep if x != "none_stated"]
    if setting == "unknown":
        out["landmark"], out["landmark_text"] = "", ""
    elif lm:
        out["landmark"], out["landmark_text"] = ";".join(lm), r["quote"]
    else:
        out["landmark"], out["landmark_text"] = "none_stated", ""
    out["missing_checks"] = missing
    if strict and missing:
        raise SystemExit(f"{r['row_uid']}: manual check missing for {missing}")
    return out


# ---------------------------------------------------------------- amendment §4: region
def load_places():
    return {p["place_id"]: p for p in read_csv(PLACES)}


def in_boxes(lat, lon):
    for (la, lo) in (C.BOX_J, C.BOX_V):
        if la[0] <= lat <= la[1] and lo[0] <= lon <= lo[1]:
            return True
    return False


def judaea_by_name(r, places):
    if r["lat"] and r["lon"]:
        return "", "own point"
    m = re.search(r"\(([a-z0-9_]+)\)", r["coordinate_source"])
    if m and m.group(1) in places and places[m.group(1)]["lat"]:
        pl = places[m.group(1)]
        return ("1" if in_boxes(float(pl["lat"]), float(pl["lon"])) else "0"), f"reader place {m.group(1)}"
    return "0", "no point"


# ---------------------------------------------------------------- catalogue rows from inventory rows
def to_catalogue(r, p, f, places):
    jbn, pos_basis = judaea_by_name(r, places)
    zone = r["count_zone"].split("_")[0]
    excl = f["exclusion"]
    if p["date_from"] is None:
        excl = excl or "no date (precedent §3)"
    flags = [f"inventory phase {r['phase']}", f"date basis: {p['date_basis']}", f"position: {pos_basis}"]
    if r["n_features"] and r["n_features"] != "1":
        flags.append(f"n_features {r['n_features']}")
    return {
        "id": "iaa_" + r["row_uid"], "site": r["site_name"], "lat": r["lat"], "lon": r["lon"],
        "country": f"southern Levant (inventory zone {zone}; Israel, Palestinian Territories or Jordan)",
        "date_from": "" if p["date_from"] is None else str(p["date_from"]),
        "date_to": "" if p["date_to"] is None else str(p["date_to"]),
        "object_type": r["feature_subtype"] or "hoard or cache", "container": p["container"],
        "setting": f["setting"], "placement": f["placement"], "context_reported": r["quote"],
        "how_found": p["how_found"],
        "source": f"{r['series']} {r['volume']} ({r['year']}) {r['pages']}; report {r['report_id']}".strip(),
        "cluster_id": "iaa_" + r["row_uid"], "include": "0" if excl else "1", "exclusion_reason": excl,
        "flags": "; ".join(flags), "judaea_by_name": jbn, "t02_id": "",
        "origin": "iaa_p4" if r["phase"].startswith("4") else "iaa_p13", "first_read": "after_freeze",
        "unexposed_at_freeze": "0", "object_class": p["object_class"], "temple_related": p["temple_related"],
        "depth_m": f["depth_m"], "depth_datum": f["depth_datum"], "depth_text": f["depth_text"],
        "landmark": f["landmark"], "landmark_text": f["landmark_text"], "discovery_year": "",
        "terminus_text": r["period_as_given"],
        "sources_pages": f"{r['series']} {r['volume']} {r['pages']} ({r['report_id']})",
        "recode_reason": "", "prec_setting": "", "prec_placement": "", "prec_include": "", "prec_date": "",
    }


# ---------------------------------------------------------------- amendment §6: duplicates
GENERIC = set("kh khirbet khirbat khurbet horbat hurvat tel tell wadi nahal ein en ain el al the of site cave area "
              "street st quarter a b c".split())


def name_tokens(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[ʿʾ'’‘`]", "", s.lower())
    toks = re.split(r"[^a-z0-9]+", s)
    return {t for t in toks if t and t not in GENERIC and not t.isdigit()}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"])))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def dates_compatible(a, b):
    try:
        a0, a1 = float(a["date_from"]), float(a["date_to"] or a["date_from"])
        b0, b1 = float(b["date_from"]), float(b["date_to"] or b["date_from"])
    except ValueError:
        return True
    return a0 <= b1 and b0 <= a1


def candidate_pairs(units, catalogue, inv_rows):
    pairs = []
    units = [u for u in units if u["include"] == "1"]  # an excluded unit enters no view; no decision needed
    for u in units:
        for c in catalogue:
            near = bool(u["lat"] and c["lat"]) and km(u, c) <= 1.0
            share = bool(name_tokens(u["site"]) & name_tokens(c["site"]))
            if (near or share) and dates_compatible(u, c):
                pairs.append((u["id"], c["id"], "near" if near else "name"))
    site = {"iaa_" + r["row_uid"]: (r["site_id"], r["report_group"]) for r in inv_rows}
    for i, u in enumerate(units):
        for v in units[i + 1:]:
            su, sv = site[u["id"]], site[v["id"]]
            if su[0] and su[0] == sv[0] and su[1] != sv[1] and dates_compatible(u, v):
                pairs.append((u["id"], v["id"], "same site_id"))
    return pairs


DEDUPE_FIELDS = ["unit", "other", "basis", "decision", "reason"]


def load_dedupe():
    if not os.path.exists(DEDUPE):
        return {}
    return {(d["unit"], d["other"]): d for d in read_csv(DEDUPE)}


# ---------------------------------------------------------------- build
def build(strict=True):
    check_amendment()
    places = load_places()
    manual = load_manual()
    inv = hoard_rows()
    selected = version_selected(inv)
    catalogue = H.derive(read_csv(os.path.join(LANE, "hoards.csv")))
    view = []
    units = []
    missing = []
    for r in sorted(inv, key=lambda x: (x["phase"], x["row_uid"])):
        line = {"row_uid": r["row_uid"], "phase": r["phase"], "report_id": r["report_id"],
                "series": r["series"], "volume": r["volume"], "year": r["year"], "pages": r["pages"],
                "site_name": r["site_name"], "report_group": r["report_group"], "site_id": r["site_id"],
                "count_zone": r["count_zone"], "version_role": r["version_role"],
                "dated_in_window": r["dated_in_window"], "period_as_given": r["period_as_given"],
                "feature_subtype": r["feature_subtype"], "quote": r["quote"], "n_features": r["n_features"]}
        prot = protected_reason(r)
        line["protected"] = prot
        line["version_selected"] = "yes" if r["row_uid"] in selected else "no"
        if prot or r["row_uid"] not in selected:
            line["status"] = "protected" if prot else "alternate version (not a unit)"
            view.append(line)
            continue
        p = propose(r)
        f = apply_manual(r, p, manual, strict=False)
        missing += [(r["row_uid"], x) for x in f["missing_checks"]]
        cat = H.derive([to_catalogue(r, p, f, places)])[0]
        units.append(cat)
        line.update({k: cat[k] for k in ("id", "date_from", "date_to", "include", "exclusion_reason", "setting",
                                         "placement", "container", "how_found", "object_class", "depth_m",
                                         "depth_datum", "landmark", "landmark_strict", "judaea_by_name",
                                         "coarse_group", "context_category", "in_window_main",
                                         "in_window_sens", "in_window_catalogue", "in_region_judaea")})
        line["date_basis"] = p["date_basis"]
        line["proposed_setting"] = ";".join(p["settings"])
        line["proposed_placement"] = ";".join(p["placements"])
        line["proposed_landmark"] = ";".join(p["landmarks"])
        line["proposed_exclusion"] = ";".join(p["elig_excl"])
        view.append(line)
    pairs = candidate_pairs(units, catalogue, inv)
    dedupe = load_dedupe()
    listed = {(a, b) for a, b, _ in pairs}
    # Pairs the screen did not list but PLAN 7 applies to (a source says so, or site and closing date agree),
    # added by hand after a lookup; reported in the README (deviation D2).
    unit_ids = {u["id"] for u in units if u["include"] == "1"}
    by_hand = [(a, b, d["basis"]) for (a, b), d in sorted(dedupe.items()) if (a, b) not in listed]
    for a, b, _ in by_hand:
        if a not in unit_ids:
            raise SystemExit(f"by-hand pair for a unit that is not an included unit: {a}")
    pairs = pairs + by_hand
    dup_of, undetermined_of = {}, {}
    missing_pairs = []
    for a, b, basis in pairs:
        d = dedupe.get((a, b))
        if d is None:
            missing_pairs.append((a, b, basis))
            continue
        if d["decision"] == "same":
            dup_of.setdefault(a if not b.startswith("iaa_") else _later(a, b, units), []).append(
                b if not b.startswith("iaa_") else _earlier(a, b, units))
        elif d["decision"] == "undetermined":
            undetermined_of.setdefault(a if not b.startswith("iaa_") else _later(a, b, units), []).append(
                b if not b.startswith("iaa_") else _earlier(a, b, units))
        elif d["decision"] != "different":
            raise SystemExit(f"bad dedupe decision {d}")
    if strict and (missing or missing_pairs):
        raise SystemExit(f"review incomplete: {len(missing)} manual checks, {len(missing_pairs)} pairs")
    for u in units:
        u["dup_of"] = ";".join(dup_of.get(u["id"], []))
        u["undetermined_with"] = ";".join(undetermined_of.get(u["id"], []))
    by_id = {u["id"]: u for u in units}
    for line in view:
        u = by_id.get(line.get("id", ""))
        if u is None:
            line["in_view_A"] = line["in_view_B"] = line["in_view_B_undetermined"] = "no"
            continue
        add = u["include"] == "1" and not u["dup_of"]
        add_main = add and not u["undetermined_with"]
        line["duplicate_of"] = u["dup_of"]
        line["undetermined_with"] = u["undetermined_with"]
        p4 = line["phase"].startswith("4")
        line["in_view_A"] = "yes" if add_main and not p4 else "no"
        line["in_view_B"] = "yes" if add_main else "no"
        line["in_view_B_undetermined"] = "yes" if add else "no"
        line["status"] = ("excluded: " + u["exclusion_reason"]) if u["include"] != "1" else (
            "duplicate" if u["dup_of"] else ("undetermined duplicate" if u["undetermined_with"] else "new unit"))
    return {"view": view, "units": units, "catalogue": catalogue, "pairs": pairs,
            "missing_checks": missing, "missing_pairs": missing_pairs}


def _phase_key(uid, units):
    u = next(x for x in units if x["id"] == uid)
    ph = "4" if u["origin"] == "iaa_p4" else "1"
    return (ph, uid)


def _earlier(a, b, units):
    return min(a, b, key=lambda x: _phase_key(x, units))


def _later(a, b, units):
    return max(a, b, key=lambda x: _phase_key(x, units))


# ---------------------------------------------------------------- runs
VIEW_FIELDS = ["row_uid", "id", "phase", "report_id", "series", "volume", "year", "pages", "site_name",
               "report_group", "site_id", "count_zone", "version_role", "version_selected", "protected",
               "status", "dated_in_window", "period_as_given", "date_basis", "date_from", "date_to",
               "feature_subtype", "quote", "n_features", "proposed_exclusion", "include", "exclusion_reason",
               "proposed_setting", "setting", "proposed_placement", "placement", "container", "how_found",
               "object_class", "depth_m", "depth_datum", "proposed_landmark", "landmark", "landmark_strict",
               "judaea_by_name", "in_region_judaea", "context_category", "coarse_group", "in_window_main",
               "in_window_sens", "in_window_catalogue", "duplicate_of", "undetermined_with",
               "in_view_A", "in_view_B", "in_view_B_undetermined"]
SCORE_FIELDS = ["view", "run", "label", "scroll_n", "comparanda_units", "comparanda_known", "comparanda_unknown",
                "chi2", "p", "D", "D_ci_low", "D_ci_high", "verdict"] + [f"comp_{g}" for g in C.COARSE_ORDER]


def expand_rows(rows):
    """Amendment §3: for run s7, an inventory row with n_features = k > 1 counts as k rows (one cluster)."""
    out = []
    for r in rows:
        out.append(r)
        m = re.search(r"n_features (\d+)", r.get("flags", "")) if r["origin"].startswith("iaa") else None
        if m:
            for i in range(1, int(m.group(1))):
                x = dict(r)
                x["id"] = f"{r['id']}#{i + 1}"
                out.append(x)
    return out


def run_view(rows, scroll):
    runs = {}
    for key, label, opts in C.RUNS:
        rr = expand_rows(rows) if opts.get("unit") == "rows" else rows
        res = C.run_one(rr, scroll, opts)
        res["label"] = label
        runs[key] = res
    for key, label, filt, opts in H.EXTRA_RUNS:
        if key in ("x1_catalogue_window", "x3_precedent_coding"):
            res = C.run_one(filt(rows), scroll, opts)
            res["label"] = label
            runs[key] = res
    bias = C.bias_checks(rows, scroll)
    return runs, bias


def score_rows(view, runs):
    out = []
    for k, r in runs.items():
        ci = r.get("D_ci95") or [None, None]
        row = {"view": view, "run": k, "label": r["label"], "scroll_n": r["n_a"],
               "comparanda_units": r["n_comparanda_units_total"], "comparanda_known": r["n_b"],
               "comparanda_unknown": r["n_comparanda_unknown"], "chi2": r.get("chi2"), "p": r.get("p"),
               "D": r.get("D"), "D_ci_low": ci[0], "D_ci_high": ci[1], "verdict": r["verdict"]}
        for g in C.COARSE_ORDER:
            row[f"comp_{g}"] = r["counts_b"].get(g, 0)
        out.append(row)
    return out


def analyse(b):
    scroll = read_csv(os.path.join(H.PREC_DIR, "scroll_contexts.csv"))
    cat = b["catalogue"]
    units = b["units"]
    view_lines = {l.get("id"): l for l in b["view"] if l.get("id")}
    a_rows = [u for u in units if view_lines[u["id"]]["in_view_A"] == "yes"]
    b_rows = [u for u in units if view_lines[u["id"]]["in_view_B"] == "yes"]
    bu_rows = [u for u in units if view_lines[u["id"]]["in_view_B_undetermined"] == "yes"]
    views = {
        "frozen": cat,
        "A_frozen_plus_p13": cat + a_rows,
        "B_frozen_plus_p1to4": cat + b_rows,
        "B_undetermined_counted": cat + bu_rows,
    }
    results, scores = {}, []
    for name, rows in views.items():
        runs, bias = run_view(rows, scroll)
        results[name] = {"runs": runs, "bias": bias, "summary": H.precedent_summary(
            {k: v for k, v in runs.items() if k in dict((x[0], 1) for x in C.RUNS)}, bias)}
        scores += score_rows(name, runs)
    # x2/x4: the inventory units alone (all are first read after the freeze)
    for name, rows in (("inventory_units_B", b_rows), ("inventory_units_p4", [u for u in b_rows if u["origin"] == "iaa_p4"])):
        res = C.run_one(rows, scroll, {})
        res["label"] = "Main run on the inventory units alone (x2/x4 analogue)"
        results[name] = {"runs": {"main": res}}
        scores += score_rows(name, {"main": res})
    # EXPLORATORY (chosen after seeing the rows): view B with the Third Wall tools catalogue row coded as the
    # phase-4 reader coded the full article (concealed in a rock pocket at a quarry edge, Stratum 4, 1st c. CE).
    tw = []
    for r in views["B_frozen_plus_p1to4"]:
        if r["id"] == "n_thirdwall_tools":
            r = dict(r, include="1", exclusion_reason="", setting="open_ground", placement="not_stated",
                     date_from="1", date_to="100")
        tw.append(r)
    res = C.run_one(tw, scroll, {})
    res["label"] = "EXPLORATORY: view B, Third Wall tools as coded by the Atiqot 88 reader"
    results["e_B_thirdwall_as_reader_coded"] = {"runs": {"main": res}}
    scores += score_rows("e_B_thirdwall_as_reader_coded", {"main": res})
    # frozen reproduction
    with open(os.path.join(LANE, "results.json"), encoding="utf-8") as f:
        frozen = json.load(f)
    repro = all(abs(results["frozen"]["runs"][k]["D"] - frozen["runs"][k]["D"]) < 1e-12 and
                results["frozen"]["runs"][k]["verdict"] == frozen["runs"][k]["verdict"] and
                results["frozen"]["runs"][k]["n_b"] == frozen["runs"][k]["n_b"] for k, _, _ in C.RUNS)
    depth = {n: H.depth_comparison(v) for n, v in views.items() if n != "frozen"}
    landmark = {n: H.landmark_comparison(v, scroll)["comparanda"] for n, v in views.items() if n != "frozen"}

    def unit_list(rows):
        return [{"id": u["id"], "site": u["site"], "source": u["source"], "setting": u["setting"],
                 "placement": u["placement"], "coarse_group": u["coarse_group"], "landmark": u["landmark"],
                 "depth_m": u["depth_m"], "date": f"{u['date_from']}..{u['date_to']}",
                 "in_window_main": u["in_window_main"], "judaea": u["in_region_judaea"]} for u in rows]

    st = {}
    for l in b["view"]:
        key = (l["phase"][:1] if l["phase"][:1] == "4" else "1-3", l["status"].split(":")[0])
        st["|".join(key)] = st.get("|".join(key), 0) + 1
    return {
        "amendment_sha256": AMENDMENT_SHA256, "amendment_commit": AMENDMENT_COMMIT,
        "plan_sha256": H.PLAN_SHA256,
        "inputs": {os.path.relpath(p, REPO): sha256(p) for p in
                   (os.path.join(MERGED, "features_all.csv"), PLACES, os.path.join(LANE, "hoards.csv"),
                    MANUAL, DEDUPE)},
        "frozen_reproduced": repro,
        "inventory": {"hoard_rows_counted": len(b["view"]), "status_by_phase": dict(sorted(st.items())),
                      "units": len(units), "candidate_pairs": len(b["pairs"])},
        "new_units_view_A": unit_list(a_rows),
        "new_units_view_B_phase4": unit_list([u for u in b_rows if u["origin"] == "iaa_p4"]),
        "undetermined_units": unit_list([u for u in bu_rows if u not in b_rows]),
        "results": results, "depth": depth, "landmark": landmark,
    }, scores


def outputs():
    b = build(strict=True)
    res, scores = analyse(b)
    view_b = csv_bytes(b["view"], VIEW_FIELDS)
    score_b = csv_bytes(scores, SCORE_FIELDS)
    sum_b = (json.dumps(res, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return {OUT_VIEW: view_b, OUT_SCORES: score_b, OUT_SUMMARY: sum_b}


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd == "candidates":
        b = build(strict=False)
        w = csv.writer(sys.stdout, lineterminator="\n")
        w.writerow(["kind", "a", "b", "detail"])
        for uid, field in b["missing_checks"]:
            w.writerow(["check", uid, field, ""])
        for a, c, basis in b["missing_pairs"]:
            w.writerow(["pair", a, c, basis])
    elif cmd == "run":
        for path, data in outputs().items():
            with open(path, "wb") as f:
                f.write(data)
        print("written")
    elif cmd == "check":
        for path, data in outputs().items():
            with open(path, "rb") as f:
                if f.read() != data:
                    raise SystemExit(f"{os.path.relpath(path, REPO)} differs from a fresh run")
        print("ok")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
