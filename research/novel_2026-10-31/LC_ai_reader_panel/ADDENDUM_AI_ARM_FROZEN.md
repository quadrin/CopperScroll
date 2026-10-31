# Letter controls: AI reader arm on series S1 (dated addendum, 31 October 2026)

Frozen before any reader has seen any item. Coordinator: a Claude Opus 5.5 instance (not a reader). Branch `claude/novel-2026-10-31-LC`.

This is a dated addendum under [PROTOCOL.md](../../text/letter_controls/PROTOCOL.md) §12 (letter-control calibration, prepared 8 October 2026). It adds one **exploratory AI reader arm** under §7. It changes nothing in the protocol, the frozen [XII 10 reading protocol](../../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md), the manifest, `sealed_key.sha256` or any other file in `research/text/letter_controls/`.

## 1. What this arm is and is not

- **Question.** Can separate AI readers tell ב from כ, ה from ח and ת, and an independent yod/waw from no sign, from the strokes alone, on the full-resolution 1988 West Semitic Research Project (WSRP) frames (series S1)?
- **Why now.** Earlier on 31 October every automatic method failed on these frames: photometric stereo (A2) and three render-and-compare models (B2, B3, B4). This arm asks whether readers can do what those models could not.
- **Status.** Exploratory. It is reported separately. It never replaces the two frozen human readers. It never enters the decisive XII 10 rule. Under §7, "an AI reader may run as an exploratory arm; it never replaces a human reader".
- **What a PASS would mean.** Exploratory evidence that these AI readers read these strokes on S1 windows of columns I–X. It would **not** calibrate the frozen XII 10 readers, and it would not change any XII 10 verdict, reading, rating or outcome count.
- **No target.** The arm has no target slot. No image of cuts 21–23 was opened. No XII 10 window exists in the packet.

## 2. Readers

| Reader | Model | Role |
|---|---|---|
| A | Claude Opus | Registered pair, first reader |
| B | Claude Sonnet | Registered pair, second reader |
| C | Claude Fable | Reported separately; never in the pair rule |

- Each reader is a separate model instance. It sees only the packet: `INSTRUCTIONS.md`, `responses_template.csv` and the 93 item PNGs. It sees no manifest, key, edition, transcription, project file or other reader's answers.
- Readers A and B are the registered pair for the decisive rule **within this arm only**: both `certain` and the same identity.
- The orchestrator starts the readers. The coordinator does not start them and does not score.

## 3. Series, lighting and resolution

- **Series.** S1 only: WSRP 1988 photographs (USC delivery), full-resolution frames. The arrays were read from A2's cache, which A2 built with `hexview.py` (SHA-256 `56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236`). The coordinator made no new bucket read.
- **Lighting class.** Top-centre and bottom-centre light. The XII 10 target frames are CT21 (RT, RB) and CT22 (six lights, including RCT and RCB), so this class exists on both target cuts.
  - Six-light cuts 3, 6, 7, 8, 10, 11, 16, 18: RCT and RCB.
  - Two-light cuts 4 and 17: RT and RB.
  - Cut 2 has only corner lights (RLT, RLB, RRT, RRB). Its candidates are excluded.
  - Each bottom-lit frame is warped into its top-lit reference frame with A2's registration (`reg/reg_cutNN.json`). The median residual is 1.57–2.66 px on the cuts with controls and 3.63 px on cut 10 (blank decoys only).
- **Target letter height.** 104.5 px. This number comes from A2's accepted placements of CT21 and CT22 on column XII (`place_cut21_XII.json`, `place_cut22_XII.json`): copy-photo letter height 41.8 px divided by scale 0.400 in both. No image was opened to obtain it.
- **Resolution matching (§5).** Control letter heights on the control cuts are 131.0–195.3 px. Only cut 16 (131.0 px) is near the ±25 % band (78.4–130.6 px), and it lies just outside. So every control and decoy window is resampled by area averaging to a letter height of 104.5 px. The target is never resampled.

## 4. Windows and presentation (§6)

- **Window.** BK and HH: a square of side 2 × letter height (209 × 209 px after matching), centred on the slot. XS: 3.5 × letter height wide and 2 × high (366 × 209 px), centred between the two marked letters.
- **Image.** Luminance (ITU-R 601 weights) of each frame, as cached by A2. The same conversion applies to every item.
- **Two views per light.** Unadjusted, and one declared linear stretch: the 1st and 99th percentiles of each panel map to 0 and 255. The rule is identical for every item.
- **Composition.** One PNG per item: a 2 × 2 grid. Rows: top light, bottom light. Columns: unadjusted, stretched. Each panel sits in a 12 px grey border. Red ticks in the border mark the slot: for BK and HH, the window centre on all four sides; for XS, the two marked letters (above and below) and the line height (left and right).
- **Enlargement.** The composed image is enlarged ×2 by pixel repetition, with no interpolation and no sharpening. Item sizes: 932 × 932 px (BK, HH) and 1560 × 932 px (XS).
- **No text and no metadata.** Each PNG has only the IHDR, IDAT and IEND chunks (checked by the build). File names are the anonymous item codes.
- **XS markers.** They sit at the copy-photo separation of the two marked letters, mapped into the frame. On the blank decoys they sit at the median control separation (0.886 letter heights).

## 5. Placement and check

- **Positions.** The position of each letter on the Puech 2006 copy photograph comes from the W2F (wave-2 plate model) data, in this order of preference:
  1. a verified W2F letter box (`labels_verified.csv`);
  2. the W2F Viterbi letter alignment (`viterbi_colNN.json` with `fac_components_colNN.json`);
  3. a letter interpolated across a W2F word unit.

  Facsimile boxes are mapped to the copy photograph with `registration.json`. They are then mapped into the 1988 reference frame through A2's 12 accepted cut/column placements (`place/*.json`, gate: distinctiveness ≥ 1.8 and local median ≤ 0.15 letter height). The pairs with series lights are cuts 3, 4 → I; 6 → II; 7, 8 → III; 11 → V; 16 → IX; 17, 18 → X.
- **Eye check.** Every placement was checked by eye. The coordinator viewed labelled context sheets (5.2 × 2.6 letter heights, both series lights), with the predicted centre of every letter of the word. Wide line views were used where the alignment was doubtful. The coordinator recentred the window on the slot by eye where needed: 30 shifts, at most 0.45 letter height, all horizontal. One more control, the second kaf of V 11, was set relative to the first kaf, because the alignment had put both kafs at one position.
- **Drops at the check.** 26 controls and 1 decoy were dropped because the slot could not be located with confidence. Reasons: corroded, crumpled or faint surface with no identifiable letter at the slot (9); slot at an out-of-focus strip edge or beyond the saw edge (11); word alignment collapsed or not matched to the visible letters (5); slot on a crack with no distinguishable letter (1); interpolated lacuna slot fell on legible letters (1 decoy).
- **Provisional placements not used.** A2's rejected fits (CT10 → IV, CT11 → VI, CT17 → IX) were mapped as a test, and one sheet was viewed. They failed A2's gate and were not verified. Nothing from them is in the packet.
- **Manual registration of rejected cuts stopped.** The coordinator began a landmark registration of CT5 → II and CT10 → IV from neighbouring Hebrew (side-by-side views) and stopped it. At the observed retention (BK 16 of 29 kept), adding every BK candidate on cuts 5, 10 and 11 would give about 34 BK controls, still under 40. XS would still be under 20 damage-matched controls. Reopening condition: a verified registration of CT5 → II, CT10 → IV/V and CT11 → VI.
- **Placement log.** The private log, with candidate, cut, frames, centre, letter height, method and check result for every manifest control and decoy, is in the coordinator's scratchpad (`panel_coord/placement_log.csv`). It reveals positions and answers and is not committed.

## 6. Items, damage and decoys

Counts in the sealed key (series S1):

| Question | Class | Controls | Damage-matched | Decoys |
|---|---|---|---|---|
| BK | ב | 9 | | |
| BK | כ | 7 | | |
| BK | all | 16 | 6 | 4 blank-surface |
| HH | ה | 21 | | |
| HH | ח | 12 | | |
| HH | ת | 13 | | |
| HH | all | 46 | 23 | 4 blank-surface |
| XS | present | 6 | | |
| XS | absent | 13 | | |
| XS | all | 19 | 7 | 4 blank-surface |
| **Total** | | **81** | **36** | **12** |

All 93 items: 81 controls (all tier A; no tier B control fell on a usable cut) and 12 decoys.

- **Damage grades.** The coordinator graded each control on its S1 window as intact, cut_edge, crack, fold, corrosion or edge_loss.
  - BK: intact 10, crack 3, corrosion 2, cut_edge 1.
  - HH: intact 23, corrosion 9, crack 7, cut_edge 7.
  - XS: intact 12, corrosion 3, crack 3, cut_edge 1.
  - No window was graded fold or edge_loss.
  - The grading was not blind: the coordinator knew each control's identity.
- **Decoys.**
  - No lacuna decoy could be used. Of the 6 manifest decoys in the placeable columns, LC-DHH-002, LC-DXS-003, LC-DXS-004, LC-DXS-006 and LC-DXS-012 have no position on an accepted cut. LC-DXS-007 was dropped at the check.
  - Each question therefore has 4 blank-surface decoys: uninscribed margin of the same frame type, secure answer "illegible". They come from cut 17 (RT/RB, 6 windows), cut 10 (RCT/RCB, 5) and cut 8 (RCT/RCB, 1).
  - Each blank window was viewed. Ten other blank candidates were rejected because they showed letter-like forms, crack boxes or the strip edge.
  - Window size follows each cut's letter height: cut 17 147.9 px and cut 8 169.0 px (A2 placements). Cut 10 has no accepted placement, so a notional 160 px was used. All are then resampled to 104.5 px like the controls.

## 7. §9 status per question, fixed before any reading

| Question | Controls ≥ 40 | Per class ≥ 12 (ת ≥ 6) | Damage-matched ≥ 20 | Decoys ≥ 4 | Status |
|---|---|---|---|---|---|
| BK | 16 ✗ | ב 9 ✗, כ 7 ✗ | 6 ✗ | 4 ✓ | **INSUFFICIENT** |
| HH | 46 ✓ | ה 21 ✓, ח 12 ✓, ת 13 ✓ | 23 ✓ | 4 ✓ | minimums met |
| XS | 19 ✗ | present 6 ✗, absent 13 ✓ | 7 ✗ | 4 ✓ | **INSUFFICIENT** |

- **BK and XS are recorded as INSUFFICIENT now, before any reading.** They are still dispatched, for an exploratory accuracy estimate only. They cannot reach PASS in this arm.
- **HH** meets every item minimum. If both registered readers answer every HH item, it ends PASS or FAIL under §11.

## 8. Key

- Built for this arm in exactly the format of `seal_key.py` (`schema letter_controls_key/1`): anonymous item codes `LC-` + 6 hex digits from the operating system's random source, a random order, a salt and the manifest candidate digest. Each item carries series S1, answer, tier, damage, letter height and crop (cut, the two frames, the centre in the reference frame, the native window size, the resampling factor, the stretch rule and the placement method). Blank decoys have candidate IDs `LC-BLK-<question>-NN`. There are no target slots.
- `seal_key.py record` was not used, because it would append to the frozen human `sealed_key.sha256`. That file is unchanged. No existing sealed key was opened.
- **Key path:** `/root/lc_ai_arm_key/letter_controls_key_ai_arm.json` (outside the repository and outside the scratchpad). Created 2026-10-31T16:15:41Z.
- **Key SHA-256:** `c83877298bf61844ea283969eae09e47e99b71863d7c262841659cc748276d87`. Recorded in [ai_arm_key.sha256](ai_arm_key.sha256) in the format that `scoring.py --sha-file` reads (last line).
- `scoring.load_key` accepts the key with this hash (checked). A format check with synthetic all-"illegible" responses ran once and gave the §9 messages of section 7. No reader response exists.

## 9. Scoring and outcome rule

- Score **once**, after readers A, B and C have all locked every row (`locked_utc` filled). No interim look. No top-up. No item is added or removed after dispatch, except an item found defective before any response is opened; it is logged with the reason.
- Command, from the repository root:

```sh
python3 -I research/text/letter_controls/scoring.py \
    --key /root/lc_ai_arm_key/letter_controls_key_ai_arm.json \
    --responses responses_A.csv responses_B.csv responses_C.csv --readers A B \
    --sha-file research/novel_2026-10-31/LC_ai_reader_panel/ai_arm_key.sha256 \
    --json ai_arm_report.json --text ai_arm_statement.txt
```

- Readers A and B are the decisive pair. `scoring.py` scores reader C individually and never uses C in the pair rule.
- Status per question follows §11 unchanged:
  - **PASS:** lower bound of decisive precision ≥ 0.90; no wrong decisive call on a damage-matched control; no decisive call on a decoy.
  - **FAIL:** the minimums are met but PASS is not reached.
  - **INSUFFICIENT:** a §9 minimum is not met. BK and XS are already INSUFFICIENT.
- §12 voiding rule: a reader's calibration is void if that reader saw the key, the manifest or another reader's answers, or recognised more than one control location in five (`recognized_location`). The question is then INSUFFICIENT.
- Report every reader's confusion matrices, accuracy, balanced accuracy, precision when certain, decoy overcalls and likelihood ratios, as `scoring.py` gives them. Agreement is never cited as accuracy.

## 10. Reader exposure audit

- **Known.** Each reader receives only the packet. Each answers from the PNGs. No reader sees the coordinator's sheets, logs or this addendum.
- **Unknown.** The models' training data may include published images of the scroll and its editions: DJD III plates, the Puech 2006 plates and USC/WSRP images. The windows are small and anonymised and hide the word. Recognition is still possible in principle. Each reader records any recognised location per item, and §12 voids a reader above one in five.
- **Model family.** All three readers are Claude models, and so is the coordinator. Their errors may be correlated. This is a further reason the arm stays exploratory.

## 11. Coordinator exposure log

Opened, as the coordinator only:
- `controls_manifest.csv`, with the secure answers.
- Labelled two-light check sheets of all 108 candidates auto-placed on accepted cuts with series lights (cuts 3, 4, 6, 7, 8, 11, 16, 17, 18).
- Wide line views of V 5, V 11, V 12, V 13, V 14, X 7 and X 10 (cuts 11, 18).
- One sheet of provisional placements on cuts 10, 11 and 17 (not used).
- Side-by-side views of CT5 with copy plate II and CT10 with copy plate IV.
- Region views of CT5 and CT10.
- Overviews of cuts 6, 8, 11 and 17 at 0.16 scale.
- Margin views of cuts 3, 6, 7, 8, 10, 11, 16, 17 and 18.
- Labelled renders of all 93 final items and of 12 further blank candidates that were not used.

Not opened:
- Any image of cuts 21, 22 or 23.
- The column XII copy plate.
- Any existing sealed key.
- SULTAN-1 material, Bavarian SCREEN FIRST, or any PROTECTED folder.

No rating, outcome ledger, ACTIVE_TEST, OPEN_QUESTIONS, atlas data or `research/text/letter_controls/` file was changed.

## 12. Private build files (scratchpad, not committed; hashes for audit)

| File | SHA-256 |
|---|---|
| `panel_coord/place_lc.py` | `165a62c2f50cde7ea2f63a65ffbfbe52a589e4a2fa79e159f66378a99e29137a` |
| `panel_coord/build_panel.py` | `8631614811c1060db846baebab74011b9e9a41f9e8a2cc7286b6ddfe0714cc68` |
| `panel_coord/manual_check.csv` | `3db49007b834cc7621a58ca361754bc5d786c018807642a649e7260b0a3c7c4f` |
| `panel_coord/auto_placements.csv` | `f657685f7aaf8925102583f5006ac9052f765f72a46e032d98467db6306229ea` |
| `panel_coord/placement_log.csv` | `c99df4f2bdb11f415f0aaf469868731417d282e9be92bbea4bbbd3a6742f9bd1` |
| `panel_coord/final_items.csv` | `ac52d5d260c2d78021de05f2fa2691e644e438ef712d3182c224d19f28c5e591` |

These files map candidates to positions, answers and item codes. They stay private. No image, key or code-to-candidate map is in this commit.

## 13. Reader packet

Path: `/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad/panel_packet/` (93 items).

| File | SHA-256 |
|---|---|
| `INSTRUCTIONS.md` | `c196e5c3a6b1c82ed217ecdbcb7e425da016de1f59c94df33b343a75a63c56ff` |
| `responses_template.csv` | `c6419833435564d0199f8aaecd0329e508c580acf13be18aba5f3160afe4bde8` |

Item PNGs (`items/`), in file-name order:

| File | SHA-256 |
|---|---|
| `LC-012815.png` | `eab0654a85c185180a2c733ae6fb6e53584a94eb7886d7d87f16af25a90fb11c` |
| `LC-071B7E.png` | `97af07906cbd29077536ec3760a292adb87a73d66717af655657ea0aeb208adc` |
| `LC-07F313.png` | `05a45fb6e88c6b3a30782125862e34f22e8fd2bbc33dcadca2a9d191e7e4badb` |
| `LC-07FB37.png` | `c70d982c03de2785fe275d8896d0d5e3afa873fdf22de361a15da0562ac80c5b` |
| `LC-0844E4.png` | `eaac45cb02553c2344492452b43a8803efc91940b9ed764ea06ed0e7d28c6258` |
| `LC-088BA4.png` | `40e839051c92b6a5024e2748f1b7dae6d3318396eb4f00aaf732c65c5657fc86` |
| `LC-0BE1CB.png` | `b7f588fd962852f013e3b468b82f865b722cabe6382060b46b8a73b26eb82af9` |
| `LC-0F74F5.png` | `ccb77372b9670228e13a31c115ca62c12401d9add61113994927ead7d3e374c7` |
| `LC-102713.png` | `20214c0f78a982cac91f545ef723c7b8c86ddda88ac5210b23a4c19190442333` |
| `LC-130AC9.png` | `c16a5df5c255f9b2790dff91e4d45d934205993acf0d910960381fac798d3337` |
| `LC-1535FB.png` | `7d6f20d964f1070214f6edd0530380abb31e665557f42230e35a8ed92323e992` |
| `LC-19B6F0.png` | `d386d28a870cabed2e73b1114993e451ad1fbc71fde878bdefc5619405cb7cb2` |
| `LC-1A4EBE.png` | `2f6b352ec5148f5179f4e8c6e5a33fb4a666a86814b01c8d65cdca0ccc7aa7dc` |
| `LC-1AA224.png` | `756edad22aacb9c11ccd2b0ef3637f15ea4162a38bc14bd8908092b0bfa499b0` |
| `LC-1DEE95.png` | `93550b40868423c982a40ec89488a171b5b686a0c9670f782c9377cd28031813` |
| `LC-1EB0B6.png` | `9cb3113ed4f71536dd1d162ed1f44b4c13118cc63cadcba1fb8d10ddcb6f9c1b` |
| `LC-210C96.png` | `0bb3b2c21b96844c3d1bdedd21b6391f4abff238a6e8833b5e6e8f835d4510ac` |
| `LC-2114B4.png` | `288bf5ee5ae2d9dea4a105cc7bd3ab75b56f448afac25e43dba140f0bd45e673` |
| `LC-21E1E7.png` | `4a4e1fd4ec23883f9b3802dc75a8c274b22b79fcc3d5a522c0072aedb23ea515` |
| `LC-26CA83.png` | `6754010c45b548ac726227998e460ffd04afdc4b9bce459e743d00a0f70ca555` |
| `LC-27D674.png` | `b6006d5fe6a5bcf200f1c6ab85b01ad1345d3cb0b51fdc153ae28a11bb4b06ae` |
| `LC-2AED28.png` | `d02428dd053999d07eb7e0af33e0b76b6b4e61b909476fda6e008958cbfd378a` |
| `LC-2B9EC1.png` | `c7cb2f5243b3dca6b0a6dea1a211f383258283e2f74040f32b85dece4f859c91` |
| `LC-2CC780.png` | `a7136ffe1c478af1623d9a6b9b40c974c5858dc1446ba64f5d6e2fbd792654d7` |
| `LC-2D32F0.png` | `75cf3f2ec0785ffda518dfd4aec3762451fdd6409cedb721a7a635eceed7365f` |
| `LC-2F3D6C.png` | `fcb5555486a4cc00b34311b93a667f9c18d1ae4d72662972733c76d55778c13b` |
| `LC-2FBD22.png` | `e7427721a3af4c4d97562b5fdf09b10902382da99c1e92c543ea8e1572bb1e7a` |
| `LC-38099C.png` | `f5bae36b64b56ad30acbeeb927a9464c79e800d3a1e93f648a44be5da5d42687` |
| `LC-42F1F4.png` | `60c91b030332b73bbf5a34be3aa0b02ca0b3f5ad7f9f8f0a0e486905d1761e59` |
| `LC-43CD62.png` | `a8827b54d25250fecd0dd03a5716beac6ca895fc59c12f716ea25d141da359d3` |
| `LC-448870.png` | `edf071b1b847e0457951d666010443ce4ac5c8ffaf95d890778f768ae9d2543f` |
| `LC-450D4E.png` | `56e65394c8775696b025c56604147c1fcafab1410033e8f865c398429867d1c4` |
| `LC-466253.png` | `103942c0c51b6957b2c0670a3020b6a630a6e06e842af77c897d3261022c3e58` |
| `LC-4E2F30.png` | `cb5efb1ef38cf0110c06b69f9138ee6a9a8b736f42f5dbe80e2c85c6e09fc6a0` |
| `LC-4EC905.png` | `30bc3668aaeef3b3fa3ea7e87fffb898f4948c92f7e73700df66adb9d236fc16` |
| `LC-5162B3.png` | `569a91bdde023ead843892fe6740a868b8aec1ea5eb6dd504a320e9c7ee675e9` |
| `LC-522B47.png` | `b19c7d483256fd99d848135fe325629eb25c5cc552ac04e611e3571b7409a8f8` |
| `LC-5C2DCD.png` | `15ebf4ba6b7541dd085e30895fcc4258bc0ba2d614af28d2b346a65d6b0534f3` |
| `LC-66AFF0.png` | `bbc33614f6620f5b1c807b350aeaaa9d123e8bff6ee74d92aaee8c246281a863` |
| `LC-680C4B.png` | `4f8fc1d8d02d4684ea0d7748da04e0c013ffdc2d66fae44565423314370ebb15` |
| `LC-69DAF2.png` | `351f46ec358bd4edade3561508da211124d37a44f969c23a2d805f60023ad832` |
| `LC-6B7675.png` | `b18818ea51344c95558d64b2497da0f9200fdc2636bb5e390bc54854433044ae` |
| `LC-6BB9F0.png` | `cc61572e684b5719fba4018da7a4834160dec391d0325efc69e7f2a9e15297a2` |
| `LC-73C8AA.png` | `78dbb350feec284cfb449e1e26a15e0aeda8e90fb0870e7ea41a495ffaa7d9c3` |
| `LC-76F16C.png` | `01e5eb09d4052b53907f4a03e9162afe5403f886112f45a26f01fc69de4d0700` |
| `LC-7A3CE0.png` | `ea4c051e7f85320c7922326d35bdf19bc56933ec05c74b1b3b218a7f9552b0fd` |
| `LC-7AA5EE.png` | `c4dc65be47b70470eacadebdf36bb3fbc63654aa6bbbd504a3bcdc79a178c71f` |
| `LC-7B955A.png` | `386b3bbbcc8efc29579544e75d05293cc6719cfa410b1ff5f60bb5cb3e1a039c` |
| `LC-7FDCD9.png` | `f7886b008ea6c9a35d3d4a6b945f961f35e682d8ea625acfbadfc6d50ec042c7` |
| `LC-815CFA.png` | `7067733a347e81def9c6c60447046e253f16656226048b81accc17d9ad55d160` |
| `LC-828C88.png` | `c8809fb00b495226f74ca93ccb0bcf913bc4b140bee6bb8968ed41edb1e98d9e` |
| `LC-83D450.png` | `f19765702f5d44627549f8f8f02d1acde8da24d3e397228c24d581229ad3deaa` |
| `LC-84226B.png` | `3f8a521a8c46453fb3ae3d9b51f0f507f3914c73109209e30d661504c515a2c8` |
| `LC-887A75.png` | `6e114a14716ddea91b50ab0267263a3a04d9bfbfcb376200ffe8fc0d880ed4be` |
| `LC-8AE8A3.png` | `bd43341812cb80fd76ca609adf70293644d4c36f2a8912f2c292593d1a5218a0` |
| `LC-8BC7C4.png` | `f77c661fb72de836b206b04c90ae09476a816f510c84937216623b5d7cf55a4e` |
| `LC-928A1A.png` | `f5cdac1ee9065487d19b5eb2667ea8bc59f57b361d72a93878725c4b1820998b` |
| `LC-9425EE.png` | `bcc8a5ddb9423f994200974ebe2ba6d2fd0a5295fad1b6efe2490e22f7aeabb3` |
| `LC-97423E.png` | `a4a616bacfa096b52d44caa80e075363450a4c69c6c6ef8ed3a8fc06faf0ff46` |
| `LC-98BFF2.png` | `5dea9ad28fab170680a02310a9269eec808f18c7bd5412fd8d025060f9000775` |
| `LC-9C7DAF.png` | `6eadcd17907a49c6dc6e670c0691fe8502d3364180f368313758f719e43e63e6` |
| `LC-A0A736.png` | `3a5ad41a251905f97505949e06a879106df602a9fd41017b20d298a0bc61787c` |
| `LC-A2BE40.png` | `91cacac7995b4de94634b4b13285422a229e2df633c9cc977085a6891763b163` |
| `LC-A4E8E7.png` | `218078dd6b6e29e3b97fec971d220476cb4017a89aa93d81d087f40d49f19c2c` |
| `LC-A59778.png` | `d927bbcba324b6de69488c05697906b7ff220325c764773fc20cb9ce170727d3` |
| `LC-A89E98.png` | `ae314da53181369bf26b5a6fb1acce777252425e56d2c3e8110d039a0ed0f1b1` |
| `LC-B03E91.png` | `a31f9dce150b46f098bb42d0e98c0ecaede68808cc24fe3aa0c6752cd2306719` |
| `LC-B19918.png` | `5e73b76f5a0fb7f2934526bf79b31968d92deaef9971cbd8e3bad89df00c20c9` |
| `LC-B3C686.png` | `cc513518ee3a939691d12dbb349b45bbf94b228e33630591838bf692749e1cbb` |
| `LC-B48CB5.png` | `4b6d04973b66cec8d2f6928711eb03afacf2c4d55c4946faeed5394631346de5` |
| `LC-B7CB6F.png` | `6a1c09b31e9c093b07113da54323ebcf6febb778a7f2ea38af42224645956569` |
| `LC-B9CB5E.png` | `57cbc2863e9f0b6a30e23f9a0f9e889c02fe44d47a2ef361a854be0ae6c8c5bc` |
| `LC-BA8478.png` | `8101e9822cf7e25016d43eb66a850fd2c351f6301ea5fbd939c6a3ea319bf891` |
| `LC-BEA893.png` | `427d2b9cd6fc411acfe36586e5fd841436ae0fff3b8feb435599e80b20b24c48` |
| `LC-C38118.png` | `7a47ac00c24f56bf6a950bccf7a9cecac6ff544efb6fbff047bb69627855065d` |
| `LC-C99E61.png` | `3f99cd1b8805f5372f8f65c2f5b7859fe64da404f035ccdfa8013d73772e73c5` |
| `LC-CA32BC.png` | `5467c06d96522609ffefab869ff01918b45a865ff4b7a2497579ae3ba2a3d06d` |
| `LC-CAB714.png` | `0a4fd86e191d3c51b10bc6bcbaac599f9faeea8e085b0baf81ec36d916c9b9c0` |
| `LC-CE0CAE.png` | `b5018311bcefa581ef9af82fce5f024b099d282b569b4da8078d5d36fff8705d` |
| `LC-CFAD40.png` | `4eaedda71ddac280c74263df7673023ee7de84fef2ebc9126566b435fd0c3ef2` |
| `LC-CFAD8E.png` | `03f67e0916ed36947b65be5c212189666219b05801c2a24fec6363ce0c0cb1ff` |
| `LC-D49E42.png` | `2fc7e5e8b893239897917f0457a5c325eac3f8be9d5065927d08136cf9e00c8a` |
| `LC-D7DDBD.png` | `b31046e519f41d7633ed08a5b6f1adc4304afef62bdcf0907fbe674eca0062c4` |
| `LC-DE5ACB.png` | `193aeed4937209f0bda452105c11cfc0c764c4e899dbe032cdf3d2ae69d1010c` |
| `LC-E3CF4F.png` | `f4821f24eaa1ae4d13b703e427602aa25fa6ce5b4815a332de52b77e5c689138` |
| `LC-E48A6A.png` | `b162b3d764057ece6c6b0aa923579d46aa75a9f46ec21782356be5d3dc495336` |
| `LC-E60E91.png` | `2d85e1cb3e2a40adbc80e59f56c494eb81e70276ecf34fbb49f9bc56522922ed` |
| `LC-E74052.png` | `c84a0416729617277cd316bbdd9a70e471f493d98b201160906f1f60c8f5d81e` |
| `LC-EBCE7B.png` | `b5bbad171b93f84d310b29536e44316ff349ea0fa0cf92397c999d4f0e514412` |
| `LC-EFEAF2.png` | `0de51c4c5cd3e61c938ff995569d27dbdaa510307bea620bbf4d74f10924d387` |
| `LC-F82BAE.png` | `c572ba12d5e618136851df7e4a41148057a0a9b3eaaee583d7ba68649d989fab` |
| `LC-F9B54E.png` | `9d6ecd6a6b1939418f44df6d7a8bf48b14c196c3249a318e699994be3e2ab93b` |
| `LC-FBBD54.png` | `c7f11adfd345c0b3c3b7c9b53d270bd936b6db780856fc5dc1d788d8e9c08de3` |

## 14. Limits

- **Coverage.** Only columns I, II (cut 6), III, V (cut 11), IX (cut 16) and X carry controls. Cuts 1, 9 and 12–15 are not delivered. Cut 2 lacks the light class. The A2 placements of cuts 5, 10 (IV, V) and 11 (VI) failed the gate.
- **Placement.** It rests on Puech's copy photograph and on W2F alignments, checked by eye. Eye shifts were horizontal only. XS markers use the copy-photo separation and were not refitted after the shifts.
- **Damage grades.** These are the coordinator's judgement on the windows, made with identities known.
- **Image processing.** Luminance only (no colour). The letter heights come from column medians per cut, so individual letters can differ from 104.5 px after matching.
- **Image terms.** USC/WSRP terms forbid publication. The items stay in the scratchpad. They are never committed or published.
