#!/usr/bin/env bash
# Fetch large Commons thumbnails (openly licensed images) when originals are rate-limited.
# Usage: fetch_commons_thumbs.sh URLS_TSV OUTDIR WIDTH
tsv="$1"; out="$2"; W="$3"; cd "$out" || exit 1
UA="CopperScrollResearchBot/0.1 (https://github.com/quadrin/CopperScroll)"
while IFS=$'\t' read -r u s; do
  path=${u#https://upload.wikimedia.org/wikipedia/commons/}
  base=${path##*/}
  turl="https://upload.wikimedia.org/wikipedia/commons/thumb/${path}/${W}px-${base}"
  fn="thumb${W}_$(python3 -I -c "import urllib.parse,sys;print(urllib.parse.unquote(sys.argv[1]))" "$base")"
  [ -s "$fn" ] && { echo "HAVE $fn"; continue; }
  for i in $(seq 1 30); do
    code=$(curl -sS -A "$UA" -D thdr.txt -o "$fn.part" -w '%{http_code}' "$turl")
    if [ "$code" = "200" ] && python3 -I -c "import sys;from PIL import Image;Image.open(sys.argv[1]).load()" "$fn.part" 2>/dev/null; then
      mv "$fn.part" "$fn"; echo "$(date -u +%H:%M:%S) OK $fn"; break
    fi
    ra=$(grep -i '^retry-after:' thdr.txt | tr -dc '0-9'); [ -z "$ra" ] && ra=30
    echo "$(date -u +%H:%M:%S) HTTP $code thumb $fn; retry-after $ra"; rm -f "$fn.part"; sleep $((ra+3))
  done
  sleep 5
done < "$tsv"
rm -f thdr.txt; echo DONE
