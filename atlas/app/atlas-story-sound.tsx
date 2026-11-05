"use client";
import {createContext,useCallback,useContext,useEffect,useRef,useState,type ReactNode} from 'react';
import {Volume2,VolumeX} from 'lucide-react';
import {createFoleyVoice,type MaterialSound} from './atlas-story-foley';
export type {MaterialSound} from './atlas-story-foley';
const FoleyContext=createContext<(cue:string,kind:MaterialSound)=>void>(()=>{});
export function useStoryFoley(cue:string,kind:MaterialSound,active:boolean){
 const request=useContext(FoleyContext),previous=useRef('');
 useEffect(()=>{if(active&&previous.current!==cue){previous.current=cue;request(cue,kind);}},[cue,kind,active,request]);
}
export function StorySound({children}:{children:ReactNode}){
 const [enabled,setEnabled]=useState(false),[unavailable,setUnavailable]=useState(false),[lastSound,setLastSound]=useState('');
 const engine=useRef<AudioContext|null>(null),on=useRef(false),voice=useRef<ReturnType<typeof createFoleyVoice>|null>(null),timer=useRef(0),fading=useRef(new Set<number>()),lastAt=useRef(-Infinity);
 const stop=useCallback(()=>{clearTimeout(timer.current);const cleanup=voice.current?.cancel();voice.current=null;if(cleanup){const id=window.setTimeout(()=>{cleanup();fading.current.delete(id);},40);fading.current.add(id);}},[]);
 const request=useCallback((cue:string,kind:MaterialSound)=>{
  const ctx=engine.current;if(!on.current||!ctx||ctx.state!=='running'||document.hidden)return;
  stop();if(performance.now()-lastAt.current<100)return;lastAt.current=performance.now();
  voice.current=createFoleyVoice(ctx,ctx.destination,kind);setLastSound(cue);
  timer.current=window.setTimeout(()=>{voice.current?.cleanup();voice.current=null;},1250);
 },[stop]);
 async function toggle(){
  if(on.current){on.current=false;setEnabled(false);stop();return;}
  try{
   const ctx=engine.current??new AudioContext();engine.current=ctx;await ctx.resume();
   if(ctx.state!=='running')throw Error('Audio unavailable');
   on.current=true;setEnabled(true);setUnavailable(false);request('sound-enabled','pin');
  }catch{on.current=false;setEnabled(false);setUnavailable(true);}
 }
 useEffect(()=>{
  const visibility=()=>{stop();const ctx=engine.current;if(ctx){if(document.hidden)void ctx.suspend().catch(()=>{});else if(on.current)void ctx.resume().catch(()=>{});}};
  document.addEventListener('visibilitychange',visibility);
  return()=>{document.removeEventListener('visibilitychange',visibility);stop();for(const id of fading.current)clearTimeout(id);fading.current.clear();void engine.current?.close().catch(()=>{});engine.current=null;on.current=false;};
 },[stop]);
 return <FoleyContext.Provider value={request}>{children}<button className="story-sound-toggle" type="button" aria-pressed={enabled} aria-label={enabled?'Mute sound effects':'Enable sound effects'} onClick={()=>void toggle()} data-sound-enabled={enabled} data-last-sound={lastSound} title={unavailable?'Sound is unavailable in this browser':undefined}>{enabled?<Volume2 size={17}/>:<VolumeX size={17}/>}<span>{unavailable?'Sound unavailable':enabled?'Sound on':'Sound off'}</span></button></FoleyContext.Provider>;
}
