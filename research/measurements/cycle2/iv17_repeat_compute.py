"""Independent manual redigitization; reads pilot only after frozen raw file."""
import json, math, hashlib, itertools, argparse
from pathlib import Path
D=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--pilot-root', type=Path, default=D.parent)
args=parser.parse_args()
rawpath=D/'iv17_repeat.json'
r=json.loads(rawpath.read_text())
p=json.loads((args.pilot_root/'iv17_pilot.json').read_text())
pcomputed=json.loads((args.pilot_root/'iv17_recomputed.json').read_text())
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def norm(v):return math.hypot(*v)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def midpoint(a,b):return ((a[0]+b[0])/2,(a[1]+b[1])/2)
def basis(tail,tip):
    v=sub(tip,tail);n=tuple(x/norm(v) for x in v);return n,(-n[1],n[0])
def bearing(v,n,e):return math.degrees(math.atan2(dot(v,e),dot(v,n)))%360
s=r['scale']; mp=s['length_m']/norm(sub(s['three_m_xy'],s['zero_xy']))
na=r['north_arrow'];n,e=basis(na['tail_xy'],na['tip_xy'])
# Frozen labels accidentally reflected page layout. Preserve picks and map by physical feature.
features=[('northern_present_gap','southern_present_gap','wall_end_xy','pillar_end_xy'),('southern_remaining_gap','northern_clear_mouth','endpoint_a_xy','endpoint_b_xy')]
def pert(pt,u):return [(pt[0]+dx,pt[1]+dy) for dx,dy in itertools.product((-u,u),repeat=2)]
scale_values=[s['length_m']/norm(sub(b,a)) for a,b in itertools.product(pert(s['zero_xy'],2),pert(s['three_m_xy'],2))]
bases=[basis(t,t2) for t,t2 in itertools.product(pert(na['tail_xy'],2),pert(na['tip_xy'],2))]
aps=[]; mids=[]
for pid,key,ka,kb in features:
    f=r[key];a,b=f[ka],f[kb];v=sub(b,a);mid=midpoint(a,b);mids.append(mid)
    normal=(-v[1],v[0]);out=sub(f['outward_side_reference_xy'],mid)
    if dot(normal,out)<0:normal=tuple(-x for x in normal)
    bd=bearing(normal,n,e);axis=bearing(v,n,e)%180
    widths=[];bs=[]
    for aa,bb in itertools.product(pert(a,f['endpoint_uncertainty_px_each']),pert(b,f['endpoint_uncertainty_px_each'])):
        vv=sub(bb,aa);nn=(-vv[1],vv[0]);oo=sub(f['outward_side_reference_xy'],midpoint(aa,bb))
        if dot(nn,oo)<0:nn=tuple(-x for x in nn)
        widths.extend(norm(vv)*z for z in scale_values)
        bs.extend(bearing(nn,nb,eb) for nb,eb in bases)
    pilot=next(x for x in p['apertures'] if x['id']==pid)
    prev=next(x for x in pcomputed['apertures'] if x['id']==pid)
    width=norm(v)*mp
    aps.append({'canonical_id':pid,'frozen_key':key,'endpoint_a_xy':a,'endpoint_b_xy':b,'midpoint_xy':mid,'width_m':width,'chord_axis_deg_mod180':axis,'outward_chord_normal_proxy_deg':bd,'independent_corner_sensitivity_width_m':[min(widths),max(widths)],'independent_corner_sensitivity_bearing_deg':[min(bs),max(bs)],'pilot_width_envelope_m':pilot['width_envelope_m'],'pilot_bearing_envelope_deg':pilot['outward_chord_normal_envelope_deg'],'point_within_pilot_width_envelope':pilot['width_envelope_m'][0]<=width<=pilot['width_envelope_m'][1],'point_within_pilot_bearing_envelope':pilot['outward_chord_normal_envelope_deg'][0]<=bd<=pilot['outward_chord_normal_envelope_deg'][1],'delta_from_pilot_unrounded_width_m':width-prev['gap_chord_m'],'delta_from_pilot_unrounded_proxy_deg':bd-prev['outward_chord_normal_deg']})
delta=sub(mids[0],mids[1]);sep=norm(delta)*mp
out={'result':'supporting reproduction of published-plan-relative pilot point metrics; site and ancient entry identification remain inconclusive','raw_picks_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'raw_file_actual_freeze_utc':'2026-10-02T05:40:28.472118Z','raw_file_timestamp_error':'frozen_utc string 05:42:00 was typed incorrectly; filesystem mtime and pre-pilot tool-record hash establish actual freeze before first pilot read at 05:40:33Z','identity_correction':'frozen northern_clear_mouth key = physical left/built-wall opening = geographic southern_remaining_gap; frozen southern_present_gap key = physical right/clear opening = geographic northern_present_gap. Classification corrected only after pilot comparison; coordinates unchanged.','source_render_sha256':'59c490eb83e918b09be1d9bdcb8a4809a08401d54988f5c9fc6028d803deb044','raster_metadata_after_pilot_read':p['raster'],'metres_per_pixel':mp,'apertures':aps,'pair':{'midpoint_separation_m':sep,'southern_to_northern_bearing_deg':bearing(delta,n,e),'northern_minus_southern_north_m':dot(delta,n)*mp,'northern_minus_southern_east_m':dot(delta,e)*mp,'pilot_separation_envelope_m':p['pair']['separation_envelope_m'],'point_within_pilot_separation_envelope':p['pair']['separation_envelope_m'][0]<=sep<=p['pair']['separation_envelope_m'][1]},'uncertainty_method':'independent per-coordinate endpoint boxes evaluated at all corners, scale endpoints +/-2px, north endpoints +/-2px, clear right opening +/-6px, ragged left opening +/-5px; non-statistical raster sensitivity only; scan distortion and north convention unquantified','limits':['same source raster; independent picks are not independent archaeological corroboration','mouth chord normal is a 2D facing proxy, not passage-axis orientation','published north true/grid/magnetic convention unspecified','left southern remaining gap does not recover ancient pre-wall mouth','phase unknown; no threshold, deposit geometry, exact site georeferencing or primary-source novelty claim']}
(D/'iv17_repeat_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
