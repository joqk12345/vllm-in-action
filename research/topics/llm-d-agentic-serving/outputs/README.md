# 专题输出

当前专题处于 `captured` 状态，已生成第一版小册子 bundle；工程事实仍未固定到 llm-d/vLLM release 或 commit，不能直接进入正文。

当前已保存：

- [`deliverables.yml`](deliverables.yml) — 输出登记表。
- [`booklet/`](booklet/) — 主题研究小册子、研讨指南、阅读路径和 capability matrix。
- [`2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md`](2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md) — Office Hours #53 PDF/自动字幕结构化分析与 QA，C/D 级线索。

## 后续输出计划

- `booklet/`：主题研究小册子、研讨指南、阅读路径和 capability matrix。
- `brief/`：面向工程决策的短报告，例如“agentic workload 是否需要 llm-d”。
- `chapter-handoff/`：进入第 11、12、15 章的候选段落和证据映射。
- `figures/`：prefix-aware routing、PD disaggregation、Wide EP/DP attention 和 flow control 图。
- `slides/`：研讨演示文稿。

## 运行 `$topic-booklet` 前的最低条件

- 至少补充 llm-d/vLLM 上游仓库或官方文档作为第二类来源。
- `claims.yml` 中核心 claim 已绑定 Source ID、边界、反例和验证缺口。
- Wide EP、PD、prefix routing 和 KV tiering 的工程事实固定到 commit/release。
- 演讲数字与本仓实验观察保持分离。
