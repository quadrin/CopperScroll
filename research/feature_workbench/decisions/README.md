# Decision queue

`plans.json` specifies seven exact record dependencies and four possible outcomes for each. The evaluator imports all six tracks from `research/measurements/queue.json` unchanged, with the source hash and original dates. Historical execution states and counters remain historical.

The atlas can select `data.tasks[].id`, then an item in `outcomes[]`. `preview()` returns **Possible outcome — not observed**, the conditional consequence and the unchanged current evidence. It never records the selected outcome, sends a request or reopens a closed test. The generated `results` use only each task's recorded evidence status; all seven currently remain unknown.

Run from the repository root:

```sh
python research/feature_workbench/decisions/evaluate.py
python research/feature_workbench/decisions/evaluate.py --task decisions-xii10 --outcome one-sequence
python -m unittest discover -s research/feature_workbench/decisions -p 'test_*.py'
```

The record dependencies are Manchester XII10; IV/17 permit L-656 and baskets656.17/656.20; Kallai1972 pp.172–173; Kenyon's separate eastern section and Plate111b; and phase-controlled Jericho, Siloam and Wadi hydraulic contacts. Priorities are qualitative, with reasons and access/effort fields. They contain no numerical information-gain or confidence estimates.

The IAA inquiry already sent concerns the regional cave inventory. It is a related pending request, not a verified L-656 request or file holding. Manchester, Jericho, Siloam and Wadi sent-request records retain unverified delivery/replies. Kallai originals and Kenyon's referenced drawings remain uninspected; Kenyon III's text and the Wadi report are already inspected.

XII10's letter protocol is frozen at `fd3f334ea2a40c0f8e99921ef663f8b126112fe1`; its unused-observation status remains unverified. Other archaeological decisions here are planning branches. Before a reserved observation is used, the finite feature/reading/phase/datum/axis/unit/tolerance choices and decision rule need an actual freeze and exposure audit. Compatibility alone supplies no identification.

No original source is newly inspected, no activity count changes, and no correspondence, purchase, delivery check or parked acquisition is performed. A future record may resolve only part of a dependency; missing documentation and unexposed contacts remain unknown. A negative deposit conclusion still requires an ancient target volume, phase/datum, excavation reach, disturbance and detection limits.

## Which records separate the surviving models (8 October 2026)

`discriminate.py` adds an exact search to the queue. `discrimination.json` holds its inputs: the model families, the finite outcomes of each record and their consequences. `evaluate.py` imports the search, so `build()` returns it as `data.discrimination`. The search reads `plans.json`, the relationships evaluator and the inventory evaluator. It changes none of them.

### Models and classes

The search uses six model families. Each family is a set of alternatives for one claim.

- Koḥlit (entries 11 and 60): the relationships module keeps 40 combinations. Twelve are contradicted and stay excluded. The other 28 survive.
- XII 10: the seven registered strings R1–R7 of the frozen protocol.
- Entry 25: 288 inventory branches (three caves, 96 branches each). All survive.
- Three closed tests each have one named branch: A(C)94 and the Wadi Nuʿeima bath (entry 29), and the Siloam main basin (entry 49). Their other alternatives are not modelled as branches.

Models that survive exactly the same outcomes of every record form one class. The 28 Koḥlit models form 10 classes. The 288 Entry 25 branches form 6 classes. The seven strings stay seven classes. So duplicated parameter choices count once. For example, the Milik and Puech readings always fall in one class. No queued record observes an opening direction or a concealed opening. The cubit units, the jar/book deposit alternatives and the vertical/horizontal direction never separate either. No queued record bears on them.

### Outcomes

Each record keeps its four `plans.json` outcomes. The search refines them into finite cases where the existing predicates allow it, and marks each refinement as derived. Examples: a pool built 71–135 CE fails only the early window; a later pillar fails only the pillar reading; a rejected R4 string removes the Janoaḥ reading. Every record also keeps outcomes that are inconclusive, partial or not obtained.

The XII 10 outcomes come from the protocol's component questions: bet or kaf, the signs before the cut letter, the cut letter, and the word boundary before צפון. Its 480 component cases fall into 28 outcome groups, plus the gate-failure outcome. The Janoaḥ branches (RB-L) need R4. If R4 is rejected, they fail. If R4 survives, nothing else fails: the protocol needs a separate linguistic and geographic argument for the place name.

### Results

- Worst case: no set of records guarantees any separation. Every record has an outcome that leaves every class alive.
- Decisive outcomes only: the XII 10 reading alone guarantees that the seven strings separate. No archaeological record guarantees anything, even when decisive. A compatible verdict at one site never excludes another site.
- In principle: the smallest set that can separate all ten Koḥlit classes is XII 10, Kallai and the Kenyon section. Each of the three is necessary. Entry 25 needs the IV/17 L-656 file. All families together need these four records.
- Best case: the queue can at most narrow Koḥlit to one class: the Jericho historical basin with NS1 or D9, in any reading and window. No queued record can exclude that class. For Entry 25, no queued record can exclude IV/11, Twin Cave or the IV/17 reported cave-level branches.
- After collapsing, every pair of classes has at least one record that can separate it. The 75 Koḥlit model pairs inside classes have none.

### What the queue now ranks first and why

The rank uses four counts in order: necessary for active-test families, necessary for any family, class pairs separated in active-test families, and class pairs separated in all families. Equal counts share a rank.

1. XII 10 reading. It is necessary for two active families. It separates 21 Koḥlit pairs and 21 string pairs. It is the only record with a frozen protocol. It is the only record whose decisive outcome guarantees separation.
2. Kenyon eastern section and Plate 111b. It is necessary for Koḥlit and separates 30 pairs. It can exclude the four quarry-pit classes.
3. Kallai pp. 172–173. It is necessary for Koḥlit and separates 28 pairs. It can exclude the four classes that use Kallai's pool.
4. IV/17 L-656 file. It is necessary for Entry 25 and separates 15 pairs.
5. Jericho contacts, Siloam and Wadi share rank 5. Each can exclude only its own named branch.

One record is the unit. XII 10 alone separates the most pairs per record (42). XII 10 with the Kenyon section separates 60 of the 66 active-family pairs. Adding Kallai separates all 66. The recorded access differs. XII 10 has sent requests. The Kenyon plates and the Kallai pages have no recorded request, and their originals are not obtained. The IV/17 file has only a related IAA request. `plans.json` names only the Manchester route for XII 10; ACTIVE_TEST also lists the USC masters and the ÉBAF visit.

### Which questions have priority

- Manuscript reading (XII 10) comes first. It is the only question that can exclude the Janoaḥ branches. Bet against kaf or the extra stroke can each reject R4 without the cut letter. The cut letter or the word boundary can also reject it.
- Construction contact comes second. Alone, the Kenyon opening date separates 28 Koḥlit pairs and the Kallai pool date 28. The Kenyon grave-access relation separates 16. For Entry 25, a dated IV/17 wall or mouth contact separates 12 of 15 pairs. Sealed finds under the spring-house wall (ACTIVE_TEST question 3) separate no class. They would need a recorded contact between that wall and the historical basin.
- Entrance bearing is third. For Koḥlit no queued record supplies it, so RB-M and RB-P stay one class. For IV/17 the individual-mouth aspect separates 9 Entry 25 pairs. It first needs a frozen qualitative aspect rule, because the edition gives no angular tolerance.
- The ancient threshold separates no class. A threshold value can make a target computable but cannot contradict a branch. It is a prerequisite for a later target test.

### Limits

The search computes no probability, likelihood or information gain. Every number is a count of classes, pairs or records. Effort and access are listed as recorded categories and are never weighted. Separation is relative to the registered branches; each roster is a selected set, so separating it identifies nothing. Derived outcomes are planning branches, not observations. Ranking a record sends no request and changes no status.

Run from the repository root:

```sh
python3 research/feature_workbench/decisions/discriminate.py --summary
python3 -m unittest discover -s research/feature_workbench/decisions -p 'test_*.py'
```
