---
title: "投机解码最小系统词汇"
status: working
topic: speculative-decoding
created: 2026-07-25
verified: 2026-07-25
applies_to: "投机解码算法、vLLM serving、DSpark 案例与性能分析"
source_ids:
  - SRC-dspark-paper-v1
  - SRC-speculators-main
chapters: ["10", "11"]
---

# 投机解码最小系统词汇

Purpose: 用最小但系统的 nouns/verbs 描述投机解码的正确性、性能与生产边界。
Evidence grade: B
Assumptions: 这是分析词汇，不等同于某个 vLLM 版本的类名或配置字段。
Open questions: 固定 vLLM release 后，将概念映射到 scheduler、model runner、sampler 和 metrics。
Handoff: 第 10、11 章。

## 10 个核心 nouns

| Noun | 中文 | 含义 | 最重要的 verbs |
|---|---|---|---|
| **Target model** | 目标模型 | 定义最终采样分布、负责验证候选的大模型 | `verify`、`accept`、`correct` |
| **Drafter** | 草稿模型 | 以较低成本提出未来 token 的模型或预测头 | `draft`、`propose`、`train` |
| **Draft block** | 草稿块 | 一轮中提出的候选 token 序列 | `generate`、`truncate`、`verify` |
| **Candidate token** | 候选 token | 等待 target 判定的单个 draft token | `score`、`accept`、`reject` |
| **Accepted prefix** | 接受前缀 | 从块起点连续通过验证的最长前缀 | `measure`、`append` |
| **Acceptance length** | 接受长度 | 每轮被接受的 token 数，常记作 `τ` | `measure`、`maximize`、`compare` |
| **Proposal length** | 提议长度 | drafter 每轮最多产生的 token 数，常记作 `γ` | `configure`、`adapt`、`cap` |
| **Confidence** | 置信度 | 对候选或前缀通过 target 验证概率的估计 | `predict`、`calibrate`、`rank` |
| **Verification budget** | 验证预算 | target 一步为候选 token 提供的 batch/compute 容量 | `allocate`、`schedule`、`prune` |
| **Workload** | 工作负载 | 模型、请求域、采样、并发、长度与硬件条件的组合 | `profile`、`benchmark`、`segment` |

## 12 个核心 verbs

| Verb | 中文 | 主语 | 宾语或结果 |
|---|---|---|---|
| `draft` | 起草 | Drafter | Draft block |
| `propose` | 提议 | Drafter | Candidate tokens |
| `verify` | 验证 | Target model | Draft block |
| `accept` | 接受 | Verification rule | 与 target distribution 一致的前缀 |
| `reject` | 拒绝 | Verification rule | 首个失败 token 及其后缀 |
| `correct` | 纠正 | Target model | rejection position 的 token |
| `calibrate` | 校准 | Validation process | Confidence |
| `schedule` | 调度 | Prefix scheduler | Verification budget |
| `prune` | 裁剪 | Scheduler | 低预期收益的候选后缀 |
| `profile` | 刻画 | Benchmark/operator | 硬件容量与负载曲线 |
| `measure` | 测量 | Experiment | 接受长度、ITL、吞吐、goodput |
| `fallback` | 回退 | Serving system | 普通自回归解码 |

## 最小处理语法

```text
Drafter drafts/proposes a Draft block
         ↓
Scheduler calibrates confidence
          and allocates Verification budget
         ↓
Target model verifies Candidate tokens
         ↓
Verification rule accepts the longest prefix
                  or rejects and corrects
         ↓
Experiment measures latency, throughput and goodput
         ↓
Serving system keeps speculation or falls back
```

压缩为：

```text
提议 → 调度 → 验证 → 接受/拒绝 → 纠正 → 测量 → 保留/回退
```

## 三组必须保持的区别

### 接受长度与端到端收益

`Acceptance length ↑` 不自动推出 `ITL ↓` 或 `throughput ↑`。至少还要同时观察：

```text
drafter cost + target verification cost + scheduling/communication cost
```

### Lossless 与“每次输出完全相同”

Lossless 指正确算法保持 target distribution；它不表示在随机采样下，两次运行必须生成完全相同的 token 序列。

### 算法能力与生产支持

论文提出算法后，还要分别验证：

```text
implemented → tested → released → benchmarked → observable → rollback-ready
```
