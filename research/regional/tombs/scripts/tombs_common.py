"""Shared helpers for the regional tomb inventory (standard library; pyproj for WBADB grid values).

Every rule comes from the JSON block of ../PLAN.md (frozen in commit cd394d7). Nothing here changes it.
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
PLAN_MD = os.path.join(FOLDER, 'PLAN.md')
PLAN_SHA256 = '206a4e1430da2939bdc7e66b3c540f6ed068118c94c366fb5c8073c2564b229d'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def load_plan(check=True):
    if check:
        got = sha256_file(PLAN_MD)
        if got != PLAN_SHA256:
            raise SystemExit(f'PLAN.md hash {got} differs from the frozen {PLAN_SHA256}')
    with open(PLAN_MD, encoding='utf-8') as f:
        s = f.read()
    m = re.search(r'```json\n(.*?)\n```', s, re.S)
    return json.loads(m.group(1))


# ---------------------------------------------------------------- geometry (EPSG:4326, haversine)
def km(lat1, lon1, lat2, lon2, r=6371.0088):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(min(1.0, a)))


def seg_km(lat, lon, a, b, r=6371.0088):
    """Distance from (lat, lon) to the segment a-b, on a local equirectangular projection
    centred on the segment midpoint (PLAN §2)."""
    lat0 = math.radians((a[0] + b[0]) / 2)

    def xy(p_lat, p_lon):
        return (math.radians(p_lon) * math.cos(lat0) * r, math.radians(p_lat) * r)
    ax, ay = xy(*a)
    bx, by = xy(*b)
    px, py = xy(lat, lon)
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def rect_km(lat, lon, lat_lo, lat_hi, lon_lo, lon_hi):
    clat = min(max(lat, lat_lo), lat_hi)
    clon = min(max(lon, lon_lo), lon_hi)
    return km(lat, lon, clat, clon)


def region_flags(plan, lat, lon):
    P = plan['points']
    R = plan['regions']
    dA = km(lat, lon, *P['jer_temple'])
    dB1 = min(km(lat, lon, *P['tell_es_sultan']), km(lat, lon, *P['jericho_palaces']))
    dB2 = seg_km(lat, lon, P['jericho_palaces'], P['kh_qumran'])
    return dict(
        d_temple_km=dA, d_jericho_km=dB1, d_road_km=dB2,
        in_A=dA <= R['A_radius_km'], in_A3=dA <= R['A_sensitivity_radius_km'],
        in_B1=dB1 <= R['B1_radius_km'], in_B2=dB2 <= R['B2_halfwidth_km'],
        in_B2_5=dB2 <= R['B2_sensitivity_halfwidth_km'],
    )


def in_any_region(f, sensitivity=False):
    return f['in_A'] or f['in_B1'] or (f['in_B2_5'] if sensitivity else f['in_B2'])


def loc_clause(d, tol, unc):
    """yes / no / unknown for 'within tol km', unknown when the tolerance lies inside the uncertainty."""
    if abs(d - tol) <= unc:
        return 'unknown'
    return 'yes' if d <= tol else 'no'


# ---------------------------------------------------------------- text
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')


def clean(text):
    if text is None:
        return ''
    t = TAG.sub(' ', str(text))
    t = html.unescape(t).replace('\xa0', ' ')
    return WS.sub(' ', t).strip()


def sentences(text):
    out, start = [], 0
    for m in re.finditer(r'[.!?](?=\s)', text):
        out.append(text[start:m.end()].strip())
        start = m.end()
    if start < len(text):
        out.append(text[start:].strip())
    return [s for s in out if s]


def term_regex(terms):
    """Whole words, any case, plurals allowed (PLAN §5)."""
    alts = sorted({t for t in terms}, key=len, reverse=True)
    pats = [re.escape(t).replace(r'\ ', r'[\s\-]+') for t in alts]
    return re.compile(r'(?<![\w])(' + '|'.join(pats) + r')(?:e?s)?(?![\w])', re.IGNORECASE)


def find_terms(rx, text):
    return [m.group(1) for m in rx.finditer(text)]


def period_classes(plan, text):
    """Return (window, partly, outside) label lists found in text, longest label first and masking
    the shorter labels inside it (PLAN §4)."""
    labels = ([(l, 'window') for l in plan['period_window']] + [(l, 'partly') for l in plan['period_partly']]
              + [(l, 'outside') for l in plan['period_outside']])
    labels.sort(key=lambda x: len(x[0]), reverse=True)
    masked = text
    found = {'window': [], 'partly': [], 'outside': []}
    for lab, cls in labels:
        rx = re.compile(r'(?<![\w])' + re.escape(lab).replace(r'\ ', r'[\s\-]+') + r'(?![\w])', re.IGNORECASE)
        for m in list(rx.finditer(masked)):
            found[cls].append(m.group(0))
        masked = rx.sub(lambda m: '#' * len(m.group(0)), masked)
    return found['window'], found['partly'], found['outside']


def norm_name(s):
    s = clean(s).lower()
    s = re.sub(r"[ʿʾ'`’‘]", '', s)
    s = re.sub(r'\b(h|kh|khirbet|khirbat|horbat|hurvat|el|al|ed|es|en|er|ez|et|the|of|tomb|tombs|cave|caves|burial)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)
