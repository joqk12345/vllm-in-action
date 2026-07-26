# llm-d agentic serving 正文落点建议

Owner:
Purpose: 将 `research/topics/llm-d-agentic-serving` 的研究内容映射到《vLLM 工程实践》章节结构，明确可进入正文的稳定概念、只能作为线索的内容和进入正文前的证据门禁。
Status: captured
Applies to: vLLM Office Hours #53；llm-d/vLLM/InferenceX 状态尚未固定 release/commit
Evidence grade: C/D 起步；本文件是章节规划，不是正文事实来源
Verified date: 2026-07-26
Assumptions: 当前主题材料主要来自公开分享 PDF 与自动字幕；工程行为必须回到 llm-d/vLLM 上游或本仓实验。
Open questions: 是否将 agentic serving 明确提升为第 16 章端到端 playbook 的主案例之一。
Handoff: 第 08、10、11、12、13、14、15、16 章

## 1. 总体判断

`llm-d-agentic-serving` 不应作为单点 “Wide EP” 内容进入正文，而应作为 **从单机 vLLM engine 走向 Kubernetes 集群级推理系统** 的综合案例。

稳定主线是：

```text
agentic long-context workload
  → prefix-aware routing
  → KV cache tiering / global state
  → prefill/decode disaggregation
  → Wide EP / DP attention for MoE/MLA models
  → flow control / priority / batch
  → SLO-aware capacity and rollback
```

主落点建议：

- **第 12 章：吞吐、利用率与单位成本** — 作为核心案例，解释为什么 agentic serving 不能只看 token/s。
- **第 15 章：升级、回滚与故障诊断** — 作为部署边界、版本一致性和回退案例。

辅助落点：第 08、10、11、13、14、16 章。

## 2. 章节映射表

| Topic 内容 | 推荐章节 | 放置方式 | 相关 claim |
|---|---|---|---|
| Agentic workload：长上下文、多轮复用、长尾请求 | 第 02、09、11 章 | workload 分类、benchmark trace、TTFT 诊断前置条件 | LD-C01, LD-C07 |
| Prefix-aware routing / Intelligent Routing | 第 10、11、12 章 | 调度与延迟优化案例；从 round-robin 到推理感知路由 | LD-C01, LD-C02 |
| Load-aware balancing / predicted latency scheduling | 第 10、13 章 | 排队、背压、调度信号和观测指标 | LD-C02 |
| KV cache tiering / global KV state | 第 04、11、12、13 章 | KV 容量、TTFT、working set 和可观测性 | LD-C03 |
| Prefill/decode disaggregation | 第 10、11、12、15 章 | prefill/decode 隔离、KV transfer、部署复杂度 | LD-C04, LD-C06 |
| Wide EP / DP attention | 第 08、12 章 | 多节点并行、MoE/MLA、拓扑和 KV 内存案例 | LD-C05, LD-C06 |
| Flow control / priority / multi-tenant QoS | 第 10、13、14 章 | 过载保护、公平性、多租户隔离 | LD-C06 |
| Batch async processing | 第 10、12、14 章 | 在线/离线混跑，提高利用率但保护在线 SLO | LD-C06 |
| SLO-aware autoscaling | 第 13 章 | 扩缩容信号：队列、TTFT、ITL、GPU、KV hit | LD-C06 |
| Deployment operator boundary / gang scheduling | 第 15 章 | llm-d router 与 operator 职责边界、版本滚动 | LD-C04, LD-C06 |
| AgentX / OpenRouter 成本数字 | 第 09、12 章 | benchmark/cost 反例；不能直接作为生产结论 | LD-C07 |
| Canary / rollback | 第 15、16 章 | 逐项启用、逐项回退的生产 playbook | LD-C06 |

## 3. 每章建议落点

### 第 02 章：工作负载、SLO 与指标

建议新增或强化一个 workload 类型：**agentic long-context workload**。

可沉淀内容：

- 多轮工具调用会反复提交相同或相似上下文；
- 平均 prompt/output 长度不足以描述这类 workload；
- 需要记录 prefix reuse、turn count、context growth、tool-call loop 和长尾请求。

证据门禁：需要 AgentX/InferenceX trace 或本仓构造 trace，不能只引用 Office Hours。

### 第 04 章：显存、KV Cache 与容量边界

建议将 `LD-C03` 作为 KV cache 章节的高级扩展：KV cache 不只存在于单个 GPU 内，还可能形成 GPU/CPU/NVMe/remote tier。

可沉淀内容：

- working set 概念；
- tier hit 与 recompute 的成本比较；
- global KV state 为什么会影响 routing。

证据门禁：固定 vLLM KV offload/tiering 实现和测试。

### 第 08 章：并行策略与硬件拓扑

建议放置 Wide EP / DP attention 的概念边界，而不是完整 llm-d 系统。

可沉淀内容：

- TP 在多节点上的 dense all-reduce 反例；
- MLA single latent KV vector 在 TP 下的 KV 复制问题；
- Wide EP / DP attention 只适合特定 MoE/MLA + 高速互联场景。

证据门禁：固定 vLLM Wide EP/DP attention PR、测试和目标模型。

### 第 09 章：构建可信 Benchmark

建议把 AgentX/OpenRouter 数字作为“不能直接引用的 benchmark 线索”案例。

可沉淀内容：

- agentic benchmark 必须记录 trace、turn count、prefix reuse、arrival model、并发、硬件和成本假设；
- 第三方 endpoint 成本对比必须注明利用率、价格口径和 SLO。

证据门禁：固定 InferenceX/AgentX commit 与配置，或建立本仓替代 workload。

### 第 10 章：调度、批处理与排队

建议作为 Intelligent Routing、flow control 和 batch async processor 的主要机制落点。

可沉淀内容：

- 集群入口调度也是 LLM serving 的一部分；
- prefix affinity 与 load-aware balancing 的冲突；
- flow control 如何保护在线请求；
- 低优先级 batch 如何填充空闲资源。

证据门禁：核查 llm-d EPP/router、flow control、batch processor 的源码和配置。

### 第 11 章：优化 TTFT 与 ITL

建议将 prefix-aware routing、KV tiering、PD 作为 TTFT/ITL 优化案例。

可沉淀内容：

- prefix hit 可降低重复 prefill；
- PD 可避免长 prefill 干扰 decode；
- prefix hit rate 高但 p99 latency 变差是重要反例。

证据门禁：本仓至少跑 round-robin vs prefix-aware routing 或等价 trace 实验。

### 第 12 章：吞吐、利用率与单位成本

建议作为本 topic 的 **主落点**。

可沉淀内容：

- `TPS/user` 与 `TPS/GPU` 的张力；
- 高利用率不等于业务有效吞吐；
- Wide EP、PD、KV tiering、routing 必须分层 ablation；
- 成本模型必须记录 GPU 单价、利用率、SLO、trace 和 tokens 口径。

建议案例框：

> 案例：为什么 agentic long-context serving 不能只看 token/s？

证据门禁：完成 AgentX-like benchmark 或本仓替代 workload，并记录所有成本假设。

### 第 13 章：可观测性与容量规划

建议将 llm-d topic 转化为指标树。

可沉淀指标：

- prefix cache hit rate；
- KV tier hit rate；
- prefill/decode backlog；
- queue length；
- saturation detector；
- TPS/user、TPS/GPU；
- GPU 利用率和网络利用率。

证据门禁：固定 llm-d/vLLM metrics 名称和暴露方式。

### 第 14 章：可靠性、隔离与安全

建议只放多租户和隔离相关内容，不展开 Wide EP 细节。

可沉淀内容：

- priority queue 与 paid/free tenant；
- batch 不得饿死 online；
- 超长请求和 KV cache 污染；
- 过载时降级和限流。

证据门禁：核查 flow control、priority、batch 的配置与失败行为。

### 第 15 章：升级、回滚与故障诊断

建议作为本 topic 的 **第二主落点**。

可沉淀内容：

- llm-d router 不是 deployment operator；
- gang scheduling/co-scheduling 可能来自 LeaderWorkerSet、Grove 或其他 operator；
- PD prefill/decode pods 必须避免版本不一致；
- KV transfer、router stale state、network 失败都要有回退。

证据门禁：核查 deployment examples、operator 文档、PD rollout 约束和失败恢复。

### 第 16 章：端到端生产 Playbook

建议作为一个可选端到端案例，而非现在就写入主线。

Playbook 草案：

```text
1. 定义 agentic trace 与 SLO
2. 跑普通 vLLM Service / round-robin baseline
3. 启用 prefix-aware routing
4. 加入 load-aware scoring
5. 评估 KV tiering
6. 评估 PD disaggregation
7. 评估 Wide EP / DP attention
8. 加入 flow control 与 batch
9. 建 canary 与 rollback
10. 形成成本模型
```

## 4. 可进入正文的稳定概念

当前可作为“研究框架”进入章节 brief 或 handoff，但不能作为已验证事实：

- agentic workload 需要记录 prefix reuse，而不只是平均长度；
- 集群级 routing 会影响 prefix cache hit rate 和 TTFT；
- KV cache 的 working set 可跨 GPU/CPU/storage tier 分析；
- PD 与 Wide EP 是不同层面的优化，不能混写；
- 成本模型必须同时约束 SLO 和利用率；
- deployment operator 能力不能误写成 llm-d router 能力。

## 5. 只能作为线索的内容

以下内容不得直接进入正文事实段：

- H200/GLM5.2/AgentX/OpenRouter 成本和性能数字；
- 90%+ prefix cache reuse 等口头数字；
- llm-d 与 vLLM production stack 的关系判断；
- gang scheduling 是否由 llm-d 支持；
- Wide EP 是大模型多节点服务最佳方案；
- AgentX 代表所有 agentic workloads。

## 6. 证据门禁

进入正文前至少需要：

1. 固定 llm-d commit/release；
2. 固定 vLLM release/tag/commit；
3. 固定 InferenceX/AgentX commit 或本仓替代 trace；
4. 为 router、KV tiering、PD、Wide EP、flow control、batch 各找到源码/测试/文档锚点；
5. 至少完成以下实验之一：
   - round-robin vs prefix-aware routing；
   - PD on/off；
   - Wide EP vs TP；
   - KV tiering on/off；
   - online + batch 混跑；
6. 记录硬件拓扑：GPU、节点、NVLink/NVL、InfiniBand、UCX/NIXL；
7. 记录 SLO：TTFT、ITL、TPS/user、TPS/GPU、goodput 和成本口径。

## 7. 对全书目录的影响建议

当前 16 章结构总体不需要大改，但建议微调章节副主题和案例安排。

### 建议 1：第 10 章标题或章节承诺补充“集群入口调度”

当前第 10 章强调调度、批处理与排队，但容易被理解为 vLLM engine 内部 scheduler。llm-d topic 显示还需要覆盖 **router-level scheduling**。

建议在第 10 章 brief 后续补充：

```text
- 集群入口路由：prefix-aware routing、load-aware balancing、priority 和 flow control。
```

### 建议 2：第 12 章增加一个“agentic serving 成本案例”

不建议新增章节，但建议第 12 章设置案例框：

```text
案例：agentic long-context serving 下，为什么 TPS/GPU、TPS/user 和 $/M tokens 必须一起看？
```

### 建议 3：第 13 章增加“推理感知扩缩容信号”

第 13 章已有可观测性与容量规划，应补充：

```text
prefix cache hit rate、KV tier hit rate、prefill/decode backlog、queue saturation、TPS/user。
```

### 建议 4：第 15 章保留 deployment boundary 主题

第 15 章应明确：

```text
serving router、engine、Kubernetes operator、gateway、deployment controller 是不同故障域。
```

这可防止把 gang scheduling、版本滚动和 llm-d router 混成一个能力。

### 建议 5：第 16 章可把 agentic serving 作为候选 playbook

如果后续本仓能复现实验，`llm-d-agentic-serving` 很适合作为第 16 章的端到端案例之一。但当前不建议调整 `spine.yml` 或新增章节。

## 8. 当前不建议调整的内容

- 不建议新增 “llm-d” 独立章节；它更适合贯穿性能工程与生产系统章节。
- 不建议把第 08 章改成大模型并行专章；Wide EP 只作为 MoE/MLA 多节点案例。
- 不建议在第 04 章展开集群级 KV 全貌；第 04 章只讲容量模型，第 12/13 章再讲集群 working set 和观测。
- 不建议在正文中提前引入 Office Hours 的成本数字。

## 9. 下一步

- 为本 topic 建立 chapter-specific TODO：第 10、12、13、15 章优先。
- 固定 llm-d/vLLM/InferenceX 上游版本后刷新 capability matrix。
- 设计 AgentX-like benchmark manifest。
- 根据实验证据决定是否将第 16 章 playbook 设为 agentic serving 案例。
