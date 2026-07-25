---
chapter_id: "10-scheduling-and-batching"
part: III
title: "调度、批处理与排队"
status: brief
depends_on: ["03-inside-vllm", "09-benchmarking"]
evidence_status: missing
---

# 章节承诺

解释调度与批处理怎样连接请求分布、GPU 利用率、延迟和公平性。

## 必须包含

- continuous batching 的收益和排队代价。
- prefill/decode 混合、chunking、抢占与饥饿。
- 并发限制与背压。
- 不同负载混跑的反例。

## 读者产物

按 workload 调整调度的实验矩阵。

## 证据缺口

目标版本默认行为；调度器源码锚点；混合负载实验。
