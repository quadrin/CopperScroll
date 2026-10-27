"""C1: distances from the channel(s) feeding/leaving L56/58 to every recorded heap or boulder, and an inventory of
channels, heaps and boulders within 60 m of L56/58. Frame: traced plan metres (M&P 2018 Fig. 9; x east, z south,
origin L110 centre), from research/models/traced_plans/qumran-settlement.json (repo, read-only)."""
import json, math, sys
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from geo import REPO, dpoly, dseg, F, FIT, BAR
plan = json.loads((REPO / 'research/models/traced_plans/qumran-settlement.json').read_text())
EL = {e['id']: e for e in plan['elements']}
pts = lambda i: [tuple(p) for p in EL[i]['geometry']['points']]
CH = {i: pts(i) for i in EL if i.startswith('CH')}
# Channel round the north and east sides of L56/L58 (not in the traced plan). Traced here from M&P Fig. 100
# (channel outside W610, W608, W607; L67 in it north of L58) and de Vaux 1973 pp. 9-10; placed ~1 m outside the
# L56/L58 polygon edges of the traced plan. Uncertainty ~ +/-1.5 m.
CH['CH-N'] = [(21.47, 24.8), (20.2, 21.2), (29.6, 24.4), (37.3, 26.9), (37.92, 28.44)]
CH['CH-L67-48'] = [(37.3, 26.9), (40.2, 25.9)]  # side channel from NE corner of L58 north to L48-49 (Galor p. 263; de Vaux p. 10); approx.
block = pts('L56') + pts('L58')
def poly_d(p, poly):  # distance from point to polygon outline (0 if inside not handled; heaps are outside)
    q = poly + [poly[0]]; return min(dseg(p, q[i], q[i + 1]) for i in range(len(q) - 1))
dL = lambda p: min(poly_d(p, pts('L56')), poly_d(p, pts('L58')))
# Channel sets (branches of the reading of "the Trench")
MAIN = ['CH02', 'CH03', 'CH04', 'CH05', 'CH06', 'CH-N', 'CH07', 'CH08']           # T1 main distribution channel (Milik)
NARROW = ['CH06', 'CH-N', 'CH07', 'CH08', 'CH-L67-48']                            # T2 the part that feeds/leaves L56/58 (from L83 on)
WIDE = sorted(CH)                                                                 # T3 every channel on Fig. 9
# along-course chainage on the main channel, origin = inflow into L56 (end of CH06)
seq = []
for c in MAIN:
    p = CH[c]
    if seq and math.dist(seq[-1], p[0]) < 3: p = p[1:]
    seq += p
cum = [0.0]
for i in range(1, len(seq)): cum.append(cum[-1] + math.dist(seq[i - 1], seq[i]))
j0 = min(range(len(seq)), key=lambda i: math.dist(seq[i], CH['CH06'][-1])); c0 = cum[j0]
def nearest_on_main(p):
    best = (1e9, 0)
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]; dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
        d = math.hypot(a[0] + t * dx - p[0], a[1] + t * dy - p[1])
        if d < best[0]: best = (d, cum[i] + t * math.sqrt(L) - c0)
    return best
ends = {'main start (aqueduct entry, CH02 start)': seq[0], 'main end (CH08 south end, W of L71)': seq[-1],
        'L69->L71 outlet (CH07 end)': CH['CH07'][-1]}
# --- heaps and boulders -------------------------------------------------------------------------------
# Reeder 2002 map (Freund 2012 Fig. 3.1, Drive copy): similarity from two control points (L110 centre, L71 centre).
R_L110, R_L71 = (459.5, 387.0), (510.5, 441.0)
T_L110, T_L71 = (0.0, 0.0), (46.75, 51.9)
def sim(a0, a1, b0, b1):
    za, zb = complex(a1[0] - a0[0], a1[1] - a0[1]), complex(b1[0] - b0[0], b1[1] - b0[1]); k = zb / za
    return lambda p: (lambda w: (w.real, w.imag))(complex(*b0) + k * complex(p[0] - a0[0], p[1] - a0[1])), abs(k), math.degrees(math.atan2(k.imag, k.real))
r2t, kscale, krot = sim(R_L110, R_L71, T_L110, T_L71)
reeder_graves_px = [(535, 401.5), (542, 408.5), (546, 404), (550.5, 407.5), (528.5, 412), (531.5, 411.5), (533.5, 414), (527, 415),
    (529.5, 417.5), (532.5, 417.5), (535, 418), (535, 421.5), (534, 427), (540, 427.5), (542, 428.5), (549.5, 429), (533, 435),
    (531, 437), (537.5, 437), (532, 441), (536, 443), (539, 443), (531, 447), (534, 449), (540.5, 450.5), (546.5, 456), (550, 461),
    (548, 467), (544, 392.5), (546.5, 395.5), (549.5, 401.5)]
# place frame -> traced (inverse of geo.traced_to_place)
def place_to_traced(x, z):
    t = math.radians(FIT['turnDegClockwise']); s = FIT['pxPerM']; c, sn = math.cos(t), math.sin(t)
    dx, dz = x - FIT['placePoint'][0], z - FIT['placePoint'][1]
    pu = s * (c * dx + sn * dz); pv = s * (-sn * dx + c * dz); return pu / BAR, pv / BAR
img_graves_place = [(31, 106), (28, 117), (28, 122), (27, 130), (30, 138), (33, 90), (24.5, 96)]  # westernmost grave marks read on Esri 2023 (out/m_cem_grid.png), +/-3 m
H = []
for k, p in enumerate(reeder_graves_px):
    H.append(('grave heap (Reeder 2002 map, visual/GPR)', f'R{k+1}', r2t(p), 'small, not "great"; grave size not to scale on the map'))
for k, p in enumerate(img_graves_place):
    H.append(('grave heap (2023 imagery, westernmost rows)', f'I{k+1}', place_to_traced(*p), 'small; matches de Vaux p. 45 "empty space of nearly fifty metres"'))
H.append(('piles of masonry at the aqueduct sluice, loc. 137 (de Vaux p. 9)', 'L137', tuple(CH['CH02'][0]), 'stone piles stopping the flow; position = aqueduct entry (+/-4 m); not "great"'))
tower = pts('tower-outline')
H.append(('stone ramp/glacis round the tower (de Vaux p. 25; M&P p. 15)', 'TWR', None, 'large stone revetment, not described as a heap'))
deb = [(-14.3, -15.9), (12.1, -15.9)], [(-15.6, -14.9), (-15.6, 5.2)]
H.append(('debris heap at foot of N wall of western building (de Vaux p. 25, Pl. XIa)', 'DEB-N', None, 'Period Ib clearance debris, not a stone heap'))
H.append(('debris heap against W wall of western building (de Vaux p. 25)', 'DEB-W', None, 'as above'))
geom = {'TWR': tower, 'DEB-N': deb[0], 'DEB-W': deb[1]}
def dist_to(set_ids, h):
    k, g = h[1], geom.get(h[1])
    if g is None: return min(dpoly(h[2], CH[c]) for c in set_ids)
    return min(min(dpoly(p, CH[c]) for c in set_ids) for p in g) if len(g) < 3 else min(min(dpoly(p, CH[c]) for p in g) for c in set_ids)
def dense(g, step=0.5):
    out = []
    for i in range(len(g) - 1):
        n = max(1, int(math.dist(g[i], g[i + 1]) / step))
        out += [(g[i][0] + (g[i + 1][0] - g[i][0]) * t / n, g[i][1] + (g[i + 1][1] - g[i][1]) * t / n) for t in range(n + 1)]
    return out
rows = []
for h in H:
    P = dense(geom[h[1]]) if h[1] in geom else [h[2]]
    d = {nm: min(min(dpoly(p, CH[c]) for c in S) for p in P) for nm, S in (('T1', MAIN), ('T2', NARROW), ('T3', WIDE))}
    near = min((nearest_on_main(p) for p in P), key=lambda x: x[0])
    de = {nm: min(math.dist(p, e) for p in P) for nm, e in ends.items()}
    dl = min(dL(p) for p in P)
    rows.append({'kind': h[0], 'id': h[1], 'note': h[3], 'at_traced': [round(v, 1) for v in (P[0] if len(P) == 1 else P[len(P)//2])],
                 'd_T1_main': round(d['T1'], 1), 'd_T2_narrow': round(d['T2'], 1), 'd_T3_all': round(d['T3'], 1),
                 'chainage_from_L56_inflow_at_nearest': round(near[1], 1),
                 **{('d_' + nm.split(' (')[0].replace(' ', '_')): round(v, 1) for nm, v in de.items()}, 'd_L56_58': round(dl, 1)})
for r in rows: print(r)
# channels within 60 m of L56/58
chan = []
for c, p in sorted(CH.items()):
    dd = min(dL(q) for q in dense(p)); chan.append({'id': c, 'label': EL[c]['label'] if c in EL else 'traced here (see script)', 'min_d_L56_58': round(dd, 1),
        'max_d_L56_58': round(max(dL(q) for q in dense(p)), 1)})
for r in chan: print(r)
json.dump({'frame': 'traced plan metres (M&P Fig. 9), origin L110', 'reeder_similarity': {'scale_m_per_px': round(1 / kscale, 3) if False else round(kscale, 3), 'rot_deg': round(krot, 2)},
           'cubit_window_m': [24, 35], 'heaps': rows, 'channels': chan, 'main_channel_length_m': round(cum[-1], 1), 'L56_inflow_chainage': round(c0, 1)},
          open('out/c1_distances.json', 'w'), indent=1)
print('reeder scale (traced m per px)', kscale, 'rot', krot, 'main length', cum[-1], 'c0', c0)
