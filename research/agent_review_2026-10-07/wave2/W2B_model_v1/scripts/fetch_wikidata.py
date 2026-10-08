#!/usr/bin/env python3
"""Fetch Wikidata search hits + P625 coordinates for candidate place names.
Usage: python3 -I fetch_wikidata.py OUTDIR term1 term2 ...
Raw JSON responses are saved under OUTDIR (untrusted data); a summary TSV is printed."""
import json, os, sys, urllib.parse, urllib.request, urllib.error, time

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
UA = {'User-Agent': 'copper-scroll-research-agent/0.1 (desk study; no contact)'}


def get(url, tries=6):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and k < tries - 1:
                time.sleep(5 * (k + 1))
                continue
            raise


for term in sys.argv[2:]:
    q = urllib.parse.urlencode(dict(action='wbsearchentities', search=term, language='en', format='json', limit=6))
    res = get('https://www.wikidata.org/w/api.php?' + q)
    ids = [h['id'] for h in res.get('search', [])]
    if not ids:
        print(f'{term}\tNO HITS')
        continue
    q2 = urllib.parse.urlencode(dict(action='wbgetentities', ids='|'.join(ids), props='labels|descriptions|claims|sitelinks',
                                     languages='en|he|ar', format='json'))
    ent = get('https://www.wikidata.org/w/api.php?' + q2)
    fn = os.path.join(out, 'wd_' + ''.join(c if c.isalnum() else '_' for c in term) + '.json')
    json.dump(ent, open(fn, 'w'), ensure_ascii=False)
    for i in ids:
        e = ent['entities'][i]
        lab = e.get('labels', {}).get('en', {}).get('value', '')
        desc = e.get('descriptions', {}).get('en', {}).get('value', '')
        c = e.get('claims', {}).get('P625', [])
        coords = []
        for cl in c:
            try:
                v = cl['mainsnak']['datavalue']['value']
                coords.append(f"{v['latitude']:.5f},{v['longitude']:.5f} (prec {v.get('precision')})")
            except Exception:
                pass
        enwiki = e.get('sitelinks', {}).get('enwiki', {}).get('title', '')
        print(f'{term}\t{i}\t{lab}\t{desc}\t{"; ".join(coords)}\tenwiki={enwiki}')
    time.sleep(3)
