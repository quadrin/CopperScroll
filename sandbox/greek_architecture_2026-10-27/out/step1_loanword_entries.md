# Run 9, step 1: loanword entries, their relations, and the control entries

Written before step 2 (no building inventory gathered yet). Rule: sandbox/greek_architecture_2026-10-27/RULE.md, commit c420100, SHA-256 170227b8ef73407021032f8452a51e1756e48dba3c53d0187918c1019d216585.

Exposure before writing: I had read text/readings.json, text/glossary_en.json, tables/landmark_lexicon_index.csv, the evidence_components ratings rows for entries 3, 8, 12, 15, 50, 51, research/logs/findings_log.md (Southern Wall / Galor-Avni / Lefkovits sections), research/sites/leads_on_old_plans §4.2 (Great Sea for entry 3), and the tomb-lane README (entry 51 branch counts). So the Temple Mount cisterns and the Kidron tombs were known to me beforehand.

Hebrew text: research/agent_review_2026-10-07/wave1/T08_real_or_legend/data/scroll_lines_with_numerals.txt (the repo's text shown).

## How the loanword list was fixed

Sources: landmark_lexicon_index.csv (terms peristylon, stoa, exedra), glossary_en.json (words glossed "from Greek": פרסטל, אסטאן, אכסדרן; also אסתר stater and בלג lagin, which are a coin and a vessel, not architecture, so excluded), readings.json (adds Puech 2006's restoration דיאט = Greek δίαιτα at III 1, not in the lexicon). No Latin architectural loan is listed in any of the three. סבין (entry 53, Puech "colonnades") is not glossed as a loanword in any file, so it is excluded.

| Loanword | Entry | Line | Status of the reading |
|---|---|---|---|
| פרסטלין / פרסטלון, peristyle (περίστυλον) | 3 | I 7 | secure; Milik, Puech, Lefkovits agree (readings.json e3-court) |
| אסטאן, stoa (στοά) | 51 | XI 2 | Milik, Puech "stoa"; Lefkovits "ossuary" (p. 366) |
| אכסדרן, exedra (ἐξέδρα) | 51 | XI 3 | read by all (ratings.csv row 79) |
| דיאט(?), diaita (δίαιτα) | 12 | III 1 | Puech 2006 restoration only, with "?"; Lefkovits restores נבט, Milik no name; the text shown leaves the letters unread. Run as a conditional branch (12-P). |

## Relations per loanword entry (scored in step 3)

Entry 3 (I 6–8): בבור הגדול שבחצר הפרסטלין בור בקרקעו סתום בחליא נגד הפתח העליון
- 3.R1 a court of a peristyle (a colonnaded court) [loanword relation]
- 3.R2 a great (large) cistern in that court
- 3.R3 a pit/hole in the cistern's floor (בור בקרקעו)
- 3.R4 closed with חליא (sense unclear; all editions differ in sense)
- 3.R5 opposite "the upper opening" (the cistern has an upper opening/shaft)

Entry 51 (XI 2–4): מתחת פנת האסטאן הדרומית בקבר צדוק תחת עמוד האכסדרן
- 51.R1 a stoa with a southern corner [loanword relation] (branch 51-O, Lefkovits "ossuary": R1 is not an outside landmark and is scored unknown)
- 51.R2 the place lies below (lower than) that southern corner
- 51.R3 a tomb
- 51.R4 the tomb is Zadok's
- 51.R5 an exedra with a pillar/column, under which the deposit lies [loanword relation]

Entry 12 (III 1–4), branch 12-P only (Puech's δίαιτα): בחצר [ש(ל) ]דיאט תחת הפנא הדרומית חפר אמות תשע
- 12.R1 a court belonging to a diaita (a residential suite/pavilion) [loanword relation]
- 12.R2 the court has a southern corner
- 12.R3 dig nine cubits under it
- (12a, III 5–7: the other, eastern corner, sixteen cubits; recorded only as context)

## Control entries (no loanword; chosen from the text before scoring)

The rule asks for two entries without loanwords "that also name a cistern in a court". Searching the text shown and the lexicon (hatser = entries 3, 8, 12; bor = 3, 6, 8, 9, 10, 15, 45): only entry 8 names both a cistern and a court. No second entry does. Most literal choice for the second control: the one other non-loanword entry with "the great cistern" (entry 15), which shares entry 3's wording; entry 50 (a court in Puech's and Lefkovits's readings, no cistern) is run as an alternative, labelled a deviation.

Control C1, entry 8 (II 5–6): בצריח שבחצר מתיה עצין וכתבן בור בו
- 8.R1 a court (named: "of Mattiyah" engraved, or "of the wood stores" by emendation)
- 8.R2 an underground chamber (צריח) in the court
- 8.R3 a cistern in it (בור בו)

Control C2, entry 15 (IV 1–2): בבור הגדול שב כחלת בעמוד בצפונו
- 15.R1 a great (large) cistern
- 15.R2 a pillar on its north side (בעמוד בצפונו)
- 15.R3 at Koḥlit (Puech's restoration; place unlocated)

Control C2-alt (deviation), entry 50 (X 17–XI 1): בברכא העליונה ב ארבעת מקצועות
- 50.R1 a court (Puech: courtyard of Zadok's tomb; Lefkovits: inner court) or, on Wise's restoration, the upper pool
- 50.R2 with four (inner) corners

## Place-name relations

Koḥlit (15.R3) and Zadok (51.R4) are names with no independent location in the repo; they are scored unknown for every building unless a source ties the name to it.
