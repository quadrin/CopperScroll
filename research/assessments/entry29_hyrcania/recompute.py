"""Reproduce the conditional page-up offset; supplies no geographic registration."""
import json
from pathlib import Path
j = json.loads(Path(__file__).with_name("geometry.json").read_text())
a,b = j["scale"]["endpoints_px"]
s = j["scale"]["length_m"] / ((b[0]-a[0])**2+(b[1]-a[1])**2)**0.5
d = [24*c for c in j["offset_model"]["unit_range_m"]]
r = {"scale_metres_per_pixel":s,"conditional_offsets_m":d,"anchors":{}}
for name in ["pool_centre_proxy_px","northmost_rim_proxy_px"]:
    x,y=j["anchors"][name]
    r["anchors"][name]=[[x,y-v/s] for v in d]
r["datum_separation_page_up_m"]=abs(j["anchors"]["pool_centre_proxy_px"][1]-j["anchors"]["northmost_rim_proxy_px"][1])*s
r["manual_pick_uncertainty_metres"]=j["anchors"]["anchor_precision_px"]*s
print(json.dumps(r,indent=2))
