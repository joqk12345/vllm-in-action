---
chapter_id: "06-serving-and-api"
part: II
title: "服务入口与 API 契约"
status: draft
depends_on: ["05-environment-and-installation"]
evidence_status: partial
---

# 章节承诺

正确暴露服务接口，并理解兼容 API、流式输出、采样与结构化输出的契约边界。

## 必须包含

- 启动命令到健康检查的最小服务。
- 请求参数、tokenizer/chat template 与返回语义。
- streaming 断连、超时、取消和幂等性。
- 网关、鉴权、限流应放在哪一层。
- Python 与 Rust frontend 的 endpoint、参数和错误语义兼容矩阵。

## 读者产物

API 上线契约与兼容性测试集。

## 证据缺口

目标版本 API 文档；边缘行为测试；客户端兼容矩阵；Rust frontend 的 feature parity 与稳定性复核。[SRC-vllm-rust-frontend-rfc-40846] [SRC-vllm-rust-frontend-readme] [SRC-vllm-rust-frontend-roadmap-44280]
