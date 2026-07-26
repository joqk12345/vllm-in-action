---
source_id: SRC-deltanet-explained-part-ii
status: captured
evidence_grade: C
source_type: technical-blog
title: "DeltaNet Explained (Part II)"
author_or_issuer: "Songlin Yang"
published: 2024-12-03
verified: 2026-07-26
applies_to: "DeltaNet chunkwise parallel algorithm explanation; background for GDN/KDA but not primary paper evidence"
url: "https://sustcsonglin.github.io/blog/2024/deltanet-2/"
archive_path: "research/topics/efficient-long-context-attention/source/articles/2024-12-03-deltanet-explained-part-ii.html"
stale_after: 2026-08-26
chapters: ["09", "11", "12"]
---

# 来源摘要

Songlin Yang 的技术博客，解释 DeltaNet 如何从 sequence-length 维度并行化，讨论 parallel scan 的局限和 chunkwise algorithm / WY representation。可帮助理解 Gated DeltaNet 和 Kimi Delta Attention 的硬件友好背景。

## 支撑的结论

- 作为教学性解释，说明原始 DeltaNet 作为纯 RNN 存在 O(L) sequential steps，对 GPU 不友好。
- 解释为什么需要 chunkwise parallel form 来实现硬件友好训练。
- 为 GDN/KDA 的“delta rule + chunkwise parallelism”提供背景理解。

## 限制

- 博客不是正式论文证据；正文机制结论应优先引用 arXiv/ICLR 论文、源码或测试。
- 博客解释 DeltaNet algorithm，不直接证明 Qwen3-Next/Qwen3.5 或 vLLM 的具体实现行为。

Owner:
Open questions: 与 Gated DeltaNet paper、Kimi Linear paper 中 chunkwise algorithm 的差异。
Handoff: efficient-long-context-attention topic。