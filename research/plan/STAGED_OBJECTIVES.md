# Staged objectives and stop rules

9 October 2026. Exploratory plan. It changes no registered result or counter, claims no identification and plans no travel. Every stop rule is PROPOSED; the project owner decides. Machine-readable copy: [stages.json](stages.json). The rating scale, [rating_scale.json](rating_scale.json), was frozen before any stage was rated ([README](README.md)).

Where the project stands ([outcome ledger](../progress/outcome_ledger.json)): 0 independently discriminated identifications, 0 confirmed deposits, 0 whole-candidate exclusions, and 3 conditional assessments, all inconclusive. No stage below is reached.

## Two lessons

- **Rate the objectives before digging (Greyfriars, Leicester, 2012).** The team set five nested objectives. It rated finding the friary "a reasonable expectation" and finding the king "not seriously considered possible". About 17% of the precinct was open to digging, and about 1% could be dug ([University of Leicester, "Where to dig"](https://le.ac.uk/richard-iii/discovery/where-to-dig)). Buckley et al. 2013, *Antiquity* 87, p. 521: the grave "seemed improbable if not impossible". The ratings set what the partners expected and decided where the trenches went.
- **Let each result pay for the next (Wood at Ephesus, 1863–69).** The British Museum Trustees wanted "some substantial return" (Wood 1877, pp. vii–viii). The Odeum and Theatre came first. The Magnesian Gate, the road and a supplementary grant followed, then the inscribed precinct wall in 1869 (ch. VI, p. 111). Each result justified the next grant.
- Applied here: each stage has a rating with its evidence. Each lane names its next observation, its cost, the result that justifies continuing, and the result or date that would park it.

## Rating scale

Ratings are ordinal judgements, not probabilities. They are judged against the current campaign: the requests listed in [ACTIVE_TEST](../ACTIVE_TEST.md), the [decision queue](../feature_workbench/decisions/README.md) and the [chain's next links](../assessments/kohlit_chain/next_links.md).

- **A, reasonable expectation.** The deciding observation is requested or in hand by more than one route, and a frozen rule exists to read it.
- **B, possible.** A named record could produce the result, and the repository holds a precedent for it. The record is not in hand, or it can return an inconclusive answer.
- **C, unlikely but worth recording.** It needs several records not yet requested, or a kind of result the project has never obtained.
- **D, not seriously expected.** It needs every earlier stage plus a field observation that the project does not plan.

A later stage never gets a higher rating than an earlier one.

## The ladder

### S1. Reserved observation in hand (rating A, reasonable expectation)
An outside observation that can decide a registered alternative arrives and passes the authentication or registration gate frozen before it was seen.
- For: three independent routes to an image of XII 10 at the 21/22 cut are open (USC masters, Manchester and Joan Taylor, the ÉBAF copy and X-rays); Facsimile Editions declined ([ACTIVE_TEST](../ACTIVE_TEST.md)). The [reading protocol](../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md) has a frozen authentication gate. The Meinardus scan is promised for mid-October; its pages are the reopen criterion of the closed St Andrew branch. Pre-camp Jericho records have a [registration protocol](../assessments/kohlit_chain/registration_protocol.md).
- Pays for: reading sessions, and a request for control frames from the same image series.

### S2. Disputed reading settled by an outside observation (rating B, possible)
The observation rejects, or supports relative to the registered alternatives, at least one registered reading, for example one of the XII 10 strings R1–R7.
- For: a decisive XII 10 reading alone separates the seven strings; bet against kaf, or the extra stroke, can each reject R4 without the cut letter ([decision queue](../feature_workbench/decisions/README.md)). The 0.15 mm saw cut cannot hide a whole yod or waw ([saw-gap check](../agent_review_2026-10-07/followup/G_saw_gap_xii10.md)).
- Against: from copy plates an AI reader scored at chance on bet/kaf and he/ḥet, and Lefkovits 2000 p. 78 calls many letters indistinguishable ([letter controls](../text/letter_controls/PROTOCOL.md) §1). The protocol returns "not identifiable" for disagreement or poor resolution; the original-photo audit of entries 31, 40 and 49 ended that way.
- Pays for: a narrower set of Koḥlit classes, so the next request goes to a record that can still separate the survivors.

### S3. One branch decided on measured ground (rating B, possible)
A frozen branch-level test of one relation or location instruction at one candidate, using a dated contact or a surveyed datum, ends supported or rejected, not "not identifiable". A rejection is a conditional model exclusion, not a site rejection. S2 and S3 can come in either order.
- For: two conditional model exclusions are already registered, both at Siloam L103 ([ledger](../progress/outcome_ledger.json)). The Kenyon eastern section and Kallai pp. 172–173 can each exclude four Koḥlit classes; a dated IV/17 contact separates 12 of 15 entry 25 pairs ([decision queue](../feature_workbench/decisions/README.md)).
- Against: every queued record can come back inconclusive, and the Kenyon plates and Kallai are neither requested nor obtained. All three formal assessments and every closed test ended inconclusive ([metrics](../PROGRESS_METRICS.md)). Only 11 of 28 next chain links can contradict their model ([methods round](../logs/methods_round_2026-10-08.md)).
- Pays for: the next link in that model's chain and, if the owner agrees, an archive order for the record that decides the next relation.

### S4. One landmark independently discriminated (rating C, unlikely but worth recording)
The identification counter moves from 0 to 1: reading, feature relations, phase and datum distinguish the candidate from its controls, and a registered unseen prediction succeeds ([AGENTS.md](../../AGENTS.md)).
- Against: rarity is not measurable (k = 0, f = 20, m = 313 of 333; [metrics](../PROGRESS_METRICS.md)). Every FAIL rests on a site-level absence covering at most about 1.1% of the northern sector ([observation audit](../rarity/kohlit/observation_process/README.md)). At best the queue narrows Koḥlit to one class, and separating a selected roster identifies nothing. Regional inventories and search coverage are not audited ([ledger](../progress/outcome_ledger.json)).
- Pays for: only then a request for a field observation, which the owner alone would decide.

### S5. Phase-to-instruction match at that landmark (rating C, unlikely but worth recording)
At a discriminated landmark, the feature the instruction names is dated to a phase when the instruction was usable. That phase's surface is the datum, and the instruction's target volume follows from it. This is the brief's "instruction tested against measured ground" at a landmark; S3 is the branch-level version. Phase comes first because the datum depends on it. S5 is strictly harder than S4.
- Against: none of the four coverage records defines a target geometry ([ledger](../progress/outcome_ledger.json)). IV/17's 8 joins and Tell es-Sultan's 4 joins are all undeterminable ([coverage](../feature_workbench/coverage/README.md)). An ancient threshold separates no class. R09 is still queued ([backlog](../OPEN_QUESTIONS.md)).
- Pays for: a check, with the six coverage gates, of whether any recorded excavation reached that volume.

### S6. Deposit location (rating D, not seriously expected)
A deposit location confirmed, or a negative excavation verified at a predicted target.
- Against: both counters are 0 ([metrics](../PROGRESS_METRICS.md)). A landmark match proves no deposit, and a negative excavation needs target volume, phase, reach, disturbance and detection limits ([AGENTS.md](../../AGENTS.md)). The project plans no excavation, and the owner declined trip planning.
- Pays for: nothing is planned beyond it.

## Rules for lanes

- **Existing rule, unchanged.** A closed test reopens only for its stated new observation or a documented analytical error, and its result is preserved ([AGENTS.md](../../AGENTS.md)). No stop rule here opens or closes a test. The six closed tests and their reopen criteria are copied from ACTIVE_TEST into `closed_tests` in stages.json.
- **PROPOSED: parking.** A parked lane resumes only when its named observation arrives. Parking is not a test result.
- **PROPOSED (Wood): spending follows results.** Spend a new message, a library item or money on a lane only for its first observation, or after its last result met its continue-if condition. Money always needs the owner's approval.
- **PROPOSED (Greyfriars): requests name their stage.** Each new request names the stage and rating it serves. A request that serves only a C or D stage needs the owner's explicit approval.
- Parked elsewhere and not restarted: Peleg's map, the JSP 18 pocket sheet and the Feldman search (owner); Patrich 1990 p. 208 n. 24 (R03); Augustinović and Gerico (R10); trip planning (owner).

## Lanes by stage

Cost: sessions (s), new or follow-up messages that need the owner's approval (msg), and library items the owner may choose to fetch (lib). No lane plans any money; a reproduction fee for AQ1 or the letter controls would need the owner's approval. State: waiting (request pending), active, park, run once, integrate (tool built this round). Full wording is in stages.json.

### S1 (A)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| N-ARRIVAL-REGISTER | S1 | integrate | A frozen prediction for each pending item before it arrives; first the Meinardus scan and any XII 10 image | 1 s | Each arrival is registered before it is opened | PROPOSED: close an entry when scored; park the register when nothing is pending |
| N-STAGES | S1 | integrate | The owner's decisions on these stop rules | 0 s | The owner adopts, edits or rejects them | PROPOSED: review once when a stage is reached or a counter changes, otherwise on 31 Jan 2027 |

### S2 (B)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| AQ1 | S2 | waiting | An XII 10 image at the 21/22 cut that passes the gate (USC, Manchester or Taylor, ÉBAF) | 2 s | The image passes the authentication gate | PROPOSED: park if every route declines or no gated image by 31 Jan 2027; the protocol stays frozen at fd3f334 |
| R11 | S2 | waiting | Zuckerman's WSRP Figure 4.6 composite with component IDs and placement map | 1 s, 1 msg | It arrives with IDs and map | PROPOSED: after one follow-up, park if no reply by 31 Dec 2026 |
| M-LETTER-CONTROLS | S2 | waiting | Control frames from the XII 10 image's series (cuts 1–6, 9–10, 13–14, 17–18) and two readers | 1 s, 1 msg | Frames arrive and readers are assigned | PROPOSED: if that series has no control frames, park and record the reading as uncalibrated |
| M-LOCATION-LANGUAGE | S2 | park | Not an observation: the owner's decision on the על פי and עד records and the atlas 6 and 32 notes | 1 s | A decision changes a reading a branch uses | PROPOSED: park after the decision; rerun when a reading changes |
| N-EDITION-CONFUSIONS | S2 | integrate | The confused-pair table applied to bet/kaf, he/ḥet and yod/waw | 1 s | The XII 10 pairs are often confused, which supports the control-frames request | PROPOSED: park after integration; never a substitute for the image |

### S3 (B)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| R01 | S3 | park | A section or context record naming the L117 joint with a dated contact; Reeder and Jol's records are requested | 1 s | A dated contact at the joint | PROPOSED: park now; stays parked if Reeder and Jol send nothing by 31 Dec 2026 |
| R02 | S3 | waiting | Dadon's IV/17 L-656 file: threshold section and levels, baskets 656.17 and 656.20 | 2 s, 1 msg | A dated wall or mouth contact, or a levelled threshold section | PROPOSED: park IV/17 if the file lacks these or nothing arrives by 31 Mar 2027; park Twin Cave now |
| R03 | S3 | park | An exact PEF item or a measured wall record with a phase-linked section | 0 s | A measured outlet-to-wall relation with a phase | PROPOSED: keep parked; Patrich stays parked |
| R04 | S3 | park | Site 143 p. 142/28*, HA 85 p. 31, HA 31/32 p. 13, Jeremias 1958 p. 86 (none in Drive) | 1 s, 4 lib | A tomb plan with entrance direction and a dated water feature | PROPOSED: park until one item is in hand |
| R05 | S3 | park | JSP 8 and JSP 20 plans, locus concordance and basket elevations (not in Drive) | 1 s, 2 lib | P5178 tied to stair, pit or cistern with a stratigraphic date | PROPOSED: park until JSP 8 or 20 is in hand |
| R06 | S3 | waiting | Szanton's main-side L103 junction section (asked 6 October) | 1 s, 1 msg | Aperture, basin edge and floor in one phase | PROPOSED: after one follow-up, park if no reply by 31 Dec 2026 |
| R07 | S3 | park | Manasseh V pp. 314–324 and 547–555 (ʿAuja alternative) and dated Achor sections; Koḥlit is in AQ1–AQ3 | 1 s, 1 lib | A named Achor or Sekakah alternative narrowed by independent evidence | PROPOSED: park until Manasseh V is in hand; no new correspondence |
| R08 | S3 | waiting | The Meinardus scan (mid-October, free) and the A(C)94 junction drawing (asked 6 October) | 2 s | Plan key and captions of pp. 183–184 and 196, or an aperture tied to a wall face and floor in one phase | PROPOSED: park the Jericho part if neither by 31 Dec 2026; park Hyrcania and Sartaba now |
| AQ2 | S3 | waiting | Pre-camp records north of the tell (Garstang, PEF, Nigro) under SULTAN-1; Kenyon's eastern section and Plate 111b | 2 s, 1 lib | An opening in the strip with a dated context, or dated quarry pits | PROPOSED: park the archive route if all report nothing or none replies by 31 Dec 2026; park Kenyon after one reading |
| AQ3 | S3 | park | Kallai 1972 pp. 172–173 on a pool east of Kh. el-Marjama (no scan found) | 1 s, 1 lib | Kallai locates and dates the pool, or a record ties the spring-house wall to the basin | PROPOSED: park Marjama if Kallai gives no position or date; park ʿAin es-Sultan until a wall-to-basin contact is named |
| M-LANDMARK-CHAIN | S3 | active | Tier-1 links: 2002 cave-survey entries (requested), MHCS IV for S6040 (Drive), HA 28–29 for Tananir | 1 s | A two-sided link contradicts, or matches a relation not used for selection | PROPOSED: after tier 1 or by 31 Dec 2026, park tiers 3–4 until their items arrive |
| M-DECISION-QUEUE | S3 | park | Reruns when XII 10, the Kenyon section, Kallai or the L-656 file arrives | 0 s | An arrival changes which classes survive | PROPOSED: no maintenance sessions |
| N-PEF-FINDS | S3 | integrate | Quarterly Statement find reports near candidates, such as north of Tell es-Sultan or the Wadi Qelt | 1 s | A located find or feature at a candidate; an exact item meets R03's resume rule | PROPOSED: park after the volumes in scope are indexed once |

### S4 (C)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| R10 | S4 | park | Netzer's 1982 Doq field plan and diary, or a verified later publication | 1 s, 1 msg | A guard or drying room, an eastern corner and an ancient surface | PROPOSED: park now except model reruns; the ordering test stays closed |
| KOHLIT-RARITY | S4 | park | Zertal Vol. I (14 units) and the 17 unread first publications | 2 s, 18 lib | Only a record of a search of the northern sectors could move m (313) materially | PROPOSED: park now; the result and both addenda stay as recorded |
| M-FEATURE-AUDIT | S4 | park | Tsafrir and Magen 1984 for the date of the S1283 pits | 1 s, 1 lib | The report dates the robbing pits or the cave-cisterns | PROPOSED: no further sessions; rerun when a coded sheet changes |
| M-OBSERVATION-PROCESS | S4 | park | None; a registered use of its scope rules needs a new pre-registration | 0 s | The owner chooses to pre-register scope rules | PROPOSED: park now |
| M-RECOVERY-DEV | S4 | active | Freeze the harness: SHA-256 of procedure.py, procedure_constants.json and harness.py | 1 s | The freeze is recorded before the reserved run | PROPOSED: no tuning after the freeze |
| M-RECOVERY-RESERVED | S4 | run once | One run of the 11 sealed cases; the owner supplies the key | 1 s | Set before the run: no more than 2 wrong selections (the dev batch had 2), a candidate chosen in a "none" case counting as wrong | PROPOSED: close after the single run, whatever the result |
| N-SEARCH-EFFECTIVENESS | S4 | integrate | Which failed or silent looks enter the W2B model, with their detection scope | 1 s | A leading candidate changes by more than the K2/K4 kernel sensitivity | PROPOSED: otherwise park after integration |

### S5 (C)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| R09 | S5 | park | Oren–Rappaport Cave III and V plans and contexts (not in Drive) | 1 s, 1 lib | A plan ties an opening or installation to its own dated construction | PROPOSED: keep queued with no sessions until an entry reaches S4 or the plans arrive |
| R12 | S5 | park | An authenticated textual correction, or an S5 result | 0 s | Such an observation exists | PROPOSED: park now; the closed inventory test reopens only for an authenticated correction |
| M-COVERAGE | S5 | park | The L-656 file (shared with R02) | 1 s | Target volume, datum and reach for one branch | PROPOSED: park until that file or another target-specific record arrives |

### S6 (D)
| Lane | Stage | State | Next observation | Cost | Continue if | Stop rule |
|---|---|---|---|---|---|---|
| N-SALVAGE-RECORDS | S6 | integrate | Recovery accounts and earlier searches, labelled EVIDENCE, TRADITION or INFERENCE | 1 s | An account names a place matching a registered candidate, with a recoverable source | PROPOSED: park after integration if none does; never confirmation |
| N-CONCEALMENT | S6 | integrate | Base rates of concealment contexts | 1 s | The rates differ enough to change which deposit contexts a lane checks | PROPOSED: park after integration; never evidence for a candidate |

## What this means now

- 20 of 32 lanes serve S1–S3, the rungs rated A or B. These are this campaign's road and precinct wall.
- Proposed now: 15 lanes park, 7 wait on a pending request, 7 tools get one integration session, 2 are active and 1 runs once.
- Taking every lane's next step would cost 32 sessions, 5 owner-approved messages, 29 library items and no money.
- The XII 10 image is still the arrival that matters most (S1 to S2). The Kenyon section and the Kallai pages come next (S3); both are library items.
