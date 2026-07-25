---
source_id: SRC-vllm-rust-frontend-roadmap-44280
status: verified
evidence_grade: A
source_type: official-roadmap
title: "[Roadmap] Rust Frontend Feature Parity #44280"
author_or_issuer: "vllm-project"
published: 2026-06-02
verified: 2026-07-25
applies_to: "Rust Frontend roadmap 的动态状态；正文前必须重新核对"
url: "https://github.com/vllm-project/vllm/issues/44280"
archive_path: ""
stale_after: 2026-08-01
chapters: ["03", "06", "09", "13", "14", "15"]
---

# 来源摘要

Rust Frontend 的官方 feature-parity roadmap。2026-07-25 核对时仍为 Open，列出当前已实现范围，以及分布式服务、API、请求兼容、生产就绪、LoRA、多模态、生命周期和 parser 等待补能力。

## 支撑的结论

- Rust Frontend 已进入主仓库，但仍是 experimental，尚未与 Python Frontend 完成功能对齐。
- 当前核心能力包括 chat/completions 的流式与非流式路径、部分 tool/reasoning 支持、常用采样参数、有限多模态、内部负载均衡、运维端点和测试基础设施。
- production readiness 路线仍明确包含 TLS、API key、CORS、reverse-proxy root path、日志参数等事项。
- 项目目标不是机械复制 Python Frontend 的所有行为；低价值、实现细节型或应重新设计的功能可能不会 1:1 移植。

## 不支撑

- roadmap 条目已经发布到某个稳定 release。
- 某个未勾选能力在所有分支中都不可用。
- Rust 与 Python Frontend 已经可以无条件互换。

## 动态性

该 Issue 是活跃清单。引用具体 feature 前，必须继续检查关联 PR、合并 commit、release tag 和测试；Issue 文本只能说明 roadmap 状态，不能替代发布验证。

## 验证记录

- [x] 官方仓库和 Issue 状态已核对
- [x] 创建日期、当前能力与 roadmap 分类已核对
- [x] 与 RFC #40846 和主仓库 `rust/` README 交叉验证
- [ ] 尚未建立 endpoint 级 feature-parity 自动测试

Owner: release tracker
Open questions: 哪个 release 首次达到本书定义的 production-ready 最小集合。
Handoff: 第 6、14、15 章与 Rust Frontend 专题。
