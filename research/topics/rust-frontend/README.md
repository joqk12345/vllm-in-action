# Rust Frontend 专题

Owner: 未指定
Purpose: 追踪 vLLM Rust Frontend 的动机、架构、性能边界与生产成熟度
Status: needs-refresh
Applies to: vLLM Rust frontend；目标核对版本 v0.27.1，演讲 benchmark 的 v0.19.0 仅作历史基线
Evidence grade: A/B 混合
Verified date: 2026-08-15
Assumptions: 暂未在本仓库环境复现实验
Open questions: v0.27.1 中实际进入 release 的能力、API/parser parity、TLS/auth/LoRA/multimodal 缺口、资源成本、稳定性和真实 GPU-bound 工作负载收益
Handoff: 第 3、6、9、13、14、15 章

## 目录

- [`research-notes.md`](research-notes.md) — 对演讲内容、RFC 与后续落地的结构化研究笔记。
- [`feature-parity-roadmap.md`](feature-parity-roadmap.md) — Issue #44280 的动态能力与缺口快照。
- [`vocabulary.md`](vocabulary.md) — 9 个核心 nouns、12 个核心 verbs 及其处理语法。
- [`talk-transcript-part-01-notes.md`](talk-transcript-part-01-notes.md) — `00:00–16:38` 自动转写的内容理解、术语勘误与待验证问题。
- [`talk-transcript-part-02-notes.md`](talk-transcript-part-02-notes.md) — 无时间戳续篇的内容理解，重点补齐分层、stream-native、parser、接入方式和长期方向。
- [`claims.yml`](claims.yml) — Brief、PPT、章节转写包和共享图共同使用的 claim spine。
- [`tracking/`](tracking/) — Issue #44280、vLLM release 与 Version Monitor 的持续漂移检测、基线和变化日志。
- [`outputs/booklet/`](outputs/booklet/) — 系统性主题阅读小册子、专项研讨指南、阅读清单和 capability matrix。
- [`outputs/`](outputs/) — 从本专题研究转出的 Brief、PPT、章节转写包和共享图。
- [`source/vllm-rust-frontend-introduction.pdf`](source/vllm-rust-frontend-introduction.pdf) — 16 页原始演讲 PDF，SHA-256：`dd20c1bd34448f25443fe19400e6493b8bcee4108625ff8af0edbafd0c906f60`。
- [`source/transcripts/2026-07-25-rust-frontend-talk-part-01.txt`](source/transcripts/2026-07-25-rust-frontend-talk-part-01.txt) — 未清洗的 ASR 原始转写，只作为 D 级研究线索。
- [`source/transcripts/2026-07-25-rust-frontend-talk-part-02.txt`](source/transcripts/2026-07-25-rust-frontend-talk-part-02.txt) — 未清洗且无时间戳的 ASR 续篇，只作为 D 级研究线索。

## 应如何进入书稿

这份材料不应整篇复制到正文。建议拆成六种用途：

| 内容                                       | 进入位置   | 使用方式                  |
| ---------------------------------------- | ------ | --------------------- |
| Python/Rust frontend 与 Python engine 的边界 | 第 3 章  | 请求生命周期图中的前端分支         |
| stream-native、parser、API feature parity  | 第 6 章  | API 契约与实验性前端案例        |
| frontend-bound benchmark                 | 第 9 章  | “压力测试证明什么、不证明什么”的方法案例 |
| CPU 前端瓶颈与多进程成本                           | 第 13 章 | 可观测性和容量规划信号           |
| 安全、观测与仍未闭合的能力契约                        | 第 14 章 | 生产安全边界                |
| 可选启用、灰度与回退                               | 第 15 章 | 实验性路径升级 runbook       |

## 当前可安全引用的判断

- Rust frontend 是替代北向 serving 层的可选实现，仍通过现有 engine 边界连接 Python engine。
- 2026-07-25 核对时，官方主仓库将其明确标为 experimental、尚未 feature-complete。
- RFC benchmark 是刻意构造的 frontend-bound 压力测试，适合证明前端上限，不适合外推所有模型和部署。
- 集成 PR 已合并；原 Inferact 仓库已归档，当前实现位于 vLLM 主仓库 `rust/`。

## 进入正文前仍需完成

- [ ] 固定一个 vLLM release tag，而不是引用浮动 `main`。
- [ ] 建立 Python 与 Rust frontend 的 endpoint/参数兼容矩阵。
- [ ] 按 Issue #44280 复查生产就绪缺口，不把 roadmap 当成已发布能力。
- [ ] 复现至少一个 frontend-bound 和一个 GPU-bound workload。
- [ ] 同时采集 CPU、内存、TTFT、ITL、吞吐和错误率。
- [ ] 验证启用、canary、回退和观测方法。
- [ ] 复查 Rust frontend 在目标 release 中的稳定性标记。

## 持续跟踪

本专题使用两个发现信号，但只以固定版本的 vLLM 上游材料作为最终事实：

- Issue #44280：发现 roadmap、checkbox、评论和关联实现发生变化；
- vLLM Version Monitor：发现新 release 和可能相关的 release note；
- vLLM tag/commit/test：确认能力是否真正发布；
- 本仓库实验：确认能力是否适用于书中的目标 workload。

每周自动运行：

```bash
python3 scripts/check_rust_frontend_tracking.py
```

检测到漂移时，按 [`tracking/README.md`](tracking/README.md) 完成人工分诊；不要因为 Issue 被勾选或 Version Monitor 出现关键词就直接修改正文结论。
