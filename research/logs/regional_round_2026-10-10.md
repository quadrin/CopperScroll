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

- **Owner downloads** (free, but behind a browser check): the IAA portal volumes in [portal_pdfs_needed.csv](../regional/haesi_features/phase2_2026-10-10/portal_pdfs_needed.csv), priority A first, including HA 28–29; IAA Reports 7 (Jericho cemetery) and IAA Reports 1 (Akeldama); five ʿAtiqot hoard articles listed in the hoards README.
- **Through the owner's library or loans:** the IEJ 1961–62 Judean Desert caves reports (JSTOR); Kloner & Zissu 2007; *Masada* III (tower plans); IGCH and *Coin Hoards* I–X (Internet Archive loans); Eshel & Zissu 2019; the Porat refuge-cave reports; Zissu 1995 (academia.edu); the 2002 *Aqueducts of Israel* (interlibrary loan already pending).
- **A later session:** the Jerusalem tier of the online HA-ESI reports from position 81 (582 left); the Annual of the Department of Antiquities of Jordan for hoards; ASI sheets that are not online (Qumran–Feshkha shore 109/8, Jericho 83/13, Beth Guvrin–Maresha, Hebron).
