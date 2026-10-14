# Book observations applied to physical witnesses

12 October 2026. This application compares the already exposed seven-book [feature-phase audit](../../sources/full_reads_2026-10-12/feature_phase_audit/README.md) with exact rows of the cave, tomb and water inventories. Its new evidence product is a reproducible source-to-clause comparison: which reported details belong to the particular feature and phase actually being proposed. It does not repeat the book audit or replace the frozen regional results.

## What changes in the comparisons

| Physical witness and entry | Immediate baseline | Applied result | Deciding source |
|---|---|---|---|
| Atara176 **western** pool, entry29 | Aggregate ASI83/2/34 has unknown feed. | Reported channel join becomes MATCH for the western child only; flow direction is unresolved. Great/north/four-sides and a dated inlet/wall/floor join remain UNKNOWN. The complete branch remains UNKNOWN. | SWP1883pp82–83 and native Benjamin1993p162 now checked; exact opening identity, gradient and dated contacts required. |
| Atara176 **eastern** pool, entry29 | Same two-pool aggregate. | No conduit promotion. The western channel supplies no eastern inlet. Dimensions remain descriptive; they do not automatically create a four-sides code. | Eastern-pool inlet/lining/floor section and dated context. |
| Absalom monument original access, entry56 | ASI102/410/T0247 has unknown west entrance, eight chambers and kokhim in its combined monument/associated-cave description. | Under the **published entrance-face model**, original southern access fails the west-access clause. Chamber count/kokhim/cistern become UNKNOWN for this separated monument witness; the sibling cave remains unpartitioned. | Original access/fabric plans and a phase-attached threshold record. |
| Absalom later breach, entry56 | Same parent record. | Later western access passes the reported-face clause, but breach date and matching chamber/threshold remain UNKNOWN. The original-access failure excludes only that access event. | Absolute breach sequence/date and feature-specific chamber plan. |
| BeneHezir and Jason, entries14/51/56 | F11 kokhim and F13 repositories already recorded. | Those observations add no new keyword match. Added rooms, collection features, original rock and fill remain distinct events; original west bearing and cistern join stay UNKNOWN. | BeneHezir plan128 contact sequence; Rahmani1967 pp61–68,92–100; distinct access/collection/blocking contexts (native follow-up below). |
| IV/17, Twin Cave, XII/53, entry25 | Published form/aspect alternatives, including Twin and XII/53 subset matches. | Every existing pillar/terrace, cave/both-mouth and ruleset branch remains. None supplies a dated ancient mouth/pillar/threshold configuration. IV/17 wall dates, Twin entrance dates and XII/53W2 date remain UNKNOWN. | L-656 frozen arrival targets; cave-specific Twin survey/diaries; L-608W2 foundation/opening section. |
| LowerHerodium B101, entry29 | Reported Herodian pool and aqueduct feed in both G-LHERODIUM-POOL accounts. | Keep those reported codes; construction transfer and unlocated inlet cannot satisfy a measured phase-attached aperture. The two accounts describe one parent pool. | Actual inlet, named wall face and contemporaneous floor section; existing closed-result rule applies. |
| EinQelt site16 and WadiQelt site6, entry32 | Previous manual review already changed site16 installation date to undated and site6 wall evidence to UNKNOWN. | These are the immediate baseline. Seven-book WadiKelt/Pharan observations have no exact outlet crosswalk and supply no new date or wall relation. The modern site6 configuration remains outside the ancient comparison. | Installation-specific original outlet/wall/use section. |
| Armon, Rogem, Ramat, entry46 | Existing native-source function/phase review. | Import every existing phase, function, anchor and radius branch. Ramat medieval storage never supplies its ancient bath phase; removed/blocked original stair failures remain separate from UNKNOWN alternative access. | Native Armon access/W11 contacts; Sion2002 or1999Rogem records; original Ramat bath-phase dating context. |

The Absalom changes use the book's reported **access face**, not a measured entrance azimuth or inferred approach path. A narrower surveyed-bearing interpretation remains unmeasured. The inventory flag `multi_tomb_record=no` does not authorize combining the monument's name and entrance with all chambers of its associated cave. Conversely, separating a child witness does not reject every feature in the parent record or remove that record from the historical denominator. Entry48's traditional-name match remains a reported catalogue match; ancient name attestation is separate. The broad facade-to-exedra keyword proxy in entry51 stays visible rather than silently acquiring an observed under-pillar relationship.

The Atara source is Benjamin1993 printed162/viewer184, observation `B93-0076`/FP05. Absalom's source is Kloner–Zissu2003 printed142–143/viewer156–157, `KZ2003-PDF156/157`/FP17, figs125–127. BeneHezir is printed144/viewer158, `KZ2003-PDF158`/FP18, fig128. Jason is printed242–243/viewer256–257, `KZ2003-PDF256/257`/FP19, figs250–252. Herodium B101 is Netzer1981 printed11/viewer19, `N002`, ill9, and printed70/viewer78, `N013`/FP20. Exact source URLs, observation-row hashes and figure IDs accompany each physical witness in [results.json](results.json). These initial references inherit verified project reading records. The subsequent Atara original-source trace below records its newly opened SWP pages and source limits.

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

## Native source application — 13 October 2026 UTC

The [five complete original-report readings](../../sources/full_reads_2026-10-12/five_remaining_2026-10-13/README.md) now feed [native_application.json](native_application.json) and the companion [evaluator](evaluate_native.py). Their results and source/hash joins appear in `results.json` under `native_application`, with [native_scores.csv](native_scores.csv) for the scored witnesses. This extends the same application record; the original lane files and existing geographic/numerical results remain the baseline.

**Jason (T0226), entries 14/51/56.** Rahmani records ten kokhim in Chamber A, including partly rock-cut/partly built kokhim 9/10, and a separate charnel Chamber B (pp. 61–64 / PDF 2–5). The earlier eight-loculi description is retained as a historical source difference; eight original rock-cut niches and ten total niches need not describe the same counting scope or phase. The source does not date a ten-niche original cutting merely by counting the excavation configuration. Two burial chambers, courts/porch, approximately 25 redeposited burials and ten kokhim are distinct quantities. The frozen F10 predicate asks for more than one chamber, so two chambers pass that limited predicate.

The southern forecourt step and internal northern courtyard doorway become separate witnesses (pp. 66–68 / PDF 7–13; Fig. 3 / PDF 8–11; plates 16–19 / PDF 49–52). For entry 56, they fail the west-opening proxy only under the explicitly inferred **reported-side-as-face** model. Under the **surveyed-bearing** model their facing bearings remain unknown; an unresolved entrance interpretation is also retained. A west jamb does not face the door west. The columned porch passes the existing broad F2x proxy for entry 51, but does not supply a named Zadok tomb, under-pillar target or joined cistern. Entries 14 and the location-constrained entry-51 branches retain their inherited location failures. Latest coins inform secondary burial/blocking (pp. 92–100 / PDF 37–45), not every cutting, threshold or usable access phase.

**Arnona, entry 46.** Exact native joins attach to phase-3 source rows 1090, 1091, 1092 (HAESI-832/A-4785) and 881 (HAESI-26567/A-9163). Area A's named group has eight pits; L105/L112 names one large partly cut feature; Area B has three pits. The 2024 bell-shaped cut is one feature. A literal ten-small-pits specification fails for each of these exact listed groups. An unlocated other set survives as unknown because selected or interrupted excavation does not establish complete coverage. Every pool/deep-pit and numerical reading from the existing entry-46 review remains visible. The fill dates, tentative Area-B building association and nearby settlement do not date the cutting or usable configuration. Native qualification changes Area B's reported-period bookkeeping from MATCH to UNKNOWN in this overlay; the historical row remains intact.

The prior unresolved Arnona grid ranges keep their disabled coordinates. Mordot keeps its enclosing report-range uncertainty. The 2.5 m and 5.3 m measurements describe features, not a ten-cubit deposit depth. No unit selection, new geographic point, original access datum or full negative excavation follows. Exact loci, dimensions, coverage and the observation needed to decide each branch accompany the native witnesses.

**Tell en-Nasbeh.** The source-defined relation “Cistern 320 functioned as an open cistern alongside the R389/390 colonnade” is contradicted by the published closure-before-colonnade sequence (McCown p. 213 / PDF 237, Fig. 53A; plate 77 / PDF 435). This rejects that simultaneous-active-use specification. It does not attach an invented candidate ID or regional exclusion to the site. The standing stone reset beside the proposed early gate supplies a second rejected photo-to-ancient-context inference (p. 244 / PDF 268; plate 73:2–3 / PDF 431). Original stone context and other feature pairings remain separate questions.

**Gibeon.** The northeast rectangular reservoir, small western stepped pool and circular cut receive distinct source witness IDs, dimensions and date/supply qualifications (Pritchard pp. 67–70 / PDF 4–7). Tunnel mouths and branches receive a separate access record (pp. 71–75 / PDF 8–12, Figs. 4–5). Combining their properties into one feature is rejected. No exact matching parent row was found in the inspected cave/tomb/water lanes, so these source-defined comparanda have no invented lane score or map geometry. A future entry comparison must first name the actual installation, original use phase and measured entrance relation.

**Atara dependency.** McCown pp. 54–55 / PDF 78–79 transmits SWP, Guérin and Dalman observations. The cited SWP pages have now been read directly: they describe an outlet but print no Atara hydraulic drawing. The detailed source comparison and replacement dependency are below.

The full candidate comparisons remain **not identifiable from available evidence**. The explicitly named relation/group/direction failures are conditional source-consistency results from exposed evidence. They add no registered unseen prediction or regional rarity inference.

Rebuild with `evaluate.py`; run `test_application.py` and `test_native_application.py`. The native checks cover entrance-model separation, niche/chamber count scope, inherited position disabling, group-count versus unknown coverage, preservation of every numerical reading and reproducible source/hash joins.

**Obtained** — native source-to-clause applications, exact locus/feature splits, conditional failures and explicit next observations.

## Atara original-source trace — 13 October UTC / 12 October Los Angeles

The original published entry is Conder and Kitchener, *SWP Memoirs III: Judaea* (1883), printed **82–83**, University of Toronto scan **PDF98–99**. The [native source pages](../../assets/plans/swp1883-atara/swp1883-atara-source-pages.pdf) preserve its title, illustration list and full entry context. The [figure manifest](../../assets/plans/swp1883-atara/figure_manifest.json) records hashes, extraction and reuse; the assets have identical atlas mirrors. The user-supplied scan matches the downloaded scan byte for byte. The [source trace](atara_source_trace.json) records observations, source labels, identity limits and access routes.

SWP describes two reservoirs, the second northeast of the first. Its principal reservoir is **78×37ft** (23.7744×11.2776m), with a nine-foot wall and four internal buttresses. It explicitly calls the pointed-arched opening an **outlet**. These dimensions closely match Benjamin1993's western **24×11.5m** pool, rather than the eastern32×14.5m pool. That supports a likely pool crosswalk. SWP does not expressly label its principal reservoir western, and supplies no plan identifying the individual opening.

Benjamin1993, printed **162 / PDF184**, site176, was reread in the native Hebrew scan. It places a vaulted corridor at the western pool bottom and a water channel at the corridor bottom, then describes that stone-section channel as **leading to the pools** (plural). This is a published supply-direction label. It does not establish which pool-wall aperture the channel enters, its gradient, or the date of operation. The spring pool and open channel about100m north are distinct installations.

| Required relationship | Source observation | Result |
|---|---|---|
| Principal SWP pool = later western pool | Dimensions agree closely; second pool is northeast | Likely pool identity; not a surveyed outline crosswalk |
| SWP arched outlet = Benjamin bottom-channel | Neither entry provides an aperture plan, section or station ID | UNKNOWN |
| Bottom-channel fed or drained the western pool | SWP labels an outlet; Benjamin describes a channel leading to the pools | Actual flow UNKNOWN until those features are crosswalked |
| Channel and pool operated together | No joint fabric contact, invert/gradient or dated use context | UNKNOWN |

There is **no Atara drawing on pp82–83**. The plan on p82 belongs to **Anata's colonnaded building**, as its surrounding text and the illustration list show. Neither it nor a general SheetXVII map can supply an Atara inlet section. A single opening described differently, separate inlet/outlet openings, and changed hydraulic phases remain unresolved possibilities; none is an observed reconstruction. The pointed arch and site-level Byzantine sherds cannot date the cutting or joint operation.

The existing entry29 **conduit=MATCH** means only a **reported channel join**, under the lane's published “feeds or joins” rule. It cannot be restated as a proved feeder, a contemporary inlet or an ancient operating configuration. The original whole-candidate comparison remains **not identifiable from available evidence** for those missing relationships.

The British Library's [AddMS71548A–V](https://searcharchives.bl.uk/catalog/032-001965756) catalogue identifies survey observation/calculation notebooks, but supplies no digitized content or confirmed Atara sheet. [AddMS69848](https://searcharchives.bl.uk/catalog/032-002043164) mainly holds mapping calculations and a four-miles-to-inch working map; its catalogue expressly says the papers are not by Conder/Kitchener themselves. The exact Atara drawing is not established in either collection. The initial PEF documents/maps URL failed; the custody follow-up below records the corrected working URL. The British Library catalogue routes identify collections, with Atara contents unconfirmed. Exact access failures remain in the trace.

Next obtain the **Atara/Attara (M s, SheetXVII, beside Tell enNasbeh) original hydraulic plan/section**, identifying the78×37ft pool, nine-foot east wall, four buttresses, pointed-arched outlet and stone-section channel. The deciding evidence is channel invert/gradient plus the pool-floor/wall contacts and a dated construction or use context. Establish the drawing's existence and shelfmark first. McCown and the published SWP entry are now resolved dependencies; rereading them cannot supply that missing section.

**Partly** — obtained the original published description and separated its outlet label from the later supply account; the exact hydraulic drawing, actual channel direction and joint-use phase remain unavailable.

## Atara drawing custody — 13 October UTC / 12 October Los Angeles

PEF's working [Documents & Maps page](https://www.pef.org.uk/collections/documents-maps/) confirms that it holds Conder and Kitchener's SWP documents, reports, plans and maps. Its [collections page](https://www.pef.org.uk/collections/) directs holdings enquiries to the curator. The [current staff page](https://www.pef.org.uk/about/staff-committee/) identifies **Felicity Cobbing, Chief Executive & Curator**, at **execsec@pef.org.uk**. The owner's existing sent Copper Scroll enquiry uses that same office address, so recipient identity is resolved for this separate subject. The earlier failing URL used `documents-and-maps`; the working page uses `documents-maps`.

Collection custody is established. **An Atara drawing, its shelfmark and its contents remain UNKNOWN.** The public pages inspected provide a collection description and access route, without an item inventory sufficient to establish absence. Bounded searches under Atara/Attara, Tell en-Nasbeh, SWP and original-plan terms located no exact reservoir/channel drawing record. OpenJerusalem's indexed PEF/Conder descriptions identify the **published** map (`JM-NLI/ELCC/Pal751`) and **published SheetXVII** (`JM-NLI/ELCC/Pal751/sheet17`), held in the National Library of Israel's Laor Collection. These records do not establish custody of an unpublished hydraulic section. Live catalogue pages timed out; their indexed descriptions were readable. PEF's linked library page describes published-volume access and database redevelopment. It supplies no Atara archival item. The [source trace](atara_source_trace.json) records the inspection scope and failures.

The surviving possibilities include an unindexed PEF sketch or notebook entry, a record with another custodian, and a drawing that was never made or no longer survives. Catalogue silence cannot choose among them. The next evidence is the curator's holdings response identifying the original record and what it actually shows.

### Holdings enquiry sent — 13 October UTC / 12 October Los Angeles

**Sent 13 October 2026 at02:58:42UTC / 12 October at19:58:42LosAngeles**, following the owner's explicit send instruction, from the existing personal project account to Felicity Cobbing's verified PEF office address. Gmail confirmed SENT. The enquiry asks for holdings metadata and a custodial reference; the drawing's existence and exact shelfmark await a reply.

Subject: **SWP holdings enquiry: ‘Attara reservoirs beside Tell en-Nasbeh**

Hello Felicity,

I’m tracing the pool and channel at ‘Attara (M s), beside Tell en-Nasbeh, described in Conder and Kitchener’s *Survey of Western Palestine, Memoirs III* (1883), pp. 82–83, Sheet XVII.

The published Sheet XVII marks ‘Attara and a tank near Tell en-Nasbeh. I’m seeking the original site-level survey record.

Does PEF hold an original survey sketch, plan, section or field-notebook entry for these reservoirs? The described principal pool measures 78 × 37 feet, with a nine-foot wall, four internal buttresses and a pointed-arched outlet. The 1993 Benjamin survey describes a vaulted corridor and stone-section water channel at the bottom of the western pool (24 × 11.5 m), with the channel leading to the pools.

I’m trying to establish whether the two reports describe the same opening and whether an original record shows channel levels or its connection to the pool. Could you identify a shelfmark and briefly describe what survives? If another archive holds the original record, a custodial reference would help.

Thank you,
Alex

**Partly** — confirmed PEF's SWP archive and curator route; sent the Atara holdings enquiry; drawing/shelfmark await a reply.

### Uploaded SWP map check

The owner's `dedupmrg54258818_IE199398504.pdf` (SHA256 `5a9bc74683887ab4cac377a476a20b832a05aa7cc73b7d6e1d513fa672a61ba7`) contains published SWP map scans. **PDF17 is SheetXVII**, whose imprint dates it1879; the handwritten library1880 and the catalogue map-set date remain distinct. This sheet places **Attara beside Tell enNasbeh** and marks **Tk.** by a small tank symbol. The [Atara detail](../../assets/plans/swp-upload-atara-2026-10-13/atara-detail.jpg), [overview](../../assets/plans/swp-upload-atara-2026-10-13/sheet-XVII-overview.jpg), [scale/legend](../../assets/plans/swp-upload-atara-2026-10-13/sheet-XVII-legend.jpg), [native map pages](../../assets/plans/swp-upload-atara-2026-10-13/swp-sheets-I-XVII.pdf) and [manifest](../../assets/plans/swp-upload-atara-2026-10-13/figure_manifest.json) have matching atlas copies. SheetI was encountered while identifying the upload, so its native page is also preserved.

The map supplies site context and a tank notation. It does not distinguish the western/eastern pool apertures or give a hydraulic section. At its printed1:63,360 scale, a24m pool occupies about0.38mm and a2.74m wall about0.043mm; these scale conversions do not measure the tank symbol. Actual flow, connection fabric and joint-use phase remain UNKNOWN. The enquiry states that the published map has been checked and asks for the original site-level record.
