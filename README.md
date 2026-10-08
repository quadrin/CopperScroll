# Copper Scroll (3Q15)

Research on the places, landmarks, text, and structure of the Copper Scroll. The repository brings together written analysis, source checks, data tables, reproducible tests, and an atlas that includes the scroll text.

## Start here

For a new research session, read [AGENTS.md](AGENTS.md), then [the active test](research/ACTIVE_TEST.md). It gives the active questions, the observation that would decide each, pending requests and the next evidence to obtain. [Open questions](research/OPEN_QUESTIONS.md) is the broader backlog and history.

1. [Current site assessment](research/sites/site_identification_review.md) explains the leading place proposals and their limits. These are site-level identifications; no individual deposit or hiding place has been identified.
2. [Research guide](research/README.md) lists every report by subject and points to the evidence behind each conclusion.
3. [Explore the atlas](https://quadrin.github.io/CopperScroll/) to browse the entries, map candidate places, review evidence, and read the scroll column by column.
4. [Atlas guide](atlas/README.md) explains the interface and how to run or rebuild it. A prebuilt static version is in [`atlas-site/`](atlas-site/).

The main site proposals remain conditional. The review rates Qumran's upper aqueduct (entry 21), Doq (31), the Wadi Qelt/Choziba stretch (32), and the Siloam outlet complex (49) at medium site confidence. [Feature investigation](research/sites/feature_investigation.md) tests individual structures separately. The [plate check](research/text/plate_check.md) revisits readings that affect several identifications. The [sequence analysis](research/text/deeper_analysis_2026-09-30.md) finds a different ordering pattern in entries 1–19, but does not locate a site. Later corrections are recorded in the reports and [findings log](research/logs/findings_log.md).

**Latest review:** [Parallel-agent review, 6–7 October 2026](research/agent_review_2026-10-07/README.md). It corrects several claims (Koḥlit, entry order, roundness) and lists the observations that would discriminate the Koḥlit candidates; no identification changes. Goals: [GOALS.md](research/agent_review_2026-10-07/GOALS.md).

**Latest source follow-up:** [Hyrcania plan registration, Christmas Cave object provenance and Salvadora contexts](research/sites/cave_plan_followup_2026-09-30.md). Includes a failed precise-registration check, a conditional pool-dimension test, museum/lab identifier joins and the located arrowhead crack.

## Repository map

| Folder | Contents |
| --- | --- |
| [`research/`](research/README.md) | Phased reports, site studies, text and sequence studies, source work, logs |
| [`tables/`](tables/) | Entry concordance, candidate-place indices, archaeological assessments, constraints, plate checks |
| [`text/`](text/) | Project translation, glossary, and notes on variant readings |
| [`deep_analysis/`](deep_analysis/README.md) | Scripts and recorded results for the sequence tests |
| [`registration/`](registration/) | Source extractions, geographic registration records, and plate-check reader data |
| [`figures/`](figures/) | Research figures |
| [`data/`](data/) | Source text and reading notes used to build the atlas reader |
| [`atlas/`](atlas/README.md) | Interactive atlas source and its research materials |
| [`atlas-site/`](atlas-site/) | Prebuilt atlas assets for GitHub Pages; the repository homepage loads the atlas |
| [`tools/`](tools/) | Scripts for producing reader data and checking images |

## Provenance and reuse

This material was migrated from the [`copper_scroll/` section of AncientHebrewTexts](https://github.com/quadrin/AncientHebrewTexts/tree/176b4c09340c4402d06bb612c493e9f97b049b53/copper_scroll) at source commit `176b4c0`. The [TIR digital-copy search](research/sources/tir_digital_copy_search.md) and its supporting assets came from that repository's root. The source repository also holds research copies of modern Copper Scroll editions and other PDFs; this repository carries the analyses and citations, while those edition files remain there. The [source inventory](research/sources/sources.md) records what was actually checked and what remained inaccessible.

The Hebrew reader uses Martin G. Abegg Jr.'s transcription from ETCBC *dss* 2.0.1, credited under CC BY-NC 4.0. The English translation, glosses, notes, and research assessments were written for this project. Maps and photographs have their own source credits. See the [research instructions](AGENTS.md) before adding textual or geographic claims.
