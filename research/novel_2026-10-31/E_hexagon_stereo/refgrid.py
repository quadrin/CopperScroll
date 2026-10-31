"""GLO-30 reference grids in UTM 36N (EPSG:32636) and hillshades.

GLO-30: Copernicus DEM GLO-30, tile Copernicus_DSM_COG_10_N31_00_E035_00_DEM
(https://copernicus-dem-30m.s3.amazonaws.com/, SHA-256 29baca4a...), heights in m
above EGM2008. A 2011-2015 TanDEM-X surface model (includes buildings and trees).
"""
import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

UTM = "EPSG:32636"
REGION = (680000.0, 3480000.0, 780000.0, 3560000.0)  # E0, N0, E1, N1


def grid(path, res, region=REGION, resampling=Resampling.bilinear, dtype=np.float32, nodata=np.nan):
    E0, N0, E1, N1 = region
    w, h = int(round((E1 - E0) / res)), int(round((N1 - N0) / res))
    dst = np.full((h, w), nodata, dtype)
    tr = rasterio.transform.from_origin(E0, N1, res, res)
    with rasterio.open(path) as src:
        reproject(rasterio.band(src, 1), dst, dst_transform=tr, dst_crs=UTM, resampling=resampling,
                  dst_nodata=nodata)
    return dst, tr


def hillshade(z, res, az_deg, el_deg=45.0):
    gy, gx = np.gradient(z, res)  # rows go south: gy = dz/d(south)
    slope = np.arctan(np.hypot(gx, gy))
    # aspect measured clockwise from north, direction of steepest descent
    aspect = np.arctan2(-gx, gy)  # descent direction (east comp = -gx, north comp = +gy since rows go south)
    az, zen = np.radians(az_deg), np.radians(90 - el_deg)
    hs = np.cos(zen) * np.cos(slope) + np.sin(zen) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(hs, 0, 1).astype(np.float32)


def slope_deg(z, res):
    gy, gx = np.gradient(z, res)
    return np.degrees(np.arctan(np.hypot(gx, gy)))
