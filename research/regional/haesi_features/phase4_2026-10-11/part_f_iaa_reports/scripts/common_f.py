#!/usr/bin/env python3
"""Part-F gazetteer screen helpers: the phase-2 frozen gazetteer and normalisation (common.py, amendment A1)
plus the A3 name variants used in phase 3. Standard library only (pyproj is not needed here)."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
P4 = PART.parent
LANE = P4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
try:
    import common  # noqa: E402  (phase-2 plan parameters and normalisation)
except ImportError:  # common imports geo, which needs pyproj; fall back to its pure functions
    import importlib.util
    import types
    sys.modules.setdefault("geo", types.ModuleType("geo"))
    spec = importlib.util.spec_from_file_location("common", P2 / "scripts" / "common.py")
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)

# Amendment A3 (phase 2) name variants, with the zone each names (as used in phase 3).
A3_VARIANTS = {"hagedud": "Z2_JORDAN_VALLEY", "anathoth": "Z4_JERUSALEM_HILLS",
               "land of benjamin": "Z4_JERUSALEM_HILLS", "kh el burj": "Z4_JERUSALEM_HILLS"}
HEB = re.compile(r"[֐-׿]")


def params():
    return common.plan_params()


def patterns(p=None):
    p = p or params()
    out = []
    for z, g in p["gazetteer"].items():
        for t in g["en"] + g["he"]:
            out.append((z, common.norm(t).strip(), "gazetteer"))
    rw = p["region_wide_terms"]
    for t in rw["en"] + rw["he"]:
        out.append(("REGION_WIDE", common.norm(t).strip(), "gazetteer"))
    for t, z in A3_VARIANTS.items():
        out.append((z, common.norm(t).strip(), "A3"))
    return sorted(set(out))


def hits(text, pats):
    nt = common.norm(text)
    return [(z, t, src) for z, t, src in pats if (" " + t + " ") in nt]


def fmt_hits(h):
    return ";".join("%s:%s%s" % (z, t, "" if src == "gazetteer" else " (A3)") for z, t, src in h)


def norm(s):
    return common.norm(s)
