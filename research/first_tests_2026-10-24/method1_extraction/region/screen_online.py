"""Apply the frozen HA-ESI screen (search_plan.json: S1 title names, S2 Hebrew prefixes, S3 map references)
to the owner-supplied online reports, vols 116-137 (2004-2025). Reads the repo scripts; writes only here."""
import csv, json, sys, re
from pathlib import Path
SC = Path('/home/claude/quadrin/copperscroll/research/regional/haesi_features/scripts')
sys.path.insert(0, str(SC))
import screen_toc as st, screen_coords as sco, geo
st.S2 = True
T = Path('/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/hadtext_data/hadtext')
OUT = Path(__file__).resolve().parent
plan = json.loads(st.PLAN.read_text(encoding='utf-8'))
groups, jd_any, jd_with, jd_terms, qelt = st.load_patterns(plan)
places = geo.load_places(); bx = sco.boxes()
meta = list(csv.DictReader(open(T / 'reports_metadata.csv', encoding='utf-8')))

def title_screen(t):
    nt = st.norm(t); matched = {}
    for gid, pats in groups.items():
        h = st.hits(nt, pats)
        if h: matched[gid] = h
    h = st.hits(nt, jd_any)
    if h: matched['R_JD_CLIFFS'] = h
    h = st.hits(nt, jd_with)
    if h and st.hits(nt, jd_terms): matched.setdefault('R_JD_CLIFFS', []).extend(h)
    h = st.hits(nt, qelt)
    if h: matched['R_WADI_QELT'] = h
    return matched

rows = []
for m in meta:
    rec = dict(id=m['id'], volume=m['volume'], date=m['date'], title_en=m['title_en'], title_he=m['title_he'], type_en=m['type_en'], en_pdf=m['en_pdf'], he_pdf=m['he_pdf'])
    s1 = {}
    for t in (m['title_en'] + ' , ' + m['group_en'], m['title_he'] + ' , ' + m['group_he']):
        for k, v in title_screen(t).items(): s1.setdefault(k, set()).update(v)
    rec['title_groups'] = ';'.join(sorted(s1)); rec['title_terms'] = ';'.join(sorted({x for v in s1.values() for x in v}))
    refs = []
    for lang, col in (('en', 'en_pdf'), ('he', 'he_pdf')):
        if not m[col]: continue
        p = T / lang / Path(m[col]).parent.name / (Path(m[col]).stem + '.txt')
        if not p.exists(): continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if lang == 'en': rec['en_words'] = len(text.split())
        for mm in sco.REF.finditer(text):
            lab = (mm.group(1) or '').upper()
            lab = 'NIG' if lab.startswith('NEW') or lab == 'NIG' else ('OIG' if lab.startswith('OLD') or lab == 'OIG' else '')
            try: r = geo.parse_ref(mm.group(2), lab)
            except ValueError: continue
            lat, lon = geo.to_wgs84(r['e'], r['n'], r['grid'])
            if not (29.4 < lat < 33.5 and 34.1 < lon < 36.0): continue
            d = geo.distances(lat, lon, places)
            refs.append((d[0][0], d[0][1], lat, lon, mm.group(2), r['grid'], sco.in_boxes(lat, lon, bx), [p for k, p in d if k <= 2.0], [p for k, p in d if k <= 5.0]))
        if refs and lang == 'en': break  # English refs found; Hebrew is the fallback
    rec['n_refs'] = len(refs)
    if refs:
        best = min(refs)
        rec.update(nearest=best[1], km=best[0], lat=round(best[2], 5), lon=round(best[3], 5), ref=best[4], grid=best[5])
        rec['within_2km'] = ';'.join(sorted({p for r in refs for p in r[7]}))
        rec['within_5km'] = ';'.join(sorted({p for r in refs for p in r[8]}))
        rec['regions'] = ';'.join(sorted({b for r in refs for b in r[6]}))
    s3 = bool(rec.get('within_5km') or rec.get('regions'))
    rec['screen'] = ';'.join(x for x, y in (('S1/S2 title', bool(s1)), ('S3 map ref', s3)) if y)
    rows.append(rec)
fields = ['id','volume','date','title_en','title_he','type_en','en_words','screen','title_groups','title_terms','n_refs','nearest','km','lat','lon','ref','grid','within_2km','within_5km','regions','en_pdf','he_pdf']
with open(OUT / 'online_screen_all.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n'); w.writeheader(); w.writerows(rows)
cand = [r for r in rows if r['screen']]
with open(OUT / 'online_candidates.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n'); w.writeheader(); w.writerows(cand)
from collections import Counter
print('reports', len(rows), 'with a map ref', sum(1 for r in rows if r['n_refs']), 'candidates', len(cand))
print(Counter(r['screen'] for r in cand))
print('within 2 km of a place', sum(1 for r in cand if r.get('within_2km')), '| 2-5 km only', sum(1 for r in cand if r.get('within_5km') and not r.get('within_2km')), '| region only', sum(1 for r in cand if r.get('regions') and not r.get('within_5km')), '| title only, no located ref', sum(1 for r in cand if r['screen']=='S1/S2 title'))
