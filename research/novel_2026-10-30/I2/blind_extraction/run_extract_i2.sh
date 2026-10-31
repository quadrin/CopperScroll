#!/bin/bash
# Lane I2 blind extractor runner (lane I method: run_extract.sh). usage: run_extract_i2.sh CHUNKFILE OUTDIR ADDENDUM
# Lane I instructions unchanged + one source addendum. No tools, no MCP, no settings, no session persistence,
# empty working directory, project and browser/e-mail environment variables removed (self-report check log).
set -u
B=$(basename "$1" .txt)
I2=/tmp/claude-0/-home-claude/cc886eb6-491a-5cbd-a0d0-e98816552f00/scratchpad/I2
cd $I2/blindcwd
{ cat $I2/instr/extractor_instructions.txt; cat "$3"; echo; echo "===== SOURCE TEXT FOLLOWS ====="; cat "$1"; } | \
env -u CLAUDE_PROJECT_UUID -u CLAUDE_PROJECT_TOOL -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
    -u CLAUDE_CODE_ENABLE_CFC -u CLAUDE_CODE_CHROME_LATE_MCP_SERVER -u CLAUDE_CHROME_PERMISSION_MODE -u CLAUDE_CODE_USER_EMAIL \
    -u CLAUDE_CODE_TERMINAL_MCP_TOOLS \
 timeout 2400 claude -p --system-prompt "You extract structured data from historical texts. Output only what the user asks for." \
 --tools "" --strict-mcp-config --setting-sources "" --no-session-persistence --output-format json > "$2/$B.json" 2> "$2/$B.err"
echo "$B exit=$?"
