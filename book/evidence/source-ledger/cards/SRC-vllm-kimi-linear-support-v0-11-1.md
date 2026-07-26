---
source_id: SRC-vllm-kimi-linear-support-v0-11-1
status: captured
evidence_grade: A
source_type: source-code
title: "vLLM v0.11.1 KimiLinearForCausalLM support"
author_or_issuer: "vllm-project/vllm"
published: 2025-11-18
verified: 2026-07-26
applies_to: "vLLM tag v0.11.1 commit 439368496db48d8f992ba8c606a0c0b1eebbfa69; first stable tag observed with KimiLinearForCausalLM in supported models"
url: "https://github.com/vllm-project/vllm/tree/v0.11.1"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

vLLM `v0.11.1` tag 中可观察到 Kimi Linear 模型支持入口。对比 `v0.11.0`、`v0.11.1rc4`、`v0.11.1rc5` 与 `v0.11.1`：

- `v0.11.0`：未观察到 `KimiLinearForCausalLM` supported-models/registry 入口。
- `v0.11.1rc4`：存在 `vllm/model_executor/layers/fla/ops/kda.py`，但未观察到 `KimiLinearForCausalLM` supported-models 入口。
- `v0.11.1rc5`：已观察到 `KimiLinearForCausalLM` supported-models 入口和 Kimi Linear 模型文件。
- `v0.11.1`：稳定 tag 中保留该支持入口。

## 支撑的结论

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`，模型示例包括 `moonshotai/Kimi-Linear-48B-A3B-Base` 和 `moonshotai/Kimi-Linear-48B-A3B-Instruct`。
- `vllm/model_executor/models/registry.py` 注册 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/kimi_linear.py` 根据 `config.is_kda_layer(layer_idx)` 在 KDA 与 MLA attention path 间选择。
- `vllm/model_executor/layers/kda.py` 存在 `KimiDeltaAttention`，并调用 `chunk_kda`、`fused_kda_gate`、`fused_recurrent_kda`。
- `vllm/model_executor/layers/fla/ops/kda.py` 存在 vendored KDA operator 实现。

## 限制

- `v0.11.1` 的实现路径与后续 main snapshot 不同；后续版本将 Kimi KDA attention 重构到 `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` 和 `vllm/third_party/flash_linear_attention/ops/kda.py` 等路径。
- 该来源证明 release tag 存在模型入口和 KDA path，不证明本仓硬件上已完成端到端 serving、质量或性能复现。
- `v0.11.1rc5` 是最早观察到的 RC；正文生产边界建议使用稳定 tag `v0.11.1`，除非专门讨论 RC。

Owner:
Open questions: `v0.11.1` 的依赖、GPU/TP 要求、Kimi Linear HF config、端到端 smoke test 和 benchmark。
Handoff: efficient-long-context-attention topic。