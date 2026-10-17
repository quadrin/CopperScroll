#!/bin/sh
# Reproduce Addendum 2 plus the Zertal Vol. I entries (17 October 2026).
# Usage: sh run_addendum_vol1.sh PACKETS_DIR OUT_DIR   (PACKETS_DIR = packet v5: build_packets.py with addendum_s2/vol1 excerpts)
# Chain: first-run sheets -> source-4 addendum -> source-2 addendum (Vols. 2-4) -> Vol. I sheets -> match.py run.
set -e
P="$1"; O="$2"; V=$(cd "$(dirname "$0")" && pwd); H="$V/.."; S4="$H/../addendum_s4"; T=$(mktemp -d)
python3 -I "$S4/merge_s4.py" "$P" "$H/../coded/A" "$S4/coded_s4/A" "$T/A1"
python3 -I "$S4/merge_s4.py" "$P" "$H/../coded/B" "$S4/coded_s4/B" "$T/B1"
cp "$S4"/coded_B_full/*.json "$T/B1/"
python3 -I "$H/merge_source.py" "$P" "$T/A1" "$H/coded_s2/A" "$T/A2" 2 s2z_
python3 -I "$H/merge_source.py" "$P" "$T/B1" "$H/coded_s2/B" "$T/B2" 2 s2z_
cp "$H"/coded_B_full/*.json "$T/B2/"
python3 -I "$H/merge_source.py" "$P" "$T/A2" "$V/coded/A" "$T/A3" 2 s2v1_
python3 -I "$H/merge_source.py" "$P" "$T/B2" "$V/coded/B" "$T/B3" 2 s2v1_
if ls "$V"/coded_B_full/*.json >/dev/null 2>&1; then cp "$V"/coded_B_full/*.json "$T/B3/"; fi
python3 -I "$H/../match.py" run "$P" "$T/A3" "$T/B3" "$O"
