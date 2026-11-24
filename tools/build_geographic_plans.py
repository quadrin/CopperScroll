"""Regenerate the atlas plan overlays with Pillow and pyproj from the reviewed source records."""
import cmath
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw
from pyproj.transformer import TransformerGroup

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'research/assets/plans/imagery-registration-2026-10-22'
PUBLIC = ROOT / 'atlas/public/geographic-plans'
DATA = ROOT / 'atlas/app/atlas-geographic-plans.json'
REPO = 'https://github.com/quadrin/CopperScroll/blob/main/'
LOG = REPO + 'research/sources/hexagon_registration_2026-11-11/edit_log_location_grades_and_image_statuses.md'
plans = []
features = []


def read(path):
    return json.loads(path.read_text())


def project(crs, operation):
    transforms = TransformerGroup(crs, 4326, always_xy=True).transformers
    return next(t for t in transforms if operation in t.description).transform


pg = project(28191, 'Palestine 1923 to WGS 84 (1)')
itm = project(2039, 'Israel 1993 to WGS 84 (2)')


def lonlat(anchor, east, south):
    """Inverse of the model's MapLibre Mercator place frame in tools/build_osm_context.py."""
    lat, lon = anchor
    radius = 6371008.8 * math.cos(math.radians(lat))
    merc = math.asinh(math.tan(math.radians(lat))) - south / radius
    return [lon + math.degrees(east / radius), math.degrees(math.atan(math.sinh(merc)))]


def corners(box):
    x0, y0, x1, y1 = box
    return [(x0,y0), (x1,y0), (x1,y1), (x0,y1)]


def round_xy(point):
    return [round(x, 8) for x in point]


def add_plan(id, site, title, detail, credit, source, image, points):
    plans.append(dict(id=id, siteIds=[site], title=title, detail=detail, credit=credit,
                      sourceUrl=source, image='geographic-plans/' + image,
                      corners=[round_xy(p) for p in points]))


def source_url(site):
    return REPO + f'research/assets/plans/imagery-registration-2026-10-22/{site}.json'


def fit(record, xy):
    offset = complex(*xy) - complex(*record['planPoint'])
    rotation = cmath.rect(1 / record['pxPerM'], math.radians(record['turnDegClockwise']))
    return complex(*record['placePoint']) + offset * rotation


def scan(record, fid, title, credit, detail, filename, crop, transform=None, source=None):
    im = Image.open(ROOT / filename)
    box = crop or (0, 0, *im.size)
    assert 0 <= box[0] < box[2] <= im.width and 0 <= box[1] < box[3] <= im.height
    im.crop(box).convert('RGB').save(PUBLIC / (fid + '.webp'), quality=89, method=6)
    to_place = transform or (lambda xy: fit(record['figures'][0]['fit'], xy))
    points = []
    for xy in corners(box):
        xz = to_place(xy)
        points.append(lonlat(record['anchor'], xz.real, xz.imag))
    add_plan(fid, record['place'], title, detail, credit, source or source_url(record['title'].split()[-1]), fid+'.webp', points)


def plan_scans():
    jer = read(REG / 'jericho.json')
    src = ROOT / 'research/assets/plans/trumper2018'
    notice = 'Monika Trümper 2018, after Ehud Netzer. CC BY-NC 3.0. Cropped from the published figure.'
    scan(jer, 'jericho-palace-overview', 'Jericho · Hasmonean palace plan', notice,
         'Fig. 18, p. 281. Registered to 2023 imagery. Fit about 3 m at the pools; imagery accuracy 5 m.',
         src / 'trumper2018-fig18-p281.jpg', (0,0,1039,820))
    # Trümper figs. 20, 22 -> Netzer frame in research/models/traced_plans/jericho-pools-complex.json.
    # The fit in jericho.json then places the traced origin and rotates the Netzer frame clockwise.
    offset = complex(*jer['placement']['target'])
    turn = cmath.rect(1, math.radians(-jer['placement']['rotationDeg']))
    figures = [
        ('20', '3', '284', (0.0001390,-0.0579073), (-41.3091,46.6602)),
        ('22', '6', '286', (-0.0000170,-0.0577412), (-40.9537,46.5682)),
    ]
    for num, stage, page, scale, shift in figures:
        def to_place(xy):
            return offset + (complex(*scale)*complex(*xy) + complex(*shift))*turn
        scan(jer, f'jericho-stage-{stage}', f'Jericho · Pools Complex, Stage {stage}', notice,
             f'Fig. {num}, p. {page}. Partly reconstructed phase plan; the printed figure crops the pools on the east. Fit inherited from the palace overview (about 3 m at the pools; imagery accuracy 5 m).',
             src / f'trumper2018-fig{num}-p{page}.jpg', (5,5,1033,819), to_place)
    qum = read(REG / 'qumran.json')
    scan(qum, 'qumran-settlement-plan', 'Qumran · General excavation plan',
         'Yitzhak Magen and Yuval Peleg 2018, Fig. 9, p. 12. CC BY-NC 4.0. Cropped.',
         'Rendered at the source plan’s fitted scale and orientation. Fit about 2 m at the buildings; imagery accuracy 5 m.',
         qum['figures'][0]['file'], (232,183,1120,1609))
    folder = ROOT / 'research/assets/plans/bethesda-early-plans-2026-10-22'
    schick = read(folder / 'registration.json')
    schick_frame = dict(place='jer_bethesda', anchor=[31.78139,35.23583])
    path = folder / 'schick1888-p6.jpg'
    width, height = Image.open(path).size
    # Controls use a 360 dpi PDF rendering; the repository scan has 300 dpi.
    def schick_fit(xy):
        return fit(schick['fit'], (xy[0]*2729/width, xy[1]*2783/height))
    scan(schick_frame, 'bethesda-schick-1888', 'Bethesda · Schick’s 1888 survey',
         'Conrad Schick, PEF Quarterly Statement, July 1888, plate 1. Public domain.',
         'Fitted to St Anne’s Church, the city wall and Lions’ Gate. Selected features read about ±2 m within the registered plan; the mapped controls have separate positional uncertainty.',
         path, None, schick_fit, REPO+'research/assets/plans/bethesda-early-plans-2026-10-22/registration.json')


def traced_plans():
    reg = read(REG/'gerizim.json')
    box = (-60,-110,121,15)
    scale = 6
    canvas = Image.new('RGBA', ((box[2]-box[0])*scale,(box[3]-box[1])*scale))
    draw = ImageDraw.Draw(canvas)
    def pixel(xy):
        return tuple((v-b)*scale for v,b in zip(xy, box[:2]))
    positions = reg['positions']
    pts = list(map(pixel,positions['coreCorners_NW_NE_SE_SW']))
    draw.polygon(pts, fill=(228,182,95,90))
    draw.line(pts + pts[:1], fill=(254,213,116,255), width=6)
    for key in ['northGate','eastGate22','southGateMidWall','eastStairCentre']:
        x,y = pixel(positions[key]); r = 9 if key == 'eastStairCentre' else 6
        draw.ellipse((x-r,y-r,x+r,y+r),fill='white',outline=(49,39,24),width=3)
    canvas.save(PUBLIC/'gerizim-precinct.webp',lossless=True)
    add_plan('gerizim-precinct','gerizim','Gerizim · Precinct and gates',
             'Project redrawing of Magen’s registered plans. Gold shows the core precinct. Small dots mark the three gates; the larger dot marks the east stair centre. The drawing omits Cistern 2, whose position on Fig. 267 has no independent map fit. Plan-to-image agreement about 2 m; imagery accuracy 5 m.',
             'Project geometry after Magen 2008, NEAEHL 5, pp. 1743 and 1746.',source_url('gerizim'),'gerizim-precinct.webp',
             [lonlat(reg['anchor'],*p) for p in corners(box)])
    # Fig. 2 (Greenhut and Mazor, p. 72*, PDF p. 3) clipped at PDF rect
    # (25,55,500,475), rendered at 3 px/point. Top grid 222200 @ x303;
    # 222500 @ x1209. Left grid 630900 @ y374 and 630800 @ y676.
    # The lower margin repeats 630800; only the unambiguous upper pair is used.
    def siloam_grid(xy):
        x,y = xy
        return itm(222200 + (x-303)*300/906,630900 - (y-374)*100/302)
    box = (575,337,900,702)
    canvas = Image.new('RGBA', (box[2]-box[0],box[3]-box[1]))
    draw = ImageDraw.Draw(canvas)
    def outline(coords, fill, stroke):
        p=[(x-box[0],y-box[1]) for x,y in coords]
        draw.polygon(p,fill=fill)
        draw.line(p+p[:1],fill=stroke,width=3)
    outline([(621,463),(708,407),(847,507),(775,639),(694,579),(644,510)],
            (64,158,195,112),(130,222,249,255))
    outline([(778,639),(795,616),(802,617),(793,655),(781,651)],
            (204,103,61,220),(255,220,168,255))
    canvas.save(PUBLIC/'siloam-fig2.webp',lossless=True)
    add_plan('siloam-pool-excavation','jer_siloam','Siloam · Pool and adjacent excavation',
             'Blue follows the generalized basin boundary. Copper marks the authors’ excavation against the southeast dam face. The positions come from the figure’s printed 100 m Israel Grid ticks. The drawing has no independent field check or outlet position.',
             'Project redrawing after Zvi Greenhut and Gabriel Mazor, ʿAtiqot 101 (2020), p. 72*, fig. 2.',
             'https://publications.iaa.org.il/atiqot/vol101/iss1/6/', 'siloam-fig2.webp',
             [siloam_grid(p) for p in corners(box)])


def research_features():
    def add(id,site,title,status,detail,credit,kind,points):
        out=[round_xy(pg(*p)) for p in points]
        geometry={'type':kind,'coordinates':out[0] if kind=='Point' else [out+out[:1]] if kind=='Polygon' else out}
        features.append(dict(type='Feature',id=id,geometry=geometry,properties=dict(
            id=id,title=title,status=status,siteId=site,detail=detail,credit=credit,sourceUrl=LOG)))
    # B135's six named quadrants within 5 km sheet 190-140. Each frame is 625 m square.
    for sheet,left,quads in [('15',192500,'I II III IV'),('16',193750,'I III')]:
        for quad in quads.split():
            e=left+(625 if quad in ['II','IV'] else 0)
            n=140625 if quad in ['I','II'] else 140000
            number=sheet+'.'+quad
            add('jericho-1930-'+number,'jericho_area','1930 Jericho · '+number,'Sheet footprint',
                '625 m printed frame of Survey of Palestine town plan 190-140.'+number+'. The six-sheet registration agreed at three modern checks to about 2–5 m by eye. This rectangle marks sheet coverage.',
                'B135 · Survey of Palestine, Jericho town plans, May 1930, 1:1,250.',
                'Polygon',[(e,n),(e+625,n),(e+625,n+625),(e,n+625)])
    add('qos-trig','tell_el_qos','Tell el-Qos · Trig station 835','Checked',
        'Survey station on the ground labelled “Threshing Floors”, about ±5 m on the registered 1930 plan. Identification as a tell remains unresolved.',
        'B136 · Survey of Palestine, May 1930.','Point',[(193913,140330)])
    add('qasab-bridge','jericho_area','Qanāt el-Qasab · Canal bridge','Checked',
        'The registered 1930 plan gives the north bank and east turn, about 88 m apart along a bearing of 149°. Endpoints lie within about 15 m of the image readings.',
        'B130, B137 · Survey of Palestine, May 1930.','LineString',[(192880,140083),(192926,140008)])
    add('sultan-north-channel','tell_es_sultan','North channel · 1918 probable course','Probable',
        'Generalized line between the mill compound, bend and track junction. Two 1918 photographs show the northeast reach; stereo shows a contour channel on the southwest reach. A local fit check was about 50 m. Construction date unknown.',
        'B140–141 · Bavarian frames BS Pal. 1020-a, 1032 and 1033, May–June 1918.','LineString',
        [(191690,142020),(191850,142550),(192270,142840)])
    add('dabakiyeh-strip','', 'Tell ed-Dabakiyeh · Observed strip extent','Approximate extent',
        'Box around an east–west uncultivated strip seen on six Wayback dates in 2011–22. The reported strip measures about 95 × 20–25 m. No pool, bank or wall outline is resolved.',
        'B158, B171 · MEGA-Jordan, Glueck site 217 and Esri Wayback.','Polygon',
        [(210630,136950),(210720,136950),(210720,136980),(210630,136980)])
    add('dabakiyeh-mega','', 'Tell ed-Dabakiyeh · Catalogue point','Possible place',
        'MEGA-Jordan 10292, JADIS 2113040. The catalogue records a reservoir; point accuracy is unstated. The adjacent outline shows imagery coverage of an observed strip.',
        'B158 · MEGA-Jordan, after Glueck 1951.','Point',[(210673,136970)])
    features[-1]['geometry']['coordinates']=[35.63981,31.82479]  # native catalogue coordinate


if __name__ == '__main__':
    PUBLIC.mkdir(parents=True,exist_ok=True)
    plan_scans()
    traced_plans()
    research_features()
    DATA.write_text(json.dumps({'plans':plans,'features':{'type':'FeatureCollection','features':features}},
                               ensure_ascii=False,indent=2)+'\n')
