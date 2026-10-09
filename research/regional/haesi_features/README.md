# HA-ESI features near the project's places

**What it is.** A coded list of cisterns, pools, channels, ritual baths, rock-cut installations, tombs, caves, walls and hoards that *Hadashot Arkheologiyot – Excavations and Surveys in Israel* records near the 48 located places of `places_v2.csv`, with a looks table for the search-effectiveness layer.\
**Main result.** Only a small part of the journal could be read by automation: 73 reports (7 volumes), giving 89 feature rows near places (23 dated in the window by the report itself). The in-window rows cluster in Jerusalem, at the Jericho palaces (Tulul Abu el-ʿAlayiq) and at Herodium. Outside Jerusalem, no report read records an in-window feature at a Koḥlit proposal; Mount Zion shares the Jerusalem rows (none on the hill itself).\
**What stays unknown.** 651 screened candidate reports were not read: the online reports (2004–2025) are closed to robots, and the portal PDFs sit behind a JavaScript check. Silence at Qumran, Feshkha, Nebi Musa, Beit Kahil, Kuḥla and other places is silence of the readable corpus, not absence.

Exploratory work, 9 October 2026 (worker haesi-features). No identification claim. No registered result, outcome count or test changes. Labels: EVIDENCE (what a report says), INFERENCE (our reasoning), CLAIM (an author's assertion).

## Freeze record

- search_plan.json SHA-256: `eb6a1de4139a460b735cf37a0177952d49d8ca7cd5ba71d6b2afdbd3dce807e9`, frozen 2026-10-09T22:18:50Z. No table of contents had been screened and no report read at that time. Before it, only robots.txt, the portal sitemaps and the item pages (metadata) were fetched.
- The plan has not changed since. Four post-freeze changes affect access and screening only. Each is labelled in the tables:
  - **D1 access.** The portal PDFs (`/cgi/viewcontent.cgi`) answer HTTP 403 with a Cloudflare JavaScript challenge. It was not bypassed. Instead, the owner's Google Drive copies listed in `research/sources/drive_index.md` were read with the Drive text tool (read only). The plan had set these copies aside as duplicates.
  - **D2 screen S2.** The frozen Hebrew matcher needs a space before a name, so titles such as "חפירות **ב**מדבר יהודה" were missed. S2 also allows one or two prefix letters (ב ה ו ל מ כ ש). It added 41 candidates.
  - **D3 screen S1h.** The portal tables of contents are truncated (ESI 9 lists 59 of 105 reports; ESI 15, 77 of 98). In the readable volumes the same name rules were also applied to the volume's own headings.
  - **D4 screen S3.** Every map reference in the readable texts was converted. Reports within 5 km of a place or inside a region box were added, whatever their title.

## Sources and access

| Corpus | Where | Status |
|---|---|---|
| HA (Hebrew) 1–108, 1961–1998 | publications.iaa.org.il/ha_hebrew_series (86 items) | Tables of contents screened. PDFs behind a JavaScript check. HA 40, 45, 59–60 and 76 read from the owner's Drive copies (HA 45 lacks printed pp. 20–25). |
| ESI (English) 1–20, 1982–2000 | publications.iaa.org.il/esi_english_series (21 items) | Screened. ESI 9 and 15 read from Drive copies. ESI 2, 3, 5, 6 and 7–8 exist on Drive, but the Drive tool returns no text (files of 70–137 MB; download limit 10 MB). ESI 20 has no table of contents. |
| HA-ESI 109–115, 1999–2003 | publications.iaa.org.il/ha_esi_bilingual_series | Screened, not readable. HA-ESI 116 has no PDF. |
| HA-ESI 138, 2026 | publications.iaa.org.il/ha-esi/vol138 | All 85 article pages fetched (HTML, allowed by robots.txt). 14 coded. |
| HA-ESI online reports, 2004–2025 | hadashot.iaa.org.il (www.hadashot-esi.org.il redirects there) | Not read. robots.txt says `User-agent: * Disallow: /`. 16 web-search queries listed candidates only (`data/unread_online_candidates.csv`). |

- robots.txt SHA-256: hadashot.iaa.org.il `15352e55…c7178`; publications.iaa.org.il `886cdc4e…8b2a` (full values in `search_plan.json`).
- `data/corpus.csv` lists all 119 items with their access status and the SHA-256 of each Drive text read.
- Every report read has the SHA-256 of the text span read in `reports.csv`. No PDF, image or text dump is stored in the repository. No image was opened.

## Method

1. **Screen.** 5,738 table-of-contents items were matched against the frozen name lists (English and Hebrew) for 48 places and 8 regions. S1 found 736 candidates, S2 41 more. False positives on author names (35) are marked, not deleted (`dropped.csv`).
2. **Read.** Every candidate in a readable volume was read, plus S1h and S3 finds: 73 reports.
3. **Locate.** Map references were converted as W2B does: Old Israel Grid with EPSG:28191 (`geo.py`, checked against W2B's Qumran and IV/17 controls), New Israel Grid with EPSG:2039. Three references printed in reverse order were corrected and flagged. A report without a map reference counts only at the place its title names (`name only`); 17 Jerusalem reports name no listed place and stay unlocated (`features_unlocated.csv`).
4. **Code.** One row per report and feature type. The period is the report's words. `dated_in_window` is yes only where the report dates the feature itself to the Hasmonean–135 CE window; "Hellenistic", "Roman" or a partly overlapping range is unknown. Each quote has 12 words or fewer and was checked against the text read.
5. **Looks.** `looks_haesi.csv` has the columns of `research/models/search_effectiveness/looks.csv`. One row per (report, covered place, candidate entry of that place). A report covers a place if it lies within max(sigma_km, 0.3 km) plus the map-reference precision, or names the place. Relation `HAESI-COVER`; result `reported` if a coded feature lies at the place, else `silent`. All four detection numbers are null with an UNKNOWN basis; stated areas and depths are in `looked_at`.

## Results

Reports read: 73. Within 2 km of a place: 24. Between 2 and 5 km: 9. Located by title name: 17. Region by title: 3. Unlocated: 17. Beyond 5 km: 3.

Feature rows near places: 89 (dated in window: yes 23, no 33, unknown 33). Unlocated Jerusalem reports add 26 rows (11 in window) in `features_unlocated.csv`.

### Features per place (from `summary.md`)

Jerusalem places lie within 2 km of each other, so their rows overlap. Read the Jerusalem lines as one cluster.

| place_id | reports ≤2 km (incl. name) | reports ≤5 km | feature rows (≤2 km) | in window yes / no / unknown | types |
|---|---|---|---|---|---|
| Jerusalem cluster (13 jer_* places and mount_zion) | 8–13 each | 17–20 each | 19–30 each | e.g. jer_tyropoeon 9 / 10 / 11 | cisterns, channels, rock-cut, tombs, walls, 2 hoards |
| ramat_rahel | 1 | 17 | 1 | 1 / 0 / 0 | tomb |
| tell_el_ful | 2 | 7 | 3 | 0 / 0 / 3 | rock-cut, cave, wall |
| tell_es_sultan | 1 (name) | 2 | 1 | 0 / 1 / 0 | wall (Early Bronze Age) |
| jericho_palaces | 2 | 2 | 4 | 3 / 0 / 1 | pools, aqueducts, ritual bath |
| choziba | 1 | 1 | 1 | 0 / 0 / 1 | stepped pool |
| nuweimeh, doq, jericho_area, tell_el_qos, iv17_abu_saraj, kh_yanun | 0 | 1 | 0 | – | none |
| buqeia | 1 (name) | 1 | 2 | 0 / 0 / 2 | check dams, forts |
| ein_ghuweir | 1 (feature sites) | 1 | 3 | 0 / 1 / 2 | cave, enclosure wall, graves |
| ein_samiya | 1 | 2 | 1 | 0 / 1 / 0 | fortifications |
| carmel_siah | 1 | 1 | 1 | 0 / 1 / 0 | rock-cut vat |
| natuf | 2 | 3 | 6 | 0 / 6 / 0 | Chariton monastery water system, walls |
| tekoa_herodium | 2 | 3 | 4 | 3 / 0 / 1 | Herodian pool, aqueduct, walls |
| gerizim | 4 (name: Shechem) | 5 | 3 | 0 / 1 / 2 | tombs, MB walls |
| beth_shean | 8 | 8 | 4 | 0 / 3 / 1 | channel, sarcophagus, walls |
| ibziq | 1 | 1 | 1 | 0 / 0 / 1 | kokhim tomb (1st–2nd c. CE) |
| beth_horon | 1 (Lower Beth Horon) | 1 | 2 | 0 / 1 / 1 | Roman tomb, Byzantine cisterns |

By type (89 rows; in window in brackets): walls and towers 24 (3), tombs 14 (7), rock-cut installations 13 (4), cisterns 12 (0), channels 12 (5), pools 7 (2), caves with finds 4 (1), hoards 2 (0), ritual baths 1 (1).

### Dated-in-window features (23 rows)

- Jerusalem (15 rows): Second Temple tombs (Rehavya, Arnona, Peace Forest, Mt. Scopus B, Supreme Court site, Mount of Olives); the Second Temple aqueduct and a Hasmonean site at the Lower Aqueduct tunnel; Herodian drainage channel and Temple Mount south wall (HA-ESI 138); Late Second Temple quarries (Shemuʾel Ha-Navi St., Naḥal Sanhedrin); the Low-Level Aqueduct (cited at the Western Wall Plaza); Second Temple wine press and tomb at East Giloh (2.3 km).
- Jericho palaces, HA 59–60 p. 37: Hasmonean pools, aqueducts and a miqveh (name only).
- Herodium, HA 45 pp. 27–28: Herodian pool, Artas aqueduct and retaining walls (name only).
- Judean Desert shore, HA 40 pp. 26–27 (Bar-Adon): caves with Second Temple finds (Wadi Mukaddam, Ḥasasa, Murabbaʿat) and a fort at the Mazin / en-Nar outlet with Hasmonean sherds (region only).

### Places with no read report within 5 km (silence, not absence)

mar_saba, hyrcania, ain_duk, kuteif, jordan_ford, asla, kh_qumran, wadi_qumran, kh_salhab, muhalhil, beit_kahil, kuhlah, ein_feshkha. Not screened: transjordan (outside HA-ESI coverage) and jer_shaveh (a mixture; see its components).

## Reports most relevant to the open questions

- **Koḥlit at Tell es-Sultan.** ESI 15 pp. 68–70 (Riklin, L-549, 1992): six squares on the tell, south of Kenyon's Trench I. Early Bronze Age city wall only. INFERENCE: the west side of the tell, not the strip to the north. Unread: HA 43 p. 17 (Jericho, Shantur 1972); HA 27 pp. 17–18 (site near Jericho, Landes); ESI 5 p. 17 and HA 88 p. 17 (Jericho 1986); HA 39 p. 22 (conservation at Tell Jericho).
- **Koḥlit at ʿEin Samiya.** HA 76 p. 19 (Zohar, Tel Marjama, OIG 1816/1554, 0.6 km): five squares c. 20 m north of the spring; casemate, massive and cyclopean walls (MB II, Iron Age). No pool, cistern or tomb is reported. EVIDENCE for looks L15/L16 (same campaign). Unread: HA 36 pp. 11–12 and HA 37 p. 23 (ʿEin Samiya, Shantur); HA 57–58 p. 23 (Kh. Marjama, A. Mazar); HA 65–66 p. 28.
- **Koḥlit at ʿEin el-Ghuweir.** HA 40 pp. 26–27 (Bar-Adon 1971): an Iron Age II cave above the spring; c. 80 m north of the reserve an Iron Age II house, an enclosure wall over 100 m long, and graves "typical of the Judean Desert sect" (no period named, so unknown). Unread: HA 30 pp. 29–30 (sites between ʿEin Feshkha and ʿEn Gedi).
- **Koḥlit at Kh. Yanun.** HA 45 p. 19 (Damati and Ilan): a road survey 4.5–5 km away; a Roman road towards Yanun village, towers and pools, undated.
- **Koḥlit on the Carmel.** HA-ESI 138 no. 66 (Ḥorbat Qasṭra South, 1.6 km): a hewn vat, Byzantine by comparison. Unread and directly on target: HA 97 p. 93 "Neve David (Naḥal Siaḥ, Haifa)" and HA 87 p. 18 "Haifa, Neve David".
- **Koḥlit at Mount Zion.** HA 40 pp. 19–20 (Broshi): Second Temple houses, no coded feature. HA-ESI 138 nos. 5 and 58: Byzantine cisterns, channels, a coin hoard; two undated cisterns south of David's Tomb.
- **Achor (entries 1, 17).** HA 45 pp. 34–35 (Buqeiʿa, Stager 1972): Iron Age II forts at Kh. Abu Tabaq and Kh. es-Samra, three farms with check dams; Roman sherds at Samra but no Roman settlement. Nothing read at Nuʿeima or ʿAin Duk. Unread: HA 83 p. 34 (Naʿaran, Hizmi); HA 33 p. 8 (Naʿaran synagogue); ESI 5 pp. 110–111 (Wadi Nuʿeima).
- **Sekakah (entries 20–23).** CLAIM (Bar-Adon, HA 40): "assuming Qumran is Sekakah". Nothing read at Kh. Qumran. Unread: ESI 13 p. 55 (Qumran Caves, Patrich); ESI 18 p. 129 (Ḥorbat Qumran, Porath); ESI 16 p. 80 (Map of Qalya survey); HA 27 p. 18 (Kh. Samra, Bar-Adon); HA-ESI 132 and 135 Qumran reports online.
- **Jericho and Wadi Qelt.** HA 59–60 p. 37 (Netzer, Tulul Abu el-ʿAlayiq 1975–76): Hasmonean pools, original and bypass aqueducts, miqvaot (all in window). HA 59–60 p. 38 (Nuṣeib ʿUweishira, 0.9 km): a stepped pool of a type "common in late Second Temple remains", stratum undated. Unread: HA 50 p. 11, HA 54–55 pp. 21–24 (palaces, Tell es-Samarat, Kypros), HA 83 p. 36, HA 69–71 p. 83 (Wadi Qelt), HA 99 p. 45 (Map of Wadi Qelt survey, Sion), HA 77 p. 57 (ancient roads to the Jericho plain).
- **Siloam.** ESI 15 pp. 75–77 (De-Groot 1991): ashlar walls "associated with the complex of retaining walls which surrounded the Siloam pool", undated in the text read (part of p. 75 is missing from the text layer); a street bedding with end of Second Temple pottery. HA-ESI 138 no. 4 (Givʿati): Iron Age installations and moat. Many online City of David reports are listed unread.
- **Gerizim.** Only Shechem reports were read (tombs on Mt. Ebal, MB fortifications at Tell Balata, a Roman mosaic, Roman/Hellenistic tombs near Tell Balata); none on the mountain. ESI 15 pp. 57–58 (Kh. Halas, 4.9 km): Byzantine fort and an undated rock-cut cistern.
- **IV/17.** No read report within 2 km. Unread cave surveys: ESI 6 pp. 39–43 and HA 90/93 pp. 39–43 (caves of the Judean Desert and Samaria 1985–86); ESI 3 p. 40 and HA 84 p. 40 (Patrich, refuge caves).

**Protected strip north of Tell es-Sultan.** No report read describes it. The unread Jericho items above (HA 27, HA 39, HA 43, HA 88, ESI 5) may describe the tell's surroundings; their content is unknown. A person who opens them must check this and, if a text describes the strip, record only its citation. No map, plan or photograph was opened.

## For the integrator

- Join `looks_haesi.csv` on (entry_id, place_id). It has 100 rows (91 reported, 9 silent) over 19 places and 35 entries. It validates with `search_model.validate_looks` (test). With null numbers every factor is 1, so it changes no posterior.
- `features.csv` gives denominators for rarity counts only for the readable corpus. Most of the journal is unread (651 candidates; P1 145, P2 91, P3 425 in `dropped.csv`).
- Proposed change to a shared file: none required. If the integrator adds rows from `looks_haesi.csv` to the looks table, PLAN.md hashes of `research/models/search_effectiveness/` must be recomputed under a new plan.

## Needs a person with a browser

1. HA-ESI map search, https://hadashot.iaa.org.il/SearchMap_eng.aspx: list report IDs inside the Jericho oasis, Qumran–Feshkha strip, Buqeiʿa, ʿEin Samiya, Yanun, Nebi Musa, Siloam and Kidron boxes (`search_plan.json` regions).
2. https://hadashot.iaa.org.il/images/Masterlist2024.pdf (a list seen in the search index; content not seen).
3. The portal PDFs for the P1 rows of `dropped.csv` (a browser passes the JavaScript check). First: HA 97 p. 93; HA 36 pp. 11–12; HA 37 p. 23; HA 57–58 p. 23; HA 30 pp. 29–30; HA 27 p. 18; HA 43 p. 17; ESI 13 p. 55; ESI 18 p. 129; HA 99 p. 45; HA 83 pp. 34, 36.
4. The online reports in `data/unread_online_candidates.csv`.

## Failed or blocked links

- https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1016&context=ha_hebrew_series (HA 40) and ?article=1001 (HA 1): HTTP 403, Cloudflare page "Just a moment... Enable JavaScript and cookies to continue" (2026-10-09T22:20Z). All portal PDFs are assumed to behave the same; no other PDF was requested.
- https://hadashot.iaa.org.il/ and https://www.hadashot-esi.org.il/: not requested; robots.txt disallows all agents except named search engines. DOIs of the form 10.69704/jhaesi.* redirect there.
- Google Drive: ESI 02, 03, 05, 06 and 07–08 (IDs in `data/corpus.csv`): the text tool returned empty text; the download tool refused files over 10 MB.

## Web-search queries (candidates only, not read)

Domain filter hadashot.iaa.org.il and hadashot-esi.org.il. Queries: Jericho excavation report; Jericho Tell es-Sultan excavation; Qumran excavation report; ʿEin Feshkha; Wadi Qelt or Naḥal Perat aqueduct survey; "Jericho" Volume Year; Jerusalem City of David Siloam pool; Jerusalem Kidron Valley or Silwan or Mount of Olives burial cave; Judean Desert caves survey Jericho cliffs; Mount Zion; Haifa Naḥal Siaḥ or Kababir; Herodium or Tekoa; Bet Sheʾan spring; Kokhav Ha-Shaḥar or ʿEin Samiya or Kafr Malik; Mount Gerizim or Shechem or Nablus; Nebi Musa or Mizpe Yeriḥo or Naʿaran; Hyrcania or Buqeiʿa or Mar Saba or Naḥal Qidron. West Bank places gave no relevant hit.

## Files

| File | What it is |
|---|---|
| `search_plan.json` | Frozen plan: names, regions, radii, feature types, coding and stop rules |
| `features.csv` | Feature rows near places (89) |
| `features_unlocated.csv` | Feature rows of read reports that cannot be placed (26) |
| `reports.csv` | Every report read (73), with location, status and text SHA-256 |
| `dropped.csv` | Every candidate not coded (737), with one reason and a tier |
| `looks_haesi.csv` | Looks rows in the looks.csv schema (100) |
| `summary.md`, `summary.json` | Generated tables |
| `data/coding_*.json` | Hand coding per volume (the build input) |
| `data/screen_candidates.csv`, `data/screen_s3_coords.csv` | Screen results (S1, S2; S3) |
| `data/corpus.csv`, `data/drop_rules.json`, `data/unread_online_candidates.csv` | Corpus status, drop rules, unread online candidates |
| `scripts/screen_toc.py`, `scripts/screen_coords.py`, `scripts/geo.py`, `scripts/build.py` | Screen, coordinate screen, grid conversion, build |
| `tests/test_haesi.py` | Tests |

## Run and test

From the repository root (Python 3 with pyproj; the looks test also uses numpy, as the W2B model):

```sh
python3 -I -B research/regional/haesi_features/scripts/build.py
python3 -I -B -m unittest discover -s research/regional/haesi_features/tests -t research/regional/haesi_features
```

The tests check the plan hash against this README, the table schemas, quotes of 12 words or fewer, report IDs, the W2B grid controls, determinism (two builds byte-identical and equal to the stored files) and that `looks_haesi.csv` passes `validate_looks`. The screens need the downloaded item pages and are not rerun by the tests (`screen_toc.py <cache> <out> [--s2]`, `screen_coords.py <out.csv> <label>=<text> ...`).

## Limits

- Title screens miss reports named after a route or an unlisted place. The portal tables of contents are truncated, so unread volumes have incomplete candidate lists.
- OCR errors in the Drive text layers remain in some Hebrew quotes (noted per report).
- One location conflict: ESI 15 p. 55 (Ḥorvat Raʿash) names Kokhav Yaʾir, but its map reference lies 4.6 km from ʿEin Samiya. It is kept with a flag.
- Name-only locations carry no distance. Lower Beth Horon is coded at the listed Upper Beth-Horon place by name; INFERENCE: it lies c. 2–3 km away.
