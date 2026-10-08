#!/usr/bin/env python3
"""Build a labelled composite of XII 10 (entry 60, second word) from Puech 2006 plates
and DJD III p. 298. Inputs are crops made from the local PDFs (see REPORT.md, section 3).
Run with: python3 -I make_xii10_figure.py PLATES_DIR OUT_PNG
PLATES_DIR must contain: galvfac-001.jpg (pdfimages -f 705 -l 705 -j on the Puech 2006 PDF),
galv400-704.png (pdftoppm -r 400 -f 704 -l 704), radio300-677.png (pdftoppm -r 300 -gray -f 677 -l 677)
and djd318_mid.png (middle of pdftoppm -r 200 -f 318 -l 318 on DJD3_full.pdf).
Full-size renders are kept outside the deliverable in scratchpad/cs/work_W2A/plates_full."""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
P = sys.argv[1]; OUT = sys.argv[2]
def load(name, box=None, scale=1.0, invert=False, gray=False):
    im = Image.open(f"{P}/{name}")
    if invert: im = ImageOps.invert(im.convert('L'))
    if gray: im = ImageOps.autocontrast(im.convert('L'), cutoff=1)
    if box: im = im.crop(box)
    if scale != 1.0: im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
    return im.convert('RGB')
panels = [
 ("A. Puech 2006, Pl. CCCLXXXII (facsimile, Fig. 13), XII 10: words 1-3 (his drawing = his reading)",
  load('galvfac-001.jpg', (560, 830, 1180, 950), 2.0, invert=True)),
 ("B. Puech 2006, Pl. CCCLXXXI (galvanoplastic copy), same words; 150-ppi source rendered at 400 dpi",
  load('galv400-704.png', (1800, 2640, 3300, 2940), 0.83)),
 ("C. Puech 2006, Pl. CCCLVI (radiograph, 150 ppi): XII 10 at the cut, seg. 22D (left) / gap / seg. 21 (right)",
  load('radio300-677.png', (1900, 2070, 2620, 2330), 1.7, gray=True)),
 ("D. DJD III p. 298 (Milik 1962): reading note on XII 10 (he prefers sade-het over yod-nun-het)",
  load('djd318_mid.png', (270, 80, 1500, 140), 1.0)),
]
W = max(p.width for _, p in panels) + 40
H = sum(p.height + 50 for _, p in panels) + 20
canvas = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception:
    font = ImageFont.load_default()
y = 10
for label, im in panels:
    d.text((20, y), label, fill='black', font=font)
    y += 30
    canvas.paste(im, (20, y)); y += im.height + 20
canvas.save(OUT)
print('saved', OUT, canvas.size)
