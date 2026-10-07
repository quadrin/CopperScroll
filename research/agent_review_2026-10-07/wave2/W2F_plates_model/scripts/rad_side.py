"""Side-by-side: copy-photo crop and the registered radiograph warped into the same frame."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cv2
reg = json.load(open(os.path.join(BASE,'data','radiograph_registration.json')))
fn = sys.argv[1]; x0,y0,x1,y1 = map(int, sys.argv[2:6]); out = sys.argv[6]; z = float(sys.argv[7]) if len(sys.argv)>7 else 2
r = reg[fn]; col = r['col']
g = load_gray(copy_plate_path(col))
rad = np.asarray(Image.open(os.path.join(BASE,'plates','png',fn)).convert('L')).astype(np.float32)
A = np.array(r['A_rad2copy'], np.float32)
w = cv2.warpAffine(rad, A, (g.shape[1], g.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)
def st(a):
    lo, hi = np.percentile(a,1), np.percentile(a,99); return (np.clip((a-lo)/(hi-lo+1e-9),0,1)*255).astype(np.uint8)
a = Image.fromarray(st(g[y0:y1,x0:x1])); b = Image.fromarray(st(w[y0:y1,x0:x1]))
W, H = int((x1-x0)*z), int((y1-y0)*z)
c = Image.new('L', (W, 2*H+6), 255); c.paste(a.resize((W,H), Image.LANCZOS), (0,0)); c.paste(b.resize((W,H), Image.LANCZOS), (0,H+6))
c.save(out)
