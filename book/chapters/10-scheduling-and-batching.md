# 第 10 章 调度、连续批处理与排队

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

调度器把业务公平、KV 容量和 GPU shape 连接在一起。优化调度不是单纯扩大 batch，而是分配每一轮的 token 预算。

## 10.1 token budget

一次 schedule 受 `max_num_seqs`、scheduled/batched token 上限、可用 KV blocks、最大模型长度、encoder budget、grammar、speculative lookahead 和 connector 依赖约束。请求数相同，128-token prefill 与 1-token decode 的工作量完全不同，故 token budget 比 request batch 更接近真实资源。

连续批处理允许完成请求退出、等待请求加入。decode 可与 chunked prefill 共批，减少设备空洞；但长 prefill 占太多 token 会拉高活跃 decode 的 ITL。

## 10.2 Chunked prefill

把长 prompt 分多轮计算有三个作用：限制单轮 shape、与 decode 交错、改善 TTFT 公平性。代价是更多调度/launch、可能较低 prefill GEMM 效率，以及请求要更久才得到首 token。

调 token budget 的方向：交互 SLO 倾向控制 chunk，批处理倾向更大 prefill。必须同时看 TTFT、ITL 与 total token/s。只看 TTFT 可能因 decode 被保护而误读，反之亦然。

## 10.3 抢占是反馈信号

KV 不足时，运行请求可能被移出并稍后 recompute。抢占不是免费的公平机制：已做的 prefill 被浪费，并形成正反馈——重算占预算，又导致更多排队。出现持续 preemption 时，应减少运行序列/长度、增加 KV、隔离长请求或扩容，而非继续增大 admission。

watermark 可保留少量 blocks，减少刚接纳就抢占的抖动；其代价是名义容量下降。评估目标应是 goodput 和稳定性。

## 10.4 策略与优先级

FCFS 容易解释，但长任务可能 head-of-line blocking；priority 能保护关键流量，却可能饿死低优先级。生产上应在入口先配额和队列隔离，再在 engine 内使用优先级，并设 aging/最大等待策略。

取消必须尽快从 waiting/running 清除。客户端超时而服务端不取消，会制造“幽灵负载”，令排队指标与业务流量对不上。

## 10.5 异步调度与重叠

异步 scheduling 或 PP batch queue 允许调度下一批与当前执行重叠，降低 CPU bubble；但多个 in-flight batch 会让 block 生命周期、KV connector 和输出顺序复杂化。当前 scheduler 对 consumer connector 可能延迟 free，防止尚在写的块被重新分配并被异步 load 覆盖。

这说明控制面优化也会改变内存一致性。打开异步模式应测试 abort、preemption、remote KV failure 和多步输出，不只测 happy path。

## 10.6 调参顺序

1. 固定 workload 和 SLO，观察 queue、KV、preemption；
2. 设足够但不过量的序列上限；
3. 扫 token budget，找到 TTFT/ITL/goodput 前沿；
4. 对长 prompt 扫 chunk；
5. 才尝试 async、priority 或 overlap。

> **判断**：batch 是调度结果，不是越大越好的配置目标。最优点位于设备效率与排队成本的 Pareto 前沿。
