# vLLM 深入研究 / vLLM Deep Dive

> **《vLLM 深入研究：从 Token 到生产服务》**
>
> 一部基于当前源码、面向推理工程师与平台负责人的中文开源书。

本仓库不再只有知识库骨架：`book/chapters/` 已包含 16 章连续正文，系统讲解请求生命周期、Paged KV、混合/线性注意力、调度、分布式推理、量化、推测解码、编译与算子、观测、安全和生产运营；附录提供源码地图与八个实验。`website/` 和零依赖 Node 构建器同时生成静态网站与单文件 Markdown book。

## 当前代码基线

正文针对 vLLM commit `fe1c317157d4478fdc0e02096447e61305b871e9`（`v0.27.2rc0-129-gfe1c317157`）于 2026-08-16 核对。版本敏感结论必须在目标部署 tag 上重验。书中不虚构 GPU benchmark 数字；硬件相关结论以可执行实验说明交付。

## 阅读

- [前言](book/front-matter/preface.md)
- [第 1 章：从能跑到能上线](book/chapters/01-from-demo-to-production.md)
- [第 4 章：显存、分页 KV Cache 与混合注意力](book/chapters/04-memory-and-kv-cache.md)
- [第 8 章：分布式推理与硬件拓扑](book/chapters/08-parallelism-and-topology.md)
- [第 11 章：热点注意力与延迟优化](book/chapters/11-latency-optimization.md)
- [第 12 章：算子优化、编译与单位成本](book/chapters/12-throughput-and-cost.md)
- [源码研究地图](book/back-matter/source-code-map.md)
- [八个递进实验](book/back-matter/labs.md)
- [完整书脊](book/spine.yml)

## 构建 book 与 website

只需 Node.js 18+，无第三方 npm 依赖：

```bash
npm run check       # 校验正文并构建
npm run build       # 生成 dist/
npm run preview     # http://127.0.0.1:4173
```

产物：

- `dist/index.html`：响应式静态网站，含侧栏、前后章导航与中文全文搜索；
- `dist/vllm-deep-dive.md`：按书脊合并的单文件 book，可继续交给 Pandoc 等工具制作 EPUB/PDF；
- 每章独立 HTML，可直接部署到 GitHub Pages、对象存储或任意静态站点。

知识库结构校验：

```bash
python3 scripts/validate_kb.py
```

## 内容与证据

`book/spine.yml` 是阅读顺序唯一来源；`book/chapters/` 是正文唯一来源；`book/evidence/` 保存来源与实验；`research/topics/` 保存尚需证据门禁的投机解码、llm-d、长上下文注意力和 Rust frontend 专题。当前本地源码快照来源卡为 `SRC-vllm-local-fe1c317`。

## 仓库地图

```text
book/chapters/       16 章正文
book/back-matter/    源码地图、实验、术语与参考
book/evidence/       来源卡、benchmark 与实验记录
research/topics/     热点专题研究
website/             网站样式与搜索逻辑
scripts/build-book.mjs  零依赖构建器
scripts/check-book.mjs  书稿门禁
```

## 边界与披露

本书由人类发起并使用 AI 辅助写作。性能配置不是通用推荐；公开出版前，人类提交者应逐行审阅、运行目标硬件实验、完成技术/安全审校并选择许可证。vLLM 是快速演进项目，源码与目标版本冲突时以目标 tag 的源码、测试和实际实验为准。
