const aside = document.querySelector('aside');
document.querySelector('#menu').addEventListener('click', () => aside.classList.toggle('open'));
let index;
const input = document.querySelector('#search');
const results = document.querySelector('#results');
input.addEventListener('focus', async () => { index ||= await (await fetch('search.json')).json(); });
input.addEventListener('input', async () => {
  index ||= await (await fetch('search.json')).json();
  const query = input.value.trim().toLowerCase();
  if (!query) { results.innerHTML = ''; return; }
  results.innerHTML = index.filter(x => `${x.title} ${x.text}`.toLowerCase().includes(query)).slice(0, 8).map(x => `<a href="${x.url}">${x.title}</a>`).join('') || '<small>没有结果</small>';
});
document.addEventListener('keydown', e => { if (e.key === '/') { e.preventDefault(); input.focus(); } });
