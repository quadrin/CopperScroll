# Repeated text constraints

This adds a source-anchored concordance of recurring clause vocabulary and an independent finite constraint evaluator. It applies the useful part of the Linear B comparison: a proposed reading or relation must work in each relevant context, while alternative parses and unresolved arguments remain visible.

From the repository root:

```sh
python research/shared_tools/text_constraints/concordance.py
python -m unittest discover -s research/shared_tools/text_constraints -p 'test_*.py' -v
```

`concordance.py --output /absolute/path/results.json` can write a separate export. The default [results.json](results.json) records source hashes, the corpus inventory, alternative parses with their existing reading provenance, and every evaluated assignment/reading/window row. [RESULTS.md](RESULTS.md) explains the findings.

The source text is `data/scroll-text.js`, the repository's ETCBC dss 2.0.1 transcription and morphology by Martin G. Abegg Jr., James E. Bowley and Edward M. Cook, converted by Jarod Jacobs, Martijn Naaijer and Dirk Roorda, under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). The project display conversion is documented in `tools/build_scroll_text.py`. This analysis removes vowel points for matching, retains homonym IDs, and adds word anchors and analytical family labels. It does not change the transcription. Project translation and reading records supply context; they are not original-metal observations.

Each lexical occurrence retains its JSON pointer, line, word index, encoded segments, morphology, text-critical flags and applicable project variant records. A lexical trigger is distinct from a bound predicate. Shared boundary lines retain both canonical owners. Bigram matching follows adjacent encoded words, permits a line break within the same entry, and cannot bridge a word with missing morphology or cross an entry boundary. It keeps prefixes rather than treating a normalized string as a grammatical parse.

[parses.json](parses.json) records selected recurring relations and their alternatives from existing reading summaries. It also lists unproved feature aliases. These are exploratory analytical labels awaiting editorial review. Where readings differ, the file retains their wording, citation and scope; it creates no reconstructed edition. The corpus is a single transcription, so different editors do not become independent witness counts.

The evaluator imports the existing relationship model's finite assignments, permitted reading IDs, windows and observations. It joins observations by exact subject, relation and reference object. Missing evidence stays unknown. Conflicting assertions stay unknown and are marked. A secure construction bound outside a window can contradict accessibility; first documentation and typological estimates cannot establish ancient construction. Duplicate records add no score or confidence. Only a contradicted required predicate removes a row; each such contradiction is saved with its observation and source IDs.

The retained domain lists are projections for inspection. Their Cartesian product is not the permitted roster: use the retained full rows to preserve assignment/reading correlations. The separate parse and alias alternatives remain factored, without invented probabilities or assumed equality. All inputs were previously exposed. This is exploratory corpus analysis and a reproducibility check, with no independent prediction or feature identification.
