---
title: "<主题名称>"
subtitle: "主题研究小册子"
status: captured
edition: "0.1"
created: YYYY-MM-DD
verified: YYYY-MM-DD
topic: <topic-id>
applies_to: "<版本、模型、硬件、拓扑或时间边界>"
source_ids: []
chapters: []
---

# <主题名称>

Owner:
Purpose: 支持系统性主题阅读、专项研讨和章节交接
Status: captured
Applies to:
Evidence grade:
Verified date:
Assumptions:
Open questions:
Handoff:

## 1. 执行摘要

- 这个主题解决什么问题？
- 当前最可靠的三个结论是什么？
- 最危险的错误泛化是什么？
- 下一项验证动作是什么？

## 2. 共同研究问题

### Q1：

### Q2：

### Q3：

## 3. 最小概念系统

| Noun | 定义 | 关键 verbs | 容易混淆的概念 |
|---|---|---|---|

## 4. 系统模型

描述组件、边界、数据流、控制流和不变量。优先引用可复用图，不按单篇来源复述。

## 5. 跨来源命题

| Claim | Proposition | Evidence | Applies to | Counterexample |
|---|---|---|---|---|

## 6. 来源如何相互校正

| 来源 | 最适合回答 | 不支持 | 与其他来源的关系 |
|---|---|---|---|

## 7. 分歧与未决问题

- 来源间事实冲突；
- 术语或问题定义不同；
- roadmap 与 release 的时间差；
- 没有足够证据回答的问题。

## 8. 验证与实验

| Test/Experiment | Hypothesis | Baseline | Metrics | Completion criteria |
|---|---|---|---|---|

## 9. 生产决策

- 适用条件；
- 代价与失效边界；
- 观测信号；
- canary；
- rollback。

## 10. 结论分层

### 已证实事实

### 工程判断

### 待验证假设

### 不得写成事实

## 11. 动态附录

只链接版本、Issue、watchlist、capability matrix 和变化日志，不在主体复制高频变化清单。

## 12. 研讨结论模板

```text
Decision:
Target version/commit:
Target workload:
Accepted claims:
Rejected generalizations:
Required tests/experiments:
Owner:
Review date:
```
