# 第 14 章 可靠性、隔离与安全

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

模型服务处理不可信输入、执行复杂本地/第三方代码并消耗昂贵加速器。可靠性与安全都从“限制故障影响范围”开始。

## 14.1 故障域

区分 API、EngineCore、worker/rank、节点、存储、网络和 control plane。TP/EP 中一个 rank 失败通常使整个 replica 不可用；DP 副本可隔离。Kubernetes readiness 先摘流，liveness 只处理不可恢复 hang；盲目重启可能扩大 checkpoint 下载风暴。

为每层定义 timeout 和 retry owner。collective 超时后往往不能安全继续同一 process group，应 fail fast 并重建 replica。客户端只重试幂等、未产生可见输出的请求；streaming 中途重试可能重复 token。

## 14.2 Admission 与多租户

限制每租户并发、token rate、prompt/max output、`n`、logprobs、media、LoRA 和 grammar。按最坏资源而非 HTTP 请求数计费：一个 128K prompt 与一句聊天不等价。关键和批处理 workload 分队列/副本，防止 noisy neighbor。

prefix cache 复用必须把影响 KV 的身份（模型、adapter、输入特征等）纳入正确语义；跨租户共享还涉及侧信道和数据治理。高敏场景宁可禁用跨边界复用。

## 14.3 输入与供应链

远程媒体防 SSRF：allowlist scheme/host、阻断 loopback/link-local/private range、限制重定向、DNS rebinding、字节与像素、解码时间。chat template 与 schema 设复杂度边界。

固定并扫描容器 digest、Python/Rust/CUDA 依赖与模型 revision；审计 remote model code、plugins、custom logits processors 和 tokenizer。模型文件不是天然可信数据。服务进程最小权限、只读根文件系统、独立下载身份，secret 通过 secret store 注入。

## 14.4 数据保护

prompt/output 可能含个人或商业数据。默认不记录正文；调试采样需审批、脱敏、加密和 TTL。metrics label 禁止 tenant-generated text。崩溃 dump、profile、KV offload 与 connector 传输也属于数据面，应限制访问和清理。

OpenAI-compatible endpoint 的鉴权通常只是边界一层；生产还需 TLS、租户授权、审计、速率限制与网络策略。

## 14.5 降级矩阵

过载时按业务允许顺序执行：拒绝低优先级 → 缩短 max output → 禁用高成本 logprobs/`n` → 路由备用量化模型 → 保留关键流量。不要在事故中临时修改十个性能 flag；预演并自动化降级。

对 P/D disaggregation 或远端 KV，明确 connector load 失败是重算、重试还是失败。重算提高可用性但可能在存储故障时把 prefill 集群压垮，需要 circuit breaker。

## 14.6 混沌测试

演练慢客户端、API kill、worker kill、单 NIC 丢包、模型存储超时、connector miss、OOM、超长输入和流量突发。验证：请求是否有界失败、blocks 是否释放、其他租户是否保持 SLO、告警是否明确、恢复是否无重试风暴。

> **安全边界**：vLLM 是推理引擎，不替代网关、sandbox、租户控制和数据治理；生产架构必须补齐这些责任。
