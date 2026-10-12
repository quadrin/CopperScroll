#!/usr/bin/env python3
"""Phase 4, part E, reader r1: write the span-check input (one JSON object per coded unit) for verify_spans.py.

  python3 -I export_spans_input.py > spans_input.jsonl
Reads data/coding/*.json. Standard library only.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODING = HERE.parent / "data" / "coding"


def main():
    for p in sorted(CODING.glob("*.json")):
        for r in json.loads(p.read_text(encoding="utf-8")):
            print(json.dumps(dict(report_id=r["report_id"], text_file=r.get("text_file", "raw"),
                                  text_lines=r["text_lines"],
                                  quotes=[f["quote"] for f in r["features"] if f.get("quote")]),
                             ensure_ascii=False))


if __name__ == "__main__":
    main()
