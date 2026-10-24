import re, html, csv, json, sys, os, glob
from collections import defaultdict, OrderedDict
D = sys.argv[1]
out = {}
def clean(s):
    s = re.sub(r'<[^>]+>', '\n', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    return s.strip()
FIELDS = ['Hoard name','Alternative names','Date of discovery (from)','(to)','Total number of coins','Summary',
          'Discovery method','Disposition','Comment','Terminal year (earliest)','Terminal year (latest)',
          'Closing reign (earliest)','Closing reign (latest)','Numismatic rating','Rating comment','Context rating',
          'Findspot rating','Site comment','Recovery method','Site class','Context','Discovery depth','Depth',
          'Finder','Discovery comment','Location details','Lat/Long/Alt','City','Region','Country']
for fn in sorted(glob.glob(os.path.join(D, '*.html'))):
    hid = os.path.basename(fn)[:-5]
    t = open(fn, encoding='utf-8', errors='replace').read()
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    rec = OrderedDict(id=hid)
    # references
    refs = []
    for m in re.finditer(r'<a href="/reference/(\d+)"[^>]*>(.*?)</a>(.*?)(?=<a href="/reference/|Twitter|$)', t, re.S):
        title = clean(m.group(2))
        tail = clean(m.group(3))
        tail = re.split(r'\n(?:Reference|Reports|Images|Credit)\n', '\n'+tail+'\n')[0] if False else tail
        refs.append({'ref_id': m.group(1), 'title': title, 'detail': tail[:600]})
    txt = clean(t)
    lines = txt.split('\n')
    for i, l in enumerate(lines):
        l = l.strip()
        if l in FIELDS and i+1 < len(lines) and l not in rec:
            rec[l] = lines[i+1].strip()
    # containers
    m = re.search(r'Containers belonging to this hoard(.*?)(?:Objects belonging|References\n)', txt, re.S)
    rec['containers'] = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    m = re.search(r'Objects belonging to this hoard(.*?)References\n', txt, re.S)
    rec['objects'] = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    # free-text reference strings block (before Context rating)
    m = re.search(r'Rating comment\n.*?\n(.*?)\nContext rating', txt, re.S)
    rec['reference_strings'] = re.sub(r'\n', ' || ', m.group(1)).strip() if m else ''
    rec['refs'] = refs
    # coins csv
    cfn = os.path.join(D, hid + '_coins.csv')
    agg = defaultdict(lambda: [0, 0])
    groups = []
    if os.path.exists(cfn):
        try:
            for r in csv.DictReader(open(cfn, encoding='utf-8')):
                q = r.get('quantity') or ''
                try: qn = int(float(q))
                except: qn = None
                key = (r.get('material',''), r.get('denomination',''), r.get('mint',''), r.get('person','') or r.get('reign',''))
                groups.append({'material': r.get('material',''), 'denomination': r.get('denomination',''), 'mint': r.get('mint',''),
                               'person': r.get('person',''), 'reign': r.get('reign',''), 'start': r.get('startingDate',''), 'end': r.get('endingDate',''),
                               'qty': qn, 'weight': r.get('weight',''), 'latest': r.get('latestCoin','')})
        except Exception as e:
            groups = [{'error': str(e)}]
    rec['coin_groups'] = groups
    out[hid] = rec
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(out))
