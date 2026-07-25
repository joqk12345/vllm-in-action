---
source_id: SRC-vllm-benchmark-cli
status: verified
evidence_grade: A
source_type: official-docs
title: "vLLM Benchmark CLI"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "stable documentation as verified; CLI flags are version-sensitive"
url: "https://docs.vllm.ai/en/stable/benchmarking/cli/"
archive_path: ""
stale_after: 2026-08-25
chapters: ["02", "09", "11", "12"]
---

# 来源摘要

官方 benchmark CLI 入口，用于核对工具能够生成的工作负载和指标。工具提供能力不等于实验方法自动正确，本书仍需规定数据分布、重复、warm-up 和公平性。

## 支撑的结论

- 当前 benchmark 子命令、参数和输出能力。
- 官方示例所展示的基本调用方式。

## 限制

- CLI 默认值和指标字段可能随版本变化。
- 跨硬件或跨框架比较需要额外的公平性设计。

Owner: chapter 09
Open questions: 标准结果 schema 与统计方法。
Handoff: 首套基线 benchmark。
