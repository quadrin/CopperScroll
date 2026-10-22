import * as T from 'three';
import type {SiteFeature,SitePlan} from './atlas-explorer-model';

// Signs at eye level: a small card at each plan feature's marker with the feature's name, its first
// source citation and a status tag. Cards are DOM text over the map canvas, placed every frame from the
// matrix that draws the site, so they always face the camera and stay sharp. They take no pointer
// events and are not part of the walk colliders. They show within SIGN_RANGE metres of the walker's
// eye, fading out beyond SIGN_FULL; where two overlap on screen the nearer one is shown.
export const SIGN_RANGE=40,SIGN_FULL=25;

// The tag reports the record's kind, not an identification.
const STATUS:Record<string,[string,string]>={
 'Reported remains':['Observed','observed'],'Excavated locus':['Observed','observed'],'Area on the general plan':['Observed','observed'],
 'Published reconstruction':['Reconstruction','reconstruction'],
 'Proposed scroll association':['Proposed association','proposed'],
 'Historical survey context':['Survey context','survey'],
};
export const signStatus=(kind:string)=>STATUS[kind]?.[0]??null;

// A line under the tag where the model's own drawing of the feature is illustrative in size or height.
// Each line restates a sentence of the record and is shown only while that sentence (`evidence`) is still
// in the feature's limit, the plan's limit or the built model's assumptions (`in`). Features not listed
// take a line only when the whole model says its heights are illustrative (MODEL_WIDE).
type DrawingNote={line:string;evidence:string;in:'feature'|'plan'|'model'};
export const MODEL_DRAWING:Record<string,DrawingNote>={
 'qumran-ilan/dam4':{line:'Height and width in the model are illustrative.',evidence:'its height and width are illustrative',in:'feature'},
 'gerizim-precinct/persian-precinct':{line:'Gate sizes in the model are illustrative.',evidence:'their sizes in the model are illustrative',in:'feature'},
 'gerizim-precinct/mansion':{line:'Its level in the model is illustrative.',evidence:'the mansion’s 8 m display level',in:'model'},
 'hyrcania-waterworks/bridge':{line:'Drawn 6 m high throughout; its preserved height varies.',evidence:'6 m high along its whole length; its preserved height varies',in:'feature'},
 'jericho-early/complex':{line:'Pool depths are published; other heights are illustrative.',evidence:'other heights are illustrative',in:'plan'},
 'jericho-late/complex':{line:'Pool depths are published; other heights are illustrative.',evidence:'other heights are illustrative',in:'plan'},
 'bethesda-pools/north-pool':{line:'Its 10 m depth in the model is inferred, not recorded.',evidence:'that volume divided by its area, an inference',in:'feature'},
 'bethesda-pools/south-pool':{line:'Steps in the model are illustrative.',evidence:'Step count, width and landings are illustrative',in:'feature'},
 'bethesda-pools/settling-basin':{line:'Size and place in the model are illustrative.',evidence:'the 5 × 5 m box in the corner is illustrative',in:'feature'},
 'bethesda-pools/threshold':{line:'Size and orientation in the model are illustrative.',evidence:'size and orientation are illustrative',in:'feature'},
 'bethesda-pools/grotto-6':{line:'Size and depth in the model are illustrative.',evidence:'the size and depth are illustrative',in:'feature'},
 'bethesda-pools/first-installation':{line:'Most sizes in the model are illustrative.',evidence:'are illustrative; positions follow Pl. II',in:'feature'},
 'east-gate-warren/gatehouse':{line:'Height and roof in the model are illustrative.',evidence:'not drawn from a published source and are illustrative',in:'feature'},
 'east-gate-warren/east-wall':{line:'Thickness and height in the model are illustrative.',evidence:'Thickness and height above the Haram surface are illustrative',in:'feature'},
 'east-gate-warren/cistern-xv':{line:'The shaft opening’s size in the model is illustrative.',evidence:'size and position over the chamber are illustrative',in:'feature'},
 'east-gate-warren/gallery':{line:'Section and shaft shape in the model are illustrative.',evidence:'section, steps and the shaft',in:'feature'},
 'east-gate-warren/column':{line:'Length in the model is illustrative.',evidence:'its length is illustrative',in:'feature'},
 'east-gate-warren/massive-wall':{line:'Base and thickness in the model are illustrative.',evidence:'Its base and thickness are unknown',in:'feature'},
 'kidron-bene-hezir/zechariah':{line:'Height in the model is illustrative.',evidence:'heights are illustrative',in:'feature'},
 'kidron-bene-hezir/absalom':{line:'Footprint, drum and cone in the model are illustrative.',evidence:'the footprint, drum and cone in the model are illustrative',in:'feature'},
 'kidron-bene-hezir/chambers':{line:'Wall thickness and floor levels in the model are illustrative.',evidence:'gives no wall thicknesses or floor levels',in:'feature'},
 'temple-great-sea/piers':{line:'Place and size in the model are illustrative.',evidence:'places and size in the model are illustrative',in:'feature'},
 'temple-great-sea/stair':{line:'Line and width in the model are illustrative.',evidence:'line, width and top opening in the model are illustrative',in:'feature'},
};
// Statements by a whole model (its assumptions) that all of its heights are illustrative.
export const MODEL_WIDE:{evidence:string;line:string}[]=[
 {evidence:'Wall heights, pool depths, terrain/platform relief and conduit cross-sections are illustrative',line:'Heights in the model are illustrative.'},
 {evidence:'tunnel cross-section and elevations are illustrative',line:'Heights in the model are illustrative.'},
 {evidence:'Cistern diameters/depths, channel cross-section, defensive wall heights and ridge relief are illustrative',line:'Sizes and heights in the model are illustrative.'},
];
export function drawingNote(plan:SitePlan,feature:SiteFeature,assumptions:string[]):string|null{
 const own=MODEL_DRAWING[`${plan.id}/${feature.id}`];
 if(own&&(own.in==='feature'?feature.limit:own.in==='plan'?plan.limit:assumptions.join('\n')).includes(own.evidence))return own.line;
 const all=assumptions.join('\n');return MODEL_WIDE.find(w=>all.includes(w.evidence))?.line??null;
}

export type WalkSign={id:string;name:string;source:string|null;status:string|null;statusKey:string|null;drawing:string|null;at:T.Vector3};
export function walkSignItems(plan:SitePlan,markers:Map<string,T.Vector3>,assumptions:string[]):WalkSign[]{
 return plan.features.flatMap(f=>{const at=markers.get(f.id);if(!at)return [];const status=STATUS[f.kind];
  return [{id:f.id,name:f.label,source:f.sources[0]??null,status:status?.[0]??null,statusKey:status?.[1]??null,drawing:drawingNote(plan,f,assumptions),at:at.clone()}];});
}
// Fully opaque within SIGN_FULL metres, fading to nothing at SIGN_RANGE.
export const signOpacity=(distance:number)=>distance>=SIGN_RANGE?0:distance<=SIGN_FULL?1:1-(distance-SIGN_FULL)/(SIGN_RANGE-SIGN_FULL);

export type WalkSigns={update:(projection:T.Matrix4|null,eye?:T.Vector3)=>void;setEnabled:(on:boolean)=>void;dispose:()=>void};
export function createWalkSigns(container:HTMLElement,signs:WalkSign[]):WalkSigns{
 const root=document.createElement('div');root.className='walk-signs';root.setAttribute('role','group');root.setAttribute('aria-label','Feature signs');root.hidden=true;root.dataset.shown='';
 const items=signs.map(sign=>{
  const el=document.createElement('div'),card=document.createElement('div');el.className='walk-sign';el.dataset.feature=sign.id;if(sign.statusKey)el.dataset.status=sign.statusKey;el.hidden=true;card.className='walk-sign-card';
  const add=(tag:string,cls:string,text:string|null)=>{if(!text)return;const node=document.createElement(tag);if(cls)node.className=cls;node.textContent=text;card.appendChild(node);};
  add('strong','',sign.name);add('span','walk-sign-source',sign.source);add('span','walk-sign-tag',sign.status);add('span','walk-sign-note',sign.drawing);
  el.appendChild(card);root.appendChild(el);return {sign,el,card,size:null as [number,number]|null};
 });
 container.appendChild(root);
 // The overlay's size, kept by an observer so that drawing a frame never forces a layout.
 let enabled=true,width=container.clientWidth,height=container.clientHeight;const v=new T.Vector4();
 const resize=typeof ResizeObserver==='undefined'?null:new ResizeObserver(([entry])=>{width=entry.contentRect.width;height=entry.contentRect.height;});resize?.observe(container);
 return {
  update(projection,eye){
   if(!projection||!eye||!enabled){if(!root.hidden){root.hidden=true;root.dataset.shown='';}return;}
   root.hidden=false;
   const placed:[number,number,number,number][]=[],shown:string[]=[];
   const visible=items.map(item=>({item,distance:item.sign.at.distanceTo(eye)})).filter(c=>c.distance<SIGN_RANGE).sort((a,b)=>a.distance-b.distance);
   const showing=new Set<typeof items[number]>();
   for(const {item,distance} of visible){
    const p=item.sign.at;v.set(p.x,p.y,p.z,1).applyMatrix4(projection);
    if(v.w<.1)continue;
    const x=(v.x/v.w+1)/2*width,y=(1-v.y/v.w)/2*height;
    if(x<-120||x>width+120||y<-10||y>height+260)continue;
    if(item.el.hidden)item.el.hidden=false;
    item.size??=[item.card.offsetWidth,item.card.offsetHeight];
    const scale=T.MathUtils.clamp(1.05-distance/100,.72,1),w=item.size[0]*scale,h=(item.size[1]+9)*scale,box:[number,number,number,number]=[x-w/2,y-h,x+w/2,y];
    // A farther card that would overlap a nearer one waits until the walker moves or turns.
    const crowded=placed.some(b=>Math.min(b[2],box[2])-Math.max(b[0],box[0])>4&&Math.min(b[3],box[3])-Math.max(b[1],box[1])>4);
    if(crowded)continue;
    placed.push(box);showing.add(item);shown.push(item.sign.id);
    item.el.style.transform=`translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0) scale(${scale.toFixed(3)})`;
    item.el.style.opacity=signOpacity(distance).toFixed(3);item.el.style.zIndex=String(1000-Math.round(distance*10));
   }
   for(const item of items)if(!showing.has(item)&&!item.el.hidden)item.el.hidden=true;
   const list=shown.join(',');if(root.dataset.shown!==list)root.dataset.shown=list;
  },
  setEnabled(on){enabled=on;if(!on){root.hidden=true;root.dataset.shown='';}},
  dispose(){resize?.disconnect();root.remove();},
 };
}
