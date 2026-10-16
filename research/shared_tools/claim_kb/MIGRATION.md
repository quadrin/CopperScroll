# Migration audit

The isolated checkout began on `main` at `da9b9c6907b7046dc30462e5314fb4aeb7e6d0c0`, with no existing worktree edits. Implementation lives on local branch `local/claim-kb-pilot`. No remote mutation, source acquisition or new source inspection forms part of this migration.

Existing infrastructure supplies most domain records. The feature workbench owns physical IDs, Koḥlit branches/assignments, cave observations, states, frames, coverage obligations, evaluations and decision targets. Shared tools own concordance packets, manuscript catalogue correspondence, SQLite and the loopback-only server. The pilot adds adapters plus claims, individually addressed edition interpretations, name occurrences/search scope, explicit identity proposals, gaps and versioned dependency results.

## Authoritative inputs and preserved identifiers

- `tables/entry_concordance.csv`, `text/readings.json`, `text/translation_en.json`, `tables/feature_constraints.csv`: all canonical entry IDs, including `12a`; edition numbering, boundaries and reading IDs such as `e11-kohlit`, `e60-janoah`, `e25-direction`, `e18-asla` remain intact. Suffixes address individual edition alternatives without replacing their parent IDs.
- `research/shared_tools/mapping_claims.json` and the three existing USC metadata manifests: catalogue image identifiers, original/replica distinction, cut 21/22, edition-scaffold status, null ROIs, source rights and existing hashes remain metadata. Image bytes and reserved new observations are excluded.
- `feature_workbench/relationships/model.json` and its evaluator: `RB-M`, `RB-P`, `RB-B`, `RB-L`, all eight assignments, both windows, all 40 comparisons and the quarry-phase diagnostic remain source controlled. Twelve assigned combinations remain contradicted and twenty-eight unknown. The historical irregular basin, 1898 reservoir, NS1, D9 and quarry pits remain separate.
- `feature_workbench/inventory/catalog.json`, `queries.json` and its evaluator: `iv17`, `iv11`, `twin`, their physical-feature IDs, four form branches and 96 target-prerequisite branches each remain intact. Three cubits stays a digging instruction; widths never replace a threshold datum.
- `feature_workbench/states/register.json`, its evaluator, the existing IV/17 registration metadata and endpoint-repeat JSON: state IDs, transition relations, local frames, hashes and phase/datum unknowns remain intact. No world placement is added.
- `regional/caves_entry25/caves.csv`, `scores.csv`, `PLAN.md`, `AMENDMENT_1.md`, index crosswalk and README: `A41:IV/17`, `A41:IV/11`, `A41:XII/53`, `REPO:TwinCave`, `REPO:JonesNorth` retain 16 separately scored regional models each. The complete frozen roster remains on the test. A41 X/47, WB:E707 and DJD site 32 retain separate identities; proposed crosswalks remain unverified. The regional IV/11 singular-opening and terrace codes remain distinct from the older workbench's unknowns.
- `feature_workbench/available_evidence_2026-10-13/cave_native_check.md`: XII/53 W2 division, its undated construction and the L10/W1 distinction remain reviewed report observations. The Bar-Adon pillar citation uses printed `[15]`, while the frozen regional table's original p16 citation remains preserved. Two different supplied digital copies retain their different pagination; no offset is inferred between them.
- `agent_review_2026-10-07/wave1/T05_period_texts/data/attestation_concordance.json`, `REPORT.md`, `source_coverage.csv`: `T05-001`, `T05-002`, `T05-062` remain individually addressable. `T05-006` remains an unproven referent-identity proposal. The grouped T05-003 loci/variants are outside this occurrence pilot pending witness-specific segmentation.
- `feature_workbench/results.json`: historical workbench register/coverage results remain available through exact JSON pointers. Selected relationship, inventory and state evaluators also recompute from their canonical inputs. Historical source/campaign identities remain separate from independent observation claims.
- `feature_workbench/decisions/plans.json` and `decisions/separation/results.json`: exact acquisition targets, frozen-protocol pointers and hypothetical consequences remain distinct from observed outcomes. Private request/correspondence fields and the outreach/active-status source records are omitted. The separation result retains its original input versions and historical baseline.

`reviewed.json` holds only the pilot's explicit bibliographic/copy mappings, original-drawing reuse identity, alias questions and migration gaps. It points to existing reviewed notes rather than maintaining a second archaeological catalogue. Edit the authoritative input to correct a measurement, reading, assessment or source scope. Rebuild to refresh the SQLite/query projection.

Every build stores a machine-readable record/locator map and input hashes in `cache/kb.json` and the `kb_*` SQLite tables. `kb demo` produces all eight query answers with IDs, branch/window context, source locations and unknowns. These generated files require no separate maintenance.

## Unresolved gaps retained

Koḥlit still needs the manuscript reading, an ancient pool phase/corner, named usable pit-mouth/grave relationships and dated coexistence. Kallai pp172–173 remain uninspected under the current repository assessment. Historical photographs and rough wall ties cannot date the basin. Kenyon's later pits do not establish early joint accessibility.

Entry 25 still lacks ancient thresholds, origins/paths, architectural contacts and individual-mouth bearings where recorded unknown. XII/53's Early Roman L10 abuts W1, without dating W2. Its printed grid is flagged as a likely misprint and remains unregistered. XII/53 and Jones North have explicit gaps for the original workbench's target-prerequisite extraction; the migration does not manufacture a fourth/fifth completed workbench test. The regional controls keep their own specification and incomplete coverage limits.

The original-object letter observation layer and complete restoration/visible-letter segmentation remain unpopulated pending reviewed evidence. Manuscript images retain catalogue associations. The pilot models these distinctions and exposes their gaps without inventing letter votes.

The external Koḥlit occurrences lack identified physical-manuscript dates and locations. Their composition dates and historical period are approximate attributions. ʿAṣla's unsuccessful search lacks a complete name-specific item-inspection log. It stays a bounded negative search with an explicit coverage gap.

Archive arrivals, new manuscript frames, independent controls, a complete regional inventory and reserved evidence remain under existing project protocols. No acquisition occurs. No deposit, landmark identification or new identification support follows from this software migration.

## Subsequent research follow-up: 15 October 2026

After the software migration, the owner authorized an extended local research pass. Targeted existing-Drive copies of the Twin Complex atlas, Kallai1968 preliminary report, Hamer2023 cave report and Frumkin2023 geology chapter were inspected to the exact scopes recorded in [the cave note](../../feature_workbench/available_evidence_2026-10-13/cave_native_check.md) and [the Koḥlit note](../../agent_review_2026-10-07/followup/B_kh_el_marjama.md). These later observations are not represented as part of the earlier evidence-preserving migration or as independent confirmation.

`reviewed.json` adds individually addressed source observations, modern Twin West states, unmerged alias proposals and a unit-concordance acquisition target. Atlas North remains distinct from the proposed Bar-Adon northern-unit / Atlas East crosswalk. The source grids stay literal text, with no geographic registration. The old hypothesis assignment and all historical evaluations remain intact; the new prerequisite requires review before relying on Twin results. Earlier SQLite snapshots retain their inputs. Kallai1972 remains an explicit uninspected source. The continuation below supersedes the earlier Freikman access status. No reserved manuscript frame, protected archive arrival or rarity re-score is part of this follow-up.


### Continued source follow-up and owner attachment

The correct owner attachment verifies Freikman2020 native pp93–96 and Figures1–4, including the ICRC2017 plan/sections. The work, screen-capture copy hash and page/slice mapping remain separate from the unrelated scraper-article attachment. The recovered ITM label does not establish a survey-point definition, coordinate precision or geographic registration. The native plan is an individually addressed observation distinct from the excavation seal/hearth context.

Gutfeld2020 indexed pp71–80 supplies a later northeast entrance description, built divider and explicit original53 / XII53A naming history. Upper XII53B remains a distinct, unassigned feature. Gutfeld's native plan Figure2 p73 is still uninspected; Figure3 p74 is XII52. Earlier east and later northeast descriptions coexist without rewriting the frozen regional comparison. The source-scope conflict concerning the natural cavity and built masonry remains qualified, with no project assertion of masonry absence. XII53 evaluations acquire reassessment dependencies; historical results retain their original inputs and scores.

Elmakyes2024 contributes only a bounded text-index/contents inspection recorded in the existing hydraulic review. No target-pool observation or archaeological absence is inferred. Source image rights remain unresolved, and no new source image enters a public export. These follow-ups are research observations separate from software completion and supply no identification support.


### Atlas homepage projection

The later atlas update publishes a deterministic, validated metadata projection through the existing `public_view` exposure filter. Entry indexes are generated after filtering, so hidden dependencies cannot leak through navigation. The static snapshot contains canonical IDs, typed edges, source locators and input hashes. It exports neither local source-image bytes nor the SQLite history. The public change-impact view traces stored dependencies and labels reassessment separately from historical outcomes. The canonical record files and their source notes remain the places to review evidence.
