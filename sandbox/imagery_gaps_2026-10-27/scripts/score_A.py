"""Score the blind scorer's Stage A answers against key_A.json. Frozen before the scorer runs.
Usage: python3 -I score_A.py answers_A.json  -> out/score_A.json + printed summary.

Definitions (fixed before any answer was seen):
 MAIN  feature set = the 10 features with record positions: 8 Qumran pools (Galor) + Hyrcania double pool + dam 44.
       found = at least one mark of any type in any tile within 10 m of the feature's key centre.
 ALT-F footprint: within 10 m of the drawn footprint (Qumran polygons) or of either double-pool member centre.
 ALT-T type: only marks typed pool / cistern mouth count (dam 44: also 'other').
 ALT-C confidence >= 0.5 only.
 SAMRA (alt only, no 10 m position on record): a pool or cistern-mouth mark within 30 m of the integrator's
       enclosure estimate; 11-feature counts reported against >=6 (literal) and >=7 (60 %).
 False pools: marks typed 'pool' in control tiles; mean per control tile must be < 1 (ALT: pool + cistern mouth).
 STAGE A PASS = MAIN found >= 6 AND mean false pools per control < 1.
 Detection rate by type (for the >=80 % weak-fail clause): pools = 7 Qumran pools + double pool (8); cistern = L110 (1);
       dam = dam 44 (1). Stairs and fissures have no fixed calibration features -> rate unknown.
 B1 (read from the same answers, only if Stage A passes): a fissure mark (centre or an end) lying 0-30 m east of the
       feature's eastern edge (L71 footprint; double pool members' east edge taken as member centre + 6 m) and within
       the feature's north-south extent +/- 15 m. Seen -> pass; not seen -> unknown (fissure detection uncalibrated).
       Samra: no record position -> unknown unless a fissure mark lies 0-30 m east of the enclosure estimate +/- 30 m N-S (reported, flagged).
"""
import json, math, sys, pathlib
RUN = pathlib.Path(__file__).parent.parent
key = json.load(open(RUN / 'key/key_A.json'))
ans = json.load(open(sys.argv[1]))
PXM = key['tile_px'] / key['tile_size_m']  # px per metre (4)
tiles = {t['code']: t for t in key['tiles']}
marks = {}
for t in ans['tiles']:
    marks[t['code']] = t.get('marks') or []
missing = [c for c in tiles if c not in marks]

MAIN = ['QUM-L71', 'QUM-L56/58', 'QUM-L91', 'QUM-L110', 'QUM-L48/49', 'QUM-L117', 'QUM-L118', 'QUM-L138', 'HYR-doublepool', 'HYR-dam44']


def mtype(m): return (m.get('type') or '').strip().lower()


def pts_of(m):
    p = [(float(m['x']), float(m['y']))]
    if m.get('ends'):
        try: p += [(float(e[0]), float(e[1])) for e in m['ends']]
        except Exception: pass
    return p


def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def inside(p, poly):
    x, y = p; c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: c = not c
    return c


def poly_dist(p, poly):
    if inside(p, poly): return 0.0
    return min(seg_dist(p, a, b) for a, b in zip(poly, poly[1:] + poly[:1]))


res = {'missing_tiles_in_answers': missing, 'features': {}}
for fid in MAIN:
    best = {'MAIN': None, 'ALT-F': None, 'ALT-T': None, 'ALT-C': None}
    for code, t in tiles.items():
        for f in t['features_px']:
            if f['id'] != fid: continue
            for i, m in enumerate(marks.get(code, [])):
                p = (float(m['x']), float(m['y']))
                d = math.dist(p, f['px']) / PXM
                dF = d
                if 'footprints_px' in f: dF = min(poly_dist(p, poly) for poly in f['footprints_px']) / PXM
                if 'members_px' in f: dF = min([d] + [math.dist(p, q) / PXM for q in f['members_px']])
                rec = {'tile': code, 'mark': i, 'type': mtype(m), 'conf': m.get('confidence'), 'd_m': round(d, 1), 'dF_m': round(dF, 1)}
                okT = mtype(m) in ('pool', 'cistern mouth', 'cistern') or (fid == 'HYR-dam44' and mtype(m) == 'other')
                try: okC = float(m.get('confidence') or 0) >= 0.5
                except ValueError: okC = False
                for k, ok, dist in (('MAIN', True, d), ('ALT-F', True, dF), ('ALT-T', okT, d), ('ALT-C', okC, d)):
                    if ok and dist <= 10 and (best[k] is None or dist < best[k]['dist']):
                        best[k] = dict(rec, dist=round(dist, 1))
    res['features'][fid] = {k: v for k, v in best.items()}

counts = {k: sum(1 for f in MAIN if res['features'][f][k]) for k in ('MAIN', 'ALT-F', 'ALT-T', 'ALT-C')}
# Samra alternative
sam = None
for code, t in tiles.items():
    for f in t['features_px']:
        if f['id'] == 'SAM-cistern-enclosure-estimate':
            for i, m in enumerate(marks.get(code, [])):
                d = math.dist((float(m['x']), float(m['y'])), f['px']) / PXM
                if mtype(m) in ('pool', 'cistern mouth', 'cistern') and d <= 30 and (sam is None or d < sam['d_m']):
                    sam = {'tile': code, 'mark': i, 'type': mtype(m), 'd_m': round(d, 1), 'conf': m.get('confidence')}
res['samra_alt'] = sam
ctrl = [c for c, t in tiles.items() if t['kind'] == 'control']
fp = {c: sum(1 for m in marks.get(c, []) if mtype(m) == 'pool') for c in ctrl}
fp2 = {c: sum(1 for m in marks.get(c, []) if mtype(m) in ('pool', 'cistern mouth', 'cistern')) for c in ctrl}
res['false_pools_per_control'] = fp; res['false_pools_mean'] = sum(fp.values()) / len(ctrl)
res['false_pool_or_cistern_per_control'] = fp2; res['false_pool_or_cistern_mean'] = sum(fp2.values()) / len(ctrl)
res['control_marks_all_types'] = {c: [mtype(m) for m in marks.get(c, [])] for c in ctrl}
res['counts'] = counts
res['counts_11_with_samra'] = {k: v + (1 if sam else 0) for k, v in counts.items()}
res['stageA_pass_MAIN'] = counts['MAIN'] >= 6 and res['false_pools_mean'] < 1
res['stageA_pass_by_branch'] = {
    k: {'found': counts[k], 'pass_10_ge6': counts[k] >= 6 and res['false_pools_mean'] < 1,
        'pass_11_ge6': counts[k] + (1 if sam else 0) >= 6 and res['false_pools_mean'] < 1,
        'pass_11_ge7': counts[k] + (1 if sam else 0) >= 7 and res['false_pools_mean'] < 1,
        'pass_alt_false_def': counts[k] >= 6 and res['false_pool_or_cistern_mean'] < 1} for k in counts}
pools = ['QUM-L71', 'QUM-L56/58', 'QUM-L91', 'QUM-L48/49', 'QUM-L117', 'QUM-L118', 'QUM-L138', 'HYR-doublepool']
res['detection_rate'] = {'pool': sum(1 for f in pools if res['features'][f]['MAIN']) / len(pools),
                         'cistern(L110)': 1.0 if res['features']['QUM-L110']['MAIN'] else 0.0,
                         'dam': 1.0 if res['features']['HYR-dam44']['MAIN'] else 0.0,
                         'stair': None, 'fissure': None}

# B1 fissures east of the reservoirs (reported; valid only if Stage A passes)
b1 = {}
for fid in ('QUM-L71', 'HYR-doublepool', 'SAM-cistern-enclosure-estimate'):
    hits = []
    for code, t in tiles.items():
        for f in t['features_px']:
            if f['id'] != fid: continue
            if 'footprints_px' in f:
                xs = [v[0] for poly in f['footprints_px'] for v in poly]; ys = [v[1] for poly in f['footprints_px'] for v in poly]
                east, n, s = max(xs), min(ys), max(ys); ns = 15
            elif 'members_px' in f:
                east = max(q[0] for q in f['members_px']) + 6 * PXM; n = min(q[1] for q in f['members_px']) - 6 * PXM; s = max(q[1] for q in f['members_px']) + 6 * PXM; ns = 15
            else:
                east, n, s = f['px'][0], f['px'][1], f['px'][1]; ns = 30
            for i, m in enumerate(marks.get(code, [])):
                if mtype(m) != 'fissure': continue
                for p in pts_of(m):
                    dx = (p[0] - east) / PXM
                    if 0 <= dx <= 30 and n - ns * PXM <= p[1] <= s + ns * PXM:
                        hits.append({'tile': code, 'mark': i, 'dx_m': round(dx, 1), 'conf': m.get('confidence'), 'note': m.get('note')}); break
    b1[fid] = {'result': ('pass' if hits else 'unknown') if fid != 'SAM-cistern-enclosure-estimate' else ('flagged-seen' if hits else 'unknown'), 'hits': hits}
res['B1_from_stageA_answers'] = b1
json.dump(res, open(RUN / 'out/score_A.json', 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('counts', 'counts_11_with_samra', 'false_pools_per_control', 'false_pools_mean', 'stageA_pass_MAIN', 'detection_rate', 'samra_alt', 'missing_tiles_in_answers')}, indent=1))
for fid in MAIN: print(fid, res['features'][fid]['MAIN'])
print('B1', json.dumps(b1))
