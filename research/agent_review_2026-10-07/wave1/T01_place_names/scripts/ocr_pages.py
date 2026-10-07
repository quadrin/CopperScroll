#!/usr/bin/env python3
"""Re-OCR the transliteration column of Palmer, SWP Arabic and English Name Lists (1881),
archive.org item surveyofwesternp00conduoft, with tesseract 5 (eng).

Usage: python3 -I ocr_pages.py OUTDIR FIRST_PAGE LAST_PAGE [WORKER_INDEX NWORKERS]
Printed page P is archive.org image /page/n{P+9}.jpg (checked: n349 = printed p. 340).
Pass 1: tesseract --psm 3 TSV to find the x position of the grid-square column (tokens like 'Os', 'Nu').
Pass 2: crop from that column rightwards and OCR with --psm 6 so that grid ref + name + gloss stay on one line.
"""
import os, re, subprocess, sys, urllib.request

ITEM = "surveyofwesternp00conduoft"

def fetch(page, path):
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return
    url = f"https://archive.org/download/{ITEM}/page/n{page+9}.jpg"
    subprocess.run(["curl", "-sSL", "-o", path, url], check=True)

def grid_x(img):
    out = subprocess.run(["tesseract", img, "stdout", "--psm", "3", "tsv"],
                         capture_output=True, text=True).stdout
    xs = []
    for line in out.splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 12:
            continue
        txt = f[11].strip()
        if re.fullmatch(r"[A-Z][a-z]", txt):
            xs.append(int(f[6]))
    if not xs:
        return None
    xs.sort()
    # robust: take the 20th percentile of candidate grid-ref x positions
    return xs[len(xs) // 5]

def main():
    outdir, p1, p2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    wi, nw = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
    from PIL import Image
    imgdir = os.path.join(outdir, "img")
    txtdir = os.path.join(outdir, "txt")
    os.makedirs(imgdir, exist_ok=True)
    os.makedirs(txtdir, exist_ok=True)
    for p in range(p1, p2 + 1):
        if (p - p1) % nw != wi:
            continue
        tpath = os.path.join(txtdir, f"p{p:03d}.txt")
        if os.path.exists(tpath):
            continue
        ipath = os.path.join(imgdir, f"p{p:03d}.jpg")
        try:
            fetch(p, ipath)
            gx = grid_x(ipath)
            im = Image.open(ipath).convert("L")
            w, h = im.size
            x0 = max(0, (gx - 25) if gx else int(w * 0.27))
            cpath = os.path.join(imgdir, f"p{p:03d}_crop.png")
            im.crop((x0, 0, w, h)).save(cpath)
            txt = subprocess.run(["tesseract", cpath, "stdout", "--psm", "6"],
                                 capture_output=True, text=True).stdout
            os.remove(cpath)
            with open(tpath, "w") as fh:
                fh.write(f"### printed page {p}; crop x0={x0}\n" + txt)
            print("done", p, x0, flush=True)
        except Exception as e:
            print("fail", p, e, flush=True)

if __name__ == "__main__":
    main()
