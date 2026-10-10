"""Shared helpers for the past-search schematics (research/schematics/searches/).

These pages reuse the entry-schematic kit (../lib/schematic.py) but draw past
searches and survey records, not scroll entries. Positions are to scale only
where a page says so; everything else is a schematic arrangement with the
distances the sources give written on it.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "lib"))
import schematic as S  # noqa: E402

P = S.P
# Two-hue scheme for this set (validated with the dataviz palette checker:
# CVD separation 20.2, normal-vision 27.0, both >= 3:1 on the page).
BLUE = "#1f6fae"   # dug, cleared or reached
RED = P["red"]     # what the scroll text names (depths, targets)
GREY = P["muted"]  # not recorded / not dug


def out_path(name: str) -> Path:
    return HERE / f"{name}.svg"


def page(num: str, title: str, subtitle: str, width: int = 1400, height: int = 1000):
    c = S.Canvas(width, height, f"Past search schematic {num}: {title}")
    c.text(40, 48, f"Past searches {num} — {title}", 24, P["ink"], 700)
    c.text(40, 74, subtitle, 14.5, P["sub"])
    return c


def load_points():
    """De Vaux 1952 survey points digitized from RB 60 pl. XX (research/history/devaux1952_cave_points)."""
    f = REPO / "research" / "history" / "devaux1952_cave_points" / "devaux1952_cave_points.csv"
    with open(f, encoding="utf-8", newline="") as fh:
        return {r["point"]: r for r in csv.DictReader(fh)}


def bullets(c, x, y, items, max_chars, size=11.5, gap=6, color=None):
    """Bulleted, wrapped list. Returns next free y."""
    for s in items:
        c.text(x, y, "•", size, color or P["sub"])
        y = c.wrap(x + 12, y, s, max_chars, size, fill=color or P["sub"]) + gap
    return y
