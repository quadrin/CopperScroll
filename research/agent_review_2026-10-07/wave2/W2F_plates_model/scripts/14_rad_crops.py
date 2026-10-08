"""Radiograph close-ups for disputed loci (located by eye from distinctive neighbouring signs;
radiograph geometry is foreshortened across curved segments, so no automatic registration).
Each crop: contrast-stretched (1-99 percentile) x2 (Lanczos). Boxes recorded in
data/disputed_crop_boxes_radiograph.json."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
BOX = json.load(open(os.path.join(BASE,'data','disputed_crop_boxes_radiograph.json')))
for name, b in BOX.items():
    fn = b['file']; x0,y0,x1,y1 = b['box']; z = b.get('zoom', 2)
    g = np.asarray(Image.open(os.path.join(BASE,'plates','png',fn)).convert('L')).astype(float)[y0:y1, x0:x1]
    lo, hi = np.percentile(g,1), np.percentile(g,99)
    im = Image.fromarray((np.clip((g-lo)/(hi-lo+1e-9),0,1)*255).astype(np.uint8)).resize((int((x1-x0)*z), int((y1-y0)*z)), Image.LANCZOS)
    im.save(os.path.join(BASE,'crops','disputed',name+'.png')); print(name, im.size)
