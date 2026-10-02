import json, numpy as np
from pathlib import Path
out=Path(__file__).parent
# Frozen manual picks in enlarged inspection crops, before similarity fitting.
# P: thumbnail718, crop(30,75,530,580), resized1000x1000.
# E: original718x1170, crop(100,500,610,1010), resized1000x1000.
controls=[('ring cistern NE of double pool',(487,113),(463,84)),('fort northern outer vertex',(611,350),(585,331)),('cistern J centre',(697,966),(692,971))]
holdouts=[('northern double-pool centre',(358,131),(337,103)),('southern double-pool centre',(303,199),(282,166)),('fort L room centre',(587,535),(561,521)),('cistern T centre',(882,596),(849,578)),('bridge SE junction',(350,341),(324,326))]
def source(p):return np.array([30+p[0]*.5,75+p[1]*.505])*np.array([1488/718,2033/981])
def target(p):return np.array([100+p[0]*.51,500+p[1]*.51])
P=np.array([source(x[1]) for x in controls]);Q=np.array([target(x[2]) for x in controls]);
# qx=a*px-b*py+tx; qy=b*px+a*py+ty (image y downward).
A=[];v=[]
for (x,y),(u,w) in zip(P,Q):A +=[[x,-y,1,0],[y,x,0,1]];v +=[u,w]
a,b,tx,ty=np.linalg.lstsq(A,v,rcond=None)[0]
M=np.array([[a,-b],[b,a]]);t=np.array([tx,ty]);north=np.linalg.solve(M,[0,-1]);north/=np.linalg.norm(north)
res=[]
for role,points in [('fit',controls),('holdout',holdouts)]:
 for name,p,q in points:
  sp=source(p);tq=target(q);pred=M@sp+t;res.append(dict(role=role,name=name,patrich_full_px=sp.tolist(),eshel_full_px=tq.tolist(),residual_eshel_px=float(np.linalg.norm(pred-tq))))
result=dict(test='source-to-source orientation transfer, no geographic registration',controls_frozen=True,transform_model='orientation-preserving isotropic similarity',manual_pick_uncertainty_eshel_px=4,rows=res,similarity=dict(matrix=M.tolist(),translation=t.tolist(),rotation_degrees=float(np.degrees(np.arctan2(b,a))),north_unit_vector_patrich_image=north.tolist()),north_status='inherited from Eshel Fig6.4 north arrow; approximate and not an independent survey bearing',geographic_registration_accepted=False,wgs84=None,counts=dict(new_source_targets=0,new_bounded_checks=1,decisive_tests=0,closures=0))
# Diagnostic affine fit is deliberately not accepted: exactly three controls leaves no training degrees of freedom.
B=np.column_stack([P,np.ones(3)]);aff=np.linalg.solve(B,Q);sv=np.linalg.svd(aff[:2,:].T,compute_uv=False)
result['affine_diagnostic']=dict(singular_value_ratio=float(sv.max()/sv.min()),warning='three controls interpolate exactly; this cannot validate distortion correction')
result['raster_frames']=dict(patrich=dict(path='recovered/aqua-archive/patrich-fig22-p256.png',dimensions_px=[1488,2033]),eshel=dict(path='tmp/eshel-p96.png',dimensions_px=[718,1170],source_pdf='recovered/reference-figures/eshel-aqueducts-pp92-107.pdf',pdf_page=5,renderer='PyMuPDF fitz page.get_pixmap(matrix=fitz.Matrix(2,2))',relation_to_archived_png='2x linear raster dimensions compared with copper-fig-113.png 359x585; rendered directly from PDF, not upsampled from archived PNG',coordinate_conversion_to_archived_png='divide x and y by 2',pick_uncertainty_render_px=4,pick_uncertainty_archived_px=2))
result['scale_consistency']=dict(patrich_m_per_px=50/231, eshel_m_per_px=40/83, fitted_eshel_m_per_px=(50/231)/np.hypot(a,b), relative_disagreement=((50/231)/np.hypot(a,b))/(40/83)-1, caveat='manual printed-bar endpoints; Eshel is a redrawn derivative, not demonstrated metric reproduction')
# Independent bounded pixel perturbations; these are sensitivity draws, not a statistical confidence interval.
rng=np.random.default_rng(29);angles=[]
for _ in range(10000):
 pp=P+rng.uniform(-8,8,P.shape);qq=Q+rng.uniform(-4,4,Q.shape);AA=[];vv=[]
 for (x,y),(u,w) in zip(pp,qq):AA +=[[x,-y,1,0],[y,x,0,1]];vv +=[u,w]
 aa,bb,_,_=np.linalg.lstsq(AA,vv,rcond=None)[0];angles.append(float(np.degrees(np.arctan2(bb,aa))))
result['picking_sensitivity']=dict(draws=10000,seed=29,source_perturbation_px=8,target_perturbation_px=4,rotation_min_max_degrees=[min(angles),max(angles)],interpretation='bounded Monte Carlo sensitivity only; excludes drawing distortion and survey-north error')
(out/'orientation-transfer.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
