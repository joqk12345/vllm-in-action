# 高效长上下文注意力研讨指南

Owner:
Purpose: 为 90–120 分钟内部研讨提供问题链、阅读顺序和练习。
Status: draft
Applies to: efficient-long-context-attention topic
Evidence grade: A/B for technical claims; C/D only for discussion leads.
Verified date: 2026-07-26
Assumptions: 参与者熟悉 Transformer attention、KV cache、vLLM serving 基础。
Open questions: 本仓尚未跑 Kimi/Qwen smoke test。
Handoff: 第 09、11、12、15 章。

## 1. 研讨目标

结束后，参与者应能回答：

1. 为什么“低复杂度”不等于“生产可用”？
2. KDA、GDN、Lightning、DSA、SWA/full attention 的风险分别在哪里？
3. 如何设计 vLLM 长上下文 benchmark 才能暴露 multi-hop / retrieval / long-output 退化？
4. 进入正文前，哪些结论还缺 release、config、源码或实验？

## 2. 建议流程

### Part A — Taxonomy warm-up（15 分钟）

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

### Part B — Mechanism deep dive（30 分钟）

重点读：

- Gated DeltaNet：gate + delta rule；
- Kimi Linear：KDA extends GDN；
- Qwen3-Next config：36 linear/GDN + 12 full attention；
- vLLM v0.25.1：QwenGatedDeltaNetAttention 和 KimiLinearForCausalLM path。

讨论问题：

1. GDN 为什么需要同时有遗忘和定向更新？
2. KDA 相比 GDN 的“更细粒度 gating”可能改变什么？
3. 3:1 hybrid ratio 是模型事实、论文建议，还是通用规律？

### Part C — Counterexample reading（25 分钟）

读 MiniMax-M2：

- M2 full attention + GQA；
- hybrid SWA 在 128K RULER、MTOB、长上下文 agent tasks 中暴露问题；
- 标准/短上下文 benchmark 可能看不出风险。

练习：用 Table 2/3 设计一个反驳“只看 MMLU/MATH 就够了”的论证。

### Part D — vLLM serving planning（30 分钟）

围绕 vLLM v0.25.1，列出 smoke test：

1. import/registry；
2. HF config 固定；
3. layer construction；
4. GDN/KDA kernel precision tests；
5. minimal serve；
6. TTFT/ITL/state memory benchmark。

讨论：如果 smoke test 成功，离生产建议还差什么？

## 3. 研讨练习

### 练习 1：将 claim 分类

把 claims.yml 中 EA-C09–EA-C17 分类为：

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

## 4. 预期输出

- 一张 capability matrix 更新建议；
- Kimi Linear/Qwen3-Next smoke test checklist；
- 第 09 章 benchmark 反例段落草案；
- 第 15 章升级/回退边界草案。
