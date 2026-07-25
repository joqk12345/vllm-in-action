---
title: "Rust Frontend 章节转写包"
status: captured
created: 2026-07-25
verified: 2026-07-25
applies_to: "书稿第 3、6、9、14、15 章；官方状态核对至 2026-07-25"
source_ids:
  - SRC-vllm-rust-frontend-rfc-40846
  - SRC-vllm-rust-frontend-readme
  - SRC-vllm-rust-frontend-roadmap-44280
---

# Rust Frontend 章节转写包

Owner: book editorial
Purpose: 把专题结论按章节问题重排，提供可写入素材、图表和验证缺口
Status: captured
Applies to: 第 3、6、9、14、15 章
Evidence grade: A/B
Verified date: 2026-07-25
Assumptions: 这是 handoff，不是已合并正文
Open questions: 目标 release tag 与本地复现实验
Handoff: 对应 chapter brief 的“evidence needed”与未来正文草稿

## 第 3 章：Inside vLLM

### 章节问题

一次 OpenAI-compatible 请求如何跨越 serving frontend 与 engine 边界？

### 可写入命题

- Rust Frontend 只替换北向 frontend，既有 Python engine/core 与 GPU 执行路径保持在边界之后。[RF-C01]
- Server → Chat → Text → LLM → Engine Core Client 的层次依次把协议收敛成结构化事件、文本增量和 token 流。[RF-C02]
- 这是一种渐进式重构案例：先找到稳定进程边界，再替换一侧实现。

### 建议图

- `../figures/rust-frontend-request-lifecycle.svg`
- `../figures/rust-workspace-layering.svg`

### 边栏

“为什么不是重写 EngineCore？”答案不是 Rust 不适合，而是 engine 重写会同时改变 scheduling、KV cache 和模型执行，验证面远大于 frontend boundary。

### 进入正文前

- [ ] 固定目标 release tag 的 crate 与依赖图。
- [ ] 核对 ZMQ/MessagePack 生命周期和取消语义。

## 第 6 章：Serving and API

### 章节问题

OpenAI compatibility 为什么不能只用一个成功响应证明？

### 可写入命题

- streaming 是主路径，non-streaming 收集同一流，从源头减少两套响应语义。[RF-C03]
- tool/reasoning parser 的关键性质是 chunk invariance，而不是对一份完整 JSON 的解析成功。[RF-C04]
- “可替代”必须拆成 endpoint、parameter/model、operations 三层 contract。[RF-C08]

### 测试清单

- 同一输出按每一个可能字符/token 边界切分，最终结构一致。
- tool marker 前缀不能提前作为普通文本泄露。
- streaming/non-streaming 的 text、tool calls、usage、finish reason 等价。
- 不支持参数明确失败，不静默忽略。

### 建议图

- `../figures/rust-frontend-feature-parity-matrix.svg`

### 进入正文前

- [ ] 从目标 release 自动枚举 endpoint 与参数。
- [ ] 为书中示例模型建立 roundtrip fixtures。

## 第 9 章：Benchmarking

### 章节问题

如何正确使用一个刻意构造的 frontend-bound benchmark？

### 可写入命题

- RFC 共同条件：vLLM 0.19.0、Qwen3-0.6B、DP=4、4×GB200、并发 1024、request rate 无限。[RF-C06]
- Decode 场景中，Rust 559.79 req/s，默认 Python 509.56 req/s；P50 TTFT 为 50.51 ms 对 165.95 ms。
- Preprocess-hot 场景中，Rust 837.00 req/s，默认 Python 162.23 req/s；Python asc=32 才接近 Rust 吞吐。
- 这些数字证明 frontend ceiling，不证明所有端到端 workload 的同等收益。

### 方法框

一个完整复现实验必须同时记录：

`model × hardware × precision × parallelism × prompt/output distribution × concurrency × cache state × frontend process count`

### 反例

当大模型已让 GPU 饱和、并发较低时，frontend 优化可能几乎不改变端到端吞吐；因此必须加入 GPU-bound 对照组。

### 进入正文前

- [ ] 复现 RFC 的一组 frontend-bound 实验。
- [ ] 增加大模型 GPU-bound 对照。
- [ ] 补采 CPU、RSS、进程数、错误率和尾延迟。

## 第 14 章：Reliability and Security

### 章节问题

为什么更安全的语言不等于 production-ready 服务？

### 可写入命题

- Rust 的类型与所有权可以减少一类运行时错误，但不能补齐 API key、TLS、CORS、root path、tracing 和日志契约。
- 2026-07-25 roadmap 仍把多项 production-readiness 能力列为缺口。[RF-C07]
- parser 正确性需要 property/fixture 测试；编译通过不是增量语义证明。

### 风险登记

| 风险 | 检测 | 缓解 |
|---|---|---|
| 不支持参数被静默忽略 | 参数差异测试 | 明确 fail closed |
| tool marker 跨 chunk 误判 | 任意边界 fixture | safe-text buffer |
| TLS/鉴权缺口 | 信任边界审查 | 上游 gateway + 网络隔离 |
| 取消未传播 | 断连/超时演练 | lifecycle instrumentation |
| 观测语义不同 | 双路径 trace 对比 | request ID 贯通 |

### 进入正文前

- [ ] 选择由 frontend 还是 gateway 承担 TLS/auth。
- [ ] 验证 shutdown、draining、cancel 和 overload。

## 第 15 章：Upgrades and Troubleshooting

### 章节问题

怎样把 experimental frontend 引入升级流程，而不把回滚变成临场操作？

### 可写入命题

- `VLLM_USE_RUST_FRONTEND=1` 提供了渐进选择面，但环境变量本身不是完整回退方案。[RF-C05]
- rollout 单位应是 model + endpoint + parameter profile，而不是整个集群。
- canary 扩流必须绑定契约错误、P99 TTFT、parser mismatch、CPU/RSS 和取消泄漏等触发器。

### Runbook 骨架

1. 固定 release、镜像 digest 和配置。
2. 离线跑 capability contract。
3. 影子比较响应语义。
4. 1% canary，只开放 allowlist。
5. 逐级扩流，并持续与 Python baseline 比较。
6. 触发阈值时停止接收新请求、drain、切回 Python。
7. 保留失败输入和 trace，进入回归 fixture。

### 进入正文前

- [ ] 在目标编排环境演练一次有状态 drain 与回退。
- [ ] 核对 Python/Rust metrics 名称和告警兼容。

## 编辑禁区

- 不引用 ASR 逐字原话。
- 不使用转写中的 mock engine 数字。
- 不写“Rust 天然无 bug”或“性能必然显著提升”。
- 不把 roadmap 条目写成已发布能力。
- 不把 gateway/control-plane 复用写成当前承诺。
