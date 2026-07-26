---
source_id: SRC-flash-linear-attention-kda
status: captured
evidence_grade: A
source_type: source-code
title: "flash-linear-attention KDA operators"
author_or_issuer: "fla-org / Flash Linear Attention contributors"
published: null
verified: 2026-07-26
applies_to: "GitHub repository HEAD fixed at 0a9b9f222e86b9a895c2447767e9b4cce6c8d530; `fla/ops/kda` implementation"
url: "https://github.com/fla-org/flash-linear-attention/tree/0a9b9f222e86b9a895c2447767e9b4cce6c8d530/fla/ops/kda"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

Flash Linear Attention 仓库中的 KDA operator 实现。当前固定 commit `0a9b9f222e86b9a895c2447767e9b4cce6c8d530` 下，`fla/ops/kda` 暴露 `chunk_kda` 与 `fused_recurrent_kda`，包含 chunk / recurrent / gate / Triton Ascend 等实现文件。

## 支撑的结论

- `fla/ops/kda/__init__.py` 导出 `chunk_kda` 与 `fused_recurrent_kda`。
- `fla/ops/kda/chunk.py` 包含训练/预填充相关 chunk KDA autograd wrapper，注释标明相关文件由 Moonshot AI Team 修改和支持。
- `fla/ops/kda/fused_recurrent.py` 包含 Triton fused recurrent KDA kernel，并有注释称该 kernel modified from vLLM gdn/kda model decode kernel。

## 限制

- 该仓库实现不是 vLLM release 本身；vLLM 内部 vendored/third-party 代码可能存在差异。
- 需要以固定 vLLM commit 或 release 核查 serving path。

Owner:
Open questions: 与 vLLM vendored KDA 代码的差异、CUDA/Ascend 覆盖、数值测试与性能测试。
Handoff: efficient-long-context-attention topic。