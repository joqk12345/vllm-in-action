import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'dist');
if (!fs.existsSync(path.join(root, 'index.html'))) throw new Error('Run npm run build first');
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.json':'application/json', '.md':'text/markdown; charset=utf-8' };
http.createServer((req,res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  const target = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!target.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(target, (err,data) => { if (err) { res.writeHead(404).end('Not found'); return; } res.setHeader('Content-Type', types[path.extname(target)] || 'application/octet-stream'); res.end(data); });
}).listen(4173, '127.0.0.1', () => console.log('Book: http://127.0.0.1:4173'));
