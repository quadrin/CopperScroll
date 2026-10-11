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
- The transcription check caught one error: for HAESI-35 the third and fourth 16-digit chunks had been typed in swapped order; the record was corrected before saving.
- HAESI-1738 and HAESI-1219: the page-text tool cut its output at 50,000 characters, inside the figure-caption list at the end; the body text was read in full and the hash covers the whole element.

## Coding notes (exploratory, no parameter change)

- Map references are recorded as printed. Misprints are handled as phase 2 did (A4): HAESI-25494 and HAESI-1801 (eastings or northings far from the named place) are located by name in Z4; HAESI-9546 printed a dash for the slash. Reports without a map reference (Giv‘ati Parking Lot, Wilson's Arch) are located by name in Z4. HAESI-25420 writes the northing first (handled by the phase-1 parser).
- Bathtubs in bathhouses are coded pool_reservoir with subtype "bathtub" (HAESI-347) so that they can be filtered out.
- Natural rock shelters with finds are coded cave_with_finds (HAESI-26591).
- Plastered installations whose function the report does not state are not coded; installations the report calls water-related are coded pool_reservoir.
- Where a survey or multi-area report gives different datings for features of one class, the class is split into rows by site or area (`site` field), so each row has one dating.
- Stepped plastered installations are coded ritual_bath whatever the excavator's label (plan §5), with the label in the subtype (for example "probably not a miqveh", HAESI-26474; "stepped pool", HAESI-26253; "storage pool" of an irrigation system, HAESI-2094).
- One rock-cut feature with successive uses dated differently is coded as one row per use, each with its own dating: HAESI-26501 (Iron Age burial cave, Second Temple miqveh, Byzantine–Mamluk shelter) and HAESI-26178 L501 (probable Second Temple miqveh, Roman–Byzantine cistern).
- Grave goods that a report calls "a cache" inside a sealed burial niche (HAESI-24894) are not coded hoard_cache.
- HAESI-2094 ('Ir Gannim) prints a northing c. 7 km south of the named streets; located by name (A4 handling). HAESI-1799 and HAESI-539 give no map reference and are located by name.
- A function discussed only as one of several proposals in the literature is not imposed: the Hasmonean wall W4493 under Wilson's Arch (HAESI-25662) is not coded as a dam; the broad wall at the Tyropoeon outlet that the excavators themselves call "probably ... a dam" (HAESI-26253) is.
- Natural pits without cutting or plaster (HAESI-20771, HAESI-2027) and a plastered pit for "liquids" with water not stated (HAESI-25770) are not coded.
- A radiocarbon range straddling the window start (HAESI-25047 furnace, 205–90 BCE) and dates given as "2nd c. CE, at the latest under Hadrian" (HAESI-1219 cardo drains) are partial overlaps: unknown.
- A terminus post quem alone is not a dating: the cistern plaster with an Archelaus prutah, dated "at the earliest" to the late 1st c. BCE–1st c. CE (HAESI-26426), is coded unknown.
- Where the report gives no dating statement for a feature and only reports pottery from its fill or covering soil, the feature is coded unknown with the pottery in `period` (as HAESI-25047): HAESI-22787 miqveh (1st c. CE fill), HAESI-587 winepress and stepped vat (Early Roman pottery in the vats).
- A quarry that the report places in a regional quarry field it dates to the Second Temple period is coded yes (as HAESI-12637): HAESI-631, HAESI-1844.
- A single step in a winepress collecting vat (HAESI-866 L103) is kept in the winepress row; a staircase descending into a plastered vat (HAESI-587 L1018) is coded ritual_bath, label in the subtype, as HAESI-2020.
- Built installations the excavator calls "possibly" pit graves are coded tomb_burial_cave with the hedge in the subtype (HAESI-25028). A rock-hewn moat is a fortification and is not coded (HAESI-268).
- A terminus ante quem alone is likewise not a dating: a rock-hewn pit sealed by Second Temple fill, dated "at the latest" to that period (HAESI-655), is coded unknown. Ranges such as "Hellenistic–Early Roman" (HAESI-230), "1st–2nd c. CE" (HAESI-25383) and "end of the Second Temple period to the Early Islamic period" (HAESI-26021) are partial overlaps: unknown.
- Rock-hewn pits and installations of unstated function are coded rockcut_installation (plan §5 class definition), for example HAESI-832, HAESI-25110 L101, HAESI-11627 L104; pits dug in fills, cesspits and built plastered installations of unstated function are not coded.
- A later quarrying of the same quarry (modern blasting holes) is a separate row coded no (HAESI-2014, 785, 5447, 25438).
- Coins that a figure caption calls a hoard are coded hoard_cache (HAESI-26022, Year 4 coins of the Great Revolt).
- Map-ref misprints located by name (A4): HAESI-432 (impossible NIG northing; the printed OIG value is consistent with the named street). HAESI-295 gives no map reference; HAESI-230 has no introduction, permit or map reference online and is located by its title. HAESI-25249 prints Old Israel Grid values without a label; the parser reads them as OIG.
- Map-ref misprints located by name (A4): HAESI-631 (northing c. 20 km south of Golda Meir Way) and HAESI-303 (Church of the Ascension; printed ref c. 60 km away). HAESI-162, HAESI-518 and HAESI-268 give no map reference and are located by name.

## Positions read

See `screen.csv` (status per position) and `summary.md`.

## Not read

Positions not yet reached are listed in `screen.csv` as `not read (time limit)`.
