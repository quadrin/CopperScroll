# Possible read-only MCP wrapper

Defer installation, authentication and deployment. A later local stdio wrapper can call the same `store.load()`, `public_view()` and `Queries` functions. It should expose bounded JSON results rather than arbitrary SQL, filesystem access or source retrieval.

Suggested tools:

- `get_entry(entry_id)` → `Queries.entry`.
- `get_claim(record_key, snapshot?)` → evidence chain and assumptions. Historical access must label its snapshot/currentness.
- `reading_dependents(record_key)` → `Queries.impact`.
- `candidate_requirements(hypothesis_id)` → `Queries.candidate`.
- `shared_observations()` → `Queries.same_observation`.
- `coexistence()` → `Queries.coexistence`.
- `name_chronology()` and `unmatched_names()` → chronology and bounded searches.
- `acquisition_targets()` → exact additional-observation targets and conditional consequences.
- `uninspected_sources()` → source-inspection gaps and affected conclusions.
- `changed_inputs()` → `store.changes`; stale caches must never masquerade as current answers.

Every response should carry snapshot ID, base commit, freshness, typed record IDs, locators and branch conditions. Apply the same public dependency filter to every tool, including historical queries. Limit result size/paginate by stable ID without omitting the existence of further retained branches. A missing record or protected dependency should return an unavailable result, without disclosing hidden content.

Do not expose ingestion, source opening, image bytes, correspondence, evidence mutation, confidence scoring, purchasing, sharing changes or test reopening. Build/review remains an explicit local maintainer operation using version-controlled reviewed inputs and existing exposure rules.
