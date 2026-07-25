---
chapter_id: "13-observability-and-capacity"
part: IV
title: "可观测性与容量规划"
status: brief
depends_on: ["02-workload-slo-and-metrics", "12-throughput-and-cost"]
evidence_status: missing
---

# 章节承诺

建立从用户 SLO 到引擎、GPU 和队列的观测链，并用它做容量规划。

## 必须包含

- RED/USE 指标映射。
- 队列、KV cache、GPU、请求长度和错误的关联。
- 告警、dashboard 与 trace 的最小集合。
- 压测曲线到副本数和扩缩容阈值。
- 识别 frontend CPU/事件循环饱和，避免把 GPU 空闲误判为引擎容量不足。

## 读者产物

dashboard 规范、告警表与容量 worksheet。

## 证据缺口

官方指标全集；可观测栈示例；扩缩容案例；Python/Rust frontend 的 CPU、内存与排队指标对照。
