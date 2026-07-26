# vLLM v0.25.1 Kimi Linear smoke test plan

Owner:
Purpose: 为 Kimi Linear 在 vLLM `v0.25.1` 上的最小验证设计 smoke test，先验证支持路径和状态形状，再进入端到端 serving benchmark。
Status: drafted
Applies to: vLLM `v0.25.1` (`752a3a504485790a2e8491cacbb35c137339ad34`), `moonshotai/Kimi-Linear-48B-A3B-Instruct` config captured 2026-07-26
Evidence grade: Plan; supporting facts from A-grade source/config cards; no local GPU run yet.
Verified date: 2026-07-26
Assumptions: 当前环境不一定具备 4×GPU 或足够显存；先设计分层验证，避免把未跑通的命令写成结果。
Open questions: HF revision、vLLM wheel/build matrix、GPU/TP 最小配置、`mamba_cache_dtype` 对 state memory 的影响。
Handoff: 第 11/12/15 章；benchmark 记录目录。

## 1. 固定基线

| 项 | 值 |
|---|---|
| vLLM tag | `v0.25.1` |
| vLLM commit | `752a3a504485790a2e8491cacbb35c137339ad34` |
| Model config | `source/configs/2026-07-26-kimi-linear-48b-a3b-instruct-config.json` |
| Config SHA256 | `a6ac3c2c4b5aa72370f9727f49ffa4432715d20061889acdb37c688be853096e` |
| Model class | `KimiLinearForCausalLM` |
| Model type | `kimi_linear` |

## 2. HF config observations

Downloaded config shows:

- `num_hidden_layers`: 27
- `linear_attn_config.full_attn_layers`: `[4, 8, 12, 16, 20, 24, 27]`
- `linear_attn_config.kda_layers`: 20 KDA layers
- `head_dim`: 128
- `num_heads`: 32
- `short_conv_kernel_size`: 4
- `mla_use_nope`: true

This is exactly a 20:7 KDA:full-MLA layer split, close to the paper's 3:1 description but not identical if counted over 27 layers. Use the config as the serving truth for this checkpoint.

## 3. Expected KDA state shapes in v0.25.1

In `vllm/model_executor/layers/mamba/mamba_utils.py` at `v0.25.1`, KDA state shape is derived as:

```python
conv_dim = proj_size + 2 * proj_k_size
conv_state_shape = orient(divide(conv_dim, tp_world_size), conv_kernel_size - 1)
recurrent_state_shape = (divide(num_heads, tp_world_size), head_dim, head_dim)
```

For the captured config:

```text
proj_size = num_heads * head_dim = 32 * 128 = 4096
proj_k_size = 32 * 128 = 4096
conv_dim = 4096 + 2 * 4096 = 12288
conv_kernel_size - 1 = 3
recurrent_state_shape per sequence before TP = (32, 128, 128)
```

Examples:

| TP size | conv dim per rank | recurrent state per rank |
|---:|---:|---|
| 1 | 12288 | `(32, 128, 128)` |
| 2 | 6144 | `(16, 128, 128)` |
| 4 | 3072 | `(8, 128, 128)` |
| 8 | 1536 | `(4, 128, 128)` |

Boundary: this is static shape derivation, not measured memory. Actual memory depends on batch/sequence state allocation, dtype, scheduler, and vLLM cache implementation.

## 4. Smoke test layers

### Layer A — source/static verification

Goal: no GPU required.

Checks:

1. `KimiLinearForCausalLM` appears in `docs/models/supported_models.md`.
2. `KimiLinearForCausalLM` appears in `vllm/model_executor/models/registry.py`.
3. `kimi_linear.py` uses `config.is_kda_layer(layer_idx)`.
4. `kimi_gdn_linear_attn.py` imports and calls:
   - `chunk_kda_with_fused_gate`
   - `fused_kda_gate`
   - `fused_recurrent_kda`
5. `tests/kernels/test_kda.py` exists.

Status: completed by static source inspection; captured in source cards.

### Layer B — config-only validation

Goal: verify that the HF config maps to vLLM's expected KimiLinearConfig.

Suggested checks:

```bash
python - <<'PY'
from transformers import AutoConfig
cfg = AutoConfig.from_pretrained(
    'moonshotai/Kimi-Linear-48B-A3B-Instruct',
    trust_remote_code=True,
)
print(cfg.architectures, cfg.model_type)
print(len(cfg.linear_attn_config['kda_layers']))
print(cfg.linear_attn_config['full_attn_layers'])
PY
```

Expected:

- `KimiLinearForCausalLM`
- `kimi_linear`
- 20 KDA layers
- full attention layers `[4, 8, 12, 16, 20, 24, 27]`

Boundary: this may use Transformers remote code; record package versions and HF revision.

### Layer C — vLLM import/registry smoke test

Goal: verify vLLM package can import Kimi Linear model class without loading 48B weights.

Candidate checks after installing vLLM `v0.25.1`:

```bash
python - <<'PY'
import vllm
from vllm.model_executor.models.registry import ModelRegistry
print(vllm.__version__)
# exact API may differ; record the method used in the final experiment log
PY
```

If registry APIs are unstable, use direct imports:

```bash
python - <<'PY'
from vllm.model_executor.models.kimi_linear import KimiLinearForCausalLM
from vllm.transformers_utils.configs.kimi_linear import KimiLinearConfig
print(KimiLinearForCausalLM.__name__)
print(KimiLinearConfig.__name__)
PY
```

Boundary: import success does not prove GPU kernels are available.

### Layer D — KDA kernel precision test

Goal: run vLLM's own KDA kernel test on CUDA.

Candidate command from vLLM checkout/tag:

```bash
pytest -q tests/kernels/test_kda.py
```

Record:

- GPU model and driver;
- CUDA version;
- PyTorch version;
- vLLM build type;
- whether tests are skipped, pass, or fail;
- exact failure if missing Triton/CUDA support.

Boundary: KDA kernel precision test is not an end-to-end serving benchmark.

### Layer E — minimal serving startup

Goal: verify vLLM server can load the real checkpoint.

Candidate command, adapted from Kimi README but fixed to vLLM `v0.25.1`:

```bash
vllm serve moonshotai/Kimi-Linear-48B-A3B-Instruct \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 1048576 \
  --trust-remote-code
```

For constrained hardware, lower `--max-model-len` for smoke test only, and clearly label it as not validating 1M context:

```bash
vllm serve moonshotai/Kimi-Linear-48B-A3B-Instruct \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 32768 \
  --trust-remote-code
```

Record whether the server reaches ready state, not just whether the command starts.

## 5. Result logging template

When actually executed, create a benchmark/experiment record with:

```text
Owner:
Purpose: Kimi Linear smoke test on vLLM v0.25.1
Status:
Applies to: vLLM v0.25.1, Kimi-Linear-48B-A3B-Instruct, fixed HF revision
Evidence grade: A if commands and raw logs are preserved
Verified date:
Hardware:
Software:
Commands:
Raw logs:
Observed result:
Failure mode:
Handoff:
```

## 6. Do not claim yet

Until Layer D/E runs, do not claim:

- vLLM `v0.25.1` can serve Kimi Linear in this environment;
- 1M context works locally;
- TP=4 is sufficient or optimal;
- paper-reported 6× throughput or 75% KV reduction is reproduced;
- KDA is production-ready for all vLLM workloads.
