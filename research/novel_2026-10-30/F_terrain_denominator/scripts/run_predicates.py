"""Direction F: count every place in each fixed region where each frozen terrain predicate is physically possible.

usage:
  python3 -I run_predicates.py DERIVED_DIR BND_DIR CS_REPO OUT_DIR [--dryrun]

--dryrun replaces the four frozen regions by one test box (OIG E 150,000-165,000, N 95,000-110,000, Hebron hills),
which lies outside RF1-RF4, and skips the Kohlit and inventory tests. It exists only to check the code runs.

Inputs (sha256 checked in PROTOCOL_FROZEN.md): dem_utm30.tif and the .npy derivatives written by derivatives.py,
geoBoundaries PSE ADM1 and JOR ADM0, and three CSVs of the CopperScroll repository (read only).
"""
import sys, os, json, csv, math, itertools
import numpy as np, rasterio
from rasterio import features
from scipy import ndimage as ndi
from scipy.signal import fftconvolve
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as stransform

D, BND, REPO, OUT = sys.argv[1:5]
DRY = '--dryrun' in sys.argv
os.makedirs(OUT, exist_ok=True)
CS = 30.0
EIGHT = np.ones((3, 3), bool)

# ---------------- frozen parameters (primary, sensitivity range) ----------------
P = {
    'A_min':   (1.0, [0.25, 4.0]),      # km2, channel = nahal (P1, P3, P3b, P5, P6)
    'A_great': (100.0, [50.0, 200.0]),  # km2, great wadi (P2)
    'S_bank':  (15.0, [10.0, 25.0]),    # deg, bank slope beside a channel (P3)
    'd_min':   (2.0, [1.0, 4.0]),       # m, closed-depression depth (P4a)
    'S_pool':  (5.0, [3.0, 8.0]),       # deg, max slope of a runoff-fed pool site (P4b)
    'A_pool':  (0.05, [0.02, 0.2]),     # km2, min contributing area of a pool site (P4b)
    'S_cliff': (30.0, [25.0, 40.0]),    # deg, cliff slope (P5)
    'H_cliff': (30.0, [20.0, 50.0]),    # m, local relief within 150 m (P5)
    'D_cliff': (150.0, [90.0, 300.0]),  # m, max distance cliff to channel (P5)
    'V_gorge': (0.75, [0.70, 0.80]),    # sky-view factor (300 m) at or below which a channel runs in a gorge (P6)
    'L_sea':   (-395.0, [-390.0, -400.0]),  # m, 1st-century CE Dead Sea level (P7) and land mask
    'D_sea':   (1000.0, [500.0, 2000.0]),   # m, band from the period shoreline (P7)
    'R_kohlit': (1000.0, [500.0, 2000.0]),  # m, Kohlit C1/C2 radius (prereg sec. 4)
}
DZ_ABOVE = 10.0   # m, cliff must stand at least this much above its nearest channel cell (P5)
MOUTH_RUN = 5     # cells, run of non-gorge channel cells below a gorge mouth (P6)

# ---------------- load ----------------
src = rasterio.open(os.path.join(D, 'dem_utm30.tif'))
TR = src.transform
ld = lambda k: np.load(os.path.join(D, k + '.npy'))
z = ld('dem'); slope = ld('slope_deg'); aspect = ld('aspect_deg'); relief = ld('relief150'); svf = ld('svf300')
acc = ld('acc_km2'); fdir = ld('fdir'); filled = ld('filled'); water = ld('water')
wbm = rasterio.open(os.path.join(D, 'wbm_utm30.tif')).read(1)
H, W = z.shape
valid = z > -9000
rows, cols = np.mgrid[0:H, 0:W]
xs = TR.c + (cols + 0.5) * TR.a
ys = TR.f + (rows + 0.5) * TR.e
del rows, cols
t_oig = Transformer.from_crs('EPSG:32636', 'EPSG:28191', always_xy=True)
t_ll = Transformer.from_crs('EPSG:32636', 'EPSG:4326', always_xy=True)
ox, oy = t_oig.transform(xs.ravel(), ys.ravel()); ox = ox.reshape(H, W); oy = oy.reshape(H, W)
lon, lat = t_ll.transform(xs.ravel(), ys.ravel()); lon = lon.reshape(H, W); lat = lat.reshape(H, W)


def rasterize_geo(path, pick):
    g = json.load(open(path))
    to_utm = Transformer.from_crs('EPSG:4326', 'EPSG:32636', always_xy=True).transform
    geoms = [stransform(to_utm, shape(f['geometry'])) for f in g['features'] if pick(f['properties'])]
    return features.rasterize([(mapping(x), 1) for x in geoms], out_shape=(H, W), transform=TR, fill=0, dtype='uint8').astype(bool)


in_wb = rasterize_geo(os.path.join(BND, 'pse_adm1.geojson'), lambda p: p.get('shapeISO') == 'PS-WBK')
in_jor = rasterize_geo(os.path.join(BND, 'jor_adm0.geojson'), lambda p: True)

# ---------------- regions ----------------
if DRY:
    REG = {'TEST': (ox >= 150000) & (ox <= 165000) & (oy >= 95000) & (oy <= 110000)}
else:
    REG = {
        'RF1_qumran_jericho_qelt_kidron': (ox >= 180000) & (ox <= 200000) & (oy >= 118000) & (oy <= 146000) & ~in_jor,
        'RF2_caves_entry25_box': (ox >= 180000) & (ox <= 197000) & (oy >= 91000) & (oy <= 150000) & ~in_jor,
        'RF3_water_systems_box': (lat >= 31.600) & (lat <= 31.900) & (lon >= 35.120) & (lon <= 35.560) & ~in_jor,
        'RF4_kohlit_R1': in_wb & (ox > 175000),
    }


def land(L):
    return valid & (water == 0) & (z >= L)


# ---------------- D8 receivers ----------------
OFF = {64: (-1, 0), 128: (-1, 1), 1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1), 16: (0, -1), 32: (-1, -1)}
rr = np.full((H, W), -1, np.int32); rc = np.full((H, W), -1, np.int32); steplen = np.zeros((H, W), np.float32)
R0, C0 = np.indices((H, W), dtype=np.int32)
for code, (dr, dc) in OFF.items():
    m = fdir == code
    rr[m] = R0[m] + dr; rc[m] = C0[m] + dc; steplen[m] = CS * math.hypot(dr, dc)
ok = (rr >= 0) & (rr < H) & (rc >= 0) & (rc < W)
rr[~ok] = -1; rc[~ok] = -1
del R0, C0


def upstream_count(chan):
    """number of channel cells draining directly into each cell"""
    cnt = np.zeros((H, W), np.int16)
    m = chan & (rr >= 0)
    np.add.at(cnt, (rr[m], rc[m]), 1)
    return cnt


def clusters(mask):
    lab, n = ndi.label(mask, structure=EIGHT)
    return lab, n


# ---------------- predicates ----------------
def p1_nahal(A, L):
    chan = (acc >= A) & land(L)
    up = upstream_count(chan)
    return chan, up


def count_linear(mask, reg):
    m = mask & reg
    length = float(steplen[m].sum()) + 0.0
    return m.sum(), length


rows_out = []


def emit(region, pred, setting, params, unit, count, cells, extent, extent_unit, note=''):
    rows_out.append(dict(region=region, predicate=pred, setting=setting, params=json.dumps(params, sort_keys=True),
                         unit=unit, count=count, cells=int(cells), extent=round(extent, 3), extent_unit=extent_unit, note=note))


def settings(names):
    """primary plus one-at-a-time low/high for each named parameter"""
    base = {k: P[k][0] for k in names}
    out = [('primary', dict(base))]
    for k in names:
        lo, hi = P[k][1]
        for lab, v in (('low', lo), ('high', hi)):
            s = dict(base); s[k] = v; out.append((f'{k}={v}', s))
    return out


# land mask for region-level predicates uses L_sea primary unless the setting changes it
def run_region(rname, reg0):
    # area of land
    for lab_, s in settings(['L_sea']):
        lm = land(s['L_sea']) & reg0
        emit(rname, 'LAND', lab_, s, 'km2', round(lm.sum() * CS * CS / 1e6, 3), lm.sum(), lm.sum() * CS * CS / 1e6, 'km2')
    L0 = P['L_sea'][0]
    reg = reg0
    # P1 nahal and P3b confluence/outlet
    for lab_, s in settings(['A_min']):
        chan, up = p1_nahal(s['A_min'], L0)
        n, length = count_linear(chan, reg)
        emit(rname, 'P1_nahal', lab_, s, '90m_stretch', int(round(length / 90.0)), n, length / 1000, 'km')
        starts = chan & reg & (up != 1)
        emit(rname, 'P1_nahal_reaches', lab_, s, 'reach', int(starts.sum()), starts.sum(), length / 1000, 'km',
             'secondary unit; reach counts scale ~1/A_min by construction')
        junction = chan & reg & (up >= 2)
        rec_ok = rr >= 0
        recv_land = np.zeros((H, W), bool)
        recv_land[rec_ok] = land(L0)[rr[rec_ok], rc[rec_ok]]
        term = chan & reg & ~recv_land & (rr >= 0)
        emit(rname, 'P3b_shulei_outlet', lab_, s, 'point', int(junction.sum() + term.sum()), junction.sum() + term.sum(), 0, '',
             f'junctions {int(junction.sum())}; terminal outlets {int(term.sum())}')
    # P2 great wadi
    for lab_, s in settings(['A_great']):
        chan, up = p1_nahal(s['A_great'], L0)
        n, length = count_linear(chan, reg)
        lab, nsys = clusters(chan & reg)
        emit(rname, 'P2_nahal_gadol', lab_, s, '90m_stretch', int(round(length / 90.0)), n, length / 1000, 'km',
             f'distinct connected trunk systems in region: {nsys}')
    # P3 shulei edge (channel bank)
    for lab_, s in settings(['A_min', 'S_bank']):
        chan = (acc >= s['A_min']) & land(L0)
        steep = (slope >= s['S_bank']) & ~chan & land(L0)
        bank_adj = ndi.binary_dilation(steep, structure=EIGHT) & chan & reg
        emit(rname, 'P3_shulei_edge', lab_, s, '90m_stretch', int(round(bank_adj.sum() * CS / 90.0)), bank_adj.sum(),
             bank_adj.sum() * CS / 1000, 'km', 'channel cells with a bank cell beside them')
    # P4a closed depression
    for lab_, s in settings(['d_min']):
        dep = (filled - z) >= s['d_min']
        m = dep & land(L0)
        lab, n = clusters(m)
        # drop clusters touching modern water cells (WBM) and clusters not in region
        touch_w = ndi.binary_dilation(water.astype(bool), structure=EIGHT)
        bad = np.unique(lab[touch_w & (lab > 0)])
        inreg = np.unique(lab[reg & (lab > 0)])
        keep = np.setdiff1d(inreg, bad)
        sizes = ndi.sum(np.ones_like(lab), lab, keep) if len(keep) else np.array([])
        big = int((sizes >= 3).sum()) if len(keep) else 0
        cells = int(sizes.sum()) if len(keep) else 0
        emit(rname, 'P4a_berekhah_depression', lab_, s, 'cluster', int(len(keep)), cells, cells * CS * CS / 1e6, 'km2',
             f'clusters of >=3 cells (resolvable, >=0.0027 km2): {big}')
    # P4b runoff-fed pool site
    for lab_, s in settings(['S_pool', 'A_pool']):
        m = (slope <= s['S_pool']) & (acc >= s['A_pool']) & land(L0) & reg
        lab, n = clusters(m)
        emit(rname, 'P4b_berekhah_runoff_site', lab_, s, 'cluster', int(n), m.sum(), m.sum() * CS * CS / 1e6, 'km2')
    # P5 cave above a channel
    for lab_, s in settings(['A_min', 'S_cliff', 'H_cliff', 'D_cliff']):
        chan = (acc >= s['A_min']) & land(L0)
        cliff = (slope >= s['S_cliff']) & (relief >= s['H_cliff']) & land(L0)
        dist, (ir, ic) = ndi.distance_transform_edt(~chan, sampling=CS, return_indices=True)
        above = (z - z[ir, ic]) >= DZ_ABOVE
        m = cliff & (dist <= s['D_cliff']) & above & reg
        lab, n = clusters(m)
        emit(rname, 'P5_mearah_above_nahal', lab_, s, 'cluster', int(n), m.sum(), m.sum() * CS * CS / 1e6, 'km2')
        me = m & (aspect >= 45) & (aspect <= 135)
        labe, ne = clusters(me)
        emit(rname, 'P5e_mearah_above_nahal_facing_east', lab_, s, 'cluster', int(ne), me.sum(), me.sum() * CS * CS / 1e6, 'km2',
             'P5 cells whose downslope aspect is 45-135 deg (entries 25, 26 "facing east")')
        c2 = cliff & reg
        lab2, n2 = clusters(c2)
        emit(rname, 'P5x_cliff_any', lab_, s, 'cluster', int(n2), c2.sum(), c2.sum() * CS * CS / 1e6, 'km2',
             'cliff component without the channel condition')
        del dist, ir, ic
    # P6 gorge (tsuq) and gorge mouths
    for lab_, s in settings(['A_min', 'V_gorge']):
        chan = (acc >= s['A_min']) & land(L0)
        g = chan & (svf <= s['V_gorge'])
        n, length = count_linear(g, reg)
        # mouth: gorge cell whose next MOUTH_RUN downstream cells are channel and not gorge
        mouth = np.zeros((H, W), bool)
        cand = np.argwhere(g & reg)
        for (r, c) in cand:
            r1, c1 = rr[r, c], rc[r, c]
            okm = True
            for _ in range(MOUTH_RUN):
                if r1 < 0 or not chan[r1, c1] or g[r1, c1]:
                    okm = False; break
                r1, c1 = rr[r1, c1], rc[r1, c1]
            if okm:
                mouth[r, c] = True
        emit(rname, 'P6_tsuq_gorge', lab_, s, '90m_stretch', int(round(length / 90.0)), n, length / 1000, 'km')
        emit(rname, 'P6m_tsuq_gorge_mouth', lab_, s, 'point', int(mouth.sum()), mouth.sum(), 0, '')
    # P7 the sea (Dead Sea shore band at the period level)
    for lab_, s in settings(['L_sea', 'D_sea']):
        below = valid & (z < s['L_sea'])
        lab, n = clusters(below)
        lake_ids = np.unique(lab[(wbm == 2) & (lab > 0)])
        lake = np.isin(lab, lake_ids)
        dist = ndi.distance_transform_edt(~lake, sampling=CS)
        lm = land(s['L_sea']) & ~lake
        band = lm & (dist <= s['D_sea']) & reg
        shore = lm & (dist <= CS * 1.5) & reg
        emit(rname, 'P7_yam_shore_band', lab_, s, 'km_shoreline', int(round(shore.sum() * CS / 1000)), band.sum(),
             band.sum() * CS * CS / 1e6, 'km2', f'shore cells {int(shore.sum())}')


for rname, reg in REG.items():
    print('region', rname, int(reg.sum()), flush=True)
    run_region(rname, reg)

keys = ['region', 'predicate', 'setting', 'params', 'unit', 'count', 'cells', 'extent', 'extent_unit', 'note']
with open(os.path.join(OUT, 'predicate_counts.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, keys); w.writeheader(); [w.writerow(r) for r in rows_out]

# ---------------- stability (failure condition F-A) ----------------
stab = []
by = {}
for r in rows_out:
    if r['predicate'] in ('LAND', 'P1_nahal_reaches'):
        continue
    by.setdefault((r['region'], r['predicate']), []).append(r)
for (rg, pr), rs in by.items():
    vals = [r['count'] for r in rs]
    prim = [r['count'] for r in rs if r['setting'] == 'primary'][0]
    lo, hi = min(vals), max(vals)
    ratio = (hi / lo) if lo > 0 else (float('inf') if hi > 0 else 1.0)
    stab.append(dict(region=rg, predicate=pr, primary=prim, min=lo, max=hi, ratio=round(ratio, 2) if ratio != float('inf') else 'inf',
                     stable=ratio <= 10))
with open(os.path.join(OUT, 'stability.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, list(stab[0].keys())); w.writeheader(); [w.writerow(r) for r in stab]

if DRY:
    print('dry run done'); sys.exit(0)

# ---------------- resolution tests (F-B ii) ----------------
t_from_ll = Transformer.from_crs('EPSG:4326', 'EPSG:32636', always_xy=True)


def cell_of(lo, la):
    x, y = t_from_ll.transform(lo, la)
    c = int((x - TR.c) / TR.a); r = int((y - TR.f) / TR.e)
    return r, c


def near(mask, pts, radius_m):
    dist = ndi.distance_transform_edt(~mask, sampling=CS)
    hit = [dist[r, c] <= radius_m for (r, c) in pts]
    return hit, dist


res = []
L0 = P['L_sea'][0]
reg2 = REG['RF2_caves_entry25_box'] & land(L0)
cliff0 = (slope >= P['S_cliff'][0]) & (relief >= P['H_cliff'][0]) & land(L0)
cav = [r for r in csv.DictReader(open(os.path.join(REPO, 'research/regional/caves_entry25/caves.csv')))
       if r['coord_ok'] == 'yes' and r['row_kind'] == 'cave' and r['precision_m'] not in ('',) and float(r['precision_m']) <= 50]
pts = [cell_of(float(r['lon']), float(r['lat'])) for r in cav]
pts = [(r, c) for (r, c) in pts if 0 <= r < H and 0 <= c < W and reg2[r, c]]
hit, dist = near(cliff0, pts, 60.0)
base = float((dist[reg2] <= 60.0).mean())
rec = float(np.mean(hit)) if pts else float('nan')
res.append(dict(test='RT_cave_cliff', n=len(pts), recall=round(rec, 3), base_rate=round(base, 3),
                passed=bool(rec >= 0.5 and rec >= 2 * base), note='recorded caves (precision<=50 m) within 60 m of a P5x cliff cell, RF2'))
# P5 full predicate recall (informative)
chan0 = (acc >= P['A_min'][0]) & land(L0)
dch, (ir, ic) = ndi.distance_transform_edt(~chan0, sampling=CS, return_indices=True)
p5 = cliff0 & (dch <= P['D_cliff'][0]) & ((z - z[ir, ic]) >= DZ_ABOVE)
hit5, dist5 = near(p5, pts, 60.0)
res.append(dict(test='RT_cave_P5_informative', n=len(pts), recall=round(float(np.mean(hit5)), 3),
                base_rate=round(float((dist5[reg2] <= 60.0).mean()), 3), passed='', note='informative'))
wat = list(csv.DictReader(open(os.path.join(REPO, 'research/regional/water_systems/water.csv'))))
reg3 = REG['RF3_water_systems_box'] & land(L0)
for typ, mask, test, inf in (('dam', chan0, 'RT_dam_channel', False),
                             ('reservoir_pool', ((slope <= P['S_pool'][0]) & (acc >= P['A_pool'][0]) & land(L0)) | (((filled - z) >= P['d_min'][0]) & land(L0)), 'RT_pool_P4_informative', True)):
    rs = [r for r in wat if r['type'] == typ and r['precision_m'] not in ('',) and float(r['precision_m']) <= 50 and r['lat']]
    pts_ = [cell_of(float(r['lon']), float(r['lat'])) for r in rs]
    pts_ = [(r, c) for (r, c) in pts_ if 0 <= r < H and 0 <= c < W and reg3[r, c]]
    h_, d_ = near(mask, pts_, 60.0)
    b_ = float((d_[reg3] <= 60.0).mean()); rc_ = float(np.mean(h_)) if pts_ else float('nan')
    res.append(dict(test=test, n=len(pts_), recall=round(rc_, 3), base_rate=round(b_, 3),
                    passed='' if inf else bool(rc_ >= 0.5 and rc_ >= 2 * b_), note=f'{typ} rows (precision<=50 m) within 60 m, RF3'))
# ---------------- inventory coverage of terrain units ----------------
cov = []


def coverage(mask, regm, pts_, label, radius=60.0):
    lab, n = clusters(mask & regm)
    if n == 0:
        cov.append(dict(test=label, terrain_units=0, units_with_record=0, share='', n_points=len(pts_), points_in_unit=0)); return
    hitlab = set()
    pin = 0
    rad = int(radius // CS)
    for (r, c) in pts_:
        w_ = lab[max(0, r - rad):r + rad + 1, max(0, c - rad):c + rad + 1]
        u = np.unique(w_[w_ > 0])
        if len(u):
            pin += 1; hitlab.update(u.tolist())
    cov.append(dict(test=label, terrain_units=int(n), units_with_record=len(hitlab), share=round(len(hitlab) / n, 4),
                    n_points=len(pts_), points_in_unit=pin))


cav_all = [r for r in csv.DictReader(open(os.path.join(REPO, 'research/regional/caves_entry25/caves.csv')))
           if r['coord_ok'] == 'yes' and r['lat'] and r['lon']]
pc = [cell_of(float(r['lon']), float(r['lat'])) for r in cav_all]
pc = [(r, c) for (r, c) in pc if 0 <= r < H and 0 <= c < W and REG['RF2_caves_entry25_box'][r, c]]
coverage(cliff0, REG['RF2_caves_entry25_box'] & land(L0), pc, 'COV_caves_on_P5x_cliff_RF2')
coverage(p5, REG['RF2_caves_entry25_box'] & land(L0), pc, 'COV_caves_on_P5_RF2')
pool_rows = [r for r in wat if r['type'] in ('reservoir_pool', 'basin_tank') and r['lat'] and r['lon']]
pp = [cell_of(float(r['lon']), float(r['lat'])) for r in pool_rows]
pp = [(r, c) for (r, c) in pp if 0 <= r < H and 0 <= c < W and REG['RF3_water_systems_box'][r, c]]
host0 = (((slope <= P['S_pool'][0]) & (acc >= P['A_pool'][0])) | (((filled - z) >= P['d_min'][0]))) & land(L0)
coverage(host0, REG['RF3_water_systems_box'] & land(L0), pp, 'COV_pools_on_P4_host_RF3')
with open(os.path.join(OUT, 'inventory_coverage.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, list(cov[0].keys())); w.writeheader(); [w.writerow(r) for r in cov]

with open(os.path.join(OUT, 'resolution_tests.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, list(res[0].keys())); w.writeheader(); [w.writerow(r) for r in res]
del dch, ir, ic

# ---------------- Kohlit terrain denominator ----------------
def sector_kernel(radius, b0, b1):
    n = int(radius // CS)
    dy, dx = np.mgrid[-n:n + 1, -n:n + 1]
    dist = np.hypot(dx, dy) * CS
    brg = (np.degrees(np.arctan2(dx, -dy)) + 360) % 360  # dx east, -dy north (rows run south)
    if b0 <= b1:
        inq = (brg >= b0) & (brg <= b1)
    else:
        inq = (brg >= b0) | (brg <= b1)
    k = (dist <= radius) & inq & (dist > 0)
    return k.astype('float32')


def exists_in_sector(mask, radius, b0, b1):
    k = sector_kernel(radius, b0, b1)
    # correlation: value at p = sum_k mask[p + off] * k[off]  -> convolve with flipped kernel
    v = fftconvolve(mask.astype('float32'), k[::-1, ::-1], mode='same')
    return v > 0.5


units = [r for r in csv.DictReader(open(os.path.join(REPO, 'research/rarity/kohlit/stage1a/stage1a_units.csv')))
         if r['in_R1'] == 'True' and r['main_set'] == 'True']
t_oig2utm = Transformer.from_crs('EPSG:28191', 'EPSG:32636', always_xy=True)
upts = []
for r in units:
    x, y = t_oig2utm.transform(float(r['x']), float(r['y']))
    upts.append((int((y - TR.f) / TR.e), int((x - TR.c) / TR.a)))
reg4 = REG['RF4_kohlit_R1'] & land(L0)
# lattice: every 10th cell (300 m) of RF4 land
lat_mask = np.zeros((H, W), bool); lat_mask[::10, ::10] = True; lat_mask &= reg4
lpts = np.argwhere(lat_mask)
kout = []
grid = list(itertools.product(P['S_pool'][1][:1] + [P['S_pool'][0]] + P['S_pool'][1][1:],
                              P['A_pool'][1][:1] + [P['A_pool'][0]] + P['A_pool'][1][1:],
                              P['R_kohlit'][1][:1] + [P['R_kohlit'][0]] + P['R_kohlit'][1][1:]))
dep0 = ((filled - z) >= P['d_min'][0]) & land(L0)
cl0 = cliff0
per_unit = {}
for (sp, ap, rk) in grid:
    host = (((slope <= sp) & (acc >= ap)) | dep0) & land(L0)
    c1 = exists_in_sector(host, rk, 45, 135)
    c2n = exists_in_sector(cl0, rk, 315, 45)
    u1 = np.array([c1[r, c] for r, c in upts]); u2 = np.array([c2n[r, c] for r, c in upts])
    l1 = c1[lpts[:, 0], lpts[:, 1]]; l2 = c2n[lpts[:, 0], lpts[:, 1]]
    prim = (sp, ap, rk) == (P['S_pool'][0], P['A_pool'][0], P['R_kohlit'][0])
    kout.append(dict(S_pool=sp, A_pool=ap, R=rk, primary=prim, N_units=len(upts), units_C1T=int(u1.sum()),
                     units_C2T_natural=int(u2.sum()), units_both=int((u1 & u2).sum()),
                     N_lattice=len(lpts), lattice_C1T=int(l1.sum()), lattice_C2T_natural=int(l2.sum()), lattice_both=int((l1 & l2).sum())))
    if prim:
        for (r, (ur, uc)), a1, a2 in zip(zip(units, upts), u1, u2):
            per_unit[r['unit_id']] = dict(unit_id=r['unit_id'], name=r['name'], x=r['x'], y=r['y'], C1T=bool(a1), C2T_natural=bool(a2))
    print('kohlit', sp, ap, rk, kout[-1]['units_C1T'], kout[-1]['lattice_C1T'], flush=True)
with open(os.path.join(OUT, 'kohlit_terrain_sensitivity.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, list(kout[0].keys())); w.writeheader(); [w.writerow(r) for r in kout]
with open(os.path.join(OUT, 'kohlit_terrain_units.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, ['unit_id', 'name', 'x', 'y', 'C1T', 'C2T_natural']); w.writeheader(); [w.writerow(v) for v in per_unit.values()]

# ---------------- small GeoJSON: RF1 primary candidate clusters / points ----------------
feats = []
reg1 = REG['RF1_qumran_jericho_qelt_kidron']


def add_points(mask, pred, as_clusters=True):
    if as_clusters:
        lab, n = clusters(mask)
        if n == 0:
            return
        cen = ndi.center_of_mass(np.ones_like(lab), lab, range(1, n + 1))
        sz = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
        for (r, c), s_ in zip(cen, sz):
            x = TR.c + (c + 0.5) * TR.a; y = TR.f + (r + 0.5) * TR.e
            lo, la = t_ll.transform(x, y)
            feats.append(dict(type='Feature', geometry=dict(type='Point', coordinates=[round(lo, 6), round(la, 6)]),
                              properties=dict(predicate=pred, cells=int(s_))))
    else:
        for r, c in np.argwhere(mask):
            x = TR.c + (c + 0.5) * TR.a; y = TR.f + (r + 0.5) * TR.e
            lo, la = t_ll.transform(x, y)
            feats.append(dict(type='Feature', geometry=dict(type='Point', coordinates=[round(lo, 6), round(la, 6)]),
                              properties=dict(predicate=pred, cells=1)))


add_points(p5 & reg1, 'P5_mearah_above_nahal')
dep_c = dep0 & reg1 & ~ndi.binary_dilation(water.astype(bool), structure=EIGHT)
add_points(dep_c, 'P4a_berekhah_depression')
g0 = chan0 & (svf <= P['V_gorge'][0])
mouth = np.zeros((H, W), bool)
for (r, c) in np.argwhere(g0 & reg1):
    r1, c1 = rr[r, c], rc[r, c]; okm = True
    for _ in range(MOUTH_RUN):
        if r1 < 0 or not chan0[r1, c1] or g0[r1, c1]:
            okm = False; break
        r1, c1 = rr[r1, c1], rc[r1, c1]
    if okm:
        mouth[r, c] = True
add_points(mouth, 'P6m_tsuq_gorge_mouth', as_clusters=False)
with open(os.path.join(OUT, 'candidates_RF1_primary.geojson'), 'w') as f:
    json.dump(dict(type='FeatureCollection', features=feats), f)
print('done', len(rows_out), 'rows;', len(feats), 'geojson features')
