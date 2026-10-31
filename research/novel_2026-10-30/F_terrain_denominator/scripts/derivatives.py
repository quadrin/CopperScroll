"""Terrain derivatives on the UTM 36N 30 m GLO-30 mosaic.
Outputs (npy, float32 unless noted) in OUT_DIR: dem, slope_deg, aspect_deg, relief150, svf300, acc_km2, fdir (int16 D8 code), water(uint8: 1 = WBM lake/river or nodata).
usage: python3 -I derivatives.py DERIVED_DIR"""
import sys, os, numpy as np, rasterio
from scipy import ndimage as ndi
if not hasattr(np, 'in1d'):
    np.in1d = np.isin  # pysheds 0.5 calls np.in1d, removed in numpy 2.x
from pysheds.grid import Grid
d = sys.argv[1]
src = rasterio.open(os.path.join(d, 'dem_utm30.tif'))
z = src.read(1).astype('float64'); nod = z <= -9000
wbm = rasterio.open(os.path.join(d, 'wbm_utm30.tif')).read(1)
water = ((wbm == 2) | (wbm == 3) | (wbm == 1) | nod).astype('uint8')
cs = 30.0
# slope/aspect (Horn 1981)
zp = np.where(nod, np.nan, z)
zz = np.pad(zp, 1, mode='edge')
a, b, c = zz[:-2, :-2], zz[:-2, 1:-1], zz[:-2, 2:]
d_, f = zz[1:-1, :-2], zz[1:-1, 2:]
g, h, i = zz[2:, :-2], zz[2:, 1:-1], zz[2:, 2:]
dzdx = ((c + 2 * f + i) - (a + 2 * d_ + g)) / (8 * cs)   # east positive
dzdy = ((g + 2 * h + i) - (a + 2 * b + c)) / (8 * cs)   # south positive (rows increase southward)
slope = np.degrees(np.arctan(np.hypot(dzdx, dzdy)))
aspect = (np.degrees(np.arctan2(-dzdx, dzdy)) + 360) % 360  # downslope azimuth (direction the slope faces), 0=N, 90=E
# downslope vector (east, north) = (-dzdx, +dzdy) because dzdy is the south-positive gradient; checked on sample cells
# local relief, circular radius 5 cells (150 m)
r = 5; yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; fp = (yy ** 2 + xx ** 2) <= r * r
zf = np.where(nod, np.nanmean(zp), z)
relief = ndi.maximum_filter(zf, footprint=fp) - ndi.minimum_filter(zf, footprint=fp)
# sky-view factor (Zaksek et al. 2011): 16 azimuths, radius 10 cells (300 m)
H, W = z.shape; nd = 16; R = 10
maxang = np.zeros((nd, H, W), dtype='float32')
for k in range(nd):
    az = 2 * np.pi * k / nd; dx, dy = np.sin(az), -np.cos(az)
    best = np.full((H, W), -np.pi / 2, dtype='float32')
    for s in range(1, R + 1):
        ox, oy = int(round(dx * s)), int(round(dy * s))
        dist = np.hypot(ox, oy) * cs
        sh = np.full((H, W), np.nan)
        ys0, ys1 = max(0, -oy), H - max(0, oy); xs0, xs1 = max(0, -ox), W - max(0, ox)
        sh[ys0:ys1, xs0:xs1] = zf[ys0 + oy:ys1 + oy, xs0 + ox:xs1 + ox]
        ang = np.arctan((sh - zf) / dist).astype('float32')
        best = np.fmax(best, np.where(np.isnan(ang), -np.pi / 2, ang))
    maxang[k] = np.maximum(best, 0)  # horizon below horizontal treated as open
svf = (1 - np.mean(np.sin(maxang), axis=0)).astype('float32')
del maxang
# hydrology (pysheds): fill pits, fill depressions, resolve flats, D8, accumulation
grid = Grid.from_raster(os.path.join(d, 'dem_utm30.tif'), nodata=-9999)
dem = grid.read_raster(os.path.join(d, 'dem_utm30.tif'), nodata=-9999)
pf = grid.fill_pits(dem); fl = grid.fill_depressions(pf); inf = grid.resolve_flats(fl)
dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
fdir = grid.flowdir(inf, dirmap=dirmap)
acc = grid.accumulation(fdir, dirmap=dirmap)
acc_km2 = (np.asarray(acc) * cs * cs / 1e6).astype('float32')
filled = np.asarray(fl).astype('float32')
out = dict(dem=z.astype('float32'), slope_deg=slope.astype('float32'), aspect_deg=aspect.astype('float32'),
           relief150=relief.astype('float32'), svf300=svf, acc_km2=acc_km2, fdir=np.asarray(fdir).astype('int16'),
           filled=filled, water=water)
for k, v in out.items():
    np.save(os.path.join(d, k + '.npy'), v)
print('done', z.shape, 'acc max km2 %.0f' % acc_km2.max(), 'svf range', float(np.nanmin(svf)), float(np.nanmax(svf)))
