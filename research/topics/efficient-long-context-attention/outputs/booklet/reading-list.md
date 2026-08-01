# 高效长上下文注意力阅读路径

Owner:
Purpose: 为 `efficient-long-context-attention` 提供分层阅读顺序，区分正文证据、机制背景和发现线索。
Status: draft
Applies to: research/topics/efficient-long-context-attention
Evidence grade: A/B 优先；C/D 仅辅助理解或发现。
Verified date: 2026-08-01
Assumptions: 读者熟悉 Transformer、KV cache、vLLM 基础。
Open questions: NSA/MoBA/MiniMax-01 尚未完成 source card。
Handoff: seminar-guide、topic booklet、chapter handoff。

## 0. 先读项目内骨架

Goal: 建立 claim/source/version 边界。Output: 写下一个目标 workload 和三个待验证 claim ID。

1. `claims.yml` — claim spine。
2. `vocabulary.md` — nouns/verbs。
3. `source/README.md` — source ID、校验和、版本边界。

## 1. 机制主线：GDN → KDA → Qwen/Kimi

Goal: 区分 GDN、KDA 与具体 checkpoint config。Output: 一张“机制—模型 config—vLLM layer path”映射。

1. `SRC-gated-deltanet-paper-v3` — Gated DeltaNet 论文。
   - 重点：gated delta rule、Table 2/3/4/5、chunkwise parallel algorithm。
2. `SRC-deltanet-explained-part-ii` — DeltaNet 算法博客。
   - 重点：为什么纯 RNN recurrence 需要 chunkwise parallelization。
3. `SRC-kimi-linear-paper-v2` — Kimi Linear 论文。
   - 重点：KDA extends GDN、3:1 hybrid、KV cache / decode throughput 作者报告。
4. `SRC-qwen3-next-hf-config-2026-07-26` + `SRC-vllm-qwen3-next-gdn-support-v0-26-0`。
   - 重点：Qwen3-Next 36 linear/GDN + 12 full attention；vLLM v0.26.0 GDN path。

## 2. 正反案例：Lightning 与 full attention 回归

Goal: 用正反案例校正“复杂度更低必然更好”。Output: 一条带反例和适用范围的工程判断。

1. `SRC-minimax-m1-paper-v1`。
   - 重点：Lightning Attention、1M context、40K/80K thinking budget、test-time compute。
2. `SRC-minimax-m2-series-paper-v1`。
   - 重点：M2 full attention + GQA；hybrid SWA 反例。
3. `outputs/2026-05-26-minimax-m2-full-vs-hybrid-swa-tables.md`。
   - 重点：RULER 128K、MTOB、Table 3 混合结果。

## 3. Serving / vLLM 支持路径

Goal: 区分 supported-models、fixed commit、stable release 与 local test。Output: 一个分层 smoke-test checklist。

1. `SRC-vllm-kimi-linear-support-v0-26-0`。
2. `SRC-vllm-qwen3-next-gdn-support-v0-26-0`。
3. `outputs/2026-07-26-vllm-v0-26-0-kimi-linear-smoke-test-plan.md`。
4. `outputs/2026-07-26-kimi-linear-implementation-snapshot.md`。

阅读重点：不要把 “supported models table 中存在” 等同于本仓生产可用。

## 4. Kimi K3 serving case：state → cache → scheduler → kernel

Goal: 理解 recurrent state 如何扩大 serving correctness surface。Output: 一张因果链和一个 failure-injection test plan。

1. `SRC-kimi-k3-tech-report-2026-07-28`：先读 KDA-aware prefix cache、spec decode replay、FlashKDA/context parallelism。
2. `SRC-vllm-kimi-k3-day0-blog-2026-07-27`：提取硬件、TP、batch、DSpark、recipe 和 author-reported benchmark 边界。
3. `SRC-vllm-kimi-k3-support-pr-50000`：确认 merge commit、拆分 PR、专用 image 和 FlashInfer RC 依赖。
4. `SRC-vllm-partial-cache-rfc-45702`：提取 `hash_block_size`、alias、`hit_length`、copy-on-write、final-tail/same-step open questions。
5. `outputs/2026-08-01-kimi-k3-vllm-tech-share-analysis.md`：使用已完成的跨来源拆解，不回到 ASR 猜术语。

必须产出：`roadmap_status`、`release_status`、`local_test_status` 三列；不得合并成一个 supported boolean。

## 5. Benchmark / 反例阅读

Goal: 设计能暴露质量、缓存和 speculative 风险的矩阵。Output: benchmark manifest 草案。

1. `outputs/2025-03-06-gated-deltanet-paper-v3-tables.md`。
2. `outputs/2026-05-26-minimax-m2-full-vs-hybrid-swa-tables.md`。
3. `SRC-glm5-paper-v2`。

问题：哪些 benchmark 能暴露 32K 之后、multi-hop、in-context learning、agentic trace 的退化？

## 6. 只作发现线索

- `SRC-kimi-linear-yang-songlin-interview` — 访谈转写，D 级。
- `SRC-qwen-gdn-zhihu-2026` — 知乎链接，当前未捕获正文，D 级。
- `SRC-efficient-attention-seed-list` — seed list，D 级。
- `SRC-kimi-k3-vllm-tech-share-local-2026-08-01` — 本地 slides/SRT，D 级；只辅助理解时间轴和问题动机。

这些不能支撑正文事实。

## 最小阅读笔记格式

```text
Question:
Proposition:
Source ID / location:
Version or capture date:
Applies to:
What it cannot prove:
Counterexample:
Required test:
```
