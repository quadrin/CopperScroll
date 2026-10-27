# Run 22 step 1: entry relations for all 61 entries (written before any site scoring).
# Base reading = project translation (text/translation_en.json); alt = one principal
# edition variant per relation where it changes the landmark (text/readings.json).
# Relation kinds:
#   F  feature type exists at the site (J7 applies: dated 100 BCE-135 CE, or natural)
#   Q  qualifier of a feature:   Q:<type>:<qual>        (subj 'L' = the entry's landmark)
#   S  spatial relation:         S:<type>:<rel>:<obj>   (subj 'L' = the entry's landmark)
#   N  place name:               N:<name>
#   R  route:                    R:jericho_route
# Deposit-only clauses (dig N cubits, in its floor, inner corners, items, sums,
# "their record beside them") are listed in 'not_scored' and are not site relations.
import json, hashlib, datetime, sys

E = {}
def e(n, lines, text, rels, not_scored=""):
    E[n] = dict(entry=n, lines=lines, text=text, relations=rels, not_scored=not_scored)

def F(t, alt=None, note=""):  return dict(k="F", code=f"F:{t}", subj=None, alt=alt, note=note)
def Q(s, q, alt=None, note=""): return dict(k="Q", code=f"Q:{s}:{q}", subj=s, alt=alt, note=note)
def S(s, r, o, alt=None, note=""): return dict(k="S", code=f"S:{s}:{r}:{o}", subj=s, alt=alt, note=note)
def N(nm, alt=None, note=""):  return dict(k="N", code=f"N:{nm}", subj=None, alt=alt, note=note)
def RT(alt=None, note=""):     return dict(k="R", code="R:jericho_route", subj=None, alt=alt, note=note)

# landmark = first relation (always an F); its type is what 'L' stands for in Q/S codes.
e("1","I 1-4","In the ruin that is in the Valley of Achor, under the steps that go in toward the east",
  [F("ruin"), N("Achor", note="García Martínez-Tigchelaar 'go past': no valley (not run)"), F("steps"), S("steps","toward","east")],
  "40 cubits; chest of silver; 17 talents")
e("2","I 5-6","In the funerary monument, in the third course of stones",
  [F("monument"), Q("L","third_course", note="Lefkovits 'third gravestone'; Milik 1960 a personal name")], "gold ingots, 100")
e("3","I 6-8","In the great cistern that is in the court of the peristyle ... opposite the upper opening",
  [F("cistern"), Q("L","great"), S("L","in","peristyle_court"), Q("L","upper_opening")], "in its floor; sealed with sand(?); 900 talents")
e("4","I 9-12","In the mound of Koḥlit ... Its opening is at the edge of the conduit, on the north, six cubits as far as the rock cleft of the immersion",
  [F("mound"), N("Kohlit"), F("conduit"), F("immersion_cleft", alt="F:cool_room", note="alt Puech 2006: frigidarium"),
   S("conduit","near","immersion_cleft", alt="S:conduit:near:cool_room")], "items; six cubits")
e("5","I 13-15","In the pit of the foundry(?) of Manos, going down to the left",
  [F("pit"), F("foundry", alt="F:spiral_stair", note="alt Puech, Høgenhaven, Lefkovits: spiral staircase"),
   S("L","in","foundry", alt="S:L:in:spiral_stair"), N("Manos")], "three cubits up from the floor; 40 talents")
e("6","II 1-2","In the cistern of ha-Melaḥ that is under the steps",
  [F("cistern"), N("Melah", alt="N:Millo", note="alt Milik/Puech: the Millo/Esplanade"), F("steps"), S("L","under","steps")], "41 talents")
e("7","II 3-4","In the cave of the old House of Washing(?), on the third ledge",
  [F("cave"), F("house"), S("L","of","house"), Q("house","old"), N("MDH"), F("ledge"), Q("L","third_ledge")], "65 gold ingots")
e("8","II 5-6","In the underground chamber that is in the court of Mattiyah ... a cistern in it",
  [F("underground_chamber"), F("court"), S("L","in","court"), N("Mattiyah", alt="N:wood_court", note="alt Milik 1962/Høgenhaven: wood-store court (m. Middot 2:5)"),
   F("cistern"), S("cistern","in","L")], "wood; their record; 70 talents")
e("9","II 7-9","In the cistern that is opposite the East Gate, nineteen cubits away ... and in its channel(?)",
  [F("cistern"), F("east_gate"), S("L","opposite_19c","east_gate", note="19 cubits = 8.4-10 m (Puech 15 cubits = 6.7-7.9 m)"), Q("L","channel")], "vessels; 10 talents")
e("10","II 10-12","In the cistern that is under the wall, on the east, in the spur of the rock. Its entrance is under the great threshold",
  [F("cistern"), F("wall"), S("L","under_east","wall"), F("rock_spur"), S("L","in","rock_spur"), F("great_threshold"), S("L","entrance_under","great_threshold")], "six jars of silver")
e("11","II 13-15","In the pool that is east of Koḥlit",
  [F("pool"), N("Kohlit")], "northern corner; dig four cubits; 22 talents")
e("12","III 1-4","In the court of ◦◦◦, under the south corner",
  [F("court", note="court name illegible (Puech diaita, Lefkovits Nebaṭ): not scored")], "dig nine cubits; vessels")
e("12a","III 5-7","Under the other corner, the eastern one",
  [F("court", note="same court as entry 12 (Puech's separate entry)")], "dig sixteen cubits; 40 talents")
e("13","III 8-10","In the pit that is in ha-Melaḥ, on its north side",
  [F("pit"), N("Melah", alt="N:Millo")], "entrance under the western corner; vessels, garments")
e("14","III 11-13","In the tomb that is in ha-Melaḥ, on its east side",
  [F("tomb"), N("Melah", alt="N:Millo")], "north side; under the dead(?); dig three; 13 talents")
e("15","IV 1-2","In the great cistern that is in Koḥlit, in the pillar on its north side",
  [F("cistern"), Q("L","great"), N("Kohlit"), F("pillar"), S("L","pillar_north","pillar")], "14 talents")
e("16","IV 3-5","In the conduit that comes in ◦◦, as you go in, forty-one cubits",
  [F("conduit"), Q("L","enterable", alt="S:L:to:pool", note="alt Puech: 'which goes to the pool'")], "41 cubits; 55 talents")
e("17","IV 6-8","Between the two domes(?) that are in the Valley of Achor",
  [F("pair_domes", note="Puech cavities; Milik tamarisks; Lefkovits buildings: not run as alts"), N("Achor")], "midway; dig three cubits; two pots")
e("18","IV 9-10","In the earth(?) pit that is at the edge of the ʿAṣla",
  [F("earth_pit"), N("Asla")], "200 talents")
e("19","IV 11-12","In the eastern pit that is north of Koḥlit",
  [F("pit"), Q("L","eastern"), N("Kohlit")], "70 talents")
e("20","IV 13-14","In the cairn of the valley of Secacah",
  [F("cairn", alt="F:dam", note="alt Lurie, Eshel: dam"), F("valley"), N("Secacah")], "dig a cubit; 12 talents")
e("21","V 1-4","At the head of the water conduit [of the valley of] Secacah, on the north side, under [the stone], the great one",
  [F("conduit_head"), N("Secacah"), F("great_stone", alt="F:pool", note="alt Allegro: pool"),
   S("great_stone","at","conduit_head", alt="S:pool:at:conduit_head"), Q("conduit_head","north_side")], "dig [three] cubits; 7 talents")
e("22","V 5-7","In the fissure that is in Secacah, east of the Reservoir of Solomon",
  [F("fissure"), N("Secacah"), F("reservoir"), N("Solomon_reservoir"), S("L","east_of","reservoir")], "vessels; their record")
e("23","V 8-11","From the Trench of Solomon as far as the great heap of stones, sixty cubits",
  [F("trench"), N("Solomon_trench", alt="N:Shallum_trench", note="alt Puech 2015 Shallum"), F("great_heap"), S("L","60c","great_heap")], "dig three cubits; 23 talents")
e("24","V 12-14","In the tomb that is in the Wadi of the Vault, on the way from Jericho to Secacah",
  [F("tomb"), F("wadi"), S("L","in","wadi"), N("Kippa"), RT(), N("Secacah")], "dig seven cubits; 32 talents")
e("25","VI 1-6","[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern entrance",
  [F("cave"), Q("L","pillar", alt="Q:L:terrace", note="alt Allegro: platform/terrace"), Q("L","two_entrances"), Q("L","faces_east"), Q("L","north_entrance")], "dig three cubits; jar with one scroll; 42 talents")
e("26","VI 7-10","In the cave of the corner of the heap of stones facing east",
  [F("cave"), F("heap", alt="F:great_stone", note="alt Puech: boulder"), S("L","at_corner","heap", alt="S:L:at_corner:great_stone"), Q("L","faces_east")], "dig at the entrance nine cubits; 21 talents")
e("27","VI 11-13","In the resting place of the Queen, on the west side",
  [F("mausoleum"), N("Queen")], "dig twelve cubits; 27 talents")
e("28","VI 14-VII 2","In the cairn that is at the ford of the High Priest",
  [F("cairn"), F("ford", alt="F:bridge", note="alt Allegro, Lefkovits: bridge"), S("L","at","ford", alt="S:L:at:bridge"), N("HighPriest")], "dig ... nine; 22 talents")
e("29","VII 3-7","In the conduit of Qi◦ [...] the great northern reservoir, on its four sides",
  [F("conduit"), N("Qi", alt="N:Cypros", note="Eshel 2002: Qi[dron] or Cy[pros]; Cypros run as alt"), F("reservoir"), Q("reservoir","great"), Q("reservoir","northern"), S("L","to","reservoir")], "four sides; 24 cubits; 400 talents")
e("30","VII 8-10","In the cave that is next to the cool room of the House of Haqqoṣ",
  [F("cave"), F("cool_room"), S("L","next_to","cool_room"), F("house"), S("cool_room","of","house"), N("Haqqos")], "dig six cubits; six jars of silver")
e("31","VII 11-13","At Doq, under the corner of the guard post, the eastern one",
  [F("guard_post", alt="F:drying_room", note="alt Puech: drying room"), N("Doq")], "dig seven cubits; 22 talents")
e("32","VII 14-16","At the mouth of the water outlet of Kozeba, dig three cubits, as far as the row of stones",
  [F("water_outlet"), N("Kozeba"), F("stone_row"), S("L","near","stone_row")], "80 talents; gold")
e("33","VIII 1-3","[In the con]duit that is on the road east of the House of the Treasury, which is east of Aḥor",
  [F("conduit"), F("road"), S("L","on","road"), F("treasury_house"), S("road","east_of","treasury_house"), N("Ahor")], "vessels and scrolls")
e("34","VIII 4-7","In the outer valley, in the middle of the ◦, on the stone",
  [F("outer_valley"), F("stone")], "dig seventeen cubits; 17 talents")
e("35","VIII 8-9","In the cairn at the mouth of the Kidron gorge",
  [F("cairn", alt="F:dam", note="alt Luria, Eshel: dam"), N("Kidron"), F("gorge_mouth"), S("L","at","gorge_mouth")], "dig three cubits; 7 talents")
e("36","VIII 10-13","In the fallow ground of the Shaveh, facing west, on the south, in the chamber facing north",
  [F("chamber"), F("fallow_field"), S("L","in","fallow_field"), N("Shaveh"), Q("L","faces_north")], "dig 24 cubits; 65 talents")
e("37","VIII 14-16","In the enclosure of the Shaveh, in the chamber that is in it",
  [F("chamber"), F("enclosure"), S("L","in","enclosure"), N("Shaveh")], "dig eleven cubits; 70 talents")
e("38","IX 1-3","In the dovecote that is at the edge of the Naṭof",
  [F("dovecote"), N("Natof")], "13 cubits from its edge; dig; staters")
e("39","IX 4-6","In the second terrace(?), in the chamber facing east",
  [F("chamber"), F("terrace"), S("L","in","terrace"), Q("L","faces_east")], "dig 8.5 cubits; 23.5 talents")
e("40","IX 7-9","In the chambers of Ḥoron, in the chamber facing the sea (west), in the channel(?)",
  [F("chamber"), N("Horon", alt="N:Horites", note="alt Puech: Ḥorites"), Q("L","faces_west"), F("channel"), S("channel","in","L")], "dig sixteen cubits; 22 talents")
e("41","IX 10","In the hollow (Qomʿah?)",
  [F("hollow", note="Lefkovits, Milik: a place name Qovaʿ/Qobʿeh (not run)")], "silver, a mina, devoted")
e("42","IX 11-13","In the waterfall(?) that is near the bend of the conduit, on the east",
  [F("waterfall"), F("conduit"), Q("conduit","bend"), S("L","near","conduit_bend")], "dig seven cubits; 9 talents")
e("43","IX 14-16","In the pit that is north of the mouth of the gorge of Beth Tamar, at the outlet of the Valley of Peleʿ(?)",
  [F("pit"), F("gorge_mouth"), S("L","north_of","gorge_mouth"), N("BethTamar"), N("Pele")], "all devoted")
e("44","IX 17-X 2","In the dovecote that is in the fortress of Nab, in the district of the south, in the second upper storey",
  [F("dovecote"), F("fortress"), S("L","in","fortress"), N("Nab", alt="N:Masada", note="alt Milik 1960: ha-Masad (Masada)"), Q("fortress","south_district"), Q("L","second_upper_storey")], "its way down from above; 9 talents")
e("45","X 3-4","In the plastered(?) cistern of the channels(?) that are watered from the great wadi",
  [F("cistern"), Q("L","plastered"), F("channels"), S("L","of","channels"), F("great_wadi"), S("channels","fed_from","great_wadi")], "in its floor; 11 talents")
e("46","X 5-7","In the reservoir that is in Beth ha-Kerem",
  [F("reservoir"), N("BethHaKerem")], "as you go in, on its left, dig ten cubits; 62 talents")
e("47","X 8-11","In the basin of the Valley of Zered(?), on its west side, a black stone ... that is the entrance",
  [F("basin"), F("valley"), S("L","in","valley"), N("Zered"), F("black_stone"), S("black_stone","west_of","L")], "two cubits; 300 talents of gold; cups")
e("48","X 12-14","Under Absalom's monument, on the west side",
  [F("monument"), N("Absalom")], "dig twelve cubits; 80 talents")
e("49","X 15-16","In the basin(?) of the bathhouse(?) of Raḥil(?), under the trough",
  [F("basin", alt="F:water_outlet", note="alt Puech: outlet of the waters"), F("bathhouse"), S("L","of","bathhouse"), N("Rahil", alt="N:Siloam", note="alt Puech: of Siloam"), F("trough")], "17 talents")
e("50","X 17-XI 1","[In the upper pool], at its four corners",
  [F("pool", note="restored (Wise); Puech, Lefkovits: a court"), Q("L","upper")], "four corners; gold, vessels")
e("51","XI 2-4","Below the southern corner of the portico, in the tomb of Zadok, under the pillar of the exedra",
  [F("tomb"), N("Zadok"), F("stoa"), S("L","below_south_corner","stoa"), F("exedra"), Q("exedra","pillar")], "vessels; record")
e("52","XI 5-7","In the seat(?) at the top of the rock facing west, opposite the garden of Zadok, under the great slab that is at its base",
  [F("rock_seat"), Q("L","faces_west"), F("garden"), S("L","opposite","garden"), N("Zadok"), F("great_slab"), S("great_slab","at_base","L")], "devoted gold")
e("53","XI 8","In the tomb that is under the rock 'knife'(?)",
  [F("tomb"), F("rock_knife", alt="F:stoa", note="alt Puech 2006/2015: colonnades"), S("L","under","rock_knife", alt="S:L:under:stoa")], "41 talents")
e("54","XI 9-11","In the tomb of the common people, which is ritually pure",
  [F("tomb"), N("BeneHaAm", alt="N:Jericho", note="alt Puech 2006: 'of Jericho'")], "vessels; record")
e("55","XI 12-15","In the House of the Two Reservoirs, in the reservoir, as you go in, on the right of it",
  [F("reservoir"), Q("L","two_in_house", note="Milik 1962 emends to Bethesda (not run)")], "vessels; record")
e("56","XI 16-XII 3","In the entrance of the [ledge] of the western resting chamber ... Its entrance is from the west. Under the black stone ... Under the threshold of the cistern",
  [F("burial_chamber"), Q("L","western"), F("ledge"), Q("L","entrance_west"), F("black_stone"), F("cistern", alt="F:burial_niche", note="alt Puech: burial niche")], "platform(?); sums; juglets")
e("57","XII 4-5","On Mount Gerizim, under the steps of the upper pit",
  [F("pit"), F("mountain"), N("Gerizim"), F("steps"), S("steps","of","L"), Q("L","upper")], "chest and vessels; 61 talents")
e("58","XII 6-7","At the mouth of the spring of Beth Sham",
  [F("spring"), N("BethSham")], "vessels; 600 talents")
e("59","XII 8-9","In the great drain of the cistern, inside the cistern",
  [F("drain"), Q("L","great"), F("cistern"), S("L","of","cistern")], "71 talents 20 minas")
e("60","XII 10-13","In the pit that is on the north side of Koḥlit, its opening to the north, with tombs at its mouth",
  [F("pit"), N("Kohlit"), Q("L","opening_north"), F("tomb"), S("tomb","at_mouth_of","L")], "copy of this document")

assert len(E) == 61, len(E)
for n, x in E.items():
    assert x["relations"][0]["k"] == "F"
    x["landmark"] = x["relations"][0]["code"][2:]

if __name__ == "__main__":
    out = sys.argv[1]
    js = json.dumps(E, ensure_ascii=False, indent=1)
    open(out + ".json", "w", encoding="utf-8").write(js)
    # markdown rendering
    L = ["# Run 22 step 1: entry relations (61 entries)", "",
         "Written before any site was scored. Base = project translation (text/translation_en.json); alt = edition variant (text/readings.json). "
         "Run 10's step-1 file covers only cave entries 7, 22, 25, 26, 30, 38; run 20's step-1 file did not exist when this was written (run 20 is running in parallel), so all 61 entries are coded here.", "",
         "Kinds: F feature exists (J7 applied); Q qualifier; S spatial relation; N place name; R route. 'L' = the entry's landmark (first F). Deposit-only clauses are not scored.", "",
         "| Entry | Lines | Relations (base; alt in brackets) | Not scored |", "|---|---|---|---|"]
    for n, x in E.items():
        rs = "; ".join(r["code"] + (f" [alt {r['alt']}]" if r["alt"] else "") for r in x["relations"])
        L.append(f"| {n} | {x['lines']} | {rs} | {x['not_scored']} |")
    open(out + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    nrel = sum(len(x["relations"]) for x in E.values())
    print("entries", len(E), "relations", nrel)
