#!/usr/bin/env python3
"""Reproduce recorded Hyrcania EN offsets and WGS84 withheld residual.
Uses the recorded geographic points; does not rerun the datum conversion.
No new controls, accepted geographic fit, or source inspection result.
"""
import json, math
from pathlib import Path

def inverse_wgs84(lon1, lat1, lon2, lat2):
    # Vincenty inverse on WGS84. This short, non-antipodal pair converges.
    a, f = 6378137.0, 1 / 298.257223563
    b = a * (1 - f)
    u1, u2 = [math.atan((1-f)*math.tan(math.radians(v))) for v in (lat1, lat2)]
    L = math.radians(lon2-lon1)
    lam = L
    for _ in range(100):
        ss = math.hypot(math.cos(u2)*math.sin(lam), math.cos(u1)*math.sin(u2)-math.sin(u1)*math.cos(u2)*math.cos(lam))
        if ss == 0:
            return 0.0
        cs = math.sin(u1)*math.sin(u2)+math.cos(u1)*math.cos(u2)*math.cos(lam)
        sig = math.atan2(ss, cs)
        sa = math.cos(u1)*math.cos(u2)*math.sin(lam)/ss
        c2a = 1-sa*sa
        c2sm = cs-2*math.sin(u1)*math.sin(u2)/c2a if c2a else 0
        C = f/16*c2a*(4+f*(4-3*c2a))
        prev = lam
        lam = L+(1-C)*f*sa*(sig+C*ss*(c2sm+C*cs*(-1+2*c2sm*c2sm)))
        if abs(lam-prev)<1e-13:
            break
    else:
        raise ValueError('Vincenty did not converge')
    u2coef = c2a*(a*a-b*b)/(b*b)
    A=1+u2coef/16384*(4096+u2coef*(-768+u2coef*(320-175*u2coef)))
    B=u2coef/1024*(256+u2coef*(-128+u2coef*(74-47*u2coef)))
    ds=B*ss*(c2sm+B/4*(cs*(-1+2*c2sm*c2sm)-B/6*c2sm*(-3+4*ss*ss)*(-3+4*c2sm*c2sm)))
    return b*A*(sig-ds)

root=Path(__file__).resolve().parent
d=json.loads((root/'hyrcania_baseline.json').read_text())
p,t,w=d['source_plan'],d['transform'],d['withheld_check']
q=[p['station44_dam_px'][0]-p['fort_symbol_px'][0],p['fort_symbol_px'][1]-p['station44_dam_px'][1]]
scale=p['scale_bar_m']/math.dist(*p['scale_bar_endpoints_px'])
en=[scale*sum(a*b for a,b in zip(q,t[key])) for key in ['east_vector','north_vector']]
assert all(abs(a-b)<1e-8 for a,b in zip(en,w['local_predicted_EN_m']))
pred,guide=w['predicted_station44_wgs84'],w['converted_guide_point']
residual=inverse_wgs84(pred['longitude'],pred['latitude'],guide['longitude'],guide['latitude'])
assert abs(residual-w['residual_m'])<0.01
out={
  'baseline_commit':'bb2fde4c76dbbe34b4c7345646acee049e875229',
  'status':'reproduction and conditional quantization budget; no new source or control',
  'scale_m_per_pixel':scale,
  'reproduced_predicted_local_EN_m':en,
  'reproduced_withheld_residual_m':residual,
  'datum_conversion_reexecuted':False,
  'conditional_100m_grid_notation_budget':{
    'rounding_max_displacement_grid_m':math.sqrt(2)*50,
    'truncation_max_displacement_grid_m':math.sqrt(2)*100,
    'residual_minus_rounding_diagonal_approx_m':residual-math.sqrt(2)*50,
    'residual_minus_truncation_diagonal_approx_m':residual-math.sqrt(2)*100,
    'interpretation':'Even a full rounding/truncation cell diagonal alone is smaller than the residual. These are approximate grid-distance budgets; actual cell location, projected scale and datum operation require verified conversion.'
  },
  'source_relative_pick_uncertainty_only_m':{'HY-pool-N':8*50/143,'HY-pool-S':8*50/143,'HY-pool-extra-S':10*50/143,'HY-S':12*50/143,'HY-F':12*50/143},
  'limits':['Existing map symbol, summit anchor, grid units, feature identity and coordinate conversion assumptions retained.',
            'Unknown source/imagery/map-generalization error prevents a statistical acceptance bound.',
            'Pick uncertainty in metres excludes scale, scan distortion and geographic registration error.'],
  'kpi_effect':{'new_primary_targets':0,'new_candidate_tests':0,'question_closures':0}
}
(root/'hyrcania_registration_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
