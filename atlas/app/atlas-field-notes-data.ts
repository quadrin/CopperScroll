// Field notes, 13–14 November 2026: places checked with the 1918 air photographs, the HEXAGON images of 1974–1978,
// survey books and the Koḥlit count audit, written as atlas records. The changelog (what changed, corrections) is
// in atlas-changelog-data.ts. Figures exist only in the access-controlled build.
export type Status='Checked'|'Probable'|'Possible'|'Seen'|'Not confirmed'|'Holds'|'Fails'|'Not decided'|'Not testable'|'No link'|'Chance level';
export type Fig={id:string;caption:string;credit:string};
export type Entry={id:string;name:string;sit?:string;sub?:string;status:Status;date:string;body:string[];figs?:string[];tasks?:string[];sources?:[string,string][]};
export type Chapter={id:string;title:string;entries:Entry[]};
export type PlaceRow={place:string;status:Status;position:string;source:string};
export type UnitRow={unit:string;name:string;result:Status;why:string};

const R='research/sources/hexagon_registration_2026-11-11/notes/20_other_methods_2026-11-13/';
export const K='research/rarity/kohlit/position_and_margin_audit_2026-11-13/';
export const REPO='https://github.com/quadrin/CopperScroll/blob/main/';
// Figures of the access-controlled build only. The public build never has these files (media/ is blocked by check-pages-payload).
const H='HEXAGON KH-9 (USGS EarthExplorer, declassified, public domain); registration and marks by the project', B='Bayerisches Hauptstaatsarchiv, Abt. IV Kriegsarchiv, Bildsammlung Palästina (1918); private study copy; registration by the project', ESRI='modern image: Esri World Imagery', SWP='Survey of Western Palestine, sheet XVIII (1880; public domain)';
export const FIGS:Record<string,Fig>={
 'doq-summit-1978-modern':{id:'doq-summit-1978-modern',caption:'Jebel Quruntul summit enclosure on 5 May 1978 and on a modern image.',credit:H+'; '+ESRI},
 'gharur-camp-1974':{id:'gharur-camp-1974',caption:'Kh. el-Gharur on 1 Dec 1974: the Roman camp (about 105 × 70 m) just north-east of the database point (cross).',credit:H},
 'saleh-dhra-gharur-wide-1974':{id:'saleh-dhra-gharur-wide-1974',caption:'Kh. el-Gharur, Kh. edh-Dhraʿ and Kh. es-Saleh on 1 Dec 1974, with the database points and the point of Zertal and Bar for Kh. es-Saleh.',credit:H},
 'saleh-spur-1974':{id:'saleh-spur-1974',caption:'Kh. es-Saleh: the spur between Wadi es-Salih and the gully to its south, 1 Dec 1974.',credit:H},
 'tananir-1974':{id:'tananir-1974',caption:'Tananir on 1 Dec 1974: database point, and the plan position of Boling 1975 by two fits; Tell Balata at the top.',credit:H},
 'udala-tell-er-ras-1974':{id:'udala-tell-er-ras-1974',caption:'Udala and Tell er-Ras (near ʿAwarta) on 25 June 1974, with the database points.',credit:H},
 'tell-er-ras-bull-1968-two-dates':{id:'tell-er-ras-bull-1968-two-dates',caption:'Tell er-Ras on 1 Dec 1974 (left) and 25 June 1974 (right): the measures of Bull 1968 (mound, enclosure, Building A) and the dark band south of the mound.',credit:H},
 'feshkha-ne-installation-three-dates':{id:'feshkha-ne-installation-three-dates',caption:'ʿAin Feshkha: main building and north-east installation in June 1974, December 1974 and on a modern image.',credit:H+'; '+ESRI},
 'feshkha-long-wall-dec-1974':{id:'feshkha-long-wall-dec-1974',caption:'ʿAin Feshkha, line of the long wall of plate XLII on 1 Dec 1974.',credit:H},
 'feshkha-long-wall-modern':{id:'feshkha-long-wall-modern',caption:'ʿAin Feshkha, line of the long wall of plate XLII on a modern image.',credit:ESRI},
 'birket-musa-1918-1978':{id:'birket-musa-1918-1978',caption:'Birket Musa on 22 June 1918 (left) and 5 May 1978 (right), on one grid of 10 m.',credit:B+'; '+H},
 'birket-musa-camp-march-1918':{id:'birket-musa-camp-march-1918',caption:'Birket Musa on 27 March 1918 (oblique view): rows of tents or shelters in and round the pool.',credit:B},
 'pool-ab101-1918-1978':{id:'pool-ab101-1918-1978',caption:'North bank of Wadi Qelt: the sunken rectangle of 2 July 1918 (left) and the two basins of pool A(B)101 on 5 May 1978 (right). Grid 50 m.',credit:B+'; '+H},
 'tell-es-samarat-swp-xviii':{id:'tell-es-samarat-swp-xviii',caption:'SWP sheet XVIII south of Tell es-Sultan: Tell el-ʿAraïs, Tell Abu Hindi, Tell es-Samarat and Tell Abu Zelef.',credit:SWP},
 'kypros-pool-1978':{id:'kypros-pool-1978',caption:'Kypros on 5 May 1978 with the points of the Koḥlit count and of the sources for the pool at Beit Jabr et-Tahtani.',credit:H},
 'kidron-gorge-mouth-1974-modern':{id:'kidron-gorge-mouth-1974-modern',caption:'The lower Kidron gorge on 1 Dec 1974 (left) and on a modern image (right).',credit:H+'; '+ESRI},
 'kidron-mount-of-olives-1918-1974':{id:'kidron-mount-of-olives-1918-1974',caption:'The Kidron valley and the west slope of the Mount of Olives on 8 April 1918 (top) and 25 June 1974 (bottom). Grid 50 m.',credit:B+'; '+H},
 'wadi-qelt-1918-1978-meshel-amit':{id:'wadi-qelt-1918-1978-meshel-amit',caption:'South side of Wadi Qelt on 17 May 1918 (top) and 5 May 1978 (bottom), with the aqueduct points of Meshel and Amit 1979.',credit:B+'; '+H},
};
export const CHAPTERS:Chapter[]=[
 {id:'jericho',title:'Jericho, Wadi Qelt and Qarantal',entries:[
  {id:'doq',name:'Jebel Quruntul, summit enclosure',sit:'SIT0023',sub:'Scroll entry 31 (Doq)',status:'Checked',date:'14 nov',
   body:['A walled enclosure of about 77 × 52 m on the summit, on the image of 5 May 1978 and on a modern image. Centre 31.8744 N, 35.4306 E (height model). The point of the entry-place table is 39 m from the centre; location grade A.'],
   figs:['doq-summit-1978-modern'],sources:[['Entry-place table','research/sources/hexagon_registration_2026-11-11/entry_places_location_assessment_2026-11-12.csv']]},
  {id:'birket-musa',name:'Birket Musa',sit:'SIT0019',status:'Checked',date:'13–14 nov',
   body:['On the Bavarian air photograph BS Pal. 1041 of 22 June 1918, fitted to the image of 5 May 1978 by edge matching (52 points, 2.8 m), the walls of 1918 and 1978 agree to 3–5 m. Outer size about 178 × 156 m; centre 31.8477 N, 35.4399 E. In 1918 the plain round the pool had no fields.',
    'The oblique frame BS Pal. 1042 of 27 March 1918 shows a military camp in and round the pool: the small objects in it on the June frame are camp remains. A row of dots from the mound to the east is the line of the road (Probable), not a channel.',
    'Koḥlit unit S2539 (Tulul Abu el-ʿAlaiq), pool to the east: with the pool measured as an area, its centre is at 130.9°, 4.1° inside the sector, and 74% of the pool is inside. Holds.'],
   figs:['birket-musa-1918-1978','birket-musa-camp-march-1918'],sources:[['Old air photographs 2',R+'08_old_air_2_bs_pal_1041_birket_musa.md'],['4',R+'10_old_air_4_bs_pal_1042_camp.md'],['9',R+'15_old_air_9_jericho_frames_automatic_fit.md'],['Koḥlit, second pass',K+'second_pass_2026-11-14_birket_musa_as_area.md']]},
  {id:'pool-ab101',name:'Pool A(B)101 of the Pools Complex',sit:'SIT0019',sub:'Netzer, Hasmonean and Herodian palaces',status:'Checked',date:'13 nov',
   body:['An open sunken rectangle of about 20 × 35 m on the frame BS Pal. 1037 of 2 July 1918, at 31.8537 N, 35.4344 E, 19 m from the centre of Netzer\'s plan. The pool was visible on the surface before the excavations.'],
   figs:['pool-ab101-1918-1978'],sources:[['Old air photographs 5',R+'11_old_air_5_bs_pal_1037_sunken_rectangle.md'],['7',R+'13_old_air_7_pool_ab101.md']]},
  {id:'samarat',name:'Tell es-Samarat',sit:'SIT0003',sub:'cut mound south-west of Tell es-Sultan',status:'Probable',date:'14 nov',
   body:['The cut mound on the frame BS Pal. 1031-c (31 May 1918), at about 31.8650 N, 35.4405 E (hand fit, 30 m). The "Tell es Samarat" sign of SWP sheet XVIII is 15 m from it; the "Tell Abu Hindi" sign is 320 m away.'],
   figs:['tell-es-samarat-swp-xviii'],sources:[['Old air photographs 1',R+'07_old_air_1_bs_pal_1031c_tell_es_sultan.md'],['Koḥlit, third pass',K+'third_pass_2026-11-14_kypros_el_muntar.md']]},
  {id:'kypros',name:'Kypros, birkeh of Beit Jabr et-Tahtani',sit:'SIT0025',status:'Probable',date:'14 nov',
   body:['SWP sheet XVIII puts the "small ruined birkeh immediately south of the fort" at a round sign 370 m from the catalogue point. On the image of 5 May 1978 a basin of about 50 × 40 m is 82 m from that sign, at 31.8485 N, 35.4307 E.',
    'Koḥlit unit S2589, pool to the east: from the unit point the birkeh is at 37–38°, outside the sector (fails); from the summit ruin, 148 m away, it is at 51–54°, inside.'],
   figs:['kypros-pool-1978'],sources:[['Koḥlit, third pass',K+'third_pass_2026-11-14_kypros_el_muntar.md']]},
  {id:'qelt-south',name:'Wadi Qelt, south side below Deir el-Qelt',sit:'SIT0041',sub:'aqueduct of Meshel and Amit 1979, points 17–26',status:'Probable',date:'13 nov',
   body:['The frame BS Pal. 897 (17 May 1918) was fitted to the image of 1978 by edge matching (148 points, 3.1 m). The mapped aqueduct line is too coarse (about 50 m) to separate ancient stretches from modern repair. A light line on the slope at points 25–26 goes up and then down: Probable a path.'],
   figs:['wadi-qelt-1918-1978-meshel-amit'],sources:[['Old air photographs 8',R+'14_old_air_8_bs_pal_897_automatic_fit.md']]},
  {id:'muntar',name:'el-Muntar',sit:'SIT0259',status:'Not testable',date:'14 nov',
   body:['Tile F017b of 1 December 1974 covers the site. At the points of the unit and of the reservoir of Qasr ʿAli it shows bare slopes; no structure is identified. Koḥlit unit S3137, pool to the east, is on the sector edge (45.0°).'],
   sources:[['Koḥlit, third pass',K+'third_pass_2026-11-14_kypros_el_muntar.md']]},
 ]},
 {id:'qumran',title:'Qumran, ʿAin Feshkha and the Kidron',entries:[
  {id:'feshkha',name:'ʿAin Feshkha, plate XLII',sit:'SIT0086',sub:'Humbert and Chambon 1994',status:'Not confirmed',date:'14 nov',
   body:['The long wall of the plate, from the north-west corner of the south-west enclosure (PG 192.757/124.827) towards about 192.88/124.97, is not seen on 25 June 1974, 1 December 1974 or the modern image. Its line today is under the road junction and the car park.',
    'The north-east installation (basins) is clear on the modern image, at about 31.7158 N, 35.4511 E; in 1974 nothing can be read there (Possible).',
    'North of the main building the plate draws its track running north-east; the road runs north on all dates. The plate line there can be 50 m or more wrong.'],
   figs:['feshkha-ne-installation-three-dates','feshkha-long-wall-dec-1974','feshkha-long-wall-modern'],sources:[['Note',R+'22_ain_feshkha_plate_xlii_long_wall_ne_installation_2026-11-14.md']]},
  {id:'wadi-qumran',name:'Wadi Qumran, the fall',sit:'SIT0081',sub:'Scroll entry 21',status:'Seen',date:'13 nov',
   body:['Water lines from the 30 m height model put the fall of Wadi Qumran at about 31.7407 N, 35.4533 E, 130 m west of the dam and the intake of the aqueduct.'],
   sources:[['Height model 1',R+'03_height_model_1_steep_drops_on_wadi_lines.md']]},
  {id:'kidron-mouth',name:'Kidron, lower gorge mouth',sit:'SIT0103',sub:'Scroll entry 35',status:'Seen',date:'13 nov',
   body:['Where the wadi leaves the last rock walls above the Dead Sea shore, at 31.6777 N, 35.4328 E. One large tree stands there on 1 December 1974 and on the modern image; no cairn is identified. No edition puts entry 35 at the lower mouth.'],
   figs:['kidron-gorge-mouth-1974-modern'],sources:[['Height model 2',R+'04_height_model_2_lower_kidron_gorge_mouth.md']]},
  {id:'kidron-1918',name:'Kidron valley and the Mount of Olives in 1918',sit:'SIT0193',status:'Seen',date:'14 nov',
   body:['The frame BS Pal. 838 of 8 April 1918 (hand fit). The two rock-cut monuments in the valley are visible in 1918 and 1974. In 1918 the west slope of the Mount of Olives is covered with dense rows of graves on both sides of the Jericho road; in 1974 most of that slope is bare.'],
   figs:['kidron-mount-of-olives-1918-1974'],sources:[['Old air photographs 10',R+'20_old_air_10_bs_pal_838_jerusalem.md']]},
 ]},
 {id:'samaria',title:'Nablus and Mount Gerizim',entries:[
  {id:'tell-er-ras',name:'Tell er-Ras, Mount Gerizim',sit:'SIT0273',sub:'Scroll entry 57',status:'Probable',date:'14 nov',
   body:['The platform at PG 176.06/179.23 is Checked (two dates of 1974; 36 m from height point 831.2 of the 1:20,000 map). Bull 1968 has no plan; its text gives the mound (not more than 122 × 81 m), the enclosure round Buildings A and B (44 × 64 m) and a wide east–west fosse at the south limit of the mound.',
    'The dark east–west band 45–80 m south of the platform centre (about PG 176.00–176.12/179.15–179.18) is in that place on 1 December and 25 June 1974: Probable the fosse. Building A is not resolved.',
    'Bull 1968 itself asks whether this fosse is the "upper fosse" of the Copper Scroll. That is the excavator\'s statement; it is recorded here as data.'],
   figs:['tell-er-ras-bull-1968-two-dates'],tasks:['Bull and Wright 1965 (the first report) for the width of the fosse.','A larger-scale image of the fosse edges and Building A.'],sources:[['Note',R+'21_tell_er_ras_bull_1968_fosse_2026-11-14.md']]},
  {id:'tananir',name:'Tananir',sit:'SIT0256',sub:'Koḥlit unit E99',status:'Probable',date:'14 nov',
   body:['Boling 1975 (BASOR Supplementary Studies 21, pp. 24–85) puts the building, 18 m square, on the lower slope of Mount Gerizim, about 300 m from Tell Balata. Its location plan, put on the grid by Tell Balata and Tell er-Ras, gives 32.2098 N, 35.2832 E (PG 176.88/179.58; about 50 m), west of the fork of the Nablus–Jerusalem road. The area is built up on the image of 1974.',
    'Koḥlit unit E99: from this position the tomb E92 is at 336° and 874 m. Holds.'],
   figs:['tananir-1974'],sources:[['Note',K+'fifth_note_2026-11-14_tananir_from_boling_1975.md']]},
  {id:'udala',name:'Udala and Tell er-Ras near ʿAwarta',sit:'SIT0257',sub:'Koḥlit unit S1032',status:'Not decided',date:'14 nov',
   body:['The database points are those of the Southern Samaria survey (Finkelstein, Lederman and Bunimovitz 1997, pp. 699–700): Udala 17625/17320, a small village of 0.3 ha; er-Ras 17675/17405, a terraced tell of 2.5 ha with en-Nabi ʿUzeir on its west side. On the image of 25 June 1974 the Udala point is in the village core and the er-Ras point near the top of a terraced hill.',
    'From the survey points the tell is 986 m from Udala; from the point of Kallai 1972 (1767/1741) it is 1006 m, over the 1000 m limit. This Tell er-Ras is 5.2 km south of Tell er-Ras on Mount Gerizim.'],
   figs:['udala-tell-er-ras-1974'],tasks:['A ground position of the tell and of the village core.','Kallai\'s grid read on the page photograph.'],sources:[['Note',K+'sixth_note_2026-11-14_saleh_dhra_gharur_udala.md']]},
 ]},
 {id:'jordan',title:'The Jordan valley north of Argaman',entries:[
  {id:'gharur',name:'Kh. el-Gharur, Roman camp',sub:'Zertal 2008, site 259; Koḥlit feature S836',status:'Checked',date:'14 nov',
   body:['A permanent Roman camp of the 2nd–3rd century on a flat hilltop: a trapezoid of 116, 104, 72 and 56 m with blocks of rooms, streets and cisterns; a broken stone sarcophagus lay outside its south-east corner (survey). On the image of 1 December 1974 a rectangle of about 105 × 70 m with a block texture; centre PG 201.437/179.826 (32.2116 N, 35.5436 E).'],
   figs:['gharur-camp-1974','saleh-dhra-gharur-wide-1974'],sources:[['Note',K+'sixth_note_2026-11-14_saleh_dhra_gharur_udala.md']]},
  {id:'dhra',name:'Kh. edh-Dhraʿ',sub:'Koḥlit unit S843; Bar 2014, site 45; Zertal and Bar, site 42',status:'Holds',date:'14 nov',
   body:['A small Chalcolithic hamlet on a narrow spur between channels 20–25 m deep, west of the valley road (grid 2018/1793, the database point). From it the camp is at 325° and 639 m; the point can move 135 m before a condition fails.'],
   sources:[['Note',K+'sixth_note_2026-11-14_saleh_dhra_gharur_udala.md']]},
  {id:'saleh',name:'Kh. es-Saleh',sub:'Koḥlit unit S845; Gophna and Porat 1972, site 170',status:'Not decided',date:'14 nov',
   body:['A ruin on three hilltops of about 4 dunams, east of the road, between Wadi es-Salih and a gully (Glueck; Gophna and Porat 2021/1791, the database point). Zertal and Bar give 2021/1790 but could not visit (minefields). On the image the spur runs from E 202.10 to 202.33.',
    'With the measured camp, the conditions hold on the west third of the spur and fail on the rest. From the point of Zertal and Bar both fail.'],
   figs:['saleh-spur-1974'],tasks:['A ground position of the ruin on its spur.'],sources:[['Note',K+'seventh_note_2026-11-14_kh_es_saleh_sources.md']]},
 ]},
];

export const OTHER:Entry[]=[
 {id:'names',name:'Scroll names against the site list',status:'Chance level',date:'13 nov',body:['The October name search, run again on 1,909 sites with exact positions and period marks, gives matches at the level of chance.'],sources:[['Note',R+'05_name_search_2_scroll_names_against_soa_site_list.md']]},
 {id:'plan',name:'Scroll distances on the Qumran plan',status:'No link',date:'13 nov',body:['One of 13 installations is at six cubits from a channel, which a chance count also gives. No entry is linked.'],sources:[['Note',R+'02_plan_search_1_scroll_distances_on_traced_qumran_plan.md']]},
 {id:'i12',name:'Line I 12, blind second reading',status:'Seen',date:'13 nov',body:['One letter with a base and a right side before ק: a low lean to the closed-letter reading. The scroll photographs are not shown.'],sources:[['Note',R+'18_scroll_photographs_3_blind_second_reading_I12.md']]},
];

export const PLACES:PlaceRow[]=[
 {place:'Jebel Quruntul, summit enclosure',status:'Checked',position:'31.8744 N, 35.4306 E',source:'1978, modern'},
 {place:'Birket Musa',status:'Checked',position:'31.8477 N, 35.4399 E',source:'1918, 1978'},
 {place:'Pool A(B)101',status:'Checked',position:'31.8537 N, 35.4344 E',source:'1918, 1978'},
 {place:'Tell es-Samarat',status:'Probable',position:'31.8650 N, 35.4405 E',source:'1918; SWP XVIII'},
 {place:'Kypros, birkeh',status:'Probable',position:'31.8485 N, 35.4307 E',source:'SWP XVIII; 1978'},
 {place:'Kidron, lower gorge mouth',status:'Seen',position:'31.6777 N, 35.4328 E',source:'1974, modern'},
 {place:'ʿAin Feshkha, north-east installation',status:'Possible',position:'31.7158 N, 35.4511 E',source:'1974; modern (Checked)'},
 {place:'ʿAin Feshkha, long wall',status:'Not confirmed',position:'PG 192.757/124.827 to 192.88/124.97',source:'1974 (two), modern'},
 {place:'Tell er-Ras, fosse',status:'Probable',position:'PG 176.00–176.12/179.15–179.18',source:'1974 (two); Bull 1968'},
 {place:'Tananir building',status:'Probable',position:'32.2098 N, 35.2832 E',source:'Boling 1975 fig. 1'},
 {place:'Kh. el-Gharur, Roman camp',status:'Checked',position:'32.2116 N, 35.5436 E',source:'1974; Zertal 2008'},
];

export const UNITS:UnitRow[]=[
 {unit:'S2539',name:'Tulul Abu el-ʿAlaiq',result:'Holds',why:'Birket Musa as an area: centre 4.1° inside the sector.'},
 {unit:'S6040',name:'Tell esh-Sheikh Dhiab',result:'Fails',why:'Database point about 1 km from the tell.'},
 {unit:'S2589',name:'Kypros',result:'Fails',why:'From the unit point the birkeh is at 37–38°.'},
 {unit:'S3137',name:'el-Muntar',result:'Not testable',why:'Pool on the sector edge (45.0°).'},
 {unit:'E99',name:'Tananir',result:'Holds',why:'Tomb E92 at 336°, 874 m from the plan position.'},
 {unit:'S843',name:'Kh. edh-Dhraʿ',result:'Holds',why:'Margin 135 m with the measured camp.'},
 {unit:'S845',name:'Kh. es-Saleh',result:'Not decided',why:'Holds on the west third of the spur only.'},
 {unit:'S1032',name:'Udala',result:'Not decided',why:'986 m or 1006 m, by the source.'},
 {unit:'E334',name:'Tell es-Sultan',result:'Holds',why:'Tomb at 993 m from the measured mound (margin 7 m).'},
 {unit:'S3961',name:'Bar-Adon 1972, site 98c',result:'Holds',why:'Cemetery at 16.9°, 883 m from the measured buildings.'},
];
