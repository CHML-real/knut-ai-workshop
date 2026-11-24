// Two families of filaments turn a flat grid into a folded ribbon.
(() => {
  const panel=document.querySelector('.weave'), canvas=panel.querySelector('canvas');
  const ctx=canvas.getContext('2d');
  if(!ctx) return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  let w,h,frame=0,x=.48,y=.48,tx=x,ty=y;
  function point(t,u) {
    const a=t*6.7-1.1+x*1.4;
    const twist=a+u*.58;
    return [
      w*(.04+t*.92 + u*.035*Math.sin(a)),
      h*(.55-.20*Math.sin(a)+u*(.05+.20*Math.cos(twist))+.065*Math.sin(t*12+y*4))
    ];
  }
  function draw(){
    frame=0;
    x+=(tx-x)*(reduce.matches?1:.18);y+=(ty-y)*(reduce.matches?1:.18);
    ctx.setTransform(canvas.width/w,0,0,canvas.height/h,0,0);
    ctx.clearRect(0,0,w,h);
    const gradient=ctx.createLinearGradient(w*.03,0,w*.97,h*.55);
    gradient.addColorStop(0,'#41d9d0');gradient.addColorStop(.32,'#a4f9e6');
    gradient.addColorStop(.53,'#d6c6ff');gradient.addColorStop(.77,'#9265ff');gradient.addColorStop(1,'#ecaff4');
    ctx.strokeStyle=gradient;
    for(let i=0;i<102;i++){
      const u=i/101*2-1;
      ctx.beginPath();ctx.lineWidth=i%10===0?1.15:.72;ctx.globalAlpha=.48+.40*Math.pow(Math.cos(u*2),2);
      for(let j=0;j<=154;j++){
        const [px,py]=point(j/154,u);
        if(j===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);
      }
      ctx.stroke();
    }
    ctx.globalAlpha=.13;ctx.lineWidth=.7;
    for(let j=0;j<=64;j++){
      ctx.beginPath();
      for(let i=0;i<=20;i++){const p=point(j/64,i/10-1);if(i===0)ctx.moveTo(...p);else ctx.lineTo(...p);}
      ctx.stroke();
    }
    ctx.globalAlpha=1;
    if(Math.abs(tx-x)+Math.abs(ty-y)>.001) schedule();
  }
  function schedule(){if(!frame)frame=requestAnimationFrame(draw);}
  function resize(){
    w=panel.clientWidth;h=panel.clientHeight;
    if(!w||!h)return;
    const scale=Math.min(2,devicePixelRatio||1);canvas.width=Math.round(w*scale);canvas.height=Math.round(h*scale);schedule();
  }
  function move(e){const box=panel.getBoundingClientRect();tx=Math.max(0,Math.min(1,(e.clientX-box.left)/w));ty=Math.max(0,Math.min(1,(e.clientY-box.top)/h));schedule();}
  panel.addEventListener('pointerdown',move);panel.addEventListener('pointermove',move);
  new ResizeObserver(resize).observe(panel);resize();
})();
