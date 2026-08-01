---
source_id: SRC-kimi-linear-hf-config-2026-07-26
status: captured
evidence_grade: A
source_type: model-config
title: "moonshotai/Kimi-Linear-48B-A3B-Instruct Hugging Face config.json"
author_or_issuer: "Moonshot AI / Hugging Face model repository"
published: null
verified: 2026-07-26
applies_to: "Downloaded config.json for moonshotai/Kimi-Linear-48B-A3B-Instruct; SHA256 a6ac3c2c4b5aa72370f9727f49ffa4432715d20061889acdb37c688be853096e"
url: "https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct/resolve/main/config.json"
archive_path: "research/topics/efficient-long-context-attention/source/configs/2026-07-26-kimi-linear-48b-a3b-instruct-config.json"
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

Kimi Linear Instruct checkpoint 的 Hugging Face `config.json`。用于核查 vLLM `KimiLinearConfig`、KDA/MLA 层分布和 state shape 推导。

## 支撑的结论

- `architectures`: `KimiLinearForCausalLM`。
- `model_type`: `kimi_linear`。
- `num_hidden_layers`: 27。
- `linear_attn_config.full_attn_layers`: `[4, 8, 12, 16, 20, 24, 27]`。
- `linear_attn_config.kda_layers`: 20 个 KDA 层，包含 `[1, 2, 3, 5, 6, 7, ...]`。
- `linear_attn_config.head_dim`: 128。
- `linear_attn_config.num_heads`: 32。
- `linear_attn_config.short_conv_kernel_size`: 4。
- `mla_use_nope`: true。

## 限制

- 该 config 来自 HF `main` 分支下载快照，尚未固定 HF revision commit。
- Config 证明模型结构参数，不证明权重可下载、vLLM 可启动或性能可复现。

Owner:
Open questions: 固定 HF repository revision、tokenizer/chat template、权重文件和 vLLM v0.26.0 实际加载行为。
Handoff: efficient-long-context-attention topic。