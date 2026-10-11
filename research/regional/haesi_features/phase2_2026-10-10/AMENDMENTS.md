# HA-ESI phase 2: amendments and deviations

The frozen plan (`PLAN.md`, commit d0f8c7c, SHA-256 in `README.md`) is not edited. Every change below was made after the freeze. All are **exploratory**: they were chosen while screening titles or reading reports, so they cannot serve as a test of anything. None changes the zones, classes, in-window rule, tiers or reading order.

## A1. Two more apostrophe characters dropped in normalisation (screen, before any report was read)

The plan's normalisation drops ʿ ʾ ‘ ’ ' ` ´ ׳. The HA-ESI titles also use ʽ (U+02BD) and ʻ (U+02BB) for ʿayin, for example "ʽEn Perat". Without them a title such as "ʽEn Gedi" would not match "en gedi". `scripts/common.py` drops both. Exposure: noticed on the title lists; no report text had been read.

## A2. Manual title screen (S-ON2): 26 report ids

After the gazetteer screen (S-ON1) I read all 4,667 titles once by eye and added 26 titles that name places inside the region under spellings or names the gazetteer lacks (for example "Khirbat" for "Kh.", Har Gillo, ʽEn el-Hanniya, Aminadav, Waladje, Bet Neqofa, Mezad Boqeq, Nahal Hazazon, Noqedim). They are listed in `data/screen_amendment_A2.csv` with the reason, and carry `screen = S-ON2 (amendment A2, exploratory)`. They take the tier their zone gives (plan §3.4) and the same SHA-256 order. INFERENCE: some may still fall outside the region once the map reference is read; they are then dropped as the plan says.

## A3. Name variants used in the local-PDF heading screen; titles dropped as plainly outside the region

- Local PDFs: report headings without a map reference were matched to the gazetteer plus these variants: Hagedud (Netiv Hagedud), Anathoth, Land of Benjamin, Kh. el-Burj (near Nebi Samwil), stated in each coding record's `screen_note`. Reports with a map reference were zoned by the reference alone.
- Online screen: the gazetteer matched a few titles that name a street or a namesake outside the region. These are listed as `dropped: outside region by title (A3)` in `online_screen.csv` and were not opened: 26443, 1714, 2329, 1652 (Yafo, Jerusalem Boulevard), 481 (Ramla, Jerusalem Boulevard), 23813, 24964, 1724 (Bet Lehem Ha-Gelilit), 25375, 25837 (Be’er Sheva, Horbat Betar), 908 (Ramot Menashe), 26027 (Ramla, Lohame Betar), 26584 (Lod, Betar Street), 9560 (Hulda–Nahshon pipeline), 1454 (Jaljuliya, Gilgal), 26090 (Jordan River, Dureijat). The full title of each is in `data/online_titles.csv`.
- Report 25212 ("Jerusalem, the Old City, St. George Street") was put in T1 by a term match and is a Jerusalem report (Z4). It keeps its T1 position (the order is not changed after the screen) and is zoned by its map reference when read.

## D1. Deviation: two held-area cave texts read before the hold was checked

Plan §7 holds cave reports in the Qumran cliffs and marl terrace, the Jericho escarpment from Jebel Qarantal to Wadi Nuweiʿimeh and ʿAin Duk, and the Wadi Qelt gorge. While reading the local PDFs I read two such passages before checking the hold:

- ESI 3 (1985), pp. 61–62, "Judean Desert, secret passages" report: the ʿEin Farʿa section (Wadi Farʿa at the head of the Wadi Qelt gorge). Coded in `ESI03-061-judean-desert-secret-passages`, feature site marked "held area, read in error".
- ESI 5 (1987), p. 58, Ketef Yeriho: the cave opposite Deir el-Quruntul (Jericho escarpment). Coded in `ESI05-058-ketef-yeriho`.

Both texts are now exposed to this lane and cannot serve as unseen evidence for the arrival items. Neither text gives a direction for the cave opening. After this, cave reports in the held areas were opened only to their first lines (title, author and map reference) and then held. The held passages are listed in `README.md` (Blocked and held).

## A4. Coding notes from the T3 reading (no parameter change)

- Hedged datings ("probably", "possibly", "tentatively") follow the period the report names: yes if it is inside the window, no if it is only outside it. The hedge is kept in `period_as_given`. Examples: HAESI-26645 winepress and stepped cavity (yes); HAESI-26484 columbaria and HAESI-26460 quarry (no).
- A range such as "Hellenistic and Early Roman" stays unknown (plan §6, partial overlap), as already done for HAESI-550. HAESI-2071 (winepresses) was entered as yes in work-in-progress commit e8c535e and set to unknown before the final tables, for consistency with HAESI-550. No other row changed.
- Features of an eligible class that the report dates to the modern era (20th-century cisterns; the 1940s–1950s genizah deposit in the disused miqveh, HAESI-969) are coded no, not left out.
- Misprinted map references are handled in `location_note`: HAESI-436 (northing falls south of Hebron; located by name in Z4) and HAESI-686 (first NIG northing misprinted; the second reference is used).
- Stop rule (plan §3.5): T3 reading stopped after position 80 of 662 so that the tables, tests and README could be finished in the session. Positions 81–662 are `not read (time limit)`.

## Access notes (not amendments)

- Portal PDF test (plan §3.2): the HA 2–3 PDF (https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1001&context=ha_hebrew_series) opened in Chrome's built-in viewer, but the page-text tool returned no text from the viewer. Nothing was downloaded. The route stopped as the brief requires, and `portal_pdfs_needed.csv` was written. HA 28–29 (Tier-1 record) is therefore unread.
