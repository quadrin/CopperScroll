# Source-4 addendum: procedure (committed before any source-4 coding)

**What changed.** On 8 October 2026 UTC the project owner supplied PDFs of 24 first publications that the first run could not read (23 sites, plus Naveh 1974 for Hyrcania).
- The first run's result ([RESULTS.md](../RESULTS.md)) stays as it is. This addendum is reported beside it.
- The rules, `match.py` and its constants are unchanged.
- Only the access to source 4 changed. In the first run, the access rule was "lawfully online"; in this addendum it is "lawfully online, or a PDF supplied by the project owner". The PDFs are copyright works and are not in the repo; [`source4_v2_access.csv`](source4_v2_access.csv) records each file's SHA-256.

**Extraction.** As in the first run, helper agents extracted, for each site, only the plan and the passages on water installations and burials, with printed and PDF page numbers. Hebrew passages are given verbatim with an English translation. The packet builder is unchanged. It read the new excerpts into packet v3. Only those 24 packets changed (see `packet_manifest.csv`).

**Coding.** For each of the 24 units, a new coder A reads only the unit record, the geometry lists and the source-4 section of the packet. The coder writes a source-4-only sheet in the format of PROTOCOL.md §10, with `"source": "4"` on every feature. `merge_s4.py` adds these features to coder A's existing sheet. It keeps every feature from sources 1, 2, 3 and 5 as it was, so the earlier coding is not redone or reopened.
- **Plans.** A plan gives a `plan` position only if the coder can place the unit's recorded centre point on it. Otherwise a feature on a plan takes `words` (for example "in the eastern part"), or `none`.
- **Coder B, random sample.** Seven of the 24 units are in coder B's random sample: E334, S1667, S2514, S2565, S2589, S3001 and S836. For these, a separate coder B codes source 4 in the same way, blind to coder A, and the result is merged into coder B's sheet.
- **Coder B, new matches.** The merged coder-A sheets are matched again. For every unit that is now a coder-A match in any branch, variant or Nigro setting, coder B codes the whole unit from packet v3 if coder B has not coded it before.
- **Merge rule.** Unchanged: where coders A and B differ on a condition, it is UNKNOWN.
