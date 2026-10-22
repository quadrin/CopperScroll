// Builds the atlas's source-based site models in a Minecraft Java server, saves the
// world, reads every block and its sky light back from the region files, and writes
// the block meshes that the atlas map renders (public/minecraft/).
//
//   node scripts/minecraft/build-world.mjs --jar server.jar --java /path/to/java --work <dir> [--sites a,b]
//   node scripts/minecraft/build-world.mjs --work <dir> --skip-server   (re-read an existing save)
//
// The server jar is Mojang's official download; running it requires accepting the
// Minecraft EULA (https://aka.ms/MinecraftEULA). Nothing from the game (code, textures)
// is copied into the atlas: only block positions and light values read from the save.
import {parseArgs} from 'node:util';
import {spawn} from 'node:child_process';
import {mkdirSync,writeFileSync,readFileSync,existsSync,rmSync,readdirSync} from 'node:fs';
import {createHash,randomBytes} from 'node:crypto';
import {setTimeout as sleep} from 'node:timers/promises';
import * as T from 'three';
import {loadModels,siteContextFeatures} from './load-models.mjs';
import {createGrid,rasterGround,rasterSolids,carve,underfill,toBlocks,fillBoxes,blockTable,MATERIALS} from './voxelize.mjs';
import {World} from './anvil.mjs';
import {connectRcon} from './rcon.mjs';
import {greedyQuads,encodeBuild} from './mesh.mjs';

// Block size in the model's units (metres, or the relative units of the source-plan
// scenes). Half a block is the vertical step, through slabs. A site may set its own
// terrain rings; a ring with `context` also builds the mapped surroundings in it.
// The plans placed in a mapped setting get 1 m rings with the mapped surroundings in them.
const CONTEXT_RINGS=[{size:1,half:304,context:true},{size:8,half:1152}];
export const SITES=[
 {id:'qumran-ilan',size:.5,pilot:true,place:'kh_qumran',domain:{minX:-90,maxX:90,minZ:-66,maxZ:54}},
 {id:'qumran-reeder',size:.25},
 {id:'jericho-ac',size:.25},
 {id:'jericho-early',size:.25,rings:CONTEXT_RINGS},
 {id:'jericho-late',size:.25,rings:CONTEXT_RINGS},
 {id:'siloam-receiver',size:.25},
 {id:'gerizim-precinct',size:.5,rings:CONTEXT_RINGS},
 {id:'doq-waterworks',size:.25},
 {id:'hyrcania-waterworks',size:.25,rings:CONTEXT_RINGS},
 {id:'abu-saraj-iv17',size:.25,roof:true,mapped:false},
 {id:'bethesda-pools',size:.5,rings:CONTEXT_RINGS},
 {id:'east-gate-warren',size:.5,rings:CONTEXT_RINGS},
 {id:'kidron-bene-hezir',size:.25,rings:CONTEXT_RINGS},
 {id:'temple-great-sea',size:.5,rings:CONTEXT_RINGS},
];
const PILOT_GROUND=new Set(['qumran-ground','qumran-ridge-back','connected-limestone-bed']);
// Plans with the wide terrain patch get coarser block rings around them, each with a
// hole exactly the size of the build inside it.
export const RINGS=[{size:2,half:400},{size:8,half:1152}];
// A traced plan outside SITES takes the context rings when it is placed in a mapped setting.
const PLACED_TRACED=new Set(['qumran-settlement']);
export const ringsFor=planId=>SITES.find(s=>s.id===planId)?.rings??(PLACED_TRACED.has(planId)?CONTEXT_RINGS:RINGS);
export const buildKey=(planId,layer)=>layer&&layer!=='remains'?`${planId}@${layer}`:planId;

// One build per site; a traced plan, or a hand-built plan with views, gives one per layer
// (remains, each published phase).
export function buildSpecs(models){
 const specs=[],traced=plan=>plan?.traced&&models.tracedPlans[plan.traced];
 const planSpecs=(plan,base)=>traced(plan)||plan?.layers?.length?(plan.layers??[{id:'remains'}]).map(l=>({...base,id:buildKey(plan.id,l.id),plan:plan.id,layer:l.id})):[{...base,plan:plan.id}];
 for(const spec of SITES)specs.push(...planSpecs(models.plans.find(p=>p.id===spec.id),spec));
 for(const plan of models.plans)if(traced(plan)&&!SITES.some(s=>s.id===plan.id))specs.push(...planSpecs(plan,{id:plan.id,size:plan.blockSize??.5}));
 for(const plan of models.plans)if(plan.terrain==='wide'&&specs.some(s=>s.plan===plan.id))ringsFor(plan.id).forEach((r,i)=>specs.push({id:`${plan.id}~ring${i+1}`,plan:plan.id,ring:i,size:r.size,half:r.half,context:!!r.context}));
 return specs;
}
// Wider terrain (atlas/public/terrain), decoded to the landscape patch shape.
export function wideTerrain(placeId){
 const path=new URL(`../../public/terrain/${placeId}.json`,import.meta.url);if(!existsSync(path))return undefined;
 const t=JSON.parse(readFileSync(path,'utf8')),bytes=Buffer.from(t.data,'base64'),elevations=new Array(t.size*t.size);
 for(let i=0;i<elevations.length;i++)elevations[i]=t.centreElevation+bytes.readInt16LE(i*2)/10;
 return {lat:t.lat,lon:t.lon,anchorPrecision:'wide patch',extent:t.extent,size:t.size,elevations,centreElevation:t.centreElevation};
}

export function voxelizeSite(models,spec){
 const plan=models.plans.find(p=>p.id===(spec.plan??spec.id));let root,ground=[],domain=spec.domain,carves=[],exclude=null;
 const options={layer:spec.layer,terrain:plan?.terrain==='wide'?wideTerrain(plan.placeIds[0]):undefined,context:plan?.terrain==='wide'?siteContextFeatures(plan.id):undefined},snap=(v,s,up)=>(up?Math.ceil(v/s):Math.floor(v/s))*s;
 if(spec.pilot){
  root=models.pilot.buildQumranPilot();const patch=models.terrain[spec.place];
  // The same Mapterhorn patch the atlas uses around the anchor, fitted once.
  models.pilot.fitQumranGround(root,(x,z)=>models.landscape.elevationAt(patch,x,z));
  root.updateMatrixWorld(true);
  root.traverse(o=>{if(o.isMesh&&PILOT_GROUND.has(o.name))ground.push(o);});
  // The tunnel recess behind the dark display plane becomes a real opening.
  root.traverse(o=>{if(o.isMesh&&o.material?.color?.getHexString?.()==='191913'){const b=new T.Box3().setFromObject(o),c=b.getCenter(new T.Vector3());carves.push({minX:c.x-.66,maxX:c.x+.66,minY:b.min.y+.14,maxY:b.max.y-.07,minZ:b.min.z-.05,maxZ:b.min.z+3.2});}});
 }else{
  const model=models.geometry.buildModel(plan,options);root=model.root;if(spec.roof)model.roof.visible=true;
  root.updateMatrixWorld(true);
  root.traverse(o=>{if(o.isMesh&&o.userData.siteContext==='ground')ground.push(o);});
  // With terrain rings, the build's edges fall on the inner ring's cells; otherwise they are the model's frame.
  const rings=ringsFor(plan.id),f=model.framing,edge=(v,up)=>options.terrain?snap(v,rings[0].size,up):v;
  domain??={minX:edge(f.min.x,false),maxX:edge(f.max.x,true),minZ:edge(f.min.z,false),maxZ:edge(f.max.z,true)};
  if(spec.ring!==undefined){
   // A ring holds only terrain; its hole is the build inside it, cell for cell.
   const inner=spec.ring?rings[spec.ring-1].half:null;
   exclude=inner?{minX:-inner,maxX:inner,minZ:-inner,maxZ:inner}:domain;
   domain={minX:-spec.half,maxX:spec.half,minZ:-spec.half,maxZ:spec.half};
  }
 }
 // A ring holds terrain, and in a context ring the mapped surroundings except fine detail (stair treads).
 const solids=[],mapped=new Set();root.traverse(o=>{if(o.userData.siteContext==='osm')o.traverse(c=>mapped.add(c));});
 root.traverseVisible(o=>{if(!o.isMesh||ground.includes(o)||(o.userData.walkCollision===false&&!o.userData.blockSolid))return;if(spec.ring===undefined||(spec.context&&mapped.has(o)&&!o.userData.contextFine))solids.push(o);});
 // Vertical extent: everything inside the domain, with a margin below for the ground.
 let minY=Infinity,maxY=-Infinity;const p=new T.Vector3();
 for(const mesh of ground){
  if(mesh.userData.heightAt){for(let x=domain.minX;x<=domain.maxX;x+=Math.max(spec.size,1))for(let z=domain.minZ;z<=domain.maxZ;z+=Math.max(spec.size,1)){if(Math.hypot(x,z)>mesh.userData.radius)continue;const y=mesh.userData.heightAt(x,z);minY=Math.min(minY,y);maxY=Math.max(maxY,y);}continue;}
  const pos=mesh.geometry.getAttribute('position');for(let i=0;i<pos.count;i++){p.fromBufferAttribute(pos,i).applyMatrix4(mesh.matrixWorld);if(p.x>=domain.minX&&p.x<=domain.maxX&&p.z>=domain.minZ&&p.z<=domain.maxZ){minY=Math.min(minY,p.y);maxY=Math.max(maxY,p.y);}}
 }
 // Scattered rubble spans the whole terrain disc; it lies on the ground, so it adds no extent.
 const extend=b=>{if(b.max.x<domain.minX||b.min.x>domain.maxX||b.max.z<domain.minZ||b.min.z>domain.maxZ)return;minY=Math.min(minY,b.min.y);maxY=Math.max(maxY,b.max.y);};
 for(const mesh of solids){
  if(mesh.userData.walkDetail)continue;
  // Instances spread over the whole surroundings (graves, wall stretches) count one by one.
  if(mesh.isInstancedMesh&&mapped.has(mesh)){mesh.geometry.computeBoundingBox();const m=new T.Matrix4();for(let n=0;n<mesh.count;n++){mesh.getMatrixAt(n,m);extend(mesh.geometry.boundingBox.clone().applyMatrix4(m.premultiply(mesh.matrixWorld)));}continue;}
  if(mapped.has(mesh)){const pos=mesh.geometry.getAttribute('position');for(let i=0;i<pos.count;i++){p.fromBufferAttribute(pos,i).applyMatrix4(mesh.matrixWorld);extend(new T.Box3(p,p));}continue;}
  extend(new T.Box3().setFromObject(mesh));
 }
 const grid=createGrid({...domain,minY:minY-1,maxY:maxY+.5,size:spec.size});
 rasterGround(grid,ground,{exclude});
 rasterSolids(grid,solids,{minDetail:spec.size*.8});
 for(const box of carves)carve(grid,box);
 if(exclude&&spec.context)carve(grid,{...exclude,minY:-Infinity,maxY:Infinity});
 underfill(grid);
 const masonry=models.surfaces.siteStyle(plan.id).masonry,blocks=toBlocks(grid,masonry);
 return {spec,plan,grid,blocks,masonry,features:grid.features};
}

function properties(password){
 return Object.entries({
  'server-ip':'127.0.0.1','server-port':'25565','enable-rcon':'true','rcon.port':'25575','rcon.password':password,'broadcast-rcon-to-ops':'false',
  'online-mode':'false','level-name':'world','level-type':'minecraft:flat',
  // A void superflat world: nothing but the builds.
  'generator-settings':JSON.stringify({layers:[{block:'minecraft:air',height:1}],biome:'minecraft:the_void'}),
  'generate-structures':'false','difficulty':'peaceful','spawn-protection':'0','view-distance':'4','simulation-distance':'4','sync-chunk-writes':'true','region-file-compression':'deflate','max-players':'1',
  // An empty server pauses after a minute by default, which would stop chunk loading and lighting.
  'pause-when-empty-seconds':'86400',
 }).map(([k,v])=>`${k}=${v}`).join('\n')+'\n';
}

async function runServer({jar,java,work,builds,log}){
 rmSync(`${work}/world`,{recursive:true,force:true});mkdirSync(work,{recursive:true});
 const password=randomBytes(12).toString('hex');
 writeFileSync(`${work}/server.properties`,properties(password));
 // Accepting the Minecraft EULA is required to run the official server.
 writeFileSync(`${work}/eula.txt`,'eula=true\n');
 const server=spawn(java,['-Xms2G','-Xmx8G','-jar',jar,'--nogui'],{cwd:work,stdio:['pipe','pipe','pipe']});
 let output='';const ready=new Promise((resolve,reject)=>{
  server.stdout.on('data',d=>{const text=d.toString();output+=text;log(text.trimEnd());if(/RCON running on/.test(output)&&/Done \(/.test(output))resolve();});
  server.stderr.on('data',d=>log(d.toString().trimEnd()));server.on('exit',code=>reject(Error(`Server exited (${code})`)));
 });
 await ready;
 const rcon=await connectRcon({port:25575,password}),run=async(command)=>rcon.command(command);
 const version=output.match(/Starting minecraft server version (\S+)/)?.[1]??null;
 const report={};
 for(const build of builds){
  const {nx,ny,nz}=build.blocks,{x0,z0,y0}=build.world;
  for(let cx=Math.floor(x0/16);cx<=Math.floor((x0+nx-1)/16);cx+=16)for(let cz=Math.floor(z0/16);cz<=Math.floor((z0+nz-1)/16);cz+=16){
   const r=await run(`forceload add ${cx*16} ${cz*16} ${Math.min(cx+15,Math.floor((x0+nx-1)/16))*16} ${Math.min(cz+15,Math.floor((z0+nz-1)/16))*16}`);
   if(!/Marked|already/i.test(r))throw Error(`forceload: ${r}`);
  }
  const boxes=fillBoxes(build.blocks),commands=boxes.map(([i,Y,k,i1,Y1,k1,state])=>`fill ${x0+i} ${y0+Y} ${z0+k} ${x0+i1} ${y0+Y1} ${z0+k1} minecraft:${build.blocks.palette[state]}`);
  let pending=commands,filled=0,attempts=0;
  while(pending.length&&attempts++<40){
   const retry=[];
   // One command at a time: the vanilla RCON listener reads a single packet per socket read.
   for(const command of pending){
    const reply=await run(command),m=reply.match(/(?:Successfully filled|filled) (\d+)/i);
    if(m)filled+=+m[1];else if(/not loaded/i.test(reply))retry.push(command);else throw Error(`${command} → ${reply}`);
   }
   pending=retry;if(pending.length){log(`${build.spec.id}: ${pending.length} fills wait for chunk loading`);await sleep(2000);}
  }
  if(pending.length)throw Error(`${build.spec.id}: ${pending.length} fills never found loaded chunks`);
  report[build.spec.id]={commands:commands.length,filled};log(`${build.spec.id}: ${commands.length} fill commands, ${filled} blocks`);
 }
 // The saved world opens in creative mode in front of the Qumran tunnel mouth.
 await run('defaultgamemode creative');await run('setworldspawn 188 -23 163');
 // Let the light engine settle before saving.
 await sleep(8000);
 log(await run('save-all flush'));await sleep(3000);
 await run('stop').catch(()=>{});await new Promise(resolve=>server.once('exit',resolve));rcon.close();
 return {version,report};
}

// Requested and read-back states compare without the default waterlogged flag. Since
// 26.x a block's default state is saved as its bare name; for a slab that is the bottom half.
// Leaves also save their distance to the nearest log, which the build does not set.
const normal=state=>state.replace(/,?waterlogged=false/,'').replace(/distance=\d+,?/,'').replace(/\[\]$/,'').replace(/\[,/,'[').replace(/_slab$/,'_slab[type=bottom]');

export function readBack(world,build){
 const {nx,ny,nz,blocks,palette,feature}=build.blocks,{x0,y0,z0}=build.world,table=blockTable(build.masonry);
 const decode=new Map();
 for(const [code,[full,slab]] of Object.entries(table)){decode.set(full,[+code,3]);if(slab){decode.set(`${slab}[type=bottom]`,[+code,1]);decode.set(`${slab}[type=top]`,[+code,2]);decode.set(`${slab}[type=double]`,[+code,3]);}}
 const cells=new Uint8Array(nx*ny*2*nz),cellFeature=new Uint8Array(cells.length),light=new Uint8Array(cells.length),counts={};
 let mismatches=0,missingLight=0;const examples=[];
 for(let i=0;i<nx;i++)for(let k=0;k<nz;k++)for(let Y=0;Y<ny;Y++){
  const n=(i*nz+k)*ny+Y,state=normal(world.block(x0+i,y0+Y,z0+k)),wanted=palette[blocks[n]];
  if(state!==wanted){mismatches++;if(examples.length<8)examples.push({at:[x0+i,y0+Y,z0+k],wanted,found:state});}
  counts[state]=(counts[state]??0)+1;
  const c=(i*nz+k)*ny*2+2*Y,[code,shape]=state==='air'?[0,0]:decode.get(state)??[0,0];
  if(shape&1)cells[c]=code;if(shape&2)cells[c+1]=code;cellFeature[c]=cellFeature[c+1]=feature[n];
  let sky=world.skyLight(x0+i,y0+Y,z0+k);if(sky===null){missingLight++;sky=15;}light[c]=light[c+1]=sky;
 }
 return {cells,feature:cellFeature,light,counts,mismatches,examples,missingLight,dims:{nx,ny:ny*2,nz}};
}

async function main(){
 const {values}=parseArgs({options:{jar:{type:'string'},java:{type:'string',default:'java'},work:{type:'string'},sites:{type:'string'},'skip-server':{type:'boolean',default:false},out:{type:'string',default:new URL('../../public/minecraft/',import.meta.url).pathname}}});
 if((!values.jar&&!values['skip-server'])||!values.work)throw Error('Usage: build-world.mjs --jar server.jar --work <dir> [--java java] [--sites a,b] [--skip-server]');
 const log=text=>process.stdout.write(`${text}\n`),models=loadModels(),wanted=values.sites?.split(',');
 const jarSha1=values.jar?createHash('sha1').update(readFileSync(values.jar)).digest('hex'):null;
 const builds=[];
 buildSpecs(models).forEach((spec,index)=>{
  if(wanted&&!wanted.includes(spec.id)&&!wanted.includes(spec.plan))return;
  const started=Date.now(),build=voxelizeSite(models,spec);
  // Each site has its own 1,024-block-wide strip of the world; the grid floor sits at y = -60.
  build.world={x0:index*1024,z0:0,y0:-60};
  if(build.blocks.ny>370)throw Error(`${spec.id}: ${build.blocks.ny} blocks high does not fit the world`);
  builds.push(build);log(`${spec.id}: ${build.blocks.nx}×${build.blocks.ny}×${build.blocks.nz} blocks at ${spec.size} per block (${Date.now()-started} ms)`);
 });
 const server=values['skip-server']?{version:null,report:{}}:await runServer({jar:values.jar,java:values.java,work:values.work,builds,log});
 const regionDir=[`${values.work}/world/region`,`${values.work}/world/dimensions/minecraft/overworld/region`].find(existsSync);
 if(!regionDir)throw Error('No region folder in the saved world');
 const world=new World(regionDir);mkdirSync(values.out,{recursive:true});
 const indexPath=`${values.out}/index.json`,index=existsSync(indexPath)?JSON.parse(readFileSync(indexPath,'utf8')):{sites:{}};
 if(!values['skip-server']){index.minecraft={edition:'Java Edition',version:server.version,serverJarSha1:jarSha1,dataVersion:null};index.built=new Date().toISOString().slice(0,10);}
 index.minecraft??={edition:'Java Edition',version:null,serverJarSha1:null,dataVersion:null};
 for(const build of builds){
  const back=readBack(world,build),{grid,spec}=build;
  index.minecraft.dataVersion??=world.chunk(Math.floor(build.world.x0/16),0)?.dataVersion??null;
  const groups=greedyQuads({...back.dims,cells:back.cells,feature:back.feature,light:back.light});
  // The header lists materials up to the highest code used (at least the eight site materials).
  const used=Math.max(7,...[...groups.keys()].map(k=>+k.split(':')[0]));
  const header={version:1,id:spec.id,plan:spec.plan,layer:spec.layer??null,ring:spec.ring??null,size:grid.s,half:grid.h,origin:[grid.x0,grid.y0,grid.z0],dims:[back.dims.nx,back.dims.ny,back.dims.nz],materials:MATERIALS.slice(0,used+1),masonry:build.masonry,features:build.features};
  const file=encodeBuild(header,groups),quads=[...groups.values()].reduce((sum,q)=>sum+q.length/6,0);
  if(spec.mapped!==false)writeFileSync(`${values.out}/${spec.id}.bin.gz`,file);
  // The Qumran build's ground was fitted to one place's terrain patch; it fits only there.
  const rings=spec.ring===undefined?builds.filter(b=>b.spec.plan===spec.plan&&b.spec.ring!==undefined).map(b=>b.spec.id):[];
  index.sites[spec.id]={file:spec.mapped===false?null:`${spec.id}.bin.gz`,plan:spec.plan,layer:spec.layer??null,ring:spec.ring??null,surroundings:rings.length?rings:null,terrainPlace:spec.pilot?spec.place:null,bytes:file.length,blockSize:grid.s,origin:header.origin,blocks:[build.blocks.nx,build.blocks.ny,build.blocks.nz],world:build.world,masonry:build.masonry,
   fills:server.report[spec.id]??index.sites[spec.id]?.fills,readback:{blocks:build.blocks.nx*build.blocks.ny*build.blocks.nz,mismatches:back.mismatches,examples:back.examples,missingSkyLight:back.missingLight},counts:Object.fromEntries(Object.entries(back.counts).filter(([k])=>k!=='air').sort()),quads};
  log(`${spec.id}: read back, ${back.mismatches} mismatches, ${back.missingLight} blocks without saved sky light, ${quads} quads, ${(file.length/1024).toFixed(0)} KiB`);
 }
 writeFileSync(indexPath,JSON.stringify(index,null,1)+'\n');
 log(`Region files: ${readdirSync(regionDir).join(', ')}`);
}
if(import.meta.url===`file://${process.argv[1]}`)main().catch(e=>{console.error(e);process.exit(1);});
