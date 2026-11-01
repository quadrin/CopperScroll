# djd3, reader A: log (run 28)

- Source: Baillet, Milik & de Vaux, *Les "Petites Grottes" de Qumrân* (DJD III), Textes (1962), Archéologie I-IV (R. de Vaux), printed pp. 3-36.
- Access: Internet Archive loan `lespetitesgrotte0000unse`, owner's Chrome. The loan was active ("Renews automatically with continued use"). I worked in my own tab (id 299151203), which is now closed. I never clicked "Return now" and opened no other item.
- Started 2026-11-01T03:01:23Z (UTC). Reading finished 03:14:25Z. Files written 03:16:10Z.
- Output: `keyed/djd3_A.csv`: 73 rows, made up of 40 top-level rows (one per numbered site 1-40) and 33 sub-feature rows.

## Pages and figures read

- Viewer leaves n22-n55 hold printed pp. 3-36 (printed p. 3 = leaf n22, "Page 3 (22/343)").
- Pages read closely, with zoomed screenshots of every site entry:
  - pp. 3-6: history; site 6Q numbered 26 (p. 4 n. 1); geography; two ancient roads; numbering rules.
  - pp. 6-12: the numbered list, sites 1-40.
  - pp. 12-13: X-1, X-2, caves A and B, start of IV "Les objets".
  - pp. 13-17: pottery discussion, the jar and lid tables by site (pp. 14-15), other periods (p. 16), other objects (pp. 16-17).
  - p. 26: 6Q = site 26.
  - p. 27: the general statement on the "grottes naturelles de la falaise rocheuse".
  - pp. 32-36: conclusions. p. 33 sorts the numbered sites by type.
- Skimmed only:
  - pp. 18-25 and 28-29: pottery catalogue and drawings (figs. 2-6).
  - The rest of pp. 26-31 (5Q, 7Q-10Q). Some lines on 5Q at the top of p. 26 and the end of the 7Q entry on p. 27 were scrolled past unread. Both are outside scope.
- Fig. 1 (map, p. 5) was seen but not used. `position_basis` = `text_only` and `grid_printed` is blank, as the brief requires.
- Plates cited in entries (pl. II.2, II.4, III.1-2, VII.3, etc.) are outside pp. 3-36 and were not opened.
- I did not open the Copper Scroll text. Its find-spot appears only in the cave 8 excavation description (pp. 7-8), which is within the allowed pages.

## Keying decisions

- `site_name` = "site N". The source's equivalences are added: 8 = 3Q, 14 = 1Q, 19 = 2Q, 26 = 6Q.
- Sub-features carry a letter suffix in text order: chambers, storeys, entrances with their own dimensions, walls, passages, tunnels, platform.
- `page` is the page(s) of the list entry. Supporting pages (13-16, 26, 27, 32-34) are cited in `notes`.
- `n_openings`:
  - Keyed 1 when the entry names a single entrance or opening with a singular noun ("à large entrée", "Ouverture vers l'est", "une entrée en pente").
  - Left blank when the entry only says the cave opens toward a direction ("ouvrant vers le nord"). This applies to sites 7, 15, 18, 19, 20 and 36: direction keyed, no count.
  - Keyed 2 for 17 (opens N and S through a spur) and for 33 (opening E plus window N).
  - Keyed 0 for 29.d (chimney "sans ouverture au sommet").
  - Left blank for 8 and 14, where the original entrance is unknown or not reported.
- Entrance dimensions (4.a, 27.a, 39.a) are on separate `doorway` rows, so they are not mistaken for cave dimensions.
- "Profonde" (extent into the rock) is keyed as `depth_m` (sites 3, 5, 22, 39, 37.f).
- For "A × B" or "A sur B", `length_m` = A and `width_m` = B. Axes are not stated.
- Ash and deposit thicknesses (sites 1, 6, 8, 24) are deposits. They are put in `notes`, not in the dimension columns.
- `n_pillars` = 2 only at site 12: two stones set side by side propping the ceiling near the entrance. Confidence is medium. The five wooden posts of site 17 are loose objects (hut or tent poles, pp. 16-17) and are not keyed as pillars.
- `construction` = `natural` on the 37 top-level cave, shelter and fissure rows (all sites except 2, 16 and 35). This rests on the source's general statements: "grottes naturelles de la falaise rocheuse, qui ont été décrites plus haut" (p. 27) and "cavités naturelles de la falaise rocheuse", after which p. 33 lists the sites by number. Sub-feature rows are left blank unless built. Built rows: walls 9.a and 23.a, and building 35.
- `in_window`:
  - `yes` where the entry reports "genre Qumrân" pottery. The source dates this pottery to Khirbet Qumrân periods Ib-II, end of the 2nd c. BCE to 68 CE (pp. 13, 32).
  - `unknown` where the entry hedges ("peut-être", "aucun n'est sûrement", "rien qui soit sûrement").
  - `no` where it says "rien du genre Qumrân" or "plus tardifs que Qumrân".
  - Site 9 is `yes` because of its Herodian-type lamp (p. 15). Site 14 is `yes` from p. 14 (1Q jars). Site 35 is `unknown`: an Israelite building with Qumrân-type sherds on the surface.
- Relations to non-numbered features (aqueduct, ancient road, 'Aïn Feshkha, wady) are in `notes`, not in `relations`.
- Direction-only relations ("au sud-ouest du n° 12", "au nord du n° 25") are keyed as `next_to` with no `rel_bearing_deg`, because no number is printed.
- "Possibilité d'habitat" and the p. 33 type grouping are recorded in `notes`.
- Class uncertain:
  - 15 and 30, "creux du rocher", keyed `rock_shelter`. p. 33 calls 15, 21 and 30 "simples anfractuosités".
  - The site 28 top row is keyed `cave` because p. 33 lists 28 among "très petites grottes".

## Coverage

- Rows marked "class only": 2 (pottery deposit under fallen rocks) and 16 (Camp de l'Expédition).
- Rows whose only attribute beyond class is the general construction statement, marked "class only apart from blanket construction statement": 14, 21, 24 and 40.
- Features keyed with `n_openings`: 3, 4, 5, 6, 10, 11, 12, 17 (2), 23, 27, 29, 29.d (0), 31, 32, 33 (2), 34, 37, 38, 39.
- Features keyed with `opening_dirs`: 4 S, 4.a S, 5 E, 6 S, 7 E, 11 SE, 15 N, 17 N;S, 18 N, 19 NE, 20 S, 32 E, 33 E;N, 36 NE, 39 NE, 39.a NE.
- Features keyed with `n_pillars`: 12 (2).
- Features keyed with `n_steps`: none. No numbered site mentions steps. The stairs at 7Q and 10Q (pp. 27, 31) are outside scope.

## Seen but out of scope (not keyed)

- X-1 and X-2 (p. 13): isolated finds of the Arab period, not features.
- Caves A and B (1956, p. 13): on the north flank of the ravine that holds cave 8 = 3Q on its south flank, about 20 m apart, A east of B.
- 5Q (p. 26) and 7Q-10Q (pp. 27-31): marl-terrace caves. 7Q has a staircase.
- The two ancient roads (p. 6) and the aqueduct.

## Problems

- The first navigation to `/page/3/mode/1up` loaded the cover while the loan was initialising. Opening `/page/n20/mode/1up` and flipping forward worked. After that the viewer showed printed page numbers.
- One scroll call returned "Couldn't determine which page this action targets". Re-reading the tab context fixed it.
- I saw a second reader's tab (299151206) in the tab group but never touched it.
- No browser failures and no loan problems.
