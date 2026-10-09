"""The project's inference rules applied to one recovery case.

Every rule is a small predicate that returns True (supported), False (contradicted)
or None (unknown). The rules are borrowed, not invented here:

- Direction words cover 90-degree sectors. A verbal NE, SE, SW or NW on the edge of a
  cardinal sector gives unknown. Numeric bearings use inclusive sector edges.
  (research/rarity/kohlit/stage2/PROTOCOL.md section 4, position rule 3;
  match.py in_sector() and position().)
- A words position with no distance counts as within the distance limit.
  (PROTOCOL.md section 4.) A words position relative to something other than the
  instruction's reference gives unknown (match.py position(), relative_to != unit).
- With no stated distance, the project's 1 km limit applies
  (protocol_constants.json limits_m).
- Dates: D and U pass, L fails (PROTOCOL.md section 11; match.py date_ok()).
- Unknown never counts as absence. One contradiction rejects a candidate; any unknown
  leaves it alive (feature_workbench/relationships/evaluate.py conjunction()).
- Cubits use the exploratory 0.40-0.60 m range
  (research/assessments/entry29_jericho_pools/README.md).

Selection: the survivors are the candidates with no contradicted predicate.
No survivor gives "none". More than one survivor gives "insufficient_evidence".
One survivor is selected only if every predicate is supported; if one is unknown,
the decisive predicate is unknown and the output is "insufficient_evidence".

The withheld relationship is predicted only when the instruction states it or the
selected candidate's recorded fields give it. Otherwise it is "unknown".

Standard library only. Run with python3 -I.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = json.loads((HERE / "procedure_constants.json").read_text(encoding="utf-8"))
COMPASS = K["compass_deg"]
DIRWORDS = K["direction_words"]
HALF = K["sector_half_width_deg"]
LEX = {t: v for t, v in K["type_lexicon"].items() if not t.startswith("_")}
SITE_TOKENS = set(K["site_level_tokens"])

_UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
          "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
          "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
          "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
          "seventy": 70, "eighty": 80, "ninety": 90}
_DIR_RE = "|".join(sorted((w for w in DIRWORDS if len(w) > 3), key=len, reverse=True))
_OPEN_NOUN = r"(?:opening|entrance|mouth|doorway|door)"


# ---------------------------------------------------------------- text helpers

def normalise(text: str) -> str:
    """Lower case, and join compound direction words ("north-east" -> "northeast")."""
    t = (text or "").lower().replace("’", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"\b(north|south)[\s-]+(east|west)", r"\1\2", t)
    t = re.sub(r"\b(north|south|east|west)[\s-]+(north|south)(east|west)", r"\1\2\3", t)
    return re.sub(r"\s+", " ", t).strip()


def dir_code(word):
    """Map a direction word or code to a compass code such as "NE", or None."""
    if word is None:
        return None
    w = re.sub(r"[^a-z]", "", str(word).lower())
    w = re.sub(r"(ern)$", "", w) if w not in DIRWORDS else w
    return DIRWORDS.get(w) or DIRWORDS.get(w + "ern")


def words_to_number(tokens):
    """Read number words such as ["one", "hundred", "and", "twenty"] -> 120."""
    total, current, seen = 0, 0, False
    for tok in tokens:
        if tok.isdigit():
            current += int(tok)
            seen = True
        elif tok in _UNITS:
            current += _UNITS[tok]
            seen = True
        elif tok == "hundred":
            current = max(current, 1) * 100
            seen = True
        elif tok == "thousand":
            total += max(current, 1) * 1000
            current = 0
            seen = True
        elif tok == "and":
            continue
        else:
            return None
    return total + current if seen else None


def in_sector(b, lo, hi):
    """Inclusive sector test, as match.py in_sector()."""
    return lo <= b <= hi if lo <= hi else (b >= lo or b <= hi)


def sector_of(code):
    a = COMPASS[code]
    return ((a - HALF) % 360, (a + HALF) % 360)


def angle_diff(a, b):
    return abs((a - b + 180) % 360 - 180)


# ---------------------------------------------------------------- instruction parsing

_DEPTH_BEFORE = re.compile(r"\b(dig|digging|dug|deep|depth|down|below|beneath|under|high|height)\b[^,;.]{0,12}$")
_DEPTH_AFTER = re.compile(r"^\s*(deep|down|in depth|of depth|below|beneath|high)\b")


def _distance(t):
    """Find the first stated horizontal distance. Returns (constraint, span) or (None, None).

    A number of cubits or metres that is a depth or height ("dig three cubits",
    "two cubits deep") is not a distance from the reference and is skipped.
    """
    m = None
    for cand in re.finditer(r"((?:\b(?:\d+|" + "|".join(_UNITS) + r"|hundred|thousand|and)\b[\s-]*)+)"
                            r"(cubits?|metres?|meters?|m)\b", t):
        if _DEPTH_BEFORE.search(t[max(0, cand.start() - 30):cand.start()]) or _DEPTH_AFTER.match(t[cand.end():]):
            continue
        m = cand
        break
    if not m:
        return None, None
    toks = [x for x in re.split(r"[\s-]+", m.group(1).strip()) if x]
    while toks and toks[0] == "and":
        toks = toks[1:]
    n = words_to_number(toks)
    if n is None:
        return None, None
    before = t[max(0, m.start() - 25):m.start()]
    limit_only = bool(re.search(r"(within|up to|no more than|not more than|less than)\s*$", before))
    unit = "cubit" if m.group(2).startswith("cubit") else "metre"
    if unit == "cubit":
        lo, hi = n * K["cubit_range_m"][0], n * K["cubit_range_m"][1]
    else:
        lo, hi = n * (1 - K["metre_tolerance"]), n * (1 + K["metre_tolerance"])
    lo = 0.0 if limit_only else lo
    return ({"stated": f"{n} {unit}s", "min_m": round(lo, 3), "max_m": round(hi, 3),
             "kind": "limit" if limit_only else "band"}, m.span())


def _opening(t):
    pats = [
        _OPEN_NOUN + r"\b(?:\s+(?:that|which|is|was|are|lies|located|faces|facing|opens|opening|looks|looking))*"
        r"\s+(?:on|to|toward|towards|in|at|onto)?\s*(?:the|its)?\s*(" + _DIR_RE + r")(?:ern)?(?:\s+side)?\b",
        _OPEN_NOUN + r"\s+(?:faces|facing|opens|looks)\s+(" + _DIR_RE + r")\b",
        r"\b(" + _DIR_RE + r")(?:ern)?[\s-]+facing\s+" + _OPEN_NOUN,
        r"\b(?:opens|faces|facing)\s+(?:to\s+|toward\s+|towards\s+)?(?:the\s+)?(" + _DIR_RE + r")\b",
    ]
    for p in pats:
        m = re.search(p, t)
        if m:
            return dir_code(m.group(1)), m.span()
    return None, None


def _position(t):
    """Find a position direction and its reference phrase."""
    pats = [
        r"\b(" + _DIR_RE + r")\s+(?:of|from)\s+(?P<ref>the\s+[^,;.]+)",
        r"\b(?:on|in|at|to|toward|towards)\s+the\s+(" + _DIR_RE + r")(?:\s+(?:side|part|end|edge|corner|slope|quarter))?"
        r"(?:\s+(?:of|from)\s+(?P<ref>the\s+[^,;.]+))?",
    ]
    for p in pats:
        m = re.search(p, t)
        if m:
            ref = m.groupdict().get("ref")
            span = m.span()
            if ref:
                cut = re.search(r"\s+(?:at|within|about|some|c\.)\s+(?:\d|" + "|".join(_UNITS) + r")", ref)
                if cut:
                    ref = ref[:cut.start()]
                    span = (m.start(), m.start("ref") + cut.start())
            return dir_code(m.group(1)), (ref.strip() if ref else None), span
    m = re.search(r"\b(?:of|from)\s+(?P<ref>the\s+[^,;.]+)", t)
    if m:
        ref = m.group("ref")
        cut = re.search(r"\s+(?:at|within|about|some|c\.)\s+(?:\d|" + "|".join(_UNITS) + r")", ref)
        if cut:
            ref = ref[:cut.start()]
        return None, ref.strip(), (m.start(), m.start("ref") + len(ref))
    return None, None, None


def _type(t, excluded):
    best = None
    for term in sorted(LEX, key=len, reverse=True):
        for m in re.finditer(r"(?<![a-z'])" + re.escape(term) + r"(?:s|es)?(?![a-z])", t):
            if any(a <= m.start() < b for a, b in excluded):
                continue
            if best is None or m.start() < best[1] or (m.start() == best[1] and len(term) > len(best[0])):
                best = (term, m.start())
            break
    if best is None:
        return None, None
    isa, maybe = LEX[best[0]]
    return best[0], (isa[0] if isa else (maybe[0] if maybe else None))


def parse_instruction(text: str) -> dict:
    """Turn the redacted instruction into explicit constraints."""
    t = normalise(text)
    dist, dspan = _distance(t)
    opening, ospan = _opening(t)
    tmasked = t
    if ospan:
        tmasked = t[:ospan[0]] + " " * (ospan[1] - ospan[0]) + t[ospan[1]:]
    direction, ref, pspan = _position(tmasked)
    excluded = [s for s in (ospan, dspan) if s]
    if pspan and ref:
        excluded.append((pspan[1] - len(ref) - 1, pspan[1] + 1) if pspan[1] - len(ref) - 1 >= 0 else pspan)
    term, target = _type(t, excluded)
    return {"type_term": term, "target_class": target, "direction": direction,
            "reference": ref, "distance": dist, "opening": opening}


# ---------------------------------------------------------------- candidate predicates

def type_classes(type_string):
    """Return (isa, maybe) class sets for a candidate's recorded type."""
    if not type_string:
        return set(), set()
    s = normalise(type_string)
    uncertain = s.endswith("?") or bool(re.search(r"\b(probably|possibly|perhaps|maybe)\b", s))
    isa, maybe = set(), set()
    covered = []
    for term in sorted(LEX, key=len, reverse=True):
        for m in re.finditer(r"(?<![a-z'])" + re.escape(term) + r"(?:s|es)?(?![a-z])", s):
            if any(a <= m.start() < b for a, b in covered):
                continue
            covered.append(m.span())
            i, mb = LEX[term]
            isa |= set(i)
            maybe |= set(mb)
    if uncertain:
        maybe |= isa
        isa = set()
    return isa, maybe


def pred_type(cand, c):
    if not c["target_class"]:
        return None, "the instruction names no recognised feature type"
    isa, maybe = type_classes(cand.get("type"))
    if c["target_class"] in isa:
        return True, f"type '{cand.get('type')}' is a {c['target_class']}"
    if c["target_class"] in maybe:
        return None, f"type '{cand.get('type')}' may or may not be a {c['target_class']}"
    if not isa and not maybe:
        return None, f"type '{cand.get('type')}' is not recorded or not recognised"
    return False, f"type '{cand.get('type')}' is not a {c['target_class']}"


def reference_matches(relative_to, reference):
    """True if the candidate's position is measured from the instruction's reference."""
    if not relative_to:
        return None
    rel = set(re.split(r"[^a-z0-9]+", str(relative_to).lower())) - {""}
    if reference is None:
        return bool(rel & SITE_TOKENS)
    ref_tokens = set(re.split(r"[^a-z0-9]+", reference.lower())) - {"", "the", "of", "at", "in", "a"}
    if rel & ref_tokens - SITE_TOKENS:
        return True
    if any(len(r) > 3 and any(r in w or w in r for w in ref_tokens if len(w) > 3) for r in rel - SITE_TOKENS):
        return True
    if rel & SITE_TOKENS and ref_tokens & SITE_TOKENS:
        return True
    return False


def _position_kind(pos):
    if pos.get("kind"):
        return pos["kind"]
    if isinstance(pos.get("bearing_deg"), (int, float)):
        return "plan"
    if pos.get("direction"):
        return "words"
    return "none"


EDGE_CODES = set(K["quadrant_edge_codes"])


def word_vs_sector(code, target, label):
    """Compare a verbal direction with the instruction's sector.

    As match.py position(): a verbal NE, SE, SW or NW gives unknown (position rule 3),
    unless the instruction uses the same word. Other words are tested by their compass
    angle: strictly inside the 90-degree sector is True, on its edge unknown, else False.
    """
    if code in EDGE_CODES:
        if code == target:
            return True, f"{label} is the instruction's own direction"
        return None, f"{label} lies on a quadrant edge and gives unknown (position rule 3)"
    diff = angle_diff(COMPASS[code], COMPASS[target])
    if diff < HALF:
        return True, f"{label} lies inside the {target} sector"
    if diff == HALF:
        return None, f"{label} lies on the edge of the {target} sector"
    return False, f"{label} lies outside the {target} sector"


def pred_direction(cand, c):
    if not c["direction"]:
        return "skip", "the instruction states no direction"
    pos = cand.get("position") or {}
    if reference_matches(pos.get("relative_to"), c["reference"]) is not True:
        return None, f"position is measured from '{pos.get('relative_to')}', not from the instruction's reference"
    lo, hi = sector_of(c["direction"])
    kind = _position_kind(pos)
    if kind == "plan":
        b, d, prec = pos.get("bearing_deg"), pos.get("distance_m"), pos.get("precision_m")
        if b is None:
            return None, "bearing not recorded"
        if prec and d is not None and d < K["bearing_precision_factor"] * prec:
            return None, f"distance {d} m is under {K['bearing_precision_factor']} x precision; bearing not valid"
        ok = in_sector(float(b) % 360, lo, hi)
        return ok, f"bearing {b} deg is {'inside' if ok else 'outside'} the {c['direction']} sector {lo:g}-{hi:g}"
    if kind == "words":
        code = dir_code(pos.get("direction"))
        if code is None:
            return None, f"direction word '{pos.get('direction')}' not recognised"
        return word_vs_sector(code, c["direction"], f"words '{pos.get('direction')}'")
    return None, "no position recorded"


def pred_distance(cand, c):
    dist = c["distance"] or {"stated": "none (default limit)", "min_m": 0.0,
                             "max_m": float(K["default_limit_m"]), "kind": "limit"}
    pos = cand.get("position") or {}
    kind = _position_kind(pos)
    if kind == "none":
        return None, "no position recorded"
    if reference_matches(pos.get("relative_to"), c["reference"]) is not True:
        return None, f"distance is measured from '{pos.get('relative_to')}', not from the instruction's reference"
    d = pos.get("distance_m")
    if d is None:
        if kind == "words" and dist["kind"] == "limit":
            return True, "words position with no distance counts as within the limit"
        if kind == "words":
            return None, f"words position with no distance; the stated band {dist['min_m']}-{dist['max_m']} m cannot be tested"
        return None, "distance not recorded"
    ok = dist["min_m"] <= float(d) <= dist["max_m"]
    return ok, f"distance {d} m is {'inside' if ok else 'outside'} {dist['min_m']}-{dist['max_m']} m ({dist['stated']})"


def pred_opening(cand, c):
    if not c["opening"]:
        return "skip", "the instruction states no opening"
    code = dir_code(cand.get("opening"))
    if code is None:
        return None, "opening side not recorded"
    return word_vs_sector(code, c["opening"], f"opening '{cand.get('opening')}'")


def date_code(cand):
    d = cand.get("date")
    if isinstance(d, dict):
        d = d.get("code")
    return (d or "U").upper()


def pred_date(cand, c):
    code = date_code(cand)
    if code == "L":
        return False, "date L (securely later than the target window) fails"
    if code in ("D", "U"):
        return True, f"date {code} passes"
    return None, f"date code '{code}' not recognised"


PREDICATES = (("type", pred_type), ("direction", pred_direction), ("distance", pred_distance),
              ("opening", pred_opening), ("date", pred_date))


def evaluate_candidate(cand, c):
    feats = cand.get("features") or {}
    checks = {}
    for name, fn in PREDICATES:
        val, why = fn(feats, c)
        if val == "skip":
            continue
        checks[name] = (val, why)
    vals = [v for v, _ in checks.values()]
    status = "contradicted" if False in vals else ("supported" if all(v is True for v in vals) else "unknown")
    return status, checks


# ---------------------------------------------------------------- withheld question

def _norm_opt(o):
    return re.sub(r"[^a-z]", "", str(o).lower())


def question_property(q):
    q = normalise(q)
    if re.search(r"\b(entrance|opening|mouth|door|doorway)\b", q):
        return "opening"
    if re.search(r"\b(date|dated|period|window)\b", q):
        return "date"
    if re.search(r"\b(side|quarter|direction|where)\b", q):
        return "quadrant"
    return None


def map_to_option(value, options):
    """Map a recorded value to one of the offered options, or "unknown"."""
    if value is None:
        return "unknown"
    norm = {_norm_opt(o): o for o in options}
    if _norm_opt(value) in norm:
        return norm[_norm_opt(value)]
    angle = None
    if isinstance(value, (int, float)):
        angle = float(value) % 360
    else:
        code = dir_code(value)
        if code:
            angle = COMPASS[code]
    dir_opts = [(o, COMPASS[dir_code(o)]) for o in options if dir_code(o)]
    if angle is None or not dir_opts:
        return "unknown"
    half = 180.0 / len(dir_opts)
    inside = [o for o, a in dir_opts if angle_diff(angle, a) < half]
    return inside[0] if len(inside) == 1 else "unknown"


def predict_withheld(case, c, selected_cand):
    options = case.get("withheld_options") or []
    prop = question_property(case.get("withheld_question", ""))
    unknown = "unknown"
    if prop is None:
        return unknown, "the withheld question names no property the procedure can read"
    if prop == "opening" and c["opening"]:
        return map_to_option(c["opening"], options), "the instruction states the opening"
    if prop == "quadrant" and c["direction"]:
        return map_to_option(c["direction"], options), "the instruction states the direction"
    if selected_cand is None:
        return unknown, "no candidate selected and the instruction does not state it"
    f = selected_cand.get("features") or {}
    if prop == "opening":
        v = f.get("opening")
        return map_to_option(v, options), (f"selected candidate records opening '{v}'" if v else
                                           "selected candidate records no opening")
    if prop == "date":
        v = date_code(selected_cand.get("features") or {})
        return map_to_option(v, options), f"selected candidate records date {v}"
    pos = f.get("position") or {}
    if _position_kind(pos) == "plan" and pos.get("bearing_deg") is not None:
        return map_to_option(float(pos["bearing_deg"]), options), f"selected candidate's bearing is {pos['bearing_deg']} deg"
    if pos.get("direction"):
        return map_to_option(pos["direction"], options), f"selected candidate's direction is '{pos['direction']}'"
    return unknown, "selected candidate records no direction"


# ---------------------------------------------------------------- main entry

def run_case(case: dict, adjust=None) -> dict:
    """Run the procedure on one case. `adjust`, if given, edits the parsed
    constraints (used only by ablate.py to remove one stated relation)."""
    c = parse_instruction(case.get("instruction", ""))
    if adjust is not None:
        c = adjust(dict(c))
    reasons = ["parsed instruction: " + json.dumps(c, ensure_ascii=False, sort_keys=True)]
    survivors, results = [], {}
    for cand in case.get("candidates", []):
        status, checks = evaluate_candidate(cand, c)
        results[cand["id"]] = status
        detail = "; ".join(f"{k}={'T' if v is True else 'F' if v is False else '?'} ({why})"
                           for k, (v, why) in checks.items())
        reasons.append(f"{cand['id']}: {status}: {detail}")
        if status != "contradicted":
            survivors.append(cand)
    if not survivors:
        selected, chosen = "none", None
        reasons.append("decision: every candidate is contradicted by at least one predicate")
    elif len(survivors) > 1:
        selected, chosen = "insufficient_evidence", None
        reasons.append("decision: more than one candidate survives: " + ", ".join(s["id"] for s in survivors))
    elif results[survivors[0]["id"]] == "supported":
        selected, chosen = survivors[0]["id"], survivors[0]
        reasons.append(f"decision: {selected} is the only survivor and every predicate is supported")
    else:
        selected, chosen = "insufficient_evidence", None
        reasons.append(f"decision: {survivors[0]['id']} is the only survivor but a decisive predicate is unknown")
    pred, why = predict_withheld(case, c, chosen)
    reasons.append("withheld: " + why)
    return {"case_id": case.get("case_id"), "selected": selected, "withheld_prediction": pred, "reasons": reasons}


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(json.dumps(run_case(json.loads(Path(p).read_text(encoding="utf-8"))), ensure_ascii=False, indent=1))
