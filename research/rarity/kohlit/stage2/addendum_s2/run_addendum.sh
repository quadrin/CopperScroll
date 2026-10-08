#!/bin/sh
# Reproduce the source-2 (Zertal) addendum result from the committed sheets.
# Usage: sh run_addendum.sh PACKETS_DIR OUT_DIR   (PACKETS_DIR = packet v4: build_packets.py with the source-4 and Zertal excerpts)
# Chain: first-run sheets -> source-4 addendum -> source-2 addendum -> match.py run.
set -e
P="$1"; O="$2"; H=$(cd "$(dirname "$0")" && pwd); S4="$H/../addendum_s4"; T=$(mktemp -d)
python3 -I "$S4/merge_s4.py" "$P" "$H/../coded/A" "$S4/coded_s4/A" "$T/A1"
python3 -I "$S4/merge_s4.py" "$P" "$H/../coded/B" "$S4/coded_s4/B" "$T/B1"
cp "$S4"/coded_B_full/*.json "$T/B1/"
python3 -I "$H/merge_source.py" "$P" "$T/A1" "$H/coded_s2/A" "$T/A2" 2 s2z_
python3 -I "$H/merge_source.py" "$P" "$T/B1" "$H/coded_s2/B" "$T/B2" 2 s2z_
cp "$H"/coded_B_full/*.json "$T/B2/"
python3 -I "$H/../match.py" run "$P" "$T/A2" "$T/B2" "$O"
