# Amendments to the frozen dedupe plan

`DEDUPE_PLAN.md` (commit bf4320f) is not edited. Changes made after the freeze are listed here. Each says what was seen when it was made.

## A1. Permit parsing (R4), before any pair was compared

Seen: a count of permit-field formats with digits masked (for example `A-9999`, `S-999/9999`, `License No. G-99/9999`, `Judea and Samaria License No. 99-99-9999`). No permit value was compared with another.

Problem: the frozen rule splits the permit field at `/`. Permits of the form `S-123/2005` or `G-12/2010` contain a slash, so the year after it would become a separate "permit" and could link unrelated reports of the same year.

Change: first the words `Judea and Samaria License No.`, `J&S License`, `License No.` and `License` are removed (case ignored); then the field is split at `,` `;` and ` and ` only (not at `/`). Each part with a digit is one permit, written with letters and digits only, upper case (so a leading or trailing `*` drops out). The place test is still required.

Effect: stricter than the frozen rule (fewer possible links). Exploratory.

## A2. HA-to-ESI volume correspondence for R2, after the first full run

Seen: the first full run's `pair_candidates.csv` (242 listed pairs; 112 flagged ambiguous) and the part-B crosswalk. Multi-season sites (City of David, Robinson's Arch, St. Peter in Gallicantu, Mamilla, ʿEn Gedi, Mount Zion) gave several passing ESI candidates per Hebrew report, and the one-to-one choice by year difference paired some reports with a different season's English report (for example HA 73, City of David 1979, with ESI 2, City of David 1982/83; the Golden Gate and Ophel Road reports of HA 106–107 crossed).

Change: R2 also requires that the ESI volume be the English volume of the report's HA volume. The correspondence is derived inside the build, by rule, and written to `ha_esi_volume_map.csv`:

1. Evidence items: (a) every row of `../phase3_2026-10-11/part_b/already_coded_crosswalk.csv` whose English report is in an ESI volume (the part-B reader's own Hebrew–English pairs); (b) every R2 link of a first pass of the frozen rules (no volume condition, no manual decisions) in which both reports had exactly one passing candidate.
2. For each HA volume, the ESI volume with the most evidence items is its English volume, if it has strictly more items than any other ESI volume. A report of a mapped HA volume is paired by R2 only with reports of its English volume. A report of an HA volume without such evidence (HA 77 and all volumes before it) is not paired automatically: its R2 pairs that pass the frozen tests are listed for review (§4.3) and linked only by a manual decision.

The year window, author test, place test and one-to-one rule stay as frozen. Manual decisions (§4.3) still override for a listed pair; a manual `same` decision on a pair outside the correspondence is applied as a manual link.

Effect: removes cross-season pairings at multi-season sites. Exploratory (chosen after seeing the first run).

## A3. R1 (identical citation) also needs the author and place tests, after the first full run

Seen: the five R1 links of the first run. All five joined two different short reports printed on the same page whose titles share a name key: ESI 1 p. 54 (ʿIsawiye; ʿIsawiye, survey of a new road; 610 m apart, different authors), ESI 13 p. 125 and HA 100 p. 109 (Morasha, City Hall Plaza and New Gate; 969 m apart), HA 34–35 p. 12 (Beit Sahur tomb and Naʿaran synagogue; the shared key came from the group heading "Judea and Samaria"), HA-ESI 112 p. 53* (Peẓaʾel East and North; 2.6 km apart). No report was found coded twice.

Change: R1 links two reports only if, besides the same series, volume, first page and name key, the author test and the place test (§4.1) also pass.

Effect: removes these five links. Exploratory.

## A4. S2 respects the readers' named-place hints, after the first full run

Seen: the first run's `sites.csv` and the names behind the commonest keys. Rows without coordinates are joined by key alone (S2), with no distance check, so one key can cover two places. The worst case for this project: the key `jericho` put ESI 15 pp. 68–70 (Tell es-Sultan; coded `name only (tell_es_sultan)`) in one site with the winter-palace reports at Tulul Abu el-ʿAlayiq (coded `name only (jericho_palaces)`), about 2 km away.

Change: when a row's `coordinate_source` carries a phase reader's named-place hint (`name only (<place_id>)` or `feature site name (<place_id>)`), S2 does not join it with a row that carries a different hint. Within one zone and key, rows are split by hint; if the key's rows carry one hint only, rows without a hint join them as frozen; if they carry several hints, each hint forms its own group and the rows without a hint form one more group. Each group then joins a located site as frozen (only if exactly one located site has that key in that zone). No new joins are made by hint alone.

Effect: splits some name-only sites; never merges more. Known key collisions that remain (for example `kerem` for ʿEn Kerem and Bet Ha-Kerem rows without coordinates) are listed in the README. Exploratory.
