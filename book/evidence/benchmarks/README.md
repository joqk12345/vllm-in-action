# Benchmark 记录

一个 benchmark 是一组可比较实验，不是一张漂亮的结果表。每组记录必须包含：

- 研究问题和公平性原则；
- 完整环境、模型 revision 和引擎参数；
- 请求长度分布、并发/到达过程和 warm-up；
- TTFT、ITL、端到端延迟、吞吐、错误率、显存；
- 原始输出路径与分析脚本；
- 结果边界、异常点和负结果。

建议按 `BENCH-YYYYMM-topic/` 建目录，实验文档复用 `templates/experiment.md`。
