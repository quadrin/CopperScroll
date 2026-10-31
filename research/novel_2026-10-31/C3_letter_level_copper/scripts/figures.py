"""C3 figures, written to SP/products/C3 only (never to the repository). Made after the confirmatory run.
1. c3_heights_III_I.png: per-letter class-normalised height, copper (frozen measure) and drawing, by line, columns III and I.
2. c3_overlay_cut07_cut08.jpg: RCT frames of cuts 7 and 8 at 1/4 scale with the mapped W2F centres and the measured copper
   extents (bar length = measured extent; bar centred on the mapped centre, position approximate)."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from c3lib import PROD, A2DIR
sys.path.insert(0, A2DIR)
from common import full_cached  # A2 cache, read only

BLUE, ORANGE, INK, MUTED = "#2a78d6", "#eb6834", "#222222", "#888888"
R = list(csv.DictReader(open("../out/letters_measured.csv", encoding="utf-8")))
for r in R:
    for k in ("l", "cut"):
        r[k] = int(r[k])
    for k in ("h_rel_cu", "h_rel_dr", "x88", "y88", "ext_ALL", "lh88"):
        r[k] = float(r[k]) if r[k] not in ("", "nan") else np.nan

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
rng = np.random.default_rng(1)
for ax, col, title in ((axes[0], "III", "Column III (test; cuts 7, 8)"), (axes[1], "I", "Column I (control; cuts 2, 3, 4)")):
    S = [r for r in R if r["col_roman"] == col and np.isfinite(r["h_rel_cu"])]
    ax.axvspan(6.5, 7.5, color="#eeeeee", zorder=0)
    ax.text(7, 1.85, "line 7\nexcluded", ha="center", va="top", fontsize=8, color=MUTED)
    for key, off, colr, mk, lab in (("h_rel_cu", -0.15, BLUE, "o", "copper (frozen measure)"),
                                    ("h_rel_dr", 0.15, ORANGE, "^", "drawing (Puech facsimile, W2F boxes)")):
        x = np.array([r["l"] for r in S]) + off + rng.uniform(-0.06, 0.06, len(S))
        y = np.array([r[key] for r in S])
        ax.scatter(x, y, s=22, marker=mk, color=colr, edgecolor="white", linewidth=0.6, alpha=0.85, label=lab, zorder=3)
        for rngl, x0, x1 in ((range(1, 7), 0.6, 6.4), (range(8, 14), 7.6, 13.4)):
            v = [r[key] for r in S if r["l"] in rngl]
            if v:
                m = float(np.median(v))
                ax.plot([x0, x1], [m, m], color=colr, lw=2, zorder=4)
                dy = 0.035 if key == "h_rel_dr" else -0.035
                ax.text(x1 + 0.05, m + dy, f"{m:.2f}", color=colr, fontsize=8, va="center", fontweight="bold")
    ax.set_title(title, fontsize=11, color=INK, loc="left")
    ax.set_xlabel("line", color=INK)
    ax.set_xticks(range(1, 14))
    ax.set_xlim(0.4, 14.2)
    ax.grid(axis="y", color="#e5e5e5", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axes[0].set_ylabel("letter height / line pitch, class-normalised", color=INK)
axes[0].set_ylim(0.3, 1.9)
axes[0].legend(loc="lower left", fontsize=8, frameon=False)
fig.suptitle("Copper contrast III 8-13 vs III 1-6: -0.05 (90 % -0.17 to +0.10); drawing on the same letters +0.13. "
             "Verdict: not identifiable. Lines = region medians.", fontsize=10, color=INK, x=0.01, ha="left")
fig.tight_layout()
fig.savefig(f"{PROD}/c3_heights_III_I.png", dpi=130)

import cv2
panels = []
for cut in (8, 7):  # cut 8 = left part of column III, cut 7 = right part
    g = np.asarray(full_cached(cut, "RCT"))
    s = 0.25
    im = cv2.cvtColor(cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), cv2.COLOR_GRAY2BGR)
    for r in R:
        if r["cut"] != cut or not np.isfinite(r["x88"]):
            continue
        x, y = int(r["x88"] * s), int(r["y88"] * s)
        colr = (214, 120, 42) if r["l"] <= 6 else ((52, 104, 235) if r["l"] >= 8 else (150, 150, 150))  # BGR
        cv2.circle(im, (x, y), 4, colr, 1)
        if np.isfinite(r["ext_ALL"]):
            hl = int(0.5 * r["ext_ALL"] * s)
            cv2.line(im, (x + 7, y - hl), (x + 7, y + hl), colr, 2)
        cv2.putText(im, f"{r['l']}", (x - 14, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.35, colr, 1)
    cv2.putText(im, f"CT{cut} RCT (1/4 scale)", (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    panels.append(im)
h = max(p.shape[0] for p in panels)
panels = [cv2.copyMakeBorder(p, 0, h - p.shape[0], 0, 0, cv2.BORDER_CONSTANT, value=0) for p in panels]
cv2.imwrite(f"{PROD}/c3_overlay_cut08_cut07.jpg", np.hstack(panels), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(os.listdir(PROD))
