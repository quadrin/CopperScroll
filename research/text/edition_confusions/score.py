"""How common is the letter confusion that a disputed reading needs?

    python3 -I research/text/edition_confusions/score.py "II 3" המרה המדה          # one pair
    python3 -I research/text/edition_confusions/score.py "IV 6" hbynyn hkynyn --words 2
    python3 -I research/text/edition_confusions/score.py --apply          # all disputes in readings.json
    python3 -I research/text/edition_confusions/score.py --apply --check  # compare with scored_readings.csv

The table is variants.csv (SHAPE rows), rebuilt without the place being scored (leave one place out):
every place on the same line whose word index is among the scored words, and every row that came
from the same readings.json record. Frozen rule (PLAN.md section 8):
  RARE      leave-one-out count_places = 0 (the rate is the add-one floor)
  UNCOMMON  1 or 2
  COMMON    3 or more
  MATRES    a yod-waw substitution, never flagged RARE
Insertions and deletions are reported, not flagged. Locations in column XII lines 8-12 are refused.
"""
import argparse, csv, io, json, random, re, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from align import YW, N_UNORDERED_PAIRS, LETTERS, levenshtein_ops, pair_key  # noqa: E402
from build import parse_reading, classify, SEED, N_BOOT, place_sort  # noqa: E402
from exclusion import is_excluded, mentions_excluded, ROMAN  # noqa: E402

RARE_MAX = 0
UNCOMMON_MAX = 2
OUT = HERE / 'scored_readings.csv'
OUT_FIELDS = ['record_id', 'location', 'words', 'who_a', 'reading_a', 'who_b', 'reading_b', 'letters_a', 'letters_b',
              'pair_class', 'needed_shape', 'needed_yod_waw', 'insertions', 'deletions', 'n_rare', 'flag']


# ------------------------------------------------------------------ table

def load_events(path=HERE / 'variants.csv'):
    """[(pair, place, row_note)] for SHAPE substitutions, and yod-waw places."""
    ev, yw = [], []
    with open(path, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            for e in filter(None, r['shape_events'].split(';')):
                pair, place = e.split('@')
                ev.append((pair, place, r['note']))
            for e in filter(None, r['yod_waw_events'].split(';')):
                yw.append((e.split('@')[1], r['note']))
    return ev, yw


def parse_location(location: str):
    parts = location.replace(':', ' ').split()
    if len(parts) < 2:
        raise ValueError('location must look like "II 3"')
    return parts[0], int(parts[1])


def excluded_places(positions, rj_id, events):
    """Places to leave out: positions are [(column, line, words or None)]."""
    out = set()
    places = {p for _, p, _ in events}
    for p in places:
        c, l, w = p.split(' ', 2)
        for col, line, words in positions:
            if c == col and int(l) == line and (words is None or w.startswith('w?') or
                                                (w[1:].isdigit() and int(w[1:]) in words)):
                out.add(p)
    if rj_id:
        tag = f'rj:{rj_id}'
        for pair, p, note in events:
            if re.search(re.escape(tag) + r'(?![\w-])', note):
                out.add(p)
    return out


def by_place(events, exclude=frozenset()):
    t = defaultdict(set)
    for pair, p, _ in events:
        if p not in exclude:
            t[pair].add(p)
    return t


def ci_for(table, pairs, n_boot=N_BOOT, seed=SEED):
    """90% bootstrap interval (resampling places) of the add-one rate, for the given pairs."""
    place_pairs = defaultdict(set)
    for pair, ps in table.items():
        for p in ps:
            place_pairs[p].add(pair)
    places = sorted(place_pairs, key=place_sort)
    sizes = [len(place_pairs[p]) for p in places]
    where = {pair: [i for i, p in enumerate(places) if pair in place_pairs[p]] for pair in pairs}
    rng = random.Random(seed)
    vals = defaultdict(list)
    n = len(places)
    for _ in range(n_boot):
        mult = Counter(rng.choices(range(n), k=n)) if n else Counter()
        total = sum(sizes[i] * m for i, m in mult.items())
        for pair in pairs:
            c = sum(mult.get(i, 0) for i in where[pair])
            vals[pair].append((c + 1) / (total + N_UNORDERED_PAIRS))
    out = {}
    for pair, v in vals.items():
        v.sort()
        out[pair] = (v[int(0.05 * (len(v) - 1))], v[int(round(0.95 * (len(v) - 1)))])
    return out


def flag_for(count):
    if count <= RARE_MAX:
        return 'RARE'
    if count <= UNCOMMON_MAX:
        return 'UNCOMMON'
    return 'COMMON'


# ------------------------------------------------------------------ scoring

def score(location, reading_a, reading_b, words=None, rj_id=None, also=(), events=None, yw_events=None):
    """Return the needed changes between two readings and how common each is elsewhere."""
    col, line = parse_location(location)
    positions = [(col, line, words)] + list(also)
    for c, l, _ in positions:
        if is_excluded(c, l):
            raise ValueError('refused: column XII lines 8-12 are reserved for the frozen XII 10 test')
    if events is None:
        events, yw_events = load_events()
    excl = excluded_places(positions, rj_id, events)
    table = by_place(events, excl)
    N = sum(len(v) for v in table.values())
    yw_places = {p for p, note in (yw_events or []) if p not in excl}
    a_seq, b_seq = parse_reading(reading_a), parse_reading(reading_b)
    la, lb = ''.join(x[0] for x in a_seq), ''.join(x[0] for x in b_seq)
    cls, _, _ = classify(a_seq, b_seq)
    ops = levenshtein_ops(la, lb)
    shape, yw, ins, dels = [], [], [], []
    for op, x, y, i, j in ops:
        if op == 'S':
            if x in YW and y in YW:
                yw.append({'pair': pair_key(x, y), 'change': f'{x}→{y}', 'loo_places': len(yw_places), 'flag': 'MATRES'})
            else:
                shape.append({'pair': pair_key(x, y), 'change': f'{x}→{y}'})
        elif op == 'D':
            dels.append(x)
        elif op == 'I':
            ins.append(y)
    pairs = sorted({s['pair'] for s in shape})
    ci = ci_for(table, pairs) if pairs else {}
    for s in shape:
        c = len(table.get(s['pair'], ()))
        s.update({'loo_places': c, 'rate': round((c + 1) / (N + N_UNORDERED_PAIRS), 6),
                  'ci90': [round(ci[s['pair']][0], 6), round(ci[s['pair']][1], 6)], 'flag': flag_for(c)})
    n_rare = sum(1 for s in shape if s['flag'] == 'RARE')
    return {'location': location, 'letters_a': la, 'letters_b': lb, 'class': cls, 'loo_N': N,
            'loo_excluded_places': len(excl), 'shape': shape, 'yod_waw': yw, 'insertions': ins, 'deletions': dels,
            'n_rare': n_rare, 'needs_rare_confusion': n_rare > 0}


# ------------------------------------------------------------------ readings.json

def split_alternatives(reading: str):
    """Each printed alternative is a separate reading (PLAN.md section 5)."""
    parts = [p for p in re.split(r'\s+/\s+|;\s*|\s+or\s+', reading) if p.strip()]
    out = []
    for p in parts:
        todo = [p.strip()]
        while todo:
            t = todo.pop()
            m = re.search(r'(\S)/(\S)', t)
            if not m:
                out.append(t)
                continue
            todo.append(t[:m.start()] + m.group(1) + t[m.end():])
            todo.append(t[:m.start()] + m.group(2) + t[m.end():])
    return out


def disputes(records):
    for r in records:
        if not r.get('line'):
            continue
        positions = [r['line']] + [a['line'] for a in r.get('also', [])]
        if any(is_excluded(*p.split()) for p in positions):
            continue
        alts = []
        for x in r['readings']:
            if not x['reading'].strip():
                continue
            for alt in split_alternatives(x['reading']):
                letters = ''.join(c[0] for c in parse_reading(alt))
                if letters:
                    alts.append((letters, x['who'], alt))
        groups = {}
        for letters, who, alt in alts:
            g = groups.setdefault(letters, {'who': [], 'reading': alt})
            if who not in g['who']:
                g['who'].append(who)
        keys = list(groups)
        if len(keys) < 2:
            continue
        also = [(a['line'].split()[0], int(a['line'].split()[1]), a.get('words')) for a in r.get('also', [])]
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                yield r, groups[keys[i]], groups[keys[j]], also


def apply_all():
    records = json.loads((ROOT / 'text' / 'readings.json').read_text(encoding='utf-8'))
    events, yw_events = load_events()
    rows = []
    for rec, ga, gb, also in disputes(records):
        res = score(rec['line'], ga['reading'], gb['reading'], words=rec.get('words'), rj_id=rec['id'],
                    also=also, events=events, yw_events=yw_events)
        rows.append({
            'record_id': rec['id'], 'location': rec['line'],
            'words': '-'.join(str(w) for w in rec.get('words') or []),
            'who_a': '; '.join(ga['who']), 'reading_a': ga['reading'],
            'who_b': '; '.join(gb['who']), 'reading_b': gb['reading'],
            'letters_a': res['letters_a'], 'letters_b': res['letters_b'], 'pair_class': res['class'],
            'needed_shape': ' | '.join(f"{s['change']} {s['pair']} loo={s['loo_places']} rate={s['rate']}"
                                       f" ci90=[{s['ci90'][0]},{s['ci90'][1]}] {s['flag']}" for s in res['shape']),
            'needed_yod_waw': ' | '.join(f"{s['change']} loo_places={s['loo_places']} MATRES" for s in res['yod_waw']),
            'insertions': ''.join(res['insertions']), 'deletions': ''.join(res['deletions']),
            'n_rare': res['n_rare'],
            'flag': 'NEEDS_RARE' if res['needs_rare_confusion'] else ('NO_SHAPE_CHANGE' if not res['shape'] else 'OK'),
        })
    return rows


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=OUT_FIELDS, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('location', nargs='?')
    ap.add_argument('reading_a', nargs='?')
    ap.add_argument('reading_b', nargs='?')
    ap.add_argument('--words', default=None, help='word indices of the place, e.g. 2 or 1-2')
    ap.add_argument('--apply', action='store_true', help='score every dispute in text/readings.json')
    ap.add_argument('--check', action='store_true', help='with --apply: compare with scored_readings.csv')
    args = ap.parse_args()
    if args.apply:
        text = render(apply_all())
        if mentions_excluded(text):
            raise SystemExit('output mentions the excluded zone')
        if args.check:
            ok = OUT.read_text(encoding='utf-8') == text
            print('check:', 'OK' if ok else 'differs')
            sys.exit(0 if ok else 1)
        OUT.write_text(text, encoding='utf-8')
        print(f'{text.count(chr(10)) - 1} scored pairs -> {OUT.name}')
        return
    if not (args.location and args.reading_a and args.reading_b):
        ap.error('give a location and two readings, or --apply')
    words = [int(x) for x in args.words.split('-')] if args.words else None
    print(json.dumps(score(args.location, args.reading_a, args.reading_b, words=words), ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
