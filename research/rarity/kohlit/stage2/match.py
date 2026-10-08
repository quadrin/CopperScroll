"""Koḥlit rarity count, Stage 2: apply the §4 conditions to the coded sheets.

Frozen with PROTOCOL.md and protocol_constants.json before any Stage 2 coding.

Commands:
    python3 -I match.py validate PACKETS_DIR CODED_DIR
    python3 -I match.py sample-b PACKETS_DIR CODED_A_DIR OUT_CSV
    python3 -I match.py run PACKETS_DIR CODED_A_DIR CODED_B_DIR OUT_DIR

A condition is MATCH if at least one coded feature qualifies, FAIL only if a source states
the absence and no recorded feature could still qualify, and UNKNOWN otherwise. A unit is
MATCH if every condition of the branch is MATCH, FAIL if any is FAIL, else UNKNOWN.
Silence is never a FAIL.
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
KOHLIT = HERE.parent
C = json.loads((HERE / "protocol_constants.json").read_text(encoding="utf-8"))
COVERAGE = json.loads((HERE / "coverage.json").read_text(encoding="utf-8"))

EXPOSED = {"E334": "Tell es-Sultan", "S1658": "Kh. Marjame (ʿEin Samiya)", "S1667": "Kh. Samiyye",
           "S1666": "Water line, ʿEin Samiya", "S2488": "Kh. Marjama (other site)", "S1001": "Kh. Yanun",
           "S1053": "Yanun", "S4546": "ʿEin el-Ghuweir", "E754": "Kh. Qumran"}
CONDITIONS = ("C1", "C2", "C3s", "C3t")
BRANCHES = {"A_survey": ("C1", "C2", "C3s"), "A_text": ("C1", "C2", "C3t"), "B": ("C1", "C2")}
TYPES = {"pool", "pit", "grave", "other"}
KINDS = {"grid", "words", "plan", "none"}
CODES = {"D", "U", "L"}
SOURCES = {"1", "2", "3", "4", "5"}


# ---------------- validation ----------------

def validate_sheet(s, packet):
    errs = []
    uid = packet["unit"]["row_id"]
    if s.get("unit_id") != uid:
        errs.append("unit_id differs from packet")
    if s.get("coder") not in ("A", "B"):
        errs.append("coder must be A or B")
    for k in SOURCES:
        if not isinstance(s.get("sources", {}).get(k), str):
            errs.append(f"sources.{k} missing")
    refs = refs_in_packet(packet)
    ids = set()
    for f in s.get("features", []):
        fid = f.get("id")
        if not fid or fid in ids:
            errs.append(f"feature id missing or repeated: {fid}")
        ids.add(fid)
        if f.get("source") not in SOURCES:
            errs.append(f"{fid}: source must be one of 1-5")
        if f.get("type") not in TYPES:
            errs.append(f"{fid}: type must be pool/pit/grave/other")
        if f.get("type") == "pool" and f.get("pool_def") not in ("yes", "no", "unclear"):
            errs.append(f"{fid}: pool_def must be yes/no/unclear")
        if f.get("type") == "pit" and not isinstance(f.get("is_tomb"), bool):
            errs.append(f"{fid}: is_tomb must be true/false")
        if f.get("type") == "grave" and not isinstance(f.get("cavity_with_opening"), bool):
            errs.append(f"{fid}: cavity_with_opening must be true/false")
        p = f.get("position") or {}
        if p.get("kind") not in KINDS:
            errs.append(f"{fid}: position.kind must be grid/words/plan/none")
        if p.get("kind") == "grid" and p.get("ref") not in refs:
            errs.append(f"{fid}: grid ref {p.get('ref')} is not a WBADB row or Nigro entry in the packet")
        if p.get("kind") == "words" and p.get("relative_to") not in ("unit", "other"):
            errs.append(f"{fid}: words position needs relative_to unit/other")
        if (f.get("date") or {}).get("code") not in CODES:
            errs.append(f"{fid}: date.code must be D/U/L")
        if not f.get("cite"):
            errs.append(f"{fid}: cite missing")
    for f in s.get("features", []):
        m = f.get("mouth")
        if m and m.get("pit_id") and m["pit_id"] not in ids:
            errs.append(f"{f.get('id')}: mouth.pit_id {m['pit_id']} is not a feature id")
    for a in s.get("explicit_absence", []):
        if a.get("condition") not in ("C1", "C2", "C3") or a.get("source") not in SOURCES or not a.get("quote"):
            errs.append(f"bad explicit_absence entry: {a}")
    return errs


def refs_in_packet(packet):
    refs = {r["row_id"]: r["geom"] for r in packet["source1_wbadb_within_2km"]}
    for n in packet["source5_nigro_2011"]["entries"]:
        refs[n["ref"]] = n["geom"]
    refs[packet["unit"]["row_id"]] = None
    return refs


# ---------------- condition logic ----------------

def in_sector(b, sector):
    lo, hi = sector
    return lo <= b <= hi if lo <= hi else (b >= lo or b <= hi)


def date_ok(f, v):
    code = f["date"]["code"]
    return code == "D" or (code == "U" and not v.get("dated_only"))


def position(f, sector, limit, refs, east_part_ok):
    """True = in sector and within limit; False = positively elsewhere; None = cannot tell."""
    p = f.get("position") or {}
    kind = p.get("kind")
    if kind == "grid":
        g = refs.get(p.get("ref"))
        if not g or not g.get("bearing_valid") or g.get("bearing_deg") is None:
            return None
        return in_sector(g["bearing_deg"], sector) and g["distance_m"] <= limit
    if kind == "plan":
        b, d = p.get("bearing_deg"), p.get("distance_m")
        if b is None or d is None:
            return None
        return in_sector(float(b) % 360, sector) and float(d) <= limit
    if kind == "words":
        if p.get("relative_to") != "unit":
            return None
        d = p.get("distance_m")
        dist_ok = True if d is None else float(d) <= limit
        word = (p.get("direction") or "").strip()
        if east_part_ok and word.lower() in C["east_part_words"]:
            return dist_ok
        w = word.upper()
        if w in C["quadrant_edge_words"]:
            return None
        if w in C["compass_deg"]:
            return in_sector(C["compass_deg"][w], sector) and dist_ok
        return None
    return None


def pit_like(f, v):
    if f["type"] == "pit":
        return (not f["is_tomb"]) or bool(v.get("tomb_shafts"))
    if f["type"] == "grave" and v.get("tomb_shafts"):
        return bool(f["cavity_with_opening"])
    return False


def evaluate(sheet, refs, v):
    lim = dict(C["limits_m"])
    lim.update({k: val for k, val in v.items() if k in lim})
    feats = sheet["features"]
    absent = {a["condition"] for a in sheet.get("explicit_absence", [])}
    out = {}

    def cond(hit_cands, could_cands, sector, limit, east, name):
        """MATCH: a candidate qualifies. FAIL: a source states the absence and no recorded
        feature (including unclear ones) could still qualify. Otherwise UNKNOWN."""
        hit = [f for f in hit_cands if date_ok(f, v) and position(f, sector, limit, refs, east) is True]
        could = [f for f in could_cands if date_ok(f, v) and position(f, sector, limit, refs, east) is not False]
        if hit:
            return "MATCH", [f["id"] for f in hit]
        if name in absent and not could:
            return "FAIL", []
        return "UNKNOWN", []

    pools = [f for f in feats if f["type"] == "pool" and f["pool_def"] == "yes"]
    pools_maybe = [f for f in feats if f["type"] == "pool" and f["pool_def"] != "no"]
    out["C1"] = cond(pools, pools_maybe, C["sectors_deg"]["C1_east"], lim["C1"], True, "C1")

    pits = [f for f in feats if pit_like(f, v)]
    out["C2"] = cond(pits, pits, C["sectors_deg"]["C2_north"], lim["C2"], False, "C2")

    graves = [f for f in feats if f["type"] == "grave"]
    out["C3s"] = cond(graves, graves, C["sectors_deg"]["C3_north"], lim["C3_survey"], False, "C3")

    qualifying_pits = set(out["C2"][1])
    hit3 = []
    for f in graves:
        m = f.get("mouth") or {}
        if not m.get("pit_id") or m["pit_id"] not in qualifying_pits or not date_ok(f, v):
            continue
        dist = m.get("distance_m")
        phrase = (m.get("phrase") or "").lower()
        if (dist is not None and float(dist) <= lim["C3_text_mouth"]) or any(ph in phrase for ph in C["mouth_phrases"]):
            hit3.append(f["id"])
    if hit3:
        out["C3t"] = ("MATCH", hit3)
    elif "C3" in absent and not [f for f in graves if date_ok(f, v)]:
        out["C3t"] = ("FAIL", [])
    else:
        out["C3t"] = ("UNKNOWN", [])
    return out


def combine(values):
    if "FAIL" in values:
        return "FAIL"
    if all(x == "MATCH" for x in values):
        return "MATCH"
    return "UNKNOWN"


def without_nigro(sheet):
    s = dict(sheet)
    s["features"] = [f for f in sheet["features"] if f["source"] != "5"]
    s["explicit_absence"] = [a for a in sheet.get("explicit_absence", []) if a["source"] != "5"]
    return s


def unit_values(sheet, refs):
    """{(variant, nigro): {condition: value}} for one coded sheet."""
    res = {}
    for vname, v in C["variants"].items():
        for nig in ("with", "without"):
            s = sheet if nig == "with" else without_nigro(sheet)
            ev = evaluate(s, refs, v)
            res[(vname, nig)] = {k: ev[k][0] for k in CONDITIONS}
            res[(vname, nig)]["_features"] = {k: ev[k][1] for k in CONDITIONS}
    return res


# ---------------- io ----------------

def load_packets(d):
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(d, "packets").glob("*.json"))}


def load_sheets(d):
    if not d or not Path(d).is_dir():
        return {}
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(d).glob("*.json"))}


def coverage_class(ref):
    ref = (ref or "").strip()
    if not ref or ref.lower() == "nan":
        return "none"
    found = [cls for key, cls in COVERAGE["surveys"].items() if key in ref]
    return ("full" if "full" in found else "partial") if found else COVERAGE["default_if_unlisted"]


def all_units():
    with open(KOHLIT / "stage1a" / "stage1a_units.csv", newline="", encoding="utf-8") as f:
        a = {r["unit_id"]: r for r in csv.DictReader(f)}
    with open(KOHLIT / "stage1b" / "stage1b_units.csv", newline="", encoding="utf-8") as f:
        b = {r["unit_id"]: r for r in csv.DictReader(f)}
    out = {}
    for uid, r in a.items():
        out[uid] = {"name": r["name"], "main": r["main_set"] == "True", "R2": r["in_R2"] == "True",
                    "excavated": r["excavated"] == "True", "coverage": coverage_class(r["survey_ref"]),
                    "stage2": b[uid]["stage1"] == "to Stage 2"}
    return out


# ---------------- commands ----------------

def cmd_validate(packets_dir, coded_dir):
    packets = load_packets(packets_dir)
    sheets = load_sheets(coded_dir)
    bad = 0
    for uid, s in sheets.items():
        if uid not in packets:
            print(f"{uid}: no packet")
            bad += 1
            continue
        errs = validate_sheet(s, packets[uid])
        if errs:
            bad += 1
            print(f"{uid}: " + " | ".join(errs))
    missing = sorted(set(packets) - set(sheets))
    print(f"{len(sheets)} sheets, {bad} with errors, {len(missing)} packets not coded")
    return bad


def cmd_sample_b(packets_dir, coded_a_dir, out_csv):
    packets = load_packets(packets_dir)
    sheets = load_sheets(coded_a_dir)
    ids = sorted(packets)
    rng = random.Random(C["seed"] + 1)
    k = round(C["coder_b_fraction"] * len(ids))
    sample = set(rng.sample(ids, k))
    matches = set()
    for uid, s in sheets.items():
        vals = unit_values(s, refs_in_packet(packets[uid]))
        for key, cv in vals.items():
            if any(combine([cv[c] for c in conds]) == "MATCH" for conds in BRANCHES.values()):
                matches.add(uid)
    rows = [{"unit_id": u, "random_20pc": u in sample, "coder_a_match": u in matches}
            for u in sorted(sample | matches)]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["unit_id", "random_20pc", "coder_a_match"])
        w.writeheader()
        w.writerows(rows)
    print(f"coder B: {len(rows)} units ({len(sample)} random, {len(matches)} coder-A matches)")


def cmd_run(packets_dir, coded_a_dir, coded_b_dir, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    packets = load_packets(packets_dir)
    A, B = load_sheets(coded_a_dir), load_sheets(coded_b_dir)
    units = all_units()
    missing = [u for u, x in units.items() if x["stage2"] and u not in A]
    if missing:
        sys.exit(f"{len(missing)} Stage 2 units have no coder-A sheet, e.g. {missing[:5]}")
    for d, sheets in (("A", A), ("B", B)):
        for uid, s in sheets.items():
            errs = validate_sheet(s, packets[uid])
            if errs:
                sys.exit(f"coder {d} sheet {uid} is invalid: {errs[:3]}")

    final, agree = {}, defaultdict(Counter)
    detail_rows = []
    for uid, u in units.items():
        if not u["stage2"]:
            final[uid] = {key: {c: "UNKNOWN" for c in CONDITIONS} for key in
                          [(v, n) for v in C["variants"] for n in ("with", "without")]}
            continue
        refs = refs_in_packet(packets[uid])
        va = unit_values(A[uid], refs)
        vb = unit_values(B[uid], refs) if uid in B else None
        merged = {}
        for key in va:
            merged[key] = {}
            for c in CONDITIONS:
                a = va[key][c]
                if vb is None:
                    merged[key][c] = a
                else:
                    b = vb[key][c]
                    merged[key][c] = a if a == b else "UNKNOWN"
                    if key == ("primary", "with"):
                        agree[c][(a, b)] += 1
            if key == ("primary", "with"):
                detail_rows.append({"unit_id": uid, "name": u["name"], "coded_by": "A+B" if vb else "A",
                                    **{f"A_{c}": va[key][c] for c in CONDITIONS},
                                    **{f"B_{c}": (vb[key][c] if vb else "") for c in CONDITIONS},
                                    **{f"final_{c}": merged[key][c] for c in CONDITIONS},
                                    "A_features": json.dumps(va[key]["_features"])})
        final[uid] = merged

    # unit results table
    rows = []
    for uid, u in units.items():
        for (vname, nig), cv in final[uid].items():
            r = {"unit_id": uid, "name": u["name"], "variant": vname, "nigro": nig, "main_set": u["main"],
                 "in_R2": u["R2"], "excavated": u["excavated"], "coverage": u["coverage"],
                 "stage1": "to Stage 2" if u["stage2"] else "not recorded"}
            r.update({c: cv[c] for c in CONDITIONS})
            r.update({br: combine([cv[c] for c in conds]) for br, conds in BRANCHES.items()})
            rows.append(r)
    with open(out_dir / "unit_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(out_dir / "coder_comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(detail_rows[0].keys()))
        w.writeheader()
        w.writerows(detail_rows)

    # summaries
    def tally(sel, branch, vname="primary", nig="with"):
        sub = [r for r in rows if r["variant"] == vname and r["nigro"] == nig and sel(r)]
        k = sum(r[branch] == "MATCH" for r in sub)
        f_ = sum(r[branch] == "FAIL" for r in sub)
        m = [r for r in sub if r[branch] == "UNKNOWN"]
        return {"N": len(sub), "k": k, "f": f_, "m": len(m),
                "m_full_coverage": sum(r["coverage"] == "full" for r in m),
                "m_no_adequate_coverage": sum(r["coverage"] != "full" for r in m),
                "m_not_recorded_stage1": sum(r["stage1"] == "not recorded" for r in m)}

    sets = {"R1_main": lambda r: r["main_set"], "R1_pre70": lambda r: True,
            "R2_main": lambda r: r["main_set"] and r["in_R2"], "R2_pre70": lambda r: r["in_R2"]}
    summary = {"headline": {}, "sensitivity": {}, "excavated_split": {}, "nigro_without": {},
               "exposed": {}, "two_of_three": [], "coder_agreement": {}}
    for sname, sel in sets.items():
        for br in BRANCHES:
            summary["headline"][f"{sname}|{br}"] = tally(sel, br)
            summary["nigro_without"][f"{sname}|{br}"] = tally(sel, br, nig="without")
            for vname in C["variants"]:
                if vname != "primary":
                    summary["sensitivity"][f"{sname}|{br}|{vname}"] = tally(sel, br, vname)
            for ex in (True, False):
                summary["excavated_split"][f"{sname}|{br}|{'excavated' if ex else 'unexcavated'}"] = \
                    tally(lambda r, sel=sel, ex=ex: sel(r) and r["excavated"] == ex, br)
    prim = {r["unit_id"]: r for r in rows if r["variant"] == "primary" and r["nigro"] == "with"}
    for uid, label in EXPOSED.items():
        if uid in prim:
            r = prim[uid]
            summary["exposed"][uid] = {"label": label, "main_set": r["main_set"], "in_R2": r["in_R2"],
                                       "stage1": r["stage1"], **{c: r[c] for c in CONDITIONS},
                                       **{br: r[br] for br in BRANCHES}}
    for uid, r in prim.items():
        vals = [r["C1"], r["C2"], r["C3s"]]
        if vals.count("MATCH") == 2:
            summary["two_of_three"].append({"unit_id": uid, "name": r["name"], "main_set": r["main_set"],
                                            "in_R2": r["in_R2"], "C1": r["C1"], "C2": r["C2"], "C3s": r["C3s"]})
    for c, cnt in agree.items():
        n = sum(cnt.values())
        po = sum(v for (a, b), v in cnt.items() if a == b) / n if n else None
        cats = {"MATCH", "FAIL", "UNKNOWN"}
        pa = Counter()
        pb = Counter()
        for (a, b), v in cnt.items():
            pa[a] += v
            pb[b] += v
        pe = sum(pa[x] * pb[x] for x in cats) / (n * n) if n else None
        kappa = (po - pe) / (1 - pe) if n and pe is not None and pe < 1 else None
        summary["coder_agreement"][c] = {"units": n, "agreement": round(po, 3) if po is not None else None,
                                         "kappa": round(kappa, 3) if kappa is not None else None,
                                         "pairs": {f"{a}/{b}": v for (a, b), v in sorted(cnt.items())}}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["headline"], indent=1))


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    if cmd == "validate":
        sys.exit(1 if cmd_validate(*args) else 0)
    elif cmd == "sample-b":
        cmd_sample_b(*args)
    elif cmd == "run":
        cmd_run(*args)
    else:
        sys.exit(__doc__)
