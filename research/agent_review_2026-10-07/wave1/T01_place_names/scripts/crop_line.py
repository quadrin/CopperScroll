#!/usr/bin/env python3
"""Crop the page image region containing a keyword (located via tesseract TSV word boxes).
Usage: python3 -I crop_line.py PAGE KEYWORD OUTPNG"""
import subprocess, sys
from PIL import Image
page, kw, out = int(sys.argv[1]), sys.argv[2].lower(), sys.argv[3]
root = "agent_review/wave1/T01_place_names/downloads/ocr/img"
img = f"{root}/p{page:03d}.jpg"
tsv = subprocess.run(["tesseract", img, "stdout", "--psm", "3", "tsv"], capture_output=True, text=True).stdout
ys = []
for line in tsv.splitlines()[1:]:
    f = line.split("\t")
    if len(f) >= 12 and kw in f[11].lower():
        ys.append(int(f[7]))
im = Image.open(img)
w, h = im.size
if not ys:
    print("keyword not found; saving full page"); im.save(out); sys.exit()
y = ys[0]
im.crop((100, max(0, y - 160), w, min(h, y + 220))).save(out)
print("found at y", ys)
