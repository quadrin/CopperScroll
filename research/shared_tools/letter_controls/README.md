# Original-letter control calibration

This module extends the existing [blind-review staging](../README.md#blind-review-and-visit-capture). It audits the catalogue, acquisition metadata, original-photo review and line mappings at pinned main `897733283606988581155a3c1df0cd235cb7bea9`. It does not inspect imagery or acquire another source.

The [XII 10 protocol](../../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md) controls the future reading test. Its complete strings, physical gates and two-human-reader rule remain authoritative. This module adds control qualification, packet preparation and response accounting. Its [result](RESULTS.md) closes the current empirical-accuracy claim as not identifiable.

Run from the repository root:

```sh
python -m unittest discover -s research/shared_tools/letter_controls -p 'test_*.py' -v
python research/shared_tools/letter_controls/letter_controls.py prepare --output research/shared_tools/letter_controls/outputs_next
python research/shared_tools/letter_controls/letter_controls.py score --input research/shared_tools/letter_controls/outputs/synthetic_pilot_input.json --output research/shared_tools/letter_controls/pilot_next.json
```

Preparation refuses to overwrite an existing packet. Outputs contain a view-level eligibility audit and ten randomly ordered metadata slots: a target and a complete local-control-pool requirement at VII 11, IX 7, X 15, X 16 and XII 10. A slot is an acquisition/registration dependency, never an observed control glyph. All image and ROI fields remain empty. `packet/reviewer/` contains anonymous items and response forms; `packet/coordinator/` contains the source key, item-level gaps, selection plan, readiness gates and withheld Stage 2 questions. The seeded order reproduces this exploratory staging; a future final packet requires its own frozen manifest.

An actual control needs authenticated original context, bounded native coordinates, verified original bytes, a physical glyph ID, observational lineage, authorized use, comparability and a complete local comparator inventory. Its certain truth must have an independently adjudicated original-image anchor established before scorer answers. The audit distinguishes exposed observations from demonstrably unused observations. A fresh scan of a known photograph retains its lineage. Existing exposed originals can support exploratory calibration with independently unexposed human readers after the remaining gates pass.

For scoring, provide a JSON object with `mode`, `items`, `readers` and `responses`. The saved synthetic input demonstrates the field structure and labels every fabricated record. An empirical record must replace those simulated qualifications with source-linked audit records; the scorer rejects synthetic items, readers and responses in empirical mode. Each control item has one code per physical glyph, with all its captured views grouped together. The reader record supplies an anonymous ID, documented human/epigraphic qualification and pairwise `independent_of` IDs. Each response supplies the code, reader ID, decision, label when read, grade, Stage 1 lock metadata and item-specific exposure/recognition audit. Keep source-linked qualification evidence with the coordinator; Boolean flags alone supply no external authentication.

The scorer retains abstain and unknown answers in the returned-control denominator, reports answered-only accuracy separately, and preserves missing responses, excluded/recognized controls, confusion matrices and every paired-reader disagreement. Unknown truths supply no accuracy denominator. It rejects duplicate glyph codes, duplicate initial answers and unlocked or Stage 2 answers; preserve revisions separately. Target readings receive no control-accuracy score. Report strata separately before pooling future real samples. No accuracy threshold changes the frozen decisive-letter rule.

The coordinator must deliver only the reviewer folder to readers, keep the truth/source keys outside their accessible package, and freeze original answers before Stage 2. A public repository containing the coordinator preparation key cannot enforce blindness by directory naming alone. No packet has been dispatched and no human reading has been collected here.
