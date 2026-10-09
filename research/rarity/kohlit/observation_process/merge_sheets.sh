#!/bin/sh
# Rebuild the merged coder sheets that the source-2 addendum result uses (no matching is run).
# Usage: sh merge_sheets.sh PACKETS_DIR OUT_DIR   (PACKETS_DIR = packet v4)
# Writes OUT_DIR/A and OUT_DIR/B. These are the same steps as stage2/addendum_s2/run_addendum.sh,
# without its last line. The stage2 scripts are only called, never changed.
set -e
P="$1"; O="$2"; H=$(cd "$(dirname "$0")" && pwd); S2="$H/../stage2"; A2="$S2/addendum_s2"; S4="$S2/addendum_s4"
mkdir -p "$O"; T="$O/_work"; rm -rf "$T" "$O/A" "$O/B"; mkdir -p "$T"
python3 -I "$S4/merge_s4.py" "$P" "$S2/coded/A" "$S4/coded_s4/A" "$T/A1"
python3 -I "$S4/merge_s4.py" "$P" "$S2/coded/B" "$S4/coded_s4/B" "$T/B1"
cp "$S4"/coded_B_full/*.json "$T/B1/"
python3 -I "$A2/merge_source.py" "$P" "$T/A1" "$A2/coded_s2/A" "$O/A" 2 s2z_
python3 -I "$A2/merge_source.py" "$P" "$T/B1" "$A2/coded_s2/B" "$O/B" 2 s2z_
cp "$A2"/coded_B_full/*.json "$O/B/"
rm -rf "$T"
