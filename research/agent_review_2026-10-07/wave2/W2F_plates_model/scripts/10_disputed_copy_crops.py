"""Close-up crops of the disputed loci from the copy photographs (Puech 2006 vol. II plates).
Two renderings per locus: (a) plain grayscale x2 (Lanczos), (b) background-normalised
(gray / Gaussian(sigma=25 px)), contrast-stretched 1-99 percentile, x2. No overlay, no labels.
Crop boxes (photo px) are listed in data/disputed_crop_boxes.json; they were placed from the
line position of the registered facsimile plus generous margins, not from letter outlines."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
BOX = {
 'XII10_copy_plCCCLXXXI': (12, (700, 815, 1140, 955)),
 'VII11_copy_plCCCLXXI':  (7,  (150, 1120, 670, 1295)),
 'X15-16_copy_plCCCLXXVII': (10, (250, 1280, 770, 1535)),
 'IX7_copy_plCCCLXXV':    (9,  (110, 570, 570, 705)),
}
json.dump({k:{'column':v[0],'box_x0y0x1y1':v[1]} for k,v in BOX.items()}, open(os.path.join(BASE,'data','disputed_crop_boxes.json'),'w'), indent=1)
for name,(col,(x0,y0,x1,y1)) in BOX.items():
    g = load_gray(copy_plate_path(col))
    sub = g[y0:y1, x0:x1]
    a = Image.fromarray(np.clip(sub,0,255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2), Image.LANCZOS)
    a.save(os.path.join(BASE,'crops','disputed',name+'_gray_x2.png'))
    n = g/(ndi.gaussian_filter(g,25)+1); s = n[y0:y1,x0:x1]
    lo, hi = np.percentile(s,1), np.percentile(s,99)
    b = Image.fromarray((np.clip((s-lo)/(hi-lo),0,1)*255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2), Image.LANCZOS)
    b.save(os.path.join(BASE,'crops','disputed',name+'_norm_x2.png'))
    print(name, sub.shape)
