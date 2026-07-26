---
source_id: SRC-speculators-main
status: captured
evidence_grade: B
source_type: upstream-repository
title: "vllm-project/speculators"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "浮动 main；用于发现训练、转换、checkpoint config 和 vLLM 部署能力"
url: "https://github.com/vllm-project/speculators"
archive_path: ""
stale_after: 2026-08-25
chapters: ["10", "15"]
---

# 来源摘要

Speculators 上游仓库，用于发现 drafter 训练、转换、微调和 vLLM 部署路径。

## 支撑的结论

- 上游公开描述和源码中存在的训练/部署能力线索。

## 限制

- 浮动 main 不能作为正文永久事实。
- README 支持项不证明任意 vLLM release、模型配置或硬件组合可运行。
- 进入正文前必须固定 commit，并核查测试和兼容 vLLM release。

Owner:
Open questions: DSpark、DFlash、EAGLE、PEEGO 的支持矩阵和 release 边界。
Handoff: capability matrix、训练流程、章节 15。