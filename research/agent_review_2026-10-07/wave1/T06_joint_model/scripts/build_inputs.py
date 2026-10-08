#!/usr/bin/env python3
"""Build the v0 input CSVs for the joint placement model from the shared files.

Outputs (in ../inputs/):
  candidates_v0.csv  - one row per (entry, candidate place): status, confidence, order_derived flag
  places_v0.csv      - one row per place: lat, lon, sigma_km, model_region, coordinate note
  name_groups_v0.csv - one row per (group, entry) for entries that name the same place
  entries_v0.csv     - the 61 canonical slots in scroll order with block label and entry confidence

The CSVs are the only inputs joint_model.py reads, so new candidates / places / name readings
(tasks 1 and 5) can be added by editing or appending rows and re-running joint_model.py.

Run:  python3 -I build_inputs.py <shared_dir> <out_dir>
"""
import csv, json, os, re, sys

SHARED = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'inputs')
os.makedirs(OUT, exist_ok=True)

entries = json.load(open(os.path.join(SHARED, 'entries.json'), encoding='utf-8'))
places = json.load(open(os.path.join(SHARED, 'places.json'), encoding='utf-8'))
p3 = {r['place_id']: r for r in csv.DictReader(open(os.path.join(SHARED, 'phase3_places.csv'), encoding='utf-8-sig'))}

# ---------------------------------------------------------------- model regions (INFERENCE: my grouping by coordinates)
REGION = {
    'JER': ['jer_temple', 'jer_east_gate', 'jer_se_corner', 'jer_south_wall', 'jer_kidron_mon', 'jer_kidron_east',
            'jer_gethsemane', 'jer_siloam', 'jer_bir_ayyub', 'jer_bethesda', 'jer_tyropoeon', 'jer_tombs_kings',
            'jer_baqa', 'jer_shaveh', 'ramat_rahel', 'tell_el_ful'],
    'SOUTH': ['natuf', 'tekoa_herodium'],
    'DESERT': ['mar_saba', 'hyrcania', 'buqeia'],
    'QUMRAN': ['kh_qumran', 'wadi_qumran', 'asla'],
    'JERICHO': ['nuweimeh', 'ain_duk', 'doq', 'tell_es_sultan', 'jericho_palaces', 'jericho_area', 'tell_el_qos',
                'choziba', 'kuteif', 'jordan_ford'],
    'NORTH': ['gerizim', 'beth_shean', 'ibziq', 'kh_salhab'],
    'WEST': ['beth_horon'],
}
REG_OF = {p: r for r, ps in REGION.items() for p in ps}


def sigma_km(prec):
    """Precision string -> 1-sigma location uncertainty in km.
    '~X m' / '~X km' -> X (a point with that uncertainty); 'area ~X km' -> X/2 (extent read as a diameter)."""
    if prec is None or 'unresolved' in prec:
        return None
    m = re.search(r'~\s*([\d.]+)\s*(m|km)', prec)
    if not m:
        return None
    v = float(m.group(1)) / (1000.0 if m.group(2) == 'm' else 1.0)
    return v / 2.0 if prec.strip().startswith('area') else v


# places without coordinates in places.json: how the model locates them (all flagged in the CSV)
NULL_COORD = {
    # midpoint of the two points the project itself cites for the label (phase3_places.csv note: Herodium
    # Wikidata Q913099 31.6658,35.2414; Kh. Tuqu' Wikidata Q12210361 31.6329,35.2113); sigma = half of 'area ~8 km'
    'tekoa_herodium': dict(lat=round((31.6658 + 31.6329) / 2, 5), lon=round((35.2414 + 35.2113) / 2, 5), sigma=4.0,
                           note='DERIVED: midpoint of Herodium (Wikidata Q913099) and Kh. Tuqu (Wikidata Q12210361) as cited in phase3_places.csv; sigma 4 km'),
    # proxy point: Qasr al-Yahud, the traditional Jordan crossing/baptism site SE of Jericho,
    # 31.838333 N 35.539167 E per https://en.wikipedia.org/wiki/Qasr_al-Yahud ; sigma = half of 'area ~10 km'
    'jordan_ford': dict(lat=31.838333, lon=35.539167, sigma=5.0,
                        note='PROXY: Qasr al-Yahud coordinates from en.wikipedia.org/wiki/Qasr_al-Yahud; no ford is identified; sigma 5 km'),
    # unresolved valley: modelled as a 50/50 mixture of the two published options (Kidron/King's Valley; Baqa plain)
    'jer_shaveh': dict(mixture='jer_kidron_mon|jer_baqa',
                       note='MIXTURE: 50/50 of jer_kidron_mon (King\'s Valley = Kidron, Puech) and jer_baqa (Milik); valley unresolved'),
}

with open(os.path.join(OUT, 'places_v0.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['place_id', 'name', 'lat', 'lon', 'sigma_km', 'mixture_of', 'model_region', 'coords_in_places_json',
                'precision_string', 'coord_note'])
    for p in places:
        pid = p['id']
        has = p['lat'] is not None
        lat, lon, sig, mix, note = p['lat'], p['lon'], sigma_km(p['precision']), '', p3.get(pid, {}).get('coord_source', '')
        if not has:
            nc = NULL_COORD[pid]
            if 'mixture' in nc:
                lat = lon = sig = ''
                mix = nc['mixture']
            else:
                lat, lon, sig = nc['lat'], nc['lon'], nc['sigma']
            note = nc['note']
        w.writerow([pid, p['name'], lat, lon, sig, mix, REG_OF[pid], 'yes' if has else 'no', p['precision'], note])

# ---------------------------------------------------------------- order-derived flags
# 'documented': the project's own text says the placement rests on (or was chosen by) the order of entries,
#   or the candidate is an area assigned to a run of entries.
#   Sources: atlas_text.json notes e4-kohlit, e60-kohlit, e20-valley, e48-absalom; entries.json evidence for 40
#   ("Natuf rests on the order of the entries"); places.json name of tekoa_herodium ("Puech's area for IX 4-X 4").
# 'likely': INFERENCE (mine): candidate for an entry whose text names no place, equal to the district of its
#   neighbours; I could not find an independent basis in the shared files.
DOC = {('4', 'tell_es_sultan'), ('11', 'tell_es_sultan'), ('15', 'tell_es_sultan'), ('19', 'tell_es_sultan'),
       ('60', 'tell_es_sultan'), ('20', 'wadi_qumran'), ('20', 'kh_qumran'), ('21', 'kh_qumran'),
       ('22', 'kh_qumran'), ('23', 'kh_qumran'), ('48', 'jer_kidron_mon'), ('40', 'natuf')}
for e in ('39', '42', '43', '44', '45'):
    DOC.add((e, 'tekoa_herodium'))
LIKELY = {('2', 'nuweimeh'), ('3', 'nuweimeh'), ('16', 'tell_es_sultan'), ('25', 'kh_qumran'), ('26', 'kh_qumran'),
          ('27', 'jericho_area'), ('28', 'jordan_ford'), ('29', 'jericho_palaces'), ('29', 'ain_duk'),
          ('29', 'tell_es_sultan'), ('29', 'hyrcania'), ('33', 'jericho_area'), ('34', 'jer_bir_ayyub'),
          ('34', 'jericho_area'), ('34', 'doq'), ('45', 'jer_bir_ayyub'), ('47', 'jer_bir_ayyub'),
          ('50', 'jer_se_corner'), ('53', 'jer_south_wall'), ('53', 'jer_kidron_east'), ('54', 'jer_kidron_east'),
          ('54', 'jer_gethsemane'), ('56', 'jer_bethesda'), ('56', 'jer_kidron_east')}

with open(os.path.join(OUT, 'candidates_v0.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['entry', 'place_id', 'status', 'confidence', 'order_derived', 'prior_override', 'source'])
    for e in entries:
        for c in e.get('candidates', []):
            k = (e['entry'], c['placeId'])
            od = 'documented' if k in DOC else ('likely' if k in LIKELY else 'no')
            w.writerow([e['entry'], c['placeId'], c['status'], c['confidence'], od, '',
                        'shared/entries.json (CopperScroll atlas); ' + (e.get('sources') or '').replace('\n', ' ')[:200]])

BLOCK = lambda n: 'A' if n <= 19 else ('B' if n <= 35 else ('C' if n <= 56 else 'D'))
with open(os.path.join(OUT, 'entries_v0.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order', 'entry', 'block', 'entry_confidence', 'status', 'title'])
    for i, e in enumerate(entries):
        n = int(re.match(r'\d+', e['entry']).group())
        w.writerow([i, e['entry'], BLOCK(n), e['confidence'], e.get('status', ''), e['title']])

# ---------------------------------------------------------------- name groups
# From deep_analysis/features.py NAMES (hand list of proper place names per entry; quadrin/CopperScroll).
# Only names shared by >= 2 entries form a group. Entry 24 names Jericho and Secacah only as the two ends of a
# route ("on the way from Jericho to Secacah"), so it is NOT tied to the Secacah location (my choice, flagged).
# Variant columns: 'kohlit15' = the group membership of 15 depends on Puech's restoration (readings.json e15-kohlit);
# 'solomon23' = 23 joins 22 only under the Solomon reading (readings.json e23-shallum; Puech 2015 prefers Shallum).
GROUPS = [('Achor', '1', ''), ('Achor', '17', ''),
          ('Kohlit', '4', ''), ('Kohlit', '11', ''), ('Kohlit', '15', 'kohlit15'), ('Kohlit', '19', ''), ('Kohlit', '60', ''),
          ('Melah', '6', ''), ('Melah', '13', ''), ('Melah', '14', ''),
          ('Secacah', '20', ''), ('Secacah', '21', ''), ('Secacah', '22', ''),
          ('Solomon', '22', ''), ('Solomon', '23', 'solomon23'),
          ('Shaveh', '36', ''), ('Shaveh', '37', ''),
          ('Zadok', '51', ''), ('Zadok', '52', '')]
with open(os.path.join(OUT, 'name_groups_v0.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['group', 'entry', 'conditional_on_reading', 'source'])
    for g, e, cond in GROUPS:
        w.writerow([g, e, cond, 'deep_analysis/features.py NAMES (quadrin/CopperScroll)'])
print('wrote', OUT)
