"""Addendum merge: append one source's new coding to a coder's existing sheets.

Usage:
    python3 -I merge_source.py PACKETS_DIR BASE_CODED_DIR ADD_CODED_DIR OUT_DIR SOURCE ID_PREFIX

Every feature and absence statement already in the base sheet is kept, including earlier coding
of the same source. The added sheet's features get ids prefixed ID_PREFIX and "source": SOURCE;
its absence statements get "source": SOURCE; sources[SOURCE] becomes "read". Units without an
added sheet are copied unchanged. Every output sheet is validated against its packet.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import match as M  # noqa: E402


def merge(base, add, source, prefix):
    out = dict(base)
    ids = {f["id"] for f in base["features"]}
    rename = {f["id"]: (f["id"] if f["id"].startswith(prefix) else prefix + f["id"]) for f in add.get("features", [])}
    new = []
    for f in add.get("features", []):
        g = dict(f, id=rename[f["id"]], source=source)
        if g.get("mouth") and g["mouth"].get("pit_id") in rename:
            g["mouth"] = dict(g["mouth"], pit_id=rename[g["mouth"]["pit_id"]])
        if g["id"] in ids:
            raise ValueError(f"{base['unit_id']}: duplicate feature id {g['id']}")
        new.append(g)
    out["features"] = base["features"] + new
    out["explicit_absence"] = base.get("explicit_absence", []) + [dict(a, source=source) for a in add.get("explicit_absence", [])]
    out["sources"] = dict(base["sources"], **{source: "read"})
    note = add.get("notes", "").strip()
    if note:
        out["notes"] = (base.get("notes", "") + f" | source-{source} addendum: " + note).strip(" |")
    return out


def main(packets_dir, base_dir, add_dir, out_dir, source, prefix):
    packets = M.load_packets(packets_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    add = M.load_sheets(add_dir)
    bad = 0
    bases = {p.stem: p for p in Path(base_dir).glob("*.json")}
    for uid, p in sorted(bases.items()):
        base = json.loads(p.read_text(encoding="utf-8"))
        if uid in add:
            sheet = merge(base, add[uid], source, prefix)
            (out_dir / p.name).write_text(json.dumps(sheet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            sheet = base
            shutil.copy(p, out_dir / p.name)
        errs = M.validate_sheet(sheet, packets[uid])
        if errs:
            bad += 1
            print(f"{uid}: {errs[:3]}")
    missing = sorted(set(add) - set(bases))
    print(f"merged {len(add)} source-{source} sheets; invalid: {bad}; added sheets with no base sheet: {missing}")
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main(*sys.argv[1:7])
