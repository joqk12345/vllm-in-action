---
source_id: SRC-vllm-release-v0-27-1
status: captured
evidence_grade: A
source_type: release
title: "vLLM v0.27.1 release"
author_or_issuer: "vLLM project"
published: 2026-08-11
verified: 2026-08-15
applies_to: "vLLM v0.27.1"
url: "https://github.com/vllm-project/vllm/releases/tag/v0.27.1"
archive_path: ""
stale_after: 2026-09-15
chapters: ["07", "10", "11"]
---

# 来源摘要

## 支撑的结论

- v0.27.1 是当前核对基线。
- release note 明确包含 quantized DSpark Markov heads 支持。

## 原文定位

- Release 页面，release summary。

## 限制与反证

- release note 不足以证明所有 speculative decoding、长上下文或 frontend 能力已完成本地验证。

## 验证记录

- [x] 身份与发布日期已核对
- [x] 适用版本已核对
- [ ] 与第二来源或本地实验交叉验证
- [ ] 正文引用位置已登记

## 备注

Owner: Codex
Open questions: 首个包含各专题能力的具体 commit 与本地复现结果。
Handoff: 四个专题的版本漂移审计。
