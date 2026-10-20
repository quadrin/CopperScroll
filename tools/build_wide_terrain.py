#!/usr/bin/env python3
"""Build a wide, fine modern-terrain patch around one atlas place from Mapterhorn tiles.

    python3 -I tools/build_wide_terrain.py [place_id] [--extent 2400] [--spacing 5]

Standard library + Pillow; tiles are fetched with curl (the proxy CA is configured for it).
Writes atlas/public/terrain/<place>.json, a hillshade PNG and a provenance manifest under
research/assets/plans/atlas-explorer/terrain-wide/ with an identical atlas/research mirror.

Frame: x east, z south, metres, exactly as atlas/app/atlas-map-site-layer.ts places models:
MercatorCoordinate(origin.x + x*scale, origin.y + z*scale) with
scale = MercatorCoordinate.meterInMercatorCoordinateUnits() at the place anchor
(MapLibre earth radius 6371008.8 m). Terrarium tiles are decoded and sampled bilinearly
from a seamless mosaic (pixel centres at +0.5). Modern terrain only; not ancient ground.
"""
import argparse, base64, datetime, gzip, hashlib, json, math, pathlib, shutil, struct, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path(__file__).resolve().parents[1]
TILE_URL = 'https://tiles.mapterhorn.com/{z}/{x}/{y}.webp'
TILEJSON = 'https://tiles.mapterhorn.com/tilejson.json'
DOWNLOAD_INDEX = 'https://download.mapterhorn.com/download_urls.json'
ATTRIBUTION_JSON = 'https://download.mapterhorn.com/attribution.json'
COVERAGE_TILEJSON = 'https://single-archive-tiles.mapterhorn.com/coverage.json'
COVERAGE_URL = 'https://single-archive-tiles.mapterhorn.com/coverage/{z}/{x}/{y}.mvt'
COVERAGE_ZOOM = 12
EARTH_RADIUS = 6371008.8            # MapLibre lng_lat.ts
WEB_MERCATOR_EQUATOR = 40075016.686  # tile-pixel ground size
TILE = 512
RAW_TILE_LIMIT = 15 * 1024 * 1024
EXISTING_PATCHES = REPO / 'atlas/app/atlas-model-terrain.json'
EXISTING_TILES = REPO / 'research/assets/plans/atlas-explorer/terrain'


# ---------- MapLibre-compatible Mercator frame ----------
def merc_x(lon): return (180 + lon) / 360

def merc_y(lat): return (180 - (180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))) / 360

def lat_from_merc_y(y): return 360 / math.pi * math.atan(math.exp((180 - y * 360) * math.pi / 180)) - 90

def lon_from_merc_x(x): return x * 360 - 180

class Frame:
    def __init__(self, lat, lon):
        self.ox, self.oy = merc_x(lon), merc_y(lat)
        self.scale = 1 / (2 * math.pi * EARTH_RADIUS) / math.cos(math.radians(lat_from_merc_y(self.oy)))

    def merc(self, x, z): return self.ox + x * self.scale, self.oy + z * self.scale

    def lnglat(self, x, z):
        mx, my = self.merc(x, z)
        return lon_from_merc_x(mx), lat_from_merc_y(my)


# ---------- fetching ----------
def curl(url, dest):
    r = subprocess.run(['curl', '-L', '--silent', '--show-error', '-o', str(dest), '-w', '%{http_code}', url],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    if r.returncode != 0 or code != '200':
        if dest.exists(): dest.unlink()
        return code or 'curl-exit-%d' % r.returncode, r.stderr.strip()
    return '200', ''

def fetch_json(url, cache):
    code, err = curl(url, cache)
    if code != '200': sys.exit(f'FAILED {url}: HTTP {code} {err}')
    return json.loads(cache.read_text())

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------- Terrarium mosaic ----------
class Mosaic:
    """Seamless elevation grid over a block of tiles at one zoom."""
    def __init__(self, zoom, tx0, ty0, tx1, ty1, tile_path):
        self.zoom, self.tx0, self.ty0 = zoom, tx0, ty0
        self.w, self.h = (tx1 - tx0 + 1) * TILE, (ty1 - ty0 + 1) * TILE
        self.data = [0.0] * (self.w * self.h)
        for ty in range(ty0, ty1 + 1):
            for tx in range(tx0, tx1 + 1):
                rgb = Image.open(tile_path(zoom, tx, ty)).convert('RGB').tobytes()
                bx, by = (tx - tx0) * TILE, (ty - ty0) * TILE
                for row in range(TILE):
                    base = (by + row) * self.w + bx
                    o = row * TILE * 3
                    for col in range(TILE):
                        k = o + col * 3
                        self.data[base + col] = rgb[k] * 256 + rgb[k + 1] + rgb[k + 2] / 256 - 32768

    def sample(self, mx, my):
        n = 2 ** self.zoom
        px = mx * n * TILE - 0.5 - self.tx0 * TILE
        py = my * n * TILE - 0.5 - self.ty0 * TILE
        x0, y0 = math.floor(px), math.floor(py)
        tx, ty = px - x0, py - y0
        if x0 < 0 or y0 < 0 or x0 + 1 >= self.w or y0 + 1 >= self.h:
            raise ValueError('sample outside mosaic')
        d, w = self.data, self.w
        a, b = d[y0 * w + x0], d[y0 * w + x0 + 1]
        c, e = d[(y0 + 1) * w + x0], d[(y0 + 1) * w + x0 + 1]
        return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + e * tx) * ty

def tile_block(zoom, mercs):
    n = 2 ** zoom
    xs = [m[0] * n * TILE - 0.5 for m in mercs]; ys = [m[1] * n * TILE - 0.5 for m in mercs]
    return (math.floor((min(xs) - 1) / TILE), math.floor((min(ys) - 1) / TILE),
            math.floor((max(xs) + 2) / TILE), math.floor((max(ys) + 2) / TILE))


# ---------- minimal Mapbox Vector Tile reader (coverage polygons) ----------
def varint(buf, i):
    out = shift = 0
    while True:
        b = buf[i]; i += 1
        out |= (b & 0x7f) << shift
        if b < 0x80: return out, i
        shift += 7

def pb_fields(buf):
    i = 0
    while i < len(buf):
        key, i = varint(buf, i)
        field, wire = key >> 3, key & 7
        if wire == 0: val, i = varint(buf, i)
        elif wire == 2:
            ln, i = varint(buf, i); val = buf[i:i + ln]; i += ln
        elif wire == 1: val = buf[i:i + 8]; i += 8
        elif wire == 5: val = buf[i:i + 4]; i += 4
        else: raise ValueError('unsupported wire type')
        yield field, val

def packed(buf):
    out, i = [], 0
    while i < len(buf):
        v, i = varint(buf, i); out.append(v)
    return out

def mvt_polygons(raw):
    if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
    result = []
    for f, layer in pb_fields(raw):
        if f != 3: continue
        keys, values, feats, extent = [], [], [], 4096
        for lf, lv in pb_fields(layer):
            if lf == 3: keys.append(lv.decode())
            elif lf == 4:
                v = None
                for vf, vv in pb_fields(lv):
                    if vf == 1: v = vv.decode()
                    elif vf in (4, 5): v = vv
                    elif vf == 6: v = (vv >> 1) ^ -(vv & 1)
                    elif vf == 7: v = bool(vv)
                    elif vf == 2: v = struct.unpack('<f', vv)[0]
                    elif vf == 3: v = struct.unpack('<d', vv)[0]
                values.append(v)
            elif lf == 2: feats.append(lv)
            elif lf == 5: extent = lv
        for feat in feats:
            tags, geom, gtype = [], [], 0
            for ff, fv in pb_fields(feat):
                if ff == 2: tags = packed(fv)
                elif ff == 3: gtype = fv
                elif ff == 4: geom = packed(fv)
            if gtype != 3: continue
            props = {keys[tags[k]]: values[tags[k + 1]] for k in range(0, len(tags), 2)}
            rings, cur, x, y, i = [], None, 0, 0, 0
            while i < len(geom):
                cid, cnt = geom[i] & 7, geom[i] >> 3; i += 1
                if cid in (1, 2):
                    for _ in range(cnt):
                        dx, dy = geom[i], geom[i + 1]; i += 2
                        x += (dx >> 1) ^ -(dx & 1); y += (dy >> 1) ^ -(dy & 1)
                        if cid == 1: cur = [(x, y)]; rings.append(cur)
                        else: cur.append((x, y))
            result.append((props, rings, extent))
    return result

def inside(rings, px, py):
    hit = False
    for ring in rings:
        for k in range(len(ring)):
            (x1, y1), (x2, y2) = ring[k - 1], ring[k]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: hit = not hit
    return hit


# ---------- hillshade figure ----------
def hillshade_png(path, vals, size, spacing, extent, place, notes):
    scale = max(1, 1000 // size)
    S = size * scale
    hs = []
    az, alt = math.radians(315), math.radians(45)
    lx, ly, lz = math.cos(alt) * math.sin(az), math.cos(alt) * math.cos(az), math.sin(alt)
    for j in range(size):
        for i in range(size):
            e = lambda a, b: vals[min(size - 1, max(0, b)) * size + min(size - 1, max(0, a))]
            dzdx = (e(i + 1, j) - e(i - 1, j)) / (2 * spacing)
            dzdn = (e(i, j - 1) - e(i, j + 1)) / (2 * spacing)  # north is row j-1
            nx, ny, nz = -dzdx, -dzdn, 1.0
            norm = math.sqrt(nx * nx + ny * ny + nz * nz)
            hs.append(max(0.0, (nx * lx + ny * ly + nz * lz) / norm))
    lo, hi = min(vals), max(vals)
    ramp = [(0.0, (92, 140, 120)), (0.25, (176, 186, 140)), (0.55, (214, 196, 150)), (0.8, (176, 140, 104)), (1.0, (236, 228, 214))]
    def tint(t):
        for (t0, c0), (t1, c1) in zip(ramp, ramp[1:]):
            if t <= t1:
                f = (t - t0) / (t1 - t0) if t1 > t0 else 0
                return tuple(c0[k] + (c1[k] - c0[k]) * f for k in range(3))
        return ramp[-1][1]
    base = Image.new('RGB', (size, size))
    base.putdata([tuple(int(min(255, c * (0.30 + 0.85 * h))) for c in tint((v - lo) / (hi - lo or 1)))
                  for v, h in zip(vals, hs)])
    img = base.resize((S, S), Image.BICUBIC)
    fe = Image.new('F', (size, size)); fe.putdata(vals)
    big = fe.resize((S, S), Image.BILINEAR)
    ef = list(getattr(big, 'get_flattened_data', big.getdata)())
    px = img.load()
    for y in range(S - 1):
        for x in range(S - 1):
            a, b, c = ef[y * S + x], ef[y * S + x + 1], ef[(y + 1) * S + x]
            for interval, col in ((100, (40, 30, 20)), (20, (95, 80, 60))):
                q = math.floor(a / interval)
                if q != math.floor(b / interval) or q != math.floor(c / interval):
                    px[x, y] = col; break
    footer = 34
    canvas = Image.new('RGB', (S, S + footer), (250, 248, 242)); canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    try: font = ImageFont.load_default(size=13); small = ImageFont.load_default(size=11)
    except TypeError: font = small = ImageFont.load_default()
    m_to_px = lambda x, z: ((x + extent / 2) / spacing * scale, (z + extent / 2) / spacing * scale)
    # Existing 800 m atlas patch (dashed outline).
    x0, y0 = m_to_px(-400, -400); x1, y1 = m_to_px(400, 400)
    for k in range(int(x0), int(x1), 12):
        d.line([(k, y0), (min(k + 6, x1), y0)], fill=(255, 255, 255), width=2); d.line([(k, y1), (min(k + 6, x1), y1)], fill=(255, 255, 255), width=2)
    for k in range(int(y0), int(y1), 12):
        d.line([(x0, k), (x0, min(k + 6, y1))], fill=(255, 255, 255), width=2); d.line([(x1, k), (x1, min(k + 6, y1))], fill=(255, 255, 255), width=2)
    d.text((x0 + 4, y0 + 3), 'existing 800 m patch', fill=(255, 255, 255), font=small)
    for mk in notes['markers']:
        cx, cy = m_to_px(mk['x'], mk['z']); r = mk['radius_m'] / spacing * scale
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=mk['colour'], width=2)
        d.line([(cx - 9, cy), (cx + 9, cy)], fill=mk['colour'], width=3); d.line([(cx, cy - 9), (cx, cy + 9)], fill=mk['colour'], width=3)
        d.text((cx + r + 4, cy - 7), mk['label'], fill=mk['colour'], font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    # North arrow and scale bar.
    ax, ay = S - 34, 18
    d.polygon([(ax, ay), (ax - 9, ay + 26), (ax, ay + 20), (ax + 9, ay + 26)], fill=(20, 20, 20))
    d.text((ax - 4, ay + 28), 'N', fill=(20, 20, 20), font=font)
    bar = 500 / spacing * scale; bx, by = 18, S - 22
    d.rectangle([bx - 4, by - 18, bx + bar + 50, by + 8], fill=(250, 248, 242))
    d.rectangle([bx, by, bx + bar / 2, by + 5], fill=(20, 20, 20)); d.rectangle([bx + bar / 2, by, bx + bar, by + 5], outline=(20, 20, 20), fill=(255, 255, 255))
    d.text((bx, by - 16), '0', fill=(20, 20, 20), font=small); d.text((bx + bar - 18, by - 16), '500 m', fill=(20, 20, 20), font=small)
    d.text((6, S + 3), notes['line1'], fill=(30, 30, 30), font=small)
    d.text((6, S + 18), notes['line2'], fill=(30, 30, 30), font=small)
    canvas.save(path, optimize=True)
    return canvas.size


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('place', nargs='?', default='kh_qumran')
    ap.add_argument('--extent', type=float, default=2400.0)
    ap.add_argument('--spacing', type=float, default=5.0)
    args = ap.parse_args()
    place_id, extent, spacing = args.place, args.extent, args.spacing
    size = int(round(extent / spacing)) + 1
    today = datetime.date.today().isoformat()

    places = {p['id']: p for p in json.loads((REPO / 'atlas/app/atlas-data.json').read_text())['places']}
    if place_id not in places or places[place_id].get('lat') is None: sys.exit(f'{place_id}: no mapped anchor')
    place = places[place_id]
    lat, lon = place['lat'], place['lon']
    frame = Frame(lat, lon)

    archive = REPO / 'research/assets/plans/atlas-explorer/terrain-wide'; archive.mkdir(parents=True, exist_ok=True)
    mirror = REPO / 'atlas/research/assets/plans/atlas-explorer/terrain-wide'
    out_path = REPO / f'atlas/public/terrain/{place_id}.json'; out_path.parent.mkdir(parents=True, exist_ok=True)
    scratch = archive / '.fetch'; scratch.mkdir(exist_ok=True)

    # 1. Zoom: finest served zoom whose pixel is <= spacing, else the finest served zoom.
    tilejson = fetch_json(TILEJSON, scratch / 'tilejson.json')
    index = fetch_json(DOWNLOAD_INDEX, scratch / 'download_urls.json')
    covering = [it for it in index['items'] if it['min_lon'] <= lon <= it['max_lon'] and it['min_lat'] <= lat <= it['max_lat']]
    area_max = max(it['max_zoom'] for it in covering)
    pixel = lambda z: WEB_MERCATOR_EQUATOR * math.cos(math.radians(lat)) / (2 ** z * TILE)
    wanted = next(z for z in range(0, 25) if pixel(z) <= spacing)
    probes = []
    for z in range(wanted, -1, -1):  # first zoom meeting the target, then coarser until one is served
        n = 2 ** z; tx, ty = int(frame.ox * n), int(frame.oy * n)
        url = TILE_URL.format(z=z, x=tx, y=ty)
        code, err = curl(url, scratch / 'probe.webp')
        probes.append({'zoom': z, 'url': url, 'http': code, 'pixel_m': round(pixel(z), 2)})
        print('probe', url, code, err, flush=True)
        if code == '200': break
    zoom = probes[-1]['zoom']
    if probes[-1]['http'] != '200': sys.exit('no Mapterhorn zoom served at the anchor')
    (scratch / 'probe.webp').unlink(missing_ok=True)

    # 2. Sample positions (row-major, north-west to south-east) and needed tiles.
    coords = [(-extent / 2 + i * spacing, -extent / 2 + j * spacing) for j in range(size) for i in range(size)]
    mercs = [frame.merc(x, z) for x, z in coords]
    tx0, ty0, tx1, ty1 = tile_block(zoom, mercs)
    records = []
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            url = TILE_URL.format(z=zoom, x=tx, y=ty); f = archive / f'{zoom}-{tx}-{ty}.webp'
            if not f.exists():
                print('Fetching', url, flush=True)
                code, err = curl(url, f)
                if code != '200': sys.exit(f'FAILED {url}: HTTP {code} {err}')
            records.append({'url': url, 'file': str(f.relative_to(REPO)), 'bytes': f.stat().st_size, 'sha256': sha256(f)})
    mosaic = Mosaic(zoom, tx0, ty0, tx1, ty1, lambda z, x, y: archive / f'{z}-{x}-{y}.webp')
    raw = [mosaic.sample(mx, my) for mx, my in mercs]
    centre = round(mosaic.sample(*frame.merc(0, 0)), 2)
    dm = [int(round((v - centre) * 10)) for v in raw]
    if min(dm) < -32768 or max(dm) > 32767: sys.exit('relief exceeds int16 decimetres')
    vals = [centre + v / 10 for v in dm]

    # 3. Source coverage from Mapterhorn's coverage vector tiles.
    attribution = fetch_json(ATTRIBUTION_JSON, scratch / 'attribution.json')
    res = {a['source']: a['resolution'] for a in attribution}
    test_pts = [(x, z) for z in (-extent / 2, -extent / 4, 0, extent / 4, extent / 2) for x in (-extent / 2, -extent / 4, 0, extent / 4, extent / 2)]
    cov_tiles, cov_records, point_sources = {}, [], []
    n = 2 ** COVERAGE_ZOOM
    for x, z in test_pts:
        mx, my = frame.merc(x, z); ctx, cty = int(mx * n), int(my * n)
        if (ctx, cty) not in cov_tiles:
            url = COVERAGE_URL.format(z=COVERAGE_ZOOM, x=ctx, y=cty); f = archive / f'coverage-{COVERAGE_ZOOM}-{ctx}-{cty}.mvt'
            if not f.exists():
                code, err = curl(url, f)
                if code != '200': sys.exit(f'FAILED {url}: HTTP {code} {err}')
            cov_tiles[(ctx, cty)] = mvt_polygons(f.read_bytes())
            cov_records.append({'url': url, 'file': str(f.relative_to(REPO)), 'bytes': f.stat().st_size, 'sha256': sha256(f)})
        srcs = sorted({props.get('source') for props, rings, ext in cov_tiles[(ctx, cty)]
                       if inside(rings, (mx * n - ctx) * ext, (my * n - cty) * ext)})
        point_sources.append({'x': x, 'z': z, 'sources': srcs,
                              'finest': min(srcs, key=lambda s: res.get(s, 1e9)) if srcs else None})
    finest = sorted({p['finest'] for p in point_sources if p['finest']})
    used_sources = sorted({s for p in point_sources for s in p['sources']})

    # 4. Overlap check against the existing 800 m atlas patch (both read in the atlas frame).
    overlap = None
    if EXISTING_PATCHES.exists() and place_id in json.loads(EXISTING_PATCHES.read_text()):
        old = json.loads(EXISTING_PATCHES.read_text())[place_id]
        on, oe = old['size'], old['extent']
        def new_at(x, z):
            u = (x + extent / 2) / spacing; v = (z + extent / 2) / spacing
            i, j = min(size - 2, max(0, math.floor(u))), min(size - 2, max(0, math.floor(v))); a, b = u - i, v - j
            g = lambda ii, jj: vals[jj * size + ii]
            return (g(i, j) * (1 - a) + g(i + 1, j) * a) * (1 - b) + (g(i, j + 1) * (1 - a) + g(i + 1, j + 1) * a) * b
        pts = [((i / (on - 1) - .5) * oe, (j / (on - 1) - .5) * oe, old['elevations'][j * on + i]) for j in range(on) for i in range(on)]
        def stats(sx=0.0, sz=0.0, against=None):
            diffs = [(o - (against(x, z) if against else new_at(x + sx, z + sz)), x, z) for x, z, o in pts]
            d = [t[0] for t in diffs]; worst = max(diffs, key=lambda t: abs(t[0]))
            return {'mean_old_minus_new_m': round(sum(d) / len(d), 2), 'mean_abs_m': round(sum(map(abs, d)) / len(d), 2),
                    'rms_m': round(math.sqrt(sum(v * v for v in d) / len(d)), 2), 'max_abs_m': round(abs(worst[0]), 2),
                    'max_at_xz_m': [worst[1], worst[2]]}
        base = stats()
        best = min(((sx, sz) for sx in range(-40, 41, 5) for sz in range(-40, 41, 5)),
                   key=lambda s: stats(*s)['rms_m'])
        overlap = {'compared': f'{on} x {on} samples of the existing {int(oe)} m patch in {EXISTING_PATCHES.relative_to(REPO)} '
                               f'vs this patch bilinearly read at the same atlas-frame x,z',
                   'zero_shift': base, 'best_shift_search': {'grid': '-40..40 m in 5 m steps, x and z',
                   'best_shift_xz_m': list(best), 'rms_at_best_m': stats(*best)['rms_m']},
                   'centre_elevation_old_m': old['centreElevation'], 'centre_elevation_new_m': centre}
        # Same-zoom control: re-read the archived z12 tiles in the Mercator frame to isolate frame vs resolution.
        old_mercs = [frame.merc(x, z) for x, z, _ in pts]
        b12 = tile_block(12, old_mercs)
        tp = lambda z, x, y: EXISTING_TILES / f'{z}-{x}-{y}.webp'
        if all(tp(12, x, y).exists() for x in range(b12[0], b12[2] + 1) for y in range(b12[1], b12[3] + 1)):
            m12 = Mosaic(12, *b12, tp)
            overlap['z12_same_tiles_mercator_frame'] = stats(against=lambda x, z: m12.sample(*frame.merc(x, z)))
            overlap['z12_same_tiles_mercator_frame']['note'] = ('Old patch vs the same archived z12 tiles re-read here in the atlas Mercator '
                'frame with a seamless mosaic: isolates frame convention (111320 m/deg local approximation vs MapLibre metres) '
                'and tile-edge clamping from the z12-to-z13 resolution change.')
        else:
            overlap['z12_same_tiles_mercator_frame'] = 'skipped: needed z12 tiles not in the existing archive'

    # 5. Output asset.
    asset = {'place': place_id, 'lat': lat, 'lon': lon, 'extent': int(extent) if extent == int(extent) else extent,
             'size': size, 'spacing': int(spacing) if spacing == int(spacing) else spacing,
             'centreElevation': centre, 'min': round(min(vals), 1), 'max': round(max(vals), 1),
             'encoding': f'int16 little-endian, decimetres relative to centreElevation, row-major from north-west '
                         f'(z=-{extent / 2:g}) to south-east, base64',
             'zoom': zoom, 'source': 'Mapterhorn terrain tiles (' + ', '.join(finest) + ')',
             'manifest': str((archive / 'manifest.json').relative_to(REPO)),
             'data': base64.b64encode(struct.pack(f'<{len(dm)}h', *dm)).decode('ascii')}
    out_path.write_text(json.dumps(asset, separators=(',', ':')) + '\n')

    # 6. Hillshade with anchor and other mapped places inside the patch.
    markers = [{'x': 0, 'z': 0, 'radius_m': 100 if place.get('precision') == '~100 m' else 50, 'colour': (200, 20, 20),
                'label': f"{place.get('shortName', place_id)} anchor ({place.get('precision', '?')})"}]
    for p in places.values():
        if p['id'] == place_id or p.get('lat') is None: continue
        mx, my = merc_x(p['lon']), merc_y(p['lat'])
        x, z = (mx - frame.ox) / frame.scale, (my - frame.oy) / frame.scale
        if abs(x) < extent / 2 - 50 and abs(z) < extent / 2 - 50:
            markers.append({'x': x, 'z': z, 'radius_m': 30, 'colour': (20, 70, 200),
                            'label': f"{p['id']} gazetteer pt ({p.get('precision', '?')})", 'id': p['id']})
    png = archive / f'{place_id}-hillshade.png'
    png_size = hillshade_png(png, vals, size, spacing, extent, place, {
        'markers': markers,
        'line1': f"{place_id}: {int(extent)} m square, {spacing:g} m grid from Mapterhorn z{zoom} ({', '.join(finest)}; "
                 f"{pixel(zoom):.1f} m tile px). Elevation {min(vals):.0f} to {max(vals):.0f} m. Contours 20 m (bold 100 m).",
        'line2': 'Hillshade az 315 alt 45. Modern terrain, not ancient ground. Red circle = anchor precision. (c) Mapterhorn; project derivative.'})

    # 7. Manifest and mirror.
    tiles_bytes = sum(r['bytes'] for r in records)
    tiles_archived = tiles_bytes <= RAW_TILE_LIMIT
    if not tiles_archived:
        for r in records: (REPO / r['file']).unlink(missing_ok=True)
    src_entries = [a for a in attribution if a['source'] in used_sources]
    manifest = {
        'date': today, 'place': place_id,
        'anchor': {'lat': lat, 'lon': lon, 'precision': place.get('precision'), 'gazetteer_source': place.get('source'),
                   'record': 'atlas/app/atlas-data.json places[id=%s]' % place_id},
        'source': 'Mapterhorn terrain tiles', 'tilejson': TILEJSON, 'tilejson_maxzoom': tilejson.get('maxzoom', 'not stated'),
        'attribution_url': 'https://mapterhorn.com/attribution/', 'attribution_json': ATTRIBUTION_JSON,
        'credit': '© Mapterhorn; ' + '; '.join(f"{a['name']} ({a['source']}): {a['producer']} — {a['license']}" for a in src_entries),
        'encoding': 'Terrarium: R*256 + G + B/256 - 32768 metres',
        'zoom_selection': {'target_pixel_m': spacing, 'first_zoom_meeting_target': wanted,
                           'pixel_m_at_zoom': round(pixel(zoom), 2), 'zoom_used': zoom,
                           'high_resolution_archives_covering_anchor': [{k: it[k] for k in ('name', 'url', 'min_zoom', 'max_zoom', 'md5sum', 'size')} for it in covering],
                           'probes': probes,
                           'note': 'tilejson states no maxzoom; Mapterhorn download index lists the z13+ archive covering the anchor and its max_zoom. '
                                   'The finest served zoom is used; 5 m sampling interpolates it and adds no terrain detail.'},
        'tiles_archived': tiles_archived, 'tiles_total_bytes': tiles_bytes, 'tiles': records,
        'coverage_check': {'tileset': COVERAGE_TILEJSON, 'zoom': COVERAGE_ZOOM, 'tiles': cov_records,
                           'method': '5 x 5 points across the patch (corners, quarter points, anchor) tested against the coverage polygons; '
                                     'Mapterhorn uses the finest covering source.',
                           'points': point_sources, 'finest_source_over_patch': finest},
        'sources': src_entries,
        'source_note': 'Mapterhorn source-catalog/isr10/metadata.json gives producer "ASTER GDEM courtesy of METI and NASA processed by 4cast LTD '
                       'using VTbuilder": a 10 m posting resampled from ASTER GDEM, so effective detail is coarser than 10 m.',
        'frame': 'x east, z south, metres; MercatorCoordinate(origin.x + x*scale, origin.y + z*scale), scale = meterInMercatorCoordinateUnits() '
                 'at the anchor (MapLibre earth radius 6371008.8 m), as in atlas/app/atlas-map-site-layer.ts.',
        'sampling': f'Bilinear decoded elevation from a seamless z{zoom} mosaic (pixel centres +0.5); {size} x {size} samples at {spacing:g} m over a '
                    f'{extent:g} m square centred on the anchor; row-major from north-west (z=-{extent / 2:g}) to south-east. Stored as int16 '
                    f'decimetres relative to centreElevation {centre} m (quantisation 0.1 m).',
        'asset': str(out_path.relative_to(REPO)), 'asset_bytes': out_path.stat().st_size, 'asset_sha256': sha256(out_path),
        'elevation_range_m': [round(min(vals), 1), round(max(vals), 1)], 'centre_elevation_m': centre,
        'hillshade': {'file': str(png.relative_to(REPO)), 'pixels': list(png_size), 'sha256': sha256(png),
                      'kind': 'project-generated derivative (hillshade, hypsometric tint, 20/100 m contours) of the sampled grid; not a source image',
                      'markers': [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in m.items() if k != 'colour'} for m in markers],
                      'overlays': 'dashed box = existing 800 m atlas patch; north arrow; 500 m scale bar'},
        'overlap_check': overlap,
        'limit': 'Modern terrain (Mapterhorn compilation), not ancient ground surface. Anchor is a gazetteer point (precision as recorded); '
                 'the patch does not register any plan or identify a feature. Modern road cuts, spoil, wadi beds and the receding Dead Sea '
                 'shoreline are present-day surfaces. Source DEM effective resolution is coarser than the 5 m grid; interpolation adds no detail, '
                 'and steep cliff faces are smoothed. Vertical datum as delivered by Mapterhorn from the source DEM (not independently checked).',
    }
    (archive / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    shutil.rmtree(scratch, ignore_errors=True)
    mirror.mkdir(parents=True, exist_ok=True)
    for f in mirror.iterdir():
        if not (archive / f.name).exists(): f.unlink()
    for f in archive.iterdir(): (mirror / f.name).write_bytes(f.read_bytes())
    print(json.dumps({'zoom': zoom, 'tiles': len(records), 'tiles_bytes': tiles_bytes, 'asset_bytes': out_path.stat().st_size,
                      'centre': centre, 'min': asset['min'], 'max': asset['max'], 'finest_source': finest, 'overlap': overlap}, indent=1))

if __name__ == '__main__':
    main()
