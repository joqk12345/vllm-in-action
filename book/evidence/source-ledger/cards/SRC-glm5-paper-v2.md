---
source_id: SRC-glm5-paper-v2
status: captured
evidence_grade: B
source_type: paper
title: "GLM-5: from Vibe Coding to Agentic Engineering"
author_or_issuer: "GLM-5 Team"
published: 2026-02-24
verified: 2026-07-26
applies_to: "arXiv:2602.15763v2；作者报告的 GLM-5 架构、DSA、长上下文训练和实验"
url: "https://arxiv.org/abs/2602.15763"
archive_path: "research/topics/efficient-long-context-attention/source/papers/2026-02-24-glm-5-paper-v2.pdf"
stale_after: 2026-08-26
chapters: ["04", "08", "09", "11", "12", "15"]
---

# 来源摘要

GLM-5 论文 v2，是本专题当前主要来源，包含 DSA、MLA、efficient attention 消融、长上下文训练、DP-aware routing 和 kernel 线索。

## 支撑的结论

- GLM-5 作者报告的 DSA 设计动机、训练流程和长上下文实验。
- efficient attention 方法之间质量/效率取舍的作者报告观察。

## 限制

- 不证明 vLLM 已支持 GLM-5/DSA 或等价 serving 路径。
- 作者 benchmark 不能直接外推到本仓目标 workload。
- 进入正文前需固定 arXiv version，并补充本仓实验或上游实现证据。

Owner:
Open questions: DSA/GLM-5 在 vLLM 中的支持状态、kernel 要求和 serving 指标。
Handoff: efficient-long-context-attention topic。