/* <before-after before="a.png" after="b.png" before-label="v0" after-label="v1" position="50">

   A wipe between two images: the after image shows left of the handle, the before image right.
   An ARIA slider. Keys: Left/Right (Shift for steps of 10), Home, End. Pointer drag. Fires
   `input` with detail.position (0-100) when the user moves it. Labels sit in the bottom corners
   and fade out when their side is narrower than 240 px. The knob and labels stay in view while a
   tall pair scrolls.

   The host clips with overflow:clip, not hidden, so the sticky knob and labels follow the page's
   scroller rather than the host.

   Shadow DOM: img#b (before), img#a (after, clipped by --p), two halves .h each holding a label
   (#la left, #lb right); the right half's left border is the handle line and holds the knob .k.

   Kept under 2 KB with whitespace collapsed, so it is written tersely on purpose. */
customElements.define('before-after',class extends HTMLElement{
static observedAttributes='before after before-label after-label position'.split(' ');
constructor(){
super();
this.attachShadow({mode:'open'}).innerHTML=`<style>:host{display:grid;position:relative;overflow:clip;touch-action:pan-y;user-select:none;cursor:ew-resize;outline:0}*{pointer-events:none}img{grid-area:1/1;width:100%}#a{clip-path:inset(0 calc(100% - var(--p)) 0 0)}.h{position:absolute;inset:0 calc(100% - var(--p)) 0 0;display:flex;align-items:end;container-type:inline-size}.h+.h{inset:0 0 0 var(--p);border-left:2px solid #fff;box-shadow:0 0 6px #0006;justify-content:space-between}span{position:sticky;bottom:16px;margin:16px;padding:8px 14px;border-radius:99px;background:#111d;color:#fff;font:600 13px/1 system-ui;white-space:nowrap}@container (width<240px){span{opacity:0}}.k{position:sticky;inset:calc(50% - 20px) 0;align-self:center;flex:none;width:40px;margin-left:-21px;border-radius:50%;background:#fff;color:#222;font:700 20px/40px system-ui;text-align:center;box-shadow:0 2px 6px #0006}:host(:focus-visible) .k{outline:2px solid #fff;outline-offset:3px}</style><img id=b><img id=a><div class=h><span id=la></span></div><div class=h><b class=k>‹ ›</b><span id=lb></span></div>`;
let g=e=>this.move(e.offsetX/this.offsetWidth*100);
this.onpointerdown=e=>(this.setPointerCapture(e.pointerId),g(e));
this.onpointermove=e=>e.buttons&&g(e);
this.onkeydown=e=>{
let s=e.shiftKey?10:2,d={ArrowLeft:-s,ArrowRight:s,Home:-1e3,End:1e3}[e.key];
d&&(e.preventDefault(),this.move(this.p+d))}}
// before/after set img#b/#a, the labels set span#lb/#la, and position (kept in this.p) redraws.
attributeChangedCallback(n,o,v){
let e=this.shadowRoot.getElementById((n.endsWith('l')?'l':'')+n[0]),p=this.p=+(this.getAttribute('position')??50);
e&&(e['src'in e?'src':'textContent']=v);
Object.assign(this,{role:'slider',tabIndex:0,ariaValueMin:0,ariaValueMax:100,ariaValueNow:p.toFixed()});
this.style.setProperty('--p',p+'%')}
move(v){
this.setAttribute('position',v=v<0?0:v>100?100:v);
this.dispatchEvent(new CustomEvent('input',{bubbles:1,detail:{position:v}}))}});
