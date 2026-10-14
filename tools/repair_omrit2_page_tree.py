"""Recover the 50 orphan /Page objects in the owner's Omrit II PDF.
Read-only source repair: original bytes remain unchanged. Modern source derivatives stay private.
Usage: python repair_omrit2_pages.py ORIGINAL.pdf OUTPUT_DIRECTORY
Requires pypdf 6.10.0. Source hash is mandatory.
"""
import hashlib,json,pathlib,re,sys
from pypdf import PdfReader,PdfWriter,PageObject
from pypdf.generic import IndirectObject
SOURCE_SHA='500f965c1f8919438d9538be98ddf0a530e41cc7e09ec39e33bdbf7802b34be1'
src=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==SOURCE_SHA
r=PdfReader(src,strict=False);old=list(r.pages);active={p.indirect_reference.idnum for p in old}
rec=[];allpages=[]
for gen,offsets in r.xref.items():
 for oid in offsets:
  if oid==0:continue
  o=IndirectObject(oid,gen,r).get_object()
  if not isinstance(o,dict) or o.get('/Type')!='/Page':continue
  allpages.append([oid,gen])
  if oid in active:continue
  pg=PageObject(r,IndirectObject(oid,gen,r));pg.update(o);t=pg.extract_text()
  m=re.search(r'^(?:the hellenistic and roman pottery|the lamps: catalog and discussion) (\d+)\n',t) or re.search(r'^(\d+) (?:sandhaus|rosenthal-heginbottom)\n',t)
  folio=int(m.group(1)) if m else (31 if 'chapter 2\n' in t[:150] else 66 if 'chapter 3\n' in t[:150] else None)
  assert folio is not None
  rec.append({'object_id':oid,'generation':gen,'printed_page':folio,'recovered_viewer_page':folio-30,'full_repaired_viewer_page':folio+21,'text':t,'page_object':pg})
rec.sort(key=lambda x:x['printed_page']);assert [x['printed_page'] for x in rec]==list(range(31,81))
assert len(old)==377 and len(allpages)==427
assert old[50].extract_text().startswith('30 overman et al.')
assert old[51].extract_text().startswith('the lamps: catalog and discussion 81')
for name,pages in [('omrit2_recovered_31-80.pdf',[x['page_object'] for x in rec]),('omrit2_repaired_full427.pdf',old[:51]+[x['page_object'] for x in rec]+old[51:])]:
 w=PdfWriter()
 for pg in pages:w.add_page(pg)
 with open(out/name,'wb') as f:w.write(f)
full=PdfReader(out/'omrit2_repaired_full427.pdf');assert len(full.pages)==427
for x in rec:
 assert full.pages[x['full_repaired_viewer_page']-1].extract_text()==x['text']
serial=[{k:v for k,v in x.items() if k!='page_object'} for x in rec]
json.dump(serial,open(out/'recovered_private_text_and_mapping.json','w'),ensure_ascii=False,indent=2)
public=[{k:v for k,v in x.items() if k not in ['text','page_object']} for x in rec]
json.dump({'source_sha256':SOURCE_SHA,'original_traversal_pages':377,'all_xref_page_objects':427,'recovered_pages':public,'historical_viewer_mapping':{'old1-51':'full1-51','old52-377':'full102-427'},'derived_full_sha256':hashlib.sha256((out/'omrit2_repaired_full427.pdf').read_bytes()).hexdigest(),'derived50_sha256':hashlib.sha256((out/'omrit2_recovered_31-80.pdf').read_bytes()).hexdigest()},open(out/'repair_manifest.json','w'),indent=2)
print('Verified source hash, all427 Page objects, exact31-80 sequence, and restored text equality.')
