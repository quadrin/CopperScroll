"""Fetch USC 1988 frames through hexview.py and log every read (C2, 31 Oct 2026).

Images are written only to SP/products/C2 or SP/C2work/cache (never to the repository).
Every call appends one line to SP/C2work/exposure_log.txt: time, item, box, scale, purpose.

CLI:
  python3 -I fetch.py overview ITEM SCALE PURPOSE...
  python3 -I fetch.py box ITEM X0 Y0 X1 Y1 SCALE PURPOSE...
"""
import os, sys, time

SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
sys.path.insert(0, SP + '/tools/hexview')
import numpy as np
import hexview as hv  # noqa: E402

PROD = SP + '/products/C2'
CACHE = SP + '/C2work/cache'
LOG = SP + '/C2work/exposure_log.txt'
os.makedirs(PROD, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)


def log(msg):
    with open(LOG, 'a') as fh:
        fh.write(time.strftime('%H:%M:%SZ', time.gmtime()) + ' ' + msg + '\n')


def item_name(cut, light):
    return f'usc:DSS_3Q15_CT{cut}_{light}_T'


def size(item):
    _, _, t = hv.tile_rec(item, '-')
    return t['width'], t['height']


def get_box(item, x0, y0, x1, y1, scale=1.0, purpose='', cache=True):
    """Return uint8 RGB array; cached as .npy in SP/C2work/cache."""
    key = f"{item.replace(':', '_')}_{int(x0)}_{int(y0)}_{int(x1)}_{int(y1)}_{scale:.5f}.npy"
    p = os.path.join(CACHE, key)
    if cache and os.path.exists(p):
        log(f'cache-read {item} box=({x0},{y0},{x1},{y1}) scale={scale} purpose={purpose}')
        return np.load(p)
    a = hv.box(item, '-', x0, y0, x1, y1, scale=scale)
    if cache:
        np.save(p, a)
    log(f'bucket-read {item} box=({x0},{y0},{x1},{y1}) scale={scale} shape={a.shape} purpose={purpose}')
    return a


def get_overview(item, scale, purpose=''):
    w, h = size(item)
    return get_box(item, 0, 0, w, h, scale=scale, purpose=purpose)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'overview':
        item, scale = sys.argv[2], float(sys.argv[3])
        purpose = ' '.join(sys.argv[4:])
        a = get_overview(item, scale, purpose)
        out = os.path.join(PROD, f"{item.replace('usc:', '')}_ov{scale:g}.png")
        hv.save_png(a, out)
        print(out, a.shape)
    elif cmd == 'box':
        item = sys.argv[2]
        x0, y0, x1, y1 = map(int, sys.argv[3:7])
        scale = float(sys.argv[7])
        purpose = ' '.join(sys.argv[8:])
        a = get_box(item, x0, y0, x1, y1, scale, purpose)
        out = os.path.join(PROD, f"{item.replace('usc:', '')}_{x0}_{y0}_{x1}_{y1}_s{scale:g}.png")
        hv.save_png(a, out)
        print(out, a.shape)
