# Benjamin survey 1993, Parts 1–3: sweep (benjamin_parts1_3_sweep)

Swept 30 October 2026 UTC. Exploratory sweep. Nothing was written to the repo, Drive or the project.

**Source.** I. Finkelstein and Y. Magen (eds), *Archaeological Survey of the Hill Country of Benjamin* (IAA, Jerusalem 1993). Parts 1–3 are by Finkelstein (sites 1–102), Hebrew pp. 15–96; an unnamed team (103–140), pp. 97–132; and Feldstein, Kidron, Hanin, Kamaisky and Eitam (141–321), pp. 133–264. Source: owner's photo set, Drive folder 1R-0w3FTEZoboyKfwJeB6kD41tDjZHEpl, manifest 1RTuJoOTh0hfW0cd-WFTv5u-7cdE6G7TE. The OCR draft was used only to find pages. Every number below was read from the photograph. Each downloaded HEIC's SHA-256 was checked against the manifest's `source_sha256`, and all 37 match.

## 0. What was already in the repo

A full sequential read of a separate PDF scan already exists: `research/sources/full_reads_2026-10-12/benjamin1993/` (12 Oct 2026, 214 observations). It covers every Parts 1–3 page **except Hebrew pp. 180–181**. That scan jumps from p. 179 to p. 182, losing the end of site 208 and all of sites 209–213. Only the English abridgements of 35* were recorded for those sites. This sweep therefore:

1. reads **pp. 180–181 from the photos, which is new evidence for the repo** (§2);
2. re-reads the shortlisted entries from the photos and records only additions or corrections to the 12 Oct observations (§3);
3. applies the new pages to the Koḥlit chain links that name "Feldstein et al. 1993" as their record (§4).

## 1. Held-area classification (done before any full reading)

All Parts 1–3 sites lie in the hill country of Benjamin west of easting about 179,000 (map sheets 15–17). In Part 3 the sites with northings below 139,000 all lie west of easting 170,000, on the northern edge of Jerusalem. No site in sites 1–321 lies in the Wadi Qelt gorge, the Jericho plain or escarpment, Abu Saraj, the Twin Cave or IV/17. The manifest flags every Parts 1–3 page `held=False`.

- **Held:** none. **Unclear:** none. **Not held:** all of sites 1–321.
- I opened no held page. The colour plates, folded map and period maps are flagged held and were not opened.

## 2. New evidence: Hebrew pp. 180–181 (IMG_1971; Drive 1ut6Sq7XIOAmx8-UTD6xvmYlRRu0NtCkv; sha256 d919b65f…)

Grid references are as printed (Israel grid, easting then northing). Below, "per page" means the label the book prints for these sites, which is "desert fringe" (ספר המדבר).

| Site | Page | Grid / alt. | Features (EVIDENCE) | Periods (EVIDENCE) | Entries | Proposed effect |
|---|---|---|---|---|---|---|
| 208 (cont. from p. 179) | 179–180 | 17590 14090; 590 m | Three shaft tombs with rounded burial chambers. Nearby, a tomb with a rectangular entrance chamber that has a vaulted ceiling; its burial chamber is **3.8 × 2.8 m**. Beside the tombs is a **cistern with a support pillar standing at its centre** (עמוד-תמך). About **120 m east**: two destroyed tombs with a cistern beside them. | No sherds that allow a conclusion. | 15 (feature type: great cistern + pillar); 60 (tombs beside a cistern) | INFERENCE: a feature-type control only. A pillared cistern beside tombs, undated, at no Koḥlit candidate. It supports treating a pillar in a cistern as not distinctive for entry 15. No rating change. |
| 209 | 180 | 17555 14090; 600 m; slope | Four tombs and two dwelling caves next to them. One tomb is a shaft tomb; another shows remains of benches. Near the caves is a rock-cut **kokh** whose end is not visible. About **100 m NW**: two more tombs. | No sherds that allow a conclusion. | Generic kokhim | None. |
| **210 Tell Maryam** | 180 | 17555 14185; 570 m; summit; 0.5 dunam; permanent water 2.3 km | A building on a prominent summit, **26 × 16 m**, of ashlar with drafted margins laid in header-and-stretcher courses. At its centre is a **destroyed cistern**. Beside it is a **system of deep channels, partly roofed with stone slabs**. **No pool, cave, tomb or shaft is mentioned, and there is no absence statement.** | Hell 22%; Rom 8%; Byz 23%; Early Islamic, single sherds; unidentified 40%; 97 sherds. Earlier surveys cited: Kallai 1972 p. 183, site 115; Mazor, Amit and Ilan 1984 p. 237. | Koḥlit chain `S2376-1-pool-east` (entry 11); rarity unit S2376 | See §4. EVIDENCE vs Kallai (repo extraction of 19 Oct): Kallai gives a **26 × 26 m** square fortress, a central elliptical cistern **10 × 6 m** with troughs, and a **15 × 7 m pool at the foot of the hill on the northern slope**. Feldstein gives 26 × **16** m, calls the cistern destroyed and **omits the pool**. The two surveys disagree on the building's width. Neither text says which is right. |
| 211 | 181 | 17510 14275; 640 m; c. 5 dunams | A ruin with cleared terraces; ashlar walls, mostly reused; cisterns; a **rock-cut cave north** of the site; a winepress to the SW. Next to the site are **several cave systems joined by narrow passages; the authors suggest hiding complexes** (מערכות-מסתור). | Byz 86%; Med/Ott 14%; 46 sherds. | Concealment comparanda (`research/comparanda/concealment_contexts`) | INFERENCE: a lead for possible hiding complexes. They are undated; the site's pottery is Byzantine and later. Add as an unverified concealment lead, with no date. |
| 212 | 181 | 17530 14240; 630 m; c. 3 dunams | A cleared ruin with walls and building stones; small quarries; a dwelling cave to the SE; **2 cisterns**. | Byz; Early Islamic (?); 32 sherds. | — | None. |
| **213** | 181 | 17575 14260; 580 m; slope; cemetery | A cemetery of **at least 13 tombs, including 3 kokhim tombs and 3 bench tombs**. The other tombs are blocked or destroyed. An **ossuary fragment** was found. | Roman sherds only. | Entry 60 (graves); rarity unit S2376 (C3) | INFERENCE: a dated Roman kokhim cemetery **776 m at 15° from WBADB S2376** (Tell Maryam). It is inside the north sector (315°–45°, ≤ 1 km), but no pit mouth is related to it. From S2300 it lies 585 m at 290° and from S2304 716 m at 295°, both outside the north sector. |

The English abridgement (35*, IMG_1810) shortens all six entries. It omits 208's pillared cistern and the tomb dimensions, 209's kokh, Tell Maryam's channels and masonry, 211's possible hiding complexes, and 213's tomb counts and types.

## 3. Shortlisted entries re-read from the photos (additions or corrections to the 12 Oct read only)

The shortlist came from all English summaries 13*–45* (IMG_1799–1815, read from the photos). It covers rock-cut pools or reservoirs, channels or aqueducts, kokhim or bench tombs, stepped structures, Hellenistic/Roman assemblages, and the named candidate places: Gibeon 315, er-Ram 188, Tell en-Nasbeh 175, Jaba 206, Kh. Marjama 231, and the Jerusalem north-fringe sites 302–321. Anathoth/ʿAnata and the Hizma–Almit area are in Part 5, already screened. Nob and Tell el-Ful are not catalogued in Parts 1–3.

| Site | Hebrew p. / photo | Features with dimensions (EVIDENCE) | Periods | Relevant entries | Effect |
|---|---|---|---|---|---|
| 13 Kh. Huriya | 38 / IMG_2045 | A large rock-cut pool west of the ruin, with **steps leading down into it**. A destroyed sheikh's tomb at the NW edge. | Byz 22%, Early Islamic, Med 37%, Ott 30%; 83 sherds | 1 (steps; type only) | None. Matches the 12 Oct read. |
| 46 Kh. Jaryut | 60–61 / IMG_2034 | The Hebrew calls the slab-covered conduit a **tunnel** (ניקבה). It carries spring water to a built, plastered pool. A vaulted building in secondary use stands beside the pool. Photo on p. 61 (general view, no scale). | Rom 2 sherds; Byz 1; Med 73%; Ott 15%; 33 sherds | 21/32 (conduit and outlet type) | Correction of term only ("tunnel", not just "conduit"). No date for the waterworks. |
| 127 Kh. Shibli | 116 / IMG_2005 | A plastered structure on the summit **with steps descending into it**. Base of a **stone measuring cup**. Robbed rock-cut tombs about 100 m north with **ossuary fragments**. A **coin of Herod**. | P(?) and Hell 47%; Rom 23%; Byz 30%; 211 sherds | Second Temple comparandum (probable miqveh: INFERENCE) | None. Not a candidate place. |
| 136 Kh. el-Judeira | 121 / IMG_2002 | A pool **about 2.5 m deep**; steps to a raised surface; many tombs to the west with an arched opening set in a square frame; a vaulted building at 15840 14125. | P(?) 2 sherds; Hell 8%; Rom 14%; Byz 73%; Early Islamic 3%; 150 sherds | Type only | None. Confirms the 12 Oct read. |
| 173 | 160 / IMG_1981 | A SW rock-cut pool **11.7 × 2.5 m**; 5 alluvium-filled graves; a cistern with mouth-stone and trough beside a monumental threshold. The authors infer a Hellenistic settlement in the east and a Byzantine spread to the west. | Iron II 4%; Hell 47%; Rom 6%; Byz 43%; 73 sherds | Mizpah sector (near Tell en-Nasbeh) | None. 11.7 m confirmed from the photo. |
| 174 Kh. Suweika | 160 / IMG_1981 | About 600 m W of Tell en-Nasbeh. About **50 m south** of the monumental building is an **arcosolium tomb, with a cistern and a rock-cut basin with a flight of steps** beside it. 3 cisterns. Test excavation by Dinur and Zeidan. | (see p. 161) | Mizpah sector; tomb + stepped basin | None. No dimensions. |
| 175 Tell en-Nasbeh | 161 / IMG_1981 | Bibliographic summary only (McCown 1947; Wampler 1947). Aerial photo on p. 161. | — | Mizpah | Nothing new. |
| 176 Kh. ʿAtara | 162 / IMG_1980 | Pools W **24 × 11.5 m** and E **32 × 14.5 m**, partly rock-cut and partly built. At the bottom of the W pool is a vaulted corridor with a water channel under it; the channel feeds the pools and is built of **stone pipe sections**. To the north is a cemetery with **kokhim and arcosolia**. About **100 m north**, a partly cut, partly built pool **that cleaned the water of ʿEin Abu Iskandar**, with remains of a channel of open stone sections nearby. | Byz, 30 sherds; McCown 1947 pp. 54–55 | R08/R09 Atara outlet (already in the feature workbench) | Confirms the dimensions. **Adds:** a kokhim cemetery north of the pools, and a third (spring-cleaning) pool about 100 m north. No phase join. |
| 195 Wadi Sheiban | 172 / IMG_1975 | Two cemeteries south of Beitin. The southern one has 12 tombs of bench, arcosolium and **kokhim** types, with bones and sherds. A rock-cut pool about **5 × 4 m**. A **plastered pool with a flight of steps** and an installation with cut basins (cross-ref. site 80). Four more tombs west of Beitin. | (no assemblage line on this page) | Tomb + stepped pool | None. |
| 196 | 172 / IMG_1975 | Two elaborate rock-cut tombs; the facade of one has **2 columns** (distyle facade). Types: kokhim and arcosolia. Four more tombs about 150 m NE. | — | 51 (tomb with vestibule/pillar; type only) | INFERENCE: a type comparandum only; entry 51 is in Jerusalem. |
| 206 Jaba (Geba) | 179 / IMG_1972 | Pool at 17510 14045, partly rock-cut, **11.3 × 6.4 m, 1.6 m deep**. Its long sides are ashlar outside and fieldstone inside. Many cisterns near the old road to Mukhmas. A jar handle with a two-winged *lmlk* stamp in the village core. | Iron I 2%; Iron II 23%; Hell 22%; Rom 10%; Byz 4%; Early Islamic 9%; Med 5%; Ott 14%; unidentified 11%; 284 sherds; Kallai p. 183, site 125 | Geba (candidate-list place) | Confirms 1.6 m. No pool date. |
| 229 | 189–190 / IMG_1967, IMG_1966 | 17620 14475. Four shaft tombs (two robbed); oval chambers 5–7 × 2 m; shafts 1.0–1.2 m in diameter; 2 cisterns. A square boulder enclosure with a cistern at its NW corner. A building with 2 large stone roof beams. 3 tombs nearby, one with kokhim. | No sherds that allow a conclusion. | — | None. |
| 230 | 190 / IMG_1966 | 4 cisterns; oil-press bed 2.2 m across and 70 cm high. | Byz, 5 sherds | — | None. |
| **231 Kh. Marjama — EXPOSED** | 190 / IMG_1966 | 17775 14035; 580 m; 15 dunams; permanent water 1 km. Fences and many heaps of fieldstones, with wall tops of courtyards and rounded buildings showing; internal divisions in places; 5 buildings counted; a central courtyard about 30 m across. **No pool, cistern, pit, cave or tomb is named.** | **IB majority; Iron single sherd; Hell single sherd; Byz (from the nearby monastery)** | Koḥlit models (exposed) | See §4. The 12 Oct read had already opened these pages, so this adds no new exposure, but I label it EXPOSED as instructed. |
| 234 Kh. ed-Duweir | 194 / IMG_1964 | Many building stones; cisterns; a rock-cut **channel roofed with stone slabs**. Several rock-cut caves to the east and south. **Sheikh Duweir's tomb about 50 m east**. No other grave. | Byz 54%; Med 23%; Ott 23%; 35 sherds; Kallai p. 182, site 119 | Chain `E357-1-graves-north` | See §4. |
| 239 Kh. Kafr Nata | 198 / IMG_1962 | Vaulted buildings; a mihrab; dwelling caves, some with **closure fittings at their openings**; a silted pool **15 m long** to the south, partly rock-cut and partly ashlar; **7 cisterns**. **Sheikh ʿUmar's tomb west of the site**, with many cuttings beside it. No other tomb. | 42 sherds, Byz and Med; Kallai p. 179, site 100 | Chain `S2096-2-mouth` | See §4. |
| 240 | 198 / IMG_1962 | 5 buildings; one stands to full height, **3.2 × 2.1 m**, walls 1 m thick, with a stone-slab floor. Threshing floors and fences to the east. **No pool.** | Iron II single sherd; Byz 6 sherds | Chain `S2096-1-pool-east` | See §4. |
| 302 Kh. Beit Tulma | 226 / IMG_1948 | A spring beside the wadi bed east of the ruin, with a pool next to it, **18 × 13 m, 5 m deep**, walled in stones with drafted margins. About 100 m SW, a square building of similar masonry with 13 m sides. | No sherds (dense vegetation) | Jerusalem N fringe; pool type | None. Confirms the 12 Oct read. |
| 303 | 226–227 / IMG_1948 | Robbers' pits in a NW building yielded large quantities of **Herodian lamps** and other vessels; the authors suggest a workshop. **2 small plastered pools.** About **100 m NW, 2 tombs: one with 6 kokhim, one a shaft tomb**. A winepress vat; 6 cisterns; **Herodian stone vessels**. Damaged by Jordanian fortification works. Pottery plate on p. 227 (Herodian lamps 19–21; scale 0–10 cm). | Iron II 20%; P single sherd; Hell 25%; Rom 25%; Byz 20%; Early Islamic 8%; Ott few; 760 sherds | Jerusalem N fringe; 1st-c. comparandum | **Adds** the 6-kokhim tomb and shaft tomb, the cistern count and the assemblage to the 12 Oct note. |
| 313 Nebi Samwil | 234 / IMG_1944 | Cut pools; the largest is **15 × 10 m**; coloured mosaic. | Iron I single sherd; Iron II 36%; P(?); Hell 8%; Byz 25%; Early Islamic 15%; 211 sherds (Med/Ott excluded) | N fringe | Confirms. |
| 314 | 234–235 / IMG_1944 | Spring installations along a cliff with several springs; a large cave in the cliff centre with a spring rising in it. To the NW, **two kokhim tombs and beside them another rock-cut cave with a spring**. | Iron II(?); Byz majority; Early Islamic(?); Ott; 42 sherds; Sapin 1968, site 54 | Tomb + spring-cave relation (type only) | INFERENCE: kokhim tombs directly beside a spring cave. A generic comparandum; undated. |
| 315 el-Jib (Gibeon) | 235 / IMG_1944 | Summary of the excavations only: occupation EB to Byz; cemeteries on the W slope (EB–LB) and E slope (Iron II). Pritchard 1961–64; Pringle 1983; Eshel 1987. | — | Gibeon | Nothing new. |
| 316 | 235 / IMG_1944 | 16880 13730. Presses and installations; a rock-cut room with a carefully cut rectangular doorway; 5 cisterns; 2 tombs, one **a kokhim tomb with a gabled ceiling**. | — | N fringe; type | None. |
| 317 | 236 / IMG_1943 | A farm along a cliff with 3 springs. East of the southern spring is a building that may have served as a pool; its south wall survives **14 m long, 2.10 m high (5 courses)**. A bench tomb about 110 m E; 2 bench tombs to the south. | Byz | — | None. |
| 319 Kh. el-Biyar | 236–237 / IMG_1943 | Two ashlar pools with drafted margins in the wadi bed to the south. **Remains of an aqueduct adjoin the eastern pool.** Collapsed, silted tombs to the north; 2 cisterns; a NW installation with a mosaic floor. | Iron II 15%; Hell 24%; Rom 27%; Byz 31%; Early Islamic few; 90 sherds; Kallai p. 186, site 144; Sapin 1968, site 57 | Pool + conduit type near Jerusalem | None (no dimensions, no join). |

The English summaries for Parts 1–2 add nothing beyond the 12 Oct read that bears on a candidate entry. The Beth-Horon sites (12, 22, 28, 139–145) and the tomb table on pp. 123–125 were skipped as instructed.

## 4. Effect on Koḥlit chain links and rarity units (PROPOSALS)

Each chain link's success and contradiction wording comes from `research/assessments/kohlit_chain/chain.json`. Those were registered before this reading.

| Link / unit | Record now read | Result against the registered criterion | Proposal |
|---|---|---|---|
| `S2376-1-pool-east` (Tell Maryam; "Kallai site 115; Feldstein site 210") | Feldstein 210, p. 180 (new) | **No pool is described.** There is **no absence statement**, so the contradiction ("record states … no pool") is not met. Kallai's pool is on the northern slope, not the east. | Mark the Feldstein half of the link as read with no decision. The link stays open. Both named records have now been read and neither places a pool in the east sector. Under the "absence-statement only" strength, neither can contradict it. |
| `S2096-1-pool-east` (Feldstein 240) | p. 198 | No pool; no absence statement. | Read, no decision. |
| `S2096-2-mouth` (Kh. Kafr Nata S2033; Feldstein 239) | p. 198 | The only tomb named is **Sheikh ʿUmar's tomb, west of the site**. No burial tomb is near any cistern or cave mouth. The record does not *date* the tomb, so the contradiction as worded ("dates the only tomb as a later shrine") is **not strictly met**. | Not success. INFERENCE: a sheikh's tomb is a later shrine by type. The integrator should decide whether that meets the wording. If not, the link stays open. |
| `E357-1-graves-north` (Feldstein 234) | p. 194 | The only grave is Sheikh Duweir's tomb **about 50 m east**, not north. There is no completeness statement. | Not success; no contradiction. |
| Rarity unit S2376 (Tell Maryam), C3 | Feldstein 213, p. 181 (new) | A Roman kokhim cemetery with an ossuary fragment lies 776 m at 15°. C3 (survey level) was already MATCH from WBADB rows. This adds a **dated** Roman grave in the sector, with no pit-mouth relation. | Any recoding must be an exploratory addendum. The Stage 2 count is frozen. |
| Rarity unit S2488 "Kh. Marjama, other site" (Feldstein 231) — **EXPOSED** | p. 190 | The entry names no pool, pit or grave. **Its Hellenistic presence rests on a single sherd** (EVIDENCE). | INFERENCE: S2488's place in the Hel/Rom main set rests on that single sherd. Note it as a sensitivity in the rarity limits. |

**Identity note (INFERENCE).** The chain model `MARJAMA-1-kallai-pool` is the Kh. el-Marjama at ʿEin Samiya: WBADB S1658, 181600/155400, Kallai site 65. **Feldstein 231 (S2488, 177750/140350, Wadi Suweinit) is a different site about 15 km to the SSW.** Nothing in 231 bears on the ʿEin Samiya pool or on the 19 Oct Kallai result.

No rating, reading or outcome count changes are proposed.

## 5. Plans and figures worth archiving (none opened here is a scaled plan)

| Page | Figure | Scale | Note |
|---|---|---|---|
| 61 | Site 46, Fig. (general view of pool and building) | none | photo of the slab-covered tunnel's terminal pool |
| 116 | Site 127 pottery plate (Hell 1–5, Hell/Rom 6–15, Rom 16, Byz 17–25, EIs 26; Roman stone vessels 27–28) | 0–10 cm bar | stone vessels |
| 161 | Site 175, Tell en-Nasbeh aerial | none | |
| 163 | Site 179 pottery (Iron I) | 0–10 cm bar | |
| 178 | Site 206 Jaba, Fig. 2 pottery (Iron I 1–8, Iron II 9–15, Hell 16, Hell/Rom 17–18) | 0–10 cm bar | |
| 188 | Site 227, Fig. 1 pottery | 0–10 cm bar | |
| 189 | Site 227, Fig. 2 aerial | none | |
| 191 | Site 231, Fig. 1 aerial looking east; Fig. 2 IB pottery 1–14 | Fig. 2 has a bar | **EXPOSED** |
| 195 | Site 235 pottery (MB 1–3, Iron I 4–10) | 0–10 cm bar | |
| 227 | Site 303 pottery incl. Herodian lamps 19–21 | 0–10 cm bar | |
| 234 | Site 313 pottery (Iron I 1, Iron II 2–12) | 0–10 cm bar | |

All rights are reserved (IAA 1993). Retain the Drive photo links; no reuse permission is recorded.

## 6. Photos used

Read: IMG_1799–1815 (English 13*–45*); IMG_2045 (pp. 38–39); IMG_2034 (60–61); IMG_2005 (116–117); IMG_2002 (120–121); IMG_1981 (160–161); IMG_1980 (162–163); IMG_1975 (172–173); IMG_1972 (178–179); **IMG_1971 (180–181)**; IMG_1967 (188–189); IMG_1966 (190–191); IMG_1964 (194–195); IMG_1962 (198–199); IMG_1948 (226–227); IMG_1944 (234–235); IMG_1943 (236–237).

Downloaded and hash-checked but not read: IMG_2035 (58–59), IMG_2019 (88–89), IMG_1969 (184–185), IMG_1968 (186–187).

One Drive ID copied by hand (p. 168) returned "not found". The correct ID is in the manifest; the page was not needed.

Files are in (session workspace, not retained) (`dl/` holds the downloads and `sha256.txt`; `img/` holds the JPEG crops; `scripts/` holds the conversion scripts).

## 7. Exposure log

- **Kh. Marjama 231 (p. 190, Fig. 1–2 on p. 191): opened, EXPOSED.** These pages had already been opened in the 12 Oct full read.
- **Feldstein 210 (Tell Maryam), 213, 239, 240 and 234:** read against registered chain links (§4). These are record reads under the registered criteria, not unseen tests.
- **Incidental, text only (no images, no frames).**
  - The `research/ACTIVE_TEST.md` item 1 status paragraph names the XII 10 Janoaḥ question and summarises the saw-gap check (that the cut cannot hide a whole yod or waw, and that ה/ח is open).
  - `kohlit_chain/next_links.md` row 10 (JANOAH-0 reading gate) and its README line on the `yanun-marjama-anchor` model.
  - `rarity/kohlit/stage2/RESULTS.md` rows naming Kh. Yanun units.
  - `OPEN_QUESTIONS.md` R07 line 180 (Marjama assignments excluded).
  - These were seen while reading the files that AGENTS.md and the brief require. I opened no Yanun/Janoaḥ file, XII 10 commentary or image.
- **Not opened:** any Copper Scroll image of columns XI–XII; USC CT19–CT23; `research/preregistration/` (every search excluded it); any held page or held area.
- **Shared download cache.** I moved each of my own Drive downloads out of the shared tool-results cache into `sweep/benj13/dl/` right after downloading it, matching each one by its unique random filename suffix. All 37 files hash-match their manifest entries, so none belongs to another agent. If another agent finds files missing from the cache, they may be these, and they can download their own copies again.

## Integrator note (main session, 30 Oct 2026)
- New evidence: Hebrew pp. 180–181 (IMG_1971), which the 12 Oct full read missed. Accepted without a main-session photo check.
- EXPOSED: Kh. Marjama site 231 (pp. 190–191), already opened on 12 Oct.
- Decision for a repo session: does Kafr Nata's undated sheikh's tomb meet the `S2096-2-mouth` contradiction wording? Not applied.
