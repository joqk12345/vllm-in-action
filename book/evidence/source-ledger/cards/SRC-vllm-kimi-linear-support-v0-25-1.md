---
source_id: SRC-vllm-kimi-linear-support-v0-25-1
status: captured
evidence_grade: A
source_type: source-code
title: "vLLM v0.25.1 KimiLinearForCausalLM support"
author_or_issuer: "vllm-project/vllm"
published: 2026-07-12
verified: 2026-07-26
applies_to: "vLLM tag v0.25.1 commit 752a3a504485790a2e8491cacbb35c137339ad34; current production-facing baseline noted by project maintainer/user"
url: "https://github.com/vllm-project/vllm/tree/v0.25.1"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

vLLM `v0.25.1` tag 中可观察到 Kimi Linear 模型支持入口和 KDA 路径。该卡用于将研究从“首个支持边界 v0.11.1”推进到当前应关注的 release 基线。

## 支撑的结论

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`，模型示例包括 `moonshotai/Kimi-Linear-48B-A3B-Base` 和 `moonshotai/Kimi-Linear-48B-A3B-Instruct`。
- `vllm/model_executor/models/registry.py` 注册 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/kimi_linear.py` 存在 Kimi Linear 模型实现。
- `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` 存在 `KimiGatedDeltaNetAttention`，并从 `vllm/model_executor/layers/fla/ops/kda.py` 引入 `chunk_kda_with_fused_gate`、`fused_kda_gate`、`fused_recurrent_kda`。
- `tests/kernels/test_kda.py` 存在 KDA kernel precision test。

## 限制

- 该来源证明 v0.25.1 中存在模型入口和 KDA 实现路径，不等于本仓已完成端到端 serving 或性能复现。
- v0.25.1 的 KDA path 与 v0.11.1、后续 main snapshot 均存在路径差异；版本敏感段落必须标注 tag/commit。
- 仍需核查 v0.25.1 的安装依赖、GPU/TP 要求、Kimi Linear HF config 和实际 benchmark。

Owner:
Open questions: v0.25.1 smoke test、serving benchmark、与 v0.11.1/后续 main 的行为差异。
Handoff: efficient-long-context-attention topic。