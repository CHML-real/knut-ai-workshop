(() => {
  const money = n => n.toLocaleString('ko-KR') + '원';
  const daysBetween = (a,b) => (Date.parse(a)-Date.parse(b))/86400000;
  function inquiries(panel) {
    const date = panel.querySelector('#asof').value;
    const days = Number(panel.querySelector('#days').value);
    const waiting = [];
    for (const [id, received, history] of workshopData.inquiries) {
      if (received > date) continue;
      const age = daysBetween(date,received);
      const state = history.filter(([when]) => when <= date).at(-1)?.[2] || '접수';
      if (age >= days && state !== '회신 완료') waiting.push({id,age,state});
    }
    waiting.sort((a,b) => b.age-a.age || a.id.localeCompare(b.id));
    return [waiting.length+'건', '기준일 당시 장기 미회신 · 오래된 순 최대 3건',
      waiting.slice(0,3).map(v => [v.id+' · '+v.state,v.age+'일'])];
  }
  function budget(panel) {
    const q = Number(panel.querySelector('#quarter').value);
    const departments = new Map();
    for (const [code,[department,name,...amounts]] of Object.entries(workshopData.projects)) {
      const group = departments.get(department) || {department,delta:0,projects:[]};
      const delta = amounts[q-1]-amounts[q-2];
      group.delta += delta;
      if (delta>0) group.projects.push({code,name,delta});
      departments.set(department,group);
    }
    const winner = [...departments.values()].filter(g => g.delta>0).sort((a,b) => b.delta-a.delta || a.department.localeCompare(b.department,'ko'))[0];
    if (!winner) return ['증가 없음','전분기 대비 증가한 부서 없음',[]];
    return [winner.department,'전분기 대비 +'+money(winner.delta)+' · 증가에 기여한 사업',
      winner.projects.sort((a,b)=>b.delta-a.delta || a.code.localeCompare(b.code)).slice(0,3).map(v=>[v.name,'+'+money(v.delta)])];
  }
  for (const panel of document.querySelectorAll('.demo')) {
    const result = panel.querySelector('.result');
    function render() {
      const [value,caption,items]=(panel.dataset.lab==='1'?inquiries:budget)(panel);
      const title=document.createElement('strong'), text=document.createElement('p'), list=document.createElement('ul');
      title.textContent=value; text.textContent=caption;
      for(const [name,number] of items){
        const li=document.createElement('li'), metric=document.createElement('b');
        li.append(name);metric.textContent=number;li.append(metric);list.append(li);
      }
      result.replaceChildren(title,text,list);
    }
    panel.addEventListener('change',render);render();
  }
})();
