#!/bin/bash
# OCR all PNGs matching prefix in a dir: upscale 2x with PIL, then tesseract eng
cd "$1"; prefix="$2"
for f in ${prefix}*.png; do
  b="${f%.png}"
  [ -f "$b.txt" ] && continue
  python3 -I -c "
from PIL import Image, ImageOps
im=Image.open('$f').convert('L'); im=im.resize((im.width*2, im.height*2), Image.LANCZOS); im.save('${b}_x2.png')"
  tesseract "${b}_x2.png" "$b" -l eng --psm 3 >/dev/null 2>&1
  rm -f "${b}_x2.png"
done
echo DONE > "${prefix}_DONE"
