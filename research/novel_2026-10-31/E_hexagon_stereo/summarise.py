"""Summarise the confirmatory run (results/confirm_JUN74_*.json + stdout log) into one CSV,
applying the frozen counting rule (>= 50 % of expected 30 m cells valid and >= 300 B cells)."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "results")
logd = {}
for line in open(os.path.join(R, "confirm_JUN74_stdout.log")):
    if line.startswith("{"):
        j = json.loads(line[:line.rindex("}") + 1])
        logd[j["zone"]] = j
rows = []
for z in ["QUMRAN", "QELT", "KIDRON", "JERICHO_OUT"]:
    p = os.path.join(R, f"confirm_JUN74_{z}.json")
    if not os.path.exists(p):
        rows.append(dict(zone=z, status="crashed before matching: no SIFT tie points; the forward F014 window lies at frame "
                                        "Y 24536-29104, beyond the frame edge (24668)", counted=False))
        continue
    r = json.load(open(p))
    L = logd[z]
    frac = r["n_cells_in_zone"] / r["zone_cells_expected"]
    counted = frac >= 0.5 and r["n_eval_B"] >= 300
    row = dict(zone=z, status="run", valid_cell_frac=round(frac, 3), counted=counted, n_eval_B=r["n_eval_B"],
               nmad_B_m=round(r["nmad_B_zone"], 2), median_B_m=round(r["median_B_zone"], 2), rmse_B_m=round(r["rmse_B_zone"], 2),
               nmad_A_fit_m=round(r["nmad_A_fit"], 2), m_per_disp_px=round(r["m_per_disp_px"], 3),
               y_resid_nmad_px=round(r["geo"]["y_resid_nmad_px"], 2))
    for k, v in L["nmad_B_zone_by_slope"].items():
        row["nmad_slope_" + k.replace("-", "_")] = round(v, 2)
    for k, v in L["n_B_zone_by_slope"].items():
        row["n_slope_" + k.replace("-", "_")] = v
    row.update(pass_target_2p5m=r["pass_precision"], n_clusters=len(r["clusters"]),
               clusters_interpretable=bool(r["pass_precision"] and counted))
    rows.append(row)
keys = []
for r in rows:
    for k in r:
        if k not in keys:
            keys.append(k)
with open(os.path.join(R, "summary_confirm_JUN74.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, keys)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(open(os.path.join(R, "summary_confirm_JUN74.csv")).read())
