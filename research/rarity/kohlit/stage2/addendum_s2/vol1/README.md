# Zertal Vol. I (English ed. 2004): source-2 extraction for 14 Stage 2 units

Intake: [../vol1_intake_2026-10-17.md](../vol1_intake_2026-10-17.md). Procedure: [../PROCEDURE.md](../PROCEDURE.md), "Extraction".

- **Reader.** A reader agent that had not seen the arrival item file or any coder sheet found and extracted all 14 entries on 17 October 2026. All 14 are `"status": "read"`. Scan index − printed page = 15 throughout.
- **Name and grid check.** 13 entries match the unit's name and grid. For S203 (er-Randeh, Site 62) the name and site number match, but the OCR grid is only partly legible ("182) 2005" against 182100/201500).
- **OCR.** Many site-number headings are garbled in the OCR. The reader confirmed them from the site index and from the order of the entries. Unreadable lines are marked `[?]` in the excerpts.
- **Plans.** One site plan: S798 el-Qul'ah, fig. 468 (p. 545, scan n560). It is captured as `plan_p545.jpg` (994 × 1584 px, from the loan viewer).
- **Files.**
  - [units.csv](units.csv): the reader's list.
  - [build_s2x.py](build_s2x.py): the reader's script. It rebuilds every excerpt and meta file from the OCR text (SHA-256 checked); the rebuild was checked byte for byte.
  - [s2x_manifest.csv](s2x_manifest.csv): each output file's SHA-256.
- **Not in Git.** The excerpts quote the book, so they are not committed. To rebuild them, put `Zertal2004_vol1_djvu_text_n0-625.txt` (owner's Drive, *zertal_2004_MHCS_vol1_IA_loan*) in `src/` next to the script and run `python3 -I build_s2x.py`. The plan image is in the same Drive folder.
- **Next (not done).** Build packet v5 with `build_packets.py … S2X_DIR`. Then a new coder A codes the 14 entries (`../s2coder_prompt.txt`), and coder B codes the units already in its sample. Then merge, run `match.py` unchanged, and write the arrival outcome record. The builder needs the *Highlands of Many Cultures* and Nigro 2011 PDFs at their frozen hashes. They are 92 MB and 79 MB, more than this session can move from Drive.
