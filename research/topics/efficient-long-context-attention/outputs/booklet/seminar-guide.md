# 高效长上下文注意力研讨指南

Owner:
Purpose: 为 90 分钟内部研讨提供问题链、阅读顺序、红队检查和决策记录。
Status: draft
Applies to: efficient-long-context-attention topic
Evidence grade: A/B for technical claims; C/D only for discussion leads.
Verified date: 2026-08-01
Assumptions: 参与者熟悉 Transformer attention、KV cache、vLLM serving 基础。
Open questions: 本仓尚未跑 Kimi/Qwen smoke test；Kimi K3 stable release 与 partial-hit correctness 未确认。
Handoff: 第 09、11、12、15 章。

## 1. 研讨目标

结束后，参与者应能回答：

1. 为什么“低复杂度”不等于“生产可用”？
2. KDA、GDN、Lightning、DSA、SWA/full attention 的风险分别在哪里？
3. 如何设计 vLLM 长上下文 benchmark 才能暴露 multi-hop / retrieval / long-output 退化？
4. 进入正文前，哪些结论还缺 release、config、源码或实验？
5. KDA state 打破 append-only KV 假设后，cache/scheduler/spec decode/PD transfer 新增了哪些不变量？

## 2. 参与者与角色

- Facilitator：控制 90 分钟节奏，不允许把 roadmap/main/local-test 状态混写。
- Evidence lead：逐项核对 Source ID、version/commit 和证据等级。
- Serving lead：负责 cache、scheduler、kernel、parallelism 与 benchmark manifest。
- Red team：寻找反例、错误泛化、stale alias、rollback/PD race 和回退缺口。
- Scribe：记录 Decision、owner、completion criteria 和 next review date。

## 3. 会前阅读

Mandatory：`claims.yml`、`vocabulary.md`、`capability-matrix.yml`、`SRC-kimi-k3-tech-report-2026-07-28`、`SRC-vllm-kimi-k3-support-pr-50000`、`SRC-vllm-partial-cache-rfc-45702`。

Role-specific：

- Evidence lead：官方 Kimi K3 blog 与 v0.26.0/PR #50000 时间边界。
- Serving lead：Kimi K3 tech-share analysis 的 Phase B–D。
- Red team：MiniMax-M2 full-attention counterexample 与 Kimi K3 性能数字冲突。
- Scribe：本文件末尾的 decision/action template。

## 4. 90 分钟议程

### Part A — Taxonomy warm-up（10 分钟）

白板画出：

```text
full attention
  ├─ sparse / DSA / NSA / MoBA
  ├─ sliding-window / SWA
  ├─ linear / recurrent state
  │   ├─ DeltaNet
  │   ├─ Gated DeltaNet / GDN
  │   └─ Kimi Delta Attention / KDA
  └─ hybrid interleaving
```

讨论：为什么本 topic 不叫 linear-attention？

### Part B — Mechanism deep dive（20 分钟）

重点读：

- Gated DeltaNet：gate + delta rule；
- Kimi Linear：KDA extends GDN；
- Qwen3-Next config：36 linear/GDN + 12 full attention；
- vLLM v0.26.0：QwenGatedDeltaNetAttention 和 KimiLinearForCausalLM path。

讨论问题：

1. GDN 为什么需要同时有遗忘和定向更新？
2. KDA 相比 GDN 的“更细粒度 gating”可能改变什么？
3. 3:1 hybrid ratio 是模型事实、论文建议，还是通用规律？

### Part C — Kimi K3 state/cache case（20 分钟）

白板完成：

```text
recurrent state
  → hybrid page alignment
  → coarse physical block
  → block-aligned checkpoint
  → partial hit + copy-on-write
  → eviction/offload/PD/spec-decode correctness
```

讨论：为什么 PR #50000 合入 `main` 仍不能写成 v0.26.0 能力？为什么更细 `hash_block_size` 不必然更快？

### Part D — Counterexample reading（20 分钟）

读 MiniMax-M2：

- M2 full attention + GQA；
- hybrid SWA 在 128K RULER、MTOB、长上下文 agent tasks 中暴露问题；
- 标准/短上下文 benchmark 可能看不出风险。

练习：用 Table 2/3 设计一个反驳“只看 MMLU/MATH 就够了”的论证。

### Part E — vLLM serving planning and decision（20 分钟）

围绕 vLLM v0.26.0 Kimi Linear/Qwen3-Next 与 Kimi K3 `main@aeeb36b1`，列出 smoke test：

1. import/registry；
2. HF config 固定；
3. layer construction；
4. GDN/KDA kernel precision tests；
5. minimal serve；
6. TTFT/ITL/state memory benchmark。
7. partial-tail/copy-on-write/eviction/PD/DSpark rejection correctness。

讨论：如果 smoke test 成功，离生产建议还差什么？

## 5. 研讨练习

### 练习 1：将 claim 分类

把 claims.yml 中 EA-C09–EA-C25 分类为：

- paper design；
- model config；
- implementation support；
- benchmark observation；
- counterexample。

### 练习 2：设计 benchmark matrix

要求至少包含：

- short context quality；
- 32K retrieval；
- 128K retrieval；
- long-output reasoning；
- code repo QA；
- agentic tool trace；
- TTFT、TPOT/ITL、throughput、state/KV memory。

### 练习 3：写一个安全结论

把这句话改写成符合项目证据规则的版本：

> Qwen3.5 的 GDN 比 full attention 更适合长上下文生产部署。

期望改写方向：固定模型、vLLM tag、硬件、任务、实验，并保留失败边界。

## 6. 红队问题

1. 如果 partial alias 在 eviction/reuse 时未清理，什么观测能最快暴露 stale hit？
2. DSpark rejection 后 KDA state 如何证明与 non-spec baseline 一致？
3. PD connector 的 zeroing 与 RDMA write 并发时，是否可能覆盖有效数据或泄漏旧 tail？
4. 370 tok/s/user 中有多少来自 DSpark、KDA kernel、metadata、LatentMoE 或硬件？现有证据能否分解？
5. 如果首个 stable release 改变 image/FlashInfer/backend，哪些 claims 立即 stale？
6. 低 cache reuse、短 prompt 或高-entropy output 下，这套优化是否可能净负收益？

## 7. 预期输出

- 一张 capability matrix 更新建议；
- Kimi Linear/Qwen3-Next smoke test checklist；
- 第 09 章 benchmark 反例段落草案；
- 第 15 章升级/回退边界草案。
- Kimi K3 correctness-first test plan 与 stable-release gate。

## 8. 决策与 action 记录

```text
Decision:
Target version/commit/image digest:
Target model/HF revisions:
Target hardware/topology/workload:
Accepted claims:
Rejected generalizations:
Required tests/experiments:
Canary signals:
Rollback:
Owner:
Completion criteria:
Next review date:
```

Completion checklist：

- [ ] Evidence lead：每条 accepted claim 有 Source ID、版本和边界。
- [ ] Serving lead：benchmark gate 完整，correctness tests 先于性能。
- [ ] Red team：至少记录一个反例和一个 failure injection。
- [ ] Scribe：所有 action 有 owner、完成条件和复查日期。
