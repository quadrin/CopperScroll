"""Shared helpers for the ASI Jerusalem-area build (standard library plus pyproj).

All rules come from ../plan.json. Nothing here changes the plan.
"""
import csv
import hashlib
import html
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(FOLDER, '..', '..', '..'))
PLAN_PATH = os.path.join(FOLDER, 'plan.json')

R_EARTH_KM = 6371.0088  # W2B scripts/grid_convert.py km()


def load_plan():
    with open(PLAN_PATH, encoding='utf-8') as f:
        return json.load(f)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R_EARTH_KM * math.asin(math.sqrt(a))


def rect_km(lat, lon, lat_lo, lat_hi, lon_lo, lon_hi):
    """Haversine distance from a point to the nearest point of a lat/lon rectangle."""
    clat = min(max(lat, lat_lo), lat_hi)
    clon = min(max(lon, lon_lo), lon_hi)
    return km(lat, lon, clat, clon)


def load_places(plan):
    path = os.path.join(REPO, plan['inputs']['places']['path'])
    placeable, not_placeable = [], []
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                lat, lon = float(r['lat']), float(r['lon'])
            except (TypeError, ValueError):
                not_placeable.append(r)
                continue
            r = dict(r)
            r['lat_f'], r['lon_f'] = lat, lon
            placeable.append(r)
    return placeable, not_placeable


def sheets_from_grid(grid):
    """map id (str) -> dict(lat_lo, lat_hi, lon_lo, lon_hi, map_num, label)."""
    out = {}
    for ft in grid['features']:
        props = ft.get('properties') or {}
        mid = str(props.get('itemid', '')).strip()
        geom = ft.get('geometry') or {}
        if not mid or geom.get('type') != 'Polygon':
            continue
        pts = geom['coordinates'][0]
        lons = [p[0] for p in pts]
        lats = [p[1] for p in pts]
        out[mid] = dict(lat_lo=min(lats), lat_hi=max(lats), lon_lo=min(lons), lon_hi=max(lons),
                        map_num=str(props.get('name', '')).strip(), label=props.get('infoContent', ''))
    return out


# ---------------------------------------------------------------- text helpers
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')


def clean(text):
    if text is None:
        return ''
    t = TAG.sub(' ', str(text))
    t = html.unescape(t)
    t = t.replace(' ', ' ')
    return WS.sub(' ', t).strip()


def words(text):
    return text.split()


def quote_window(text, start_char, before=4, n=12):
    """Verbatim window of at most n words that starts up to `before` words before start_char."""
    toks = list(re.finditer(r'\S+', text))
    if not toks:
        return ''
    idx = 0
    for i, m in enumerate(toks):
        if m.end() > start_char:
            idx = i
            break
    else:
        idx = len(toks) - 1
    s = max(0, idx - before)
    return ' '.join(m.group(0) for m in toks[s:s + n])


def first_words(text, n=12):
    return ' '.join(words(text)[:n])


def split_sentences(text):
    """Return list of (start, end) spans. Split at '. ', '! ', '? ' or end of text."""
    spans, start = [], 0
    for m in re.finditer(r'[.!?](?=\s)', text):
        spans.append((start, m.end()))
        start = m.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


# ---------------------------------------------------------------- site record parsing
ROW = re.compile(r'<tr>\s*<td>\s*<b>(.*?)</b>\s*</td>\s*<td>(.*?)</td>\s*</tr>', re.S | re.I)
BLOCK = re.compile(r'<b>\s*(Description|Bibliography)\s*</b>\s*<br\s*/?>\s*(.*?)(?=<!--|<hr|<b>\s*(?:Description|Bibliography)\s*</b>|$)',
                   re.S | re.I)


def parse_site_desc(d):
    """Parse the GetSiteDesc2 'd' object into a flat dict of cleaned fields."""
    content = d.get('content') or ''
    fields = {}
    for k, v in ROW.findall(content):
        key = clean(k).rstrip(':').strip()
        fields[key] = clean(v)
    for k, v in BLOCK.findall(content):
        fields[k.strip().title()] = clean(v)
    loc = d.get('location') or {}
    fields['_loc_lat'] = loc.get('X')
    fields['_loc_lon'] = loc.get('Y')
    fields['_name'] = clean(d.get('name'))
    return fields


def parse_grid_pair(s):
    nums = re.findall(r'\d+(?:\.\d+)?', s or '')
    if len(nums) != 2:
        return None
    a, b = float(nums[0]), float(nums[1])
    n, e = (a, b) if a > b else (b, a)
    return e, n


def parse_wgs_pair(s):
    nums = re.findall(r'-?\d+(?:\.\d+)?', s or '')
    if len(nums) != 2:
        return None
    return float(nums[0]), float(nums[1])


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
