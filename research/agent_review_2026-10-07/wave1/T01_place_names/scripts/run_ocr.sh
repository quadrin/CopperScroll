#!/bin/bash
O=agent_review/wave1/T01_place_names
W=$1
for R in "339 358" "279 338" "219 264" "383 422"; do
  set -- $R
  python3 -I $O/scripts/ocr_pages.py $O/downloads/ocr $1 $2 $W 2
done
