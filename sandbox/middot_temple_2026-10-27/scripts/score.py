# Steps 3-5: score every entry against every gazetteer feature, joint fit, control.
# Scoring rule as fixed in out/step1_entry_relations.json (SHA-256 89319d0e...8e81).
# Literal reading of that rule (stated in RESULT): for a NAMED anchor, type agreement needs a
# shared word/root with the Middot name; an UNNAMED Middot feature therefore cannot give type
# agreement for a named anchor -> unknown. An unread name -> unknown.
import json, sys, itertools, csv, math
sys.path.insert(0, sys.argv[1])
from gazetteer import F
FEAT = {f[0]: f for f in F}
IDS = [f[0] for f in F]
KIND = {f[0]: set(f[3]) for f in F}
courts = [i for i in IDS if 'court' in KIND[i]]
chambers = [i for i in IDS if 'chamber' in KIND[i]]
gates = [i for i in IDS if 'gate' in KIND[i]]
stairs = [i for i in IDS if 'stair' in KIND[i]]
channels = [i for i in IDS if 'channel' in KIND[i]]
valleys = [i for i in IDS if 'valley' in KIND[i]]

U, P, X = 'unknown', 'pass', 'fail'
# cell = (strict, lenient_if_cond_true, lenient_if_false, cond, note)
cells = {}
def put(e, fids, strict, lt, lf=None, cond=None, note=''):
    for f in fids:
        cells[(e, f)] = (strict, lt, lt if lf is None else lf, cond, note)

# ---- Temple candidates ----
put('3', courts, U, U, note='court kind agrees; name "peristyle" shares no word with any Middot court name')
put('3', ['M44'], U, P, U, 'r3_struct', 'DEVIATION only: Azarah with an exedra (portico) around it (Tam 1:3) read as a peristyle court; R3.2-R3.4 silent')
put('3', ['M71'], U, U, note='object "cistern" agrees; it lies in the Golah chamber of the Azarah, not in a court named peristyle')
put('5', stairs, U, P, U, 'r5_stair_noun', 'stair kind agrees only on the samekh reading (המסבא); "of Manos" is a name on most readings -> no Middot name match (unknown); pass only if מנס is the noun "refuge". R5.2-R5.3 silent')
put('5', ['M06'], U, P, U, 'r5_stair_noun', 'as other stairs, plus R5.2 descent AGREES (Mid 1:6 יורדים; Tam 1:1 ירד וטבל); "left" and 3 cubits silent')
put('6', ['M65'], U, P, U, 'r6_salt', 'name המלח identical to לשכת המלח (Mid 5:3); cistern in it SILENT; "under the steps" SILENT')
put('6', ['M71'], U, U, note='object cistern agrees; name Golah vs ha-Melah differ')
put('6', ['M40'] + stairs, U, U, note='steps/chambers-under-court only as relation targets; ha-Melah not named there')
put('7', chambers, U, U, note='house/chamber kind; name MDH not shared (unnamed or differently named chamber)')
put('7', ['M03'], U, U, note='name Moqed vs MDH differ; R7.2 revad AGREES (Mid 1:8 מוקף רובדין של אבן); Allegro 1960 variant "platform of the chain" also agrees (Mid 1:9 שלשלת)')
put('7', ['M67'], U, P, U, 'r7_wash', 'on the reading המדח (text shown; Hoegenhaven "washer\'s house") the root דח matches המדיחין; bayit = lishkah alias attested in Mid 5:3 (בית הפרוה / לשכת הפרוה). "old", cave, third revad SILENT')
put('7', ['M53'], X, X, note='12 steps with three landings (רבד, Mid 3:6) echo "third revad", but a stair cannot be the "house"')
put('8', courts, U, U, note='court kind agrees; name (Mattiyah / wood) not shared')
put('8', ['M36'], U, P, note='"court ... wood" shares עצ with לשכת העצים, which Mid 2:5 calls a court in the corner (Ezek 46:21-22); R8.1 chamber in it, R8.3 cistern in it SILENT')
put('8', ['M69'], X, X, note='לשכת העץ is roofed (Mid 5:4 וגג שלשתן שוה): not a court')
put('8', ['M71'], U, U, note='cistern as R8.3 target; lies in the Golah chamber')
put('9', gates, X, X, note='gate kind, but stated direction (N/S/W) or name contradicts "the East Gate"')
put('9', ['M14'], U, P, note='"שער המזרחי" identical (Mid 1:3); cistern opposite at 19 (or 15) cubits SILENT; channel SILENT')
put('9', ['M25'], U, P, note='Azarah east gate = "שער המזרח" (Tam 5:6) = Nicanor (Mid 1:4); cistern, distance, channel SILENT')
put('9', ['M54', 'M56', 'M57'], U, U, note='east-facing doorways, but called porch/Hekhal/great gate, not "East Gate"')
put('9', ['M02'], X, X, note='north gate')
put('9', ['M71'], U, U, note='cistern; position relative to an east gate not stated')
put('10', ['M33'], U, P, note='wall kind agrees, "east" AGREES (Mid 2:4 כותל המזרחי); under the wall, spur of rock, great threshold SILENT')
put('10', ['M30'], U, U, note='Soreg is a 10-handbreadth lattice, not a rampart (חומה); kind doubtful')
put('10', ['M14', 'M25', 'M19'], U, U, note='only as relation targets of the "great threshold" (סף); Middot has no סף; M19 has מפתן הבית')
put('10', ['M71'], U, U, note='cistern; not under a wall in Middot')
for e in ('12', '12a'):
    put(e, courts, U, U, note='court kind agrees, but the court\'s name is unread (◦◦◦) -> type cannot be judged; corners SILENT (Middot corners are two-direction: SE, NE...)')
    put(e, ['M15', 'M16'], U, U, note='corners only as relation targets')
put('13', ['M65'], U, P, U, 'r13_salt', 'salt/Melah reading of מלח(מ) matches לשכת המלח; pit, north side, entrance under the western corner SILENT. Millo/Esplanade/embankment readings -> unknown')
put('13', ['M47'], U, U, note='object word identical (שית, Mid 3:3) and entrance through a floor slab at a corner (Middot SW, scroll "western corner") partly agrees; but container is the altar, not ha-Melah')
put('14', ['M65'], U, P, U, 'r13_salt', 'salt reading matches לשכת המלח; tomb, NE, slab SILENT. Purity branch: a tomb in a chamber of the Azarah is excluded -> fail (not Middot text)')

# ---- Control ----
put('20', valleys, U, U, note='valley kind; Secacah vs Bet Kerem / Kidron differ')
put('21', channels, U, U, note='conduit kind (אמה identical for M46); named "of [the valley of] Secacah", Middot channel unnamed/Kidron -> no name match')
put('21', valleys, U, U, note='Secacah vs Bet Kerem / Kidron differ')
put('22', ['M71'], U, U, note='reservoir ~ cistern kind; "Solomon" vs unnamed fixed cistern; contained in Secacah vs Azarah')
put('23', channels, U, U, note='trench (חריץ) taken as channel kind (Milik: canal); named "of Solomon/Shallum" -> no Middot name match')
put('24', valleys, U, U, note='wadi kind; Kippa vs Kidron / Bet Kerem differ')
put('24', ['M03'], X, X, note='lexical echo only: Bet ha-Moqed is כפה (vaulted, Mid 1:8), but a house is not a wadi')
put('25', ['M57'], X, X, note='structural echo only: great gate with two wickets N and S, north one used, facing east (Mid 4:2; Tam 3:7); but no cave kind in Middot')
put('27', chambers, U, U, note='משכן as dwelling ~ house kind; "the Queen" shares no Middot name. As tomb: no tomb kind -> fail')
put('29', channels, U, U, note='אמה identical (Mid 3:2); name unread (קי◦)')
put('29', ['M46'], U, P, U, 'r29_kidron', 'Eshel Qi[dron] -> conduit of Kidron ~ "the channel ... out to the Kidron" (Mid 3:2); "great northern reservoir, four sides, 24 cubits" SILENT. Puech: Kidron too long for the space')
put('29', ['M71'], X, X, note='as "the great northern reservoir": Golah cistern is on the SOUTH side (Mid 5:4) -> contradicts')
put('30', chambers, U, U, note='house kind; "Haqqots" shares no Middot name; cave and cool room SILENT')

TEMPLE = ['3', '5', '6', '7', '8', '9', '10', '12', '12a', '13', '14']
CONTROL = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']
EXTRA = ['30']
BRANCHES = {
 'best_any_edition': dict(r5_stair_noun=True, r6_salt=True, r7_wash=True, r13_salt=True, r29_kidron=True, r3_struct=False),
 'text_shown':       dict(r5_stair_noun=False, r6_salt=True, r7_wash=True, r13_salt=True, r29_kidron=False, r3_struct=False),
 'puech_2006_2015':  dict(r5_stair_noun=True, r6_salt=True, r7_wash=False, r13_salt=False, r29_kidron=False, r3_struct=False),
 'milik_1962':       dict(r5_stair_noun=False, r6_salt=False, r7_wash=False, r13_salt=False, r29_kidron=False, r3_struct=False),
 'lefkovits_2000':   dict(r5_stair_noun=False, r6_salt=True, r7_wash=False, r13_salt=False, r29_kidron=False, r3_struct=False),
 'best+struct_dev':  dict(r5_stair_noun=True, r6_salt=True, r7_wash=True, r13_salt=True, r29_kidron=True, r3_struct=True),
 'best_no_eshel':    dict(r5_stair_noun=True, r6_salt=True, r7_wash=True, r13_salt=True, r29_kidron=False, r3_struct=False),
}
def cell(e, f, br):
    if (e, f) not in cells:
        return X, X, 'no type or name agreement (feature kind cannot be the entry\'s anchor or object)'
    s, lt, lf, cond, note = cells[(e, f)]
    l = lt if (cond is None or br[cond]) else lf
    return s, l, note

def fisher_one_sided(a, n1, b, n2):
    # P(X >= a) for X ~ hypergeometric, total passes a+b, groups n1, n2
    K = a + b; N = n1 + n2
    def h(k): return math.comb(n1, k) * math.comb(n2, K - k) / math.comb(N, K)
    return sum(h(k) for k in range(a, min(n1, K) + 1))

def joint(entries, br, mode, share_groups):
    # max number of entries assignable to features with lenient pass;
    # literal: all features distinct; deviation: entries in a share group may share one feature
    opts = {e: [f for f in IDS if cell(e, f, br)[1] == P] for e in entries}
    cand = [e for e in entries if opts[e]]
    best = (0, None)
    def rec(i, used, assign):
        nonlocal best
        if len(assign) + (len(cand) - i) <= best[0]:
            return
        if i == len(cand):
            if len(assign) > best[0]: best = (len(assign), dict(assign))
            return
        e = cand[i]
        for f in opts[e]:
            owner = used.get(f)
            ok = owner is None or (mode == 'shared' and any(e in g and owner <= g for g in share_groups))
            if ok:
                used2 = dict(used); used2[f] = (owner or frozenset()) | {e}
                assign[e] = f; rec(i + 1, used2, assign); del assign[e]
        rec(i + 1, used, assign)
    used0 = {}
    rec(0, used0, {})
    return best

if __name__ == '__main__':
    out = sys.argv[2]
    share = [frozenset({'12', '12a'}), frozenset({'13', '14'})]
    rows = []
    for br_name, br in BRANCHES.items():
        for e in TEMPLE + CONTROL + EXTRA:
            grp = 'temple' if e in TEMPLE else ('control' if e in CONTROL else 'control_extra')
            for f in IDS:
                s, l, note = cell(e, f, br)
                rows.append(dict(branch=br_name, group=grp, entry=e, feature=f, feature_name=FEAT[f][2],
                                 strict=s, lenient=l, note=note))
    with open(out + '/scores_all_branches.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    summary = {}
    for br_name, br in BRANCHES.items():
        def best_of(e, which):
            vals = [cell(e, f, br)[which] for f in IDS]
            return P if P in vals else (U if U in vals else X)
        per = {e: dict(strict=best_of(e, 0), lenient=best_of(e, 1),
                       lenient_pass_features=[f for f in IDS if cell(e, f, br)[1] == P],
                       n_unknown=sum(cell(e, f, br)[1] == U for f in IDS),
                       n_fail=sum(cell(e, f, br)[1] == X for f in IDS)) for e in TEMPLE + CONTROL + EXTRA}
        tp = sum(per[e]['lenient'] == P for e in TEMPLE); cp = sum(per[e]['lenient'] == P for e in CONTROL)
        ts = sum(per[e]['strict'] == P for e in TEMPLE); cs = sum(per[e]['strict'] == P for e in CONTROL)
        jt_lit = joint(TEMPLE, br, 'literal', share); jt_sh = joint(TEMPLE, br, 'shared', share)
        jc_lit = joint(CONTROL, br, 'literal', share)
        summary[br_name] = dict(readings=br, per_entry=per,
            temple_strict_pass=ts, control_strict_pass=cs,
            temple_lenient_pass=tp, control_lenient_pass=cp,
            fisher_one_sided_p_lenient=round(fisher_one_sided(tp, len(TEMPLE), cp, len(CONTROL)), 5),
            temple_joint_literal=jt_lit, temple_joint_shared=jt_sh, control_joint_literal=jc_lit)
        print(f"{br_name:18s} strict T{ts}/11 C{cs}/10 | lenient T{tp}/11 C{cp}/10 p={summary[br_name]['fisher_one_sided_p_lenient']} | joint T literal {jt_lit[0]} {jt_lit[1]} | T shared {jt_sh[0]} | C {jc_lit[0]} {jc_lit[1]}")
    json.dump(summary, open(out + '/summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=list)
