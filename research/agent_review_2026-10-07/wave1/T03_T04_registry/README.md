# Copper Scroll prediction registry (draft 0.1, 6 October 2026)

This folder preserves the original Copper Scroll (3Q15) prediction registry. Its records and scoring rules are historical preparation material; repository publication does not certify that their observations were unused.

**Current entry-60 work, 8 October UTC / 7 October Los Angeles:** [registry v2](../../wave2/W2B_model_v1/registry_v2_entry60.json) supersedes the entry-60 target ranking for the corrected model and source checks. The dedicated [XII 10 image-reading specification](XII10_IMAGE_READING_PROTOCOL.md) fixes the finite letter alternatives, frame/neighbor authentication, manual decision rules, exposure and lineage audit before further Manchester scans. The [image-reading freeze `fd3f334`](https://github.com/quadrin/CopperScroll/commit/fd3f334ea2a40c0f8e99921ef663f8b126112fe1) supplies the protocol timestamp; no unused image or confirmatory identification is claimed. Reading outcomes stay separate from this registry's archaeological L0–L4/MISS fields. For any future confirmatory use, the AGENTS.md unused-observation/discrimination requirements govern; a later download or report date alone cannot establish an unseen prediction. The instructions below describe the original draft workflow.

## Files

| File | What it is |
|---|---|
| `registry.json` | The registry: `meta` (version, cubit ranges, outcome levels, licence) plus 79 `records` |
| `registry.csv` | The same records, flattened (lists joined with ` \| `) |
| `registry_schema.json` | JSON Schema (draft 2020-12) for one record |
| `registry_hashes.txt` | SHA-256 of each record (canonical JSON, outcome fields excluded) |
| `MANIFEST.sha256` | Current file hashes, including this README and the frozen protocol; original registry data hashes remain unchanged |
| `entry60_readings.csv`, `copy_interpretations.csv`, `kohlit_proposals.csv`, `kohlit_joint_constraints.csv`, `kohlit_context_and_access.csv` | Goal B tables: entry 60 readings, views on "a copy of this document", Koḥlit proposals, joint constraints, rabbinic attestations, the access log |
| `scripts/` | `records_a.py`, `records_b.py`, `records_c.py` (record text), `build_registry.py` (assembly, conversions, coordinates, hashes), `check_conversions.py` (checks that hand-typed metre windows match the computed ones), `make_goalB_tables.py` |
| `downloads/` | Untrusted copies of repo files fetched from GitHub raw (read only) |

The harness blocked a separate REPORT.md for this sub-agent. The findings are in the CSV and JSON files above and in the hand-back message to the coordinator.

Rebuild: `python3 -I scripts/build_registry.py <cs_root> <this_dir> && python3 -I scripts/check_conversions.py registry.json && python3 -I scripts/make_goalB_tables.py <this_dir>`

## Scope

The registry covers every entry whose status in `shared/entries.json` is "best-supported" or whose confidence is "medium". It adds entries 23, 25 and 29 as the task asked, and the Koḥlit entries 4, 11, 15, 16, 19 and 60. That is 35 entries in 79 records. A competing reading or site becomes its own record (a "branch"), so a find cannot be scored for two incompatible readings at once.

## Record schema (main fields)

| Field | Meaning |
|---|---|
| `id` | `P<entry>-<letter>`; entry-60 search targets are `P60-T<rank>` |
| `entry`, `lines`, `milik_item`, `lefkovits_item` | Puech number, column:line, and the Milik and Lefkovits item numbers (from `entry_concordance.csv`) |
| `entry_text_he`, `entry_text_en_project` | Hebrew (Abegg/Bowley/Cook, ETCBC, CC BY-NC 4.0) and the CopperScroll project's English, copied from `shared/entries.json` |
| `branch`, `reading_assumed`, `reading_editions`, `reading_status` | Which reading the prediction assumes, whose reading it is, and how secure it is |
| `place_id`, `site_name`, `anchor_lat`, `anchor_lon`, `anchor_precision` | Copied from `shared/places.json`. **The anchor is the gazetteer point for the site or area, not the predicted feature.** It is `null` when the target is not in the gazetteer; no coordinate was typed by hand |
| `feature_type`, `feature_detail` | The installation predicted |
| `period_requirement` | The same rule for every record: the feature must have existed (built, or standing as an accessible ruin) within c. 50 BCE–70 CE, with an extended window to 135 CE. A feature first built after 135 CE is a period MISS |
| `orientation_constraint`, `location_constraint` | Direction and position constraints under this reading |
| `measures` | Cubit figures with their edition and type (depth, distance, side length), converted at **0.445–0.525 m** per cubit (primary) and 0.40–0.60 m (wide). Both ranges come from the repo's working assumptions (`cycle7/kohlit_pool.md` item 5) and were not derived independently here |
| `confirm`, `miss`, `inconclusive` | Decision rules (see outcome levels) |
| `deposit_expected` | What the entry says was hidden (used only for L4) |
| `report_must_record` | Seven core fields plus record-specific ones. If a report lacks them, the record can only be scored L0 |
| `priority`, `scorability`, `rank`, `rank_scores` | Priority is high, medium or low. Scorability is feature-level, area-level or not scorable at present. Rank and the 0–2 criterion scores apply to entry-60 targets only |
| `evidence[]` | Each item is labelled EVIDENCE, with a source. Most sources are cited second-hand from the repo files ("via …") |
| `inference` | Labelled INFERENCE, with a stated confidence |
| `outcome`, `outcome_level`, `scored_report`, `scored_by`, `scored_date` | Empty. Filled only at scoring time and excluded from the record hash |
| `record_sha256` | SHA-256 of the record's canonical JSON (keys sorted, UTF-8), without the outcome fields |

## Outcome levels and the scoring protocol

- **L0 INCONCLUSIVE.** The criteria cannot be applied.
- **L1 TYPE.** A feature of the right type exists in the period. Many of these are already known, so L1 counts only for a new observation.
- **L2 FEATURE.** The predicted feature is observed and dated, and it meets every constraint of the reading: orientation, relative position and distance. Any rival features must be listed.
- **L3 SPOT.** A cut, cavity or disturbance of the period is documented at the predicted spot or depth. An empty or refilled cavity is consistent with retrieval in antiquity.
- **L4 DEPOSIT.** The kind of deposit the entry lists is found there.
- **MISS.** The record's own MISS rule is met. Each rule states its scope: one feature, or a whole target zone. No single excavation can produce an area-level miss.

Scoring protocol:
1. Two scorers each receive one record and one report. They should not have written the record.
2. Each scorer records the level reached for each branch, citing report pages.
3. The two scores are then reconciled. Any disagreement is published along with the result.
4. A result counts only if the report's observation was made after the registry was timestamped. Known facts listed under `evidence` can never be scored as confirmations.
5. A confirmation on one branch counts against the other branches of the same entry.

## How to timestamp it publicly (not done; for the user to decide)

The aim is to prove that these exact predictions existed before a given report. Any of these methods works, and they can be combined:

1. **Freeze the content.** Rebuild, then record `sha256sum registry.json registry.csv registry_schema.json` (also in `MANIFEST.sha256`). Do not edit a frozen version. Publish corrections as a new version that cites the old hash.
2. **Commit to a public git repository**, for example as `research/registry/` in github.com/quadrin/CopperScroll. Use a signed commit and a signed tag (`git tag -s registry-v0.1`). The commit hash and GitHub's server-side timestamp date the content. The repo already notes that "no confirmatory freeze or unused prediction is claimed" (`research/ACTIVE_TEST.md`), and this registry is meant to supply that freeze.
3. **Archive it.** A Zenodo deposit gets a DOI and a fixed date, and Zenodo can archive a GitHub release automatically. A Software Heritage archive of the repo is another option.
4. **Preregister it on OSF.** Create an OSF preregistration (for example the "Open-Ended Registration" template) and attach `registry.json` and the README. OSF registrations are time-stamped and frozen.
5. **Anchor the hash in a blockchain with OpenTimestamps.** `ots stamp registry.json` produces `registry.json.ots`. Later, `ots upgrade` and then `ots verify registry.json.ots` prove the file existed at that time without revealing anything new. This needs the `opentimestamps-client` package and network access to the public calendars.
6. **Embargoed option.** Publish only the hash list (`registry_hashes.txt`) now, and publish the records later. The hashes prove the content was not changed afterwards. Note that blind scoring by others needs the records to be public.

Any of these steps posts content publicly. They need the user's decision and, for the repo, the maintainer's agreement.

## Limits

- Most archaeological facts come second-hand from the repo's files. Each `evidence` item says which file.
- Measurement type (depth or distance) is disputed in many entries. Records carry both where the editions differ.
- The registry predicts features and spots. It does not predict whether treasure survives. A MISS on a deposit, as opposed to a feature, is never claimed.

