# MiniMax-M2 系列论文 v1 结构化分析

Owner:
Purpose: 将用户提供的 arXiv:2605.26494 纳入高效长上下文注意力专题，记录 MiniMax 从 M1/Lightning 到 M2/full attention 的证据和边界。
Status: captured
Applies to: arXiv:2605.26494v1；research/topics/efficient-long-context-attention
Evidence grade: B — 作者论文，尚未本地复现。
Verified date: 2026-07-26
Assumptions: 已下载 arXiv PDF 并进行快速结构化阅读；尚未核查 MiniMax-M2 repo/HF/vLLM support。
Open questions: M2 release repo、HF config、vLLM support、full attention serving 成本、M1→M2 attention 选择差异。
Handoff: `claims.yml`、source card `SRC-minimax-m2-series-paper-v1`、chapter 09/11/12/15。

## 1. 文件信息

- 来源：<https://arxiv.org/abs/2605.26494>
- 文件：`source/papers/2026-05-26-minimax-m2-series-paper-v1.pdf`
- 标题：The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence
- arXiv：2605.26494v1
- PDF metadata 日期：2026-05-26
- SHA256：`4c090a07b73dade56ed3e90f7fdf56a183601c12d2f2d1f81eb46f24cff311fd`

## 2. 核心内容

论文介绍 MiniMax-M2 系列，重点不是 efficient attention 本身，而是 agentic deployment / agent-native RL / MoE 小激活量。与本专题最相关的是第 2.2.2 节 attention 选择：

- M2 flagship：229.9B total parameters，9.8B activated per token；
- 62-layer decoder-only Transformer；
- 256 experts，8 experts activated per token；
- full multi-head attention with GQA；
- native context window 192K；
- MTP module 可作为 speculative-decoding draft path。

## 3. 对 efficient attention 专题的关键意义

### 3.1 这是 M1/Lightning 路线的重要反例

MiniMax-M1 论文把 Lightning Attention 作为 long-output/test-time compute/RL scaling 的效率核心；M2 论文则明确说：

- M2 adopts full multi-head attention across all layers；
- departed from MiniMax-Text-01 hybrid design, which interleaves Lightning Attention with full attention；
- in production settings spanning reasoning, coding, and agent tasks, no efficient attention variant reliably matched full attention quality。

这说明本专题必须保留反例：**efficient attention 的工程价值不能只看 FLOPs 或长上下文长度；质量、multi-hop、agentic tasks 和基础设施成熟度可能让团队回到 full attention。**

### 3.2 论文给出的失败/风险维度

M2 论文提到的风险包括：

- 标准 benchmark 上 hybrid attention 可能看似接近 full attention；
- 但 long-context retrieval、multi-hop reasoning、in-context learning 暴露缺陷；
- SFT 后 >32K context 的 agent tasks / complex long-context evaluations 差距更明显；
- linear/sparse attention 基础设施仍不成熟；
- inference 侧存在 low-precision storage sensitivity、native prefix caching support 不足、deployment behavior 不清晰等问题。

这些可用于第 09 章 benchmark 设计和第 15 章升级/选型边界。

### 3.3 与 agentic serving 的交叉

虽然 M2 用 full attention，但它非常适合与 `llm-d-agentic-serving` 交叉：

- windowed-FIFO scheduling；
- prefix-tree merging；
- training–inference–agent decoupling；
- global L3 KV cache pool；
- long-horizon agent trajectories；
- white-box / black-box agents；
- context management 和 trajectory-length variance。

这些更像 serving/system design 线索，不是 attention kernel 结论。

## 4. 与现有来源的关系

| 来源 | 对 attention 路线的作用 |
|---|---|
| Kimi Linear v2 | 支持 hybrid linear/KDA 可在作者设置中超过 full attention 的正例 |
| MiniMax-M1 v1 | 支持 Lightning Attention 在 long-output/test-time compute 上的正例 |
| MiniMax-M2 v1 | 提供回到 full attention 的生产设置反例 |
| GLM-5 v2 | 提供 DSA/GDN/SimpleGDN/MLA 消融和 serving routing 线索 |

## 5. 推荐写法

可以写：

> MiniMax-M2 论文报告其在 M2 中选择 full multi-head attention + GQA，并明确将这一选择与 MiniMax-Text-01 的 hybrid Lightning/full attention 区分开；作者称在 reasoning、coding 和 agent tasks 的生产设置中，尚未找到可靠匹配 full attention 质量的 efficient attention 变体。

不能写：

> MiniMax 证明 linear/sparse/hybrid attention 都不行。

因为这只是 MiniMax-M2 作者报告的具体设置和观察。

## 6. 后续任务

1. 建立 MiniMax-M2 repo/HF config source card。
2. 查 vLLM `v0.25.1` 是否支持 MiniMax-M2 或其模型类型。
3. 抽取 Table 2/3 中 full attention vs hybrid SWA 的完整数值。
4. 与 MiniMax-M1 对齐，形成 “M1 Lightning → M2 full attention” 的版本化 case study。
5. 将 windowed-FIFO、prefix-tree merging、global L3 KV cache pool 交叉移交给 `llm-d-agentic-serving`。
