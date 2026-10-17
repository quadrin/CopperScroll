# Zertal Vol. I (English ed. 2004): source-2 extraction for 14 Stage 2 units

Intake: [../vol1_intake_2026-10-17.md](../vol1_intake_2026-10-17.md). Procedure: [../PROCEDURE.md](../PROCEDURE.md), "Extraction".

- **Reader.** A reader agent that had not seen the arrival item file or any coder sheet found and extracted all 14 entries on 17 October 2026. All 14 are `"status": "read"`. Scan index − printed page = 15 throughout.
- **Name and grid check.** 13 entries match the unit's name and grid. For S203 (er-Randeh, Site 62) the name and site number match, but the OCR grid is only partly legible ("182) 2005" against 182100/201500).
- **OCR.** Many site-number headings are garbled in the OCR. The reader confirmed them from the site index and from the order of the entries. Unreadable lines are marked `[?]` in the excerpts.
- **Plans.** One site plan: S798 el-Qul'ah, fig. 468 (p. 545, scan n560). It is captured from the loan viewer at 994 × 1584 px (JPEG in Drive; PNG `plan_p545.png` in the packets).
- **Files.**
  - [units.csv](units.csv): the reader's list.
  - [build_s2x.py](build_s2x.py): the reader's script. It rebuilds every excerpt and meta file from the OCR text (SHA-256 checked); the rebuild was checked byte for byte.
  - [s2x_manifest.csv](s2x_manifest.csv): each output file's SHA-256.
- **Not in Git.** The excerpts quote the book, so they are not committed. To rebuild them, put `Zertal2004_vol1_djvu_text_n0-625.txt` (owner's Drive, *zertal_2004_MHCS_vol1_IA_loan*) in `src/` next to the script and run `python3 -I build_s2x.py`. The plan image is in the same Drive folder.
- **Plan image.** `build_packets.py` reads only `*.png`, so the plan was saved as `plan_p545.png` before the packets were built.

## Packets, coding and result (17 October 2026)

- **Packets.** The owner linked his Mac, and the inputs were copied from his synced Drive folder. Every input matched its frozen hash: WBADB, *Highlands*, Nigro 2011 and both SWP texts. The builder is unchanged.
  - `packet_manifest_base.csv`: packets built without excerpts.
  - `packet_manifest_v5.csv`: the same packets with these 14 Vol. I entries.
  - The source-4 excerpts and the Vols. 2–4 Zertal excerpts of packet v4 were not available. So 114 packets differ from v4, in quoted text only; geometry and references are the same. Check: `run_addendum.sh` on the base packets reproduced Addendum 2's three result files byte for byte.
- **Coding** (`../s2coder_prompt.txt`, with this session's paths). Two new coder-A agents coded all 14 entries ([coded/A/](coded/A/)). One blind coder-B agent coded the 8 units already in coder B's sample: S103, S112, S137, S157, S178, S563, S778, S806 ([coded/B/](coded/B/)). No unit became a new coder-A match in any branch, so no full coder-B coding was needed.
- **Matching.** `match.py` and its constants are unchanged. To reproduce: `sh run_addendum_vol1.sh PACKETS_v5 OUT`. The outputs are in [results/](results/).

| Set | Branch | N | k | f | m | Before (Addendum 2): k / f / m |
|---|---|---|---|---|---|---|
| R1, Hel/Rom (main) | A, survey level (headline) | 333 | 0 | 20 | 313 | 0 / 20 / 313 |
| R1, Hel/Rom (main) | B | 333 | 5 | 19 | 309 | 5 / 19 / 309 |
| R1, any pre-70 | A, survey level | 499 | 0 | **32** | **467** | 0 / 31 / 468 |
| R1, any pre-70 | A, text level | 499 | 0 | **31** | **468** | 0 / 30 / 469 |
| R1, any pre-70 | B | 499 | 6 | **31** | **462** | 6 / 30 / 463 |

R2 does not change.

- **What changed.**
  - S798 el-Qul'ah (Site 280, p. 543): C2 UNKNOWN → FAIL, from "Cisterns: none" in the data block. It is in the pre-70 set only.
  - Under the dated-only variant, S144 (Site 52) and S780 (Site 277) also become C2 FAIL on the same field.
  - S103 Kh. Bal'ame: C3s UNKNOWN → MATCH (both coders). C1 and C2 stay UNKNOWN, so no branch changes.
- **Main set.** All six main-set entries record cisterns, so none becomes a C2 FAIL. The headline stays k = 0, f = 20, m = 313: rarity is still not measurable from the evidence (pre-registration §6). Nothing here identifies a site.
- **Arrival record:** [outcomes/zertal-vol-1_2026-10-17.json](../../../../preregistration/arrivals/outcomes/zertal-vol-1_2026-10-17.json), with pred1 confirm, pred2 confirm, pred3 contradict (calibration only) and one unregistered observation (S103).
