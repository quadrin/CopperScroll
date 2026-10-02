"""Recompute manual source-plan offsets; no geographic coordinate registration."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
samples=[
 {'phase':3,'figure':20,'pdf_page':30,'printed_page':284,'scale_px':[689,804],'north_pool_longwalls_x':[523,679],'south_pool_longwalls_x':[306,459],'line_x':499,'visible_finite_y':[650,676],'line_identity':'central aqueduct branch, published reconstructed plan','qualifying_channel':True},
 {'phase':5,'figure':21,'pdf_page':31,'printed_page':285,'scale_px':[279,394],'north_pool_longwalls_x':[489,643],'south_pool_longwalls_x':[270,425],'line_x':463,'visible_finite_y':[652,676],'line_identity':'central aqueduct branch, published reconstructed plan','qualifying_channel':True},
 {'phase':6,'figure':22,'pdf_page':32,'printed_page':286,'scale_px':[314,432],'north_pool_longwalls_x':[523,679],'south_pool_longwalls_x':[306,459],'line_x':511,'visible_finite_y':[650,676],'line_identity':'central line; channel identity unresolved','qualifying_channel':False}]
# All picks in full-page 2x fitz raster. Point ±3px, combined separation ±6px;
# scale endpoint combined uncertainty ±4px. This is manual digitization only,
# not surveyed archaeological accuracy, wall-phase uncertainty or raster distortion.
for s in samples:
 scale=s['scale_px'][1]-s['scale_px'][0]
 s['metres_per_pixel']=10/scale
 s['picking_uncertainty_px']=3
 s['stress_picking_uncertainty_px']=5
 s['wall_endpoints_px']={pool:[[[x,s['visible_finite_y'][0]],[x,s['visible_finite_y'][1]]] for x in s[f'{pool}_pool_longwalls_x']] for pool in ['north','south']}
 s['sample_line_endpoints_px']=[[s['line_x'],s['visible_finite_y'][0]],[s['line_x'],s['visible_finite_y'][1]]]
 s['offsets']=[]
 for pool in ['north','south']:
  for j,x in enumerate(s[f'{pool}_pool_longwalls_x']):
   d=abs(x-s['line_x']);lo=max(0,d-6)*10/(scale+4);hi=(d+6)*10/(scale-4)
   stress_lo=max(0,d-10)*10/(scale+6);stress_hi=(d+10)*10/(scale-6)
   s['offsets'].append({'stress_interval_m':[round(stress_lo,3),round(stress_hi,3)],'stress_overlap_24_cubits':stress_lo<=14.4 and stress_hi>=9.6,'stress_overlap_27_cubits':stress_lo<=16.2 and stress_hi>=10.8,'pool':pool,'wall_index':j,'pixel_distance':d,'metres':round(d*10/scale,3),'manual_interval_m':[round(lo,3),round(hi,3)],'overlap_24_cubits':lo<=14.4 and hi>=9.6,'overlap_27_cubits':lo<=16.2 and hi>=10.8})
result={'source':'Monika Trümper 2018, printed pp.284–286, Figs20–22','raster':'fitz Matrix(2,2), full page','north_direction':'right in Figs20–22','unit_sensitivity':{'24_cubits_m':[9.6,14.4],'27_cubits_m':[10.8,16.2],'cubit_m':[0.4,0.6]},'scope':'perpendicular distance from two visible long-wall inner-edge stubs to central inter-pool route; projections must fall within visible finite stubs; no test of all channels, chainage, vertical distance, or arbitrary points on extended walls','samples':samples}
(ROOT/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
for s in samples:
 print('phase',s['phase'],[(q['pool'],q['wall_index'],q['metres'],q['manual_interval_m'],q['overlap_24_cubits'],q['overlap_27_cubits']) for q in s['offsets']])
