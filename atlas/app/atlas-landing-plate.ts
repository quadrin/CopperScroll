/** Adapted from the animated copper plate supplied in Copper Scroll Experimental
 * Approaches (2).zip. Procedural illustration, not a manuscript photograph or
 * measured surface. Text: M. G. Abegg Jr., ETCBC, CC BY-NC 4.0 (credit in page).
 * No source-document scripts, remote fonts, images or event handlers are loaded.
 */
export function mountCopperPlate(canvas: HTMLCanvasElement) {
 const context=canvas.getContext('2d');
 if(!context)return ()=>{};
 const W=900,H=408,N=W*H;canvas.width=W;canvas.height=H;
 const mask=document.createElement('canvas');mask.width=W;mask.height=H;
 const pen=mask.getContext('2d');if(!pen)return ()=>{};
 pen.fillStyle='#000';pen.fillRect(0,0,W,H);pen.fillStyle='#fff';pen.direction='rtl';pen.textAlign='right';pen.textBaseline='middle';
 pen.font='600 52px "Times New Roman", serif';
 ['בחרובא שבעמק עכור תחת','המעלות הביאה למזרח אמות','ארבעין שדת כסף וכליה','משקל ככרין שבעשרה ΚΕΝ'].forEach((line,i)=>pen.fillText(line,W-45,72+i*88));
 const letters=pen.getImageData(0,0,W,H).data;
 let seed=19;const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
 function blur(source:Float32Array,radius:number){
  const mid=new Float32Array(N),out=new Float32Array(N),d=radius*2+1;
  for(let y=0;y<H;y++){
   let sum=0;for(let x=-radius;x<=radius;x++)sum+=source[y*W+Math.max(0,Math.min(W-1,x))];
   for(let x=0;x<W;x++){mid[y*W+x]=sum/d;sum+=source[y*W+Math.min(W-1,x+radius+1)]-source[y*W+Math.max(0,x-radius)];}
  }
  for(let x=0;x<W;x++){
   let sum=0;for(let y=-radius;y<=radius;y++)sum+=mid[Math.max(0,Math.min(H-1,y))*W+x];
   for(let y=0;y<H;y++){out[y*W+x]=sum/d;sum+=mid[Math.min(H-1,y+radius+1)*W+x]-mid[Math.max(0,y-radius)*W+x];}
  }
  return out;
 }
 const noise=new Float32Array(N),text=new Float32Array(N);
 for(let i=0;i<N;i++){noise[i]=random();text[i]=letters[i*4]/255;}
 const broad=blur(blur(noise,22),22),fine=blur(noise,1),mid=blur(noise,4),engraving=blur(text,1);
 let low=Infinity,high=-Infinity;for(const v of broad){low=Math.min(low,v);high=Math.max(high,v);}
 const heights=new Float32Array(N),patina=new Float32Array(N),seam=Math.round(W*.69);
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){
  const i=y*W+x,b=(broad[i]-low)/(high-low),s=Math.abs(x-seam);
  heights[i]=-Math.pow(y/H-.5,2)*60+b*14+(mid[i]-.5)*5+(fine[i]-.5)*1.2-Math.pow(engraving[i],1.3)*7-(s<3?9*(1-s/3):0);
  patina[i]=Math.max(0,Math.min(1,(b-.42)*2.4+(mid[i]-.5)*1.6+engraving[i]*.55+(s<8?.4:0)));
 }
 for(let k=0;k<700;k++){
  const px=Math.floor(random()*W),py=Math.floor(random()*H),r=1+random()*2.5;
  for(let y=-3;y<=3;y++)for(let x=-3;x<=3;x++){
   const X=px+x,Y=py+y,d=x*x+y*y;if(X<0||X>=W||Y<0||Y>=H||d>=r*r)continue;
   heights[Y*W+X]-=1.6*(1-d/(r*r));patina[Y*W+X]=Math.min(1,patina[Y*W+X]+.25);
  }
 }
 const nx=new Float32Array(N),ny=new Float32Array(N),nz=new Float32Array(N),base=new Float32Array(N*3);
 const copper=[196,118,70],dark=[112,58,30],green=[78,140,118];
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){
  const i=y*W+x,gx=(heights[y*W+Math.min(W-1,x+1)]-heights[y*W+Math.max(0,x-1)])*.5,gy=(heights[Math.min(H-1,y+1)*W+x]-heights[Math.max(0,y-1)*W+x])*.5,l=1/Math.hypot(gx,gy,1);
  nx[i]=-gx*l;ny[i]=-gy*l;nz[i]=l;
  const p=patina[i],g=Math.min(.85,Math.max(0,p-.45)*1.6);
  for(let c=0;c<3;c++)base[i*3+c]=((copper[c]+(fine[i]-.5)*(40-c*10))*(1-.35*p)+dark[c]*.35*p)*(1-g)+green[c]*g;
 }
 const image=context.createImageData(W,H);let lx=W*.7,ly=H*.15,frame=0,disposed=false,visible=true,last=0,elapsed=0,previous=0,interactive=false;
 const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
 function draw(){
  const pixels=image.data;
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){
   const i=y*W+x,dx=lx-x,dy=ly-y,il=1/Math.hypot(dx,dy,150),Lx=dx*il,Ly=dy*il,Lz=150*il;
   const diffuse=Math.max(0,nx[i]*Lx+ny[i]*Ly+nz[i]*Lz),h=1/Math.hypot(Lx,Ly,Lz+1);
   let spec=Math.max(0,(nx[i]*Lx+ny[i]*Ly+nz[i]*(Lz+1))*h);for(let n=0;n<5;n++)spec*=spec;
   const fall=1/(1+(dx*dx+dy*dy)/420000),light=.2+1.05*diffuse*fall;
   for(let c=0;c<3;c++)pixels[i*4+c]=Math.min(255,base[i*3+c]*light+spec*(255-c*52)*fall*.95);
   pixels[i*4+3]=255;
  }
  context!.putImageData(image,0,0);
 }
 function tick(time:number){
  frame=0;if(disposed||!visible||document.hidden||motion.matches)return;
  if(previous)elapsed+=Math.min(100,time-previous);previous=time;
  if(time-last>65){
   if(!interactive){lx=W*(.56+.22*Math.sin(elapsed/7500));ly=H*(.16+.12*Math.sin(elapsed/11000));}
   draw();last=time;
  }
  frame=requestAnimationFrame(tick);
 }
 function resume(){previous=0;if(frame)cancelAnimationFrame(frame);frame=0;if(!disposed&&visible&&!document.hidden&&!motion.matches)frame=requestAnimationFrame(tick);}
 function point(event:PointerEvent){
  // Touch scrolling remains native. Reduced-motion readers keep a static plate.
  if(motion.matches||event.pointerType==='touch')return;
  const r=canvas.getBoundingClientRect(),scale=Math.max(r.width/W,r.height/H),offsetX=(r.width-W*scale)*.5,offsetY=(r.height-H*scale)*.5;
  lx=(event.clientX-r.left-offsetX)/scale;ly=(event.clientY-r.top-offsetY)/scale;interactive=true;
 }
 function leave(){interactive=false;}
 const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;resume();},{threshold:0});observer.observe(canvas);
 canvas.addEventListener('pointermove',point);canvas.addEventListener('pointerleave',leave);
 document.addEventListener('visibilitychange',resume);motion.addEventListener('change',resume);
 draw();resume();
 return ()=>{disposed=true;cancelAnimationFrame(frame);observer.disconnect();canvas.removeEventListener('pointermove',point);canvas.removeEventListener('pointerleave',leave);document.removeEventListener('visibilitychange',resume);motion.removeEventListener('change',resume);};
}
