# Lane I2 blind extractor: self-report check (31 October 2026)

Method: lane I `run_extract.sh` (`claude -p`, Sonnet 5.5, `--tools ""`, `--strict-mcp-config`, `--setting-sources ""`,
`--no-session-persistence`, empty working directory `scratchpad/I2/blindcwd`, project env vars removed). Before the
extraction run, one instance was asked to list every project, document, file, directory, tool, MCP server and prior context it could see.

Run 1 (env -u CLAUDE_PROJECT_UUID, CLAUDE_PROJECT_TOOL, CLAUDE_ADDITIONAL_DIRECTORIES,
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD; exactly as lane I). Output sha256 815b9638d5cb46fed0717eb28df8679d0837859592734148dc662231e9e5b2ea.
- Projects / attached documents / prior context: NONE.
- Leak found: the instance reported **browser (Claude in Chrome) tools** in spite of `--tools ""`, and the account e-mail address
  from the user context. No project document name, repo path, scroll name or candidate was reported.

Run 2 (also removed CLAUDE_CODE_ENABLE_CFC, CLAUDE_CODE_CHROME_LATE_MCP_SERVER, CLAUDE_CHROME_PERMISSION_MODE,
CLAUDE_CODE_USER_EMAIL, CLAUDE_CODE_TERMINAL_MCP_TOOLS). Output sha256 c9e8fafb550da09283036904d17c96ed251be6a9166e86de418d8ac647a7b01d.
- Projects / documents / files: NONE. Tools: none. MCP servers: NONE. Skills: none. Prior conversation: none.
- Still visible: the working directory and a scratchpad path (both outside the repository, no project names in them),
  generic proxy notes, git attribution text, and the account e-mail address (supplied by the host context, not by an env var
  that the runner can remove).
- Result: **pass** for the blinding requirement. The extractor sees no scroll names, readings, candidates, project
  documents or repo paths. The visible e-mail address and environment notes carry no information about the test.

All 28 extraction runs used the run-2 environment (`run_extract_i2.sh`). The prompt was lane I `extractor_instructions.txt`
(byte-identical copy) plus one source addendum (`addendum_hebrew.txt`, `addendum_french.txt`, `addendum_hutt.txt`).

Run log:
- First launch (02:11 UTC): all 28 instances received an empty source text, because the runner changes to the empty working
  directory and the chunk paths were relative. The instances replied that no passages were given. These outputs were set aside
  (scratchpad `ext_failed_relpath/`, not used) and the run was repeated with absolute paths.
- Second launch: 28 of 28 runs exited 0 with stop reason end_turn; 0 malformed JSON lines; 755 records.
