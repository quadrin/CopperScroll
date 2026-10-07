#!/usr/bin/env bash
# Query the Wikimedia Commons API with polite retries (the shared egress IP is often rate-limited).
# Usage: commons_query.sh OUTFILE key=value [key=value ...]
out="$1"; shift
args=()
for kv in "$@"; do args+=(--data-urlencode "$kv"); done
for i in 1 2 3 4 5 6; do
  curl -sS -G -A "CopperScrollResearchBot/0.1 (https://github.com/quadrin/CopperScroll)" \
    "https://commons.wikimedia.org/w/api.php" "${args[@]}" --data-urlencode "format=json" -o "$out"
  if head -c 1 "$out" | grep -q '{'; then echo "ok after $i tries"; exit 0; fi
  sleep $((20*i))
done
echo "failed"; exit 1
