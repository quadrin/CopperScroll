"""Exploratory helper: summarise A2 placement gates and registration fields (numbers only)."""
import json, glob, os, sys
H = os.path.dirname(os.path.abspath(__file__)) + "/a2_reused"
for f in sorted(glob.glob(H + "/place/*.json")):
    P = json.load(open(f))
    print(os.path.basename(f), P["cut"], P["col"], round(P["distinctiveness"], 2), round(P["local"]["median_shift_lh"], 3),
          round(P["scale"], 3), P["rot_deg"], P.get("template_part"))
for c in (2, 3, 4, 6, 7, 8, 11, 16, 17, 18, 21, 22):
    r = json.load(open(f"{H}/reg/reg_cut{c:02d}.json"))
    print(c, r["ref"], r["mask_ref_bbox"], list(r["frames"].keys()),
          {k: (v.get("median_px"), v.get("n_patches")) for k, v in r.get("residual", {}).items()})
