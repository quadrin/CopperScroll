"""Helpers for the Mandate 1:20,000 map regression (standard library and pyproj only).

Frames: WGS84 (EPSG:4326) and the Palestine Grid (EPSG:28191, metres). The datum operation is
pinned to PROJ's 'Palestine 1923 to WGS 84 (1)' so that results do not depend on which grids
happen to be installed.
"""
from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from functools import lru_cache

OPERATION = "Palestine 1923 to WGS 84 (1)"


@lru_cache(maxsize=1)
def _transformers():
    from pyproj.transformer import TransformerGroup
    fwd = [t for t in TransformerGroup(4326, 28191, always_xy=True).transformers if OPERATION in t.description]
    inv = [t for t in TransformerGroup(28191, 4326, always_xy=True).transformers if OPERATION in t.description]
    if not fwd or not inv:
        raise RuntimeError(f"PROJ operation '{OPERATION}' is not available")
    return fwd[0], inv[0]


def operation_names() -> tuple[str, str]:
    f, i = _transformers()
    return f.description, i.description


def to_grid(lat: float, lon: float) -> tuple[float, float]:
    e, n = _transformers()[0].transform(lon, lat)
    return e, n


def to_wgs(e: float, n: float) -> tuple[float, float]:
    lon, lat = _transformers()[1].transform(e, n)
    return lat, lon


def sheet_of(e: float, n: float) -> str:
    return f"{int(e // 10000):02d}-{int(n // 10000):02d}"


def residual(observed_en, reference_en):
    de = observed_en[0] - reference_en[0]
    dn = observed_en[1] - reference_en[1]
    return de, dn, math.hypot(de, dn)


def summary(vectors):
    """Summary of residual vectors [(dE, dN), ...]: mean vector, median and max length, RMS about the mean."""
    n = len(vectors)
    if n == 0:
        return {"n": 0}
    me = sum(v[0] for v in vectors) / n
    mn = sum(v[1] for v in vectors) / n
    lengths = sorted(math.hypot(*v) for v in vectors)
    med = lengths[n // 2] if n % 2 else 0.5 * (lengths[n // 2 - 1] + lengths[n // 2])
    rms = math.sqrt(sum(math.hypot(*v) ** 2 for v in vectors) / n)
    rms_about = math.sqrt(sum((v[0] - me) ** 2 + (v[1] - mn) ** 2 for v in vectors) / n)
    return {"n": n, "mean_dE_m": me, "mean_dN_m": mn, "mean_length_m": math.hypot(me, mn),
            "median_m": med, "max_m": lengths[-1], "rms_m": rms, "rms_about_mean_m": rms_about}


def fit_similarity(source, destination):
    """Least-squares 2D similarity (scale, rotation, shift), as in kohlit_chain/registration.py."""
    if len(source) != len(destination) or len(source) < 2:
        raise ValueError("At least two paired points required")
    n = len(source)
    sx = sum(p[0] for p in source) / n
    sy = sum(p[1] for p in source) / n
    dx = sum(p[0] for p in destination) / n
    dy = sum(p[1] for p in destination) / n
    num_a = num_b = den = 0.0
    for (x, y), (u, v) in zip(source, destination):
        x, y, u, v = x - sx, y - sy, u - dx, v - dy
        num_a += x * u + y * v
        num_b += x * v - y * u
        den += x * x + y * y
    if den < 1e-12:
        raise ValueError("Degenerate geometry")
    a, b = num_a / den, num_b / den
    return {"a": a, "b": b, "tx": dx - (a * sx - b * sy), "ty": dy - (b * sx + a * sy),
            "scale": math.hypot(a, b), "rotation_deg": math.degrees(math.atan2(b, a))}


def apply_similarity(p, point):
    x, y = point
    return p["a"] * x - p["b"] * y + p["tx"], p["b"] * x + p["a"] * y + p["ty"]


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# --- names -------------------------------------------------------------------------------
ABBREVIATIONS = [(r"\bKh\.", "Khirbat"), (r"\bW\.", "Wādī"), (r"\bSh\.", "Sheikh"), (r"\bJ\.", "Jebel"),
                 (r"\bSp\.", ""), (r"\bCis\.", "cistern"), (r"\bAqd\.", "aqueduct"), (r"\bCem\.", "cemetery"),
                 (r"\bCh\.", "church"), (r"\bMt\.", "Mount")]


def expand_translit(printed: str) -> str:
    s = printed
    for pat, rep in ABBREVIATIONS:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize(text: str) -> list[str]:
    """Lower-case words with diacritics, ʿ and ʾ removed; brackets and punctuation dropped."""
    t = unicodedata.normalize("NFKD", text)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("ʿ", "").replace("ʾ", "").replace("'", "").replace("’", "")
    t = t.lower()
    return [w for w in re.split(r"[^a-z]+", t) if w]


def root_flags(printed: str, roots: list[dict]) -> list[str]:
    words = normalize(printed)
    out = []
    for r in roots:
        if any(p in w for w in words for p in r["patterns"]):
            out.append(r["root"])
    return out


CONTEXT_TOKENS = ["buqei", "sumr", "samr", "mird", "tabaq", "qumran"]
CONTEXT_WINDOWS = {"B_buqeia", "Q_qumran"}  # plan.json: "the Buqeiʿa and Qumran windows"


def context_flag(printed: str, window: str) -> bool:
    if window not in CONTEXT_WINDOWS:
        return False
    return any(tok in w for w in normalize(printed) for tok in CONTEXT_TOKENS)
