# 第 13 章 可观测性与容量规划

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

可观测性应能回答“用户为何慢”和“还可接多少流量”，而不只是证明进程活着。

## 13.1 四层信号

1. 边缘：RPS、状态码、连接、重试、payload、客户端 TTFT；
2. 前端：render/tokenize/media、queue、stream backpressure；
3. engine：running/waiting、scheduled tokens、KV usage/hit、preemption、spec acceptance；
4. 设备：显存、功耗、kernel、collective、PCIe/NIC。

统一 request ID、model revision、replica、DP rank 和 workload class。高基数 prompt/tenant 不应直接成为 metric label；放入受控 trace/log，并脱敏。

## 13.2 指标关系比单点更重要

queue 上升 + GPU 忙：容量饱和；queue 上升 + GPU 空：前端/调度/编译/通信停顿；KV 高 + preemption：缓存压力；cache hit 高但 TTFT 不降：命中 token 少或 queue 支配；GPU 忙但 token/s 降：batch 形态、长 context、通信或重算改变。

告警应基于 SLO burn rate、队列年龄和引擎 progress，而不是瞬时利用率。多窗口 burn-rate 兼顾快速故障与慢性退化。

## 13.3 容量模型

从 benchmark 得到每种 workload class 的最大合格到达率，再乘安全系数。副本数粗略为

$$N=\left\lceil\frac{\lambda_{peak}}{g_{replica}\times target\ utilization}\right\rceil + failure\ reserve$$

其中 $g_{replica}$ 是目标 SLO 下 goodput。不要用峰值 token/s。混合流量还需回放比例，因为长 prefill 与短 decode 的干扰不是简单线性加权。

容量受两条边界限制：计算/带宽服务率与 KV token residency。后者由活跃上下文长度和请求驻留时间决定。突发时排队会增加驻留，又进一步占用 KV，形成耦合。

## 13.4 Autoscaling

仅用 GPU utilization 扩容太迟或误判。组合 queued requests/age、running、arrival rate、TTFT burn 与 KV pressure。考虑模型加载和 graph warm-up 的分钟级冷启动，保留 warm pool；scale-in 先停止 admission、drain，再终止。

prefix-aware routing 会提高局部命中，却可能造成热副本。路由评分应在 cache locality 与 queue/KV load 间折中，并在副本故障时允许重算。

## 13.5 Dashboard 与 runbook

首页只放 SLO、offered load/goodput、错误、queue 和容量余量；下钻页分别展示 cache/scheduler、前端、GPU/collective、每 rank imbalance。每个告警链接 runbook：确认影响 → 定位层 → 安全缓解 → 保存证据 → 根因。

trace 采样覆盖慢请求、错误和随机正常基线；不要全量记录 token 文本。跨服务的客户端 span、API span 和 engine stats 用 request ID 关联，避免把代理等待算成 GPU。

> **验收**：给值班同学一条 p99 TTFT 告警，他应在十分钟内区分流量饱和、长 prompt、KV 抢占、前端 CPU 与分布式停顿。
