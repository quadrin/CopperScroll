"""Step 2 record: one row per inventory cave with position, entrances, size, period and deposit signs."""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from overrides import O  # noqa: E402

OUT = os.path.join(HERE, "..", "out")
rows = {r["cave_id"]: r for r in json.load(open(os.path.join(OUT, "all_rows.json"), encoding="utf-8"))}
texts = json.load(open(os.path.join(OUT, "cave_texts.json"), encoding="utf-8"))
inv = list(csv.DictReader(open(os.path.join(OUT, "inventory.csv"), encoding="utf-8")))
by = {}
for x in inv:
    by.setdefault(x["cave_id"], []).append(x)
SIZE = re.compile(r"\d+(?:\.\d+)?\s*(?:x|×)\s*\d+(?:\.\d+)?\s*m|\b\d+(?:\.\d+)?\s*m (?:deep|wide|high|long)|depth \d+ ?m|\d+ sq m", re.I)
DEP = re.compile(r"blocked|sealed|walled|closed by|hidden|stored|robb|plunder|emptied|holes|pickax|violated|looter|earlier digging|spoil", re.I)
cols = ["cave_id", "src", "kind", "entries", "near_place", "dist_m", "lat", "lon", "precision_m", "placement", "source_records",
        "n_openings", "opening_facings", "size", "period_stated", "period_in_window", "excavation_status", "finds",
        "deposit_signs", "override_basis"]
with open(os.path.join(OUT, "inventory_descriptors.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for cid, xs in sorted(by.items()):
        r = rows[cid]; t = texts.get(cid, "")
        dep = sorted({m.group(0).lower() for m in DEP.finditer(t)})
        if O.get(cid, {}).get("removal"):
            dep.append("(hand) removal/blocking stated")
        w.writerow({"cave_id": cid, "src": r["_src"], "kind": r["_kind"], "entries": ";".join(x["entry"] for x in xs),
                    "near_place": xs[0]["near_place"], "dist_m": xs[0]["dist_m"], "lat": r["lat"], "lon": r["lon"],
                    "precision_m": r.get("precision_m", ""), "placement": xs[0].get("placement", ""),
                    "source_records": r.get("source_records", ""), "n_openings": r.get("n_openings", ""),
                    "opening_facings": r.get("opening_facings", ""), "size": "; ".join(SIZE.findall(t))[:120],
                    "period_stated": r.get("period_stated", "") or r.get("asi_periods", ""),
                    "period_in_window": r.get("period_in_window", "") or r.get("asi_cave_dated_in_window", ""),
                    "excavation_status": r.get("excavation_status", ""), "finds": r.get("finds", ""),
                    "deposit_signs": "; ".join(dep), "override_basis": O.get(cid, {}).get("basis", "")})
print(len(by))
