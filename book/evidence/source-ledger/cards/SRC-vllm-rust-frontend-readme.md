---
source_id: SRC-vllm-rust-frontend-readme
status: verified
evidence_grade: A
source_type: source-code-docs
title: "vLLM rust/ README and implementation"
author_or_issuer: "vllm-project"
published: null
verified: 2026-07-25
applies_to: "main branch as verified;正文前必须固定 release tag/commit"
url: "https://github.com/vllm-project/vllm/tree/main/rust"
archive_path: ""
stale_after: 2026-08-08
chapters: ["03", "06", "13", "15"]
---

# 来源摘要

官方主仓库当前 Rust workspace 和 README。2026-07-25 核对时明确称其为替代 northbound serving layer 的 drop-in frontend，同时仍连接 Python engine，并标记为 experimental、not feature-complete。

## 支撑的结论

- 当前代码位于 vLLM 主仓库 `rust/`。
- workspace 的主要 crate 分层。
- Python-supervised 与 standalone/external-engine 的当前入口说明。
- 当前官方成熟度表述。

## 限制

- `main` 是浮动分支，不能作为长期稳定正文锚点。
- README 不能替代 endpoint 契约测试和生产实验。

Owner: chapter 06
Open questions: 首个适合作为书稿基线的 release tag。
Handoff: 功能矩阵与 canary 实验。
