#!/usr/bin/env python3
"""Export the frozen phase-2 plan parameters (the JSON block of ../../phase2_2026-10-10/PLAN.md) for the screen
scripts that run on the owner's computer (screen_volume.py, locate_headings.py --params).

  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_c/scripts/export_params.py OUT.json
"""
import json
import re
import sys
from pathlib import Path

PLAN = Path(__file__).resolve().parents[3] / "phase2_2026-10-10" / "PLAN.md"


def main(out):
    m = re.search(r"```json\n(.*?)\n```", PLAN.read_text(encoding="utf-8"), re.S)
    params = json.loads(m.group(1))
    Path(out).write_text(json.dumps(params, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
