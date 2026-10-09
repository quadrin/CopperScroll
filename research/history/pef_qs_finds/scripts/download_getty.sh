#!/bin/bash
# usage: download_getty.sh OUTDIR id1 id2 ...
out=$1; shift
for id in "$@"; do
  f="$out/${id}_djvu.txt"
  [ -s "$f" ] && continue
  for k in 1 2 3 4 5; do
    code=$(curl -sS -L -m 300 -o "$f" -w "%{http_code}" "https://archive.org/download/$id/${id}_djvu.txt")
    [ "$code" = "200" ] && [ -s "$f" ] && break
    sleep $((3*k))
  done
  echo "$id $code"
done
