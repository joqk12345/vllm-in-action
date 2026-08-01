---
source_id: SRC-kimi-k3-tech-report-2026-07-28
status: captured
evidence_grade: B
source_type: technical-report
title: "Kimi K3: Open Frontier Intelligence"
author_or_issuer: "Kimi Team"
published: 2026-07-28
verified: 2026-08-01
applies_to: "Kimi K3 technical report; vLLM main support fixed to aeeb36b1, stable release and HF/model revisions not fixed"
url: "https://huggingface.co/moonshotai/Kimi-K3"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2026-07-28-kimi-k3-tech-report.pdf"
stale_after: 2026-10-28
chapters: ["08", "09", "11", "12", "15"]
---

# 来源摘要

Kimi K3 作者技术报告。本仓当前只用作高效长上下文注意力专题的 B 级作者报告来源，重点关注 KDA/Kimi Linear 路线在 1M context、hybrid KDA–MLA、prefix cache、speculative decoding 和 prefill/context parallelism 上的系统设计线索。

## 支撑的结论

- Kimi K3 报告称模型采用 2.8T total parameters、104B activated parameters、1M-token context window。
- 报告称 Kimi K3 使用 hybrid KDA–MLA：每个 block 为 3 KDA + 1 Gated MLA；表格给出全模型 69 KDA + 24 MLA。
- 报告描述 FlashKDA 与 KDA Context Parallelism，用于缓解 KDA recurrent state 在长上下文 prefill 中的串行传播瓶颈。
- 报告描述 KDA-aware prefix cache：MLA KV 与 KDA recurrent state 必须在同一命中边界共同恢复。
- 报告描述 KDA decoding 与 MTP/speculative decoding rollback 的冲突，并提出 projected-input replay。

## 原文定位

- §2.1 Hybrid Attention / Kimi Delta Attention：3:1 KDA–MLA、KDA 变体。
- Table 1：Kimi K2 vs Kimi K3 架构对比，含 1M context、69 KDA + 24 MLA。
- §5.1 Algorithm-System Co-Design for KDA：FlashKDA、KDA Context Parallelism。
- §5.4 Inference and Online Serving：KDA-aware prefix cache、高性能 kernels、fleet scheduling。
- §5.4.2 High-Performance Kernels：KDA decoding 与 speculative decoding state replay。

## 限制与反证

- 报告中的性能、排行榜、部署效果和 `2.5× scaling efficiency` 均为作者报告，未在本仓复现。
- `2.5× scaling efficiency` 来自 KDA、Attention Residuals、Stable LatentMoE、数据和训练 recipe 等组合，不能归因于 KDA 单项。
- 当前未固定 Kimi K3 HF revision、模型 config、公开报告 URL或首个稳定 vLLM support release；仅已固定 `main` merge commit。
- 不能把 Kimi K3 的 3:1 KDA–MLA 写成所有 hybrid attention 模型的通用最优。

## 验证记录

- [x] 本地 PDF 已捕获并登记 SHA256。
- [ ] 身份与发布日期已通过公开页面核对。
- [ ] HF model/config revision 已固定。
- [x] vLLM `main` 支持 merge commit、源码范围和相关 tests 已核查。
- [ ] 首个稳定 vLLM release 已核查。
- [ ] 与本仓 smoke test 或 serving benchmark 交叉验证。
- [ ] 正文引用位置已登记。

## 备注

Owner: 未指定
Open questions: 首个稳定 release、HF revisions、镜像 digest、FlashInfer 稳定依赖，以及 KDA-aware cache/KDA spec decode replay 的本仓复现。
Handoff: 第 08、09、11、12、15 章。
