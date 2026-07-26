# llm-d 分布式推理与 Agentic Workloads

Owner: 未指定
Purpose: 系统研究 llm-d + vLLM 在 Kubernetes 上服务 agentic long-context workloads 的路由、KV cache、PD 分离、Wide EP、QoS 与成本边界。
Status: captured
Applies to: vLLM Office Hours #53（2026-07-09）公开分享；llm-d/vLLM 上游状态尚未固定到 release 或 commit
Evidence grade: C/D 起步；进入正文前必须回到 llm-d/vLLM 源码、PR、release、官方文档或本仓实验
Verified date: 2026-07-26
Assumptions: `LMD`/`LLMD`/`VLM` 等字幕写法多为 ASR 误识别，分别按 `llm-d` 和 `vLLM` 理解。
Open questions: 哪些 llm-d 能力已经发布、哪些需要特定 vLLM release、Wide EP/DP attention 在目标硬件和 AgentX-like workload 下是否可复现收益。
Handoff: 第 11、12、15 章；Kubernetes 部署与生产调度章节。

## 主题边界

本主题不只研究 Wide EP，而是研究 agentic workload 下的分布式 LLM serving 系统：

```text
agentic workload
  → long prompt / multi-turn reuse
  → prefix-aware routing
  → KV cache management and tiering
  → prefill/decode disaggregation
  → Wide expert parallelism / DP attention for MoE/MLA models
  → flow control / priority / batch / autoscaling
  → latency, throughput, goodput, cost and SLO
```

Wide expert parallelism（Wide EP）是关键机制之一，但不是唯一主题。llm-d 的 endpoint picker、prefix affinity、KV cache tiering、PD disaggregation 和 flow control 才构成完整生产问题。

## 当前来源

- [`source/talks/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.pdf`](source/talks/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.pdf) — vLLM Office Hours #53 幻灯片，C 级线索。
- [`source/transcripts/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.en.srt`](source/transcripts/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.en.srt) — YouTube 自动字幕，D 级线索。
- [`source/README.md`](source/README.md) — 来源等级、文件校验和权利边界。
- [`claims.yml`](claims.yml) — 本主题 claim spine。
- [`vocabulary.md`](vocabulary.md) — 最小 nouns/verbs 与术语清洗。
- [`tracking/README.md`](tracking/README.md) — 后续 release/PR/benchmark 跟踪规则。
- [`tracking/2026-07-09-office-hours-53-qa.yml`](tracking/2026-07-09-office-hours-53-qa.yml) — Office Hours #53 QA 与 benchmark 线索追踪。
- [`outputs/2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md`](outputs/2026-07-09-office-hours-53-llm-d-wide-ep-analysis.md) — PDF/自动字幕结构化分析与 QA 整理。
- [`outputs/booklet/`](outputs/booklet/) — 主题研究小册子 bundle。

## 共同研究问题

1. 为什么 agentic workloads 不能用普通 round-robin Kubernetes Service 负载均衡？
2. llm-d router / endpoint picker 如何结合 prefix cache affinity、load/backpressure 和 latency prediction？
3. KV cache 如何从单 pod 扩展到集群级 working set，并让 router 感知 GPU/CPU/storage tier？
4. Prefill/decode disaggregation 何时有用，KV transfer 和部署复杂度如何影响收益？
5. Wide EP / DP attention 为什么适合 GLM/DeepSeek 这类 MoE/MLA 大模型和 100K-token agentic traces？
6. 生产中如何用 flow control、priority、batch 和 autoscaling 同时服务在线与离线 workload？
7. Office Hours 中的 H200/GLM5.2/AgentX/OpenRouter 成本数字如何验证，哪些不能外推？

## 进入正文前的门禁

- [ ] 固定 llm-d 与 vLLM 目标 release/tag/commit。
- [ ] 将演讲中的功能 claim 回查到 llm-d/vLLM 源码、测试、PR 或官方文档。
- [ ] 建立 AgentX-like workload 或本仓可复现长上下文多轮 trace。
- [ ] 同时记录 prefix cache hit rate、TTFT、ITL、output TPS/user、TPS/GPU、GPU 利用率、KV cache 使用和成本假设。
- [ ] 验证 naive Service/round-robin、prefix-aware routing、PD、Wide EP、KV tiering 的分层贡献。
- [ ] 记录反例：低复用 workload、短 prompt、无高速网络、KV transfer 失败、版本滚动不一致。
- [ ] 明确 rollback：关闭 llm-d router、降级为普通 vLLM 服务、关闭 PD 或 Wide EP 的条件。
