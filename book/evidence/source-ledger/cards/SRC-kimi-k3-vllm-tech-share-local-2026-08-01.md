---
source_id: SRC-kimi-k3-vllm-tech-share-local-2026-08-01
status: captured
evidence_grade: D
source_type: local-slides-and-asr-transcript
title: "Kimi K3 vLLM Tech Share / vLLM day-0 Kimi K3 支持"
author_or_issuer: "Jiangyun Zhu and Yongye Zhu, Inferact; publication event/date not yet fixed"
published: null
verified: 2026-08-01
applies_to: "local 23-page slides and 95-minute ASR transcript; discovery and explanation only"
url: ""
archive_path: "research/topics/efficient-long-context-attention/Kimi K3 vLLM Tech Share.pdf"
stale_after: 2026-09-01
chapters: ["08", "11", "12", "13", "15"]
---

# 来源摘要

用户补充的 Kimi K3 vLLM 技术分享 PDF、自动字幕和链接说明。演讲者署名为 Inferact 的 Jiangyun Zhu、Yongye Zhu，内容覆盖 hybrid memory allocator、block-aligned scheduling、partial cache hit、Marconi-style retention、DSpark、PDL 和 LatentMoE tail optimization。

## 本地文件

- PDF：`research/topics/efficient-long-context-attention/Kimi K3 vLLM Tech Share.pdf`，23 页，SHA256 `f9a1c8cf1736f97f3d2cad11c66c0870be3d70a3ba90db90d8ed390ba08760d2`。
- SRT：`research/topics/efficient-long-context-attention/vLLM day-0 Kimi K3支持：探索智能新前沿的推理边界.srt`，SHA256 `2f56f81f4dbbdbbd5f4c989fb68fb8f7cf27e7c38d00618231af1102088bf6db`。
- 链接说明：`research/topics/efficient-long-context-attention/k3_info.txt`，SHA256 `b2679aaa7de5fecd8fd5db4c8722ebf6207abc52268c8e90c19b47f3d18ee557`。

## 可用于发现的问题

- KDA recurrent state 如何打破 append-only KV cache 假设。
- hybrid allocator/page alignment 如何把 KDA state 与 MLA KV 放进统一管理框架。
- block-aligned scheduling 与 partial hit 如何平衡 state checkpoint 成本和 cache-hit granularity。
- tensor reuse/zeroing 与 PD/RDMA 写入之间如何避免 stale data、NaN 或 data race。
- 低并发优化为何需要 PDL、专用 GEMM 和 LatentMoE tail fusion。

## 限制与反证

- SRT 为自动语音识别，包含大量术语误转，不能作权威引文或数值来源。
- PDF 未包含活动 URL、发布日期、版本/commit 或完整 benchmark manifest。
- 演讲口头报告的 410/464 tok/s 与 2026-07-27 官方博客的 331/370 tok/s 不一致；在硬件、代码快照和 workload 对齐前不得选用其中一组作为稳定事实。
- 该来源只做解释与线索；稳定结论使用官方博客、PR、RFC、release/tag 和本仓实验。

## 验证记录

- [x] PDF 文本与关键页面已人工复核。
- [x] SRT 的 allocator/cache/partial-hit/kernel 段落已按时间轴拆解。
- [x] 链接已回到 vLLM 官方博客、recipe、PR #50000 和 RFC #45702 核验。
- [ ] 补充原始活动/回放 URL、发布日期和字幕来源。
- [ ] 获取可引用的原始讲稿或公开 slides URL。

Owner: 未指定
Open questions: 活动日期、公开视频 URL、talk 性能数字的代码/硬件/workload 条件。
Handoff: 仅作为当前 topic 的 Kimi K3 serving case-study 线索。
