# Feature recovery benchmark

Run the exposed source-record pilot and tests from the repository root:

```sh
python research/shared_tools/recovery_benchmark/benchmark.py run
python -m unittest discover -s research/shared_tools/recovery_benchmark/tests -v
```

The [result](RESULTS.md), [source-grounded factual cases](source_grounded_cases.json), [decision protocol](PROTOCOL.md) and [reserved-batch protocol](RESERVED_BATCH.md) preserve the scientific scope. Generated [predictions](outputs/predictions.json), [grades](outputs/results.json), [anonymous reviewer inputs](outputs/packets/reviewer/packet.json), [coordinator key](outputs/packets/coordinator/answer_key.json) and [freeze hashes](outputs/packets/coordinator/freeze_manifest.json) are reproducible.

Run prediction and grading as separate programs:

```sh
python research/shared_tools/recovery_benchmark/benchmark.py predict --packet research/shared_tools/recovery_benchmark/outputs/packets/reviewer/packet.json --output research/shared_tools/recovery_benchmark/outputs/predictions.json
python research/shared_tools/recovery_benchmark/benchmark.py grade --packet research/shared_tools/recovery_benchmark/outputs/packets/reviewer/packet.json --predictions research/shared_tools/recovery_benchmark/outputs/predictions.json --key research/shared_tools/recovery_benchmark/outputs/packets/coordinator/answer_key.json --output research/shared_tools/recovery_benchmark/outputs/results.json
```

The grader reads the key's adjacent freeze manifest. This pilot's open source key supplies software and distribution separation; the analyst already knows these answers. A real reserved batch requires a distinct curator and inaccessible truth until prediction freeze.

[PR31 reproduction](outputs/pr31_reproduction.json) preserves its source commit and retrieved-file hashes. That result uses PR31's original program and selections; it adds no point measurements and makes no branch changes. Original image/caption manifests remain in [PR31's source archive](https://github.com/quadrin/CopperScroll/blob/7504f1f42014a745e1df044abc86d2bba0b90e42/research/assets/plans/published-dimension-pilot/figure_manifest.json). No source raster was newly inspected or redistributed.
