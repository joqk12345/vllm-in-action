---
chapter_id: "15-upgrades-and-troubleshooting"
part: IV
title: "升级、回滚与故障诊断"
status: draft
depends_on: ["05-environment-and-installation", "13-observability-and-capacity", "14-reliability-and-security"]
evidence_status: partial
---

# 章节承诺

用版本化基线安全升级，并用证据链而非经验列表诊断问题。

## 必须包含

- release triage、兼容性测试、性能回归与 canary。
- 错误分类：环境、模型、显存、通信、调度、API。
- 最小复现、二分和回滚。
- “修复一个指标、破坏另一个指标”的升级案例。
- 实验性 Rust Frontend 的 feature gate、canary、契约测试与回退路径。

## 读者产物

升级 runbook、诊断决策树与 issue 报告模板。

## 证据缺口

历史破坏性变化样本；典型日志；回滚实践；Rust Frontend 在目标 release 的打包、启用方式和 roadmap 完成度。[SRC-vllm-rust-frontend-pr-40848] [SRC-vllm-rust-frontend-roadmap-44280]
