// Semantic UI/rendering checks; these do not substitute for browser interaction QA.
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
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
const filters=compile('../app/atlas-kb-filters-model.ts');
const catalogue=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const nav=compile('../app/atlas-navigation.ts');
const contextRoutes=compile('../app/atlas-context-routes.ts');
const siteNav=compile('../app/atlas-site-nav.tsx','',{'./atlas-navigation':nav,'./atlas-context-routes':contextRoutes});
const components=compile('../app/atlas-kb.tsx','',{'./atlas-kb-model':model,'./atlas-kb-filters-model':filters});
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
const names=render(components.Names,{i,onSelect});assert.ok(names.includes('כוחלית'));assert.ok(names.includes('T05-062'));assert.ok(names.includes('Object / manuscript'));assert.ok(names.includes('across passages'));
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
 const overview=render(components.ReadingAlternatives,{i,context,onSelect})+render(components.Comparison,{i,candidates,onSelect})+render(components.Targets,{i,context,onSelect});
 for(const heading of ['One retained reading and period across every candidate and control.','What evidence would help decide?'])assert.ok(overview.includes(heading));
 for(const candidate of candidates)assert.ok(overview.includes(candidate.label.replaceAll('&','&amp;').replaceAll("'",'&#x27;')),candidate.key);
 assert.ok(overview.includes(entry==='25'?'permit L-656':'Kallai pp.172'));
 assert.ok(overview.includes('Comparison branch'));assert.ok(overview.includes('never identification confidence'));
}
const defaultComparison=render(components.Comparison,{i,candidates,onSelect});assert.ok(defaultComparison.includes('Show all registered depth'));assert.equal((defaultComparison.split('aria-label="Comparison branch"')[1].split('</select>')[0].match(/<option /g)||[]).length,4);
const choices=model.comparisonChoices(i,candidates),choice=choices.find(c=>c.branch.includes('target-prerequisites'));
assert.ok(choice);
const controls=model.comparisonRows(i,candidates,choice.key);
assert.equal(controls.find(r=>r.candidate.key==='hypothesis/A41:XII/53').result,undefined);
const bad=structuredClone(data),original=bad.records.find(r=>r.kind==='evaluation');bad.records.push({...original,key:original.key+'-duplicate'});
assert.throws(()=>model.comparisonRows(model.index(bad),[i.by.get(original.payload.hypothesis_key)],model.comparisonKey(original)),/Ambiguous/);
const entryOnly=render(components.Comparison,{i,candidates:[],onSelect});
assert.ok(entryOnly.includes('no populated candidate comparison'));
console.log('KB checks passed: 61 entry graphs, contextual reading alternatives and missing-observation targets, all exact branch/period comparisons, explicit missing controls, separate readings, bounded impact, source locators and rendered views.');

const foundRecords=components.searchEvidenceRecords(data.records,'icrc2017-native-plan');assert.ok(foundRecords.some(record=>record.key==='observation/icrc2017-native-plan'));
assert.ok(components.searchEvidenceRecords(data.records,'כוחלית').some(record=>record.kind==='occurrence'));
assert.deepEqual(components.searchEvidenceRecords(data.records,'a-record-that-does-not-exist'),[]);assert.deepEqual(components.searchEvidenceRecords(data.records,' '),[]);
const recordSearch=render(components.RecordSearch,{i,onSelect});assert.ok(recordSearch.includes('Search all records'));assert.ok(recordSearch.includes('outside this passage'));

// One immutable snapshot/index serves map and reader context panels.
const contextual=compile('../app/atlas-context-evidence.tsx','',{'./atlas-kb-model':model,'./atlas-kb':components,'./atlas-components':{EvidenceComponents:()=>null},'./atlas-data.json':catalogue,'./atlas-kb.json':data});
const loading=contextual.loadContextEvidence(),sameLoading=contextual.loadContextEvidence();assert.equal(loading,sameLoading);
const cached=await loading;assert.equal(await contextual.loadContextEvidence(),cached);
const contextProps={entryId:'25',view:'compare',onView(){},onRecord(){}};
const contextComparison=render(contextual.default,contextProps);
assert.ok(contextComparison.includes('One retained reading and period across every candidate and control.'));assert.ok(contextComparison.includes('permit L-656'));
assert.ok(!contextComparison.includes('<main'));assert.ok(!contextComparison.includes('Atlas sections'));assert.ok(!contextComparison.includes('Browse all entries'));assert.ok(!contextComparison.includes('<img'));
const missingRecord=render(contextual.default,{...contextProps,view:'record',record:'observation/does-not-exist'});
assert.ok(missingRecord.includes('This evidence record is unavailable'));assert.ok(!missingRecord.includes('RECORD INSPECTOR'));
const actualRecord=render(contextual.default,{...contextProps,view:'record',record:'observation/icrc2017-native-plan'});
assert.ok(actualRecord.includes('Follow the evidence chain'));assert.ok(actualRecord.includes('p. 95'));assert.ok(actualRecord.includes('Back to compare candidates'));
const alternatives=render(contextual.default,{...contextProps,view:'readings'});assert.ok(alternatives.includes('Readings, editions'));assert.ok(!alternatives.includes('<img'));
const targets=render(components.Targets,{i,context:model.entryContext(i,'1'),onSelect});assert.ok(targets.includes('No acquisition target'));
const impactStart=render(contextual.default,{...contextProps,view:'impact'});assert.ok(impactStart.includes('Select a source below'));assert.ok(impactStart.includes('Repeated publications may report the same original observation.'));
console.log('Contextual evidence checks passed: shared cached snapshot/index, retained comparison controls/unknowns/targets, source chains, explicit missing records, and no duplicated passage, figure or standalone navigation.');

// Canonical sources feed the real map plan viewer and manuscript reader.
const plate=plans.find(plan=>plan.id==='abu-saraj-iv17');
assert.equal(plate.image,'dossiers/sion2002-plan5-iv17.webp');assert.equal(plate.width,660);assert.equal(plate.height,615);
assert.ok(plate.source.includes('Plan 5 p. 63'));assert.equal(plate.sourceUrl,'https://publications.iaa.org.il/atiqot/vol41/iss1/6/');
assert.equal(plate.licenseUrl,'https://creativecommons.org/licenses/by-nc/4.0/');
for(const value of ['Ofer Sion','CC BY-NC 4.0','source caption, scale and north arrow retained'])assert.ok(plate.credit.includes(value),value);
for(const value of ['No geographic registration','no rotation or annotation baked','right opening as northern'])assert.ok(plate.limit.includes(value),value);
const asset=new URL('../public/'+plate.image,import.meta.url);assert.ok(existsSync(asset));const signature=readFileSync(asset).subarray(0,12).toString('ascii');assert.ok(signature.startsWith('RIFF')&&signature.endsWith('WEBP'));
const concordance=i.by.get('entry/25').payload.edition_concordance;assert.equal(concordance.item_milik,'27');assert.equal(concordance.item_allegro,'26');
assert.ok(textData.source.includes('ETCBC dss 2.0.1'));assert.ok(textData.source.includes('CC BY-NC 4.0'));
const cancelled=textData.entries['60'].flatMap(line=>line.w).find(word=>word.h.some(([letters,flag])=>letters==='צח'&&flag==='x'));
assert.ok(cancelled);const cancellation=render(text.Segments,{w:cancelled});assert.ok(cancellation.includes('צח'));assert.ok(cancellation.includes('st-x'));
console.log('Canonical source checks passed: complete map plan asset, caption/credit/licence/orientation/registration limits, edition concordance and real reader cancellation renderer.');

// Contextual filters retain exact branch, period, assignment and unknowns.
const compared=model.comparisonRows(i,candidates,model.comparisonChoices(i,candidates)[0].key);
assert.deepEqual(filters.filterCandidateRows(compared,'','all'),compared);
const conflicts=filters.filterCandidateRows(compared,'','conflict');assert.ok(conflicts.some(r=>r.candidate.id==='iv11'));
for(const row of filters.filterCandidateRows(compared,'','fits'))assert.ok(row.result.payload.checks.every(c=>c.status==='compatible'));
const missing=controls.find(r=>r.candidate.key==='hypothesis/A41:XII/53');assert.ok(filters.filterCandidateRows([missing],'','unknown').includes(missing));assert.equal(filters.filterCandidateRows([missing],'','fits').length,0);
const iv17=filters.filterCandidateRows(compared,'IV17','all');assert.equal(iv17.length,1);assert.equal(iv17[0],compared.find(r=>r.candidate.id==='iv17'));
console.log('Filter checks passed: exact-branch candidate subsets, explicit missing results and source assignments.');

// Two primary destinations; research tools open within the selected passage.
const routes=siteNav.sectionRoutes('25');assert.equal(routes.map,'#entry-25/2d');assert.equal(routes.scroll,'#entry-25/scroll');
for(const active of ['map','scroll']){
 const html=render(siteNav.default,{entry:'25',active});
 for(const label of ['Atlas sections','Map','Scroll','Research tools'])assert.ok(html.includes(label));
 assert(html.includes('<details'));assert(!html.includes('More sections'));
 const primary=html.match(/<nav aria-label="Atlas sections">(.*?)<\/nav>/)?.[1];assert(primary&&!primary.includes('Evidence'));assert.equal((primary.match(/<a /g)||[]).length,2);
 assert.equal((html.match(/aria-current="page"/g)||[]).length,1);
}
console.log('Shared navigation checks passed: geographic map route, selected-entry context, direct section access and one active section.');
