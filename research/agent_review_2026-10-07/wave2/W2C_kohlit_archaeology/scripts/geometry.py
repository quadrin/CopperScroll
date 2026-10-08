#!/usr/bin/env python3
"""Distances and bearings between Kohlit-candidate features.

Inputs are coordinates copied from published sources (see 'src').
Old Israel Grid values (WBADB) are metres on a Cassini grid; for the short
distances here (<3 km) planar differences are adequate (error << 1%).
Lat/lon values (Nigro 2011 catalogue) are converted with a local
equirectangular approximation.
Run: python3 -I geometry.py  -> writes ../data/geometry.csv
"""
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'geometry.csv')

def dms(d, m, s):
    return d + m / 60 + s / 3600

# --- Jericho: lat/lon from Nigro 2011 (ROSAPAT 07) catalogue
LL = {
    'Tell es-Sultan (centroid point)': (dms(31,52,15.99), dms(35,26,39.32), 'Nigro 2011 p.146 (cat. 85)'),
    "'Ain es-Sultan (spring)": (dms(31,52,13.23), dms(35,26,41.48), 'Nigro 2011 p.110 (cat. 21)'),
    'Mughr el-Maqrabanna (Hachlili cemetery point)': (dms(31,52,13.87), dms(35,26,15.64), 'Nigro 2011 p.131 (cat. 61)'),
    'Tell es-Samarat (hippodrome)': (dms(31,51,52.50), dms(35,26,22.01), 'Nigro 2011 p.144 (cat. 82)'),
    'Suwwanet eth-Thaniya (Early Roman house, 1997)': (dms(31,52,54.88), dms(35,27,23.24), 'Nigro 2011 p.154 (cat. 90)'),
}
# --- Old Israel Grid (WBADB = Greenberg & Keinan 2009 gazetteer)
GRID = {
    'Tell es-Sultan [WBADB 328]': (192150, 142050, 'WBADB p.68-69 no.328'),
    'Jericho Cemetery (Hachlili) [WBADB 343]': (190900, 141050, 'WBADB p.70 no.343'),
    'Kh. Marjame (tell) [WBADB 213]': (181600, 155400, 'WBADB p.56 no.213'),
    'Dhahr Mirzbaneh (IB site above large cemetery) [WBADB 209]': (181800, 155950, 'WBADB p.55 no.209'),
    'Water Line - Ein Samiya (IB shaft-tomb cemetery, ~60 tombs) [WBADB 214]': (182500, 155000, 'WBADB p.56 no.214'),
    'Kh. Samiyye (Rom-Byz burial caves w/ ossuary fragments) [WBADB 215]': (181700, 155000, 'WBADB p.56 no.215'),
    "'Ein Samiya (large IB shaft-tomb cemetery) [WBADB 217]": (181700, 154700, 'WBADB p.56 no.217'),
}

def ll_vec(a, b):
    (la1, lo1), (la2, lo2) = a[:2], b[:2]
    mlat = math.radians((la1 + la2) / 2)
    dn = (la2 - la1) * 111_132.0
    de = (lo2 - lo1) * 111_320.0 * math.cos(mlat)
    return de, dn

def bearing(de, dn):
    return (math.degrees(math.atan2(de, dn)) + 360) % 360

def compass(b):
    pts = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
    return pts[int((b + 11.25) // 22.5) % 16]

rows = []
o = 'Tell es-Sultan (centroid point)'
for k, v in LL.items():
    if k == o:
        continue
    de, dn = ll_vec(LL[o], v)
    d = math.hypot(de, dn); b = bearing(de, dn)
    rows.append([o, k, round(d), round(b), compass(b), LL[o][2] + ' ; ' + v[2]])
o = 'Tell es-Sultan [WBADB 328]'
k = 'Jericho Cemetery (Hachlili) [WBADB 343]'
de = GRID[k][0] - GRID[o][0]; dn = GRID[k][1] - GRID[o][1]
d = math.hypot(de, dn); b = bearing(de, dn)
rows.append([o, k, round(d), round(b), compass(b), GRID[o][2] + ' ; ' + GRID[k][2]])
o = 'Kh. Marjame (tell) [WBADB 213]'
for k, v in GRID.items():
    if k == o or 'Jericho' in k or 'Sultan' in k:
        continue
    de = v[0] - GRID[o][0]; dn = v[1] - GRID[o][1]
    d = math.hypot(de, dn); b = bearing(de, dn)
    rows.append([o, k, round(d), round(b), compass(b), GRID[o][2] + ' ; ' + v[2]])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['from', 'to', 'distance_m', 'bearing_deg', 'compass', 'sources'])
    w.writerows(rows)
for r in rows:
    print(r)
