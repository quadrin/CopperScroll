"""Shared geometry: place frame (repo convention), traced-plan -> place transform, Esri z18 mosaic."""
import math, json, pathlib, time, urllib.request
REPO = pathlib.Path('/home/claude/copperscroll')
RUN = pathlib.Path(__file__).resolve().parent.parent
R = 6371008.8
def merc_x(lon): return (180 + lon) / 360
def merc_y(lat): return (180 - (180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))) / 360
def lat_from_merc_y(y): return 360 / math.pi * math.atan(math.exp((180 - y * 360) * math.pi / 180)) - 90
ANCHOR = (31.74183, 35.45941)
class Frame:
    def __init__(self, lat, lon):
        self.ox, self.oy = merc_x(lon), merc_y(lat)
        self.scale = 1 / (2 * math.pi * R) / math.cos(math.radians(lat))
    def xz(self, lat, lon): return ((merc_x(lon) - self.ox) / self.scale, (merc_y(lat) - self.oy) / self.scale)
    def latlon(self, x, z): return lat_from_merc_y(self.oy + z * self.scale), (self.ox + x * self.scale) * 360 - 180
F = Frame(*ANCHOR)
REG = json.loads((REPO / 'research/assets/plans/imagery-registration-2026-10-22/qumran.json').read_text())['figures'][0]
BAR = REG['bar_pxPerM']; FIT = REG['fit']
def traced_to_place(u, v):
    """Traced plan metres (x east, z south, origin L110) -> place frame metres via the repo registration."""
    pu, pv = BAR * u, BAR * v  # plan pixel offsets from L110 centre
    t = math.radians(FIT['turnDegClockwise']); s = FIT['pxPerM']; c, sn = math.cos(t), math.sin(t)
    dx = (c * pu - sn * pv) / s; dz = (sn * pu + c * pv) / s
    return FIT['placePoint'][0] + dx, FIT['placePoint'][1] + dz
import os
Z = int(os.environ.get("ZOOM", "18"))
URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
UA = {'User-Agent': 'research-script/1.0'}
def tile(x, y):
    from PIL import Image
    p = RUN / 'dl' / f"esri{Z}" / f'{Z}_{x}_{y}.jpg'
    if not p.exists():
        req = urllib.request.Request(URL.format(z=Z, x=x, y=y), headers=UA)
        p.write_bytes(urllib.request.urlopen(req, timeout=60).read()); time.sleep(0.5)
    return Image.open(p).convert('RGB')
def dseg(p, a, b):
    ax, ay = a; bx, by = b; px, py = p; dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(ax + t * dx - px, ay + t * dy - py)
def dpoly(p, pts): return min(dseg(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else math.dist(p, pts[0])
