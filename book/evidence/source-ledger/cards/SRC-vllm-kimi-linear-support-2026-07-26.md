---
source_id: SRC-vllm-kimi-linear-support-2026-07-26
status: captured
evidence_grade: A
source_type: source-code
title: "vLLM KimiLinearForCausalLM and KDA support snapshot"
author_or_issuer: "vllm-project/vllm"
published: null
verified: 2026-07-26
applies_to: "vLLM GitHub commit 1240c74c0a47473449cf0c3a9c2d87a1e159f73b; not a release tag"
url: "https://github.com/vllm-project/vllm/tree/1240c74c0a47473449cf0c3a9c2d87a1e159f73b"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

vLLM upstream snapshot，固定 commit `1240c74c0a47473449cf0c3a9c2d87a1e159f73b`。用于研究阶段核查 Kimi Linear / KDA serving 支持。

## 支撑的结论

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`，模型示例包括 `moonshotai/Kimi-Linear-48B-A3B-Base` 和 `moonshotai/Kimi-Linear-48B-A3B-Instruct`。
- `vllm/model_executor/models/registry.py` 注册 `KimiLinearForCausalLM` 到 `kimi_linear`。
- `vllm/model_executor/models/kimi_linear.py` 中 `KimiDecoderLayer` 根据 `config.is_kda_layer(layer_idx)` 选择 `KimiGatedDeltaNetAttention` 或 `KimiMLAAttention`。
- `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` 调用 vendored KDA ops：`chunk_kda_with_fused_gate`、`fused_kda_gate`、`fused_recurrent_kda`。
- `tests/kernels/test_kda.py` 包含 vLLM KDA Triton operator 与 naive recurrent reference 的精度测试。

## 限制

- 这是研究阶段固定 commit，不是 release tag；正文或生产建议必须固定 vLLM release 或明确 commit。
- 支持矩阵中未标注 LoRA 支持；模型 serving 仍需本仓环境实际运行验证。
- KDA operator precision tests 不等于端到端 serving benchmark。

Owner:
Open questions: 首个包含 Kimi Linear 支持的 vLLM release/tag、依赖要求、GPU 支持、性能基线。
Handoff: efficient-long-context-attention topic。