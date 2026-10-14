#!/usr/bin/env python3
"""Exploratory evidence audit; unknown is never converted to absence."""
from pathlib import Path
import csv, json, hashlib, argparse
from collections import Counter

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
parser=argparse.ArgumentParser()
parser.add_argument('--full',action='store_true',help='Generate complete row matrix locally; large output is not part of committed packet')
args=parser.parse_args()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def dump(name,data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def aggregate(vals):
    if 'contradicted' in vals:return 'contradicted'
    if all(v=='compatible' for v in vals):return 'compatible'
    return 'unknown'

tomb_path=REPO/'research/regional/tombs/tombs.csv'
cave_path=REPO/'research/regional/caves_entry25/caves.csv'
tombs=rows(tomb_path);caves=rows(cave_path)
assert len(tombs)==1159 and len(caves)==665
out=[]
e2branches=['PUECH_ALLEGRO_COURSE','LEFKOVITS_THIRD_GRAVESTONE','MILIK_PERSONAL_NAME','WOLTERS_PERSON_THIRD','LEFKOVITS_OTHER_APPARATUS']
for t in tombs:
    for branch in e2branches:
        # Negative F1 coding reflects dictionary silence, not archaeological absence.
        monument='compatible' if t['monument_F1']=='yes' else 'unknown'
        clauses={'funerary_monument':monument,'original_component_or_gravestone':'unknown','third_course_or_gravestone_or_person_identity':'unknown','ancient_existence_of_target_component':'unknown','deposit':'unknown'}
        out.append({'entry':2,'record':t['unit_id'],'record_id':t['record_id'],'locator':t['locator'],'possible_duplicate_of':t['possible_duplicate_of'],'aggregate_record':t['multi_tomb_record'],'branch':branch,'clauses':clauses,'full_status':aggregate(list(clauses.values())),'date_descriptor_only':t['period_terms']})

e26branches=['PUECH_BASE_BOULDER','MILIK_ROCK_BASE','PROJECT_CORNER_HEAP','LURIE_CORNER_CLOD','LEFKOVITS_BUILDER_SEPULCHER','LEFKOVITS_OTHER_APPARATUS']
def direct_cave_aspect(c):
    pairs=[x.split(':',1) for x in c['opening_facings'].split(';') if ':' in x]
    # The cave-level observation must identify its own subject. Position-in-wall inference stays unknown.
    if 'INFERENCE' in c['facing_basis'] or 'position word' in c['facing_basis']:return 'unknown'
    cave=[v for k,v in pairs if k=='cave']
    if len(cave)!=1:return 'unknown'
    if cave[0]=='E':return 'documentary_E_code'
    if cave[0] in ['N','S','W','NW']:return 'documentary_non_E_code'
    return 'unknown' # NE/SE boundary and plan normals unresolved; exact physical aspect stays unknown.
for c in caves:
    for branch in e26branches:
        for attachment in ['cave','landmark']:
            aspect=direct_cave_aspect(c) if attachment=='cave' else 'unknown'
            clauses={'cave':'compatible' if not c['c1_override'] and c['row_kind']!='cluster' else 'unknown','edition_specific_landmark_relation':'unknown','east_aspect_current_form':'unknown','ancient_aspect_and_landmark_phase':'unknown','nine_cubit_axis_surface_and_target':'unknown','deposit':'unknown'}
            # Catalogue codes describe coarse documentary labels; adjacent four-wind sectors can share a boundary.
            ancient=dict(clauses);ancient['east_aspect_current_form']='unknown'
            out.append({'entry':26,'record':c['cave_id'],'locator':c['source_records'],'possible_duplicate_of':c['possible_duplicate_of'],'aggregate_record':c['row_kind'],'branch':branch,'aspect_attachment':attachment,'documentary_aspect_code':aspect,'facing_basis':c['facing_basis'],'opening_facings':c['opening_facings'],'clauses':clauses,'current_form_status':aggregate(list(clauses.values())),'full_ancient_status':aggregate(list(ancient.values())),'date_descriptor_only':c['period_stated']})
    out.append({'entry':26,'record':c['cave_id'],'locator':c['source_records'],'branch':'ALLEGRO_INNER_CHAMBER_WATCHTOWER','clauses':{'inner_chamber':'unknown','watchtower':'unknown','east_aspect':'unknown','nine_cubit_datum':'unknown'},'full_ancient_status':'not_scored_natural_cave_inventory'})

native=[
 {'entry':2,'component':'KZ6-2 Absalom rock-cut lower body','source':'Kloner/Zissu2003 p142/viewer156','funerary_monument':'compatible','literal_built_courses':'contradicted','scope':'preserved rock-cut lower component only; upper built section separately recorded','full_ancient_identification':'unknown'},
 {'entry':2,'component':'KZ6-2 Absalom built upper body','source':'Kloner/Zissu2003 p142/viewer156','funerary_monument':'compatible','built_stone_component':'compatible','literal_built_courses':'unknown','third_original_course_origin':'unknown','scope':'source describes upper part built of two large dressed stones; no third-course datum established','full_ancient_identification':'unknown'},
 {'entry':2,'component':'KZ6-4 Zechariah preserved nefesh','source':'Kloner/Zissu2003 p146/viewer160','funerary_monument':'compatible','literal_built_courses':'contradicted','scope':'source explicitly calls preserved monument monolithic and wholly carved out of rock; grave itself absent; gravestone/name branches unknown','full_ancient_identification':'unknown'},
 {'entry':2,'component':'Mird rubble monument','source':'Wright/Milik1961 pp14–16, Fig4, platesVIII–IX; existing extraction re-used','funerary_monument':'unknown','literal_built_courses':'compatible','third_original_course_origin':'unknown','scope':'funerary versus high-place function unresolved; retaining walls founded at differing levels; no complete excavation negative','full_ancient_identification':'unknown'}
]
if args.full:dump('all_row_predicates.json',out)
dump('native_component_checks.json',native)
summary={
 'claim':'Entries 2 and 26 identify an archaeological structure in available evidence',
 'terminal_result':'not identifiable from available evidence',
 'observations_exposed':True,'confirmation':False,'landscape_rarity':False,
 'source_record_counts':{'tomb_catalogue_rows':len(tombs),'cave_catalogue_rows':len(caves),'cave_cluster_rows':sum(c['row_kind']=='cluster' for c in caves),'cave_scope':'canonical caves.csv only; phase4 supplementary11 rows not imported'},
 'E2_complete_status':dict(Counter(x['full_status'] for x in out if x['entry']==2)),
 'E26_complete_ancient_status':dict(Counter(x['full_ancient_status'] for x in out if x['entry']==26)),
 'E26_documentary_cave_aspect_codes':dict(Counter(direct_cave_aspect(c) for c in caves)),
 'documentary_non_E_codes':[{'record':c['cave_id'],'facing':c['opening_facings'],'locator':c['source_records'],'phase':'not established'} for c in caves if direct_cave_aspect(c)=='documentary_non_E_code'],
 'hashes':{str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in [tomb_path,cave_path,ROOT/'PREDICATES.md']},
 'no_false_exclusions':'Survey silence, old tomb dates, modern orientation without ancient phase, blocked openings and incomplete groups do not exclude whole sites.'
}
dump('result.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ['documentary_non_E_codes','hashes']},indent=2))
