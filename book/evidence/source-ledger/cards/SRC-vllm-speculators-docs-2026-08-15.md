---
source_id: SRC-vllm-speculators-docs-2026-08-15
status: captured
evidence_grade: A
source_type: docs
title: "Speculators getting started and supported algorithms"
author_or_issuer: "vLLM project"
published: 2026-08-15
verified: 2026-08-15
applies_to: "Speculators docs current at capture; deployment through vLLM"
url: "https://docs.vllm.ai/projects/speculators/en/stable/user_guide/getting_started/"
archive_path: ""
stale_after: 2026-09-15
chapters: ["10", "11"]
---

# 来源摘要

## 支撑的结论

- Speculators 提供 speculator 训练、转换和通过 vLLM 部署的统一路径。
- 文档当前列出 Eagle-3 和 DFlash 等算法与预训练模型部署方式。

## 原文定位

- Getting Started：Serve a Speculator、Supported Algorithms。

## 限制与反证

- 文档能力清单不等于目标硬件上的 ITL、吞吐或 goodput 收益。
- DSpark 的具体 release 边界仍需 v0.27.1 源码/测试核对。

## 验证记录

- [x] 身份与发布日期已核对
- [x] 适用版本已核对
- [ ] 与第二来源或本地实验交叉验证
- [ ] 正文引用位置已登记

## 备注

Owner: Codex
Open questions: DSpark、MTP、EAGLE、DFlash 在固定模型/硬件下的可复现矩阵。
Handoff: speculative-decoding topic booklet。
