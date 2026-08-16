---
chapter_id: "02-workload-slo-and-metrics"
part: I
title: "工作负载、SLO 与指标"
status: draft
depends_on: ["01-from-demo-to-production"]
evidence_status: partial
---

# 章节承诺

把模糊的“快”转化为可测的工作负载模型和服务目标。

## 核心问题

- TTFT、ITL、端到端延迟和吞吐分别回答什么？
- 输入/输出长度、到达过程、并发和采样如何改变结果？
- 离线批处理、交互聊天与 agent 工作负载为何不能共用一个基准？

## 必须包含

- 指标定义与测量边界。
- 三类请求分布的示例数据集。
- 平均值掩盖尾延迟的反例。

## 读者产物

可直接填写的 workload profile 与 SLO 表。

## 证据缺口

官方指标语义；业界 SLO 案例；请求分布采样方案。
