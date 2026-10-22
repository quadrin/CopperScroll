#!/usr/bin/env python3
"""Project OpenStreetMap context features around an atlas site into the site's model frame.

    python3 -I tools/build_osm_context.py <name> <osm.xml> [--radius 450] [--centre X,Z]

<name> is a key in TARGETS below. The OSM file is a map-call extract from the OSM API
(https://api.openstreetmap.org/api/0.6/map?bbox=...), passed as an argument (an untrusted download).

Writes:
- research/assets/plans/osm-context-2026-10-22/<name>.json: the selected OSM elements (ids,
  versions, timestamps, tags, lat/lon), under the ODbL, with an identical atlas/research mirror;
- atlas/public/context/<name>.json: the same features projected to the place frame (metres, x east,
  z south, MapLibre Mercator frame at the place anchor, as tools/build_wide_terrain.py and
  atlas/app/atlas-map-site-layer.ts); the atlas loads it with the terrain;
- atlas/app/atlas-site-context.json: per plan, the place, the record, the features file and the
  placement (registration) the model builder needs.

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
    'kidron': {'plans': ['kidron-bene-hezir'], 'place': 'jer_kidron_mon',
               'outlines': {'bene-hezir': 'w288284732', 'zechariah': 'w288284733', 'absalom': 'w137729556'}},
    # The south-west and south-east corners of the Haram enclosure (relation 5862584, Temple Mount).
    'great-sea': {'plans': ['temple-great-sea'], 'place': 'jer_temple', 'outlines': {},
                  'corners': {'sw': '29979854', 'se': '2915691228'}},
    # The mapped outline of the excavated settlement (way 611895589, 'Qumran').
    'qumran': {'plans': ['qumran-settlement'], 'place': 'kh_qumran', 'outlines': {'site': 'w611895589'}, 'placement': 'site'},
    # The mapped excavation area of the pools (way 126864878, 'Pool of Bethesda').
    'bethesda': {'plans': ['bethesda-pools'], 'place': 'jer_bethesda', 'outlines': {'site': 'w126864878'}, 'placement': 'site'},
    # The mapped Golden Gate building (way 291836693): its centre and the bearing of its long sides.
    'golden-gate': {'plans': ['east-gate-warren'], 'place': 'jer_east_gate', 'outlines': {'gate': 'w291836693'}, 'placement': 'gate'},
    # No mapped outline that a model point can be tied to: the models stay at the place anchor.
    'jericho': {'plans': ['jericho-early', 'jericho-late'], 'place': 'jericho_palaces', 'outlines': {}, 'placement': 'anchor'},
    'gerizim': {'plans': ['gerizim-precinct'], 'place': 'gerizim', 'outlines': {}, 'placement': 'anchor'},
    'hyrcania': {'plans': ['hyrcania-waterworks'], 'place': 'hyrcania', 'outlines': {}, 'placement': 'anchor'},
}
FEATURES = REPO / 'atlas/public/context'
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
    if hw in ROAD_CLASSES or (hw or '').endswith('_link'): return 'road'
    if barrier == 'city_wall' or historic == 'citywalls': return 'wall'
    if barrier == 'retaining_wall': return 'retaining-wall'
    if tags.get('landuse') == 'cemetery' or tags.get('amenity') == 'grave_yard': return 'cemetery'
    if historic == 'city_gate' and 'building' in tags: return 'gate'
    if tags.get('building', 'no') not in ('no', 'roof', 'wall', 'construction', 'ruins') or tags.get('building:part', 'no') != 'no': return 'building'
    if cover(tags): return 'green'
    return None


ROAD_CLASSES = ('motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'living_street', 'service')


def cover(tags):
    """Planted or green ground: 'wood' (forest, wood, tree groups), 'orchard', or 'grass'."""
    landuse, natural, leisure = tags.get('landuse'), tags.get('natural'), tags.get('leisure')
    if landuse == 'forest' or natural in ('wood', 'tree_group'): return 'wood'
    if landuse == 'orchard': return 'orchard'
    if landuse in ('grass', 'meadow', 'village_green') or natural in ('scrub', 'grassland', 'heath') or leisure in ('park', 'garden'): return 'grass'
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


def area_centroid(pts):
    a = cx = cz = 0.0
    for (x0, z0), (x1, z1) in zip(pts, pts[1:] + pts[:1]):
        k = x0 * z1 - x1 * z0; a += k; cx += (x0 + x1) * k; cz += (z0 + z1) * k
    return (cx / (3 * a), cz / (3 * a)) if abs(a) > 1e-9 else (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def site_registration(outline):
    """A model point is placed on the area centroid of a mapped outline; the model is not turned."""
    c = area_centroid(outline); xs = [p[0] for p in outline]; zs = [p[1] for p in outline]
    return {'target': [round(c[0], 2), round(c[1], 2)], 'rotationDeg': 0, 'outlineSize_m': [round(max(xs) - min(xs), 1), round(max(zs) - min(zs), 1)],
            'method': 'A chosen model point is placed on the area centroid of the mapped outline; the model keeps its own orientation.'}


def gate_registration(outline):
    """The gatehouse centre on the mapped building's centroid, turned so that its long axis (the model's x
    axis) runs along the mapped building's long sides."""
    c = area_centroid(outline); sides = [(outline[i], outline[(i + 1) % len(outline)]) for i in range(len(outline))]
    longest = max(sides, key=lambda s: math.dist(*s)); b = bearing(*longest) % 180
    turn = (90 - b + 90) % 180 - 90
    return {'target': [round(c[0], 2), round(c[1], 2)], 'rotationDeg': round(turn, 1), 'longSideBearing': round(b, 1),
            'method': "The model's gatehouse centre is placed on the mapped Golden Gate building's centroid and the model is turned so that its gatehouse runs along the building's longest side."}


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
        elif kind in ('building', 'green') and (refs[0] != refs[-1] or len(refs) < 4): continue
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
        if kind == 'road': feature['road'] = t['highway'].removesuffix('_link')
        if kind == 'green': feature['cover'] = cover(t)
        if kind == 'building':
            levels = number(t.get('building:levels', ''))
            if feature.get('height') is None and levels: feature['height'] = round(levels * 3.2 + (number(t.get('roof:height', '')) or 0), 1)
            for key, out in (('min_height', 'minHeight'), ('roof:height', 'roofHeight')):
                if number(t.get(key, '')) is not None: feature[out] = number(t[key])
            if t.get('roof:shape') in ('dome', 'pyramidal'): feature['roofShape'] = t['roof:shape']
            if t.get('roof:colour', '').startswith('#'): feature['roofColour'] = t['roof:colour']
            if t.get('building:part', 'no') != 'no': feature['part'] = True
        projected.append(feature)
    # Mapped single trees (nodes).
    for n in root.iter('node'):
        t = tags(n)
        if t.get('natural') != 'tree': continue
        x, z = pos[n.get('id')]
        if math.hypot(x - cx, z - cz) > args.radius: continue
        selected.append({'id': 'n' + n.get('id'), 'version': int(n.get('version')), 'timestamp': n.get('timestamp'), 'tags': t,
                         'lat_lon': [[round(float(n.get('lat')), 7), round(float(n.get('lon')), 7)]]})
        feature = {'id': 'n' + n.get('id'), 'kind': 'tree', 'pts': [[round(x, 2), round(z, 2)]]}
        if t.get('leaf_type') in ('needleleaved', 'broadleaved'): feature['leafType'] = t['leaf_type']
        projected.append(feature)
    missing = set(target['outlines']) - set(outlines)
    if missing: sys.exit(f'outlines not in the extract: {sorted(missing)}')
    at = terrain_sampler(target['place'])
    corners = {k: pos[v] for k, v in target.get('corners', {}).items() if v in pos}
    if set(corners) != set(target.get('corners', {})): sys.exit('corner nodes not in the extract')
    for k, v in target.get('corners', {}).items():
        n = nodes[v]; selected.append({'id': 'n' + v, 'version': int(n.get('version')), 'timestamp': n.get('timestamp'), 'tags': {}, 'role': f'{k} corner', 'lat_lon': [[float(n.get('lat')), float(n.get('lon'))]]})
    placement = target.get('placement')
    if args.name == 'kidron': registration = kidron_registration(outlines, at)
    elif corners: registration = great_sea_registration(corners)
    elif placement == 'site': registration = site_registration(outlines['site']['xz'])
    elif placement == 'gate': registration = gate_registration(outlines['gate']['xz'])
    else: registration = {'target': [0, 0], 'rotationDeg': 0, 'placement': 'anchor', 'method': "Not registered: no mapped outline can be tied to a model point, so the model stays at the place anchor with the anchor's precision."}
    # A placement registered to satellite imagery (tools/imagery_registration.py apply) is kept: it is
    # finer than an outline centroid or the anchor.
    if OUT.exists():
        previous = json.loads(OUT.read_text())['plans'].get(target['plans'][0], {}).get('registration') or {}
        if previous.get('placement') == 'imagery': registration = previous

    ARCHIVE.mkdir(parents=True, exist_ok=True); MIRROR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    record = {'source': 'OpenStreetMap API 0.6 map call', 'bbox': args.bbox, 'retrieved': today,
              'osm_file_sha256': sha256(args.osm), 'generator': root.get('generator'),
              'licence': LICENCE, 'place': target['place'], 'plans': target['plans'],
              'frame': 'x east, z south, metres from the place anchor in the MapLibre Mercator frame',
              'selection': f'ways classified as context (steps, paths, roads, city walls, retaining walls, cemeteries, gate buildings, buildings and building parts, woods, orchards and grass) and mapped single trees with any vertex within {args.radius:g} m of ({cx:g}, {cz:g}); plus the monument outlines or corner nodes used for registration',
              'counts': {k: sum(1 for f in projected if f['kind'] == k) for k in sorted({f['kind'] for f in projected})},
              'registration': registration, 'elements': selected}
    (ARCHIVE / f'{args.name}.json').write_text(json.dumps(record, ensure_ascii=False, indent=1) + '\n')
    (MIRROR / f'{args.name}.json').write_bytes((ARCHIVE / f'{args.name}.json').read_bytes())
    FEATURES.mkdir(parents=True, exist_ok=True)
    (FEATURES / f'{args.name}.json').write_text(json.dumps({'licence': LICENCE, 'retrieved': today, 'place': target['place'], 'features': projected}, ensure_ascii=False, separators=(',', ':')) + '\n')
    out = json.loads(OUT.read_text()) if OUT.exists() else {'licence': LICENCE, 'plans': {}}
    for plan in target['plans']:
        out['plans'][plan] = {'place': target['place'], 'retrieved': today, 'record': f'research/assets/plans/osm-context-2026-10-22/{args.name}.json',
                              'features': f'context/{args.name}.json', 'counts': record['counts'], 'registration': registration}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps({'features': record['counts'], 'registration': registration}, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
