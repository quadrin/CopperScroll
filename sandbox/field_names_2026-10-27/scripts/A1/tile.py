import json, os, math
from PIL import Image; Image.MAX_IMAGE_PIXELS=None
B='/mnt/user-data/uploads/Copper Scroll/07 Maps and GIS/Palestine Open Maps 1-20000 (1940s)/'
S={'18-12':('18-12-Deir Mar Saba.jpg',(765,577,6640,6463)),
   '18-13':('18-13-Wadi El Qilt.jpg',(518,461,6381,6346)),
   '19-14':('19-14-Jericho.jpg',(314,446,7658,6355))}
T,ST,M=1300,1150,60
idx={}
for k,(f,(x0,y0,x1,y1)) in S.items():
    im=Image.open(B+f); x0-=M;y0-=M;x1+=M;y1+=M
    nc=math.ceil((x1-x0-T)/ST)+1; nr=math.ceil((y1-y0-T)/ST)+1
    for r in range(nr):
        half='top' if r < math.ceil(nr/2) else 'bottom'
        d=f'tiles/{k}_{half}'; os.makedirs(d,exist_ok=True)
        for c in range(nc):
            ox=min(x0+c*ST,x1-T); oy=min(y0+r*ST,y1-T)
            n=f'{k}_r{r}c{c}'
            im.crop((ox,oy,ox+T,oy+T)).save(f'{d}/{n}.jpg',quality=92)
            idx[n]=dict(sheet=k,ox=ox,oy=oy,dir=d)
    print(k,nr,nc)
json.dump(idx,open('tile_index.json','w'),indent=1)
