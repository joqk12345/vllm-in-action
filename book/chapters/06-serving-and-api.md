# 第 6 章 服务入口与 API 契约

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

vLLM 同时提供离线 `LLM` 与在线 OpenAI-compatible server。兼容意味着常见请求/响应形状可迁移，不意味着每个供应商扩展、错误码和采样细节完全相同。

## 6.1 边界分层

API 层负责 HTTP、鉴权、限流、renderer/chat template、tokenization、媒体获取和 SSE；引擎层接收 token 化请求并维护生成状态。生产系统应在 API 前再放 ingress，但避免在多层代理重复排队，导致客户端已超时而 GPU 仍计算。

建立契约测试覆盖 `/health`、模型列表、chat/completions、streaming、usage、logprobs、tool call、structured output、embedding/pooling（若使用）和取消传播。升级时比较语义，不只比较 200 状态码。

## 6.2 Chat template 是模型程序的一部分

相同 messages 经不同 template 会产生不同 token、角色标记和输出。固定 tokenizer revision、template 与 renderer；把渲染后 token 数纳入审计。工具定义常形成巨大共享前缀，既是 APC 机会，也是 TTFT 和 KV 风险。

结构化输出通过 grammar/constraint 限制候选 token。grammar 编译可能异步发生，复杂 schema 会影响排队；测普通文本的结果不能外推。schema 应设大小和复杂度上限。

## 6.3 Streaming 与背压

SSE 的首事件不一定包含首个内容 token，客户端计时要定义清楚。慢客户端若不被隔离，会累积响应 buffer。断连应尽快 abort 请求并释放 KV；代理 timeout 应大于合理的 server timeout，且保留取消传播。

服务至少有三类 timeout：排队、首 token、总生成。把它们合为一个总 timeout，会让已经不可能满足 SLO 的请求继续占 GPU。

## 6.4 输入安全

远程图片/音频 URL 会把 serving 变成网络客户端：需要域名 allowlist、大小/类型/重定向限制、下载超时和私网地址防护。限制 prompt token、max tokens、`n`、logprobs、schema 和并发；否则一个合法请求也可成为资源耗尽攻击。

不要把 API key 直接写启动参数或日志。对 prompt/output 的日志默认脱敏，trace 中只保留长度和匿名 request ID；多租户还需隔离 LoRA、prefix cache 语义和配额。

## 6.5 过载控制

推荐顺序：入口 admission 检查 → 有界队列 → 业务 class 配额 → 引擎调度。负载超过 goodput 区域时应返回可重试错误或降级 max tokens，而不是让 queue 无限增长。重试必须有指数退避和 jitter，否则故障恢复会产生重试风暴。

readiness 与 liveness 不同：进程活着不代表模型已加载或 engine 能推进；readiness 失败时停止新流量，liveness 只在不可恢复停滞时重启。滚动升级应先 warm 新副本，再切流。

## 6.6 最小服务测试

```bash
curl -N http://host:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"<model>","messages":[{"role":"user","content":"hi"}],"stream":true}'
```

这只能验证烟雾路径。真正门禁还包括并发断连、超长拒绝、坏 schema、慢消费者、代理 idle timeout、模型 alias 与 usage 对账。

> **原则**：协议兼容是起点；tokenization、错误、超时、取消和资源上限才是生产契约。
