# Freeze the C2 control list BEFORE any matching is run.
# Pool: place names of Josh 15 and 18 (MT, Sefaria "Miqra according to the Masorah"), in this fixed order:
# Josh 15:21-62 town list, Josh 18:21-28 town list, then the boundary names of Josh 15:1-12 and 18:12-19.
# Excluded: names the scroll uses or whose consonants equal a scroll variant (see EXCL). Duplicates kept once.
# Length = count of Hebrew letters other than א ה ע ו י (ח counted), per name. Each of the 40 scroll names
# (scroll_names.json order, first variant) takes the first unused pool name of the same length; if none is
# left, the nearest length (shorter first).
import json, sys
SN, OUT = sys.argv[1], sys.argv[2]
POOL = """קבצאל|15:21 עדר|15:21 יגור|15:21 קינה|15:22 דימונה|15:22 עדעדה|15:22 קדש|15:23 חצור|15:23 יתנן|15:23
זיף|15:24 טלם|15:24 בעלות|15:24 חצורחדתה|15:25 קריותחצרון|15:25 אמם|15:26 שמע|15:26 מולדה|15:26
חצרגדה|15:27 חשמון|15:27 ביתפלט|15:27 חצרשועל|15:28 בארשבע|15:28 בזיותיה|15:28 בעלה|15:29 עיים|15:29 עצם|15:29
אלתולד|15:30 כסיל|15:30 חרמה|15:30 צקלג|15:31 מדמנה|15:31 סנסנה|15:31 לבאות|15:32 שלחים|15:32 עין|15:32 רמון|15:32
אשתאול|15:33 צרעה|15:33 אשנה|15:33 זנוח|15:34 עיןגנים|15:34 תפוח|15:34 עינם|15:34 ירמות|15:35 עדלם|15:35 שוכה|15:35 עזקה|15:35
שערים|15:36 עדיתים|15:36 גדרה|15:36 גדרתים|15:36 צנן|15:37 חדשה|15:37 מגדלגד|15:37 דלען|15:38 מצפה|15:38 יקתאל|15:38
לכיש|15:39 בצקת|15:39 עגלון|15:39 כבון|15:40 לחמס|15:40 כתליש|15:40 גדרות|15:41 ביתדגון|15:41 נעמה|15:41 מקדה|15:41
לבנה|15:42 עתר|15:42 עשן|15:42 יפתח|15:43 נציב|15:43 קעילה|15:44 אכזיב|15:44 מראשה|15:44 עקרון|15:45 אשדוד|15:47 עזה|15:47
שמיר|15:48 יתיר|15:48 דנה|15:49 קריתסנה|15:49 דבר|15:49 ענב|15:50 אשתמה|15:50 ענים|15:50 גשן|15:51 חלן|15:51 גלה|15:51
ארב|15:52 רומה|15:52 אשען|15:52 ינום|15:53 ביתתפוח|15:53 אפקה|15:53 חמטה|15:54 קריתארבע|15:54 חברון|15:54 ציער|15:54
מעון|15:55 כרמל|15:55 יוטה|15:55 יזרעאל|15:56 יקדעם|15:56 קין|15:57 גבעה|15:57 תמנה|15:57 חלחול|15:58 ביתצור|15:58 גדור|15:58
מערת|15:59 ביתענות|15:59 אלתקן|15:59 קריתבעל|15:60 קריתיערים|15:60 רבה|15:60 ביתהערבה|15:61 מדין|15:61 סככה|15:61
נבשן|15:62 עירהמלח|15:62 עיןגדי|15:62
יריחו|18:21 ביתחגלה|18:21 עמקקציץ|18:21 צמרים|18:22 ביתאל|18:22 עוים|18:23 פרה|18:23 עפרה|18:23 כפרהעמנה|18:24 עפני|18:24 גבע|18:24
גבעון|18:25 רמה|18:25 בארות|18:25 כפירה|18:26 מצה|18:26 רקם|18:27 ירפאל|18:27 תראלה|18:27 צלעהאלף|18:28 יבוסי|18:28 ירושלם|18:28 גבעת|18:28
צן|15:1 עקרבים|15:3 צנה|15:3 קדשברנע|15:3 חצרון|15:3 אדרה|15:3 קרקע|15:3 עצמונה|15:4 נחלמצרים|15:4 יםהמלח|15:5 ירדן|15:5
אבןבהן|15:6 דברה|15:7 עמקעכור|15:7 גלגל|15:7 מעלהאדמים|15:7 עיןשמש|15:7 עיןרגל|15:7 גיבןהנם|15:8 עמקרפאים|15:8 מינפתוח|15:9
הרעפרון|15:9 בעלה|15:9 הרשעיר|15:10 כסלון|15:10 ביתשמש|15:10 שכרונה|15:11 יבנאל|15:11
ביתאון|18:12 לוז|18:13 עטרותאדר|18:13 ביתחרון|18:13 גלילות|18:17"""
# names the scroll uses (or equal-consonant forms of scroll variants): Hazor (variant חצור), Achzib (= כזב, Chezib/Koziba
# discussion), Secacah, Ir-ha-Melah and Yam ha-Melah (ha-Melah), Jericho, Emek Keziz (variant קיציצ), Emek Achor, Beth-horon.
EXCL = {'חצור','אכזיב','סככה','עירהמלח','יםהמלח','יריחו','עמקקציץ','עמקעכור','ביתחרון'}
FIN = str.maketrans('ךםןףץ','כמנפצ')
def L(h): return sum(1 for c in h.translate(FIN) if c not in 'אהעוי')
pool=[]; seen=set()
for tok in POOL.split():
    h, ref = tok.split('|'); h=h.translate(FIN)
    if h in EXCL or h in seen: continue
    seen.add(h); pool.append((h, ref))
names = json.load(open(SN))
used=set(); out=[]
for n in names:
    v = n['variants'][0]['core'].translate(FIN); want = L(v)
    pick=None
    for d in [0,-1,1,-2,2,-3,3]:
        for h,ref in pool:
            if h not in used and L(h)==want+d: pick=(h,ref); break
        if pick: break
    used.add(pick[0]); out.append(dict(for_scroll=n['id'], scroll_core=v, length=want, c2_hebrew=pick[0], ref='Josh '+pick[1], c2_length=L(pick[0])))
json.dump(out, open(OUT,'w'), ensure_ascii=False, indent=1)
for o in out: print(o)
print(len(pool),'pool names after exclusions')
