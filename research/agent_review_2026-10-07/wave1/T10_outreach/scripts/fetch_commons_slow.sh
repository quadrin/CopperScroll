#!/usr/bin/env bash
# Slow, polite downloader for openly licensed Commons originals.
# Honours the HTTP 429 Retry-After header; verifies SHA-1 against the Commons API value.
# Usage: fetch_commons_slow.sh URLS_TSV OUTDIR   (TSV: url<TAB>sha1)
tsv="$1"; out="$2"; cd "$out" || exit 1
UA="CopperScrollResearchBot/0.1 (https://github.com/quadrin/CopperScroll)"
while IFS=$'\t' read -r u s; do
  fn=$(python3 -I -c "import urllib.parse,sys;print(urllib.parse.unquote(sys.argv[1].rsplit('/',1)[1]))" "$u")
  if [ -f "$fn" ] && [ "$(sha1sum "$fn" | cut -d' ' -f1)" = "$s" ]; then echo "HAVE $fn"; continue; fi
  for i in $(seq 1 40); do
    code=$(curl -sS -A "$UA" -D hdr.txt -o "$fn.part" -w '%{http_code}' "$u")
    if [ "$code" = "200" ] && [ "$(sha1sum "$fn.part" | cut -d' ' -f1)" = "$s" ]; then
      mv "$fn.part" "$fn"; echo "$(date -u +%H:%M:%S) OK $fn"; break
    fi
    ra=$(grep -i '^retry-after:' hdr.txt | tr -dc '0-9'); [ -z "$ra" ] && ra=60
    echo "$(date -u +%H:%M:%S) HTTP $code for $fn; retry-after $ra"; rm -f "$fn.part"; sleep $((ra+5))
  done
  sleep 20
done < "$tsv"
rm -f hdr.txt
echo DONE
