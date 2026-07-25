---
source_id: SRC-vllm-repository
status: verified
evidence_grade: A
source_type: source-code
title: "vLLM official repository"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "main branch and tagged releases; cite an exact commit for正文结论"
url: "https://github.com/vllm-project/vllm"
archive_path: ""
stale_after: 2026-08-25
chapters: ["01", "03", "04", "05", "06", "07", "08", "10", "15"]
---

# 来源摘要

vLLM 的官方源码、测试、Issue 与 PR 入口。它是实现行为的一手来源，但 `main` 会持续变化；正文不得只引用浮动分支，必须补充 tag 或 commit。

## 支撑的结论

- 实现细节、默认行为和支持范围的最终核对入口。
- release、Issue、PR 与代码变更之间的追踪入口。

## 不支撑

- 未经测量的生产性能结论。
- 某项功能在特定模型和硬件上“最佳”的判断。

## 验证记录

- [x] 官方组织与仓库身份已核对
- [x] 适用版本边界已写明
- [ ] 具体正文引用需固定 commit

Owner: research
Open questions: 首批源码锚点随第 3、4 章调研补齐。
Handoff: release triage 与章节研究。
