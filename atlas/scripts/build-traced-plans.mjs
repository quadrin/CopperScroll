// Checks the traced plans in research/models/traced_plans (format: SCHEMA.md there) and
// writes the compact copy the atlas builds from, app/atlas-traced-plans.json.
//   node scripts/build-traced-plans.mjs [--check]
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,readdirSync} from 'node:fs';

const dir=new URL('../../research/models/traced_plans/',import.meta.url),out=new URL('../app/atlas-traced-plans.json',import.meta.url);
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const finite=(v,what)=>assert.ok(Number.isFinite(v),`${what}: not a finite number`);
const point=(p,what)=>{assert.ok(Array.isArray(p)&&p.length===2,`${what}: not a point`);p.forEach(v=>finite(v,what));};
const result={};
for(const name of readdirSync(dir).filter(f=>f.endsWith('.json')).sort()){
 const t=JSON.parse(readFileSync(new URL(name,dir),'utf8')),where=`${name}`;
 assert.equal(`${t.id}.json`,name,`${where}: id must match the file name`);
 assert.ok(t.frame&&t.sources?.length&&t.layers?.length&&t.elements?.length,`${where}: frame, sources, layers and elements are required`);
 const layers=new Set(t.layers.map(l=>l.id)),sources=new Set(t.sources.map(s=>s.id));
 for(const l of t.layers)assert.ok(['observed','published-reconstruction'].includes(l.kind),`${where}: layer ${l.id} kind`);
 const ids=new Set();
 for(const e of t.elements){
  const at=`${where} ${e.id}`;assert.ok(e.id&&!ids.has(e.id),`${at}: element ids must be unique`);ids.add(e.id);
  assert.ok(e.layers?.length&&e.layers.every(l=>layers.has(l)),`${at}: unknown layer`);
  assert.ok(['observed','published-reconstruction','project-inference'].includes(e.status),`${at}: status`);
  // An element drawn from several figures names them joined by "+".
  for(const s of e.source?String(e.source).split(/\s*\+\s*/):[])assert.ok(sources.has(s),`${at}: unknown source ${s}`);
  const g=e.geometry;
  if(g.type==='raster'){
   point(g.origin,at);finite(g.cell,at);const runs=typeof g.rle==='string'?g.rle.split(/[\s,]+/).filter(Boolean).map(Number):g.rle;
   assert.equal(runs.reduce((a,b)=>a+b,0),g.cols*g.rows,`${at}: raster runs must cover ${g.cols} × ${g.rows} cells`);
  }else if(g.type==='point'){point(g.at??g.points?.[0],at);if(g.radius!=null)finite(g.radius,at);}
  else{assert.ok(['polyline','polygon'].includes(g.type),`${at}: geometry type ${g.type}`);assert.ok(g.points.length>=2,`${at}: too few points`);g.points.forEach(p=>point(p,at));if(g.width!=null)finite(g.width,at);}
  for(const v of Object.values(e.levels??{}))if(typeof v==='number')finite(v,at);
 }
 // Keep what the builder and the atlas read; the full record stays in research.
 result[t.id]={id:t.id,title:t.title,frame:{origin:t.frame.origin,north:t.frame.north,datum:t.frame.datum??null,ground:t.frame.ground??null},
  sources:t.sources.map(s=>({id:s.id,citation:s.citation})),layers:t.layers.map(l=>({id:l.id,label:l.label,kind:l.kind})),
  elements:t.elements.map(e=>{const g=e.geometry.type==='point'&&!e.geometry.at?{...e.geometry,at:e.geometry.points[0],points:undefined}:e.geometry;return {id:e.id,label:e.label,kind:e.kind,layers:e.layers,status:e.status,lineStyle:e.lineStyle,geometry:g,levels:e.levels,height:e.height,steps:e.steps,source:e.source,locator:e.locator};}),
  features:t.features?.filter(f=>f.at).map(f=>({id:f.id,at:f.at})),walkStart:t.walkStart,focus:t.focus?.at};
}
// Plans that name a traced plan must name its layers in the same order.
for(const plan of plans.filter(p=>p.traced)){
 const t=result[plan.traced];if(!t)continue;
 for(const l of plan.layers??[])assert.ok(t.layers.some(x=>x.id===l.id&&x.kind===l.kind),`${plan.id}: layer ${l.id} is not in ${plan.traced}`);
}
const text=JSON.stringify(result)+'\n';
if(process.argv.includes('--check')){assert.equal(readFileSync(out,'utf8'),text,'app/atlas-traced-plans.json is out of date: run node scripts/build-traced-plans.mjs');console.log(`Traced plans current: ${Object.keys(result).join(', ')||'none'}.`);}
else{writeFileSync(out,text);console.log(`Wrote ${Object.keys(result).length} traced plans: ${Object.keys(result).join(', ')||'none'}.`);}
