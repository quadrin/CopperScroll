"""Stage A known features (fixed by RULE.md), positioned from repo records. Writes out/known_features.json."""
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import Frame, rot_cw

REPO = pathlib.Path('/home/claude/copperscroll')
OUT = pathlib.Path(__file__).parent.parent / 'out'

feats = []

# --- Qumran: traced plan of M&P 2018 Fig. 9 placed by imagery-registration-2026-10-22/qumran.json
reg = json.load(open(REPO / 'research/assets/plans/imagery-registration-2026-10-22/qumran.json'))
plan = json.load(open(REPO / 'research/models/traced_plans/qumran-settlement.json'))
anchor = reg['anchor']; fq = Frame(*anchor)
target = reg['placement']['target']; turn = reg['figures'][0]['fit']['turnDegClockwise']  # -0.6
els = {e['id']: e for e in plan['elements']}


def q_place(x, z):
    rx, rz = rot_cw(x, z, turn)
    return target[0] + rx, target[1] + rz


def poly_centroid(pts):
    a = cx = cz = 0
    for (x0, z0), (x1, z1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * z1 - x1 * z0; a += c; cx += (x0 + x1) * c; cz += (z0 + z1) * c
    a /= 2
    return cx / (6 * a), cz / (6 * a)


galor = {'L71': ['L71'], 'L56/58': ['L56', 'L58'], 'L91': ['L91'], 'L110': ['L110'], 'L48/49': ['L48-L49'],
         'L117': ['L117'], 'L118': ['L118'], 'L138': ['L138']}
for fid, parts in galor.items():
    polys = []; cents = []
    for p in parts:
        g = els[p]['geometry']
        if g['type'] == 'point':  # L110 round cistern, radius 2.31 m (inner)
            cx, cz = g['at']; r = g['radius']
            pts = [(cx + r * math.cos(t / 16 * 2 * math.pi), cz + r * math.sin(t / 16 * 2 * math.pi)) for t in range(16)]
        else:
            pts = [tuple(v) for v in g['points']]
        pl = [q_place(*v) for v in pts]
        polys.append([list(fq.latlon(*v)) for v in pl])
        cents.append(poly_centroid(pl) if g['type'] != 'point' else q_place(*g['at']))
    cx = sum(c[0] for c in cents) / len(cents); cz = sum(c[1] for c in cents) / len(cents)
    feats.append({'id': 'QUM-' + fid, 'site': 'Kh. Qumran', 'type': 'pool' if fid != 'L110' else 'cistern',
                  'centre': list(fq.latlon(cx, cz)), 'footprints': polys,
                  'source': 'Magen & Peleg 2018 Fig. 9 traced (research/models/traced_plans/qumran-settlement.json) placed by imagery-registration-2026-10-22/qumran.json (L110 at place (-67.5,63.0), turn -0.6 deg); unc. ~2 m + imagery 5 m'})

# --- Hyrcania: double pool from imagery-registration-2026-10-22/hyrcania.json positions (Patrich 1989 Fig. 22)
hy = json.load(open(REPO / 'research/assets/plans/imagery-registration-2026-10-22/hyrcania.json'))
fh = Frame(*hy['anchor']); P = hy['positions']
feats.append({'id': 'HYR-doublepool', 'site': 'Hyrcania', 'type': 'pool',
              'centre': list(fh.latlon(*P['doublePoolCentre'])),
              'members': [list(fh.latlon(*P['northMemberCentre'])), list(fh.latlon(*P['southMemberCentre']))],
              'source': 'Patrich 1989 Fig. 22 p. 256 registered (hyrcania.json positions.doublePoolCentre, members); unc. ~3 m + imagery 5 m'})
# --- dam 44: Mar Saba map (Patrich 1994) Site 48 IAA online point
feats.append({'id': 'HYR-dam44', 'site': 'Naḥal Sekhakha (Hyrcania N aqueduct head)', 'type': 'dam',
              'centre': [31.7272578252728, 35.3548919289433],
              'source': 'ASI Map of Mar Saba (Patrich 1994) Site 48 IAA online point (sandbox run 7 out/marsaba_sites_dist.json n=48); dam 17.5 m long (Patrich 1989 p. 251); point precision not stated'})
json.dump(feats, open(OUT / 'known_features_partial.json', 'w'), indent=1, ensure_ascii=False)
for f in feats: print(f['id'], ['%.6f' % v for v in f['centre']])
