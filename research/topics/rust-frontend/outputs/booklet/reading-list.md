---
title: "Rust Frontend 主题阅读清单"
status: captured
created: 2026-07-25
verified: 2026-07-25
topic: rust-frontend
---

# Rust Frontend 主题阅读清单

Owner: performance research / book editorial
Purpose: 按共同问题安排多来源阅读，并规定每轮应产生的研究输出
Status: captured
Applies to: Rust Frontend 架构、能力、性能与生产采用研究
Evidence grade: 按来源卡分别记录；C/D 级不得越级支撑事实
Verified date: 2026-07-25
Assumptions: 阅读者能够访问 topic 内材料和 vLLM 官方上游
Open questions: 目标 release、能力测试与本地复现实验
Handoff: claim spine、capability matrix、小册子和专项研讨

这份清单按问题组织，不按资料发布时间组织。阅读时先写下问题，再从多个来源提取命题、适用边界和反例。

## 第一轮：建立问题和边界

目标：用 30～45 分钟回答“为什么做、替换什么、没有替换什么”。

| 顺序 | 阅读材料 | 关注问题 | 输出 |
|---:|---|---|---|
| 1 | RFC #40846 | 动机、engine boundary、benchmark 假设 | 3 个核心命题和 3 个不能外推的结论 |
| 2 | Integration PR #40848 | 集成边界和启用方式 | 进程/组件关系 |
| 3 | `rust/` README | workspace 分层和数据流 | nouns/verbs 到源码入口的初步映射 |

不要在第一轮判断 production-ready。

## 第二轮：比较设计主张

目标：回答“Rust 实现是否只是语言替换”。

| 主题 | 主来源 | 对照来源 | 阅读动作 |
|---|---|---|---|
| Workspace layering | `rust/` README | 演讲 PDF | 对齐 Server/Chat/Text/LLM/Client |
| Streaming | README/设计说明 | 研究笔记 | 区分 token/text/event/SSE |
| Parser | Issue #44280 | 演讲 PDF | 提取 redesigned 与 parity 的张力 |
| Launcher | RFC/PR | 目标 tag 源码 | 验证环境变量和进程监管 |

输出一张请求生命周期图，并标出每个边界的错误与取消语义。

## 第三轮：建立能力契约

目标：把“支持/不支持”改写成可测试问题。

1. 读取 Issue #44280 的 Current status。
2. 只选择目标 workload 使用的 endpoint、参数、模型和运维能力。
3. 在 `capability-matrix.yml` 记录 roadmap 状态。
4. 找到关联 PR、merge commit 和首个 release。
5. 在目标 tag 执行或补充契约测试。

禁止把 `roadmap_status: checked` 自动改写成 `release_status: verified`。

## 第四轮：审查性能证据

目标：判断 benchmark 的适用范围。

阅读 RFC benchmark 时逐项记录：

```text
version
model
hardware
precision
parallelism
prompt/output distribution
concurrency
request rate
cache state
frontend process count
metrics
missing metrics
```

随后设计两组实验：

- 尽量复现原 benchmark 的 frontend-bound 条件；
- 使用更大模型构造 GPU-bound 对照。

## 第五轮：生产与反例

目标：回答“怎样失败、怎样发现、怎样恢复”。

按以下顺序阅读：

1. roadmap 的 production readiness、lifecycle 和 testing 部分；
2. 目标 tag 的 server args、metrics 和 integration tests；
3. 本仓库第 14、15 章 brief；
4. capability matrix 的 operations 项。

每个能力至少写出：

- 成功行为；
- 明确拒绝行为；
- 超时、断连和 overload 行为；
- 观测信号；
- fallback。

## 第六轮：版本更新

每周：

```bash
python3 scripts/check_rust_frontend_tracking.py
```

每个新 release：

1. 从 Version Monitor 发现 release 和相关 release-note 段落；
2. 回到 vLLM 官方 release、PR、tag 和测试；
3. 更新 capability matrix；
4. 判断 RF claim 是否需要修改；
5. 记录受影响章节和输出；
6. 完成人工复核后接受 tracking 基线。

## 阅读笔记最小格式

```text
Question:
Source:
Proposition:
Evidence grade:
Applies to:
Counterexample:
Conflict with:
Needs verification:
Claim/handoff:
```

只有能够跨来源回答同一个 Question 的笔记，才进入主题综合；单篇资料摘要继续保留在 research notes。
