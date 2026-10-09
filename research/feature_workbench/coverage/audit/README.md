# Negative notices and plan registration

This audit applies the useful parts of the AF447 search reconstruction and the Ephesus landscape reconstruction to the already inspected Copper Scroll evidence. It keeps the observation process separate from the location hypothesis: a survey field, excavation exposure and searched ancient target are different records.

The new dataset joins each source-2 absence field to its exact survey entry, coder sheets and frozen Koḥlit result. It imports the existing Jericho and IV/17 target gates without changing them. The registration assessment checks the actual Hyrcania, Qumran and IV/17 records for named geographic controls, independent validation, error bounds and the ancient landscape phase.

Run from the repository root:

```sh
python research/feature_workbench/coverage/audit/audit.py --write
python -m unittest discover -s research/feature_workbench/coverage/audit -p 'test_*.py'
```

`results.json` is generated; `absence_witnesses.csv` is its compact source-instrument crosswalk. `RESULTS.md` explains the result. `input_manifest.json` records the SHA-256 of every input read. Rebuilding never writes a frozen matcher, coder sheet, plan registration or historical result.

The audit uses exposed evidence. A historical field called “full coverage” does not supply the exact northern-sector search footprint or a detection probability. No negative notice becomes an archaeological exclusion without its target, instrument, reach and preservation join. A named old check, a fresh copy of its image and leave-one-out points chosen after fitting are also exposed observations; they cannot become a new independent holdout. Unknown quantities remain null.
