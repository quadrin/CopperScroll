#!/bin/bash
# Cuts four full-size windows from CORONA mission 1101-2, 26 September 1967 (strips DF041 and DF040, tile d).
# The window positions are from the overviews (reduced 12 times); a window can be some hundreds of pixels off.
# It uses the tiles that cut_may1978_and_corona_overviews_2026-11-11.sh put in ~/Downloads/corona1967.
# Run in the Mac Terminal:  bash "<path>/cut_corona1967_windows_2026-11-11.sh"
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
cut(a, "DF041d_sep67_jericho_oasis_and_scarp_full", 16500, 1500, 5500, 4000)     # Jericho oasis near x19200, y3000
cut(a, "DF041d_sep67_plain_deir_hajla_jordan_full", 20500, 4300, 3000, 3000)     # plain south-east of Jericho, the Jordan
cut(a, "DF041d_sep67_east_bank_kafrein_full", 25000, 1300, 3600, 3600)           # fields and wadi mouth east of the Jordan
del a
a = load("DS1101-2168DF040_40/**/*_d.tif")
cut(a, "DF040d_sep67_oasis_north_of_jericho_full", 19500, 3800, 3600, 3200)      # oasis west of the Jordan, north of the Jericho frame
PY
echo "Done. The windows are in: $COUT"
