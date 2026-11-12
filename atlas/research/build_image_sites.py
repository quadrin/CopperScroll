"""Build app/atlas-image-sites.json from the site table of the satellite image work.

    python3 -I atlas/research/build_image_sites.py [--check]

Source: research/sources/hexagon_registration_2026-11-11/sites.csv (positions read on registered HEXAGON 1974/1978
and CORONA 1967 images). The layer is a separate overlay: it changes no entry, candidate, rating or site pin.
"""
import csv, json, sys
from pathlib import Path

root = Path(__file__).resolve().parent
src = root.parents[1] / 'research/sources/hexagon_registration_2026-11-11/sites.csv'
out = root.parent / 'app/atlas-image-sites.json'
features = []
for i, r in enumerate(csv.DictReader(src.open(encoding='utf-8', newline=''))):
    status = r['status']
    group = 'checked' if status.startswith('Checked') else 'seen' if status.startswith('Seen') else 'probable' if status.startswith(('Probable', 'Possible')) else 'open'
    features.append({'type': 'Feature', 'id': i + 1, 'geometry': {'type': 'Point', 'coordinates': [float(r['lon']), float(r['lat'])]},
                     'properties': {'name': r['name'], 'status': status, 'group': group, 'kind': r['type'], 'errorM': int(float(r['error_m'])) if r['error_m'] else None,
                                    'source': r['position_source'], 'image': r['image'], 'note': r['note'], 'altNames': r['alt_names']}})
text = json.dumps({'type': 'FeatureCollection', 'source': 'research/sources/hexagon_registration_2026-11-11/sites.csv', 'features': features}, ensure_ascii=False, indent=1) + '\n'
if '--check' in sys.argv:
    if out.read_text(encoding='utf-8') != text:
        raise SystemExit('app/atlas-image-sites.json does not match a fresh build')
    print('app/atlas-image-sites.json matches a fresh build')
else:
    out.write_text(text, encoding='utf-8')
    groups = {}
    for f in features: groups[f['properties']['group']] = groups.get(f['properties']['group'], 0) + 1
    print(f'Built {len(features)} image-checked places: {groups}')
