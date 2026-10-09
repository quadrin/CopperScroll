#!/usr/bin/env python3
"""Write looks_v2.csv: looks.csv with the IV/17 rows moved to the new W2B v2 place state.

    python3 -I research/models/search_effectiveness/build_looks_v2.py [--check]

looks.csv codes the IV/17 records (L43, L44) at U_JERICHO, because places_v1 has no IV/17 state.
The W2B v2 inputs add the place iv17_abu_saraj. This script changes only the place_id field of
L43 and L44 (U_JERICHO -> iv17_abu_saraj). Every other byte of looks.csv is kept. looks.csv is not edited.
"""
import argparse
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOOKS = HERE / "looks.csv"
LOOKS_V2 = HERE / "looks_v2.csv"
REMAP = {"L43": ("25", "U_JERICHO", "iv17_abu_saraj"), "L44": ("25", "U_JERICHO", "iv17_abu_saraj")}


def build(src=LOOKS):
    raw = Path(src).read_bytes()
    lines = raw.split(b"\n")
    done = set()
    for i, line in enumerate(lines):
        for lid, (entry, old, new) in REMAP.items():
            prefix = f"{lid},{entry},{old},".encode()
            if line.startswith(prefix):
                lines[i] = f"{lid},{entry},{new},".encode() + line[len(prefix):]
                done.add(lid)
    if done != set(REMAP):
        raise SystemExit(f"rows not found for remapping: {sorted(set(REMAP) - done)}")
    return b"\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = build()
    if a.check:
        if not LOOKS_V2.exists() or LOOKS_V2.read_bytes() != out:
            raise SystemExit("looks_v2.csv differs from a fresh build")
        print("looks_v2.csv matches a fresh build")
        return
    LOOKS_V2.write_bytes(out)
    print(f"wrote {LOOKS_V2.name} sha256 {hashlib.sha256(out).hexdigest()}")


if __name__ == "__main__":
    main()
