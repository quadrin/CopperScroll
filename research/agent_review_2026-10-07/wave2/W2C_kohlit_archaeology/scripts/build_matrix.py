#!/usr/bin/env python3
"""Build the Kohlit feature matrix (CSV + JSON) and a simple transparent score.

Status vocabulary
  PRESENT_DATED    feature attested and dated within 1st c. BCE - 135 CE (or Hasmonean)
  PRESENT_UNDATED  feature attested, period not established (or later/earlier date only)
  PARTIAL          something close is attested but a required attribute (direction, size,
                   period, location) is missing or contradicts
  ABSENT_IN_SOURCES  not mentioned in the sources read; 'thoroughness' says how much that means
  UNKNOWN          no source consulted covers the point
Scores (for ranking only; weights are a judgement, stated in REPORT.md):
  PRESENT_DATED 1.0, PRESENT_UNDATED 0.6, PARTIAL 0.3, ABSENT_IN_SOURCES 0.0, UNKNOWN 0.0
Run: python3 -I build_matrix.py
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')

FEATURES = [
    ('F1', 'Mound (tel) - entry 4 "in the tel of Kohlit"', 2.0),
    ('F2', 'Conduit (amma) at the site - entry 4', 1.0),
    ('F3', 'Immersion rock-cleft / miqveh near the conduit - entry 4', 0.5),
    ('F4', 'Cornered pool EAST of the site - entry 11 ("pool east of Kohlit, northern corner")', 2.0),
    ('F5', 'Great cistern with a pillar IN the site - entry 15 (Kohlit restored)', 0.5),
    ('F6', 'Several pits/caves NORTH of the site, one "eastern" - entry 19', 1.5),
    ('F7', 'Pit on N side, opening N (or hidden), tombs (or "buried") at its mouth - entry 60', 1.5),
    ('F8', 'Hellenistic-Early Roman occupation on/at the site (to 135 CE)', 1.5),
    ('F9', 'Jewish presence in period (ossuaries, kokhim, miqvaot, synagogue)', 1.0),
    ('F10', 'Desert setting (b. Qid. 66a "Kohalit in the desert") - contextual', 0.5),
    ('F11', 'Name preservation k-h-l - contextual', 0.5),
]
SCORE = {'PRESENT_DATED': 1.0, 'PRESENT_UNDATED': 0.6, 'PARTIAL': 0.3,
         'ABSENT_IN_SOURCES': 0.0, 'UNKNOWN': 0.0}

M = {}
def cell(cand, f, status, evidence, sources, thoroughness='', confidence=''):
    M.setdefault(cand, {})[f] = dict(status=status, evidence=evidence, sources=sources,
                                      thoroughness=thoroughness, confidence=confidence)

TS = 'Tell es-Sultan (Puech)'
cell(TS, 'F1', 'PRESENT_DATED', '40-dunam multi-period tell; double mound; Roman "architectural remains, wine-presses" and tombs on it (thin occupation)',
     'Nigro 2011 pp.146,152; SWP Memoirs III (1883) p.222', '', 'high')
cell(TS, 'F2', 'PRESENT_UNDATED', 'Spring water "conducted ... by various channels" (19th c.); an aqueduct from Ain es-Sultan joined the Auja line at Kh. el-Mefjir, water carried in pipes "like those of the high level aqueduct in Wady Kelt"; a 4th aqueduct ran S to Rujm el-Mogheifir (bridge modern-looking); a Byzantine aqueduct by the tell; Hamamrah states generically that Hellenistic-Roman aqueducts drew on Ain es-Sultan',
     'SWP III pp.206-207, 223; Nigro 2011 p.153 (cat.86); Hamamrah in Nigro 2011 p.306', 'No excavated, dated conduit at the tell in the sources read', 'medium')
cell(TS, 'F3', 'ABSENT_IN_SOURCES', 'No immersion installation at the tell; Hasmonean miqveh in the synagogue complex at Tulul Abu el-Alayiq (~2 km S); a 3-step small cistern of Early Roman date at Jiser Abu Ghabush (~3 km N)',
     'Netzer, NEAEHL 5 (2008) p.1799; Taha in Nigro 2011 p.273', 'Gazetteer-level (Nigro catalogue) + Taha salvage reports; Kenyon 1981 not seen', 'medium')
cell(TS, 'F4', 'PRESENT_UNDATED', 'Spring "comes out beneath the mound on the east" into "a shallow reservoir, 24 feet by 40 feet, of hewn stones, well dressed"; W wall of small masonry in hard cement with a semicircular statue niche facing E. Catalogue lists a Roman-period "nympheum" at the spring; a pool only for Ottoman/Modern. Nigro coordinates put the spring point ~100 m SSE of the tell centroid point',
     'SWP III pp.222-223; Nigro 2011 pp.110-112 (cat.21); geometry.csv', 'Second Temple date of the rectangular pool not shown; Dorrell 1993 (PEQ 125) not seen', 'medium')
cell(TS, 'F5', 'ABSENT_IN_SOURCES', 'No great cistern at/near the tell in the catalogue or SWP; Puech asserts "une grande citerne au nord" without an archaeological reference; Byzantine monastery cisterns 1 km SE',
     'Nigro 2011 pp.146-154; SWP III pp.222-223; Puech 2006 pp.174-175 n.49; Puech 2015 p.13 n.49', 'Catalogue is a compiled gazetteer (moderate); Kenyon 1981, Sellin-Watzinger 1913 not seen', 'medium')
cell(TS, 'F6', 'PRESENT_UNDATED', '>400 EB IV shaft tombs "in the limestone plateau north of the tell" (Kenyon); Garstang/Kenyon necropolis W and NW of the tell; caves 1.5-3 km NW at Jebel Abu Saraj used in the Hasmonean period (Jannaeus coins in cave IV/1; "Hasmonean Cave" IV/8)',
     'Nigro 2011 pp.11, 68; Sion, Atiqot 41 (2002) pp.46-47 and Index pp.257-258', 'Shaft field is Bronze Age (visible/reusable shafts); caves are 1.5-3 km away', 'high (shafts exist) / low (that they are the scroll pits)')
cell(TS, 'F7', 'PARTIAL', 'Roman-period tombs (loculi, kokhim, arcosolium; ossuaries, wooden coffins) "both on the tell and in the nearby necropolis"; Puech: Qumran-type graves on the N side of the tell (Kenyon 1981:173-174, not seen). Necropolis now "partly concealed under modern edification" (Ain es-Sultan camp). No specific pit with a northward opening is published in sources read',
     'Nigro 2011 pp.146, 152 (citing Kenyon 1965:516-545; 1981:173-174); Puech 2006 pp.174-175 n.49; Puech 2015 p.13 n.49', 'Primary Kenyon tomb registers not seen', 'medium')
cell(TS, 'F8', 'PARTIAL', 'On the tell: Hellenistic "scattered materials" / "no more than occasionally frequented"; Roman: some architecture, installations, tombs. Around it: Early Roman villa/house 1-1.7 km N/NE (police station/college; 1st c. CE domestic unit with bath), Herodian hippodrome ~0.6-0.9 km SSW, Hasmonean-Herodian palaces ~2 km S',
     'Nigro 2011 pp.18, 20, 30, 152; Taha in Nigro 2011 pp.278-280; Hamamrah in Nigro 2011 p.315; geometry.csv', '', 'high')
cell(TS, 'F9', 'PRESENT_DATED', 'Second Temple Jewish cemetery (Hachlili; mid-1st c. BCE-1st c. CE) W/SW of the tell; eth-Thiniya arcosolium tomb W of the tell with 10 ossuaries (2 Greek-inscribed) + wooden coffin; Hasmonean synagogue with miqveh at the palaces; Roman tombs with ossuaries in Kenyon necropolis',
     'Nigro 2011 pp.131-132, 152; Taha in Nigro 2011 p.285; WBADB p.70 no.343; NEAEHL 5 pp.1798-1799', '', 'high')
cell(TS, 'F10', 'PARTIAL', 'Oasis; Puech concedes the problem but argues the tell is "still in the desert"',
     'Puech 2015 p.13 n.49; Zissu 2001 p.149', '', 'medium')
cell(TS, 'F11', 'ABSENT_IN_SOURCES', 'No k-h-l toponym recorded; Jericho name persists at the site (Zissu objection)', 'Zissu 2001 p.149; SWP III pp.222-223', 'SWP + Palmer lists (T01) searched', 'medium')

ES = "Ein Samiya / Kh. el-Marjama + Kh. Samiya (Zissu)"
cell(ES, 'F1', 'PRESENT_UNDATED', 'Kh. el-Marjama: tell >30 dunams; EB-Iron fortified town; Hellenistic, Roman listed as minor periods; Kallai: settlement "descended" to Kh. Samiya from the Roman period',
     'Zissu 2001 pp.151, 154; WBADB p.56 no.213', '', 'high')
cell(ES, 'F2', 'PRESENT_UNDATED', 'Rock-cut pool "next to aqueducts and additional water installations near the tell" (Kallai); "there is an aqueduct at Ein Samiya" (Eshel); irrigation canals and pools "from ancient times until the present"; remains of two mills',
     'Zissu 2001 pp.150-151; Eshel in Copper Scroll Studies (2002) p.106 n.35; SWP II (1882) p.394', 'Kallai 1972 not seen; no dates', 'medium')
cell(ES, 'F3', 'ABSENT_IN_SOURCES', 'No immersion installation reported', 'Zissu 2001; WBADB pp.55-56', 'Survey-level sources; Mazar 1995, Zohar 1980 not seen', 'low')
cell(ES, 'F4', 'PARTIAL', 'A rock-cut pool near the tell (direction not stated); spring issues on the NW side of the valley "from a strongly-built wall forming a tank" with a column fragment and drafted stones; on Zissu figs 2-3 the spring lies S/SW of Kh. el-Marjama and N/NW of Kh. Samiya, i.e. not east of either',
     'Zissu 2001 pp.151-153 (figs 2-3), 155; SWP II p.394', 'Kallai 1972 not seen; pool location unknown', 'medium')
cell(ES, 'F5', 'PARTIAL', '"A water reservoir that kept the water out of Ein Samiya spring" (Zohar 1980) - size, pillar and date unknown; Byzantine monastery cistern at el-Qasr',
     'Zissu 2001 pp.151, 155', 'Zohar 1980 (IEJ 30:219-220) not seen', 'low')
cell(ES, 'F6', 'PRESENT_UNDATED', 'Dhahr Mirzbaneh ridge ~0.6 km NNE of the tell: Intermediate Bronze site "above large cemetery", "hundreds of burial caves" (shaft tombs); graveyard symbols N of Kh. el-Marjama on Zissu fig.2; further IB shaft-tomb fields S and ESE; "caves" along the wadi on the 1941 map; "a great many grottoes" cut in the slopes (Guerin)',
     'Zissu 2001 pp.151-153; WBADB pp.55-56 nos 209, 214, 217; SWP II p.394; geometry.csv', 'Shafts are IB (c. 2200-2000 BCE)', 'high (shafts exist) / low (that they are the scroll pits)')
cell(ES, 'F7', 'PARTIAL', 'IB shaft tombs N/NNE of the tell (pits among tombs) as at Jericho; no Roman reuse of the N shafts reported in sources read; the Early Roman Jewish tombs are at Kh. Samiya, S of the tell (Baramki Tomb 1: entrance in E wall)',
     'Zissu 2001 pp.151, 155; WBADB p.56 no.215', 'Lapp 1966, Dever 1972, Finkelstein 1990 not seen', 'medium')
cell(ES, 'F8', 'PARTIAL', 'Kh. el-Marjama "settled during the Hellenistic, Roman and Byzantine periods" but "maybe still settled during the Second Temple period"; Kh. Samiya mainly Roman-Byzantine (WBADB: [Late Roman], Byz, bracketed); Early Roman evidence = tombs',
     'Zissu 2001 pp.151, 154-155; WBADB p.56 nos 213, 215', 'Survey-level; Mazar 1995 not seen', 'medium')
cell(ES, 'F9', 'PRESENT_DATED', 'Baramki 1942 Tomb 1: kokhim tomb, Roman pottery and lamp, ossuary fragments -> Early Roman Jewish burial; Yeivin: 16 Roman-Byzantine tombs incl. kokhim; Lyon 1908 Jewish kokhim; WBADB: three Rom-Byz burial caves with ossuary fragments',
     'Zissu 2001 p.155; WBADB p.56 no.215', '', 'medium-high')
cell(ES, 'F10', 'PRESENT_UNDATED', 'Semi-arid "Samarian desert" margin between Jordan valley and watershed', 'Zissu 2001 p.150', '', 'medium')
cell(ES, 'F11', 'PRESENT_UNDATED', 'Wadi Kuheila (on 1941 1:20,000 sheet 15-18) runs E of Kh. el-Marjama into the valley', 'Zissu 2001 pp.150, 153 (fig.3)', 'Name attested only from Mandate maps in sources read', 'medium')

TM = 'Tell Muhalhil near Nebi Musa (Lurie)'
cell(TM, 'F1', 'PARTIAL', 'Named "tell"; Bar-Adon 1968 survey found only a small structure 3.5 x 2.5 m', 'Zissu 2001 p.148 (citing Bar-Adon 1972:118 site 83)', 'Bar-Adon 1972 not seen', 'medium')
for f in ['F2','F3','F4','F5','F6','F7']:
    cell(TM, f, 'UNKNOWN', 'No description in sources read', 'Zissu 2001 p.148; Nigro 2011 (not catalogued)', 'Nigro catalogue omits the site; Nebi Musa itself has only Middle/Late Islamic-Ottoman periods (Nigro 2011 p.130)', '')
cell(TM, 'F8', 'UNKNOWN', 'No period data', 'Zissu 2001 p.148', '', '')
cell(TM, 'F9', 'UNKNOWN', '', '', '', '')
cell(TM, 'F10', 'PRESENT_UNDATED', 'Judean desert near Nebi Musa', 'Zissu 2001 p.148; Lefkovits 2000 p.74', '', 'high')
cell(TM, 'F11', 'PARTIAL', 'm-h-l-h-l only loosely like k-h-l-t ("only connection ... phonetic similarity")', 'Zissu 2001 p.148', '', 'medium')

BK = 'Beit Kahil NW of Hebron (listed by Milik, Lurie)'
cell(BK, 'F1', 'ABSENT_IN_SOURCES', 'A village "on a ridge"; no tell described', 'SWP III p.303', 'SWP topographical entry only', 'low')
cell(BK, 'F2', 'UNKNOWN', '', '', '', '')
cell(BK, 'F3', 'UNKNOWN', '', '', '', '')
cell(BK, 'F4', 'ABSENT_IN_SOURCES', 'Only "a well to the south"', 'SWP III p.303', 'SWP entry only', 'low')
cell(BK, 'F5', 'UNKNOWN', '', '', '', '')
cell(BK, 'F6', 'PARTIAL', '"Apparently an ancient place, with rock-cut tombs" (direction not given)', 'SWP III p.303', '', 'low')
cell(BK, 'F7', 'UNKNOWN', '', '', '', '')
cell(BK, 'F8', 'UNKNOWN', 'Guerin equated it with Roman Cela (tertiary report)', 'Wikipedia "Beit Kahil" (tertiary)', '', 'low')
cell(BK, 'F9', 'UNKNOWN', '', '', '', '')
cell(BK, 'F10', 'ABSENT_IN_SOURCES', 'Hebron hill country, not desert', 'SWP III p.303', '', 'medium')
cell(BK, 'F11', 'PRESENT_UNDATED', 'Kahil ~ k-h-l', 'Milik DJD III p.274 n.71; Lefkovits 2000 p.74', '', 'medium')

KQ = 'Kh. Quhlet / Kuhlah NE of Beersheba (listed by Milik, Lurie)'
for f, _, _ in FEATURES:
    cell(KQ, f, 'UNKNOWN', 'No archaeological description located', 'Milik DJD III p.274 n.71; Zissu 2001 p.148', 'Not found in SWP OCR text searched', '')
cell(KQ, 'F11', 'PRESENT_UNDATED', 'Name ~ k-h-l', 'Milik DJD III p.274 n.71', '', 'medium')
cell(KQ, 'F10', 'PARTIAL', 'Northern Negev margin (inference from location only)', 'Milik DJD III p.274 n.71', '', 'low')

MZ = 'Mount Zion, Greek Orthodox cemetery area (Pixner)'
for f, _, _ in FEATURES:
    cell(MZ, f, 'UNKNOWN', 'Not covered by sources read (Pixner 1983 not available)', 'Zissu 2001 pp.148-149', '', '')
cell(MZ, 'F1', 'ABSENT_IN_SOURCES', 'Pixner reads "tel" as a technical term for a community gathering place, not a ruin mound; Goranson objects that a tell inside such a centre is implausible', 'Zissu 2001 p.148; Goranson in Copper Scroll Studies (2002) p.228', '', 'medium')
cell(MZ, 'F10', 'ABSENT_IN_SOURCES', 'Jerusalem, not desert', 'Zissu 2001 pp.148-149', '', 'high')
cell(MZ, 'F11', 'ABSENT_IN_SOURCES', 'No k-h-l name', 'Zissu 2001 p.148', '', 'medium')

rows = []
scores = {}
for cand, cells in M.items():
    tot = 0.0; mx = 0.0
    for f, label, w in FEATURES:
        c = cells.get(f, dict(status='UNKNOWN', evidence='', sources='', thoroughness='', confidence=''))
        tot += w * SCORE[c['status']]; mx += w
        rows.append([cand, f, label, c['status'], c['evidence'], c['sources'], c['thoroughness'], c['confidence']])
    scores[cand] = (round(tot, 2), round(mx, 2))

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, 'feature_matrix.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['candidate', 'feature_id', 'feature', 'status', 'evidence', 'sources_pages', 'source_thoroughness_note', 'confidence'])
    w.writerows(rows)
with open(os.path.join(DATA, 'feature_matrix.json'), 'w', encoding='utf-8') as fh:
    json.dump({'features': FEATURES, 'score_map': SCORE, 'matrix': M, 'scores': scores}, fh, ensure_ascii=False, indent=1)
with open(os.path.join(DATA, 'scores.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['candidate', 'weighted_score', 'max_possible'])
    for k, v in sorted(scores.items(), key=lambda kv: -kv[1][0]):
        w.writerow([k, v[0], v[1]])
for k, v in sorted(scores.items(), key=lambda kv: -kv[1][0]):
    print(f'{v[0]:5.2f} / {v[1]}  {k}')

# sensitivity: drop contextual F10-F11, and drop F4 weighting to 1.0
def rescore(drop=(), override=None):
    out = {}
    for cand, cells in M.items():
        t = 0
        for f, label, w in FEATURES:
            if f in drop: continue
            if override and f in override: w = override[f]
            t += w * SCORE[cells.get(f, {'status': 'UNKNOWN'})['status']]
        out[cand] = round(t, 2)
    return out
print('no contextual F10/F11:', rescore(drop=('F10', 'F11')))
print('F4 weight 1.0, F10/F11 weight 1.5:', rescore(override={'F4': 1.0, 'F10': 1.5, 'F11': 1.5}))
