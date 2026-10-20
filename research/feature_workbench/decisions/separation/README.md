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

12 October integration: acquisition statuses are refreshed from the canonical queue (Manchester’s limited TPA file, the sent L-656 request and Rachel Bar-Nathan’s reported records). Input links now address exact Git blobs, with SHA-256 content pins and the historical baseline retained separately, so refreshed records cannot be mislabelled as bytes from the old baseline. No predicted observation or separation rule changed.

19 October 2026: Kallai 1972 pp. 172–173 put Kallai's pool west of the Marjama tell ([decision record](../README.md#kallai-outcome-recorded-19-october-2026)). The saved `prediction_sets.json` and `results.json` stay the 12 October run; they were not rerun. On the current inputs the relationship evaluator excludes 20 branches (adding `samiya-kallai` and `yanun-marjama-anchor`), and 20 hypotheses in 10 families form 4 classes under this observation menu. The tests check the current inputs.
