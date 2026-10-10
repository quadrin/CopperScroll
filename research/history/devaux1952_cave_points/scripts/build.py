"""Build the cave-point CSV, comparisons and numbers for the README.

Usage: python3 -I build.py <workdir> <repo>
Writes devaux1952_cave_points.csv, devaux1952_cave_points_measurements.csv, build_summary.json
"""
import sys, os, json, csv, re, math
import numpy as np
from pyproj import Transformer
from pyproj.transformer import TransformerGroup

W, REPO = sys.argv[1], sys.argv[2]
T = json.load(open(os.path.join(W, 'transforms.json')))
PP = json.load(open(os.path.join(W, 'points_px.json')))
OFF = T['south_row_offset_px']
A = T['combined']['affine']

# --- CRS chain (repo convention: Palestine grid km x 1000 = EPSG:28191 metres) ---
tg = TransformerGroup('EPSG:28191', 'EPSG:4326', always_xy=True)
T_WGS = tg.transformers[0]          # Palestine 1923 to WGS 84 (1), 2 m
T_ITM = Transformer.from_crs('EPSG:28191', 'EPSG:2039', always_xy=True)  # Palestine 1923 to Israel 1993 (1), 1.5 m
T_ITM_via = TransformerGroup('EPSG:4326', 'EPSG:2039', always_xy=True).transformers[0]
T_INV = TransformerGroup('EPSG:4326', 'EPSG:28191', always_xy=True).transformers[0]
chain = dict(wgs=T_WGS.description, itm=T_ITM.description, itm_from_wgs=T_ITM_via.description, inv=T_INV.description)


def px2pal(half, x, y):
    yy = y + (OFF if half == 'south' else 0)
    return (A['E'][0] + A['E'][1] * x + A['E'][2] * yy, A['N'][0] + A['N'][1] * x + A['N'][2] * yy)


def conv(E_km, N_km):
    x, y = E_km * 1000, N_km * 1000
    lon, lat = T_WGS.transform(x, y)
    ix, iy = T_ITM.transform(x, y)
    jx, jy = T_ITM_via.transform(lon, lat)
    return dict(oig_x=x, oig_y=y, itm_x=ix, itm_y=iy, lat=lat, lon=lon, itm_path_diff_m=math.hypot(ix - jx, iy - jy))


def wgs2pal(lat, lon):
    x, y = T_INV.transform(lon, lat)
    return x / 1000, y / 1000


def dist_m(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) * 1000


def bearing(a, b):
    return (math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) + 360) % 360


# --- per-point uncertainty model (metres, 1 sigma) ---
S_MEAS = {'sure': 2.0, 'probable': 4.0, 'uncertain': 8.0}
S_TRANS = 5.4      # combined affine RMS at the 24 grid intersections
S_DRAFT = 20.0     # assumed: 1 mm plotting error on the 1:20,000 sheet
S_GRID = 15.0      # assumed: base map / grid / datum to modern frame (cf. control offsets)
pts = {}
for r in PP['points']:
    E, N = r['E'], r['N']
    s = math.sqrt(S_MEAS[r['dot_conf']] ** 2 + S_TRANS ** 2 + S_DRAFT ** 2 + S_GRID ** 2)
    pts[r['point']] = dict(r, E=E, N=N, sigma_m=s, **conv(E, N))
P8 = (pts[8]['E'], pts[8]['N'])

# --- prior extraction (same plate, by eye) ---
prior = {}
md = open(os.path.join(REPO, 'research/history/devaux1953_cave_list_extracted.md'), encoding='utf-8').read()
for line in md.splitlines():
    m = re.match(r'^\|\s*\**(\d+)[^|]*\|\s*\**(19\d\.\d+)\s*/\s*(1\d\d\.\d+)', line)
    if m and int(m.group(1)) <= 40 and int(m.group(1)) not in prior:
        prior[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
prior_cmp = {p: round(dist_m((pts[p]['E'], pts[p]['N']), prior[p]), 1) for p in pts if p in prior}

# --- controls on the plate vs repo / modern ---
mm = {r['item_id']: r for r in csv.DictReader(open(os.path.join(REPO, 'research/regional/mandate_maps/features.csv'), encoding='utf-8'))}
g2 = {r['control_id']: r for r in csv.DictReader(open(os.path.join(REPO, 'research/regional/mandate_maps/g2_controls.csv'), encoding='utf-8'))}
ctrl = {c['id']: c for c in PP['controls']}
# manual centre for the -388 triangle: the automatic centroid is pulled W by a drawn line crossing its left side
ctrl['trig_-388']['x'], ctrl['trig_-388']['y'] = 1548.5, 748.0
for c in ctrl.values():
    c['E'], c['N'] = px2pal(c['half'], c['x'], c['y'])
esri_q = wgs2pal(float(g2['ESRI-Q04']['ref_lat']), float(g2['ESRI-Q04']['ref_lon']))
refs_khq = {
    'Esri 2025 main complex centre (repo g2_controls ESRI-Q04, sigma 11 m)': esri_q,
    'NEAEHL 193620/127720 (100 m rounding)': (193.620, 127.720),
    'Mandate 1:20k sheet 19-12 "R" symbol in enclosure (repo Q04)': (int(mm['Q04']['grid_e']) / 1000, int(mm['Q04']['grid_n']) / 1000),
    'Pleiades 688011 / places kh_qumran 31.74183,35.45941 (~100 m)': wgs2pal(31.74183, 35.45941),
    'CHRE 7692 31.741119,35.459027 (salvage S02)': wgs2pal(31.741119, 35.459027),
}
controls_out = []
sq = (ctrl['khq_square']['E'], ctrl['khq_square']['N'])
for k, v in refs_khq.items():
    controls_out.append(dict(plate='Kh. Qumran filled square', ref=k, ref_E=round(v[0], 4), ref_N=round(v[1], 4),
                             dE_m=round((sq[0] - v[0]) * 1000, 1), dN_m=round((sq[1] - v[1]) * 1000, 1), d_m=round(dist_m(sq, v), 1)))
for cid, mid, lab in [('trig_-72', 'Q12', 'Mandate trig 639 (h -72.1)'), ('trig_-388', 'Q11', 'Mandate trig 636 (h -387.7)')]:
    v = (int(mm[mid]['grid_e']) / 1000, int(mm[mid]['grid_n']) / 1000)
    c = (ctrl[cid]['E'], ctrl[cid]['N'])
    controls_out.append(dict(plate=cid, ref=f'{lab}, repo mandate_maps {mid}, position error {mm[mid]["position_error_m"]} m', ref_E=v[0], ref_N=v[1],
                             dE_m=round((c[0] - v[0]) * 1000, 1), dN_m=round((c[1] - v[1]) * 1000, 1), d_m=round(dist_m(c, v), 1)))

# --- repo cave records ---
h09 = wgs2pal(31.7418, 35.4594)   # hoards.json H09 "Qumran Cave 1 scroll jars"
twin = (193.700, 129.300)          # Twin Cave site centre, Greenberg-Keinan rec. 709 / Bar-Adon 1937/1293
def nearest(ref, k=4):
    d = sorted(((dist_m((p['E'], p['N']), ref), n) for n, p in pts.items()))
    return [(n, round(x)) for x, n in d[:k]]
# Patrich & Arubas 1989 Cave 13: (i) sketch Fig. 1 offset from 3Q; (ii) text 2.8 km N of Kh. Qumran
PA_PXKM = (963 - 712) / 2.0                         # scale bar 0-2 km on the 200-dpi page render
pa_13, pa_3q, pa_ruin = (481.6, 940.8), (482.8, 972.4), (477.0, 1257.0)
pa_dE = (pa_13[0] - pa_3q[0]) / PA_PXKM; pa_dN = -(pa_13[1] - pa_3q[1]) / PA_PXKM
pa_sketch = (P8[0] + pa_dE, P8[1] + pa_dN)
pa_3q_to_ruin = math.hypot(pa_3q[0] - pa_ruin[0], pa_3q[1] - pa_ruin[1]) / PA_PXKM
pa_13_to_ruin = math.hypot(pa_13[0] - pa_ruin[0], pa_13[1] - pa_ruin[1]) / PA_PXKM
pa_text_N = esri_q[1] + 2.8
repo_cmp = dict(
    point8_vs_prior_m=prior_cmp.get(8),
    point8_to_khq_square_m=round(dist_m(P8, sq)), point8_to_khq_esri_m=round(dist_m(P8, esri_q)),
    point8_bearing_from_khq_esri=round(bearing(esri_q, P8), 1),
    point14_to_H09_m=round(dist_m((pts[14]['E'], pts[14]['N']), h09)), H09_pal=[round(h09[0], 4), round(h09[1], 4)],
    twin_nearest=nearest(twin), twin_to_8_m=round(dist_m(twin, P8)),
    pa_sketch_offset_km=[round(pa_dE, 3), round(pa_dN, 3)], pa_sketch_pos=[round(pa_sketch[0], 3), round(pa_sketch[1], 3)],
    pa_sketch_nearest=nearest(pa_sketch), pa_3q_to_ruin_km=round(pa_3q_to_ruin, 2), pa_13_to_ruin_km=round(pa_13_to_ruin, 2),
    pa_text_N=round(pa_text_N, 3),
    pa_text_dN_by_point={n: round((pa_text_N - pts[n]['N']) * 1000) for n in (1, 2, 3, 4)},
    northing_above_khq_esri_m={n: round((pts[n]['N'] - esri_q[1]) * 1000) for n in (1, 2, 3, 4, 8)},
)

# --- neighbours of 8 ---
nb = []
for n, p in sorted(pts.items()):
    if n == 8:
        continue
    d = dist_m(P8, (p['E'], p['N']))
    rel = math.sqrt(2 * (S_MEAS[p['dot_conf']] ** 2) + 2 * S_DRAFT ** 2)  # common-mode grid/transform terms cancel
    nb.append(dict(point=n, d_m=round(d), bearing=round(bearing(P8, (p['E'], p['N']))), rel_sigma_m=round(rel)))
nb.sort(key=lambda r: r['d_m'])

# --- CSV outputs ---
cols = ['point', 'label_reading', 'confidence', 'pal_e_km', 'pal_n_km', 'oig_x', 'oig_y', 'itm_x', 'itm_y', 'lat', 'lon', 'dist_to_8_m', 'notes']
with open(os.path.join(W, 'devaux1952_cave_points.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(cols)
    for n, p in sorted(pts.items()):
        notes = (f"Dot position {p['dot_conf']} (pixel term +/-{S_MEAS[p['dot_conf']]:.0f} m); total 1-sigma ~30 m, ~60 m at 95%; printed label relative to dot: {p['label_side'].replace('label ', '')}. "
                 + (p['note'] + ' ' if p['note'] else '')
                 + (f"Prior by-eye reading {prior[n][0]:.2f}/{prior[n][1]:.2f} ({prior_cmp[n]:.0f} m)." if n in prior else ''))
        w.writerow([n, p['label'], p['label_conf'], f"{p['E']:.3f}", f"{p['N']:.3f}", f"{round(p['E'], 3) * 1000:.0f}", f"{round(p['N'], 3) * 1000:.0f}",
                    f"{p['itm_x']:.0f}", f"{p['itm_y']:.0f}", f"{p['lat']:.5f}", f"{p['lon']:.5f}",
                    f"{dist_m(P8, (p['E'], p['N'])):.0f}", notes.strip()])
mcols = ['point', 'half', 'x_px', 'y_px', 'y_px_combined', 'core_radius_px', 'pal_e_km_4dp', 'pal_n_km_4dp', 'pal_e_halfonly', 'pal_n_halfonly',
         'd_half_vs_combined_m', 'label_conf', 'dot_conf', 'sigma_m', 'itm_path_diff_m']
with open(os.path.join(W, 'devaux1952_cave_points_measurements.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(mcols)
    for n, p in sorted(pts.items()):
        w.writerow([n, p['half'], p['x'], p['y'], p['y_combined'], p['core_radius_px'], f"{p['E']:.4f}", f"{p['N']:.4f}",
                    p['E_half'], p['N_half'], p['d_half_vs_combined_m'], p['label_conf'], p['dot_conf'], round(p['sigma_m'], 1),
                    round(p['itm_path_diff_m'], 2)])
    for c in ctrl.values():
        w.writerow([c['id'], c['half'], c['x'], c['y'], c['y'] + (OFF if c['half'] == 'south' else 0), '', f"{c['E']:.4f}", f"{c['N']:.4f}",
                    '', '', '', '', '', '', ''])

summary = dict(chain=chain, n_points=len(pts), point8={k: pts[8][k] for k in ('E', 'N', 'oig_x', 'oig_y', 'itm_x', 'itm_y', 'lat', 'lon', 'sigma_m', 'x', 'y')},
               fits={h: T[h]['fits'] for h in ('north', 'south', 'combined')}, diag={h: T[h]['diag'] for h in ('north', 'south', 'combined')},
               controls=controls_out, repo=repo_cmp, neighbours=nb, prior_diff_m=prior_cmp,
               max_half_vs_combined_m=max(p['d_half_vs_combined_m'] for p in pts.values()),
               max_itm_path_diff_m=max(p['itm_path_diff_m'] for p in pts.values()),
               esri_khq_pal=[round(esri_q[0], 4), round(esri_q[1], 4)],
               ctrl_plate={k: [round(v['E'], 4), round(v['N'], 4)] for k, v in ctrl.items()})
json.dump(summary, open(os.path.join(W, 'build_summary.json'), 'w'), indent=1, default=float)
print(json.dumps({k: summary[k] for k in ('chain', 'n_points', 'point8', 'controls', 'repo', 'max_half_vs_combined_m', 'max_itm_path_diff_m', 'esri_khq_pal', 'ctrl_plate')}, indent=1, default=float))
print('neighbours', nb[:10])
print('prior diffs', prior_cmp)
