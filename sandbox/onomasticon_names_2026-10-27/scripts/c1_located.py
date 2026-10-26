"""EXPLORATORY (not in the rule): chance level for a LOCATED match. Every Onomasticon entry and Madaba label gets an
automatic in/out/none call (keyword classifier, validated against the manual review in locations.py); then the C1 shuffles
and C2 are re-scored counting only matches to entries called 'in'."""
import sys, os, re, csv, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skel import heb_skeletons, latin_word_forms, greek_unicode_forms, match, FIN, strip_acc
from locations import E
SN, OUT = sys.argv[1], sys.argv[2]
IN_LOC = ['Jerusalem', 'Aelia', 'Jericho', 'Neapolis', 'Sebast', 'Scythopolis', 'Bethel', 'Hebron', 'Chebron', 'Bethlehem', 'Bethleem',
          'Gaba', 'Gabaon', 'Rama', 'Anathoth', 'Thekou', 'Galgal', 'Akrabattine', 'Nicopolis', 'Eleutheropolis', 'Legeon', 'Pella',
          'Livias', 'Sikim', 'Sychem', 'Engaddi', 'Dead Sea', 'Aulon', 'Machmas', 'Gophna', 'Diospolis', 'Mt. of Olives', 'Salim', 'Jordan']
OUT_LOC = ['Ascalon', 'Azotus', 'Gaza', 'Iamnia', 'Caesarea', 'Diocaesarea', 'Ptolemais', 'Tyre', 'Sidon', 'Damascus', 'Petra',
           'Philadelphia', 'Esbus', 'Esbon', 'Hesebon', 'Hesbon', 'Areopolis', 'Gerasa', 'Gerash', 'Gadara', 'Bostra', 'Zoora', 'Zoara', 'Mapsis',
           'Aila', 'Tabor', 'Thabor', 'Capharna', 'Paneas', 'Egypt', 'Babylon', 'Mesopotamia', 'Edessa', 'Arnon', 'India', 'Assyria',
           'Galilee', 'Gennesar', 'Sinai', 'Madaba', 'Dibon', 'Batanaea', 'Basan', 'Galaad', 'Moab', 'Arabia', 'Phoenicia', 'Emes']
POS = re.compile(r'mile|near|between|east|west|north|south|beside|suburb|region of|on the road|located|pointed out|opposite|border', re.I)
def auto_onom(text):
    if not POS.search(text): return 'none'
    if any(l in text for l in IN_LOC): return 'in'
    if any(l in text for l in OUT_LOC): return 'out'
    return 'none'
onom = {e['no']: e for e in csv.DictReader(open(os.path.join(OUT, 'gaz_onomasticon.csv')))}
auto = {('O', int(k)): auto_onom(e['text']) for k, e in onom.items()}
# Madaba: map region by Piggin identification (manual list of labels inside region+10 km)
MAD_IN = {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 49, 50, 51,
          52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 20}
mad = list(csv.DictReader(open(os.path.join(OUT, 'gaz_madaba.csv'))))
for r in mad: auto[('M', int(r['piggin']))] = 'in' if int(r['piggin']) in MAD_IN else 'out'
# validation against manual (headword-level) calls
agree = tot = 0; conf = {}
for k, (st, _) in E.items():
    if st in ('nonplace',): continue
    a = auto.get(k); tot += 1; agree += (a == st) or (st == 'edge'); conf[(st, a)] = conf.get((st, a), 0) + 1
print(f'auto vs manual agreement {agree}/{tot}; confusion {sorted(conf.items())}')
# gazetteer with located flag (headword forms only: Greek + Latin + Madaba; body names excluded here)
gaz = []
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_match.py')).read().split('# ---------- gazetteer names ----------')[1].split('def find')[0])
def located_match(vl):
    for v in vl:
        sks = heb_skeletons(v)
        for g in gaz:
            if g['set'] not in ('greek', 'latin'): continue
            if auto.get((g['src'][0], int(g['id']))) != 'in': continue
            for s in sks:
                for gs in g['sk']:
                    if match(s, gs, 'both'): return True
    return False
names = json.load(open(SN)); rng = random.Random(20261027)
obs = 0; chance = []
rows = []
for n in names:
    vl = [v['core'] for v in n['variants']]; o = located_match(vl); obs += o
    c = 0
    for k in range(100):
        sh = []
        for v in n['variants']:
            L = list(v['core'].translate(FIN)); rng.shuffle(L); sh.append(''.join(L))
        c += located_match(sh)
    chance.append(c / 100); rows.append((n['id'], int(o), c / 100))
c2 = json.load(open(os.path.join(OUT, 'c2_names.json')))
k2 = sum(located_match([c['c2_hebrew']]) for c in c2)
from math import comb
def pb_tail(ps, k):
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist): new[i] += d * (1 - p); new[i + 1] += d * p
        dist = new
    return sum(dist[k:])
print(f'scroll names with a located (auto) match: {obs}/40; C1-located expected {sum(chance):.1f}/40, P(X>={obs}) = {pb_tail(chance, obs):.3f}; C2 located (auto) {k2}/40')
with open(os.path.join(OUT, 'c1_located_exploratory.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['name', 'located_match_auto', 'c1_located_rate']); w.writerows(rows)
