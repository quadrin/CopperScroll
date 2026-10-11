#!/bin/bash
# Part A, step 1 (run on the owner's Mac, Cowork VM): check each part-A PDF against partition.csv and extract text.
# Input: partA.txt (one line per file: "<local_file> <sha256>", the part-A rows of ../../partition.csv).
# Output (outside the repository): ~/p3a_scratch/txt/<base>.raw.txt and .layout.txt, and hashcheck.tsv
# (file, OK/MISMATCH, sha256, PDF pages, base, raw sha256, layout sha256, raw bytes).
# Copied from ~/p3a_scratch/run_extract.sh as run on 11 October 2026.
D="$HOME/mnt/Downloads/IAA portal volumes"
O=$HOME/p3a_scratch/txt
cd $HOME/p3a_scratch
[ -n "$1" ] || : > hashcheck.tsv
while read f h; do
  got=$(sha256sum "$D/$f" | cut -d' ' -f1)
  ok=MISMATCH; [ "$got" = "$h" ] && ok=OK
  pages=$(pdfinfo "$D/$f" 2>/dev/null | awk '/^Pages:/{print $2}')
  b=${f%.pdf}; b=${b#IAA_}
  if [ "$ok" = OK ]; then
    [ -s "$O/$b.raw.txt" ] || pdftotext -raw "$D/$f" "$O/$b.raw.txt"
    [ -s "$O/$b.layout.txt" ] || pdftotext -layout "$D/$f" "$O/$b.layout.txt"
    rs=$(sha256sum "$O/$b.raw.txt" | cut -d' ' -f1); ls_=$(sha256sum "$O/$b.layout.txt" | cut -d' ' -f1)
    chars=$(wc -c < "$O/$b.raw.txt")
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$f" "$ok" "$got" "$pages" "$b" "$rs" "$ls_" "$chars" >> hashcheck.tsv
done < "${1:-partA.txt}"
