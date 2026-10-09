"""Observation-process audit of the Koḥlit rarity count (exploratory).

Written on 8 October 2026 UTC, after the registered result and both addenda were seen.
Nothing here changes the registered result. stage2/match.py is imported and never changed.

Commands:
    python3 -I observation.py absences PACKETS_DIR CODED_A CODED_B OUT_CSV
    python3 -I observation.py rescope  PACKETS_DIR CODED_A CODED_B OUT_DIR

CODED_A and CODED_B are the merged sheets of the source-2 addendum (merge_sheets.sh builds them).

`absences` lists every explicit_absence statement in the merged sheets. It records the feature
class that the statement names and the area that it can cover, and whether that area reaches the
1 km northern sector that C2 and C3 need.

`rescope` runs match.py under three models:
    registered      the merged sheets as they are; must equal the committed addendum result
    scoped          an absence statement counts only where its covered scope reaches the whole
                    target of the condition (the 1 km sector and the whole feature class);
                    elsewhere the condition stays UNKNOWN
    sector_records  the registered rules, plus pit records for the sector that the same surveys
                    published outside the packets (sector_records.csv; hand-checked)
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import math
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE2 = HERE.parent / "stage2"
sys.path.insert(0, str(STAGE2))
import match as M  # noqa: E402

REGISTERED_DIR = STAGE2 / "addendum_s2" / "results"
SECTOR_AREA_M2 = math.pi * 1000.0 ** 2 / 4  # quarter disc, 1 km radius (C2 and C3 target)
STATUS = ("exploratory: scope rules written after the registered result was seen; "
          "the registered result is unchanged")

# Scope rules for the statement forms found in the merged sheets. A statement that matches no
# rule stops the script, so a new form must be read and classified before it is counted.
RULES = [
    {
        "rule": "zertal_cisterns_field",
        "source": "2",
        "pattern": r"\bcisterns:\s*none\b",
        "statement_form": "data-block field",
        "class_named": "cisterns (the field counts cistern openings at the site)",
        "class_covers_condition": False,
        "class_note": "C2 also counts caves, silos, shafts, pits, tunnels and underground chambers",
        "spatial_scope": "site only",
        "stated_radius_m": None,
        "scope_basis": ("Zertal Vol. II p. 8: item 11 is the number of cistern openings, item 7 the area "
                        "on which the structures stood; p. 7: features outside sites were recorded "
                        "and published separately"),
    },
    {
        "rule": "swp_no_tombs_sentence",
        "source": "3",
        "pattern": r"\bno tombs were found\b",
        "statement_form": "sentence in the entry text",
        "class_named": "tombs",
        "class_covers_condition": False,
        "class_note": "C3 also counts cist, pit and trench graves, which leave no visible chamber",
        "spatial_scope": "site and immediate surroundings",
        "stated_radius_m": None,
        "scope_basis": ("SWP Mem I p. 41: Section B describes the remains at each named place, with no "
                        "search radius; Mem II p. 236: the sentence is about the ruin and 'the place'"),
    },
]
CONDITION_LIMIT_M = {"C1": 1000, "C2": 1000, "C3": 1000}


# ---------------- scope helpers ----------------

def classify(source, quote):
    for r in RULES:
        if r["source"] == source and re.search(r["pattern"], quote, re.I):
            return r
    raise ValueError(f"no scope rule for source {source} statement {quote!r}; read it and add a rule")


def reaches_sector(rule, condition):
    """True only if the statement covers the whole target area and the whole feature class."""
    radius = rule.get("stated_radius_m")
    spatial = rule["spatial_scope"] == "stated radius" and radius is not None and radius >= CONDITION_LIMIT_M[condition]
    return bool(spatial and rule["class_covers_condition"])


def area_m2(text):
    """Zertal 'Area:' field -> square metres ('1 dunam (1000 sq. m)', '7.5 dunams (...)')."""
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*dunams?", text or "")
    return round(float(m.group(1)) * 1000) if m else None


def site_share_pct(a_m2):
    """Largest share of the 1 km northern sector that a site record can cover, in per cent.
    The site is taken as a disc centred on the unit point, so a quarter of it lies in the sector."""
    if a_m2 is None:
        return None
    return round(100.0 * (a_m2 / 4) / SECTOR_AREA_M2, 3)


def grid_geom(ux, uy, x, y, precision_m=100):
    d = math.hypot(x - ux, y - uy)
    b = math.degrees(math.atan2(x - ux, y - uy)) % 360
    return {"distance_m": round(d), "bearing_deg": round(b, 1), "bearing_valid": d >= 3 * precision_m}


def unit_set(packet_unit):
    s = "main" if packet_unit.get("main_set") else "pre-70 only"
    return s + (", R2" if packet_unit.get("in_R2") else "")


def entry_area(packet):
    for o in packet["source2_survey_entry"].get("other_entries") or []:
        for e in o.get("excerpts", []):
            m = re.search(r"Area:\s*([^\n]*?)(?:\s{3,}|\n|$)", e)
            if m:
                return m.group(1).strip()
    return None


def survey_label(source, cite):
    if source == "2":
        m = re.match(r"(Zertal[^)]*\))", cite)
        return m.group(1) if m else cite
    return {"3": "SWP Memoirs", "1": "WBADB", "4": "first publication", "5": "Nigro 2011"}[source]


PAGE_CHECKS = {
    ("S676", "3"): "printed p. 236 (Sheet XII, Archaeology); 'p. 30' is the packet's OCR page",
}


def registered_rows():
    with open(REGISTERED_DIR / "unit_results.csv", newline="", encoding="utf-8") as f:
        return {r["unit_id"]: r for r in csv.DictReader(f) if r["variant"] == "primary" and r["nigro"] == "with"}


# ---------------- absences ----------------

ABSENCE_FIELDS = ["absence_id", "coder", "unit_id", "unit_name", "unit_set", "condition", "source", "survey",
                  "cite", "page_check", "quote", "statement_form", "class_named", "class_covers_condition",
                  "class_note", "spatial_scope", "stated_radius_m", "scope_basis", "site_area_text",
                  "site_area_m2", "site_share_of_sector_pct", "reaches_1km_sector", "registered_condition",
                  "registered_A_survey", "registered_B"]


def absence_rows(packets, sheets_by_coder):
    reg = registered_rows()
    rows = []
    for coder in ("A", "B"):
        for uid, s in sorted(sheets_by_coder[coder].items()):
            for i, a in enumerate(s.get("explicit_absence", [])):
                rule = classify(a["source"], a["quote"])
                pk = packets[uid]
                area = entry_area(pk)
                am = area_m2(area)
                r = reg[uid]
                cond = a["condition"]
                regc = f"C2={r['C2']}" if cond == "C2" else (f"C1={r['C1']}" if cond == "C1" else
                                                               f"C3s={r['C3s']}; C3t={r['C3t']}")
                rows.append({
                    "absence_id": f"{coder}:{uid}:{cond}:{i + 1}", "coder": coder, "unit_id": uid,
                    "unit_name": pk["unit"]["name"], "unit_set": unit_set(pk["unit"]), "condition": cond,
                    "source": a["source"], "survey": survey_label(a["source"], a.get("cite", "")),
                    "cite": a.get("cite", ""), "page_check": PAGE_CHECKS.get((uid, a["source"]), ""),
                    "quote": a["quote"], "statement_form": rule["statement_form"],
                    "class_named": rule["class_named"],
                    "class_covers_condition": "yes" if rule["class_covers_condition"] else "no",
                    "class_note": rule["class_note"], "spatial_scope": rule["spatial_scope"],
                    "stated_radius_m": "" if rule["stated_radius_m"] is None else rule["stated_radius_m"],
                    "scope_basis": rule["scope_basis"], "site_area_text": area or "",
                    "site_area_m2": "" if am is None else am,
                    "site_share_of_sector_pct": "" if am is None else site_share_pct(am),
                    "reaches_1km_sector": "yes" if reaches_sector(rule, cond) else "no",
                    "registered_condition": regc, "registered_A_survey": r["A_survey"], "registered_B": r["B"],
                })
    return rows


def cmd_absences(packets_dir, coded_a, coded_b, out_csv):
    packets = M.load_packets(packets_dir)
    sheets = {"A": M.load_sheets(coded_a), "B": M.load_sheets(coded_b)}
    rows = absence_rows(packets, sheets)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ABSENCE_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} absence statements; {sum(r['reaches_1km_sector'] == 'yes' for r in rows)} reach the 1 km sector")


# ---------------- models ----------------

def load_absence_table(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {(r["coder"], r["unit_id"], r["condition"], r["source"], r["quote"]): r["reaches_1km_sector"] == "yes"
                for r in csv.DictReader(f)}


def scoped_sheet(sheet, coder, table):
    keep = []
    for a in sheet.get("explicit_absence", []):
        key = (coder, sheet["unit_id"], a["condition"], a["source"], a["quote"])
        if key not in table:
            raise KeyError(f"absence {key} is not in absences.csv; run the absences command first")
        if table[key]:
            keep.append(a)
    s = dict(sheet)
    s["explicit_absence"] = keep
    return s


def load_sector_records(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def record_feature(rec, packet):
    """A sector record as a coded feature, positioned by the protocol's own rules."""
    if rec["ref"]:
        pos = {"kind": "grid", "ref": rec["ref"]}
    else:
        u = packet["unit"]
        g = grid_geom(u["x"], u["y"], int(rec["x"]), int(rec["y"]), max(int(rec["precision_m"]), u["precision_m"]))
        # 'plan' carries a bearing and distance from the unit point; here they come from the two
        # grid points, and position rule 2 is applied first.
        pos = ({"kind": "plan", "bearing_deg": g["bearing_deg"], "distance_m": g["distance_m"]}
               if g["bearing_valid"] else {"kind": "none"})
    return {"id": rec["record_id"], "source": rec["protocol_source"], "cite": rec["cite"], "quote": rec["quote"],
            "type": "pit", "subtype": rec["subtype"], "is_tomb": False, "position": pos,
            "date": {"code": "U", "basis": "not dated by the source"}}


def with_records(sheet, recs, packet):
    s = dict(sheet)
    s["features"] = list(sheet["features"]) + [record_feature(r, packet) for r in recs]
    return s


def write_sheets(d, sheets):
    d.mkdir(parents=True, exist_ok=True)
    for uid, s in sheets.items():
        (d / f"{uid}.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")


def run_match(packets_dir, a_dir, b_dir, out_dir):
    with contextlib.redirect_stdout(io.StringIO()):
        M.cmd_run(str(packets_dir), str(a_dir), str(b_dir), str(out_dir))
    summary = json.loads((Path(out_dir) / "summary.json").read_text(encoding="utf-8"))
    with open(Path(out_dir) / "unit_results.csv", newline="", encoding="utf-8") as f:
        units = {(r["unit_id"], r["variant"], r["nigro"]): r for r in csv.DictReader(f)}
    return summary, units


def comparison_rows(summaries):
    rows = []
    reg = summaries["registered"]
    for table in ("headline", "sensitivity", "nigro_without"):
        for key in reg[table]:
            parts = key.split("|")
            sset, branch = parts[0], parts[1]
            variant = parts[2] if table == "sensitivity" else "primary"
            nigro = "without" if table == "nigro_without" else "with"
            row = {"table": table, "set": sset, "branch": branch, "variant": variant, "nigro": nigro,
                   "N": reg[table][key]["N"]}
            for model, s in summaries.items():
                t = s[table][key]
                row.update({f"{model}_k": t["k"], f"{model}_f": t["f"], f"{model}_m": t["m"],
                            f"{model}_m_full_coverage": t["m_full_coverage"]})
            rows.append(row)
    return rows


def moved_rows(units_by_model):
    reg = units_by_model["registered"]
    out = []
    for model, units in units_by_model.items():
        if model == "registered":
            continue
        changed = {}
        for key, r in units.items():
            r0 = reg[key]
            diffs = [c for c in M.CONDITIONS + tuple(M.BRANCHES) if r[c] != r0[c]]
            if diffs:
                changed.setdefault(key[0], {})[(key[1], key[2])] = (r0, r, diffs)
        for uid in sorted(changed, key=lambda u: (u[0], int(re.sub(r"\D", "", u) or 0))):
            per = changed[uid]
            any_r0 = next(iter(per.values()))[0]
            prim = per.get(("primary", "with"))
            fmt = (lambda r0, r, cols: "; ".join(f"{c} {r0[c]}->{r[c]}" for c in cols))
            out.append({
                "model": model, "unit_id": uid, "name": any_r0["name"],
                "unit_set": ("main" if any_r0["main_set"] == "True" else "pre-70 only") + (", R2" if any_r0["in_R2"] == "True" else ""),
                "conditions_primary": fmt(prim[0], prim[1], [c for c in prim[2] if c in M.CONDITIONS]) if prim else "",
                "branches_primary": fmt(prim[0], prim[1], [c for c in prim[2] if c in M.BRANCHES]) if prim else "",
                "variants_changed": " ".join(sorted(f"{v}|{n}" for v, n in per)),
            })
    return out


def cmd_rescope(packets_dir, coded_a, coded_b, out_dir, absences_csv=None, records_csv=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    absences_csv = Path(absences_csv or HERE / "absences.csv")
    records_csv = Path(records_csv or HERE / "sector_records.csv")
    packets = M.load_packets(packets_dir)
    A, B = M.load_sheets(coded_a), M.load_sheets(coded_b)
    table = load_absence_table(absences_csv)
    recs = load_sector_records(records_csv)
    by_unit = {}
    for r in recs:
        u = packets[r["unit_id"]]["unit"]
        if (int(r["unit_x"]), int(r["unit_y"])) != (u["x"], u["y"]):
            sys.exit(f"{r['record_id']}: unit point differs from the packet")
        if r["ref"] and r["ref"] not in M.refs_in_packet(packets[r["unit_id"]]):
            sys.exit(f"{r['record_id']}: {r['ref']} is not a WBADB row in the packet")
        by_unit.setdefault(r["unit_id"], []).append(r)

    models = {
        "registered": (A, B),
        "scoped": ({u: scoped_sheet(s, "A", table) for u, s in A.items()},
                   {u: scoped_sheet(s, "B", table) for u, s in B.items()}),
        "sector_records": ({u: (with_records(s, by_unit[u], packets[u]) if u in by_unit else s) for u, s in A.items()},
                           {u: (with_records(s, by_unit[u], packets[u]) if u in by_unit else s) for u, s in B.items()}),
    }
    summaries, units = {}, {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, (sa, sb) in models.items():
            write_sheets(tmp / name / "A", sa)
            write_sheets(tmp / name / "B", sb)
            summaries[name], units[name] = run_match(packets_dir, tmp / name / "A", tmp / name / "B", tmp / name / "out")

    committed = json.loads((REGISTERED_DIR / "summary.json").read_text(encoding="utf-8"))
    same = summaries["registered"] == committed
    if not same:
        sys.exit("the registered model does not reproduce stage2/addendum_s2/results/summary.json; check the inputs")

    comp = comparison_rows(summaries)
    with open(out_dir / "comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(comp[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(comp)
    moved = moved_rows(units)
    with open(out_dir / "moved_units.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["model", "unit_id", "name", "unit_set", "conditions_primary",
                                          "branches_primary", "variants_changed"], lineterminator="\n")
        w.writeheader()
        w.writerows(moved)
    out = {"status": STATUS, "registered_reproduces_committed_result": same,
           "models": {"registered": "stage2/match.py on the merged sheets of the source-2 addendum",
                      "scoped": "absence statements count only where their covered scope reaches the whole target",
                      "sector_records": "registered rules plus sector_records.csv (outside the packets)"},
           "headline": {m: s["headline"] for m, s in summaries.items()}}
    (out_dir / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for key in summaries["registered"]["headline"]:
        cells = "  ".join(f"{m}: k={s['headline'][key]['k']} f={s['headline'][key]['f']} m={s['headline'][key]['m']}"
                          for m, s in summaries.items())
        print(f"{key:18s} {cells}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or [""]
    if cmd == "absences" and len(args) == 4:
        cmd_absences(*args)
    elif cmd == "rescope" and len(args) in (4, 5, 6):
        cmd_rescope(*args)
    else:
        sys.exit(__doc__)
