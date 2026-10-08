import math, sys, os, subprocess
from PIL import Image
# usage: fetch_s2.py outdir layer z lat_min lat_max lon_min lon_max
outdir, layer, z = sys.argv[1], sys.argv[2], int(sys.argv[3])
la0, la1, lo0, lo1 = map(float, sys.argv[4:8])
def tile(lat, lon):
    n = 2**z; x = (lon+180)/360*n; y = (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n
    return x, y
x0, y1 = tile(la0, lo0); x1, y0 = tile(la1, lo1)
xs = range(int(x0), int(x1)+1); ys = range(int(y0), int(y1)+1)
os.makedirs(os.path.join(outdir, 'tiles'), exist_ok=True)
W = Image.new('RGB', (256*len(xs), 256*len(ys)))
for j, y in enumerate(ys):
    for i, x in enumerate(xs):
        p = os.path.join(outdir, 'tiles', f'{layer}_{z}_{y}_{x}.jpg')
        if not os.path.exists(p):
            subprocess.run(['curl', '-sS', '-m', '30', '-o', p, f'https://tiles.maps.eox.at/wmts/1.0.0/{layer}/default/g/{z}/{y}/{x}.jpg'], check=True)
        W.paste(Image.open(p).convert('RGB'), (256*i, 256*j))
out = os.path.join(outdir, f'{layer}_z{z}_mosaic.png'); W.save(out)
# record georeference: top-left tile corner lon/lat and bottom-right
def tile2ll(x, y):
    n = 2**z; lon = x/n*360-180; lat = math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))); return lat, lon
tl = tile2ll(xs[0], ys[0]); br = tile2ll(xs[-1]+1, ys[-1]+1)
open(out+'.geo.txt', 'w').write(f'EPSG:3857 tiles z={z} x={xs[0]}..{xs[-1]} y={ys[0]}..{ys[-1]}\nTL lat,lon={tl}\nBR lat,lon={br}\nsize={W.size}\n')
print(out, W.size, tl, br)
