---
chapter_id: "11-latency-optimization"
part: III
title: "优化 TTFT 与 ITL"
status: draft
depends_on: ["09-benchmarking", "10-scheduling-and-batching"]
evidence_status: partial
---

# 章节承诺

把 TTFT 与 ITL 分开诊断，按瓶颈选择优化而不是堆叠特性。

## 必须包含

- 排队、tokenization、prefill、decode、网络对延迟的贡献。
- 并发、批大小、prefix caching、推测解码等策略的适用边界。
- p50 改善但 p99 恶化的反例。

## 读者产物

延迟分解表和逐层实验顺序。

## 证据缺口

端到端 trace；至少两类模型的对照；高级解码质量验证。
