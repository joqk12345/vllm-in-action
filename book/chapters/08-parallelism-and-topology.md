# 第 8 章 分布式推理与硬件拓扑

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

并行不是“多卡就更快”。它用通信和协调换容量或计算。先问单副本为什么不能满足，再选维度。

## 8.1 五种主要维度

| 维度 | 切什么 | 主要通信 | 适用目标 |
|---|---|---|---|
| TP | 层内矩阵/heads | 高频 AllReduce/AllGather | 单卡放不下、低延迟 |
| PP | 层 | stage 间 activation | 跨慢互联扩容量 |
| DP | 请求/副本 | 路由；MoE 可能同步 | 横向吞吐与隔离 |
| EP | experts | token All-to-All | 大 MoE 权重与吞吐 |
| CP(DCP/PCP) | 序列上下文 | KV/attention 状态通信 | 超长 decode/prefill |

当前 `ParallelConfig` 明确区分 tensor、pipeline、data、prefill context 与 decode context parallel，并提供 EP、EPLB、All-to-All backend、dual batch overlap 等配置。这些组合受模型和 backend 约束，不能自由相乘。

## 8.2 TP：通信频繁但路径直接

TP 把每层 GEMM 切到多个 rank，层间通常需要 collective。NVLink/NVSwitch 内适合较大 TP；跨节点 TP 常被 latency 和带宽拖累。小 batch decode 的计算块更小，collective 占比更敏感。选择能装下模型的最小 TP，再实测扩大 TP 是否改善 SLO。

KV heads 不可整除、量化 pack 或特定模型层会限制 TP。custom all-reduce 与 NCCL fallback 要用 profiler 确认，不能从 flag 推断实际路径。

## 8.3 PP：容量与气泡

PP 把层放到不同 stage，只传 activation，适合跨节点或不均匀模型，但单 microbatch 会产生 pipeline bubble。V1 可通过 batch queue/并发 batch 减少气泡；这会增加在途状态和调度复杂度。stage 层数应按计算和显存平衡，不只按层数平均。

## 8.4 DP 与路由

DP 复制 dense 模型，天然扩大 request throughput 与故障域。路由应考虑每 rank queue、KV 利用率、prefix locality 和 adapter，而非简单 round-robin。外部 DP 模式适合一 pod 一 rank，hybrid 模式可在节点内由 vLLM 平衡、节点间由外部 LB 平衡。

对 MoE，DP ranks 还可能共同形成 wide EP，不能再把它理解为完全独立副本。

## 8.5 EP 与负载不均

EP 将 experts 分到 ranks。router 输出决定 token 发往何处，核心成本是 dispatch/combine All-to-All。专家热度倾斜会使最慢 rank 成为迭代屏障。EPLB 可根据窗口统计重排/冗余专家，但迁移有通信与一致性成本。

backend 的 high-throughput 与 low-latency 模式对应不同 workload。比较时报告每 rank token、All-to-All 时间、balancedness、互联和 batch，而不是只报总 token/s。

## 8.6 上下文并行与 P/D 解耦

PCP 分摊 prefill 序列计算，DCP 针对 decode context；二者的 world-size、KV shard 和通信语义不同。prefill/decode disaggregation 则把两个阶段放入不同实例，经 KV connector 传状态。它可独立扩容与隔离长 prefill，但引入 KV 传输、路由、失败重算和一致性。

判断解耦是否值得：节省的排队/干扰必须大于传输与额外调度。短 prompt 通常很难摊薄远端 KV 成本。

## 8.7 拓扑优先的放置

画出 GPU—NVLink—PCIe switch—NUMA—NIC。高频 TP 放最快域内，PP/DP 跨较慢边界，EP 尽量匹配高带宽 fabric。先用 collective benchmark 建立链路上限，再 profile 模型。多节点问题先检查 rank mapping、NIC 选择、MTU、GID、拓扑和时钟。

> **决策式**：并行收益 = 被切分的计算/容量收益 − collective − 气泡 − 不均衡 − 控制面开销。任何方案都应逐项量化。
