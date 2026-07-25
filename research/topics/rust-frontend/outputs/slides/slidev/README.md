# Rust Frontend Slidev

18 页 Slidev 演示，主文件为 [`slides.md`](slides.md)。`prepare:assets` 会在预览、构建或导出前，把专题输出层的三张共享 SVG 同步到 `public/figures`。专题 `outputs/figures/` 仍是唯一源文件。

## 安装

在本目录执行：

```bash
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install
```

依赖已固定为：

- `@slidev/cli@52.18.0`
- `@slidev/theme-default@0.25.0`
- `playwright-chromium@1.62.0`

跳过 Playwright 浏览器下载，是因为导出命令会复用本机 Google Chrome。

## 预览与构建

```bash
npm run dev
npm run build
```

以上命令会自动先执行 `npm run prepare:assets`，避免 Vite 的 `slide-import-guard` 拒绝项目根目录外的软链接资源。

## 导出

```bash
npm run export:png
npm run export:pptx
```

- PNG 会写入 `.qa/`，用于逐页检查。
- PPTX 会写入上一级 `rust-frontend-architecture-and-production-readiness.pptx`。
- Slidev 的 PPTX 是逐页图片，文字不可直接编辑；讲者备注会随各页保留。

## 证据入口

- Claim spine：`../../../claims.yml`
- Research Brief：`../../brief/rust-frontend-research-brief.md`
- 章节转写包：`../../chapter-handoff/chapter-contributions.md`
