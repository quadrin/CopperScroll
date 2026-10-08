# Feature workbench contract

This is a user-requested implementation of methods 2–6. Existing source records are already exposed exploratory evidence. This work does not reopen parked tests, add source-inspection counters, certify an unused observation, identify a deposit, or authorize correspondence or purchases.

The integrator owns this contract, `features.json`, `build.py`, all atlas files, shared trackers and Git operations. Each worker owns only its named subdirectory: `relationships`, `inventory`, `states`, `coverage` or `decisions`. Do not edit another worker's files. Read the root AGENTS.md and the evidence relevant to your pilot. No Git commits or branch changes by workers.

Each module provides `evaluate.py` with `build(repo_root: pathlib.Path) -> dict`. It must work using Python's standard library and local reviewed inputs. A CLI may print its result as JSON. Keep source data and meaningful evaluator tests within the module directory. Do not depend on another module's uncompleted output. The integrator runs all modules and generates the shared register and atlas snapshot.

The returned object has these keys:

- `id`: directory name; `number`: method number 2–6; `title`, `summary`, `scope`: plain text.
- `sources`: records with unique module-prefixed `id`, `title`, `citation` (exact pages/figures where available), `repo_path` (existing evidence file), `url` (optional), `inspection` (`already_inspected`, `not_inspected` or `derived`), `original_campaign` (optional). Never imply an unread original was inspected.
- `features`: optional new feature definitions with `id`, `name`, `kind`, `site`, `geometry` (null unless justified). Do not redefine a feature in the shared list below. A documentary source notice is not automatically a distinct physical feature.
- `observations`: records with module-prefixed `id`, `feature_id`, `property`, `value`, `evidence_kind` (`observed`, `published_reconstruction`, `excavator_label`, `textual_constraint` or `inference`), `source_ids`, `exposure` (`already_inspected`, `not_inspected` or `derived`), and optional `phase`, `reference_frame`, `uncertainty`. Preserve nulls for missing observations. Quantities must carry their units/reference frame in the value or metadata.
- `states`: optional records with module-prefixed `id`, `feature_id`, `label`, `status` (`observed`, `reconstructed` or `unknown`), `source_ids` and optional `phase`, `geometry`, `reference_frame`, `uncertainty`, `note`. A local plan is not a registered geographic overlay.
- `results`: records with module-prefixed `id`, `title`, `claim`, `status` (`compatible`, `contradicted`, `unknown`, `mixed` or `info`), `checks`, `unknowns` (list of strings), `source_ids`, `feature_ids`. Each check has `id`, `label`, `status` from the same set, `detail`, `source_ids`, `feature_ids`, and optional `value`. Status `compatible` means exploratory compatibility only. No numerical identification confidence.
- `data`: optional module-specific JSON for interactive presentation. Prefer finite saved branches/queries with transparent predicates and results over prose-only reports. Include full retained misses and unknowns.

Shared feature IDs (definitions are in `features.json`):

- `iv17-cave`, `iv17-north-mouth`, `iv17-south-mouth`, `iv17-pillar`, `iv17-south-wall` (Sion Plan 5; uncertain dates/thresholds/bearings).
- `iv11-cave`, `iv11-pillar`, `twin-cave` (separate controls; missing mouths/dimensions are unknown).
- `jericho-tell`, `jericho-historical-basin`, `jericho-reservoir-1898`, `jericho-springhouse-wall`, `jericho-shaft-d9`, `jericho-cistern-ns1`, `jericho-north-graves`, `jericho-later-quarry-pits`.
- `marjama-tell`, `marjama-kallai-pool`, `samiya-crypt-basin`, `samiya-hydraulic-system`, `yanun-site`.

Relations: pilot Koḥlit; optional Sekakah only when a bounded source-grounded implementation is feasible. Keep textual interpretations separate from candidate assignments. The modern 1898 reservoir cannot supply an early feature. Kallai's unlocated pool must remain unknown, not a fit or miss.

Inventory: pilot Entry 25 on IV/17, IV/11 and Twin Cave with equal branches. Two mouths, pillar, opening size, orientation and phase are separate predicates. Connectivity is not a mandatory textual criterion. Existing 2D connectivity is no traversal observation. No regional rarity or completeness claim.

States: pilot IV/17 and Jericho north. Observed architecture and reconstructed ancient arrangements are separate. Do not invent north thresholds, sealed wall dates or world coordinates. Keep inaccessible section/plate dependencies explicit.

Coverage: pilot the existing 28-notice Jericho pool inventory and IV/17. Deduplicate physical identity/campaign, report unknown denominators, excavation reach/datum/phase/disturbance separately. No fabricated detection probability or negative-deposit inference.

Decisions: extend the historical measurement queue by importing it without rewriting its statuses. Add finite possible outcomes (including inconclusive), branch consequences, required records, effort/access/status and qualitative priority. Retain Manchester/IAA requests as pending; do not duplicate outreach or restart parked acquisition.
