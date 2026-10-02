# M05 / R10: region grouping with all text slots retained

Date: 2 October 2026 UTC / 1 October Los Angeles. Input pin: `quadrin/CopperScroll@4a6c4434ff86f213aa2471351707ef2e8d7ab663`.

This pass freezes the project's existing associations, then measures how confidence exclusions, Achor alternatives, an unresolved Secacah branch and documented entry divisions change regional adjacency. The atlas and concordance each contain **61 project slots: entries 1–60 plus 12a**. Every scenario preserves those slots as explicit members, including unknowns. The previous selected-stop distance cases remain historical output; this pass adds no distance rerun.

## Frozen inputs and provenance

`sequence_grouping/frozen_input_ledger.json` records all 61 slots, their edition spans, source citations, phase statements, current candidate association grades, candidate alternatives, point/area coordinates, coordinate provenance and stated precision. `frozen_input_ledger.csv` supplies a flat audit copy. `run_manifest.json` hashes the ledger, copied source inputs, scripts and outputs. The ledger was written before the metrics were computed.

The primary association source is current `atlas/app/atlas-data.json`. The older `tables/phase3_places.csv` and site index provide an audit comparison. Current atlas entry 46 is low confidence; the older table still says medium. This calculation uses the atlas grade and preserves the discrepancy in its input copies. Every candidate remains a project hypothesis; independent verification of its association and coordinate source remains pending. The coordinates denote site/area anchors. No individual deposit location follows from this calculation.

The existing place categories are `jericho`, `jerusalem` and `region`. The first two retain their recorded spelling and membership. `region` combines geographically separate places such as Gerizim, Beth Shean, Hyrcania and Mar Saba; the calculation therefore treats it as unclassified. An unclassified regional slot can still have a published site-level hypothesis and coordinates. The current data supply no independently reviewed fine-district footprint map. This pass assigns no new district labels.

## Experiment

The frozen family contains 64 descriptive cases: every combination of two Achor anchors, two Secacah treatments and two confidence rules, crossed with eight explicit division cases. There is no random seed or sampling.

Achor cases retain Nuweimeh or replace it with the existing Buqeia alternative at entries 1 and 17. Each retains that candidate's recorded confidence. Secacah cases retain the current Qumran associations or leave 20–23 region-unassigned; the latter also avoids propagating an uncertain attachment to 23. Confidence cases retain low/medium/high associations or retain medium/high alone. Weak and ruled-out candidates are excluded throughout.

A sole preferred retained candidate supplies its recorded region. In the absence of a preferred candidate, the region is assigned only when every retained alternative shares one classified region. Conflicting or unclassified alternatives keep the slot unknown. Unknown slots break runs and remain in the adjacency denominator.

Division cases use project order; join 12/12a; join 40/41; join 41/42; join 49/50; split 9 at II 8/9; split 56 at the concordance's XII 1a/1b and XII 2a/2b boundaries; and combine the two splits. Concordance citations include Puech p.173 n.26 and Lefkovits pp.126, 142, 293–296, 358–362 and 399. These are recorded edition references; this pass inspected no new original edition pages.

A joined unit receives a region only when every original member has that same known region. Split subunits remain region-unassigned because the current evidence does not independently attribute the parent anchor to each subspan. Thus the split results measure the consequence of unresolved subspan attribution. They cannot establish a geographical change at a manuscript boundary. The combined split case yields 64 item-body units; it supplies no complete Milik apparatus reconstruction.

Closing-phrase attachments around 22/23 and 50–55 remain explicit pending mappings in the ledger. Moving a phrase preserves physical order but can change which item carries a proximity claim. The current input cannot assign an independent feature location to each moved phrase. Fine-district JO/QB/DS calculations and vocabulary/name tests under these attachments remain pending.

## Results

With current Qumran assignments, Nuweimeh Achor and low-confidence associations included, the canonical 61-slot case has 43 region-classified slots, 31 same-region adjacent pairs, four different-region pairs and 25 pairs touching an unknown slot. Its longest run contains 11 entries, 46–56, assigned to the recorded Jerusalem category. Excluding low-confidence associations leaves 13 classified slots, six same-region pairs and a longest run of three. Removing Qumran assignments as well leaves ten classified slots and four same-region pairs. Substituting Buqeia in that case leaves nine classified slots and three same-region pairs.

Across the eight canonical cases, same-region adjacency ranges from 3 to 31 and the longest run from 3 to 11. Three canonical pairs persist in every model: 9–10, 30–31 and 31–32. The 30–32 run persists in all 64 division/model cases under the existing coarse Jericho category. This describes a macroregion assignment and leaves fine-district proximity and independent association verification unresolved. Splitting entry 9 leaves its separate cistern/channel spans unassigned, so the 9–10 pair lacks an independently anchored equivalent in those cases.

The ten-entry run at 17–26 requires the Nuweimeh choice, current Qumran associations and low-confidence intermediate assignments. The 46–56 Jerusalem run requires low-confidence assignments. These runs describe the frozen candidate ledger; they do not establish uninterrupted ancient travel. The current ledger cannot verify a regional transition at 35/36 because entry 35's place carries the heterogeneous unclassified category. The calculation leaves unknown intervening entries in their physical order.

Joining 12/12a reduces same-region adjacency by one when both low-confidence Jerusalem assignments are retained. Joining 49/50 has the same effect in that confidence case and reduces the longest Jerusalem run from 11 to 10. Attachments involving 40/41/42 change the item denominator while all involved regions remain unresolved. Explicit outputs separate these denominator changes from the unchanged order of scroll passages.

Buqeia's `region` label remains unclassified in this coarse ledger. Its reduced pair count measures missing classification at that scale. It supplies no evidence favoring Nuweimeh over Buqeia. The former fine-district/HMM preference for Buqeia remains outside the scope of this calculation.

## Completion and next discriminating work

This bounded grouping sensitivity calculation is complete. R10 remains open. The next work requires independent association audits for the surviving anchors 9/10 and 30/31/32; geographic footprints and provenance for a fine-district partition; separate cistern/channel locations at entry 9; independent subspan locations at 56; and exact edition-page verification for the moved closing phrases. Secacah/Qumran and Achor need location evidence acquired independently of entry order before they can support held-out itinerary tests. Existing labels and approximate coordinate precisions supply no calibrated location probabilities.

Primary-source inspection increment: 0. Bounded source-check increment: 0. Decisive candidate-test increment: 0. Question closures: 0. The 64 cases constitute one computational sensitivity pass, with repeat pilot work excluded.

Reproduce the measurements with `python sequence_grouping/measure_grouping.py`. The script requires only `frozen_input_ledger.json` beside it. `scenario_metrics.csv` contains all summaries; `scenario_edges.csv` preserves every ordered pair; `stability_summary.json` gives surviving edges and ranges. `grouping_results.json` additionally includes every unit assignment and run and can be regenerated from the frozen ledger. Full source snapshots and the ledger-generation helper remain local provenance material. The manifest records their pinned repository URLs and normalized SHA-256 hashes; recreating the ledger requires those exact UTF-8 source files normalized from CRLF to LF.
