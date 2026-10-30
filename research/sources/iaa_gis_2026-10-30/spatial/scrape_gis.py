"""Scrape the IAA public GIS layers into a place-keyed spatial register.

Usage:
    python3 scrape_gis.py [--places data/places.csv] [--radius 3000]

Layers (public ArcGIS services behind discover.iaa.org.il, read with the
public app key served at /api/config/gis.js):

  CaveAtlas                151 Judean Desert cave points (ITM grid, elevation,
                           excavated flag). Includes the Copper Scroll Cave Q3.
  MegilaSurveyPoints        83 "Operation Scroll" (1993) cave-survey points,
                           cave series X, XI, XII around Qumran.
  SURVEY_MAPS_SITE_POINTS_PUBLIC
                           23,312 Archaeological Survey of Israel site points
                           with period, remains, description and bibliography.
  HACRAZOT_PUBLIC1         31,594 declared antiquities sites with polygons and
                           short descriptions. Israel-side coverage only.

Outputs are written to data/. Standard library only; deterministic ordering.
"""
import argparse
import csv
import json
import math
import pathlib
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
ORG = "https://services1.arcgis.com/SzLu0BtKF8WSi3ll/arcgis/rest/services"
GIS_CONFIG = "https://discover.iaa.org.il/api/config/gis.js"
USER_AGENT = "Mozilla/5.0 (compatible; CopperScroll research intake)"
PAGE = 1000


def get_token():
    req = urllib.request.Request(GIS_CONFIG, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        js = r.read().decode("utf-8", "ignore")
    m = re.search(r"esriApiKey:\s*'([^']+)'", js)
    if not m:
        raise RuntimeError("no esriApiKey in gis.js")
    return m.group(1)


def post(url, params, timeout=180):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        url, data=data, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def layer_info(service, layer, token):
    url = f"{ORG}/{urllib.parse.quote(service)}/FeatureServer/{layer}"
    d = post(url, {"f": "json", "token": token})
    if "error" in d:
        raise RuntimeError(f"{service}: {d['error']}")
    count = post(
        url + "/query",
        {"f": "json", "token": token, "where": "1=1", "returnCountOnly": "true"},
    ).get("count")
    return {
        "service": service,
        "layer": layer,
        "name": d.get("name"),
        "geometryType": d.get("geometryType"),
        "fields": [f["name"] for f in d.get("fields", [])],
        "spatialReference": (d.get("extent") or {}).get("spatialReference"),
        "count": count,
    }


def query(service, layer, token, where="1=1", envelope=None, out_fields="*",
          geometry=True, extra=None, oid="OBJECTID"):
    """Fetch every matching feature, paging past the service record limit."""
    url = f"{ORG}/{urllib.parse.quote(service)}/FeatureServer/{layer}/query"
    out = []
    offset = 0
    while True:
        p = {
            "f": "json",
            "token": token,
            "where": where,
            "outFields": out_fields,
            "returnGeometry": "true" if geometry else "false",
            "outSR": "4326",
            "resultOffset": str(offset),
            "resultRecordCount": str(PAGE),
            "orderByFields": oid,
        }
        if envelope:
            p["geometry"] = json.dumps(envelope)
            p["geometryType"] = "esriGeometryEnvelope"
            p["inSR"] = "4326"
            p["spatialRel"] = "esriSpatialRelIntersects"
        if extra:
            p.update(extra)
        d = post(url, p)
        if "error" in d:
            raise RuntimeError(f"{service} offset {offset}: {d['error']}")
        feats = d.get("features", [])
        out.extend(feats)
        if len(feats) < PAGE:
            break
        offset += PAGE
    return out


def envelope(lat, lon, metres):
    dlat = metres / 111_320.0
    dlon = metres / (111_320.0 * math.cos(math.radians(lat)))
    return {
        "xmin": lon - dlon,
        "ymin": lat - dlat,
        "xmax": lon + dlon,
        "ymax": lat + dlat,
        "spatialReference": {"wkid": 4326},
    }


def haversine(lat1, lon1, lat2, lon2):
    r = 6_371_008.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def clean(text):
    if not text:
        return ""
    text = text.replace("&nbsp;", " ").replace("&mdash;", "—")
    text = TAG.sub(" ", text)
    return WS.sub(" ", text).strip()


def centroid(geom):
    """Area-weighted centroid of the first ring; fall back to vertex mean."""
    if not geom:
        return None, None
    if "x" in geom and "y" in geom:
        return geom["y"], geom["x"]
    rings = geom.get("rings") or []
    if not rings:
        return None, None
    ring = rings[0]
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        cross = x1 * y2 - x2 * y1
        a += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    if abs(a) < 1e-12:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return sum(ys) / len(ys), sum(xs) / len(xs)
    a *= 0.5
    return cy / (6 * a), cx / (6 * a)


def point_geom(feat):
    g = feat.get("geometry") or {}
    if "x" in g and "y" in g:
        return g["y"], g["x"]
    return centroid(g)


def load_places(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["_lat"] = float(r["lat"]) if r.get("lat") else None
            r["_lon"] = float(r["lon"]) if r.get("lon") else None
            rows.append(r)
    return rows


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def nearest(lat, lon, places, radius=3000):
    """Return (nearest place id, its distance, ids of every place within radius)."""
    best = None
    within = []
    for p in places:
        if p["_lat"] is None:
            continue
        d = haversine(lat, lon, p["_lat"], p["_lon"])
        if d <= radius:
            within.append(p["place_id"])
        if best is None or d < best[1]:
            best = (p["place_id"], d)
    return best[0], best[1], sorted(within)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--places", default=str(ROOT / "data/places.csv"))
    ap.add_argument("--radius", type=int, default=3000)
    ap.add_argument("--out", default=str(ROOT / "data"))
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    places = load_places(args.places)
    located = [p for p in places if p["_lat"] is not None]
    token = get_token()

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "token_source": GIS_CONFIG,
        "radius_m": args.radius,
        "places_file": str(pathlib.Path(args.places).name),
        "places_total": len(places),
        "places_located": len(located),
        "layers": {},
    }

    # --- whole-layer registries -------------------------------------------
    print("CaveAtlas ...", flush=True)
    info = layer_info("CaveAtlas", 0, token)
    caves = query("CaveAtlas", 0, token)
    manifest["layers"]["CaveAtlas"] = info
    cave_rows = []
    for f in caves:
        a = f["attributes"]
        lat, lon = point_geom(f)
        n = nearest(lat, lon, located, args.radius)
        cave_rows.append({
            "objectid": a.get("OBJECTID"),
            "name_heb": (a.get("מערה") or "").strip(),
            "itm_x": a.get("X"),
            "itm_y": a.get("Y"),
            "elevation_m": a.get("רום"),
            "excavated": (a.get("נחפר") or "").strip(),
            "source": (a.get("מקור") or "").strip(),
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "nearest_place": n[0],
            "dist_m": round(n[1]),
            "places_within_radius": ";".join(n[2]),
        })
    cave_rows.sort(key=lambda r: (r["dist_m"] if r["dist_m"] != "" else 9e9, r["name_heb"]))
    write_csv(out / "cave_atlas.csv", list(cave_rows[0].keys()), cave_rows)

    print("MegilaSurveyPoints ...", flush=True)
    info = layer_info("MegilaSurveyPoints", 0, token)
    meg = query("MegilaSurveyPoints", 0, token, oid="FID")
    manifest["layers"]["MegilaSurveyPoints"] = info
    meg_rows = []
    for f in meg:
        a = f["attributes"]
        lat, lon = point_geom(f)
        n = nearest(lat, lon, located, args.radius)
        meg_rows.append({
            "fid": a.get("FID"),
            "cave_no": (a.get("מערה") or "").strip(),
            "cave_type": (a.get("סוג_ה") or "").strip(),
            "excavated": a.get("חפירה"),
            "itm_x": a.get("X"),
            "itm_y": a.get("Y"),
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "nearest_place": n[0],
            "dist_m": round(n[1]),
            "places_within_radius": ";".join(n[2]),
        })
    meg_rows.sort(key=lambda r: (r["dist_m"] if r["dist_m"] != "" else 9e9, r["cave_no"]))
    write_csv(out / "megila_survey_points.csv", list(meg_rows[0].keys()), meg_rows)

    # --- windowed ASI survey sites ----------------------------------------
    print("ASI survey sites ...", flush=True)
    asi_info = layer_info("SURVEY_MAPS_SITE_POINTS_PUBLIC", 0, token)
    manifest["layers"]["SURVEY_MAPS_SITE_POINTS_PUBLIC"] = asi_info
    asi = {}
    for p in located:
        feats = query(
            "SURVEY_MAPS_SITE_POINTS_PUBLIC", 0, token,
            envelope=envelope(p["_lat"], p["_lon"], args.radius),
        )
        for f in feats:
            lat, lon = point_geom(f)
            d = haversine(p["_lat"], p["_lon"], lat, lon)
            if d > args.radius:
                continue
            key = f["attributes"].get("OBJECTID")
            rec = asi.setdefault(key, {"attrs": f["attributes"], "lat": lat, "lon": lon, "hits": {}})
            rec["hits"][p["place_id"]] = min(rec["hits"].get(p["place_id"], 9e9), d)
        print(f"  {p['place_id']:24s} cumulative {len(asi)}", flush=True)

    asi_rows = []
    for key, rec in asi.items():
        a = rec["attrs"]
        n = min(rec["hits"].items(), key=lambda kv: kv[1])
        asi_rows.append({
            "objectid": key,
            "site_num": a.get("SITE_NUM"),
            "field_num": (a.get("FIELD_NUM") or "").strip(),
            "map_id": a.get("MAP_ID"),
            "name_en": (a.get("NAME_EN") or "").strip(),
            "name_heb": (a.get("NAME_HEB") or "").strip(),
            "additional_name_en": (a.get("ADDITIONAL_NAME_EN") or "").strip(),
            "additional_name_heb": (a.get("ADDITIONAL_NAME_HEB") or "").strip(),
            "period_en": (a.get("PERIOD_EN") or "").strip(),
            "period_heb": (a.get("PERIOD_HEB") or "").strip(),
            "remains_en": (a.get("REMAINS_EN") or "").strip(),
            "remains_heb": (a.get("REMAINS_HEB") or "").strip(),
            "authors_en": clean(a.get("AUTHORS_EN")),
            "bibliography_en": clean(a.get("BIBLIOGRAPHY_EN")),
            "bibliography_heb": clean(a.get("BIBLIOGRAPHY_HEB")),
            "description_en": clean(a.get("DESCRIPTION_EN")),
            "description_heb": clean(a.get("DESCRIPTION_HEB")),
            "lat": round(rec["lat"], 6),
            "lon": round(rec["lon"], 6),
            "itm_x": a.get("X_NEW"),
            "itm_y": a.get("Y_NEW"),
            "palestine_grid_x": a.get("X_OLD"),
            "palestine_grid_y": a.get("Y_OLD"),
            "nearest_place": n[0],
            "dist_m": round(n[1]),
            "places_within_radius": ";".join(sorted(rec["hits"])),
        })
    asi_rows.sort(key=lambda r: (r["nearest_place"], r["dist_m"]))
    write_csv(out / "asi_sites.csv", list(asi_rows[0].keys()), asi_rows)

    # --- windowed declared sites (with polygons) --------------------------
    print("Declared sites ...", flush=True)
    dec_info = layer_info("HACRAZOT_PUBLIC1", 0, token)
    manifest["layers"]["HACRAZOT_PUBLIC1"] = dec_info
    dec = {}
    for p in located:
        feats = query(
            "HACRAZOT_PUBLIC1", 0, token,
            out_fields="objectid,atar_number,meh_id,mehoz_name,ata_shem,atar_eng_desc,atar_heb_desc",
            envelope=envelope(p["_lat"], p["_lon"], args.radius),
        )
        for f in feats:
            lat, lon = point_geom(f)
            d = haversine(p["_lat"], p["_lon"], lat, lon)
            if d > args.radius:
                continue
            key = f["attributes"].get("objectid")
            rec = dec.setdefault(key, {"attrs": f["attributes"], "geom": f.get("geometry"),
                                       "lat": lat, "lon": lon, "hits": {}})
            rec["hits"][p["place_id"]] = min(rec["hits"].get(p["place_id"], 9e9), d)
        print(f"  {p['place_id']:24s} cumulative {len(dec)}", flush=True)

    dec_rows = []
    features = []
    for key, rec in dec.items():
        a = rec["attrs"]
        n = min(rec["hits"].items(), key=lambda kv: kv[1])
        dec_rows.append({
            "objectid": key,
            "atar_number": a.get("atar_number"),
            "meh_id": a.get("meh_id"),
            "mehoz_name": a.get("mehoz_name"),
            "name_heb": (a.get("ata_shem") or "").strip(),
            "description_heb": clean(a.get("atar_heb_desc")),
            "description_en": clean(a.get("atar_eng_desc")),
            "lat": round(rec["lat"], 6),
            "lon": round(rec["lon"], 6),
            "nearest_place": n[0],
            "dist_m": round(n[1]),
            "places_within_radius": ";".join(sorted(rec["hits"])),
        })
        if rec["geom"]:
            rings = rec["geom"].get("rings") or []
            if not rings:
                continue
            geometry = ({"type": "Polygon", "coordinates": [rings[0]]}
                        if len(rings) == 1
                        else {"type": "MultiPolygon", "coordinates": [[r] for r in rings]})
            features.append({
                "type": "Feature",
                "properties": {
                    "objectid": key,
                    "atar_number": a.get("atar_number"),
                    "name_heb": (a.get("ata_shem") or "").strip(),
                    "nearest_place": n[0],
                    "dist_m": round(n[1]),
                },
                "geometry": geometry,
            })
    dec_rows.sort(key=lambda r: (r["nearest_place"], r["dist_m"]))
    write_csv(out / "declared_sites.csv", list(dec_rows[0].keys()), dec_rows)
    with open(out / "declared_sites.geojson", "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection",
                   "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                   "features": features}, fh, ensure_ascii=False)

    # --- per-place coverage ----------------------------------------------
    print("Place coverage ...", flush=True)
    cov = []
    for p in places:
        if p["_lat"] is None:
            cov.append({
                "place_id": p["place_id"], "name": p["name"], "lat": "", "lon": "",
                "map_group": p.get("map_group", ""),
                "asi_1km": "", "asi_3km": "", "declared_1km": "", "declared_3km": "",
                "caves_3km": "", "megila_3km": "", "declared_layer": "not assessed",
            })
            continue
        lat, lon = p["_lat"], p["_lon"]

        def tally(rows, radius):
            return sum(1 for r in rows
                       if r["lat"] != "" and haversine(lat, lon, float(r["lat"]), float(r["lon"])) <= radius)

        d1 = tally(dec_rows, 1000)
        d3 = tally(dec_rows, 3000)
        cov.append({
            "place_id": p["place_id"],
            "name": p["name"],
            "lat": lat,
            "lon": lon,
            "map_group": p.get("map_group", ""),
            "asi_1km": tally(asi_rows, 1000),
            "asi_3km": tally(asi_rows, 3000),
            "declared_1km": d1,
            "declared_3km": d3,
            "caves_3km": tally(cave_rows, 3000),
            "megila_3km": tally(meg_rows, 3000),
            "declared_layer": "present" if d3 else "no polygon within 3 km",
        })
    cov.sort(key=lambda r: (r["map_group"], r["place_id"]))
    write_csv(out / "place_coverage.csv", list(cov[0].keys()), cov)

    manifest["outputs"] = {
        "cave_atlas.csv": len(cave_rows),
        "megila_survey_points.csv": len(meg_rows),
        "asi_sites.csv": len(asi_rows),
        "declared_sites.csv": len(dec_rows),
        "declared_sites.geojson": len(features),
        "place_coverage.csv": len(cov),
    }
    with open(out / "manifest.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    print(json.dumps(manifest["outputs"], indent=2))


if __name__ == "__main__":
    main()
