"""Helpers for the hand-coded cave records (research/regional/caves_entry25/coded/*.py).

Each coded module builds two lists with R() and X():
- R(): one admitted cave row (PLAN.md 4.1), with the fields of caves.csv that are coded by hand.
- X(): one record read but not admitted (rock shelter, niche, cistern, outside the box, ...).

Field conventions (PLAN.md 4.3-4.5):
- n_open: int or None. open_basis: 'stated number' | 'singular description' | 'plan' | 'pair named' | ''.
- facings: '' or 'cave:E' (a facing for the cave as a whole) or 'm1:E;m2:E' (per mouth), compass
  abbreviations N, NNE, NE, ..., as in rules.json; facing_basis: 'word in text' | 'numeric' | 'plan' | ''.
- res: 4, 8 or 16 (compass-word resolution of the source report), or None.
- pillar / terrace: 'yes' | 'no' | None (unknown).
- north: 'decided' | 'undetermined' | None. C5 is scored from it and from n_open.
- piw (period in window): 'yes' | 'yes+other' | 'partly' | 'no' | '' (none stated).
- exposure: 'exposed-repo' | 'page-opened-before' | 'unexposed-at-freeze' | 'exposed-this-worker'.
- grid: the printed grid reference string; crs: 'OIG' (Palestine/Old Israel Grid) or 'ITM' or 'WGS84'.
"""

FIELDS = [
    "cave_id", "name_number", "source_records", "other_ids", "lineage", "feature_type_source",
    "row_kind", "cluster_count", "coord_printed", "crs_printed", "precision_m", "coord_basis",
    "where_described", "n_openings", "openings_basis", "opening_facings", "facing_basis",
    "facing_resolution", "north_case", "pillar", "pillar_kind", "pillar_position", "pillar_basis",
    "terrace", "terrace_basis", "northern_member", "northern_basis", "published_plan",
    "period_stated", "period_in_window", "excavation_status", "finds", "exposure", "first_read_utc",
    "c1_override", "coord_ok", "notes",
]

XFIELDS = ["record_id", "name_number", "source_records", "feature_type_source", "coord_printed",
           "crs_printed", "reason", "exposure", "first_read_utc", "notes"]


def R(rows, cave_id, *, num, src, lineage, ftype="cave", kind="cave", cluster=None, grid="", crs="OIG",
      prec=None, cbasis="printed grid", where="", n_open=None, open_basis="", facings="",
      facing_basis="", res=None, north_case="", pillar=None, pillar_kind="", pillar_pos="",
      pillar_basis="", terrace=None, terrace_basis="", north=None, north_basis="", plan="none",
      period="", piw="", exc="", finds="", exposure="unexposed-at-freeze", read="", c1=None,
      other_ids="", notes="", coord_ok=True):
    rows.append({
        "cave_id": cave_id, "name_number": num, "source_records": src, "other_ids": other_ids,
        "lineage": lineage, "feature_type_source": ftype, "row_kind": kind,
        "cluster_count": cluster, "coord_printed": grid, "crs_printed": crs if grid else "",
        "precision_m": prec, "coord_basis": cbasis if grid else "", "where_described": where,
        "n_openings": n_open, "openings_basis": open_basis, "opening_facings": facings,
        "facing_basis": facing_basis, "facing_resolution": res, "north_case": north_case,
        "pillar": pillar, "pillar_kind": pillar_kind, "pillar_position": pillar_pos,
        "pillar_basis": pillar_basis, "terrace": terrace, "terrace_basis": terrace_basis,
        "northern_member": north, "northern_basis": north_basis, "published_plan": plan,
        "period_stated": period, "period_in_window": piw, "excavation_status": exc, "finds": finds,
        "exposure": exposure, "first_read_utc": read, "c1_override": c1, "coord_ok": coord_ok, "notes": notes,
    })


def X(excl, record_id, *, num, src, ftype, reason, grid="", crs="OIG", exposure="unexposed-at-freeze",
      read="", notes=""):
    excl.append({"record_id": record_id, "name_number": num, "source_records": src,
                 "feature_type_source": ftype, "coord_printed": grid, "crs_printed": crs if grid else "",
                 "reason": reason, "exposure": exposure, "first_read_utc": read, "notes": notes})
