# vLLM in Action / vLLM 工程实践

> **《vLLM 工程实践：从推理原理到生产级服务》**
> *vLLM in Action: From Inference Mechanics to Production Serving*

这是一个面向长期维护的开源书籍知识库：持续追踪 vLLM 的架构、版本变化与生产实践，并把可验证的经验沉淀为一本中文技术书。

它参考了 `../no-one-did-it` 的“正文—证据—流程—出版”分层，但当前保持轻量：先把研究、实验和章节契约做扎实，等正文成熟后再加入 EPUB/PDF 构建。

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
- 新增来源：复制 [`templates/source-card.md`](templates/source-card.md)
- 跑实验：复制 [`templates/experiment.md`](templates/experiment.md)
- 跟进新版本：复制 [`templates/release-impact.md`](templates/release-impact.md)
- 写章节：先完成对应的 `book/chapter-briefs/`，再在 `book/chapters/` 起草

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
```

## 校验

```bash
python3 scripts/validate_kb.py
```

校验器会检查必要目录、书脊与章节 brief 的对应关系、front matter 和 Source ID 的基本格式。

## 当前边界

- 仓库中的配置不是默认生产建议；只有在适用条件和证据齐全时才进入正文。
- 暂不绑定具体出版工具链，避免知识结构被某个渲染器反向约束。
- 许可证尚未选择；公开发布或接受外部贡献前应补充 `LICENSE` 与贡献约定。
