# Blind period coding: log

## What was coded

- `strings.csv`: 3,161 distinct period strings (whitespace-collapsed), sorted alphabetically, ids P0001–P3161. Sources: HA-ESI merged `period_as_given`, ASI `period_as_given`, caves `period_stated`, columbaria `date_text`. Built by `../code/build_strings.py`. SHA-256 `0885a311eeb344f5bad80d70678bf41c914f2246d9d3c26d18b6087e386e0495`.
- Batches: `batches/batch_01.tsv` … `batch_08.tsv` (400 lines each, last 361), `sid<TAB>text`, by `../code/make_batches.py`.

## Coder instances (8, one per batch)

- Started 2026-10-31 06:13 UTC (container clock), finished by 06:17 UTC.
- Tool: Claude Code CLI 2.1.314, `claude -p`, model `claude-opus-5-5`, run by `../code/run_blind_coder.sh`.
- Isolation: empty working directory in the scratchpad; `--tools ""` (no tools), `--strict-mcp-config` (no MCP servers), `--setting-sources ""`, `--disable-slash-commands`, `--no-chrome`, `--no-session-persistence`; environment variables for the attached claude.ai Project and user email unset. A test call with the same flags (06:0x UTC) reported no attached project and no mention of a scroll, an ancient text or a research project in its context. The CLI still injects a generic Claude Code system prompt (git attribution lines, proxy notes); it names no project.
- System prompt: "You are a careful data-coding assistant. Follow the user's coding instructions exactly."
- User prompt: `CODER_INSTRUCTIONS.md` (SHA-256 `0a6efabdb779517a63fbf2be89a3e4f546cd3251106fefba229c05d04bb6347b`) + "INPUT LINES:" + one batch.
- The instructions contain a neutral period table (conventional southern-Levant period limits). They do not mention the scenarios, the hypothesis, the Copper Scroll, Qumran or any project. The strings themselves sometimes name the revolts, Bar Kokhba or Qumran (they are report wording); this is the source text and cannot be removed.

| instance | prompt SHA-256 | output | output SHA-256 | lines |
|---|---|---|---|---|
| coder_01 | 70829af9eb7b8dbeed83ce3a74b6ce11d5095de283f7cd1ca8420fcf1f2497c4 | raw/coded_batch_01.csv | 6bf335d87eaf5e6c8cc695dc862c47d941056ba58cf0feafe24dba83dd005552 | 400 |
| coder_02 | 179f73ed2823bb71510696be5733372d613e8eb59dc665695bccbc2717077bbc | raw/coded_batch_02.csv | 220dcc9cf705601ea2b52eb3e29b730b4190fbbe8e0175cc009ac98f13ed4135 | 400 |
| coder_03 | f06a9066ef669a3cddd985597a3ef2ca6f17759535f1e017a2f1d3c65faca322 | raw/coded_batch_03.csv | feb6725e466345aae85af24bf01898304b7844f4891d8515f3516f1efb2080d3 | 400 |
| coder_04 | 31d3b871cf85a00eb2aecc8f16443e557b271cdfc459de4078b5ac4dc6ccff02 | raw/coded_batch_04.csv | c0e533720fa92ad46766360ead62c7f98fadc4aca8aff2c8b14c29bdcbfc9617 | 400 |
| coder_05 | 84ad590e8851d8f841177b8e15c5fe1b84b5fec5caae6583be9c843c32f738dc | raw/coded_batch_05.csv | d89afbd56b223b3ac01e8d38fb206335a6dd2af67bfc11ae6eac79e1bd47827e | 400 |
| coder_06 | 512eaad91e416b97e37f87fa7a00a93c4fd873d5a94a5d9dda37ba0fe9b912d0 | raw/coded_batch_06.csv | 3c718e9b26facd4ea4a01f678413d7e513e2cc3fa1c234ec83ca5f48a034c131 | 400 |
| coder_07 | ef1de135ec22963558510a172b030ae2cd0f7387fc59da18b596162e9cb01500 | raw/coded_batch_07.csv | c075da2c67b8d666cef9cef6d94209456c1686cd16d6dca1fb4aef2068a9762f | 400 |
| coder_08 | 001dc0e8b296310923e36861fcba6e5a252323b6279f0e52bd09194979c85ece | raw/coded_batch_08.csv | a264eb58423217d36e6796e87bf5e7c9f4f0b7144c2a996c4666bcdae82adfe3 | 361 |

The prompt files are reproducible: `CODER_INSTRUCTIONS.md` + `\nINPUT LINES:\n` + batch file (see `run_blind_coder.sh`).

- Merge: `../code/merge_coded.py` → `coded_intervals.csv` (SHA-256 `b52b83db970db12e6df3a61bbf2d50d1afb01c0ad78e9972dd135cffcf0913d0`). 3,161 of 3,161 strings coded; 0 missing; 0 rows with start > end. Kinds: feature 2,059; finds 430; undated 251; site 233; relative 135; other 53. Confidence: high 860, medium 1,602, low 699.
- This worker did not edit any coded value.

## Check instance (third instance)

- Sample: 150 strings, `coded_intervals.csv` `.sample(150, random_state=20261030)`; `check_sample_input.csv` / `.tsv` (tsv SHA-256 `d4f60445babf1f55175b65609e286807c70f909bcdf16183b941f54bcaf3aa10`).
- Instructions: `CHECKER_INSTRUCTIONS.md` (SHA-256 `8ed1223c679e3809d9c106a3cc0fb19af5d29fffb46d3cca83dfc118b5f621fb`): the coder's rules and period table, then a request to judge each coded line against the source text (interval within 25 years, events, kind) and give its own values. Same isolation and model.
- Prompt SHA-256 `dc85dac2773c1ecbb112ebbb07ef8a901355d6901532b20238f03e4cbeaea1e0`; output `raw/check_sample_output.csv` SHA-256 `4ef9e31a54f8c8e0ede75498e600e289dc915c94c98b2ce5440e8416c288bb3c`, 150 lines.
- Result (`check_sample_result.csv`):
  - interval agrees: 148 / 150 (98.7 %);
  - start/end events agree: 149 / 150 (99.3 %);
  - kind agrees: 145 / 150 (96.7 %);
  - all three agree: 143 / 150 (95.3 %).
  - The two interval disagreements: "late Byzantine-Umayyad" (coder 491, checker 534: definition of "late"); one "not dated (Herodian cooking-pot rim in the fill ...)" string that the coder left undated and the checker dated from the fill sherds. Neither changes the test.
- Limitation: the checker is the same model family with the same table, so agreement measures consistency with the instructions, not historical truth.

## How the intervals map to "in existence"

The coded interval is mostly a period of use or a period label, not a construction or destruction event. The frozen rule (PROTOCOL_FROZEN.md §5) treats `start` as "built by then" and treats `end` as an end of existence **only** when `end_event = yes` (the text states destruction, abandonment, filling or going out of use). A period label's end is not an abandonment. The alternative rule `attested` (sensitivity) uses the coded interval literally as the time of existence.
