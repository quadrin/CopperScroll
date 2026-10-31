# Attribute inventory: reader instructions (frozen before any source is keyed)

You are keying archaeological descriptions into a table. You are not identifying places for anything.

1. Read only the source and section you are given (`sources.csv`) and `SCHEMA.md`. Do not open the Copper Scroll text, any edition or commentary of it, the project's candidate lists, ratings, atlas files or earlier keyed files.
2. Key every feature the section describes that has at least one attribute beyond its class: a size, a count of openings or steps, a direction, plaster, pillars, construction, or a relation to another feature.
3. Copy numbers as printed. Do not round, average or infer. If the text and a plan disagree, key the text, and add the plan value in `notes`.
4. Measure from a plan only if it has a scale bar, and a north arrow for directions. Set `dims_basis = plan_scaled`, name the figure, and give the value to the nearest 0.5 m.
5. Use the 8-point compass. "Faces east" means the opening looks east, out of the feature. If the source does not say which way an opening faces and the plan has no north arrow, leave `opening_dirs` blank.
6. A cave with several chambers: one row for the cave and one row per chamber, with `parent_id` pointing to the cave.
7. Quotes: at most 15 words per row, only to support the most specific attribute. Paraphrase everything else.
8. When unsure, key the row with `confidence = low` and say why in `notes`. Do not drop it.
9. Write the CSV to `keyed/<source_id>_<reader>.csv`. Also write `keyed/<source_id>_<reader>_log.md`: the pages and figures you read, anything you could not read, and the time you started and finished.
10. Two readers key each source independently. They do not see each other's files until both have finished.

## Agreement (computed after both readers finish)

- Rows are matched on `site_name` plus local id. Features without a local id are matched by class and page.
- Reported: the share of rows matched; on matched rows, class agreement, dimensions within 10 % or 0.2 m, exact `n_openings`, `opening_dirs` the same or neighbours on the compass, and exact `n_steps`.
- Disagreements are settled by a third reading of the page. The third reading is logged and does not overwrite either reader's file.
