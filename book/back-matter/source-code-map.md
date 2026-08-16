# 附录 A：源码研究地图

以问题驱动阅读，避免从仓库第一行顺序读。

| 问题 | 第一站 | 第二站 | 验证 |
|---|---|---|---|
| 请求如何进入引擎 | `vllm/entrypoints/openai/` | `vllm/v1/engine/async_llm.py` | `tests/entrypoints/` |
| step 如何推进 | `vllm/v1/engine/core.py` | `vllm/v1/core/sched/scheduler.py` | `tests/v1/core/` |
| blocks 如何分配 | `kv_cache_manager.py` | `kv_cache_coordinator.py`, `block_pool.py` | KV cache tests |
| backend 如何选择 | `attention/selector.py` | `attention/backends/registry.py` | attention tests |
| GPU batch 如何构造 | `worker/gpu_model_runner.py` | `model_runner/` | model runner tests |
| 模型如何注册/加载 | `model_executor/models/registry.py` | model implementation/loader | model tests |
| TP/EP 如何通信 | `distributed/` | `model_executor/layers/` | distributed tests |
| compile/graph 如何覆盖 | `compilation/` | `v1/cudagraph_dispatcher.py` | compile tests |
| API 指标从何而来 | `v1/metrics/` | entrypoint metrics | metrics tests |

## A.1 五层新模型检查法

1. **语义层**：HF config 映射到哪个 model class，attention/SSM 层序列是什么？
2. **状态层**：每层返回何种 `KVCacheSpec`，state 大小、block 与 sharing 如何定义？
3. **控制层**：scheduler 能否分配、抢占、prefix cache、speculate？
4. **backend 层**：metadata builder 和 selector 是否覆盖 dtype/head/platform？
5. **kernel 层**：prefill/decode、quant、graph、distributed shape 是否都有实现？

## A.2 追一个配置

从 CLI 搜 option string，进入 EngineArgs 到 config dataclass，读 validator/hash，再找所有字段 consumer 和 tests。最后查看 release note/PR。若只找到定义而没有 consumer，它可能是兼容字段或未完成路径。

## A.3 追一次性能回归

先 `git bisect` 或 A/B tag 确认版本边界；比较 resolved config/backend；用 engine stats 区分 queue/cache/compute；最后采短 profiler。代码 diff 只能提出假设，不能代替运行证据。