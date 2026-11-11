#!/bin/bash
# Cuts one full-size window at Shunat Nimrin (South Shuna) from HEXAGON 1 December 1974, strip A017, tile e.
# Purpose: control for CORONA 1967 there, and the place of Tell Nimrin (published point 31.9003 N, 35.6247 E).
# The position is from the Kafrein transform of tile A017e, extended 5 km to the north (error possibly 300 m),
# thus the window is large. Strip F017 does not include this place. The place is near the edge of tile A017e:
# if the script prints "outside the tile", tell Claude the tile size that it prints.
# Run in the Mac Terminal:  bash "<path>/cut_dec1974_shunat_nimrin_2026-11-11.sh"   (not tested)
set -e
D="$HOME/Downloads/hexwin"; mkdir -p "$D"; cd "$D"
OUT=$(ls -d "$HOME/Library/CloudStorage/GoogleDrive-"*"/My Drive/Copper Scroll/08 Working files/hexagon windows 2026-11-10" | head -1)
[ -d venv ] || python3 -m venv venv
. venv/bin/activate
pip -q install tifffile imagecodecs numpy pillow
S=D3C1209-200214A017_e; T="$S.tif"; A="${S%_*}"
[ -f "$T" ] || gsutil cp "gs://<project-bucket>/hexagon/$A/$T" .
python3 - "$OUT" "$T" <<'PY'
import sys, numpy as np, tifffile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out, n = sys.argv[1], sys.argv[2]
a = tifffile.imread(n)
if a.ndim == 3: a = a[..., 0] if a.shape[-1] in (3, 4) else a[0]
H, W = a.shape[:2]; print(n, "tile size (width, height):", W, H)
x0, y0, w, h = 19000, 19200, 4000, 4000          # Tell Nimrin calculated near x21020, y21205
if x0 >= W or y0 >= H: sys.exit("outside the tile")
b = np.ascontiguousarray(a[y0:y0+h, x0:x0+w][::-1, ::-1])   # turned 180 degrees, as the other A017e windows
name = f"{out}/A017e_dec74_shunat_nimrin_full_x{x0}_y{y0}.jpg"
Image.fromarray(b).save(name, quality=92); print("saved", name, b.shape)
PY
echo "Done."
