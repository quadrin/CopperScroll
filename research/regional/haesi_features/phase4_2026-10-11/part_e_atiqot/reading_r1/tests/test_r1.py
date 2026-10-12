#!/usr/bin/env python3
"""Tests for phase 4, part E, reader r1 (standard library plus pyproj through the phase-1 geo.py).

  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r1/tests/test_r1.py
(or pytest). Checks the column order against phase 2, zones recomputed from coordinates, that no held unit
has a feature row, that every assigned unit is accounted for once, quote length, and that the counts in
README.md match the tables.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
R1 = HERE.parent
PART_E = R1.parent
LANE = PART_E.parents[1]
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402
import geo  # noqa: E402

ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]


def rows(name):
    with open(R1 / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def test_column_order():
    assert header(R1 / "features.csv") == header(P2 / "features.csv")
    assert header(R1 / "reports.csv") == header(P2 / "reports.csv")
    assert header(R1 / "held.csv") == header(PART_E / "held.csv")


def test_zones_recomputed():
    params = common.plan_params()
    for r in rows("features.csv"):
        assert r["region_zone"] in ZONES, r["report_id"]
        if r["lat"]:
            z = common.zone_of(float(r["lat"]), float(r["lon"]), params)
            assert z == r["region_zone"], (r["report_id"], r["feature_type"], z, r["region_zone"])
            lat, lon = geo.to_wgs84(int(r["easting_m"]), int(r["northing_m"]), r["grid"])
            assert abs(lat - float(r["lat"])) < 1e-5 and abs(lon - float(r["lon"])) < 1e-5, r["report_id"]
        else:
            assert r["coordinate_source"].startswith(("name only", "feature name only")), r["report_id"]
    for r in rows("reports.csv"):
        if r["lat"]:
            assert common.zone_of(float(r["lat"]), float(r["lon"]), params) == r["region_zone"], r["report_id"]


def test_no_held_unit_coded():
    held = {r["unit_id"] for r in rows("held.csv")}
    coded = {r["report_id"] for r in rows("features.csv")} | {r["report_id"] for r in rows("reports.csv")}
    assert not (held & coded)
    assert all(r["protected_strip"] == "no" for r in rows("features.csv"))


def test_assignment_accounted_once():
    need = list(csv.DictReader(open(PART_E / "pdfs_needed.csv", newline="", encoding="utf-8")))
    assigned = [r["unit_id"] for r in need if r["tier"] in ("T1", "U", "T3")
                or (r["tier"] == "T2" and int(r["order_position_in_tier"]) <= 60)]
    rep = [r["report_id"] for r in rows("reports.csv")]
    nr = [r["unit_id"] for r in rows("not_read.csv")]
    held = [r["unit_id"] for r in rows("held.csv")]
    allu = rep + nr + held
    assert sorted(allu) == sorted(assigned)
    assert len(set(allu)) == len(allu)


def test_feature_rows_valid():
    reps = {r["report_id"]: r for r in rows("reports.csv")}
    n = Counter()
    for f in rows("features.csv"):
        assert f["feature_type"] in CLASSES
        assert f["dated_in_window"] in ("yes", "no", "unknown")
        assert 0 < len(f["quote"].split()) <= 12, f["quote"]
        assert f["exposure_at_freeze"] == "unexposed at freeze"
        assert f["report_id"] in reps
        n[f["report_id"]] += 1
    for rid, r in reps.items():
        assert int(r["n_feature_rows"]) == n[rid], rid
        assert re.fullmatch(r"[0-9a-f]{64}", r["text_sha256"]), rid
        assert r["exposure_at_freeze"] == "unexposed at freeze"


def test_readme_counts():
    text = (R1 / "README.md").read_text(encoding="utf-8")
    feats = rows("features.csv")
    reps = rows("reports.csv")
    nr = rows("not_read.csv")
    m = re.search(r"Units read and coded: (\d+)\.", text)
    assert m and int(m.group(1)) == len(reps)
    m = re.search(r"Feature rows: (\d+) \(yes (\d+), no (\d+), unknown (\d+)\)", text)
    w = Counter(f["dated_in_window"] for f in feats)
    assert m and [int(x) for x in m.groups()] == [len(feats), w["yes"], w["no"], w["unknown"]]
    m = re.search(r"Dropped as outside the region: (\d+)\.", text)
    assert m and int(m.group(1)) == sum(1 for r in nr if r["reason"].startswith("dropped"))
    m = re.search(r"Not read \(time limit\): (\d+)\.", text)
    assert m and int(m.group(1)) == sum(1 for r in nr if r["reason"].startswith("not read"))
    tab = Counter((f["feature_type"], f["region_zone"], f["dated_in_window"]) for f in feats)
    for c in CLASSES:
        line = [ln for ln in text.splitlines() if ln.startswith("| %s |" % c)]
        assert len(line) == 1, c
        cells = [x.strip() for x in line[0].strip("|").split("|")][1:]
        for z, cell in zip(ZONES, cells):
            k = [tab[(c, z, t)] for t in ("yes", "no", "unknown")]
            want = "0" if sum(k) == 0 else "%d (%d/%d/%d)" % (sum(k), *k)
            assert cell == want, (c, z, cell, want)
    summ = json.loads((R1 / "summary.json").read_text(encoding="utf-8"))
    assert summ["feature_rows"] == len(feats) and summ["reports_read"] == len(reps)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
