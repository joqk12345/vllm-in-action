import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const spine = fs.readFileSync(path.join(root, 'book/spine.yml'), 'utf8');

function parseSpine(text) {
  const items = [];
  let part = '前后文';
  let section = '';
  for (const line of text.split('\n')) {
    const partMatch = line.match(/^\s{4}title:\s*"(.+)"/);
    if (partMatch) part = partMatch[1];
    if (/^front_matter:/.test(line)) section = 'front';
    if (/^parts:/.test(line)) section = 'parts';
    if (/^back_matter:/.test(line)) { section = 'back'; part = '附录与索引'; }
    const fileMatch = line.match(/^\s+- file:\s*(\S+)/);
    if (fileMatch) items.push({ file: fileMatch[1], part });
    const chapterMatch = line.match(/^\s+- "(\d{2}-[^"]+)"/);
    if (chapterMatch && section === 'parts') {
      items.push({ file: `book/chapters/${chapterMatch[1]}.md`, part });
    }
  }
  return items;
}

const escapeHtml = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const slugify = (s) => s.trim().toLowerCase().replace(/[\s/：]+/g, '-').replace(/[^\p{L}\p{N}_.-]/gu, '');
function inline(s) {
  let out = escapeHtml(s);
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return out;
}

function markdown(md) {
  const lines = md.replace(/^---\n[\s\S]*?\n---\n/, '').split('\n');
  const out = [];
  let inCode = false, code = [], list = null, quote = false, table = null;
  const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };
  const closeQuote = () => { if (quote) { out.push('</blockquote>'); quote = false; } };
  const closeTable = () => { if (table) { out.push('</tbody></table>'); table = null; } };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('```')) {
      closeList(); closeQuote(); closeTable();
      if (!inCode) { inCode = true; code = []; }
      else { out.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`); inCode = false; }
      continue;
    }
    if (inCode) { code.push(line); continue; }
    if (/^<!--/.test(line)) continue;
    const heading = line.match(/^(#{1,4})\s+(.+)/);
    if (heading) { closeList(); closeQuote(); closeTable(); const n = heading[1].length; out.push(`<h${n} id="${slugify(heading[2])}">${inline(heading[2])}</h${n}>`); continue; }
    if (/^\|.+\|$/.test(line) && /^\|[\s:|-]+\|$/.test(lines[i + 1] || '')) {
      closeList(); closeQuote(); const cells = line.slice(1, -1).split('|').map(x => `<th>${inline(x.trim())}</th>`).join('');
      out.push(`<table><thead><tr>${cells}</tr></thead><tbody>`); table = true; i++; continue;
    }
    if (table && /^\|.+\|$/.test(line)) { const cells = line.slice(1, -1).split('|').map(x => `<td>${inline(x.trim())}</td>`).join(''); out.push(`<tr>${cells}</tr>`); continue; }
    closeTable();
    const bullet = line.match(/^\s*[-*]\s+(.+)/); const ordered = line.match(/^\s*\d+\.\s+(.+)/);
    if (bullet || ordered) { closeQuote(); const wanted = bullet ? 'ul' : 'ol'; if (list !== wanted) { closeList(); list = wanted; out.push(`<${list}>`); } out.push(`<li>${inline((bullet || ordered)[1])}</li>`); continue; }
    closeList();
    if (line.startsWith('> ')) { if (!quote) { out.push('<blockquote>'); quote = true; } out.push(`<p>${inline(line.slice(2))}</p>`); continue; }
    closeQuote();
    if (!line.trim()) continue;
    if (line === '$$') { const math = []; while (++i < lines.length && lines[i] !== '$$') math.push(lines[i]); out.push(`<pre class="math">${escapeHtml(math.join('\n'))}</pre>`); continue; }
    out.push(`<p>${inline(line)}</p>`);
  }
  closeList(); closeQuote(); closeTable();
  if (inCode) out.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
  return out.join('\n');
}

const items = parseSpine(spine).map((item, index, all) => {
  const source = path.join(root, item.file);
  if (!fs.existsSync(source)) throw new Error(`Spine file missing: ${item.file}`);
  const md = fs.readFileSync(source, 'utf8');
  const title = md.match(/^#\s+(.+)$/m)?.[1] || path.basename(item.file, '.md');
  const slug = item.file.includes('/chapters/') ? path.basename(item.file, '.md') : `_${path.basename(item.file, '.md')}`;
  return { ...item, md, title, slug, index };
});

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });
const nav = items.map((x, i) => `${i === 0 || items[i - 1].part !== x.part ? `<h3>${escapeHtml(x.part)}</h3>` : ''}<a href="${x.slug}.html">${escapeHtml(x.title)}</a>`).join('');
const shell = (item, body) => `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="vLLM 架构、混合注意力、分布式推理与算子优化深入研究"><title>${escapeHtml(item.title)} · vLLM 深入研究</title><link rel="stylesheet" href="assets/style.css"></head><body><button id="menu" aria-label="菜单">☰</button><aside><div class="brand">vLLM 深入研究<small>从 Token 到生产服务</small></div><input id="search" placeholder="全文搜索 /"><div id="results"></div><nav>${nav}</nav></aside><main><article>${body}</article><footer>${item.index > 0 ? `<a href="${items[item.index - 1].slug}.html">← ${escapeHtml(items[item.index - 1].title)}</a>` : '<span></span>'}${item.index + 1 < items.length ? `<a href="${items[item.index + 1].slug}.html">${escapeHtml(items[item.index + 1].title)} →</a>` : ''}</footer></main><script src="assets/app.js"></script></body></html>`;
for (const item of items) fs.writeFileSync(path.join(dist, `${item.slug}.html`), shell(item, markdown(item.md)));
fs.writeFileSync(path.join(dist, 'index.html'), shell(items[0], `<section class="hero"><p class="eyebrow">CODE-VERIFIED OPEN BOOK</p><h1>vLLM 深入研究</h1><p>从请求生命周期、分页 KV 与混合注意力，到分布式推理、算子优化和生产运营。</p><a class="start" href="${items[1].slug}.html">开始阅读 →</a><div class="stats"><span><b>16</b> 章正文</span><span><b>2</b> 个实践附录</span><span><b>${items.reduce((n,x)=>n+x.md.length,0).toLocaleString()}</b> 字符</span></div></section>`));
fs.writeFileSync(path.join(dist, 'search.json'), JSON.stringify(items.map(x => ({ title: x.title, url: `${x.slug}.html`, text: x.md.replace(/[`#>*|\[\]()-]/g, ' ').replace(/\s+/g, ' ').slice(0, 5000) }))));
const combined = items.map(x => `\n\n<!-- source: ${x.file} -->\n\n${x.md}`).join('').trim() + '\n';
fs.writeFileSync(path.join(dist, 'vllm-deep-dive.md'), combined);
fs.mkdirSync(path.join(dist, 'assets'));
fs.copyFileSync(path.join(root, 'website/style.css'), path.join(dist, 'assets/style.css'));
fs.copyFileSync(path.join(root, 'website/app.js'), path.join(dist, 'assets/app.js'));
console.log(`Built ${items.length} pages and combined Markdown in ${path.relative(root, dist)}/`);
