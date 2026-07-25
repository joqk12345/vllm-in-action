# 项目版本说明

## 当前工作版本

```text
Knowledge-base version: 0.2.0-dev
Release status: Unreleased
Git tag: not created
Updated: 2026-07-25
```

`0.2.0-dev` 描述的是 `vllm-in-action` 知识库和研究工作流，不是 vLLM 软件版本。

## 三种版本必须分开

| 版本层 | 示例 | 负责回答 |
|---|---|---|
| 知识库版本 | `0.2.0-dev` | 仓库具备哪些研究、写作和校验能力？ |
| vLLM 上游版本 | `v0.25.1` | 某项功能首次出现或当前 release 是什么？ |
| 结论/实验版本 | `vLLM 0.19.0 + Qwen3-0.6B + 4×GB200` | 某个技术结论或 benchmark 在什么条件下成立？ |

不能因为知识库升级到 `0.2.0`，就把 Rust Frontend 的结论自动升级到最新 vLLM release。

## 0.2.0 的范围

本版本聚焦“可持续专题研究”：

- 建立主题阅读小册子标准；
- 提供 `$topic-booklet` Skill 和 `topic_booklet` Subagent；
- 建立 capability matrix；
- 接入 Issue #44280 与 vLLM Version Monitor 的双信号跟踪；
- 增加上游漂移检查和专题小册子校验；
- 用 Rust Frontend 完成第一套端到端样例。

详细变更见 [`CHANGELOG.md`](CHANGELOG.md) 的 `Unreleased` 部分。

## Rust Frontend 适用版本说明

截至 2026-07-25：

| 内容 | 当前边界 |
|---|---|
| RFC benchmark | vLLM 0.19.0、Qwen3-0.6B、DP=4、4×GB200、并发 1024、`request_rate=inf` |
| 架构研究 | 官方 RFC、主仓 `rust/` README 与 Issue #44280，核对至 2026-07-25 |
| 上游 release 发现信号 | v0.25.1 |
| 正文 target release | 尚未选择 |
| 本仓 capability test | 尚未执行 |
| 本仓 benchmark 复现 | 尚未执行 |

因此，本版本可以支持专题研讨、证据审计和正文规划，但不能把 Rust Frontend 写成无条件生产建议。

## 发布 0.2.0 前的完成条件

- [x] Topic-booklet Skill、Subagent 和标准输出就绪。
- [x] Rust Frontend 上游漂移检测就绪。
- [x] Topic-booklet 与知识库校验通过。
- [ ] 刷新嵌入旧 feature-parity 图的 PPTX。
- [x] 复核 CHANGELOG 和 README。
- [ ] 创建 `v0.2.0` Git tag。

创建 tag、GitHub Release 或 push 不属于文档更新动作，必须由用户明确要求。

## 版本号策略

在 `1.0.0` 之前采用以下含义：

- `0.x.0`：研究架构、正文结构或交付流程发生明显扩展；
- `0.x.y`：兼容的来源、模板、校验和内容修正；
- `-dev`：尚未形成 Git tag 的工作版本。

知识库内容随上游持续变化。即使项目版本不变，动态 Source Card、tracking snapshot 和 capability matrix 仍可能更新，但必须保留核对日期和版本边界。
