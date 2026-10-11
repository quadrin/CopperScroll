"""Scan the HGV FileMaker XML dump (idp.data HGV_metadata/XML_dump/HGV.xml) for records whose
provenance (field 'Ort') lies in the Judaean Desert / Judaea / Arabia-Petra region.

Usage: python3 -I hgv_provenance.py <HGV.xml> <out.csv>
Output: one row per matching HGV record with publication, place, dates, TM number and DDbDP id.
"""
import sys, csv, re
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]
NS = '{http://www.filemaker.com/fmpxmlresult}'
KEEP = ['Publikation', 'Band', 'Nummer', 'zusätzlich', 'Ort', 'Datierung', 'ChronMinimum', 'ChronMaximum',
        'TM_Nr.', 'ddbFull', 'ddbSerIDP', 'Material', 'InhaltUnicode', 'Originaltitel']
# place patterns (case-insensitive) for core + extended window regions
PLACE = re.compile(r"murabba|muraba|hever|ḥever|hever|naḥal|nahal|se'?elim|seelim|ṣe|mahoza|maḥoza|ma'oza|en[- ]?gedi|ein[- ]?gedi|"
                   r"engedi|masada|jericho|jerusalem|hierosolym|aelia|qumran|daliyeh|judaea|judäa|iudaea|palaest|palästina|"
                   r"arabia|petra|zoar|zoora|rabbath|ma'oz|gaza|nessana|nessa|askalon|ashkelon|caesarea|samaria|galil|"
                   r"sepphoris|tiberias|hebron|idum|toten meer|dead sea|wadi", re.I)

fields = []
rows = []
for ev, el in ET.iterparse(src, events=('end',)):
    tag = el.tag.replace(NS, '')
    if tag == 'FIELD':
        fields.append(el.get('NAME'))
    elif tag == 'ROW':
        cols = el.findall(NS + 'COL')
        vals = []
        for c in cols:
            ds = c.findall(NS + 'DATA')
            vals.append(' | '.join((d.text or '') for d in ds))
        rec = dict(zip(fields, vals))
        if PLACE.search(rec.get('Ort', '') or ''):
            rows.append({k: rec.get(k, '') for k in KEEP})
        el.clear()
with open(out, 'w', encoding='utf8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=KEEP)
    w.writeheader()
    w.writerows(rows)
print(len(fields), 'fields;', len(rows), 'matching records')
