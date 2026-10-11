"""Scan all current HGV EpiDoc metadata files (idp.data HGV_meta_EpiDoc) for documents whose
origPlace / provenance placeName lies in Judaea / Judaean Desert / Arabia-Petra / Palaestina.

Usage: python3 -I hgv_epidoc_provenance.py <HGV_meta_EpiDoc dir> <out.csv>
"""
import sys, os, re, csv

root, out = sys.argv[1], sys.argv[2]
PLACE = re.compile(r"murabba|muraba|hever|ḥever|naḥal|nahal|se.?elim|mahoza|maḥoza|maoza|ma'oza|en ?- ?gedi|ein[- ]?gedi|"
                   r"engedi|masada|jericho|jerusalem|hierosolym|aelia|qumran|daliyeh|judaea|judäa|iudaea|palaest|palästina|"
                   r"arabia|petra|zoar|zoora|rabbath|gaza|nessana|askalon|ashkelon|caesarea|aristobulias|mishmar|mird|"
                   r"sepphoris|tiberias|hebron|idum|toten meer|dead sea|qitna|hyrcania|herodium|bostra|phakusai", re.I)
EGYPT_HOMONYM = re.compile(r"arsinoites|mauretan|oxyrhynch|eileithyiopol|wadi sarga|hammamat|karien", re.I)

def g(pat, s):
    m = re.search(pat, s, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''

rows = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith('.xml'):
            continue
        s = open(os.path.join(dp, f), encoding='utf8').read()
        op = g(r'<origPlace[^>]*>(.*?)</origPlace>', s)
        prov = ' ; '.join(re.sub(r'\s+', ' ', x).strip() for x in re.findall(r'<placeName[^>]*>([^<]+)</placeName>', s))
        place = op + ' ; ' + prov
        if not PLACE.search(place):
            continue
        rows.append(dict(
            hgv=f[:-4], tm=g(r'<idno type="TM">([^<]+)<', s), ddb_hybrid=g(r'<idno type="ddb-hybrid">([^<]+)<', s),
            title=g(r'<title>([^<]*)</title>', s), origPlace=op, placenames=prov,
            origDate=g(r'<origDate[^>]*>(.*?)</origDate>', s),
            notBefore=g(r'notBefore="([^"]+)"', s), notAfter=g(r'notAfter="([^"]+)"', s), when=g(r'when="([^"]+)"', s),
            egypt_homonym=bool(EGYPT_HOMONYM.search(place)),
            principal=g(r'subtype="principal">(.*?)</bibl>', s)[:200]))
with open(out, 'w', encoding='utf8', newline='') as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(sorted(rows, key=lambda r: r['hgv']))
print(len(rows), 'records')
