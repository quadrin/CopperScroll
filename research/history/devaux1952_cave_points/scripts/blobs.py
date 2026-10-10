"""Detect filled round dots (site symbols) on both halves of pl. XX.

Usage: python3 -I blobs.py <workdir>
Writes <workdir>/blobs.json and annotated tiles under <workdir>/tiles/
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

W = sys.argv[1]
T = json.load(open(os.path.join(W, 'transforms.json')))
IMGS = {'north': 'img_p23-001.jpg', 'south': 'img_p24-001.jpg'}


def px2grid(half, x, y):
    a = T[half]['affine']
    E = a['E'][0] + a['E'][1] * x + a['E'][2] * y
    N = a['N'][0] + a['N'][1] * x + a['N'][2] * y
    return E, N


out = {}
for half, fn in IMGS.items():
    g = np.asarray(Image.open(os.path.join(W, fn)).convert('L')).astype(float)
    dark = g < 110
    # opening with a disk removes thin strokes (lines, hachures, digits) and keeps solid dots
    r = 5
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    disk = (xx ** 2 + yy ** 2) <= r * r
    core = ndi.binary_opening(dark, structure=disk)
    lab, n = ndi.label(core)
    objs = ndi.find_objects(lab)
    blobs = []
    for i, sl in enumerate(objs, 1):
        m = lab[sl] == i
        area = int(m.sum())
        if area < 60:
            continue
        h, w = m.shape
        cy, cx = ndi.center_of_mass(m)
        cy += sl[0].start; cx += sl[1].start
        # intensity-weighted centroid on the original dark mask within a dilated core region
        reg = ndi.binary_dilation(lab == i, iterations=3)[sl[0].start - 0:sl[0].stop, sl[1].start:sl[1].stop] if False else None
        E, N = px2grid(half, cx, cy)
        blobs.append(dict(id=f'{half[0]}{len(blobs)+1:03d}', x=round(float(cx), 1), y=round(float(cy), 1), area=area,
                          w=int(w), h=int(h), fill=round(area / (w * h), 2), E=round(E, 4), N=round(N, 4)))
    out[half] = blobs
    print(half, len(blobs))
    for b in blobs:
        print('  ', b)
    # annotated overview
    im = Image.open(os.path.join(W, fn)).convert('RGB')
    d = ImageDraw.Draw(im)
    for b in blobs:
        d.ellipse([b['x'] - 16, b['y'] - 16, b['x'] + 16, b['y'] + 16], outline=(255, 0, 0), width=2)
        d.text((b['x'] + 18, b['y'] - 18), b['id'], fill=(255, 0, 0))
    im.save(os.path.join(W, 'tiles', f'blobs_{half}.png'))

json.dump(out, open(os.path.join(W, 'blobs.json'), 'w'), indent=1)
