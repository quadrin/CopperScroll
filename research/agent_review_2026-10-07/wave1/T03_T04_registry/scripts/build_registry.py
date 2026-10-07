# -*- coding: utf-8 -*-
"""Build registry.json / registry.csv / registry_schema.json and the Goal-B tables.

Run:  python3 -I build_registry.py <cs_root> <out_dir>
Reads only shared/ inputs (entries.json, places.json, entry_concordance.csv).
Coordinates are copied from places.json; nothing is typed by hand.
"""
import csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # records_* live next to this script (not in downloads/)
import records_a, records_b, records_c  # noqa: E402

CS, OUT = sys.argv[1], sys.argv[2]
SH = os.path.join(CS, "shared")

CUBIT_PRIMARY = (0.445, 0.525)   # working range used by the repo (cycle7 kohlit_pool.md item 5; site_identification_review)
CUBIT_WIDE = (0.40, 0.60)        # exploratory range used by the repo (cycle7 kohlit_pool.md item 5)
REGISTRY_VERSION = "0.1-draft"
DRAFTED = "2026-10-06"

PERIOD_STD = ("Feature must be shown to exist (built, or standing as an accessible ruin) at some time within c. 50 BCE–70 CE "
              "(the repo's criterion 'in use 1st c. BCE–70 CE'); an extended window to 135 CE is allowed to cover the Bar Kokhba-era "
              "dating reported for Gibson 2025/26. A feature whose earliest construction is securely later than 135 CE is a period MISS for that feature.")
REPORT_CORE = ["excavation/survey identifier, permit number, dates and director",
               "locus/feature IDs with stratigraphic phase assignments and the dating evidence for construction, use and abandonment (pottery, coins with catalogue numbers, 14C lab numbers)",
               "surveyed coordinates of the feature outline and key points, with datum (ITM/ICS/WGS84) and horizontal accuracy",
               "absolute elevations of ancient floors/surfaces, thresholds, bedrock and the excavation limits",
               "plan of excavated vs unexcavated area and the depth reached in each part (needed to score absence)",
               "disturbances: robber pits, modern intrusions, earlier excavation dumps",
               "any cache/hoard or inscribed object with exact findspot (x, y, z) relative to the feature"]
OUTCOME_LEVELS = {
    "L0": "INCONCLUSIVE — criteria cannot be applied (undated, partial coverage, missing measurements).",
    "L1": "TYPE — a feature of the predicted type exists at the site in the period (already known for several entries; counts only if newly observed).",
    "L2": "FEATURE — the predicted feature with all reading-specific constraints (orientation, relative position, distance) is observed and dated; rival features listed.",
    "L3": "SPOT — at the predicted spot/depth window a cut, cavity or disturbance of the period is documented (an empty or refilled cavity is consistent with ancient retrieval).",
    "L4": "DEPOSIT — a deposit of the kind the entry lists is found at the spot.",
    "MISS": "The record's MISS criterion is met (scope stated in the record: feature-level or target-level).",
}

places = {p["id"]: p for p in json.load(open(os.path.join(SH, "places.json"), encoding="utf-8"))}
entries = {e["entry"]: e for e in json.load(open(os.path.join(SH, "entries.json"), encoding="utf-8"))}
conc = {}
with open(os.path.join(SH, "entry_concordance.csv"), encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        conc[row["entry_puech"]] = row

from decimal import Decimal, ROUND_HALF_UP
def metres(c, rng):
    q = lambda x: float((Decimal(str(c)) * Decimal(str(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return [q(rng[0]), q(rng[1])]

OVERRIDES = {"P49-C": {"priority": "low"}}  # unscorable branch inherits the shortlist priority otherwise

records = []
for src in (records_a.R, records_b.R, records_c.R):
    for r in src:
        r = {**r, **OVERRIDES.get(r["id"], {})}
        e = entries[r["entry"]]
        pid = r.get("place_id")
        p = places.get(pid) if pid else None
        if pid and p is None:
            raise SystemExit(f"unknown place_id {pid} in {r['id']}")
        meas = []
        for m in r.get("measures", []):
            mm = dict(m)
            if m.get("cubits") is not None:
                mm["metres_primary_0.445_0.525"] = metres(m["cubits"], CUBIT_PRIMARY)
                mm["metres_wide_0.40_0.60"] = metres(m["cubits"], CUBIT_WIDE)
            else:
                mm["metres_primary_0.445_0.525"] = None
                mm["metres_wide_0.40_0.60"] = None
            meas.append(mm)
        c = conc.get(r["entry"], {})
        out = {
            "id": r["id"], "registry_version": REGISTRY_VERSION, "drafted": DRAFTED, "status": "open (draft, not yet publicly timestamped)",
            "entry": r["entry"], "lines": c.get("col_line", e["lines"][0]["ref"] + "–" + e["lines"][-1]["ref"]),
            "milik_item": c.get("item_milik"), "lefkovits_item": c.get("item_lefkovits"),
            "entry_title_project": e["title"],
            "entry_text_he": " / ".join(l["hebrew"] for l in e["lines"]),
            "entry_text_en_project": " / ".join(l["english"] for l in e["lines"]),
            "branch": r["branch"], "rank": r.get("rank"),
            "reading_assumed": r["reading_assumed"], "reading_editions": r["reading_editions"], "reading_status": r["reading_status"],
            "place_id": pid,
            "site_name": p["name"] if p else None,
            "project_entry_status": e["status"], "project_entry_confidence": e["confidence"],
            "project_candidate_status": next((f"{x['status']}/{x['confidence']}" for x in e["candidates"] if x.get("placeId") == pid), None),
            "anchor_lat": p["lat"] if p else None, "anchor_lon": p["lon"] if p else None,
            "anchor_precision": p["precision"] if p else "not in project gazetteer — no coordinate asserted",
            "anchor_note": "Gazetteer anchor for the site/area (shared/places.json), NOT the predicted feature's position.",
            "feature_type": r["feature_type"], "feature_detail": r["feature_detail"],
            "period_requirement": PERIOD_STD,
            "orientation_constraint": r["orientation"],
            "measures": meas,
            "location_constraint": r["location"],
            "confirm": r["confirm"], "miss": r["miss"], "inconclusive": r["inconclusive"],
            "deposit_expected": r.get("deposit", "As listed in the entry text (entry_text_en_project); used only for L4."),
            "report_must_record": REPORT_CORE + r.get("report_extra", []),
            "priority": r["priority"], "scorability": r["scorability"],
            "rank_scores": r.get("rank_scores"),
            "evidence": [{"label": "EVIDENCE", "claim": a, "source": b} for a, b in r["evidence"]],
            "inference": {"label": "INFERENCE", "text": r["inference"][0], "confidence": r["inference"][1]},
            "sources": r["sources"],
            "outcome": None, "outcome_level": None, "scored_report": None, "scored_by": None, "scored_date": None,
        }
        hashed = {k: v for k, v in out.items() if not k.startswith(("outcome", "scored_"))}
        out["record_sha256"] = hashlib.sha256(json.dumps(hashed, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        records.append(out)

ids = [r["id"] for r in records]
assert len(ids) == len(set(ids)), "duplicate ids"

meta = {
    "title": "Copper Scroll (3Q15) prediction registry — draft",
    "version": REGISTRY_VERSION, "drafted": DRAFTED,
    "numbering": "Puech 2006/2015 entry numbers (1–60 + 12a); Milik and Lefkovits item numbers from shared/entry_concordance.csv",
    "cubit_ranges_m": {"primary": CUBIT_PRIMARY, "wide": CUBIT_WIDE,
                        "note": "Ranges adopted from the quadrin/CopperScroll research files (cycle7 kohlit_pool.md item 5); not independently derived here."},
    "outcome_levels": OUTCOME_LEVELS,
    "hebrew_text_license": "Hebrew: Abegg, Bowley and Cook, ETCBC dss 2.0.1 (CC BY-NC 4.0), via shared/entries.json. English: CopperScroll project translation.",
    "n_records": len(records),
}
json.dump({"meta": meta, "records": records}, open(os.path.join(OUT, "registry.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- CSV (flattened)
cols = ["id", "entry", "lines", "milik_item", "lefkovits_item", "branch", "rank", "priority", "scorability", "reading_assumed", "reading_editions", "reading_status",
        "place_id", "site_name", "project_candidate_status", "anchor_lat", "anchor_lon", "anchor_precision", "feature_type", "feature_detail", "orientation_constraint",
        "measures", "location_constraint", "period_requirement", "confirm", "miss", "inconclusive", "deposit_expected", "report_must_record", "rank_scores",
        "evidence", "inference", "sources", "record_sha256", "outcome", "outcome_level", "scored_report", "scored_by", "scored_date"]

def flat(v):
    if v is None:
        return ""
    if isinstance(v, list):
        if v and isinstance(v[0], dict):
            if "claim" in v[0]:
                return " | ".join(f"EVIDENCE: {d['claim']} [{d['source']}]" for d in v)
            return " | ".join(
                f"{d.get('cubits')} c. ({d.get('edition')}; {d.get('type')}) = {d.get('metres_primary_0.445_0.525')} m [wide {d.get('metres_wide_0.40_0.60')}]" for d in v)
        return " | ".join(str(x) for x in v)
    if isinstance(v, dict):
        if v.get("label") == "INFERENCE":
            return f"INFERENCE ({v['confidence']}): {v['text']}"
        return "; ".join(f"{k}={x}" for k, x in v.items())
    return str(v)

with open(os.path.join(OUT, "registry.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for r in records:
        w.writerow([flat(r.get(c)) for c in cols])

# ---- schema
schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Copper Scroll prediction registry record",
    "type": "object",
    "required": ["id", "entry", "branch", "reading_assumed", "feature_type", "confirm", "miss", "inconclusive", "report_must_record", "record_sha256"],
    "properties": {
        "id": {"type": "string", "description": "P<entry>-<branch letter> or P60-T<rank>"},
        "registry_version": {"type": "string"}, "drafted": {"type": "string", "format": "date"}, "status": {"type": "string"},
        "entry": {"type": "string", "description": "Puech entry number"}, "lines": {"type": "string"},
        "milik_item": {"type": ["string", "null"]}, "lefkovits_item": {"type": ["string", "null"]},
        "entry_title_project": {"type": "string"}, "entry_text_he": {"type": "string"}, "entry_text_en_project": {"type": "string"},
        "branch": {"type": "string", "description": "the reading/site branch this record predicts under"},
        "rank": {"type": ["integer", "null"], "description": "entry-60 search-target rank (1 = first); null elsewhere or unrankable"},
        "reading_assumed": {"type": "string"}, "reading_editions": {"type": "array", "items": {"type": "string"}}, "reading_status": {"type": "string"},
        "place_id": {"type": ["string", "null"], "description": "shared/places.json id; null if the target is not in the gazetteer"},
        "site_name": {"type": ["string", "null"]}, "project_entry_status": {"type": "string"}, "project_entry_confidence": {"type": "string"},
        "project_candidate_status": {"type": ["string", "null"]},
        "anchor_lat": {"type": ["number", "null"]}, "anchor_lon": {"type": ["number", "null"]}, "anchor_precision": {"type": "string"}, "anchor_note": {"type": "string"},
        "feature_type": {"type": "string"}, "feature_detail": {"type": "string"}, "period_requirement": {"type": "string"},
        "orientation_constraint": {"type": "string"},
        "measures": {"type": "array", "items": {"type": "object", "properties": {
            "cubits": {"type": ["number", "null"]}, "edition": {"type": "string"}, "type": {"type": "string"},
            "metres_primary_0.445_0.525": {"type": ["array", "null"]}, "metres_wide_0.40_0.60": {"type": ["array", "null"]}}}},
        "location_constraint": {"type": "string"}, "confirm": {"type": "string"}, "miss": {"type": "string"}, "inconclusive": {"type": "string"},
        "deposit_expected": {"type": "string"}, "report_must_record": {"type": "array", "items": {"type": "string"}},
        "priority": {"enum": ["high", "medium", "low"]}, "scorability": {"type": "string"},
        "rank_scores": {"type": ["object", "null"]},
        "evidence": {"type": "array", "items": {"type": "object", "properties": {"label": {"const": "EVIDENCE"}, "claim": {"type": "string"}, "source": {"type": "string"}}}},
        "inference": {"type": "object", "properties": {"label": {"const": "INFERENCE"}, "text": {"type": "string"}, "confidence": {"type": "string"}}},
        "sources": {"type": "array", "items": {"type": "string"}},
        "outcome": {"type": ["string", "null"]}, "outcome_level": {"enum": [None, "L0", "L1", "L2", "L3", "L4", "MISS"]},
        "scored_report": {"type": ["string", "null"]}, "scored_by": {"type": ["string", "null"]}, "scored_date": {"type": ["string", "null"]},
        "record_sha256": {"type": "string", "description": "SHA-256 of the canonical JSON (sort_keys, UTF-8) of the record without outcome*/scored_* fields"},
    },
}
json.dump(schema, open(os.path.join(OUT, "registry_schema.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- manifest of hashes
with open(os.path.join(OUT, "registry_hashes.txt"), "w", encoding="utf-8") as f:
    for r in records:
        f.write(f"{r['record_sha256']}  {r['id']}\n")

print(len(records), "records")
from collections import Counter
print(Counter(r["priority"] for r in records))
print(Counter(r["entry"] for r in records))
