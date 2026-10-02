#!/usr/bin/env python3
"""Reproduce conditional cubit ranges without assigning an archaeological datum."""
import json
from decimal import Decimal
from pathlib import Path

BASELINE = "bb2fde4c76dbbe34b4c7345646acee049e875229"
INPUTS = [("11", "II 13–15", 4), ("25", "VI 1–6", 3), ("26", "VI 7–10", 9)]


def calculate():
    rows = []
    for entry, lines, cubits in INPUTS:
        values = [
            {"metres_per_cubit": float(Decimal(i) / 100),
             "distance_m": float(Decimal(cubits) * Decimal(i) / 100)}
            for i in range(40, 61)
        ]
        rows.append({"entry": entry, "lines": lines, "cubits": cubits,
                     "range_m": [values[0]["distance_m"], values[-1]["distance_m"]],
                     "samples": values,
                     "datum": None,
                     "direction_of_measurement": "unresolved; downward is a conditional model",
                     "architectural_phase": "unresolved"})
    return {"baseline_commit": BASELINE,
            "input_source": "text/translation_en.json (project translation)",
            "unit_range_status": "exploratory sensitivity assumption",
            "independent_archaeological_measurement": False,
            "results": rows}


if __name__ == "__main__":
    output = Path(__file__).with_name("unit_sensitivity.json")
    output.write_text(json.dumps(calculate(), indent=2) + "\n", encoding="utf-8")
    print(output)
