"""Prefix-compatibility of the seven Copper Scroll groups with fixed, sourced word lists
representing candidate 'systems'. A group is compatible with a list if some list item,
normalized (no accents, uppercase, final sigma -> Σ), begins with the group.
Lists were fixed before running. Output: data/system_tests.json
"""
import json, unicodedata

GROUPS = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΔΙ', 'ΤΡ', 'ΣΚ']
SENS = {'ΘΕ': ['ΞΕ'], 'ΤΡ': ['ΤΡΙ'], 'ΣΚ': ['ΧΚ', 'ΞΚ']}

def norm(w):
    w = unicodedata.normalize('NFD', w)
    w = ''.join(c for c in w if not unicodedata.combining(c))
    return w.upper().replace('ς', 'Σ').replace('Ϲ', 'Σ')

SYSTEMS = {
    'priestly_courses_LXX_1Chr24': dict(
        source='LXX 1 Chr 24:7-18 as printed at https://www.ellopos.net/elpenor/greek-texts/septuagint/chapter.asp?book=13&page=24',
        items=['Ιωαρίμ', 'Ιεδία', 'Χαρίβ', 'Σεωρίμ', 'Μελχία', 'Μεϊαμίν', 'Κώς', 'Αβία', 'Ιησοῦ', 'Σεχενία',
               'Ελιαβί', 'Ιακίμ', 'Οπφά', 'Ιεσβαάλ', 'Βελγά', 'Εμμήρ', 'Χηζίν', 'Αφεσή', 'Φεταία', 'Εζεκήλ',
               'Αχίμ', 'Γαμούλ', 'Αδαλλαί', 'Μαασαί']),
    'macedonian_months': dict(
        source='https://en.wikipedia.org/wiki/Ancient_Macedonian_calendar (variants included)',
        items=['Δίος', 'Ἀπελλαῖος', 'Αὐδυναῖος', 'Αὐδναῖος', 'Περίτιος', 'Δύστρος', 'Ξανδικός', 'Ξανθικός',
               'Ἀρτεμίσιος', 'Ἀρταμίτιος', 'Δαίσιος', 'Πάνημος', 'Πάναμος', 'Λώιος', 'Γορπιαῖος', 'Ὑπερβερεταῖος']),
    'greek_units_of_measure': dict(
        source='https://en.wikipedia.org/wiki/Ancient_Greek_units_of_measurement (all Greek-script names) + λίτρα (IIP bani0100) + ἡμιόγδοον (IIP mare0220)',
        items=['δάκτυλος', 'κόνδυλος', 'παλαιστή', 'δῶρον', 'διχάς', 'ἡμιπόδιον', 'λιχάς', 'ὀρθόδωρον', 'σπιθαμή',
               'πούς', 'πυγμή', 'πυγών', 'πῆχυς', 'βῆμα', 'ὄργυια', 'κάλαμος', 'ἄκαινα', 'δεκάπους', 'ἅμμα',
               'πλέθρον', 'στάδιον', 'δίαυλος', 'ἱππικόν', 'μίλιον', 'δόλιχος', 'παρασάγγης', 'σχοινός', 'ἑξαπόδης',
               'ἡμίεκτος', 'ἕκτος', 'ἄρουρα', 'κοχλιάριον', 'χήμη', 'μύστρον', 'κόγχη', 'κύαθος', 'ὀξύβαφον',
               'τέταρτον', 'ἡμικοτύλη', 'κοτύλη', 'τρύβλιον', 'ἡμίνα', 'ξέστης', 'χοῦς', 'κεράμιον', 'μετρητής',
               'χοῖνιξ', 'ἡμίεκτον', 'ἑκτεύς', 'μέδιμνος', 'ὀβολός', 'δραχμή', 'μνᾶ', 'τάλαντον', 'λίτρα', 'ἡμιόγδοον']),
    'maresha_greek_label_vocabulary': dict(
        source='IIP expansions of Korzakova 2010 Maresha Greek ostraca (seah, qab, bat, wheat, chickpea, tax, silver, gift, drachma)',
        items=['σέα', 'σέαι', 'κάβοι', 'βάτοι', 'πυρός', 'ἐρέβινθος', 'φόρος', 'ἀργυρίου', 'δῶρον', 'δραχμή']),
}

out = {}
for name, s in SYSTEMS.items():
    words = [norm(w) for w in s['items']]
    res = {}
    for g in GROUPS:
        m = [s['items'][i] for i, w in enumerate(words) if w.startswith(g)]
        alt = {a: [s['items'][i] for i, w in enumerate(words) if w.startswith(a)] for a in SENS.get(g, [])}
        res[g] = dict(matches=m, sensitivity=alt)
    k = sum(1 for g in GROUPS if res[g]['matches'])
    out[name] = dict(source=s['source'], n_items=len(s['items']), compatible_groups=k, detail=res)
    print(f"{name}: {k}/7 compatible ->", {g: res[g]['matches'] for g in GROUPS if res[g]['matches']},
          '| sensitivity hits:', {a: v for g in GROUPS for a, v in res[g]['sensitivity'].items() if v})
json.dump(out, open('data/system_tests.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
