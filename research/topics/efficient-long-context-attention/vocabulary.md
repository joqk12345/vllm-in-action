---
title: "高效长上下文注意力最小系统词汇"
status: working
topic: efficient-long-context-attention
created: 2026-07-26
verified: 2026-07-26
applies_to: "长上下文 attention 架构、vLLM serving、KV cache、kernel 和 benchmark"
source_ids:
  - SRC-glm5-paper-v2
chapters: ["04", "08", "09", "11", "12", "15"]
---

# 高效长上下文注意力最小系统词汇

Purpose: 用统一 nouns/verbs 区分 sparse、linear、window、block 和 hybrid attention，并连接到 vLLM serving 指标。
Evidence grade: B/D 混合
Assumptions: 当前已纳入 GLM-5、Kimi Linear、MiniMax-M1/M2、Gated DeltaNet 和 Qwen3-Next config；NSA/MoBA/MiniMax-01 尚未细读。
Open questions: 固定 vLLM release 后，将概念映射到具体模型实现、kernel、KV layout 和 metrics。
Handoff: 第 04、08、09、11、12、15 章。

## 核心 nouns

| Noun | 中文 | 含义 | 关键 verbs |
|---|---|---|---|
| Dense attention | 稠密注意力 | 每个 query 关注所有历史 token 的标准 softmax attention | attend, compute, cache |
| Sparse attention | 稀疏注意力 | 只选择部分历史 token 或 block 参与 attention | select, retrieve, prune |
| Linear attention | 线性注意力 | 用核化或递归状态替代二次 attention 矩阵 | recurrentize, update, scan |
| Delta rule | Delta 更新规则 | 用输入 key/value 对递归状态做定向校正/替换的更新机制 | update, replace, correct |
| Gated DeltaNet / GDN | 门控 Delta 网络 | 将 gating 的遗忘能力与 delta rule 的定向更新结合的线性/RNN-style token mixer | gate, forget, update |
| Kimi Delta Attention / KDA | Kimi Delta Attention | Kimi Linear 中扩展 GDN 的线性注意力模块，引入更细粒度 gating 和专用 kernel 设计 | gate, chunk, decode |
| Sliding-window attention | 滑动窗口注意力 | 固定只看局部窗口，常与 full attention 层混合 | window, interleave |
| Block attention | 块级注意力 | 以 block 为选择或路由单位的注意力 | route, group, score |
| Hybrid attention | 混合注意力 | full/window/sparse/linear 不同层或阶段组合 | mix, search, adapt |
| DSA | DeepSeek Sparse Attention | GLM-5 论文采用/讨论的动态稀疏注意力机制 | index, top-k, sparse-attend |
| Indexer | 索引器 | 为 sparse attention 选择相关 KV/token 的组件 | rank, select, retrieve |
| KV layout | KV 布局 | KV cache 的形状、分片、复制和存储位置 | shard, replicate, offload |
| Long-context fidelity | 长上下文保真度 | 长上下文任务上保持信息访问和推理能力 | evaluate, regress |
| Prefill cost | 预填充成本 | 处理 prompt/context 时的 attention 计算和 KV 写入成本 | measure, reduce |
| Decode cost | 解码成本 | 逐 token 生成时的 attention/KV 读取和 kernel 成本 | measure, amortize |

## 核心 verbs

| Verb | 中文 | 主语 | 宾语或结果 |
|---|---|---|---|
| `select` | 选择 | Indexer/router | token、block 或 KV entry |
| `sparsify` | 稀疏化 | Attention mechanism | attention pattern |
| `linearize` | 线性化 | Linear attention | recurrence/state update |
| `interleave` | 交错 | Architecture | full attention 与 window/efficient 层 |
| `retrieve` | 检索 | Sparse attention | relevant KV entries |
| `cache` | 缓存 | vLLM/model | KV cache |
| `replicate` | 复制 | Parallel runtime | KV vector 或 attention state |
| `benchmark` | 评测 | Experiment | 长上下文质量与 serving 指标 |
| `regress` | 退化 | Model/method | long-context benchmark score |
| `fallback` | 回退 | Serving system | dense/full attention 或已验证模型 |

## 三组必须区分的概念

### Sparse attention vs linear attention

Sparse attention 保留 softmax attention 的部分条目或 block；linear attention 通常改变 attention 计算形式，用递归/核化状态避免二次矩阵。二者都可能降低成本，但质量风险和 kernel 风险不同。

### 训练期高效 vs serving 期高效

训练中减少 FLOPs 不等于 vLLM serving 中 TTFT、ITL 或 goodput 改善。serving 还受 kernel、KV cache、batch、并行、prefix reuse 和 request distribution 影响。

### 长上下文 benchmark vs 生产 workload

RULER、RepoQA、LongBench、HELMET 等 benchmark 能测试不同能力，但不能单独代表 agentic tool-use traces、代码仓库 QA 或真实多租户 serving。