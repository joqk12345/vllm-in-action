---
chapter_id: "14-reliability-and-security"
part: IV
title: "可靠性、隔离与安全"
status: brief
depends_on: ["06-serving-and-api", "13-observability-and-capacity"]
evidence_status: missing
---

# 章节承诺

识别推理服务的故障域、滥用面与多租户风险，设计有界降级。

## 必须包含

- 超长请求、突发流量、OOM、worker/node 故障。
- 限流、配额、超时、取消、输入输出边界。
- remote code、模型制品、日志数据和密钥风险。
- 多租户隔离与降级策略。
- 实验性 frontend 缺少 TLS、鉴权、CORS 或 reverse-proxy 支持时的责任边界与补偿控制。

## 读者产物

威胁模型、故障演练表与生产安全清单。

## 证据缺口

安全公告；故障注入实验；平台层与引擎层责任边界；Rust Frontend production-readiness roadmap 与目标 release 实测。[SRC-vllm-rust-frontend-roadmap-44280]
