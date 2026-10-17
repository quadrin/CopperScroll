# Online images, video and 3D models for the atlas places — 17 October 2026 (English-language search)

What online footage exists for each atlas place, what it would add to the renders, and which open question it bears on. Found by five parallel web searches on 17 Oct 2026 (main at 0d0bbdf). **VERIFIED** = the page, API record or search result was seen; **LEAD** = exists but content or licence not confirmed. Sketchfab licences and download flags for the ten top models, and the Matson rights wording, were re-checked against the providers' own data.

**Limits.** A photo or video can show that a feature exists, how it looks and where it is. It cannot date a construction or a use phase (the SULTAN-1 protocol says the same). None of the questions below closes on footage alone; footage only sharpens a question or a render. Meshes from Sketchfab have no georeference: before any traced feature goes on the terrain, it needs control points and a recorded residual, as `PHOTO_INTEGRATION.md` requires.

## Licence classes

- **Usable in the published atlas (with credit):** Library of Congress Matson collection ("No known restrictions on publication", checked on three items); Commons PD, CC0, CC BY, CC BY-SA (share-alike); Pikiwiki Israel (CC BY 2.5); Sketchfab CC BY; Mapillary (CC BY-SA). CC BY-NC / NC-SA (FABDEM, Manar al-Athar, some Sketchfab) only while the atlas stays non-commercial. Sketchfab "Free Standard" allows use inside a project; check its terms before redistributing the mesh.
- **Reference only:** all YouTube and Vimeo (no CC licence found on any; YouTube terms forbid downloading); BibleWalks, BiblePlaces, HolyLandPhotos, Madain Project, Danny the Digger (copyright, permission needed); PEF Flickr (all rights reserved); APAAME (CC BY-NC-ND, so no textures); Sketchfab models with no licence; Google Photorealistic 3D Tiles (streaming only with attribution; no caching, no tracing, no derived models); Esri World Imagery.

## Reserved: do not view before the protocols allow

- **SULTAN-1 strip north of Tell es-Sultan.** These may show it and were not opened. Treat them as arrival items: run `arrival.py check` and register under `assessments/kohlit_chain/registration_protocol.md` first.
  - LoC Matson: 2019692534 (ruins of Jericho "from the north"), 2019712922 (mound, looking south), 2019712921 (modern Jericho above the Ain Sultan road, looking S), 2019712923 (Mount of Temptation and gardens of Ain Duke), 2019706617 (Ain Duke, Jericho and the Jordan), 2019706618 (Jericho plain and oasis of Ain Duke).
  - Commons: Aerial photographs of Jericho; Views from Tell es-Sultan; Views from Monastery of the Temptation; Monastery of the Temptation Téléphérique; the Tell es-Sultan excavation-area subcategories.
  - Video: Jericho cable-car rides (YouTube 9_2PvRIWS_8, BlPe2D3r7SA; 360cities "jerichocablesphere1stmin"); Jericho drone tours (X_Wq4yk1sC8, DtGFHAXz5kI, UbmwiHQWC8U, JweqiSigq9U); Ministry of Tourism "Tell es-Sultan In Jericho" (gvoMigHqRhI).
  - Pages: CBRL "Jericho off the record" and "Treasures from Our Archive Collection"; Durham stories "Jericho"; *Archaeology International* article 3690.
  - Survey of Israel 2015 2 m orthophoto, Jericho sheet (`yrh`, data.gov.il).
  - **Screen first** (may pan over the strip): the Doq drone videos and Matson 2019712924 (section Jericho, Doq); the Tel Sultan tower mesh (check its extent before opening); NINO Scholten "Ain Duke" nos. 24, 28, 30; Commons Cypros files tagged "Views of Jericho".
- **XII 8–12 and the 21/22 cut.** The Jordan Museum photos of the scroll on Commons (the source of the strip 13 view) may include segments 21–22. No search looked at scroll photos. Any XII 8–12 frame stays reserved under the arrival procedure.
- **Abu Saraj IV/17 and Twin Cave mouths.** Not searched. Apply the frozen Entry 25 rules (`preregistration/entry25_iv17_rules/RULES.md`) before looking at any online image of them.
- **RP-SPRING** (the ʿAin es-Sultan spring-house wall) is the protocol's default withheld check. Photos of the spring are fine to look at for entry 11, but do not use them to place that point.

## Biggest gains for the renders

1. **Free CC BY photogrammetry meshes** (downloadable; checked 17 Oct) can replace the zoom-12 terrain locally:
   - Qumran terrace and caves: "Caves Qumran – PALESTINE", juanbrualla, 1.6M faces — https://sketchfab.com/3d-models/caves-qumran-palestine-1d453db43e01420ba03359a0c96d4f9e
   - Doq / Jebel Qarantal: "Mount of Temptation", middleasset, 1.0M faces — https://sketchfab.com/3d-models/fd88ccdba1724ee8b0fff44be67b8123
   - Kidron: "Avshalom Tomb" (516k) and "Kidron Valley" (750k), jerusalemheritage — https://sketchfab.com/3d-models/e233f465ba884194b5c0101feacca5e9, https://sketchfab.com/3d-models/9f6304a36b074d36b8c950bb86deda4e; plus Zechariah's north, south and east faces and two Kidron burial caves (CC BY, moshecaine/jerusalemheritage)
   - Mar Saba gorge: matousekfoto, 855k, Free Standard — https://sketchfab.com/3d-models/mar-saba-monastery-4bff096a20064d65b8af65ab8c51d9cf (GLB on Zenodo 10.5281/zenodo.10346867, labelled CC BY-NC); spogna RAWscan, CC BY-NC, 1.18M
   - Masada: matousekfoto, CC BY, 465k — https://sketchfab.com/3d-models/masada-17b256653dc74c80ad03f2c7d4036742
   - Maresha Sidonian cave (columbarium/loculi comparison): Eliad.Ayalon, CC BY, 375k — https://sketchfab.com/models/b8fbde980e5e4e79892ecc318e4ff1f8
   - Hisham's Palace water installations: middleasset series, CC BY.
   - Tel Sultan tower trench: middleasset, CC BY, 999k — **screen its extent first** (see Reserved).
2. **Matson 1931 and 1937 air views** (public domain) give oblique camera references before modern building, for Mar Saba, Herodium, the Temple Mount's SE quarter, Gerizim–Nablus, Tell el-Ful, Wadi Qelt and the Jordan.
3. **Terrain: no free improvement exists.** Mapterhorn holds only Copernicus GLO-30 here; zoom 13 is resampled GLO-30, zoom 14 is 404. There is no open Israeli DTM on data.gov.il and no open LiDAR (OpenTopography). Options: FABDEM (GLO-30 with buildings removed; helps Jerusalem; CC BY-NC-SA), AW3D30 as a cross-check, TanDEM-X 12 m by DLR science proposal, or buying Survey of Israel data.
4. **Textures:** Survey of Israel 2015 2 m orthophoto sheets on data.gov.il cover the West Bank too (Jerusalem `yrs`, Jericho `yrh` [reserved], Kalia `qly`, Shechem `shk`, Beth Shean `bsh`, Ramallah, Hebron). The licence field is empty, and the download gave 403 from the cloud; try from Alex's browser and ask about the licence.
5. **Commons geosearch** lists every geotagged file near a point: `https://commons.wikimedia.org/w/api.php?action=query&list=geosearch&gscoord=LAT|LON&gsradius=500&gsnamespace=6&gslimit=500&format=json` (49 files within 500 m of Qumran, 25 at Mar Saba). Send a User-Agent and go slowly; it rate-limits.

## Judean Desert

**Kh. Qumran and its aqueduct (entries 20–23; R01)**
- Meshes: juanbrualla (above); "QUMRAN", Davide.Specchi, CC BY; "Dead Sea Qumran", hermes3, CC BY-NC, 211k.
- ACOR Lapp collection (free for scholarly use): 75922 "aqueduct enters compound from tower" (1957); 75892 "cistern showing earthquake crack" (1983); 75924 double cistern; 75938 cistern 48–49; Schick slides 62712–62713 water channel. URL form `https://archives.acorjordan.org/s/acor/item/<ID>`.
- The only dam photo found: BiblePlaces "Qumran Dam" (©) — https://www.bibleplaces.com/qumran/. INPA leaflet map: station 1 "Aqueduct Entrance".
- Drone: Jeffrey Worthington, Vimeo 139644903 (1:55, 2015), YouTube Qr020JwgLrU; SZERMAN FILMS JW-XTXT6khU.
- Render: true cliff-foot and terrace shape; channel-entry camera angle.
- Question: can the cliff channel and the right-angle bend at Ilan–Amit point 16 be traced on the mesh (Stacey's earlier head, entry 21)? A green-marked trail follows the channel through the tunnels (Times of Israel), so hiker video of the tunnels may exist; none was confirmed. Footage cannot date L117.

**Wadi Qumran caves**
- View-only meshes: Yakov.Shmidov "Qumran Caves 1Q" (2.9M) and "4Q 10Q" (1.6M), 2026.
- ACOR 75927 "Cave 4 – 3 entrances; cave 5 right; caves 7 & 10 seen from 4" (a ready sightline); Matson 2019704383–84 (Cave 4 and view out). BiblePlaces has Cave 3 outside and inside.
- Question: the setting of 3Q against the de Vaux 1952 points already on the atlas layer.

**ʿAin Feshkha (T20; entries 23, 25, 26)**
- ACOR 75911–75912 (1958 excavation rooms and drain, with de Vaux); Matson 2019693218 (the spring), 2002715357 (reeds).
- Question: farm-building layout and drains, as a cross-check for the Callegher and Magness extractions. ʿAin el-Ghuweir: nothing found.

**Hyrcania / Kh. el-Mird (entries 16, 29, 35; R08)**
- Excavation media: HUJI "Hyrcania Fortress Excavation Project" (YouTube xqfsYNp2JKY, linked from en.huji.ac.il); HU drone clips via ClassiCult (EZix48BndRU, LOGnUAwzts8) and Medievalists (DXNCI8XhiIA, 2024).
- BibleWalks "Horkania" (©) — https://www.biblewalks.com/Horkania/: aqueduct bridge; the place where the Kidron and Muntar channels run side by side; the southern reservoir; cisterns; a 10 m square Herodian tower; a 360° summit panorama.
- View-only mesh: Yakov.Shmidov, 1.75M, 2026 (the only 3D model of Hyrcania).
- Tunnels: The Running Tour Guide (p0plWZeDDd8) describes the two stepped tunnels.
- Render: bridge, reservoir and cistern placement on the slopes.
- Questions: (1) R08 asks for the measuring origin and a validated north at Hyrcania; the 360° panorama and drone clips give bearings to known peaks. (2) Is BibleWalks' 10 m square tower the square "monument" ~300 m SW that Allegro took for item 2 (Wright 1961, grid 1845/1250)? Check its position against Wright's grid.

**el-Buqeiʿa (entries 1, 17)**
- ACOR 75624 (1958): Kh. Mird with the Buqeia in the centre and the Wadi Qumran depression behind; a ready viewpoint tying three atlas places together. Also 75640 (from Herodium) and 75901 (from Murabbaʿat).
- Commons "Hyrcania Valley IMG 1913/1914/1918". The forts and dams: nothing found.

**Mar Saba / Wadi en-Nar (entry 35)**
- Meshes above. Matson air views Oct 1931: 2019712917 (looking W), 2019712918 (looking S, valley bed), 2019712916 (Kidron's entrance to the Dead Sea); ground 2019692495–96 up the gorge; ACOR 75625.
- Drone: Polychronis Film (mefBGKZvqzs); Vimeo 120893736 (Magal, 3:29, 2015).
- Question: gorge geometry at the place entry 35 names. The monastery's cisterns: no footage.

**ʿAin en-Naṭuf / Wadi Khureitun (entries 38, 40)**
- Commons Category:Wadi Khureitun (99 files, incl. Khureitun Cave).
- CORPS-CMHL "Khirbet Khureitun – Chariton" (plan; the "Hanging Cave" with a terrace and two pools; Bir el-ʿUneiziya reservoir) — https://dig.corps-cmhl.huji.ac.il/Monasteries/khirbet-khureitun-chariton-souka-old-laura
- Hiking in the Holyland (2020): cave interior and the spring falling into a square pool.
- No columbarium near Khureitun found online.

**Herodium and the Tekoa sector (39–45)**
- Commons Category:Herodium (subcategories for aerials, underground tunnels, Lower Herodium, the tomb). BibleWalks aerial videos (7jJdYULtOqM, p0GPY6ajSM8). Matson 2019713063 (1931 air view). ACOR 75626–75633.
- No usable 3D model.

**Masada (entry 44, columbarium reading)**: matousekfoto CC BY mesh; UWG repository "Columbarium Tower" (2023, no licence).

**Christmas Cave** is in Wadi en-Nar / Nahal Qidron (Heritage Science 2022, 10.1186/s40494-022-00652-2). This agrees with the 10 Oct note. No photo of its mouth found. Wadi el-ʿAṣla and Wadi Kuteif: nothing found.

## Jericho and the Jordan valley

**Doq / Jebel Qarantal (entry 31)**
- middleasset mesh (above). Commons "IHM מבצר דוק" 1–7 (GorALexeY, 2021, CC BY-SA 4.0), in Category:Mount of Temptation.
- AllAboutJerusalem "Cypros, Dok (Dagon)… Winter Palaces" (xUkWu4FjWOo, 5:16).
- **Screen first** (they may pan east over the plain): KaPadli Adventure Israel, "MOUNT OF TEMPTATION DRONE FOOTAGE" (3:23, about 2022); Sharbel Sassine, Mavic Air 2 (xC9OuftdxYo, 1:35); Matson 2019712924 (1931, viewing direction not stated).
- Question: does the summit plateau, with the Dagon cisterns, fall inside the mesh? No online image of the Doq aqueduct or cisterns found.

**Winter palaces, Tulul Abu el-ʿAlayiq (entry 29; closed result)**
- Commons Category:Tulul al-Alaiq (60 files, subcategories per palace); "Swimming pool in Hasmonean royal winter palace" (10 files, CC BY-SA 4.0); "2611 ארמונות החשמונאים – לדרום-מערב – קיפרוס" (palaces to Kypros, a ready viewpoint).
- Historical Sites in Israel: "Ancient Jericho – Water Sources" (71Oz9F3hEyY, 15:08) and the two palace films (AnptQqQZBOI, TA9gM17FeFs).
- Render use only. Entry 29 reopens only for a phase-controlled field section (A(C)94), which no footage gives. Area AC and the restoration: nothing found.

**Wadi Qelt at Choziba (entry 32; R03)**
- Public domain: Kluger 1936 "A channel bringing water from the hills to the bottom of Wadi Kelt"; *Picturesque Palestine* (1881) "One of the arches of an aqueduct over the Wady Kelt"; Matson "Ain Farah Waterworks"; Matson 2019712926 (1931 air view of the gorge and St George's).
- Commons Category:Wadi Qelt (277 files; St George's 155, Ein Farah 72). "IHM גשר אמת מים הרודיוני" (zstadler, 2020, CC BY-SA 4.0), geotagged 31.8342 N 35.3795 E, about 3.3 km upstream of the monastery.
- Video: "עין קלט ואספקת המים ליריחו" (Dj8cQxY9ys4, 14:53); Rubi Hammer FPV of the monastery (6JI294O-bXA).
- Question: R03 wants the wall and outlet pair near the monastery. The 1881 arch and the 1936 channel photo are the oldest views; check whether either is at the PEF Sheet XVIII bridge sector. No culvert at the monastery itself was found.
- **ʿEin Kuweiziba**: Khirbet Kuwayzibah is near Saʿir, NE of Hebron (about 31°36′N 35°09′E), on the ʿArrub aqueduct side, not Wadi Qelt. UNESCO tentative list 6958 (2026) covers the ʿArrub aqueduct with text and coordinates only. No footage.

**ʿAin Duk / Naʿaran (entries 1, 17, 29, 31)**
- Commons NINO / Frank Scholten "Ain Duke" series, 31 photos, 1921–23, public domain: bridges, streams and a waterway (nos. 05, 10). **Screen first** nos. 24, 28 and 30 (views over the plain).
- Commons Category:Naaran synagogue (12 files); "IHM עין דיוק" (2021, CC BY-SA 4.0); Category:An-Nuway'imah (6).
- Question: the channel and bridge at ʿAin Duk before modern works (R07 asks for spring and conduit sections). Wadi Nuweiʿimeh gorge (Achor reading): nothing found.

**Tell es-Sultan mound and spring (entry 11)**
- Commons Category:Spring of Elisha (40 files; van de Poll 1953); Matson 2019692160 (Elisha's fountain, 30 Apr 1944) and 2019697889 (fountain and mill).
- Question: what lies east of the spring house today. This does not date the pool (Active question 3). See the RP-SPRING note.

**Lower Jordan fords (entry 28)**
- Commons: Jordan River at Qasr al-Yahud (45), Historical pictures of Qasr al-Yahud (29), Deir Hajla (284), Ein Hajla (65), Allenby Bridge (57, by decade 1910s–60s).
- Matson: 2019705565 "River Jordan, the Ford"; 2019692525 Beth Hogla; 2019694628–30 Jordan floods at Allenby Bridge; 2019712826 (1931 meanders).
- HALO Trust baptism-site drone (ioCvp57s2b4).

**Qarn Sartaba / Alexandrium and Kypros (R08)**
- Commons Category:Sartaba: "Water delivery system near Sartaba" (11 files, CC0, 2023, including the siphon and a guide holding diagrams of the system); "Sartaba water reservoirs" (20); PEF 1877 drawing "Khan Sartabeh aqueduct" (PD).
- BibleWalks Sartaba (©): December 2017 drone flyover; about 4 km of aqueduct; 14 cisterns on three levels; Abel's 1910 plan.
- Video: "The 2025 Sartaba-Alexandrion fortress excavations" (s3ftyZ50wno); i24NEWS (1IJOwVtPJZs); Vimeo 520530729.
- Kypros: Commons Category:Cypros (64 files; Bukvoed 2021, CC BY 4.0, about 40 photos); Yuval Dax aerial (yK0HF0WOKo0).
- Question: R08 needs matched Amit and 2001-survey endpoints for the 190, 250 m and 0.60 m figures. The CC0 photos and the guide's diagram may show where the segments start and end; footage alone will not settle the lengths.

## Jerusalem

**East Gate / Golden Gate (entries 9, 10)**
- Matson 1898 "Interior of the Golden Gate" (2019698463, rights checked); 2019698464, 2019698488. HolyLandPhotos IJNTHRGG01 (interior, ©).
- Commons Category:Golden Gate (89 files; Bab al-Rahmah Cemetery 39).
- HOLYLAND Walk ISRAEL "Silent walk around the GOLDEN GATE" (bB-lrO8WVo0, 2024, 33 min): ground level along the foot of the wall.
- Bab al-Rahma interiors after 2019 (titles only): pRcbcIREzAI, GZTPcHhWopk, aY20DJ3z5Uc.
- Question: floor and threshold level of the gatehouse ("its entrance under the great threshold"); the ground surface where a cistern 19 cubits out would be. No footage of the cisterns or of Warren's shafts.

**SE corner / Solomon's Stables (entry 51)**
- Matson series c. 1898–1950: 2019692400 ("spring of arch"), 2019697349, 2019698480, 2019705445 (1950). This is the only pre-1996 interior record. NLI 1894 "Écuries de Salomon" (public domain in Israel).
- Commons Category:Al-Marwani Mosque (44 files). YouTube qjwcoAUDj6c (2012), GbjcApHdHLY.
- Double Gate halls: Matson 2019696203 (1920); "Double Gate Halls under the Al Aqsa Mosque" (2FdCPMinF18; whether it shows the monolith column is not confirmed).
- Question: the pier grid under the SE corner, and the monolith column ("the pillar of the exedra"), for the Baruch & Reich extraction.

**Southern wall, Ophel (entries 51, 53)**
- Matson 1900: 2019693827–29 (Single, Double, Triple Gates); Ophel rock-cuttings and rock-cut tomb 2019693839, 2019693840, 2019693842; 1931 air views of the Temple area from S, SE and E (2019706624, 2019713017–19).
- Commons: Jerusalem Archaeological Park (260), Huldah Gates (46).
- Davidson Center / UCLA reconstruction (NrYQEIfhl8U) for Royal Stoa massing; Armstrong Institute Ophel tours (PiM481z-2ME, 97MAen7stvU).
- Question: the 1900 Ophel rock-cuttings and tomb are the closest thing online to entry 53's "rock" by the wall.

**Wilson's Arch (entry 28, bridge reading)**
- Commons Category:Wilson's Arch (72). Doron Altaratz LiDAR "Multi-Period Section, Western Wall Tunnels" (view only).
- Western Wall Heritage "Behind the Scenes of the Western Wall Excavations" (XvNBi5n7poE); 2017 dig beneath the arch (qcTylUbYmJc).
- Question: the excavation shaft beneath the arch, for the Uziel et al. 2025 extraction.

**Kidron monuments (entries 48, 51, 52)**
- CC BY meshes (above). Commons: Tomb of Absalom (109), Bnei Hazir (37), Bnei Hazir and Zechariah (83), Zechariah (59). Matson 2019695396 (stairway inside Absalom's pillar, 1900; the only interior view).
- Question: sheet 11 found nothing recorded on the **west side** of Absalom's monument. Open the jerusalemheritage meshes and see whether the west face and the ground there are captured.

**Silwan necropolis (entries 52–56)**: Commons Category:Silwan necropolis (19); PEF lecture on the "Tomb of Pharaoh's Daughter" (1-_4DTHq4Tg); Virtual JERUSALEM walk Kidron → Siloam (S9myE4MVygU, 61 min).

**Siloam (entry 49)**
- Commons: Pool of Siloam (103), Hezekiah's Tunnel (126), Warren's Shaft (40), Gihon (32). Matson 2019699055, 2019693836, 2019699056.
- City of David channel: Pilgrimage Road (J2NiLXIajC4), Gihon (izEvnrRua3Y); new pool excavations 2023 (lkIh1y78-l0, dig at 3:19).
- ScriptureCentral "3D Siloam Scan" (Sketchfab, Nov 2025, view only). Worth opening first.
- Question: does any footage show the main-side L103 junction with basin edge and floor? Caution: the ~800 BCE dam is at Birkat el-Hamra, which Szanton separates from the Siloam pool; check which basin a clip shows.

**Bethesda (entries 55, 56)**
- Commons Category:Pool of Bethesda (175). BibleWalks (©): captioned S pool, seven-arch supports, a central channel feeding a cistern, grottoes. HolyLandPhotos gallery s=398 ("Cistern"). 360° video SGT8Q7U1GKk. Sketchfab "Piscine Probatique" (view only). Matson 1898 2019697399, 2019697952.
- Question: Duprez 1970 puts a threshold with its jamb between grotto 6 and cistern 1 (p. 41). Does a photo show that doorway, and which side the jamb is on? Not found yet.

**Other Jerusalem places**
- Tombs of the Kings (entry 27): Commons (112); Matson 2019697965, 2019698446 (rolling stone), 2019693819 (stair), 2019698492, 2019693820 (interior); Zahi Shaked "Rare Access" (jhNDcM6r38Y, 2026).
- Bir Ayyub: Commons Ein Rogel (14); Matson 2019698160, 2019692436.
- Tyropoeon: Matson 2019701640 (Crowfoot 1927); City of David Givati (uW7zygjk0f0).
- Gethsemane: Commons Grotto of Gethsemane (45); Matson 2019713024 (1931 air view of the Kidron looking N).
- Ramat Raḥel (entry 46): Commons (298); BibleWalks aerials (1qTLRkZmMXI); "Ramat Rahel lower aqueduct" (UhOs4rndRfU); Sketchfab royalbag (view only).
- Tell el-Ful (entry 43): Matson 2019713052 (1931 air view), 2019692050 (1917).
- el-Baqʿa: nothing found.

## Samaria and the north

**Mount Gerizim (entry 57; R05)**
- Commons Category:Mount Gerizim (archaeological site) (200+ files; Ovedc 2013 series with camera coordinates; Deror_avi 2013; "Path from Kiryat Luza to archaeological site", which may show the western stair).
- BibleWalks "Mount Gerizim – Aerial views" (KZBRWvvBeJc) and page: the best summit drone reference; one still of the northern foothills with Tell er-Ras.
- Matson 2019713160 "Nablus & Gerizim, looking S.E.", 10 July 1937 (rights checked); 2019692553, 2019701810.
- HolyLandPhotos ICHMMG08: the upper eastern staircase.
- deadseaquake.info Tell er-Ras page: reproduces Bull & Campbell 1968 site plan, Building A, Cistern II section and the stair line (©).
- Questions: (1) the 1937 air view shows the north slope before modern building: look for Bull's north-slope steps and the stair to Neapolis. (2) **The fosse south of Tell er-Ras** is inside an IDF post and closed to visitors, so no ground footage exists. The HEXAGON 1974/1978 frames already in Drive (A012/F011–F012 of 25 Jun 1974; A015/F014–F015 of 1 Dec 1974) and RAF PS3 6065 are the only views. (3) No 3D model of the summit.

**Kh. Ibziq and Kh. Salhab (entry 59)**
- Nothing online shows the 45 cisterns, the road east of Upper Ibziq, the ~70 burial caves or the kokhim tomb.
- Context only: Matson 2019712864 (1931, the eastern end of Wadi Faraʿ); Sketchfab "Rock-cut Tomb, Zawata" (Palestine-Arc-Project, a kokhim tomb near Nablus, view only) as a stand-in; "Burj el-Far'a" (view only).
- Already held: RAF PS19 5080–5083 (orderable), HEXAGON A011/F010 (1974-06-25) and A013–A014/F013 (1974-12-01) in Drive.
- Warning: Commons "Tal Salhab.jpg" is the Salhab in Syria.

**Beth Shean (entry 58)**: HipposExcavations "Nysa-Scythopolis" (1.1M, view only; the best 3D reference); Commons Aerial photographs of Ancient Beit Sheʾan (27, Pikiwiki; check each licence) and Tel Bet She'an (108); Matson 2019707839 (1937 air film); BibleWalks aerial (TJEGSqDuLKY).

**Beth-Horon (entry 40; R04)**: Commons Beit Ur al-Fauqa (20) and al-Tahta (19); Matson 2019695119 (the ascent), 2019695121, 2019695472. No imagery of the tombs, their entrance bearing or water channels.

**Beit Guvrin / Maresha (entries 38, 40, 44)**: Sidonian cave CC BY mesh (above); Commons Columbarium cave at Beit Govrin (44, e.g. Bukvoed 2018, CC BY 4.0); Matson 2019692883 (columbarium); "Bell Caves" mesh (hibs71, CC BY). Lead: Berko 2021 (Bar-Ilan) mobile LiDAR of Maresha cavities; data availability unknown.

**Shechem context**: Matson Jacob's Well series (2019692551, 2019700308); Sketchfab "Tell Balata ruins" (view only).

## Gaps no online source fills

The Qumran dam/intake on video and the point 16 bend close up; Mar Saba's cisterns; Hyrcania's SW monument (identity); the Buqeiʿa dams; ʿAin el-Ghuweir; Wadi el-ʿAṣla, Wadi Kuteif, Wadi Nuweiʿimeh; the Doq aqueduct and cisterns; Area AC; the Choziba culverts; ʿEin Kuweiziba; Tell el-Qos; the Gerizim fosse; anything at Ibziq/Salhab or the Bezek road; the Beth-Horon tombs; the Golden Gate cisterns; Bethesda's grotto 6 doorway; the Siloam L103 junction; el-Baqʿa.

## Later the same day

Hebrew and Arabic searches for the gaps: [hebrew_arabic_search.md](hebrew_arabic_search.md). What went into the atlas: [README.md](README.md).
