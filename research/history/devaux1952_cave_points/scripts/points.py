"""Refine dot centres (distance-transform core), transform to Palestine grid, and
measure the control symbols (trig triangles, Kh. Qumran square).

Usage: python3 -I points.py <workdir>
Writes <workdir>/points_px.json
"""
import sys, os, json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

W = sys.argv[1]
T = json.load(open(os.path.join(W, 'transforms.json')))
OFF = T['south_row_offset_px']
IMG = {'north': np.asarray(Image.open(os.path.join(W, 'img_p23-001.jpg')).convert('L')).astype(float),
       'south': np.asarray(Image.open(os.path.join(W, 'img_p24-001.jpg')).convert('L')).astype(float)}

# point, half, approx x, approx y, label reading, label confidence, dot-position confidence, label side, notes
PTS = [
    (1, 'north', 875.5, 994.8, '1', 'sure', 'sure', 'label below-left', 'Dot at the end of a dashed line, ~20 px (35 m) below the "-44" spot-height triangle; isolated "1".'),
    (2, 'north', 922.6, 1065.7, '2', 'sure', 'sure', 'label right', ''),
    (3, 'north', 1008.0, 1195.0, '3', 'sure', 'probable', 'label above', 'Dot merged with the foot of the flat-topped "3".'),
    (4, 'north', 1050.9, 1205.5, '4', 'probable', 'probable', 'label above', 'Dot merged with the foot of the "4"; hachure strokes cross the label.'),
    (7, 'north', 1058.1, 1259.2, '7', 'probable', 'probable', 'label above', 'Label overprinted by hachures; dot merged with its foot. Reading as "7" is by elimination as much as by shape.'),
    (8, 'north', 1096.7, 1265.3, '8', 'sure', 'sure', 'label right', 'De Vaux: no. 8 = 3Q (RB 60, 555).'),
    (9, 'north', 1015.1, 1285.6, '9', 'probable', 'sure', 'label above', 'Glyph has the loop at the top and tail curling left: read "9"; "5" not fully excluded.'),
    (10, 'north', 1046.7, 1311.4, '10', 'sure', 'sure', 'label right', ''),
    (12, 'north', 970.4, 1611.9, '12', 'sure', 'probable', 'label right', 'Dot touches a hachure stroke.'),
    (14, 'north', 958.7, 1791.4, '14', 'sure', 'probable', 'label right', 'De Vaux: no. 14 = 1Q (RB 60, 542). Dot touches a hachure stroke.'),
    (15, 'north', 954.9, 1830.0, '15', 'sure', 'probable', 'label right', 'Dot merged with a hachure stroke.'),
    (17, 'north', 1002.3, 1892.4, '17', 'sure', 'sure', 'label right', ''),
    (18, 'north', 995.8, 1867.5, '18', 'sure', 'sure', 'label right', ''),
    (19, 'north', 969.0, 1859.0, '19', 'sure', 'probable', 'label left', 'De Vaux: no. 19 = 2Q (RB 60, 553). Dot touches the tail of the "9" and a hachure; at first sight reads "192".'),
    (21, 'north', 937.2, 1972.1, '21', 'sure', 'sure', 'label right', ''),
    (22, 'south', 772.5, 348.3, '22', 'probable', 'uncertain', 'label below', 'Digits and dot run together with hachures on the N bank of W. Qumran; dot taken as the round blob above-between the two "2"s.'),
    (26, 'south', 956.6, 405.0, '26', 'sure', 'probable', 'label above-right', 'Dot crossed by a drawn line.'),
    (27, 'south', 897.9, 485.4, '27', 'sure', 'probable', 'label left', 'Dot among hachures to the right of the label.'),
    (28, 'south', 889.7, 555.7, '28', 'sure', 'sure', 'label left', ''),
    (29, 'south', 924.1, 541.3, '29', 'sure', 'probable', 'label right', 'Dot touches a hachure stroke.'),
    (30, 'south', 907.6, 584.7, '30', 'sure', 'sure', 'label right', ''),
    (31, 'south', 841.7, 693.3, '31', 'sure', 'sure', 'label above-left', ''),
    (32, 'south', 876.2, 699.3, '32', 'sure', 'sure', 'label right', ''),
    (35, 'south', 1177.8, 779.6, '35', 'sure', 'sure', 'label right', 'In the plain E of the cliff; not mentioned in the text.'),
    (37, 'south', 354.5, 1918.6, '37', 'sure', 'probable', 'label above', 'Dot straddles the N 125 grid line.'),
    (39, 'south', 656.3, 2476.0, '39', 'sure', 'sure', 'label right', 'Beside the "Ras Feshkha" label.'),
    (40, 'south', 561.5, 2611.3, '40', 'sure', 'uncertain', 'label above', 'Blob below the "4" merged with hachures; may be partly a hachure cluster. Near the bottom edge of the map.'),
]


def refine(half, x0, y0, r=16, thr=120):
    a = IMG[half]
    xs, ys = int(round(x0)), int(round(y0))
    win = a[ys - r - 6:ys + r + 7, xs - r - 6:xs + r + 7]
    dark = win < thr
    edt = ndi.distance_transform_edt(dark)
    # restrict max search to radius r around the approximate point
    yy, xx = np.mgrid[0:win.shape[0], 0:win.shape[1]]
    cy, cx = r + 6, r + 6
    near = (yy - cy) ** 2 + (xx - cx) ** 2 <= r * r
    e = np.where(near, edt, 0)
    mx = e.max()
    core = e >= max(2.5, 0.55 * mx)
    lab, _ = ndi.label(core)
    iy, ix = np.unravel_index(np.argmax(e), e.shape)
    comp = lab == lab[iy, ix]
    w = edt * comp
    py = (yy * w).sum() / w.sum(); px = (xx * w).sum() / w.sum()
    return xs - r - 6 + px, ys - r - 6 + py, float(mx)


def to_grid(kind, half, x, y):
    if kind == 'combined':
        yy = y + (OFF if half == 'south' else 0); a = T['combined']['affine']
    else:
        yy = y; a = T[half]['affine']
    return (a['E'][0] + a['E'][1] * x + a['E'][2] * yy, a['N'][0] + a['N'][1] * x + a['N'][2] * yy)


rows = []
for p, half, x0, y0, lab, lconf, dconf, side, note in PTS:
    x, y, rad = refine(half, x0, y0)
    Ec, Nc = to_grid('combined', half, x, y)
    Eh, Nh = to_grid('half', half, x, y)
    rows.append(dict(point=p, half=half, x=round(x, 1), y=round(y, 1), y_combined=round(y + (OFF if half == 'south' else 0), 1),
                     shift_from_blob_px=round(float(np.hypot(x - x0, y - y0)), 1), core_radius_px=round(rad, 1),
                     E=round(Ec, 4), N=round(Nc, 4), E_half=round(Eh, 4), N_half=round(Nh, 4),
                     d_half_vs_combined_m=round(float(np.hypot(Ec - Eh, Nc - Nh) * 1000), 1),
                     label=lab, label_conf=lconf, dot_conf=dconf, label_side=side, note=note))
    print(f"{p:3d} {half} px ({x:7.1f},{y:7.1f}) shift {rows[-1]['shift_from_blob_px']:4.1f} r {rad:4.1f}  E {Ec:.4f} N {Nc:.4f}  half-fit diff {rows[-1]['d_half_vs_combined_m']:.1f} m")

# controls: triangle centroids (outline) and the ruin square
CTRL = [
    ('trig_-72', 'south', (686, 836, 720, 866), 'Trig triangle labelled "-72"'),
    ('trig_-388', 'south', (1532, 732, 1566, 766), 'Trig triangle labelled "-388"'),
    ('khq_square', 'south', (1148, 355, 1170, 377), 'Filled square below "Kh. Qumran" label'),
    ('khq_spotdot', 'south', (1174, 357, 1189, 372), 'Small dot of the "-338" spot height beside the square'),
]
ctrl = []
for cid, half, (x0, y0, x1, y1), desc in CTRL:
    a = IMG[half][y0:y1, x0:x1]
    m = a < 120
    yy, xx = np.mgrid[y0:y1, x0:x1]
    cx, cy = xx[m].mean(), yy[m].mean()
    E, N = to_grid('combined', half, cx, cy)
    Eh, Nh = to_grid('half', half, cx, cy)
    ctrl.append(dict(id=cid, half=half, x=round(float(cx), 1), y=round(float(cy), 1), npix=int(m.sum()), E=round(E, 4), N=round(N, 4),
                     E_half=round(Eh, 4), N_half=round(Nh, 4), desc=desc))
    print(cid, round(cx, 1), round(cy, 1), int(m.sum()), round(E, 4), round(N, 4))

json.dump(dict(points=rows, controls=ctrl), open(os.path.join(W, 'points_px.json'), 'w'), indent=1)
