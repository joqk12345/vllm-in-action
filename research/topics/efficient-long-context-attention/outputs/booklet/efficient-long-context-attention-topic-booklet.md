---
title: "高效长上下文注意力"
subtitle: "主题研究小册子"
status: draft
edition: "0.2"
created: 2026-07-26
verified: 2026-08-01
topic: efficient-long-context-attention
applies_to: "vLLM v0.26.0 Kimi Linear/Qwen3-Next；Kimi K3 main@aeeb36b1，稳定 release 尚未确认"
source_ids:
  - SRC-kimi-linear-paper-v2
  - SRC-kimi-k3-tech-report-2026-07-28
  - SRC-vllm-kimi-k3-support-pr-50000
  - SRC-vllm-kimi-k3-day0-blog-2026-07-27
  - SRC-vllm-partial-cache-rfc-45702
chapters: ["04", "08", "09", "11", "12", "13", "15"]
---

# 高效长上下文注意力专题小册子

Owner:
Purpose: 将 sparse、linear、GDN/KDA、Lightning、SWA/full attention 反例和 vLLM 支持状态组织成可维护的研究小册子。
Status: draft
Applies to: research/topics/efficient-long-context-attention
Evidence grade: A/B 为正文候选；C/D 仅作解释、发现和待核查问题。
Verified date: 2026-08-01
Assumptions: 论文 benchmark 均为作者报告；生产建议必须回到固定 vLLM release、源码/测试和本仓实验。
Open questions: NSA/MoBA/MiniMax-01、Qwen3.5 config、GLM-5/DSA vLLM 支持、Kimi/Qwen smoke test、Kimi K3 首个稳定 release 与 partial-hit correctness。
Handoff: book/chapter-briefs/09, 11, 12, 15；与 `llm-d-agentic-serving` 交叉。

## 1. 如何使用本小册子

稳定主体按共同问题综合论文、config、vLLM 固定 tag/commit 和反例；不要按单篇来源顺序阅读。易变的 release、RFC、镜像依赖和测试状态以 `capability-matrix.yml` 为第一检查点，并在动态附录记录。

建议顺序：先读共同问题与最小概念系统，再用跨来源命题检查结论，最后根据目标 workload 进入测试、canary 和 rollback。`roadmap_status`、`release_status`、`local_test_status` 必须分别判断；任一状态不推出另外两个状态。

## 2. 执行摘要

当前最可靠的工程结论是：高效 attention 的收益从来不只是复杂度变化。Kimi K3 把这一点具体化——固定大小 KDA recurrent state 降低随序列增长的 KV 压力，却引入 state checkpoint、hybrid page alignment、粗粒度 prefix hit、copy-on-write、speculative rejection 和 PD transfer correctness。

最危险的泛化是把 `main`/专用镜像的 day-0 支持写成稳定 release 能力，或把 DSpark + kernels + LatentMoE + 并行共同产生的 tok/s 数字归因于 KDA。

下一项验证动作是固定 Kimi K3 镜像/FlashInfer/HF revisions，确认首个稳定 release，然后先跑 partial-tail、eviction/reuse、PD tail zeroing 和 DSpark rejection correctness，再跑性能矩阵。

## 3. 共同研究问题

1. 哪些 long-context workload 真正受 attention 复杂度限制，而不是受 MoE、通信、调度或 I/O 限制？
2. Sparse、linear/GDN/KDA、Lightning、SWA 与 full attention hybrid 分别在哪些任务上退化？
3. vLLM 中的 supported model、kernel test、HF config 和端到端 serving 成功之间相差哪些验证层？
4. 如何用 benchmark 同时覆盖质量、TTFT、ITL、throughput、state/KV memory 和成本？
5. KDA/Mamba recurrent state 打破 append-only KV 假设后，allocator、scheduler、prefix cache、offload 和 speculative decoding 必须建立哪些新不变量？

## 2. 一句话结论

高效长上下文注意力不是单一算法路线，而是一个工程选择空间：dynamic sparse、linear/GDN/KDA、Lightning、SWA、block routing 和 full-attention hybrids 都在试图降低长上下文 prefill/decode/state 成本；但能否用于 vLLM 生产服务，取决于 **质量退化边界、kernel/backend、state/KV layout、prefix cache 支持、模型 config、workload 分布和固定 release 的实际测试**。

## 3. 当前证据地图

| 路线 | 代表来源 | 当前证据 | 主要边界 |
|---|---|---|---|
| DSA / dynamic sparse | GLM-5 v2 | 论文报告 DSA、indexer/top-k、KV reuse/routing 线索 | DeepSeek NSA/DSA 原文和 vLLM 支持未补齐 |
| KDA / hybrid linear | Kimi Linear v2 + vLLM v0.26.0 | KDA 扩展 GDN；KimiLinearForCausalLM 已在 vLLM v0.26.0 出现 | 未本地 serving；HF revision 未固定 |
| GDN / gated delta rule | Gated DeltaNet v3 + Qwen3-Next config | GDN = gate + delta rule；Qwen3-Next 48 层默认 36 GDN/linear + 12 full | Qwen3.5 config 未固定；backend 未实测 |
| Lightning Attention | MiniMax-M1 v1 | 作者报告 1M context、40K/80K thinking budget、test-time compute 效率 | MiniMax-M1 vLLM/HF config 未核查 |
| Full attention counterexample | MiniMax-M2 v1 | M2 回到 full attention + GQA；hybrid SWA 在长上下文/多跳任务退化 | 只适用于 MiniMax 作者设置，不能泛化 |
| Kimi K3 serving case | K3 technical report + vLLM blog + PR #50000 + RFC #45702 | KDA/MLA hybrid cache、partial hit、DSpark/KDA state、main merge 已建立 | v0.26.0 不包含 K3；首个稳定 release、本仓 correctness/性能未验证 |

## 4. 最小概念系统

最小概念系统由六个 nouns 和五个 verbs 组成：

- nouns：full attention、sparse attention、linear recurrent state、GDN/KDA state、hybrid attention、KV/state cache；
- verbs：select、gate、update、interleave、benchmark。

判断一个方法时，必须同时回答：它选择什么信息、如何更新状态、哪些层保留 full attention、vLLM 如何缓存/调度、用什么任务验证质量。

## 5. 核心概念

### 3.1 Sparse attention

Sparse attention 保留 softmax attention 的语义框架，但只选择部分 token/block/KV entry 参与计算。GLM-5 中的 DSA 线索提示 dynamic sparse 可能引入 indexer/top-k selection，从而把瓶颈转移到选择、kernel、确定性和硬件支持上。

### 3.2 Linear attention / recurrent state

Linear attention 用递归状态或核化形式替代二次 attention 矩阵。优点是 decode state 可以不随上下文线性增长；风险是有限状态可能在精确检索、多跳推理和 in-context learning 上丢信息。

### 3.3 GDN 与 KDA

Gated DeltaNet 把两类机制结合：

- gating：快速遗忘/清空旧信息；
- delta rule：定向更新 key-value association。

Kimi Linear 论文把 KDA 描述为扩展 GDN 的模块，引入更细粒度 gating。Qwen3-Next/Qwen3.5 在 vLLM v0.26.0 中有 QwenGatedDeltaNetAttention 路径。

### 3.4 Hybrid attention

Hybrid 是当前主流工程形态：用大多数 linear/GDN/KDA/Lightning/SWA 层降低成本，再周期性插入 full attention 层保留全局信息流。例如：

- Kimi Linear Instruct config：27 层中 20 KDA + 7 full MLA；
- Qwen3-Next config：48 层默认每 4 层 full attention，即 36 linear/GDN + 12 full；
- MiniMax-M2 反例：作者报告最终选择 full attention + GQA。

### 3.5 Hybrid KDA/MLA cache

Kimi K3 让 hybrid attention 从“层如何交错”扩展到“cache 如何共同恢复”。MLA KV 随 token 增长，KDA 保存固定大小 recurrent state；两者必须在同一 prefix boundary 都可恢复，命中才有效。

物理 page 对齐简化统一分配，却会因 KDA state 与压缩 MLA KV 尺寸悬殊而产生很大的物理 block。partial cache hit 因此把 hash granularity 与物理 block size 解耦，并引入精确 `hit_length`、alias、copy-on-write 和 state checkpoint。它改善命中机会的同时扩大 correctness surface。

## 6. 跨来源命题

- EA-C01：本专题应覆盖 efficient long-context attention，而不是只覆盖 linear attention。
- EA-C09/EA-C16：KDA 与 GDN 存在机制继承关系，但不能混同实现。
- EA-C12/EA-C17：vLLM v0.26.0 已有 Kimi Linear 和 Qwen3-Next/GDN 支持路径，但尚未本仓端到端验证。
- EA-C15：MiniMax-M2 是 full attention 回归反例，校正“低复杂度必然更好”的叙述。
- EA-C22：Kimi K3 已合入 vLLM `main`，但晚于 v0.26.0；稳定 release 尚未确认。
- EA-C23：partial-hit 相关 PR 已合入，但 final-tail checkpoint/same-step reuse 仍是开放设计。
- EA-C24/EA-C25：官方博客 benchmark 必须保留硬件/workload 边界；talk 的更高 tok/s 数字只作冲突线索。

## 7. 来源如何相互校正

- Kimi Linear 和 MiniMax-M1 提供 efficient attention 正例；MiniMax-M2 提供失败/回退边界。
- GDN 论文解释 KDA/Qwen GDN 的机制背景；HF config 和 vLLM 源码校正论文中的概括比例。
- 访谈和知乎链接只能发现问题；论文、config、vLLM tag 和实验决定正文事实。
- Kimi K3 技术报告解释算法—系统协同，vLLM 博客给出官方 deployment/benchmark 叙述，PR/commit 确认代码状态，RFC 暴露仍未稳定的设计选择；本地 slides/SRT 只补充讲解路径。

## 8. 三个正例与一个反例

### 4.1 Kimi Linear：KDA 正例

Kimi Linear 论文报告 KDA 扩展 GDN，并在作者设置中减少 KV cache、提升长上下文 decode throughput。vLLM v0.26.0 已静态观察到 KimiLinearForCausalLM 和 KDA path。正文写作时必须区分：

- 论文 claim；
- HF config claim；
- vLLM source support claim；
- 本仓实验 claim。

### 4.2 Qwen3-Next：GDN serving path

Qwen3-Next HF config 和 vLLM v0.26.0 显示默认每四层一个 full attention，其他层走 linear/GDN path。它是理解 vLLM 对 GDN-family model 支持的关键样本。

### 4.3 MiniMax-M1：Lightning 与 long-output / RL rollout

MiniMax-M1 把 efficient attention 的价值从长输入扩展到长输出和 test-time compute。它报告 1M context、40K/80K thinking budget 和 RL scaling 效率，但这些数字不能直接写成 vLLM production cost。

### 4.4 MiniMax-M2：full attention 反例

MiniMax-M2 论文报告 M2 回到 full attention + GQA，并指出 hybrid SWA 在长上下文 retrieval、多跳推理、in-context learning 和 >32K agent tasks 中存在风险。这个反例非常重要：复杂度更低不等于质量可接受。

### 4.5 Kimi K3：从 KDA 机制到 vLLM serving

Kimi K3 是本专题的系统纵切面。它展示的因果链不是“线性 attention → 更快”，而是：recurrent state → hybrid allocator/page alignment → 粗物理 block → block-aligned checkpoint → partial prefix hit/copy-on-write → eviction/offload/PD correctness → KDA/metadata/DSpark 低延迟优化。

版本边界必须写清：PR #50000 于 2026-07-30 合入 `main`，晚于 v0.26.0；PR 当日仍要求专用 `kimi-k3` 镜像和 FlashInfer `v0.6.16rc5`。因此它目前是 main/special-image case study，不是 v0.26.0 production recommendation。

## 9. Benchmark 设计原则

1. **长度分层**：32K 持平不代表 128K/1M 仍安全。
2. **任务分层**：MMLU/MATH 不能替代 RULER、HELMET、RepoQA、MTOB、agentic traces。
3. **阶段分层**：pretraining、SFT、RL/post-training 后风险可能不同。
4. **指标分层**：TTFT、ITL/TPOT、throughput、KV/state memory、goodput 和质量要同时记录。
5. **实现分层**：同一论文算法在不同 vLLM tag、backend、dtype、TP/DP 上可能行为不同。
6. **缓存状态分层**：cold/warm、full/partial hit、system prompt/turn boundary、eviction/reuse、PD transfer 必须分别测。
7. **spec decode 分层**：记录 dataset entropy、acceptance、draft length 和 KDA rejection 后的 state correctness。

## 10. 实验与验证计划

优先实验：

1. vLLM v0.26.0 Kimi Linear import/config/layer smoke test；
2. vLLM v0.26.0 Qwen3-Next GDN backend smoke test；
3. KDA/GDN kernel precision test；
4. 32K/128K retrieval + long-output reasoning + agentic trace serving benchmark；
5. 记录 TTFT、ITL/TPOT、throughput、state/KV memory、失败日志。
6. 固定 Kimi K3 main/image/FlashInfer/HF revisions，运行 partial-tail extension、copy-on-write、eviction/reuse、PD tail-zeroing 与 DSpark rejection correctness。
7. 对齐官方博客 GB300 NVL72、TP8/TP16、batch 1 baseline；talk 的 410/464 tok/s 不作为复现目标，除非补齐其 manifest。

## 11. 生产采用判断

生产采用某个 efficient attention 模型前，必须满足：

- 固定 vLLM release/tag；
- 固定 HF revision 和 config；
- 跑通 minimal serve；
- 在目标硬件和 workload 上通过质量与性能 benchmark；
- 明确 full attention fallback 或替代模型。
- 对 main-only/RC 依赖模型，固定镜像 digest、依赖 lock 和退出条件；不要把浮动 day-0 image 直接纳入生产升级通道。

## 12. 章节落点

- 第 04 章：KV cache、state cache、linear recurrent state 与 full attention KV 的差异。
- 第 08 章：TP/DP/EP 拓扑如何影响 attention state 和 KV reuse。
- 第 09 章：长上下文 benchmark 设计和反例。
- 第 11 章：TTFT/ITL 优化、prefill/decode path、kernel/backend。
- 第 12 章：成本模型，特别是 long-output/test-time compute。
- 第 13 章：观测 GDN/KDA/DSA backend、state memory、prefix cache hit。
- 第 15 章：升级、回退和模型选型边界。

## 13. 结论分层

- A 级：固定源码/config/vLLM tag 中可直接观察到的模型类、layer path、config 字段。
- B 级：论文作者报告的机制、benchmark、消融和反例。
- C 级：技术博客用于解释算法背景。
- D 级：访谈、知乎、seed list 只用于发现问题。

## 14. 未决问题

1. NSA/MoBA/MiniMax-01 原文和 source cards 未补齐。
2. Qwen3.5 具体 HF config 未固定。
3. Kimi Linear/Qwen3-Next vLLM v0.26.0 smoke test 未运行。
4. GDN/MiniMax-M2 表格需 PDF 人工复核。
5. GLM-5/DSA 是否有 vLLM 支持路径未核查。
6. Kimi K3 首个稳定 vLLM release、镜像 digest、FlashInfer 稳定依赖和 HF revisions 未固定。
7. Partial-hit final-tail checkpoint、same-step reuse、PD zero/RDMA race 尚未本仓验证。

## 15. 当前不可写成正文事实的内容

- Kimi Linear 的作者报告加速可直接在 vLLM v0.26.0 复现。
- Qwen3.5 的 GDN 配置等同于 Qwen3-Next Instruct。
- MiniMax-M2 证明所有 efficient attention 都不如 full attention。
- 访谈或知乎文章中的公司路线判断可作为事实。
- NSA/MoBA/MiniMax-01 已完成验证。
- Kimi K3 属于 vLLM v0.26.0 稳定支持，或官方 day-0 tok/s 可脱离 GB300/TP/batch/DSpark 条件复现。
- 本地 SRT 的 410/464 tok/s 比官方博客 331/370 tok/s 更新或更权威。

## 16. 动态附录

动态状态：

- roadmap_status：researching；
- release_status：v0.26.0 已捕获 Kimi Linear/Qwen3-Next；Kimi K3 `main@aeeb36b1` 已合入但首个稳定 release 未确认；
- local_test_status：not_run；
- Kimi K3 dependency：专用镜像 + FlashInfer RC，待固定 digest/稳定版本；
- stale_after：2026-09-01。

刷新条件见 `outputs/deliverables.yml`。

## 17. 研讨结论模板

```text
Decision:
Applies to:
Evidence used:
Rejected alternatives:
Required vLLM tag/config:
Required benchmark:
Failure boundary:
Fallback:
Owner:
Next review date:
```

## 18. 下一步

1. 基于 vLLM v0.26.0 跑 Kimi Linear 和 Qwen3-Next smoke test。
2. 固定 HF revision 和模型 config。
3. 补齐 NSA、MoBA、MiniMax-01 source cards。
4. 抽取 GLM-5/DSA 和 GDN/KDA 的更多表格设置。
5. 形成 chapter handoff：第 09 章 benchmark 反例 + 第 11/12 章 serving cost model。
6. 固定并验证 Kimi K3 image/FlashInfer/HF revisions，确认首个稳定 release；优先跑 correctness，再跑性能。
