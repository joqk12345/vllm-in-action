---
title: "Rust Frontend Feature Parity Roadmap 快照"
status: captured
verified: 2026-07-25
source_ids:
  - SRC-vllm-rust-frontend-roadmap-44280
applies_to: "GitHub Issue #44280 在 2026-07-25 的动态状态"
chapters: ["06", "13", "14", "15"]
---

# Rust Frontend Feature Parity Roadmap 快照

## 为什么单独记录

演讲回答“为什么做”和“怎样设计”，roadmap 回答“当前能做什么、距离生产替代还缺什么”。后者变化频繁，因此保留为研究快照，不把完整 checklist 复制到正文。

官方 roadmap 的关键原则不是追求机械的 1:1 parity，而是优先用户价值与 Rust Frontend 的架构目标。低频生产功能、Python 实现细节或需要重新设计的复杂功能，可能被跳过或重新定义。[SRC-vllm-rust-frontend-roadmap-44280]

## 2026-07-25 能力快照

本次基线对应 Issue 更新时间 `2026-07-24T11:34:59Z`，正文 SHA-256 为
`18dc5249c3be01bccde1edfb76a092c4938936dd728a56451e284b19b3e64a5a`。
Roadmap 共记录 40 项完成、61 项未完成。

Roadmap 当前列出的已有核心能力包括：

- `/v1/chat/completions` 与 `/v1/completions` 的流式、非流式处理；
- 若干关键模型家族的 tool calling 与 reasoning output；
- 常用 OpenAI-compatible 采样参数；
- 已注册 image processor/model 的 image-only 多模态路径；
- 多 engine 内部负载均衡和 scheduler-stat-aware routing；
- health、load、version、metrics、reset-cache、sleep/wake 等运维路由；
- mock engine 与 HTTP integration-test 基础设施。
- external/hybrid DP load balancing 与 tokenization APIs；
- TLS、API key、CORS 和 `/server_info`；
- LoRA 启动加载、动态加载和多 adapter 路由；
- pause/resume、abort、world size 与部分新增 parser/request 能力。

这些是 roadmap 作者对当前状态的描述，不等于已经在本书目标 release 和目标模型上验证。

## 缺口分类

| 类别     | Roadmap 中的代表性缺口                                          | 对书稿的意义                            |
| ------ | -------------------------------------------------------- | --------------------------------- |
| 分布式服务  | elastic EP、扩缩容期间 draining 与 rejection behavior        | 不能仅凭常规请求成功外推动态集群控制面能力              |
| API 覆盖 | Messages、Responses、embedding/pooling、speech、realtime     | “OpenAI-compatible”必须细化到 endpoint |
| 请求兼容   | `n > 1`、beam search、prompt truncation、tracing            | 需要参数级契约测试，不能只做 smoke test         |
| 生产就绪   | reverse-proxy root path、日志参数、tracing                    | 已勾选安全能力仍需在目标 release 验证            |
| LoRA   | 已勾选启动、动态加载和多 adapter 路由                                | roadmap 完成不等于目标 release/模型组合已验证      |
| 多模态    | image embedding、audio、video、更广模型覆盖                       | 不能用 text-only 结果代表多模态能力           |
| 生命周期   | weight update、weight transfer engine                      | 运维和在线训练/更新场景仍存在差距                 |
| Parser | tool/reasoning parser 家族覆盖                               | 需要按目标模型建立 roundtrip fixture       |
| 测试设施   | 真正的 `vllm serve` Rust CI 路径                              | feature 存在与端到端可用需要分开判断            |

## 一个正在发生的例子

Roadmap 中的 `truncate_prompt_tokens` 已关联到 PR #48584。2026-07-25 核对时该 PR 仍为 Open，说明 roadmap 条目可以已经有实现工作，但在合并和进入 release 前仍不能写成“已支持”。

## 本书采用的最小生产就绪门槛

在 Rust Frontend 被写成生产建议前，至少需要：

- [ ] 目标 endpoint 和参数的契约测试通过；
- [ ] TLS/鉴权或明确由上游网关承担，并验证信任边界；
- [ ] request ID、日志、metrics 和 tracing 满足观测需求；
- [ ] 超时、取消、断连、过长输入与非法参数行为明确；
- [ ] frontend-bound 与 GPU-bound 两类性能实验完成；
- [ ] canary、快速回退到 Python Frontend 的路径演练通过；
- [ ] 所有结论固定到 release tag 与 commit。

## 追踪方式

每周通过 [`tracking/`](tracking/) 复查 Issue #44280，并结合 vLLM Version Monitor 发现新 release。只把“已合并并进入目标 release、且本书验证通过”的能力升级为正文事实。其他条目保留为 roadmap 或实验假设。
