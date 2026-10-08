# Source-2 addendum (Zertal survey entries): procedure (committed before extraction and coding)

**What changed.** On 8 October 2026 UTC the project owner supplied PDFs of three volumes of *The Manasseh Hill Country Survey*. These are Brill's English editions of the Hebrew volumes that WBADB cites:

| English edition | Hebrew volume cited in WBADB |
|---|---|
| Vol. 2, *The Eastern Valleys and the Fringes of the Desert* (2008) | Zertal 1996 |
| Vol. 3, *From Nahal ʿIron to Nahal Shechem* | Zertal and Mirkam 2000 |
| Vol. 4, *From Nahal Bezeq to the Sartaba* (2019) | Zertal 2005 |

Source 2 is "the original survey entry named in Survey_Ref". The English editions give the same numbered site entries in translation, so a site's entry in the English edition is used as its source 2.
- Vol. I (Zertal 1992) was not supplied, so 14 Stage 2 units stay "not accessed".
- The PDFs are copyright works and are not in the repo. `source2_zertal_access.csv` records each file's SHA-256.

**Units.** These are the 78 Stage 2 units whose Survey_Ref names Zertal 1996, Zertal and Mirkam 2000 or Zertal 2005: 30, 1 and 47 units. Units that stopped at Stage 1 stay there, because Stage 1 screened only sources 1 and 3.

**Extraction.** For each unit, a helper agent finds the survey entry with the site number that Survey_Ref names. It checks the name and grid reference against WBADB. It writes the whole entry verbatim, any site plan or figure of the site, and the page numbers to `s2x/<unit_id>/`.

**Packets.** `build_packets.py` gained an optional last argument, the folder of these entries. With it, a unit's source-2 section holds the entry under `other_entries`. Without it, the builder gives exactly the earlier packets; this was checked by comparing the manifest. Only the packets of the 78 units change (packet v4).

**Coding.** This follows the source-4 addendum.
- **Coder A.** A new coder A codes only the new source-2 entries for the 78 units: features, positions, dates and absence statements under PROTOCOL.md, with `"source": "2"`.
- **Merge.** `merge_source.py` appends these features to coder A's sheet. It keeps every earlier feature.
- **Coder B, random sample.** A blind coder B does the same for the 16 of these units that coder B had already coded, and the result is merged into coder B's sheets.
- **Coder B, new matches.** After the merge, coder B codes in full every unit that has become a coder-A match in any branch, variant or Nigro setting, if coder B has not coded it before.
- **Matching.** `match.py` and its constants are unchanged, and the merge rule is unchanged. The result is reported as Addendum 2. RESULTS.md and the source-4 addendum stay on record.
