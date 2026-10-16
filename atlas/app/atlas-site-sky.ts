import * as T from 'three';

// Only used at eye level. The map retains its geographic background in orbit.
export function createSiteSky(){
 const material=new T.ShaderMaterial({depthTest:false,depthWrite:false,uniforms:{inverseProjection:{value:new T.Matrix4()},eye:{value:new T.Vector3()}},vertexShader:`
  varying vec2 vClip; void main(){vClip=position.xy;gl_Position=vec4(position.xy,1.0,1.0);}
 `,fragmentShader:`
  uniform mat4 inverseProjection; uniform vec3 eye; varying vec2 vClip;
  void main(){
   vec4 p=inverseProjection*vec4(vClip,0.999,1.0); vec3 ray=normalize(p.xyz/p.w-eye);
   vec3 horizon=vec3(0.66,0.74,0.77),zenith=vec3(0.09,0.28,0.49),earth=vec3(0.32,0.27,0.19);
   vec3 colour=mix(horizon,zenith,pow(max(ray.y,0.0),0.45));
   colour=mix(colour,earth,1.0-smoothstep(-0.12,0.01,ray.y));
   float sun=max(dot(ray,normalize(vec3(-0.8,1.3,0.65))),0.0);
   colour+=vec3(0.25,0.18,0.08)*pow(sun,32.0);
   gl_FragColor=vec4(colour,1.0);
   #include <colorspace_fragment>
  }
 `});
 const mesh=new T.Mesh(new T.PlaneGeometry(2,2),material);mesh.frustumCulled=false;mesh.renderOrder=-10000;mesh.visible=false;
 return {mesh,update(projection:T.Matrix4,eye:T.Vector3,walking:boolean){mesh.visible=walking;material.uniforms.inverseProjection.value.copy(projection).invert();material.uniforms.eye.value.copy(eye);}};
}
