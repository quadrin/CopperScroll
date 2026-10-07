"""Plate index (plate -> series, column, segment labels, image size) with resolution estimates.
Copy photos: H = median photo height of full-height letters (from verified labels).
Radiographs: line spacing from the autocorrelation of the row profile of a high-pass image,
converted to letter height with the copy-photo ratio H/line-spacing of the same column.
Output: data/plate_index.csv"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from scipy.signal import find_peaks
idx = json.load(open(os.path.join(BASE,'data','plate_index_raw.json')))
Hc = {int(k):v for k,v in json.load(open(os.path.join(BASE,'data','crops_train_H.json'))).items()}
reg = json.load(open(os.path.join(BASE,'data','registration.json')))
RN = {r:i+1 for i,r in enumerate(ROM)}
spc = {}
for col in range(1,13):
    fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
    a = np.array(sorted(fc['line_a'])); d = np.diff(a)
    M = np.array(reg[str(col)]['A_fac2photo']); s = float(np.sqrt(abs(np.linalg.det(M[:,:2]))))
    spc[col] = float(np.median(d))*s
def rad_spacing(path):
    g = np.asarray(Image.open(path).convert('L')).astype(float)
    hp = g - ndi.gaussian_filter(g, 6)
    e = ndi.gaussian_filter(np.abs(hp), 2)
    # keep the central 60% of the width (strip interior)
    w = g.shape[1]; prof = e[:, int(.2*w):int(.8*w)].mean(1)
    prof = prof - ndi.gaussian_filter1d(prof, 60)
    ac = np.correlate(prof, prof, 'full')[len(prof)-1:]; ac /= ac[0]
    pk, pr = find_peaks(ac[30:200], prominence=0.02)
    if len(pk)==0: return None, None
    k = pk[np.argmax(pr['prominences'])] + 30
    return float(k), float(ac[k])
rows = []
for r in idx:
    col = RN.get(r['column'])
    rec = dict(plate=r['plate'], series=r['series'], column=r['column'], pdf_page_A=r['pdf_page'], pdf_page_B=r['pdf_page']-2,
               file=r['file'], width=r['width'], height=r['height'], segment_labels_in_caption=r['segment_labels_in_caption'],
               letter_height_px='', line_spacing_px='', method='', reliability='')
    if r['series']=='copy_photo' and col:
        rec.update(letter_height_px=round(Hc[col],1), line_spacing_px=round(spc[col],1), method='median drawn-box height of verified full-height letters x facsimile->photo scale', reliability='good')
    elif r['series']=='radiograph' and col:
        ls, q = rad_spacing(os.path.join(BASE,'plates','png',r['file']))
        if ls:
            rec.update(line_spacing_px=round(ls,1), letter_height_px=round(ls*Hc[col]/spc[col],1),
                       method=f'row-profile autocorrelation (peak {q:.2f}) x copy ratio H/spacing={Hc[col]/spc[col]:.2f}',
                       reliability=('doubtful: spacing >1.3x copy (harmonic?)' if ls > 1.3*spc[col] else 'approximate (vertical only; horizontal foreshortening varies)'))
    elif r['series']=='facsimile' and col:
        rec.update(method='registered onto copy photo (affine); see data/registration.json')
    rows.append(rec)
rows.sort(key=lambda r: (r['pdf_page_A'], r['file']))
with open(os.path.join(BASE,'data','plate_index.csv'),'w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
    if r['series'] in ('copy_photo','radiograph'):
        print(r['plate'], r['series'][:4], r['column'], r['segment_labels_in_caption'], r['width'], r['height'], r['line_spacing_px'], r['letter_height_px'])
