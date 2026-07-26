---
source_id: SRC-kimi-linear-paper-v2
status: captured
evidence_grade: B
source_type: paper
title: "Kimi Linear: An Expressive, Efficient Attention Architecture"
author_or_issuer: "Kimi Team"
published: 2025-11-01
verified: 2026-07-26
applies_to: "arXiv:2510.26692v2；作者报告的 Kimi Linear/KDA 架构、实验和 vLLM integration 描述"
url: "https://arxiv.org/abs/2510.26692"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2025-11-01-kimi-linear-paper-v2.pdf"
stale_after: 2026-08-26
chapters: ["04", "08", "09", "11", "12", "15"]
---

# 来源摘要

Kimi Linear 技术报告 v2，提出 hybrid linear attention 架构和 Kimi Delta Attention（KDA），并报告与 full attention MLA、hybrid GDN-H 的公平比较。

## 支撑的结论

- KDA 扩展 Gated DeltaNet，引入更细粒度 gating，并使用 chunkwise / DPLR 相关硬件友好算法。
- Kimi Linear 采用 KDA 与 full MLA 的层级混合结构，论文报告 3:1 KDA:MLA 比例。
- 作者报告 Kimi Linear 在短上下文、长上下文和 RL-style 评估中对比 MLA/GDN-H 的结果，以及 KV cache 与 decoding throughput 收益。
- 论文声明开源 KDA kernel 与 vLLM implementations。

## 限制

- 作者报告的性能和加速数字不能直接外推到本仓目标 vLLM release、硬件或 workload。
- “vLLM implementation” 需回查具体仓库 commit、支持版本和测试覆盖。
- Kimi Linear 与 DeepSeek sparse attention、Qwen3-Next、MiniMax M1/M2 的比较仍需各自官方来源。

Owner:
Open questions: KDA kernel/vLLM integration 的具体 commit、模型 checkpoint、serving 配置和本仓复现 benchmark。
Handoff: efficient-long-context-attention topic。