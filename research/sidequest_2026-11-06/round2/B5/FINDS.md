# Side-quest B5, round 2: discovery history of 3Q15. 6 Nov 2026

Builds on `out/B5/` (cards B5-1 to B5-3), `out/B5b/` (B5b-1 to B5b-3) and reviews R1 and R7. Round 1 left these open: B5-2 points 1 (4 days against "little more than a week"), 3 (Dajani "in 1956") and 4 (2 or 3 Jan 1956); R7's note that Allegro's "embassy official" may not be Muhammad Saleh; and the blocked Kuhn THLZ 79 and 81 reports, which were needed to rule out a second Kuhn visit in spring 1953.

**New inputs used this round (none of them used before in the project):**
- **Kuhn, ThLZ 79 (1954) and ThLZ 81 (1956).** Both are open access at Tübingen OpenDigi: `https://opendigi.ub.uni-tuebingen.de/opendigi/thlz_079_1954` and `.../thlz_081_1956`. I read the TEI OCR (`/ocr`). The key sentences were checked against the page images: `thlz_079_1954_00164` (cols. 303–304) and `thlz_081_1956_00280` (cols. 543–544).
- **Allegro 1960, first edition, Foreword p. 6.** Drive `08 Working files`, file `1fbAmSphdQGhtMnt1dczCfPMzNlA9PAzJ`, connector text. The repo extraction gives only a paraphrase of this passage.
- **Davies 2002, pp. 28–32.** In *Copper Scroll Studies* (Drive `1w-Y2yZjeAUSwnB7sF09Yfyc1uxFN2l0j`).
- **DQCAAS pages.** The Copper Scroll film page, which cites J. A. Brown 2005 p. 63, and the ASOR 1952 caption pages.
- **Web sources.** The UCL Discovery thesis list for 1956, and Wikipedia "Kemal Mehmood Homoud".

**Data products:**
- `timeline_round2_additions.csv`: 18 dated rows, in the same column scheme as `out/B5b/timeline_v2.csv` plus a note column.
- Private products: none. No restricted image was used. The ThLZ page crops in scratch are open-access scans, kept only for checking.

---

FIND CARD
Title (one line): Baker's "Mr. Homoud", the Jordanian embassy man who was expected in Manchester and did not come, is very probably Kemal Mehmood Homoud, counsellor at the Jordanian Embassy in London 1954–56. Jordan had three distinct men around the opening: Homoud (embassy), Dajani (a London doctoral student, sent by the Ambassador) and Saleh (Department of Antiquities, on a British Council bursary).
Lane: B5 (round 2)
Round-1 link: B5-2 point 2 (and R7's caveat), B5-2 point 3, B5b-2
What is odd (2–4 sentences): Davies 2002 p. 29 says the first roll was finished by 5 Oct 1955 "to the satisfaction of all, including the Jordanian embassy official who had been delegated to keep an eye" on it. Baker's letter of 19 Oct, answering Harding's remark about "some slight misunderstanding with the Embassy in London", says he knew of no "difficulty with London, and although Mr. Homoud was not able to visit us as expected, we hope to see him". A Jordanian diplomat named Kemal Mehmood Homoud was counsellor in London from 1954 to 1956, after serving as Chief of Protocol of the Royal Palace (1952–54) and as military attaché in London (1946–50). He is therefore the likely "embassy official". On Baker's evidence he had not visited by 19 Oct, so Davies's "satisfaction" can only have been given at a distance. The second Jordanian is ʿAwni Dajani. Allegro's own 1960 Foreword (p. 6) says Dajani was "asked to attend its cutting in Manchester in 1956 as official Jordan representative, while he was studying at the University of London Institute of Archaeology". UCL lists "Dajani, A.K. (al-Dajani, Awni), Hyksos period in Palestine, doctoral thesis, 1956". So the man the Ambassador sent on 15 Nov 1955 (Davies p. 30) was a Department archaeologist then studying in London, not an embassy diplomat. The third is Muhammad/Mohamed Saleh, the Department's Technical Assistant (B5b-2), whose bursary came from the British Council. Davies p. 32 says the British Council also "paid for the Copper Scroll to be brought from Jordan".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- TPA/1/132 (Drive `1QYCHkEFl7bzCdXFGrgkE7ZRG8Rk97TTv`): Harding to Bowden, 12 Oct 1955 (PDF p. 3); Baker to Harding, 19 Oct 1955, ref. 15879/55 (PDF p. 4).
- Davies 2002 pp. 29 (embassy official), 30 (Dajani, 15 Nov 1955, "at the Ambassador's request and without Harding's knowledge") and 32 (British Council paid the transport).
- Allegro 1960, Foreword p. 6 (Drive `1fbAmSphdQGhtMnt1dczCfPMzNlA9PAzJ`).
- UCL Discovery, `https://discovery.ucl.ac.uk/view/UCL/F31/1956.type.html` (fetched through WebFetch; curl got a Cloudflare 403).
- Wikipedia, `https://en.wikipedia.org/wiki/Kemal_Mehmood_Homoud`, career list ("From 1954 to 1956 he was counselor in London"). Its sources are the *Times of India Directory* 1965 p. 1205 and *Who's Who in the Arab World* 2007–08 p. 393.
- BJRL 39 p. 56 (Saleh's bursary); DJD III p. 210.
Literature check (queries run, result, tag):
- "Homoud": no hit in the repo main tree, `branch_only/`, the store, Davies, Shanks 2007 or the Allegro 1960/1964 texts. The only hits are the round-1 B5 files.
- Web searches "Homoud OR Hamoud Jordanian Embassy London 1955" and "Kemal/Kamal Homoud counsellor London" found only the Wikipedia biography and pages about his son Mazen Homoud (ambassador 2011). No Copper Scroll source names him.
- Dajani's London studies: the project extraction of Allegro 1960 has only "in 1956" (`allegro1960_treasure_extracted.md` l.224) and leaves out the London clause. A web search for Dajani + Institute of Archaeology + Copper Scroll found nothing.
- Tags: **NEW TO THE LITERATURE** for identifying Homoud as the embassy counsellor and for splitting the "Jordanian representative" into three people. **NEW TO THE PROJECT** for Dajani's London status (it is printed in Allegro 1960).
Why it might matter: It settles R7's caveat. The "embassy official" is a fourth person, neither Saleh nor Dajani. It also explains the "misunderstanding with the Embassy": the London embassy, through its counsellor and the Ambassador, wanted its own witness, and on 15 Nov it sent Dajani, a Department man who happened to be in London. Allegro's "in 1956" for Dajani is then either a slip for 15 Nov 1955 or a second, undocumented visit during the 11–16 Jan 1956 cutting. Dajani was in London all that academic year, so a January visit is possible. The British Council paid both for the transport and for Saleh's bursary. That supports, but does not prove, B5b-2's untested guess that Saleh was Harding's "Arab assistant" who flew in with the large roll (Allegro 1964 pp. 19–20).
How to confirm or kill it (with data in hand, or what is missing): The Jordanian diplomatic list in the *London Diplomatic List* (FCO) for 1955 would confirm "Homoud, counsellor". The full TPA/1/132 file, or Allegro's letters in Brown 2005 (pp. 60–75; not in the corpus), would show whether Homoud ever came and whether Dajani came in January 1956. The identification is killed if the 1955 list has no Homoud at the Jordanian Embassy, or if the letters name another "Mr Homoud" (for example a Department or Ministry official in Amman).
Confidence: high (what the sources say); medium (Homoud = Kemal M. Homoud: one tertiary source, but the name, post, place and years all match); low (Saleh = courier).
Touches the Copper Scroll? yes, but only its custody history. ARGUMENT: no bearing on any entry's identification.

---

FIND CARD
Title (one line): Kuhn's two German reports, both cited by Lefkovits, date his study to "Herbst 1953" and mention no mirrors. This rules out a second "spring 1953" visit. They also show that Kuhn first made the treasure-list hypothesis public at the Berlin Theologentag of 3–6 January 1954.
Lane: B5 (round 2)
Round-1 link: B5-3 (R1: "needs new data only to exclude a second, spring visit (Kuhn, THLZ 79)")
What is odd (2–4 sentences):
- ThLZ 79 (1954) col. 304: "Aus diesen Spuren konnte ich bei meinem Aufenthalt in Jerusalem im Herbst 1953 einiges entziffern" (checked on the page image).
- ThLZ 81 (1956) col. 542 gives only "im Jahre 1953" and adds "So habe ich sie damals immer nur unter Glas gesehen". Neither report mentions mirrors. Allegro 1964 p. 15 says Kuhn "was lent photographs of their hidden undersides". Photographs, not mirrors, are the second aid in every primary account.
- Lefkovits 2000 p. 5 n. 10 cites both ThLZ reports. He gives the first as "THLZ 74 (1954)"; 1954 is volume 79. Yet he writes "In the spring of 1953 … with help of mirrors and photographs" (p. 4), and Shanks 2007 repeats this.
- The 1954 text is a "Résumé" of a paper given at the Deutscher Evangelischer Theologentag in Berlin, 3–6 January 1954 (ThLZ 79 col. 193). An editorial note in Nr. 6 says the paper belonged to the New Testament section. RB 61 is announced there for April 1954. So the hypothesis was given in public in Berlin about five weeks after de Vaux's letter of 1 Dec 1953, and three months before RB. Kuhn also gives "about 25" occupied caves for the 1952 survey, where the DQCAAS summary of the ASOR expedition (after DJD III) gives 40 caves with remains.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- OpenDigi `thlz_079_1954`: col. 193 (Theologentag dates, image `_00109`); cols. 303–304 (Kuhn's résumé, image `_00164`); editorial note in Nr. 6 (image `_00204`).
- OpenDigi `thlz_081_1956`: cols. 541–546 (images `_00279`–`_00281`).
- Lefkovits 2000, store `Lefkovits-2000-…-db4f91b2`, PDF pp. 25–26 (= pp. 4–5, n. 10).
- Allegro 1964 p. 15 (Drive `1JTa1JlpTCO0j3mKRBAuQg1iH7FEu3lR2`, OCR in `scratch/B5/allegro_drive.txt`).
- Shanks 2007 (Drive `1sNzZT2RmBUp9Wa9q2gw8ErUswu-nX8WH`).
- DJD III p. 201.
Literature check (queries run, result, tag):
- "Herbst 1953", "Theologentag", "ThLZ/THLZ/Literaturzeitung": no hits on main or `branch_only/`, other than round-1 swarm files saying THLZ was unread.
- Store `pdf-search "Kuhn"`: EDF cites only RB 1954. Lefkovits cites the ThLZ reports but follows a different source for the season.
- Lefkovits n. 10 also cites Yadin, *Message of the Scrolls* (1957) pp. 156–57, which may be where "spring" and "mirrors" come from. I could not open it: the Internet Archive copy is lending-only (403).
- Tag: **KNOWN BUT UNDER-DISCUSSED.** The autumn date is in DJD III. What is new is that Kuhn's own two later statements also say autumn and say nothing of mirrors, which closes the two-visit escape. The January 1954 Berlin presentation is **NEW TO THE PROJECT**. The "THLZ 74" miscitation is a small **NEW TO THE LITERATURE** item.
Why it might matter: "Spring 1953 … mirrors" now has no primary witness, so the conflict is an error that spread from one secondary source (Lefkovits, then Shanks). It is not two visits. The Berlin date gives an earliest public date for the treasure reading: 3–6 Jan 1954, with the RB 1954 text following in April. That matters for any claim about who knew what before the opening (for example the 1955 press and Allegro's "amusement" story, 1964 p. 15).
How to confirm or kill it (with data in hand, or what is missing): Yadin 1957 pp. 156–57 (lending copy `messageofscrolls00yiga`). If Yadin, or another Kuhn text, reports a spring visit or mirrors from Kuhn himself, the conflict reopens. Lefkovits's dissertation vol. 2 pp. 1190–1204 is still unread.
Confidence: high.
Touches the Copper Scroll? yes: who saw the outer turns of the unopened rolls, when, and by what means. ARGUMENT: no effect on any identification.

---

FIND CARD
Title (one line): Kuhn reports a German attempt to open 3Q15 that the standard histories omit: a chemist of the Bayer main laboratory in Leverkusen tested chemical reduction, parallel to Baltimore. Kuhn names Albright, not Corwin, for Baltimore. Even in September 1956 Kuhn says he had not seen the opened text.
Lane: B5 (round 2)
Round-1 link: new (it bears on B5-1/R1, "fully examined in the U.S.A.", and on DJD III p. 201's "fragments sent to foreign laboratories")
What is odd (2–4 sentences):
- ThLZ 81 col. 544 (checked on the page image): "Professor Albright in Baltimore, USA, stellte mit seinem chemischen Kollegen an der Universität Untersuchungen an" on reducing the oxide. "Auch ich konnte in Deutschland durch die freundliche Mithilfe eines Chemikers aus dem Hauptlaboratorium der Bayerwerke in Leverkusen Untersuchungen in derselben Richtung anstellen". Both found that reduction needs high temperatures, which was too risky.
- Kuhn then says he proposed in a 1954 memorandum to the PAM that the rolls be coated with "einem Film von durchsichtigem synthetischen Kunststoff" and cut into pieces. Plenderleith had also proposed sawing. "Genau in dieser Weise" Baker opened them in winter 1955/56.
- DJD III p. 201 credits only Plenderleith (cutting) and Corwin (reduction, on an oxidised copper replica). Lefkovits p. 5 keeps the memorandum and leaves out Leverkusen.
- In the same report (cols. 544–546, Heft 9, 1956), Kuhn says he cannot yet judge de Vaux's "Phantasieprodukt" verdict "weil ich noch nicht den Wortlaut des ganzen Textes gesehen habe". He quotes only the 1 June 1956 press passage. So the man whose hypothesis was "confirmed" had not been shown the text eight months after the first roll was read.
Evidence (exact sources: file path / page / figure / frame / coordinates): OpenDigi `thlz_081_1956`, cols. 542 (rolls only seen under glass), 544 (Albright, Leverkusen, the 1954 memorandum, Plenderleith, the Manchester method, the 1 June 1956 release), 544–546 (has not seen the full text; Josephus parallels; Temple-treasure option). Images `_00280`, `_00281`. Compare DJD III p. 201 (store `DJD-III-…-db2d5e3d`, PDF 221); Lefkovits 2000 p. 5; TPA/1/132 PDF p. 2 ("fully examined in the U.S.A.").
Literature check (queries run, result, tag):
- "Leverkusen" and "Bayer": no hit in the repo, `branch_only/`, the store (the Lefkovits "Bayer" hits are B. Bayer, "Music"), Copper Scroll Studies, Shanks 2007, the Allegro 1960/1964 texts, Baker BJRL 1956 or DJD III.
- One web search (Kuhn, copper scroll, 1954 memorandum, Bayer, Leverkusen) found nothing.
- The memorandum itself is in Lefkovits.
- Tag: **NEW TO THE PROJECT** (Kuhn published it in 1956). It is under-discussed in the literature: no later account I found repeats the Leverkusen tests or Kuhn's September 1956 lack of access.
Why it might matter: It adds a third laboratory programme (Baltimore, British Museum, Leverkusen) to the pre-opening history. DJD III p. 201 says uninscribed fragments that fell off the rolls "aussitôt après la découverte" went to foreign laboratories, and no list of where they went exists. ARGUMENT: if the Leverkusen chemist worked on a real fragment rather than a replica, Bayer is one more possible home for a detached piece of 3Q15. This is an inference only: Kuhn does not say what material was tested. It does not bear on any entry's identification.
How to confirm or kill it (with data in hand, or what is missing): Kuhn's RB 61 (1954) pp. 193–205 (Drive `1Q4urT-ZFgOLEck3ty_ZDx8b62rClVuN-`): does it mention Leverkusen or a sample? A search of Kuhn's Nachlass or the Bayer archive would need an archive request, which is outside AI-only work. The material question is killed if a source says the Leverkusen tests used a replica or a copper sample of the chemist's own.
Confidence: high (what Kuhn wrote); low (any fragment implication).
Touches the Copper Scroll? maybe: the physical history of detached fragments.

---

FIND CARD
Title (one line): The two openings can now be dated to the day. Roll 1 was cut from Sat 1 to Wed 5 Oct 1955, so Baker's "4 days" is right and Allegro's "little more than a week" (copied by Shanks) is wrong. Roll 2 was cut by 11 Jan and finished at 9 p.m. on Mon 16 Jan 1956. Only "2 vs 3 January" stays open.
Lane: B5 (round 2)
Round-1 link: B5-2 points 1 and 4 (R1: "1 not a real contradiction"; "4 trivial")
What is odd (2–4 sentences):
- DQCAAS's film page, citing Brown 2005 p. 63 (Allegro's letters), puts the first cut on Saturday 1 Oct 1955. Baker then called Allegro so that a second cut could be made on Monday 3 Oct, which Allegro filmed. Davies (letters of 1 and 5 Oct) has the roll done by 5 Oct. Baker's 19 Oct letter: "completely opened and rough cleaned in my spare time on 4 days".
- So Allegro 1964 p. 19, "In little more than a week the roll was open", repeated by Shanks 2007, overstates the cutting by about half, though it may include cleaning. Baker says detailed cleaning took "about as long again".
- Roll 2: Allegro 1964 p. 20 has it arrive in Manchester on "2 January", with Baker "away on holiday", and the last piece free "by nine o'clock on the evening of 16 January". Davies p. 31 has it reach England on 3 January, with Baker cutting "by 11 January".
- So roll 2 took about 6 calendar days of cutting, against Baker's own forecast of "about ten days" (19 Oct letter). The 6 Sept 1955 minute ("One of these scrolls is now in the College") brackets roll 1's arrival before 6 Sept, consistent with DJD III's "juillet 1955".
Evidence (exact sources: file path / page / figure / frame / coordinates): `https://dqcaas.com/photographic-collections/copperscroll/` (fetched 6 Nov 2026); Davies 2002 pp. 29, 31; TPA/1/132 PDF pp. 2, 4; Allegro 1964 pp. 19–20; DJD III p. 202. Weekdays computed (1 Oct 1955 Sat; 3 Oct Mon; 2 Jan 1956 Mon; 16 Jan 1956 Mon). Rows in `timeline_round2_additions.csv`.
Literature check (queries run, result, tag): Brown 2005 is not in the corpus. The repo atlas (`atlas/app/atlas-history-data.ts`) already uses the 1 and 3 Oct dates for the film, but not to test the "week" claim. No source I read reconciles Allegro's "week" with Baker's "4 days". Tag: **KNOWN BUT UNDER-DISCUSSED**. Each date is published; putting them together closes B5-2 points 1 and 4 (partly).
Why it might matter: The cutting rate is evidence of how much care was possible at the saw lines (B5-2). Roll 2, the larger and "more compact" roll with the closer convolutions, was cut faster than Baker forecast. That fits Allegro's "even more quickly than the first part". ARGUMENT: anyone blaming lost letters at the cuts of segments 1–14 on haste has a date bracket (≤11 Jan to 16 Jan 1956) to work with. That does not change any reading.
How to confirm or kill it (with data in hand, or what is missing): Brown 2005 pp. 63–75 and Allegro's letters of early January 1956 (not in the corpus) would settle 2 or 3 January. If Brown has a cut of roll 1 after 5 Oct, the "4 days" span is killed.
Confidence: high (Oct 1955 dates); medium (Jan 1956 start date).
Touches the Copper Scroll? yes: opening history only.

---

## Status of round-1 open points after round 2

| Item | Status | Basis |
|---|---|---|
| B5-2 (1): 4 days vs "little more than a week" | **Resolved:** 1–5 Oct 1955; Allegro 1964 is the outlier | card 4 |
| B5-2 (2) / R7 caveat: who was the "embassy official"? | **Probably resolved:** Kemal M. Homoud, embassy counsellor (expected, absent by 19 Oct) | card 1 |
| B5-2 (3): Dajani "in 1956" | **Partly resolved:** he was a London doctoral student sent by the Ambassador, documented on 15 Nov 1955; a January 1956 visit is possible but undocumented | card 1 |
| B5-2 (4): 2 vs 3 Jan 1956 | **Open** (Allegro: Manchester, 2 Jan; Davies: England, 3 Jan) | card 4 |
| B5-3: second Kuhn visit in spring 1953? | **Killed:** both ThLZ reports say autumn or only 1953, with no mirrors | card 2 |
| B5b-2: Saleh = Harding's courier? | **Supported, not proved:** the British Council paid for both the transport and Saleh's bursary | card 1 |

## Dead ends
- Allegro 1964 Pl. 7 ("Dajani … with Professor Karl Georg Kuhn"): I wanted to see whether it was taken in Manchester. The IA copy `treasureofcopper0000john` is print-disabled (403). Allegro cites the plate in his account of Kuhn's Jerusalem visit (p. 15), and Kuhn says in Sept 1956 he had not seen the text, so a Manchester setting is unlikely. Dropped.
- Source of Lefkovits's "spring … mirrors": Yadin 1957 is a lending-only IA copy, and inside-search returned no JSON. Not resolved.
- DQCAAS ASOR 1952 captions (21 pages): their 3Q content (G8 = GQ8, the rolls "one on top of the other" on a shelf) is already in DJD III and the project's DQCAAS README. Nothing new for this lane.
- johnallegro.org: book pages only. The Brown 2005 page has no text from the book.
- Kuhn ThLZ 81 col. 25–30 (Heft 1, January 1956): it is about the War Scroll and does not mention the copper rolls.
- Kuhn's "three plates of about 30 × 80 cm" and his deliberate-separation view (still held in 1956, cols. 542, 545): not new (Puech 2006 already rejects the separation view; plate sizes superseded by EDF).

## Blocked inputs
- J. A. Brown, *John Marco Allegro: The Maverick of the Dead Sea Scrolls* (2005), pp. 60–75: not in the corpus. Known only through DQCAAS's citation of p. 63.
- Yadin, *The Message of the Scrolls* (1957), IA `messageofscrolls00yiga`: `_djvu.txt` gave HTTP 403; `fulltext/inside.php` returned non-JSON.
- Allegro 1964, IA `treasureofcopper0000john`, page images: HTTP 403 (print-disabled). The Drive PDF `1JTa1JlpTCO0j3mKRBAuQg1iH7FEu3lR2` could not be downloaded in round 1 ("message from the server was too large").
- UCL Discovery thesis list: curl gave HTTP 403 (Cloudflare challenge). Read through WebFetch.
- Drive folder listing `dqcaas-allegro (2026-10-31)/data` (`1vSYDiETq5oXLEQ-PxXMuuvJTB6s41snZ`): search_files broke the connector ("message from the server was too large"). I used the live DQCAAS site instead.

## Reproducibility
ThLZ TEI files were saved to `scratch2/B5/web/thlz79_tei.xml` and `thlz81_tei.xml`, and converted with `scratch2/B5/tei2pages.py`. The column split at x = 1170 px is approximate, and headers and footnotes can interleave.
