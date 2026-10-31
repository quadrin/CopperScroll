#!/bin/bash
# Run one blind coder instance on one batch. Isolation: empty cwd, no tools,
# no MCP, no settings, no slash commands, no project attachment env vars,
# no session persistence. The instance sees only: system prompt line + instructions + batch.
# usage: run_blind_coder.sh INSTRUCTIONS BATCH OUT WORKDIR
set -e
INS="$1"; BATCH="$2"; OUT="$3"; WD="$4"
mkdir -p "$WD"; cd "$WD"
{ cat "$INS"; echo; echo "INPUT LINES:"; cat "$BATCH"; } > prompt.txt
env -u CLAUDE_PROJECT_UUID -u CLAUDE_PROJECT_TOOL -u CLAUDE_CODE_USER_EMAIL \
    -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
  claude -p --system-prompt "You are a careful data-coding assistant. Follow the user's coding instructions exactly." \
    --strict-mcp-config --tools "" --setting-sources "" --no-session-persistence \
    --disable-slash-commands --no-chrome --model claude-opus-5-5 < prompt.txt > "$OUT" 2> "$OUT.err"
