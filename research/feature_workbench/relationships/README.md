# Landmark relationships pilot

`evaluate.py` resolves textual roles to named feature assignments, then evaluates
each permitted reading and date window from `model.json`. It exposes every saved
combination, its required predicates, source pointers and observation IDs to the
shared workbench. Run it from the repository root:

```sh
python research/feature_workbench/relationships/evaluate.py
python -m unittest discover -s research/feature_workbench/relationships -p 'test_*.py'
```

The pilot compares Entry 11’s pool east of Koḥlit with Entry 60’s northern pit and
separate opening/tomb readings. The 50 BCE–70 CE and extended 50 BCE–135 CE windows
come from the existing exploratory registry. These are project windows, not dates
established by the Scroll or by this implementation. A date is tested only when
construction or accessible use is actually constrained; an undated older feature
does not receive an invented survival date.

Eight explicit assignments produce 40 permitted combinations. Twelve fail a
specific assigned-feature requirement: the present reservoir was built in 1898,
or the named crypt-basin/spring crosswalk is west/southwest of the Marjama tell.
The other 28 remain unknown. These failures do not exclude every pool at either
site. The historical irregular basin and modern reservoir remain distinct;
Kallai’s unlocated pool remains unknown. NS1, D9 and the north-slope quarry pits
retain separate identities. A burial at D9’s shaft base does not establish tombs
at a pit mouth.

The quarry/grave diagnostic separately rejects same-phase construction: Kenyon’s
later pits truncate earlier graves. That relative order does not by itself reject
later jointly accessible mouths during an early use window. The pit dates and
mouth layout remain unresolved. Kenyon II and III belong to the same excavation
lineage and add no numerical confidence.

Direction predicates use attributed qualitative source relations or explicitly
marked inference. They generate no surveyed bearings, metric tolerances, outlines
or coordinates. Opening direction, concealment, ancient basin corner and dated
pit-mouth/tomb-mouth joins are unobserved here. Missing roles stay unknown. The
saved Janoaḥ route keeps the absent Yanun pit separate from its hypothetical
Koḥlit anchor.

Restored Entry 15/16 links and Entry 19’s eastern-pit comparison are recorded in
`data.supplementary_graph` as unresolved dependencies. NS1 is not assigned to the
great cistern with its pillar; Entry 16’s restored destination is not equated to
Entry 11’s pool. The no-place-name Entry 19 alternative and other Koḥlit regional
proposals remain outside this selected pilot; no regional completeness or rarity
claim follows.

All archaeological inputs were already exposed before this work. Re-running the
evaluator adds no source inspection, holdout, identification or deposit result.
To extend it, add a reviewed named feature and its source-controlled observations,
declare the permitted assignments/readings, and preserve earlier misses. A
confirmatory test requires its own frozen specification and demonstrably unused
observation under the repository’s AGENTS.md rules.
