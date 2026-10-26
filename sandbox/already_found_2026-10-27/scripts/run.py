"""Sandbox run 4 (already_found_2026-10-27): apply RULE.md (commit 0d0240b) literally.

Inputs (read-only, repo): hoards.csv (include=1), Method 10 scroll_sums.json and hoard masses
(match_results.json), scroll_contexts.csv (P branch), places.csv + ratings.csv candidates,
atlas-data.json for coordinates of ratings candidates missing from places.csv.
Standard library only. Deterministic (seed 20261027).
"""
import csv, json, math, random, re, sys, itertools
from collections import defaultdict, Counter

REPO = '/home/claude/copperscroll'
OUT = '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/already_found_2026-10-27'
SEED = 20261027
NPERM = 10000

H_ALL = list(csv.DictReader(open(f'{REPO}/research/comparanda/hoards_full/hoards.csv', encoding='utf-8')))
M10 = {h['id']: h for h in json.load(open(f'{REPO}/research/first_tests_2026-10-24/method10_hoards/match_results.json'))['hoards']}
SUMS = json.load(open(f'{REPO}/research/first_tests_2026-10-24/method10_hoards/scroll_sums.json'))
CTX = {r['entry']: r for r in csv.DictReader(open(f'{REPO}/research/comparanda/concealment_contexts/scroll_contexts.csv', encoding='utf-8'))}
PLACES = {p['place_id']: p for p in csv.DictReader(open(f'{REPO}/research/measurements/sequence/places.csv', encoding='utf-8'))}
RATINGS = list(csv.DictReader(open(f'{REPO}/research/assessments/evidence_components/ratings.csv', encoding='utf-8')))
ATLAS = {p['id']: p for p in json.load(open(f'{REPO}/atlas/app/atlas-data.json'))['places']}

# Mass fixes for Method-10 rows whose silver is recorded as 0 although CHRE (T02 chre_details.json) states silver.
# Applied only in the 'fixed' variant; documented as a deviation. Values: count x registered standard mass.
MASS_FIX = {
    'chre7281': (13 * 14.2, 0.0, 'CHRE summary: 13 provincial tetradrachms'),
    'chre7603': (3 * 14.2, 0.0, 'CHRE summary: 3 silver tetradrachms (+3 bronze)'),
}

BOX = (31.40, 32.55, 35.00, 35.60)


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(d))


def coord(pid):
    p = PLACES.get(pid)
    if p and p['lat'] and p['lon']:
        return float(p['lat']), float(p['lon']), 'places.csv'
    a = ATLAS.get(pid)
    if a and a.get('lat') is not None:
        return float(a['lat']), float(a['lon']), 'atlas-data.json'
    return None


# ---- candidates per entry: union of ratings.csv and places.csv entry lists
cand = defaultdict(set)
for r in RATINGS:
    if r['candidate']:
        cand[r['entry']].add(r['candidate'])
for pid, p in PLACES.items():
    for fld in ('entries_best_supported', 'entries_possible'):
        for m in re.finditer(r'(\d+a?)\(', p[fld]):
            cand[m.group(1)].add(pid)

# ---- scroll units: entries with sums
entries = []
by_entry = defaultdict(list)
for s in SUMS:
    by_entry[s['entry']].append(s)
for e in sorted(by_entry, key=lambda x: (int(re.match(r'\d+', x).group(0)), x)):
    c = CTX[e]
    placed = {pid: coord(pid) for pid in sorted(cand[e]) if coord(pid)}
    unplaced = sorted(pid for pid in cand[e] if not coord(pid))
    entries.append(dict(entry=e, sums=by_entry[e], fine=c['fine_P'], coarse=c['coarse_P'],
                        setting=c['setting_P'], placement=c['placement_P'], container=c['container_P'],
                        placed=placed, unplaced=unplaced, use_box=not placed))


def sum_mass_g(s, reading, weight):
    t = (21.3 if weight == 'light' else 42.6) * 1000
    if reading == 'karsh' and s['unit'] == 'kk':
        return s['value'] * t / 300
    if reading == 'allkarsh':  # deviation D1: every sum read as karsh
        return s['value'] * t / 300
    return s['value'] * t


def midpoint(h):
    try:
        a = float(h['date_from']); b = float(h['date_to']) if h['date_to'] else a
    except ValueError:
        return None
    return (a + b) / 2


def build_hoards(variant):
    out = []
    for h in H_ALL:
        if h['include'] != '1':
            continue
        m = M10.get(h['id'])
        ag = au = None
        mass_note = ''
        if m is not None:
            if m['excluded'] and variant['qumran_merge']:
                continue  # Method 10 merged Qumran 1955 B and C into A (7.8 kg printed for all three pots)
            ag = (m['ag_lo'], m['ag_hi']); au = (m['au_lo'], m['au_hi'])
            mass_note = m['basis']
            if h['id'] == 'chre7692' and not variant['qumran_merge']:
                ag = tuple(m['count_based']); mass_note = 'count-based (pot A alone)'
            if ag[1] + au[1] <= 0:
                if variant['fix'] and h['id'] in MASS_FIX:
                    f = MASS_FIX[h['id']]; ag = (f[0], f[0]); au = (f[1], f[1]); mass_note = 'fixed: ' + f[2]
                else:
                    ag = au = None; mass_note = 'Method 10 mass 0 (contents not parsed)'
        else:
            ot = h['object_type'].lower()
            if re.search(r'silver|gold', ot):
                mass_note = 'precious metal, no mass in Method 10'
            elif 'bronze' in ot or 'lead' in ot or 'document' in ot:
                ag = au = (0.0, 0.0); mass_note = 'no silver or gold (object_type: %s)' % h['object_type']
            else:
                mass_note = 'metal unknown (object_type: %s)' % h['object_type']
        mp = midpoint(h)
        try:
            ll = (float(h['lat']), float(h['lon']))
        except ValueError:
            ll = None
        if variant['window'] == 'midpoint':
            inwin = mp is not None and -63 <= mp <= 135
        else:  # overlap
            try:
                a = float(h['date_from']); b = float(h['date_to']) if h['date_to'] else a
                inwin = a <= 135 and b >= -63
            except ValueError:
                inwin = False
        out.append(dict(id=h['id'], site=h['site'], ag=ag, au=au, mass_note=mass_note, ll=ll, inwin=inwin,
                        fine=h['context_category'], coarse=h['coarse_group'], setting=h['setting'],
                        placement=h['placement'], container=h['container'], context_text=h['context_reported'],
                        source=h['source'], date=(h['date_from'], h['date_to']), object_type=h['object_type']))
    return out


def metal_mass(metal, ag, au, end):
    i = 0 if end == 'lo' else 1
    if metal == 'silver':
        return ag[i]
    if metal == 'gold':
        return au[i]
    return ag[i] + au[i]


def c1(entry_sums, h):
    """Metal: hoard holds the metal the sum names. None = unknown."""
    if h['ag'] is None:
        return None
    for s in entry_sums:
        if metal_mass(s['metal'], h['ag'], h['au'], 'hi') > 0:
            return True
    return False


def c2_total(entry_sums, h, reading, weight, mode):
    """Mass alone: total precious-metal mass within E/2..2E (metal ignored)."""
    if h['ag'] is None:
        return None
    lo, hi = h['ag'][0] + h['au'][0], h['ag'][1] + h['au'][1]
    return any(inrange(lo, hi, sum_mass_g(s, reading, weight), mode) for s in entry_sums)


def c12(entry_sums, h, reading, weight, mode):
    """Metal and mass jointly: the named metal's mass within E/2..2E for at least one sum of the entry."""
    if h['ag'] is None:
        return None
    for s in entry_sums:
        lo = metal_mass(s['metal'], h['ag'], h['au'], 'lo'); hi = metal_mass(s['metal'], h['ag'], h['au'], 'hi')
        if hi > 0 and inrange(lo, hi, sum_mass_g(s, reading, weight), mode):
            return True
    return False


def inrange(lo, hi, E, mode):
    if mode == 'sure':
        return E / 2 <= lo <= 2 * E and E / 2 <= hi <= 2 * E
    return hi >= E / 2 and lo <= 2 * E  # 'possible': interval overlap


def c3(ctx, h, level):
    if h['fine'] == 'UNK' or not h['fine']:
        return None  # unknown context = no match
    if level == 'fine':
        return h['fine'] == ctx['fine']
    return bool(h['coarse']) and h['coarse'] == ctx['coarse']


def c4(e, h):
    if h['ll'] is None:
        return None
    if e['use_box']:
        return BOX[0] <= h['ll'][0] <= BOX[1] and BOX[2] <= h['ll'][1] <= BOX[3]
    return min(hav(h['ll'], c[:2]) for c in e['placed'].values()) <= 5.0


def nearest(e, h):
    if h['ll'] is None or e['use_box']:
        return None
    return min((hav(h['ll'], c[:2]), pid) for pid, c in e['placed'].items())


def evaluate(entries_, hoards, reading, weight, level, mode, place_fixed=None):
    """Return list of (entry, hoard, flags) for in-window hoards. place_fixed: per-entry place records."""
    rows = []
    for idx, e in enumerate(entries_):
        pe = place_fixed[idx] if place_fixed else e
        for h in hoards:
            if not h['inwin']:
                continue
            f = dict(c1=c1(e['sums'], h), c2=c2_total(e['sums'], h, reading, weight, mode),
                     c12=c12(e['sums'], h, reading, weight, mode), c3=c3(e, h, level), c4=c4(pe, h))
            rows.append((pe['entry'], h, f))
    return rows


def tally(rows):
    t = Counter()
    for _, _, f in rows:
        T = {k: (v is True) for k, v in f.items()}
        t['n_pairs'] += 1
        for k in ('c1', 'c2', 'c3', 'c4'):
            t[k] += T[k]
        t['c12'] += T['c12']
        for a, b in itertools.combinations(['c1', 'c2', 'c3', 'c4'], 2):
            t[a + '&' + b] += T[a] and T[b]
        t['c12&c3'] += T['c12'] and T['c3']
        t['c12&c4'] += T['c12'] and T['c4']
        t['c3&c4'] += T['c3'] and T['c4']
        t['c12&c3&c4'] += T['c12'] and T['c3'] and T['c4']
        t['all4'] += T['c12'] and T['c3'] and T['c4']
        # fail only on condition 3 because context unknown (AF447 gap)
        t['fail_only_c3_unknown'] += T['c12'] and T['c4'] and f['c3'] is None
        t['fail_only_c3_known_mismatch'] += T['c12'] and T['c4'] and f['c3'] is False
        # mass unknown but the other three hold
        t['c3&c4_mass_unknown'] += T['c3'] and T['c4'] and f['c12'] is None
    return t


def k_of(rows):
    return sum(1 for _, _, f in rows if f['c12'] is True and f['c3'] is True and f['c4'] is True)


def perm_test(hoards, reading, weight, level, mode, k_obs):
    # Bitmask form: bundle b (sums + context) travels; place stays with position i.
    rng = random.Random(SEED)
    hw = [h for h in hoards if h['inwin']]
    MB = []  # per bundle: hoards meeting c12 and c3
    for e in entries:
        m = 0
        for j, h in enumerate(hw):
            if c12(e['sums'], h, reading, weight, mode) is True and c3(e, h, level) is True:
                m |= 1 << j
        MB.append(m)
    PB = []  # per position: hoards meeting c4
    for e in entries:
        m = 0
        for j, h in enumerate(hw):
            if c4(e, h) is True:
                m |= 1 << j
        PB.append(m)
    assert sum(bin(MB[i] & PB[i]).count('1') for i in range(len(entries))) == k_obs
    idx = list(range(len(entries)))
    ge = 0
    dist = Counter()
    for _ in range(NPERM):
        rng.shuffle(idx)
        k = sum(bin(MB[idx[i]] & PB[i]).count('1') for i in range(len(entries)))
        dist[k] += 1
        ge += k >= k_obs
    return ge / NPERM, dict(sorted(dist.items()))


def main():
    variants = {
        'main': dict(qumran_merge=True, fix=False, window='midpoint'),
        'fixmass': dict(qumran_merge=True, fix=True, window='midpoint'),
        'qumran_pots_separate': dict(qumran_merge=False, fix=False, window='midpoint'),
        'window_overlap': dict(qumran_merge=True, fix=False, window='overlap'),
    }
    branches = [(r, w) for r in ('karsh', 'talent', 'allkarsh') for w in ('light', 'heavy')]
    results = {}
    leads = []
    nearmiss = []
    for vname, v in variants.items():
        hoards = build_hoards(v)
        for level in ('fine', 'coarse'):
            for mode in ('sure', 'possible'):
                for reading, weight in branches:
                    key = f'{vname}|{level}|{mode}|{reading}|{weight}'
                    rows = evaluate(entries, hoards, reading, weight, level, mode)
                    t = tally(rows)
                    k = t['all4']
                    do_perm = (vname == 'main' and mode == 'sure') or k > 0
                    p, dist = perm_test(hoards, reading, weight, level, mode, k) if do_perm else (None, None)
                    results[key] = dict(k=k, p=p, null_dist=dist, tally=dict(t),
                                        entries=sorted({e for e, h, f in rows if f['c12'] and f['c3'] and f['c4']}))
                    for e, h, f in rows:
                        if f['c12'] and f['c3'] and f['c4']:
                            leads.append(dict(branch=key, entry=e, hoard=h['id'], site=h['site']))
                        if vname == 'main' and mode == 'sure' and f['c3'] and f['c4'] and f['c12'] is not True:
                            nearmiss.append(dict(branch=key, entry=e, hoard=h['id'], site=h['site'], c12=f['c12'], c1=f['c1']))
                    print(f'{key:55s} k={k} p={p} c1={t["c1"]} c2={t["c2"]} c12={t["c12"]} c3={t["c3"]} c4={t["c4"]} '
                          f'c12&c4={t["c12&c4"]} c3&c4={t["c3&c4"]} c12&c3={t["c12&c3"]} '
                          f'onlyC3unk={t["fail_only_c3_unknown"]} onlyC3mis={t["fail_only_c3_known_mismatch"]} '
                          f'c3c4_massunk={t["c3&c4_mass_unknown"]} pairs={t["n_pairs"]}')
    json.dump(dict(results=results, leads=leads, nearmiss=nearmiss), open(f'{OUT}/results.json', 'w'), indent=1, ensure_ascii=False)

    # per-entry detail table (main pool)
    hoards = build_hoards(variants['main'])
    inw = [h for h in hoards if h['inwin']]
    with open(f'{OUT}/entry_table.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['entry', 'sums', 'fine_P', 'coarse_P', 'placed_candidates', 'unplaced_candidates', 'place_rule',
                    'hoards_within_5km_or_box', 'of_which_known_context', 'same_fine_context_and_place',
                    'same_coarse_context_and_place', 'mass_match_and_place_klight', 'mass_match_and_place_kheavy',
                    'mass_match_and_place_tlight', 'mass_match_and_place_theavy'])
        for e in entries:
            near = [h for h in inw if c4(e, h)]
            known = [h for h in near if h['fine'] != 'UNK']
            ff = [h['id'] for h in near if c3(e, h, 'fine')]
            cc = [h['id'] for h in near if c3(e, h, 'coarse')]
            mm = {}
            for r, wgt in (('karsh', 'light'), ('karsh', 'heavy'), ('talent', 'light'), ('talent', 'heavy')):
                mm[(r, wgt)] = [h['id'] for h in near if c12(e['sums'], h, r, wgt, 'sure')]
            w.writerow([e['entry'], '; '.join(f"{s['line']} {s['value']:g} {s['unit']} {s['metal']}" for s in e['sums']),
                        e['fine'], e['coarse'], ' '.join(e['placed']), ' '.join(e['unplaced']),
                        'region box' if e['use_box'] else '5 km', len(near), len(known), ' '.join(ff), ' '.join(cc),
                        ' '.join(mm[('karsh', 'light')]), ' '.join(mm[('karsh', 'heavy')]),
                        ' '.join(mm[('talent', 'light')]), ' '.join(mm[('talent', 'heavy')])])
    # hoard table (main pool, in window)
    with open(f'{OUT}/hoard_table.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['id', 'site', 'date_from', 'date_to', 'object_type', 'ag_g', 'au_g', 'mass_note', 'fine', 'coarse',
                    'lat', 'lon', 'entries_within_5km_or_box', 'nearest_candidate_km'])
        for h in inw:
            ens = [e['entry'] for e in entries if c4(e, h)]
            nn = min((nearest(e, h) for e in entries if nearest(e, h)), default=None)
            w.writerow([h['id'], h['site'], h['date'][0], h['date'][1], h['object_type'],
                        '' if h['ag'] is None else f"{h['ag'][0]:.1f}-{h['ag'][1]:.1f}",
                        '' if h['au'] is None else f"{h['au'][1]:.1f}", h['mass_note'], h['fine'], h['coarse'],
                        h['ll'][0] if h['ll'] else '', h['ll'][1] if h['ll'] else '', ' '.join(ens),
                        '' if nn is None else f'{nn[0]:.2f} ({nn[1]})'])
    print('entries', len(entries), 'in-window hoards', len(inw), 'box entries', [e['entry'] for e in entries if e['use_box']])
    print('coords from atlas:', sorted({pid for e in entries for pid, c in e['placed'].items() if c[2] != 'places.csv'}))


if __name__ == '__main__':
    main()
