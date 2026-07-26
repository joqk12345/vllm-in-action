---
source_id: SRC-dspark-paper-v1
status: captured
evidence_grade: B
source_type: paper
title: "DSpark arXiv v1"
author_or_issuer: "DSpark authors"
published: 2026-07-06
verified: 2026-07-25
applies_to: "arXiv:2607.05147v1；作者报告的算法、实验设置和结果"
url: "https://arxiv.org/abs/2607.05147"
archive_path: "research/topics/speculative-decoding/source/papers/2026-07-06-dspark-paper-v1.pdf"
stale_after: 2026-08-25
chapters: ["10", "11"]
---

# 来源摘要

DSpark 论文 v1，是本专题 DSpark 算法结构、训练目标、作者实验和限制的主要一手来源。

## 支撑的结论

- DSpark 的并行 backbone、顺序 head、confidence/prefix survival probability 和 hardware-aware prefix scheduling 设计。
- 论文中指定模型、数据、采样和内部系统条件下的作者报告结果。

## 限制

- 不能证明任意 vLLM release 已实现等价能力。
- 作者报告 benchmark 不能外推到本仓目标 workload。
- 进入正文前应固定 arXiv version，并与本仓实验区分。

Owner:
Open questions: 本仓是否能复现 DSpark 相对 DFlash/EAGLE/MTP 的接受长度和端到端收益。
Handoff: 第 10、11 章。