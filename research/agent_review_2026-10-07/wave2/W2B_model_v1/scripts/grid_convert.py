#!/usr/bin/env python3
"""Old Israel (Palestine) grid -> WGS84, with a control-point check.

Archaeological "Israel grid" / "map ref." values such as 181/155 or 18425/17385 are Palestine Grid values
(Cassini-Soldner on the Palestine 1923 datum, Clarke 1880 Benoit ellipsoid) WITHOUT the 1000-km northing
offset.  That is EPSG:28191 ("Palestine 1923 / Palestine Grid", false northing 126 867.909 m).  EPSG:28193
("Palestine 1923 / Israeli CS Grid") is the same projection with false northing 1 126 867.909 m, so it
gives identical results only if 1 000 000 m is added to the northing first.  Datum shift: PROJ's
"Palestine 1923 to WGS 84 (1)" (stated accuracy 2 m) -- negligible at the precisions used here.

Run: python3 -I grid_convert.py  -> prints controls and writes ../inputs/grid_conversions.csv
"""
import csv, math, os
from pyproj import Transformer

T191 = Transformer.from_crs('EPSG:28191', 'EPSG:4326', always_xy=True)
T193 = Transformer.from_crs('EPSG:28193', 'EPSG:4326', always_xy=True)
INV = Transformer.from_crs('EPSG:4326', 'EPSG:28191', always_xy=True)


def oig(e_m, n_m):
    lon, lat = T191.transform(e_m, n_m)
    lon2, lat2 = T193.transform(e_m, n_m + 1_000_000)
    assert abs(lon - lon2) < 1e-9 and abs(lat - lat2) < 1e-9
    return lat, lon


def km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


# Controls: NEAEHL vol. 5 (2008) pp. 2117-2122 table (OIG E/N; the table's column heads call them "LA/LO")
# against independent WGS84 coordinates already used in the project (places_v0.csv) or Wikidata.
CONTROLS = [
    ('Qumran, Khirbet', 193620, 127720, 31.74183, 35.45941, 'Pleiades 688011 (places_v0 kh_qumran)'),
    ('Ramat Rahel', 170800, 127500, 31.73999, 35.21899, 'Pleiades 671109966 (places_v0 ramat_rahel)'),
    ('Hyrcania', 184700, 125200, 31.719, 35.366, 'Wikidata Q1510248 (places_v0 hyrcania)'),
    ('Beth-Shean', 197489, 212014, 32.5037, 35.50309, 'Pleiades 678378 (places_v0 beth_shean)'),
    ('Gerizim, Mount', 175000, 178000, 32.20082, 35.27326, 'Pleiades 678147 (places_v0 gerizim)'),
    ('Mar Saba', 181500, 123600, 31.70494, 35.33115, 'Pleiades 687969 (places_v0 mar_saba)'),
    ('Jericho (NEAEHL entry point)', 191350, 140250, 31.87172, 35.44456, 'Wikidata Q2402267 Tell es-Sultan'),
    ('Ful, Tell el-', 171900, 136700, 31.82348, 35.2312, 'Pleiades 749935552 (places_v0 tell_el_ful)'),
]

TARGETS = [
    # id, label, E, N, unit_m (grid resolution of the published figure), source
    ('ein_samiya_neaehl', "'Ein Samiya and Dhahr Mirzbaneh (NEAEHL site point)", 181010, 155470, 10,
     'NEAEHL vol. 5 (2008) p. 2118, map-reference table (OIG 181010/155470)'),
    ('kh_marjameh_neaehl', 'Khirbet Marjameh (el-Marjama), the tell', 181600, 155400, 100,
     'NEAEHL vol. 5 (2008) p. 2121, map-reference table (OIG 181600/155400)'),
    ('ein_samiya_valley_zissu', "'Ein Samiya valley (Zissu's map ref.)", 181000, 155000, 1000,
     'Zissu, PEQ 133 (2001) p. 150: "map. ref. 181/155, Israel grid"'),
    ('kh_yanun_zissu', 'Khirbet Yanun (Janoah, preferred identification)', 184250, 173850, 10,
     'Zissu, PEQ 133 (2001) p. 149, citing Finkelstein et al. 1997: 828-29 (18425/17385)'),
    ('yanun_village_zissu', 'Yanun village (alternative Janoah point)', 183700, 172450, 10,
     'Zissu, PEQ 133 (2001) p. 149, citing Finkelstein et al. 1997: 822-23 (18370/17245)'),
    ('ein_ghuweir_cave_xiv51', "Cave XIV/51 above the site of 'Ein el-Ghuweir (foot of the cliff)", 189200, 115050, 10,
     "Dahari, 'Atiqot 41 (2002), Region XIV, p. 246 (Hebrew): cave XIV/51 'above the site of Ein el-Ghuweir', map ref. 18920/11505"),
    ('qasr_turabeh_area', "Wadi bottom west of Qasr et-Turabeh (survey centre point)", 188700, 112900, 100,
     "Dahari, 'Atiqot 41 (2002), Region XIV, p. 246 (Hebrew): caves XIV/53-58 'west of Qasr a-Turba', central map ref. 1887/1129"),
]

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    print('CONTROL CHECK (NEAEHL OIG -> WGS84 vs independent coordinate)')
    errs = []
    for name, e, n, lat0, lon0, src in CONTROLS:
        lat, lon = oig(e, n)
        d = km(lat, lon, lat0, lon0)
        errs.append(d)
        print(f'  {name:32s} -> {lat:.5f},{lon:.5f}  vs {lat0:.5f},{lon0:.5f}  diff {d:.2f} km  [{src}]')
    print('  median diff %.2f km, max %.2f km' % (sorted(errs)[len(errs) // 2], max(errs)))
    rows = []
    for pid, lab, e, n, unit, src in TARGETS:
        lat, lon = oig(e, n)
        rows.append(dict(id=pid, label=lab, oig_e=e, oig_n=n, grid_unit_m=unit, lat=round(lat, 5), lon=round(lon, 5),
                         method='EPSG:28191 -> EPSG:4326 (pyproj, PROJ "Palestine 1923 to WGS 84 (1)"); '
                                'identical to EPSG:28193 with N+1000 km', source=src))
        print(f'{pid:28s} {e}/{n} -> {lat:.5f},{lon:.5f}')
    with open(os.path.join(here, '..', 'inputs', 'grid_conversions.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    # wrong-EPSG demonstration: EPSG:28193 with the raw northing lands ~1000 km south
    lon, lat = T193.transform(181010, 155470)
    print(f'(EPSG:28193 used with raw northing would give {lat:.3f},{lon:.3f} -- wrong by ~1000 km)')
