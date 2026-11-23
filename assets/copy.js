for(const pre of document.querySelectorAll('pre')){const text=pre.textContent;const b=document.createElement('button');b.textContent='복사';b.onclick=async()=>{try{await navigator.clipboard.writeText(text);b.textContent='복사됨'}catch{const range=document.createRange();range.selectNodeContents(pre.querySelector('code')||pre);getSelection().removeAllRanges();getSelection().addRange(range);b.textContent='Ctrl+C'}};pre.append(b)}
const host = location.hostname, repo = location.pathname.split('/')[1];
if (host.endsWith('.github.io') && /^[A-Za-z0-9_.-]+$/.test(repo)) {
 const box = document.getElementById('repo-link');
 if (box) {
  const a = document.createElement('a');
  a.href = 'https://github.com/' + host.split('.')[0] + '/' + repo;
  a.textContent = 'GitHub 저장소 열기 · Code에서 복제 주소 복사';
  box.append(a);
 }
}
