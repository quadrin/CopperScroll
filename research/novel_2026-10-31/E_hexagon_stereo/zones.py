"""Candidate zones for direction E (and the SULTAN-1 / Jericho-oasis exclusion zone, now NOT applied).

Defined from geography only, before any HEXAGON 1974 image read (31 Oct 2026).
MASK DECISION (31 Oct, before the freeze): the exclusion zone below was set before any
read (commit 26d6a59e). The owner's message of 31 Oct (SP/tools/hexview/SULTAN1.md,
SHA-256 8abcfe31...) made masking E's own choice: amendment A1 (24 Oct) opened reading
north of the tell; HEXAGON failed the 0.5 m resolvability gate (26 Oct, R_eff about 1 m)
and cannot test SULTAN-1-precamp-mouth. E drops the mask. QELT now runs down to the
oasis edge, and JERICHO_OUT is the ring 1-4 km from the tell centre. The 250 m strip
north of the tell lies inside 1 km and is not a zone; nothing E produces tests SULTAN-1.
Writes zones.geojson (EPSG:4326 lon/lat) and prints UTM 36N (EPSG:32636) bounds.

Tell es-Sultan centre: WBADB E334, 31.871116 N 35.444274 E
(research/regional/water_systems/site_points.csv). Check: Old Israel Grid
192150 / 142050 -> EPSG:28193 with the 1,000,000 m false northing added
(192150, 1142050) -> 35.444274 E, 31.871116 N (pyproj; same result with
EPSG:28191 at 192150, 142050).
"""
import json
import sys

from pyproj import Transformer
from shapely.geometry import Point, box, mapping
import warnings
from shapely.ops import transform, unary_union
warnings.filterwarnings("ignore", category=DeprecationWarning)

UTM = "EPSG:32636"
to_utm = Transformer.from_crs("EPSG:4326", UTM, always_xy=True).transform
to_ll = Transformer.from_crs(UTM, "EPSG:4326", always_xy=True).transform

TELL_LL = (35.444274, 31.871116)
R_TELL_M = 3000.0           # "at least all ground within 3 km of the tell centre"
# Jericho oasis envelope (project-defined, generous; not a mapped boundary):
# irrigated land of 'Ain es-Sultan, 'Ain Duk/Nu'eima and the Wadi Qelt fan,
# from the cliff foot (35.415 E) to the eastern farms (35.500 E),
# from south of the Wadi Qelt exit (31.835 N) to Nu'eima (31.905 N).
OASIS_LL = (35.415, 31.835, 35.500, 31.905)
BUFFER_M = 1000.0           # georeferencing-error buffer (coarse 1/32 registration + panoramic distortion)

ZONES_LL = {
    # name: (lon0, lat0, lon1, lat1), reason
    "QUMRAN": ((35.445, 31.728, 35.470, 31.752), "Kh. Qumran plateau, marl terrace and Wadi Qumran mouth; WBADB E754 31.741223 N 35.459768 E"),
    "QELT": ((35.320, 31.822, 35.432, 31.858), "Wadi Qelt from 'Ein Fara (WBADB S2709) past 'Ein el-Fawwar (S2621) and Deir el-Qelt (ASI 109/5/3) to the wadi exit at Tulul Abu el-'Alayiq (ASI 109/5/14 at 35.436 E is just outside)"),
    "KIDRON": ((35.325, 31.700, 35.385, 31.735), "Lower Kidron (Wadi en-Nar) from Mar Saba (ASI 109/7/98) to Hyrcania (ASI 109/7/70) and Nahal Sekhakha (ASI 109/7/48)"),
}
JERICHO_RING_M = (1000.0, 4000.0)  # JERICHO_OUT = ring 1-4 km from the tell centre
# Exploratory training window (used to tune the method; not a candidate zone)
TRAIN_LL = (35.395, 31.758, 35.430, 31.785)


def build():
    tell = transform(to_utm, Point(*TELL_LL))
    core = unary_union([tell.buffer(R_TELL_M, 256), transform(to_utm, box(*OASIS_LL))])
    excl = core.buffer(BUFFER_M, 256)
    zones = {k: transform(to_utm, box(*v[0])) for k, v in ZONES_LL.items()}
    zones["JERICHO_OUT"] = tell.buffer(JERICHO_RING_M[1], 128).difference(tell.buffer(JERICHO_RING_M[0], 128))
    train = transform(to_utm, box(*TRAIN_LL))
    return tell, core, excl, zones, train


def main(out="zones.geojson"):
    tell, core, excl, zones, train = build()
    feats = [
        dict(type="Feature", properties=dict(name="EXCLUSION_CORE", note="3 km circle about Tell es-Sultan E334 + Jericho oasis envelope"),
             geometry=mapping(transform(to_ll, core))),
        dict(type="Feature", properties=dict(name="EXCLUSION", note=f"core + {BUFFER_M:.0f} m buffer; defined 31 Oct before any read; NOT APPLIED after the mask decision (see module docstring)"),
             geometry=mapping(transform(to_ll, excl))),
        dict(type="Feature", properties=dict(name="TRAIN", note="exploratory training window"),
             geometry=mapping(transform(to_ll, train))),
    ]
    for k, g in zones.items():
        note = ZONES_LL[k][1] if k in ZONES_LL else "Jericho outskirts: ring 1-4 km from Tell es-Sultan E334 (tell and 250 m strip excluded)"
        feats.append(dict(type="Feature", properties=dict(name=k, note=note, intersects_exclusion=bool(g.intersects(excl)),
                                                          min_dist_to_exclusion_m=round(g.distance(excl), 1)),
                          geometry=mapping(transform(to_ll, g))))
    fc = dict(type="FeatureCollection", crs_note="coordinates EPSG:4326 lon/lat; metric work in EPSG:32636 (UTM 36N)", features=feats)
    with open(out, "w") as fh:
        json.dump(fc, fh, indent=1)
    print("tell UTM", [round(c, 1) for c in tell.coords[0]])
    print("exclusion UTM bounds", [round(c) for c in excl.bounds], "area km2", round(excl.area / 1e6, 1))
    for k, g in list(zones.items()) + [("TRAIN", train)]:
        print(k, "UTM bounds", [round(c) for c in g.bounds], "km2", round(g.area / 1e6, 2), "dist to exclusion m", round(g.distance(excl)))


if __name__ == "__main__":
    main(*sys.argv[1:])
