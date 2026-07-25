---
source_id: SRC-vllm-rust-frontend-rfc-40846
status: verified
evidence_grade: A
source_type: official-rfc
title: "[RFC]: Rust front-end #40846"
author_or_issuer: "vllm-project"
published: 2026-04-24
verified: 2026-07-25
applies_to: "RFC 提案与 vLLM 0.19.0 benchmark"
url: "https://github.com/vllm-project/vllm/issues/40846"
archive_path: ""
stale_after: 2026-08-08
chapters: ["03", "06", "09", "13", "15"]
---

# 来源摘要

Rust Frontend 的官方 RFC。2026-07-25 核对时仍为 Open。它给出动机、drop-in 集成方式、性能测试环境与限制、初期功能范围和代码归属讨论。

## 支撑的结论

- 项目动机包括 Python 前端 CPU/并发瓶颈、复杂度与多进程扩容成本。
- `VLLM_USE_RUST_FRONTEND` 的渐进接入设想。
- Qwen3-0.6B、DP=4、4×GB200、并发 1024、无限请求速率的 benchmark 数字。
- 作者明确说明测试并非典型真实配置，而是突出 Python 前端上限。

## 限制

- RFC 描述提案与特定时点实现；后续真实行为需以 release 源码和测试为准。
- RFC benchmark 尚未在本仓库复现。

Owner: release tracker
Open questions: RFC 何时关闭、以什么稳定性标准关闭。
Handoff: release impact 与第 9 章。
