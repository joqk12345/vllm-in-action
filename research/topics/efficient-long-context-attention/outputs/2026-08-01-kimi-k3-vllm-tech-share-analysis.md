# Kimi K3 vLLM 技术分享：材料拆解与 topic 融合决策

Owner: 未指定
Purpose: 拆解新增 PDF、SRT 与链接说明，判断 topic 归属，并把可核验命题映射到当前 claim spine、实验和章节交接。
Status: captured
Applies to: Kimi K3；vLLM main merge commit `aeeb36b1f17145975c6713242f2447bb8b98782b`；官方博客 2026-07-27；本地材料捕获于 2026-08-01
Evidence grade: A/B/D 混合；PR/commit 为 A，官方博客/RFC 为 B，本地 slides/ASR 为 D
Verified date: 2026-08-01
Assumptions: 不把自动字幕当权威引文；不把 day-0 镜像可用性等同于稳定 release 支持。
Open questions: 首个稳定 release、镜像 digest、FlashInfer 稳定依赖、HF revision、partial-hit/KDA state 的本仓复现。
Handoff: 当前 topic booklet；第 04、08、09、11、12、13、15 章。

## 1. 融合决策

**结论：并入 `efficient-long-context-attention`，不新建 topic。**

新增材料回答的核心问题正是当前专题缺口：KDA 从论文中的 recurrent-state 机制进入 vLLM serving 后，如何改变 cache layout、prefix-cache 语义、调度边界、speculative decoding correctness 和 kernel 优化。它不是一个独立于“高效长上下文注意力”的 Kimi K3 产品专题。

采用“主 topic + case study 纵切面”结构：

| 内容 | 处理 | 原因 |
|---|---|---|
| KDA state、hybrid allocator/cache manager、block-aligned scheduling、partial cache hit | 纳入当前 topic 主线 | 直接改变长上下文 state/KV memory、TTFT、cache hit 与 correctness |
| KDA decode/prefill kernel、metadata builder | 纳入实现/实验主线 | 决定理论线性复杂度能否转化为实际 ITL/TTFT |
| DSpark 与 KDA rollback/state checkpoint | 作为跨专题接口 | 只保留 KDA correctness/状态管理部分；通用 speculative decoding 另有更大问题域 |
| LatentMoE、TP/EP、PD disaggregation、MXFP4 | 只做章节/专题交叉链接 | 它们影响端到端性能，但不是 attention 机制本体 |
| 多模态、chat template、模型质量排行榜 | 不进入本 topic 主体 | 与当前共同研究问题关联弱 |

只有在后续材料持续扩展到 Kimi K3 的完整多模态、LatentMoE、quantization、frontend、部署拓扑和运维生命周期时，才建议新建 `kimi-k3-production-serving`；当前三份材料尚不满足这个拆题条件。

## 2. 原始材料清单与证据边界

| 材料 | 最适合回答 | 不能证明 |
|---|---|---|
| `Kimi K3 vLLM Tech Share.pdf`，23 页 | 系统设计图、术语、分享结构 | 发布日期、代码版本、稳定 release、benchmark 可复现性 |
| `vLLM day-0 Kimi K3支持…srt`，约 95 分钟 | 设计动机、Q&A、潜在失效边界 | 精确术语、权威引文、数值事实 |
| `k3_info.txt` | 官方博客、recipe、PR 的导航入口 | 链接内容本身的真实性或版本状态 |
| vLLM 官方博客 | day-0 功能范围与作者报告 benchmark | 本仓复现、稳定 release 边界 |
| PR #50000 / merge commit | `main` 中的模型注册、代码和 tests | wheel/image/release 的完整可用性 |
| RFC #45702 + 相关 PR | partial cache hit 的设计、不变量和动态问题 | RFC 中所有选项都已成为稳定默认 |

Rights note: 本地 PDF/SRT 的再分发授权未确认；保留为 raw evidence，不复制大段原文到可发布正文。

## 3. 演讲时间轴拆解

| 时间 | 主题 | 抽取命题 | 上游核验 |
|---|---|---|---|
| 00:02–00:08 | 架构与性能概览 | K3 将 KDA、MLA、LatentMoE 放在同一模型；低并发性能是优化目标 | 架构由 K3 技术报告/官方博客支持；talk 数字需隔离 |
| 00:08–00:11 | KDA state | recurrent state 原地覆盖，打破“KV 连续增长且 append-only”的引擎假设 | 与技术报告 §5.4 和官方博客一致 |
| 00:11–00:16 | hybrid allocator/manager | 同一物理 tensor 支持不同逻辑 cache view；各 manager 汇报共同命中边界 | PR #50000 的 KV-cache interface/scheduler/model 路径提供实现入口 |
| 00:16–00:28 | block-aligned scheduling | chunked prefill 在物理 block 边界保存 KDA/Mamba state；block size 不是越大越好 | 与 vLLM hybrid/Mamba cache 设计及 RFC #45702 动机一致 |
| 00:28–00:38 | partial cache hit | KDA state 与 MLA cache 尺寸悬殊使物理 block 达 6K+ token；`hash_block_size` 解耦命中粒度并用 copy-on-write 延伸 partial tail | RFC #45702；PR #45939/#46384/#49502 已合入 |
| 00:38–00:41 | selective retention / PD risk | system prompt 和 turn boundary 是高价值 checkpoint；tensor reuse 需清零，zeroing 与 RDMA 写存在并发风险 | 官方博客讨论 selective retention、PD tail zeroing；需本仓 correctness test |
| 00:43–00:57 | 低并发 kernels | PDL、专用小 batch GEMM、LatentMoE tail fusion 优化单用户 latency | 官方博客提供 KDA/metadata/LatentMoE 优化与条件；不归因于 KDA 单项 |
| 00:57–01:35 | Q&A | H 系列兼容、TP/EP、DSpark 随 batch/workload 变化、依赖未 ready、1M decode 未测 | 多数为动态/口头判断，只转成验证任务 |

## 4. 系统链路拆解

```text
KDA recurrent update
  → state 不能按 token 任意 rollback
  → full-attention KV 与 KDA state 的分配单位不一致
  → hybrid allocator / cache coordinator 对齐物理 page
  → 对齐导致很大的物理 block 与很粗的 prefix-hit granularity
  → block-aligned scheduling 在合法边界物化 state checkpoint
  → partial cache hit 用更细 hash boundary + alias + hit_length
  → 从 partial hit 延伸时执行 copy-on-write
  → eviction/reset/offload/PD 必须清理 alias、复制有效 slice、清零尾部
  → benchmark 同时测 TTFT、hit rate、state memory、ITL 与 correctness
```

这条链路是新增材料对本 topic 最有价值的贡献：它把“固定大小 recurrent state 节省 KV memory”校正为一个带有调度、checkpoint、copy-on-write、eviction 和分布式传输代价的完整 serving 命题。

## 5. 命题拆解与 claim spine 映射

| 新 claim | 类别 | 证据 | 结论边界 |
|---|---|---|---|
| EA-C22 | implementation-support | PR #50000 / merge commit，A | 仅证明 `main` 合入；v0.26.0 不包含；稳定 release 未确认 |
| EA-C23 | system-design | RFC #45702 + merged PRs，A/B | partial hit 已有实现组成，但 RFC/open questions 仍动态 |
| EA-C24 | benchmark-observation | 官方博客，B | 只适用于 GB300 NVL72、TP8/TP16、batch 1、指定 DSpark/SPEED Bench |
| EA-C25 | evidence-boundary | local slides/SRT + 官方博客，B/D | talk 的 410/464 与博客 331/370 不可混用 |

原有 EA-C19/20/21 继续承担 KDA-aware prefix cache、spec decode rollback、FlashKDA/context parallelism；新增 claims 不复制技术报告，而是补上 vLLM 实现与版本边界。

## 6. 关键冲突与无效泛化

### 6.1 性能数字冲突

- 本地 SRT 约 00:04 报告 TP8 + DSpark 约 410 tok/s、TP16 约 464 tok/s，slides 标题写 460 tok/s。
- 2026-07-27 官方博客报告 GB300 NVL72、batch size 1：TP8 111→331 tok/s/user，TP16 118→370 tok/s/user。

两组数字缺少同一代码 commit、GPU 拓扑、frequency、dataset、input/output distribution 和 DSpark 配置对齐。处理规则：官方博客数字可作为 B 级作者报告；talk 数字仅作后续优化线索。

### 6.2 `day-0` 不是 stable release

- 最新稳定 release 为 v0.26.0，发布时间早于 PR #50000 的 2026-07-30 merge。
- PR 明示使用专用 `vllm/vllm-openai:kimi-k3` 镜像，且仍需 FlashInfer `v0.6.16rc5`。

因此当前状态应写成：`roadmap_status: checked/implemented signal`、`release_status: unverified`、`local_test_status: not-run`，而不是 `supported: true`。

### 6.3 不能把端到端收益归因于 KDA

370 tok/s/user 的链路同时包含 DSpark、KDA kernels、metadata builder、low-latency GEMM、LatentMoE tail fusion、并行/通信和硬件特性。KDA 只解释其中 attention/state 的一部分。

## 7. 详细验证分解

### Phase A：版本与依赖固定

1. 固定 PR #50000 merge commit 与四个拆分 PR commit。
2. 固定 `vllm/vllm-openai:kimi-k3` 镜像 digest，而不是浮动 tag。
3. 固定 FlashInfer `v0.6.16rc5` 或后续稳定版本、CUDA/driver/NCCL。
4. 固定 `moonshotai/Kimi-K3` 与 `Inferact/Kimi-K3-DSpark` HF revisions。
5. 记录首个包含 Kimi K3 的稳定 vLLM release；若尚无，则明确 main-only。

### Phase B：静态能力核查

1. registry/supported-models：`KimiK3ForConditionalGeneration`。
2. KDA/MLA layer mapping 与 cache group 构建。
3. `hash_block_size`、partial alias、`hit_length`、copy-on-write 和 eviction cleanup。
4. DSpark config、KDA state verification/replay 路径。
5. NIXL/PD connector 的 logical-to-physical mapping 与 tail zeroing。

### Phase C：correctness smoke tests

| Test | Workload | Oracle | 通过条件 |
|---|---|---|---|
| cold vs warm prefix | 相同 system prompt，不同 user tail | logits/output equivalence | 命中不改变结果；命中长度正确 |
| partial-tail extension | 共享 prefix 落在物理 block 内 | no-cache baseline | copy-on-write 后旧/新请求互不污染 |
| eviction/reuse | 强制 block eviction 后复用 | sanitizer + output comparison | 无 stale alias、NaN、旧 token 泄漏 |
| PD transfer | prefill/decode 不同 block mapping | non-disaggregated baseline | padding/tail 被正确清零，无 race |
| DSpark rejection | 构造低 acceptance workload | non-spec decode | rejection 后 KDA state 与基线一致 |
| multimodal boundary | image tokens + text continuation | non-cache baseline | cache boundary 不跨越不合法 multimodal state |

### Phase D：性能矩阵

记录完整 benchmark gate：

```text
vLLM commit/image × HF revision × FlashInfer
× GPU/driver/interconnect × MXFP4/FP8 cache
× TP/DP/EP/DCP × prefix caching/partial hit
× DSpark on/off × input/output distribution
× concurrency/arrival rate × cold/warm cache
× TTFT/ITL/E2E/tok-s-user/TPGS/cache-hit/HBM
```

至少包含：短 prompt 控制组、8K/1K random、长 system prompt、多轮 agentic/tool-call trace、低/高 entropy 输出、32K/128K/1M 长度分层。1M 能加载不等于 1M TTFT/ITL/质量已经验证。

### Phase E：生产 canary 与 rollback

1. Canary 仅导入固定镜像 digest 和固定 HF revisions。
2. 观察 partial-hit rate、recompute tokens、TTFT p50/p99、NaN、cache eviction、NIXL/RDMA error、DSpark acceptance。
3. 关闭顺序：DSpark → partial-hit/prefix cache → PD disaggregation → K3 专用 kernel。
4. 回退目标：已验证的 full-attention/其他模型服务，而不是假设 Kimi K3 有等价 full-attention mode。

## 8. 下游落点

- 第 04 章：KV cache 与 recurrent state cache 的语义差异。
- 第 08 章：TP/DP/EP/DCP、PD transfer 和 hybrid cache group。
- 第 09 章：cache-aware workload 与 speculative acceptance benchmark。
- 第 11 章：KDA prefill/decode、metadata、TTFT/ITL。
- 第 12 章：state checkpoint、重算、缓存命中和硬件成本模型。
- 第 13 章：partial-hit、stale alias、NaN、PD/RDMA race 观测。
- 第 15 章：main-only/RC 依赖、canary 和 rollback。

当前没有 chapter-handoff、figures 或 slides 子目录中的成品需要标记 `needs-refresh`；booklet、reading list、seminar guide 和 capability matrix 在本次同步刷新。
