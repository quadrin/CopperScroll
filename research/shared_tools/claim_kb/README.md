# Local claim pilot

This pilot joins reviewed project records without changing their scientific assessments. It extends the shared-tools CLI, HTTP server and SQLite cache. It uses Python 3.10+ and the standard library; it needs no account, external service or running atlas.

From the repository root:

```sh
python3 research/shared_tools/cli.py kb build
python3 research/shared_tools/cli.py kb validate
python3 research/shared_tools/cli.py serve
```

Open `http://127.0.0.1:8765/kb`. Select an entry, candidate assignment and branch. Click a result or requirement to inspect its evidence, assumptions and exact source locators. The name view separates composition, physical-witness and described-period dates. The impact view previews a changed input without changing evidence. Atlas links open the existing historical-state view; the pilot creates no geographic overlay.

The original source-search index can still use `cli.py build`. Its rebuild preserves the pilot's `kb_*` tables in `research/shared_tools/cache/evidence.sqlite`. A fresh pilot can run `kb build` alone. Generated databases, JSON snapshots, query demonstrations and exports remain in the existing ignored cache. Retain the SQLite file if you need local revision history; a new checkout reproduces the current graph from version-controlled inputs. Git retains earlier canonical research records.

Design and maintenance decisions are in [DICTIONARY.md](DICTIONARY.md). [MIGRATION.md](MIGRATION.md) maps authoritative inputs, preserved identifiers and gaps. The formal transport definition is [schema.json](schema.json). [schema.svg](schema.svg) and [schema.png](schema.png) show the six groups and an actual evidence chain. Edit `diagram.py` to regenerate SVG, or edit `schema.mmd` for the Mermaid version.

## Query demonstrations

```sh
python3 research/shared_tools/cli.py kb demo --output research/shared_tools/cache/kb-demo.json
python3 research/shared_tools/cli.py kb query 1 --id reading/e60-janoah:4
python3 research/shared_tools/cli.py kb query 2
python3 research/shared_tools/cli.py kb query 3 --id iv17
python3 research/shared_tools/cli.py kb query 4
python3 research/shared_tools/cli.py kb query 5
python3 research/shared_tools/cli.py kb query 6 --id claim/relationships-quarries-later-phase
python3 research/shared_tools/cli.py kb query 7
python3 research/shared_tools/cli.py kb query 8
python3 research/shared_tools/cli.py kb claim claim/relationships-modern-reservoir-chronology
python3 research/shared_tools/cli.py kb entry 25
python3 research/shared_tools/cli.py kb names
```

1. The Janoaḥ reading reaches four `RB-L` conclusions: two named assignments across two saved windows. Other retained reading branches stay separate.
2. Four source/analysis records report or reuse the same Sion Plan 5 observation. They remain one original drawing lineage. Individual endpoint measurements and other observations within the campaign keep their IDs.
3. Each candidate exposes its requirement checks under every materialized branch. IV/17, IV/11 and Twin Cave retain the same workbench opportunities. The regional comparison also retains XII/53 and the Jones North control under its separate rulesets. Regional and workbench coding disagreements remain visible.
4. No imported candidate arrangement establishes instruction-period coexistence. Kenyon's later quarrying contradicts same-phase construction; it leaves later joint accessibility unresolved. State-query results preserve this distinction.
5. `T05-062` records no external ʿAṣla match within its stated search. Queries, corpus descriptions, inspection scope, homograph cautions and incomplete name-specific coverage accompany it.
6. Changing the quarry/grave dating claim reaches the dependent chronology/accessibility assessments and the original phase diagnostic. Input-file changes also cause query refusal until rebuilding, with persistent reassessment flags for affected evidence-derived results.
7. Exact image, pool, section, threshold and phase targets retain their possible consequences. The saved minimum-separation planner stays historical: its named Koḥlit dependencies do not fully distinguish its surviving model classes. No possible outcome becomes an observation.
8. Uninspected Kallai pages, Kenyon drawings and field files remain separate from already inspected reports that lack the needed observation. Partial-inspection qualifications and exact locators travel with the answers.

`Queries` in `queries.py` exposes these operations as pure Python functions over an exported graph. Outputs retain typed record IDs, locators, branch/window conditions and unknowns. [MCP.md](MCP.md) describes a later read-only wrapper.

## Input changes and review

```sh
python3 research/shared_tools/cli.py kb changes
python3 research/shared_tools/cli.py kb history claim/relationships-modern-reservoir-chronology
python3 research/shared_tools/cli.py kb build
```

`store.load()` compares hashes of allowlisted inputs and builder/schema files. A mismatch blocks ordinary derived queries. `kb changes` explains affected records; `kb history` retains old record values and input hashes. `kb claim ID --snapshot HASH` reads a labelled historical version even when its input files have changed. A build appends a content-addressed snapshot and recomputes selected existing evaluators. It never silently treats changed source prose as a reviewed new observation.

Evidence changes set a separate `payload.reassessment.required` flag. Repeated builds preserve that flag. After reviewing and updating the canonical evidence, a maintainer may record an explicit acknowledgment in `reviewed.json`:

```json
{"reassessment_reviews": [{
  "evaluation_key": "evaluation/EXACT-ID",
  "reviewer": "analyst identifier",
  "note": "Exact canonical correction reviewed; scope and consequence",
  "input_hashes": {"changed/source/path": "current SHA-256"}
}]}
```

List every changed input named by that evaluation's reassessment. This acknowledges a reviewed software/evidence dependency; it supplies no independent confirmation or identification confidence. Frozen tests require their existing exposure and reopening procedures before any reserved observation is opened.

## Verification

```sh
python3 -m unittest discover -s research/shared_tools/tests -v
python3 -m unittest discover -s research/feature_workbench/relationships -p 'test_*.py'
python3 -m unittest discover -s research/feature_workbench/inventory -p 'test_*.py'
python3 -m unittest discover -s research/feature_workbench/states -p 'test_*.py'
python3 research/shared_tools/cli.py kb build
python3 research/shared_tools/cli.py kb validate
```

The tests mutate records to exercise duplicate IDs, broken references, missing locators/lineages, alias merges, flattened branches, unknown-as-absent scoring, reused publications, incompatible states, geographic precision, switched assignments, stale inputs and unauthorized views. They also verify snapshot retention through source-index rebuilds and rollback on validation failure.

To regenerate the schematic:

```sh
python3 research/shared_tools/claim_kb/diagram.py
```

The SVG is the deterministic standalone rendering. The included PNG was rendered from it with `sharp`; PNG regeneration is optional and does not affect the pilot. Browser rendering needs a locally installed browser. The checked runtime had no Chromium executable; JavaScript syntax and HTTP/API behavior were checked separately.


## Atlas publication

The atlas homepage renders a public metadata projection of this pilot. Generate it with `PYTHONPATH=research/shared_tools python3 -m claim_kb.web_export` from the repository root; `--check` verifies freshness without writing. The exporter validates canonical records, applies the existing exposure filter, then creates entry indexes. It reads no source assets or private correspondence. `atlas/app/atlas-kb.json` remains generated and must not be maintained separately. The public view exposes graph traversal, branch requirements, chronology, source coverage and impact paths, while the local SQLite store retains historical snapshots and review flags. See the [atlas guide](../../../atlas/README.md#knowledge-base-landing-page).
