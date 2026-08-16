---
chapter_id: "09-benchmarking"
part: III
title: "构建可信的 Benchmark"
status: draft
depends_on: ["02-workload-slo-and-metrics", "06-serving-and-api"]
evidence_status: partial
---

# 章节承诺

设计可复现、公平且与业务决策相关的 benchmark。

## 必须包含

- offline 与 serving benchmark 的差别。
- warm-up、随机性、输入输出分布和到达模型。
- 指标采集、重复次数、置信度和原始数据保留。
- 常见作弊方式与不可比结果。
- 用 Rust Frontend RFC 演示“刻意构造的 frontend-bound 测试能证明什么、不能证明什么”。

## 读者产物

标准实验协议、结果表和审阅清单。

## 证据缺口

官方 benchmark 工具语义；统计方法复核；首套基线数据；复现一个 frontend-bound 与一个 GPU-bound 对照。[SRC-vllm-rust-frontend-rfc-40846]
