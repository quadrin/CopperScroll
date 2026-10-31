"""Mosaic GLO-30 tiles N31/N32 E035, crop lon 35.0-35.65 lat 31.30-32.65, reproject to UTM 36N (EPSG:32636) 30 m.
usage: python3 -I prep_dem.py DEM_DIR OUT_DIR"""
import sys, os, numpy as np, rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
src_dir, out = sys.argv[1], sys.argv[2]
tiles = ['N31_00_E035_00', 'N32_00_E035_00']
for kind, rs in (('DEM', Resampling.bilinear), ('WBM', Resampling.nearest)):
    srcs = [rasterio.open(os.path.join(src_dir, f'Copernicus_DSM_COG_10_{t}_{kind}.tif')) for t in tiles]
    arr, tr = merge(srcs, bounds=(35.0, 31.30, 35.65, 32.65))
    crs = srcs[0].crs
    dst_crs = 'EPSG:32636'
    h, w = arr.shape[1:]
    left, top = tr.c, tr.f; right = left + w * tr.a; bottom = top + h * tr.e
    dtr, dw, dh = calculate_default_transform(crs, dst_crs, w, h, left, bottom, right, top, resolution=30)
    dst = np.full((dh, dw), -9999 if kind == 'DEM' else 255, dtype='float32' if kind == 'DEM' else 'uint8')
    reproject(arr[0], dst, src_transform=tr, src_crs=crs, dst_transform=dtr, dst_crs=dst_crs, resampling=rs,
              src_nodata=None, dst_nodata=(-9999 if kind == 'DEM' else 255))
    prof = dict(driver='GTiff', height=dh, width=dw, count=1, dtype=dst.dtype, crs=dst_crs, transform=dtr,
                nodata=(-9999 if kind == 'DEM' else 255), compress='deflate')
    with rasterio.open(os.path.join(out, f'{kind.lower()}_utm30.tif'), 'w', **prof) as f:
        f.write(dst, 1)
    print(kind, dst.shape, dtr)
