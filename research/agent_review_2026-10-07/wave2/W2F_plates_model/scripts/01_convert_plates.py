"""Convert natively extracted plate JPEGs (pdfimages -all) to PNG (RGB for copy photos,
L for radiographs/facsimiles), fixing Adobe-inverted CMYK. Builds plate index.
Usage: python3 -I 01_convert_plates.py <outdir>"""
import sys, os, json, glob, re
import numpy as np
from PIL import Image, ImageChops

O = sys.argv[1]
raw = os.path.join(O, 'plates', 'A_raw')
out = os.path.join(O, 'plates', 'png')
os.makedirs(out, exist_ok=True)

roman = {}
def to_roman(n):
    vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    s=''
    for v,r in vals:
        while n>=v: s+=r; n-=v
    return s

# radiograph captions from pdftotext (order of labels in text layer, not necessarily left-to-right)
rad_labels = {654:'4C 3G 3D 2G',655:'2D 1C',656:'6G 6D',657:'5G 5C 5D',658:'8G 8D',659:'7G 7C',660:'10C 10D2 9D',
 661:'9C 9G',662:'11G 11C',663:'11D 10G',664:'11G 12D',665:'12C 12G',666:'14G 14D',667:'13C 13 13B',668:'15G',
 669:'15C 15D',670:'17C 16 16D',671:'16C 16G',672:'18 18G 18C',673:'18D 17C',674:'20G 16 20C 20D',675:'19G 19C 19D',
 676:'23 22G',677:'22C 22D 21'}
cols = ['I','I','II','II','III','III','IV','IV','V','V','VI','VI','VII','VII','VIII','VIII','IX','IX','X','X','XI','XI','XII','XII']
index = []
for f in sorted(glob.glob(os.path.join(raw, 'A-*.jpg'))):
    m = re.match(r'A-(\d+)-(\d+)\.jpg', os.path.basename(f))
    page, num = int(m.group(1)), int(m.group(2))
    im = Image.open(f)
    if im.mode == 'CMYK':
        # Adobe APP14 CMYK JPEGs store inverted values
        if im.info.get('adobe') is not None:
            im = ImageChops.invert(im)
        im = im.convert('RGB')
    if 654 <= page <= 677:
        series = 'radiograph'; plate_n = 333 + (page - 654); col = cols[page-654]; lab = rad_labels[page]
    elif page in (680, 681):
        series = 'copy_photo' if page == 680 else 'facsimile'; plate_n = 357 + (page-680); col = 'start of scroll'; lab=''
    elif 682 <= page <= 705:
        k = page - 682
        series = 'copy_photo' if k % 2 == 0 else 'facsimile'
        plate_n = 359 + k; col = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][k//2]; lab=''
    else:
        series = 'overview'; plate_n = 383; col='whole scroll (copy)'; lab=''
    name = f'pl{to_roman(plate_n)}_{series}_p{page}_{num:03d}.png'
    im.save(os.path.join(out, name))
    index.append(dict(file=name, pdf_page=page, image_num=num, plate=to_roman(plate_n), series=series,
                      column=col, segment_labels_in_caption=lab, width=im.size[0], height=im.size[1], mode=im.mode))
json.dump(index, open(os.path.join(O, 'data', 'plate_index_raw.json'), 'w'), indent=1, ensure_ascii=False)
print(len(index))
