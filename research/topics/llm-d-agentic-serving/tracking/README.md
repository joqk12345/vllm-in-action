# llm-d agentic serving 持续跟踪

Owner: release tracker
Purpose: 跟踪 llm-d、vLLM、InferenceX/AgentX 与 Wide EP/PD/KV routing 相关能力的实现、发布和实验漂移。
Status: active
Applies to: 研究阶段跟踪浮动上游；正文结论固定到 release/tag/commit 和本仓实验。
Evidence grade: discovery only；接受结论时回到源码、测试、release 文档、PR 或实验。
Verified date: 2026-08-15
Assumptions: Office Hours 线索不证明目标版本可用；AgentX/InferenceX 数字不证明本仓 workload 可复现。
Open questions: 第一个可稳定复现 llm-d + vLLM agentic workload 收益的版本组合。
Handoff: 第 11、12、15 章。

## 跟踪对象

| 对象 | 关注变化 | 进入正文前的固定点 |
|---|---|---|
| llm-d | router/EPP、prefix affinity、flow control、batch、deployment examples | commit 或 release |
| vLLM | prefix cache、KV offload/tiering、PD disaggregation、NIXL/UCX、Wide EP、DP attention | release tag + commit |
| InferenceX/AgentX | trace、benchmark 方法、提交结果和配置 | commit + workload manifest |
| Kubernetes Gateway API inference extension | inference pool、EPP 接入、gateway 兼容性 | spec version + implementation commit |
| LeaderWorkerSet / Grove / deployment operator | gang/co-scheduling、版本滚动、拓扑感知 | operator version + example manifest |
| 本仓实验 | prefix hit rate、TTFT、ITL、TPS/user、TPS/GPU、goodput、成本 | 环境 manifest + 原始结果 |

## 节奏

- 每个 vLLM 或 llm-d release：复查 capability、配置和测试。
- 每月：检查 InferenceX/AgentX 和 Gateway API 相关变化。
- 每季度或关键实现变化后：刷新 agentic workload benchmark。

## 漂移分诊

1. 记录变化 URL、日期、commit/release 和相关 claim。
2. 区分 routing、KV cache、PD、parallelism、flow control、batch 和 deployment operator 变化。
3. 用源码与测试确认 README/演讲中的能力是否进入目标版本。
4. 标记需要重跑的 workload、指标和基线。
5. 先更新 `claims.yml` 和来源信息，再刷新 booklet、brief 或 chapter handoff。

## 优先核查项

1. llm-d EPP/router 如何发现 pod、收集 prefix/KV 状态并做 scoring。
2. vLLM 中 KV offload/tiering 与 router 的状态接口。
3. PD disaggregation 的 KV transfer 后端、失败恢复和版本滚动约束。
4. Wide EP / DP attention 的目标模型、硬件和测试覆盖。
5. AgentX trace 的可获得性、重放方法和指标定义。
6. Flow control 和 batch async processor 如何保护在线 SLO。
