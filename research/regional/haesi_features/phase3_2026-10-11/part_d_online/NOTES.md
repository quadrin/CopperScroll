# HA-ESI phase 3, part D: online tier T3 (Jerusalem), positions 81–662

Work in progress; this file is updated with each batch commit.

## Scope and rules

- Scope: online tier T3 (titles beginning "Jerusalem"), positions 81–662 of 662 in the frozen order of `../../phase2_2026-10-10/online_screen.csv` (ascending SHA-256 of the report id). Positions 1–80 were read in phase 2 and are not re-coded.
- Rules: phase-2 frozen plan (`../../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c08…b3be`) with amendments A1–A4, under the phase-3 scope freeze (`../PLAN.md`, commit 4d8325e, SHA-256 `312c2733…5cf2`). Classes and in-window rule as plan §5–§6; A4 coding notes followed (hedged datings follow the named period; partial-overlap ranges unknown; modern-dated features coded no).
- Exposure: every report coded here was first read in this session, after both freezes (`unexposed at freeze`).
- Held cave areas and the Tell es-Sultan strip (plan §7) do not occur in T3 so far; no report was held.

## Access route

- hadashot.iaa.org.il in the owner's Chrome (Claude in Chrome), one tab created for this session, one report page at a time. No downloads; no linked files (for example the full text of an "Extended report") were opened.
- Pacing: each load is followed by a script step that waits until at least 3 s after that page's navigation start (and until the page has finished loading) before anything else happens, so successive loads are at least 3 s apart; in practice the gap was much longer.
- No Cloudflare or other check appeared. The extension disconnected once (before position 85); after reconnecting, the already-loaded page was read without reloading.

## Text read and hashes

- The report body was read with the page-text tool (`get_page_text`).
- The hash is SHA-256 (UTF-8) of the `innerText` of the page's `.reportcontent` element with whitespace collapsed to single spaces and trimmed, computed in the page by a short script (no network request). This reproduces the phase-2 hash exactly: checked on the already-read T3 position 1 (HAESI-886, `9e50e172…5c65`, 2,930 characters), the only page reloaded outside the scope.
- From position 119 on, the script also returns the first 8 hex digits of SHA-256 of the hash string; `scripts/add_records.py` rejects a record whose typed hash does not match it (transcription check). Hashes for positions 81–118 were copied from the same script output without that check.
- HAESI-20777: the first hash attempt ran before the content element existed; the hash was taken again after the page finished loading (no reload). The script waits for the element from then on.
- HAESI-1738 and HAESI-1219: the page-text tool cut its output at 50,000 characters, inside the figure-caption list at the end; the body text was read in full and the hash covers the whole element.

## Coding notes (exploratory, no parameter change)

- Map references are recorded as printed. Misprints are handled as phase 2 did (A4): HAESI-25494 and HAESI-1801 (eastings or northings far from the named place) are located by name in Z4; HAESI-9546 printed a dash for the slash. Reports without a map reference (Giv‘ati Parking Lot, Wilson's Arch) are located by name in Z4. HAESI-25420 writes the northing first (handled by the phase-1 parser).
- Bathtubs in bathhouses are coded pool_reservoir with subtype "bathtub" (HAESI-347) so that they can be filtered out.
- Natural rock shelters with finds are coded cave_with_finds (HAESI-26591).
- Plastered installations whose function the report does not state are not coded; installations the report calls water-related are coded pool_reservoir.
- Where a survey or multi-area report gives different datings for features of one class, the class is split into rows by site or area (`site` field), so each row has one dating.
- Stepped plastered installations are coded ritual_bath whatever the excavator's label (plan §5), with the label in the subtype (for example "probably not a miqveh", HAESI-26474; "stepped pool", HAESI-26253).
- A function discussed only as one of several proposals in the literature is not imposed: the Hasmonean wall W4493 under Wilson's Arch (HAESI-25662) is not coded as a dam; the broad wall at the Tyropoeon outlet that the excavators themselves call "probably ... a dam" (HAESI-26253) is.
- Natural pits without cutting or plaster (HAESI-20771, HAESI-2027) and a plastered pit for "liquids" with water not stated (HAESI-25770) are not coded.
- A radiocarbon range straddling the window start (HAESI-25047 furnace, 205–90 BCE) and dates given as "2nd c. CE, at the latest under Hadrian" (HAESI-1219 cardo drains) are partial overlaps: unknown.

## Positions read

See `screen.csv` (status per position) and `summary.md`.

## Not read

Positions not yet reached are listed in `screen.csv` as `not read (time limit)`.
