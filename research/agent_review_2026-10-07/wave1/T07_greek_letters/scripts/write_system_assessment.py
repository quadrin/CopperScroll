"""Write the system-level assessment table (criterion fixed in PREREGISTRATION.md:
>=5/7 groups under one rule, predicting end-of-entry position and cols I-IV confinement)."""
import csv
rows = [
 ('Greek numerals','well-formed only ΣΚ=220; ΞΕ=65 if read; ΔΙ=14 only reversed, 4th-6th c. Negev','repo T3; Masada ΚΓ (IIP masa0595); IIP zoor0255','no','values must relate to amounts: 0/5 (repo T3)','falsified'),
 ('Greek units of measure / capacity marks','2/7 (ΔΙ διχάς; ΤΡ τρύβλιον); sens. ΞΕ ξέστης','https://en.wikipedia.org/wiki/Ancient_Greek_units_of_measurement + IIP weights','no','unit must fit commodity; marked entries are metal already measured in Hebrew','falsified'),
 ('Semitic measures/commodities in Greek letters (Maresha)','0/7 vs attested vocabulary','Korzakova 2010 via IIP mare0196-0244','no','group must expand to commodity/measure in the entry','falsified (attested vocabulary)'),
 ('Produce-status / fund-category tags (Masada)','not testable in Greek (Masada uses Hebrew; Greek only single letters)','Masada I via IIP masa0109, 0201, 0254, 0281, 0282-0341','weakly','groups should recur with categories; all 7 differ; repo T6 no association','not supported'),
 ('Owner/depositor initials or names','2/7 in repo Ilan pilot (ΘΕ, ΣΚ)','repo R11; Jerusalem ossuary Greek groups (Rahmani 1994 nos. 289, 319, 322, 582 via IIP)','weakly','recurrence for repeat depositors; none; needs external list','open'),
 ('24 priestly courses','0/7','LXX 1 Chr 24:7-18 https://www.ellopos.net/elpenor/greek-texts/septuagint/chapter.asp?book=13&page=24','possible','groups must open course names','falsified'),
 ('Macedonian months','1/7 (ΔΙ = Δῖος)','https://en.wikipedia.org/wiki/Ancient_Macedonian_calendar','possible','groups must open month names','falsified'),
 ('Ordinal/position labels (Temple baskets α β γ; mason marks)','needs alphabetic sequence; none','Mishnah Shekalim 3:2; Herodium I (2015) p. 464','no','letters should be in order; Κ Χ Η Θ Δ Τ Σ are not (repo T7); Herodian mason marks are Hebrew','falsified'),
 ('Checker/removal marks (Goranson H5)','1/7 (ΚΕΝ ~ κεν(ός) "empty": new, low confidence)','-','would explain partial marking','one status word must cover all groups','not supported'),
]
with open('data/system_assessment.csv','w',newline='',encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(['system','groups_compatible','list_or_practice_source','predicts_position','falsifier_on_scroll','verdict'])
    w.writerows(rows)
print(len(rows))
