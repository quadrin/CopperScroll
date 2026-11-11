#!/bin/bash
# 1) Cuts four full-size windows from HEXAGON strip D3C1214-200439F007, tile c (5 May 1978), at positions calculated
#    with the transform of 11 November 2026 (registered to the elevation model at preview scale; error approximately 100 m).
# 2) Makes overviews (reduced 12 times) of the CORONA strips DS1101-2168DF040 and DF041 (26 September 1967).
# Run in the Mac Terminal:  bash "<path>/cut_may1978_and_corona_overviews_2026-11-11.sh"
# It needs approximately 3 GB (tile c) and 3 GB (the two CORONA strips) in ~/Downloads.
set -e
DR=$(ls -d "$HOME/Library/CloudStorage/GoogleDrive-"*"/My Drive/Copper Scroll" | head -1)
OUT="$DR/08 Working files/hexagon windows 2026-11-10"
COUT="$DR/08 Working files/corona windows 2026-11-11"; mkdir -p "$COUT"
D="$HOME/Downloads/hexwin"; mkdir -p "$D"; cd "$D"
[ -d venv ] || python3 -m venv venv
. venv/bin/activate
pip -q install tifffile imagecodecs numpy pillow
T="D3C1214-200439F007_c.tif"
if [ ! -f "$T" ]; then
  gsutil cp "gs://<project-bucket>/hexagon/D3C1214-200439F007/$T" . || {
    echo "Bucket copy failed; I take the tile from the Drive archive (2.9 GB)."
    tar -xzf "$DR/06 Imagery/HEXAGON 1978-05-05/D3C1214-200439F007.tgz" --wildcards "*F007_c.tif" 2>/dev/null || tar -xzf "$DR/06 Imagery/HEXAGON 1978-05-05/D3C1214-200439F007.tgz"
    F=$(find . -name "D3C1214-200439F007_c.tif" | head -1); [ "$F" != "./$T" ] && mv "$F" "$T"
  }
fi
python3 - "$OUT" <<'PY'
import sys, numpy as np, tifffile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out = sys.argv[1]
a = tifffile.imread("D3C1214-200439F007_c.tif")
if a.ndim == 3: a = a[..., 0] if a.shape[-1] in (3, 4) else a[0]
print(a.shape)
def cut(tag, x0, y0, w, h, step=1):
    H, W = a.shape[:2]; x0 = max(0, min(x0, W-1)); y0 = max(0, min(y0, H-1))
    b = np.ascontiguousarray(a[y0:y0+h:step, x0:x0+w:step])
    name = f"{out}/{tag}_x{x0}_y{y0}" + ("" if step == 1 else f"_r{step}") + ".jpg"
    Image.fromarray(b).save(name, quality=92); print("saved", name, b.shape)
cut("F007c_may78_jericho_palaces_quruntul_full", 23000, 1500, 4200, 6200)   # Tell es-Sultan 25575/2845, Tulul 25042/5733, Birket Musa 25490/6035, Quruntul 23743/2633
cut("F007c_may78_nebi_musa_full", 24700, 13600, 1700, 1700)                 # centre 25536/14445
cut("F007c_may78_deir_hajla_full", 32000, 7700, 2000, 2000)                 # centre 32999/8712 (cloud is possible)
cut("F007c_may78_qumran_feshkha_full", 28000, 19000, 3000, 5600)            # Qumran 29537/20113, Feshkha 29117/23630 (thin cloud)
PY
# CORONA overviews
C="$HOME/Downloads/corona1967"; mkdir -p "$C"; cd "$C"
for S in DS1101-2168DF040_40 DS1101-2168DF041_41; do
  [ -d "$S" ] || { mkdir "$S"; tar -xzf "$DR/06 Imagery/CORONA 1967/$S.tgz" -C "$S"; }
done
python3 - "$COUT" <<'PY'
import sys, glob, os, tifffile, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out = sys.argv[1]
for f in sorted(glob.glob("DS1101-2168DF04[01]_*/**/*.tif", recursive=True)):
    a = tifffile.imread(f)
    if a.ndim == 3: a = a[..., 0] if a.shape[-1] in (3, 4) else a[0]
    b = np.ascontiguousarray(a[::12, ::12]); n = os.path.splitext(os.path.basename(f))[0]
    Image.fromarray(b).save(f"{out}/{n}_overview_r12.jpg", quality=90); print("saved", n, a.shape)
PY
echo "Done. HEXAGON windows: $OUT ; CORONA overviews: $COUT"
