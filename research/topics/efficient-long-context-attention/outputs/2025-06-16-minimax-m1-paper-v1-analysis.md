# MiniMax-M1 论文 v1 结构化分析

Owner:
Purpose: 将用户提供的 AlphaXiv 线索 `2506.13585v1` 回到 arXiv 原文，整理 MiniMax-M1 / Lightning Attention 对本专题的价值和证据边界。
Status: captured
Applies to: arXiv:2506.13585v1；research/topics/efficient-long-context-attention
Evidence grade: B — 作者论文，尚未本地复现；AlphaXiv overview 仅作发现入口。
Verified date: 2026-07-26
Assumptions: 已下载 arXiv PDF；未核查 MiniMax-M1 GitHub、HF config 或 vLLM release 支持。
Open questions: MiniMax-M1 implementation commit、Lightning Attention kernel、vLLM support tag、HF config 和 serving benchmark。
Handoff: `claims.yml`、source card `SRC-minimax-m1-paper-v1`、后续 capability matrix。

## 1. 文件信息

- 用户线索：<https://www.alphaxiv.org/overview/2506.13585v1>
- 固定来源：<https://arxiv.org/abs/2506.13585>
- 文件：`source/papers/2025-06-16-minimax-m1-paper-v1.pdf`
- 标题：MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention
- arXiv：2506.13585v1
- PDF metadata 日期：2025-06-16
- SHA256：`d355a6a41a26b85ca145aec5154650f4d39733c92f54775ae7f5851ecbedf600`

## 2. 核心内容

论文介绍 **MiniMax-M1**：

- hybrid-attention reasoning model；
- hybrid MoE architecture + Lightning Attention；
- 基于 MiniMax-Text-01；
- 总参数 456B，每 token 激活 45.9B；
- 原生支持 1M context；
- 发布 40K 与 80K thinking budget 版本；
- 用 CISPO 和 Lightning Attention 支持更高效 RL scaling。

## 3. 对本专题的价值

### 3.1 taxonomy：Lightning Attention / hybrid attention 路线

MiniMax-M1 是 Kimi Linear 之外的另一个 high-profile hybrid/linear-family long-context serving 案例。它可用于比较：

```text
Kimi Linear / KDA
  → hybrid linear attention + MLA
MiniMax-M1
  → hybrid attention + Lightning Attention
DeepSeek NSA / DSA
  → sparse / dynamic sparse attention
GLM-5
  → DSA + GDN/SimpleGDN 消融
```

### 3.2 test-time compute 与长输出

MiniMax-M1 把 efficient attention 的价值从“长输入”扩展到“长输出 / 长思考 / RL rollout”：

- 1M context；
- 40K/80K max generation/thinking budget；
- 论文报告在 100K generation length 下与 DeepSeek R1 的 FLOPs 对比；
- 强调 rollout computation / latency 是 RL training 的主要瓶颈之一。

这对第 11、12 章有价值：efficient attention 不只影响 prefill，也影响 decoding-heavy / agentic / RL-style workload。

### 3.3 benchmark 维度

论文覆盖：

- math；
- coding；
- SWE-bench；
- reasoning & knowledge；
- long context；
- agentic tool use；
- factuality。

对本仓 benchmark 的启发：

- 不能只做 RULER/RepoQA；
- 需要覆盖 long-output reasoning 和 tool-use traces；
- 需要分离 40K 与 80K output budget 下的 latency/cost。

## 4. 与访谈材料的关系

此前访谈中提到 MiniMax 方向变化和 Lightning Attention，但口述材料是 D 级线索。MiniMax-M1 论文可以支撑以下更稳固的事实：

| 访谈/seed 线索 | 论文状态 | 处理建议 |
|---|---|---|
| MiniMax 使用 Lightning Attention | MiniMax-M1 支持 | 可升级为 B 级 claim，但限于 M1/论文版本 |
| MiniMax-M1 是长上下文/长思考模型 | 论文支持 | 可进入 taxonomy |
| Lightning Attention 有 serving/RL 效率价值 | 作者报告支持 | 需本仓复现后才能写生产建议 |
| MiniMax M2 回到 full attention | 本论文不证明 | 仍需 MiniMax M2 官方来源 |

## 5. 待验证任务

1. 核查 `https://github.com/MiniMax-AI/MiniMax-M1` 的 commit、license、README 和 vLLM deployment guide。
2. 下载 MiniMax-M1 HF config，抽取 attention/hybrid/lightning 配置。
3. 查 vLLM `v0.26.0` 是否支持 MiniMax-M1 或 MiniMax-Text-01，以及模型类/attention kernel 路径。
4. 抽取论文中 Table 1、核心 benchmark 表和 FLOPs 对比图的完整数值。
5. 与 Kimi Linear/KDA 的 vLLM support 路径并列到 capability matrix。
6. 如果后续要讨论 “MiniMax M2 回 full attention”，必须另建 MiniMax-M2 source card。

## 6. 不得直接写入正文的泛化

- “Lightning Attention 一定优于 full attention”。
- “MiniMax-M1 的 1M context 能在本仓 vLLM 环境中直接跑通”。
- “论文 FLOPs 对比可直接等价为 vLLM serving 成本”。
- “MiniMax-M1 证明 long-output reasoning 不再受 attention 限制”。
- “MiniMax 后续模型已经放弃或回归某一路线”。
