"""Source-4 addendum: merge source-4-only coding into a coder's existing sheets.

Usage:
    python3 -I merge_s4.py PACKETS_DIR BASE_CODED_DIR S4_CODED_DIR OUT_DIR

For every unit in S4_CODED_DIR, the base sheet keeps all its features and absence statements
from sources 1, 2, 3 and 5. Its source-4 entries are replaced by the source-4 coding: features
get ids prefixed "s4_", sources["4"] becomes the packet's source-4 status. Units without a
source-4 sheet are copied unchanged. Every output sheet is validated against its packet.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import match as M  # noqa: E402


def merge(base, s4):
    out = dict(base)
    keep = [f for f in base["features"] if f.get("source") != "4"]
    ids = {f["id"] for f in keep}
    new = []
    rename = {}
    for f in s4.get("features", []):
        nid = f["id"] if f["id"].startswith("s4_") else "s4_" + f["id"]
        rename[f["id"]] = nid
    for f in s4.get("features", []):
        g = dict(f)
        g["id"] = rename[f["id"]]
        g["source"] = "4"
        if g.get("mouth") and g["mouth"].get("pit_id") in rename:
            g["mouth"] = dict(g["mouth"], pit_id=rename[g["mouth"]["pit_id"]])
        if g["id"] in ids:
            raise ValueError(f"{base['unit_id']}: duplicate feature id {g['id']}")
        new.append(g)
    out["features"] = keep + new
    out["explicit_absence"] = [a for a in base.get("explicit_absence", []) if a.get("source") != "4"] + \
        [dict(a, source="4") for a in s4.get("explicit_absence", [])]
    out["sources"] = dict(base["sources"], **{"4": s4.get("source4_status", "read")})
    note = s4.get("notes", "").strip()
    if note:
        out["notes"] = (base.get("notes", "") + " | source-4 addendum: " + note).strip(" |")
    return out


def main(packets_dir, base_dir, s4_dir, out_dir):
    packets = M.load_packets(packets_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    s4 = M.load_sheets(s4_dir)
    bad = 0
    for p in sorted(Path(base_dir).glob("*.json")):
        uid = p.stem
        base = json.loads(p.read_text(encoding="utf-8"))
        sheet = merge(base, s4[uid]) if uid in s4 else base
        errs = M.validate_sheet(sheet, packets[uid])
        if errs:
            bad += 1
            print(f"{uid}: {errs[:3]}")
        if uid in s4:
            (out_dir / p.name).write_text(json.dumps(sheet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            shutil.copy(p, out_dir / p.name)
    missing = sorted(set(s4) - {p.stem for p in Path(base_dir).glob("*.json")})
    print(f"merged {len(s4)} source-4 sheets into {base_dir}; invalid: {bad}; s4 sheets with no base sheet: {missing}")
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main(*sys.argv[1:5])
