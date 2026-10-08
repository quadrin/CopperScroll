#!/usr/bin/env python3
"""Compare the size of real silver hoards (hoards.json, scored + comparanda) with the scroll's amounts
under the talent and karsh readings.  Output: ../quantity_overview.csv and printed summary.
Conventions (see scoring_rules.json): talent 21.3 kg; karsh 71 g (alt. 142 g); karsh only for bare ככ."""
import csv
import json
import os
import statistics as st

OUT = "agent_review/wave1/T02_hoard_match"
hoards = json.load(open(os.path.join(OUT, "hoards.json")))
entries = json.load(open(os.path.join(OUT, "entry_features.json")))

hm = []
for h in hoards:
    m = h.get("mass_g")
    if m and m[0] and set(h["contents"]) & {"silver_coins", "silver_bullion"} and h["scope"] != "out_period":
        mid = (m[0] + (m[1] or m[0])) / 2
        hm.append((h["id"], h["name"], h["scope"], mid))
hm.sort(key=lambda x: -x[3])

rows = []
for e in entries:
    a = e.get("amount_talents_as_translated")
    if not a:
        continue
    uf = e["unit_form"]
    rows.append({"entry": e["entry"], "title": e["title"], "amount": a, "unit_form": uf,
                 "as_talents_kg": round(a * 21.3, 1),
                 "as_karsh71_kg": round(a * 0.071, 2) if uf in ("abbr", "mixed") else "",
                 "as_karsh142_kg": round(a * 0.142, 2) if uf in ("abbr", "mixed") else ""})
with open(os.path.join(OUT, "quantity_overview.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

inreg = [x[3] / 1000 for x in hm if x[2] in ("in", "edge")]
allm = [x[3] / 1000 for x in hm]
abbr71 = [r["as_karsh71_kg"] for r in rows if r["as_karsh71_kg"] != ""]
abbr142 = [r["as_karsh142_kg"] for r in rows if r["as_karsh142_kg"] != ""]
tal_full = [r["as_talents_kg"] for r in rows if r["unit_form"] in ("full", "none")]
tal_abbr = [r["as_talents_kg"] for r in rows if r["unit_form"] in ("abbr", "mixed")]


def rng(v):
    return f"n={len(v)} min={min(v):.2f} median={st.median(v):.2f} max={max(v):.2f} kg"


print("Silver hoards with a mass estimate (in/edge region):", rng(inreg))
print("  largest:", [(x[0], x[1][:35], round(x[3] / 1000, 2)) for x in hm[:6]])
print("Scroll abbreviated amounts as karsh 71 g:", rng(abbr71))
print("Scroll abbreviated amounts as karsh 142 g:", rng(abbr142))
print("Scroll abbreviated amounts read as talents:", rng(tal_abbr))
print("Scroll full-spelled talent amounts:", rng(tal_full))
mx = max(inreg)
print("share of abbreviated amounts (karsh 71 g) <= largest in-region hoard (%.2f kg):" % mx,
      sum(v <= mx for v in abbr71), "/", len(abbr71))
print("share of abbreviated amounts (karsh 142 g) <= largest in-region hoard:", sum(v <= mx for v in abbr142), "/", len(abbr142))
print("share of any amount read as talents <= largest in-region hoard:", sum(v <= mx for v in tal_full + tal_abbr), "/", len(tal_full + tal_abbr))
print("Isfiya (out of region) nominal kg:", [round(x[3] / 1000, 1) for x in hm if x[0] == "X01"])
