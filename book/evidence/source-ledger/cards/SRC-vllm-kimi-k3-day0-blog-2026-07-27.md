---
source_id: SRC-vllm-kimi-k3-day0-blog-2026-07-27
status: verified
evidence_grade: B
source_type: official-blog
title: "Kimi K3 Is Here: Efficient Day-0 Support on vLLM"
author_or_issuer: "vLLM Team and Inferact"
published: 2026-07-27
verified: 2026-08-01
applies_to: "Kimi K3 day-0 vLLM integration and author-reported serving results; not a stable release boundary"
url: "https://vllm.ai/blog/2026-07-27-k3"
archive_path: ""
stale_after: 2026-09-01
chapters: ["08", "09", "11", "12", "15"]
---

# 来源摘要

vLLM 与 Inferact 发布的 Kimi K3 day-0 支持说明。它把 Kimi K3 的混合 KDA/full-attention cache、DSpark、prefill/decode disaggregation、partial block cache hit、KDA kernels 和 LatentMoE 优化放进同一生产 serving 叙事，并给出可复现 recipe。

## 支撑的结论

- 官方博客把 Kimi K3 支持表述为 day-0 支持，并给出 `moonshotai/Kimi-K3` 与 `Inferact/Kimi-K3-DSpark` 的启动/benchmark recipe。
- 博客报告：16 张 NVIDIA GB300 NVL72、TP16、batch size 1、SPEED Bench 条件下，不启用 speculative decoding 为 118 tok/s/user，启用 DSpark 为 370 tok/s/user；TP8 对应 111 与 331 tok/s/user。
- 博客说明 Kimi K3 serving 涉及 hybrid KDA/full-attention cache、partial block cache hit、PD disaggregation、KDA decode/prefill kernels、KDA metadata builder 和 LatentMoE tail fusion。
- 博客说明至少需要 8×B300/GB300 节点，或 16×B200；AMD MI355X 也在 launch 支持范围内。

## 限制与反证

- 博客是官方一手说明，但性能数字仍是作者报告，未在本仓复现。
- `day-0` 描述发布时间/可用镜像，不等于某个稳定 release 已包含全部实现。
- 性能数字不能脱离 GPU、TP、batch size、dataset、DSpark 配置、MXFP4/FP8 cache 和 backend 外推。
- 博客描述的 DSpark、LatentMoE、PD disaggregation 和多模态能力不应全部归因于 KDA。

## 验证记录

- [x] 标题、作者、发布日期和 canonical URL 已于 2026-08-01 核对。
- [x] benchmark 的 TP8/TP16、GB300 NVL72、batch size 1 与 DSpark 边界已提取。
- [x] 与 PR #50000、RFC #45702 和本地技术分享交叉核对。
- [ ] 本仓按官方 recipe 复现。
- [ ] 固定首个包含 Kimi K3 的稳定 vLLM release。

Owner: 未指定
Open questions: 官方 recipe 使用的镜像 digest、FlashInfer 依赖和 HF revision 尚未固定。
Handoff: efficient-long-context-attention；第 08、09、11、12、15 章。
