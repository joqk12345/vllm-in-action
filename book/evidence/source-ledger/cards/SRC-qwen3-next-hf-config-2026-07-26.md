---
source_id: SRC-qwen3-next-hf-config-2026-07-26
status: captured
evidence_grade: A
source_type: model-config
title: "Qwen/Qwen3-Next-80B-A3B-Instruct Hugging Face config.json"
author_or_issuer: "Qwen / Hugging Face model repository"
published: null
verified: 2026-07-26
applies_to: "Downloaded config.json for Qwen/Qwen3-Next-80B-A3B-Instruct; SHA256 2d483c7cabad7c8704478ed4038fa7e7b2eff840bc00a118eccbe38e2b488303"
url: "https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/resolve/main/config.json"
archive_path: "research/topics/efficient-long-context-attention/source/configs/2026-07-26-qwen3-next-80b-a3b-instruct-config.json"
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

Qwen3-Next-80B-A3B-Instruct 的 Hugging Face `config.json`。用于核查 Qwen3-Next/Qwen3.5 GDN/Gated Delta Networks serving 路径中的 layer type、full attention interval 和 linear attention 参数。

## 支撑的结论

- `architectures`: `Qwen3NextForCausalLM`。
- `model_type`: `qwen3_next`。
- `num_hidden_layers`: 48。
- `max_position_embeddings`: 262144。
- `full_attention_interval`: 4。
- 未显式提供 `layer_types` 时，vLLM `Qwen3NextConfig` 默认每 4 层一个 `full_attention`，其余为 `linear_attention`。
- 线性注意力相关参数包括 `linear_conv_kernel_dim=4`、`linear_key_head_dim=128`、`linear_value_head_dim=128`、`linear_num_key_heads=16`、`linear_num_value_heads=32`。

## 限制

- 该 config 来自 HF `main` 分支下载快照，尚未固定 HF revision commit。
- Config 证明模型结构参数，不证明 vLLM 可启动、kernel 可用或性能可复现。
- “Qwen3.5 GDN” 的命名需回到 Qwen 官方文档/模型卡进一步核查；本卡当前固定的是 Qwen3-Next Instruct config。

Owner:
Open questions: 固定 HF revision、Qwen3.5 对应模型 config、vLLM v0.25.1 smoke test、GDN backend 选择。
Handoff: efficient-long-context-attention topic。