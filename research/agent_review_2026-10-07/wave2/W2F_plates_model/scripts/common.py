import numpy as np, json, os, glob
from PIL import Image
from scipy import ndimage as ndi

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = {c: None for c in range(1, 13)}
ROM = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
def copy_plate_path(col):
    p = 682 + 2*(col-1)
    return glob.glob(os.path.join(BASE, 'plates', 'png', f'*_copy_photo_p{p}_*.png'))[0]
def fac_plate_path(col):
    p = 683 + 2*(col-1)
    return glob.glob(os.path.join(BASE, 'plates', 'png', f'*_facsimile_p{p}_*.png'))[0]
def load_gray(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    return a.mean(2)
def ink_map(g, bg_sigma=25, sm=1.5):
    bg = ndi.gaussian_filter(g, bg_sigma)
    n = g/(bg+1)
    ink = np.clip(1-n, 0, None)
    return ndi.gaussian_filter(ink, sm)
def load_text():
    t = open(os.path.join(BASE, '..', '..', 'shared', 'scroll-text.js'), encoding='utf-8').read()
    return json.loads(t[t.index('{'):t.rindex('}')+1])
