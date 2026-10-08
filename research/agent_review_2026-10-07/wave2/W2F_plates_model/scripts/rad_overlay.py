import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cv2
reg = json.load(open(os.path.join(BASE,'data','radiograph_registration.json')))
fn = sys.argv[1]; r = reg[fn]; col = r['col']
g = load_gray(copy_plate_path(col))
rad = np.asarray(Image.open(os.path.join(BASE,'plates','png',fn)).convert('L')).astype(np.float32)
A = np.array(r['A_rad2copy'], np.float32)
w = cv2.warpAffine(rad, A, (g.shape[1], g.shape[0]), borderValue=0)
m = cv2.warpAffine(np.ones_like(rad), A, (g.shape[1], g.shape[0])) > 0.5
vis = np.stack([np.clip((g-g.mean())/g.std()*40+128,0,255)]*3, -1)
vis[...,0] = np.where(m, np.clip(w,0,255), vis[...,0])
Image.fromarray(vis.astype(np.uint8)).resize((g.shape[1]//2, g.shape[0]//2)).save(os.path.join(BASE,'work','radov_'+fn))
