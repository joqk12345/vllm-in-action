# 投机解码持续跟踪

Owner: release tracker
Purpose: 跟踪 DSpark、Speculators 与 vLLM speculative decoding 的算法和实现漂移
Status: active
Applies to: 研究阶段跟踪论文和上游 `main`；正文结论固定到 release/tag/commit
Evidence grade: discovery only；接受结论时回到论文版本、源码、测试或本仓实验
Verified date: 2026-07-25
Assumptions: 上游 README/文档负责发现能力，不证明目标 workload 已可用
Open questions: 第一个可在本书基准环境稳定复现 DSpark 端到端收益的版本组合
Handoff: 第 10、11、15 章

## 跟踪对象

| 对象                                                                                   | 关注变化                                                               | 进入正文前的固定点            |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ | -------------------- |
| [DSpark arXiv](https://arxiv.org/abs/2607.05147)                                     | 新版本、勘误、实验或限制变化                                                     | arXiv version        |
| [Speculators](https://github.com/vllm-project/speculators)                           | DSpark/DFlash/EAGLE 支持、checkpoint config、hidden-state connector、测试 | commit 或 release     |
| [vLLM](https://github.com/vllm-project/vllm)                                         | speculative decoding model runner、sampler、scheduler、配置和兼容性         | release tag + commit |
| [vLLM speculative decoding 文档](https://docs.vllm.ai/en/latest/features/spec_decode/) | 支持矩阵、限制、参数和默认行为                                                    | 对应 release 文档        |
| 本仓库实验                                                                                | latency、throughput、goodput、显存和回退                                   | 环境 manifest + 原始结果   |

## 节奏

- 每个 vLLM 或 Speculators release：复查支持、配置和测试。
- 每月：检查论文版本、相关方法和 checkpoint 更新。
- 每季度或关键实现变化后：刷新端到端 benchmark。

## 漂移分诊

1. 记录发生变化的 URL、日期、commit/release 和相关 claim。
2. 区分算法变化、训练框架变化、vLLM serving 变化和模型 checkpoint 变化。
3. 用源码与测试确认 README/文档中的能力是否真实落入目标版本。
4. 标记需要重跑的 workload、指标和基线。
5. 先更新 `claims.yml` 和来源信息，再刷新 booklet、brief 或章节 handoff。

动态支持状态不得覆盖稳定主体。即使某个算法被移除或配置改名，`draft → verify → accept/reject → measure` 的分析框架仍应保持有效。
