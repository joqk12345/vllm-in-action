# 专题输出

当前专题处于 `captured` 状态，尚未生成小册子、brief 或章节 handoff。

当前已保存：

- [`2025-11-01-kimi-linear-paper-v2-analysis.md`](2025-11-01-kimi-linear-paper-v2-analysis.md) — Kimi Linear 论文 v2 结构化分析，B 级作者报告。
- [`2025-06-16-minimax-m1-paper-v1-analysis.md`](2025-06-16-minimax-m1-paper-v1-analysis.md) — MiniMax-M1 / Lightning Attention 论文 v1 结构化分析，B 级作者报告。
- [`2026-05-26-minimax-m2-series-paper-v1-analysis.md`](2026-05-26-minimax-m2-series-paper-v1-analysis.md) — MiniMax-M2 full attention 选择与 hybrid/SWA 反例分析，B 级作者报告。
- [`2026-05-26-minimax-m2-full-vs-hybrid-swa-tables.md`](2026-05-26-minimax-m2-full-vs-hybrid-swa-tables.md) — MiniMax-M2 Table 2/3 full attention vs hybrid SWA 数值抽取。
- [`2026-07-26-kimi-linear-implementation-snapshot.md`](2026-07-26-kimi-linear-implementation-snapshot.md) — Kimi Linear/KDA 源码与 vLLM 支持快照，固定 commit。
- [`2026-07-26-vllm-v0-25-1-kimi-linear-smoke-test-plan.md`](2026-07-26-vllm-v0-25-1-kimi-linear-smoke-test-plan.md) — vLLM v0.25.1 Kimi Linear 分层 smoke test 计划。
- [`2026-07-26-qwen3-next-gdn-explainer.md`](2026-07-26-qwen3-next-gdn-explainer.md) — Qwen3-Next/Qwen3.5 GDN 机制、config 和 vLLM support path 解释分析。
- [`2025-03-06-gated-deltanet-paper-v3-tables.md`](2025-03-06-gated-deltanet-paper-v3-tables.md) — Gated DeltaNet 论文 Table 2/3/4/5 快速抽取。
- [`2026-kimi-linear-yang-songlin-interview-analysis.md`](2026-kimi-linear-yang-songlin-interview-analysis.md) — Kimi Linear / 线性注意力访谈材料使用建议，D 级线索。

## 后续输出计划

- `booklet/`：主题研究小册子、研讨指南、阅读路径和 capability matrix。
- `brief/`：面向工程决策的短报告，例如“高效 attention 是否能降低 vLLM 长上下文 serving 成本”。
- `chapter-handoff/`：进入第 04、08、09、11、12、15 章的候选段落和证据映射。
- `figures/`：dense/sparse/linear/window/block attention 对比图，prefill/decode 成本图。
- `slides/`：研讨演示文稿。

## 运行 `$topic-booklet` 前的最低条件

- 至少补齐 NSA、MoBA、Lightning Attention 三篇来源之一的 source card。
- `claims.yml` 中核心 claim 已绑定边界、反例和验证缺口。
- vLLM 支持状态已固定到研究 commit；进入正文前需进一步定位 release tag。
- 论文长上下文质量结论与本仓 serving 实验观察保持分离。