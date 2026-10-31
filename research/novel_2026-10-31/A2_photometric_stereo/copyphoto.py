"""Fetch the Puech 2006 (STDJ 55, Brizemeure, Lacoudre & Puech 2006, vol. II) copy photograph of one column
through hexview.py and extract the embedded plate image natively (same pixels as W2F's `pdfimages -all`),
so W2F letter coordinates (labels_verified.csv px, py; controls_manifest.csv crop_box) apply directly.
Copy A PDF pages (W2F plate_index.csv): column k (1..12) copy photograph on page 682 + 2 (k - 1).
The image is cached in the scratchpad only (publication not permitted)."""
import os, sys, io
import numpy as np
from common import hv, CACHE

DOC_A = "8ca55af0"
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


def copy_photo(col_roman):
    k = ROMAN.index(col_roman) + 1
    page = 682 + 2 * (k - 1)
    p = f"{CACHE}/copyphoto_{col_roman}.npy"
    if os.path.exists(p):
        return np.load(p), page
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    b = hv.pdf_page(DOC_A, page)
    doc = fitz.open(stream=b, filetype="pdf")
    best = None
    for img in doc[0].get_images(full=True):
        d = doc.extract_image(img[0])
        if best is None or d["width"] * d["height"] > best["width"] * best["height"]:
            best = d
    from PIL import Image, ImageChops
    im = Image.open(io.BytesIO(best["image"]))
    if im.mode == "CMYK":
        if im.info.get("adobe") is not None:
            im = ImageChops.invert(im)
        im = im.convert("RGB")
    a = np.asarray(im.convert("L"))
    np.save(p, a)
    return a, page


if __name__ == "__main__":
    a, page = copy_photo(sys.argv[1])
    print(sys.argv[1], page, a.shape)
