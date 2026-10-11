"""Shared rules of the water-systems lane (PLAN.md and PLAN_AMENDMENT_1.md). Standard library only."""
import csv
import hashlib
import html
import math
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(LANE, '..', '..', '..'))

BOX = dict(lat_lo=31.600, lat_hi=31.900, lon_lo=35.120, lon_hi=35.560)

# water.csv columns (plan §8). Tri-state attributes use yes / no / unknown.
COLUMNS = [
    'id', 'lineage', 'source', 'locator', 'record_id', 'name', 'site_key', 'type', 'aggregate', 'count',
    'lat', 'lon', 'crs', 'precision_m', 'coord_source',
    'feed', 'feed_wadi', 'flow_from', 'dims', 'capacity_m3', 'shape', 'plaster', 'entrance',
    'great', 'north', 'head', 'head_marker', 'marker_side', 'bend', 'wall_at_outlet', 'fissure_east', 'solomon',
    'named_wadi', 'qelt', 'kidron_feed', 'cypros', 'jericho_oasis', 'qumran',
    'period_as_given', 'date_code', 'site_period_in_window', 'excavated',
    'dup_of', 'superseded_by', 'group_id', 'label', 'first_read_after_freeze', 'quote', 'span_sha256', 'notes',
]
TYPES = ['aqueduct', 'dam', 'reservoir_pool', 'cistern', 'well', 'spring', 'basin_tank', 'outlet', 'waterfall',
         'water_system']
R_EARTH_KM = 6371.0088
WBADB_SHA256 = '3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b'
ASI_MAPS = {'72': '101', '63': '102', '51': '105', '53': '106', '65': '83/1', '70': '83/2', '73': '83/12',
            '52': '108/2', '68': '109/4', '78': '109/5', '62': '109/7'}
EIN_KAREM = (31.766728, 35.161996)  # Wikidata Q1022487 P625 (plan §5, entry 46)

PLACES_CSV = os.path.join(REPO, 'research', 'agent_review_2026-10-07', 'wave2', 'W2B_model_v1', 'inputs_v2',
                          'places_v2.csv')


def load_places():
    out = {}
    with open(PLACES_CSV, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                out[r['place_id']] = (float(r['lat']), float(r['lon']), float(r['sigma_km'] or 0))
            except ValueError:
                pass
    return out


def in_box(lat, lon):
    return lat is not None and lon is not None and BOX['lat_lo'] <= lat <= BOX['lat_hi'] and \
        BOX['lon_lo'] <= lon <= BOX['lon_hi']


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(math.sqrt(a))


def bearing(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def sha256_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fold(s):
    """Lower case, strip diacritics and ayin/alef marks (amendment 1 §3)."""
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[ʿʾ'’‘`]", '', s).lower()


# ------------------------------------------------------------------ sentences
TAG = re.compile(r'<[^>]+>')
ABBR = re.compile(r'\b(ca|c|Kh|H|Ḥ|N|St|km|m|cf|No|no|fig|Fig|pl|Pl)\.\s', re.U)


def clean(text):
    t = html.unescape(TAG.sub(' ', text or ''))
    return re.sub(r'\s+', ' ', t.replace('\xa0', ' ')).strip()


def sentences(text):
    t = ABBR.sub(lambda m: m.group(1) + '․ ', clean(text))  # protect abbreviation stops
    parts = re.split(r'(?<=[.;!?])\s+|\n+', t)
    return [p.replace('․', '.').strip() for p in parts if p.strip()]


# ------------------------------------------------------------------ types (plan §4)
def wre(words):
    return re.compile(r'\b(?:' + '|'.join(words) + r')\b', re.I)


TYPE_RE = {
    'aqueduct': wre([r'aqueducts?', r'conduits?', r'water[- ]channels?', r'channels?', r'canals?',
                     r'water[- ]tunnels?', r'siphons?', r'water[- ]pipes?', r'pipelines?']),
    'dam': wre([r'dams?', r'weirs?', r'barrages?', r'dikes?', r'dykes?']),
    'reservoir_pool': wre([r'pools?', r'reservoirs?', r'birk(?:a|e|eh|et|at|ah)', r'open tanks?']),
    'cistern': wre([r'cisterns?', r'water[- ]holes?']),
    'well': re.compile(r'(?<!as )\bwells?\b(?![-‐])', re.I),
    'spring': wre([r'springs?', r'spring[- ]houses?']),
    'basin_tank': wre([r'basins?', r'tanks?', r'troughs?', r'settling tanks?']),
    'outlet': wre([r'outlets?', r'sluices?', r'spillways?', r'overflows?', r'inlets?', r'intakes?']),
    'waterfall': wre([r'waterfalls?', r'cascades?']),
    'water_system': wre([r'water systems?', r'water installations?', r'waterworks']),
}
SPRING_NAME = re.compile(r"^\s*(?:[ʿ'’]?(?:Ein|Ain|En))\s", re.I)
PRESS = wre([r'wine ?press(?:es)?', r'oil ?press(?:es)?', r'olive ?press(?:es)?', r'press(?:es)?',
             r'treading floors?'])
CHANNEL_ONLY = wre([r'channels?'])
SWIMMING = re.compile(r'swimming pools?', re.I)
SOLOMON_PHRASE = re.compile(r"\b(?:from|to|towards|toward|leading|leads|led)\b[^.;]{0,40}Solomon['’]?s Pools", re.I)
SOLOMON_POOL = re.compile(r"Solomon['’]?s Pools?|Pools? of Solomon|Birak Suleiman|Birket Suleiman|Birkat Suleiman|"
                          r"Birak Sulaiman|Birket Sulaiman", re.I)
WELL_EXCL = re.compile(r'\bwell[- ]?(?:known|preserved|built|constructed|dressed|cut|made|founded|defined|'
                       r'hewn|executed|plastered)\b|\bas well\b', re.I)


def type_hits(sentence, record_name=''):
    """Types coded in one sentence (plan §4 with its exclusions)."""
    out = set()
    press = bool(PRESS.search(sentence))
    for t, rx in TYPE_RE.items():
        ms = list(rx.finditer(sentence))
        if not ms:
            continue
        if t == 'well':
            s2 = WELL_EXCL.sub(' ', sentence)
            if not rx.search(s2):
                continue
        if t == 'reservoir_pool':
            s2 = SWIMMING.sub(' ', sentence)
            if not ('solomon' in fold(record_name) or 'suleiman' in fold(record_name)):
                s2 = SOLOMON_PHRASE.sub(' ', s2)
            if not rx.search(s2):
                continue
        if t == 'basin_tank' and press:
            continue
        if t == 'aqueduct' and press:
            # only the bare word "channel(s)" is press-sensitive
            s2 = CHANNEL_ONLY.sub(' ', sentence)
            if not rx.search(s2):
                continue
        out.add(t)
    return out


# ------------------------------------------------------------------ attribute words (plan §5 survey text)
ATTR_RE = {
    'great': wre(['great', 'large', 'big', 'huge', 'main', 'largest', 'enormous']),
    'north': wre(['north', 'northern']),
    'plaster': wre(['plaster', 'plastered']),
    'entrance': wre([r'steps?', r'stairs?', 'staircase', 'stepped', 'entrance', 'doorway']),
    'head': wre(['head', 'intake', 'begins', 'starts', 'source']),
    'stone': wre([r'stones?', r'boulders?']),
    'pool_marker': wre([r'pools?', r'basins?', r'reservoirs?']),
    'any_marker': wre([r'stones?', r'boulders?', r'pools?', r'basins?', r'reservoirs?', r'dams?', r'structures?']),
    'bend': wre([r'bends?', r'turns?', r'curves?', r'elbows?']),
    'wall': wre([r'walls?', 'row of stones', r'retaining walls?', r'courses?']),
    'fissure': wre([r'fissures?', r'cracks?', r'clefts?', r'crevices?']),
    'four': re.compile(r'\b(?:rectangular|square|quadrangular|oblong)\b|\d+(?:\.\d+)?\s*(?:m\s*)?(?:×|x|by)\s*\d',
                       re.I),
    'notfour': wre(['round', 'circular', 'oval', 'bell-shaped', 'pear-shaped', 'irregular', 'triangular']),
    'solomon': re.compile(r"\bsolomon|\bsuleiman|\bsulaiman", re.I),
}
FEED_RE = [
    re.compile(r'\b(?:fed|filled|supplied|diverted|led|leads|leading|conveyed|carried|brought|flowed|flows|'
               r'drained|draining)\b[^.;]{0,80}\b(?:channels?|conduits?|aqueducts?|canals?)\b', re.I),
    re.compile(r'\b(?:channels?|conduits?|aqueducts?|canals?)\b[^.;]{0,60}\b(?:to|into|feeding|fed|filling|filled|'
               r'supplying|supplied|leading to|leads to|led to)\b[^.;]{0,40}\b(?:cisterns?|reservoirs?|pools?)\b',
               re.I),
]
WADI_FEED_RE = re.compile(r'\bfrom (?:the )?(?:wadi|nahal|n\.|stream|streambed|stream bed|flood)', re.I)

# ------------------------------------------------------------------ dates (plan §5 common clause)
IN_LABELS = [r'hasmonaean', r'hasmonean', r'herodian', r'early roman', r'late second temple',
             r'first century (?:bce|ce|b\.c\.|a\.d\.|bc|ad)', r'1st (?:century|c\.) (?:bce|ce|bc|ad)',
             r'bar[- ]kokhba', r'bar[- ]kochba', r'herod\b', r'jannaeus', r'hyrcanus']
PARTLY_LABELS = [r'late hellenistic', r'hellenistic', r'middle roman', r'second temple', r'(?<!late )(?<!early )\broman\b',
                 r'second century (?:bce|ce)', r'2nd (?:century|c\.) (?:bce|ce)']
OUT_LABELS = [r'iron age', r'iron ii', r'persian', r'late roman', r'byzantine', r'early arab', r'early islamic',
              r'umayyad', r'abbasid', r'crusader', r'mamluk', r'mameluke', r'ottoman', r'modern', r'british mandate',
              r'chalcolithic', r'bronze', r'neolithic', r'medieval', r'arab period', r'islamic']
HEDGE = wre(['possibly', 'probably', 'prob', 'apparently', 'perhaps', 'may', 'might', 'presumably', 'likely'])
# WBADB notation (case-sensitive abbreviations, sourcebook p. 17), mapped onto the plan's labels:
# Rom1 = Early Roman (in); Hel, Rom, Hel-Rom = Hellenistic, Roman (partly); the rest are outside the window.
WB_IN = r'(?-i:\bRom ?1\b)'
WB_PARTLY = r'(?-i:\bHel\b|\bRom\b(?! ?1))'
WB_OUT = r'(?-i:\bByz\b|\bIA ?[12]?\b|\bEIs\b|\bCru\b|\bMam\b|\bMed\b|\bOtt\b|\bMB ?2?[abc]*\b|\bLB\b|' \
         r'\bEB ?[123]*\b|\bPer\b|\bChal\b)'
IN_RX = re.compile('|'.join(IN_LABELS + [WB_IN]), re.I)
PARTLY_RX = re.compile('|'.join(PARTLY_LABELS + [WB_PARTLY]), re.I)
OUT_RX = re.compile('|'.join(OUT_LABELS + [WB_OUT]), re.I)


def date_code(sentence):
    """Return (date_code, labels) for the labels in one sentence."""
    s = sentence or ''
    ins = [m.group(0) for m in IN_RX.finditer(s)]
    # remove in-window labels before testing the broader ones, so "Early Roman" is not also "Roman"
    s2 = IN_RX.sub(' ', s)
    s2_noout = OUT_RX.sub(' ', s2)
    parts = [m.group(0) for m in PARTLY_RX.finditer(s2_noout)]
    outs = [m.group(0) for m in OUT_RX.finditer(s2)]
    labels = ins + parts + outs
    if ins:
        return ('in_hedged' if (HEDGE.search(s) or '(?)' in s) else 'in'), labels
    if parts:
        return 'partly', labels
    if outs:
        return 'out', labels
    return 'undated', labels


DATE_RANK = {'in': 0, 'in_hedged': 1, 'partly': 2, 'out': 3, 'undated': 4}


def combine_dates(codes):
    """Combine sentence codes of one row: any in-window phase wins (plan §5)."""
    codes = [c for c in codes if c]
    if not codes:
        return 'undated'
    for c in ('in', 'in_hedged', 'partly'):
        if c in codes:
            return c
    if 'out' in codes:
        return 'out'
    return 'undated'


# ------------------------------------------------------------------ names (kohlit stage 1b skeleton)
DROP = {'el', 'al', 'es', 'esh', 'ed', 'en', 'er', 'et', 'ez', 'ej', 'ech', 'ha', 'he', 'the', 'kh', 'khirbet',
        'khirbat', 'khurbet', 'horvat', 'h', 'tell', 'tel', 'ein', 'ain', 'wadi', 'nahal', 'bir', 'birket', 'birkat',
        'qasr', 'rujm', 'mt', 'mount', 'jebel', 'n', 'site', 'cave', 'of'}


def skeleton(name):
    s = fold(name)
    s = re.sub(r'[^a-z ]', ' ', s)
    toks = [t for t in s.split() if t not in DROP]
    s = ''.join(toks)
    s = s.replace('kh', 'h').replace('q', 'k')
    s = re.sub(r'(.)\1+', r'\1', s)
    s = re.sub(r'[aeiou]', '', s)
    return s
