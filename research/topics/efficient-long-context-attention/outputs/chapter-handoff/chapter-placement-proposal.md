# 高效长上下文注意力与 Kimi K3 Serving 正文落点建议

Owner: 未指定
Purpose: 保存高效长上下文注意力专题，特别是 Kimi K3/KDA serving 案例进入《vLLM 工程实践》正文的编辑判断、章节分工与证据门禁。
Status: proposal — awaiting decision
Applies to: 当前 `book/toc.yml`、`book/spine.yml`、chapter briefs，以及截至 2026-08-01 的 Kimi K3/KDA/vLLM 研究材料
Evidence grade: editorial judgment；技术 claim 以 `claims.yml` 和 Source ID 为准
Verified date: 2026-08-02
Assumptions: 维持现有 16 章结构；不新增 Kimi K3 独立章节；正式正文尚未创建。
Open questions: 是否批准本落点；各章篇幅；Kimi K3 首个稳定 release、镜像/HF revisions 和本仓 correctness/performance 何时补齐。
Handoff: 第 04、08、09、10、11、12、13、15、16 章。

## 1. 决策状态

本文件只保存编辑判断，不表示已经批准进入正文。

- 未修改 `book/chapter-briefs/`；
- 未创建或修改 `book/chapters/`；
- 未把 Kimi K3 main/special-image 支持写成稳定 release 能力；
- 未把官方博客或技术分享的性能数字升级为本书性能结论；
- 未决定 Kimi K3 是否作为第 16 章贯穿案例。

## 2. 总体判断

新增材料不应写成“Kimi K3 模型介绍”，而应呈现为一个系统工程案例：

> 当注意力从 append-only KV cache 变成会被覆盖的递归状态后，推理引擎为了恢复 prefix reuse、推测解码和分布式传输语义，需要付出哪些调度、缓存和正确性代价？

Kimi K3 是该问题的案例，不是正文的组织中心。耐久主线是：

```text
固定大小 recurrent state
  → 降低随上下文增长的 KV 容量压力
  → 失去任意 token 边界的天然 rollback
  → 必须物化 state checkpoint
  → KDA state 与 MLA KV 必须联合命中
  → page alignment 可能产生超大物理 block
  → prefix cache 命中粒度变粗
  → 需要 partial hit、alias、hit_length 与 copy-on-write
  → eviction/offload/PD/spec decode 扩大 correctness surface
```

## 3. 章节映射

| 内容 | 主/辅位置 | 正文职责 | 建议篇幅 |
|---|---|---|---:|
| KV cache 与 recurrent state cache 的语义差异 | 第 04 章，主 | 建立 append-only KV、原地 state update、rollback/checkpoint 心智模型 | 4–6 页 |
| Hybrid cache 与联合命中边界 | 第 04 章，主 | 解释 KDA state 与 MLA KV 为什么必须在同一 prefix boundary 恢复 | 包含在上项 |
| Block-aligned chunked prefill / state checkpoint | 第 10 章，主 | 解释 cache 语义如何改变 scheduler chunk boundary | 2–3 页 |
| Partial cache hit / copy-on-write | 第 10、11 章 | 第 10 章讲调度和所有权；第 11 章讲 TTFT 收益与代价 | 2–3 页 |
| KDA prefill/decode、metadata builder | 第 11 章，主案例 | 说明理论复杂度如何受 kernel、launch 和 metadata 影响 | 2–3 页 |
| DSpark rejection 与 KDA state | 第 11 章；交叉投机解码专题 | 只讲 state correctness，不重复 drafter 基础机制 | 1–2 页 |
| 331/370 vs 410/464 tok/s | 第 09 章，反例框 | 演示缺失 manifest 的数字为什么不可比较 | 1 个案例框 |
| TP/EP/DCP、KV/state 复制与互联 | 第 08 章，辅助 | 用作并行与内存复制的具体案例 | 0.5–1 页 |
| 吞吐、缓存命中与单位成本 | 第 12 章，辅助 | 说明减少 KV growth 不等于降低端到端成本 | 0.5–1 页 |
| partial-hit/stale alias/PD 指标 | 第 13 章，辅助 | 转化为最小观测信号 | 0.5–1 页 |
| main/special image/RC/stable release | 第 15 章，主案例 | 展示 release、merge、镜像、依赖和 local test 必须分开 | 1–2 页 |
| Kimi K3 端到端上线案例 | 第 16 章，候选 | 仅在本仓完成可复现实验后考虑 | 暂缓 |

## 4. 第 04 章：主机制叙事

建议新增一节：

```text
从 KV Cache 到 Attention State

1. Full attention 为什么天然适合 append-only KV cache
2. Recurrent attention 用固定状态换掉了什么
3. 固定大小状态为什么不等于“免费缓存”
4. Hybrid attention 为什么需要联合命中边界
5. 物理 block size 与 prefix hash granularity
6. Kimi K3：KDA–MLA hybrid cache 案例
7. 容量估算与失效边界
```

### 候选正文段落

> 标准自回归注意力会为每个历史 token 保留键和值。新 token 只在缓存尾部追加数据，已经写入的缓存不会被后续 token 修改。这种 append-only 语义使 prefix caching、回滚和按 block 复用相对直接：命中某个前缀，就意味着对应范围内的 KV 数据仍然有效。
>
> Kimi Delta Attention（KDA）采用不同的状态语义。它用固定大小的递归状态概括历史信息，每处理一个 token，旧状态都会被更新甚至覆盖。这降低了状态大小随上下文增长的压力，却失去了“任意历史边界都天然存在”的性质。要复用某个前缀，推理引擎必须事先在该边界保存状态快照。
>
> Kimi K3 又把问题推进了一步：模型同时包含 KDA 层和 MLA 层。一次 prefix hit 只有在 MLA KV 与全部 KDA state 都能恢复到同一 token 边界时才成立。为了统一分配，两类缓存可以共享物理内存池并对齐 page size；但当 KDA state 远大于压缩后的 MLA KV 时，对齐可能产生很大的物理 block，降低前缀命中的有效粒度。
>
> vLLM 的 partial cache hit 路线因此把物理分配粒度与哈希命中粒度分开：物理 block 仍负责内存所有权，更细的 hash boundary 用于定位可复用前缀；从一个未填满 block 的命中继续生成时，通过 copy-on-write 避免修改其他请求仍在引用的数据。[SRC-kimi-k3-tech-report-2026-07-28] [SRC-vllm-partial-cache-rfc-45702]
>
> 这个案例说明，线性或递归注意力减少的是一种内存增长方式，并没有消除缓存管理成本。状态快照、调度切分、复制、回收和分布式传输可能成为新的瓶颈与正确性边界。

版本敏感实现若进入正文，应标记：

```html
<!-- verified: vLLM commit aeeb36b1f17145975c6713242f2447bb8b98782b, 2026-08-01; stable release pending -->
```

在首个稳定 release 固定前，只能写成 fixed-commit case study，不能写成生产默认建议。

## 5. 第 10 章：状态检查点也是调度问题

第 10 章不重复 cache 容量模型，只回答 scheduler 问题：

```text
chunked prefill
  → 在合法 block/hash boundary 切分
  → forward 结束时物化 recurrent state
  → final-tail boundary 可能落在 scheduled chunk 内
  → scheduler split 或 backend checkpoint materialization
  → forward 次数、batching 与 kernel work 的权衡
```

稳定判断：

> 当 prefix reuse 依赖 recurrent state checkpoint 时，chunk boundary 不再只是性能参数，它也承载缓存正确性语义。

不应提前把 RFC 中的 final-tail 方案写成稳定默认；当前仍需保留 scheduler split 与 backend materialization 两种选择。

## 6. 第 11 章：Kimi K3 作为性能诊断案例

建议案例标题：

```text
案例：为什么“线性注意力”不自动等于更低延迟？
```

诊断顺序：

1. KDA recurrent state 是否降低 decode memory growth；
2. KDA prefill 的 recurrence 和 kernel 是否限制 TTFT；
3. 大物理 block 是否降低实际 prefix hit；
4. partial hit 的 copy/checkpoint/alias 成本；
5. metadata builder 与小 kernel launch overhead；
6. DSpark acceptance 与 rejection 后 state correctness；
7. 低并发收益是否在高并发下挤占 batch capacity。

这一节应围绕瓶颈定位，不写成优化清单或模型排行榜。

## 7. 第 09 章：不可比性能数字案例

建议只在 benchmark 章节呈现以下对照：

| 来源 | Commit/image | 硬件 | TP | Batch | Workload | DSpark | 结果 |
|---|---|---|---:|---:|---|---|---:|
| vLLM 官方博客 | 待固定 image digest | GB300 NVL72 | 8/16 | 1 | SPEED Bench | 开/关 | 111/331、118/370 tok/s/user |
| 本地技术分享 | 未披露 | 未完全固定 | 8/16 | 1 | 未完全披露 | 开 | 410/464 tok/s |

正文只能得出：

> 两组结果缺少统一的代码、硬件频率、输入输出分布和 DSpark 配置，不能据此判断哪一组更快或代表更新版本。

不得选择更高的一组数字写进摘要或模型介绍。

## 8. 图示建议

不直接复制技术分享 PDF，重新绘制 repo-native 图。

### 图 1：两种缓存语义

```text
Full attention: KV0 → KV1 → KV2 → append
KDA:            S0 → overwrite S1 → overwrite S2
```

放在第 04 章，用来解释 rollback/checkpoint 差异。

### 图 2：物理块与哈希粒度解耦

```text
physical block: |------------- 6144 tokens -------------|
hash boundary:  |--512--|--512--|--512--| ... |
partial hit:                    ↑ hit_length
extension:                      copy-on-write → new block
```

放在第 10 或第 11 章。数字只作为 Kimi K3 case illustration，并注明不能泛化。

## 9. 暂不进入正文

- “Kimi K3 达到 460 tok/s”等无完整 manifest 的标题数字；
- 自动字幕中的术语、数字和 Q&A 判断；
- KDA state 约 600× MLA cache、block size 6K+ 作为通用事实；
- KDA:MLA 3:1 作为通用最优比例；
- vLLM `main` 合入等同于稳定 release 支持；
- 把 DSpark、LatentMoE、PDL、MXFP4 和并行优化的联合收益归因于 KDA；
- 未固定 image/HF/dependency 前的生产启动命令；
- 未完成 correctness test 前的生产启用建议。

## 10. 进入正文前的证据门禁

1. 固定首个包含 Kimi K3 PR #50000 的稳定 vLLM release；
2. 固定 Kimi K3 image digest、FlashInfer、CUDA/driver/NCCL；
3. 固定 Kimi K3 与 DSpark HF revisions；
4. 完成 cold/warm prefix、partial-tail extension、copy-on-write、eviction/reuse 测试；
5. 完成 PD logical/physical mapping、tail zeroing 和 RDMA race 测试；
6. 完成 DSpark rejection 后 KDA state 与 non-spec baseline 一致性测试；
7. 对齐官方博客 benchmark，记录 TTFT、ITL、E2E、tok/s/user、TPGS、acceptance 和 HBM；
8. 至少完成一个低复用或高 entropy 反例；
9. 技术审校确认 cache/state/scheduler 术语；
10. 再决定是否把 Kimi K3 纳入第 16 章端到端 playbook。

## 11. 若批准后的执行顺序

1. 更新第 04、10、11、15 章 brief 的必须解释、必须包含和证据缺口；
2. 第 08、09、12、13 章只增加交叉案例契约，避免重复解释；
3. 重绘两张 cache/state 图；
4. 完成 correctness-first 实验；
5. 固定稳定 release 后撰写第 04 章主机制段落；
6. 将调度、性能、benchmark 和升级内容拆到对应章节；
7. 双重审阅通过后再把章节状态从 `brief` 推进到 `draft/review`。

## 12. 研究来源

- `EA-C18`–`EA-C25`：Kimi K3/KDA 架构、cache、spec decode、vLLM support 与 benchmark 边界。
- [SRC-kimi-k3-tech-report-2026-07-28]
- [SRC-vllm-kimi-k3-support-pr-50000]
- [SRC-vllm-kimi-k3-day0-blog-2026-07-27]
- [SRC-vllm-partial-cache-rfc-45702]
- `outputs/2026-08-01-kimi-k3-vllm-tech-share-analysis.md`
