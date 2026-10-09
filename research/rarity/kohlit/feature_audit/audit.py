"""Koḥlit rarity count: feature-level audit of every positive condition (EXPLORATORY).

Made on 8 October 2026 UTC, after the registered result was seen. It changes no registered
number: stage2/RESULTS.md and its two addenda stay as recorded.

The audit imports stage2/match.py. A feature counts as "behind a MATCH" here exactly when
match.unit_values() lists it for that condition, so the qualifying rules are match.py's own.

Commands:
    python3 -I audit.py run PACKETS_DIR CODED_A_DIR CODED_B_DIR OUT_DIR
    python3 -I audit.py run-committed PACKETS_DIR OUT_DIR
    python3 -I audit.py readme OUT_DIR README_PATH

PACKETS_DIR holds packets/<unit>.json (packet v4). CODED_*_DIR hold the merged coder sheets
(scratch s2/coded_v3/{A,B}). "run-committed" rebuilds those sheets in memory from the committed
sheets, with the same merge functions and order as addendum_s2/run_addendum.sh.
"readme" rewrites the generated block of README.md from the two CSVs in OUT_DIR.
"""
from __future__ import annotations

import csv
import importlib.util
import itertools
import math
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
STAGE2 = HERE.parent / "stage2"
sys.path.insert(0, str(STAGE2))
import match as M  # noqa: E402

CONDS = M.CONDITIONS
KEYS = [(v, n) for v in M.C["variants"] for n in ("with", "without")]
WINDOW = "50 BCE-135 CE"
SRC_LABEL = {"1": "WBADB", "2": "survey entry", "3": "SWP", "4": "first publication", "5": "Nigro 2011"}
MAX_QUOTE_WORDS = 12
MAX_COMBOS = 200000

# Units in the order the README presents them (registered lists, RESULTS.md and the addenda).
BRANCH_B = ["S6040", "S2539", "S2589", "S3137", "E357"]
TWO_OF_THREE = ["S206", "E99", "S845", "S1032", "S1137", "S1502", "S1667", "S1929", "S2376", "S2430",
                "S2849", "S3036", "S3419", "S3961", "S843", "S2096", "S2594", "S3072"]
PRIORITY = ["S1283"] + BRANCH_B + ["E754", "E334"] + TWO_OF_THREE


# ---------------- loading ----------------

def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def committed_sheets():
    """The merged sheets, rebuilt in memory from the committed chain (as run_addendum.sh does)."""
    s4 = _load_module("merge_s4", STAGE2 / "addendum_s4" / "merge_s4.py")
    s2 = _load_module("merge_source", STAGE2 / "addendum_s2" / "merge_source.py")
    out = {}
    for coder in "AB":
        sheets = M.load_sheets(STAGE2 / "coded" / coder)
        add4 = M.load_sheets(STAGE2 / "addendum_s4" / "coded_s4" / coder)
        sheets = {u: (s4.merge(b, add4[u]) if u in add4 else b) for u, b in sheets.items()}
        if coder == "B":
            sheets.update(M.load_sheets(STAGE2 / "addendum_s4" / "coded_B_full"))
        add2 = M.load_sheets(STAGE2 / "addendum_s2" / "coded_s2" / coder)
        sheets = {u: (s2.merge(b, add2[u], "2", "s2z_") if u in add2 else b) for u, b in sheets.items()}
        if coder == "B":
            sheets.update(M.load_sheets(STAGE2 / "addendum_s2" / "coded_B_full"))
        out[coder] = sheets
    return out["A"], out["B"]


# ---------------- text helpers ----------------

STOP = set("""a an and or the of in on at to with is are was were be been by from for as it its this that these
those there which who also some one two three four five six seven eight nine ten than then into over under about
very more most other others such no not only all any each both near beside site""".split())


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def stem(w):
    return w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w


def toks(s):
    return {stem(w) for w in re.findall(r"[a-z0-9]+", fold(s)) if w not in STOP and (len(w) > 1 or w.isdigit())}


def containment(a, b):
    """Share of the smaller token set that the larger one contains (0 if either is empty)."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def short_quote(q, n=MAX_QUOTE_WORDS):
    w = (q or "").split()
    return " ".join(w) if len(w) <= n else " ".join(w[:n]) + " …"


# ---------------- place identity (WBADB rows and Nigro entries) ----------------

GENERIC = set("""tell tel tulul tall khirbet khirbat kh ain ein en wadi nahal area cave caves no north south east west
el es ed et er esh ez ash al ad abu umm deir beit bir birket birkat birkeh jebel ras qasr the of and church spring
upper lower rock shelter niche recess cemetery tomb tombs site ruin ruins village""".split())


def skeleton(w):
    if w.isdigit():
        return w
    w = w.replace("c", "k").replace("q", "k")
    return w[0] + re.sub(r"[aeiouyhw]", "", w[1:])


def name_keys(*names):
    keys = set()
    for n in names:
        for w in re.findall(r"[a-z0-9]+", fold(n)):
            if w in GENERIC:
                continue
            sk = skeleton(w)
            if len(sk) >= 2:
                keys.add(sk)
    return keys


class UnionFind:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            lo, hi = sorted((ra, rb))
            self.p[hi] = lo


def place_index(packet):
    """ref -> place id. Only duplicate WBADB rows are joined: two rows at the same point that share a
    distinctive name word; a Surveyed and an Excavations row at the same point with mostly the same
    component text; or a Surveyed and an Excavations row within 500 m that share a name word and almost
    all their component text. Every Nigro entry is its own place: a WBADB row and a Nigro entry of the
    same name are not joined, because a named area often holds several features of one type."""
    u = packet["unit"]
    nodes = {u["row_id"]: (u["x"], u["y"], name_keys(u["name"], u["other_names"]), u["sheet"], toks(u["components"]))}
    for r in packet["source1_wbadb_within_2km"]:
        nodes[r["row_id"]] = (r["x"], r["y"], name_keys(r["name"], r["other_names"]), r["sheet"], toks(r["components"]))
    uf = UnionFind(nodes)
    for a, b in itertools.combinations(sorted(nodes), 2):
        xa, ya, ka, sa, ca = nodes[a]
        xb, yb, kb, sb, cb = nodes[b]
        if None in (xa, ya, xb, yb):
            continue
        d = math.hypot(float(xa) - float(xb), float(ya) - float(yb))
        if d == 0 and ((ka & kb) or (sa != sb and containment(ca, cb) >= 0.5)):
            uf.union(a, b)
        elif d <= 500 and sa != sb and (ka & kb) and containment(ca, cb) >= 0.8:
            uf.union(a, b)
    out = {r: uf.find(r) for r in nodes}
    out.update({n["ref"]: n["ref"] for n in packet["source5_nigro_2011"]["entries"]})
    return out


# ---------------- feature identity ----------------

ROW_RE = re.compile(r"\b([SE]\d+)\b")
CAT_RE = re.compile(r"cat\.?\s*(\d+)", re.I)


def family(f):
    if f["type"] == "pool":
        return "pool"
    if f["type"] == "pit":
        return "tomb" if f.get("is_tomb") else "pit"
    if f["type"] == "grave":
        return "tomb"
    return "other"


def locus(f, unit_id, place):
    """('P', place id) for a WBADB row or Nigro entry; ('T', source, volume) for a text source."""
    src, p, cite = f["source"], f.get("position") or {}, f.get("cite", "")
    if src == "1":
        m = ROW_RE.search(cite)
        ref = m.group(1) if m else (p.get("ref") or unit_id)
        return ("P", place.get(ref, ref))
    if src == "5":
        m = CAT_RE.search(cite)
        ref = "N" + m.group(1) if m else (p.get("ref") or "")
        return ("P", place.get(ref, ref))
    m = re.search(r"Mem\.?\s*(III|II|I)\b", cite) if src == "3" else None
    return ("T", src, m.group(1) if m else "")


def _expand(part):
    m = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", part)
    if not m:
        return {int(part)} if part.isdigit() else set()
    a, b = m.group(1), m.group(2)
    if len(b) < len(a):
        b = a[: len(a) - len(b)] + b
    a, b = int(a), int(b)
    return set(range(a, b + 1)) if 0 <= b - a <= 60 else {a, b}


def pages(cite):
    out = set()
    for m in re.finditer(r"\bpp?\.\s*([\d][\d\s,–\-]*)", cite or ""):
        for part in re.split(r"[,\s]+(?![-–])", m.group(1).strip()):
            out |= _expand(part.strip().replace(" ", ""))
    return out


def figs(cite):
    out = set()
    for m in re.finditer(r"\b(figs?|pls?)\.?\s*([\dxivlc][\dxivlc\s,–\-]*)", fold(cite or "")):
        for part in re.split(r"[,\s]+", m.group(2).strip()):
            if part:
                out.add(m.group(1)[:2] + part)
    return out


def same_passage(f, g, la, lb):
    """Two text-source features from the same passage: same source and volume, overlapping pages or
    figures (if both give pages), and mostly the same quoted words."""
    if la != lb or la[0] != "T":
        return False
    pa, pb = pages(f.get("cite")), pages(g.get("cite"))
    if pa and pb and not (pa & pb) and not (figs(f.get("cite")) & figs(g.get("cite"))):
        return False
    return containment(toks(f.get("quote")), toks(g.get("quote"))) >= 0.6


def placed_at(f, place):
    p = f.get("position") or {}
    return place.get(p.get("ref")) if p.get("kind") == "grid" else None


def identity_groups(unit_id, packet, sheets):
    """Group the coders' features that describe the same physical feature.

    sheets: {coder: sheet}. Returns ({(coder, fid): group id}, {group id: basis}).
    Links (always within one family: pool, pit or tomb):
      row      same WBADB row or Nigro entry (or a duplicate WBADB row of the same place) and mostly
               the same quoted words;
      passage  same text-source passage (see same_passage), or the same page of the same text source
               placed by both records at the same row or entry;
      placed   a text-source feature that a coder placed at a row or entry, joined to that record's
               feature of the same family when the record has exactly one such group and the text
               source has exactly one group placed there."""
    place = place_index(packet)
    feats = [(c, f) for c in sorted(sheets) for f in sheets[c]["features"]]
    keys = [(c, f["id"]) for c, f in feats]
    uf = UnionFind(keys)
    loc = {(c, f["id"]): locus(f, unit_id, place) for c, f in feats}
    basis = defaultdict(set)

    def link(ka, kb, why):
        uf.union(ka, kb)
        basis[ka].add(why)
        basis[kb].add(why)

    for (ca, fa), (cb, fb) in itertools.combinations(feats, 2):
        ka, kb = (ca, fa["id"]), (cb, fb["id"])
        if family(fa) != family(fb):
            continue
        la, lb = loc[ka], loc[kb]
        if la[0] == "P" and la == lb and containment(toks(fa.get("quote")), toks(fb.get("quote"))) >= 0.5:
            link(ka, kb, "row")
        elif same_passage(fa, fb, la, lb):
            link(ka, kb, "passage")
        elif la[0] == "T" and la == lb and placed_at(fa, place) and placed_at(fa, place) == placed_at(fb, place) \
                and pages(fa.get("cite")) & pages(fb.get("cite")):
            link(ka, kb, "passage")
    # a text-source feature placed at a row or entry, joined to that record's feature
    at_place = defaultdict(lambda: defaultdict(set))  # (place, family) -> "record" or "T<source>" -> {group roots}
    for c, f in feats:
        k = (c, f["id"])
        if loc[k][0] == "P":
            at_place[(loc[k][1], family(f))]["record"].add(uf.find(k))
        elif placed_at(f, place):
            at_place[(placed_at(f, place), family(f))]["T" + f["source"]].add(uf.find(k))
    for (pl, fam), kinds in sorted(at_place.items()):
        rec = kinds.get("record", set())
        if len(rec) != 1:
            continue
        r = next(iter(rec))
        for kind, groups in sorted(kinds.items()):
            if kind != "record" and len(groups) == 1:
                t = next(iter(groups))
                if uf.find(t) != uf.find(r):
                    link(t, r, "placed")
    roots, gid = {}, {}
    for k in keys:
        r = uf.find(k)
        if r not in roots:
            roots[r] = f"{unit_id}:g{len(roots) + 1:02d}"
        gid[k] = roots[r]
    gbasis = defaultdict(set)
    for k in keys:
        gbasis[gid[k]] |= basis[k]
    return gid, {g: ("+".join(sorted(b)) if b else "one record") for g, b in gbasis.items()}


# ---------------- dates ----------------

STRADDLE = re.compile(r"2nd c|second century|late rom", re.I)
IN_WINDOW = re.compile(r"\brom|herod|hasmon|maccab|second temple|\bhel\b|\bhel-|hellenist|nabat|"
                       r"1st c|first century|bar kokhba|"
                       r"periods? ib\s*-\s*ii|period ii\b|period ib\b", re.I)  # last three: de Vaux's Qumran periods
BEFORE = re.compile(r"\b(ia\d*\w*|iron|eb\d*\w*|early bronze|mb\d*\w*|middle bronze|lb|late bronze|ib|"
                    r"intermediate bronze|chal\w*|neolith\w*|ppn\w*|pn|natuf\w*|per|persian|paleo\w*|"
                    r"pottery neolithic|pre-pottery)\b|\d{3,4}\s*bce", re.I)
OUT_OF_USE = re.compile(r"out of use|defunct|filled in|abandoned before|destroyed before", re.I)


def date_class(f):
    """How a feature's date code and basis sit against the window (50 BCE-135 CE).

    after 135 CE (code L) / undated (code U) / for code D: straddles 135 CE (a 2nd-century or late Roman
    date), in window (a period that overlaps the window), before window (only earlier periods), before
    window, out of use (earlier periods and stated out of use), D, period not stated."""
    code, basis = f["date"]["code"], f["date"].get("basis", "")
    if code == "L":
        return "after 135 CE"
    if code == "U":
        return "undated"
    if STRADDLE.search(basis):
        return "straddles 135 CE"
    if IN_WINDOW.search(basis):
        return "in window"
    if BEFORE.search(basis):
        return "before window, out of use" if OUT_OF_USE.search(basis) else "before window"
    return "D, period not stated"


# ---------------- positions ----------------

def cond_params(c, v):
    """Sector, limit and east-part flag for condition c under variant v, as match.evaluate sets them.
    Used only to describe why a counterpart feature does not qualify; qualification itself is
    always taken from match.unit_values()."""
    lim = dict(M.C["limits_m"])
    lim.update({k: val for k, val in v.items() if k in lim})
    sec = M.C["sectors_deg"]
    return {"C1": (sec["C1_east"], lim["C1"], True), "C2": (sec["C2_north"], lim["C2"], False),
            "C3s": (sec["C3_north"], lim["C3_survey"], False), "C3t": (sec["C3_north"], lim["C3_survey"], False)}[c]


def pos_fields(f, refs):
    p = f.get("position") or {}
    kind = p.get("kind", "none")
    out = {"pos_kind": kind, "pos_ref": "", "pos_direction": "", "pos_bearing_deg": "", "pos_distance_m": "",
           "pos_relative_to": "", "pos_precision_m": "", "pos_bearing_valid": ""}
    if kind == "grid":
        g = refs.get(p.get("ref")) or {}
        out.update(pos_ref=p.get("ref", ""), pos_bearing_deg=g.get("bearing_deg", ""), pos_distance_m=g.get("distance_m", ""),
                   pos_relative_to="unit point", pos_precision_m=g.get("precision_m", ""),
                   pos_bearing_valid=g.get("bearing_valid", ""))
    elif kind == "plan":
        out.update(pos_bearing_deg=p.get("bearing_deg", ""), pos_distance_m=p.get("distance_m", ""),
                   pos_relative_to="unit centre on a plan (coder-measured)")
    elif kind == "words":
        out.update(pos_direction=p.get("direction", ""), pos_distance_m=p.get("distance_m") if p.get("distance_m") is not None else "",
                   pos_relative_to=p.get("relative_to", ""))
    return {k: ("" if v is None else v) for k, v in out.items()}


def pos_summary(f, refs):
    p = f.get("position") or {}
    kind = p.get("kind")
    if kind == "grid":
        g = refs.get(p.get("ref")) or {}
        b = g.get("bearing_deg")
        return f"{p.get('ref')} {g.get('distance_m')} m {b if b is not None else '?'}°" + ("" if g.get("bearing_valid") else " (bearing invalid)")
    if kind == "plan":
        return f"plan {p.get('bearing_deg')}° {p.get('distance_m')} m"
    if kind == "words":
        d = p.get("distance_m")
        rel = "" if p.get("relative_to") == "unit" else " of another feature"
        return f"{p.get('direction')}{rel}" + (f" {d} m" if d is not None else "") + " (words)"
    return "no position"


def why_not(g, c, v, refs):
    """Plain reason why feature g does not qualify for condition c (descriptive only)."""
    if c == "C3t":
        return "no grave at a qualifying pit's mouth"
    if not M.date_ok(g, v):
        return f"date {g['date']['code']}"
    sector, limit, east = cond_params(c, v)
    pos = M.position(g, sector, limit, refs, east)
    if pos is None:
        return f"no usable position ({pos_summary(g, refs)})"
    if pos is False:
        return f"outside the sector or limit ({pos_summary(g, refs)})"
    detail = g.get("pool_def", g.get("is_tomb", g.get("cavity_with_opening", "")))
    return f"type or definition ({g['type']}, {detail})"


DIR_OF = re.compile(r"\b(?:north|south|east|west)(?:ern|ward|wards)?\s+(?:side\s+|end\s+|part\s+)?of\s+(?:the\s+)?[\"“”']?([a-z][a-z\-]*)", re.I)
SITE_WORDS = {"site", "summit", "tell", "tel", "ruin", "ruins", "village", "khirbet", "khirbat", "kh", "hill", "mound",
              "town", "settlement", "top", "acropolis", "it", "here", "tells"}


def reference_object(f, unit_words):
    """The object a source's direction is taken from, if it is not the site itself (heuristic on the quote)."""
    p = f.get("position") or {}
    if p.get("kind") != "words" or p.get("relative_to") != "unit":
        return ""
    for m in DIR_OF.finditer(fold(f.get("quote", ""))):
        obj = m.group(1)
        if obj not in SITE_WORDS and obj not in unit_words:
            return obj
    return ""


def on_edge(f, c, refs):
    if c not in ("C1", "C2", "C3s"):
        return ""
    p = f.get("position") or {}
    b = None
    if p.get("kind") == "grid":
        b = (refs.get(p.get("ref")) or {}).get("bearing_deg")
    elif p.get("kind") == "plan" and p.get("bearing_deg") is not None:
        b = float(p["bearing_deg"]) % 360
    sector = cond_params(c, {})[0]
    return f"{b}°" if b is not None and float(b) in (float(sector[0]), float(sector[1])) else ""


def reading(f):
    """The reading a coder gave a feature's position: a compass word from the site ('east part' counts
    as E), 'grid', 'plan', 'from another feature', or '' (no position)."""
    p = f.get("position") or {}
    if p.get("kind") == "words":
        if p.get("relative_to") != "unit":
            return "from another feature"
        d = (p.get("direction") or "").strip()
        return "E" if d.lower() in M.C["east_part_words"] else d.upper()
    return "" if p.get("kind") in (None, "none") else p.get("kind")


# ---------------- the audit ----------------

def unit_meta():
    try:
        return M.all_units()
    except OSError:
        return {}


PLURAL = re.compile(r"\b(tombs|graves|burials|cemetery|cemeteries|necropolis|kokhim|loculi|caves|cisterns|pits|silos)\b", re.I)


class Unit:
    """Everything the audit needs about one unit: sheets, match.py values, identity groups."""

    def __init__(self, uid, packet, sheets):
        self.uid, self.packet, self.sheets = uid, packet, sheets
        self.refs = M.refs_in_packet(packet)
        self.vals = {c: M.unit_values(s, self.refs) for c, s in sheets.items()}
        self.gid, self.gbasis = identity_groups(uid, packet, sheets)
        self.byid = {c: {f["id"]: f for f in s["features"]} for c, s in sheets.items()}
        self.place = place_index(packet)
        self.members = defaultdict(list)
        for (c, fid), g in self.gid.items():
            self.members[g].append(f"{c}:{fid}")
        self.unit_words = set(re.findall(r"[a-z]+", fold(packet["unit"]["name"] + " " + packet["unit"]["other_names"])))

    def any_match(self):
        return any(self.vals[c][k][cd] == "MATCH" for c in self.vals for k in KEYS for cd in CONDS)

    def qualifying(self, x, key, c):
        return list(self.vals[x][key]["_features"][c])

    def groups(self, x, key, c):
        return {self.gid[(x, fid)] for fid in self.qualifying(x, key, c)}

    def merged(self, key, c):
        a = self.vals["A"][key][c]
        return a if "B" not in self.vals or self.vals["B"][key][c] == a else "UNKNOWN"

    def counterpart(self, x, fid, c, key):
        """(text, ok): how the other coder recorded the same physical feature.
        ok is True if the other coder's record also qualifies, False if not, None if the unit has one coder."""
        y = "B" if x == "A" else "A"
        if y not in self.sheets:
            return f"{y} did not code this unit", None
        g = self.gid[(x, fid)]
        ys = [f for f in self.sheets[y]["features"] if self.gid[(y, f["id"])] == g]
        if not ys:
            f = self.byid[x][fid]
            lf = locus(f, self.uid, self.place)
            other = [h for h in self.sheets[y]["features"] if family(h) != family(f)
                     and locus(h, self.uid, self.place) == lf
                     and containment(toks(h.get("quote")), toks(f.get("quote"))) >= 0.8]
            if other:
                return "; ".join(f"{y} {h['id']} records the same words as {h['type']}" +
                                 (" (tomb)" if h.get("is_tomb") else "") for h in other), False
            return f"not recorded by {y}", False
        q = set(self.qualifying(y, key, c))
        hit = [f["id"] for f in ys if f["id"] in q]
        if hit:
            return f"{y} {','.join(hit)} qualifies", True
        v = M.C["variants"][key[0]]
        return "; ".join(f"{y} {f['id']}: {why_not(f, c, v, self.refs)}" for f in ys), False


def audit(packets, A, B):
    """Returns (feature_rows, joint_rows, {unit_id: Unit})."""
    meta = unit_meta()
    feature_rows, joint_rows, units = [], [], {}
    order = {u: i for i, u in enumerate(PRIORITY)}
    for uid in sorted(A, key=lambda u: (order.get(u, len(order)), u)):
        U = Unit(uid, packets[uid], {"A": A[uid]} | ({"B": B[uid]} if uid in B else {}))
        if not U.any_match():
            continue
        units[uid] = U
        m = meta.get(uid, {})
        base = {"unit_id": uid, "name": U.packet["unit"]["name"],
                "main_set": m.get("main", U.packet["unit"].get("main_set")),
                "in_R2": m.get("R2", U.packet["unit"].get("in_R2"))}
        for key in KEYS:
            for c in CONDS:
                for x in sorted(U.sheets):
                    if U.vals[x][key][c] != "MATCH":
                        continue
                    y = "B" if x == "A" else "A"
                    if y not in U.sheets:
                        flag = "single coder"
                    elif U.vals[y][key][c] != "MATCH":
                        flag = f"{y} not MATCH"
                    else:
                        flag = "shared feature" if U.groups("A", key, c) & U.groups("B", key, c) else "NO SHARED FEATURE"
                    for fid in U.qualifying(x, key, c):
                        f = U.byid[x][fid]
                        g = U.gid[(x, fid)]
                        row = dict(base, variant=key[0], nigro=key[1], condition=c, merged=U.merged(key, c), coder=x,
                                   coder_value="MATCH", other_coder_value=U.vals[y][key][c] if y in U.sheets else "",
                                   condition_flag=flag, feature_id=fid, source=f["source"], cite=f.get("cite", ""),
                                   quote=short_quote(f.get("quote", "")), type=f["type"], subtype=f.get("subtype", ""),
                                   type_detail=f.get("pool_def", f.get("is_tomb", f.get("cavity_with_opening", ""))))
                        row.update(pos_fields(f, U.refs))
                        row.update(date_code=f["date"]["code"], date_basis=f["date"].get("basis", ""),
                                   date_class=date_class(f), identity_group=g, identity_basis=U.gbasis[g],
                                   identity_members=" ".join(sorted(U.members[g])),
                                   other_coder_same_feature=U.counterpart(x, fid, c, key)[0])
                        feature_rows.append(row)
            matched = [c for c in CONDS if U.merged(key, c) == "MATCH"]
            if len(matched) >= 2:
                joint_rows.append(joint_test(U, key, matched, base))
    return feature_rows, joint_rows, units


DATE_TEXT = {"undated": f"undated: must exist in {WINDOW}",
             "before window": "dated only before the window: must survive into it",
             "straddles 135 CE": "dated to a period that runs past 135 CE: must date before 135 CE",
             "D, period not stated": "dated D with no period stated"}


def clip(s, n=110):
    return s if len(s) <= n else s[: n - 1] + "…"


def ctext(t):
    """Text of one condition (kind, core, detail)."""
    return f"{t[1]} ({t[2]})" if t[2] else t[1]


def feature_conditions(U, x, f, c, key, dispute=True):
    """(fatal reason or '', [(kind, core text, detail)]) for coder x using feature f for condition c."""
    conds, fatal = [], ""
    dc = date_class(f)
    basis = clip(f["date"].get("basis", ""))
    if dc in DATE_TEXT:
        conds.append(("date", DATE_TEXT[dc], basis))
    elif dc == "before window, out of use":
        fatal = f"{x} {f['id']} is dated before the window and stated out of use ({basis})"
    if dispute:
        cp, ok = U.counterpart(x, f["id"], c, key)
        if ok is False:
            conds.append(("dispute", f"disputed: {cp}", ""))
    obj = reference_object(f, U.unit_words)
    if obj:
        conds.append(("reference", f"the source gives the direction from '{obj}', not from the site", ""))
    edge = on_edge(f, c, U.refs)
    if edge:
        conds.append(("edge", f"bearing {edge} lies on the sector edge (inside only by the inclusive rule)", ""))
    if (f.get("position") or {}).get("kind") == "plan":
        conds.append(("plan", "bearing measured by the coder on a plan, from a centre the coder chose", ""))
    r = reading(f)
    if r and r not in ("grid", "plan", "from another feature"):
        q = toks(f.get("quote"))
        for g in U.sheets[x]["features"]:
            if g["id"] == f["id"] or g["source"] != f["source"] or not q or toks(g.get("quote")) != q:
                continue
            rg = reading(g)
            if rg == r:
                continue
            if f["type"] == "pool" and (f.get("position") or {}).get("direction", "").lower() in M.C["east_part_words"] \
                    and g["type"] != "pool" and rg == "":
                continue  # 'east part' is allowed for C1 only (PROTOCOL.md §4), so a pit from the same words has no position
            conds.append(("reading", f"the coder reads the same words as '{r}' here but as '{rg or 'no position'}' for {g['id']}", ""))
    return fatal, conds


def best_combo(options, matched):
    """options: {condition: [(group, label, fatal, [(kind, text)], plural)]}.
    Returns (number of valid combinations, best or None, reason if none)."""
    lists = [options[c] for c in matched]
    if any(not li for li in lists):
        return 0, None, "no qualifying feature"
    total = 1
    for li in lists:
        total *= len(li)
    if total > MAX_COMBOS:
        return -1, None, f"too many combinations ({total})"
    n_valid, best, reasons = 0, None, set()
    for combo in itertools.product(*lists):
        groups = [o[0] for o in combo]
        extra = []
        if len(set(groups)) < len(groups):
            reused = [o for o in combo if groups.count(o[0]) > 1]
            if not all(o[4] for o in reused):
                reasons.add("the only qualifying features would use one physical feature twice")
                continue
            extra = [f"{reused[0][1]} is one record of several features: one must serve as the pit and another as the graves"]
        fatal = [o[2] for o in combo if o[2]]
        if fatal:
            reasons.add(fatal[0])
            continue
        n_valid += 1
        conds = sorted({f"{o[1]}: {ctext(t)}" for o in combo for t in o[3]}) + extra
        score = (bool(extra), len(conds), [o[1] for o in combo])  # prefer combinations that use no record twice
        if best is None or score < best[0]:
            best = (score, combo, conds)
    if best is None:
        return 0, None, "; ".join(sorted(reasons))
    return n_valid, {"features": dict(zip(matched, [o[1] for o in best[1]])), "conditions": best[2]}, ""


def _options_for_coder(U, x, key, matched):
    opts = {}
    for c in matched:
        per_group = {}
        for fid in U.qualifying(x, key, c):
            f = U.byid[x][fid]
            fatal, conds = feature_conditions(U, x, f, c, key)
            cand = (U.gid[(x, fid)], f"{x} {fid}", fatal, conds, bool(PLURAL.search(f.get("subtype", "") + " " + f.get("quote", ""))))
            old = per_group.get(cand[0])
            if old is None or (bool(fatal), len(conds), cand[1]) < (bool(old[2]), len(old[3]), old[1]):
                per_group[cand[0]] = cand
        opts[c] = [per_group[g] for g in sorted(per_group)]
    return opts


def _options_consensus(U, key, matched):
    """Groups that both coders qualify; each group's conditions come from both coders' records."""
    opts = {}
    for c in matched:
        lst = []
        for g in sorted(U.groups("A", key, c) & U.groups("B", key, c)):
            per = {}
            for x in ("A", "B"):
                fid = sorted(fid for fid in U.qualifying(x, key, c) if U.gid[(x, fid)] == g)[0]
                f = U.byid[x][fid]
                per[x] = (fid, f, feature_conditions(U, x, f, c, key, dispute=False))
            label = f"A {per['A'][0]} = B {per['B'][0]}"
            fatal = "; ".join(p[2][0] for p in per.values() if p[2][0])
            texts = {x: {t[0]: t for t in per[x][2][1]} for x in per}
            conds = []
            for kind in sorted(set(texts["A"]) | set(texts["B"])):
                ta, tb = texts["A"].get(kind), texts["B"].get(kind)
                if ta and tb and ta[1] == tb[1]:
                    conds.append((kind, ta[1] + " (both coders)", ""))
                elif ta and tb:
                    conds.append((kind, f"A: {ctext(ta)}; B: {ctext(tb)}", ""))
                else:
                    conds.append((kind, f"{'A' if ta else 'B'} only: {ctext(ta or tb)}", ""))
            plural = all(PLURAL.search(p[1].get("subtype", "") + " " + p[1].get("quote", "")) for p in per.values())
            lst.append((g, label, fatal, conds, plural))
        opts[c] = lst
    return opts


def joint_test(U, key, matched, base):
    two = "B" in U.sheets
    out = dict(base, variant=key[0], nigro=key[1], matched_conditions="+".join(matched), coders="A+B" if two else "A only")
    shared = {c: ("yes" if U.groups("A", key, c) & U.groups("B", key, c) else "no") if two else "n.a." for c in matched}
    out["same_feature_both_coders"] = " ".join(f"{c}:{shared[c]}" for c in matched)
    results = {x: best_combo(_options_for_coder(U, x, key, matched), matched) for x in sorted(U.sheets)}
    if two:
        results["consensus"] = best_combo(_options_consensus(U, key, matched), matched)
    for x in ("consensus", "A", "B"):
        n, best, why = results.get(x, (None, None, ""))
        out[f"{x}_valid_combinations"] = "" if n is None else n
        out[f"{x}_best"] = "" if not best else "; ".join(f"{c}: {best['features'][c]}" for c in matched)
        out[f"{x}_conditions"] = "" if n is None else (" | ".join(best["conditions"]) if best else f"none: {why}")
    lead = results["consensus"] if two else results["A"]
    note = "" if two else "Coder A only; no second coder checked these features. "
    if lead[1] and not lead[1]["conditions"]:
        verdict, why = "jointly compatible", note + "One feature set meets every matched condition: distinct features, " \
                                                    "all dated in the window, no dispute."
    elif any(r[1] for r in results.values()):
        verdict = "conditionally compatible"
        if lead[1]:
            why = note + " | ".join(lead[1]["conditions"])
        else:
            no = ", ".join(c for c in matched if shared[c] == "no")
            why = f"No feature set that both coders accept ({no}: no shared feature). " + \
                  " / ".join(f"Coder {x}: " + " | ".join(results[x][1]["conditions"]) for x in ("A", "B") if results[x][1])
    else:
        verdict = "not shown compatible"
        why = note + " / ".join(f"{x}: {results[x][2]}" for x in sorted(results))
    out["verdict"], out["verdict_conditions"] = verdict, why
    return out


# ---------------- output ----------------

FEATURE_FIELDS = ["unit_id", "name", "main_set", "in_R2", "variant", "nigro", "condition", "merged", "coder", "coder_value",
                  "other_coder_value", "condition_flag", "feature_id", "source", "cite", "quote", "type", "subtype",
                  "type_detail", "pos_kind", "pos_ref", "pos_direction", "pos_bearing_deg", "pos_distance_m",
                  "pos_relative_to", "pos_precision_m", "pos_bearing_valid", "date_code", "date_basis", "date_class",
                  "identity_group", "identity_basis", "identity_members", "other_coder_same_feature"]
JOINT_FIELDS = ["unit_id", "name", "main_set", "in_R2", "variant", "nigro", "matched_conditions", "coders",
                "same_feature_both_coders", "verdict", "verdict_conditions",
                "consensus_valid_combinations", "consensus_best", "consensus_conditions",
                "A_valid_combinations", "A_best", "A_conditions", "B_valid_combinations", "B_best", "B_conditions"]


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def run(packets, A, B, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frows, jrows, _ = audit(packets, A, B)
    write_csv(out_dir / "features_behind_matches.csv", frows, FEATURE_FIELDS)
    write_csv(out_dir / "joint_compatibility.csv", jrows, JOINT_FIELDS)
    prim = [r for r in jrows if r["variant"] == "primary" and r["nigro"] == "with"]
    flagged = sorted({(r["unit_id"], r["condition"]) for r in frows if r["variant"] == "primary" and r["nigro"] == "with"
                      and r["condition_flag"] == "NO SHARED FEATURE"})
    print(f"{len(frows)} feature rows for {len({r['unit_id'] for r in frows})} units; {len(jrows)} joint rows "
          f"({len(prim)} primary/with)")
    print("primary/with conditions where both coders MATCH on different features:", flagged)
    for r in prim:
        print(f"  {r['unit_id']:6} {r['matched_conditions']:8} {r['verdict']}")


# ---------------- README tables ----------------

MARK_START, MARK_END = "<!-- generated tables: start -->", "<!-- generated tables: end -->"


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _pos(r):
    return {"grid": f"{r['pos_ref']} {r['pos_distance_m']} m {r['pos_bearing_deg']}°",
            "plan": f"plan {r['pos_bearing_deg']}° {r['pos_distance_m']} m",
            "words": f"{r['pos_direction']} (words" + (f", {r['pos_distance_m']} m)" if r["pos_distance_m"] else ")")
            }.get(r["pos_kind"], "no position")


def _feat_label(r, n=34):
    sub = r["subtype"] if len(r["subtype"]) <= n else r["subtype"][: n - 1] + "…"
    return f"{r['feature_id']} {sub} ({SRC_LABEL.get(r['source'], r['source'])}; {_pos(r)}; {r['date_code']})"


def _short(r, n=24):
    sub = r["subtype"] if len(r["subtype"]) <= n else r["subtype"][: n - 1] + "…"
    return f"{r['feature_id']} {sub} ({_pos(r)}; {r['date_code']})"


def _cell(rows, coder, coded):
    labs = [_feat_label(r) for r in rows if r["coder"] == coder]
    if labs:
        return "; ".join(labs)
    return "not MATCH" if coded else "not coded"


def markdown_tables(out_dir):
    """Per-unit tables for the README, primary rules with Nigro, from the two CSVs."""
    frows = _read(Path(out_dir) / "features_behind_matches.csv")
    jrows = _read(Path(out_dir) / "joint_compatibility.csv")
    jprim = {r["unit_id"]: r for r in jrows if r["variant"] == "primary" and r["nigro"] == "with"}
    units = list(dict.fromkeys(r["unit_id"] for r in frows))
    lines = []

    def setting_rows(u):
        rows = [r for r in frows if r["unit_id"] == u and r["variant"] == "primary" and r["nigro"] == "with"]
        if rows:
            return rows, ""
        first = [r for r in frows if r["unit_id"] == u]
        k = (first[0]["variant"], first[0]["nigro"])
        return [r for r in first if (r["variant"], r["nigro"]) == k], f"{k[0]}, {k[1]} Nigro"

    for u in [u for u in units if u in jprim]:
        rows, _ = setting_rows(u)
        j = jprim[u]
        two = j["coders"] == "A+B"
        name = rows[0]["name"] if rows[0]["name"] not in ("", "-") else "unnamed"
        lines += [f"#### {name} ({u})", "",
                  "| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |",
                  "|---|---|---|---|---|"]
        for c in CONDS:
            rc = [r for r in rows if r["condition"] == c]
            if rc:
                lines.append(f"| {c} | {rc[0]['merged']} | {_cell(rc, 'A', True)} | {_cell(rc, 'B', two)} | {rc[0]['condition_flag']} |")
        lines += ["", f"Joint test ({j['matched_conditions']}): **{j['verdict']}**. {j['verdict_conditions']}", ""]
    lines += ["#### Every other unit with a MATCH", "",
              "One row per unit. Primary rules with Nigro; a unit that matches only in a variant shows its first such setting.",
              "Each cell lists condition: merged value, then coder A's and coder B's features ('-' = no MATCH, 'n.c.' = not coded).", "",
              "| Unit | Setting | Conditions and features | Same physical feature? |", "|---|---|---|---|"]
    for u in [u for u in units if u not in jprim]:
        rows, setting = setting_rows(u)
        parts, flags = [], []
        for c in CONDS:
            rc = [r for r in rows if r["condition"] == c]
            if not rc:
                continue
            coded_b = any(r["coder"] == "B" for r in rc) or rc[0]["other_coder_value"] != ""
            a = ", ".join(_short(r) for r in rc if r["coder"] == "A") or "-"
            b = ", ".join(_short(r) for r in rc if r["coder"] == "B") or ("-" if coded_b else "n.c.")
            parts.append(f"{c} {rc[0]['merged']}: A {a}; B {b}")
            flags.append(f"{c}: {rc[0]['condition_flag']}")
        name = rows[0]["name"] if rows[0]["name"] not in ("", "-") else "unnamed"
        lines.append(f"| {name} ({u}) | {setting or 'primary'} | {' / '.join(parts)} | {'; '.join(flags)} |")
    return "\n".join(lines)


def update_readme(out_dir, readme):
    text = Path(readme).read_text(encoding="utf-8")
    i, j = text.index(MARK_START), text.index(MARK_END)
    new = text[: i + len(MARK_START)] + "\n" + markdown_tables(out_dir) + "\n" + text[j:]
    Path(readme).write_text(new, encoding="utf-8")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or [""]
    if cmd == "run" and len(args) == 4:
        run(M.load_packets(args[0]), M.load_sheets(args[1]), M.load_sheets(args[2]), args[3])
    elif cmd == "run-committed" and len(args) == 2:
        a, b = committed_sheets()
        run(M.load_packets(args[0]), a, b, args[1])
    elif cmd == "readme" and len(args) == 2:
        update_readme(*args)
    else:
        sys.exit(__doc__)
