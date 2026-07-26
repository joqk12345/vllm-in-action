# 投机解码专题小册子输出

Owner:
Purpose: 为投机解码专题提供可研讨、可刷新、可交接的综合材料。
Status: captured
Applies to: DSpark arXiv v1、2026-07-22 公开分享线索、Speculators/vLLM 浮动状态核对至 2026-07-25
Evidence grade: B/C/D 混合；正文结论仅接受 A/B 级证据
Verified date: 2026-07-25
Assumptions: 当前尚未固定 vLLM/Speculators commit，也未运行本仓端到端 benchmark。
Open questions: DSpark 在目标 vLLM release 中的支持状态、confidence head 推理、LoRA 兼容和在线 hidden states 训练链路仍需核验。
Handoff: 第 10、11、15 章；hidden states 训练链路关联第 8、12 章。

## 文件职责

- [`speculative-decoding-topic-booklet.md`](speculative-decoding-topic-booklet.md)：稳定主体，按共同研究问题综合算法、性能、工程和生产决策。
- [`seminar-guide.md`](seminar-guide.md)：60–90 分钟研讨指南，包含议程、角色、红队问题和决策记录模板。
- [`reading-list.md`](reading-list.md)：按研究问题组织的阅读路径，不是简单 URL 清单。
- [`capability-matrix.yml`](capability-matrix.yml)：动态能力矩阵，优先用于 release/roadmap 漂移复查。

## 稳定主体与动态附录

- 稳定主体只写可长期复用的系统模型、概念、风险和验证方法。
- 动态事实，例如 vLLM 当前支持状态、Speculators 支持矩阵、模型 checkpoint、QA tracker 状态和 benchmark 数字，优先放入 capability matrix、tracking 文件或动态附录。
- ASR 字幕中的问答只能作为 D 级线索，不能直接支撑正文结论。

## 刷新顺序

1. 先检查 `tracking/README.md` 和 `tracking/2026-07-22-dspark-talk-qa.yml`。
2. 更新 `capability-matrix.yml` 中 roadmap/release/local-test 三类状态。
3. 只有稳定 claim 变化时，才更新 `speculative-decoding-topic-booklet.md` 主体。
4. 如研讨目标或阅读材料变化，再更新 `seminar-guide.md` 和 `reading-list.md`。
5. 同步 `claims.yml`、source ledger、benchmark/experiment records 和 chapter handoff。

## 重要边界

Roadmap 或演讲状态不证明功能已 release；README 描述不证明目标 workload 已可用；论文接受长度不等于 vLLM 端到端 speedup。进入正文前必须固定 release/tag/commit 或本仓实验。