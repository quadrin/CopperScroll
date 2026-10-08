"""Koḥlit rarity count, Stage 1a: the scripted WBADB screen for pool words.

Implements §5 Stage 1 of research/preregistration/kohlit_rarity_2026-10-08.md for
source 1 (WBADB). Source 3 (SWP Memoirs) is screened separately in Stage 1b; until
then a unit with no WBADB pool word is "pending SWP", never "not recorded".

Usage:
    python3 -I stage1_screen.py WBADB_data1.xlsx OUT_DIR

Needs pandas, openpyxl and pyproj. The script checks the spreadsheet's SHA-256
against the value recorded below and stops if it differs.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
WBADB_URL = "https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx"
WBADB_SHA256 = "3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b"

# Fixed by the pre-registration (§3, §5)
R1_EAST_OF_X = 175_000            # Old Israel Grid easting, metres
R2_CENTRE_LATLON = (31.7418, 35.4594)  # Kh. Qumran (places_v1)
R2_RADIUS_M = 30_000
SCREEN_RADIUS_M = 2_000           # Stage 1: pool words within 2 km of the unit

W = json.loads((HERE / "words.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def word_regex(words):
    alts = sorted((re.escape(w).replace(r"\ ", r"[\s\-]") for w in words), key=len, reverse=True)
    return re.compile(r"(?<![a-z])(" + "|".join(alts) + r")(?:e?s)?(?![a-z])", re.IGNORECASE)


POOL_RE = word_regex(W["pool_words"])
SETTLE_RE = word_regex(W["settlement_terms"])


def text(row, fields):
    vals = []
    for f in fields:
        v = row.get(f)
        if isinstance(v, str) and v.strip() not in ("", "-", "NDA"):
            vals.append(v)
    return " ; ".join(vals)


def flag(row, cols):
    out = []
    for c in cols:
        v = row.get(c)
        try:
            if v is not None and not (isinstance(v, float) and math.isnan(v)) and int(v) > 0:
                out.append(c)
        except (TypeError, ValueError):
            pass
    return out


def main(xlsx: Path, out_dir: Path) -> None:
    digest = sha256(xlsx)
    if digest != WBADB_SHA256:
        sys.exit(f"WBADB file hash {digest} does not match the frozen {WBADB_SHA256}")
    out_dir.mkdir(parents=True, exist_ok=True)

    book = pd.ExcelFile(xlsx)
    sur = book.parse("Surveyed")
    exc = book.parse("Excavations")
    sur["row_id"] = "S" + sur["Index"].astype(str)
    exc["row_id"] = "E" + exc["Index"].astype(str)
    rows = pd.concat([sur, exc], ignore_index=True, sort=False)
    rows = rows[pd.to_numeric(rows["X"], errors="coerce").notna() & pd.to_numeric(rows["Y"], errors="coerce").notna()]
    rows["X"] = rows["X"].astype(float)
    rows["Y"] = rows["Y"].astype(float)

    to_grid = Transformer.from_crs("EPSG:4326", "EPSG:28193", always_xy=True)
    qx, qy = to_grid.transform(R2_CENTRE_LATLON[1], R2_CENTRE_LATLON[0])
    qy -= 1_000_000  # WBADB uses the Old Israel Grid without the 1,000,000 m false-northing offset

    # pool-word rows (any sheet, any region)
    pool_rows = []
    for _, r in rows.iterrows():
        t = text(r, W["pool_fields"])
        m = POOL_RE.findall(t)
        if m:
            pool_rows.append((r["row_id"], str(r.get("Site_Name", "")), r["X"], r["Y"],
                              sorted({x.lower() for x in m})))

    units = []
    for _, r in rows.iterrows():
        sheet = "Surveyed" if r["row_id"].startswith("S") else "Excavations"
        if sheet == "Excavations" and str(r.get("Surveyed", "")).strip().lower() == "yes":
            continue  # already a unit through its survey row
        name = str(r.get("Site_Name", "")).strip()
        settle_text = text(r, W["settlement_fields"])
        terms = sorted({x.lower() for x in SETTLE_RE.findall(settle_text)})
        prefix = next((p for p in W["settlement_name_prefixes"] if name.lower().startswith(p)), None)
        if not terms and not prefix:
            continue
        main_p = flag(r, W["periods"]["main"])
        pre70 = flag(r, W["periods"]["sensitivity_pre70"])
        if not pre70:
            continue
        x, y = r["X"], r["Y"]
        in_r1 = x > R1_EAST_OF_X
        in_r2 = in_r1 and math.hypot(x - qx, y - qy) <= R2_RADIUS_M
        if not in_r1:
            continue
        hits = []
        for rid, pname, px, py, words in pool_rows:
            d = math.hypot(px - x, py - y)
            if d <= SCREEN_RADIUS_M:
                hits.append((round(d), rid, pname, "/".join(words)))
        hits.sort()
        excavated = sheet == "Excavations" or str(r.get("Excavated", "")).strip().lower() not in ("", "-", "no", "nan")
        units.append({
            "unit_id": r["row_id"],
            "name": name,
            "x": int(x), "y": int(y),
            "in_R1": in_r1, "in_R2": bool(in_r2),
            "main_set": bool(main_p),            # Hellenistic or Roman recorded
            "pre70_set": True,                   # sensitivity run: any period before 70 CE
            "periods_hel_rom": ",".join(main_p),
            "settlement_basis": ";".join(terms + ([f"name:{prefix.strip()}"] if prefix else [])),
            "excavated": bool(excavated),
            "survey_ref": str(r.get("Survey_Ref", "")),
            "wbadb_pool_hits": len(hits),
            "nearest_hit_m": hits[0][0] if hits else "",
            "hits": " | ".join(f"{d} m {rid} {pn} [{w}]" for d, rid, pn, w in hits[:12]),
            "stage1a": "to Stage 2" if hits else "pending SWP screen",
        })

    df = pd.DataFrame(units).sort_values(["main_set", "y"], ascending=[False, False])
    df.to_csv(out_dir / "stage1a_units.csv", index=False)

    def counts(sub):
        return {
            "units": int(len(sub)),
            "to_stage2": int((sub["stage1a"] == "to Stage 2").sum()),
            "pending_swp": int((sub["stage1a"] == "pending SWP screen").sum()),
            "excavated": int(sub["excavated"].sum()),
        }

    summary = {
        "wbadb_sha256": digest,
        "wbadb_url": WBADB_URL,
        "screen_radius_m": SCREEN_RADIUS_M,
        "R1_main (Hel/Rom)": counts(df[df["main_set"]]),
        "R1_pre70 (sensitivity)": counts(df),
        "R2_main (Hel/Rom)": counts(df[df["main_set"] & df["in_R2"]]),
        "R2_pre70 (sensitivity)": counts(df[df["in_R2"]]),
        "pool_word_rows_in_wbadb": len(pool_rows),
    }
    (out_dir / "stage1a_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
