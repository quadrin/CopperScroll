# Shared research tools

These tools apply across the project's entries. They import existing source records and preserve their inspection, uncertainty and exposure limits. The initial adapters originated at main commit `26871df2e5e673f590b6fdf031489791dd88c38b`. Source-index links now pin the checked-out commit at build time; build from a committed checkout. Without Git, links fall back to that original snapshot.

## Run

From the repository root, using Python 3.10 or later with SQLite FTS5:

```sh
python research/shared_tools/cli.py build
python research/shared_tools/cli.py serve
```

Open `http://127.0.0.1:8765`. The read-only interface has sources, photographs, entry packets, controls and benchmark views. It makes no external requests. Original source links open on demand.

The CLI exposes the same records:

```sh
python research/shared_tools/cli.py search 'L-656' --kind note
python research/shared_tools/cli.py search 'Plan1' --kind figure
python research/shared_tools/cli.py map --line 'VII 11' --substrate original
python research/shared_tools/cli.py map --cut 21
python research/shared_tools/cli.py entry 12a
python research/shared_tools/cli.py controls
python research/shared_tools/cli.py benchmark
```

## Source retrieval

The local SQLite index searches project notes, catalogue rows and structured figure/page metadata. A result retains its source path, source-line or JSON-pointer identity, and original-asset path where recorded. Printed pages and one-based PDF pages remain separate; the builder never estimates an offset. For example, the Siloam Plan 1 record links printed 74* to PDF 5 and its archived original.

Search normalizes accents and Hebrew vocalization. Displayed snippets identify that normalization; follow the source for exact spellings. Query input is literal text, rather than an SQL or FTS expression. Source and builder hashes reject stale indexes; separate dependency hashes protect the manuscript, entry and control caches. Atlas mirrors are excluded; documentary records retain separate provenance even when they refer to the same underlying observation.

`build --ocr` also indexes existing local `.txt` files. The default index imports metadata and notes. Original PDFs, restricted images and OCR remain in their existing locations. Generated databases and exports stay outside Git through this directory's `.gitignore`. A search hit establishes retrieval, with inspection scope inherited from its record.

## Manuscript correspondence

The adapter joins the USC catalogue to both acquisition manifests by identifier, retaining original/replica distinction, catalogued cut/column, lighting labels, asset dimensions and hashes. Acquisition checks are imported as recorded metadata. The adapter performs no new image inspection.

`mapping_claims.json` adds source-linked locus queries. Each records an edition scaffold, physical scaffold, provisional association or unregistered target. Every original target ROI and neighboring-original-Hebrew field is currently null. Column-II cut-5 damage anchors remain distinct from the provisional cut-6 Greek-group transfer. Conflicting column-IX/X cut proposals retain their alternatives. A catalogue cut number never authenticates a Hebrew line; rotation never becomes an illumination angle or depth calibration.

This gives complete catalogue coverage and a partial, explicitly unverified line correspondence. Completing original line registration requires the labeled composite/component maps or newly usable original images identified in the existing research. Closed preview passes retain their stopping rules.

## Entry and control inputs

The entry adapter imports all canonical concordance slots, their project translation context, edition alternatives, global alternatives and existing reviewed constraint records. Shared boundary lines remain marked as context. Complete formal predicate extraction remains pending editorial review; absent origins and ancient reference surfaces stay null. These packets provide a consistent starting point for that review.

The control adapter imports the workbench's cave records, physical-feature register and observations, alongside the Jericho documentary notices and their source records. Notices remain notices. Regional denominator and coverage completeness stay unknown. It reuses existing control observations; a new uniformly measured regional sample remains an evidence dependency.

## Calibration results

The [saved diagnostics](results.json) contain four synthetic affine-transform checks with a fourth control withheld from fitting, plus a deliberately wrong held-out control. They test scale, rotation, reflection, shear and rejection of a failed control. Collinear, nonfinite and Boolean coordinate inputs are rejected.

The exposed-plan diagnostic independently recomputes the frozen IV/17 point distances: approximately 0.858630 m and 1.164143 m. Both reproduce the stored computations. The northern chord differs from the published 0.8 m opening width by approximately 0.058630 m; those quantities have different definitions and an unquantified total error. This supplies no ancient threshold, true bearing or identification support.

The Hyrcania diagnostic reproduces the local transform for the existing failed registration. Its source records a 244.371 m residual at the exposed check and rejects precise feature placement. The adapter preserves that failure; it does not rerun the geodetic conversion or certify an unused observation.

Independent empirical accuracy and human letter-reading accuracy remain untested. Those evaluations need independently established answers, appropriate controls and a record of which observations were reserved before testing. Synthetic holdouts are computational fixtures.

The [published-dimension pilot](plan_pilot/RESULTS.md) now checks newly selected scale-bar chords against three excavation reports. Prediction inputs exclude the prose reference values; input hashes and recomputation reject stale saved results. The analyst saw the references before selecting points, and independent field-reference provenance is unverified. Both measurable primary chords exceed the chosen screening budget; the third plan lacks a reliable second boundary and remains unmeasurable. This supplies documentary agreement errors, with source/datum uncertainty preserved.

Reproduce the staged computation:

```sh
python research/shared_tools/plan_benchmark.py predict research/shared_tools/plan_pilot/measurements.json --protocol research/shared_tools/plan_pilot/PROTOCOL.md --output research/shared_tools/cache/pilot-predictions.json
python research/shared_tools/plan_benchmark.py grade research/shared_tools/cache/pilot-predictions.json research/shared_tools/plan_pilot/references.json --output research/shared_tools/cache/pilot-results.json
python research/shared_tools/cli.py benchmark
```

## Blind review and visit capture

Prepare local packets:

```sh
python research/shared_tools/cli.py review --output research/shared_tools/exports/review01
python research/shared_tools/cli.py capture --output research/shared_tools/exports/visit01
python research/shared_tools/cli.py capture --validate research/shared_tools/exports/visit01/capture.csv
```

The review export separates anonymous reviewer item codes and a response form from a coordinator-only source key. It is a metadata staging packet. Images, verified crops, legible original-letter controls and independent readers are required before dispatch. It contains no new reading votes, sends no invitations and reopens no stopped test.

The capture form records document/object identifiers, custodian, printed/PDF page, figure, view, lighting, rotation, scale, north convention, coordinate frame, phase basis, derivation and reuse terms. Validation computes local-file hashes, detects duplicates/hash mismatches/path escapes and keeps unrecorded information unknown. Complete capture metadata supplies neither depth calibration nor an ancient phase.

## Verification

```sh
python -m unittest discover -s research/shared_tools/tests -v
python research/shared_tools/cli.py build
```

Tests cover locator ambiguity, Unicode retrieval, stale input rejection, original/replica separation, unresolved mappings, shared entry boundaries, missing control observations, transformation errors and capture/review separation. The five interface API routes and JavaScript syntax were checked. Browser rendering remains unverified because Chromium is unavailable in this runtime.

Next evidence remains in [ACTIVE_TEST](../ACTIVE_TEST.md). These tools support retrieval and preparation across lanes; each closed scientific test retains its recorded reopening condition.
