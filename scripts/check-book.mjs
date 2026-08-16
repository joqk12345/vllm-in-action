import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
execFileSync(process.execPath, ['scripts/build-book.mjs'], { cwd: root, stdio: 'inherit' });
const chapters = fs.readdirSync(path.join(root, 'book/chapters')).filter(x => /^\d{2}-.+\.md$/.test(x)).sort();
const errors = [];
if (chapters.length !== 16) errors.push(`expected 16 chapters, got ${chapters.length}`);
for (const file of chapters) {
  const text = fs.readFileSync(path.join(root, 'book/chapters', file), 'utf8');
  if (!/^# 第 \d+ 章/m.test(text)) errors.push(`${file}: missing chapter title`);
  if (!/<!-- verified: [0-9a-f]{40}, \d{4}-\d{2}-\d{2} -->/.test(text)) errors.push(`${file}: missing verified marker`);
  if (text.length < 1400) errors.push(`${file}: too short (${text.length})`);
}
const html = fs.readdirSync(path.join(root, 'dist')).filter(x => x.endsWith('.html'));
if (html.length < 21) errors.push(`expected at least 21 HTML pages, got ${html.length}`);
const index = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
if (!index.includes('vLLM 深入研究') || !index.includes('search')) errors.push('website shell incomplete');
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log(`Book check passed: ${chapters.length} chapters, ${html.length} HTML files.`);
