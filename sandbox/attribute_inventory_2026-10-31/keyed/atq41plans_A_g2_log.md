# Plan pass, reader A, group g2: log

- Source: *ʿAtiqot* 41 part 1 (Hebrew), articles 2543 (Sion, Regions IV and VI, 42 pp.) and 2545 (Feig, Cave IV/11, 7 pp.).
- Started 2026-10-31T23:47:20Z; finished 2026-11-01T00:28Z (UTC).
- Files read: PLAN_PASS.md, SCHEMA.md, and the two article PDFs, rendered with `render_iss1.py`. No other project files were opened. Article text was not used for any value.

## Pages looked at

Every page of both articles was rendered at 70 dpi and checked on contact sheets:

- 2543 pp. 1-42. Plans on pp. 4, 6, 13, 18, 21, 29, 31 and 34 (plans 1-8). P. 2 is a regional map (Map IV-VI), not a cave plan, so it was not keyed. The other pages hold text, photographs, coin, vessel and object drawings, and tables. That includes the hinted pp. 5, 17, 28, 30 and 40, which mention plans in their text but print none. P. 29 also has an object drawing (fig. 22, a buckle), not a plan.
- 2545 pp. 1-7. One plan, on p. 2 (plan 1). The other pages hold text, photographs, finds and references.

The plan pages were then rendered at 300 dpi and cropped. P. 4 was also rendered at 200 and 400 dpi. Measurements were taken on the 300 dpi renders with pixel profiles.

## Plans found (9 plans, 9 cave rows)

| plan_ref | page | caption | key |
|---|---|---|---|
| 2543:1 | 4 | תוכנית 1. תוכנית סכמתית של מערה IV/1 (schematic) | IV/1 |
| 2543:2 | 6 | תוכנית 2. מחסה סלע IV/2: תוכנית וחתך (rock shelter, plan and section) | IV/2 |
| 2543:3 | 13 | תוכנית 3. מערה IV/7: תוכנית וחתך | IV/7 |
| 2543:4 | 18 | תוכנית 4. מערה IV/8 | IV/8 |
| 2543:5 | 21 | תוכנית 5. מערה IV/17 | IV/17 |
| 2543:6 | 29 | תוכנית 6. מערה VI/43 | VI/43 |
| 2543:7 | 31 | תוכנית 7. מערה VI/46 | VI/46 |
| 2543:8 | 34 | תוכנית 8. מערה VI/52 | VI/52 |
| 2545:1 | 2 | תוכנית 1. מערה IV/11 | IV/11 |

All nine plans have a north arrow and a scale bar (2, 3, 4 or 5 m).

## Conventions I applied (the same for every plan)

- **North arrow tip.** In every arrow, the half-filled head narrows to the tip, and a thin shaft runs on past the broad base. Plan 3 (IV/7) is the exception in direction: its arrow points to the bottom of the page.
- **Opening gap.** The gap is the shortest segment between the two sides of the outline at the mouth. Its length is the opening width, and the outward perpendicular to it gives the direction.
- **Direction and width.** The true bearing is the page bearing minus the arrow's page bearing. A `/` value is used within 10° of a sector boundary. Where the gap could not be defined, the direction or width is `unknown`.
- **Built walls.** A built wall in a mouth counts as part of the outline. In IV/2 the opening is the gap left beside the wall. In IV/7 the wall fills the whole rock mouth; that mouth is still counted as one opening, with a note.
- **Pillars.** A detached cross-hatched rock mass counts as a pillar or pier. In IV/1 and IV/17, the pier is the mass that separates the two openings.
- **Steps.** None of the plans draws tread lines, so steps are `0` everywhere. Ticked edges, which mark level changes or cliff edges, are described in `other_features` instead.
- **Sizes.** Sizes are given for single-space caves. For the multi-space complexes VI/43 and VI/52 they are left blank, and the overall extents go in the notes.

## Unclear or partly readable

- **2543:6 (VI/43), confidence low.**
  - Four entrances are labelled on the plan.
  - Entrance I has no clear gap, so its direction and width are `unknown`.
  - Entrances II and III are narrow slots, about 0.2-0.3 m where they meet the cliff-edge line, so their widths are `unknown`.
  - The main space cannot be defined, so the sizes are blank.
  - The pillar count is blank.
- **2543:8 (VI/52), confidence low.**
  - Four entrance arrows are drawn. The directions come from the arrows because the mouths are irregular.
  - Only opening 1 has a width.
  - The sizes, pillars and niches are blank.
  - Features marked I and II are not identified.
- **2543:3 (IV/7).** The north arrow is inverted on the page; it was checked by its width profile. The mouth is fully walled.
- **2545:1 (IV/11).** The single mouth's bearing (339°) is near the N/NW boundary.
