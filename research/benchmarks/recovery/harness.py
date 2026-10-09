"""Recovery benchmark harness.

Loads case files (dev-NNN.json or res-NNN.json) from one directory, runs the
procedure on each, writes one output per case, and scores the outputs against a key
file given on the command line. The key is never read from the case directory
unless you name it.

Usage (from the repository root):
    python3 -I research/benchmarks/recovery/harness.py CASE_DIR --out OUT_DIR [--key KEY_FILE]
    python3 -I research/benchmarks/recovery/harness.py CASE_DIR --key KEY_FILE --verify-key

--verify-key only checks each case's key_sha256 against the key file and exits
(status 1 on any mismatch, missing entry or unused entry). It writes nothing.

Key file: a JSON array of key entries, a JSON object {case_id: entry}, or JSON Lines.
Canonical hash: sha256 of json.dumps(entry, ensure_ascii=False, sort_keys=True,
separators=(",", ":")) encoded as UTF-8.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import procedure  # noqa: E402

CASE_NAME = re.compile(r"^(dev|res)-\d{3}\.json$")
REQUIRED = ("case_id", "batch", "instruction", "context", "candidates", "degradations",
            "withheld_question", "withheld_options", "key_sha256")


def canonical_sha256(entry: dict) -> str:
    data = json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def load_cases(case_dir: Path) -> list[dict]:
    cases = []
    for p in sorted(case_dir.iterdir()):
        if p.is_file() and CASE_NAME.match(p.name):
            case = json.loads(p.read_text(encoding="utf-8"))
            missing = [k for k in REQUIRED if k not in case]
            if missing:
                raise ValueError(f"{p.name}: missing fields {missing}")
            if case["case_id"] + ".json" != p.name:
                raise ValueError(f"{p.name}: case_id {case['case_id']} does not match the file name")
            ids = [c.get("id") for c in case["candidates"]]
            if len(ids) != len(set(ids)) or not all(ids):
                raise ValueError(f"{p.name}: candidate ids missing or repeated")
            cases.append(case)
    if not cases:
        raise ValueError(f"no case files (dev-NNN.json or res-NNN.json) in {case_dir}")
    return cases


def load_key(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8").strip()
    try:
        data = json.loads(text)
        entries = list(data.values()) if isinstance(data, dict) and "case_id" not in data else (
            data if isinstance(data, list) else [data])
    except json.JSONDecodeError:
        entries = [json.loads(line) for line in text.splitlines() if line.strip()]
    key = {}
    for e in entries:
        if e["case_id"] in key:
            raise ValueError(f"key file repeats {e['case_id']}")
        key[e["case_id"]] = e
    return key


def verify_key(cases: list[dict], key: dict[str, dict]) -> dict:
    rows, ok = [], True
    for c in cases:
        e = key.get(c["case_id"])
        if e is None:
            rows.append({"case_id": c["case_id"], "status": "missing_from_key"})
            ok = False
            continue
        h = canonical_sha256(e)
        good = h == c["key_sha256"]
        ok &= good
        rows.append({"case_id": c["case_id"], "status": "ok" if good else "hash_mismatch",
                     "case_hash": c["key_sha256"], "key_hash": h})
    unused = sorted(set(key) - {c["case_id"] for c in cases})
    if unused:
        ok = False
    return {"all_ok": ok, "cases": rows, "key_entries_without_case": unused}


def score(outputs: list[dict], key: dict[str, dict]) -> dict:
    rows = []
    tally = {"cases": 0, "selection_correct": 0, "wrong_selections": 0, "abstentions_on_decidable": 0,
             "correct_abstentions": 0}
    wh = {"non_abstentions": 0, "correct": 0, "wrong": 0, "unknown_when_answer_known": 0}
    for out in outputs:
        k = key[out["case_id"]]
        tally["cases"] += 1
        sel, ans = out["selected"], k["answer"]
        if sel == "insufficient_evidence":
            outcome = "correct" if ans == "insufficient" else "abstained_on_decidable"
        else:
            outcome = "correct" if sel == ans else "wrong"
        if outcome == "correct":
            tally["selection_correct"] += 1
            if sel == "insufficient_evidence":
                tally["correct_abstentions"] += 1
        elif outcome == "wrong":
            tally["wrong_selections"] += 1
        else:
            tally["abstentions_on_decidable"] += 1
        w_pred, w_key = out["withheld_prediction"], k["withheld_answer"]
        if w_pred == w_key:
            w_out = "correct"
        elif w_pred == "unknown":
            w_out = "unknown_when_answer_known"
        else:
            w_out = "wrong"
        if sel != "insufficient_evidence":
            wh["non_abstentions"] += 1
            wh[w_out] += 1
        rows.append({"case_id": out["case_id"], "key_answer": ans, "selected": sel, "selection": outcome,
                     "withheld_key": w_key, "withheld_prediction": w_pred, "withheld": w_out,
                     "withheld_counted": sel != "insufficient_evidence"})
    return {"summary": tally, "withheld_among_non_abstentions": wh, "per_case": rows,
            "rules": ("An insufficient_evidence output is correct only when the key says insufficient. "
                      "A candidate or 'none' output is correct only when it equals the key answer. "
                      "Withheld accuracy is counted only where the output is not insufficient_evidence.")}


def code_hashes() -> dict:
    """SHA-256 of the files that define the procedure, recorded with every score."""
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("procedure.py", "procedure_constants.json", "harness.py")}


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case_dir", type=Path)
    ap.add_argument("--out", type=Path, help="directory for one output per case and score.json")
    ap.add_argument("--key", type=Path, help="key file (kept outside the repository for the reserved batch)")
    ap.add_argument("--verify-key", action="store_true", help="only check key_sha256 values against --key")
    a = ap.parse_args(argv)
    cases = load_cases(a.case_dir)
    if a.verify_key:
        if not a.key:
            ap.error("--verify-key needs --key")
        report = verify_key(cases, load_key(a.key))
        for r in report["cases"]:
            print(f"{r['case_id']}: {r['status']}")
        if report["key_entries_without_case"]:
            print("key entries without a case: " + ", ".join(report["key_entries_without_case"]))
        print("all key hashes match" if report["all_ok"] else "KEY CHECK FAILED")
        return 0 if report["all_ok"] else 1
    if not a.out:
        ap.error("--out is required unless --verify-key is given")
    a.out.mkdir(parents=True, exist_ok=True)
    outputs = []
    for case in cases:
        out = procedure.run_case(case)
        write_json(a.out / f"{case['case_id']}.json", out)
        outputs.append(out)
    print(f"{len(outputs)} outputs written to {a.out}")
    if a.key:
        key = load_key(a.key)
        check = verify_key(cases, key)
        if not check["all_ok"]:
            print("KEY CHECK FAILED; no score written")
            for r in check["cases"]:
                if r["status"] != "ok":
                    print(f"  {r['case_id']}: {r['status']}")
            return 1
        result = score(outputs, key)
        result["key_check"] = "all key_sha256 values match"
        result["code_sha256"] = code_hashes()
        write_json(a.out / "score.json", result)
        s, w = result["summary"], result["withheld_among_non_abstentions"]
        print(f"selection correct {s['selection_correct']}/{s['cases']}; wrong {s['wrong_selections']}; "
              f"abstained on decidable {s['abstentions_on_decidable']}; correct abstentions {s['correct_abstentions']}")
        print(f"withheld (non-abstentions {w['non_abstentions']}): correct {w['correct']}, wrong {w['wrong']}, "
              f"unknown {w['unknown_when_answer_known']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
