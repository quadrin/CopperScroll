// Short, original material studies. No recordings, downloads or music loop.
export type MaterialSound='sand'|'stone'|'metal'|'scratch'|'cut'|'paper'|'clay'|'silver'|'pin'|'measure';
export function createFoleyVoice(ctx:BaseAudioContext,output:AudioNode,kind:MaterialSound,at=ctx.currentTime){
 const bus=ctx.createGain();bus.connect(output);bus.gain.setValueAtTime(.65,at);
 const sources:AudioScheduledSourceNode[]=[],nodes:AudioNode[]=[bus];
 let seed=731;const random=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
 function noise(start:number,duration:number,frequency:number,level:number,filter:BiquadFilterType='bandpass'){
  const buffer=ctx.createBuffer(1,Math.ceil(ctx.sampleRate*duration),ctx.sampleRate),data=buffer.getChannelData(0);
  for(let i=0;i<data.length;i++)data[i]=random()*2-1;
  const source=ctx.createBufferSource(),tone=ctx.createBiquadFilter(),gain=ctx.createGain();source.buffer=buffer;
  tone.type=filter;tone.frequency.value=frequency;tone.Q.value=.65;
  gain.gain.setValueAtTime(0,at+start);gain.gain.linearRampToValueAtTime(level,at+start+Math.min(.018,duration*.15));gain.gain.exponentialRampToValueAtTime(.0001,at+start+duration);
  source.connect(tone).connect(gain).connect(bus);source.start(at+start);source.stop(at+start+duration);sources.push(source);nodes.push(tone,gain);
 }
 function resonance(start:number,frequency:number,duration:number,level:number){
  const source=ctx.createOscillator(),gain=ctx.createGain();source.type='sine';source.frequency.value=frequency;
  gain.gain.setValueAtTime(0,at+start);gain.gain.linearRampToValueAtTime(level,at+start+.003);gain.gain.exponentialRampToValueAtTime(.0001,at+start+duration);
  source.connect(gain).connect(bus);source.start(at+start);source.stop(at+start+duration);sources.push(source);nodes.push(gain);
 }
 const tap=(t:number)=>{noise(t,.035,1500,.24);resonance(t,190,.055,.07);};
 switch(kind){
  case 'sand':noise(0,.65,1150,.16,'lowpass');for(let i=0;i<7;i++)noise(.04+i*.065,.07,1800+random()*900,.045);break;
  case 'stone':noise(0,.38,620,.3,'lowpass');resonance(0,85,.12,.1);for(let i=0;i<4;i++)noise(.1+i*.065,.05,1000,.08);break;
  case 'metal':noise(0,.32,2100,.16);[710,1297,2089].forEach((f,i)=>resonance(.02,f,.35-i*.06,.026/(i+1)));break;
  case 'scratch':for(let i=0;i<5;i++)noise(i*.08,.055,2600,.14);break;
  case 'cut':for(let i=0;i<5;i++){noise(i*.17,.135,2400,.22);resonance(i*.17,1170,.09,.014);}break;
  case 'paper':noise(0,.22,2500,.18,'highpass');noise(.11,.27,1350,.13);break;
  case 'clay':noise(0,.045,650,.16);[430,763,1182].forEach((f,i)=>resonance(0,f,.14-i*.025,.055/(i+1)));break;
  case 'silver':[1810,2717,3913].forEach((f,i)=>resonance(i*.025,f,.21,.035/(i+1)));noise(0,.035,3400,.1);break;
  case 'pin':tap(0);break;
  case 'measure':[0,.14,.28].forEach(tap);break;
 }
 // One cleanup for natural completion, rapid cue changes and mute.
 const cleanup=()=>{for(const s of sources){try{s.stop();}catch{/* already ended */}s.disconnect();}for(const n of nodes)n.disconnect();};
 return {cancel(){bus.gain.cancelScheduledValues(ctx.currentTime);bus.gain.setTargetAtTime(0,ctx.currentTime,.008);return cleanup;},cleanup};
}
