# Entry 24 and Mughâret Ekteif: result of the frozen test (6 November 2026)

Protocol: [PROTOCOL_FROZEN.md](PROTOCOL_FROZEN.md), committed in 8d97a0d at 2026-11-06T20:12Z (SHA-256 `d0e441e027ff45426a2b08e80e81f92c3ee1c0d81a3d1f94dd67a320bbc021d2`). Blind reader scores: [reader_scores.json](reader_scores.json), SHA-256 `83a50ba8e096a8f41502653e56de51efbf57c3da02a31cc52d35ec1d044d0eb1`, written by the reader and hashed at 2026-11-06T20:24Z, before unblinding.

## Outcomes

| Claim | Outcome | Reason |
|---|---|---|
| **A.** A visible open cut of the SWP size lies within 300 m of the SWP sheet XVIII label "Mght. Ekteif" | **Not identifiable from available evidence** | Decision rule step 1: the positive control P (Kh. Qumran) was not positive. The reader marked no probable feature in any of the 10 windows, so the method did not show known cut features at this scale. |
| **B.** Mughâret Ekteif is the tomb of entry 24 (V 12–14) | **Not identifiable from available evidence** | As stated before the reading: no available observation gives the kind or the date of the excavation, and the 24-J controls include window-dated tombs. Branch T2 (Allegro) has no route clause, so the route cannot reject the claim. |

Registered prediction P1 (T positive, on the north side of the drainage line, with c ≤ 2): **not tested**, because the adequacy condition failed first.

## What was run

- **Epoch E1.** Esri World Imagery at zoom 18. Its metadata at the target gives WorldView-2, 21 Oct 2023, 0.5 m (Vantor). Ten windows, each 600 m × 600 m at 0.5 m per pixel, in the frozen shuffle (seed 3504620000). The reader read them as W01–W10.
- **Epoch E2 (HEXAGON, 25 June 1974): left out, as the frozen rule requires.** F015 does not reach the target: its tiles a–g lie side by side, and the target is about 1.3 km north of the frame edge. F014 tile d covers it. A local SIFT registration of F014 against Esri at four anchors 4 km from the target gave 3–5 inliers with impossible scales and rotations, so the RMS ≤ 60 m condition was not met. The registration crops (at 1.75 m per pixel, and Esri at 2.4 m per pixel) reach no closer than about 1.4 km to the target, and nobody viewed them.
- **Reader.** A separate agent saw only the ten PNG files and the feature definition. It was told nothing about the scroll, the place or which window was the target.

## Mechanical scoring (after unblinding)

| Window | Role | Usability | Disturbed (central circle) | Probable | Possible | Positive | Eligible |
|---|---|---|---|---|---|---|---|
| W06 | T (target) | usable | <25 % | 0 | 1 | no | yes |
| W08 | P (Kh. Qumran) | usable | 25–50 % | 0 | 0 | **no** | yes |
| W07 | C1 (0°) | usable | <25 % | 0 | 1 | no | yes |
| W04 | C2 (45°) | usable | >50 % | 0 | 1 | no | no |
| W10 | C3 (90°) | usable | 25–50 % | 0 | 1 | no | yes |
| W01 | C4 (135°) | usable | <25 % | 0 | 0 | no | yes |
| W03 | C5 (180°) | usable | <25 % | 0 | 0 | no | yes |
| W02 | C6 (225°) | usable | <25 % | 0 | 0 | no | yes |
| W05 | C7 (270°) | usable | 25–50 % | 0 | 1 | no | yes |
| W09 | C8 (315°) | usable | <25 % | 0 | 0 | no | yes |

Result: n = 7 eligible controls, c = 0. The criterion itself did not discriminate, because it was never met. The reader's note says that the imagery is soft (resampled) and that features about 2 px wide are only just visible. The reader also excluded the walls of the excavated ruin and the trench networks in P under the "not a wall / not a continuous network" clauses. INFERENCE: the definition was too strict for this imagery. It is not evidence that the excavation is absent.

## Exploratory notes (after unblinding; not evidence for either claim)

- The reader graded one feature in the target window as `possible`. It is about 32 m long and about 1.5 m wide, about 250 m from the centre, on the north side of the marked drainage line, and on a bare slope just south of a modern highway. On my look after unblinding, it is a curved dark line. It can be an erosion rill or a road-works cut as well as a sloping excavation. Its position is in the private files only.
- The target window has a modern highway across its northern part and a group of modern buildings near its centre. Alternative a2 (destruction by road works) is therefore realistic for the north side of the valley. This is an inference from one image, not a tested result.
- **Route component (exploratory).** The private point lies inside the 3 km corridor of all 8 Jericho→Secacah lines: from Tell es-Sultan and from Tulul Abu el-ʿAlayiq to Kh. Qumran, Kh. Abu Ṭabaq, Karm es-Samra and Kh. el-Maqari. The route clause does not separate the candidate from the 24-J controls.

## Exposure after this test

The ten E1 windows (target, 8 controls and Kh. Qumran) are now **EXPOSED** for any later test. Eight of them are in held area H1. The reader agent and this coordinator have seen them. A repeat of this test on the same imagery would be exploratory.

## Reopening conditions

- **Claim A** reopens only with a new observation. Examples are an unviewed epoch at the target (a 1940s RAF frame that covers the lower Wadi Ekteif, or a registered HEXAGON F014 window) read under a revised, newly frozen criterion with a positive control of known size, or a field visit to the private point. A revised criterion applied to the same 2023 windows would be exploratory.
- **Claim B** reopens with a dated plan or finds from the excavation, or a new reading of V 12–13.
- The project assessment is unchanged. The entry 24 rating keeps its "decisive next" ("a dated record of the stepped chamber"). This pass adds a private position that is accurate to about 250–300 m.
