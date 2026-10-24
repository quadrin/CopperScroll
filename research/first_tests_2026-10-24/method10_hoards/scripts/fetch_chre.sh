#!/bin/bash
# polite fetch: 3.5 s between requests
D=/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests/hoard/raw/chre/hoards
mkdir -p $D
while read id; do
  [ -s $D/$id.html ] || { curl -sS -m 60 "https://chre.ashmus.ox.ac.uk/hoard/$id" -o $D/$id.html; sleep 3.5; }
  [ -s $D/${id}_coins.csv ] || { curl -sS -m 60 "https://chre.ashmus.ox.ac.uk/hoard/$id/csv/coins" -o $D/${id}_coins.csv; sleep 3.5; }
done < $1
echo DONE
