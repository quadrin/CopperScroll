# Run 28 reader briefs (frozen with the first launch, 31 Oct 2026)

All readers: you are keying or listing archaeological records. You are not identifying any place. Do not open the Copper Scroll text or any edition or commentary of it (DJD III also contains it: stay inside the pages named below), the project's candidate lists, ratings, atlas files, `sandbox/` result files, or any file under `research/preregistration/`. Do not open another reader's output. Quotes: at most 15 words per row. Write files with Python's `csv` module, UTF-8.

## Concordance readers (A, B)
- Read the *ʿAtiqot* 41.2 region and single-cave reports (article ids 2544–2593). Text: `/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/atiqot/text/vol-041/iss-2/*.txt`. Page images if needed: bucket `atiqot/pdf/vol-041/iss-2/`.
- List every statement that a feature of this survey is **the same** as a feature recorded by an earlier survey: Bar-Adon 1972 (ASI 1), the Benjamin survey (Finkelstein & Magen 1993; Goldfus & Golani), the 1952 survey (de Vaux, Baillet, DJD III numbering), or any other (name it). Comparisons ("similar to") are not identity.
- Output `keyed/concordance_<A|B>.csv`, columns: `atq41_keys` (survey labels such as `II/3`, `;`-separated), `describer` (`ba72`, `ben93`, `djd3`, or `other:<name>`), `describer_ref` (as printed), `ref_type` (`site_number`, `cave_number`, `page`, `name`), `atq_article`, `atq_page`, `copied` (`yes` if the sentence repeats the earlier survey's description of the feature, else `no`), `quote`, `confidence`, `notes`. Log: `keyed/concordance_<A|B>_log.md`.

## Bar-Adon site-header reader
- Bucket PDF `01-ASI1-Kochavi-1972-indexed-81b7cd39` (Hebrew; the text layer is in reversed order, so read page images). Render with `scripts/render_bucket.py` after `source /root/.hexcog_env`.
- For every site of the chapter (printed pp. 90–150) record only the entry header: site number, name, map reference, grid as printed, printed page. Do not read or summarise the descriptions.
- Output `keyed/ba72_headers.csv` (`site`, `name`, `map_ref`, `grid_printed`, `page`, `notes`) and `keyed/ba72_headers_log.md`.

## Describer keyers (A, B per source)
- Use `../attribute_inventory_2026-10-31/SCHEMA.md` and `../attribute_inventory_2026-10-31/READER_INSTRUCTIONS.md` unchanged, with the source and scope in `describers.csv`. Never open *ʿAtiqot* 41, any `../attribute_inventory_2026-10-31/keyed/` or `out/` file, or the concordance.
- `feature_id` = `<source_id>:<site or cave number as printed>`, plus a suffix for sub-features. `grid_printed` as printed (blank for the 1952 list).
- Output `keyed/<source_id>_<A|B>.csv` and `keyed/<source_id>_<A|B>_log.md`.
- **djd3 (Internet Archive loan, owner's Chrome):** load the Chrome tools with ToolSearch, call `tabs_context_mcp`, create your own tab and use only that tab. Open `https://archive.org/details/lespetitesgrotte0000unse/page/<n>/mode/1up`. Read printed pp. 3–36 only. Never click "Return now", never open another item, and close your tab when done.
- **ben93:** bucket PDFs as in `describers.csv`; locate the pages by rendering at low resolution first.
