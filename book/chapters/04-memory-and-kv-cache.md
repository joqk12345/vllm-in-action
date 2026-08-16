# 第 4 章 显存、分页 KV Cache 与混合注意力

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

权重决定服务能否启动，KV cache 决定启动后能承载多少历史。对标准 attention，单 token 的 KV 字节可近似为

$$M_{token}=2\times L\times H_{kv}\times D\times b$$

其中 2 是 K/V，$L$ 为层数，$H_{kv}$ 为 KV heads，$D$ 为 head size，$b$ 为元素字节。GQA/MQA 通过减少 $H_{kv}$ 降低缓存；实际还受对齐、块、并行切分和混合层影响。

## 4.1 分页而非连续预留

vLLM 把 token 位置映射到固定大小 block。scheduler 持有逻辑 block IDs，attention kernel 用 block table 找物理页。请求增长时按需分块，结束后回收到 pool，不要求为最大长度预留一段连续空间。

最后一个块可能未填满，形成内部碎片；block 越小碎片越低，但管理表、hash 和 kernel 元数据开销越高。调 block size 必须做端到端测试，不是越小越好。

`KVCacheManager` 是 scheduler 接口，coordinator 处理一个或多个 KV group，single-type manager 实现特定 attention 的分配/命中语义，底层 block pool 管理空闲与缓存块。这个分层比“一个 block manager”更能解释现代混合模型。

## 4.2 自动前缀缓存（APC）

完整 block 的 hash 一般由此前 block hash、当前 token、影响计算的附加信息组成。相同前缀可复用已计算 KV，命中只减少 prefill，不消除 decode，也不保证低 TTFT：hash 查找、排队和 cache eviction 仍存在。

观测应同时报告 request hit、命中 token 数、节省的 prefill 工作量和 eviction。前缀顺序、chat template、工具描述或 multimodal hash 变化都会使看似相同的文本 miss。安全上必须保证租户/adapter/模型身份进入隔离或 hash 语义。

## 4.3 抢占与回收

当新 token 需要 block 而 pool 不足，调度器可能抢占请求并在之后重算。高 KV 使用率伴随重复 prefill 时，吞吐和尾延迟会同时崩塌。应联看 cache usage、preemption、waiting queue 与 recomputed tokens。降低 `max_num_seqs`、限制长度、增加副本或缓存空间，可能比继续追求满显存更稳。

## 4.4 混合注意力为何困难

现代模型会交错 full attention、sliding-window/local attention、Mamba/线性 recurrent state，甚至 KV sharing。它们的保留规则不同：

- full 层需要完整历史；
- sliding window 只需最近窗口，但跨请求前缀命中仍需正确的边界；
- Mamba 保存固定/分块状态，其每层 state 大小可能远大于 attention 单 token KV；
- shared-KV 层不应重复分配。

当前设计把同类型层组成 KV cache group，并让组拥有相同物理 page size。规则整齐时按层数比例分组；不整齐时按启发式填 padding；attention 与 Mamba state 尺寸不同时，可能放大 attention block size 或填充状态。代价是 padding、较大 block 和更复杂的 prefix 交集。

## 4.5 混合前缀命中

full attention 从左向右找最长连续命中；sliding-window 可从候选边界向左验证最近窗口。整个模型能跳过的 prefix 是各 group 可复用范围的交集，而非任一组最大值。当前源码中 `HybridKVCacheCoordinator`、`UnitaryKVCacheCoordinator` 与无-prefix coordinator 分担这些场景；新模型不能仅因“有 backend”就假定 APC 完整可用。

## 4.6 容量估算与验证

粗略并发 token 容量：

$$T_{cap}\approx \frac{M_{device}-M_{weights}-M_{runtime}-M_{graphs}}{M_{token}}$$

TP 往往切分 KV heads，PP 切分层，DP 则复制权重和 cache；DCP/PCP 有各自布局，不能直接把容量乘 world size。最终以启动日志中的 blocks、压力下 cache usage 和真实长短分布校准。

建议实验：构造 90% 共享 system prompt、完全随机 prompt、混合长短三组 workload；比较 APC 开关下 TTFT、computed token、hit token 和 preemption。若只比较总 token/s，会错过 APC 真正的适用边界。

> **热点结论**：混合注意力不是换一个 kernel；它同时改变状态表示、页尺寸、保留规则、prefix 语义与调度预算。
