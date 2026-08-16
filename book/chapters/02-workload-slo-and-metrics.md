# 第 2 章 工作负载、SLO 与指标

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

性能不是引擎属性，而是引擎与工作负载的关系。同一模型在固定并发、Poisson 到达和突发流量下会得到三组不同结果。

## 2.1 描述分布而不是平均值

最小 workload schema 包含：请求到达时间、input/output token、模型或 LoRA、采样参数、是否流式、共享前缀长度、模态大小、取消率。至少报告 p50/p90/p99 和二维长度桶。均值会掩盖长 prompt 对 KV 容量和排队的非线性影响。

到达率记为 $\lambda$，平均系统驻留时间为 $W$，平均在途请求数为 $L$。稳定区间可用 Little 定律 $L=\lambda W$ 做一致性检查，但它不预测尾延迟。利用率接近饱和点时，微小抖动也会形成长队列。

## 2.2 指标的精确定义

对请求 $i$：到达为 $a_i$，首 token 为 $f_i$，后续 token 时间为 $t_{i,j}$，完成为 $c_i$：

- $TTFT_i=f_i-a_i$；
- $ITL_{i,j}=t_{i,j}-t_{i,j-1}$；
- $E2E_i=c_i-a_i$；
- normalized latency 可用 $E2E/output\_tokens$，但不能替代 ITL；
- throughput 分 input、output、total token/s 与 request/s。

服务端应继续拆解 queue、prefill、decode、tokenization 与网络时间。客户端 TTFT 才包含真实代理链与网络，服务端指标则适合定位，两者不可混用。

## 2.3 SLO 与 goodput

例如定义“p99 TTFT < 2 s 且 p95 ITL < 80 ms，错误率 < 0.1%”。goodput 只统计两项均合格的请求。这样，靠无限扩大 batch 获得的 token/s 若破坏交互体验，就不会被误判为优化。

容量测试分三层：

1. **单请求**：测算子与模型下限；
2. **固定并发**：观察引擎饱和曲线；
3. **开放到达**：寻找满足 SLO 的最大稳定速率。

固定并发会在请求完成后立刻补请求，具有自节流效应；线上流量不会，所以最终容量必须以开放模型复核。

## 2.4 四类典型画像

| 画像 | 主目标 | 常见瓶颈 | 优先实验 |
|---|---|---|---|
| 短问答 | TTFT/ITL | 调度、launch、权重带宽 | graph、批策略 |
| 长文档 | TTFT | prefill、KV 容量 | chunked prefill、CP |
| 多轮 agent | goodput | prefix 重算、突发 | APC、路由、隔离 |
| 离线生成 | token/s、成本 | 利用率 | 大批次、量化、DP |

混在同一队列中的长 prefill 会干扰短 decode。先按业务 class 分指标，再决定是否用优先级、配额或独立副本。

## 2.5 可复现实验记录

记录 vLLM commit、模型 revision、tokenizer、GPU 型号/数量/互联、driver/CUDA/ROCm、dtype/quant、全部非默认参数、随机种子、warm-up、请求数据和原始输出。模型输出长度必须由真实分布或固定 token 控制，否则 EOS 差异会污染吞吐。

推荐图表：到达率—p99 TTFT、到达率—goodput、并发—output token/s、KV 使用率时间序列以及 input/output 长度热力图。拐点比单个最大值更重要：生产目标通常位于拐点左侧并保留故障冗余。

## 2.6 反例

“GPU 利用率 100%”既可能表示高效 GEMM，也可能表示通信自旋；“cache hit 90%”没有说明节省了多少 prefill token；“平均 ITL 低”可能掩盖严重 p99 停顿。指标必须与用户结果、工作量和资源消耗形成三角验证。

> **实验**：用同一 trace 分别跑固定并发与开放到达测试，标出 token/s 最大点和 goodput 最大点。它们通常不是同一点。
