# 第 3 章 vLLM 的请求生命周期

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

本章以当前 V1 源码为地图。稳定概念是“前端—核心—执行器—worker”，具体类和默认值会演进。

## 3.1 进程与职责

`vllm serve` 进入 CLI 与 OpenAI-compatible server。API 进程完成鉴权/协议、renderer、tokenization、多模态下载与流式响应；它经 ZMQ 与 EngineCore 通信。`vllm/v1/engine/core.py::EngineCore` 初始化 executor、分析可用显存、建立 KV 配置与 scheduler。一个数据并行 rank 通常拥有一个 EngineCore；worker 加载该 rank 所需权重并执行 forward。

这种拆分避免 Python HTTP 路径直接阻塞 GPU 内循环，也意味着容量规划不能只给 GPU：tokenizer、媒体加载、detokenizer 和序列化同样消耗 CPU 与内存。

## 3.2 请求状态机

```text
HTTP body
  -> render/validate/tokenize
  -> EngineCoreRequest
  -> WAITING -> RUNNING -> FINISHED
                 |  ^
                 v  |
              PREEMPTED
```

scheduler 维护 `waiting`、`skipped_waiting`、`running` 和 finished IDs。一次 step 不是“选若干请求”，而是在 token budget、KV block、encoder budget、grammar/speculative 状态和远端 KV 依赖下，为每个请求决定本轮 token 数。输出更新请求已计算 token、采样结果和停止条件，然后释放或缓存 blocks。

## 3.3 初始化为何先 profile

模型权重、临时 activation、通信 buffer、编译与 graph 占用显存后，余量才能给 KV cache。EngineCore 调 worker profile，再由 `generate_scheduler_kv_cache_config` 等逻辑生成物理配置。故 `gpu_memory_utilization` 不是“KV 占显存百分比”的简单同义词；模型、运行时和缓存共享设备预算。

如果启动 OOM，应按阶段判断：权重加载 OOM、profile 峰值、KV 分配还是 graph capture，而不是盲目降低最大长度。

## 3.4 一次迭代

SchedulerOutput 把新请求、cached request 更新、每请求 scheduled tokens、block IDs、encoder 输入、grammar 和 connector metadata 交给 model runner。runner 组织扁平 token batch、position、slot mapping，选择 eager/compiled/graph 路径，执行模型和 sampler。EngineCore 再调用 scheduler 的 output update，产生 EngineCoreOutputs 发回前端。

关键点：连续批处理允许每轮成员变化。decode 请求通常每轮推进一个或少量 token，prefill 可被切块后与 decode 同轮执行。公平性和设备效率因此都由“每轮 token 预算”连接起来。

## 3.5 配置如何穿透

`VllmConfig` 聚合 model、cache、parallel、scheduler、compilation、speculative 等配置，传过各层；模型构造签名以 `vllm_config` 和 `prefix` 统一。权重在模型初始化时即按 TP/量化布局创建，避免先在每 rank 装入完整大模型再切分。

排查一个 flag 时，推荐使用代码考古链：

```text
CLI EngineArgs -> config dataclass/validator -> consumer
-> tests -> docs/release note
```

只读 help 不足以理解交互与约束。

## 3.6 三条关键旁路

- **结构化输出**：grammar 编译与掩码会改变请求何时可调度，并非仅后处理；
- **多模态**：encoder 输入有独立 compute/cache budget，媒体加载也可能成为前端瓶颈；
- **KV connector**：远端 load/save 让请求出现等待依赖，失败策略可能选择重算。

## 3.7 源码阅读路线

先读 `vllm/v1/engine/async_llm.py` 与 `core.py`，再读 `core/sched/scheduler.py`、`core/kv_cache_manager.py`、`worker/gpu_model_runner.py`，最后下钻 `attention/`、`model_executor/layers/` 和 `csrc/`。每层回答一个问题：谁拥有状态、谁作决策、谁搬数据、谁真正计算。

> **诊断法**：一次请求慢，先把时间归属到前端、排队、执行或回传；只有执行慢才立即下钻 kernel。
