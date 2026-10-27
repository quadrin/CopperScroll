"""Score Stage B2 (Kh. Nabbuh): pass if any mark typed pool (alt: pool or cistern mouth) lies inside the union
of the two east wedges (bearing 45-135 deg, <= 500 m from S1396 or S1375). Not seen -> 'weak fail' only if the
Stage A pool detection rate >= 0.8 (from out/score_A.json), else unknown. Decoy pool marks reported separately.
Usage: python3 -I score_B.py answers/answers_B.json"""
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import Frame
import esri
RUN = pathlib.Path(__file__).parent.parent
key = json.load(open(RUN / 'key/key_B.json')); ans = json.load(open(sys.argv[1]))
sa = json.load(open(RUN / 'out/score_A.json'))
marks = {t['code']: t.get('marks') or [] for t in ans['tiles']}
f = Frame(*key['S1396']); p2 = key['S1375_xz_from_S1396']


def inwedge(x, z, ox, oz):
    dx, dz = x - ox, z - oz; r = math.hypot(dx, dz)
    if r > 500: return False
    b = math.degrees(math.atan2(dx, -dz)) % 360
    return r == 0 or 45 <= b <= 135


hits, hits2, decoy = [], [], {}
for t in key['tiles']:
    for i, m in enumerate(marks.get(t['code'], [])):
        ty = (m.get('type') or '').lower()
        if t['kind'] == 'decoy':
            decoy.setdefault(t['code'], []).append(ty); continue
        lat, lon = esri.latlon_of_px(float(m['x']), float(m['y']), *t['centre'], 150.0, 600)
        x, z = f.xz(lat, lon)
        w = [n for n, (ox, oz) in (('S1396', (0, 0)), ('S1375', p2)) if inwedge(x, z, ox, oz)]
        if not w: continue
        rec = {'tile': t['code'], 'mark': i, 'type': ty, 'conf': m.get('confidence'), 'wedges': w, 'xz_from_S1396': [round(x), round(z)], 'note': m.get('note')}
        if ty == 'pool': hits.append(rec)
        if ty in ('pool', 'cistern mouth', 'cistern'): hits2.append(rec)
rate = sa['detection_rate']['pool']
res = {'B2_main': 'pass' if hits else ('weak fail' if rate >= 0.8 else 'unknown'), 'B2_alt_pool_or_cistern': 'pass' if hits2 else ('weak fail' if rate >= 0.8 else 'unknown'),
       'pool_detection_rate_stageA': rate, 'hits': hits, 'hits_alt': hits2,
       'decoy_marks': decoy, 'decoy_pool_mean': sum(v.count('pool') for v in decoy.values()) / max(1, len([t for t in key['tiles'] if t['kind'] == 'decoy']))}
json.dump(res, open(RUN / 'out/score_B.json', 'w'), indent=1); print(json.dumps(res, indent=1))
