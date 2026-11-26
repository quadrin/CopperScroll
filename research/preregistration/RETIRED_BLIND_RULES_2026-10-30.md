# Blind, reserve and held-area rules retired, 30 October 2026

**Decision.** On 30 October 2026 the project owner, Alex Kesin, retired every blind-reading, reserve, held-area and "do not open" rule in the project. All material is visible. Read any source, image or record normally, at any resolution, as soon as it is useful. No masking, coded tiles, blind scorers, human administrators, exposure logs or prior registration are needed before opening anything.

This record overrides the files listed below. Several of those files are hash-frozen (by `MANIFEST.md`, `MANIFEST.sha256` or `register.json`), so they are kept byte-for-byte as historical records instead of being edited. Where they conflict with this page, this page governs.

## What is retired

| Rule | Where it was set | Now |
|---|---|---|
| SULTAN-1: the strip north of Tell es-Sultan reserved for a blind registration test | `assessments/kohlit_chain/registration_protocol.md` and amendment A1 (coded tiles, blind scorer) | Open. Garstang, PEF, Nigro, RAF, Mandate-map, Bavarian and Commons/Matson records are read normally. |
| Held areas (Jericho escarpment, Wadi Qelt, Qumran cliff caves) | the owner's rule of 25 October; the arrival-register holds on cave reports | Open. Held-area material is ordinary evidence. "EXPOSED" labels on it no longer limit its use. |
| XII 10 blind reading at the segment 21/22 cut | `agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md` (frozen at `fd3f334`); `arrivals/ARRIVAL_PROCEDURE.md` §2 (reserved items, human administrator, two blinded human readers) | Open. Any reader, human or AI, may read XII 8–12 and the 21/22 cut on any image. The protocol's letter strings and criteria may still be used as a checklist, but nothing gates access. |
| Letter-control calibration as a precondition for an XII 10 reading | `text/letter_controls/PROTOCOL.md` | Optional. It is a calibration tool, not a gate. |
| Arrival gating: "run `arrival.py check` and follow the procedure before opening any arrival" | `arrivals/README.md`, `ARRIVAL_PROCEDURE.md` | Optional. An arriving item is opened and read at once. The frozen predictions stay on record and can be scored afterwards for interest; scoring is not a precondition for reading. |
| Entry 25 / IV/17 rules as a precondition for reading the L-656 file or IAA cave records | `entry25_iv17_rules/RULES.md` | Optional. The rules remain usable as a scoring method; they do not gate reading. |
| XII 8–12 exclusion in the edition-confusion matrix | `text/edition_confusions/exclusion.py` | No longer required. The matrix was built without XII 8–12 and stays as built; a rebuild may include those lines. |
| Drive folders marked "reserved", "SCREEN FIRST", "PROTECTED" or "do not open" | Drive | Renamed and opened on 30 October (below). |

## Drive changes made on 30 October

- `06 Imagery/SULTAN-1 reserved – do not open` is renamed `06 Imagery/Tell es-Sultan and Jericho photos – Commons and LoC Matson (2026-10-17)`, with a rewritten README.
- `07 Maps and GIS/Bavarian aerials 1918/SCREEN FIRST – do not open`: BS Pal. 901, 980, 1032 and 1034 and the README were moved into `Bavarian aerials 1918`. The empty folder is renamed `_to_delete – empty (formerly SCREEN FIRST)`.
- The four `PROTECTED – … – do not open` folders under `08 Working files/Unsorted source scans`, and their files, were renamed without "PROTECTED", "do not open" or "blind".

## What does not change

- Published results keep their recorded status. A test that ended "not identifiable" or "exploratory" is not upgraded, and an earlier exposure note stays as history.
- The general evidence standards in [AGENTS.md](../../AGENTS.md) for a formal confirmation claim still apply. A formal claim must say which evidence selected the model and which tested it. That is a reporting standard, not an access restriction.
- Copyright and reuse limits are unchanged. For example, the USC/WSRP images may be read but not published, and IAA descriptive text stays out of the public repository.
