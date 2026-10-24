"""One deterministic reading of the frozen dated_in_window rule, applied to period_as_given.

yes      the period names only in-window terms (Hasmonean, Herodian, Early Roman, Late Hellenistic,
         Second Temple, Bar Kokhba, first century BCE/CE, Jewish revolt)
no       the period names only out-of-window terms
unknown  blank, ambiguous terms ('Roman', 'Hellenistic', 'Middle Roman', second century CE), or a mix of
         in- and out-of-window terms (a range that only partly overlaps)
"""
import re

IN = re.compile(r"hasmon|herod|early roman|late hellenistic|second[- ]temple|bar[- ]?kokh?ba|bar kosiba|"
                r"jewish revolt|first revolt|first[- ]century|1st[- ]c|first centuries|late first century", re.I)
OUT = re.compile(r"byzantin|late roman|early islamic|umayyad|abbasid|fatimid|crusad|mamluk|ottoman|iron age|"
                 r"bronze|chalcolith|neolith|paleolith|natufian|persian|mandate|modern|medieval|middle ages|ayyubid|"
                 r"islamic|(third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|3rd|4th|5th|6th|7th|8th)[- ]century|"
                 r"(third|fourth|fifth|sixth|seventh|eighth)[–-]", re.I)
AMBIG = re.compile(r"(?<!early )(?<!late )\broman\b|(?<!late )\bhellenistic\b|middle roman|second[- ]century c|"
                   r"second[–-](third|fourth)|first[–-]second|1st[–-]2nd", re.I)


def rule(period):
    p = (period or '').strip()
    if not p:
        return 'unknown'
    i, o = bool(IN.search(p)), bool(OUT.search(p))
    a = bool(AMBIG.search(re.sub(r"early roman|late roman|late hellenistic|middle roman", "", p, flags=re.I))) or \
        bool(re.search(r"middle roman|second[- ]century c|first[–-]second", p, re.I))
    if i and not o and not a:
        return 'yes'
    if o and not i and not a:
        return 'no'
    return 'unknown'


if __name__ == '__main__':
    tests = {'Second Temple period': 'yes', 'Byzantine period': 'no', 'Roman period': 'unknown', 'Hellenistic': 'unknown',
             'Early Roman period': 'yes', 'Early Roman–Byzantine periods': 'unknown', 'Hasmonean and Herodian': 'yes',
             'first–second centuries CE': 'unknown', 'Late Roman': 'no', 'Iron Age II': 'no', '': 'unknown',
             'Middle Roman period': 'unknown', 'Late Hellenistic (Hasmonean) period': 'yes', 'Hellenistic–Roman': 'unknown',
             'first century CE': 'yes', 'Ottoman period': 'no', 'Roman and Byzantine periods': 'unknown'}
    bad = [(k, v, rule(k)) for k, v in tests.items() if rule(k) != v]
    print('rule self-test failures:', bad)
