# Online imagery for the atlas places — 17 October 2026

**Evidence sought this session:** openly licensed photographs (Wikimedia Commons, Library of Congress Matson) and embeddable video and 3D references for the atlas places, plus a Hebrew and Arabic search for the features no English-language source shows. **Obtained.**

Exploratory. Photographs and videos show what a place looks like and where a feature is. They do not date a construction or use phase, and none of them changes a reading, an identification or a confidence level.

## What is in the atlas now

- **Photo gallery per place.** 160 photographs at 31 places, beside the four existing annotated scenes. 113 are modern (Commons) and 47 historical (Matson, 1898–1977, 13 of them 1931/1937 air views). Archive set and manifest: [site-photos-2026-10-17](../../assets/plans/site-photos-2026-10-17/README.md). Every image was looked at before its caption was written; captions say what the photograph does not show.
- **Curated site videos.** 58 YouTube videos at 26 places (62 place links), embedded from youtube-nocookie.com. Each was checked with YouTube's oEmbed service on 17 October (embedding allowed). They stay their makers' work; the atlas only embeds them. Data: `atlas/app/atlas-site-media.json`.
- **3D models.** 28 Sketchfab models at 15 places, shown in Sketchfab's own viewer when selected. Title, author, licence, download flag and face count come from the Sketchfab API (17 October). 11 are CC BY, 2 CC BY-NC and 1 Sketchfab Free Standard, all downloadable; 14 have no reuse licence and are view-only. None is georeferenced.
- Code: `atlas/app/atlas-ground.tsx` (gallery, 240 px thumbnails), `atlas/app/atlas-map-references.tsx` (videos, 3D models), built by `tools/build_site_gallery.py`.

| Place | Modern photos | Historical | Videos | 3D models |
|---|---|---|---|---|
| jer_temple | 2 | 0 | 3 | 1 |
| jer_east_gate | 6 | 4 | 4 | 0 |
| jer_se_corner | 5 | 4 | 3 | 0 |
| jer_south_wall | 4 | 8 | 5 | 1 |
| jer_kidron_mon | 5 | 1 | 2 | 11 |
| jer_kidron_east | 5 | 0 | 2 | 0 |
| jer_gethsemane | 4 | 1 | 0 | 0 |
| jer_siloam | 3 | 4 | 6 | 1 |
| jer_bir_ayyub | 1 | 3 | 0 | 0 |
| jer_bethesda | 5 | 2 | 2 | 1 |
| jer_tyropoeon | 0 | 1 | 0 | 0 |
| jer_tombs_kings | 4 | 4 | 1 | 0 |
| jer_givati | 3 | 0 | 1 | 0 |
| ramat_rahel | 3 | 0 | 3 | 1 |
| tell_el_ful | 3 | 2 | 1 | 0 |
| mar_saba | 4 | 5 | 1 | 3 |
| hyrcania | 3 | 0 | 10 | 1 |
| buqeia | 3 | 0 | 0 | 0 |
| natuf | 4 | 0 | 0 | 0 |
| tekoa_herodium | 5 | 1 | 3 | 0 |
| doq | 2 | 0 | 0 | 1 |
| jericho_palaces | 3 | 0 | 0 | 0 |
| ain_duk | 2 | 1 | 0 | 0 |
| choziba | 4 | 2 | 2 | 0 |
| jordan_ford | 3 | 1 | 1 | 0 |
| kh_qumran | 4 | 3 | 4 | 3 |
| wadi_qumran | 4 | 0 | 4 | 3 |
| gerizim | 5 | 2 | 3 | 0 |
| beth_shean | 5 | 1 | 1 | 1 |
| beth_horon | 3 | 2 | 0 | 0 |
| ibziq, kh_salhab | 0 | 1 (regional air view) | 0 | 1 (comparison tomb near Nablus) |

## Searches

- English-language search of image, video, 3D and platform sources, with licences: [sources_list.md](sources_list.md).
- Hebrew and Arabic search for the gaps: [hebrew_arabic_search.md](hebrew_arabic_search.md).

## Frozen tests

- No photograph of the Copper Scroll was opened. Abu Saraj IV/17 and Twin Cave were not searched for.
- SULTAN-1: a collection worker opened eight Commons files that may show the plain north of Jericho, deleted them and did not describe them. They are recorded as exposed, and about 30 more sources are listed as reserved and not opened: [online_sources_2026-10-17.md](../../assessments/kohlit_chain/online_sources_2026-10-17.md). No curated video or photograph is attached to Tell es-Sultan or the Jericho oasis.

## Checks

- Gallery build: every archive JPEG matches its manifest hash; licences limited to PD, CC0, CC BY, CC BY-SA and LoC "No known restrictions on publication" (checked per item); no duplicate source file; two files that repeated existing annotated scenes were dropped.
- `tsc --noEmit` passes. `check-pages-payload.mjs` passes on a Pages-layout copy of the build (83.1 MiB). The Docker-based `check-pages-build.sh` could not run (no Docker daemon in the session).
- Browser check (Playwright, Chromium 1248, desktop 1440 × 950 and phone 390 × 844): gallery thumbnails, photo loading, credit lines, a video embed and a 3D embed at Mar Saba, the East Gate and Gerizim; no page errors and no missing local files.
- `check-map-browser.mjs`: phone passes. The desktop walk-collision step (line 89, 60 s wait) timed out in some runs on this branch and also on a build of unchanged main in the same sandbox (main: 4 passes, 1 timeout); every run passed when given 25 s more. It is a timing margin under software rendering, not a change in walking.

## Not obtained or still open

- Sketchfab downloads need a signed-in account (API 401), so no mesh is imported into the atlas's own 3D scenes. The CC BY meshes (Qumran caves, Mount of Temptation, Absalom's tomb, the Kidron valley, Zechariah's tomb, Masada, the Maresha Sidonian cave) can be downloaded from a signed-in browser.
- National Library of Israel, "Solomon's Stables / Écuries de Salomon", 1894 (public domain in Israel; credit: Lenkin Family Collection of Photography at the University of Pennsylvania Library, The Pritzker Family National Photography Collection, The National Library of Israel; ARC. 4* 2092 / 4159): https://www.nli.org.il/en/images/NNL_ARCHIVE_AL997009563568405171/NLI — Cloudflare browser check (HTTP 403) from the cloud session.
- Tyropoeon and el-Baqʿa: the Commons search was cut off by rate limits; the gallery has one historical photo for the Tyropoeon and none for el-Baqʿa.
- Commons serves only standard thumbnail widths, so modern photos are 1920 px (or 1280/960 px) on the long side. Matson images were taken from the TIFF masters and reduced to 2000 px.

## Copies in Google Drive

- 06 Imagery / Atlas site photos 2026-10-17: the 160 archive JPEGs, the manifest and the README (SHA-256 checked against the repository copy).
- 06 Imagery / SULTAN-1 reserved – do not open: 221 reserved files saved unopened ([record](../../assessments/kohlit_chain/online_sources_2026-10-17.md)).
- The Drive index (`../drive_index.md`, `../drive_manifest.csv`) was rebuilt with `tools/drive_navtree.py` on the owner's Mac. It also picks up the 16 October reorganization of the IAA portal volumes, which the previous index did not show.

## Source leads found (not read)

- *Kardom* (Ariel), "סיורים ב'כתף יריחו'", map of the Dok fortress (Kotar book 95087647): cisterns of about 1,800 m³, an aqueduct of about 1,000 m, a rock-cut moat to the west (entry 31). A trip summary gives the aqueduct as 500 m, citing Amit & Mashal.
- Israel Hayom, 19 February 2025: Hyrcania's Kidron aqueduct filled 2 pools and 26 cisterns; Gutfeld proposes a mausoleum on the hill opposite the summit (bears on Allegro's item 2 monument).
- Yad Ben-Zvi, "מבט אל העבר: חורבת הורקניה – סיכום שלוש עונות חפירה" (a summary of three excavation seasons).
- Taawon, "معبد جوبيتر" (Gerizim, Tell er-Ras): a platform of about 64 × 44 m; 65 steps of the stair to Neapolis survive.
