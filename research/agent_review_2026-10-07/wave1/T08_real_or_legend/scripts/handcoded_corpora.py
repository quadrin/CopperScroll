"""Hand-coded comparison amounts (read by eye from the downloaded texts; numbers verified against the Hebrew).

L_kelim  : Massekhet Kelim (Treatise of the Vessels), Hebrew text ed. A. Jellinek, Bet ha-Midrasch II (Leipzig 1853)
           pp. 88-91, archive.org item bethamidraschsam02jell (OCR, OCR lines ~5008-5140). Treasure amounts only
           (persons, e.g. the 130 Levites killed and 100 who escaped in mishnah 4, are left out; so are the
           dimensions of stones in m. 5, kept separately as 'measure').  'ocr' flags a figure whose OCR is damaged.
           ribbo (רבוא/ריבוא) = 10,000.
L_bibchr : idealised biblical treasure figures (1 Chr 22:14; 1 Chr 29:4,7; 1 Kgs 10:14,16-17; 2 Chr 9:13,15-16),
           Hebrew Masoretic text via Sefaria API (Miqra according to the Masorah).
B_admin  : biblical lists written in an administrative register (Exod 38:24-29; Num 7:84-86; Ezra 1:9-11; Ezra 2:69;
           Ezra 8:26-27; Neh 7:69-71), same source. Reference set only (neither 'genuine' nor 'legendary').
G_eleph  : Elephantine collection account, Cowley 22 (A. Cowley, Aramaic Papyri of the Fifth Century B.C.,
           Oxford 1923, pp. 65-76; archive.org aramaicpapyrioff00ahikuoft). Totals only (lines 120-125);
           every legible individual entry is 'the sum of 2 shekels'.
Fields: corpus, ref, value (as written, in its leading unit), unit, has_subunit, object, note
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = 10000
K = [
 # m.3
 ('L_kelim','m.3',120*R,'count',False,'silver sprinkling basins (מזרקי כסף)','OCR "מארק ועשרים ריבוא" read מאה ועשרים ריבוא; ocr'),
 ('L_kelim','m.3',5*R,'count',False,'basins of fine gold (חמשת ריבוא)','ocr'),
 ('L_kelim','m.3',60*R,'count',False,'of fine gold (ששים ריבוא)',''),
 ('L_kelim','m.3',120*R,'count',False,'of silver (ק״ך ריבוא)','followed by וחמשה, sense unclear'),
 # m.4
 ('L_kelim','m.4',50*R,'count',False,'bowls of fine gold (קערות ... חמשים ריבוא)','OCR המשים'),
 ('L_kelim','m.4',120*R,'count',False,'silver bowls (מאה ועשרים ריבוא)',''),
 ('L_kelim','m.4',50*R,'count',False,'jugs of fine gold (קשות ... חמשים רבוא)','OCR המשים'),
 ('L_kelim','m.4',120*R,'count',False,'silver jugs (ק״ך רבוא)',''),
 ('L_kelim','m.4',5,'count',False,'pearls/precious stones on each jug (ה׳)',''),
 ('L_kelim','m.4',100,'talent',False,'value of each stone, talents of gold (מאה ככרי זהב)',''),
 ('L_kelim','m.4',200000,'talent',False,'value of all the pearls, talents of gold (מאתים אלפים ככרי זהב)',''),
 ('L_kelim','m.4',36,'count',False,'gold trumpets (ל״ו)',''),
 ('L_kelim','m.4',10*R,'count',False,'menorah(s) of fine gold (עשרה רבוא)','object/weight unclear'),
 ('L_kelim','m.4',7,'count',False,'lamps on each (ז׳ נרות)',''),
 ('L_kelim','m.4',26,'count',False,'precious stones on each menorah (כ״ו)',''),
 ('L_kelim','m.4',200,'count',False,'stones between each stone (מאתים אבנים)',''),
 # m.5-6
 ('L_kelim','m.5',77,'count',False,'tables of gold (ע״ז)',''),
 ('L_kelim','m.5',7000,'talent',False,'talents of gold (ז׳ אלפים ככרי זהב)',''),
 ('L_kelim','m.5',3,'count',False,'courses of precious stones (נדבכין ג׳)',''),
 ('L_kelim','m.6',36000,'count',False,'number of stones (ל״ו אלף)',''),
 # m.7
 ('L_kelim','m.7',1000000,'talent',False,'talents of silver (אלף אלפים ככרי כסף)',''),
 ('L_kelim','m.7',100000,'talent',False,'talents of gold (מאת אלפים ככרי זהב)',''),
 ('L_kelim','m.7',666*R,'talent',False,'talents of fine gold (שש מאות וששים ושש רבוא)',''),
 # m.8
 ('L_kelim','m.8',7,'count',False,'curtains of gold (פרוכת של זהב ז׳)',''),
 ('L_kelim','m.8',12000,'talent',False,'talents of gold in them (י״ב אלפים ככרי זהב)',''),
 ('L_kelim','m.8',12000,'count',False,'garments of the Levites (י״ב אלף מלבושים)',''),
 ('L_kelim','m.8',70000,'count',False,'priestly garments (ע׳ אלף)',''),
 # m.9
 ('L_kelim','m.9',1000,'count',False,'lyres (כנורות ... אלף)',''),
 ('L_kelim','m.9',7000,'count',False,'harps (נבלים ז׳ אלפים)',''),
 ('L_kelim','m.9',5,'count',False,'stones on each lyre (אבנים ה׳)',''),
 # m.10 (hidden in עין כחל)
 ('L_kelim','m.10',120*R,'talent',False,'talents of silver (ככרי כסף ק״ך רבוא)',''),
 ('L_kelim','m.10',160*R,'talent',False,'of fine silver (ק״ס רבוא)',''),
 ('L_kelim','m.10',200*R,'count',False,'vessels/pots of bronze (מאתים רבוא)',''),
 ('L_kelim','m.10',110*R,'count',False,'of iron (ק״י רבוא)',''),
 ('L_kelim','m.10',3000,'count',False,'pans of fine gold (ג׳ אלפים)',''),
 ('L_kelim','m.10',70,'count',False,'tables of fine gold (ע׳)',''),
 # m.11
 ('L_kelim','m.11',1353000,'count',False,'pearls and precious stones (אלף אלפים וש׳ אלפים ונ״ג אלף)','reading of וש׳ אלפים uncertain; ocr'),
 ('L_kelim','m.11',1009000,'count',False,'gold, from the House of the Forest of Lebanon (אלף אלפים ותשע אלפים)',''),
 # m.12
 ('L_kelim','m.12',12,'count',False,'precious stones of the tribes (י״ב)',''),
 # idealised biblical figures
 ('L_bibchr','1 Chr 22:14',100000,'talent',False,'gold',''),
 ('L_bibchr','1 Chr 22:14',1000000,'talent',False,'silver',''),
 ('L_bibchr','1 Chr 29:4',3000,'talent',False,'gold of Ophir',''),
 ('L_bibchr','1 Chr 29:4',7000,'talent',False,'refined silver',''),
 ('L_bibchr','1 Chr 29:7',5000,'talent',False,'gold',''),
 ('L_bibchr','1 Chr 29:7',10000,'daric',False,'darics',''),
 ('L_bibchr','1 Chr 29:7',10000,'talent',False,'silver',''),
 ('L_bibchr','1 Chr 29:7',18000,'talent',False,'bronze',''),
 ('L_bibchr','1 Chr 29:7',100000,'talent',False,'iron',''),
 ('L_bibchr','1 Kgs 10:14',666,'talent',False,'gold per year',''),
 ('L_bibchr','1 Kgs 10:16',200,'count',False,'shields',''),
 ('L_bibchr','1 Kgs 10:16',600,'shekel',False,'gold per shield',''),
 ('L_bibchr','1 Kgs 10:17',300,'count',False,'bucklers',''),
 ('L_bibchr','1 Kgs 10:17',3,'mina',False,'gold per buckler',''),
 ('L_bibchr','2 Chr 9:13',666,'talent',False,'gold per year','parallel of 1 Kgs 10:14'),
 ('L_bibchr','2 Chr 9:15',200,'count',False,'shields','parallel'),
 ('L_bibchr','2 Chr 9:15',600,'shekel',False,'per shield','parallel'),
 ('L_bibchr','2 Chr 9:16',300,'count',False,'bucklers','parallel'),
 ('L_bibchr','2 Chr 9:16',300,'shekel',False,'per buckler','parallel (1 Kgs: 3 minas)'),
 # biblical lists in administrative register
 ('B_admin','Exod 38:24',29,'talent',True,'gold: 29 talents 730 shekels',''),
 ('B_admin','Exod 38:25',100,'talent',True,'silver: 100 talents 1,775 shekels',''),
 ('B_admin','Exod 38:26',603550,'count',False,'men registered',''),
 ('B_admin','Exod 38:27',100,'count',False,'sockets',''),
 ('B_admin','Exod 38:29',70,'talent',True,'copper: 70 talents 2,400 shekels',''),
 ('B_admin','Num 7:84',12,'count',False,'silver bowls',''),
 ('B_admin','Num 7:84',12,'count',False,'silver basins',''),
 ('B_admin','Num 7:84',12,'count',False,'gold ladles',''),
 ('B_admin','Num 7:85',130,'shekel',False,'per bowl',''),
 ('B_admin','Num 7:85',70,'shekel',False,'per basin',''),
 ('B_admin','Num 7:85',2400,'shekel',False,'total silver',''),
 ('B_admin','Num 7:86',10,'shekel',False,'per ladle',''),
 ('B_admin','Num 7:86',120,'shekel',False,'total gold',''),
 ('B_admin','Ezra 1:9',30,'count',False,'gold basins',''),
 ('B_admin','Ezra 1:9',1000,'count',False,'silver basins',''),
 ('B_admin','Ezra 1:9',29,'count',False,'knives',''),
 ('B_admin','Ezra 1:10',30,'count',False,'gold bowls',''),
 ('B_admin','Ezra 1:10',410,'count',False,'silver double bowls',''),
 ('B_admin','Ezra 1:10',1000,'count',False,'other vessels',''),
 ('B_admin','Ezra 1:11',5400,'count',False,'total vessels','items add to 2,499'),
 ('B_admin','Ezra 2:69',61000,'drachma',False,'gold',''),
 ('B_admin','Ezra 2:69',5000,'mina',False,'silver',''),
 ('B_admin','Ezra 2:69',100,'count',False,'priestly robes',''),
 ('B_admin','Ezra 8:26',650,'talent',False,'silver',''),
 ('B_admin','Ezra 8:26',100,'count',False,'silver vessels (of talents)',''),
 ('B_admin','Ezra 8:26',100,'talent',False,'gold',''),
 ('B_admin','Ezra 8:27',20,'count',False,'gold bowls',''),
 ('B_admin','Ezra 8:27',1000,'daric',False,'value of the bowls',''),
 ('B_admin','Ezra 8:27',2,'count',False,'bronze vessels',''),
 ('B_admin','Neh 7:69',1000,'drachma',False,'gold',''),
 ('B_admin','Neh 7:69',50,'count',False,'basins',''),
 ('B_admin','Neh 7:69',530,'count',False,'priestly robes',''),
 ('B_admin','Neh 7:70',20000,'drachma',False,'gold',''),
 ('B_admin','Neh 7:70',2200,'mina',False,'silver',''),
 ('B_admin','Neh 7:71',20000,'drachma',False,'gold',''),
 ('B_admin','Neh 7:71',2000,'mina',False,'silver',''),
 ('B_admin','Neh 7:71',67,'count',False,'priestly robes',''),
 # Elephantine, Cowley 22 lines 120-125 (totals)
 ('G_eleph','Cowley 22:122',31,'karsh',True,'total received: 31 karsh 8 shekels','Cowley p. 75: 159 persons x 2 sh expected; allocations sum to 31 k 6 sh'),
 ('G_eleph','Cowley 22:123',12,'karsh',True,'for YHW: 12 karsh 6 shekels',''),
 ('G_eleph','Cowley 22:124',7,'karsh',False,'for Ishumbethel: 7 karsh',''),
 ('G_eleph','Cowley 22:125',12,'karsh',False,'for Anathbethel: 12 karsh',''),
]
if __name__ == '__main__':
    out = os.path.join(HERE, '..', 'data', 'handcoded_amounts.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['corpus','ref','value','unit','has_subunit','object','note']); w.writerows(K)
    print(len(K), 'rows ->', out)
