# 项目 Subagents

## `topic_booklet`

把一个已有的 `research/topics/<topic>/` 系统综合成主题研究小册子套件，或在上游变化后刷新已有小册子。

这个 Subagent 是薄执行层：流程、证据门禁和输出契约的唯一事实来源是
[`$topic-booklet` Skill](../../.agents/skills/topic-booklet/SKILL.md)。

典型调用：

```text
使用 topic_booklet subagent，为 research/topics/rust-frontend
生成或刷新主题研究小册子，执行 $topic-booklet Skill，
完成校验，但不要 commit。
```

指定研讨目标：

```text
使用 topic_booklet subagent 处理 research/topics/rust-frontend。
目标读者是 serving、SRE 和安全团队，准备一次 90 分钟生产采用研讨；
重点回答 capability parity、可观测性和 fallback。
```

上游变化后的刷新：

```text
使用 topic_booklet subagent，根据 tracking/change-log.md 的最新记录
刷新 rust-frontend 小册子，执行 $topic-booklet Skill；无法同步更新
的 PPT 或图标记 needs-refresh。
```

Agent 配置位于 [`topic-booklet.toml`](topic-booklet.toml)。Codex 以其中的
`name = "topic_booklet"` 作为调用名称。
