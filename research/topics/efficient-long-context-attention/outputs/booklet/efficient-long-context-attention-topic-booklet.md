# 高效长上下文注意力专题小册子

Owner:
Purpose: 将 sparse、linear、GDN/KDA、Lightning、SWA/full attention 反例和 vLLM 支持状态组织成可维护的研究小册子。
Status: draft
Applies to: research/topics/efficient-long-context-attention
Evidence grade: A/B 为正文候选；C/D 仅作解释、发现和待核查问题。
Verified date: 2026-07-26
Assumptions: 论文 benchmark 均为作者报告；生产建议必须回到固定 vLLM release、源码/测试和本仓实验。
Open questions: NSA/MoBA/MiniMax-01、Qwen3.5 config、GLM-5/DSA vLLM 支持、Kimi/Qwen smoke test。
Handoff: book/chapter-briefs/09, 11, 12, 15；与 `llm-d-agentic-serving` 交叉。

## 1. 一句话结论

高效长上下文注意力不是单一算法路线，而是一个工程选择空间：dynamic sparse、linear/GDN/KDA、Lightning、SWA、block routing 和 full-attention hybrids 都在试图降低长上下文 prefill/decode/state 成本；但能否用于 vLLM 生产服务，取决于 **质量退化边界、kernel/backend、state/KV layout、prefix cache 支持、模型 config、workload 分布和固定 release 的实际测试**。

## 2. 当前证据地图

| 路线 | 代表来源 | 当前证据 | 主要边界 |
|---|---|---|---|
| DSA / dynamic sparse | GLM-5 v2 | 论文报告 DSA、indexer/top-k、KV reuse/routing 线索 | DeepSeek NSA/DSA 原文和 vLLM 支持未补齐 |
| KDA / hybrid linear | Kimi Linear v2 + vLLM v0.25.1 | KDA 扩展 GDN；KimiLinearForCausalLM 已在 vLLM v0.25.1 出现 | 未本地 serving；HF revision 未固定 |
| GDN / gated delta rule | Gated DeltaNet v3 + Qwen3-Next config | GDN = gate + delta rule；Qwen3-Next 48 层默认 36 GDN/linear + 12 full | Qwen3.5 config 未固定；backend 未实测 |
| Lightning Attention | MiniMax-M1 v1 | 作者报告 1M context、40K/80K thinking budget、test-time compute 效率 | MiniMax-M1 vLLM/HF config 未核查 |
| Full attention counterexample | MiniMax-M2 v1 | M2 回到 full attention + GQA；hybrid SWA 在长上下文/多跳任务退化 | 只适用于 MiniMax 作者设置，不能泛化 |

## 3. 核心概念

### 3.1 Sparse attention

Sparse attention 保留 softmax attention 的语义框架，但只选择部分 token/block/KV entry 参与计算。GLM-5 中的 DSA 线索提示 dynamic sparse 可能引入 indexer/top-k selection，从而把瓶颈转移到选择、kernel、确定性和硬件支持上。

### 3.2 Linear attention / recurrent state

Linear attention 用递归状态或核化形式替代二次 attention 矩阵。优点是 decode state 可以不随上下文线性增长；风险是有限状态可能在精确检索、多跳推理和 in-context learning 上丢信息。

### 3.3 GDN 与 KDA

Gated DeltaNet 把两类机制结合：

- gating：快速遗忘/清空旧信息；
- delta rule：定向更新 key-value association。

Kimi Linear 论文把 KDA 描述为扩展 GDN 的模块，引入更细粒度 gating。Qwen3-Next/Qwen3.5 在 vLLM v0.25.1 中有 QwenGatedDeltaNetAttention 路径。

### 3.4 Hybrid attention

Hybrid 是当前主流工程形态：用大多数 linear/GDN/KDA/Lightning/SWA 层降低成本，再周期性插入 full attention 层保留全局信息流。例如：

- Kimi Linear Instruct config：27 层中 20 KDA + 7 full MLA；
- Qwen3-Next config：48 层默认每 4 层 full attention，即 36 linear/GDN + 12 full；
- MiniMax-M2 反例：作者报告最终选择 full attention + GQA。

## 4. 三个正例与一个反例

### 4.1 Kimi Linear：KDA 正例

Kimi Linear 论文报告 KDA 扩展 GDN，并在作者设置中减少 KV cache、提升长上下文 decode throughput。vLLM v0.25.1 已静态观察到 KimiLinearForCausalLM 和 KDA path。正文写作时必须区分：

- 论文 claim；
- HF config claim；
- vLLM source support claim；
- 本仓实验 claim。

### 4.2 Qwen3-Next：GDN serving path

Qwen3-Next HF config 和 vLLM v0.25.1 显示默认每四层一个 full attention，其他层走 linear/GDN path。它是理解 vLLM 对 GDN-family model 支持的关键样本。

### 4.3 MiniMax-M1：Lightning 与 long-output / RL rollout

MiniMax-M1 把 efficient attention 的价值从长输入扩展到长输出和 test-time compute。它报告 1M context、40K/80K thinking budget 和 RL scaling 效率，但这些数字不能直接写成 vLLM production cost。

### 4.4 MiniMax-M2：full attention 反例

MiniMax-M2 论文报告 M2 回到 full attention + GQA，并指出 hybrid SWA 在长上下文 retrieval、多跳推理、in-context learning 和 >32K agent tasks 中存在风险。这个反例非常重要：复杂度更低不等于质量可接受。

## 5. Benchmark 设计原则

1. **长度分层**：32K 持平不代表 128K/1M 仍安全。
2. **任务分层**：MMLU/MATH 不能替代 RULER、HELMET、RepoQA、MTOB、agentic traces。
3. **阶段分层**：pretraining、SFT、RL/post-training 后风险可能不同。
4. **指标分层**：TTFT、ITL/TPOT、throughput、KV/state memory、goodput 和质量要同时记录。
5. **实现分层**：同一论文算法在不同 vLLM tag、backend、dtype、TP/DP 上可能行为不同。

## 6. 章节落点

- 第 04 章：KV cache、state cache、linear recurrent state 与 full attention KV 的差异。
- 第 08 章：TP/DP/EP 拓扑如何影响 attention state 和 KV reuse。
- 第 09 章：长上下文 benchmark 设计和反例。
- 第 11 章：TTFT/ITL 优化、prefill/decode path、kernel/backend。
- 第 12 章：成本模型，特别是 long-output/test-time compute。
- 第 13 章：观测 GDN/KDA/DSA backend、state memory、prefix cache hit。
- 第 15 章：升级、回退和模型选型边界。

## 7. 当前不可写成正文事实的内容

- Kimi Linear 的作者报告加速可直接在 vLLM v0.25.1 复现。
- Qwen3.5 的 GDN 配置等同于 Qwen3-Next Instruct。
- MiniMax-M2 证明所有 efficient attention 都不如 full attention。
- 访谈或知乎文章中的公司路线判断可作为事实。
- NSA/MoBA/MiniMax-01 已完成验证。

## 8. 下一步

1. 基于 vLLM v0.25.1 跑 Kimi Linear 和 Qwen3-Next smoke test。
2. 固定 HF revision 和模型 config。
3. 补齐 NSA、MoBA、MiniMax-01 source cards。
4. 抽取 GLM-5/DSA 和 GDN/KDA 的更多表格设置。
5. 形成 chapter handoff：第 09 章 benchmark 反例 + 第 11/12 章 serving cost model。
