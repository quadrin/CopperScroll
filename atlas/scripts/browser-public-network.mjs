// Chromium cannot reach loopback through the cloud egress proxy. Forward only
// public map/image requests via curl, preserving proxy routing and TLS checks.
const {execFile}=await import('node:child_process');
const {promisify}=await import('node:util');
const {mkdtemp,readFile,rm}=await import('node:fs/promises');
const {tmpdir}=await import('node:os');
const {join}=await import('node:path');
const run=promisify(execFile);
export async function forwardPublic(route){
 const dir=await mkdtemp(join(tmpdir(),'atlas-network-'));
 try{
  await run('curl',['--silent','--show-error','--fail','--location','--compressed','--max-time','45','--dump-header',join(dir,'headers'),'--output',join(dir,'body'),route.request().url()]);
  const raw=await readFile(join(dir,'headers'),'utf8');const blocks=raw.trim().split(/\r?\n\r?\n/);const last=blocks[blocks.length-1];
  const type=last.match(/^content-type:\s*(.+)$/im)?.[1].trim()??'application/octet-stream';
  await route.fulfill({status:200,contentType:type,body:await readFile(join(dir,'body'))});
 }catch{await route.abort('failed')}finally{await rm(dir,{recursive:true,force:true});}
}
