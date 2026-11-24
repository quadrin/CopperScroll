import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const require=createRequire(import.meta.url);
function compile(file,deps={}){const exports={};const code=ts.transpileModule(readFileSync(new URL(file,import.meta.url),'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true}}).outputText.replaceAll("import.meta.env", "({})");vm.runInNewContext(code,{exports,URLSearchParams,require:n=>n.endsWith('.css')?{}:deps[n]??require(n)});return exports;}
const routing=compile('../app/atlas-navigation.ts');
const contextRoutes=compile('../app/atlas-context-routes.ts');
const siloam=compile('../app/atlas-siloam-navigation.tsx',{'./atlas-siloam-reading':compile('../app/atlas-siloam-reading.ts')});
const nav=compile('../app/atlas-site-nav.tsx',{'./atlas-siloam-navigation':siloam,'./atlas-navigation':routing,'./atlas-context-routes':contextRoutes});
const html=renderToStaticMarkup(React.createElement(nav.default,{entry:'21',active:'map'}));
const primary=html.match(/<nav aria-label="Atlas sections">(.*?)<\/nav>/)?.[1];
assert(primary);assert.equal((primary.match(/<a /g)??[]).length,4);assert(primary.includes('Field notes'));assert(!primary.includes('Evidence')&&primary.includes('Map')&&primary.includes('Scroll'));
assert(primary.includes('What is the Copper Scroll?'));assert.equal(nav.sectionRoutes('25').introduction,'#what-is-the-copper-scroll');assert(html.includes('Research tools'));assert(html.includes('Connection graph'));
assert(!html.includes('More sections'));assert(html.includes('<details'));assert(!html.includes('Sites &amp; 3D'));assert(!html.includes('Eye-level simulation'));
assert.equal(nav.sectionRoutes('25').map,'#entry-25/2d');
assert.equal(nav.sectionRoutes('25').scroll,'#entry-25/scroll');
const map=readFileSync(new URL('../app/atlas-map.tsx',import.meta.url),'utf8');
assert(map.includes('aria-label="Site reference panel"'));
assert(!map.includes('map-place-details'));assert(!map.includes('Show selected site details'));assert(map.includes('Inspect site'));assert(!map.includes('onDetails'));assert(map.includes('document.addEventListener("pointerdown",close)'));assert(map.includes('document.addEventListener("keydown",escape)'));
assert(!map.includes('className="map-selection-note"'));assert(!map.includes('className="terrain-controls"'));assert(!map.includes('className="map-legend"'));
assert(map.includes('startMapWalk'));assert(map.includes('createMapSiteLayer'));assert.equal((map.match(/className="map-place-panel"/g)??[]).length,1);
assert(map.includes('<SiteReference '));assert(!map.includes('SiteExplorer'));
console.log('Interface checks passed: map/scroll plus the explainer and contextual research tools, source-plan defaults, one place panel, one map surface with inline references, dismissal handlers and no legacy floating cards.');

const reader=compile('../app/atlas-reader-branches.tsx',{'./atlas-siloam-navigation':siloam,'./atlas-siloam-reading':compile('../app/atlas-siloam-reading.ts')});
const siloamDetails=compile('../app/atlas-siloam-comparison.tsx',{
 './atlas-siloam-navigation':siloam,'./atlas-siloam-reading':compile('../app/atlas-siloam-reading.ts'),
 './atlas-dossiers-data':compile('../app/atlas-dossiers-data.ts'),
 './atlas-site-gallery.json':JSON.parse(readFileSync(new URL('../app/atlas-site-gallery.json',import.meta.url),'utf8')),
});
const state={entryId:'49',mode:'site',placeId:'jer_siloam',planId:'siloam-receiver',siloamReading:'displayed-baths',siloamSubject:'conduit',featureId:'L103'};
function renderAt(component,props) {
 return renderToStaticMarkup(React.createElement(siloam.default,{state,navigate:()=>{}},React.createElement(component,props)));
}
assert.match(renderAt(reader.default,{entryId:'49'}), /aria-pressed="true"><strong>Base text · baths/);
assert.match(renderAt(siloamDetails.default,{}), /0.75 m above the small receiver floor/);
const contextualHeader=renderAt(nav.default,{entry:'49',active:'map',place:'jer_siloam'});
assert.match(contextualHeader, /site\/siloam-receiver\/L103\/source\?reading=displayed-baths&amp;subject=conduit/);
assert.match(contextualHeader, /scroll\?reading=displayed-baths&amp;subject=conduit&amp;feature=L103/);
console.log('Siloam passage, map panel and section links share the selected reading and feature.');
