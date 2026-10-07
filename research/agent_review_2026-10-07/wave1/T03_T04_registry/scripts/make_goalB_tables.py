# -*- coding: utf-8 -*-
"""Write the Goal-B (entry 60 / Koḥlit) tables. Data are typed from the sources named in each row.
Run: python3 -I make_goalB_tables.py <out_dir>"""
import csv, os, sys
OUT = sys.argv[1]

def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

READ = "shared/readings.json"
write("entry60_readings.csv",
      ["line", "phrase", "who", "reading", "meaning_or_translation", "source", "access", "label"],
      [
       ["XII 10", "second word (שבצח/שכנה/שבינח…)", "Milik 1962", "שבצח", "'of the Smooth Rock'", "DJD III (via readings.json e60-janoah)", "via " + READ, "EVIDENCE"],
       ["XII 10", "whole line", "Milik 1960 (item 64)", "", "'the tunnel in the Smooth Rock to the north of Kohlit, which opens towards the north'", "Milik 1960 (via repo findings_log F1.24)", "via repo", "EVIDENCE"],
       ["XII 10", "second word", "Milik preliminary (1956–57), reported by Lefkovits as 'Milik (org.)'", "בחלה", "(early reading)", "via repo findings_log F2.5", "via repo", "EVIDENCE"],
       ["XII 10", "second word", "Puech 2002", "שבנה", "(earlier reading)", "via " + READ, "via repo", "EVIDENCE"],
       ["XII 10", "second word", "Puech 2006", "שכנה", "'situated'; rejects Janoah on the engraving", "Puech 2006 p. 175 n. 49 (via readings.json)", "via repo", "EVIDENCE"],
       ["XII 10", "second word", "Lefkovits 2000; Beyer", "שבינח", "'in Janoah'", "via " + READ, "via repo", "EVIDENCE"],
       ["XII 10", "second word", "Wolters; Allegro", "שכינה", "(gloss not recorded in repo files)", "via " + READ, "via repo", "EVIDENCE"],
       ["XII 10", "second word", "repo plate check 2026 (two blind readers, Puech pl. CCCLXXXI)", "ש + ב/כ + נ-like + fold letter + clear בצפון; no צ, no yod", "fits Puech's 'situated' best; against Milik's Smooth Rock and Lefkovits's Janoah; not decisive", "repo research_text_plate_check.md (XII 10, Q12)", "repo file read", "EVIDENCE"],
       ["XII 10", "whole line (translation)", "Høgenhaven 2016", "", "'I krypten ved den glatte klippe nord for Kohlit, hvis åbning vender mod nord' (in the crypt by the smooth rock north of Kohlit, whose opening faces north)", "Dansk Teologisk Tidsskrift 79 (2016) p. 70 — https://tidsskrift.dk/dtt/article/download/105777/154549/217156", "direct (web)", "EVIDENCE"],
       ["XII 10", "כחלת", "all editions", "כחלת", "Koḥlit (place name secure here)", "via " + READ + " e60-kohlit; tables_phase5_assessments.csv", "via repo", "EVIDENCE"],
       ["XII 10", "פתח אצפון", "Milik 1960", "", "'which opens towards the north'", "via readings.json e60-opening", "via repo", "EVIDENCE"],
       ["XII 10", "פתח אצפון", "Puech", "", "'its opening hidden' (צפון read as 'hidden')", "via readings.json e60-opening", "via repo", "EVIDENCE"],
       ["XII 11", "צפון", "Lefkovits 2000", "prints צפון in XII 11", "listed as an error in the repo findings log", "via readings.json e60-opening", "via repo", "EVIDENCE"],
       ["XII 11", "וקברין על פיה", "CopperScroll project translation", "", "'with tombs at its mouth'", "shared/entries.json", "shared file", "EVIDENCE"],
       ["XII 11", "וקברין על פיה", "Høgenhaven 2016", "", "'med grave ved indgangen' (with graves at the entrance)", "DTT 79 p. 70", "direct (web)", "EVIDENCE"],
       ["XII 11", "וקברין על פיה", "Encyclopaedia Judaica (F. F. Bruce / S. Gibson, 2nd ed.)", "", "'In the pit nearby toward the north, near the graves, in a hole opening to the north'", "https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/copper-scroll", "direct (web)", "EVIDENCE"],
       ["XII 11", "וקברין על פיה", "Wikipedia 'Copper Scroll' (citing Lurie 1964)", "", "'there are buried at its mouth' (participle 'buried', no tomb landmark)", "https://en.wikipedia.org/wiki/Copper_Scroll (fn. citing Lurie 1964)", "direct (web; tertiary)", "EVIDENCE"],
       ["XII 11–13", "משנא הכתב הזא ופרושיו ומשחותיהם ופרוט כל אחד ואחד", "CopperScroll project translation", "", "'a copy of this document, and its explanation, and their measurements, and the details of each and every one'", "shared/entries.json", "shared file", "EVIDENCE"],
       ["XII 11–13", "same", "Høgenhaven 2016", "", "'En afskrift af dette dokument med forklaring, mål og fortegnelse over hver enkelt ting'", "DTT 79 p. 70", "direct (web)", "EVIDENCE"],
       ["XII 11–13", "same", "Encyclopaedia Judaica (Bruce/Gibson)", "", "'a copy of this book, with explanations, measurements and all details'", "encyclopedia.com (EJ 2nd ed.)", "direct (web)", "EVIDENCE"],
       ["XII 11–13", "same", "Wikipedia (citing Lurie 1964)", "", "'a copy of this writing and its interpretation and their measures, with a detailed description of each and every thing'", "https://en.wikipedia.org/wiki/Copper_Scroll", "direct (web; tertiary)", "EVIDENCE"],
       ["XII 11–13", "same", "repo Phase 1 summary", "", "'this last entry holds the duplicate document'; no editor's disagreement over these closing words reported", "via readings.json e60-duplicate", "via repo", "EVIDENCE"],
      ])

write("copy_interpretations.csv",
      ["view", "proponent", "statement", "source", "access", "label", "confidence_if_inference", "search_implication"],
      [
       ["Duplicate of the list", "L. H. Schiffman (1994)", "'the Copper Scroll does mention that a copy of itself was deposited in another location'", "Reclaiming the Dead Sea Scrolls (JPS 1994), excerpt at https://cojs.org/the_copper_scroll-_lawrence_h-_schiffman-_reclaiming_the_dead_sea_scrolls-_jewish_publication_society-_philadelphia-_1994/", "direct (web excerpt)", "EVIDENCE", "", "a second inventory text of similar form"],
       ["Duplicate of the list", "repo Phase 1", "'the duplicate document'", "shared/readings.json e60-duplicate", "via repo", "EVIDENCE", "", ""],
       ["Copy with added detail (a key)", "Encyclopaedia Judaica (F. F. Bruce / S. Gibson)", "the entry 'suggests the copper scroll itself contained a reference to a duplicate document containing additional details'", "encyclopedia.com (EJ 2nd ed.)", "direct (web)", "EVIDENCE", "", "expect explanations/measurements beyond the copper text"],
       ["Copy with added detail (a key)", "B. Pixner (ABD 1992, 1:1133–1134)", "'a copy of a more detailed inventory (col. XII, lines 11–13)'", "https://cojs.org/?p=5267", "direct (web transcription)", "EVIDENCE", "", "same"],
       ["Copy with added detail (a key)", "Wikipedia 'Kohlit'", "the second scroll contains 'a more detailed list'", "https://en.wikipedia.org/wiki/Kohlit", "direct (tertiary)", "EVIDENCE", "", "same"],
       ["Companion record of names/identifying details", "S. Gibson 2025/26, Eretz-Israel 36 pp. 32*–48* (as reported)", "'That missing companion scroll may have contained the names, confirmations or identifying details absent from the copper text.'", "Arkeonews, 1 June 2026 — https://arkeonews.net/mysterious-dead-sea-copper-scroll-may-hide-the-financial-secrets-of-a-failed-jewish-revolt/ (Gibson's article not read; wording may be the reporter's)", "secondary (news)", "EVIDENCE", "", "an administrative register; Bar Kokhba-period dating"],
       ["Symbolic/literary", "J. Høgenhaven (2016)", "the book-roll in the last hiding place makes wisdom 'the final or ultimate goal of the addressee's long search' (Danish original quoted in REPORT)", "Dansk Teologisk Tidsskrift 79 (2016) p. 70", "direct (web)", "EVIDENCE", "", "no physical target implied"],
       ["Lexical: idiom for a copy", "this registry", "משנא הכתב הזא has the same construction as Deut 17:18 משנה התורה הזאת ('a copy of this Teaching', JPS 2023); the root ש-נ-ה can mean 'repeat (copy)' and 'change' (Fraade). The noun alone therefore means 'copy'; the three following nouns name content beyond a duplicate (explanation, measurements, particulars), i.e. copy + key.", "Deut 17:18 via https://www.sefaria.org/api/texts/Deuteronomy.17.18 ; S. Fraade, 'The Second Torah', https://www.thetorah.com/article/the-second-torah", "direct (web)", "INFERENCE", "medium", "the deposit should be longer than the copper text; durable material not implied"],
       ["Material survival", "this registry", "If the copy were on copper it would likely survive; on parchment/papyrus survival depends on a dry, sealed setting (pit mouth in a cemetery is not obviously such).", "reasoning only", "", "INFERENCE", "low", "favours targets with dry rock-cut shafts"],
      ])

write("kohlit_proposals.csv",
      ["proposal", "proponents", "reasons_given", "sources", "access", "repo_status", "in_gazetteer_place_id", "entry60_target_id", "notes"],
      [
       ["Tell es-Sultan (Old Jericho), north of Hasmonaean/Herodian Jericho", "É. Puech (2006, 2015) 'à titre d'hypothèse'; J. Høgenhaven (2016 as one option; 2020 only if Achor = Wadi Nuweiʿimeh)",
        "an ancient tell (entry 4 'tel'); abundant spring at its east foot (entry 11 pool east); cemetery north/west with Qumran-type graves on the north side (Kenyon)",
        "Puech 2006 p. 175 n. 49; Puech 2015 pp. 13–14 n. 49; Høgenhaven 2016 DTT 79 p. 72 n. 22; Høgenhaven 2020 p. 89", "Puech/Høgenhaven 2020 via repo; Høgenhaven 2016 direct", "possible, low (leading working hypothesis)", "tell_es_sultan", "P60-T1", ""],
       ["ʿEin Kohel near Mount Carmel", "J. T. Milik (1962)", "name of a spring in the medieval Massekhet Kelim (Treatise of the Vessels)", "Milik DJD III pp. 274–275, 280–281 (via Høgenhaven 2016 p. 72 n. 22, citing also Davila 2013 p. 400 n. 22); Puech 2015 pp. 13–14 calls it doubtful (via repo cycle7)", "secondary", "unresolved", "", "P60-T6", "spring not located in sources read"],
       ["Transjordan (an area east of the Jordan)", "S. Goranson (1992; 2002)", "b. Qiddushin 66a: Yannai went to Koḥalit 'in the desert' and conquered sixty cities; Jannaeus's campaigns", "Goranson JJS 43 (1992) 282–287; Goranson in Copper Scroll Studies (2002) 226–232 at p. 231 (via Cook, Scriptura 88 (2005) 225–229); Wikipedia 'Kohlit'", "secondary", "unresolved", "", "P60-T5", "no site named"],
       ["ʿEin Samiya / Wadi Kuḥeila, Samarian desert ('Tel Kakhelet')", "B. Zissu (2001)", "modern name resemblance (Kuḥeila); desert setting; depends first on Lefkovits's Yanoaḥ reading at XII 10 (per Puech)", "Zissu PEQ 133 (2001) 145–158; Zissu JSRS 10 (2001) 119–136 (Hebrew); Puech 2015 p. 14 (via repo cycle7); BibleWalks (popular)", "bibliographic only; PEQ page 403", "conditional; disputed textual premise", "", "P60-T3", "Wikipedia village coordinate 31°59′21″N 35°20′00″E (external, village-level)"],
       ["'In the desert', unidentified", "H. Eshel (2002)", "cannot be identified; b. Qid 66a desert setting", "Eshel, Copper Scroll Studies pp. 99–100, 106 (via readings.json)", "via repo", "—", "", "", ""],
       ["Between ʿAyn el-Ghuweir and ʿAyn et-Turabeh (western Dead Sea shore)", "Tübingen Bible Atlas (TAVO) sheet B V 18", "cartographic placement (rationale unread)", "Puech 2015 p. 14 (via repo cycle7); Puech objects: no tell, freshwater abundance", "via repo; sheet uninspected", "published cartographic proposal", "", "P60-T2", ""],
       ["ʿAyn Feshkha", "proposer not identified in sources read", "spring/water installations", "Puech 2015 p. 14 rejects it (no tell) (via repo cycle7)", "via repo", "weaker feature-class proposal", "", "P60-T7", ""],
       ["Qumran–Buqeia district", "repo sequence study (not a published proposal)", "Koḥlit and ha-Melaḥ share a 'north' frame; district-level", "repo research_text_deeper_analysis_2026-09-30 §2.1; cycle7", "repo file", "regional alternative, unranked", "", "P60-T4", "do not merge with Sekakah = Qumran"],
       ["Pixner's grouping (implicit)", "B. Pixner (ABD 1992)", "groups Milik items 1–17 'near the Essene Gate on the SW hill' of Jerusalem, 19–34 around Qumran, 61–64 'at diverse locations in the N'", "ABD 1:1133–1134 via https://cojs.org/?p=5267", "direct (web transcription)", "—", "", "", "INFERENCE (low): Milik items 4 and 12 (Koḥlit) fall in his Jerusalem group, Milik 21 (P19) in the Qumran group and Milik 64 (P60) in the northern group; Pixner's explicit Koḥlit discussion (RevQ 11, 1983) not read"],
       ["Jordan River area (blog)", "R. Glick (Times of Israel blog)", "title only: 'Kahlat and the hidden archive of section 60 – Jordan River and Copper Scroll'", "https://blogs.timesofisrael.com/kahlat-and-the-hidden-archive-of-section-60-jordan-river-and-copper-scroll/", "body not served to the fetcher", "not scholarly", "", "", "recorded for completeness only"],
      ])

write("kohlit_joint_constraints.csv",
      ["entry", "lines", "feature", "direction_clause", "anchor_of_direction", "reading_status", "source"],
      [
       ["4", "I 9–12", "tell/mound; conduit; opening at its edge; immersion cleft (Milik) or frigidarium (Puech) 6 cubits away", "opening at the edge of the conduit 'on the north'", "the conduit", "Koḥlit secure; landmark words disputed", "shared/entries.json; readings.json e4-*"],
       ["11", "II 13–15", "pool with corners; dig 4 cubits", "pool 'east of Koḥlit'; 'northern corner'", "Koḥlit; internal pool corner", "secure", "readings.json e11-*"],
       ["15", "IV 1–2", "great cistern; pillar", "[north(?) of Ko]ḥlit (restored); pillar 'on its north side'", "Koḥlit (restored); the cistern", "restored (Milik read …QH)", "readings.json e15-kohlit"],
       ["16", "IV 3–5", "conduit going to [pool?]; 14/40/41 cubits", "none", "—", "no place name; link to Koḥlit contextual (Puech)", "readings.json e16-*; cycle7"],
       ["19", "IV 11–12", "'the eastern pit' (implies ≥2 pits)", "'north of Koḥlit'; 'eastern'", "Koḥlit; pit group", "secure (Allegro 'hole')", "readings.json e19-*"],
       ["60", "XII 10–13", "pit; opening north (Milik) or hidden (Puech); tombs (or 'buried') at its mouth; copy of the document", "'north of Koḥlit'; opening 'north'", "Koḥlit; the pit mouth", "Koḥlit secure; others disputed", "readings.json e60-*; plate_check"],
      ])
print("ok")

write("kohlit_context_and_access.csv",
      ["kind", "item", "content", "source", "label", "confidence_if_inference"],
      [
       ["attestation", "b. Qiddushin 66a", "מַעֲשֶׂה בִּינַאי הַמֶּלֶךְ שֶׁהָלַךְ לְכוּחְלִית שֶׁבַּמִּדְבָּר, וְכִיבֵּשׁ שָׁם שִׁשִּׁים כְּרַכִּים — King Yannai 'went to Koḥalit in the desert and conquered sixty cities there'", "https://www.sefaria.org/api/texts/Kiddushin.66a", "EVIDENCE", ""],
       ["attestation", "m. Parah 11:7", "אֵזוֹב כּוֹחֲלִית ('Koḥalit hyssop', invalid for the rite) — gives no location", "https://www.sefaria.org/api/texts/Mishnah_Parah.11.7", "EVIDENCE", ""],
       ["context", "Høgenhaven 2016 p. 72", "Koḥlit is 'det hyppigst forekommende toponym i 3Q15' (the most frequent toponym in 3Q15)", "DTT 79 (2016) p. 72", "EVIDENCE", ""],
       ["context", "Høgenhaven 2016 p. 72", "'Ved de første to besøg passeres Kohlit på vejen såvel derhen som derfra; dette sted synes at fungere som slags base eller tilflugtssted uden for Jerusalem' (on the first two visits Kohlit is passed going and returning; it seems to function as a base or refuge outside Jerusalem)", "DTT 79 (2016) p. 72", "EVIDENCE", ""],
       ["context", "Høgenhaven 2016 p. 70", "'Ved at være repræsenteret gennem bogrullen i det sidste gemmested, der beskrives, bliver visdommen på en måde det endelige eller ultimative mål for adressatens lange søgen' (symbolic reading of the final deposit)", "DTT 79 (2016) p. 70", "EVIDENCE", ""],
       ["context", "repo sequence study", "All five Koḥlit entries say 'north' (hypergeometric p = 1.3e-4); north occurs in 6 of 7 Koḥlit/ha-Melaḥ entries in 1–19 vs 0 of 13 others (Fisher p = 1.8e-4)", "repo research_text_deeper_analysis_2026-09-30.md §2.1", "EVIDENCE", ""],
       ["context", "repo cycle7 qualification", "each 'north' attaches to its own anchor (conduit edge, pool corner, cistern pillar); only 19 and 60 put a feature north of Koḥlit", "downloads/research_measurements_cycle7_kohlit_pool.md", "EVIDENCE", ""],
       ["inference", "joint constraints", "Koḥlit must combine: a tell/ruin-mound (4), a conduit with an opening 6 c. from an immersion cleft/frigidarium (4), a cornered pool east (11), possibly a great cistern with a pillar (15, restored), ≥2 pits north (19), tombs at one pit's mouth (60 unless 'buried')", "this registry", "INFERENCE", "medium"],
       ["inference", "entry 19 + 60", "entry 60's pit is plausibly the non-eastern member of entry 19's pit group; one survey of the north sector scores P19-A and P60-T1 together", "this registry", "INFERENCE", "low-medium"],
       ["inference", "reading branches", "'north' vs 'hidden' (צפון) and 'tombs' vs 'buried' (קברין) change the physical target; registry scores RB-M, RB-P, RB-L, RB-B separately", "this registry", "INFERENCE", "high"],
       ["inference", "already-failed matches", "recorded features already fail for entry 9 (no cistern 8.5–10 m from the Golden Gate on Warren's plan), 29/Hyrcania (pool sides 15–19 m vs 10.7–12.6 m), 46 (known pool buried before the period): only new observations can confirm these", "this registry, from repo files", "INFERENCE", "high"],
       ["access", "tandfonline (Zissu PEQ 2001)", "HTTP 403; not retrieved by other means", "https://www.tandfonline.com/doi/abs/10.1179/peq.2001.133.2.145", "", ""],
       ["access", "he.wikipedia.org", "cache-only domain; not fetched", "https://he.wikipedia.org/wiki/מגילת_הנחושת", "", ""],
       ["access", "hamichlol.org.il", "robots.txt disallowed", "https://www.hamichlol.org.il/מסכת_כלים_(כלי_המקדש)", "", ""],
       ["access", "archive.org Lefkovits 2000 / Allegro 1960", "lending-restricted items; search-inside returned 'Item not available'; not pursued", "archive.org items copperscroll3q150000lefk, treasureofcopper0000alle", "", ""],
       ["access", "revistas.uam.es (Jericho necropolis article)", "bot wall (Anubis)", "https://revistas.uam.es/isimu/article/download/3701/3939/7228", "", ""],
       ["access", "Times of Israel blog (Glick)", "article body not served to the fetcher", "https://blogs.timesofisrael.com/kahlat-and-the-hidden-archive-of-section-60-jordan-river-and-copper-scroll/", "", ""],
       ["access", "BAS Library (McCarter 1992)", "paywalled", "https://library.biblicalarchaeology.org/article/the-mysterious-copper-scroll", "", ""],
       ["not read", "key primary sources", "Milik DJD III pp. 274–275, 280–281; Puech 2015 pp. 13–14 n. 49 (only via repo); Goranson 1992/2002; Pixner RevQ 11 (1983); Gibson EI 36; Kenyon's Jericho tomb publications; Hachlili & Killebrew PEQ 115 (1983) 109–139 and IAA Reports 7 (1999)", "", "", ""],
      ])
print("context ok")
