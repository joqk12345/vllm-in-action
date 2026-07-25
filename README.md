# vLLM in Action / vLLM 工程实践

> **《vLLM 工程实践：从推理原理到生产级服务》**
> *vLLM in Action: From Inference Mechanics to Production Serving*

这是一个面向长期维护的开源书籍知识库：持续追踪 vLLM 的架构、版本变化与生产实践，并把可验证的经验沉淀为一本中文技术书。

它参考了 `../no-one-did-it` 的“正文—证据—流程—出版”分层，但当前保持轻量：先把研究、实验和章节契约做扎实，等正文成熟后再加入 EPUB/PDF 构建。

## 当前版本

- 知识库开发版本：[`0.2.0-dev`](VERSION.md)
- 变更记录：[`CHANGELOG.md`](CHANGELOG.md)
- 当前书稿阶段：知识库骨架完成，进入证据采集、专题研究和章节调研

知识库版本、vLLM 上游版本和单项实验版本是三个不同概念。知识库版本描述本仓库的结构与研究能力；技术结论仍必须在 Source Card、claim 或实验记录中单独声明适用的 vLLM tag/commit。

## 这本书解决什么问题

vLLM 的参数很多，但生产问题通常不是“某个 flag 怎么写”，而是目标和约束没有对齐：

- 为什么吞吐上去了，首 token 延迟却恶化？
- 什么时候该用张量并行、流水线并行或数据并行？
- KV cache、批处理、量化和推测解码之间如何互相影响？
- benchmark 为什么无法复现，怎样建立公平基线？
- 如何做容量规划、可观测性、故障降级和安全升级？

本书将围绕一个统一决策框架组织答案：

> 工作负载 → SLO → 模型与硬件约束 → 引擎机制 → 配置 → 测量 → 生产反馈

## 从哪里开始

- 看全书结构：[`book/toc.yml`](book/toc.yml)
- 看当前进度：[`book/STATUS.md`](book/STATUS.md)
- 看待追踪主题：[`research/watchlist.yml`](research/watchlist.yml)
- 看 Rust Frontend 专题：[`research/topics/rust-frontend/`](research/topics/rust-frontend/)
- 读 Rust Frontend 小册子：[`research/topics/rust-frontend/outputs/booklet/rust-frontend-topic-booklet.md`](research/topics/rust-frontend/outputs/booklet/rust-frontend-topic-booklet.md)
- 看投机解码专题：[`research/topics/speculative-decoding/`](research/topics/speculative-decoding/)
- 审阅投机解码正文落点建议：[`research/topics/speculative-decoding/outputs/chapter-handoff/chapter-placement-proposal.md`](research/topics/speculative-decoding/outputs/chapter-handoff/chapter-placement-proposal.md)
- 新增来源：复制 [`templates/source-card.md`](templates/source-card.md)
- 跑实验：复制 [`templates/experiment.md`](templates/experiment.md)
- 跟进新版本：复制 [`templates/release-impact.md`](templates/release-impact.md)
- 生成专题小册子：使用 `$topic-booklet`
- 写章节：先完成对应的 `book/chapter-briefs/`，再在 `book/chapters/` 起草

## 主题研究小册子

专题研究小册子位于 Research Brief 与正式书稿之间，用共同问题组织多个来源，并把结论转成研讨、能力测试、实验和章节交接。

直接在当前 Agent 中执行：

```text
使用 $topic-booklet，为 research/topics/<topic>
生成或刷新主题研究小册子，完成校验但不要 commit。
```

素材较多、需要隔离上下文时：

```text
使用 topic_booklet subagent，为 research/topics/<topic>
执行 $topic-booklet，完成校验但不要 commit。
```

- Skill：[`.agents/skills/topic-booklet/SKILL.md`](.agents/skills/topic-booklet/SKILL.md)
- Subagent：[`.codex/agents/topic-booklet.toml`](.codex/agents/topic-booklet.toml)
- 通用模板：[`templates/topic-booklet.md`](templates/topic-booklet.md)
- 专题方法：[`research/topics/README.md`](research/topics/README.md)

## 持续跟踪 Rust Frontend

Rust Frontend 使用双信号跟踪：

- vLLM Issue #44280 发现 roadmap、checkbox 和评论变化；
- vLLM Version Monitor 发现新 release 和 release-note 线索；
- 最终结论回到 vLLM 官方 tag、commit、源码、测试和本仓库实验。

手动检查：

```bash
python3 scripts/check_rust_frontend_tracking.py
```

GitHub Actions 每周运行同一检查。检测到漂移只表示需要人工分诊，不代表能力已经发布、验证或可以进入正文。

## 投机解码专题

投机解码专题以 `draft → verify → accept/reject → measure` 为稳定分析框架，以 DSpark 为首个重点案例，研究 drafter 延迟、接受长度、验证预算和生产指标之间的取舍。

当前已建立：

- 版本化来源清单与文件校验值；
- SD-C01～SD-C08 claim spine；
- 论文、Speculators 和 vLLM 的持续跟踪协议；
- 第 9、10、11、12、15 章的正文落点建议。

专题仍处于 `captured` 状态。DSpark 论文结果属于作者报告，Speculators/vLLM 工程事实尚需固定到 tag 或 commit，并在本仓库复现低并发 latency 与高并发 throughput/goodput 场景后，才可进入正文。

## 建议的日常节奏

每周处理一次 watchlist 和上游变化；每月复查所有 `stale_after` 到期的来源；每个 vLLM 版本发布后创建一份 release impact；每个进入正文的性能结论至少对应一份实验记录。

## 仓库地图

```text
book/
  chapter-briefs/       章节契约与证据缺口
  chapters/             正文唯一来源
  evidence/             来源台账、benchmark、实验
  front-matter/         前言等
  back-matter/          术语、参考资料等
research/
  releases/             版本影响记录
  topics/               专题研究
  decision-log/         关键决策
process/
  review-memos/         技术审校与事实核查
  reader-reports/       读者测试
templates/              所有标准模板
scripts/                知识库校验工具
.agents/skills/         仓库级可复用工作流
.codex/agents/          项目级自定义 Subagent
.github/workflows/      定时上游漂移检查
```

## 校验

```bash
python3 scripts/validate_kb.py
python3 .agents/skills/topic-booklet/scripts/validate_topic_booklet.py \
  research/topics/rust-frontend
git diff --check
```

知识库校验器检查必要目录、书脊、章节 brief、front matter 和 Source ID 的基本格式；小册子校验器检查五类标准输出、claims、来源卡、capability matrix 和 deliverables 登记。

## 当前边界

- 仓库中的配置不是默认生产建议；只有在适用条件和证据齐全时才进入正文。
- 暂不绑定具体出版工具链，避免知识结构被某个渲染器反向约束。
- Rust Frontend 的 target release 尚未固定，本仓 benchmark 尚未复现。
- 投机解码专题尚未固定兼容的 vLLM/Speculators 版本组合，也未独立复现 DSpark 端到端收益。
- roadmap checkbox 和 Version Monitor 输出都是变化线索，不能替代 release/local-test 证据。
- DSpark 演讲 PPT 与字幕的再分发授权状态尚未核对。
- 许可证尚未选择；公开发布或接受外部贡献前应补充 `LICENSE` 与贡献约定。
