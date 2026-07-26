# Efficient Long-Context Attention Booklet Bundle

Owner:
Purpose: 汇总 `efficient-long-context-attention` 专题小册子交付物，供章节写作、研讨和后续刷新使用。
Status: draft
Applies to: research/topics/efficient-long-context-attention
Evidence grade: A/B claims only for正文候选；C/D 仅作解释或发现线索。
Verified date: 2026-07-26
Assumptions: 论文结果均为作者报告；vLLM serving 事实必须固定 release/tag/commit 并本仓验证。
Open questions: NSA/MoBA/MiniMax-01 尚未补齐；Qwen3.5 具体 config 和 vLLM smoke test 未完成。
Handoff: 第 04、08、09、11、12、13、15 章。

## Files

- [`efficient-long-context-attention-topic-booklet.md`](efficient-long-context-attention-topic-booklet.md) — 主题研究小册子。
- [`seminar-guide.md`](seminar-guide.md) — 研讨课问题、流程和练习。
- [`reading-list.md`](reading-list.md) — 分层阅读路径。
- [`capability-matrix.yml`](capability-matrix.yml) — 机器可读能力矩阵。

## Refresh triggers

- vLLM 发布新 tag，改变 Kimi Linear / Qwen3-Next / GDN / sparse attention 支持。
- Kimi Linear、Qwen3-Next/Qwen3.5、MiniMax-M1/M2、GLM-5 论文或模型 config 更新。
- NSA、MoBA、MiniMax-01 source cards 补齐。
- 本仓完成 Kimi Linear 或 Qwen3-Next serving smoke test / benchmark。
