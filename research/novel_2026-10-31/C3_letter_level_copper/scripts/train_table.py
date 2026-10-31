"""C3 training table (EXPLORATORY material; training cuts 6, 11, 16, 17, 18, 21, 22 only).
Measures the training letters with the final parameters (measure_set.FINAL), reports the reliability and validity
values that set the expectation for the frozen gate, and writes the frozen class-median table used to class-normalise
copper heights in the confirmatory run.
Outputs: out/train_letters.csv, out/class_medians.json, out/train_summary.json."""
import json, csv
import numpy as np
from measure_set import FINAL, load_placed, measure_rows, class_table, normalise, split_half, class_validity, compression_k, region_contrast

TRAIN = {6, 11, 16, 17, 18, 21, 22}
rows = load_placed("../out/placed_letters.csv", TRAIN)
assert not any(r["cut"] in (2, 3, 4, 7, 8) for r in rows)
meas = measure_rows(rows)
own = [d for d in meas if d["pitch_src"] == "own"]
fb = [d for d in meas if d["pitch_src"] == "fallback"]
tab, allmed = class_table([d for d in meas if d["pitch_src"] != "none"])
normalise(meas, tab, allmed)
k, nk = compression_k([d for d in meas if np.isfinite(d["h_ALL"])], tab, allmed)
summ = dict(params=FINAL, n_placed=len(rows), n_own_pitch=len(own), n_fallback=len(fb),
            n_measured=int(sum(np.isfinite(d["h_ALL"]) for d in meas)),
            split_half_all=split_half(meas), split_half_own=split_half(own), split_half_fallback=split_half(fb),
            split_half_by_cut={str(c): split_half([d for d in meas if d["cut"] == c]) for c in sorted(TRAIN)},
            class_validity=class_validity(meas), compression_k=k, compression_n_classes=nk,
            pitch_over_lh_median=float(np.nanmedian([d["pitch"] / d["lh88"] for d in meas])))
# exploratory: does the copper reproduce the drawing's column contrasts on training columns? (drawing as reference)
cc = {}
for col in sorted(set(d["col_roman"] for d in meas)):
    m = [d for d in meas if d["col_roman"] == col]
    c_cu, b, a = region_contrast(m, "h_rel_cu")
    c_dr, _, _ = region_contrast([d for d in m if np.isfinite(d["h_rel_cu"])], "h_rel_dr")
    cc[col] = dict(copper=c_cu, drawing_same_letters=c_dr, n_before=len(b), n_after=len(a))
summ["training_column_contrasts"] = cc
rob = []
for col in cc:
    for rng in (range(1, 7), range(8, 14)):
        v = np.array([d["h_rel_cu"] for d in meas if d["col_roman"] == col and d["l"] in rng and np.isfinite(d["h_rel_cu"])])
        if len(v) >= 8:
            rob.append(float(1.4826 * np.median(np.abs(v - np.median(v))) / np.median(v)))
summ["robust_sd_rel_within_region_median"] = float(np.median(rob))
json.dump(dict(class_medians=tab, overall_median=allmed, min_n=5, source="training cuts 6,11,16,17,18,21,22; h_ALL"),
          open("../out/class_medians.json", "w"), indent=1, ensure_ascii=False)
json.dump(summ, open("../out/train_summary.json", "w"), indent=1, default=float)
keys = ["uid", "col_roman", "cut", "l", "ref", "word_index", "char_index", "letter", "x88", "y88", "lh88", "n_lights",
        "pitch", "pitch_src", "acpk", "ext_ALL", "ext_T", "ext_B", "h_ALL", "h_T", "h_B", "h_rel_cu", "hp_dr", "h_rel_dr"]
with open("../out/train_letters.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for d in meas:
        w.writerow({k: (round(d[k], 4) if isinstance(d[k], float) else d[k]) for k in keys})
print(json.dumps({k: v for k, v in summ.items() if k != "params"}, indent=1, default=float))
