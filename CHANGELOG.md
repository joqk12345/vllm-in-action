# Changelog

本文件记录 `vllm-in-action` 知识库、研究流程和交付能力的变化。

它不记录完整的 vLLM 上游 release 内容。上游版本影响位于 `research/releases/`，具体技术结论的版本边界位于 Source Card、claim 和实验记录中。

## [Unreleased]

### Planned for 0.2.0

#### Added

- Rust Frontend 主题研究小册子，包括：
  - 问题驱动的主题综合；
  - 专项研讨指南；
  - 分轮主题阅读清单；
  - endpoint、parameter/model、operations 三级 capability matrix。
- 仓库级 `$topic-booklet` Skill：
  - 证据与动态刷新规则；
  - 小册子输出契约；
  - 确定性小册子校验脚本；
  - Codex UI metadata。
- 项目级 `topic_booklet` Subagent，作为 `$topic-booklet` 的隔离执行层。
- Rust Frontend 持续跟踪：
  - Issue #44280 正文 SHA、状态、评论和 checklist 基线；
  - vLLM 官方最新 release 信号；
  - vLLM Version Monitor manifest 和工作流健康信号；
  - 每周 GitHub Actions 漂移检查；
  - 人工分诊协议和追加式变化日志。
- 投机解码专题研究骨架，以 DSpark 为首个重点案例，包括：
  - 版本化论文、演讲和字幕素材清单及文件校验值；
  - SD-C01～SD-C08 claim spine 与最小术语表；
  - 论文、Speculators 和 vLLM 的持续跟踪协议；
  - 2026-07-22 DSpark 分享 QA 结构化整理、可维护 tracker 与 QA tracking best practices；
  - 投机解码主题小册子 bundle：主题综合、研讨指南、阅读路径和 capability matrix；
  - DSpark 论文、演讲、字幕、Speculators 和 vLLM spec decode 的来源卡；
  - 第 9、10、11、12、15 章的正文落点建议。
- llm-d agentic serving 专题研究骨架，包括：
  - vLLM Office Hours #53 PDF 与自动字幕的规范化 source 目录；
  - LD-C01～LD-C07 claim spine 与最小术语表；
  - Office Hours #53 结构化分析、QA tracker 与 benchmark 线索；
  - llm-d、vLLM、InferenceX/AgentX、Gateway API 和 deployment operator 的持续跟踪规则；
  - llm-d agentic serving 主题小册子 bundle：主题综合、研讨指南、阅读路径和 capability matrix；
  - Office Hours、llm-d repository 和 InferenceX/AgentX 的来源卡。
- 高效长上下文注意力专题研究骨架，从原 `linear-attention` 线索扩展为 `efficient-long-context-attention`，包括：
  - GLM-5 v2 PDF 与 NSA/MoBA/Lightning Attention seed list 的规范化 source 目录；
  - EA-C01～EA-C07 claim spine 与最小术语表；
  - DSA、sparse/linear/window/block/hybrid attention、vLLM 支持状态和长上下文 benchmark 的持续跟踪规则；
  - GLM-5 v2 与 seed list 的来源卡。
- 通用主题小册子模板与专题研究准入条件。

#### Changed

- 将 Rust Frontend 演讲材料从 B 级调整为 C 级证据，与项目证据规则一致。
- 为 RF-C01～RF-C09 补充反例或无效泛化，以及 `verification_gap`。
- 将 feature-parity 图调整为稳定的三层 capability contract，不再嵌入易过期的 roadmap checkbox 判断。
- 根据 Issue #44280 当前快照修正 TLS、API key、CORS、LoRA、DP 和生命周期能力的动态表述。
- 明确 Version Monitor 只负责发现和初步分诊，最终事实必须回到 vLLM 官方上游验证。
- 扩展高级解码 watchlist，加入 DSpark、drafter/checkpoint 兼容性，以及接受长度与 latency、throughput、goodput 的指标边界。

#### Validation

- Topic-booklet validator：Rust Frontend 与投机解码专题均通过。
- Knowledge-base validator：通过。
- Skill frontmatter、metadata、YAML 和 Subagent TOML：通过。
- 两轮独立 Subagent forward test 已执行；发现的问题均已回写 Skill、校验器和 Rust Frontend 小册子。

#### Known gaps

- 尚未为正式正文选择 Rust Frontend target release/commit。
- RFC benchmark 尚未在本仓库复现，缺少 GPU-bound 对照和完整 CPU/RSS 数据。
- Slidev/PPTX 仍包含早期 feature-parity 图，已标记 `needs-refresh`。
- 第三方演讲 PDF 的开放许可尚未确认。
- 投机解码专题尚未固定兼容的 vLLM/Speculators 版本组合，也未在本仓库独立复现 DSpark 端到端 serving benchmark。
- DSpark 演讲 PPT 与字幕的再分发授权状态尚未核对。
- `book/chapters/` 尚未开始正式章节草稿。

## [0.1.0] - 2026-07-25

初始知识库基线，对应初始化阶段；当前尚未创建 `v0.1.0` Git tag。

### Added

- 16 章书籍结构、chapter briefs、spine 和状态页。
- 来源台账、实验、benchmark、review memo 与 release-impact 模板。
- 首批 vLLM 官方来源卡和 v0.23.0 上游 release impact。
- Rust Frontend 原始材料、研究笔记、claim spine、Brief、章节 handoff、共享图和 Slidev/PPTX。
- 基础知识库校验脚本。
