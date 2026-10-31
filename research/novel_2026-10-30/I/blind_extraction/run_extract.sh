#!/bin/bash
# usage: run_extract.sh CHUNKFILE OUTDIR
set -u
B=$(basename "$1" .txt)
cd /tmp/claude-0/-home-claude/cc886eb6-491a-5cbd-a0d0-e98816552f00/scratchpad/I/blindcwd
{ cat ../scripts/extractor_instructions.txt; echo; echo "===== SOURCE TEXT FOLLOWS ====="; cat "$1"; } | \
env -u CLAUDE_PROJECT_UUID -u CLAUDE_PROJECT_TOOL -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
 timeout 1500 claude -p --system-prompt "You extract structured data from historical texts. Output only what the user asks for." \
 --tools "" --strict-mcp-config --setting-sources "" --no-session-persistence --output-format json > "$2/$B.json" 2> "$2/$B.err"
echo "$B exit=$?"
