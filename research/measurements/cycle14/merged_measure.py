"""Recalculate a dimensional counterfactual, never a surveyed candidate footprint."""
import json
from pathlib import Path
base=Path(__file__).resolve().parent
inputs=json.loads((base/'merged_measure_input.json').read_text())
w=inputs['rectangle_width_m']
rows=[]
for count in inputs['cubit_counts']:
 lo,hi=[round(count*c,6) for c in inputs['cubit_range_m']]
 rows.append({'cubits':count,'distance_m':[lo,hi],
 'inside_from_west_side_x_m':[lo,hi],
 'inside_from_east_side_x_m':[round(w-hi,6),round(w-lo,6)],
 'outside_west_x_m':[-hi,-lo],
 'outside_east_x_m':[round(w+lo,6),round(w+hi,6)],
 'fits_within_assumed_width':hi<=w,
 'both_sides_inside_bands_overlap':max(lo,w-hi)<=min(hi,w-lo)})
result={'kind':'unsurveyed_dimensional_counterfactual','axes':inputs['axes'],
'rows':rows,'archaeological_points_tested':0,'qualifying_archaeological_hits':None,
'not_a_coordinate':True,'limitations':inputs['limitations']}
(base/'merged_measure_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
