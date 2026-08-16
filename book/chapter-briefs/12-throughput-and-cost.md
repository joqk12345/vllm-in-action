---
chapter_id: "12-throughput-and-cost"
part: III
title: "吞吐、利用率与单位成本"
status: draft
depends_on: ["08-parallelism-and-topology", "09-benchmarking", "10-scheduling-and-batching"]
evidence_status: partial
---

# 章节承诺

在 SLO 约束内优化有效吞吐，并把 GPU 利用率转化为容量和成本判断。

## 必须包含

- request/s、token/s 与有效完成量。
- 饱和曲线和吞吐拐点。
- 量化、并行、副本数与批处理的成本权衡。
- 高利用率但低业务效率的反例。

## 读者产物

每百万 token 成本模型与容量选择表。

## 证据缺口

硬件价格口径；多卡/多副本对照；能耗是否纳入范围。
