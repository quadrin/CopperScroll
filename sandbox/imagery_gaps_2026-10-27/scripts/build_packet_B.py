"""Stage B packet (RUN ONLY IF STAGE A PASSES; see score_A.py). Same tile size/scale/instructions as Stage A.
B1 is read from the Stage A answers (the Stage A known tiles already cover 0-30 m east of L71, the Hyrcania double
pool and the Samra enclosure; the scorer marked every fissure there).
B2 Kh. Nabbuh (WBADB S1396 / S1375): every 150 m tile (grid anchored on S1396) that meets the union of the two
   east wedges (bearing 45-135 deg, r <= 500 m) of the two points -> 36 tiles.
B3 Jisr Abu Ghabush: no published coordinates (Taha 2020 p. 277: 'southern bank of Wadi Nueima, c. 3 km north of
   Jericho'), so no tile can be placed on it -> B3 = unknown; no tiles cut (see report).
Decoys: 8 tiles of Samaria-highland terrain 2-6 km from Nabbuh with no WBADB site point within 300 m, mixed in so
   the scorer cannot tell which tiles matter; their pool marks are reported as an exploratory false-pool rate."""
import json, math, random, sys, pathlib, hashlib, datetime, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import Frame, dist_m
import esri

RUN = pathlib.Path(__file__).parent.parent
SCR = RUN.parent
PACKET = SCR / 'blind_packet_B'
SIZE_M, PX = 150.0, 600
rng = random.Random(int('d735f2cf', 16) + 2)
S1396 = (32.07958850686579, 35.33942735586948)   # Palestine grid 182200/165150 (EPSG:28191 -> WGS84, pyproj)
S1375 = (32.082290466476614, 35.342608943814874)  # 182500/165450
f = Frame(*S1396)
p2 = f.xz(*S1375)


def inwedge(x, z, ox, oz):
    dx, dz = x - ox, z - oz; r = math.hypot(dx, dz)
    if r > 500: return False
    if r == 0: return True
    b = math.degrees(math.atan2(dx, -dz)) % 360
    return 45 <= b <= 135


tiles = []
for i in range(-1, 8):
    for j in range(-8, 8):
        x0, z0 = i * SIZE_M, j * SIZE_M
        if any(inwedge(x0 + a * SIZE_M / 10, z0 + b * SIZE_M / 10, 0, 0) or inwedge(x0 + a * SIZE_M / 10, z0 + b * SIZE_M / 10, *p2)
               for a in range(11) for b in range(11)):
            tiles.append({'slot': f'N{i}_{j}', 'kind': 'B2-target', 'site': 'Kh. Nabbuh east wedge',
                          'grid': [i, j], 'centre': list(f.latlon(x0 + SIZE_M / 2, z0 + SIZE_M / 2))})
sites = json.load(open(RUN / 'out/site_points.json'))
cands = [s for s in sites if abs(s['lat'] - S1396[0]) < 0.1 and abs(s['lon'] - S1396[1]) < 0.1]
for k in range(8):
    for attempt in range(20000):
        r, b = rng.uniform(2000, 6000), rng.uniform(0, 360)
        lat, lon = f.latlon(r * math.sin(math.radians(b)), -r * math.cos(math.radians(b)))
        if any(dist_m(lat, lon, s['lat'], s['lon']) < 300 for s in cands): continue
        if any(dist_m(lat, lon, *t['centre']) < 400 for t in tiles): continue
        break
    tiles.append({'slot': f'DEC{k}', 'kind': 'decoy', 'site': 'Samaria highland decoy', 'centre': [lat, lon]})

letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
codes = set()
while len(codes) < len(tiles): codes.add(''.join(rng.choice(letters) for _ in range(2)) + str(rng.randint(10, 99)))
codes = sorted(codes); rng.shuffle(codes)
for t, c in zip(tiles, codes): t['code'] = c
if PACKET.exists(): shutil.rmtree(PACKET)
PACKET.mkdir()
for t in tiles:
    im, meta = esri.cut(*t['centre'], SIZE_M, PX)
    im.save(PACKET / f"tile_{t['code']}.png", optimize=True)
    t['cut'] = {'native_m_per_px': round(meta['native_m_per_px'], 4), 'esri_z18_tiles': meta['tiles']}
order = sorted(t['code'] for t in tiles)
instr = (SCR / 'blind_packet_A/INSTRUCTIONS.txt').read_text()
instr = instr.replace('The folder holds 10 aerial', f'The folder holds {len(tiles)} aerial')
instr = instr.split('List every tile code')[0] + 'List every tile code, including tiles with no marks: ' + ', '.join(order) + '.\n'
(PACKET / 'INSTRUCTIONS.txt').write_text(instr)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
key = {'stage': 'B', 'created_utc': now, 'S1396': S1396, 'S1375': S1375, 'S1375_xz_from_S1396': p2, 'tiles': tiles,
       'packet_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PACKET.iterdir())}}
kp = RUN / 'key/key_B.json'; kp.write_text(json.dumps(key, indent=1))
print('key_B sha256', hashlib.sha256(kp.read_bytes()).hexdigest(), now, len(tiles), 'tiles; esri cached', len(list((RUN / 'dl/esri18').iterdir())))
