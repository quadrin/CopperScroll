"""Extract the nine generated object studies without retouching their appearance."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
parser=argparse.ArgumentParser();parser.add_argument('input',type=Path);args=parser.parse_args()
root=Path(__file__).resolve().parents[1];out=root/'public/introduction/object-studies';out.mkdir(exist_ok=True)
image=Image.open(args.input).convert('RGBA');w,h=image.size
references=json.loads((root/'app/atlas-intro-study-references.json').read_text())
names=['cave','jar','copper','document','sanctuary','settlement','strata','landscape','silver'];assets={}
for i,name in enumerate(names):
 if name in references:
  assets[name]=references[name];continue
 box=[round(i%3*w/3),round(i//3*h/3),round((i%3+1)*w/3),round((i//3+1)*h/3)]
 tile=image.crop(box);tile.putalpha(tile.getchannel('A').point(lambda alpha:0 if alpha<3 else alpha));tile.save(out/f'{name}.webp','WEBP',quality=94,method=6,exact=True)
 assets[name]={'file':f'introduction/object-studies/{name}.webp','width':tile.width,'height':tile.height,'kind':'illustrative-render'}
 print(name,tile.size)
(root/'app/atlas-intro-object-studies.json').write_text(json.dumps(assets,indent=2)+'\n')
(out/'provenance.json').write_text(json.dumps({'source':'Seven generated illustrative object studies and two sourced documentary references.','sourceSheetSha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),'processing':'Equal-cell extraction and WebP encoding. Only sub-visible alpha fringe (below 3/255) is cleared. No object retouching, invented reconstruction of a source photograph, vector tracing or texture smoothing. Original generated PNG is retained unchanged.','limitations':'These are generated explanatory renders, not photographs of excavated objects, surveyed cave mouths, measured architecture or readings of the manuscript. Architectural forms are illustrative massing only. Actual manuscript photographs, source radiographs and plans are separate evidence assets.','referenceOverrides':['copper','sanctuary'],'assets':assets},indent=2)+'\n')
