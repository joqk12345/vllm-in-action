# 专题研究

用于容纳尚未达到正文证据标准的主题，例如新调度器、硬件后端、推测解码方法或多模态支持。每个主题先写问题、版本边界、来源和验证计划，成熟后再分流到来源卡片、实验和章节。

## 主题阅读方法

专题研究不按“逐篇资料摘要”组织最终结论，而按共同问题组织：

```text
定义问题
  → 建立最小术语
  → 收集不同来源的命题
  → 对齐适用边界
  → 找出分歧与反例
  → 形成综合判断
  → 转成测试、实验和生产决策
```

单篇摘要仍可保存在 topic 根目录；只有完成跨来源综合的内容才进入主题研究小册子。

## 建议的专题结构

```text
research/topics/<topic>/
├── README.md
├── claims.yml
├── vocabulary.md
├── source/
├── tracking/                 # 活跃主题需要
└── outputs/
    ├── brief/
    ├── booklet/
    │   ├── <topic>-topic-booklet.md
    │   ├── seminar-guide.md
    │   ├── reading-list.md
    │   └── capability-matrix.yml
    ├── chapter-handoff/
    ├── figures/
    └── slides/
```

复制 [`../../templates/topic-booklet.md`](../../templates/topic-booklet.md) 初始化小册子。

在当前 Agent 中直接运行可复用流程：

```text
使用 $topic-booklet，为 research/topics/<topic>
生成或刷新主题研究小册子，完成校验但不要 commit。
```

素材较多、需要隔离上下文时调用项目 Subagent：

```text
使用 topic_booklet subagent，为 research/topics/<topic>
执行 $topic-booklet，完成校验但不要 commit。
```

Skill 位于 [`.agents/skills/topic-booklet/`](../../.agents/skills/topic-booklet/)；
Subagent 定义和更多调用示例见 [`.codex/agents/README.md`](../../.codex/agents/README.md)。

## 小册子进入研讨的最低条件

- [ ] 至少有两个不同来源围绕同一个研究问题；
- [ ] 核心 claim 有 Source ID、证据等级和适用边界；
- [ ] 已建立统一 nouns/verbs，避免来源术语混乱；
- [ ] 至少记录一个反例或无效泛化；
- [ ] 动态事实与稳定主体分离；
- [ ] 未决问题已经转成测试、实验或上游核对任务；
- [ ] 有研讨目标、参与角色、决策模板和 owner 机制。

小册子是研究中间产物，不是正式正文。只有 A/B 级证据、版本边界和必要验证完成后，内容才通过 chapter handoff 进入 `book/chapters/`。
