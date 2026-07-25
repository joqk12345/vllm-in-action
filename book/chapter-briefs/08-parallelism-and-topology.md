---
chapter_id: "08-parallelism-and-topology"
part: II
title: "并行策略与硬件拓扑"
status: brief
depends_on: ["04-memory-and-kv-cache", "07-model-loading-and-precision"]
evidence_status: missing
---

# 章节承诺

根据模型尺寸、单请求延迟、吞吐目标和互联拓扑选择并行策略。

## 必须包含

- tensor、pipeline、data 与 expert parallel 的问题边界。
- PCIe/NVLink/网络拓扑对通信的影响。
- 单机多卡与多机的失败模式。
- “能切开”但更慢的反例。

## 读者产物

并行选型树和拓扑验收清单。

## 证据缺口

各并行模式当前语义；拓扑对照实验；多机故障案例。
