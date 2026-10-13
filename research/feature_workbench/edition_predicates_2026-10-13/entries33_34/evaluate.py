"""Reproduce the bounded E33/E34 data-sufficiency and metric-branch audit.

No row-position proxy or missing column becomes an archaeological contradiction.
This is exploratory; the raw rows are source records, not independent sites.
"""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WATER = REPO / "research/regional/water_systems/water.csv"
FEATURES = REPO / "research/regional/haesi_features/features.csv"

def main():
    spec = json.loads((HERE / 'branch_spec.json').read_text())
    with (WATER).open() as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        water = list(reader)
    missing = [x for x in ['road_feature_id', 'road_conduit_relation',
                          'treasury_house_id', 'ahiyah_house_id',
                          'ahim_reference_id', 'east_of_treasury',
                          'treasury_east_of_reference',
                          'ancient_relationship_phase'] if x not in fields]
    with (FEATURES).open() as stream:
        feature_rows = list(csv.DictReader(stream))
    road_observations = [dict((k, r[k]) for k in
                        ['report_id', 'url', 'pages', 'site_name',
                         'feature_type', 'period_as_given', 'quote'])
                        for r in feature_rows if 'channel' in r['feature_type']
                        and 'street' in r['period_as_given'].lower()]
    result = {
        'claim': spec['scope'],
        'exposure': spec['exposure'],
        'metric_sensitivity_m': {
            str(c): round(17*c, 3) for c in spec['parameter_policy']['cubit_m_sensitivity']
        },
        'metric_warning': 'These lengths belong to each selected axis/path branch. A linear length is not automatically a depth.',
        'source_water_rows': len(water),
        'source_aqueduct_rows': sum(r['type'] == 'aqueduct' for r in water),
        'activity_count_warning': 'Raw coding/coverage diagnostics only; neither independent feature counts nor outcome/identification progress.',
        'required_E33_relation_columns_not_in_existing_table': missing,
        'E33_table_result': 'unknown: the table cannot score the full road/house/reference chain',
        'E33_existing_road_drain_source_observation': road_observations,
        'road_drain_qualification': 'Source states road/drain relation only. Hydraulic noun compatibility, treasury identity, second reference, east-of relations and same-phase ties remain unknown.',
        'E34_existing_inventory_result': 'unknown: no typed marker inscription, ancient valley association, stone datum and seventeen-cubit target relation have been supplied',
        'outcome': spec['outcome'],
        'reopening_conditions': [
            'A corrected edition-branch coding or direct ancient-text reading can change the branch predicates',
            'An original report identifies the Treasury/reference house and links it to a same-phase road/conduit relationship',
            'An original report locates a retained type of valley stone/monument with phase, inscription or slope context and surveyed local target datum'
        ],
        'source_sha256': {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in [HERE/'branch_spec.json', WATER, FEATURES]}
    }
    (HERE/'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'outcome': result['outcome'], 'changes': spec['changes']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
