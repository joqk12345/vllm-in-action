# Efficient Long-Context Attention Booklet Bundle

Owner:
Purpose: 汇总 `efficient-long-context-attention` 专题小册子交付物，供章节写作、研讨和后续刷新使用。
Status: draft
Applies to: research/topics/efficient-long-context-attention
Evidence grade: A/B claims only for正文候选；C/D 仅作解释或发现线索。
Verified date: 2026-08-01
Assumptions: 论文结果均为作者报告；vLLM serving 事实必须固定 release/tag/commit 并本仓验证。
Open questions: NSA/MoBA/MiniMax-01 尚未补齐；Qwen3.5 config、Kimi/Qwen smoke test、Kimi K3 首个稳定 release 与 correctness 未完成。
Handoff: 第 04、08、09、11、12、13、15 章。

## Files

- [`efficient-long-context-attention-topic-booklet.md`](efficient-long-context-attention-topic-booklet.md) — 主题研究小册子。
- [`seminar-guide.md`](seminar-guide.md) — 研讨课问题、流程和练习。
- [`reading-list.md`](reading-list.md) — 分层阅读路径。
- [`capability-matrix.yml`](capability-matrix.yml) — 机器可读能力矩阵。

## Refresh triggers

- vLLM 发布新 tag，改变 Kimi Linear / Qwen3-Next / GDN / sparse attention 支持。
- vLLM 发布首个包含 Kimi K3 PR #50000 的稳定 tag，或 Kimi K3 image/FlashInfer dependency 变化。
- Kimi Linear、Qwen3-Next/Qwen3.5、MiniMax-M1/M2、GLM-5 论文或模型 config 更新。
- NSA、MoBA、MiniMax-01 source cards 补齐。
- 本仓完成 Kimi Linear 或 Qwen3-Next serving smoke test / benchmark。
- 本仓完成 Kimi K3 partial-hit、PD transfer、DSpark rejection correctness 或性能复现。

## Stable body and dynamic appendix

小册子主体只在稳定 claims 改变时重写。release、RFC、镜像 digest、依赖、parser/backend 清单和本地测试状态先更新 `capability-matrix.yml`，再刷新动态附录。roadmap/RFC 状态不证明 stable release，也不证明本仓 local validation。

刷新顺序：capability matrix → claims/source cards → booklet dynamic appendix → reading/seminar → downstream handoff/figures/slides。
