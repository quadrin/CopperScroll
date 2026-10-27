import csv,sys
P='/home/claude/copperscroll/research/measurements/sequence/places.csv'
pl={r['place_id']:r for r in csv.DictReader(open(P,encoding='utf-8'))}
def row(e,pid,basis,sets):
    r=pl[pid]; return dict(entry=e,place_id=pid,place=r['name'],lat=r['lat'],lon=r['lon'],precision=r['precision'],
        csv_listing=f"entries_best_supported: {r['entries_best_supported']}",basis=basis,sets=sets)
A=[
 row('9','jer_east_gate',"text: cistern opposite the East Gate; East Gate of the Temple enclosure (agreed monument); places.csv best 9(medium)",'P D1 D2 D0'),
 row('10','jer_east_gate',"text: cistern under the wall, on the east; places.csv place = eastern wall of the Temple enclosure; best 10(medium)",'P D1 D2'),
 row('35','mar_saba',"text: cairn at the mouth of the Kidron gorge (the Kidron); best 35(medium)",'P D1 D2 D0'),
 row('49','jer_siloam',"text: basin of the bathhouse(?) of Rahil(?) read as Siloam; best 49(medium)",'P D1 D2 D0'),
 row('51','jer_se_corner',"text: below the southern corner of the portico, in the tomb of Zadok (Zadok's tomb / Temple enclosure); best 51(medium)",'P D1 D2 D0'),
 row('57','gerizim',"text: on Mount Gerizim; best 57(medium)",'P D1 D2 D0'),
 row('58','beth_shean',"text: mouth of the spring of Beth Sham (Beth-shean); best 58(medium)",'P D1 D2 D0'),
 row('31','doq',"DEVIATION D1: surviving name Doq/Duk (not in the rule's parenthetical list); best 31(medium)",'D1 D2'),
 row('32','choziba',"DEVIATION D1: surviving name Kozeba/Choziba (not in list); best 32(medium)",'D1 D2'),
 row('38','natuf',"DEVIATION D1: surviving name Natof/Ain en-Natuf (not in list); best 38(medium)",'D1 D2'),
 row('55','jer_bethesda',"DEVIATION D1: House of the Two Reservoirs = Bethesda pools (monument not in list); best 55(medium)",'D1 D2'),
 row('17','nuweimeh',"DEVIATION D2 only: Valley of Achor, no surviving name; best 17(medium)",'D2'),
 row('20','wadi_qumran',"DEVIATION D2 only: valley of Secacah, no surviving name; best 20(medium)",'D2'),
 row('21','kh_qumran',"DEVIATION D2 only: Secacah, no surviving name; best 21(medium)",'D2'),
 row('22','kh_qumran',"DEVIATION D2 only: Secacah, no surviving name; best 22(medium)",'D2'),
 row('46','ramat_rahel',"DEVIATION D2 only: Beth ha-Kerem = Ramat Rahel by Aharoni, name not surviving there; best 46(medium)",'D2'),
]
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(A[0]))
w.writeheader(); [w.writerow(a) for a in A]
