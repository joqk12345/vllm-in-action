# 投机解码专题

Owner: 未指定
Purpose: 系统研究投机解码的算法、vLLM 集成、性能边界与生产采用方法，并以 DSpark 作为首个重点案例
Status: needs-refresh
Applies to: DSpark、Speculators 与 vLLM speculative decoding；目标核对版本 v0.27.1
Evidence grade: B/C/D 混合
Verified date: 2026-08-15
Assumptions: 尚未在本仓库复现 DSpark 训练、接受长度或端到端 serving benchmark
Open questions: v0.27.1/Speculators 中各 proposer 的 release 边界，以及不同 workload、并发、采样参数和硬件下接受长度能否转化为 ITL、吞吐或 goodput 收益
Handoff: 第 10、11 章为主；训练与分布式隐藏状态链路作为第 8、12 章背景材料

## 研究边界

本专题研究的是 **speculative decoding**，而不是只描述 DSpark：

```text
目标模型分布
  → drafter 提议候选 token
  → target 并行验证
  → 接受最长前缀
  → 用延迟、吞吐和 goodput 判断是否值得启用
```

DSpark 是第一个案例，用于研究两个更耐久的问题：

1. 如何在 drafter 延迟与接受长度之间取舍；
2. 如何根据请求置信度、引擎负载和硬件容量动态分配验证预算。

EAGLE、MTP、DFlash、P-EAGLE 等方法只在回答共同问题时纳入，不按论文逐篇堆叠摘要。

## 当前来源

- [`source/papers/2026-07-06-dspark-paper-v1.pdf`](source/papers/2026-07-06-dspark-paper-v1.pdf) — DSpark arXiv v1，算法和作者实验的主要一手来源。
- [`source/talks/2026-07-22-dspark-speculative-decoding-talk.pptx`](source/talks/2026-07-22-dspark-speculative-decoding-talk.pptx) — 公开分享，覆盖 Speculators、vLLM、Mooncake 和 DSpark 工程链路。
- [`source/transcripts/2026-07-22-dspark-speculative-decoding-talk.zh.srt`](source/transcripts/2026-07-22-dspark-speculative-decoding-talk.zh.srt) — 未清洗 ASR 字幕，仅作为 D 级线索。
- [`source/README.md`](source/README.md) — 来源身份、证据等级、权利状态和校验值。
- [`claims.yml`](claims.yml) — 本专题的 claim spine。
- [`vocabulary.md`](vocabulary.md) — 最小 nouns、verbs 与分析语法。
- [`tracking/README.md`](tracking/README.md) — 论文、Speculators 和 vLLM 的持续跟踪规则。
- [`tracking/2026-07-22-dspark-talk-qa.yml`](tracking/2026-07-22-dspark-talk-qa.yml) — 2026-07-22 分享 QA 的持续追踪表。
- [`outputs/booklet/`](outputs/booklet/) — 投机解码主题研究小册子 bundle。

## 三层内容

### 可沉淀的稳定主体

- 正确的拒绝采样如何保持 target distribution；
- `draft → verify → accept/reject → correct` 的解码循环；
- drafter 时间、target 验证时间和接受长度之间的关系；
- 单请求延迟与高并发吞吐可能要求不同的 proposal/verification 策略；
- benchmark 必须同时记录模型、采样、并发、硬件、batch 和端到端指标。

### 方法与实现相关的动态事实

- DSpark 的半自回归结构、confidence head 和 hardware-aware prefix scheduler；
- Speculators 支持的算法、checkpoint 格式和训练命令；
- vLLM 对 speculator config、Model Runner 和验证路径的支持；
- 隐状态在线提取、KVConnector/Mooncake 数据通路。

这些内容引用前必须固定论文版本、仓库 commit 或 vLLM release。

### 尚不能进入正文的结论

- “DSpark 是当下最强投机解码”；
- 论文接受长度能直接外推成本仓库目标 workload 的加速比；
- DeepSeek-V4 线上结果能直接外推 Qwen、Llama 或其他 serving 栈；
- 演讲中的 Mooncake/vLLM 命令在任意版本都可直接运行。

## 进入正文前的门禁

- [ ] 固定目标 vLLM 与 Speculators tag/commit。
- [ ] 将 PPT/SRT 中的工程 claim 回查到源码、测试或官方文档。
- [ ] 复现至少一个低并发 latency 场景和一个高并发 throughput/goodput 场景。
- [ ] 同时记录 `T_draft`、`T_verify`、接受长度、ITL、吞吐、GPU 利用率和显存。
- [ ] 覆盖代码、数学、开放式对话以及一个低接受率反例。
- [ ] 验证禁用投机解码的回退路径和配置兼容性。
- [x] 已生成第一版 `$topic-booklet` bundle；当前状态仍为 `captured`，需要先补 release/commit 与本仓实验后才能进入正文。
