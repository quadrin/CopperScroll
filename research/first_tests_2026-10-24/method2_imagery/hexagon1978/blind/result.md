# Blind marking of the HEXAGON 1978 Qumran crop — result (24 October 2026)

Rule: [registration.md](registration.md) (SHA-256 34dcbc3bac91479d465a60a063335efeb10231f80f2778c574d38032af299f0b), written before the marker ran.
Marker: a fresh agent that saw only `marker_inputs/` (hashes in `marker_inputs.sha256`). Its marks: [marks.json](marks.json)
(SHA-256 178919e3c283f3d8696e1a3676cca058c3de6a34b790a4832d2e552f1e52a5ea): 56 features, 5 called open basins (class B).
Scoring: `python3 -I score_blind.py marks.json` -> [blind_score.json](blind_score.json).

## Primary (registered Method 2 rule, applied blind)

7 of 8 pools have a mark that meets their outline dilated by 1.5 m: L71, L56/58, L91, L110, L48/49, L117, L118. L138 has none.
4 or more -> **the blind marking confirms the pass for this film.**

## Secondary (registered, descriptive)

Disc of 3 m round each locus label point of Magen & Peleg Fig. 9.

| Marks counted | Pools hit (of 8) | Control rooms hit (of 16) |
|---|---:|---:|
| all marks, conf >= 1 | 7 | 15 |
| all marks, conf >= 2 | 7 | 15 |
| basin calls (class B), conf >= 1 | 5 | 3 |
| basin calls (class B), conf >= 2 | 5 | 3 |

The 3 control hits under class B all come from one mark, the L48/49 basin call, whose box also meets the discs of the
adjoining rooms L51, L52 and L53.

## Exploratory (not registered)

- Each of the 5 basin calls meets a pool outline: L118, L110 (also L117's dilated outline), L91, L48/49, L58.
- 18 of the 51 class-A boxes meet a pool outline. At that rate, 5 of 5 by chance is 0.353^5, about 1 in 190.
- Pools plus 1.5 m cover 12.5 % of the ruin's footprint (convex hull of the Fig. 9 walls north of z = 65 m).

## Reading

The registered rule is met almost everywhere in a dense ruin (15 of 16 rooms), so it shows the film resolves the
buildings. The marker's own basin calls are specific to pools, so deep open pools stand out by their shadows on this
film. Nothing here tests buried pools.
