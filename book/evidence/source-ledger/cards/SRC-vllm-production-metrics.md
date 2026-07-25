---
source_id: SRC-vllm-production-metrics
status: verified
evidence_grade: A
source_type: official-docs
title: "Production Metrics"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "latest documentation as verified; metric names and labels are version-sensitive"
url: "https://docs.vllm.ai/en/latest/usage/metrics/"
archive_path: ""
stale_after: 2026-08-25
chapters: ["02", "13", "15"]
---

# 来源摘要

官方生产指标说明。用于建立指标词典和 dashboard 映射；升级时必须检查 metric rename、label 变化和基数风险。

## 支撑的结论

- 官方 `/metrics` 暴露方式和当前指标语义。

## 限制

- `latest` 是浮动页面，引用正文前必须固定版本。
- 指标存在不代表应对其直接告警；阈值必须来自本地 SLO 和容量实验。

Owner: chapter 13
Open questions: 哪些指标在目标版本稳定，哪些存在弃用计划。
Handoff: dashboard 与告警设计。
