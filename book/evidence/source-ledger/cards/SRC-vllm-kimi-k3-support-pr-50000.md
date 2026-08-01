---
source_id: SRC-vllm-kimi-k3-support-pr-50000
status: verified
evidence_grade: A
source_type: source-code-pr
title: "[New model] Kimi K3"
author_or_issuer: "vllm-project/vllm contributors"
published: 2026-07-30
verified: 2026-08-01
applies_to: "vLLM main merge commit aeeb36b1f17145975c6713242f2447bb8b98782b; not contained in v0.26.0"
url: "https://github.com/vllm-project/vllm/pull/50000"
archive_path: ""
stale_after: 2026-09-01
chapters: ["08", "11", "12", "15"]
---

# 来源摘要

Kimi K3 总集成 PR。PR 于 2026-07-30 合入 `main`，merge commit 为 `aeeb36b1f17145975c6713242f2447bb8b98782b`。固定 commit 的 supported-models 表登记 `KimiK3ForConditionalGeneration` / `moonshotai/Kimi-K3`。

## 支撑的结论

- Kimi K3 model/kernels、Python frontend、Rust frontend 和 Attention Residual kernels 分别由 PR #50089、#50093、#50104、#50090 合入，总 PR #50000 随后完成合并。
- 变更触及 Kimi K3 model、KDA、MLA backend、partial prefix-cache tests、DSpark config/tests、LatentMoE runner、MXFP4 MoE、scheduler 和 KV-cache interface。
- PR 描述要求使用 `vllm/vllm-openai:kimi-k3` 镜像，并在 2026-07-30 注明仍需 FlashInfer `v0.6.16rc5`。
- v0.26.0 是合并前的最新稳定 release，因此不能用 v0.26.0 支撑 Kimi K3 模型注册或端到端 serving 结论。

## 限制与反证

- `main` merge 证明源码已合入，不等于首个稳定 release、所有 wheel 或所有硬件组合均可用。
- supported-models 登记和 kernel/unit tests 不等于本仓完成端到端 serving、prefix-cache correctness 或性能复现。
- PR 使用 release candidate 依赖，生产采用前必须固定镜像 digest、FlashInfer 版本和后续 release 边界。

## 验证记录

- [x] PR 状态、merge timestamp、merge commit 与拆分 PR 已通过 GitHub API 核对。
- [x] 固定 merge commit 的 supported-models 条目已核对。
- [x] 最新稳定 release v0.26.0 与 merge timestamp 已比较。
- [ ] 固定 `kimi-k3` 镜像 digest。
- [ ] 确认首个包含 merge commit 的稳定 release/tag。
- [ ] 运行本仓 smoke test 与 benchmark。

Owner: 未指定
Open questions: FlashInfer RC 依赖何时进入稳定依赖；后续 release 是否改变 Kimi K3 专用路径。
Handoff: efficient-long-context-attention；第 08、11、12、15 章。
