#!/usr/bin/env python3
"""Build the T05 attestation concordance (CSV + JSON) from hand-checked records.

Every row was checked against the source named in `source_url` during this
session (Sefaria API texts, CCAT lxxmorph Rahlfs files, Perseus grc2 Josephus
XML, tertullian.org Wolf translation of Eusebius, Schechter-Taylor 1899 on
archive.org, and web pages listed).  `label` is EVIDENCE (what the source says)
or INFERENCE (my reasoning; confidence in `confidence`).  `vs_repo` says whether
the CopperScroll repo (landmark_lexicon_index.csv, findings_log.md,
site_identification_review.md, atlas_text.json) already had it.

Usage: python3 -I scripts/build_concordance.py <outdir>
"""
import csv
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
SEF = 'https://www.sefaria.org/'
CCAT = 'http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/'
PERS = 'https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0526/'
ONOM = 'https://www.tertullian.org/fathers/eusebius_onomasticon_02_trans.htm'

F = ['id', 'name', 'scroll_entries', 'scroll_form', 'attested_form', 'source',
     'reference', 'date', 'quote', 'location_implied', 'name_type', 'label',
     'confidence', 'vs_repo', 'source_url', 'note']

R = []


def add(**k):
    row = {f: k.get(f, '') for f in F}
    row['id'] = f'T05-{len(R) + 1:03d}'
    R.append(row)


# ---------------- KOḤLIT ----------------
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת',
    attested_form='כוחלית (לכוחלית שבמדבר)', source='Babylonian Talmud (baraita)',
    reference='b. Qiddushin 66a', date='baraita (tannaitic attribution); Bavli redacted c. 6th c. CE',
    quote='מעשה בינאי המלך שהלך לכוחלית שבמדבר וכיבש שם ששים כרכים — "King Yannai went to Koḥalit in the wilderness and conquered there sixty towns"',
    location_implied='A district "in the wilderness" containing many towns, conquered by Alexander Jannaeus (103-76 BCE); no direction or distance given',
    name_type='place name (district)', label='EVIDENCE', confidence='high (text); location unknown',
    vs_repo='NEW: not in lexicon (which cites only m. Parah 11:7), findings_log or atlas',
    source_url=SEF + 'Kiddushin.66a.8',
    note='Parallel banquet story in Josephus AJ 13.288-296 is told of John Hyrcanus after the siege of Samaria (AJ 13.275-283) and names no Kohalit (Perseus Niese text checked), so the Talmud\'s place is not derived from Josephus.')
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת',
    attested_form='אזוב כוחלית / כחלת (MSS vary)', source='Mishnah',
    reference='m. Parah 11:7', date='c. 200 CE',
    quote='אזוב יון, אזוב כוחלית, אזוב רומי, אזוב מדברי, פסול — Greek, Koḥalit, Roman and desert hyssop are invalid',
    location_implied='None directly; Jastrow takes it as a hyssop named after the district; could also be "kohl-like" (eye-paint) hyssop',
    name_type='adjective; place-derived or common noun (ambiguous)', label='EVIDENCE', confidence='high (text)',
    vs_repo='KNOWN (lexicon: m. Parah 11:7)', source_url=SEF + 'Mishnah_Parah.11.7')
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת',
    attested_form='אזוב כוחלי / כוחלת', source='Mishnah; Bavli baraita',
    reference='m. Negaim 14:6; b. Sukkah 13a; b. Hullin 62b', date='c. 200-600 CE',
    quote='לא אזוב יון, לא אזוב כוחלי ... ולא כל אזוב שיש לו שם לווי — "not Greek hyssop, not Koḥali hyssop ... nor any hyssop with a qualifying name"',
    location_implied='None; "Koḥali" is one of several qualifying epithets (Greek, Roman, desert)',
    name_type='adjective (ambiguous)', label='EVIDENCE', confidence='high (text)',
    vs_repo='PARTLY NEW (lexicon counts 1 of 2 Mishnah hits)', source_url=SEF + 'Mishnah_Negaim.14.6')
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת', attested_form='כּוֹחֲלִית',
    source='Jastrow, Dictionary (1903), s.v.', reference='Jastrow s.v. כּוֹחֲלִית (Sefaria lexicon API)', date='1903 (secondary)',
    quote='"Koḥălith, a district conquered by John Hyrcan, [perh. = נפח Num. XXI, 30 ...]. Kidd. 66a ... אזוב כ׳ a species of hyssop named after that district"',
    location_implied='Jastrow guesses Moabite Nophah (Num 21:30), i.e. Transjordan; no evidence given',
    name_type='place name', label='EVIDENCE (of a modern opinion)', confidence='low (opinion)',
    vs_repo='NEW', source_url=SEF + 'api/words/כוחלית')
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת', attested_form='כחלת (verb)',
    source='Hebrew Bible', reference='Ezek 23:40', date='6th c. BCE',
    quote='כחלת עיניך — "you painted your eyes"', location_implied='none', name_type='common verb (homograph, not a place)',
    label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon flags it as a false hit)', source_url=SEF + 'Ezekiel.23.40')
add(name='Kohlit', scroll_entries='4 11 15 19 60', scroll_form='כחלת', attested_form='כוחלית = scroll כחלת?',
    source='inference', reference='b. Qid 66a vs scroll entries 4/11/15/19/60', date='',
    quote='', location_implied='If the scroll\'s Koḥlit is the Talmud\'s Koḥalit, it is a desert district with many settlements outside Hasmonean territory before Jannaeus, not a single tell inside Judaea such as Tell es-Sultan (Jericho was Judaean long before Jannaeus).',
    name_type='', label='INFERENCE', confidence='low-medium (identity of the two names unproven: spelling differs, כחלת vs כוחלית)',
    vs_repo='NEW', note='Weakens, but does not exclude, Puech\'s tentative Tell es-Sultan; the scroll\'s own "tell of Koḥlit" (I 9) and "tombs at its mouth" (XII 11) need a settlement-scale place inside a wider district.')

# ---------------- SEKAKAH ----------------
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא / הסככא',
    attested_form='סככה (וּסְכָכָה)', source='Hebrew Bible (MT)', reference='Josh 15:61-62', date='list of Judah towns (Iron Age list; text 1st mill. BCE)',
    quote='במדבר בית הערבה מדין וסככה והנבשן ועיר המלח ועין גדי ערים שש — "In the wilderness: Beth-arabah, Middin, Secacah, Nibshan, the City of Salt and En-gedi: six towns"',
    location_implied='Wilderness of Judah district; listed between Middin and Nibshan, before City of Salt and En-gedi (the list runs roughly north to south from Beth-arabah to En-gedi)',
    name_type='place name', label='EVIDENCE', confidence='high (text)', vs_repo='KNOWN (lexicon: Josh 15:61)', source_url=SEF + 'Joshua.15.61-62')
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='וּסְכָכָה', source='Targum Jonathan to the Prophets',
    reference='Tg. Josh 15:61', date='c. 2nd-5th c. CE (Babylonian redaction)',
    quote='בְּמַדְבְּרָא בֵּית מֵישְׁרָא מִדִין וּסְכָכָה', location_implied='none beyond MT; the name is kept, not glossed', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=SEF + 'Targum_Jonathan_on_Joshua.15.61')
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='Σοχοχα (A); Αιχιοζα (B)', source='Septuagint (Rahlfs, CCAT lxxmorph)',
    reference='LXX Josh 15:61 (JoshA / JoshB)', date='Greek translation, c. 2nd-1st c. BCE',
    quote='A: Βαδδαργις καὶ Βηθαραβα καὶ Μαδων καὶ Σοχοχα; B: καὶ Βαδδαργις καὶ Θαραβααμ καὶ Αινων καὶ Αιχιοζα',
    location_implied='none (same list); A preserves a form close to Sekakah, B is corrupt', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=CCAT + '08.JoshA.mlxx')
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='(no entry)', source='Eusebius, Onomasticon (Wolf tr.)',
    reference='Section S (Joshua), searched', date='early 4th c. CE',
    quote='no Secacah/Sochocha entry; nearest Joshua-Judah entries are Sachoron, Sama, Soual', location_implied='none',
    name_type='', label='EVIDENCE (negative)', confidence='medium (translation searched, not Klostermann Greek)', vs_repo='KNOWN (lexicon: Onomasticon 0)', source_url=ONOM)
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='סְכָכָה "covering"', source='Mishnah/Talmud',
    reference='b. Sukkah 6b, 12b; Jastrow s.v. סְכָכָה', date='c. 200-600 CE',
    quote='סככה בעיא קרא — "covering [of a sukkah] needs a verse"', location_implied='none', name_type='common noun (homograph)',
    label='EVIDENCE', confidence='high', vs_repo='NEW (negative check)', source_url=SEF + 'Sukkah.6b.12',
    note='344 Sefaria hits for סככה are all the sukkah-covering noun; no rabbinic place Secacah found.')
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='תרע סכותה "Gate of Sakkutha"', source='Rehov synagogue inscription (via Wikipedia translation after Sussmann)',
    reference='Rehov mosaic, Beth Shean section', date='6th-7th c. CE',
    quote='"from the north, that is to say, the Gate of Sakkūtha extending as far as Kefar Ḳarnos"', location_implied='a gate of Beth Shean (north side)',
    name_type='place name, but not Secacah', label='EVIDENCE', confidence='medium (secondary translation)', vs_repo='NEW (negative)',
    source_url='https://en.wikipedia.org/wiki/Mosaic_of_Rehob', note='Shared root skk/sukkot only; not a match.')
add(name='Sekakah', scroll_entries='20 21 22 24', scroll_form='סככא', attested_form='עמק סכות "Valley of Sukkot"', source='Bereshit Rabbah',
    reference='Gen. Rab. 42:5', date='c. 5th c. CE',
    quote='שלשה שמות נקראו לו, עמק השדים, עמק שוה, עמק סכות ... עמק סכות שהוא מסוכך באילנות ... הוא ים המלח',
    location_implied='the Dead Sea valley (Siddim), homiletically "covered (mesukkakh) with trees"', name_type='homiletic name; root skk only',
    label='EVIDENCE', confidence='high (text); no value as geography', vs_repo='NEW', source_url=SEF + 'Bereshit_Rabbah.42.5',
    note='Not the name Secacah; recorded because it applies the root skk ("covered") to a Dead Sea valley.')

# ---------------- HA-MELAḤ ----------------
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח / במלחמ', attested_form='עיר המלח', source='Hebrew Bible (MT)', reference='Josh 15:62',
    date='as above', quote='והנבשן ועיר המלח ועין גדי', location_implied='desert district of Judah, between Nibshan and En-gedi; after Secacah',
    name_type='place name (compound)', label='EVIDENCE', confidence='high', vs_repo='KNOWN (Lefkovits p. 183 via findings_log F12.1)', source_url=SEF + 'Joshua.15.62')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='קִרְיַת מֶלַח', source='Targum Jonathan', reference='Tg. Josh 15:62', date='c. 2nd-5th c. CE',
    quote='וְנִבְשָׁן וְקִרְיַת מֶלַח וְעֵין גֶדִי', location_implied='same', name_type='place name', label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=SEF + 'Targum_Jonathan_on_Joshua.15.62')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='αἱ πόλεις ἁλῶν (A); αἱ πόλεις Σαδωμ (B)', source='Septuagint (Rahlfs)',
    reference='LXX Josh 15:62', date='c. 2nd-1st c. BCE',
    quote='A: καὶ Νεβσαν καὶ αἱ πόλεις ἁλῶν καὶ Ηνγαδδι; B: καὶ Ναφλαζων καὶ αἱ πόλεις Σαδωμ καὶ Ανκαδης',
    location_implied='B renders "City of Salt" as "the cities of Sodom", i.e. reads it as the salt/Sodom zone of the Dead Sea', name_type='place name (translated)',
    label='EVIDENCE', confidence='high', vs_repo='NEW', source_url=CCAT + '07.JoshB.mlxx')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='ים המלח / ימא דמלחא', source='Bible; Targums',
    reference='Gen 14:3; Num 34:3, 12; Josh 15:2, 5; 18:19; Onq. Gen 14:3', date='various',
    quote='עמק השדים הוא ים המלח', location_implied='the Dead Sea', name_type='place name (compound)', label='EVIDENCE', confidence='high',
    vs_repo='NEW (as a candidate expansion of bare "ha-Melaḥ")', source_url=SEF + 'Genesis.14.3')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='גיא (ה)מלח', source='Hebrew Bible', reference='2 Sam 8:13; 2 Kgs 14:7; 2 Chr 25:11; Ps 60:2',
    date='', quote='וילך גיא המלח ויך את בני שעיר', location_implied='Valley of Salt in an Edomite war context (far south); not near Jericho/Jerusalem',
    name_type='place name (compound)', label='EVIDENCE', confidence='high', vs_repo='NEW (negative for location)', source_url=SEF + 'II_Chronicles.25.11')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='מלח דזרכאיי', source='Baraita of the Boundaries',
    reference='y. Shevi\'it 6:1 (36c)', date='c. 3rd-4th c. CE text',
    quote='וטרכונא דמתחם לבוצרא ומלח דזרכאיי ונמרין', location_implied='a boundary point in Transjordan (Trachonitis/Bostra sector)',
    name_type='place name element', label='EVIDENCE', confidence='high (text)', vs_repo='NEW (irrelevant location)', source_url=SEF + 'Jerusalem_Talmud_Sheviit.6.1')
add(name='ha-Melah', scroll_entries='6 13 14', scroll_form='המלח', attested_form='bare "ha-Melaḥ" as a settlement name', source='inference',
    reference='all hits above', date='', quote='',
    location_implied='No period text uses bare המלח as the name of a settlement; every toponym is compound (City of / Sea of / Valley of / Tel). As a toponym the scroll\'s form would be a short form, most naturally of ʿIr ha-Melaḥ (Lefkovits) or of the Dead Sea shore; the common-noun readings remain open.',
    name_type='', label='INFERENCE', confidence='medium', vs_repo='PARTLY NEW (sharpens F12.1)')

# ---------------- ACHOR ----------------
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='עמק עכור', source='Hebrew Bible', reference='Josh 15:7',
    date='', quote='ועלה הגבול דברה מעמק עכור וצפונה פנה אל הגלגל אשר נכח למעלה אדמים',
    location_implied='On Judah\'s northern border, west of the Jordan mouth, before the line turns north to Gilgal opposite the Ascent of Adummim: south-west of Jericho, not north of it',
    name_type='place name', label='EVIDENCE', confidence='high (text); exact line disputed', vs_repo='KNOWN (lexicon: Josh 15:7; repo debates Buqeia vs Wadi Nuweiʿimeh)', source_url=SEF + 'Joshua.15.7')
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='φάραγξ Αχωρ; Εμεκαχωρ', source='Septuagint (Rahlfs B)', reference='LXX Josh 7:24, 26; 15:7',
    date='', quote='εἰς φάραγγα Αχωρ ... εἰς Εμεκαχωρ; ἐπὶ τὸ τέταρτον τῆς φάραγγος Αχωρ', location_implied='none new; ʿemeq rendered "ravine"',
    name_type='place name', label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=CCAT + '07.JoshB.mlxx')
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='מֵישַׁר עָכוֹר', source='Targum Jonathan', reference='Tg. Josh 7:26; 15:7; Isa 65:10; Hos 2:17',
    date='', quote='מִמֵישַׁר עָכוֹר וְצִפּוּנָא מִתְפְּנֵי לְגִלְגָלָא', location_implied='same as MT; ʿemeq rendered "plain"; no gloss', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=SEF + 'Targum_Jonathan_on_Joshua.15.7')
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='Achōr / Emekachōr', source='Eusebius, Onomasticon', reference='Wolf no. 49; Klostermann 18.17-20, 84.18-20',
    date='early 4th c. CE', quote='"north of Jericho"; "near Jericho ... beside Galgala"; locals still use the name',
    location_implied='north of Jericho, near Gilgal', name_type='place name', label='EVIDENCE', confidence='high', vs_repo='KNOWN (findings_log F2.2)', source_url=ONOM)
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='(none)', source='Josephus (Niese Greek); Madaba map labels (ToposText list); rabbinic corpus',
    reference='AJ 5.33-44 (Achar the man only); ToposText work 788; m. Sanh. 6:2, b. Sanh. 43b-44b (wordplay only)', date='',
    quote='Ἄχαρος ... (person); no Achor label in ToposText\'s Madaba list', location_implied='none', name_type='', label='EVIDENCE (negative)',
    confidence='medium (Madaba list may be incomplete)', vs_repo='PARTLY KNOWN (F2.6 for Josephus)', source_url='https://topostext.org/work/788')
add(name='Achor', scroll_entries='1 17', scroll_form='עמק עכור', attested_form='two traditions', source='inference', reference='Josh 15:7 vs Eusebius',
    location_implied='The period texts preserve two incompatible placements (biblical boundary SW of Jericho; 4th-c. tradition N of Jericho). No text closer in date to the scroll (2nd c. BCE-1st c. CE) was found that chooses between them.',
    label='INFERENCE', confidence='medium', vs_repo='KNOWN in substance (repo: Achor unresolved)')

# ---------------- DOQ ----------------
add(name='Doq', scroll_entries='31', scroll_form='דוק', attested_form='Δωκ', source='1 Maccabees (Rahlfs, CCAT)', reference='1 Macc 16:11, 14-16',
    date='late 2nd c. BCE (Greek tr. of Hebrew original)',
    quote='ὑπεδέξατο αὐτοὺς ... εἰς τὸ ὀχυρωμάτιον τὸ καλούμενον Δωκ μετὰ δόλου ὃ ᾠκοδόμησεν — "received them ... into the little fortress called Dok, which he had built"',
    location_implied='a small fort built by Ptolemy son of Abubus, governor of the plain of Jericho (16:11); Simon went down to Jericho (16:14)', name_type='place name (fortress)',
    label='EVIDENCE', confidence='high', vs_repo='KNOWN (cited via Elitzur in findings_log); Greek text now quoted', source_url=CCAT + '24.1Macc.mlxx')
add(name='Doq', scroll_entries='31', scroll_form='דוק', attested_form='Δαγών', source='Josephus (Niese, Perseus grc2)', reference='AJ 13.230; BJ 1.56 (Niese numbering)',
    date='late 1st c. CE', quote='εἴς τι τῶν ὑπὲρ Ἱεριχοῦντος ἐρυμάτων, ὃ Δαγὼν καλεῖται — "to one of the fortresses above Jericho, which is called Dagon"',
    location_implied='a fortress above (overlooking) Jericho', name_type='place name (fortress)', label='EVIDENCE', confidence='high',
    vs_repo='KNOWN (lexicon cites AJ 13.230 and "BJ 1.54 (eng)"; Niese numbering is BJ 1.56)', source_url=PERS + 'tlg004/tlg0526.tlg004.perseus-grc2.xml')
add(name='Doq', scroll_entries='31', scroll_form='דוק', attested_form='Douka (laura)', source='CMHL record "Deir el-Quruntul - DOUKA" (secondary)', reference='dig.corps-cmhl.huji.ac.il/node/566',
    date='Byzantine laura; record modern', quote='"The laura founded there was named \'Douka\' after the name of the Second Temple fortress of Doq-Dagon located above it."',
    location_implied='Jebel Qarantal (Mount of Temptation) above Jericho', name_type='place name', label='EVIDENCE (secondary)', confidence='medium',
    vs_repo='KNOWN in substance (Eshel; entry 31 shortlist)', source_url='https://dig.corps-cmhl.huji.ac.il/node/566')
add(name='Doq', scroll_entries='31', scroll_form='דוק', attested_form='(none)', source='rabbinic corpus (Sefaria)', reference='queries דוק / בדוק / לדוק',
    quote='hits are the verb "examine/pound" and the noun "eye spot"', location_implied='none', name_type='homograph', label='EVIDENCE (negative)',
    confidence='medium (homograph noise; not every hit read)', vs_repo='NEW (negative)', source_url=SEF + 'api/words/דוק')

# ---------------- KOZEBA ----------------
add(name='Kozeba', scroll_entries='32', scroll_form='הכוזבא', attested_form='כֹזֵבָא; Χωζηβα', source='Hebrew Bible; LXX', reference='1 Chr 4:22',
    date='', quote='ויוקים ואנשי כזבא ויואש ושרף — LXX: καὶ ἄνδρες Χωζηβα', location_implied='a Judahite clan/place in the Shelah genealogy (Judah), not Wadi Qelt',
    name_type='place name (gentilic "men of")', label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon; Milik: a different place)', source_url=SEF + 'I_Chronicles.4.22')
add(name='Kozeba', scroll_entries='32', scroll_form='הכוזבא', attested_form='בן/בר כוזיבא, כוזבא, כוזבה', source='Tosefta; Yerushalmi; Bavli; midrash',
    reference='t. Shabbat 15:9 (Lieberman); y. Taanit 4:5; b. Sanhedrin 93b, 97b; Lam. Rab. 2:4', date='c. 3rd-6th c. CE',
    quote='הרבה מלו בימי בן כוזבא — "many were circumcised [again] in the days of Ben Koziba"', location_implied='none (personal name of the revolt leader)',
    name_type='personal name (patronymic)', label='EVIDENCE', confidence='high', vs_repo='NEW',
    source_url=SEF + 'Tosefta_Shabbat_(Lieberman).15.9', note='Rabbinic spelling כוזבא = scroll\'s כוזבא (with article ה-). Documentary letters spell כוסבה/כוסבא (secondary: Wikipedia "Simon bar Kokhba").')
add(name='Kozeba', scroll_entries='32', scroll_form='הכוזבא', attested_form='בית כוזבא (valley of Beth Kuzevah)', source='Midrash Tanhuma', reference='Tanhuma Huqqat 1; Jastrow s.v. כּוֹזְבָא sense 2',
    date='c. 5th-9th c. CE', quote='"a certain reaper who stood and reaped in the valley of Beth-Kuzevah" (Sefaria English)',
    location_implied='none; Jastrow lists parallel readings טופח, תופת, בי טרפא, בית שופרי, נטופא — the name is textually unstable', name_type='place name (unstable)',
    label='EVIDENCE', confidence='high (text); no geographic value', vs_repo='NEW', source_url=SEF + 'Midrash_Tanchuma,_Chukat.1')
add(name='Kozeba', scroll_entries='32', scroll_form='הכוזבא', attested_form='Chasbi', source='Eusebius, Onomasticon', reference='Wolf no. 948 (Gen 38:5 Chezib)',
    date='early 4th c. CE', quote='"Where the wife of Juda bore a son. A deserted place ... in the region of Eleutheropolis near Odollam"', location_implied='Shephelah near Adullam',
    name_type='place name (different place)', label='EVIDENCE', confidence='high', vs_repo='NEW (negative)', source_url=ONOM)
add(name='Kozeba', scroll_entries='32', scroll_form='הכוזבא', attested_form='—', source='inference', reference='',
    location_implied='No pre-Byzantine text puts a place Kozeba in Wadi Qelt; the Choziba link rests on the later monastery name. The scroll\'s article (ה-כוזבא) suggests a descriptive name ("the deceiving [spring/stream]", cf. אכזב "failing wadi") rather than a town.',
    label='INFERENCE', confidence='low-medium', vs_repo='PARTLY NEW')

# ---------------- HAQQOZ ----------------
add(name='Haqqoz', scroll_entries='30', scroll_form='בית הקץ', attested_form='הקוץ (priestly family)', source='Hebrew Bible', reference='1 Chr 24:10; Ezra 2:61; Neh 7:63; Neh 3:4, 21',
    date='Persian period texts', quote='בני הקוץ; מרמות בן אוריה בן הקוץ', location_implied='a priestly family active in Jerusalem (wall repairs near the high priest\'s house); no estate located',
    name_type='family name', label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon)', source_url=SEF + 'Nehemiah.3.21')
add(name='Haqqoz', scroll_entries='30', scroll_form='בית הקץ', attested_form='מרמות בן אוריה הכהן', source='Hebrew Bible', reference='Ezra 8:33',
    date='', quote='נשקל הכסף והזהב והכלים בבית אלהינו על יד מרמות בן אוריה הכהן — "the silver, gold and vessels were weighed in the house of our God into the hand of Meremoth son of Uriah the priest"',
    location_implied='Jerusalem Temple', name_type='personal name (Hakkoz family, via Neh 3:4)', label='EVIDENCE', confidence='high (text)',
    vs_repo='NEW', source_url=SEF + 'Ezra.8.33', note='Meremoth son of Uriah = Meremoth son of Uriah son of Hakkoz (Neh 3:4, 21): the family received Temple silver, gold and vessels.')
add(name='Haqqoz', scroll_entries='30', scroll_form='בית הקץ', attested_form='Ἀκκως', source='1 Maccabees', reference='1 Macc 8:17',
    date='c. 161 BCE events', quote='τὸν Εὐπόλεμον υἱὸν Ἰωάννου τοῦ Ἀκκως', location_implied='none', name_type='family name',
    label='EVIDENCE', confidence='high', vs_repo='NEW', source_url=CCAT + '24.1Macc.mlxx', note='Shows the Hakkoz family still prominent in the Hasmonean period.')
add(name='Haqqoz', scroll_entries='30', scroll_form='בית הקץ', attested_form='בית הקוץ (0 hits); הקוץ = "the thorn"', source='rabbinic corpus (Sefaria)', reference='queries הקוץ, בית הקוץ',
    quote='המצניע את הקוץ ... (m. Bava Kamma 3:2)', location_implied='none', name_type='common noun (homograph)', label='EVIDENCE (negative)', confidence='high',
    vs_repo='NEW (negative)', source_url=SEF + 'Mishnah_Bava_Kamma.3.2')
add(name='Haqqoz', scroll_entries='30', scroll_form='בית הקץ', attested_form='—', source='inference', reference='Ezra 8:33 + Neh 3:4 + 1 Macc 8:17',
    location_implied='"House of Haqqoz" as a property of the priestly Hakkoz family fits a Temple-treasure context (the family handled Temple silver and gold), but no period text locates any Hakkoz estate; Tell el-Qos rests on sound-likeness only.',
    label='INFERENCE', confidence='medium (family reading); location: none', vs_repo='PARTLY NEW')

# ---------------- BET TAMAR ----------------
add(name='Bet Tamar', scroll_entries='43', scroll_form='בית תמר', attested_form='בעל תמר', source='Hebrew Bible', reference='Judg 20:33',
    date='', quote='ויערכו בבעל תמר ואורב ישראל מגיח ממקמו ממערה גבע', location_implied='near Gibeah/Geba (Benjamin), north of Jerusalem',
    name_type='place name', label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon)', source_url=SEF + 'Judges.20.33')
add(name='Bet Tamar', scroll_entries='43', scroll_form='בית תמר', attested_form='Baalthamar ... Beththamar', source='Eusebius, Onomasticon', reference='Wolf no. 268',
    date='early 4th c. CE', quote='"Baalthamar. Near Gaba ... This place (little town) is also (even today) called Beththamar"',
    location_implied='a small town near Gaba, still named Beth-Tamar in the 4th c.', name_type='place name', label='EVIDENCE', confidence='high (translation)',
    vs_repo='KNOWN (lexicon Wolf n. 268; atlas: Milik near Gibeah)', source_url=ONOM, note='Only attestation found of the exact form Beth Tamar outside the scroll.')
add(name='Bet Tamar', scroll_entries='43', scroll_form='בית תמר', attested_form='Messab ... near Gaba', source='Eusebius, Onomasticon', reference='Wolf no. 698',
    date='early 4th c. CE', quote='"Messab. \'Of the heathen\' (enemy city) near Gaba (Gabaa)"', location_implied='Eusebius\'s Gaba is beside the Philistine post (מצב) of 1 Sam 13:23-14:4 at the Michmash pass, i.e. Geba (Jabaʿ)',
    name_type='place name', label='EVIDENCE', confidence='medium (Eusebius uses "Gaba" for more than one site)', vs_repo='NEW', source_url=ONOM)
add(name='Bet Tamar', scroll_entries='43', scroll_form='צוק (פי הצוק של בית תמר)', attested_form='מצוק', source='Hebrew Bible', reference='1 Sam 14:4-5',
    date='', quote='השן האחד מצוק מצפון מול מכמש והאחד מנגב מול גבע — "the one crag rose [matsuq] on the north in front of Michmash, the other on the south in front of Geba"',
    location_implied='a crag-lined gorge (Wadi es-Suweinit) between Michmash and Geba', name_type='landmark term', label='EVIDENCE', confidence='high (text)',
    vs_repo='KNOWN as a lexical parallel (lexicon: tsuq, shen_sela); NOT used geographically for entry 43', source_url=SEF + 'I_Samuel.14.4-5')
add(name='Bet Tamar', scroll_entries='43', scroll_form='בית תמר', attested_form='—', source='inference', reference='Onom. 268 + 698 + 1 Sam 14:4-5',
    location_implied='If the scroll\'s Beth Tamar is Eusebius\'s Beththamar near Gaba (= Geba), a gorge with the scroll\'s word צוק exists next to Geba (the Michmash pass). That answers Puech\'s objection that there is no gorge near Gibeah, but places entry 43 north of Jerusalem, out of line with Puech\'s Tekoa-Herodium sequence for IX 4-X 4.',
    label='INFERENCE', confidence='low', vs_repo='NEW', note='A testable candidate, not an identification.')
add(name='Bet Tamar', scroll_entries='43', scroll_form='בית תמר', attested_form='Thamara; Ḥaṣaṣon-Tamar; "city of palms"', source='Eusebius Onom. no. 8; Madaba map label; 2 Chr 20:2; Deut 34:3; m. Yevamot 16:7',
    reference='as listed', date='', quote='"a village Thamara one day journey from Mapsis ... a garrison"; חצצון תמר היא עין גדי; ירחו עיר התמרים; צוער עיר התמרים',
    location_implied='other "Tamar/palm" names around the Dead Sea: southern Tamar (Arabah), En-gedi, Jericho, Zoar', name_type='place names; תמר is also the common noun "palm"',
    label='EVIDENCE', confidence='high (texts)', vs_repo='NEW', source_url=ONOM, note='Common-noun caution: Beth Tamar may simply mean "palm house/place".')

# ---------------- NETOFAH ----------------
add(name='Netofah', scroll_entries='38', scroll_form='הנטף', attested_form='נטפה; Νετωφα', source='Hebrew Bible; LXX', reference='Ezra 2:21-22; Neh 7:26; 1 Chr 9:16; Neh 12:28',
    date='', quote='אנשי בית לחם ונטפה (Neh 7:26); ומן הככר סביבות ירושלם ומן חצרי נטפתי (Neh 12:28)',
    location_implied='a village paired with Bethlehem; Levite/singer villages "around Jerusalem"', name_type='place name', label='EVIDENCE', confidence='high',
    vs_repo='KNOWN (lexicon)', source_url=SEF + 'Nehemiah.12.28')
add(name='Netofah', scroll_entries='38', scroll_form='הנטף', attested_form='בקעת בית נטופה / בקעת דבית נטופא', source='Mishnah; Bereshit Rabbah', reference='m. Shevi\'it 9:5; Gen. Rab. 79:6',
    date='c. 200-450 CE', quote='עד שיכלו סגריות מבקעת בית נטופה', location_implied='the Beth Netofa valley in Lower Galilee', name_type='place name (different region)',
    label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon, Lefkovits\'s Galilee option)', source_url=SEF + 'Mishnah_Sheviit.9.5')
add(name='Netofah', scroll_entries='38', scroll_form='הנטף', attested_form='זית נטופה', source='Mishnah; Tosefta; Yerushalmi', reference='m. Peah 7:1; t. Peah 3:9 (Lieberman); y. Peah 7:1',
    date='c. 200-400 CE', quote='נטופה נוטף שמן — "Netofah: [an olive] that drips oil" (y. Peah 7:1)', location_implied='none; an olive variety',
    name_type='common noun / variety name from נטף "drip"', label='EVIDENCE', confidence='high', vs_repo='NEW (sense)', source_url=SEF + 'Jerusalem_Talmud_Peah.7.1')
add(name='Netofah', scroll_entries='38', scroll_form='הנטף', attested_form='—', source='inference', reference='',
    location_implied='Rabbinic "Netofah" is Galilean or a variety name; the Judaean Netophah appears only in Ezra-Nehemiah-Chronicles. The scroll\'s articular הנטף ("the drip") reads more naturally as a spring descriptor than as the village name, consistent with the repo\'s ʿAin en-Naṭuf.',
    label='INFERENCE', confidence='medium', vs_repo='CONSISTENT (no change)')

# ---------------- BETH HA-KEREM ----------------
add(name='Beth ha-Kerem', scroll_entries='46', scroll_form='בית הכרם', attested_form='בית הכרם', source='Hebrew Bible', reference='Jer 6:1; Neh 3:14',
    date='', quote='ובתקוע תקעו שופר ועל בית הכרם שאו משאת', location_implied='a signal-height in sight of Tekoa; a district (pelekh) seat', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon)', source_url=SEF + 'Jeremiah.6.1')
add(name='Beth ha-Kerem', scroll_entries='46', scroll_form='בית הכרם', attested_form='Καρεμ (Josh 15:59a); Βηθαχαρμ (Neh 3:14)', source='Septuagint (Rahlfs)', reference='LXX Josh 15:59a; 2 Esdr 13:14',
    date='', quote='Θεκω καὶ Εφραθα αὕτη ἐστὶν Βηθλεεμ ... καὶ Σωρης καὶ Καρεμ καὶ Γαλλιμ καὶ Βαιθηρ', location_implied='Karem in the Tekoa-Bethlehem district (11-town group absent from MT)',
    name_type='place name', label='EVIDENCE', confidence='high (text); identity Karem = Beth-hakkerem probable, not certain', vs_repo='NEW (lexicon lacks LXX)', source_url=CCAT + '08.JoshA.mlxx')
add(name='Beth ha-Kerem', scroll_entries='46 36 37', scroll_form='בית הכרם; השוא', attested_form='בקעת בית כרמא = עמק שוה = עמק מלכא', source='Genesis Apocryphon (1Q20), via Newman 2005 citing Fitzmyer',
    reference='1QapGen XXII 13-14', date='c. 1st c. BCE-1st c. CE (Qumran Cave 1)',
    quote='"while Abram camped in the Valley of Shaveh, which is the Valley of the King, the Valley of Beth Hakerem"',
    location_implied='equates the Valley of Shaveh / King\'s Valley with the valley of Beth-hakkerem; Newman puts it between Ramat Raḥel and Bethlehem',
    name_type='place names', label='EVIDENCE', confidence='high (text, secondary transcription)',
    vs_repo='KNOWN to editors (atlas: Puech p. 194 n. 304 "towards Beth ha-Kerem"; Høgenhaven p. 77) but not as a primary-text entry; Q22 left open',
    source_url='https://www.bsw.org/biblica/vol-86-2005/a-hippodrome-on-the-road-to-ephrath/134/article-p221.html')
add(name='Beth ha-Kerem', scroll_entries='46 36 37', scroll_form='השוא', attested_form='מישר מפנא הוא (אתר) בית ריסא דמלכא', source='Targum Onqelos; Targum Ps.-Jonathan', reference='Onq. and Ps.-J. Gen 14:17',
    date='c. 2nd-5th c. CE', quote='לְמֵישַׁר מַפְנָא הוּא אֲתַר בֵּית רֵיסָא דְמַלְכָּא — "to the plain of Mafna, the place of the king\'s race-course"',
    location_implied='Newman 2005 argues this is a hippodrome on the road to Ephrath (Bethlehem), in the same Beth-hakkerem valley', name_type='place description',
    label='EVIDENCE (text) + secondary interpretation', confidence='high (text); medium (Newman\'s location)', vs_repo='NEW', source_url=SEF + 'Onkelos_Genesis.14.17')
add(name='Beth ha-Kerem', scroll_entries='46', scroll_form='בית הכרם', attested_form='בקעת בית כרם', source='Mishnah', reference='m. Middot 3:4', date='c. 200 CE',
    quote='אחד אבני הכבש ואחד אבני המזבח מבקעת בית כרם', location_implied='source of the altar and ramp stones (implies a Judaean valley within reach of the Temple)',
    name_type='place name', label='EVIDENCE', confidence='high', vs_repo='KNOWN (lexicon)', source_url=SEF + 'Mishnah_Middot.3.4')
add(name='Beth ha-Kerem', scroll_entries='46', scroll_form='בית הכרם', attested_form='בקעת בית כרם', source='Mishnah; Tosefta; Bavli', reference='m. Niddah 2:7; t. Niddah 3:5; b. Niddah 20a',
    date='c. 200-600 CE', quote='מביא אדמה מבקעת בית כרם ... ר\' יהודה אומר מבקעת סכני ר\' יוסי אומר מבקעת יוטבת',
    location_implied='ambiguous: the alternatives offered are Galilean valleys (Sakhnin, Yodfat, Gennesar), and a modern note on Sefaria places this Beth-hakkerem valley near Akko',
    name_type='place name (possibly the Galilean Beit HaKerem valley)', label='EVIDENCE', confidence='high (text)', vs_repo='PARTLY NEW (caution)', source_url=SEF + 'Tosefta_Niddah.3.5')
add(name='Beth ha-Kerem', scroll_entries='46', scroll_form='בית הכרם', attested_form='Bethacharma', source='Jerome, Comm. on Jeremiah 6:1 (as reported by ISBE)', reference='ISBE s.v. Beth-haccherem',
    date='early 5th c. CE (Jerome); 1915 (ISBE)', quote='"a village which he could see daily from Bethlehem"', location_implied='visible from Bethlehem',
    name_type='place name', label='EVIDENCE (secondary)', confidence='low-medium (Latin not checked)', vs_repo='NEW',
    source_url='https://www.bibletools.org/index.cfm/fuseaction/def.show/RTD/ISBE/ID/1409/printer/friendly')

# ---------------- SHAVEH / KING'S VALLEY ----------------
add(name='Shaveh', scroll_entries='36 37 48', scroll_form='השוא; יד אבשלום', attested_form='ἐν τῇ κοιλάδι τῇ βασιλικῇ ... δύο σταδίους ἀπέχουσαν Ἱεροσολύμων', source='Josephus (Niese)',
    reference='AJ 7.243; AJ 1.179', date='93/94 CE',
    quote='Absalom set up "in the King\'s Valley a pillar of marble two stadia from Jerusalem", which he called his own "hand"; (1.179) the king of Sodom met Abram "at a place they call the King\'s Plain"',
    location_implied='a King\'s Valley about 370 m from Jerusalem (contrast 1QapGen\'s Beth-hakkerem valley further south)', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='KNOWN for AJ 7.243 (Absalom); the contrast with 1QapGen is NEW', source_url=PERS + 'tlg001/tlg0526.tlg001.perseus-grc2.xml')
add(name='Shaveh', scroll_entries='36 37 48', scroll_form='השוא; יד אבשלום', attested_form='κοιλὰς Σαυη ... πεδίον βασιλέως; Χεὶρ Αβεσσαλωμ', source='Septuagint (Rahlfs)', reference='LXX Gen 14:17; 2 Sam 18:18',
    date='', quote='εἰς τὴν κοιλάδα τὴν Σαυη τοῦτο ἦν τὸ πεδίον βασιλέως; ἐκάλεσεν τὴν στήλην Χεὶρ Αβεσσαλωμ', location_implied='none beyond MT', name_type='place name',
    label='EVIDENCE', confidence='high', vs_repo='NEW (minor)', source_url=CCAT + '13.2Sam.mlxx')
add(name='Shaveh', scroll_entries='36 37', scroll_form='השוא', attested_form='עמק שוה = עמק השדים = עמק סכות', source='Bereshit Rabbah', reference='Gen. Rab. 42:5',
    date='c. 5th c. CE', quote='שלשה שמות נקראו לו, עמק השדים, עמק שוה, עמק סכות ... הוא ים המלח', location_implied='homiletically identifies Emek Shaveh with the Dead Sea valley',
    name_type='place name (homiletic)', label='EVIDENCE', confidence='high (text); low geographic value', vs_repo='NEW', source_url=SEF + 'Bereshit_Rabbah.42.5')
add(name='Shaveh', scroll_entries='36 37 46 48', scroll_form='השוא; בית הכרם; יד אבשלום', attested_form='—', source='inference', reference='1QapGen XXII 13-14; Onq. Gen 14:17; 2 Sam 18:18; AJ 7.243',
    location_implied='Two ancient placements of the King\'s Valley: (a) near Jerusalem (Absalom\'s pillar 2 stadia out, Josephus) and (b) the Beth-hakkerem valley toward Bethlehem (Genesis Apocryphon). The Genesis Apocryphon is the text closest to the Copper Scroll in date and find-context (Qumran Cave 1 vs Cave 3). On its equation, the scroll\'s Shaveh (36-37) and Beth ha-Kerem (46) are one district south of Jerusalem, which favours Puech\'s placement over Milik\'s Bethso (south-west necropolis).',
    label='INFERENCE', confidence='low-medium', vs_repo='PARTLY NEW (sharpens Q22)')

# ---------------- ʿAṢLA ----------------
add(name='Asla', scroll_entries='18', scroll_form='העצלא', attested_form='(none); עצלה "laziness"', source='Sefaria corpus; Eusebius', reference='queries עצלא, עצלה; Onom. Wolf no. 183 "Asel (Asael). Zachariah mentions this"',
    quote='עצלה תפיל תרדמה (Prov 19:15); "Asel ... Zachariah mentions this" (no location)', location_implied='none', name_type='common noun / unrelated name (Zech 14:5 אצל has א, not ע)',
    label='EVIDENCE (negative)', confidence='medium', vs_repo='KNOWN (lexicon: 0)', source_url=ONOM, note='No period attestation; the name rests on the Arabic toponym Wadi el-ʿAṣla only.')

# ---------------- LANDMARK TERMS ----------------
add(name='ashiah (term)', scroll_entries='22 29 46 55', scroll_form='אשיח / אשוח', attested_form='אשיח', source='Ben Sira, Cairo Genizah MS B (Schechter & Taylor 1899)',
    reference='Sir 50:3 (MS B; = 50:2 in Kahana\'s numbering)', date='c. 190-180 BCE composition',
    quote='MS B אשיח כים בהמונו, translated "A pit (or store) like the sea (?) in its abundance"; editors\' note: read "A pit (or reservoir) like the sea", citing Moabite אשוח (Mesha) "Teich"',
    location_implied='a reservoir dug at the Temple under Simon the High Priest (Jerusalem)', name_type='landmark term (reservoir)', label='EVIDENCE', confidence='medium (OCR of the Hebrew is garbled; Kahana\'s edition prints ושיח)',
    vs_repo='NEW (lexicon gives אשיח 0 attestations)', source_url='https://archive.org/details/wisdomofbensirap00scheuoft',
    note='Gives a 2nd-century BCE Jerusalem use of the scroll\'s reservoir word, in a Temple context.')
add(name='yegar (term)', scroll_entries='20 28 35', scroll_form='יגר', attested_form='יגר שהדותא', source='Baraita of the Boundaries', reference='y. Shevi\'it 6:1 (36c)',
    date='c. 3rd-4th c. CE text', quote='ונחלא דזרד ויגר שהדותא ורקם דגועה', location_implied='a named cairn used as a boundary point in Transjordan (after Gen 31:47)',
    name_type='landmark term used as toponym', label='EVIDENCE', confidence='high (text)', vs_repo='NEW (lexicon has only Gen 31:47)', source_url=SEF + 'Jerusalem_Talmud_Sheviit.6.1')
add(name='Zered (Wolters reading)', scroll_entries='47', scroll_form='גי זרד (Wolters) / גי איך (Milik)', attested_form='נחלא דזרד; Zared',
    source='Baraita of the Boundaries; Rehov inscription; Madaba map', reference='y. Shevi\'it 6:1; Rehov mosaic (Wikipedia tr.); ToposText Madaba no. 030', date='3rd-6th c. CE',
    quote='ונחלא דזרד', location_implied='the Transjordanian Wadi Zered (south-east of the Dead Sea)', name_type='place name', label='EVIDENCE', confidence='high',
    vs_repo='PARTLY KNOWN (lexicon: Onomasticon Zared)', source_url=SEF + 'Jerusalem_Talmud_Sheviit.6.1', note='All period Zereds are Transjordanian; a Zered reading would not fit the Jerusalem setting of entries 46-49.')
add(name='Qobʿeh (Milik reading)', scroll_entries='41', scroll_form='קובעה (Milik) / "hollow" (Puech)', attested_form='קובעיא / קוּבַּעְיָיא דְאַיְיתָא', source='Baraita of the Boundaries',
    reference='y. Shevi\'it 6:1', date='3rd-4th c. CE', quote='וקובעיא ומילתא דביר', location_implied='a boundary point in Upper Galilee', name_type='topographic term used as toponym',
    label='EVIDENCE', confidence='high', vs_repo='NEW (irrelevant location)', source_url=SEF + 'Jerusalem_Talmud_Sheviit.6.1')

# ---------------- JERUSALEM FEATURES ----------------
add(name='Bethesda / two reservoirs', scroll_entries='55', scroll_form='בית אשוחין', attested_form='piscinae gemellares ... Bethsaida', source='Itinerarium Burdigalense', reference='Bordeaux Pilgrim, Jerusalem section',
    date='333 CE', quote='"Interius vero civitati sunt piscinae gemellares, quinque porticus habentes, quae appellantur bethsaida"', location_implied='twin pools inside the city (north of the Temple)',
    name_type='place name + description', label='EVIDENCE', confidence='high', vs_repo='PARTLY NEW (repo: Bethesda medium, twin-pool description)', source_url='https://avande1.sites.luc.edu/jerusalem/sources/bordeauxJerus.htm')
add(name='Absalom\'s monument', scroll_entries='48', scroll_form='יד אבשלום', attested_form='monoliths of Isaiah and Hezekiah', source='Itinerarium Burdigalense', reference='Bordeaux Pilgrim, Kidron valley',
    date='333 CE', quote='"In unum positus est isaias propheta, qui est vere monolitus, et in alio ezechias rex iudaeorum"', location_implied='Kidron valley monuments',
    name_type='monument labels', label='EVIDENCE', confidence='high', vs_repo='CONSISTENT (repo caution: earliest labels name Zacharias)', source_url='https://avande1.sites.luc.edu/jerusalem/sources/bordeauxJerus.htm',
    note='In 333 CE the Kidron monolith was attributed to Isaiah, not Absalom; Josephus\'s Absalom pillar is only "in the King\'s Valley, 2 stadia" from the city.')
add(name='Horon', scroll_entries='40', scroll_form='החורון / החורין', attested_form='Upper and Lower Beth-Ḥoron', source='4Q522 (Apocryphon of Joshua), per Tov', reference='4Q522 frg. 9 i',
    date='1st c. BCE ms.', quote='list includes "Upper and Lower Beth-Ḥoron (Josh 16:3,5)"', location_implied='Beth-Horon pass (Benjamin/Ephraim)', name_type='place name',
    label='EVIDENCE (secondary)', confidence='medium', vs_repo='NEW (minor)', source_url='https://orion.huji.ac.il/symposiums/1st/papers/tov.html')

os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
with open(os.path.join(OUT, 'data', 'attestation_concordance.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=F)
    w.writeheader()
    w.writerows(R)
with open(os.path.join(OUT, 'data', 'attestation_concordance.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(len(R), 'rows')
from collections import Counter
print(Counter(r['name'] for r in R))
print(Counter(r['vs_repo'].split(' ')[0] for r in R))
