import sys
from PIL import Image, ImageDraw
src,out,x0,y0,x1,y1,s=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:8])
im=Image.open(src).convert('RGB').crop((x0,y0,x1,y1))
im=im.resize((im.width*s,im.height*s),Image.LANCZOS)
d=ImageDraw.Draw(im)
for x in range((x0//10+1)*10,x1,10):
    X=(x-x0)*s; d.line([(X,0),(X,im.height)],fill=(255,0,0) if x%50==0 else (255,180,180),width=1)
    if x%50==0: d.text((X+2,2),str(x),fill=(255,0,0))
for y in range((y0//10+1)*10,y1,10):
    Y=(y-y0)*s; d.line([(0,Y),(im.width,Y)],fill=(0,0,255) if y%50==0 else (180,180,255),width=1)
    if y%50==0: d.text((2,Y+2),str(y),fill=(0,0,255))
im.save(out)
