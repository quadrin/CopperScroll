import * as T from 'three';
import type {MeasurePoint} from './atlas-walk-measure';

// The three.js side of the measuring tool (atlas-walk-measure.ts): picking a point on what is drawn and the
// measurement drawn over the canvas.
// The nearest drawn mesh surface under a canvas point. `projection` is the matrix that drew the last frame
// (site frame to clip space); ndc are the point's normalized device coordinates. Hidden objects are skipped,
// so in Blocks the ray meets the block meshes and the smooth terrain outside them, as drawn.
export function pickSurface(root:T.Object3D,projection:T.Matrix4,ndcX:number,ndcY:number):T.Vector3|null{
 const inverse=projection.clone().invert(),near=new T.Vector3(ndcX,ndcY,-1).applyMatrix4(inverse),far=new T.Vector3(ndcX,ndcY,1).applyMatrix4(inverse);
 if(![near.x,near.y,near.z,far.x,far.y,far.z].every(Number.isFinite))return null;
 const meshes:T.Mesh[]=[];root.traverseVisible(o=>{if(o instanceof T.Mesh&&!o.userData.measureIgnore)meshes.push(o);});
 const raycaster=new T.Raycaster(near,far.clone().sub(near).normalize(),0,near.distanceTo(far));
 return raycaster.intersectObjects(meshes,false)[0]?.point??null;
}

// The measurement drawn over the canvas: the slope line from A to B, and dashed horizontal and vertical
// legs. Placed every frame from the matrix that draws the site (as the walk signs are), so it stays on
// the picked points and shows through walls. It takes no pointer events.
const SVG='http://www.w3.org/2000/svg';
export type WalkMeasure={set:(points:MeasurePoint[])=>void;update:(projection:T.Matrix4|null)=>void;dispose:()=>void};
export function createWalkMeasure(container:HTMLElement):WalkMeasure{
 const svg=document.createElementNS(SVG,'svg');svg.classList.add('walk-measure');svg.setAttribute('aria-hidden','true');svg.style.display='none';
 const make=(tag:string,cls:string)=>{const e=document.createElementNS(SVG,tag);e.setAttribute('class',cls);svg.appendChild(e);return e;};
 const legs=[make('line','walk-measure-leg'),make('line','walk-measure-leg')],halo=make('line','walk-measure-halo'),line=make('line','walk-measure-line');
 const dots=[make('circle','walk-measure-dot'),make('circle','walk-measure-dot')],labels=[make('text','walk-measure-label'),make('text','walk-measure-label')];
 labels[0].textContent='A';labels[1].textContent='B';dots.forEach(d=>d.setAttribute('r','5'));
 container.appendChild(svg);
 let points:MeasurePoint[]=[],width=container.clientWidth,height=container.clientHeight;
 const resize=typeof ResizeObserver==='undefined'?null:new ResizeObserver(([entry])=>{width=entry.contentRect.width;height=entry.contentRect.height;});resize?.observe(container);
 const clip=(p:MeasurePoint,m:T.Matrix4)=>new T.Vector4(p[0],p[1],p[2],1).applyMatrix4(m);
 const screen=(v:T.Vector4):[number,number]=>[(v.x/v.w+1)/2*width,(1-v.y/v.w)/2*height];
 // A segment cut where it passes behind the camera (w below a small positive value).
 function segment(el:Element,a:MeasurePoint,b:MeasurePoint,m:T.Matrix4){
  let p=clip(a,m),q=clip(b,m);const eps=1e-3;
  if(p.w<eps&&q.w<eps){el.setAttribute('visibility','hidden');return;}
  if(p.w<eps)p=p.clone().lerp(q,(eps-p.w)/(q.w-p.w));else if(q.w<eps)q=q.clone().lerp(p,(eps-q.w)/(p.w-q.w));
  const [x1,y1]=screen(p),[x2,y2]=screen(q);
  el.setAttribute('x1',x1.toFixed(1));el.setAttribute('y1',y1.toFixed(1));el.setAttribute('x2',x2.toFixed(1));el.setAttribute('y2',y2.toFixed(1));el.setAttribute('visibility','visible');
 }
 return {
  set(next){points=next.slice(0,2);if(!points.length)svg.style.display='none';},
  update(projection){
   if(!projection||!points.length){svg.style.display='none';delete svg.dataset.points;return;}
   svg.style.display='';svg.setAttribute('width',String(width));svg.setAttribute('height',String(height));
   const shown:string[]=[];
   points.forEach((p,i)=>{const v=clip(p,projection),visible=v.w>1e-3;dots[i].setAttribute('visibility',visible?'visible':'hidden');labels[i].setAttribute('visibility',visible?'visible':'hidden');
    if(visible){const [x,y]=screen(v);dots[i].setAttribute('cx',x.toFixed(1));dots[i].setAttribute('cy',y.toFixed(1));labels[i].setAttribute('x',(x+8).toFixed(1));labels[i].setAttribute('y',(y-8).toFixed(1));shown.push(`${x.toFixed(1)},${y.toFixed(1)}`);}else shown.push('behind');});
   for(let i=points.length;i<2;i++){dots[i].setAttribute('visibility','hidden');labels[i].setAttribute('visibility','hidden');}
   if(points.length===2){
    const [a,b]=points,corner:MeasurePoint=[b[0],a[1],b[2]];
    segment(line,a,b,projection);segment(halo,a,b,projection);segment(legs[0],a,corner,projection);segment(legs[1],corner,b,projection);
   }else for(const el of [line,halo,...legs])el.setAttribute('visibility','hidden');
   svg.dataset.points=shown.join(' ');
  },
  dispose(){resize?.disconnect();svg.remove();},
 };
}
