# 来源台账

每个来源一个 Markdown 卡片，放在 `cards/`，文件名与 `source_id` 一致，例如：

```text
cards/SRC-vllm-docs-serving.md
```

正文只引用 Source ID。一个来源可以支撑多个结论，但卡片必须明确“支撑什么”和“不支撑什么”。网页易变时记录验证日期和版本；可合法保存的快照放到忽略提交的 `raw/`，卡片内写相对路径。

来源状态：

```text
captured → verified → cited → stale
```

创建新卡片时复制 `templates/source-card.md`，不要直接在 `references.md` 堆链接。
