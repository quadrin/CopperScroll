#!/bin/bash
# OCR Elitzur 2004 (no text layer) page by page with tesseract eng.
PDF="user-library/Ancient place names in the Holy Land _ preservation and -- Yoel Elitzur -- Jerusalem, Winona Lake, Ind, 2004 -- Hebrew University, Magnes Press ; -- isbn13 9781575060712 -- 3fb05748eff6d6a.pdf"
OUT=agent_review/wave2/W2E_primary_checks/elitzur_ocr
mkdir -p $OUT
ocr_page() {
  p=$1
  pp=$(printf "%03d" $p)
  [ -s $OUT/p$pp.txt ] && return
  pdftoppm -f $p -l $p -r 300 -gray -png "$PDF" $OUT/tmp_$pp
  f=$(ls $OUT/tmp_$pp*.png | head -1)
  tesseract "$f" $OUT/p$pp -l eng >/dev/null 2>&1
  rm -f "$f"
}
export -f ocr_page; export PDF OUT
seq 1 237 | xargs -P 8 -I{} bash -c 'ocr_page {}'
