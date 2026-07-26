# Gated DeltaNet 论文 v3 核心表格抽取

Owner:
Purpose: 从 Gated DeltaNet / GDN 论文 `arXiv:2412.06464v3` 抽取核心表格，用于解释 GDN 相比 Mamba2/DeltaNet 的机制收益和边界。
Status: captured
Applies to: `source/papers/2024-12-09-gated-delta-networks-paper-v1.pdf`；PDF 文本显示 `arXiv:2412.06464v3 [cs.CL] 6 Mar 2025`。
Evidence grade: B — ICLR 2025 作者论文表格，尚未本地复现。
Verified date: 2026-07-26
Assumptions: 数值来自 `pdftotext` 快速抽取，进入正文前应回看 PDF 表格排版复核。
Open questions: 1.3B/400M 具体训练 token、实现 commit、hybrid H1/H2 配比、vLLM/Qwen GDN backend 对应关系。
Handoff: `claims.yml` EA-C16/EA-C17；Qwen3-Next GDN explainer；第 09/11/12/15 章。

## 1. Table 2 — S-NIAH synthetic in-context retrieval

论文用 S-NIAH 说明 gating 与 delta rule 的互补性。

### S-NIAH-1: pass-key retrieval

| Model | 1K | 2K | 4K | 8K |
|---|---:|---:|---:|---:|
| DeltaNet | 97.4 | 96.8 | 99.0 | 98.8 |
| Mamba2 | 99.2 | 98.8 | 65.4 | 30.4 |
| Gated DeltaNet | 98.4 | 88.4 | 91.4 | 91.8 |

观察：DeltaNet 在简单 pass-key retention 上最稳；Mamba2 在 4K/8K 明显掉分，论文解释为 decay 伤害长期保留。

### S-NIAH-2: number in haystack

| Model | 1K | 2K | 4K | 8K |
|---|---:|---:|---:|---:|
| DeltaNet | 98.4 | 45.6 | 18.6 | 14.4 |
| Mamba2 | 99.4 | 98.8 | 56.2 | 17.0 |
| Gated DeltaNet | 100.0 | 99.8 | 92.2 | 29.6 |

观察：加入真实上下文后，DeltaNet 因缺少快速清空/过滤能力在长序列掉分；GDN 在 2K/4K 显著高于 DeltaNet/Mamba2。

### S-NIAH-3: UUID in haystack

| Model | 1K | 2K | 4K | 8K |
|---|---:|---:|---:|---:|
| DeltaNet | 85.2 | 47.0 | 22.4 | 待 PDF 复核 |
| Mamba2 | 64.4 | 47.6 | 4.6 | 待 PDF 复核 |
| Gated DeltaNet | 86.6 | 84.2 | 27.6 | 待 PDF 复核 |

观察：UUID 任务测试更复杂模式记忆。GDN 在 1K/2K 优于 DeltaNet/Mamba2，但 4K 仍明显退化，说明 GDN 不是“无限记忆”。8K 列在 `pdftotext` 中缺失，进入正文前必须回看 PDF。

## 2. Table 3 — language modeling + zero-shot commonsense

Table 3 比较语言建模 perplexity 与 commonsense zero-shot accuracy。这里抽取代表性字段和 Avg。

### Recurrent models

| Model | Wiki ppl ↓ | LMB ppl ↓ | LMB acc ↑ | Avg ↑ |
|---|---:|---:|---:|---:|
| RetNet | 19.08 | 17.27 | 40.52 | 52.02 |
| HGRN2 | 19.10 | 17.69 | 39.54 | 51.79 |
| Mamba | 17.92 | 15.06 | 43.98 | 53.12 |
| Mamba2 | 16.56 | 12.56 | 45.66 | 54.89 |
| DeltaNet | 17.71 | 16.88 | 42.46 | 52.14 |
| Gated DeltaNet | 16.42 | 12.17 | 46.65 | 55.32 |

### Attention or hybrid models

| Model | Wiki ppl ↓ | LMB ppl ↓ | LMB acc ↑ | Avg ↑ |
|---|---:|---:|---:|---:|
| Transformer++ | 18.53 | 18.32 | 42.60 | 52.25 |
| Samba | 16.13 | 13.29 | 44.94 | 54.00 |
| Gated DeltaNet-H1 | 16.07 | 12.12 | 47.73 | 56.40 |
| Gated DeltaNet-H2 | 15.91 | 12.55 | 48.76 | 56.18 |

观察：

- 在 recurrent group 中，GDN 的 Avg 55.32 高于 Mamba2 54.89 和 DeltaNet 52.14。
- Hybrid GDN-H1/H2 进一步提高 Avg，说明 GDN 与 SWA/Mamba2 组合后可改善短/常识 benchmark。
- 这些是作者训练设置结果，不能直接外推到 vLLM serving。

## 3. Table 4 — real-world recall-intensive retrieval

| Model | SWDE | SQD | FDA | TQA | NQ | Drop | Avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| RetNet | 14.0 | 28.5 | 7.0 | 54.4 | 16.2 | 17.3 | 22.9 |
| HGRN2 | 8.3 | 25.3 | 4.8 | 51.2 | 14.2 | 16.9 | 20.1 |
| Mamba | 9.8 | 25.8 | 3.7 | 54.3 | 14.9 | 17.4 | 21.0 |
| Mamba2 | 19.1 | 33.6 | 25.3 | 61.0 | 20.8 | 19.2 | 29.8 |
| DeltaNet | 17.9 | 30.9 | 18.4 | 53.9 | 17.3 | 18.6 | 26.2 |
| Gated DeltaNet | 25.4 | 34.8 | 23.7 | 60.0 | 20.0 | 19.8 | 30.6 |
| Transformer++ | 29.5 | 38.0 | 52.2 | 58.3 | 22.5 | 21.6 | 37.0 |
| Samba | 33.0 | 39.2 | 50.5 | 57.7 | 23.5 | 20.2 | 37.3 |
| Gated DeltaNet-H1 | 35.6 | 39.7 | 52.0 | 60.1 | 24.6 | 22.2 | 39.0 |
| Gated DeltaNet-H2 | 38.2 | 40.4 | 50.7 | 63.3 | 24.8 | 23.3 | 40.1 |

观察：

- 纯 recurrent 中 GDN Avg 30.6 高于 Mamba2 29.8 和 DeltaNet 26.2，但差距小于 synthetic S-NIAH。
- Hybrid GDN-H1/H2 明显高于 pure GDN，并超过 Transformer++/Samba 的 Avg。
- 论文也提醒 real-world recall 里小模型 instruction alignment/repetition error 会影响差异。

## 4. Table 5 — LongBench

`pdftotext` 抽取到了完整数值但表头跨页，当前先记录 Avg 和若干组观察，进入正文前需回看 PDF。

| Model | LongBench Avg ↑ |
|---|---:|
| RetNet | 13.2 |
| HGRN2 | 13.5 |
| Mamba | 14.6 |
| DeltaNet | 13.6 |
| Mamba2 | 13.5 |
| Gated DeltaNet | 16.6 |
| Transformer++ | 11.0 |
| Samba | 15.9 |
| Gated DeltaNet-H1 | 17.8 |
| Gated DeltaNet-H2 | 18.4 |

观察：

- GDN 在 pure recurrent group 中 LongBench Avg 最高。
- Hybrid H1/H2 继续提高 LongBench Avg。
- Transformer++ 在该设置下 Avg 低于 hybrid GDN，但这不应泛化为 full attention 在所有长上下文任务差；需要结合模型规模、训练长度和 sliding window 设置。

## 5. 对 Qwen3-Next / Qwen3.5 GDN 的启发

GDN 论文提供的是机制前提和小/中规模 benchmark 证据。Qwen3-Next/Qwen3.5 的 serving 事实还需要：

1. 固定 Qwen checkpoint config；
2. 固定 vLLM tag，例如 v0.25.1；
3. 验证 `QwenGatedDeltaNetAttention` 的 prefill/decode backend；
4. 运行 smoke test 与 serving benchmark。

不能把 GDN 论文中的训练/benchmark 结论直接写成 Qwen3-Next 在 vLLM 上的生产性能。

## 6. 进入正文前必须复核

- Table 2 的 S-NIAH-3 8K 列；
- Table 5 的 14 个 LongBench 子项表头与每项数值；
- H1/H2 的层级组合和 SWA window；
- 论文 appendix 中 400M/1.3B 训练设置；
- NVlabs/GatedDeltaNet repo commit 与实现是否仍可运行。
