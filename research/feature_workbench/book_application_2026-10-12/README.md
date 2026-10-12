# Book observations applied to physical witnesses

12 October 2026. This application compares the already exposed seven-book [feature-phase audit](../../sources/full_reads_2026-10-12/feature_phase_audit/README.md) with exact rows of the cave, tomb and water inventories. Its new evidence product is a reproducible source-to-clause comparison: which reported details belong to the particular feature and phase actually being proposed. It does not repeat the book audit or replace the frozen regional results.

## What changes in the comparisons

| Physical witness and entry | Immediate baseline | Applied result | Deciding source |
|---|---|---|---|
| Atara176 **western** pool, entry29 | Aggregate ASI83/2/34 has unknown feed. | Reported conduit becomes MATCH for the western child only. Great/north/four-sides and a dated inlet/wall/floor join remain UNKNOWN. The complete branch remains UNKNOWN. | McCown1947pp54–55 and original western bottom-channel section. |
| Atara176 **eastern** pool, entry29 | Same two-pool aggregate. | No conduit promotion. The western channel supplies no eastern inlet. Dimensions remain descriptive; they do not automatically create a four-sides code. | Eastern-pool inlet/lining/floor section and dated context. |
| Absalom monument original access, entry56 | ASI102/410/T0247 has unknown west entrance, eight chambers and kokhim in its combined monument/associated-cave description. | Under the **published entrance-face model**, original southern access fails the west-access clause. Chamber count/kokhim/cistern become UNKNOWN for this separated monument witness; the sibling cave remains unpartitioned. | Original access/fabric plans and a phase-attached threshold record. |
| Absalom later breach, entry56 | Same parent record. | Later western access passes the reported-face clause, but breach date and matching chamber/threshold remain UNKNOWN. The original-access failure excludes only that access event. | Absolute breach sequence/date and feature-specific chamber plan. |
| BeneHezir and Jason, entries14/51/56 | F11 kokhim and F13 repositories already recorded. | Those observations add no new keyword match. Added rooms, collection features, original rock and fill remain distinct events; original west bearing and cistern join stay UNKNOWN. | BeneHezir plan128 contact sequence; Rahmani's1956 Jason excavation contexts. |
| IV/17, Twin Cave, XII/53, entry25 | Published form/aspect alternatives, including Twin and XII/53 subset matches. | Every existing pillar/terrace, cave/both-mouth and ruleset branch remains. None supplies a dated ancient mouth/pillar/threshold configuration. IV/17 wall dates, Twin entrance dates and XII/53W2 date remain UNKNOWN. | L-656 frozen arrival targets; cave-specific Twin survey/diaries; L-608W2 foundation/opening section. |
| LowerHerodium B101, entry29 | Reported Herodian pool and aqueduct feed in both G-LHERODIUM-POOL accounts. | Keep those reported codes; construction transfer and unlocated inlet cannot satisfy a measured phase-attached aperture. The two accounts describe one parent pool. | Actual inlet, named wall face and contemporaneous floor section; existing closed-result rule applies. |
| EinQelt site16 and WadiQelt site6, entry32 | Previous manual review already changed site16 installation date to undated and site6 wall evidence to UNKNOWN. | These are the immediate baseline. Seven-book WadiKelt/Pharan observations have no exact outlet crosswalk and supply no new date or wall relation. The modern site6 configuration remains outside the ancient comparison. | Installation-specific original outlet/wall/use section. |
| Armon, Rogem, Ramat, entry46 | Existing native-source function/phase review. | Import every existing phase, function, anchor and radius branch. Ramat medieval storage never supplies its ancient bath phase; removed/blocked original stair failures remain separate from UNKNOWN alternative access. | Native Armon access/W11 contacts; Sion2002 or1999Rogem records; original Ramat bath-phase dating context. |

The Absalom changes use the book's reported **access face**, not a measured entrance azimuth or inferred approach path. A narrower surveyed-bearing interpretation remains unmeasured. The inventory flag `multi_tomb_record=no` does not authorize combining the monument's name and entrance with all chambers of its associated cave. Conversely, separating a child witness does not reject every feature in the parent record or remove that record from the historical denominator. Entry48's traditional-name match remains a reported catalogue match; ancient name attestation is separate. The broad facade-to-exedra keyword proxy in entry51 stays visible rather than silently acquiring an observed under-pillar relationship.

The Atara source is Benjamin1993 printed162/viewer184, observation `B93-0076`/FP05. Absalom's source is Kloner–Zissu2003 printed142–143/viewer156–157, `KZ2003-PDF156/157`/FP17, figs125–127. BeneHezir is printed144/viewer158, `KZ2003-PDF158`/FP18, fig128. Jason is printed242–243/viewer256–257, `KZ2003-PDF256/257`/FP19, figs250–252. Herodium B101 is Netzer1981 printed11/viewer19, `N002`, ill9, and printed70/viewer78, `N013`/FP20. Exact source URLs, observation-row hashes and figure IDs accompany each physical witness in [results.json](results.json). These references inherit verified project reading records; no new source page or protected arrival was opened here.

## Where application stops

Every FP01–FP25 row has an explicit identity disposition and a next source in `results.json`. A shared place name is insufficient to identify an individual feature. In particular:

- UpperBethHoron's east pool and west tombs have descriptive locators but no exact row in the inspected lane tables. Four tombs, one repository and ten separately counted cisterns supply no single tomb–cistern complex, west-facing original entrance or in-window usable configuration.
- Pharan/EinFara descriptions span several cisterns and cave complexes. They crosswalk only at site level to ASI102/610/WB2709; later stairs cannot fill an ancient mouth/aspect clause. Benjamin and Hirschfeld partly transmit shared fieldwork.
- Ein esSawiya is not the WadiQelt ASI EsSawiya installation solely by name. Rock ofCrosses is not A41VIII/2 Cave ofCrosses solely by name. Neither coincidence supplies a source-to-feature identity.
- Herodium B40/B58, C11/2/C35 and cistern-mouth corridors remain distinct from B101. Earlier B52 floor, Herodian floor pottery and a reconstructed divider cannot migrate into another feature's dating, floor datum or geometry.
- Choziba's restored boundary gates do not identify ancient individual cave mouths. Ordinary Dalman plates22–23 lack a dated geolocated feature join; plate25 fine detail stays reserved.

This is a selected application, with unequal existing inspection among candidates and controls. It provides no regional counts or rarity estimate. The common rule applies to each witness: a required undocumented relationship/date stays UNKNOWN. A usable configuration may predate the scroll's window if its relevant use is dated; demanding in-window construction would exclude such cases incorrectly. None of the present source joins supplies that missing use/configuration observation. An old label of Roman/Herodian use, fill, occupation or source typology remains visible without becoming a sealed construction context.

**Terminal claim:** the full phase-attached comparisons are **not identifiable from available evidence**. The original southern-access witness fails only the specified west-access/entrance-face branch; the later western-access alternative survives as unknown. The entry29 closed measurement assessment remains closed pending its named section. These exposed exploratory records supply no unused prediction or independent confirmation.

## Reproduce and verify

[applications.json](applications.json) contains authored feature/phase bindings. [evaluate.py](evaluate.py) joins by exact inventory IDs, carries source observation/figure references, preserves all selected lane branches, uses the existing manual water corrections as its immediate baseline, and imports the complete existing bath phase review. [applied_scores.csv](applied_scores.csv) reports raw historical result, prior manual result, before/after clauses and the additional configuration/datum requirements separately. Child witnesses never increment site counts.

Run from the repository root:

```bash
python3 -I -B research/feature_workbench/book_application_2026-10-12/evaluate.py
python3 -I -B research/feature_workbench/book_application_2026-10-12/test_application.py
```

[input_manifest.json](input_manifest.json) pins the inspected source/inventory/score bytes and authored evaluator. Eight regression checks cover sibling isolation, access-phase alternatives, occupation-to-configuration transfer, unchanged historical inputs, exact source/parent identity, previous water corrections, all bath alternatives and byte-for-byte reproducibility. Passing checks establish provenance and evaluation discipline; they do not independently verify the original archaeology.

**Obtained** — an applied physical-witness comparison with explicit phase/access branches and source-to-score identities; exact-feature records and dated contacts remain the next dependencies.
