# Proposed additions, 6 November 2026 (not merged into `hoards.csv`)

**What.** Three excavated, dated deposits are missing from the context-and-placement catalogue `hoards.csv` (204 rows, window 200 BCE–135 CE). The side-quest swarm found the gap (card B4-3; review R6: "the omission is explained by timing, not bad coding"). JSP 19 reached Drive on 17 Oct and Amichay et al. 2023 on 13 Oct, both after this catalogue's freeze on 10–12 Oct.

| Proposed id | Deposit | Terminus | Setting / placement | Note |
|---|---|---|---|---|
| `prop2611a` | Mount Gerizim silver hoard: 129 Tyrian coins in a decorated bronze vessel, hidden in the NW wall of building P-II | 120/119 BCE (or 126/125, see note) | structure / wall_cavity | `temple_related` = 1 would be the first in the catalogue: Magen asks whether it is the vessel from the Samaritan temple treasury (JSP 19 p.[44]). |
| `prop2611b` | Mount Gerizim bronze hoard: 61 coins, SE fortress of the sacred precinct | 121/120 BCE | structure / not_stated | — |
| `prop2611c` | Vespasian Coins Cave (U2-007), 7 prutot hidden in a rock crack (L108) | 68/69 CE (tetradrachms on the step below to 69/70) | cave / not_stated | PLAN has no placement code for a rock crack; the position is left blank here (site protection; see the source). |

The rows are in `proposed_additions_2026-11-06.csv`, with the same 48 columns as `hoards.csv`. Only the fields a source states are filled. The derived columns (`context_category`, `coarse_group`, the window and region flags) are left blank for `hoards_full.py` to compute.

**Caveat on `prop2611a` (card B4b-1; review R7).** The hoard's K numbers run K 29807–29936 with one gap, K 29935. K 29935 is Cat. 233, a bronze of Antiochus IV from the same locus and basket (P L4749 B47518), catalogued as an isolated coin. The only coin later than 126/125, Cat. 890 (K 29922), is the sole basis for the 120/119 closing date. If it is intrusive, the hoard closes 126/125, as JSP 8 (2008) had it.

**Decision for the owner (not taken here).** Whether to add these rows under the frozen PLAN coding and re-run the main comparison. A re-run after seeing these deposits is a new exploratory model (AGENTS.md). The frozen result (D = 0.68) stands as recorded.
