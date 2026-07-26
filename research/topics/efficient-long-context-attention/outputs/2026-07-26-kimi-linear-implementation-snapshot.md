# Kimi Linear / KDA implementation snapshot

Owner:
Purpose: 固定 Kimi Linear 相关源码与 vLLM 支持状态，区分论文声明、模型仓库 README、KDA kernel 和 vLLM serving path。
Status: captured
Applies to: Kimi Linear / KDA；research/topics/efficient-long-context-attention
Evidence grade: A for fixed source-code commits; not yet reproduced locally.
Verified date: 2026-07-26
Assumptions: 当前只做源码/文档静态核查，未下载 HF checkpoint，未启动 vLLM。
Open questions: vLLM v0.11.1 依赖版本、GPU 支持、端到端性能；后续版本实现路径变化。
Handoff: `claims.yml`、后续 benchmark、chapter 11/12/15。

## 1. 固定来源

| Source | Commit | 用途 |
|---|---:|---|
| `MoonshotAI/Kimi-Linear` | `8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3` | README、模型链接、vLLM serve 示例 |
| `fla-org/flash-linear-attention` | `0a9b9f222e86b9a895c2447767e9b4cce6c8d530` | `fla/ops/kda` kernel/operator 实现 |
| `vllm-project/vllm` | `v0.11.1` / `439368496db48d8f992ba8c606a0c0b1eebbfa69` | 当前已观察到的首个包含 `KimiLinearForCausalLM` 支持入口的稳定 tag |
| `vllm-project/vllm` | `v0.25.1` / `752a3a504485790a2e8491cacbb35c137339ad34` | 当前应优先验证的 release 基线；包含 Kimi Linear/KDA 支持路径 |
| `vllm-project/vllm` | `1240c74c0a47473449cf0c3a9c2d87a1e159f73b` | vLLM Kimi Linear support snapshot；后续 main/research commit，路径已继续重构 |

## 2. Kimi-Linear repository snapshot

固定 commit 的 README 给出：

- Paper link；
- HF checkpoints：
  - `moonshotai/Kimi-Linear-48B-A3B-Base`
  - `moonshotai/Kimi-Linear-48B-A3B-Instruct`
- 模型参数：48B total / 3B activated；context length 1M；
- Transformers 推理依赖：`python >= 3.10`、`torch >= 2.6`、`fla-core >= 0.4.0`；
- vLLM serve 示例：

```bash
vllm serve moonshotai/Kimi-Linear-48B-A3B-Instruct \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 1048576 \
  --trust-remote-code
```

边界：README 写的是 “latest vllm”，不是固定 release。正文不能据此宣称某个 vLLM 版本支持。

## 3. FLA KDA operator snapshot

`fla/ops/kda/__init__.py` 导出：

- `chunk_kda`
- `fused_recurrent_kda`

相关文件包括：

- `chunk.py`
- `fused_recurrent.py`
- `gate.py`
- `chunk_fwd.py`
- `chunk_bwd.py`
- `backends/triton_ascend/*`

静态观察：

- `chunk.py` 包含训练/预填充相关 autograd wrapper，并注释 “Related files are modified and supported by the Moonshot AI Team”。
- `fused_recurrent.py` 包含 Triton recurrent decode kernel，并注释 “modified from the Decode kernel of the vllm gdn/kda model”。

边界：FLA 实现不等于 vLLM release 内部 vendored 实现，仍需比较 vLLM third_party 代码和依赖。

## 4. vLLM release boundary

当前已观察到的 release 边界：

- `v0.11.0`：未观察到 `KimiLinearForCausalLM` supported-models/registry 入口。
- `v0.11.1rc4`：存在 `vllm/model_executor/layers/fla/ops/kda.py`，但未观察到 `KimiLinearForCausalLM` supported-models 入口。
- `v0.11.1rc5`：已观察到 `KimiLinearForCausalLM` supported-models 入口和 Kimi Linear 模型文件。
- `v0.11.1`：稳定 tag 中保留该支持入口。commit 为 `439368496db48d8f992ba8c606a0c0b1eebbfa69`。

在 `v0.11.1` 中观察到：

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/registry.py` 注册 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/kimi_linear.py` 根据 `config.is_kda_layer(layer_idx)` 选择 `KimiDeltaAttention` 或 `KimiMLAAttention`。
- `vllm/model_executor/layers/kda.py` 存在 `KimiDeltaAttention`，并调用 `chunk_kda`、`fused_kda_gate`、`fused_recurrent_kda`。
- `vllm/model_executor/layers/fla/ops/kda.py` 存在 vendored KDA operator 实现。

## 5. Current vLLM release baseline: v0.25.1

用户提醒当前 vLLM 已到 `v0.25.1`，因此后续 smoke test 和 benchmark 不应停留在 `v0.11.1`。固定 `v0.25.1` tag commit `752a3a504485790a2e8491cacbb35c137339ad34` 中观察到：

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/registry.py` 注册 `KimiLinearForCausalLM`。
- `vllm/model_executor/models/kimi_linear.py` 存在 Kimi Linear 模型实现。
- `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` 存在 `KimiGatedDeltaNetAttention`。
- 该文件从 `vllm/model_executor/layers/fla/ops/kda.py` 引入 `chunk_kda_with_fused_gate`、`fused_kda_gate`、`fused_recurrent_kda`。
- `tests/kernels/test_kda.py` 存在 KDA kernel precision test。

## 6. vLLM support snapshot after later path refactor

固定 vLLM commit `1240c74c0a47473449cf0c3a9c2d87a1e159f73b` 中观察到：

- `docs/models/supported_models.md` 列出 `KimiLinearForCausalLM`，示例模型包括 Kimi Linear Base/Instruct。
- `vllm/model_executor/models/registry.py` 注册：`KimiLinearForCausalLM -> kimi_linear.KimiLinearForCausalLM`。
- `vllm/model_executor/models/kimi_linear.py` 中 `KimiDecoderLayer` 根据 `config.is_kda_layer(layer_idx)` 选择：
  - `KimiGatedDeltaNetAttention`，或
  - `KimiMLAAttention`。
- `vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn.py` 调用 vendored KDA ops：
  - `chunk_kda_with_fused_gate` for prefill / chunk path；
  - `fused_kda_gate`；
  - `fused_recurrent_kda` for decode / recurrent path。
- `tests/kernels/test_kda.py` 将 vLLM chunk KDA Triton operator 与 naive recurrent reference 做精度比较。

边界：

- 这是 vLLM upstream snapshot，不是 tag。
- kernel precision test 不是端到端 serving correctness/performance test。
- supported models table 说明模型类存在，不等于所有硬件、量化、并行配置都可生产使用。

## 7. 对 claims 的影响

可以把 “Kimi Linear 论文声称开源 KDA kernel 与 vLLM implementation” 细化为三层事实：

1. 论文/README 层：Kimi Team 声明 KDA kernel、checkpoint 和 vLLM deployment path。
2. Kernel 层：FLA 固定 commit 下存在 `fla/ops/kda` chunk/recurrent/gate 实现。
3. vLLM 层：vLLM 固定 commit 下存在 KimiLinearForCausalLM、Kimi GDN/KDA attention layer、vendored KDA ops 和 KDA kernel tests。

尚不能得出：

- 某个 vLLM release 已生产可用；
- `vllm serve` 在本仓硬件上可运行；
- 论文报告的 6× TPOT 或 75% KV cache 收益可复现。

## 8. 下一步

1. 基于 vLLM `v0.25.1` 建立最小启动命令和依赖清单。
2. 核查 Kimi Linear HF config 中 `linear_attn_config`、`kda_layers` 和 MLA 层分布。
3. 抽取 vLLM KDA state shape/cache dtype 逻辑，判断 KV cache 计量方式。
4. 比较 `v0.11.1`、`v0.25.1` 与后续 main snapshot 的 KDA path 重构差异。
5. 设计 smoke test：不跑 48B 全量模型时，可先用 config-only/model-loader 路径或小型 mock config 验证 registry 与 layer construction。
