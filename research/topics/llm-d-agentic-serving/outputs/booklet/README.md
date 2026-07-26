# llm-d agentic serving 小册子输出

Owner:
Purpose: 为 llm-d + vLLM 在 agentic long-context workloads 下的分布式 serving 研究提供可研讨、可刷新、可交接的综合材料。
Status: captured
Applies to: vLLM Office Hours #53；llm-d/vLLM/InferenceX 上游状态尚未固定 release/commit
Evidence grade: C/D 起步；正文结论仅接受 A/B 级证据或本仓可复现实验
Verified date: 2026-07-26
Assumptions: Office Hours 幻灯片和自动字幕只作为研究线索。
Open questions: llm-d router/EPP、PD、Wide EP、KV tiering 和 AgentX benchmark 的固定版本与测试覆盖。
Handoff: 第 11、12、15 章。

## 文件职责

- [`llm-d-agentic-serving-topic-booklet.md`](llm-d-agentic-serving-topic-booklet.md)：稳定主体，按共同研究问题综合路由、KV cache、PD、Wide EP、QoS 和 batch。
- [`seminar-guide.md`](seminar-guide.md)：60–90 分钟研讨指南。
- [`reading-list.md`](reading-list.md)：按阅读轮次组织来源和输出。
- [`capability-matrix.yml`](capability-matrix.yml)：动态能力矩阵，优先用于 release/roadmap 漂移复查。

## 稳定主体与动态附录

稳定主体保留系统模型、概念、反例和验证计划。动态事实，例如 llm-d/vLLM release 支持、PR 状态、AgentX benchmark 数字和 deployment operator 能力，优先放入 capability matrix、tracking 文件和 source cards。

## 刷新顺序

1. 检查 `tracking/README.md` 与 `tracking/2026-07-09-office-hours-53-qa.yml`。
2. 更新 `capability-matrix.yml` 的 roadmap/release/local-test 三类状态。
3. 只有稳定 claim 或系统模型变化时，才更新小册子主体。
4. 同步 `claims.yml`、source cards、benchmark/experiment records 和 chapter handoff。

## 重要边界

Office Hours 幻灯片不证明 release 支持；自动字幕不能支撑正文；AgentX/OpenRouter 成本数字不能直接外推到本仓目标 workload。