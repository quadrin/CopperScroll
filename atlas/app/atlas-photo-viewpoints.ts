import data from './atlas-photo-viewpoints.json';

// Where a reference photograph was taken, in a site model's frame, so that the eye-level view can show
// the photo from its own standpoint (atlas-photo-view.tsx). Viewpoints live in atlas-photo-viewpoints.json,
// keyed by gallery photo id (or a scene's src), so the gallery files stay untouched.
//
// A viewpoint "aligned by eye" is an INFERENCE: someone moved the camera until the model's outlines sat on
// the photograph's. It is not a measured camera position, and it inherits every error of the model.
export type ViewpointStatus='aligned by eye'|'from EXIF/GPS';
export type PhotoViewpoint={
 plan:string;                 // the site plan whose model frame the position is in
 position:[number,number];    // metres from the place anchor: x east, z south (as model.markers)
 eyeHeight?:number;           // metres above the ground under the position (default 1.6)
 y?:number;                   // or an absolute height in the model frame, instead of eyeHeight
 bearing:number;              // degrees clockwise from north
 pitch:number;                // degrees above the horizon (negative looks down)
 roll?:number;                // degrees the photo is turned (clockwise) to level it with the model
 hfov:number;                 // horizontal field of view of the photograph, degrees
 status:ViewpointStatus;
 uncertainty?:{position?:number;bearing?:number;height?:number}; // estimated ± metres, degrees, metres
 note:string;
 alignedBy:string;
 date:string;
 alignedIn?:'smooth'|'minecraft';  // the model style used while aligning
};
export const DEFAULT_EYE_HEIGHT=1.6;

const viewpoints=(data as {viewpoints:Record<string,PhotoViewpoint>}).viewpoints;
export const viewpointFor=(photoId:string,planId?:string|null)=>{const v=viewpoints[photoId];return v&&(!planId||v.plan===planId)?v:null;};
export const allViewpoints=()=>viewpoints;

// One plain sentence on how far to trust the viewpoint.
export function viewpointStatus(v:PhotoViewpoint):string{
 const u=v.uncertainty??{},parts=[u.position!=null&&`position about ±${u.position} m`,u.height!=null&&`height about ±${u.height} m`,u.bearing!=null&&`bearing about ±${u.bearing}°`].filter(Boolean);
 const head=v.status==='aligned by eye'?'Viewpoint aligned by eye':'Viewpoint from the photo’s EXIF/GPS record';
 return `${head}${parts.length?`; ${parts.join(', ')}`:'; uncertainty not stated'}.`;
}

// The camera for a photo of horizontal field of view `hfov` and aspect `aspect` (width / height), on a canvas
// of `width` × `height` CSS pixels: the vertical field of view that keeps the whole photo on the canvas, and
// the photo's rectangle on the canvas, so that the photo's field of view matches the camera's. It assumes a
// distortion-free photo with its principal point at the centre.
export function photoFrame(hfov:number,aspect:number,width:number,height:number){
 const half=Math.tan(hfov*Math.PI/360),canvas=width/Math.max(height,1);
 const vertical=Math.max(half/aspect,half/canvas),drawn=width*half/(vertical*canvas);
 return {vfov:2*Math.atan(vertical)*180/Math.PI,width:drawn,height:drawn/aspect,left:(width-drawn)/2,top:(height-drawn/aspect)/2};
}

// The eye for a viewpoint: an absolute y, or eyeHeight above the ground found under the position.
export function viewpointEye(v:PhotoViewpoint,groundAt:(x:number,z:number)=>number|null):[number,number,number]{
 const [x,z]=v.position;
 return [x,v.y??(groundAt(x,z)??0)+(v.eyeHeight??DEFAULT_EYE_HEIGHT),z];
}

const round=(n:number,d:number)=>Math.round(n*10**d)/10**d;
// The JSON an editor pastes into atlas-photo-viewpoints.json, keyed by the photo id.
export function viewpointJson(photoId:string,v:PhotoViewpoint):string{
 const clean:PhotoViewpoint={...v,position:[round(v.position[0],2),round(v.position[1],2)],bearing:round(((v.bearing%360)+360)%360,2),pitch:round(v.pitch,2),hfov:round(v.hfov,2)};
 if(clean.eyeHeight!=null)clean.eyeHeight=round(clean.eyeHeight,2);if(clean.y!=null)clean.y=round(clean.y,2);if(clean.roll!=null)clean.roll=round(clean.roll,2);
 return JSON.stringify({[photoId]:clean},null,1);
}
