"""Method 10 hoard check: apply the registered rule (registration.md, SHA-256 c74724e6...) to the compiled hoards."""
import csv, json, re, os
from collections import defaultdict

D = '/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests/hoard'
H = list(csv.DictReader(open(f'{D}/compiled/hoards.csv', encoding='utf-8')))
S = json.load(open(f'{D}/scroll_sums.json'))

# Registered standard masses (g). Added after registration, flagged: tridrachm, triobol.
STD = [(r'half[- ]shekel|didrachm', 7.1), (r'shekel|sela|tetradrachm', 14.2), (r'tridrachm', 10.65),
       (r'quinari|hemidrachm|triobol', 1.9), (r'denari|drachm', 3.8), (r'aure', 7.9)]
EXCLUDE = {'igch1616', 'igch1617', 'igch1622', 'igch1627', 'chre18785', 'chre18786'}  # IGCH rows: read from coinhoards.org, whose robots.txt bars Anthropic's crawler; Qumran B and C: merged into Qumran A, one deposit in three pots, using the printed 7.8 kg for all three  # read from coinhoards.org, whose robots.txt bars Anthropic's crawler


def first_int(s):
    m = re.search(r'\d[\d,]*', s or '')
    return int(m.group(0).replace(',', '')) if m else None


def masses(h):
    """Return (silver_lo, silver_hi, gold_lo, gold_hi, basis) in grams."""
    ag = [0.0, 0.0]; au = [0.0, 0.0]; basis = 'count x standard mass'; unk = False
    for part in h['contents'].split(';'):
        m = re.search(r'^(.*?)\s*\[(AR|AV)\]\s*(.*)$', part.strip())
        if not m:
            continue
        name, metal, rest = m.group(1).lower(), m.group(2), m.group(3)
        n = first_int(rest)
        if n is None:
            continue
        mass = None
        for pat, g in STD:
            if re.search(pat, name):
                mass = g; break
        if mass is None:
            lo, hi = 1.9, 14.2; unk = True
        else:
            lo = hi = mass
        tgt = au if metal == 'AV' else ag
        tgt[0] += n * lo; tgt[1] += n * hi
    pw = h['printed_total_weight_g']
    m = re.search(r'([\d.]+)\s*kg', pw or '')
    if m:
        v = float(m.group(1)) * 1000
        return v, v, au[0], au[1], 'printed (estimate)', (ag[0], ag[1])
    if unk:
        basis += '; some denominations unknown (1.9-14.2 g)'
    return ag[0], ag[1], au[0], au[1], basis, None


def sum_mass(s, talent_kg, reading):
    t = talent_kg * 1000
    if reading == 'karsh' and s['unit'] == 'kk':
        return s['value'] * t / 300
    return s['value'] * t


def metal_mass(s, hm, end):
    ag = hm[0] if end == 'lo' else hm[1]
    au = hm[2] if end == 'lo' else hm[3]
    if s['metal'] == 'silver':
        return ag
    if s['metal'] == 'gold':
        return au
    return ag + au


rows = []
for h in H:
    hm = masses(h)
    if h['id'] == 'chre9152':  # published as 500-800 Tyrian shekels: registered rule takes the middle
        hm = (650 * 14.2, 650 * 14.2, 0, 0, 'count x standard mass (middle of 500-800)', (500 * 14.2, 800 * 14.2))
    rows.append(dict(id=h['id'], name=h['name_as_published'], window=h['window'], excluded=h['id'] in EXCLUDE,
                     ag_lo=hm[0], ag_hi=hm[1], au_lo=hm[2], au_hi=hm[3], basis=hm[4], count_based=hm[5]))

out = {}
for window in ('A', 'B'):
    pool = [r for r in rows if r['window'] == window and not r['excluded']]
    for reading in ('talent', 'karsh'):
        for tname, tkg in (('light', 21.3), ('heavy', 42.6)):
            res = []
            for s in S:
                if reading == 'karsh' and s['unit'] != 'kk':
                    continue  # P2 counts the 30 kk sums; full-form sums stay talents (covered by the talent run)
                E = sum_mass(s, tkg, reading)
                hits_sure, hits_possible = [], []
                for r in pool:
                    hm = (r['ag_lo'], r['ag_hi'], r['au_lo'], r['au_hi'])
                    lo, hi = metal_mass(s, hm, 'lo'), metal_mass(s, hm, 'hi')
                    if hi <= 0:
                        continue
                    if E / 2 <= lo <= 2 * E and E / 2 <= hi <= 2 * E:
                        hits_sure.append(r['id'])
                    elif hi >= E / 2 and lo <= 2 * E:
                        hits_possible.append(r['id'])
                res.append(dict(entry=s['entry'], line=s['line'], unit=s['unit'], value=s['value'], metal=s['metal'],
                                mass_kg=round(E / 1000, 3), sure=hits_sure, possible=hits_possible))
            out[f'{window}|{reading}|{tname}'] = res

json.dump(dict(hoards=rows, results=out), open(f'{D}/match_results.json', 'w'), ensure_ascii=False, indent=1)
for k, res in out.items():
    sure = sum(1 for x in res if x['sure']); poss = sum(1 for x in res if x['sure'] or x['possible'])
    print(f'{k:22s} sums {len(res):2d}  matched (sure) {sure:2d}  matched (incl. unknown-denomination ranges) {poss:2d}')
big = sorted(rows, key=lambda r: -(r['ag_hi'] + r['au_hi']))[:8]
for r in big:
    print(f"{r['id']:22s} {r['window']} AG {r['ag_lo']/1000:.2f}-{r['ag_hi']/1000:.2f} kg AU {r['au_hi']/1000:.3f} kg {r['basis']} {'' if r['count_based'] is None else 'count-based %.1f-%.1f kg' % (r['count_based'][0]/1000, r['count_based'][1]/1000)} {'EXCLUDED' if r['excluded'] else ''}")
