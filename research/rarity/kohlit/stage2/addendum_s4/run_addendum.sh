#!/bin/sh
# Reproduce the source-4 addendum result from the committed sheets.
# Usage: sh run_addendum.sh PACKETS_DIR OUT_DIR   (PACKETS_DIR = output of build_packets.py with the v2 source-4 excerpts)
set -e
P="$1"; O="$2"; H=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d)
python3 -I "$H/merge_s4.py" "$P" "$H/../coded/A" "$H/coded_s4/A" "$T/A"
python3 -I "$H/merge_s4.py" "$P" "$H/../coded/B" "$H/coded_s4/B" "$T/B"
cp "$H"/coded_B_full/*.json "$T/B/"
python3 -I "$H/../match.py" run "$P" "$T/A" "$T/B" "$O"
