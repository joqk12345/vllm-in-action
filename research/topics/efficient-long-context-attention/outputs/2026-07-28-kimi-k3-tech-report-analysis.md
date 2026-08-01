# Kimi K3 Technical Report 对 KDA serving 的启发

Owner: 未指定
Purpose: 捕获 `Kimi K3: Open Frontier Intelligence` 技术报告中与高效长上下文注意力、KDA 系统协同和 serving 相关的可用信息，并给出合并到本专题的边界。
Status: captured; refreshed after vLLM Kimi K3 main merge verification
Applies to: Kimi K3 Technical Report；vLLM main merge `aeeb36b1`；未固定公开报告 URL、HF revision 或首个稳定 vLLM release
Evidence grade: B（作者技术报告；性能、部署和 scaling efficiency 结果未本地复现）
Verified date: 2026-08-01
Assumptions: 本记录只使用本地 PDF 文本抽取与人工快速核读；报告中的 benchmark、部署效果和 scaling efficiency 均按作者报告处理。
Open questions: Kimi K3 的公开报告 URL、HF revisions、首个稳定 vLLM release、镜像/FlashInfer 依赖，以及 KDA-aware cache 的本仓 correctness/performance。
Handoff: 第 08、09、11、12、15 章。

## Source

- Source ID: `SRC-kimi-k3-tech-report-2026-07-28`
- Local file: `source/papers/2026-07-28-kimi-k3-tech-report.pdf`
- SHA256: `1f2978d89a9d7f138f6d6ae5f17fd6890dc673abeaea7fca96c1eca432c75ce8`
- PDF metadata: 47 pages; LaTeX/pdfTeX; creation/modification date 2026-07-28.

## 结论摘要

Kimi K3 报告最适合合并为 **KDA 从 Kimi Linear 论文机制走向 3T 级、1M context、生产 serving 的系统案例**，而不是作为普通排行榜或模型质量 benchmark 来源。

可支撑的 claim 已进入 `claims.yml`：

- `EA-C18`: Kimi K3 的 3:1 KDA–MLA 架构与 69 KDA + 24 MLA 层分布。
- `EA-C19`: hybrid KDA–MLA serving 需要 KDA-aware prefix cache，而不是只复用 MLA KV。
- `EA-C20`: KDA recurrent-state 原地更新与 speculative decoding rollback 的冲突，以及 projected-input replay 方案。
- `EA-C21`: FlashKDA 与 KDA Context Parallelism 处理长上下文 prefill 的 recurrent-state 串行瓶颈。

## 架构信息

报告称 Kimi K3 是 2.8T 参数 MoE，104B activated parameters，native vision，1M-token context window。其 token mixing 使用 hybrid attention：每个 block 包含 3 个 Kimi Delta Attention（KDA）层和 1 个 Gated MLA 层。表格给出 Kimi K3 相比 Kimi K2 的差异：

- Training context length: 128K → 1M
- Attention mechanism: MLA → Hybrid KDA–MLA
- Attention-layer composition: 61 MLA → 69 KDA + 24 MLA

边界：这些是作者报告的设计信息。vLLM PR #50000 已于 2026-07-30 合入 `main`，但晚于 v0.26.0；进入正文或实验前仍需固定 HF revision/config、镜像 digest、依赖和首个稳定 release。

## KDA 系统协同

报告第 5.1 节把 KDA 的系统瓶颈描述为 recurrent state 的串行传播：KDA 用固定大小 recurrent state 替代随上下文增长的 softmax KV cache，但 chunk/segment 间的 state propagation 会限制 GPU 并行度。

作者提出两类设计：

1. FlashKDA：CUTLASS-based chunkwise kernel，用于 training 和 inference prefill，并作为 flash-linear-attention backend auto-dispatch。
2. KDA Context Parallelism：跨 context-parallel ranks 同步 fixed-size recurrent-state fragments，而不是像 softmax attention 那样交换随上下文增长的 KV blocks。

工程启发：讨论 KDA/linear recurrent attention 的 serving 成本时，不能只写“KV cache 固定大小”；还要写 prefill 里的 recurrent dependency、kernel backend 和 context parallelism 是否存在。

## KDA-aware prefix cache

报告第 5.4 节是本专题最有价值的部分。Kimi K3 的 hybrid KDA–MLA 架构同时维护两类 cache：

- MLA KV cache：随 sequence length 增长，按 token/page 管理；
- KDA recurrent state：每个请求固定大小，但 prefix reuse 需要在命中边界恢复 state snapshot。

作者指出，cached prefix 只有在 MLA KV 与 KDA recurrent state 能在同一边界共同恢复时才可复用。因此其 prefix cache 设计包括：

- 将 KDA states 打包到与 MLA KV 相同的 paged pool；
- decouple physical block granularity 与 prefix hash granularity；
- 物理 block 可为 1024–6144 tokens，hash endpoint 可更细，例如 512 tokens；
- KDA checkpoint 只在 sparse subset 的 hash endpoints 或 conversation-turn boundaries 保留；
- hit boundary 必须同时满足 MLA hash 命中和所有 KDA cache group checkpoint 存在。

工程启发：vLLM 讨论 KDA/Kimi Linear prefix cache 时，不能默认沿用 full-attention block-hash KV cache 的语义；需要核查 KDA state snapshot、copy-on-write、eviction 和 PD transfer 是否有专门路径。

## Speculative decoding 风险

报告第 5.4.2 节指出 KDA decoding 与 MTP/speculative decoding 存在特殊冲突：KDA state 在每个 decode step 原地更新；如果 speculative verification 拒绝一部分 draft tokens，state 已经推进到未接受 token 之后，不能简单 rollback。

作者方案是缓存 projected inputs，而不是为每个 draft position 保存完整 state；accepted tokens 的 state 在 fused kernel 内 replay 重建。

工程启发：对于 KDA/linear recurrent attention，spec decode 的正确性和性能不能从 full-attention 模型直接外推。进入正文前应核查 vLLM 的 Kimi Linear/KDA spec decode 路径和 tests。

## 不应直接合并的内容

- 排行榜和专有模型对比：benchmark harness、内部评测和未公开模型差异较大，只能作为背景线索。
- `2.5× scaling efficiency`：报告把收益归因于 KDA、Attention Residuals、Stable LatentMoE、数据和训练 recipe 的组合，不能写成 KDA 单独收益。
- 生产部署效果：可写成作者设计/作者报告，不能写成 vLLM 可用能力。

## 后续验证任务

1. 捕获公开报告 URL 和 Kimi-K3 HF model/config revision。
2. 固定 vLLM Kimi K3 `main@aeeb36b1` 对应的专用镜像 digest、FlashInfer 依赖，并确认首个稳定 release。
3. 设计最小 smoke test：模型加载、KDA/MLA 层识别、prefill、decode、partial prefix hit、eviction/reuse、PD transfer、spec decode rejection。
4. 在 stable release 和本仓复现完成前，把 Kimi K3 保留为 main/special-image 系统设计案例，不进入 vLLM production recommendation。
