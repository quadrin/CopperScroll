"""Lane J: build the unified feature table and the entry x feature eligibility table.

Eligibility uses ONLY feature class and location (distance to an entry's candidate place).
No date field (dated_in_window, period_in_window, date_code, candidate_entries) is read.
"""
import math
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
J = Path(__file__).resolve().parents[1]
RADIUS_KM = 2.0

# Zone boxes of the HA-ESI phase-2 plan (research/regional/haesi_features/phase2_2026-10-10/PLAN.md §2), first match wins
ZONES = [
    ("Z1_GERIZIM", [(32.14, 32.26, 35.19, 35.37)]),
    ("Z2_JORDAN_VALLEY", [(31.76, 32.06, 35.40, 35.60)]),
    ("Z4_JERUSALEM_HILLS", [(31.62, 31.90, 35.10, 35.27)]),
    ("Z3_JUDEAN_DESERT", [(31.20, 31.92, 35.27, 35.60), (31.92, 32.06, 35.30, 35.60)]),
]

HAESI_CLASS = {"cistern": "cistern", "pool_reservoir": "pool_reservoir", "channel_aqueduct": "channel_aqueduct",
               "dam": "dam", "ritual_bath": "steps_ritual_bath", "cave_with_finds": "cave",
               "tomb_burial_cave": "tomb", "columbarium_dovecote": "dovecote",
               "rockcut_installation": "rockcut"}  # hoard_cache, wall_tower: not installations of the list's landmark kinds
ASI_CLASS = {"cistern": "cistern", "pool": "pool_reservoir", "reservoir": "pool_reservoir", "basin": "pool_reservoir",
             "conduit": "channel_aqueduct", "steps": "steps_ritual_bath", "cave": "cave", "tomb": "tomb",
             "monument": "tomb", "dovecote": "dovecote", "rock_cut": "rockcut", "pit": "rockcut",
             "installation": "rockcut", "winepress": "rockcut", "oil_press": "rockcut", "quarry": "rockcut",
             "fortress": "fortress"}
# Entry landmark word (entry_features.csv) -> unified classes. Words naming no built installation are not used.
LANDMARK_CLASS = {"cistern": ["cistern"], "pool": ["pool_reservoir"], "reservoir": ["pool_reservoir"],
                  "basin": ["pool_reservoir"], "conduit": ["channel_aqueduct", "dam"], "outlet": ["channel_aqueduct", "dam"],
                  "tomb": ["tomb"], "monument": ["tomb"], "cave": ["cave"], "dovecote": ["dovecote"],
                  "steps": ["steps_ritual_bath"], "pit": ["cistern", "rockcut"], "chamber": ["rockcut"],
                  "fortress": ["fortress"]}


def norm(s):
    return " ".join(str(s).split()) if isinstance(s, str) else ""


def zone_of(lat, lon):
    if lat is None or (isinstance(lat, float) and math.isnan(lat)):
        return ""
    for z, boxes in ZONES:
        for a, b, c, d in boxes:
            if a <= lat <= b and c <= lon <= d:
                return z
    return "OUT"


def hav(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def build():
    rows = []
    h = pd.read_csv(REPO / "research/regional/haesi_features/merged_2026-10-12/features_all.csv", dtype=str)
    h = h[h.version_role != "alternate"]  # one version per report (merge rule §4.4); not a date rule
    for r in h.itertuples():
        cls = HAESI_CLASS.get(r.feature_type)
        if not cls:
            continue
        lat = float(r.lat) if isinstance(r.lat, str) else np.nan
        lon = float(r.lon) if isinstance(r.lon, str) else np.nan
        z = r.count_zone if isinstance(r.count_zone, str) and r.count_zone.startswith("Z") and "|" not in r.count_zone else ""
        if not z and not np.isnan(lat):
            z = zone_of(lat, lon)
        name_place = r.nearest_place if (np.isnan(lat) and isinstance(r.nearest_place, str)) else ""
        rows.append(dict(fid="H:" + r.row_uid, inventory="HAESI", cls=cls, lat=lat, lon=lon, zone=z or "UNZONED",
                         name_place=name_place, period_text=norm(r.period_as_given)))
    a = pd.read_csv(REPO / "research/regional/asi_jerusalem/features.csv", dtype=str)
    for i, r in enumerate(a.itertuples()):
        cls = ASI_CLASS.get(r.feature_class)
        if not cls:
            continue
        lat, lon = float(r.lat), float(r.lon)
        rows.append(dict(fid=f"A:{r.record_id}:{r.feature_class}", inventory="ASI", cls=cls, lat=lat, lon=lon,
                         zone=zone_of(lat, lon), name_place="", period_text=norm(r.period_as_given)))
    c = pd.read_csv(REPO / "research/regional/caves_entry25/caves.csv", dtype=str)
    for r in c.itertuples():
        lat = float(r.lat) if isinstance(r.lat, str) else np.nan
        lon = float(r.lon) if isinstance(r.lon, str) else np.nan
        rows.append(dict(fid="C:" + r.cave_id, inventory="CAVES", cls="cave", lat=lat, lon=lon,
                         zone=zone_of(lat, lon) or "Z3_JUDEAN_DESERT", name_place="", period_text=norm(r.period_stated)))
    k = pd.read_csv(REPO / "research/regional/columbaria/columbaria.csv", dtype=str)
    for r in k.itertuples():
        lat = float(r.lat) if isinstance(r.lat, str) else np.nan
        lon = float(r.lon) if isinstance(r.lon, str) else np.nan
        rows.append(dict(fid="K:" + r.id, inventory="COLUMB", cls="dovecote", lat=lat, lon=lon,
                         zone=zone_of(lat, lon) or "UNZONED", name_place="", period_text=norm(r.date_text)))
    f = pd.DataFrame(rows)
    assert f.fid.is_unique, f[f.fid.duplicated()].fid.head()
    s = pd.read_csv(J / "period_coding/strings.csv", dtype=str)
    f = f.merge(s.rename(columns={"text": "period_text"}), on="period_text", how="left")
    f["stratum"] = f.cls + "|" + f.zone
    f.to_csv(J / "data/features_unified.csv", index=False)

    # eligibility
    e = pd.read_csv(REPO / "research/agent_review_2026-10-07/wave1/T02_hoard_match/entry_features.csv", dtype=str)
    p = pd.read_csv(REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv", dtype=str)
    p = p[p.lat.notna()]
    pl = {r.place_id: (float(r.lat), float(r.lon)) for r in p.itertuples()}
    el = []
    for r in e.itertuples():
        lms = [w for w in str(r.landmarks).split(";") if w in LANDMARK_CLASS]
        classes = sorted({c for w in lms for c in LANDMARK_CLASS[w]})
        places = [q for q in str(r.candidate_places).split(";") if q in pl]
        if not classes or not places:
            continue
        sub = f[f.cls.isin(classes)]
        hit = np.zeros(len(sub), bool)
        for q in places:
            la, lo = pl[q]
            d = hav(sub.lat.values, sub.lon.values, la, lo)
            hit |= (np.nan_to_num(d, nan=1e9) <= RADIUS_KM) | (sub.name_place.values == q)
        for fid in sub.fid.values[hit]:
            el.append(dict(entry=r.entry, fid=fid))
    el = pd.DataFrame(el)
    el.to_csv(J / "data/eligibility.csv", index=False)
    print("features", len(f), "unmatched strings", f.sid.isna().sum() - (f.period_text == "").sum())
    print(f.inventory.value_counts().to_dict()); print(f.zone.value_counts().to_dict())
    print("entries with >=1 eligible feature", el.entry.nunique(), "pairs", len(el))


if __name__ == "__main__":
    build()
