"""Extract every talent/drachma/obol amount from Attic Inscriptions Online translations.

Input: downloads/aio/*.txt (made by aio_to_text.py from AIO pages, translations by Lambert, Osborne et al.).
Only the translation body (between 'Date:' and 'References:') is parsed; footnotes are skipped.
Consecutive unit tokens ("3 tal. 3,237 dr. ½ ob.") form one amount.
Duplicates: the Pronaos stele (IG I3 302) repeats one handover list for nine years; there a weight
already listed is flagged duplicate=True (key = amount string). Other texts are single lists: no dedup.
Output: data/greek_amounts.csv
Run: python3 -I scripts/parse_aio.py
"""
import re, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'downloads', 'aio')
OUT = os.path.join(HERE, '..', 'data', 'greek_amounts.csv')

CORPUS = {  # file stem -> (corpus, citation, AIO URL path)
 'IGI3_302': ('G_inventory', 'IG I3 302 = AIUK 4.4 no. 3, Inventory of the Pronaos 426/5-423/2, 414/3-411/0 BC', 'IGI3/302'),
 'ML_76': ('G_inventory', 'IG I3 329, Inventory of the Hekatompedon 418/7 BC', 'ML/76'),
 'AleshireAsklepieion_3': ('G_inventory', 'Aleshire, Asklepieion 3, Inventory of the Asklepieion 329/8 BC', 'AleshireAsklepieion/3'),
 'AleshireAsklepieion_6': ('G_inventory', 'Aleshire, Asklepieion 6, Inventory of the Asklepieion ca. 229/8-210/9 BC', 'AleshireAsklepieion/6'),
 'IGII31_1010': ('G_inventory', 'IG II3 1 1010, dedications in the sanctuary of Asklepios 248/7 BC', 'IGII31/1010'),
 'IGII31_898': ('G_inventory', 'IG II3 1 898, dedications in the sanctuary of Asklepios 274/3 BC', 'IGII31/898'),
 'Meyer2010_1': ('G_inventory', 'Meyer, Metics no. 1, manumissions and dedicatory bowls', 'Meyer2010/1'),
 'IGI3_369': ('G_accounts', 'IG I3 369, loans from the sacred treasuries 426/5-423/2 BC', 'IGI3/369'),
 'IGI3_375': ('G_accounts', 'IG I3 375, payments from the treasury of Athena 410/9 BC', 'IGI3/375'),
 'OR_170': ('G_accounts', 'OR 170, payments from the treasury of Athena 418/7-415/4 BC', 'OR/170'),
 'IGI3_259': ('G_tribute', 'IG I3 259, Athenian tribute list 454/3 BC', 'IGI3/259'),
 'IGI3_278': ('G_tribute', 'IG I3 278, Athenian tribute list 434/3 BC', 'IGI3/278'),
 'OR_119b': ('G_tribute', 'OR 119B, Athenian tribute list 442/1 BC', 'OR/119b'),
}
DEDUP_BY_AMOUNT = {'IGI3_302'}   # the Pronaos stele repeats the same list for nine years
FR = {'½': .5, '¼': .25, '¾': .75}
UNIT = r'(talents?|tal\.|drachmas?|drachmai|dr\.|obols?|ob\.)'
TOK = re.compile(r'(\(≥\)\s*)?(\[?\d[\d,]*\]?)?\s*([½¼¾])?\s*' + UNIT)

def unit_of(u):
    return 'tal' if u.startswith('tal') else 'dr' if u.startswith('dr') else 'ob'

def parse(text):
    out = []
    pos = 0; cur = None
    for m in TOK.finditer(text):
        num, frac, u = m.group(2), m.group(3), unit_of(m.group(4))
        if not num and not frac:
            continue
        val = float(num.strip('[]').replace(',', '')) if num else 0.0
        if frac: val += FR[frac]
        gap = text[pos:m.start()] if cur else ''
        if cur and re.fullmatch(r'[\s\[\]]*', gap) and u not in cur['units']:
            cur['units'][u] = val; cur['end'] = m.end(); cur['partial'] |= bool(m.group(1))
            cur['restored'] |= ('[' in (num or '') or '[' in gap)
        else:
            if cur: out.append(cur)
            cur = dict(start=m.start(), end=m.end(), units={u: val}, partial=bool(m.group(1)),
                       restored='[' in (num or ''))
        pos = m.end()
    if cur: out.append(cur)
    return out

rows = []
for stem, (corpus, cite, path) in CORPUS.items():
    p = os.path.join(D, stem + '.txt')
    if not os.path.exists(p):
        print('missing', p); continue
    t = open(p, encoding='utf-8').read()
    body = t[t.find('Date:'):t.find('References:')]
    body = re.sub(r'\[\d+\]', '', body)            # footnote markers
    body = re.sub(r'\(\d+\)\s*', '', body)          # line numbers like (5)
    seen = set()
    for a in parse(body):
        s = body[a['start']:a['end']]
        ctx = re.sub(r'[\[\]\s]+', ' ', body[max(0, a['start'] - 60):a['start']]).strip()[-40:]
        key = re.sub(r'[\[\]\s]+', ' ', s).strip()
        # handover inventories re-list the same holdings every year: keep the first listing of each weight
        dup = (stem in DEDUP_BY_AMOUNT) and key in seen; seen.add(key)
        u = a['units']
        lead_unit = 'tal' if 'tal' in u else 'dr' if 'dr' in u else 'ob'
        lead = u[lead_unit]
        rows.append(dict(corpus=corpus, source=cite, url='https://www.atticinscriptions.com/inscription/' + path,
            amount=re.sub(r'\s+', ' ', s).strip(), context=ctx, tal=u.get('tal', ''), dr=u.get('dr', ''), ob=u.get('ob', ''),
            lead_unit=lead_unit, lead_value=lead, has_subunit=len(u) > 1 or (lead != int(lead)),
            value_dr=u.get('tal', 0) * 6000 + u.get('dr', 0) + u.get('ob', 0) / 6,
            partial=a['partial'], restored=a['restored'], duplicate=dup))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
from collections import Counter
c = Counter((r['corpus'], r['duplicate']) for r in rows)
print(len(rows), 'amounts;', dict(c))
