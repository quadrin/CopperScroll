"""Build a flat JSON of all IIP inscriptions from downloaded __data.json pages."""
import sys, json, glob, os
sys.path.insert(0, os.path.dirname(__file__))
import devalue
src, out = sys.argv[1], sys.argv[2]
allins = {}
meta = []
for f in sorted(glob.glob(os.path.join(src, 'p*.json'))):
    r = devalue.load(f)
    d = r[-1]
    meta.append((os.path.basename(f), d.get('page'), d.get('pages'), d.get('total'), len(d['inscriptions'])))
    for i in d['inscriptions']:
        allins[i['filename']] = i
print(meta[0], meta[-1], 'unique', len(allins))
json.dump(list(allins.values()), open(out, 'w', encoding='utf8'), ensure_ascii=False)
