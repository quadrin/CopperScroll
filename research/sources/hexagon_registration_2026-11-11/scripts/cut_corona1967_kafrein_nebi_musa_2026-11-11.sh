#!/bin/bash
# Cuts two more full-size windows from CORONA mission 1101-2, 26 September 1967, strip DF041, tile d.
# The positions are from the transform of 11 November 2026 (341 blocks against HEXAGON 1 Dec 1974, rms 16 m west of the Jordan;
# east of the Jordan the transform is extended, error possibly 100 to 200 m).
# It uses the tile that is in ~/Downloads/corona1967.
# Run in the Mac Terminal:  bash "<path>/cut_corona1967_kafrein_nebi_musa_2026-11-11.sh"
set -e
DR=$(ls -d "$HOME/Library/CloudStorage/GoogleDrive-"*"/My Drive/Copper Scroll" | head -1)
COUT="$DR/08 Working files/corona windows 2026-11-11"; mkdir -p "$COUT"
. "$HOME/Downloads/hexwin/venv/bin/activate"
cd "$HOME/Downloads/corona1967"
python3 - "$COUT" <<'PY'
import sys, glob, numpy as np, tifffile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out = sys.argv[1]
def load(pat):
    f = sorted(glob.glob(pat, recursive=True))[0]; a = tifffile.imread(f)
    if a.ndim == 3: a = a[..., 0] if a.shape[-1] in (3, 4) else a[0]
    print(f, a.shape); return a
def cut(a, tag, x0, y0, w, h):
    H, W = a.shape[:2]; x0 = max(0, min(x0, W-1)); y0 = max(0, min(y0, H-1))
    b = np.ascontiguousarray(a[y0:y0+h, x0:x0+w]); name = f"{out}/{tag}_x{x0}_y{y0}.jpg"
    Image.fromarray(b).save(name, quality=92); print("saved", name, b.shape)
a = load("DS1101-2168DF041_41/**/*_d.tif")
cut(a, "DF041d_sep67_kafrein_rameh_iktanu_full", 26900, 4300, 2800, 3300)   # Kafrein dam near x28790 y5435; Tell er-Rameh x27320 y6520; Tell Iktanu x28490 y7050
cut(a, "DF041d_sep67_nebi_musa_full", 17200, 6300, 1400, 1400)             # Nebi Musa near x17890 y6975
PY
echo "Done. The windows are in: $COUT"
