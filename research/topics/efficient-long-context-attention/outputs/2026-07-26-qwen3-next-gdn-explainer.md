# Qwen3-Next / Qwen3.5 GDN（Gated Delta Networks）解释分析

Owner:
Purpose: 基于 Gated DeltaNet 论文、DeltaNet 算法博客、Qwen3-Next HF config 和 vLLM v0.26.0 源码，解释 Qwen3-Next/Qwen3.5 中 GDN 路线的机制、证据边界和 serving 验证任务。
Status: captured
Applies to: Qwen3-Next/Qwen3.5 GDN research；vLLM v0.26.0；research/topics/efficient-long-context-attention
Evidence grade: B for GDN paper; A for fixed configs/source snapshots; C/D for blogs/community links.
Verified date: 2026-07-26
Assumptions: 用户称 “Qwen3.5 GDN”，当前已固定 Qwen3-Next Instruct config 和 vLLM Qwen3-Next/Qwen3.5 GDN path；Qwen3.5 具体 HF config 尚未固定。
Open questions: Qwen3.5 官方模型卡/config、GDN prefill backend、实际 vLLM serving benchmark。
Handoff: `claims.yml`、第 09/11/12/15 章。

## 1. 来源和证据等级

| 来源 | 等级 | 用途 |
|---|---:|---|
| Gated DeltaNet paper `arXiv:2412.06464v3` | B | GDN 机制、chunkwise parallel algorithm、hybrid GDN 架构 |
| DeltaNet Explained Part II | C | DeltaNet chunkwise/WY 算法的教学解释 |
| Qwen3-Next HF config | A | checkpoint 的层数、full-attention interval、linear attention 参数 |
| vLLM v0.26.0 source | A | Qwen3-Next/Qwen3.5 GDN serving path |
| Zhihu link | D | 当前未抓到正文，只作发现线索 |

## 2. GDN 解决什么问题？

GDN 可以理解为把两种记忆操作合并到同一个线性/RNN-style token mixer：

1. **gating / forgetting**：像 Mamba2 一样，用 data-dependent gate 控制状态衰减，能快速遗忘或清空旧信息；
2. **delta rule**：像 DeltaNet 一样，用 delta update 定向修改 key-value association，适合更精确地替换或更新某个记忆项。

Gated DeltaNet 论文的核心判断是：

- 只有 gating：容易把所有历史关联一起衰减，缺少针对性；
- 只有 delta rule：能做定向更新，但缺少快速清空旧上下文的能力；
- gated delta rule：同时具备自适应遗忘和定向更新。

## 3. 为什么 GDN 与硬件效率相关？

原始 DeltaNet 如果按纯 RNN 递推，会有 O(L) sequential steps，不适合 GPU 训练。DeltaNet Explained Part II 和 GDN 论文都强调需要把 recurrence 改写为 chunkwise / matrix multiplication form：

```text
sequence recurrence
  → chunkwise parallel form
  → matmul / tensor-core-friendly computation
```

GDN 论文在 DeltaNet chunkwise algorithm 基础上加入 gating terms，使 gated delta rule 仍可硬件友好训练。

对 serving 来说，仍需区分：

- prefill/training：通常依赖 chunk/parallel path；
- decode：通常依赖 recurrent/state update path；
- 真正性能取决于 vLLM kernel/backend、state layout、batching 和硬件。

## 4. Qwen3-Next config 中的结构

已捕获 `Qwen/Qwen3-Next-80B-A3B-Instruct` config：

- `architectures`: `Qwen3NextForCausalLM`
- `model_type`: `qwen3_next`
- `num_hidden_layers`: 48
- `max_position_embeddings`: 262144
- `full_attention_interval`: 4
- `linear_conv_kernel_dim`: 4
- `linear_key_head_dim`: 128
- `linear_value_head_dim`: 128
- `linear_num_key_heads`: 16
- `linear_num_value_heads`: 32

vLLM `Qwen3NextConfig` 在未显式提供 `layer_types` 时默认：

```python
"linear_attention" if bool((i + 1) % 4) else "full_attention"
```

因此对 48 层模型，默认层分布为：

- full attention 层：4, 8, 12, ..., 48，共 12 层；
- linear/GDN 层：其余 36 层；
- 也就是 3:1 的 linear/GDN : full attention 结构。

这和 Kimi Linear 的 hybrid 设计在高层形式上相似，但具体 operator、参数、state layout 和 kernel path 不同，不能混写。

## 5. vLLM v0.26.0 中的 Qwen GDN path

vLLM `v0.26.0` 静态核查到：

- `docs/models/supported_models.md` 列出 `Qwen3NextForCausalLM`；
- `vllm/model_executor/models/qwen3_next.py` 根据 `layer_type` 选择：
  - `QwenGatedDeltaNetAttention`，或
  - `Qwen3NextAttention`；
- `vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn.py` 文件注释为 “Inference-only Qwen3-Next/Qwen3.5 model”；
- 该文件使用 FLA ops：
  - `chunk_gated_delta_rule`；
  - `fused_recurrent_gated_delta_rule_packed_decode`；
  - `fused_sigmoid_gating_delta_rule_update`。

边界：这证明 vLLM v0.26.0 存在 Qwen3-Next/GDN 支持路径，但不证明本仓硬件上已经跑通。

## 6. 与 Kimi Linear/KDA 的关系

可以把关系整理为：

```text
DeltaNet / delta rule
  → Gated DeltaNet / GDN: delta rule + gate
    → Qwen3-Next/Qwen3.5 GDN path in vLLM
    → Kimi Linear/KDA: extends GDN with finer-grained/channel-wise gating and KDA-specific kernel design
```

Kimi Linear 论文明确说 KDA extends Gated DeltaNet with finer-grained gating。也就是说，GDN 是理解 KDA 的直接前置概念之一。

## 7. 与 MiniMax-M2 反例的关系

GDN/Qwen 与 MiniMax-M2 形成一个很好的对照：

- Qwen3-Next/Kimi Linear：继续探索 hybrid GDN/KDA + full attention；
- MiniMax-M2：作者报告回到 full attention + GQA，因为其生产设置中 efficient attention 质量/基础设施风险仍高。

这说明章节中应避免写单一路线胜利，而应写：

> Efficient attention 正在分化为多个工程分支；是否可用取决于模型训练、任务分布、长上下文质量、kernel/backend、prefix/cache 支持和 serving 实测。

## 8. 后续验证任务

1. 固定 Qwen3.5 具体 HF config，确认是否与 Qwen3-Next 共用/继承 GDN path。
2. 基于 vLLM `v0.26.0` 设计 Qwen3-Next smoke test：registry、config、layer construction、GDN backend。
3. 核查 `--gdn-prefill-backend` 在 vLLM v0.26.0 中的可选值和默认选择。
4. 抽取 GDN 论文的核心表格：Mamba2 vs DeltaNet vs Gated DeltaNet。
5. 将 Qwen3-Next/Kimi Linear/MiniMax-M2 放入 capability matrix：operator、full-attention interval、context length、vLLM support、待复现项。
