---
title: "llm-d 分布式推理与 Agentic Workloads"
subtitle: "主题研究小册子"
status: needs-refresh
edition: "0.1"
created: 2026-07-26
verified: 2026-08-15
topic: llm-d-agentic-serving
applies_to: "目标核对 vLLM v0.27.1；llm-d/vLLM/InferenceX 版本组合尚未固定"
source_ids:
  - SRC-vllm-office-hours-53-llm-d
  - SRC-vllm-office-hours-53-llm-d-transcript
  - SRC-llm-d-repository
  - SRC-vllm-repository
  - SRC-inferencex-agentx
chapters: ["11", "12", "15"]
---

# llm-d 分布式推理与 Agentic Workloads

Owner:
Purpose: 支持 llm-d + vLLM 在 agentic long-context workloads 下的分布式 serving 研究、研讨和章节交接。
Status: needs-refresh
Applies to: vLLM Office Hours #53；llm-d/vLLM/InferenceX 上游状态尚未固定 release/commit。
Evidence grade: C/D 起步；进入正文前必须补 A/B 级来源或本仓实验。
Verified date: 2026-08-15
Assumptions: 当前主要素材是公开分享和自动字幕；`VLM/BLM` 按 `vLLM` 理解，`LMD/LLMD` 按 `llm-d` 理解。
Open questions: router/EPP、KV tiering、PD、Wide EP/DP attention、flow control、batch 和 AgentX benchmark 的准确 release 边界。
Handoff: 第 11、12、15 章。

## 1. How to use the booklet

本小册子用于把 Office Hours 线索整理成可验证研究框架。它不是正文，也不是 llm-d/vLLM release 支持矩阵。使用时应先读 `claims.yml` 和 `vocabulary.md`，再用 `capability-matrix.yml` 跟踪动态能力状态。

规则：

- 演讲和自动字幕只用于发现问题；正文事实必须回到 llm-d/vLLM 源码、测试、PR、release 文档或本仓实验。
- 性能数字必须记录模型、硬件、网络、并发、trace、SLO 和成本假设。
- `roadmap_status`、`release_status`、`local_test_status` 必须分开维护。

## 2. Executive summary

llm-d 的核心问题不是让单个 vLLM engine 更快，而是在 Kubernetes 集群中让多个 vLLM pods 面向 LLM 请求特征协同工作。Agentic workloads 具有长上下文、多轮工具调用、重复上下文和长尾请求特征；普通 round-robin Service 不知道 prefix cache、KV cache、prefill/decode 阶段或不同 pod 的负载，因此可能反复重算 prompt 或制造热点。

当前最可靠的研究判断：

1. Agentic workload 的多轮 prefix 复用使 prefix-aware routing 成为关键优化线索。见 `LD-C01`。
2. llm-d router/EPP 的价值在于把 prefix affinity、load/backpressure 和可能的 predicted latency 结合成集群级路由决策。见 `LD-C02`。
3. Wide EP/DP attention、PD disaggregation、KV tiering 和 flow control 必须组合评估；单项能力不能保证端到端收益。见 `LD-C04`、`LD-C05`、`LD-C06`。

最危险的错误泛化：把 Office Hours 中 H200/GLM5.2/AgentX/OpenRouter 的口头数字写成“llm-d + vLLM 普遍比共享 endpoint 更便宜”。见 `LD-C07`。

下一项验证动作：固定 llm-d/vLLM commit，核查 router/EPP、KV tiering、PD、Wide EP/DP attention 的源码和测试，并建立 AgentX-like trace 的本仓 benchmark。

## 3. 共同研究问题（Shared research questions）

### Q1：为什么 agentic workloads 不能只用普通 Kubernetes Service round-robin？

需要解释长上下文、多轮复用、prefix cache hit rate、请求长尾和 pod 负载不均如何破坏普通 HTTP 负载均衡假设。

### Q2：Intelligent Routing 到底在优化什么？

需要明确 endpoint picker 如何组合 prefix affinity、load-aware balancing、filters/scorers 和 predicted latency scheduling，以及这些信号冲突时如何取舍。

### Q3：Advanced KV-Cache Management 如何改变集群 working set？

需要研究 GPU/CPU/NVMe/remote tier 的 KV 状态、全局索引、router 感知和读取/重算成本边界。

### Q4：Prefill/decode disaggregation 与 Wide EP 分别解决什么问题？

PD 分离 inference phases；Wide EP/DP attention 改变大 MoE/MLA 模型的并行拓扑和 KV 内存布局。二者可组合，但不能混为一谈。

### Q5：Operational Excellence 如何保护多租户 SLO？

需要研究 flow control、priority、saturation detection、SLO-aware autoscaling 和 batch async processor 如何避免离线任务压垮在线服务。

### Q6：Office Hours benchmark 和成本线索如何复现或降级处理？

需要固定 AgentX/InferenceX trace、GLM5.2/DeepSeek-like 模型、H200/B300、NVLink/InfiniBand、并发、TPS/user、TPS/GPU 和成本假设。

## 4. 最小概念系统（Minimal concept system）

| Noun | 定义 | 关键 verbs | 容易混淆的概念 |
|---|---|---|---|
| Agentic workload | 长上下文、多轮工具调用、上下文重复提交的请求集合 | trace, replay, segment | 不等于所有 chat workload |
| Prefix cache | 已计算 prefix 的 KV 可复用状态 | hit, miss, reuse | hit rate 不等于端到端收益 |
| Endpoint picker / EPP | 承载 LLM serving 路由逻辑的组件 | score, filter, pick | 需回查正式 API 名称 |
| llm-d router | proxy + endpoint picker 组成的推理感知入口 | route, queue, balance | 不是 deployment operator |
| KV cache tier | GPU、CPU、NVMe、remote storage 中的 KV 层级 | offload, fetch, tier | tier 命中可能比重算更慢 |
| PD disaggregation | prefill 与 decode worker 分离 | split, transfer, compose | 不是模型并行方式 |
| Wide EP | 单个逻辑 replica 横跨多个 pods/nodes 的专家并行 | shard, dispatch, combine | 不是普通 tensor parallelism |
| DP attention | 每 rank 管理 attention/KV，专家层稀疏通信 | attend, dispatch, combine | 是否适合取决于模型结构 |
| Flow control | 饱和检测、排队、优先级与 QoS | detect, queue, prioritize | 不等于简单限流 |
| Batch async processor | 异步派发低优先级离线任务的组件 | submit, throttle, drain | 不能抢占在线 SLO |

## 5. System or architecture model

### 5.1 集群级请求路径

```text
Client / Batch API
  → Gateway / llm-d router
  → endpoint picker scores prefix affinity + load + policy
  → selected vLLM pod/rank or prefill/decode worker
  → vLLM uses prefix/KV cache or computes prefill
  → optional KV transfer / offload / tier fetch
  → decode and stream output
  → metrics feed routing, flow control and autoscaling
```

### 5.2 五类能力如何组合

- **Intelligent Routing**：让请求去“最可能命中 prefix 且不过载”的 pod/rank。
- **Advanced KV-Cache Management**：扩大可复用 KV 的 working set，并让 router 知道 KV 在哪个 tier。
- **Serving Large Models**：用 PD 避免 prefill 干扰 decode，用 Wide EP/DP attention 支撑超大 MoE/MLA 模型和长 KV。
- **Operational Excellence**：用 flow control、priority 和 autoscaling 保护多租户 SLO。
- **Batch Processing**：用低优先级异步 batch 填充空闲 GPU，而不饿死在线请求。

### 5.3 Wide EP/DP attention 的系统动机

对 GLM/DeepSeek-like MLA/MoE 模型，传统 TP 在多节点上会遇到两类问题：跨节点 dense all-reduce 昂贵；MLA single latent KV vector 在 TP 下可能复制，压缩 KV cache 空间。DP attention + Wide EP 的目标是让 attention/KV 管理更适合长上下文，同时让专家层使用稀疏 dispatch/combine，减少跨节点密集通信。该判断必须绑定模型结构、硬件互联和 vLLM 实现。

## 6. 跨来源命题（Cross-source claims）

| Claim | Proposition | Evidence | Applies to | Counterexample |
|---|---|---|---|---|
| LD-C01 | Agentic workload 使 round-robin 难以稳定命中 prefix cache | Office Hours C/D 线索 | Cloud Code/AgentX-like traces | 短 prompt、低复用单轮请求 |
| LD-C02 | llm-d endpoint picker 结合 prefix affinity 与 load/backpressure | Office Hours C 线索，待 llm-d 源码核查 | llm-d router/EPP | 状态滞后或热点 pod 可抵消收益 |
| LD-C03 | KV tiering 扩大 working set 但需要 router 感知状态 | Office Hours C 线索 | GPU/CPU/NVMe/remote tier | 读取慢于重算时可能退化 |
| LD-C04 | PD 隔离 prefill/decode 但引入 KV transfer 和部署复杂度 | Office Hours C 线索 | NIXL/UCX/InfiniBand 场景 | 无高速网络或短 prompt 不划算 |
| LD-C05 | DP attention + Wide EP 旨在减少多节点 TP all-reduce 和 MLA KV 复制问题 | Office Hours C 线索 | GLM/DeepSeek-like MoE/MLA | Dense 小模型或单节点不一定需要 |
| LD-C06 | 多项优化需组合评估，单项不保证收益 | 工程判断，C 级来源 | agentic long-context serving | 某些 workload 只需 prefix routing |
| LD-C07 | 演讲性能/成本数字只能作为线索 | 自动字幕/PDF C/D | H200/GLM5.2/AgentX/OpenRouter 语境 | 不能外推所有 workload 和价格 |

## 7. 来源如何相互校正（Source correction map）

| 来源 | 最适合回答 | 不支持 | 与其他来源的关系 |
|---|---|---|---|
| Office Hours PDF | 系统能力框架、图示、benchmark 线索 | release 支持、源码行为、生产结论 | 生成 claim 和实验计划 |
| 自动字幕 | QA、术语、口头边界 | 任何正文事实 | 需人工/上游交叉核对 |
| llm-d repository | router/EPP、flow control、batch、deployment examples | vLLM engine 内部行为 | 需要固定 commit 后校正演讲线索 |
| vLLM repository | prefix cache、KV offload、PD、Wide EP、DP attention | llm-d router policy | 需要固定 release/tag 与测试 |
| InferenceX/AgentX | agentic benchmark trace 和指标 | 生产普遍收益 | 需固定 commit、trace 和硬件配置 |
| 本仓实验 | 目标 workload 的可复现收益 | 其他模型/硬件泛化 | 尚未运行，是正文门禁 |

## 8. 分歧、反例与未决问题（Disagreements, counterexamples, and open questions）

- llm-d 与 vLLM production stack 是替代、互补还是通过 Gateway API inference extension 组合，尚需上游证据。
- gang scheduling/co-scheduling 不应误写成 llm-d router 自带能力；它可能来自 LeaderWorkerSet、Grove 或其他 operator。
- Prefix cache hit rate 高不必然代表 latency/goodput 改善，因为可能引入热点或 tier fetch 成本。
- PD 需要高速网络和版本一致性；KV transfer 失败或跨版本 pod 混用是生产风险。
- Wide EP/DP attention 的收益取决于模型结构、网络拓扑和 KV 内存压力。
- AgentX/OpenRouter 数字缺少完整配置，当前不能写成成本结论。

## 9. 验证与实验（Tests and experiments）

| Test/Experiment | Hypothesis | Baseline | Metrics | Completion criteria |
|---|---|---|---|---|
| E1：round-robin vs prefix-aware routing | 多轮长上下文 trace 中 prefix-aware routing 降低 TTFT | Kubernetes Service round-robin | prefix hit rate、TTFT、ITL、TPS/GPU | 固定 llm-d/vLLM commit 和 trace |
| E2：load-aware scoring ablation | 只看 prefix 会制造热点，加入 load/backpressure 改善尾延迟 | prefix-only routing | p95/p99 latency、队列、pod load | 记录 scorer/filter 配置 |
| E3：KV tiering ablation | CPU/NVMe tier 扩大 working set 但存在读取成本 | GPU-only KV | tier hit rate、fetch time、recompute time、TTFT | 找到 tiering 收益/退化边界 |
| E4：PD disaggregation | 长 prefill 与 decode 分离改善 decode QoS | colocated prefill/decode | TTFT、ITL、KV transfer time、网络利用率 | 记录 NIXL/UCX/IB 配置 |
| E5：Wide EP vs TP | MoE/MLA 大模型上 Wide EP 改善 KV 容量和多节点扩展 | TP deployment | KV blocks、tokens/s/GPU、latency、通信时间 | 固定模型、并行配置和硬件 |
| E6：flow control + batch | 低优先级 batch 可填充空闲资源且不伤在线 SLO | 无 batch 或无 priority | online SLO、batch throughput、queue time | 在线请求无饥饿，batch 有进展 |
| E7：成本模型 | llm-d+vLLM 成本需依赖利用率和 SLO 假设 | shared endpoint 价格 | $/M tokens、utilization、TPS/user | 显式列出所有假设 |

## 10. 生产采用、canary 与 rollback（Production decision）

### 适用条件

- 多轮长上下文 agentic workload，prefix 复用率高；
- 模型足够大，prefill 和 KV cache 成本显著；
- 有高速互联支持 PD 或 Wide EP；
- 团队能运维 Kubernetes、router、metrics、KV 状态和版本滚动；
- 已建立 target-only / round-robin 基线。

### 代价与失效边界

- router 状态不准导致错误路由；
- prefix affinity 与 load balancing 冲突；
- KV tier fetch 慢于重算；
- PD KV transfer 失败或网络成为瓶颈；
- Wide EP 对不匹配模型没有收益；
- batch 抢占在线 SLO；
- deployment operator 与 llm-d/vLLM 版本不一致。

### Canary

1. 从单模型、单 trace、低流量开始。
2. 先启用 prefix-aware routing，观察 hit rate 和热点。
3. 再加入 load-aware scoring、flow control 和 batch。
4. 对 PD 和 Wide EP 分别做 A/B，而不是一次性全开。
5. 每次扩展并发都记录 SLO、队列和成本。

### Rollback

- 回退普通 vLLM Service；
- 关闭 PD，回到 colocated prefill/decode；
- 关闭 Wide EP 或回到已验证 TP/单节点配置；
- 禁止低优先级 batch；
- 清空或降级 KV tiering；
- 固定版本滚动，避免 prefill/decode pod 混用不同 vLLM 版本。

## 11. 结论分层（Layered conclusions）

### 已证实事实

当前没有 A/B 级本地验证结论。已有内容主要是 C/D 级研究线索。

### 工程判断

- llm-d 的研究价值在于集群级推理感知调度，而非替代 vLLM engine 内部优化。
- Agentic workloads 应以 trace 和 prefix reuse 分布来定义，不能用普通 prompt/output 平均长度替代。
- Wide EP、PD、KV tiering 和 routing 必须分层 ablation。

### 待验证假设

- llm-d router 能稳定提高目标 agentic trace 的 prefix hit rate 和 TTFT。
- PD 在目标网络上带来的 QoS 收益超过 KV transfer 成本。
- Wide EP/DP attention 在目标 MoE/MLA 模型上优于 TP。
- Batch async processor 可提高利用率且不伤在线 SLO。

### 不得写成事实

- “llm-d 一定比 vLLM production stack 更好”。
- “Wide EP 是所有大模型多节点部署的最佳方案”。
- “AgentX 数字代表所有 agentic workloads”。
- “演讲中的 $/M tokens 成本可直接作为采购建议”。

## 12. 动态附录（Dynamic appendix）

<!-- verified: v0.27.1, 2026-08-15 -->

当前 vLLM 基线为 v0.27.1；llm-d guide/image 仍需固定 release/commit 后，才能判断接口和部署兼容性。Office Hours 材料继续作为 C/D 级发现线索。

动态材料位置：

- 能力状态：[`capability-matrix.yml`](capability-matrix.yml)
- QA 追踪：`../../tracking/2026-07-09-office-hours-53-qa.yml`
- 来源清单：`../../source/README.md`
- Claim spine：`../../claims.yml`
- 术语：`../../vocabulary.md`
- 结构化分析：`../2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md`

下一步验证：固定 llm-d release、vLLM tag、模型/硬件/网络拓扑，运行 OpenAI API 与 gRPC engine smoke test，再测 prefix affinity、KV transfer 和 PD 对照。

## 13. 研讨结论模板（Seminar decision template）

```text
Decision:
Target llm-d commit/release:
Target vLLM commit/release:
Target workload/trace:
Accepted claims:
Rejected generalizations:
Required tests/experiments:
Owner:
Review date:
```
