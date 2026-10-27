"""Stage A: choose tiles (seeded from the RULE.md SHA-256), cut them, code them, write the blind packet
(images + neutral instructions only) and the key (kept out of the packet)."""
import json, math, random, sys, pathlib, hashlib, datetime, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import Frame, rot_cw, dist_m
import esri

RUN = pathlib.Path(__file__).parent.parent
SCR = RUN.parent
PACKET = SCR / 'blind_packet_A'          # the ONLY folder the scorer is given
SIZE_M, PX = 150.0, 600                  # 150 m square, 0.25 m per display pixel (native imagery 0.5 m)
RULE_SHA = 'd735f2cf240a44323b800a6469d7c77f1aaa900ddc124a23607a4409dd7ad809'
rng = random.Random(int(RULE_SHA[:8], 16))

feats = {f['id']: f for f in json.load(open(RUN / 'out/known_features_partial.json'))}
sites = json.load(open(RUN / 'out/site_points.json'))

# Qumran place frame (registration anchor) for the west/east split at plan x = 15.07 (between L91 and L56)
reg = json.load(open('/home/claude/copperscroll/research/assets/plans/imagery-registration-2026-10-22/qumran.json'))
fq = Frame(*reg['anchor'])
split_x = reg['placement']['target'][0] + 15.07          # place-frame x of the split (turn -0.6 deg negligible here)
zmid = reg['placement']['target'][1] + 13.0               # plan z mid of the 8 pools (-35..61) -> 13
tiles = []
for name, cx in (('QW', split_x - SIZE_M / 2), ('QE', split_x + SIZE_M / 2)):
    cz = zmid + rng.uniform(-15, 15)
    tiles.append({'slot': name, 'kind': 'known', 'site': 'Kh. Qumran', 'centre': list(fq.latlon(cx, cz))})


def offset(lat, lon, dx, dz):
    f = Frame(lat, lon); return list(f.latlon(dx, dz))


hp = feats['HYR-doublepool']['centre']
tiles.append({'slot': 'HP', 'kind': 'known', 'site': 'Hyrcania', 'centre': offset(*hp, rng.uniform(-30, 30), rng.uniform(-30, 30))})
d44 = feats['HYR-dam44']['centre']
tiles.append({'slot': 'D44', 'kind': 'known', 'site': 'Nahal Sekhakha dam 44', 'centre': offset(*d44, rng.uniform(-30, 30), rng.uniform(-30, 30))})
SAMRA_C = [31.716862483, 35.392041313]   # integrator's estimate of the Kh. es-Samra enclosure centre on the imagery (see key note)
tiles.append({'slot': 'SAM', 'kind': 'known', 'site': 'Kh. es-Samra', 'centre': offset(*SAMRA_C, rng.uniform(-25, 25), rng.uniform(-25, 25))})

# Controls: similar terrain, no recorded site point within 300 m of the tile centre (WBADB surveyed+excavations, Mar Saba map)
zones = [
    ('CQ1', 'Qumran-type marl terrace / cliff foot', (31.715, 31.785), (35.440, 35.468), [((31.7412, 35.4591), 500)]),
    ('CQ2', 'Qumran-type marl terrace / cliff foot', (31.715, 31.785), (35.440, 35.468), [((31.7412, 35.4591), 500)]),
    ('CB', 'Buqeia hills (Samra-type)', (31.690, 31.740), (35.375, 35.415), []),
    ('CH', 'hill slopes round Hyrcania', (31.700, 31.738), (35.345, 35.385), [((31.7188, 35.3652), 600)]),
    ('CW', 'upper Nahal Sekhakha / wadi slopes (dam-44-type)', (31.720, 31.745), (35.320, 35.356), [((31.727258, 35.354892), 400)]),
]
cands = [s for s in sites if 31.6 < s['lat'] < 31.85 and 35.25 < s['lon'] < 35.55]
chosen = []
for slot, terr, (la0, la1), (lo0, lo1), extra in zones:
    for attempt in range(5000):
        lat, lon = rng.uniform(la0, la1), rng.uniform(lo0, lo1)
        if any(dist_m(lat, lon, *p) < r for p, r in extra): continue
        if any(dist_m(lat, lon, *c) < 400 for c in chosen): continue   # controls must not overlap each other
        if any(dist_m(lat, lon, s['lat'], s['lon']) < 300 for s in cands): continue
        if any(dist_m(lat, lon, *t['centre']) < 400 for t in tiles): continue
        break
    else:
        raise SystemExit('no control for ' + slot)
    chosen.append((lat, lon))
    near = min(cands, key=lambda s: dist_m(lat, lon, s['lat'], s['lon']))
    tiles.append({'slot': slot, 'kind': 'control', 'site': terr, 'centre': [lat, lon], 'attempts': attempt + 1,
                  'nearest_site_point': {'src': near['src'], 'id': near['id'], 'm': round(dist_m(lat, lon, near['lat'], near['lon']))}})

# Codes and order
letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
codes = set()
while len(codes) < len(tiles):
    codes.add(''.join(rng.choice(letters) for _ in range(2)) + str(rng.randint(10, 99)))
codes = sorted(codes); rng.shuffle(codes)
for t, c in zip(tiles, codes): t['code'] = c

if PACKET.exists(): shutil.rmtree(PACKET)
PACKET.mkdir()
for t in tiles:
    im, meta = esri.cut(*t['centre'], SIZE_M, PX)
    im.save(PACKET / f"tile_{t['code']}.png", optimize=True)   # PIL writes no geo metadata
    t['cut'] = {'native_m_per_px': round(meta['native_m_per_px'], 4), 'display_m_per_px': meta['out_m_per_px'], 'esri_z18_tiles': meta['tiles']}
    t['features_px'] = []
    for fid, f in feats.items():
        c, r = esri.px_of(*f['centre'], *t['centre'], SIZE_M, PX)
        if -40 <= c <= PX + 40 and -40 <= r <= PX + 40:
            entry = {'id': fid, 'type': f['type'], 'px': [round(c, 1), round(r, 1)]}
            if 'footprints' in f:
                entry['footprints_px'] = [[[round(v, 1) for v in esri.px_of(la, lo, *t['centre'], SIZE_M, PX)] for la, lo in poly] for poly in f['footprints']]
            if 'members' in f:
                entry['members_px'] = [[round(v, 1) for v in esri.px_of(la, lo, *t['centre'], SIZE_M, PX)] for la, lo in f['members']]
            t['features_px'].append(entry)
    if t['slot'] == 'SAM':
        t['features_px'].append({'id': 'SAM-cistern-enclosure-estimate', 'type': 'cistern (open, 18x22 m)',
                                 'px': [round(v, 1) for v in esri.px_of(*SAMRA_C, *t['centre'], SIZE_M, PX)],
                                 'note': 'NOT a 10 m position: integrator estimate of the enclosure centre from imagery; C&M p. 11 put the cistern in the SW quarter of a ~68x40 m enclosure. Scored only in the alternative count (pool/cistern mark within 30 m of this point).'})

order = sorted(tiles, key=lambda t: t['code'])
instr = f"""Imagery reading task

The folder holds {len(tiles)} aerial image tiles (files tile_XXNN.png). Each tile is a north-up
satellite image, {PX} x {PX} pixels, covering {SIZE_M:.0f} m x {SIZE_M:.0f} m of ground
({SIZE_M/PX:.2f} m per pixel; the source imagery is about 0.5 m resolution, so fine detail is soft).
Pixel (0,0) is the top-left (north-west) corner; x increases to the east (right), y to the south (down).

For each tile, mark every one of the following that you can see:
  - pool        (an open, built or rock-cut basin or reservoir, any size)
  - cistern mouth (an opening or shaft into an underground cistern)
  - stair       (a flight of steps; give the direction in which it descends, as a compass bearing, if you can)
  - fissure     (a crack or cleft in rock)
  - other       (any other water installation or rock-cut feature you think is relevant; describe it)

For each mark give: tile code, type, pixel position (x, y) of its centre (for a fissure or stair,
also the two end points), approximate size in metres, confidence from 0 to 1, and a short note.
Mark only what you can see in the image. Mark nothing where you see nothing; an empty tile is a
valid answer. Do not use any outside information or try to find where the tiles are.

Return your answers as JSON in exactly this form:
{{"scorer_notes": "...",
  "tiles": [
    {{"code": "XX00", "marks": [
       {{"type": "pool", "x": 0, "y": 0, "ends": null, "size_m": "5 x 3", "descends_bearing_deg": null, "confidence": 0.0, "note": ""}}
    ]}}
  ]}}
List every tile code, including tiles with no marks: {', '.join(t['code'] for t in order)}.
"""
(PACKET / 'INSTRUCTIONS.txt').write_text(instr)

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
key = {'run': 'imagery_gaps_2026-10-27', 'stage': 'A', 'created_utc': now, 'rule_sha256': RULE_SHA,
       'tile_size_m': SIZE_M, 'tile_px': PX, 'imagery': 'Esri World Imagery z18; identify metadata at QUM, HP, D44, SAM: Vantor WV02 2023-10-21, 0.5 m, stated accuracy 5 m',
       'tiles': tiles, 'packet_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PACKET.iterdir())},
       'esri_tiles_fetched_this_run_so_far': len(list((RUN / 'dl/esri18').iterdir()))}
kp = RUN / 'key' / 'key_A.json'
kp.write_text(json.dumps(key, indent=1, ensure_ascii=False))
print('key sha256', hashlib.sha256(kp.read_bytes()).hexdigest(), now)
for t in tiles: print(t['code'], t['slot'], t['kind'], [round(v, 6) for v in t['centre']], [f['id'] for f in t['features_px']], t.get('nearest_site_point', ''))
