"""Run 28 model (RULE.md, "Attributes used" and "Model"). Shared by bench28.py and score28.py.

Written 31 Oct 2026 before any consolidated describer file existed.
"""
import csv
import math
import re
from pathlib import Path

import numpy as np
from scipy.special import comb

RUN = Path(__file__).resolve().parents[1]
INV = RUN.parent / "attribute_inventory_2026-10-31"
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
ATTRS = ["cls", "n_open", "dirs", "pillar", "steps"]
NONCLASS = ["n_open", "dirs", "pillar", "steps"]
GROUPS = {
    "cave": {"cave", "chamber", "rock_shelter", "columbarium", "fissure"},
    "water": {"cistern", "pool", "reservoir", "basin", "ritual_bath", "pit"},
    "channel": {"conduit", "outlet", "dam"},
    "tomb": {"tomb", "burial"},
    "spring": {"spring"},
    "built": {"building", "room", "court", "tower", "wall", "doorway", "steps", "terrace", "road", "cairn", "pillar"},
    "other": {"other"},
}
ITEM_GROUPS = {"cave", "water", "channel", "tomb"}
ALPHA_GRID = np.round(np.arange(0.0, 1.0, 0.01), 2)  # 0.00 .. 0.99


def read_csv(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def clean(v):
    v = ("" if v is None else str(v)).strip()
    if v.lower() in ("", "unknown", "undecidable") or "|" in v:
        return None
    return v


def group(cls):
    c = clean(cls)
    if c is None:
        return None
    for g, s in GROUPS.items():
        if c in s:
            return g
    return "other"


def intval(v):
    v = clean(v)
    if v is None:
        return None
    m = re.match(r"^(\d+)(?:\.0+)?$", v)
    return int(m.group(1)) if m else None


def dir_list(v):
    """'E;N/NE' -> [{'E'}, {'N','NE'}]; None if no valid direction."""
    v = clean(v)
    if v is None:
        return None
    out = []
    for part in filter(None, v.replace(",", ";").split(";")):
        s = {p.strip().upper() for p in part.split("/") if p.strip().upper() in COMPASS}
        if s:
            out.append(frozenset(s))
    return tuple(out) or None


def presence(v):
    n = intval(v)
    return None if n is None else (n >= 1)


def attrs_of(row, cls_field="feature_class", f_open="n_openings", f_dirs="opening_dirs", f_pil="n_pillars", f_steps="n_steps"):
    return {"cls": group(row.get(cls_field)), "n_open": intval(row.get(f_open)), "dirs": dir_list(row.get(f_dirs)),
            "pillar": presence(row.get(f_pil)), "steps": presence(row.get(f_steps))}


def _near(a, b):
    i, j = COMPASS.index(a), COMPASS.index(b)
    return min((i - j) % 8, (j - i) % 8) <= 1


def _pair(x, y):
    return any(_near(p, q) for p in x for q in y)


def dirs_match(d, v):
    """The shorter list pairs one-to-one into the longer, each pair equal or neighbouring."""
    short, long_ = (d, v) if len(d) <= len(v) else (v, d)

    def rec(i, used):
        if i == len(short):
            return True
        return any(k not in used and _pair(short[i], long_[k]) and rec(i + 1, used | {k}) for k in range(len(long_)))
    return rec(0, frozenset())


def match(a, d, v):
    if a == "dirs":
        return dirs_match(d, v)
    return d == v


class Model:
    """Candidates: list of attribute dicts. q_a(d) computed over candidates with a known value of a."""

    def __init__(self, cands):
        self.cands = cands
        self.N = len(cands)
        self._q = {}

    def q(self, a, d):
        key = (a, d)
        if key not in self._q:
            known = [c[a] for c in self.cands if c[a] is not None]
            self._q[key] = (sum(match(a, d, v) for v in known) / len(known)) if known else 1.0
        return self._q[key]

    def loglik(self, clue, alpha, attrs):
        """log of the product of LR_a over candidates (numpy array, natural log)."""
        out = np.zeros(self.N)
        for a in attrs:
            d = clue.get(a)
            if d is None:
                continue
            q = max(self.q(a, d), 1e-9)
            al = alpha[a]
            lm = math.log(al / q + (1 - al))
            lx = math.log(max(1 - al, 1e-12))
            for j, c in enumerate(self.cands):
                v = c[a]
                if v is None:
                    continue
                out[j] += lm if match(a, d, v) else lx
        return out

    def posterior(self, clue, alpha, attrs):
        ll = self.loglik(clue, alpha, attrs)
        p = np.exp(ll - ll.max())
        return p / p.sum()


def fit_alpha(pairs):
    """pairs: list of (matched: bool, q). Grid posterior mean, uniform prior."""
    logp = np.zeros(len(ALPHA_GRID))
    for m, q in pairs:
        pr = ALPHA_GRID + (1 - ALPHA_GRID) * q if m else (1 - ALPHA_GRID) * (1 - q)
        logp += np.log(np.maximum(pr, 1e-300))
    w = np.exp(logp - logp.max())
    w /= w.sum()
    return float((w * ALPHA_GRID).sum()), w


def training_pairs(model, items, a):
    pairs = []
    for it in items:
        if len(it["truth"]) != 1:
            continue
        d = it["clue"].get(a)
        v = model.cands[it["truth"][0]][a]
        if d is None or v is None:
            continue
        pairs.append((match(a, d, v), model.q(a, d)))
    return pairs


def expected_coverage(post, truth, level):
    """Credible set built by descending posterior, ties in random order; returns P(truth set hit)."""
    order = np.argsort(-post, kind="stable")
    vals = post[order]
    tset = set(truth)
    s = 0.0
    i = 0
    n = len(vals)
    while i < n:
        p = vals[i]
        j = i
        while j < n and abs(vals[j] - p) <= 1e-12 * max(p, 1e-300):
            j += 1
        block = order[i:j]
        k = len(block)
        jt = sum(1 for b in block if b in tset)
        if s + k * p < level - 1e-12:
            if jt:
                return 1.0
            s += k * p
            i = j
            continue
        m = int(math.ceil((level - s) / p - 1e-9))
        m = max(1, min(m, k))
        if jt == 0:
            return 0.0
        return 1.0 - comb(k - jt, m, exact=True) / comb(k, m, exact=True)
    return 1.0


def set_size(post, level):
    c = np.cumsum(np.sort(post)[::-1])
    return int(np.searchsorted(c, level - 1e-12) + 1)
