# llm-d agentic serving 阅读路径

Owner:
Purpose: 按研究问题组织 llm-d agentic serving 的阅读轮次，指导读者从 Office Hours 线索走向上游核查和实验设计。
Status: captured
Applies to: research/topics/llm-d-agentic-serving
Evidence grade: C/D 起步
Verified date: 2026-07-26
Assumptions: 阅读输出必须回写到 `claims.yml`、`tracking/`、`capability-matrix.yml` 或实验记录。
Open questions: llm-d/vLLM/InferenceX commit 尚未固定。
Handoff: topic booklet、seminar、chapter handoff

## Round 0：建立证据边界

目标：先理解 Office Hours 材料只能作为线索。

主要材料：

- `source/README.md`
- `claims.yml`
- `tracking/2026-07-09-office-hours-53-qa.yml`

提取内容：

- 哪些 claim 只有 C/D 级证据；
- 哪些数字不能进入正文；
- 哪些问题需要源码/测试/实验。

输出：

- high priority QA 的 owner、next_action 和 done_criteria。

## Round 1：Agentic workload 与 routing

目标：回答普通 round-robin 为什么不够，以及 Intelligent Routing 优化什么。

主要材料：

- `outputs/2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md`
- `claims.yml`：LD-C01、LD-C02
- llm-d repository，待固定 commit

提取内容：

- prefix cache affinity；
- load/backpressure；
- filters/scorers；
- predicted latency scheduling；
- endpoint picker / EPP 的正式 API。

输出：

- routing capability 状态；
- round-robin vs prefix-aware benchmark 计划。

## Round 2：KV cache management

目标：理解 KV working set 如何从单 pod 扩展到集群。

主要材料：

- `claims.yml`：LD-C03
- vLLM repository/docs，待固定 release
- llm-d repository，待固定 commit

提取内容：

- GPU/CPU/NVMe/remote storage tier；
- KV offload/reload 成本；
- router 如何感知 KV state；
- tiered prefix affinity。

输出：

- KV tiering 状态表；
- tier hit vs recompute ablation。

## Round 3：PD disaggregation 与 Wide EP

目标：拆清 Serving Large Models 的两个机制。

主要材料：

- `claims.yml`：LD-C04、LD-C05、LD-C06
- Office Hours PDF Wide EP slides
- vLLM PD/Wide EP/DP attention 源码与 PR，待固定

提取内容：

- prefill/decode worker；
- NIXL/UCX/InfiniBand KV transfer；
- MLA single latent KV vector 与 TP 复制问题；
- DP attention、Wide EP、DP-aware scheduling；
- LeaderWorkerSet/Grove/operator 与 llm-d 边界。

输出：

- PD 与 Wide EP 职责对照表；
- TP vs Wide EP benchmark 计划。

## Round 4：Operational excellence 与 batch

目标：研究 flow control、priority、batch async processor 和 SLO-aware autoscaling。

主要材料：

- Office Hours PDF 的 llm-d feature slides
- llm-d repository，待固定 commit
- QA-llmd-oh53-003

提取内容：

- saturation detector；
- queueing and priority；
- online vs offline/batch；
- OpenAI-compatible Batch API；
- autoscaling signals。

输出：

- multi-tenant SLO canary；
- batch 不伤害 online traffic 的实验设计。

## Round 5：AgentX/InferenceX benchmark 与成本模型

目标：验证或降级处理演讲中的 benchmark/cost 数字。

主要材料：

- `claims.yml`：LD-C07
- `tracking/2026-07-09-office-hours-53-qa.yml`：QA-004、QA-005
- InferenceX/AgentX repository，待固定 commit

提取内容：

- trace 来源；
- input/output 长度分布；
- concurrency；
- tokens/s/user 与 tokens/s/GPU；
- GPU 单价、利用率和成本计算。

输出：

- benchmark manifest 模板；
- 成本模型模板；
- 哪些演讲数字只能保留为线索。

## 最小阅读笔记格式

```text
Source:
Question answered:
Claim/proposition:
Evidence grade:
Version/commit:
Applies to:
Does not prove:
Counterexample:
Follow-up action:
Related QA/claim:
```
