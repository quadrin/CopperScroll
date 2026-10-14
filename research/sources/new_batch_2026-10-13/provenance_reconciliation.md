# New-source provenance and archive reconciliation

Baseline: quadrin/CopperScroll main 23e2b74bdc4ceac8b4418b79a5fa501db20e7b5e, inspected 13 October 2026 Los Angeles. Live project source: https://drive.google.com/drive/folders/114qehR0C8LouGds9UwZ5-hpStbv2GMQb .

## Grounded batch

The latest intake is exactly 72 PDF file identities: 41 files created 13 October 2026 20:16–21:30 UTC, followed by 31 files created 22:51 UTC through 14 October 01:50 UTC. Both windows occur on 13 October in Los Angeles. The CSV records each stable Drive ID, original/current name, created timestamp, bytes, URL and copy scope. These windows agree with the acquisition-history document's two intake updates. The older repository manifest yields a broader delta and must not silently redefine the latest batch.

The master Resources tab has 707 resources and explicitly records reading status as not inferred from file inventory. Its copy-scope and title-check descriptions are acquisition evidence, not this lane's native reading. The live CSV manifest has 1,468 rows including folders; that is a different denominator from the index summary's file/resource counts.

## Reconciliation decisions

- Omrit Volume I copies A/B describe the same publication; different page counts do not make copy B Volume II. The newly held separate Volume II has its own identity.
- Wadi Hamam's 34-page introduction does not contain Mount Nitai Chapters 7–8. The later complete monograph supplies the containing source. It needs substantive chapter reading.
- Invisible Synagogues' three-page excerpt is incomplete. A Vision of the Days supplies the 2024 containing chapter; the Hebrew 2022 article is a distinct publication. Treat reused field observations as one ancestry.
- Huqoq 2023 remains front matter and opening printed p.48 only. Its missing chapter cannot be closed by the separate Huqoq hiding-complex article.
- Shaar-HaAmakim's 12 selected pages and the Kirzner/Hater/Torge short reports do not supply the missing monograph. Preserve their individual source identities.
- Cave 11Q's publisher sample is incomplete; the later 2019 monograph is separately held. The recorded cover/date discrepancy needs the copyright/title information, already recorded in copy scope.
- Ancient Synagogues Revealed 1981 is distinct from Ancient Synagogues Revealed: 1981–2022 (2023).
- The latest Remaining resource gaps ONLY document supersedes the older Missing resources and incomplete copies document for acquisition state. Its top intake update records five newly filled containing sources plus Frumkin's published chapter. Acquisition does not close archaeological questions.

The exact normalized-title search across repository research Markdown/JSON/CSV, excluding Drive indexes/manifests, found one contextual title pointer for Umm edh-Dhiyab in phase2 online_titles.csv. No latest-batch document's full reading was established through that search. The CSV preserves this retrieval result without assigning unread/read by assumption. Prior observations, previews and related field campaigns still require the owning evidence lane's exposure check.

## Archive paths and permissions

Preserve original source IDs and SHA256 per received raw file. Research prose/evidence belongs under the existing affected record when appropriate; root owns shared repository integration. New intake coverage may be placed under research/sources/new_batch_2026-10-13/ with a matching atlas mirror if published through that directory.

Per-source page/figure registers must retain title, authors, edition, printed and viewer pages, figure identifiers, source URL, raw-file hash, asset hash, crop/render details, captions, scales/north arrows, attribution and reuse status. Use research/assets/plans/<source-name>/ only for source rasters whose reproduction is permitted; mirror any public assets under atlas/research/assets/plans. Otherwise retain a link and retrieval record in the public repository and persist private supplied-source inspection derivatives on Drive.

This lane rendered all 83 supplied pages across Arumah 2011, Kh. el-Hamam 2023, Frumkin 2014 and the Amit–Gibson 34-page author draft at 150dpi without cropping. Whole-page derivatives preserve captions, scale bars, north arrows and surrounding printed context where present. Rendering does not establish substantive reading. The separate evidence lane owns its page/figure and observation review. Public redistribution permission remains unestablished. These inspection derivatives are private archive material; do not commit them publicly.

The separately rendered dissertation selection preserves viewer5–7,36–39,50–55 and73–88, 29 whole pages, with an unchanged-page PDF extract. The manifest records both thesis and incorporated-article pagination. Root read the incorporated Deir Sam’an article and selected context pages; full dissertation reading and full dissertation figure coverage are not claimed. Article1 repeats the separately supplied IEJ2023 field observations and adds no independent corroboration.

Existing figure backfill history remains in research/assets/plans/README.md and MISSING.md. Later appendices there have already recovered Twin Cave B1, Hyrcania/Doq source plans and Galor L138; the historical opening missing lists must not be treated as current gaps.

## Source index paths to update

The repo's research/sources/drive_manifest.csv and drive_index.md predate the latest holdings names and acquisitions. Rebuild using tools/drive_navtree.py after the new Drive deliverable is created rather than installing this lane's inventory as a substitute. Keep required paired atlas source records aligned. Update ACTIVE_TEST, relevant backlog question and outcome ledger only for a grounded evidence/status change supplied by an evidence reader.

Source indexes used: master spreadsheet https://docs.google.com/spreadsheets/d/1YOxcF5Toa3Uxsrs3McsiqBKtl2SNF0_FF8XsdQJg4Gw/edit ; acquisition history https://docs.google.com/document/d/1yZSS7Hi5Kcnxr9F_FVyViGOCuf5C8tWVe2RtxTQ42cY/edit ; current gaps https://docs.google.com/document/d/15spcwfaH9RUvfls4LZrcWBTLcgOT5QF4bWsZ7U-tKjs/edit .

**Last session: obtained** — reconciled latest 72 stable PDF identities with current acquisition scopes and separated source possession from established reading; private water-source derivatives preserve complete page context with source/asset hashes.
