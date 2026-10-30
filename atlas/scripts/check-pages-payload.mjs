// Validate the actual output of GitHub's Jekyll Pages builder.
// Intentionally do not model Jekyll include/exclude rules here.
import assert from 'node:assert/strict';
import {existsSync,readFileSync,readdirSync,statSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
const option=process.argv.indexOf('--site-dir');assert(option!==-1&&process.argv[option+1],'Provide --site-dir with the actual Jekyll output directory');
const output=resolve(process.argv[option+1]);assert(output!==resolve(root),'Validate generated output, not the source checkout');
assert(existsSync(output+'/index.html'),'The published homepage is missing');
function files(directory,prefix=''){return readdirSync(directory,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(directory+'/'+e.name,prefix+e.name+'/'):[prefix+e.name]);}
const published=files(output),bytes=published.reduce((n,p)=>n+statSync(output+'/'+p).size,0);
assert(bytes<1024**3,'The Pages output must stay below 1 GiB');
for(const directory of ['atlas','research','images','private-media'])assert(!published.some(p=>p.startsWith(directory+'/')),directory+' archive leaked into the published output');
// The WSRP 1988 photographs belong only to the access-controlled build.
assert(!published.some(p=>/(^|\/)(wsrp|media)\//.test(p)||p.endsWith('.enc')),'Protected images or encrypted media leaked into the public Pages output');
for(const name of ['index.html',...files(root+'atlas-site').map(p=>'atlas-site/'+p)]){
 assert(existsSync(output+'/'+name),'Missing published app file: '+name);
 assert(readFileSync(output+'/'+name).equals(readFileSync(root+name)),'Jekyll changed app bytes: '+name);
}
for(const name of ['index.html','atlas-site/index.html']){
 const html=readFileSync(output+'/'+name,'utf8');
 for(const match of html.matchAll(/(?:src|href)="\/CopperScroll\/([^"?#]+)/g))assert(existsSync(output+'/'+match[1]),'Missing startup asset: '+match[1]);
}
console.log(`Actual Pages output passed: ${(bytes/1024**2).toFixed(1)} MiB; all app files retain their bytes, startup assets resolve, research archives are absent.`);
