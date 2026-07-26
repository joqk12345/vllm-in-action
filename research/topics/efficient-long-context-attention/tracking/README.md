# 高效长上下文注意力持续跟踪

Owner: release tracker
Purpose: 跟踪 DSA/NSA/MoBA/Lightning/linear-window-hybrid attention 的论文、实现、vLLM 支持状态和本仓 benchmark 需求。
Status: active
Applies to: 研究阶段跟踪论文和上游 main；正文结论固定到论文版本、release/tag/commit 或本仓实验。
Evidence grade: discovery only；接受结论时回到论文、源码、测试或实验。
Verified date: 2026-07-26
Assumptions: seed list 只是来源发现入口，不证明算法结论。
Open questions: 哪类高效 attention 能在目标 vLLM serving workload 中同时保持质量和降低成本。
Handoff: 第 04、08、09、11、12、15 章。

## 跟踪对象

| 对象 | 关注变化 | 进入正文前的固定点 |
|---|---|---|
| GLM-5 paper | DSA、efficient attention 消融、DP-aware routing、kernel 说明 | arXiv version |
| DeepSeek NSA | Native Sparse Attention 训练/硬件/质量边界 | paper version + implementation commit |
| Kimi MoBA | Mixture of Block Attention block routing 与长上下文表现 | paper version + implementation commit |
| MiniMax Lightning Attention | Lightning Attention / MiniMax-01/M1 架构和 serving 约束 | paper version + implementation commit |
| MiniMax-M2 | full attention 回归、hybrid/SWA 反例、agentic serving/RL 系统线索 | paper version + repo/HF/vLLM support |
| Kimi Linear | 线性注意力架构、表达能力、KV/state 形式和长上下文 serving 约束 | paper version + implementation commit |
| Gated DeltaNet / Qwen GDN | gated delta rule、Qwen3-Next/Qwen3.5 GDN layer 分布、vLLM GDN backend | paper version + HF config + vLLM tag |
| vLLM | 对相关模型 attention、kernel、KV layout、long context serving 的支持 | release tag + commit |
| 本仓实验 | 长上下文质量、TTFT、ITL、throughput、显存和成本 | 环境 manifest + 原始结果 |

## 节奏

- 每篇论文纳入后：建立 source card、抽取 claim、记录反例。
- 每个 vLLM release：复查模型支持、attention kernel、KV layout 和 long-context 限制。
- 每季度或关键实现变化后：刷新长上下文 benchmark。

## 漂移分诊

1. 区分模型架构变化、kernel 支持变化、vLLM serving 支持变化和 benchmark 变化。
2. 不把 paper result 自动提升为 vLLM serving 事实。
3. 对每个方法记录：复杂度、质量风险、kernel 要求、KV cache 影响、prefill/decode 影响。
4. 更新 `claims.yml` 后再刷新 booklet、brief 或 chapter handoff。

## 优先核查项

1. 下载并校验 NSA、MoBA、MiniMax-01 Lightning Attention 论文；MiniMax-M1/M2 已完成 arXiv 捕获。
2. 基于当前 release 基线 vLLM `v0.25.1` 建立 Kimi Linear 最小 smoke test；`v0.11.1` 只保留为首个支持入口的历史边界。
3. 固定 Kimi Linear HF revision；当前已捕获 Instruct config，但来源仍是 HF `main` 下载。
4. 固定 Qwen3.5 具体 HF config，确认是否与 Qwen3-Next 共用 vLLM Qwen GDN path；知乎链接目前只作 D 级线索。
5. 核对 Kimi Linear 访谈原始 URL、发布日期、授权和转写准确性。
6. 回看 PDF 复核 MiniMax-M2 Table 2/3 OCR 数值，并抽取 hybrid SWA ratio/window/RoPE 设置。
7. 抽取 GLM-5 中 DSA vs SWA/GDN/SimpleGDN 的实验设置和表格。
8. 回看 PDF 复核 Gated DeltaNet Table 2/3/4/5 OCR 数值，尤其 S-NIAH-3 8K 和 LongBench 子项；核查 NVlabs/GatedDeltaNet repo。
9. 查 vLLM 是否支持 GLM-5/DSA 或相关 sparse/linear attention kernel。
10. 设计 long-context benchmark：RULER/RepoQA/HELMET/LongBench + serving metrics。
11. 与 `llm-d-agentic-serving` 交叉核查 DP-aware routing 和长上下文 KV reuse。