---
source_id: SRC-vllm-partial-cache-rfc-45702
status: verified
evidence_grade: B
source_type: upstream-rfc
title: "[RFC]: Partial Cache Hits for Hybrid Models"
author_or_issuer: "vllm-project/vllm contributors"
published: 2026-06-15
verified: 2026-08-01
applies_to: "vLLM hybrid full-attention + Mamba/GDN/KDA prefix caching; RFC remains open"
url: "https://github.com/vllm-project/vllm/issues/45702"
archive_path: ""
stale_after: 2026-09-01
chapters: ["04", "08", "11", "13", "15"]
---

# 来源摘要

该 RFC 提议把 prefix-cache hash granularity 与物理 cache block size 解耦，引入 `hash_block_size`、partial aliases、显式 `hit_length` 和 copy-on-write，以缓解 hybrid 模型因 Mamba/KDA state 对齐而产生的粗粒度命中问题。

## 支撑的结论

- 物理 block 仍是分配/所有权单位；`hash_block_size` 只改变 prefix lookup 粒度。
- full-attention partial hit 需要把可复用 KV slice copy-on-write 到新 block，避免修改旧请求共享的 partial block。
- Mamba/KDA final-tail checkpoint 仍存在 scheduler split 与 backend checkpoint materialization 两种设计选择。
- 相关实现 PR #45939、#46384、#49502 已合入，但 RFC 本身仍为 open，且 same-step reuse、final-tail checkpointing 等问题仍动态变化。

## 限制与反证

- RFC 是设计与状态信号，不等于稳定 CLI、默认值或 release 保证。
- `hash_block_size` 越小不必然越好：更细命中与 hash/alias/state checkpoint/内存开销之间需要按 workload 权衡。
- Kimi K3 技术分享中“已端到端支持”的口头描述必须回到具体 PR、commit、tests 和 release 验证。

## 验证记录

- [x] RFC 状态、正文与相关 PR 已于 2026-08-01 核对。
- [x] 三个相关 PR 的 merge commit 已记录。
- [ ] 固定首个包含完整 partial-hit 路径的稳定 release。
- [ ] 本仓复现多轮对话、system prompt、tool-call boundary 的 TTFT/cache-hit 收益。

Owner: 未指定
Open questions: final-tail checkpoint、same-step reuse、offload/PD data race 的最终设计。
Handoff: efficient-long-context-attention；第 04、08、11、13、15 章。
