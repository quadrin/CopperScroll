# Regional round 2, 10–11 October 2026

The owner asked the project to stop looking only at places already proposed for the scroll. For six kinds of evidence, the aim was to inventory every recorded example in the region and score them all against the entry in the same way. Six workers ran in parallel, one folder each, and each froze its plan in a commit before it scored anything. The integrator merged the six branches (merge commits a012ca7 to a9c659a) and owns the shared files.

All of this work is exploratory. It makes no identification claim. No registered result, closed test, outcome-ledger count or atlas candidate changed. The counts give denominators: how many recorded features meet each clause, how many fail it, and how many records are silent. In every lane, most records are silent on most clauses, so rarity cannot be measured yet. A zero rejects nothing.

## What was built

| Lane | Folder | Freeze commit | Main result |
|---|---|---|---|
| IAA reports, phase 2 (HA, ESI, HA-ESI) | [haesi_features/phase2_2026-10-10](../regional/haesi_features/phase2_2026-10-10/README.md) | d0f8c7c | 274 more reports coded (95 from ten ESI/HA volumes on the owner's computer, 179 online HA-ESI reports). The online title screen covered all 22 volumes (4,667 titles, 798 candidates). 526 feature rows in the region, 98 dated by the report to the window. Desert, Jordan Valley, Gerizim and Jerusalem-hills tiers read in full; the Jerusalem city tier only sampled (80 of 662). The 111 portal volume PDFs could not be read in the browser and were not downloaded. |
| Caves, entry 25 | [caves_entry25](../regional/caves_entry25/README.md) | 2ff6e5a | 635 cave rows (605 after merging duplicates) from Jericho to Naḥal Ḥever. Cave-level pillar reading: 1 matches every clause, 198 fail, 436 unknown. The match is ʿAtiqot 41 cave XII/53 in Naḥal Qumran: an east-facing opening divided in two by a built pillar (undated), with an Early Roman layer in the cave. At the stricter both-mouths level only the Twin Cave (already in the repo) matches. Terrace reading: no match. |
| Columbaria, entries 38 and 44 | [columbaria](../regional/columbaria/README.md) | afdd69f | 179 rows (at least 269 columbaria) in Judea. Only the dovecote reading is tested; of the four core editions only Puech reads it. Entry 38: no recorded columbarium within 2 km of either Netophah candidate (the ASI map there records none; silence, not absence). Entry 44 (Puech): 3 match, Masada's three towers, resting on Netzer's reconstruction drawing; 55 fail, 121 unknown. |
| Tombs, the tomb entries | [tombs](../regional/tombs/README.md) | cd394d7 | 1,055 tomb units. Jerusalem (within 5 km of the Temple Mount), strictly dated to the window: 197. No survey record names Zadok or carries an ancient garden. The single matches are already-known places: Absalom's monument record (102/410) for 48, the Tomb of the Kings (102/320) for "the Queen" in 27, and a Kidron burial cave with a bone repository (102/408) for 14 and 53 (the 53 match only through the distance tolerance). West-facing kokhim tombs are common. The Jericho cemetery is barely covered: its report (IAA Reports 7) is behind a browser check. |
| Water installations, entries 21, 22, 29, 32, 42, 45, 46 | [water_systems](../regional/water_systems/README.md) | 0b07fad | 1,437 merged units (2,043 rows). No conduit head has a recorded stone on its north (verified count 0). No reservoir with "Solomon" in its name has a fissure recorded to its east. Entry 29: 0 matches; three dated reservoirs miss only "northern" (Lower Herodium pool, Qumran L71, Birket Musa); the closed entry 29 result is not reopened. Entry 45: one cistern fed by channels from a large wadi (Hyrcania). Exploratory lead for entry 32: the ʿArrub aqueduct starts at ʿEin Kuweiziba. |
| Hoards and hidden deposits | [hoards_full](../comparanda/hoards_full/README.md) | be266e2 | 204 deposits (23 new). The scroll's mix of hiding places still differs from recorded deposits (D = 0.68, p = 0.00005, 78 with known context), but the new known-context deposits are almost all Qumran caves. Only 5 deposits state a depth (median 0.5 m); half or more of the scroll's dig depths lie deeper than the deepest one. No recorded deposit sits by a step, pillar or gate. |

## Integration

- Every lane's tests pass on the merged tree (IAA 16, caves 12, columbaria 10 + 1 skipped, tombs 13 + 2 skipped, water 12 + 1 skipped, hoards 13; the concealment precedent 15 and phase 1 IAA 10 still pass). Skips need the local survey caches.
- New files are text only (about 10 MB of tables). No PDF, page image or full text was committed; long fields are the workers' own notes and citations.
- Shared files changed: this index, the findings log and its atlas mirror, ACTIVE_TEST (last-session line and key reports), and OPEN_QUESTIONS R01 and R02 with the byte-identical atlas copy.

## Exposure and deviations

- The caves lane read the ʿAtiqot 41 cave entries (Tier 1 in the arrival register) after its plan was frozen. It reclassified XII/49, XII/52 and XII/53 as already exposed, because the repo held their report titles and period summaries. XII/53 can serve as a named control in any future entry 25 test, not as a holdout.
- The IAA lane held seven cave items unread for the arrival procedure (online reports 25219, 25868, 126 and 25871; ESI 6 pp. 66–68; ESI 7–8 pp. 92–93 and 95–97). It read ESI 3 pp. 61–62 and ESI 5 p. 58, both in held areas, before checking the hold (deviation D1). Neither gives an opening direction.
- The columbaria lane read the ASI record of Kh. ʿAlmit after its freeze; the Tier 1 IAA notices on Kh. ʿAlmit stay unread. The water lane flagged its Kh. ʿAlmit rows.
- The online HA-ESI reports were read through the owner's own browser, one page at a time, at his request. No bot check appeared and nothing was downloaded.
- Two workers' scratch caches collided (the tombs worker wrote into a shared survey cache, then moved its files back). One Downloads listing used a filter that also matched unrelated file names; none was opened or recorded.

## Proposed, not applied (owner or a later session decides)

- Arrival register: add the seven held IAA cave items; record deviation D1 against the IAA-archive cave-records item; compare the Kh. ʿAlmit extraction (`ESI05-001-kh-almit`) under the arrival procedure. The caves lane notes that no ʿAtiqot 41 record gives a compass facing for IV/11, IV/17 or the Twin Cave, and that the Index lists IV/17 as permit L-656 and IV/11 as L-603.
- Concealment precedent data (not edited): CHRE 8178 placement `wall_cavity`; CHRE 5386 lay in the NE corner of the NW room (Leibner 2010 p. 225); the Naḥal Shalva hoard lay near a skeleton. None changes a coarse group.
- Archive the 1989 aqueducts-volume figures listed in the water README under `research/assets/plans/aqueducts1989/`.
- Labels to watch: "Q3" means both the Copper Scroll cave (ESI 6) and X/35 (ʿAtiqot 41); WBADB has a separate "Cave of the Pillar" about 360 m from the Twin Cave.

## What would fill the gaps

- **Done 11 October:** all 101 IAA portal volumes and IAA Reports 7 and 1 are now on the owner's computer (`~/Downloads/IAA portal volumes/`, hashes in [portal_downloads_2026-10-11.csv](../regional/haesi_features/phase2_2026-10-10/portal_downloads_2026-10-11.csv)); none read yet, and HA 28–29 only under the arrival procedure. **Still for the owner:** five ʿAtiqot hoard articles listed in the hoards README.
- **Through the owner's library or loans:** the IEJ 1961–62 Judean Desert caves reports (JSTOR); Kloner & Zissu 2007; *Masada* III (tower plans); IGCH and *Coin Hoards* I–X (Internet Archive loans); Eshel & Zissu 2019; the Porat refuge-cave reports; Zissu 1995 (academia.edu); the 2002 *Aqueducts of Israel* (interlibrary loan already pending).
- **A later session:** the Jerusalem tier of the online HA-ESI reports from position 81 (582 left); the Annual of the Department of Antiquities of Jordan for hoards; ASI sheets that are not online (Qumran–Feshkha shore 109/8, Jericho 83/13, Beth Guvrin–Maresha, Hebron).

## Reading pass, 11 October 2026

With the owner's approval the IAA portal volumes and two IAA Reports were downloaded to his computer, then read by five more workers (merge commits d8983c0 to 198ec5c).

- **IAA reports, phase 3** ([README](../regional/haesi_features/phase3_2026-10-11/README.md); scope frozen in commit 4d8325e, phase-2 rules unchanged): all 101 downloaded volumes screened heading by heading, the online Jerusalem tier finished. 1,260 more reports coded; 2,582 feature rows in the region, 628 dated to the window; all 684 phase-1 candidates in these volumes accounted for. Rows are not yet deduplicated across seasons or across Hebrew and English versions. HA 28–29 and the Kh. ʿAlmit notices were extracted blind; no arrival item exists for them, so nothing is scored.
- **Tombs addendum** ([README](../regional/tombs/README.md), section "Addendum, 11 October 2026"): IAA Reports 7 read by OCR, 104 Jericho tomb units coded (25 dated to the window; entrances 8 north, 12 east, 7 south, none west; names in A2, D1 and H, none Zadok or Absalom). Under the frozen rules every region-B count is unchanged, because the report gives no grid positions and every tomb is a possible duplicate of the cemetery's WBADB row. Counted alone, "the Queen" (27-T) gets one hit, Tomb H, where an ossuary names Queen Agrippina as a freedman's patron; it is not her tomb. Akeldama (IAA Reports 1, exploratory amendment 2): three first-century caves, no Region A count changes.

## Phase 4: more sources, 11 October 2026

The owner asked for more of the region's reports to be mined. Five workers read ʿAtiqot, IAA Reports, QDAP, the nineteenth-century surveys and ADAJ under the phase-2 rules, unchanged. The scope was frozen in commit b002e03 and the parts were merged in commits 26d7ded to 9d4e011. See the [phase-4 README](../regional/haesi_features/phase4_2026-10-11/README.md).

- **Read:** 347 units in the region gave 265 feature rows: 22 dated to the window, 91 dated outside it, 152 undated. There are also 94 SWP rows split between two zones.
- **Waiting for the owner:** ʿAtiqot 42–121 and IAA Reports were screened only. Their 249 in-region PDFs need his approval to download.
- **Exposure:** four parts saw some held text before applying the hold, including ADAJ 16 pp. 5–12 (Kenyon, "Burial Customs at Jericho"). Nothing was coded from it, and the exact lines are in each part's NOTES.
- **12 October, reading of the portal PDFs.** With the owner's approval, the 249 ʿAtiqot and IAA Reports PDFs were downloaded to his Mac and read by four readers (merge commits after 8f01a3b). 245 units were read and 453 feature rows coded: 130 dated to the window, 215 dated outside it, 108 undated; 426 of the rows are in Z4. Phase 4 now totals 592 units and 718 single-zone rows (152 / 306 / 260). Nothing was held. Two IAA Reports chapters are missing from the portal scans.
