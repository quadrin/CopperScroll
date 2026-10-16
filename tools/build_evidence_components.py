#!/usr/bin/env python3
"""Build the evidence-component ratings outputs.

Input:  research/assessments/evidence_components/ratings.json (reviewed ratings, one row per atlas candidate)
Output: research/assessments/evidence_components/ratings.csv
        atlas/app/atlas-components.json (compact copy for the atlas)

  python3 tools/build_evidence_components.py            # validate and write outputs
  python3 tools/build_evidence_components.py --check    # validate and fail if outputs are stale
  python3 tools/build_evidence_components.py --merge DIR  # first assembly from rater part files

The rubric is research/assessments/evidence_components/RUBRIC.md.
"""
import argparse, csv, io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/assessments/evidence_components"
RATINGS = DIR / "ratings.json"
CSV_OUT = DIR / "ratings.csv"
ATLAS_DATA = ROOT / "atlas/app/atlas-data.json"
ATLAS_OUT = ROOT / "atlas/app/atlas-components.json"
LABELS = {3: "strong", 2: "partial", 1: "weak", 0: "none"}
U_VALUES = {"discriminates", "not unique", "conditionally excluded", "untested"}
LEVEL_KEYS = ("R", "P", "F", "D")


def key(row):
    return f"{row['entry']}|{row['candidate'] or ''}"


def finish(row):
    """Recompute the derived fields so they always follow the levels."""
    levels = [row[k]["level"] for k in LEVEL_KEYS if row.get(k) and row[k].get("level") is not None]
    if row["candidate"] is None:
        row["weakest"], row["label"], row["limited_by"] = None, "unplaced", []
        return row
    w = min(levels)
    row["weakest"] = w
    row["label"] = LABELS[w]
    row["limited_by"] = [k for k in LEVEL_KEYS if row[k]["level"] == w]
    return row


def validate(rows, atlas):
    errors = []
    expected = {f"{e['id']}|{c['placeId']}" for e in atlas["entries"] for c in e["candidates"]}
    expected |= {f"{e['id']}|" for e in atlas["entries"] if not e["candidates"]}
    seen = {}
    for r in rows:
        k = key(r)
        if k in seen:
            errors.append(f"duplicate row {k}")
        seen[k] = r
        if r["candidate"] is not None:
            for c in LEVEL_KEYS:
                lv = r.get(c, {}).get("level")
                if lv not in (0, 1, 2, 3):
                    errors.append(f"{k}: {c} level {lv!r}")
                if not r.get(c, {}).get("sources"):
                    errors.append(f"{k}: {c} has no source")
            if r.get("U", {}).get("value") not in U_VALUES:
                errors.append(f"{k}: U value {r.get('U', {}).get('value')!r}")
        elif r.get("R", {}).get("level") not in (0, 1, 2, 3):
            errors.append(f"{k}: R level missing")
    for k in sorted(expected - set(seen)):
        errors.append(f"missing row {k}")
    for k in sorted(set(seen) - expected):
        errors.append(f"row not in atlas {k}")
    # R may differ between candidates of one entry only when they rely on different anchor words.
    by_entry = {}
    for r in rows:
        by_entry.setdefault(r["entry"], []).append(r)
    for e, rs in by_entry.items():
        if len({r["R"]["level"] for r in rs}) > 1 and len({tuple(r.get("anchor_words") or []) for r in rs}) == 1:
            errors.append(f"entry {e}: R differs between candidates with the same anchor words")
    return errors


def entry_order(atlas):
    return {e["id"]: i for i, e in enumerate(atlas["entries"])}


def render_csv(rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["entry", "lines", "candidate", "candidate_name", "R", "P", "F", "D", "U", "weakest", "label",
                "limited_by", "R_basis", "P_basis", "F_basis", "D_basis", "U_basis", "decisive_next",
                "atlas_status", "atlas_confidence"])
    for r in rows:
        g = lambda c: r[c]["level"] if r.get(c) and r[c].get("level") is not None else ""
        b = lambda c: r[c]["basis"] if r.get(c) else ""
        w.writerow([r["entry"], r["lines"], r["candidate"] or "", r.get("candidate_name") or "", g("R"), g("P"), g("F"),
                    g("D"), r["U"]["value"] if r.get("U") else "", "" if r["weakest"] is None else r["weakest"],
                    r["label"], " ".join(r["limited_by"]), b("R"), b("P"), b("F"), b("D"), b("U"),
                    r.get("decisive_next") or "", r.get("atlas_status") or "", r.get("atlas_confidence") or ""])
    return buf.getvalue()


def render_atlas(rows):
    out = {"rubric": "https://github.com/quadrin/CopperScroll/blob/main/research/assessments/evidence_components/RUBRIC.md",
           "table": "https://github.com/quadrin/CopperScroll/blob/main/research/assessments/evidence_components/ratings.csv",
           "window": "50 BCE–70 CE, extended to 135 CE", "rows": {}}
    for r in rows:
        if r["candidate"] is None:
            continue
        out["rows"][key(r)] = {
            "levels": {c: r[c]["level"] for c in LEVEL_KEYS},
            "basis": {c: r[c]["basis"] for c in LEVEL_KEYS} | {"U": r["U"]["basis"]},
            "u": r["U"]["value"], "weakest": r["weakest"], "label": r["label"], "limitedBy": r["limited_by"],
            "limitingWord": r["R"].get("limiting_word") or "", "next": r.get("decisive_next") or "",
        }
    return json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--merge", metavar="DIR")
    a = ap.parse_args()
    atlas = json.loads(ATLAS_DATA.read_text(encoding="utf-8"))
    order = entry_order(atlas)
    if a.merge:
        rows = [row for p in sorted(Path(a.merge).glob("*.json")) for row in json.loads(p.read_text(encoding="utf-8"))]
    else:
        rows = json.loads(RATINGS.read_text(encoding="utf-8"))
    rows = [finish(r) for r in rows]
    cand_order = {f"{e['id']}|{c['placeId']}": i for e in atlas["entries"] for i, c in enumerate(e["candidates"])}
    rows.sort(key=lambda r: (order.get(r["entry"], 999), cand_order.get(key(r), 0)))
    errors = validate(rows, atlas)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    outputs = {CSV_OUT: render_csv(rows), ATLAS_OUT: render_atlas(rows)}
    if a.merge:
        outputs[RATINGS] = json.dumps(rows, ensure_ascii=False, indent=1) + "\n"
    if a.check:
        if json.dumps(rows, ensure_ascii=False, indent=1) + "\n" != RATINGS.read_text(encoding="utf-8"):
            print("ratings.json derived fields are stale; run without --check", file=sys.stderr)
            sys.exit(1)
        stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            print("stale: " + ", ".join(stale), file=sys.stderr)
            sys.exit(1)
        print(f"ok: {len(rows)} rows")
        return
    if not a.merge:
        outputs[RATINGS] = json.dumps(rows, ensure_ascii=False, indent=1) + "\n"
    for p, text in outputs.items():
        p.write_text(text, encoding="utf-8")
    counts = {}
    for r in rows:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    print(f"{len(rows)} rows; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
