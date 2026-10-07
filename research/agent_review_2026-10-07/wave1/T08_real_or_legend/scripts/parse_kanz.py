"""Kitab al-Durr al-Maknuz (Book of Buried Pearls), French translation by Ahmed Bey Kamal (Cairo 1907),
archive.org item livredesperlesen00amad (OCR text). Treasure-hunting manual: one paragraph (§) per hiding place.

Segments the French translation (OCR lines 373-9930, before INDEX I) at paragraph headings ("§ N. —").
OCR damages many headings, so a 'clean' unit is a segment whose heading number n is followed by a
heading numbered n+1 (single paragraph). Codes per paragraph, by regex (validated by hand on a sample,
see REPORT): dig instruction, stated depth and its unit, distances, direction words, container,
explicit numbered treasure, vague treasure, magic/ritual element. Extracts the numbers.
Outputs: data/kanz_paragraphs.csv, data/kanz_amounts.csv
Run: python3 -I scripts/parse_kanz.py downloads/livredesperlesen00amad_djvu.txt
"""
import re, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '..', 'data')
src = sys.argv[1]
L = open(src, encoding='utf-8').read().split('\n')
L = L[372:9930]
text = '\n'.join(L)

U = {'un':1,'une':1,'deux':2,'trois':3,'quatre':4,'cinq':5,'six':6,'sept':7,'huit':8,'neuf':9,'dix':10,'onze':11,
     'douze':12,'treize':13,'quatorze':14,'quinze':15,'seize':16,'vingt':20,'vingts':20,'trente':30,'quarante':40,
     'cinquante':50,'soixante':60}
NUMW = r"(?:\d[\d.]*|(?:(?:un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingts?|trente|quarante|cinquante|soixante|cents?|mille|et)(?:[\s-]+|$))+)"

def fr2num(s):
    s = s.strip().lower()
    if re.fullmatch(r'\d[\d.]*', s): return float(s.replace('.', ''))
    toks = [t for t in re.split(r'[\s-]+', s) if t and t != 'et']
    total = 0; cur = 0
    for i, t in enumerate(toks):
        if t in U:
            v = U[t]
            if t.startswith('vingt') and cur in (4,):  # quatre-vingt(s)
                cur = 80; continue
            if v == 10 and cur in (60, 80): cur += 10; continue      # soixante-dix
            if 11 <= v <= 16 and cur in (60, 80): cur += v; continue  # soixante-douze
            cur += v
        elif t.startswith('cent'):
            cur = (cur or 1) * 100
        elif t == 'mille':
            total += (cur or 1) * 1000; cur = 0
    return float(total + cur) if (total + cur) else None

# --- segmentation
H = re.compile(r'^\s*(?:§|S|\$|5|g)\s*([0-9]{1,3}|1er)\s*\.?\s*[—\-–]+\s*(.*)$')
heads = []
for i, l in enumerate(L):
    m = H.match(l)
    if m:
        n = 1 if m.group(1) == '1er' else int(m.group(1))
        heads.append((i, n, m.group(2).strip()))
paras = []
for k, (i, n, title) in enumerate(heads):
    j = heads[k + 1][0] if k + 1 < len(heads) else len(L)
    nxt = heads[k + 1][1] if k + 1 < len(heads) else None
    body = ' '.join(L[i + 1:j])
    body = re.sub(r'\s+', ' ', body)
    paras.append(dict(n=n, title=title, clean=(nxt == n + 1), body=body))

TREAS = r"(dinars?|mithqals?|qantars?|quintaux|quilitals?|lingots?|ardebs?|drachmes?|dirhams?|jarres?|bassins?|caisses?|coffres?|marmites?|urnes?|cruches?|vases?|pièces? d'or|pièces? de monnaie)"
DEPTHU = r"(coudées?|qamahs?|tailles? d'homme|bastas?|empans?|mètres?)"
rows = []; amts = []
for p in paras:
    b = p['body']; bl = b.lower()
    f = dict(n=p['n'], title=p['title'][:40], clean=p['clean'], n_chars=len(b))
    f['dig'] = bool(re.search(r'creus|fouill', bl))
    dm = re.findall(r'(?:profondeur|creusez|creuse|descendez)[^.;]{0,60}?\b(' + NUMW + r')\s*' + DEPTHU, bl)
    dm2 = re.findall(r'\b(une|d\'une|deux|trois|quatre|cinq|six|sept|\d+)\s+(?:bonne\s+|demi-)?(taille d\'homme|qamah)', bl)
    f['depth_stated'] = bool(dm) or bool(re.search(r'profondeur', bl)) or bool(dm2)
    f['depth_cubit'] = any(u.startswith('coud') for _, u in dm)
    f['depth_body_unit'] = any(u.startswith(('qamah', 'taille', 'basta', 'empan')) for _, u in dm) or bool(dm2)
    for num, u in dm:
        v = fr2num(num)
        if v: amts.append(dict(n=p['n'], clean=p['clean'], kind='depth', value=v, unit=u, text=f'{num.strip()} {u}'))
    # distances: paces, miles (plural 'milles', or 'un/demi mille'); 'mille' alone is usually 'thousand'
    dist = re.findall(r'\b(' + NUMW + r')\s*(pas|milles)\b', bl) + [('un', 'mille') for _ in re.findall(r"\b(?:à|d')\s*(?:un|une)\s+(?:demi-)?mille\b", bl)]
    f['distance_stated'] = bool(dist) or bool(re.search(r'\bà\s+(' + NUMW + r')\s*coudées? (?:de|du|à l)', bl))
    for num, u in dist:
        if True:
            v = fr2num(num)
            if v: amts.append(dict(n=p['n'], clean=p['clean'], kind='distance', value=v, unit=u, text=f'{num.strip()} {u}'))
    f['direction'] = bool(re.search(r"\b(nord|sud|est|ouest|orient|occident|qiblah|méridional|septentrional|oriental|occidental|droite|gauche)\b", bl))
    f['container'] = bool(re.search(r"\b(jarres?|bassins?|marmites?|caisses?|coffres?|urnes?|vases?|cruches?|sacs?|naos|coffrets?)\b", bl))
    tq = re.findall(r'\b(' + NUMW + r')\s*(?:\w+\s+)?' + TREAS, bl)
    tq = [(n_, u) for n_, u in tq if fr2num(n_)]
    f['treasure_numbered'] = bool(tq)
    for num, u in tq:
        amts.append(dict(n=p['n'], clean=p['clean'], kind='treasure', value=fr2num(num), unit=u, text=f'{num.strip()} {u}'))
    f['treasure_vague'] = bool(re.search(r"beaucoup d|autant qu|ce qu'il vous faut|ce qu’il vous faut|richesses|incalculable|innombrable|quantité|trésors?\b|plein[es]* d", bl))
    f['magic'] = bool(re.search(r"fumig|encens|formule|incantation|talisman|magique|génie|esprit|conjur|sortil|gardien", bl))
    rows.append(f)

os.makedirs(OUTD, exist_ok=True)
with open(os.path.join(OUTD, 'kanz_paragraphs.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUTD, 'kanz_amounts.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(amts[0].keys())); w.writeheader(); w.writerows(amts)
clean = [r for r in rows if r['clean']]
print(len(rows), 'segments;', len(clean), 'clean single paragraphs')
for k in ['dig','depth_stated','depth_cubit','depth_body_unit','distance_stated','direction','container','treasure_numbered','treasure_vague','magic']:
    print(f"{k:18s} all={sum(r[k] for r in rows)/len(rows):.2f}  clean={sum(r[k] for r in clean)/len(clean):.2f}")
print(len(amts), 'numbers extracted')
