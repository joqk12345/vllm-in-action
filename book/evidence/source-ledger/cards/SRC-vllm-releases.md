---
source_id: SRC-vllm-releases
status: verified
evidence_grade: A
source_type: release-notes
title: "vLLM Releases"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "all tagged releases"
url: "https://github.com/vllm-project/vllm/releases"
archive_path: ""
stale_after: 2026-08-08
chapters: ["05", "06", "07", "08", "10", "13", "14", "15"]
---

# 来源摘要

官方 release note 索引，是版本影响分析的第一入口。每个版本还需继续核对关键 PR、文档和必要实验，不能把 release note 宣称直接当作通用最佳实践。

## 支撑的结论

- 某项变化在哪个 tag 发布。
- 官方标注的 feature、fix、breaking change 与迁移线索。

## 不支撑

- 没有披露环境的性能收益。
- 未经核对的兼容性外推。

## 验证记录

- [x] 官方发布页已核对
- [x] 已设短复查周期
- [ ] 各版本需建立独立 impact 文档

Owner: release tracker
Open questions: 是否需要自动生成版本差异清单。
Handoff: `research/releases/`。
