# Registration protocol, amendment A1 (DRAFT): blind scoring instead of sealed records

Drafted 24 October 2026 by Claude at the owner's request. **Status: DRAFT, not adopted.** It takes effect only when the owner adopts it in writing (chat or commit message) and the integrator commits it with that note. Until then [registration_protocol.md](registration_protocol.md) applies unchanged.

## Why

The prediction (`SULTAN-1-precamp-mouth`, registered in [chain.json](chain.json) and the [arrival register](../../preregistration/arrivals/README.md)) is frozen and hashed. Seeing a record cannot change it. The real risk is in *scoring*: deciding where the strip lies, what counts as an opening, and whether graves lie within 10 m. A reader who knows where the target is can lean those calls toward it. The protocol's preview-first rule (§2.5) tries to prevent that by keeping records unseen, which blocks ordinary reading. Blind scoring prevents it more directly and leaves the records open.

## What changes

1. **Reading is open.** Anyone may open and read a record north of Tell es-Sultan in full, at any resolution. §2.5's low-resolution-first rule and the "do not open" folder rule no longer apply to records opened after adoption.
2. **The frozen parts stay frozen.** The prediction and its success wording (§2.1), the intake record (§2.2), the fit rules (§4), the acceptance thresholds (§5) and "locating is not dating" (§6) are unchanged. Controls and the check point still come from outside the target zone (§2.6), and the fit is declared and committed before any verdict.
3. **Blind scoring replaces sealing.** For each registered record:
   - **Tiles.** The integrator cuts the target strip (tell's north foot to 250 m north, as §1) and at least four control strips of the same size and scale from the same record: same distance band off the west, south and east feet of the tell, and one band farther north beyond 250 m. Tiles are given random codes; the key (code → strip) is hashed and kept by the integrator.
   - **Scorer.** A person or a fresh agent who has not seen the record, the repository, the key or this project's predictions. The scorer receives only the coded tiles, the scale, and the frozen criteria written neutrally: "Is there a pit or shaft mouth? Are there graves within 10 m of it? Mark positions." The scorer locks the answers (UTC time and SHA-256) before the key is opened. One scorer per record; a second scorer is optional and is reported separately.
   - **Verdict.** Map the locked marks back through the registration and apply §5's thresholds. Report every tile.
4. **Discrimination rule (owner's choice; default proposed).** The target strip counts as *supported relative to the controls* only if (a) it is scored positive under §5 and (b) fewer than half of the control strips are scored positive. If the target is positive and half or more of the controls are too, the record is *not discriminating*. If the target is negative, the record is *silent* (§6: silence is not absence).

## What does not change

- Already-exposed items stay exploratory: the SULTAN-1 Drive folder (seal lifted 24 Oct), the Wagemakers 2014 chapter 6 (read 24 Oct), the PEF *Quarterly Statement* items, and the eight Commons files of 17 Oct. Blind scoring could still be run on them, but the result is labelled exploratory unless the owner decides otherwise in writing.
- Reserved items under other protocols (XII 10 images; the arrival register's frozen procedure for other items) are untouched.
- AGENTS.md's "Require an unseen prediction" rule is met by the frozen prediction plus a blind scorer. Adopting A1 needs one line added to ACTIVE_TEST question 2 replacing "follow the registration protocol" with "follow the registration protocol as amended by A1".

## Owner decisions needed to adopt
1. Adopt A1 (yes/no).
2. The discrimination rule in point 4: keep the default ("fewer than half the controls positive") or set another.
3. Whether the exposed items listed above may be blind-scored as confirmatory (default: no, exploratory only).
