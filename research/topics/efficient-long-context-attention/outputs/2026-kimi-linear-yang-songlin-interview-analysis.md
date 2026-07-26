# Kimi Linear / 线性注意力访谈材料使用建议

Owner:
Purpose: 评估并结构化整理 `source/transcripts/2026-kimi-linear-yang-songlin-interview.zh.txt`，明确它在高效长上下文注意力专题中的用途、证据边界和后续核查任务。
Status: captured
Applies to: research/topics/efficient-long-context-attention
Evidence grade: D — 访谈转写/口述材料，未核对原始音频、发布日期、逐字稿准确性和论文原文。
Verified date: 2026-07-26
Assumptions: 文本来自中文播客/访谈转写，嘉宾为杨松林，主题围绕 Kimi Linear、KDA、hybrid linear attention、sparse attention 与算法架构演进。
Open questions: 原始节目 URL、发布日期、访谈授权、Kimi Linear 论文版本、KDA 的准确术语和实现细节。
Handoff: `claims.yml`、`tracking/README.md`、Kimi Linear source card、后续 booklet。

## 1. 这份材料有没有用？

有用，但只能作为 **D 级研究线索**。

它的价值不在于直接证明算法事实，而在于提供一组非常清晰的研究问题和术语线索：

- Kimi Linear 的核心模块 KDA / Kimi Delta Attention；
- hybrid linear attention 与 full attention 的混合比例，例如 3:1；
- linear attention、sparse attention、sliding window attention 的关系；
- MiniMax M1/M2 从 Lightning Attention 回到 full attention 的可能原因；
- 多跳推理、长上下文 reasoning、coding/math 任务对 global/full attention 的依赖；
- KDA 相比早期 Lightning Attention / RetNet / Gated DeltaNet 的改进线索；
- 算法是否硬件友好：矩阵乘、chunk 并行、Triton/CUDA kernel、memory bound decode；
- sparse attention 与 linear attention 未来可能组合，而不是非此即彼。

## 2. 推荐用法

### 2.1 作为 Kimi Linear 分支的 QA / research agenda

这份访谈可以驱动一个 Kimi Linear 子专题：

```text
Kimi Linear / KDA
  → 为什么长 CoT / agentic decoding 使 full attention decode cost 成为瓶颈？
  → 为什么纯 linear attention 不够？
  → hybrid linear attention 如何保留少量 full attention 层？
  → KDA 相比 Gated DeltaNet / Lightning Attention 改了什么？
  → 多跳推理为什么可能暴露 hybrid attention 缺陷？
  → 如何与 sparse attention 结合？
```

### 2.2 作为 benchmark 设计反例来源

访谈中最有用的 benchmark 警告是：

> 只看 MMLU 这类短上下文/通用指标，可能选出在 multi-hop reasoning 或长上下文任务上退化的 efficient attention 方案。

这可以进入第 09 章 benchmark 设计：

- 必须覆盖 multi-hop reasoning；
- 必须覆盖 long-context retrieval / RepoQA / RULER / HELMET；
- 必须覆盖 coding/math/agentic traces；
- 必须区分 short-context quality 与 long-context fidelity。

### 2.3 作为 taxonomy 修正来源

它进一步支持本 topic 不应叫 `linear-attention`：

- Kimi / Qwen：hybrid linear attention 路线；
- DeepSeek：sparse attention 路线；
- MiniMax：M1 线性/Lightning，M2 回到 full attention；
- OpenAI 公开模型/报告：sliding window + full attention 线索；
- 未来可能组合：用 sparse attention 替换 hybrid 架构中的 full/global attention 层。

这些都属于 efficient long-context attention，而不只是 linear attention。

## 3. 可抽取的待验证问题

1. Kimi Linear 论文中的 KDA / Kimi Delta Attention 准确定义是什么？
2. KDA 与 Gated DeltaNet、DeltaNet、RetNet、Mamba-2 的关系是什么？
3. 3:1 linear/full attention 混合比例是否来自 Kimi、Qwen 和其他论文的独立实验？
4. Hybrid linear attention 在 multi-hop reasoning 上的退化是否有公开实验支持？
5. MiniMax M2 回到 full attention 的原因是否有官方技术报告支撑？
6. Kimi Linear 是否提供 apple-to-apple full attention baseline？是否提供 sparse attention baseline？
7. KDA 的 chunk-parallel 算法和 kernel 实现在哪里？Triton 还是 CUDA？
8. vLLM/SGLang 是否支持 Kimi Linear / Qwen3-Next / MiniMax M1/M2 的 hybrid attention serving？
9. Linear attention 与 sparse attention 是否已有组合实现或论文？
10. 对 decode 来说，比较 sliding window 与 linear attention 时是否应控制 state size / KV cache size？

## 4. 可进入 claims.yml 的方式

不要把访谈口述写成事实。建议只用于补充 `verification_gap` 或新增 D 级边界 claim，例如：

```yaml
- id: EA-C08
  statement: "中文访谈材料提示 Kimi Linear/KDA、Qwen3-Next、MiniMax M1/M2 和 DeepSeek sparse attention 可作为比较 hybrid linear 与 sparse attention 路线的研究入口。"
  grade: D
  kind: research-lead
```

真正的技术 claim 必须来自：

- Kimi Linear 论文；
- Qwen3-Next 技术报告；
- MiniMax M1/M2 技术报告；
- DeepSeek DSA/NSA 论文；
- vLLM/SGLang 源码或测试；
- 本仓实验。

## 5. 推荐下一步

优先级从高到低：

1. 下载并校验 Kimi Linear 论文 `arXiv:2510.26692`，建立 `SRC-kimi-linear`。
2. 抽取 KDA、hybrid ratio、benchmark、full attention baseline、kernel 信息。
3. 查 Qwen3-Next 是否有公开技术报告或模型配置，建立 source card。
4. 查 MiniMax M1/M2 的官方材料，验证 Lightning Attention → full attention 的说法。
5. 建立 `tracking/kimi-linear-research-questions.yml` 或并入 capability matrix。
6. 将 benchmark 计划扩展到 multi-hop reasoning 和 long-context coding/RepoQA。
