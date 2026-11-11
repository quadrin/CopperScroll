import sys, pickle, json, numpy as np, os
sys.path.insert(0,'/home/claude/dem')
import reg2, auto
from demtool import ds
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
L=lambda n: pickle.load(open('/home/claude/dem/A_%s.pkl'%n,'rb'))
def hgt(lat,lon): return float(list(ds.sample([(lon,lat)]))[0][0])
O='/mnt/user-data/outputs/gis/chips/'; os.makedirs(O,exist_ok=True)
PRJ='PROJCS["Israel 1993 / Israeli TM Grid",GEOGCS["Israel 1993",DATUM["Israel_1993",SPHEROID["GRS 1980",6378137,298.257222101],TOWGS84[-48,55,52,0,0,0,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",31.7343936111111],PARAMETER["central_meridian",35.2045169444444],PARAMETER["scale_factor",1.0000067],PARAMETER["false_easting",219529.584],PARAMETER["false_northing",626907.39],UNIT["metre",1],AUTHORITY["EPSG","2039"]]'
T={ # name: (affine 3x2 in frame px, relief (A4,h0) or None)
 'F017b':(L('f017b'),L('F017b_west_relief')),'F018b':(L('f018b'),L('F018b_west_relief')),'F018b_mazin':(L('f018b_mazin'),None),
 'A017e':(L('a017e_both'),L('A017e_relief')),'A015c':(L('a015c'),None)}
def chip(tag,path,ox,oy,tname,cx,cy,half=500):
    A,rel=T[tname]; im=Image.open(path); W,H=im.size
    wx,wy=cx-ox,cy-oy; x0=int(max(0,wx-half)); y0=int(max(0,wy-half)); x1=int(min(W,wx+half)); y1=int(min(H,wy+half))
    if x1-x0<200 or y1-y0<200: print('skip',tag); return
    c=im.crop((x0,y0,x1,y1)).convert('L'); fn=O+tag+'.jpg'; c.save(fn,quality=92)
    M=A[:3].copy()
    la,lo=reg2.ll(M,cx,cy); sh=np.zeros(2)
    if rel is not None:
        A4,h0=rel; M=A4[:3].copy(); sh=(hgt(la,lo)-h0)*A4[3]
    c0=np.array([ox+x0,oy+y0,1.])@M+sh
    open(O+tag+'.jgw','w').write('\n'.join('%.9f'%v for v in [M[0,0],M[0,1],M[1,0],M[1,1],c0[0],c0[1]])+'\n'); open(O+tag+'.prj','w').write(PRJ)
    cen=np.array([cx,cy,1.])@M+sh; lo2,la2=auto.Ti.transform(*cen); print(tag,c.size,'centre',round(la2,5),round(lo2,5))
J='/home/claude/w/jer.png'
chip('F017b_dec74_tulul_abu_el_alayiq',J,15800,1900,'F017b',18020,6000)
chip('F017b_dec74_birket_musa',J,15800,1900,'F017b',18420,6265)
chip('F017b_dec74_tell_es_sultan',J,15800,1900,'F017b',18183,3350)
chip('F017b_dec74_quruntul_summit',J,15800,1900,'F017b',16673,3169)
chip('F017b_dec74_qumran','/home/claude/w/qum.png',20850,16380,'F017b',23050,19130)
chip('F017b_dec74_ein_feshkha','/home/claude/w/qum.png',20850,16380,'F017b',23031,22340)
chip('F017b_dec74_deir_hajla','/home/claude/t3/haj.png',23400,7200,'F017b',24800,8690)
chip('F018b_dec74_hyrcania','/home/claude/t3/hyr.png',11300,3700,'F018b',13230,5055,700)
chip('F018b_dec74_mar_saba','/home/claude/hy/aqw.png',8200,3700,'F018b',10585,7332)
chip('F018b_dec74_khirbet_mazin','/home/claude/t3/maz.png',20500,7500,'F018b_mazin',21370,8360)
K='/home/claude/hx5/kaf_dec_rot.png'
chip('A017e_dec74_habbasa',K,0,0,'A017e',3786,4971)
chip('A017e_dec74_plateau_fort',K,0,0,'A017e',4250,4621)
chip('A017e_dec74_kafrein_dam_barakat',K,0,0,'A017e',3350,3450,600)
chip('A017e_dec74_tell_er_rameh','/home/claude/hx6/ram_rot.png',-1500,6000,'A017e',330,7300)
Q='/home/claude/hx2/kaf_rot.png'
chip('A015c_jun74_habbasa',Q,0,0,'A015c',3242,3072)
chip('A015c_jun74_kafrein_dam_barakat',Q,0,0,'A015c',2650,1700,600)
chip('A015c_jun74_tell_er_rameh',Q,0,0,'A015c',785,4979)
chip('A015c_jun74_tell_iktanu',Q,0,0,'A015c',3043,5431)
# transforms json
D={k:{'affine_E_N_per_x_y_const':v[0][:3].tolist(),'relief':None if v[1] is None else {'affine':v[1][0][:3].tolist(),'per_metre_height':v[1][0][3].tolist(),'h0':float(v[1][1])}} for k,v in T.items()}
for n in ('f018b_east','f018c','f018c_mach','f017c','f017b_east'): D[n]={'affine_E_N_per_x_y_const':L(n).tolist(),'relief':None}
A4,h0=L('f018c_mach_relief'); D['f018c_mach']['relief']={'affine':A4[:3].tolist(),'per_metre_height':A4[3].tolist(),'h0':float(h0)}
D['_note']='E,N in EPSG:2039 = [x,y,1] @ affine (+ (h-h0)*per_metre_height). F tiles: tile pixels. A017e, A015c: pixels of the Kafrein window turned 180 degrees (A017e window origin tile x12000,y12500, size 7000x6500; A015c origin x10500,y16500, size 6500x6000).'
json.dump(D,open('/mnt/user-data/outputs/gis/hexagon_1974_transforms_2026-11-11.json','w'),indent=1)
