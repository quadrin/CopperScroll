# M06: cubit and datum sensitivity

Parent question: R08. Prepared 2 October 2026 (UTC); 1 October in Los Angeles.

Target: separate unit uncertainty from the uncertainty in the origin, direction and ancient surface of a measurement.

Inputs: project translation at baseline `bb2fde4c76dbbe34b4c7345646acee049e875229`, entry 11 / II 13–15 (four cubits), entry 25 / VI 1–6 (three), entry 26 / VI 7–10 (nine). These quantities are conditional on those translation choices. Entry 11 has an editorial measurement disagreement; retain its Text-tab alternatives before interpreting a site test. This packet does not settle any edition disagreement.

Method: sample 0.40–0.60 m per cubit at 0.01 m increments. Keep an unknown datum as null. Record each future source's reference surface, measured axis, architectural phase and uncertainty independently. A surface-displacement interval must come from a cited section/context; do not assign a guessed ancient-floor elevation.

Reproduce with `python unit_sensitivity.py`. Output: `unit_sensitivity.json`. Decimal arithmetic yields conditional ranges of 1.60–2.40 m for entry 11, 1.20–1.80 m for entry 25 and 3.60–5.40 m for entry 26.

Pilot status: arithmetic completed; archaeological datum and axis await evidence. These ranges repeat existing exploratory conversions and add no source inspection or candidate test.

Completion criterion: a named feature has a cited ancient datum and measurement axis; its observed span and uncertainty can then be compared with each viable textual quantity and unit range. Until then, retain conditional distances and an unresolved feature comparison. Keep geographic geometry unchanged.
