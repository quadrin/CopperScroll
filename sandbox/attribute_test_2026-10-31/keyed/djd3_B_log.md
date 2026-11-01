# djd3, reader B: keying log (run 28)

- Source: Baillet, Milik & de Vaux, *Les 'Petites Grottes' de Qumrân* (DJD III), Textes (1962), ch. I "Exploration de la falaise de Qumrân". Read on the Internet Archive loan `lespetitesgrotte0000unse` in the owner's Chrome, in a tab of my own (closed at the end). Loan active throughout ("Renews automatically with continued use"). "Return now" was never clicked.
- Started: 2026-11-01T03:01Z (UTC). Finished: 2026-11-01T03:17Z (UTC). The browser clock and these shell times may compress the elapsed time; the order of work is as logged.
- Output: `keyed/djd3_B.csv`, 72 rows covering all 40 numbered sites (feature_id `djd3:<n>`, sub-features `.a`, `.b`...). grid_printed and grid_system are blank. position_basis = text_only.

## Pages read
- Printed pp. 3–36 (viewer leaves n22–n55; p. 3 = n22).
  - pp. 3–4, 6: history, geography and the section introduction. The equivalences are on p. 6: 8 = 3Q, 14 = 1Q, 19 = 2Q, 26 = 6Q.
  - p. 5: Fig. 1 map (grid 192–194 / 124–129, site numbers). Viewed only, **not used** for positions or attributes.
  - pp. 6–12: the numbered list, sites 1–40. Read in full at full width, with zoom checks on the dimensions of sites 1, 37 and 39.
  - pp. 12–13: isolated finds X-1, X-2 and the 1956 caves A and B (p. 13).
  - pp. 13–17: objects. Used for dating (p. 13 defines "genre Qumrân" as Kh. Qumrân periods I–II, end of the 2nd c. BCE to 68 CE), p. 15 (site 34 pot, site 9 lamp type), p. 16 (other periods; sites 33, 36, 38 later Roman) and pp. 16–17 (site 17 wooden posts).
  - pp. 18–25: pottery figures and catalogues (Figs. 2–5). **Skimmed** for site-feature statements and found none. Part of the p. 24 catalogue, entries 8–21, was not read line by line.
  - p. 26: 5Q and 6Q. The 6Q paragraph was used for site 26.
  - pp. 27–31: caves 7Q–10Q. **Skimmed**; these are not numbered sites. The only numbered-site mention is a site 29 lamp parallel.
  - pp. 32–36: conclusions. p. 33 gives the class grouping of sites. p. 34 repeats site 29 (round chamber reached by a narrow tunnel) and site 17 (hut or tent posts).
- Plates (pl. II–VII) are cited in the entries but are in the plates volume and were not viewed. The `figure` column is blank throughout because no figure was used for any value.

## Out of scope (not keyed)
- X-1 and X-2: isolated Arab-period surface finds, not numbered sites.
- Grottes A and B (1956, p. 13): lettered, not numbered. A is a low cave with a low entrance. B is a low cave whose front part has collapsed; it has three occupation levels. They lie about 20 m apart, A east of B, on the N flank of the ravine that has site 8 on its S flank.
- 5Q and 7Q–10Q: marl-terrace caves with no site number.
- The two ancient roads (p. 6): not numbered.

## Conventions used (for the agreement step)
- **n_openings**: keyed when the entry describes an entrance or opening (for example "large entrée", "ouverture vers l'est", "ouvrant vers le nord"). It is 1 per opening described. Site 17 is 2 (opens N and S). Site 33 is 2 (opening E plus a "fenêtre" N). When the count comes from a verb such as "ouvrant" rather than a stated number, the note says so. It is left blank for site 8 (original entrance unknown) and site 19 (plural chambers "ouvrant vers le nord-est"). Site 3 has 1: the small low seepage opening, although the entrance layout is not establishable.
- **"profonde de X m"** for caves and chambers (sites 3, 5, 22, 37.f, 39) is keyed as `depth_m`. It is the horizontal depth into the rock, not a vertical depth.
- Where dimensions are printed as "a × b" or "a sur b", length and width follow the printed order (sites 1.a, 7, 8.a, 27.a).
- Approximate values ("environ") are keyed as printed, without a flag column.
- Ash and deposit thicknesses (sites 1, 6, 8, 24) are deposit measurements. They are in `notes` and not in the dimension columns.
- **rel_bearing_deg**: there is no printed angle anywhere. Compass words were converted to degrees, read from the row's feature to the related feature. Site 13 is printed "au SO du n° 12", so 13→12 = 45. Site 23 is printed "au nord du n° 25", so 23→25 = 180. For 37.d→37.b the value is 45; for 37.e→37.f it is 270.
- **construction**: keyed only where the site entry itself says it. Site 2 and site 21 are natural. Site 9 is mixed (crevice plus dry-stone wall), 9.a and 23.a are built, site 12 is mixed and site 35 is built. The general p. 33 statement that cliff cavities are "cavités naturelles" was **not** applied row by row.
- **in_window**: yes where the entry or the pp. 13–15 tables give pottery "genre Qumrân" (Qumran-type) for the site. no where the entry says nothing of Qumran type, or says later Roman, Byzantine, Arab or Israelite. unknown where the entry says "peut-être" or "pas sûrement".
- **class choices that a third reader should check**:
  - Sites 15 and 30, "creux du rocher", are keyed rock_shelter. p. 33 calls them "simples anfractuosités" together with fissure 21.
  - Site 2, the pottery deposit under fallen rocks, is keyed other.
  - Site 28 has no class word in its entry. It is keyed cave from the p. 33 phrase "très petites grottes".
  - 29.c (cheminée) is keyed other but could be pit.
  - Tunnels and passages (8.b, 29.a, 32.a, 37.e) are keyed other.
  - 37.a (plateforme) is keyed terrace.
  - The entrance, porch and opening of sites 4, 27 and 39 are keyed doorway.
- **n_pillars**: site 12 = 2. These are two stones placed side by side to prop ("étayer") the ceiling near the entrance. They are supports, not built or rock-cut pillars, so this flags a possible disagreement. The five wooden posts of site 17 are objects (hut or tent poles, pp. 16–17) and were not keyed as pillars.
- **n_steps**: none of sites 1–40 mentions steps, so the column is blank everywhere. Site 34 has a sloping entrance with no steps mentioned.
- Rows keyed "class only" (confidence low): 14, 16, 24, 26, 40. Site 16 is the expedition camp, not an ancient feature.
- The entry for site 8 mentions where the two inscribed copper rolls lay in the rear chamber. Only that find position is noted (row 8.a). No text or edition of the scroll was consulted.

## Problems
- Navigating by URL to `/page/<n>` was unreliable. The viewer reopened at the last page read in the shared Chrome profile, which the other reader's tab was also moving. After the first page load I worked only with the in-viewer next/previous buttons and scrolling, and did not reload the page.
- One "browser extension is not connected" error happened mid-read, after site 20. The tab context call succeeded on the first retry, and reading resumed in the same tab at the same place.
- No other failures. I did not open any other item.
