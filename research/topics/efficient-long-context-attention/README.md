# 高效长上下文注意力专题

Owner: 未指定
Purpose: 系统研究面向长上下文 LLM 的高效注意力机制，包括稀疏注意力、线性注意力、滑动窗口/混合层、MoBA/Lightning Attention/DSA/NSA 等方法，以及它们对 vLLM 推理、KV cache、并行和 benchmark 的影响。
Status: needs-refresh
Applies to: GLM-5/Kimi Linear/Kimi K3/MiniMax/GDN/Qwen3-Next；目标核对版本 vLLM v0.27.1，v0.26.0 与 `aeeb36b1` 作为历史基线
Evidence grade: A/B/C/D 混合；进入正文前必须回到固定论文版本、上游实现、vLLM release/tag/commit 或本仓实验
Verified date: 2026-08-15
Assumptions: 原目录名 `linear-attention` 过窄；当前主题扩展为 efficient long-context attention，以覆盖 sparse、linear、block、window、hybrid 等多类方法。
Open questions: v0.27.1 中各 hybrid/linear/GDN/KDA 路径的首个包含 commit、Kimi K3 stable release、partial-hit/KDA state correctness，以及目标硬件和 workload 下的性能复现。
Handoff: 第 04、08、09、11、12、15 章。

## 命名判断

原目录 `linear-attention` 不够准确。当前材料包括：

- GLM-5 使用的 DSA / DeepSeek Sparse Attention；
- DeepSeek Native Sparse Attention；
- Kimi MoBA / Mixture of Block Attention；
- MiniMax Lightning Attention；
- GLM-5 论文中比较的 Gated DeltaNet、SimpleGDN、SWA 等 linear/window/hybrid 方案。

这些不全是 linear attention。更合适的主题名是：

```text
research/topics/efficient-long-context-attention/
```

中文标题：**高效长上下文注意力**。

该命名保留 linear attention，但把研究边界扩展到更实际的生产问题：如何降低长上下文 attention 的训练/推理成本，同时保持质量、KV cache 可服务性和硬件效率。

## 当前来源

- [`source/papers/2026-02-24-glm-5-paper-v2.pdf`](source/papers/2026-02-24-glm-5-paper-v2.pdf) — GLM-5 arXiv v2，本地 PDF。
- [`source/papers/2026-07-28-kimi-k3-tech-report.pdf`](source/papers/2026-07-28-kimi-k3-tech-report.pdf) — Kimi K3 技术报告，本地 PDF；用于 KDA serving 系统案例，B 级作者报告。
- [`Kimi K3 vLLM Tech Share.pdf`](Kimi%20K3%20vLLM%20Tech%20Share.pdf)、[`vLLM day-0 Kimi K3支持：探索智能新前沿的推理边界.srt`](vLLM%20day-0%20Kimi%20K3支持：探索智能新前沿的推理边界.srt) — vLLM 技术分享 slides/ASR，D 级解释与发现线索。
- [`source/notes/seed-papers.txt`](source/notes/seed-papers.txt) — 待补充来源列表，包括 NSA、MoBA、MiniMax Lightning Attention。
- [`source/README.md`](source/README.md) — 来源等级、文件校验和引用边界。
- [`claims.yml`](claims.yml) — 本专题 claim spine。
- [`vocabulary.md`](vocabulary.md) — 最小概念系统。
- [`tracking/README.md`](tracking/README.md) — 上游论文、实现和 vLLM 支持状态跟踪规则。
- [`outputs/2026-08-01-kimi-k3-vllm-tech-share-analysis.md`](outputs/2026-08-01-kimi-k3-vllm-tech-share-analysis.md) — 新材料拆解、topic 融合决策、上游版本校正与验证计划。
- [`outputs/chapter-handoff/chapter-placement-proposal.md`](outputs/chapter-handoff/chapter-placement-proposal.md) — 正文呈现与章节落点提案，等待决定是否更新 chapter briefs/正式正文。
- [`outputs/booklet/`](outputs/booklet/) — 当前 topic booklet bundle。

## 共同研究问题

1. 高效长上下文注意力到底优化什么：训练 FLOPs、prefill latency、decode memory、KV cache、还是长上下文质量？
2. Sparse attention、linear attention、sliding-window/hybrid、block routing 的机制边界是什么？
3. 为什么某些 linear/window 方法在长上下文 benchmark 上会退化，而 DSA/NSA/MoBA 试图保留更多内容选择能力？
4. 这些机制对 vLLM serving 的影响是什么：kernel、KV layout、prefix cache、chunked prefill、spec decode、PD/Wide EP 是否受影响？
5. benchmark 如何同时覆盖长上下文质量、TTFT/ITL、吞吐、显存、成本和反例？
6. 哪些能力是模型架构内生的，哪些是 serving engine 可以透明优化的？

## 进入正文前的门禁

- [ ] 固定每篇论文版本、实现仓库和模型 checkpoint。
- [ ] 查明目标 vLLM release 是否支持对应 attention 机制或模型结构。
- [ ] 对每个机制区分训练期收益、prefill 收益、decode 收益和 KV cache 收益。
- [ ] 复现至少一个长上下文质量 benchmark 和一个 serving benchmark。
- [ ] 记录模型、上下文长度、硬件、精度、并行、kernel、batch、cache 状态和指标。
- [ ] 覆盖反例：短上下文、检索式任务、needle、多跳推理、代码 repo QA、低复用 workload。
- [ ] 不把“理论 O(n)”直接写成端到端生产加速。
