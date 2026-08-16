# 参考资料与代码锚点

本版不使用浮动网页支撑版本敏感事实。核心一手材料均来自 vLLM 本地快照 `fe1c317157d4478fdc0e02096447e61305b871e9`：

- 架构总览：`docs/design/arch_overview.md`
- EngineCore：`vllm/v1/engine/core.py`
- 调度器：`vllm/v1/core/sched/scheduler.py`
- KV cache 接口：`vllm/v1/core/kv_cache_manager.py`
- 混合 KV coordinator：`vllm/v1/core/kv_cache_coordinator.py`
- KV cache 规格：`vllm/v1/kv_cache_interface.py`
- 混合缓存设计：`docs/design/hybrid_kv_cache_manager.md`
- 注意力 backend 设计：`docs/design/attention_backends.md`
- attention selector/backends：`vllm/v1/attention/`
- 分布式配置：`vllm/config/parallel.py`
- 分布式部署：`docs/serving/parallelism_scaling.md`
- torch.compile：`docs/design/torch_compile.md`
- CUDA Graph：`docs/design/cuda_graphs.md`
- 融合算子：`docs/design/fusions.md`
- 模块化 MoE kernel：`docs/design/fused_moe_modular_kernel.md`
- benchmark CLI：`vllm/benchmarks/`
- production metrics：`docs/design/metrics.md`
- OpenAI-compatible server：`docs/serving/online_serving/openai_compatible_server.md`

论文背景：Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention*；Dao et al., *FlashAttention*；Leviathan et al. 与 Chen et al. 的 speculative decoding 工作。论文解释机制，不能替代当前实现证据。

完整来源卡位于 `book/evidence/source-ledger/cards/`。专题来源与尚未达到正文证据门禁的结论位于 `research/topics/`。引用在线内容时应记录 URL、tag/commit 与捕获日期。