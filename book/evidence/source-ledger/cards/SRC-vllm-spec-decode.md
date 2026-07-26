---
source_id: SRC-vllm-spec-decode
status: captured
evidence_grade: B
source_type: official-docs
title: "vLLM speculative decoding documentation"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "vLLM 官方浮动文档；用于发现 speculative decoding 配置、限制和支持矩阵"
url: "https://docs.vllm.ai/en/latest/features/spec_decode/"
archive_path: ""
stale_after: 2026-08-25
chapters: ["10", "11", "15"]
---

# 来源摘要

vLLM speculative decoding 官方文档入口，用于发现当前配置、限制、支持矩阵和生产注意事项。

## 支撑的结论

- 官方文档中声明的当前 speculative decoding 能力和限制线索。

## 限制

- `latest` 是浮动文档，不能作为正文固定事实。
- 需要绑定具体 release 文档、源码和测试。
- 文档支持不等于本仓目标 workload 通过。

Owner:
Open questions: 目标 release 中 dynamic speculation、LoRA、DSpark Markov/confidence head 的确切支持状态。
Handoff: capability matrix、生产决策、benchmark 设计。