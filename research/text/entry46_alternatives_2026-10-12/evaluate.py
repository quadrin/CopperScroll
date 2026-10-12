#!/usr/bin/env python3
"""Exploratory entry-46 pool/pit and distance/depth/count comparison.

Consumes existing, exposed source rows. Writes only this review directory (or
an explicitly supplied temporary output directory). No protected image access.
"""
import csv
import gzip
import hashlib
import io
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
try:
    import pyproj
except ImportError:
    # Local installation used only by this workspace; never public vendored
    # code. Other project grid conversions already require pyproj.
    sys.path.insert(0,str(Path(__file__).resolve().parent/'.deps'))
    import pyproj
Transformer=pyproj.Transformer
TRANSFORMERS={}

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MERGED = REPO / 'research/regional/haesi_features/merged_2026-10-12/features_all.csv'
PHASES = REPO / 'research/regional/water_systems/entry46_phase_review_2026-10-12/phases.csv.gz'
HELD_ROOT = REPO / 'research/regional/haesi_features/phase4_2026-10-11'
PLACES = REPO / 'research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv'
READINGS = REPO / 'text/readings.json'
M, F, U = 'MATCH', 'FAIL', 'UNKNOWN'
BOX = (31.600, 31.900, 35.120, 35.560)
POTENTIAL = {'rockcut_installation', 'cistern', 'pool_reservoir', 'ritual_bath',
             'cave_with_finds', 'tomb_burial_cave', 'columbarium_dovecote'}
PIT = re.compile(r'\b(?:pits?|shafts?)\b', re.I)
DEEP = re.compile(r'\bdeep (?:rock[- ](?:cut|hewn) )?(?:pits?|shafts?)\b|\b(?:pits?|shafts?) (?:was |were |is |are )?deep\b', re.I)
SHALLOW = re.compile(r'\bshallow (?:rock[- ](?:cut|hewn) )?pit\b', re.I)
ENTRANCE = re.compile(r'\b(?:entrance|doorway|stairs?|staircase|steps?|stepped)\b', re.I)
COUNT_PITS = re.compile(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+) (?:small |round |circular |hewn |plastered |unplastered |rock[- ](?:cut|hewn) )*(?:pits?|shafts?)\b(?:[- ](?:tombs?|graves?))?', re.I)
METRES = re.compile(r'(\d+(?:\.\d+)?)\s*m\s*(?:deep|depth)|\b(?:depth|height)\s*(?:of |c\.?\s*)?(\d+(?:\.\d+)?)\s*m\b', re.I)


def read(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, rows, fields=None):
    fields = fields or list(rows[0])
    buf = io.StringIO(newline='')
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    b = buf.getvalue().encode()
    if str(path).endswith('.gz'):
        with Path(path).open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as f:
                f.write(b)
    else:
        Path(path).write_bytes(b)


def overall(*codes):
    if F in codes:
        return F
    return M if codes and all(x == M for x in codes) else U


def km(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d))
    return 6371.0088 * 2 * math.asin(math.sqrt(math.sin((c-a)/2)**2 +
               math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2))


def place(row, anchor, radius):
    if not row['lat'] or not row['lon']:
        return U
    dist = km(float(row['lat']), float(row['lon']), *anchor)
    # Same coordinate-envelope convention as the inherited water evaluator.
    # Anchor association is a separate UNKNOWN gate, never supplied by radius.
    err = float(row['precision_m'] or 0) / 1000
    return M if dist + err <= radius else F if dist - err > radius else U


def axis_range(text, normalized):
    """Expand shortened final grid digits, using existing axis scale as a check.

    Older printed grids use 10/100 m digits. Their existing normalized
    projected axis must authenticate that scale; unknown scale stays unknown.
    """
    m=re.fullmatch(r'(\d+)\s*[–—−-]\s*(\d+)',text.strip())
    if not m:
        return None
    first,last=m.groups()
    if len(last)>len(first):
        return None
    a=int(first);b=int(first[:len(first)-len(last)]+last)
    if b<a:
        return None
    if len(first)==6:
        scale=1
    else:
        try:
            scales=[s for s in (1,10,100,1000) if abs(a*s-float(normalized))<0.01]
        except (TypeError,ValueError):
            return None
        if len(scales)!=1:
            return None
        scale=scales[0]
    return a*scale,b*scale,scale


def position_envelope(r):
    ref=r['map_ref_as_given']
    base=dict(lat=r['lat'],lon=r['lon'],precision_m=r['precision_m'],
              position_kind='inherited source point',map_ref_as_given=ref,
              crs_used=r['crs_used'],range_bounds_m='')
    if not re.search(r'\d\s*[–—−-]\s*\d',ref):
        return base
    base.update(lat='',lon='',precision_m='',position_kind='range unresolved; point disabled')
    if r['crs_used'] not in ('EPSG:2039','EPSG:28191') or ref.count('/')!=1:
        return base
    xs,ys=ref.split('/')
    x=axis_range(xs,r['easting_m']);y=axis_range(ys,r['northing_m'])
    if x is None or y is None:
        return base
    if r['crs_used'] not in TRANSFORMERS:
        TRANSFORMERS[r['crs_used']]=Transformer.from_crs(r['crs_used'],'EPSG:4326',always_xy=True)
    tr=TRANSFORMERS[r['crs_used']]
    clon,clat=tr.transform((x[0]+x[1])/2,(y[0]+y[1])/2)
    corners=[tr.transform(a,b) for a in x[:2] for b in y[:2]]
    # Enclosing circle is conservative for both anchors; half-grid rounding
    # enters the envelope. It never turns a range crossing a radius into MATCH.
    err=max(km(clat,clon,lat,lon)*1000 for lon,lat in corners)+math.hypot(x[2],y[2])/2
    return dict(base,lat=f'{clat:.8f}',lon=f'{clon:.8f}',precision_m=f'{err:.3f}',
                position_kind='report range; conservative enclosing circle',
                range_bounds_m=json.dumps([list(x[:2]),list(y[:2])],separators=(',',':')))


def numeric(obs, interpretation):
    """Match branch-specific measurements only; missing datum always unknown.

    No metre value is derived from ten unless a sourced unit interval and
    tolerance are supplied. Source dimensions never act as a deposit target.
    """
    if not obs or obs.get('phase_join') != M or obs.get('left_origin') != M:
        return U
    if interpretation == 'ten-small-pits':
        if obs.get('kind') != 'left-side-pit-set' or obs.get('count_complete') is not True:
            return U
        if obs.get('members_small_pits') != M:
            return U
        return M if obs.get('distinct_count') == 10 else F
    kind = {'ten-cubits-distance': 'entrance-to-target-horizontal',
            'ten-cubits-depth': 'ancient-datum-to-target-vertical'}[interpretation]
    if obs.get('kind') != kind or obs.get('datum_identified') != M:
        return U
    if not obs.get('unit_source') or not obs.get('target_source'):
        return U
    unit = obs.get('unit_interval_m')
    measured = obs.get('measured_interval_m')
    tolerance = obs.get('tolerance_m')
    if unit is None or measured is None or tolerance is None:
        return U
    if len(unit) != 2 or len(measured) != 2 or unit[0] <= 0 or unit[0] > unit[1] or measured[0] > measured[1] or tolerance < 0:
        raise ValueError('invalid numeric interval')
    lo, hi = unit[0]*10 - tolerance, unit[1]*10 + tolerance
    # Entire measurement interval inside the allowed envelope is a match;
    # disjoint is a fail; overlap at an uncertainty boundary stays unknown.
    if lo <= measured[0] and measured[1] <= hi:
        return M
    if measured[1] < lo or measured[0] > hi:
        return F
    return U


def select(rows, held=()):
    """Preferred version per report-group/class; same opportunity for controls."""
    by = defaultdict(list)
    excluded = Counter()
    for r in rows:
        # Metadata exclusions precede text-derived morphology screening.
        if r['counted'] != 'yes' or r['feature_type'] not in POTENTIAL:
            continue
        if r['report_id'] in held or r['protected_strip'] == 'yes' or re.match(r'HA(?:28|29)-', r['report_id']) or re.search(r'almit|עלמית|\bt[ae]l+[- ]?(?:e[sl][- ])?sultan|tall al-sultan', r['site_name'], re.I):
            excluded['protected_or_tier1_metadata'] += 1
            continue
        if r['series'] == 'SWP Memoirs':
            excluded['SWP_unresolved_placement'] += 1
            continue
        pos=position_envelope(r)
        if pos['lat']:
            lat,lon=float(pos['lat']),float(pos['lon'])
            angular=float(pos['precision_m'] or 0)/1000/6371.0088*180/math.pi
            lon_err=angular/max(math.cos(math.radians(lat)),0.01)
            outside=lat+angular<BOX[0] or lat-angular>BOX[1] or lon+lon_err<BOX[2] or lon-lon_err>BOX[3]
        else:
            outside=False
        if outside:
            excluded['outside_prior_water_box'] += 1
            continue
        by[(r['report_group'], r['feature_type'])].append(r)
    chosen = []
    for k in sorted(by):
        rs = by[k]
        chosen.extend([r for r in rs if r['version_role'] in ('single', 'preferred')] or rs)
    return chosen, excluded


def held_inputs():
    paths = sorted(HELD_ROOT.glob('**/held*.csv'))
    if not paths:
        raise ValueError('held metadata absent; cannot silently drop protected exclusions')
    # Inspect identifier columns only; the report contents remain unopened.
    return paths, {r['unit_id'] for p in paths for r in read(p)}


def pit_record(r):
    # Prefer the existing reader's feature description. A brief quote may
    # mention an excavator's test pit beside a feature of another kind.
    text = r['feature_subtype'] or r['quote']
    mentions = [m.group(0) for m in COUNT_PITS.finditer(text)]
    measurements = [m.group(0) for m in METRES.finditer(text)]
    # A generic cave/cistern label cannot prove the deep-pit alternative, but
    # the broad sensitivity keeps these recorded underground possibilities.
    pit = M if PIT.search(text) else U
    deep = M if DEEP.search(text) else U
    # A shallow isolated pit contradicts the deep-pit form. Aggregates can
    # contain a separate shaft/deep pit, so retain their ambiguity.
    if SHALLOW.search(text) and r['n_features'] == '1' and len(PIT.findall(text)) == 1:
        deep = F
    ent = M if ENTRANCE.search(text) else U
    window = M if r['dated_in_window'] == 'yes' else F if r['dated_in_window'] == 'no' else U
    p=dict(phase_id='IAA:' + r['row_uid'] + '@unsplit', origin_row=r['row_uid'],
                name=r['site_name'], source=f"{r['series']} {r['volume']} ({r['year']})",
                locator=f"pp.{r['pages']}; {r['url']}", source_file=r['source_file'],
                report_group=r['report_group'], site_id=r['site_id'],
                feature_type=r['feature_type'], feature_subtype=r['feature_subtype'],
                phase='unsplit source description; physical feature joins unverified',
                lat=r['lat'], lon=r['lon'], precision_m=r['precision_m'],
                original_n_features=r['n_features'], original_period=r['period_as_given'],
                reported_window=window, configuration_in_window=U, entrance=ent,
                same_phase=U, pit_form=pit, deep_qualification=deep,
                reported_pit_count_phrases=';'.join(mentions),
                reported_vertical_dimensions=';'.join(measurements),
                numerical_target=U, evidence='derivative source coding; original quantity preserved; no datum/target transfer')
    p.update(position_envelope(r))
    return p


def normalize_pool(p, source_rows):
    row=dict(phase_id=p['phase_id'], origin_row=p['origin_row'], name=p['name'], source=p['source'],
                locator=p['locator'], source_file='inherited pool phase review', report_group='', site_id='',
                feature_type=p['type'], feature_subtype='', phase=p['phase'], lat=p['lat'], lon=p['lon'],
                precision_m=p['precision_m'], original_n_features='', original_period=p['reported_period'],
                reported_window=M if p['reported_period'] in ('in', 'in_hedged') else F if p['reported_period']=='out' else U,
                configuration_in_window=p['configuration_in_window'], entrance=p['entrance'], same_phase=p['same_phase'],
                pit_form=U, deep_qualification=U, reported_pit_count_phrases='', reported_vertical_dimensions='',
                numerical_target=U, evidence=p['evidence_level'], contained_water=p['contained_water'],
                storage_use=p['storage_use'], reported_contained_water=p['reported_contained_water'],
                original_stair_origin=p['original_stair_origin'])
    row.update(position_kind='inherited phase position',map_ref_as_given='',crs_used='EPSG:4326',range_bounds_m='')
    matches=[r for r in source_rows if p['origin_row'].endswith(r['row_uid'])]
    if matches:
        r=max(matches,key=lambda r:len(r['row_uid']))
        envelope=position_envelope(r)
        # Even a favored phase override cannot shrink an unspecific source
        # rectangle to a metre point. The same rule updates all comparators.
        if 'range' in envelope['position_kind']:
            row.update(envelope)
    return row


def apply_native(pits, source_rows, specs):
    by={r['row_uid']:r for r in source_rows}
    replace=defaultdict(list)
    additions=[]
    for spec in specs:
        base=pit_record(by[spec['origin_row']])
        base.update({k:v for k,v in spec.items() if k not in ('replace_origin','source_measurement_id')})
        # Original source counts remain visible beside separately inspected
        # individual features. No source/phase count aggregation occurs.
        base['evidence']='native owner-supplied report inspection; source_measurement_id='+spec['source_measurement_id']
        if spec.get('replace_origin'):
            replace[spec['origin_row']].append(base)
        else:
            additions.append(base)
    out=[]
    for p in pits:
        out.extend(replace.get(p['origin_row'],[p]))
    out.extend(additions)
    if len({p['phase_id'] for p in out})!=len(out):
        raise ValueError('duplicate native feature identity')
    return out


def evaluate(records, anchors, observations):
    scores = []
    for reading, model, r in records:
        if reading == 'pool':
            form = r['contained_water'] if model == 'contained-water' else r['storage_use']
            reported_form = r['reported_contained_water'] if model=='contained-water' else form
        else:
            form = overall(r['pit_form'], r['deep_qualification'])
            reported_form = form
        for anchor, point in sorted(anchors.items()):
            for radius in (1, 2):
                geo = place(r, point, radius)
                for interp in ('ten-cubits-distance', 'ten-cubits-depth', 'ten-small-pits'):
                    obs = observations.get((r['phase_id'], interp))
                    left = obs.get('left_origin', U) if obs else U
                    num = numeric(obs, interp)
                    full = overall(geo, r['entrance'], form, r['same_phase'],
                                   r['configuration_in_window'], U, left, num)
                    scores.append(dict(phase_id=r['phase_id'], origin_row=r['origin_row'],
                      installation_reading=reading, function_model=model, interpretation=interp,
                      anchor=anchor, radius_km=radius, conditional_place=geo, form=form,
                      entrance=r['entrance'], same_phase=r['same_phase'],
                      reported_window=r['reported_window'], configuration_in_window=r['configuration_in_window'],
                      ancient_place_association=U, left_origin=left, numerical_relation=num,
                      reported_subset=overall(geo, reported_form, r['entrance'], r['reported_window']),
                      full_branch=full))
    return scores


def main(out=HERE):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    held_paths, held = held_inputs()
    inputs = [MERGED, PHASES, PLACES, READINGS, HERE/'SPEC.md', HERE/'numerical_observations.json',
              HERE/'native_sources.json',HERE/'native_feature_overrides.json',HERE/'evaluate.py'] + held_paths
    input_hashes = {str(p.relative_to(REPO)):sha(p) for p in inputs}
    # Numeric exposure is explicit. Unique observation keys forbid overwriting
    # a failed phase/interpretation with another datum under the same key.
    rawobs = json.loads((HERE/'numerical_observations.json').read_text())['observations']
    observations = {(o['phase_id'],o['interpretation']):o for o in rawobs}
    if len(observations) != len(rawobs):
        raise ValueError('duplicate numerical observation key')
    if sha(MERGED) != '23a23214ed475b5c3a3a213f29d4094518acbdf1b187cffd7c78949a635eae38':
        raise ValueError('merged inventory differs from baseline phase4 input pin')
    source_rows=read(MERGED)
    selected, excluded = select(source_rows, held)
    pits = [pit_record(r) for r in selected]
    pits = apply_native(pits,source_rows,json.loads((HERE/'native_feature_overrides.json').read_text()))
    pools = [normalize_pool(p,source_rows) for p in read(PHASES)]
    points = {r['place_id']:(float(r['lat']),float(r['lon'])) for r in read(PLACES) if r['lat']}
    anchors = dict(ramat_rahel=points['ramat_rahel'], ein_kerem=(31.766728,35.161996))
    records = [('deep-pit','deep-pit',p) for p in pits]
    for p in pools:
        records.extend([('pool','contained-water',p),('pool','storage-service',p)])
    scores = evaluate(records,anchors,observations)
    write(out/'pit_source_records.csv.gz',pits)
    write(out/'scores.csv.gz',scores)
    counts = defaultdict(Counter)
    for s in scores:
        for layer in ('reported_subset','full_branch'):
            counts[(s['installation_reading'],s['function_model'],s['interpretation'],s['anchor'],s['radius_km'],layer)][s[layer]] += 1
    write(out/'counts.csv',[dict(installation_reading=a,function_model=b,interpretation=c,anchor=d,radius_km=e,layer=f,
         N=sum(n.values()),match=n[M],fail=n[F],unknown=n[U]) for (a,b,c,d,e,f),n in sorted(counts.items())])
    # Keep source rows near either named anchor, plus unlocated possibilities.
    near = [p for p in pits if not p['lat'] or any(place(p,a,2)!=F for a in anchors.values())]
    write(out/'pit_followup.csv',near)
    write(out/'pit_morphology_shortlist.csv',[p for p in near if p['pit_form']==M])
    audited = {p['phase_id'] for p in pools if '@unsplit' not in p['phase_id']}
    write(out/'audited_bath_scores.csv',[s for s in scores if s['phase_id'] in audited])
    branch_defs = []
    for installation in ('pool','deep-pit'):
        for interp in ('ten-cubits-distance','ten-cubits-depth','ten-small-pits','ten-feet','twelve-feet','notches'):
            branch_defs.append(dict(installation=installation,interpretation=interp,
              status='evaluated with missing observations retained as UNKNOWN' if interp.startswith('ten-cubits') or interp=='ten-small-pits' else 'retained; original metric/count interpretation unverified',
              edition='Puech2015 pp85,87-88; Lefkovits2000 pp331,333' if interp.startswith('ten-cubits') else 'Lefkovits2000 p333' if interp=='ten-small-pits' else 'inherited text/readings.json; no native reinspection',
              conversion='none; explicit unit/target interval required' if interp.startswith('ten-cubits') else 'count only' if interp=='ten-small-pits' else 'unverified',
              result='not identifiable from available evidence'))
    write(out/'reading_branches.csv',branch_defs)
    corrections=[]
    for r in selected:
        pos=position_envelope(r)
        if 'range' not in pos['position_kind']:
            continue
        for anchor,point in sorted(anchors.items()):
            for radius in (1,2):
                corrections.append(dict(origin_row=r['row_uid'],report_group=r['report_group'],
                  map_ref_as_given=r['map_ref_as_given'],crs_used=r['crs_used'],
                  old_lat=r['lat'],old_lon=r['lon'],old_precision_m=r['precision_m'],
                  corrected_lat=pos['lat'],corrected_lon=pos['lon'],corrected_precision_m=pos['precision_m'],
                  correction_kind=pos['position_kind'],anchor=anchor,radius_km=radius,
                  old_place=place(r,point,radius),corrected_place=place(pos,point,radius)))
    write(out/'position_corrections.csv.gz',corrections)
    summary = dict(baseline_commit='3b2d5c44b8c0add84a69d25f8e72cd16acc886db',exploratory=True,
      result='not identifiable from available evidence', claim='complete entry46 landmark/left/numerical relation',
      input_sha256=input_hashes, exclusions=dict(excluded), pit_source_descriptions=len(pits),
      pit_reported_morphology=dict(Counter(p['pit_form'] for p in pits)),
      pit_reported_deep_qualification=dict(Counter(p['deep_qualification'] for p in pits)),
      unlocated_pit_sensitivity_descriptions=sum(not p['lat'] for p in pits),
      pit_dimension_descriptions=sum(bool(p['reported_vertical_dimensions']) for p in pits),
      pit_count_phrase_descriptions=sum(bool(p['reported_pit_count_phrases']) for p in pits),
      retained_held_metadata_files=[str(p.relative_to(REPO)) for p in held_paths],
      pool_phase_descriptions=len(pools), numerical_target_observations=len(rawobs),
      full_branch=dict(Counter(s['full_branch'] for s in scores)),
      numeric_clause=dict(Counter(s['numerical_relation'] for s in scores)),
      denominator='source/phase descriptions; unresolved physical duplicates/aggregates, not installations or regional rarity',
      protected_access='metadata exclusions only; no new protected originals opened',
      metric_limit='basin/shaft depth, cave height and original n_features remain source observations; none supplies a deposit target/datum or complete left-side pit count',
      branch_provenance='Cartesian operational sensitivity across retained installation and numeric interpretations; not a claim that every combination is one edition\'s continuous translation. Puech sequence lacks displayed derivative חפור; no digging imperative is silently borrowed.',
      position_range_correction='all comparator/candidate source mapref ranges use a conservative enclosing circle including printed-grid rounding; unparseable range/CRS disables prior point and leaves geography UNKNOWN',
      pit_position_kinds=dict(Counter(p['position_kind'] for p in pits)),
      pool_position_kinds=dict(Counter(p['position_kind'] for p in pools)),
      pyproj_version=pyproj.__version__,
      source_access_errors=['https://hadashot.iaa.org.il/report_detail_eng.aspx?id=26686','https://hadashot.iaa.org.il/report_detail_eng.aspx?id=26098'])
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    if input_hashes != {str(p.relative_to(REPO)):sha(p) for p in inputs}:
        raise ValueError('input changed during run')
    print(json.dumps({k:summary[k] for k in ('result','pit_source_descriptions','pool_phase_descriptions','full_branch','numeric_clause')}))


if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else HERE)
