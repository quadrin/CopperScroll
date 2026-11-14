// Field notes of 13–14 November 2026: results of the work with other methods, the Koḥlit count audit
// and the fifth issue of the regional atlas. Text only: the image crops behind these results are private study copies.
export type Status='Checked'|'Probable'|'Possible'|'Seen'|'Not confirmed'|'Holds'|'Fails'|'Not decided'|'Not testable'|'Changed'|'Corrected'|'No link'|'Chance level';
export type Note={title:string;status?:Status;date:string;text:string;links?:[string,string][]};
export type Section={id:string;title:string;intro?:string;notes:Note[]};
export type PlaceRow={place:string;status:Status;position:string;source:string};
export type UnitRow={unit:string;name:string;before:string;now:Status;why:string};

const R='research/sources/hexagon_registration_2026-11-11/notes/20_other_methods_2026-11-13/';
const K='research/rarity/kohlit/position_and_margin_audit_2026-11-13/';
export const REPO='https://github.com/quadrin/CopperScroll/blob/main/';

export const SUMMARY=[
 'No rating, candidate or strength of a match was changed by any of this work.',
 'The registered Koḥlit count is not changed. The audit notes stand beside it.',
 'The images behind these results (HEXAGON 1974–1978, Bavarian air photographs of 1918, survey plans) are private study copies and are not shown here.',
];

export const PLACES:PlaceRow[]=[
 {place:'Kh. el-Gharur, Roman camp (Zertal 2008, site 259)',status:'Checked',position:'PG 201.437/179.826 (32.2116 N, 35.5436 E)',source:'1 Dec 1974; survey plan 116/104/72/56 m'},
 {place:'Tananir building (Boling 1975, fig. 1)',status:'Probable',position:'PG 176.88/179.58 (32.2098 N, 35.2832 E), about 50 m',source:'Location plan on the grid by Tell Balata and Tell er-Ras'},
 {place:'Tell er-Ras, fosse south of the mound',status:'Probable',position:'PG 176.00–176.12/179.15–179.18',source:'Bull 1968 text; two dates of 1974'},
 {place:'Jebel Quruntul (Doq), summit enclosure',status:'Checked',position:'31.8744 N, 35.4306 E; table point 39 m away',source:'Entry test 4, height model'},
 {place:'Birket Musa',status:'Checked',position:'Centre 31.8477 N, 35.4399 E',source:'BS Pal. 1041 (1918) and 1978; walls agree to 3–5 m'},
 {place:'Pool A(B)101 of the Pools Complex',status:'Checked',position:'31.8537 N, 35.4344 E',source:'BS Pal. 1037 (2 July 1918): open hollow of 20 × 35 m'},
 {place:'Cut mound SW of Tell es-Sultan = Tell es-Samarat',status:'Probable',position:'31.8650 N, 35.4405 E',source:'BS Pal. 1031-c (1918); SWP sheet XVIII sign at 15 m'},
 {place:'Kypros, birkeh south of Beit Jabr et-Tahtani',status:'Probable',position:'31.8485 N, 35.4307 E',source:'SWP sheet XVIII; basin on the 1978 image'},
 {place:'Kidron, lower gorge mouth',status:'Seen',position:'31.6777 N, 35.4328 E',source:'1 Dec 1974 and modern image: a tree, no cairn'},
 {place:'ʿAin Feshkha, north-east installation (plate XLII)',status:'Possible',position:'About 31.7158 N, 35.4511 E',source:'Checked on the modern image; nothing readable in 1974'},
 {place:'ʿAin Feshkha, long wall (plate XLII)',status:'Not confirmed',position:'Plan line from PG 192.757/124.827 to about 192.88/124.97',source:'June 1974, Dec 1974 and modern image; under the road and car park today'},
];

export const UNITS:UnitRow[]=[
 {unit:'E99',name:'Tananir',before:'Not decided (margin 50 m)',now:'Holds',why:'Boling 1975 places the building 82 m north of the database point; the tomb E92 is then at 336° and 874 m.'},
 {unit:'S843',name:'Kh. edh-Dhraʿ',before:'Not decided (margin 75 m)',now:'Holds',why:'The feature is the Roman camp of Kh. el-Gharur, now measured; the margin is 135 m.'},
 {unit:'S845',name:'Kh. es-Saleh',before:'Not decided (margin 5 m)',now:'Not decided',why:'Gophna and Porat 1972 (site 170) give the database point; Zertal and Bar give a point 100 m south and did not visit. The conditions hold on the west third of the spur only.'},
 {unit:'S1032',name:'Udala',before:'Not decided (margin 15 m)',now:'Not decided',why:'Tell er-Ras is 986 m away from the points of Finkelstein et al. 1997 and 1006 m from the point of Kallai 1972.'},
 {unit:'E334',name:'Tell es-Sultan',before:'Margin 70 m',now:'Holds',why:'From the measured mound centre the tomb condition is at 993 m (margin 7 m); the pool condition is from words.'},
 {unit:'S3961',name:'Bar-Adon 1972, site 98c',before:'Margin 85 m',now:'Holds',why:'From the measured Qumran buildings the cemetery is at 16.9° and 883 m.'},
 {unit:'S2539',name:'Tulul Abu el-ʿAlaiq',before:'Branch B match',now:'Holds',why:'Birket Musa measured as an area: centre 4.1° inside the east sector; 74% of the pool inside.'},
 {unit:'S6040',name:'Tell esh-Sheikh Dhiab',before:'Branch B match',now:'Fails',why:'The database point is about 1 km from the tell measured on the images.'},
 {unit:'S2589',name:'Kypros',before:'Branch B match',now:'Fails',why:'From the unit point the birkeh is at 37–38°, outside the east sector; from the summit ruin it is inside.'},
 {unit:'S3137',name:'el-Muntar',before:'Branch B match',now:'Not testable',why:'The pool is on the sector edge (45.0°); nothing is identified on the image of 1 Dec 1974.'},
];

export const SECTIONS:Section[]=[
 {id:'atlas',title:'Atlas and entry-place table',intro:'The printed atlas (edition of 13 November 2026) was built again on 14 November: 318 pages, 269 figures, 72 revised entries.',notes:[
  {title:'What the fifth issue adds',date:'14 Nov',status:'Changed',text:'The Doq offset, the Tananir position, the two survey distances at Udala, the Tell er-Ras fosse, the ʿAin Feshkha plate XLII results, and three new rows in the place register (Kh. el-Gharur camp, Tananir building, Tell er-Ras fosse). A sentence about Tell er-Ras on Mount Gerizim that stood under the record "Udala / Tell er-Ras" since the third issue is moved to Mount Gerizim.',links:[['Note',R+'23_atlas_fifth_issue_2026-11-14.md']]},
  {title:'Doq (Jebel Qarantal): offset 157 m → 39 m',date:'14 Nov',status:'Changed',text:'By the owner\'s decision. With the height model the table point is 39 m from the centre of the walled summit enclosure (about 77 × 52 m). The value of 157 m came from a fit without a height model. Location grade A is not changed. Edit log row A17.',links:[['Entry-place table','research/sources/hexagon_registration_2026-11-11/entry_places_location_assessment_2026-11-12.csv'],['Edit log','research/sources/hexagon_registration_2026-11-11/edit_log_location_grades_and_image_statuses.md']]},
 ]},
 {id:'kohlit',title:'Koḥlit count: positions and margins',intro:'The count was not run again (the database file is not in the repository). These are checks by hand, beside the count.',notes:[
  {title:'Branch B matches with measured positions',date:'14 Nov',text:'Of the four branch B matches, one holds (Tulul Abu el-ʿAlaiq), two fail from their database points (Tell esh-Sheikh Dhiab, Kypros) and one is not testable (el-Muntar).',links:[['Second pass',K+'second_pass_2026-11-14_birket_musa_as_area.md'],['Third pass',K+'third_pass_2026-11-14_kypros_el_muntar.md']]},
  {title:'The 22 units with two of three conditions',date:'14 Nov',text:'Each unit point was moved in all directions until a condition failed. 14 units have 130 m or more, or conditions from words only. The six close units were checked on the images and in the survey books. Now 20 hold and 2 are not decided (S845, S1032); none fails.',links:[['Fourth pass',K+'fourth_pass_2026-11-14_two_of_three_units.md'],['Table',K+'kohlit_two_of_three_margins_and_images_2026-11-14.csv'],['Tananir',K+'fifth_note_2026-11-14_tananir_from_boling_1975.md'],['Survey records',K+'sixth_note_2026-11-14_saleh_dhra_gharur_udala.md'],['Kh. es-Saleh',K+'seventh_note_2026-11-14_kh_es_saleh_sources.md']]},
 ]},
 {id:'images',title:'Places on the images',notes:[
  {title:'Tell er-Ras: Bull 1968',date:'14 Nov',status:'Probable',text:'Bull 1968 has no plan; its text puts a wide east–west fosse at the south limit of the mound. The dark band 45–80 m south of the platform is in that place on both dates of 1974. Bull himself asks whether this fosse is the "upper fosse" of the Gerizim entry; that is recorded as his statement only.',links:[['Note',R+'21_tell_er_ras_bull_1968_fosse_2026-11-14.md']]},
  {title:'ʿAin Feshkha: plate XLII',date:'14 Nov',status:'Not confirmed',text:'The long wall is not seen on June 1974, December 1974 or the modern image. North of the main building the plate\'s track runs north-east, but the road runs north on all dates, so the plate line there can be 50 m or more wrong.',links:[['Note',R+'22_ain_feshkha_plate_xlii_long_wall_ne_installation_2026-11-14.md']]},
  {title:'Bavarian air photographs of 1918',date:'13–14 Nov',text:'Frames of the Bavarian air unit were fitted to the 1978 image by edge matching (two frames 2.8–3.1 m; a moved start gives the same result). Birket Musa had no fields round it and a military camp in it in March 1918; pool A(B)101 was an open hollow in 1918; the Mount of Olives cemetery was complete in April 1918. There is no air photograph of Nablus in the collection.',links:[['Birket Musa',R+'08_old_air_2_bs_pal_1041_birket_musa.md'],['Camp',R+'10_old_air_4_bs_pal_1042_camp.md'],['Pool A(B)101',R+'13_old_air_7_pool_ab101.md'],['Automatic fits',R+'15_old_air_9_jericho_frames_automatic_fit.md'],['Jerusalem',R+'20_old_air_10_bs_pal_838_jerusalem.md']]},
  {title:'Height model: water lines and the Kidron gorge',date:'13 Nov',status:'Seen',text:'The fall of Wadi Qumran is 130 m west of the aqueduct intake. The lower mouth of the Kidron gorge has a tree and no cairn. The "largest drop" on the lower Kidron was an artefact of a gorge narrower than the 30 m cells (corrected).',links:[['Water lines',R+'03_height_model_1_steep_drops_on_wadi_lines.md'],['Kidron',R+'04_height_model_2_lower_kidron_gorge_mouth.md']]},
 ]},
 {id:'other',title:'Other methods',notes:[
  {title:'Name search, second run',date:'13 Nov',status:'Chance level',text:'The October name search, run again on 1,909 sites with exact positions and period marks, gives matches at the level of chance.',links:[['Note',R+'05_name_search_2_scroll_names_against_soa_site_list.md']]},
  {title:'Scroll distances on the Qumran plan',date:'13 Nov',status:'No link',text:'One of 13 installations is at six cubits from a channel, which a chance count also gives. No entry is linked.',links:[['Note',R+'02_plan_search_1_scroll_distances_on_traced_qumran_plan.md']]},
  {title:'Scroll photographs at line I 12',date:'13 Nov',text:'A blind second reader saw one letter with a base and a right side before ק: a low lean to the closed-letter reading. The left-light frames are not registered there. No rating changed. The photographs are not published.',links:[['Note',R+'18_scroll_photographs_3_blind_second_reading_I12.md']]},
 ]},
];

export const CORRECTIONS:[string,string][]=[
 ['D8','The "largest drop" on the lower Kidron (height model 1) was a gorge artefact.'],
 ['D9','The bearing from the mound to the centre of Birket Musa (old air photographs 3) was withdrawn: it used hand-picked points.'],
 ['D10','"The six-frame stack is possible to 3–8 px" was too wide: the left-light frames are not registered at I 12.'],
 ['D11','"No HEXAGON cover for el-Muntar" was wrong: tile F017b covers it.'],
 ['D12','A Tell er-Ras sentence stood under the wrong atlas record (Udala) since the third issue.'],
 ['D13','"Kubur ed Delameh" of the British survey is 1.8 km south of Kh. es-Saleh, not "roughly in this place".'],
 ['—','The source for Tananir is Boling 1975, not Bull.'],
];
