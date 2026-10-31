"""Fetch Mishnah and Tosefta (Hebrew) from the Sefaria v3 API. Records version title and licence.
Usage: python3 -I fetch_sefaria.py INDEX_JSON OUTDIR"""
import json, sys, time, urllib.request, urllib.parse, os, hashlib
idx = json.load(open(sys.argv[1])); out = sys.argv[2]
titles = []
def walk(n, path):
    if 'contents' in n:
        for c in n['contents']: walk(c, path + [n.get('category', '')])
    elif 'title' in n: titles.append((path[1:], n['title']))
for n in idx: walk(n, [''])
mish = [t for p, t in titles if p[:1] == ['Mishnah'] and t.startswith('Mishnah ')]
tos = [t for p, t in titles if p[:2] == ['Tosefta', 'Vilna Edition']]
UA = {'User-Agent': 'Mozilla/5.0 (research script)'}
OK_LIC = {'public domain', 'pd', 'cc0', 'cc-by', 'cc-by-sa', 'cc-by 3.0', 'cc-by-sa 3.0', 'cc-by-sa 4.0', 'cc-by 4.0'}
KAUF = "Mishnah based on the Kaufmann manuscript, edited by Dan Be'eri"
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            err = e; time.sleep(3)
    raise err
manifest = []
for t in mish + tos:
    fn = os.path.join(out, t.replace(' ', '_').replace("'", '') + '.json')
    base = 'https://www.sefaria.org/api/v3/texts/' + urllib.parse.quote(t)
    urls = ([base + '?version=' + urllib.parse.quote('hebrew|' + KAUF)] if t.startswith('Mishnah') else []) + [base + '?version=hebrew']
    rec = {'title': t, 'status': 'not fetched'}
    for u in urls:
        try:
            d = get(u)
        except Exception as e:
            rec = {'title': t, 'url': u, 'status': 'error', 'error': repr(e)}; continue
        vs = [v for v in d.get('versions', []) if v.get('language') == 'he' and v.get('text')]
        if not vs:
            rec = {'title': t, 'url': u, 'status': 'no hebrew version', 'error': d.get('error')}; continue
        v = vs[0]
        lic = (v.get('license') or '').strip()
        rec = {'title': t, 'url': u, 'versionTitle': v.get('versionTitle'), 'license': lic, 'versionSource': v.get('versionSource')}
        if lic.lower() not in OK_LIC:
            rec['status'] = 'licence not open: skipped'; continue
        raw = json.dumps({'title': t, 'versionTitle': v.get('versionTitle'), 'license': lic, 'text': v['text']}, ensure_ascii=False)
        open(fn, 'w', encoding='utf-8').write(raw)
        rec['status'] = 'ok'; rec['sha256'] = hashlib.sha256(raw.encode('utf-8')).hexdigest(); rec['file'] = os.path.basename(fn)
        break
    manifest.append(rec); print(rec['title'], rec['status'], rec.get('versionTitle'), rec.get('license'), flush=True)
    time.sleep(0.4)
json.dump(manifest, open(os.path.join(out, '..', 'sefaria_manifest.json'), 'w'), ensure_ascii=False, indent=1)
