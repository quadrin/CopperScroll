# Attribute inventory (step 1 toward run 28), 31 Oct 2026

Exploratory sandbox work. No rating, ledger, ACTIVE_TEST or atlas change.

## Why

Runs 26 and 27 showed that class-level records ("a cistern is recorded in this cell") separate a true place from others by 0.99–1.4×. Run 27 named the condition that would reopen the question: an inventory with feature attributes (size, steps, plaster, number and direction of openings, pillars, relations) that lets rarer conjunctions be scored ([run 27 RESULT](../landscape_map_1km_2026-10-31/RESULT.md), "Reopening conditions"). This folder builds that inventory from sources the project holds in text form.

## Owner decision, 31 Oct 2026, 14:31 PT

The owner lifted the held-area rule of 25 Oct: "We don't need to hold anymore." All zones are in scope, including the Jericho plain and escarpment, the Wadi Qelt gorge, Abu Saraj / IV/17 and the Twin Cave. Material from those areas read from now on is unblinded. Earlier tests that relied on it staying unseen can no longer be run blind.

## Order of work

1. `SCHEMA.md`, `READER_INSTRUCTIONS.md` and `sources.csv` are committed before any source is keyed. This commit is that step.
2. Two independent readers key each source (`keyed/`), in the order of `sources.csv`. The first is the 1993 cave survey (*ʿAtiqot* 41, English issue).
3. Agreement is computed and reported as in `READER_INSTRUCTIONS.md`.
4. Run 28 (`../attribute_test_*`): a rule, written and committed **before any benchmark item is scored**, tests whether attribute conjunctions carry evidence. It uses held-out describers and leave-one-source-out, calibrated as in run 27, and uses only the attribute types the scroll entries use. The scroll is scored only if that gate passes.

## Sources

`sources.csv` lists 13 sources in reading order: the 1993 cave survey; IIIA's lists of loci and built elements; Magen & Peleg 2018; Hirschfeld 2004; Eshel et al. 2002; Bar-Adon 1977; IVA; *ʿAtiqot* 119; the ASI maps of Herodium and Mar Saba; JSP 8; Stager 1976; and *The Aqueducts of Israel*. Text copies are in the project bucket (`gs://copper-scroll-cog-1030`) or on the owner's Drive. No source text or page image is stored in this repository.

## Before this commit

The main session ran a regex over the 1993 cave-survey texts. It printed per-article counts only: distinct "Cave N/N" labels (112), dimension phrases (316) and the words "opening"/"entrance" (398). It also listed the article titles. No sentence of any source was displayed.
