"""Compare the two PDF scans of Puech 2006 on the copy-photo plates (same pixel dimensions):
A = French-edition PDF (CMYK JPEG, Adobe-inverted, first generation); B = Poffet copy (RGB re-encode).
Metrics on grayscale: Pearson r between A and B, normalised Laplacian variance (high-frequency
energy after z-scoring and sigma 0.5 blur), JPEG luminance quantisation-table mean."""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
out = []
for col in range(1,13):
    pa = 682 + 2*(col-1); pb = pa - 2
    fa = glob.glob(os.path.join(BASE,'plates','A_raw',f'A-{pa}-*.jpg'))[0]; fb = glob.glob(os.path.join(BASE,'plates','B_raw',f'B-{pb}-*.jpg'))[0]
    qa = float(np.mean(Image.open(fa).quantization[0])); qb = float(np.mean(Image.open(fb).quantization[0]))
    a = load_gray(copy_plate_path(col)); b = np.asarray(Image.open(fb).convert('L')).astype(float)
    def hf(x):
        x = (x-x.mean())/x.std(); return float(ndi.laplace(ndi.gaussian_filter(x,0.5)).var())
    out.append(dict(column=ROM[col-1], r=float(np.corrcoef(a.ravel(), b.ravel())[0,1]), hf_A=hf(a), hf_B=hf(b), qtab_mean_A=qa, qtab_mean_B=qb))
    print(out[-1])
json.dump(out, open(os.path.join(BASE,'data','scan_comparison.json'),'w'), indent=1)
