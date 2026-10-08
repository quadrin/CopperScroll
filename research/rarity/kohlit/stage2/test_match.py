"""Synthetic tests of match.py. Run: python3 -I test_match.py (no real data is used)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import match as M  # noqa: E402

V = M.C["variants"]


def g(d, b, valid=True):
    return {"distance_m": d, "bearing_deg": b, "precision_m": 10, "bearing_valid": valid}


PACKET = {
    "unit": {"row_id": "S1"},
    "source1_wbadb_within_2km": [
        {"row_id": "S2", "geom": g(400, 90)},     # east, 0.4 km
        {"row_id": "S3", "geom": g(800, 10)},     # north, 0.8 km
        {"row_id": "S4", "geom": g(1500, 100)},   # east, 1.5 km
        {"row_id": "S5", "geom": g(120, 0, False)},  # north but too close for rule 2
        {"row_id": "S6", "geom": g(700, 200)},    # south-south-west
    ],
    "source5_nigro_2011": {"entries": [{"ref": "N7", "geom": g(600, 350)}]},
}
REFS = M.refs_in_packet(PACKET)


def feat(fid, typ, pos, code="U", src="1", **kw):
    f = {"id": fid, "source": src, "cite": "x", "quote": "x", "type": typ, "position": pos,
         "date": {"code": code, "basis": "x"}}
    if typ == "pool":
        f["pool_def"] = kw.get("pool_def", "yes")
    if typ == "pit":
        f["is_tomb"] = kw.get("is_tomb", False)
    if typ == "grave":
        f["cavity_with_opening"] = kw.get("cav", False)
        if "mouth" in kw:
            f["mouth"] = kw["mouth"]
    return f


def sheet(features, absence=()):
    return {"unit_id": "S1", "coder": "A", "sources": {k: "read" for k in "12345"},
            "explicit_absence": [{"condition": c, "source": "1", "cite": "x", "quote": "none"} for c in absence],
            "features": features}


def ev(s, v="primary"):
    return {k: val[0] for k, val in M.evaluate(s, REFS, V[v]).items()}


def check(name, got, want):
    ok = all(got[k] == w for k, w in want.items())
    print(("ok   " if ok else "FAIL ") + name, got if not ok else "")
    return ok


results = []
# C1 by grid, by words, quadrant edge, east part, unclear pool, distance variants
results.append(check("C1 grid east 0.4 km", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"})])), {"C1": "MATCH"}))
results.append(check("C1 grid east 1.5 km primary", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S4"})])), {"C1": "UNKNOWN"}))
results.append(check("C1 grid east 1.5 km at 2 km", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S4"})]), "C1_2km"), {"C1": "MATCH"}))
results.append(check("C1 grid east 0.4 km at 0.5 km", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"})]), "C1_0.5km"), {"C1": "MATCH"}))
results.append(check("C1 words E", ev(sheet([feat("a", "pool", {"kind": "words", "direction": "E", "relative_to": "unit"}, src="3")])), {"C1": "MATCH"}))
results.append(check("C1 words NE edge", ev(sheet([feat("a", "pool", {"kind": "words", "direction": "NE", "relative_to": "unit"})])), {"C1": "UNKNOWN"}))
results.append(check("C1 words east part", ev(sheet([feat("a", "pool", {"kind": "words", "direction": "east part", "relative_to": "unit"})])), {"C1": "MATCH"}))
results.append(check("C1 words relative to other", ev(sheet([feat("a", "pool", {"kind": "words", "direction": "E", "relative_to": "other"})])), {"C1": "UNKNOWN"}))
results.append(check("C1 unclear pool", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"}, pool_def="unclear")])), {"C1": "UNKNOWN"}))
results.append(check("C1 dated L", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"}, code="L")])), {"C1": "UNKNOWN"}))
results.append(check("C1 U under dated only", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"})]), "dated_only"), {"C1": "UNKNOWN"}))
results.append(check("C1 D under dated only", ev(sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"}, code="D")]), "dated_only"), {"C1": "MATCH"}))
# absence
results.append(check("C1 absence, no pools", ev(sheet([], absence=["C1"])), {"C1": "FAIL"}))
results.append(check("C1 absence but unclear pool with no position", ev(sheet([feat("a", "pool", {"kind": "none"}, pool_def="unclear")], absence=["C1"])), {"C1": "UNKNOWN"}))
results.append(check("C1 absence, pool positively west", ev(sheet([feat("a", "pool", {"kind": "words", "direction": "W", "relative_to": "unit"})], absence=["C1"])), {"C1": "FAIL"}))
results.append(check("silence is not FAIL", ev(sheet([])), {"C1": "UNKNOWN", "C2": "UNKNOWN", "C3s": "UNKNOWN", "C3t": "UNKNOWN"}))
# C2, rule 2, tomb shafts, Nigro ref
results.append(check("C2 grid north", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "S3"})])), {"C2": "MATCH"}))
results.append(check("C2 rule 2 too close", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "S5"})])), {"C2": "UNKNOWN"}))
results.append(check("C2 tomb excluded", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "S3"}, is_tomb=True)])), {"C2": "UNKNOWN"}))
results.append(check("C2 tomb allowed in variant", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "S3"}, is_tomb=True)]), "C2_tomb_shafts"), {"C2": "MATCH"}))
results.append(check("C2 shaft grave in variant", ev(sheet([feat("t", "grave", {"kind": "grid", "ref": "S3"}, cav=True)]), "C2_tomb_shafts"), {"C2": "MATCH"}))
results.append(check("C2 Nigro ref N7 (350 deg)", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "N7"}, src="5")])), {"C2": "MATCH"}))
results.append(check("C2 south", ev(sheet([feat("p", "pit", {"kind": "grid", "ref": "S6"})])), {"C2": "UNKNOWN"}))
# C3 survey and text
pit = feat("p", "pit", {"kind": "grid", "ref": "S3"})
results.append(check("C3 survey north grave", ev(sheet([feat("g", "grave", {"kind": "grid", "ref": "S3"})])), {"C3s": "MATCH"}))
results.append(check("C3 text mouth phrase", ev(sheet([pit, feat("g", "grave", {"kind": "none"}, mouth={"pit_id": "p", "phrase": "tombs at its mouth"})])), {"C3t": "MATCH", "C3s": "UNKNOWN"}))
results.append(check("C3 text 8 m", ev(sheet([pit, feat("g", "grave", {"kind": "none"}, mouth={"pit_id": "p", "distance_m": 8})])), {"C3t": "MATCH"}))
results.append(check("C3 text 25 m", ev(sheet([pit, feat("g", "grave", {"kind": "none"}, mouth={"pit_id": "p", "distance_m": 25})])), {"C3t": "UNKNOWN"}))
south_pit = feat("q", "pit", {"kind": "grid", "ref": "S6"})
results.append(check("C3 text needs a C2 pit", ev(sheet([south_pit, feat("g", "grave", {"kind": "none"}, mouth={"pit_id": "q", "phrase": "at its mouth"})])), {"C3t": "UNKNOWN"}))
results.append(check("C3 absence", ev(sheet([], absence=["C3"])), {"C3s": "FAIL", "C3t": "FAIL"}))
# branches and Nigro removal
s = sheet([feat("a", "pool", {"kind": "grid", "ref": "S2"}), pit,
           feat("g", "grave", {"kind": "grid", "ref": "N7"}, src="5")])
vals = M.unit_values(s, REFS)
pv = vals[("primary", "with")]
results.append(check("branch A survey with Nigro", {"A": M.combine([pv["C1"], pv["C2"], pv["C3s"]])}, {"A": "MATCH"}))
pw = vals[("primary", "without")]
results.append(check("branch A survey without Nigro", {"A": M.combine([pw["C1"], pw["C2"], pw["C3s"]])}, {"A": "UNKNOWN"}))
results.append(check("branch B", {"B": M.combine([pw["C1"], pw["C2"]])}, {"B": "MATCH"}))
results.append(check("combine FAIL wins", {"x": M.combine(["MATCH", "FAIL", "UNKNOWN"])}, {"x": "FAIL"}))
# validation
results.append(check("validate good sheet", {"n": len(M.validate_sheet(s, PACKET))}, {"n": 0}))
bad = sheet([feat("a", "pool", {"kind": "grid", "ref": "S99"})])
results.append(check("validate unknown ref", {"n": len(M.validate_sheet(bad, PACKET))}, {"n": 1}))

print(f"{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
