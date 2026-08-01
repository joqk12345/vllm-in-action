---
source_id: SRC-gated-deltanet-paper-v3
status: captured
evidence_grade: B
source_type: paper
title: "Gated Delta Networks: Improving Mamba2 with Delta Rule"
author_or_issuer: "Songlin Yang, Jan Kautz, Ali Hatamizadeh"
published: 2025-03-06
verified: 2026-07-26
applies_to: "arXiv:2412.06464v3 / ICLR 2025；Gated DeltaNet/GDN 机制、chunkwise parallel training algorithm、hybrid GDN architectures"
url: "https://arxiv.org/abs/2412.06464"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2024-12-09-gated-delta-networks-paper-v1.pdf"
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

ICLR 2025 论文，提出 Gated DeltaNet / Gated Delta Networks。论文把 Mamba2 式 gating 和 DeltaNet 的 delta update rule 结合，提出 gated delta rule，并扩展 chunkwise parallel algorithm 以支持硬件友好训练。

## 支撑的结论

- GDN 结合 gating 的快速遗忘/清空能力与 delta rule 的定向 key-value association 更新能力。
- 论文将 GDN 定位为改进 Mamba2 与 DeltaNet 的线性注意力/RNN-style token mixer。
- 论文提出 hardware-efficient chunkwise training algorithm，并强调 matmul/tensor-core 友好。
- 论文报告 Gated DeltaNet 在 language modeling、commonsense reasoning、in-context retrieval、length extrapolation、long-context understanding 等 benchmark 上超过 Mamba2/DeltaNet。
- 论文还探索将 Gated DeltaNet 与 SWA 或 Mamba2 组合的 hybrid architectures。

## 限制

- 作者论文结果尚未本地复现，不能直接转化为 vLLM serving 性能结论。
- GDN 与 Qwen3-Next/Qwen3.5 的关系需要回查 Qwen 官方 config、技术报告和 vLLM 源码。
- 论文 PDF 文件名含 `v1`，但 PDF 文本显示 arXiv v3 / ICLR 2025；进入正文前需复核 arXiv 版本和下载 URL。

Owner:
Open questions: Qwen3-Next/Qwen3.5 中 GDN 的具体参数、层分布、vLLM v0.26.0 serving path 和 kernel backend。
Handoff: efficient-long-context-attention topic。