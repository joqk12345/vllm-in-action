# MiniMax-M2 full attention vs hybrid SWA table extraction

Owner:
Purpose: 从 MiniMax-M2 arXiv:2605.26494v1 抽取 Table 2/3，用作 efficient attention 失败边界和 benchmark 设计反例。
Status: captured
Applies to: `source/papers/2026-05-26-minimax-m2-series-paper-v1.pdf`
Evidence grade: B — 作者论文表格，尚未本地复现。
Verified date: 2026-07-26
Assumptions: 数值来自 `pdftotext` 快速抽取，进入正文前应回看 PDF 表格排版复核。
Open questions: hybrid SWA 的具体 ratio/RoPE/训练 token 配置、Table 2/3 是否有 appendix 补充设置。
Handoff: `claims.yml` EA-C15；第 09/11/12/15 章。

## 1. 论文原文上下文

MiniMax-M2 论文第 2.2.2 节说明：

- M2 adopts full multi-head attention across all layers；
- this departs from MiniMax-Text-01 的 hybrid Lightning/full attention 设计；
- 作者称在 reasoning、coding、agent tasks 的生产设置中，尚未找到可靠匹配 full attention 质量的 efficient attention 变体；
- hybrid SWA 在标准 benchmark 上可能看起来接近 full attention，但在 long-context retrieval、multi-hop reasoning、in-context learning 和 SFT 后 >32K agent/long-context tasks 上暴露差距。

## 2. Table 2 — Pretraining evaluation

Table 2 比较 M2 architecture scale 下 full attention baseline 与 hybrid SWA，覆盖 general knowledge、long-context retrieval 和 in-context translation。

| Benchmark | Baseline full attention | w/ SWA | Delta (SWA - baseline) |
|---|---:|---:|---:|
| HELMET ICL | 75.8 | 72.7 | -3.1 |
| MMLU | 85.5 | 85.6 | +0.1 |
| MATH | 60.3 | 60.3 | 0.0 |
| RULER 128K CWE | 90.0 | 72.0 | -18.0 |
| RULER 128K MQ | 99.0 | 93.0 | -6.0 |
| RULER 32K CWE | 99.0 | 99.0 | 0.0 |
| RULER 32K MQ | 99.0 | 99.0 | 0.0 |
| MTOB K-e Bleurt | 60.0 | 45.0 | -15.0 |
| MTOB e-k ChrF | 44.8 | 27.2 | -17.6 |

### 观察

- 短/通用指标并不总能暴露风险：MMLU 和 MATH 基本持平。
- 长上下文和 in-context translation 更敏感：RULER 128K CWE、MTOB 两项差距明显。
- RULER 32K 两项持平，提示问题可能在更长上下文或特定任务形态下显现。

## 3. Table 3 — SFT benchmark

Table 3 比较 SFT 后 full attention baseline 与 hybrid SWA，覆盖 general reasoning/knowledge 和 agentic tasks。

| Benchmark | Baseline full attention | w/ SWA | Delta (SWA - baseline) |
|---|---:|---:|---:|
| AIME 2025 | 86.7 | 86.7 | 0.0 |
| ARC-AGI-1 | 38.9 | 39.6 | +0.7 |
| GPQA-Diamond | 75.3 | 72.7 | -2.6 |
| MMLU-Pro | 80.5 | 80.1 | -0.4 |
| IFBench | 23.1 | 27.2 | +4.1 |
| SWE-verified | 50.2 | 54.7 | +4.5 |
| Terminal-Bench | 23.8 | 26.7 | +2.9 |
| BrowseComp-zh | 28.7 | 32.8 | +4.1 |
| GAIA-103 | 51.5 | 53.4 | +1.9 |
| XBench-ds | 63.0 | 58.0 | -5.0 |
| τ2-Bench retail | 67.5 | 62.3 | -5.2 |
| τ2-Bench telecom | 21.0 | 32.5 | +11.5 |

### 观察

- SFT 后 agent/general 指标呈混合结果：SWA 在部分短/agent benchmark 上更高。
- 作者原文特别强调 >32K context 的 agent tasks / complex long-context evaluations 上 SWA 更差，但 Table 3 摘录本身需要结合任务上下文长度解释。
- 不能只按平均值判断；要分组看 long-context、multi-hop、agent trace length 和是否需要全局信息流。

## 4. 对本书 benchmark 设计的启发

1. **必须包含长度分层。** 32K 持平不代表 128K 或更长仍持平。
2. **必须包含任务类型分层。** MMLU/MATH 不能替代 RULER/MTOB/HELMET/agentic traces。
3. **必须保留反例。** efficient attention 的候选方案即使在部分 benchmark 上更高，也可能在长上下文检索、多跳推理或 in-context learning 上退化。
4. **必须记录训练阶段。** pretraining evaluation 与 SFT benchmark 可能呈现不同风险形态。
5. **不要把 SWA 反例泛化到所有 linear/sparse attention。** Table 2/3 是 MiniMax-M2 作者报告的 hybrid SWA 设置，不直接否定 Kimi Linear/KDA 或 DeepSeek sparse attention。

## 5. 待复核

- 回看 PDF 表格，确认 `τ2-Bench`、`MTOB` 和 RULER 子项名称无 OCR 误差。
- 查 appendix 是否给出 hybrid SWA ratio、window size、RoPE 设置和训练 token 数。
- 抽取 Table 2/3 对应上下文长度，特别是作者所说 “benchmarks exceeding 32K context”。
