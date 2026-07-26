---
title: "llm-d agentic serving 最小系统词汇"
status: working
topic: llm-d-agentic-serving
created: 2026-07-26
verified: 2026-07-26
applies_to: "llm-d、vLLM、agentic workloads、Wide EP、PD disaggregation、KV cache routing"
source_ids:
  - SRC-vllm-office-hours-53-llm-d
chapters: ["11", "12", "15"]
---

# llm-d agentic serving 最小系统词汇

Purpose: 用统一 nouns/verbs 描述 llm-d 在 agentic long-context workload 下的路由、缓存、并行和生产调度问题。
Evidence grade: C/D 起步
Assumptions: 字幕中的 `VLM` 多数按 `vLLM` 理解；`LMD/LLMD` 按 `llm-d` 理解；`EP/EPP` 需回查上游准确命名。
Open questions: 固定 llm-d/vLLM release 后，将概念映射到具体 CRD、gateway API、endpoint picker、router、vLLM flags 和 metrics。
Handoff: 第 11、12、15 章。

## 核心 nouns

| Noun | 中文 | 含义 | 关键 verbs |
|---|---|---|---|
| Agentic workload | 智能体工作负载 | 长上下文、多轮工具调用、重复发送上下文的请求集合 | trace, replay, segment |
| Prefix cache | 前缀缓存 | vLLM 复用已计算 prompt/prefix KV 的机制 | hit, miss, reuse |
| Prefix affinity | 前缀亲和 | 将请求路由到已有对应 prefix/KV 的 pod/rank | route, score, target |
| Endpoint picker / EPP | 端点选择器 | llm-d router 中承载 LLM serving 逻辑的组件 | pick, filter, score |
| llm-d router | llm-d 路由层 | proxy + endpoint picker 等组成的推理感知入口 | route, balance, queue |
| KV cache tier | KV 缓存层级 | GPU、CPU、NVMe、远程存储等不同位置的 KV 状态 | offload, fetch, tier |
| PD disaggregation | prefill/decode 分离 | 将 prefill 和 decode 放在不同 worker/replica 执行 | split, transfer, compose |
| KV transfer | KV 传输 | prefill pod 到 decode pod 或不同 tier 间移动 KV | push, pull, recover |
| Wide EP | 宽专家并行 | 单个逻辑 vLLM replica 横跨多个 pod/node 的 expert parallelism | shard, dispatch, combine |
| DP attention | 数据并行注意力 | 每个 rank 运行逻辑 attention 并管理 KV，专家层做稀疏通信 | attend, dispatch, combine |
| MLA | 多头潜在注意力 | DeepSeek/GLM-like 模型中单 latent KV vector 的注意力结构 | compress, cache, replicate |
| Flow control | 流控 | 饱和检测、排队、优先级和 QoS 调度 | detect, queue, prioritize |
| Batch workload | 离线批任务 | eval、background agent、RL jobs 等低优先级请求 | submit, throttle, drain |

## 核心 verbs

| Verb | 中文 | 主语 | 宾语或结果 |
|---|---|---|---|
| `route` | 路由 | Endpoint picker | pod、rank、prefill/decode worker |
| `score` | 打分 | Router/scorer | prefix hit、load、predicted latency |
| `hit/miss` | 命中/未命中 | Prefix cache | cached prefix/KV |
| `offload` | 卸载 | vLLM/KV manager | GPU KV 到 CPU/NVMe/remote tier |
| `transfer` | 传输 | KV connector | prefill KV 到 decode worker |
| `disaggregate` | 分离 | Serving system | prefill 与 decode 阶段 |
| `dispatch` | 分发 | EP router / MoE router | token 或 expert 请求 |
| `combine` | 合并 | Expert parallel runtime | expert 输出 |
| `queue` | 排队 | Flow control | 低优先级或过载请求 |
| `prioritize` | 优先处理 | Router/flow control | 高 QoS tenant 或在线请求 |
| `profile` | 刻画 | Benchmark | latency/throughput/cost 曲线 |
| `fallback` | 回退 | Operator/system | 普通 vLLM service 或关闭 PD/Wide EP |

## 最小处理语法

```text
Agentic trace repeats long prefixes
  → router scores prefix affinity and load
  → request targets pod/rank with useful KV state
  → prefill/decode may be split and KV transferred
  → Wide EP/DP attention changes communication and KV memory layout
  → flow control protects online SLO
  → benchmark measures hit rate, TTFT, ITL, TPS/user, TPS/GPU and cost
```

## 容易混淆的区别

### Prefix hit rate 与端到端收益

Prefix hit rate 高通常有利于 TTFT 和成本，但如果路由造成热点、队列或错误 tier 读取，端到端 latency 仍可能变差。

### PD disaggregation 与 Wide EP

PD 分离的是 inference phases；Wide EP 分离的是模型专家/并行拓扑。二者可以组合，但解决的问题不同。

### Tensor parallelism 与 DP attention + Wide EP

TP 常依赖每层 dense all-reduce；DP attention + Wide EP 试图让 attention/KV 管理和专家稀疏通信更适合多节点 MoE/MLA 模型。该判断必须绑定模型结构和网络条件。

### 演讲数字与生产成本

Office Hours 中的 H200、OpenRouter、AgentX 数字只能作为 benchmark 线索。生产成本必须记录 GPU 单价、利用率、并发、请求分布和 SLO。