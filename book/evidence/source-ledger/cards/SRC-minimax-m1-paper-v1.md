---
source_id: SRC-minimax-m1-paper-v1
status: captured
evidence_grade: B
source_type: paper
title: "MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention"
author_or_issuer: "MiniMax"
published: 2025-06-16
verified: 2026-07-26
applies_to: "arXiv:2506.13585v1；MiniMax-M1 hybrid attention / Lightning Attention、1M context、40K/80K thinking budget 和作者报告 benchmark"
url: "https://arxiv.org/abs/2506.13585"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2025-06-16-minimax-m1-paper-v1.pdf"
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

MiniMax-M1 技术报告 v1。论文介绍 MiniMax-M1，称其为 open-weight large-scale hybrid-attention reasoning model，基于 MiniMax-Text-01，结合 MoE 与 Lightning Attention，并报告 1M context、40K/80K generation/thinking budget、RL scaling 和长上下文/agentic/tool-use benchmark。

## 支撑的结论

- MiniMax-M1 论文将模型描述为 hybrid-attention reasoning model，使用 Lightning Attention。
- 论文报告模型总参数 456B，每 token 激活 45.9B 参数。
- 论文报告模型 natively supports 1M token context，并发布 40K 和 80K thinking budget 两个版本。
- 论文报告 Lightning Attention 有助于 test-time compute/RL rollout 效率；例如与 DeepSeek R1 在 100K generation length 的 FLOPs 对比。
- 论文声明 MiniMax-M1 supported by vLLM and Transformers，并提供 GitHub/HF 发布入口。

## 限制

- 作者报告的质量、FLOPs、训练成本和效率数字尚未本地复现，不能直接写成 vLLM 生产结论。
- 论文中的 vLLM 支持声明需要回查 vLLM release/tag、MiniMax-M1 仓库和模型 config。
- 与 Kimi Linear、DeepSeek NSA/DSA、Qwen3-Next 的优劣比较需要公平 benchmark 和固定实现。

Owner:
Open questions: MiniMax-M1 GitHub commit、HF config、vLLM support release、Lightning Attention kernel path、实际 serving memory/throughput。
Handoff: efficient-long-context-attention topic。