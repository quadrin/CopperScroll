import json, re, csv, sys
from collections import defaultdict, OrderedDict

BASE = '/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests/hoard'
d = json.load(open(BASE + '/raw/chre/parsed.json'))
ids = [x.strip() for x in open(BASE + '/raw/chre/cand_ids2.txt') if x.strip()]
q1 = {r['id']: r for r in csv.DictReader(open(BASE + '/raw/chre/q1.out', encoding='utf-8'))}

# CHRE records not carried into the table (reason recorded in notes.md)
EXCLUDE = {
    '7659': 'bronze mint debitage only', '7703': 'prutot/uncertain metal (bronze hoard per Bijovsky 2009)',
    '7724': 'bronze only', '8132': 'bronze only', '18771': 'bronze only (same find as 8132?)',
    '9041': 'bronze only', '8463': 'bronze only', '8500': 'bronze, no count', '9040': 'bronze, no count',
    '18784': 'bronze only', '20958': 'Late Roman nummi, out of window', '7691': 'metal not recorded',
    '8009': 'metal not recorded; closing 100-300 CE', '8526': 'metal not recorded; closing 100-300 CE',
    '8046': 'no count', '8445': 'no count', '8455': 'no count', '7841': 'no count',
    '8084': 'no count', '8085': 'no count', '8086': 'no count',
    '9728': 'findspot only "Lebanon" (cannot place inside box)', '21015': 'findspot only "Lebanon(?)"',
    '8036': 'latest secure coin 2nd-1st c. BCE (deposit 200-1 BCE per IGCH): cannot be placed after 63 BCE',
    '7618': 'single gold coin', '8013': 'single gold coin', '8043': 'single gold coin',
    '8594': 'single gold coin', '8595': 'single gold coin', '18787': 'single gold coin',
}
LEONARD = set(r['id'] for r in csv.DictReader(open(BASE + '/raw/chre/leonard.csv', encoding='utf-8')))

PREC = {'Silver', 'Base Silver', 'Silver OR Base Silver', 'Gold'}

def plural(dn):
    m = {'Denarius': 'denarii', 'Tetradrachm': 'tetradrachms', 'Drachm': 'drachms', 'Didrachm': 'didrachms',
         'Tridrachm': 'tridrachms', 'Shekel': 'shekels', 'Half shekel': 'half-shekels', 'Aureus': 'aurei',
         'Triobol': 'triobols', 'AR (silver)': 'silver coins (denomination not specified)',
         'AE (brass or copper)': 'bronze coins', 'Prutah': 'prutot', 'Quadrans': 'quadrans', 'As': 'as',
         'Dupondius': 'dupondii', 'Uncertain': 'uncertain coins',
         'Denarius OR Drachm': 'denarii or drachms', 'Denarius OR Tetradrachm': 'denarii or tetradrachms',
         'AE (brass or copper) OR AR (silver)': 'bronze or silver coins'}
    return m.get(dn, dn)

def fmt_year(y):
    try:
        y = int(float(y))
    except Exception:
        return '?'
    return f'{-y} BCE' if y < 0 else f'{y} CE'

rows = []
for i in ids:
    if i in EXCLUDE:
        continue
    r = d[i]
    q = q1.get(i, {})
    groups = r['coin_groups']
    agg = OrderedDict()
    silver = gold = other = 0
    unknown_prec = False
    for g in groups:
        mat = g['material'] or 'material not recorded'
        dn = g['denomination'] or 'denomination not recorded'
        mint = g['mint'] if g['mint'] and g['mint'] != 'Uncertain' else ''
        key = (mat, dn, mint)
        agg[key] = agg.get(key, 0) + (g['qty'] or 0)
        qty = g['qty'] or 0
        if mat == 'Gold':
            gold += qty
        elif mat in PREC or ('Silver' in mat and 'Copper' not in mat and 'Brass' not in mat):
            silver += qty
        else:
            other += qty
    parts = []
    for (mat, dn, mint), n in agg.items():
        lab = plural(dn)
        if mint:
            lab += f' ({mint})'
        if 'Silver' in mat and 'Copper' not in mat:
            mlab = 'AR' if mat == 'Silver' else ('AR, CHRE "base silver"' if mat == 'Base Silver' else 'AR/base AR')
        elif mat == 'Gold':
            mlab = 'AV'
        elif mat in ('Copper alloy', 'Brass', 'Copper'):
            mlab = 'AE'
        else:
            mlab = mat
        parts.append(f'{lab} [{mlab}] {n if n else "number not given"}')
    contents = '; '.join(parts)
    lat = q.get('latitude', '').strip()
    lon = q.get('longitude', '').strip()
    locdet = r.get('Location details', '')
    if lat:
        coord_basis = f'CHRE coordinates ({locdet or "precision not stated"}); approximate'
        lat = f'{float(lat):.4f}'; lon = f'{float(lon):.4f}'
    else:
        coord_basis = f'no coordinates in CHRE; findspot given only as country/region ({q.get("country","")})'
    y1 = r.get('Date of discovery (from)', '') or ''
    y2 = r.get('(to)', '') or ''
    if y1.startswith('Total number') or y1.startswith('(to)'):
        y1 = ''
    if y2.startswith('Total number'):
        y2 = ''
    year = y1 if not y2 or y2 == y1 else (f'{y1} to {y2}' if y1 else f'by {y2}')
    ctx = []
    for k in ('Discovery method', 'Context'):
        if r.get(k):
            ctx.append(f'{k}: {r[k]}')
    if r.get('containers'):
        ctx.append('Container: ' + r['containers'][:220])
    if r.get('Site comment'):
        ctx.append('Site: ' + re.sub(r'\s+', ' ', r['Site comment'])[:400])
    if q.get('discoveryDepth'):
        ctx.append('Depth (CHRE): ' + q['discoveryDepth'])
    context = ' | '.join(ctx) + ' [CHRE wording]'
    t1, t2 = q.get('terminalYear1', ''), q.get('terminalYear2', '')
    try:
        T1 = int(float(t1))
    except Exception:
        T1 = None
    try:
        T2 = int(float(t2))
    except Exception:
        T2 = None
    if T1 is not None and T2 is not None and T2 != T1:
        closing = f'{fmt_year(T1)} to {fmt_year(T2)} (CHRE terminal years)'
    elif T1 is not None:
        closing = f'{fmt_year(T1)} (CHRE terminal year)'
    else:
        closing = 'not given'
    window = 'A' if (T1 is not None and T1 <= 70) else 'B'
    wnote = []
    if T1 is not None and T2 is not None and T1 <= 70 < T2:
        wnote.append('terminal range spans 70 CE; window set by earliest terminal year (latest coin not securely after 70)')
    if T2 is not None and T2 > 136:
        wnote.append('terminal range runs past 136 CE (e.g. Hadrian 117-138); kept because latest coin can date before 136')
    if T1 is not None and T1 < -63:
        wnote.append('terminal range starts before 63 BCE')
    refs = []
    for x in r['refs']:
        det = re.sub(r'\s+', ' ', x['detail']).replace('Reference', '').replace('URI 1', '').replace('URI 2', '')
        det = re.sub(r'(J\. Goldman|Updated by|Uploaded by|M\. Spoerri|R\. Bennett|Corrected, updated).*', '', det).strip()
        pg = re.search(r'Ref (.{1,80}?)(?: Comment|$)', det)
        refs.append(x['title'] + (f' [ref: {pg.group(1).strip()}]' if pg else ''))
    src = (f'CHRE hoard {i}, https://chre.ashmus.ox.ac.uk/hoard/{i} (record and coin CSV read 2026-10-23). '
           f'CHRE cites (not opened by me): ' + ('; '.join(refs) if refs else 'no reference listed'))
    status = 'CHRE data type: ' + ('Hoard' if i not in {'7603', '7698', '8177', '7722', '9149', '9150', '8101'} else
                                   {'7603': 'Group of single finds', '7698': 'Group of single finds', '8177': 'Group of single finds',
                                    '7722': 'Hoard?', '9149': 'Hoard?', '9150': 'Hoard?', '8101': 'Hoard?'}[i])
    rows.append(OrderedDict(
        id=f'chre{i}', name_as_published=r.get('Hoard name', ''), chre_id=i, hoard_status=status,
        lat=lat, lon=lon, coord_basis=coord_basis, year_found=year, context=context,
        closing_date=closing, window=window, window_note='; '.join(wnote),
        contents=contents, total_precious_coins=silver + gold, silver_coins=silver, gold_coins=gold,
        base_metal_or_unrecorded_coins=other, chre_total_coins=r.get('Total number of coins', ''),
        other_precious_objects=r.get('objects', ''), printed_total_weight_g='', printed_weight_source='',
        gold_weight_g='', chre_summary=r.get('Summary', ''), sources=src, confidence='',
        leonard2000_cited_in_chre='yes' if i in LEONARD else 'no'))

json.dump(rows, open(BASE + '/raw/rows_auto.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows))
