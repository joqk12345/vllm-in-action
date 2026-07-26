---
source_id: SRC-kimi-linear-repository
status: captured
evidence_grade: A
source_type: source-code
title: "MoonshotAI/Kimi-Linear repository"
author_or_issuer: "Moonshot AI / Kimi Team"
published: null
verified: 2026-07-26
applies_to: "GitHub repository HEAD fixed at 8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3; README deployment and model links"
url: "https://github.com/MoonshotAI/Kimi-Linear/tree/8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3"
archive_path: ""
stale_after: 2026-08-26
chapters: ["09", "11", "12", "15"]
---

# 来源摘要

Kimi Linear 官方仓库。当前固定 commit `8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3` 的 README 提供论文、Hugging Face checkpoint、`fla-core` 依赖和 vLLM serve 示例。

## 支撑的结论

- README 推荐 Transformers 推理依赖 `python >= 3.10`、`torch >= 2.6`、`fla-core >= 0.4.0`。
- README 给出 `moonshotai/Kimi-Linear-48B-A3B-Base` 与 `moonshotai/Kimi-Linear-48B-A3B-Instruct`，context length 为 1M。
- README 给出使用 latest vLLM 启动 OpenAI-compatible endpoint 的示例命令。

## 限制

- README 的 “latest vllm” 不是固定 release；生产建议必须回到 vLLM tag/commit、安装环境和测试。
- 仓库不等于本仓已复现性能数字。

Owner:
Open questions: 固定 vLLM release、依赖版本、GPU 拓扑、benchmark 配置。
Handoff: efficient-long-context-attention topic。