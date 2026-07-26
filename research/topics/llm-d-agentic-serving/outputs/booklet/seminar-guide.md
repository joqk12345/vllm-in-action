# llm-d agentic serving 研讨指南

Owner:
Purpose: 支持 60–90 分钟研讨，围绕 llm-d + vLLM 在 agentic workloads 下的路由、KV、PD、Wide EP、QoS 和 batch 决策形成可执行任务。
Status: captured
Applies to: research/topics/llm-d-agentic-serving
Evidence grade: C/D 起步；研讨中不得把 Office Hours 线索当作正文事实。
Verified date: 2026-07-26
Assumptions: 参与者已读小册子执行摘要、`claims.yml` 和 QA tracker。
Open questions: llm-d/vLLM commit 尚未固定。
Handoff: `claims.yml`、capability matrix、benchmark 计划和第 11/12/15 章 handoff。

## 1. 目标与非目标

### 目标

- 对齐 agentic workloads 与普通 HTTP/QPS serving 的差异。
- 拆清 Intelligent Routing、KV tiering、PD、Wide EP、flow control、batch 的职责边界。
- 将 QA tracker 中 high priority 项转成源码核查或实验任务。
- 定义 AgentX-like benchmark 的最低配置和指标。

### 非目标

- 不决定正式生产建议。
- 不把 Office Hours 数字写成 benchmark 结论。
- 不讨论与 llm-d/vLLM 无关的通用 Kubernetes 网关设计。

## 2. 参与角色

| 角色 | 责任 |
|---|---|
| Facilitator | 控制议程，防止逐页复述 PPT。 |
| Routing reviewer | 核查 EPP/router、prefix affinity、load-aware scoring。 |
| vLLM runtime reviewer | 核查 prefix cache、KV offload、PD、Wide EP、DP attention。 |
| Kubernetes/operator reviewer | 核查 Gateway API、InferencePool、LeaderWorkerSet、Grove、版本滚动。 |
| Benchmark owner | 定义 trace、硬件、并发、指标和成本模型。 |
| Red team | 提出低复用、无高速网络、状态滞后和成本误导反例。 |

## 3. 会前必读

- `outputs/booklet/llm-d-agentic-serving-topic-booklet.md`：第 2、3、8、9、10、11 节。
- `claims.yml`：LD-C01 至 LD-C07。
- `tracking/2026-07-09-office-hours-53-qa.yml`。
- `outputs/2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md`。
- `source/README.md`。

## 4. 90 分钟议程

| 时间 | 主题 | 输出 |
|---|---|---|
| 0–10 分钟 | 证据等级与主题边界 | 共同接受的证据门禁 |
| 10–25 分钟 | Q1：agentic workload 为什么需要推理感知路由 | workload 定义和反例 |
| 25–40 分钟 | Q2/Q3：routing 与 KV cache tiering | 需要核查的 router/KV 状态接口 |
| 40–55 分钟 | Q4：PD 与 Wide EP 的职责边界 | 并行/部署能力拆分表 |
| 55–70 分钟 | Q5：flow control、priority、batch 和 autoscaling | 生产 SLO 保护策略 |
| 70–82 分钟 | Q6：AgentX-like benchmark 与成本模型 | 实验矩阵草案 |
| 82–90 分钟 | 决策记录、owner 和 review date | action list |

60 分钟压缩版：只讨论 routing、PD/Wide EP、benchmark 三项。

## 5. 核心研讨问题

1. Prefix affinity 与 load-aware balancing 冲突时，应该如何打分？
2. KV 在 GPU/CPU/NVMe/remote tier 中的状态如何被 router 精确感知？
3. PD 的收益何时超过 KV transfer 和部署复杂度？
4. Wide EP/DP attention 适用于哪些模型结构，不适用于哪些？
5. Flow control 如何避免 batch 或低优先级租户伤害在线 SLO？
6. AgentX-like benchmark 必须记录哪些指标才能支撑成本结论？

## 6. Red-team questions

- 如果 prefix cache hit rate 高但 p99 latency 变差，说明哪里出了问题？
- 如果 router 状态滞后，把请求打到错误 pod，会如何回退？
- 如果没有 InfiniBand，PD 是否仍值得启用？
- 如果 deployment operator 启动了不同 vLLM 版本的 prefill/decode pods，会发生什么？
- 如果 workload 不是多轮复用，llm-d 还有多少收益？
- 如果 batch 占满 KV cache，在线请求如何保护？

## 7. 决策/action record

```text
Decision:
Accepted claims:
Claims blocked:
Target llm-d commit/release:
Target vLLM commit/release:
Trace/benchmark owner:
Source verification owner:
Capability matrix changes:
New experiments:
Canary/rollback requirement:
Next review date:
```

## 8. 完成 checklist

- [ ] 每个 accepted claim 绑定上游 commit/release 或实验。
- [ ] capability matrix 更新 roadmap/release/local-test 三类状态。
- [ ] benchmark 记录 trace、模型、硬件、网络、并发和成本假设。
- [ ] 至少覆盖低复用、无高速网络、KV tier 读取慢、版本滚动不一致四类反例。
- [ ] 需要刷新的 handoff、brief、figures 或 slides 已标记。