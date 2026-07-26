---
source_id: SRC-vllm-qwen3-next-gdn-support-v0-25-1
status: captured
evidence_grade: A
source_type: source-code
title: "vLLM v0.25.1 Qwen3-Next/Qwen3.5 GDN support path"
author_or_issuer: "vllm-project/vllm"
published: 2026-07-12
verified: 2026-07-26
applies_to: "vLLM tag v0.25.1 commit 752a3a504485790a2e8491cacbb35c137339ad34; Qwen3NextForCausalLM and Qwen GatedDeltaNetAttention path"
url: "https://github.com/vllm-project/vllm/tree/v0.25.1"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

vLLM `v0.25.1` 中的 Qwen3-Next/Qwen3.5 GDN support path。`qwen_gdn_linear_attn.py` 文件注释为 “Inference-only Qwen3-Next/Qwen3.5 model”。

## 支撑的结论

- `docs/models/supported_models.md` 列出 `Qwen3NextForCausalLM`，示例模型包括 `Qwen/Qwen3-Next-80B-A3B-Instruct`。
- `docs/models/supported_models.md` 也列出 Qwen3.5 相关 multimodal classes，例如 `Qwen3_5ForConditionalGeneration` 和 `Qwen3_5MoeForConditionalGeneration`。
- `vllm/model_executor/models/qwen3_next.py` 根据 `layer_type` 选择 `QwenGatedDeltaNetAttention` 或 `Qwen3NextAttention`。
- `vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py` 定义 Qwen GDN path，并使用 FLA ops：`chunk_gated_delta_rule`、`fused_recurrent_gated_delta_rule_packed_decode`、`fused_sigmoid_gating_delta_rule_update` 等。
- `vllm/transformers_utils/configs/qwen3_next.py` 在未显式提供 `layer_types` 时默认每 4 层一个 `full_attention`，其他层为 `linear_attention`。

## 限制

- 该来源证明 v0.25.1 中存在 Qwen3-Next/GDN 实现路径，不等于本仓已完成端到端 serving 或性能复现。
- “Qwen3.5 GDN” 的具体模型/配置需要结合 Qwen 官方模型卡或 HF config 固定，不应只凭 vLLM 文件注释泛化。
- backend 选择、CUDA/ROCm/CUTLASS/Triton 可用性和性能需实验验证。

Owner:
Open questions: Qwen3.5 具体 config、GDN prefill backend、vLLM smoke test、state memory 和 long-context benchmark。
Handoff: efficient-long-context-attention topic。