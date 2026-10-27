"""Harvest Palestine Open Maps 1940s vector overlay (Tegola, ODbL) at z14 over the scroll region. Polite: 0.25 s between requests."""
import sys, os, time, urllib.request, ssl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tileutil import deg2num
OUT = sys.argv[1]; Z = 14
x0, y0 = deg2num(32.55, 35.0, Z); x1, y1 = deg2num(31.40, 35.6, Z)
ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt')
n = 0
for x in range(int(x0), int(x1) + 1):
    for y in range(int(y0), int(y1) + 1):
        fn = f'{OUT}/{Z}_{x}_{y}.pbf'
        if os.path.exists(fn): continue
        for attempt in range(3):
            try:
                req = urllib.request.Request(f'https://tiler.palopenmaps.org/maps/osm/{Z}/{x}/{y}.pbf', headers={'User-Agent': 'research-script/1.0'})
                b = urllib.request.urlopen(req, timeout=60, context=ctx).read()
                open(fn, 'wb').write(b); break
            except Exception as e:
                print('ERR', x, y, e, flush=True); time.sleep(3)
        n += 1; time.sleep(0.25)
        if n % 100 == 0: print(n, flush=True)
print('done', n)
