"""Shared helpers for direction E (HEXAGON 1974 stereo).

- All bucket reads go through hexview.py (SP/tools/hexview, SHA-256 56b21cb0...).
- HEXCOG_PROTECTED is set to protected_boxes.json (this folder) before any read; hexview
  refuses windows that overlap a protected box. --allow-protected is never used.
- Every overview/window read is appended to masking_log.csv (committed).
"""
import csv
import datetime as dt
import json
import os
import sys

import numpy as np

SP = "/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad"
WORK = os.path.join(SP, "E_work")
PROD = os.path.join(SP, "products", "E")
HERE = os.path.dirname(os.path.abspath(__file__))
PROT = os.path.join(HERE, "protected_boxes.json")  # committed; HEXCOG_PROTECTED points here
LOG = os.path.join(HERE, "masking_log.csv")
GLO = os.path.join(WORK, "dl_glo30", "glo30_N31_E035.tif")
WC = os.path.join(WORK, "dl_glo30", "wc2021_N30E033.tif")
os.environ["HEXCOG_PROTECTED"] = PROT
os.environ.setdefault("OMP_NUM_THREADS", "2")
sys.path.insert(0, os.path.join(SP, "tools", "hexview"))
import hexview as hv  # noqa: E402

LOG_FIELDS = ["utc", "item", "tile", "x0", "y0", "x1", "y1", "scale", "purpose", "masked_boxes_in_tile", "note"]


def load_prot():
    if os.path.exists(PROT):
        with open(PROT) as fh:
            return json.load(fh)
    return []


def save_prot(entries):
    with open(PROT, "w") as fh:
        json.dump(entries, fh, indent=1)


def add_prot(item, tile, bx, note):
    e = load_prot()
    e.append({"item": item, "tile": tile, "box": [int(v) for v in bx], "note": note})
    save_prot(e)


def prot_boxes(item, tile):
    if item in ("", "-"):
        return []
    stem = hv.resolve(item)
    return [p["box"] for p in load_prot() if p["item"] in stem and p.get("tile") in (None, tile)]


def log_read(item, tile, x0, y0, x1, y1, scale, purpose, note=""):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as fh:
        w = csv.DictWriter(fh, LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow(dict(utc=dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), item=item, tile=tile, x0=x0, y0=y0, x1=x1, y1=y1,
                        scale=scale, purpose=purpose, masked_boxes_in_tile=json.dumps(prot_boxes(item, tile)), note=note))


def read_overview(item, tile, scale=1 / 32, purpose="coarse registration (code only)"):
    """Overview of a whole tile in STORED orientation. Protected boxes are not read:
    the tile is read in strips around them, and the boxes are returned blank (valid=False)."""
    stem, rec, t = hv.tile_rec(item, tile)
    W, H = t["width"], t["height"]
    oh, ow = round(H * scale), round(W * scale)
    out = np.zeros((oh, ow), np.uint8)
    valid = np.zeros((oh, ow), bool)
    boxes = prot_boxes(stem, tile)
    if not boxes:
        a = hv.box(stem, tile, 0, 0, W, H, scale=scale)
        out[:a.shape[0], :a.shape[1]] = a[:oh, :ow]
        valid[:a.shape[0], :a.shape[1]] = True
        log_read(stem, tile, 0, 0, W, H, scale, purpose)
    else:
        # read a grid of blocks (aligned to 1/scale px) that avoid all boxes
        step = 4096  # full-res px per block
        for y0 in range(0, H, step):
            for x0 in range(0, W, step):
                x1, y1 = min(W, x0 + step), min(H, y0 + step)
                if any(x0 < b[2] and x1 > b[0] and y0 < b[3] and y1 > b[1] for b in boxes):
                    continue
                a = hv.box(stem, tile, x0, y0, x1, y1, scale=scale)
                oy, ox = round(y0 * scale), round(x0 * scale)
                hh, ww = min(a.shape[0], oh - oy), min(a.shape[1], ow - ox)
                out[oy:oy + hh, ox:ox + ww] = a[:hh, :ww]
                valid[oy:oy + hh, ox:ox + ww] = True
        log_read(stem, tile, 0, 0, W, H, scale, purpose, note="read in blocks avoiding protected boxes")
    return out, valid, rec.get("stored_orientation"), (W, H)
