---
source_id: SRC-vllm-openai-server
status: verified
evidence_grade: A
source_type: official-docs
title: "OpenAI-Compatible Server"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "stable documentation as verified; exact endpoint behavior is version-sensitive"
url: "https://docs.vllm.ai/en/stable/serving/openai_compatible_server/"
archive_path: ""
stale_after: 2026-08-25
chapters: ["06", "14", "15"]
---

# 来源摘要

官方在线服务与兼容 API 入口。API 的“兼容”不等于所有参数和边缘行为等价，书中必须用契约测试明确差异。

## 支撑的结论

- 官方暴露的服务入口、端点和基础行为。
- 官方明确声明的限制与警告。

## 限制

- 客户端版本、chat template 和模型 generation config 都可能改变结果。
- 安全、限流、幂等和网关设计不能只依赖此页。

Owner: chapter 06
Open questions: 兼容性测试覆盖哪些客户端与 endpoint。
Handoff: API 契约测试。
