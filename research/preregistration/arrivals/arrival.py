#!/usr/bin/env python3
"""Arrival register tool: write or check MANIFEST.md, validate outcome records.

    python3 -I research/preregistration/arrivals/arrival.py check
    python3 -I research/preregistration/arrivals/arrival.py manifest --write
    python3 -I research/preregistration/arrivals/arrival.py validate outcomes/<file>.json
    python3 -I research/preregistration/arrivals/arrival.py status

Standard library only. `check` exits 1 on any mismatch, missing or extra file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

FROZEN_FILES = [
    "register.json",
    "RANKING.md",
    "RANKING_PLAN.md",
    "ARRIVAL_PROCEDURE.md",
    "specs.py",
    "build_register.py",
    "arrival.py",
]

STATEMENT = """A prediction in this folder counts only if it was committed and pushed before the item arrived. The registration time is the time of the push that first contains this manifest; the integrator records that commit in the README and in ACTIVE_TEST. As of 9 October 2026 none of the listed items has arrived. Parts that arrived earlier are marked in their item files as "arrived before registration: not a test". Any later edit to a file below changes its hash: a changed prediction is a new exploratory model, never a rescue of this one."""

ROW = re.compile(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \| (\d+) \|$")
ALLOWED_STATUS = {"pending", "partial", "not_obtained", "declined"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def frozen_paths(folder: Path) -> list[str]:
    items = sorted(f"items/{p.name}" for p in (folder / "items").glob("*.md"))
    return FROZEN_FILES + items


def manifest_text(folder: Path) -> str:
    lines = ["# Manifest of the arrival register", "", STATEMENT, "",
             "Recompute and check: `python3 -I research/preregistration/arrivals/arrival.py check`.", "",
             "| File | SHA-256 | Bytes |", "|---|---|---|"]
    for rel in frozen_paths(folder):
        path = folder / rel
        lines.append(f"| `{rel}` | `{sha256_file(path)}` | {path.stat().st_size} |")
    return "\n".join(lines) + "\n"


def read_manifest(folder: Path) -> dict[str, tuple[str, int]]:
    out = {}
    for line in (folder / "MANIFEST.md").read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out[m.group(1)] = (m.group(2), int(m.group(3)))
    return out


def check(folder: Path) -> list[str]:
    problems = []
    if not (folder / "MANIFEST.md").exists():
        return ["MANIFEST.md is missing"]
    listed = read_manifest(folder)
    expected = set(frozen_paths(folder))
    for rel in sorted(set(listed) - expected):
        problems.append(f"listed but missing: {rel}")
    for rel in sorted(expected - set(listed)):
        problems.append(f"present but not in manifest: {rel}")
    for rel, (digest, size) in sorted(listed.items()):
        path = folder / rel
        if not path.exists():
            continue
        if sha256_file(path) != digest or path.stat().st_size != size:
            problems.append(f"hash mismatch: {rel}")
    return problems


def load_register(folder: Path) -> dict:
    return json.loads((folder / "register.json").read_text(encoding="utf-8"))


def prediction_key(outcome_id: str) -> str:
    """Outcomes of one prediction share a key; only one may be scored."""
    if outcome_id.startswith("dec:"):
        return "dec"
    if outcome_id.startswith("item:"):
        return outcome_id
    return outcome_id.rsplit(":", 1)[0]


def validate(record: dict, register: dict) -> list[str]:
    errors = []
    items = {i["id"]: i for i in register["items"]}
    item = items.get(record.get("item_id"))
    if item is None:
        return [f"unknown item_id: {record.get('item_id')!r}"]
    if item["status"] == "declined":
        errors.append("item was declined; nothing to score")
    for field in ("arrived_utc", "opened_by", "compared_by", "register_commit", "manifest_check", "scores"):
        if field not in record:
            errors.append(f"missing field: {field}")
    if record.get("manifest_check") != "pass":
        errors.append("manifest_check must be 'pass' before comparison")
    arrived = str(record.get("arrived_utc", ""))
    if arrived[:10] < register["registered_utc"]:
        errors.append("arrived_utc precedes registration: record it as exploratory, not as a test")
    pushed = record.get("register_pushed_before_arrival")
    if pushed is not True and record.get("test_status") != "exploratory":
        errors.append("register_pushed_before_arrival must be true, or test_status must be 'exploratory'")
    registered = set(item["registered_outcome_ids"])
    seen = {}
    for s in record.get("scores", []):
        oid = s.get("outcome_id")
        if oid not in registered:
            errors.append(f"outcome id not registered for this item: {oid!r}")
            continue
        key = prediction_key(oid)
        if key in seen:
            errors.append(f"two outcomes scored for one prediction: {seen[key]!r} and {oid!r}")
        seen[key] = oid
        if not oid.endswith(":silent") and oid != "item:silent" and not s.get("evidence"):
            errors.append(f"non-silent outcome needs evidence (page, figure or frame): {oid!r}")
        if s.get("result") and str(s["result"]).upper() == "FAIL" and oid.endswith(":silent"):
            errors.append("silence is never a FAIL")
    if "item:unregistered-observation" in seen and not record.get("unregistered_observations"):
        errors.append("item:unregistered-observation needs the observation described in unregistered_observations")
    if "item:partial" in seen and not record.get("parts_pending"):
        errors.append("item:partial needs parts_pending")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    m = sub.add_parser("manifest")
    m.add_argument("--write", action="store_true")
    v = sub.add_parser("validate")
    v.add_argument("record", type=Path)
    sub.add_parser("status")
    ap.add_argument("--folder", type=Path, default=HERE)
    args = ap.parse_args()
    folder = args.folder
    if args.cmd == "check":
        problems = check(folder)
        for p in problems:
            print(p)
        print("manifest: " + ("FAILED" if problems else "ok") + f" ({len(read_manifest(folder)) if (folder / 'MANIFEST.md').exists() else 0} files)")
        sys.exit(1 if problems else 0)
    if args.cmd == "manifest":
        text = manifest_text(folder)
        if args.write:
            (folder / "MANIFEST.md").write_text(text, encoding="utf-8")
            print("wrote MANIFEST.md")
        else:
            print(text)
        return
    if args.cmd == "validate":
        record = json.loads(args.record.read_text(encoding="utf-8"))
        errors = validate(record, load_register(folder))
        for e in errors:
            print(e)
        print("record: " + ("INVALID" if errors else "valid"))
        sys.exit(1 if errors else 0)
    if args.cmd == "status":
        for item in load_register(folder)["items"]:
            print(f"{item['id']}: {item['status']} ({item['status_note']})")


if __name__ == "__main__":
    main()
