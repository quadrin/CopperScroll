// Loads the atlas's source-model builders in Node, the same way check-models.mjs does.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import ts from 'typescript';
import * as Three from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';

const app=path=>new URL(`../../app/${path}`,import.meta.url);
const json=path=>JSON.parse(readFileSync(app(path),'utf8'));
function module(path,deps){const exports={};const code=ts.transpileModule(readFileSync(app(path),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;new Function('exports','require',code)(exports,name=>{assert(name in deps,`Missing dependency: ${name}`);return deps[name]});return exports;}
const asModule=value=>({__esModule:true,default:value,...value});

// SVGLoader parses the generic plans' path strings through DOMParser. Node has none;
// these strings are only <svg>, <g transform> and <path d> elements, so a small
// element tree is enough.
class Element{
 constructor(nodeName,attributes){this.nodeType=1;this.nodeName=nodeName;this.attributes=attributes;this.childNodes=[];this.style=undefined;}
 hasAttribute(name){return name in this.attributes;}
 getAttribute(name){return this.attributes[name]??null;}
 getElementsByTagName(){return [];}
 querySelectorAll(){return [];}
}
globalThis.DOMParser??=class{
 parseFromString(text){
  const root=new Element('#document',{}),stack=[root];
  for(const [,close,name,body,self] of text.matchAll(/<(\/?)([\w:-]+)([^>]*?)(\/?)>/g)){
   if(close){stack.pop();continue;}
   const attributes=Object.fromEntries([...body.matchAll(/([\w:-]+)="([^"]*)"/g)].map(([,k,v])=>[k,v]));
   const node=new Element(name,attributes);stack.at(-1).childNodes.push(node);if(!self)stack.push(node);
  }
  return {documentElement:root.childNodes[0],querySelectorAll:()=>[]};
 }
};

export function loadModels(){
 const terrain=json('atlas-model-terrain.json'),siteSurfaces=json('atlas-site-surfaces.json');
 const surfaces=module('atlas-site-materials.ts',{'three':Three,'./atlas-site-surfaces.json':asModule(siteSurfaces)});
 const landscape=module('atlas-model-landscape.ts',{'three':Three,'./atlas-model-terrain.json':terrain,'./atlas-site-materials':surfaces});
 const tracedHelpers=module('atlas-traced.ts',{}),tracedPlans=json('atlas-traced-plans.json');
 const geometry=module('atlas-model-geometry.ts',{'three':Three,'three/addons/loaders/SVGLoader.js':{SVGLoader},'./atlas-model-landscape':landscape,'./atlas-site-materials':surfaces,'./atlas-traced':tracedHelpers,'./atlas-traced-plans.json':asModule(tracedPlans)});
 // The pilot only needs MercatorCoordinate for map placement helpers, not for its geometry.
 const pilot=module('atlas-qumran-pilot.ts',{'three':Three,'maplibre-gl':{MercatorCoordinate:class{}},'./atlas-site-materials':surfaces});
 return {Three,terrain,tracedPlans,plans:json('atlas-site-plans.json'),places:json('atlas-data.json').places,surfaces,landscape,geometry,pilot};
}
