#!/usr/bin/env python3
"""Heatmap of region posteriors per entry: stated-confidence prior (M0) vs itinerary-only (M1) vs joint (M3).
Run: python3 -I plot_regions.py ../outputs"""
import csv, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

out = sys.argv[1]
REG = ['NORTH', 'WEST', 'JER', 'SOUTH', 'DESERT', 'QUMRAN', 'JERICHO']
LAB = {'NORTH': 'North (Samaria, Beth Shean)', 'WEST': 'West (Beth Horon)', 'JER': 'Jerusalem',
       'SOUTH': 'South (Natuf, Tekoa-Herodium)', 'DESERT': 'Desert (Buqeia, Hyrcania, Mar Saba)',
       'QUMRAN': 'Qumran / NW Dead Sea', 'JERICHO': 'Jericho oasis'}
ramp = ['#ffffff', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']
cmap = LinearSegmentedColormap.from_list('seqblue', ramp)
panels = [('M0_prior', 'Stated-confidence prior (no sequence, no names)'),
          ('M1_itinerary_fitted', 'Itinerary term only (fitted weight)'),
          ('M3_joint_fitted', 'Joint: itinerary + repeated names (tempered)')]
fig, axes = plt.subplots(len(panels), 1, figsize=(16, 8.6), sharex=True)
for ax, (name, title) in zip(axes, panels):
    rows = list(csv.DictReader(open(os.path.join(out, f'posterior_{name}.csv'))))
    M = [[float(r[f'R_{g}']) for r in rows] for g in REG]
    im = ax.imshow(M, aspect='auto', cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
    ax.set_yticks(range(len(REG)))
    ax.set_yticklabels([LAB[g] for g in REG], fontsize=8, color='#333333')
    ax.set_title(title, fontsize=10, loc='left', color='#111111')
    for b in (19.5, 35.5, 56.5):  # block boundaries after 19 (index 19 = entry 19 incl. 12a), 35, 56
        ax.axvline(b, color='#888888', lw=1, ls='--')
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
ents = [r['entry'] for r in rows]
axes[-1].set_xticks(range(len(ents)))
axes[-1].set_xticklabels(ents, fontsize=7, rotation=90, color='#333333')
axes[-1].set_xlabel('Entry (scroll order; dashed lines = blocks A | B | C | D)', fontsize=9, color='#333333')
cb = fig.colorbar(im, ax=axes, fraction=0.015, pad=0.01)
cb.set_label('Posterior probability of region', fontsize=9)
cb.outline.set_visible(False)
fig.suptitle('Copper Scroll joint placement model v0: where each entry is placed, by region', x=0.01, ha='left',
             fontsize=12, color='#111111')
fig.savefig(os.path.join(out, 'region_posteriors.png'), dpi=130, bbox_inches='tight', facecolor='white')
print('saved')
