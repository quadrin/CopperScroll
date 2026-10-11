"""Shared helpers for the columbaria lane (standard library; pyproj only for WBADB grid points).

Every rule comes from ../PLAN.md (frozen 2026-10-11T04:06:45Z, commit afdd69f). Nothing here changes it.
"""
import hashlib
import html
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(FOLDER, '..', '..', '..'))
TERMS_PATH = os.path.join(HERE, 'terms.json')
R_EARTH_KM = 6371.0088  # as in research/regional/asi_jerusalem/scripts/asi_common.py

HEB = 'א-ת'


def load_terms():
    with open(TERMS_PATH, encoding='utf-8') as f:
        return json.load(f)


TERMS = load_terms()
POLY = [tuple(p) for p in TERMS['region_polygon_lonlat_wgs84']]


def in_region(lon, lat):
    """Ray-casting test on decimal degrees (PLAN §3)."""
    if lon is None or lat is None:
        return False
    inside = False
    n = len(POLY)
    for i in range(n):
        x1, y1 = POLY[i]
        x2, y2 = POLY[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            xi = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
            if lon < xi:
                inside = not inside
    return inside


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R_EARTH_KM * math.asin(math.sqrt(a))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _he(pat):
    pre = TERMS['hebrew_prefix']
    return re.compile(f'(?<![{HEB}]){pre}(?:{pat})(?![{HEB}])')


def _en(pat):
    return re.compile(pat, re.IGNORECASE)


COL_EN = [_en(p) for p in TERMS['columbarium_en']]
COL_HE = [_he(p) for p in TERMS['columbarium_he']]
FLAGS = {k: ([_en(p) for p in v['en']], [_he(p) for p in v['he']]) for k, v in TERMS['flags'].items()}


def find_columbarium(text):
    """Return the list of matched columbarium terms (in order of appearance)."""
    if not text:
        return []
    hits = []
    for rx in COL_EN + COL_HE:
        for m in rx.finditer(text):
            hits.append((m.start(), m.group(0)))
    return [h for _, h in sorted(hits)]


def flag_hits(text):
    out = {}
    for k, (en, he) in FLAGS.items():
        terms = []
        for rx in en + he:
            terms += [m.group(0) for m in rx.finditer(text or '')]
        if terms:
            out[k] = sorted(set(t.strip().lower() for t in terms))
    return out


TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')


def clean(text):
    if text is None:
        return ''
    t = TAG.sub(' ', str(text))
    t = html.unescape(t).replace(' ', ' ')
    return WS.sub(' ', t).strip()


def geojson_props(feature):
    props = feature.get('properties')
    if isinstance(props, list):
        return {p.get('key'): p.get('value') for p in props}
    return dict(props or {})


def cache_name(endpoint, **params):
    parts = [endpoint.replace('/', '_').replace('.aspx', '')]
    for k in sorted(params):
        parts.append(f'{k}-{params[k]}')
    return re.sub(r'[^A-Za-z0-9_.-]', '_', '__'.join(parts)) + '.json'


def sheets_in_region(grid, online):
    """Map ids (str) of online maps whose sheet rectangle touches the polygon (11 x 11 sample grid)."""
    out = []
    for ft in grid['features']:
        p = ft.get('properties') or {}
        mid = str(p.get('itemid', '')).strip()
        geom = ft.get('geometry') or {}
        if not mid or geom.get('type') != 'Polygon' or mid not in online:
            continue
        pts = geom['coordinates'][0]
        lons = [q[0] for q in pts]
        lats = [q[1] for q in pts]
        hit = any(in_region(min(lons) + (max(lons) - min(lons)) * i / 10,
                            min(lats) + (max(lats) - min(lats)) * j / 10)
                  for i in range(11) for j in range(11))
        if hit:
            out.append((mid, str(p.get('name', '')).strip()))
    return sorted(out, key=lambda t: int(t[0]))
