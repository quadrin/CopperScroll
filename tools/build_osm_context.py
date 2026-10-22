#!/usr/bin/env python3
"""Project OpenStreetMap context features around an atlas site into the site's model frame.

    python3 -I tools/build_osm_context.py <name> <osm.xml> [--radius 450] [--centre X,Z]

<name> is a key in TARGETS below. The OSM file is a map-call extract from the OSM API
(https://api.openstreetmap.org/api/0.6/map?bbox=...), passed as an argument (an untrusted download).

Writes:
- research/assets/plans/osm-context-2026-10-22/<name>.json: the selected OSM elements (ids,
  versions, timestamps, tags, lat/lon), under the ODbL, with an identical atlas/research mirror;
- atlas/app/atlas-site-context.json: per plan, the same features projected to the plan's frame
  (metres, x east, z south, MapLibre Mercator frame at the place anchor, as
  tools/build_wide_terrain.py and atlas/app/atlas-map-site-layer.ts), and any registration.

Context is modern: today's stairs, paths, cemeteries and standing walls. It locates and
orients a model where the mapped monuments allow it; it is never archaeological evidence.
"""
import argparse, base64, datetime, hashlib, json, math, pathlib, struct, sys
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = REPO / 'research/assets/plans/osm-context-2026-10-22'
MIRROR = REPO / 'atlas/research/assets/plans/osm-context-2026-10-22'
OUT = REPO / 'atlas/app/atlas-site-context.json'
EARTH_RADIUS = 6371008.8
LICENCE = 'Open Database License (ODbL) 1.0; © OpenStreetMap contributors, https://www.openstreetmap.org/copyright'

# Which elements each target keeps. Monument outlines or corner nodes register the model; the rest is
# drawn as context.
TARGETS = {
    'kidron': {'plan': 'kidron-bene-hezir', 'place': 'jer_kidron_mon',
               'outlines': {'bene-hezir': 'w288284732', 'zechariah': 'w288284733', 'absalom': 'w137729556'}},
    # The south-west and south-east corners of the Haram enclosure (relation 5862584, Temple Mount).
    'great-sea': {'plan': 'temple-great-sea', 'place': 'jer_temple', 'outlines': {},
                  'corners': {'sw': '29979854', 'se': '2915691228'}},
}
WARREN = REPO / 'research/assets/plans/warren1884-plate-vii/measurements.json'


def merc_x(lon): return (180 + lon) / 360
def merc_y(lat): return (180 - (180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))) / 360
def lat_from_merc_y(y): return 360 / math.pi * math.atan(math.exp((180 - y * 360) * math.pi / 180)) - 90


class Frame:
    def __init__(self, lat, lon):
        self.ox, self.oy = merc_x(lon), merc_y(lat)
        self.scale = 1 / (2 * math.pi * EARTH_RADIUS) / math.cos(math.radians(lat_from_merc_y(self.oy)))

    def xz(self, lat, lon): return ((merc_x(lon) - self.ox) / self.scale, (merc_y(lat) - self.oy) / self.scale)


def classify(tags):
    """The context kinds drawn by the atlas, in priority order, or None. Tunnels, bridges, indoor
    and below-ground ways are left out: the atlas drapes context on the terrain surface."""
    if tags.get('tunnel', 'no') != 'no' or tags.get('bridge', 'no') != 'no' or tags.get('indoor', 'no') != 'no' or tags.get('covered', 'no') == 'yes': return None
    try:
        if float(tags.get('layer', '0')) < 0: return None
    except ValueError: pass
    hw, barrier, historic = tags.get('highway'), tags.get('barrier'), tags.get('historic')
    if hw == 'steps': return 'steps'
    if hw in ('footway', 'path', 'pedestrian', 'track'): return 'path'
    if barrier == 'city_wall' or historic == 'citywalls': return 'wall'
    if barrier == 'retaining_wall': return 'retaining-wall'
    if tags.get('landuse') == 'cemetery' or tags.get('amenity') == 'grave_yard': return 'cemetery'
    if historic == 'city_gate' and 'building' in tags: return 'gate'
    if tags.get('building', 'no') not in ('no', 'roof', 'wall', 'construction', 'ruins') or tags.get('building:part', 'no') != 'no': return 'building'
    return None


def sha256(path): return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def terrain_sampler(place):
    path = REPO / f'atlas/public/terrain/{place}.json'
    if not path.exists(): return None
    t = json.loads(path.read_text()); s, ext, sp = t['size'], t['extent'], t['spacing']
    dm = struct.unpack(f'<{s * s}h', base64.b64decode(t['data']))
    def at(x, z):
        u, v = (x + ext / 2) / sp, (z + ext / 2) / sp
        i, j = min(s - 2, max(0, int(u))), min(s - 2, max(0, int(v))); a, b = u - i, v - j
        g = lambda ii, jj: dm[jj * s + ii] / 10
        return (g(i, j) * (1 - a) + g(i + 1, j) * a) * (1 - b) + (g(i, j + 1) * (1 - a) + g(i + 1, j + 1) * a) * b
    return at


def bearing(a, b): return math.degrees(math.atan2(b[0] - a[0], -(b[1] - a[1]))) % 360


def number(value):
    try: return float(str(value).split()[0].replace(',', '.'))
    except (ValueError, IndexError): return None


def great_sea_registration(corners):
    """Place and turn the Great Sea model (Warren Pl. VII frame) by the Haram's two south corners."""
    m = json.loads(WARREN.read_text()); reg = m['registration']
    o, mpp, t = m['greatSea']['origin_px'], m['scale']['m_per_px'], math.radians(m['north']['degrees_clockwise_from_plate_up'])
    def model(px):
        X, Y = (px[0] - o[0]) * mpp, (px[1] - o[1]) * mpp
        return (X * math.cos(t) + Y * math.sin(t), -X * math.sin(t) + Y * math.cos(t))
    msw, mse = model(reg['sw_corner_px']), model(reg['se_corner_px'])
    osw, ose = corners['sw'], corners['se']
    # three.js rotation.y = phi turns bearings by -phi; the midpoints of the two corner pairs coincide.
    phi = math.radians(bearing(msw, mse) - bearing(osw, ose))
    rot = lambda p: (p[0] * math.cos(phi) + p[1] * math.sin(phi), -p[0] * math.sin(phi) + p[1] * math.cos(phi))
    mm, om = rot(((msw[0] + mse[0]) / 2, (msw[1] + mse[1]) / 2)), ((osw[0] + ose[0]) / 2, (osw[1] + ose[1]) / 2)
    origin = (om[0] - mm[0], om[1] - mm[1])
    placed = lambda p: (rot(p)[0] + origin[0], rot(p)[1] + origin[1])
    return {
        'origin': [round(origin[0], 2), round(origin[1], 2)],
        'rotationDeg': round(math.degrees(phi), 2),
        'residuals_m': [round(math.dist(placed(msw), osw), 2), round(math.dist(placed(mse), ose), 2)],
        'checks': {'plateCornerDistance_m': round(math.dist(msw, mse), 1), 'mappedCornerDistance_m': round(math.dist(osw, ose), 1),
                   'plateWallBearing': round(bearing(msw, mse), 2), 'mappedWallBearing': round(bearing(osw, ose), 2)},
        'method': ('The Haram\'s south-west and south-east corners, measured on Warren Pl. VII (line fits on the 600 ppi mask) and '
                   'taken from OpenStreetMap (relation 5862584), fix the model: its frame (the plate at its own scale bar, turned by '
                   'its north arrow) is turned so that the two south walls agree and moved so that their midpoints coincide.'),
    }


def kidron_registration(outlines, at):
    """Place and turn Avigad's frame from the mapped outlines (see the plan's assumptions)."""
    bh = outlines['bene-hezir']['xz']
    sides = [(bh[i], bh[(i + 1) % len(bh)]) for i in range(len(bh))]
    long_sides = sorted(sides, key=lambda s: -math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]))[:2]
    # Façade normal from the long sides: perpendicular, toward the valley (the westerly choice).
    normals = []
    for a, b in long_sides:
        br = bearing(a, b) % 180  # undirected line
        for n in ((br + 90) % 360, (br + 270) % 360):
            if 180 <= n <= 300: normals.append(n)
    outline_normal = sum(normals) / len(normals)
    centroid = lambda pts: (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    porch, zech, absa = centroid(bh), centroid(outlines['zechariah']['xz']), centroid(outlines['absalom']['xz'])
    # Zechariah's centre lies at bearing 170.6° from the porch centre in Avigad's frame (model: porch
    # centre at his (2.1, 0), Zechariah at (4.9, 17.0)); his "west" is the normal, at 270°.
    zech_normal = (270 + bearing(porch, zech) - 170.6) % 360
    normal = (outline_normal + zech_normal) / 2
    path = round(at(*absa), 2) if at else 0.0
    return {
        'porchCentre': [round(porch[0], 2), round(porch[1], 2)],
        'facadeNormalBearing': round(normal, 1),
        'frameRotationDeg': round(270 - normal, 1),
        'absalomCentre': [round(absa[0], 2), round(absa[1], 2)],
        'absalomSideBearing': round(bearing(outlines['absalom']['xz'][0], outlines['absalom']['xz'][1]) % 90, 1),
        'zechariahCentre': [round(zech[0], 2), round(zech[1], 2)],
        'pathLevel': path,
        'checks': {
            'outlineNormalBearing': round(outline_normal, 1), 'zechariahNormalBearing': round(zech_normal, 1),
            'beneHezirToAbsalom_m': round(math.dist(porch, absa), 1), 'beneHezirToZechariah_m': round(math.dist(porch, zech), 1),
            'avigad': 'Bene Ḥezir façade centre about 50 m from Absalom and about 20 m from Zechariah (p. 37); façade faces south-west (p. 37)',
        },
        'method': ('Porch centre = centroid of the OSM outline of the tomb (a 7–8 × 2–3 m strip along the façade). '
                   'Façade normal = mean of the perpendicular to the outline\'s long sides and the bearing that puts Zechariah\'s '
                   'centre where Avigad\'s plan puts it. Path level = modern terrain (Mapterhorn) at Absalom\'s mapped centre, '
                   'Absalom standing on the valley floor.'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name', choices=sorted(TARGETS)); ap.add_argument('osm')
    ap.add_argument('--radius', type=float, default=450); ap.add_argument('--centre', default=None)
    ap.add_argument('--bbox', default=None, help='the bbox of the API call, recorded for provenance')
    args = ap.parse_args()
    target = TARGETS[args.name]
    places = {p['id']: p for p in json.loads((REPO / 'atlas/app/atlas-data.json').read_text())['places']}
    place = places[target['place']]; frame = Frame(place['lat'], place['lon'])
    root = ET.parse(args.osm).getroot()
    nodes = {n.get('id'): n for n in root.iter('node')}
    pos = {i: frame.xz(float(n.get('lat')), float(n.get('lon'))) for i, n in nodes.items()}
    tags = lambda e: {t.get('k'): t.get('v') for t in e.findall('tag')}
    cx, cz = (float(v) for v in args.centre.split(',')) if args.centre else (0.0, 0.0)
    keep_ids = set(target['outlines'].values())
    selected, projected, outlines = [], [], {}
    for w in root.iter('way'):
        t, wid = tags(w), 'w' + w.get('id')
        refs = [nd.get('ref') for nd in w.findall('nd') if nd.get('ref') in pos]
        if len(refs) < 2: continue
        xz = [pos[r] for r in refs]
        kind = classify(t)
        near = min(math.hypot(x - cx, z - cz) for x, z in xz) <= args.radius
        if wid in keep_ids:
            name = next(k for k, v in target['outlines'].items() if v == wid)
            outlines[name] = {'xz': xz[:-1] if refs[0] == refs[-1] else xz}
        elif not (kind and near): continue
        elif kind == 'building' and (refs[0] != refs[-1] or len(refs) < 4): continue
        record = {'id': wid, 'version': int(w.get('version')), 'timestamp': w.get('timestamp'), 'tags': t,
                  'lat_lon': [[round(float(nodes[r].get('lat')), 7), round(float(nodes[r].get('lon')), 7)] for r in refs]}
        selected.append(record)
        if wid in keep_ids: continue
        feature = {'id': wid, 'kind': kind, 'pts': [[round(x, 2), round(z, 2)] for x, z in xz]}
        for key in ('name:en', 'name'):
            if key in t: feature['name'] = t[key]; break
        if 'width' in t:
            try: feature['width'] = float(t['width'].split()[0])
            except ValueError: pass
        if 'height' in t:
            try: feature['height'] = float(t['height'].split()[0])
            except ValueError: pass
        if kind == 'steps' and 'incline' in t: feature['incline'] = t['incline']
        if kind == 'cemetery' and 'religion' in t: feature['religion'] = t['religion']
        if kind == 'path' and t.get('area') == 'yes' and refs[0] == refs[-1]: feature['area'] = True
        if kind == 'building':
            levels = number(t.get('building:levels', ''))
            if feature.get('height') is None and levels: feature['height'] = round(levels * 3.2 + (number(t.get('roof:height', '')) or 0), 1)
            for key, out in (('min_height', 'minHeight'), ('roof:height', 'roofHeight')):
                if number(t.get(key, '')) is not None: feature[out] = number(t[key])
            if t.get('roof:shape') in ('dome', 'pyramidal'): feature['roofShape'] = t['roof:shape']
            if t.get('roof:colour', '').startswith('#'): feature['roofColour'] = t['roof:colour']
            if t.get('building:part', 'no') != 'no': feature['part'] = True
        projected.append(feature)
    missing = set(target['outlines']) - set(outlines)
    if missing: sys.exit(f'outlines not in the extract: {sorted(missing)}')
    at = terrain_sampler(target['place'])
    corners = {k: pos[v] for k, v in target.get('corners', {}).items() if v in pos}
    if set(corners) != set(target.get('corners', {})): sys.exit('corner nodes not in the extract')
    for k, v in target.get('corners', {}).items():
        n = nodes[v]; selected.append({'id': 'n' + v, 'version': int(n.get('version')), 'timestamp': n.get('timestamp'), 'tags': {}, 'role': f'{k} corner', 'lat_lon': [[float(n.get('lat')), float(n.get('lon'))]]})
    registration = kidron_registration(outlines, at) if args.name == 'kidron' else great_sea_registration(corners) if corners else None

    ARCHIVE.mkdir(parents=True, exist_ok=True); MIRROR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    record = {'source': 'OpenStreetMap API 0.6 map call', 'bbox': args.bbox, 'retrieved': today,
              'osm_file_sha256': sha256(args.osm), 'generator': root.get('generator'),
              'licence': LICENCE, 'place': target['place'], 'plan': target['plan'],
              'frame': 'x east, z south, metres from the place anchor in the MapLibre Mercator frame',
              'selection': f'ways classified as context (steps, paths, city walls, retaining walls, cemeteries, gate buildings, buildings and building parts) with any vertex within {args.radius:g} m of ({cx:g}, {cz:g}); plus the monument outlines or corner nodes used for registration',
              'counts': {k: sum(1 for f in projected if f['kind'] == k) for k in sorted({f['kind'] for f in projected})},
              'registration': registration, 'elements': selected}
    (ARCHIVE / f'{args.name}.json').write_text(json.dumps(record, ensure_ascii=False, indent=1) + '\n')
    (MIRROR / f'{args.name}.json').write_bytes((ARCHIVE / f'{args.name}.json').read_bytes())
    out = json.loads(OUT.read_text()) if OUT.exists() else {'licence': LICENCE, 'plans': {}}
    out['plans'][target['plan']] = {'place': target['place'], 'retrieved': today, 'record': f'research/assets/plans/osm-context-2026-10-22/{args.name}.json',
                                    'registration': registration, 'features': projected}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(json.dumps({'features': record['counts'], 'registration': registration}, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
