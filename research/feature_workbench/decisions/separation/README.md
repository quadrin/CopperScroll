# Logical separation planner

Run from the repository root:

```sh
python research/feature_workbench/decisions/separation/planner.py --write
python -m unittest discover -s research/feature_workbench/decisions/separation -p 'test_*.py'
python research/feature_workbench/decisions/separation/planner.py --domain xii10-letters --observation xii10-medial --outcome ינ
python research/feature_workbench/decisions/separation/planner.py --domain xii10-letters --observation xii10-medial --outcome נ,ינ
python research/feature_workbench/decisions/separation/planner.py --domain kohlit-relationships --observation quarry-graves-at-mouth --outcome unresolved
```

`--write` writes only this directory's `prediction_sets.json` and `results.json`. An outcome argument previews a scalar or comma-separated ambiguous outcome set and prints **Possible outcome — not observed**. `unresolved` retains every original branch. `other` in a decisive reading component can reject the finite registered strings. Queue evidence, request status and closed results remain untouched.

The Python API is `run(repo_root: pathlib.Path) -> (results: dict, prediction_sets: dict)`. `analyze(domain: dict, dependencies: list[dict], scenario: str) -> dict` accepts `available_now`, `named_dependencies` or `all_planning`. `survivors(domain: dict, observation_id: str, outcome: str | list[str]) -> list[str]` previews compatible original branch IDs.

Prediction `None` means unknown and permits all decisive outcomes; an explicit list must be a nonempty subset of the observation universe. Hypotheses sharing `family_id` retain their nuisance branches jointly; families with identical joint observable signatures collapse. Pair counts measure finite logical capability and never probability or confidence. Independent queue claims remain separate domains rather than becoming mutually exclusive site predictions.

See [RESULTS.md](RESULTS.md) for the run, acquisition limits and consequences.
