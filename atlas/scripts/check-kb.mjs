// Semantic UI/rendering checks; these do not substitute for browser interaction QA.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import ts from 'typescript';
const require=createRequire(import.meta.url);
function compile(path,extras='',deps={}){
 const file=new URL(path,import.meta.url);const module={exports:{}};
 const compiled=ts.transpileModule(readFileSync(file,'utf8').replaceAll('import.meta.env?.BASE_URL',JSON.stringify('/CopperScroll/atlas-site/'))+extras,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true}}).outputText;
 const localRequire=id=>id in deps?deps[id]:id.endsWith('.css')?{}:require(id);
 new Function('require','module','exports',compiled)(localRequire,module,module.exports);return module.exports;
}
const model=compile('../app/atlas-kb-model.ts');
const data=JSON.parse(readFileSync(new URL('../app/atlas-kb.json',import.meta.url),'utf8'));
const i=model.index(data);
assert.equal(Object.keys(data.entries).length,61);
assert.ok(model.isKBRoute(''));assert.ok(model.isKBRoute('#kb?entry=25'));
for(const route of ['#entry-25/site','#entry-11/scroll','#workbench/states'])assert.equal(model.isKBRoute(route),false);
assert.equal(new Set(data.records.map(r=>r.key)).size,data.records.length);
for(const r of data.records){assert.equal(r.visibility,'public_metadata');assert.notEqual(r.exposure,'reserved');assert.equal(r.review_status,'accepted');}
for(const e of data.edges){assert.ok(i.by.has(e.subject));assert.ok(i.by.has(e.object));}
const readings=model.entryContext(i,'25').filter(r=>r.kind==='reading');
assert.ok(readings.some(r=>r.key==='reading/e25-direction:0'));
assert.ok(readings.some(r=>r.key==='reading/e25-direction:1'));
const janoah=model.impact(i,'reading/e60-janoah:4').filter(r=>r.record.kind==='evaluation');
assert.equal(janoah.length,4);assert.ok(janoah.every(r=>r.record.payload.branch_key==='branch/RB-L'));
const survey=model.impact(i,'observation/icrc2017-native-plan').filter(r=>r.record.kind==='evaluation');
assert.equal(survey.length,16);assert.ok(survey.every(r=>r.record.payload.hypothesis_key==='hypothesis/A41:XII/53'));
const text=compile('../app/atlas-text.tsx');
const textData=JSON.parse(readFileSync(new URL('../app/atlas-text.json',import.meta.url),'utf8'));
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const fieldwork=compile('../app/atlas-kb-fieldwork.tsx','',{'./atlas-text':{Segments:text.Segments,useScrollText:()=>({data:textData,failed:false})},'./atlas-explorer-model':{sitePlans:plans}});
const components=compile('../app/atlas-kb.tsx','\nexport {Graph,Inspector,Requirements,Names,Impact,Sources,CaseOverview,Comparison};',{'./atlas-kb-model':model,'./atlas-kb-fieldwork':fieldwork});
const render=(c,props)=>renderToStaticMarkup(createElement(c,props));
const onSelect=()=>{};
for(const entry of Object.keys(data.entries)){
 const chosen=i.by.has('claim/gutfeld-northeast-aspect')&&entry==='25'?'claim/gutfeld-northeast-aspect':'entry/'+entry;
 const graph=model.graphRecords(i,entry,chosen);
 const keys=new Set(graph.records.map(r=>r.key));
 for(const edge of graph.edges){assert.ok(keys.has(edge.subject)&&keys.has(edge.object));assert.ok(data.edges.includes(edge));}
 assert.ok(render(components.Graph,{i,entry,selected:chosen,onSelect}).includes('stored relationship types'));
}
const inspected=render(components.Inspector,{i,record:i.by.get('observation/icrc2017-native-plan'),onSelect,onImpact(){}});
assert.ok(inspected.includes('4–5'));assert.ok(inspected.includes('p. 95'));assert.ok(inspected.includes('W2_identity'));assert.ok(inspected.includes('null'));assert.ok(inspected.includes('Follow the evidence chain'));
const names=render(components.Names,{i,onSelect});assert.ok(names.includes('כוחלית'));assert.ok(names.includes('T05-062'));assert.ok(names.includes('Object / manuscript'));
const candidates=model.entryContext(i,'25').filter(r=>r.kind==='hypothesis');
const requirements=render(components.Requirements,{i,candidates,onSelect});
for(const id of ['hypothesis/iv17','hypothesis/iv11','hypothesis/twin','hypothesis/A41:XII/53'])assert.ok(requirements.includes(id),id);
assert.ok(requirements.includes('fixed')||requirements.includes('Fixed')||requirements.includes('FIXED'));
const sources=render(components.Sources,{i,context:model.entryContext(i,'25'),onSelect});assert.ok(sources.includes('Uninspected:'));
const changed=render(components.Impact,{i,selected:i.by.get('reading/e60-janoah:4'),onSelect});assert.ok(changed.includes('4 dependent candidate results'));assert.ok(changed.includes('RB-L')||changed.includes('Lefkovits'));
// Compare the same branch and period across every candidate and control.
for(const entry of ['25','11','60']){
 const context=model.entryContext(i,entry),candidates=context.filter(r=>r.kind==='hypothesis');
 for(const choice of model.comparisonChoices(i,candidates)){
  const rows=model.comparisonRows(i,candidates,choice.key);
  assert.equal(rows.length,candidates.length);
  for(const {candidate,result} of rows)if(result){assert.equal(result.payload.hypothesis_key,candidate.key);assert.equal(model.comparisonKey(result),choice.key);}
 }
 const overview=render(components.CaseOverview,{i,entry:i.by.get('entry/'+entry),context,candidates,onSelect});
 for(const heading of ['What does the passage say?','How do the candidates compare?','What evidence would help decide?'])assert.ok(overview.includes(heading));
 for(const candidate of candidates)assert.ok(overview.includes(candidate.label.replaceAll('&','&amp;').replaceAll("'",'&#x27;')),candidate.key);
 assert.ok(overview.includes(entry==='25'?'permit L-656':'Kallai pp.172'));
 assert.ok(overview.includes('Comparison branch'));assert.ok(overview.includes('never identification confidence'));
}
const defaultComparison=render(components.Comparison,{i,candidates,onSelect});assert.ok(defaultComparison.includes('Show all registered depth'));assert.equal((defaultComparison.match(/<option /g)||[]).length,4);
const choices=model.comparisonChoices(i,candidates),choice=choices.find(c=>c.branch.includes('target-prerequisites'));
assert.ok(choice);
const controls=model.comparisonRows(i,candidates,choice.key);
assert.equal(controls.find(r=>r.candidate.key==='hypothesis/A41:XII/53').result,undefined);
const bad=structuredClone(data),original=bad.records.find(r=>r.kind==='evaluation');bad.records.push({...original,key:original.key+'-duplicate'});
assert.throws(()=>model.comparisonRows(model.index(bad),[i.by.get(original.payload.hypothesis_key)],model.comparisonKey(original)),/Ambiguous/);
const entryOnly=render(components.CaseOverview,{i,entry:i.by.get('entry/1'),context:model.entryContext(i,'1'),candidates:[],onSelect});
assert.ok(entryOnly.includes('no populated candidate comparison'));
console.log('KB checks passed: 61 entry graphs, guided passage flow, all exact branch/period comparisons, explicit missing controls, separate readings, bounded impact, source locators and rendered views.');

// Archaeological display adapters preserve the native plate and transcription signs.
const edition=render(fieldwork.PassageEdition,{entry:i.by.get('entry/25'),onSelect});
assert.ok(edition.includes('lang="he"'));assert.ok(edition.includes('dir="rtl"'));
assert.ok(edition.includes('מערת'));assert.ok(edition.includes('Milik 27'));
assert.ok(edition.includes('Allegro 26'));assert.ok(edition.includes('CC BY-NC 4.0'));
assert.ok(!render(fieldwork.PassageEdition,{entry:i.by.get('entry/11'),onSelect}).includes('{{east'));
const plate=render(fieldwork.SourcePlate,{onSelect});
for(const value of ['/CopperScroll/atlas-site/dossiers/sion2002-plan5-iv17.webp','Plan 5 p. 63','CC BY-NC 4.0','north arrow','No geographic registration','Evidence record'])assert.ok(plate.includes(value),value);
assert.equal((plate.match(/<img /g)||[]).length,1);assert.ok(!plate.split('kb-plate-image')[1].split('</a>')[0].includes('<svg'));
for(const id of ['hypothesis/twin','hypothesis/A41:XII/53','hypothesis/iv11']){
 const dossier=render(fieldwork.CandidateFieldRecord,{candidate:i.by.get(id),onSelect});
 assert.ok(dossier.includes('Figure coverage'));assert.ok(!dossier.includes('<img'));
}
const e60=render(fieldwork.PassageEdition,{entry:i.by.get('entry/60'),onSelect});assert.ok(e60.includes('{צח}'));
console.log('Archaeological presentation checks passed: source plate, attribution, figure gaps, Hebrew sigla and edition concordance.');
