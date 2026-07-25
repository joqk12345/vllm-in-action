# 专题输出

当前专题处于 `captured` 状态，尚未生成小册子或正文转写包。

当前已保存一份待审议的正文落点建议：

- [`chapter-handoff/chapter-placement-proposal.md`](chapter-handoff/chapter-placement-proposal.md) — 第 9、10、11、12、15 章的候选内容映射；尚未修改章节 brief 或正文。

达到以下条件后运行 `$topic-booklet`：

- 至少两个来源围绕相同研究问题完成交叉综合；
- `claims.yml` 中的核心 claim 已补齐边界、反例和验证缺口；
- Speculators 与 vLLM 的工程事实已经固定到 commit/release；
- 论文结论与本仓库实验观察保持分离。

后续输出按用途进入：

- `booklet/`：主题研究小册子、研讨指南、阅读清单和 capability matrix；
- `brief/`：面向工程决策的短报告；
- `chapter-handoff/`：进入第 10、11、15 章的候选段落和证据映射；
- `figures/`：可复用架构图与性能模型图；
- `slides/`：研讨演示文稿。
