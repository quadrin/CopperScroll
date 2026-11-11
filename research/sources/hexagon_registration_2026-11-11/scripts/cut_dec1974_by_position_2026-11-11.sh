#!/bin/bash
# Cuts three full-size windows from HEXAGON tiles of 1 December 1974, at positions calculated from latitude and longitude
# with the transforms of 11 November 2026 (hexagon_1974_transforms_2026-11-11.json):
#   Nebi Musa (strip F017 tile b), Tell Iktanu and the Umm Hadhar hill (strip A017 tile e).
# Run in the Mac Terminal:  bash "<path>/cut_dec1974_by_position_2026-11-11.sh"
# It uses the tiles in ~/Downloads/hexwin. If a tile is not there, it copies it from the bucket.
set -e
D="$HOME/Downloads/hexwin"; mkdir -p "$D"; cd "$D"
OUT=$(ls -d "$HOME/Library/CloudStorage/GoogleDrive-"*"/My Drive/Copper Scroll/08 Working files/hexagon windows 2026-11-10" | head -1)
[ -d venv ] || python3 -m venv venv
. venv/bin/activate
pip -q install tifffile imagecodecs numpy pillow
for S in D3C1209-200214F017_b D3C1209-200214A017_e; do
  T="$S.tif"; A="${S%_*}"
  [ -f "$T" ] || gsutil cp "gs://<project-bucket>/hexagon/$A/$T" .
done
python3 - "$OUT" <<'PY'
import sys, numpy as np, tifffile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out = sys.argv[1]
def load(n):
    a = tifffile.imread(n)
    if a.ndim == 3: a = a[..., 0] if a.shape[-1] in (3, 4) else a[0]
    print(n, a.shape); return a
def cut(a, tag, x0, y0, w, h, step=1):
    H, W = a.shape[:2]; x0 = max(0, min(x0, W-1)); y0 = max(0, min(y0, H-1))
    b = np.ascontiguousarray(a[y0:y0+h:step, x0:x0+w:step])
    name = f"{out}/{tag}_x{x0}_y{y0}" + ("" if step == 1 else f"_r{step}") + ".jpg"
    Image.fromarray(b).save(name, quality=92); print("saved", name, b.shape)
a = load("D3C1209-200214F017_b.tif")
cut(a, "F017b_dec74_nebi_musa_full", 18450, 13150, 1600, 1600)      # centre tile pixel 19248, 13958 (31.7867 N, 35.4317 E)
del a
a = load("D3C1209-200214A017_e.tif")                                 # stored with south up; turn 180 degrees for north up
cut(a, "A017e_dec74_tell_iktanu_full", 15253, 10521, 1400, 1400)     # centre 31.8192 N, 35.6713 E
cut(a, "A017e_dec74_umm_hadhar_hill_full", 14999, 16341, 1400, 1400) # centre 31.8630 N, 35.6754 E
PY
echo "Done. The windows are in: $OUT"
