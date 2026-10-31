# Novel lines of evidence, 30 October 2026: index of six parallel runs

On 30 October 2026, six workers each opened one Tier 1 direction from the session prompt "open a genuinely new line of evidence". They worked at the same time. Each direction has its own branch, its own folder `research/novel_2026-10-30/<direction>/` and its own `NOTE_2026-10-30.md`. Each worker committed and pushed a frozen protocol (SHA-256 in the commit message) before its confirmatory run. The orchestrator did these checks on each branch:

- The protocol hash agrees with the hash in the commit.
- The protocol file did not change after the freeze commit.
- No image product is in the repository.

No run changed a rating, the outcome ledger, ACTIVE_TEST or the atlas data.

| Dir. | Branch (final commit) | Frozen SHA-256 (commit) | New dataset | Result |
|---|---|---|---|---|
| A. Photometric stereo on the 1988 multi-light frames | `claude/novel-2026-10-30-A` (f4b2765f) | 130de878… (9b1860fb) | Per-cut normal and depth maps (private, outside the repo); `relief_features_controls.csv`; `confirmatory_result.json` | **Not obtained.** ח/ת rule on held-out controls: 1 of 8 correct (1 of 7 under the frozen count), p = 0.996. No target was scored. |
| B. Analysis by synthesis | `claude/novel-2026-10-30-B` (bd06dcc6) | 2ec4b4da… (66e87413) | `calibration_rankings.csv` (72 rows); `target_rankings.csv` = NOT RUN | **Not obtained** for the test: true reading ranked first on 4 of 13 held-out lines (2.4 expected), p = 0.21, pass mark 6. Targets (XII 10, IX 10 and others) were not scored. The worker reports "partly" because the first rendering pipeline now exists. |
| C. Engraver hand | `claude/novel-2026-10-30-C` (39774863) | 505d5681… (7958efe4) | `out/hand_features_by_column.csv` (12 columns), `out/hand_features_by_line.csv` (181 lines) | **Not obtained.** The drawn letter proportions change at III 6–8 and XI 7–8 (p = 0.0034), each 10 lines after a seam, so not within ±3 lines of the seams S11 (II 12–13) or S49 (X 14–15). The change is in Puech's drawing; the previews cannot show whether it is on the copper. |
| D. Vorlage (ink exemplar) copying errors | `claude/novel-2026-10-30-D` (e4060122) | 5198777b… (8f8f5610) | `data/vorlage_confusion_matrix.csv` (231 pairs), `data/emendations_frozen.csv`, `results/gazetteer_hits.csv` | **Not obtained.** Vorlage emendations 162 hits, edition-confusion control 173, uniform control mean 145. The excess over chance comes from the matchers, not the model. |
| E. HEXAGON 1974 stereo | none | none | none | **Blocked, not started.** The 4.6 GB archives are only in Drive (`06 Imagery/HEXAGON 1974-06-25/D3C1208-400636*.tgz`, `HEXAGON 1974-12-01/D3C1209-200214*.tgz`). The Drive connector returns base64 only; USGS EarthExplorer needs a login. |
| F. Terrain-derived denominator | `claude/novel-2026-10-30-F` (679163bf) | 0b330036… (16e1e175) | `out/predicate_counts.csv` (280 rows: 4 regions × 12 predicates × low / central / high) and a GeoJSON of 547 candidate points | **Partly.** The cliff/cave-host count is stable and resolved: 64.9 % of 359 recorded caves are within 60 m of a cliff cell, against 11.5 % by chance. The channel words (נחל, שולי, צוק) are not resolved at 30 m. Koḥlit k = 0 of 333 stays "not measurable": 93 % of units can host a pool to the east, against 94 % of the landscape. |
| G. Logistics simulation | `claude/novel-2026-10-30-G` (ad939e61) | 8e6bf1b2… (acfcc7fc) | `out/feasibility_envelope.csv` (1,944 rows), `out/sensitivity_indices.csv` | **Not obtained.** The talent reading is unaffected: the reading explains 1.6 % of effort variance, and transport mode explains 72 %. Only constraint: a region-wide deposit that starts at the Temple must be done before June 68 CE (Vespasian at Jericho). |

## Common limit

Directions A, B and C used the USC Digital Library public previews of the 1988 photographs (about 1000 px; 20–30 px per letter height). The private WSRP 1988 TIFFs (Drive `06 Imagery/3Q15 Copper Scroll Zuckerman USC`, 93 files, 28–58 MB) were not reachable from the compute container. The encrypted 1/4-scale copies in `private-media/wsrp-1988/` need the `WSRP_MEDIA_KEY` secret. A, B and C each name this resolution as the probable cause of failure.

## Reopening conditions (stated by the workers)

- **A, B, C:** a new frozen specification on the full-resolution WSRP TIFFs in a compute environment that can read them (for example the Colab runner that mounts Drive).
- **D:** a semi-cursive confusion model built from the scroll's own ו/ר and נ/ר corrections, tested against a fresh gazetteer.
- **F:** the channel predicates with a finer open elevation model, or a dam-calibrated threshold run as a new labelled model.
- **G:** no second AI-only session. The remaining discriminator (load for each entry against cavity size) needs measured cavity dimensions.
