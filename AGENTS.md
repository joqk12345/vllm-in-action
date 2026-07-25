# 《vLLM 工程实践》项目约定

> 本文件是项目规则的唯一事实来源。`CLAUDE.md` 与 `GEMINI.md` 只引用本文件。

项目目标：持续追踪 vLLM 的版本、设计与生产实践，写成一本证据充分、可复现、能随软件演进而维护的中文技术书——《vLLM 工程实践：从推理原理到生产级服务》。

## 项目引用

| 项目 | 地址 | 在本知识库中的职责 |
|---|---|---|
| vLLM | <https://github.com/vllm-project/vllm> | 上游技术事实源。源码、测试、文档、release、Issue 和 PR 用于验证功能、默认值、行为与版本边界。 |
| vLLM Version Monitor | <https://github.com/joqk12345/vllm-version-monitor> | 版本变化发现与初步分诊入口。用于发现 release、PR 和潜在章节影响，但不能替代上游证据。 |

使用规则：

- 涉及 vLLM 行为、兼容性或发布状态时，最终结论必须回到 `vllm-project/vllm` 的 release tag、commit、源码、测试或官方讨论验证。
- `vllm-version-monitor` 的输出属于变化线索；写入本仓库时要附带对应的上游 URL、目标版本或 commit，以及捕获日期。
- 两个项目的信息不一致时，以固定版本的 vLLM 上游材料和本仓库复现实验为准，并记录差异。
- 不在正文中引用浮动 `main` 作为永久事实；研究阶段可以跟踪 `main`，进入正文前必须固定 tag 或 commit。

## 五条总原则

1. **先验证，再总结。** 任何性能、兼容性或行为结论都必须能追溯到文档、代码、Issue/PR 或本仓库实验。
2. **版本必须明确。** 涉及 API、默认值、特性状态的文字必须标记 vLLM 版本或验证日期。
3. **基线必须公平。** 性能比较要记录模型、硬件、精度、并行配置、请求分布和测量方法。
4. **区分事实与建议。** 上游事实、实验观察、工程判断和待验证假设不得混写。
5. **正文只保留耐久知识。** 易变信息先进入研究卡片和版本记录，验证稳定后再进入正文。

## 核心读者与承诺

- 读者：需要把开源大模型稳定部署到生产环境的推理工程师、平台工程师和技术负责人。
- 前置知识：熟悉 Python、Linux、容器、GPU 基础和 Transformer 推理概念。
- 读完后：能建立性能基线，选择正确的 vLLM 配置，诊断吞吐/延迟/显存问题，并安全地升级生产服务。

## 证据等级

- **A — 一手且可复现：** vLLM 源码/测试、官方文档、release note、原始 PR，以及本仓库可复现实验。
- **B — 一手但未本地复现：** 官方设计文档、维护者讨论、硬件或框架官方文档。
- **C — 可信二手：** 高质量技术文章、公开演讲、独立 benchmark，且方法披露充分。
- **D — 线索：** 社区帖子、聊天记录、无完整配置的数字。只能用于发现问题，不能支撑正文结论。

## 每个技术结论都要回答

1. 结论适用于哪个 vLLM 版本？
2. 适用于哪些模型、硬件、精度和部署拓扑？
3. 优化的目标是 TTFT、ITL、吞吐、成本还是稳定性？
4. 代价和失效边界是什么？
5. 证据在哪里，别人如何复现？
6. 哪个上游变化可能让它失效？

## 写作与术语规则

- 首次出现时写中文名称并保留英文/缩写，例如“首 token 延迟（TTFT）”。
- 命令和配置必须来自已验证环境；示例不得假装是通用最优配置。
- 不写“显著提升”“大幅降低”等无基线判断；必须给出测量条件。
- 不把实验性功能写成生产默认建议。
- 对版本敏感段落使用 `<!-- verified: vX.Y.Z, YYYY-MM-DD -->`。
- 正文中的来源用稳定的 Source ID 引用，例如 `[SRC-vllm-docs-serving]`。

## 默认交付格式

重要研究、实验和评审文档应包含：

```text
Owner:
Purpose:
Status:
Applies to:
Evidence grade:
Verified date:
Assumptions:
Open questions:
Handoff:
```

## 目录职责

- `book/toc.yml` — 认知路线与章节规划。
- `book/spine.yml` — 最终成书顺序；构建工具未来应只读取它。
- `book/chapter-briefs/` — 章节契约、问题清单与证据缺口。
- `book/chapters/` — 正文唯一来源。
- `book/evidence/source-ledger/` — 来源卡片和 claim 映射。
- `book/evidence/benchmarks/` — 可复现 benchmark 记录。
- `book/evidence/experiments/` — 单项实验记录。
- `research/releases/` — vLLM 版本变化及其对全书的影响。
- `research/topics/` — 尚未成熟到进入正文的专题研究。
- `research/decision-log/` — 关键选型和写作决策。
- `process/review-memos/` — 技术审校、事实核查和红队意见。
- `templates/` — 新增资料时必须复用的模板。

## 工作流

1. **捕获变化：** 将 release、PR、文档变化录入 `research/releases/` 或来源卡片。
2. **判定影响：** 标出受影响章节、结论和实验。
3. **最小复现：** 在固定环境执行实验，保留命令、配置和原始结果路径。
4. **形成建议：** 明确适用条件、收益、代价、反例与回退方案。
5. **进入正文：** 只有 A/B 级证据可直接支撑正文；C 级需交叉验证。
6. **双重审阅：** 事实核查与读者可用性审阅都通过后，章节才能标记 `ready`。

## 专题小册子 Skill 与 Subagent

- `.agents/skills/topic-booklet/SKILL.md` 是专题小册子流程、证据门禁和输出契约的唯一事实来源。
- 普通调用：“使用 `$topic-booklet`，为 `research/topics/<topic>` 生成或刷新主题研究小册子，完成校验但不要 commit。”
- 素材较多或需要隔离上下文时，使用项目级 `topic_booklet` Subagent 执行 `$topic-booklet` Skill。
- Skill 必须以 `claims.yml` 为 claim spine，把动态 roadmap 状态与 release/local-test 状态分开，并遵守本文件证据等级。
- Subagent 配置和调用示例位于 `.codex/agents/`；通用内容模板位于 `templates/topic-booklet.md`。

## 状态词

- 来源：`captured → verified → cited → stale`
- 章节：`brief → researching → draft → review → ready`
- 版本影响：`untriaged → relevant → tested → integrated → no-impact`

## 校验

从仓库根目录运行：

```bash
python3 scripts/validate_kb.py
```

新增规则或长期记忆只修改 `AGENTS.md`，不要在其他 AI 配置中复制。
