---
source_id: SRC-minimax-m2-series-paper-v1
status: captured
evidence_grade: B
source_type: paper
title: "The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence"
author_or_issuer: "MiniMax"
published: 2026-05-26
verified: 2026-07-26
applies_to: "arXiv:2605.26494v1；MiniMax-M2 architecture, full-attention choice, agentic deployment/RL system observations"
url: "https://arxiv.org/abs/2605.26494"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2026-05-26-minimax-m2-series-paper-v1.pdf"
stale_after: 2026-08-26
chapters: ["09", "11", "12", "13", "15"]
---

# 来源摘要

MiniMax-M2 系列技术报告 v1。论文介绍 MiniMax-M2 系列 MoE 模型，并明确说明 M2 在 attention 设计上采用 full multi-head attention + GQA，偏离 MiniMax-Text-01 中 interleaves Lightning Attention with full attention 的 hybrid 设计。

## 支撑的结论

- M2 flagship 模型报告 229.9B total parameters、9.8B activated per token、62-layer decoder-only Transformer、256 experts、8 experts activated per token。
- 论文报告 M2 使用 full multi-head attention with GQA，native context window 为 192K。
- 论文第 2.2.2 节说明 M2 放弃 MiniMax-Text-01 的 hybrid Lightning/full attention 设计，并称在 reasoning、coding、agent tasks 的生产设置中未找到可靠匹配 full attention 质量的 efficient attention 变体。
- 论文报告 hybrid SWA variants 在长上下文 retrieval、multi-hop reasoning、in-context learning 和 SFT 后 >32K 场景中表现劣于 full attention。
- 论文提出 Forge、windowed-FIFO scheduling、prefix-tree merging、inference optimization、global L3 KV cache pool 等 agentic RL / serving 系统线索。

## 限制

- 作者论文结论尚未本地复现；“full attention 更适合 M2”不能外推到所有模型或所有 efficient attention 方案。
- 论文对 hybrid/SWA/linear/sparse 的负面观察是 MiniMax 自身生产设置中的报告，需要固定训练 recipe、任务和模型规模理解。
- vLLM 支持、具体模型 config、推理 kernel 和 serving 性能仍需另查源码/实验。

Owner:
Open questions: MiniMax-M2 release repo/HF config、vLLM support status、M2 full attention serving cost、与 M1 Lightning Attention 的版本差异。
Handoff: efficient-long-context-attention topic；llm-d-agentic-serving topic。