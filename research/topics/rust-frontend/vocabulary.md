---
title: "Rust Frontend 最小系统词汇"
status: working
topic: rust-frontend
created: 2026-07-25
verified: 2026-07-25
applies_to: "vLLM Rust Frontend 的架构、源码、Issue 与生产分析"
source_ids:
  - SRC-vllm-rust-frontend-rfc-40846
  - SRC-vllm-rust-frontend-readme
  - SRC-vllm-rust-frontend-roadmap-44280
chapters: ["03", "06", "13", "14", "15"]
---

# Rust Frontend 最小系统词汇

Purpose: 建立研究 vLLM Rust Frontend 时统一、可组合的名词和动词集合。
Evidence grade: A
Assumptions: 这是分析词汇，不等于 Rust crate 或源码类型的完整清单。
Open questions: 进入目标 release 后，需要把概念映射到固定 commit 的具体类型和函数。
Handoff: 第 3、6、13、14、15 章。

## 9 个核心 nouns

| Noun | 中文 | 在本专题中的含义 | 最重要的 verbs |
|---|---|---|---|
| **Request** | 请求 | 外部 API 输入，包括消息、采样参数和多模态内容 | `accept`、`validate`、`normalize`、`reject` |
| **Frontend** | 前端 | Rust 实现的北向 serving 层，不负责 GPU 模型执行 | `serve`、`coordinate`、`fallback` |
| **Protocol** | 协议 | OpenAI API、HTTP/SSE、gRPC 和内部 Engine Protocol | `parse`、`serialize`、`frame`、`negotiate` |
| **Chat** | 对话语义 | Chat Template、reasoning、tool call 和 structured output | `render`、`interpret`、`structure` |
| **Token** | token | Frontend 与 Engine 之间最核心的数据形态 | `tokenize`、`detokenize`、`truncate` |
| **Stream** | 流 | token、文本 delta、结构化事件和 SSE chunk 的连续序列 | `transform`、`emit`、`collect`、`cancel` |
| **Engine Client** | 引擎客户端 | Rust Frontend 与 Python EngineCore 之间的通信边界 | `submit`、`multiplex`、`demultiplex`、`abort` |
| **Router** | 路由器 | 在多个 Engine 或 DP rank 之间选择请求目标 | `route`、`balance`、`drain`、`reroute` |
| **Capability** | 能力契约 | Rust/Python Frontend 的 API 和行为支持范围 | `support`、`verify`、`deprecate`、`fallback` |

## 12 个核心 verbs

| Verb | 中文 | 主语 | 宾语或结果 |
|---|---|---|---|
| `accept` | 接收 | Frontend | Request |
| `validate` | 校验 | Protocol/Frontend | 参数、schema、能力边界 |
| `render` | 渲染 | Chat layer | messages → prompt |
| `tokenize` | 编码 | Text layer | text → tokens |
| `route` | 路由 | Router | Request → Engine |
| `submit` | 提交 | Engine Client | EngineCoreRequest |
| `generate` | 生成 | EngineCore | token outputs |
| `detokenize` | 增量解码 | Text layer | tokens → text deltas |
| `parse` | 解析 | Chat layer | text → reasoning/tool events |
| `stream` | 流式返回 | Server | events → response chunks |
| `observe` | 观测 | Operator/平台 | 指标、日志、trace、状态 |
| `abort` | 中止 | Client/Frontend/Operator | in-flight Request |

## 完整处理语法

```text
Frontend accepts Request
         ↓
Protocol validates parameters
         ↓
Chat renders messages
         ↓
Text layer tokenizes text
         ↓
Router routes request
         ↓
Engine Client submits tokens
         ↓
EngineCore generates token outputs
         ↓
Text layer detokenizes tokens
         ↓
Chat layer parses structured events
         ↓
Server streams Response
```

压缩为中文：

```text
接收 → 校验 → 渲染 → 编码
     → 路由 → 提交 → 生成
     → 解码 → 解析 → 流式返回
```

生产控制旁路：

```text
observe → detect → drain/abort → fallback
观测      检测       排空/中止       回退
```

## 三组必须保持的区别

### Frontend 与 Engine

- **Frontend** 负责 HTTP/API、Chat Template、tokenization、解析和流式返回。
- **Engine** 负责调度、KV Cache、模型执行和 GPU 计算。

因此，Rust Frontend 优化的是 CPU serving path，不是重新实现 vLLM 推理引擎。

### 三种 stream

```text
Engine token stream
    → decoded text stream
    → reasoning/tool event stream
    → SSE response stream
```

工具调用标记可能跨越多个 token 或 chunk，所以 detokenization、structured parsing 和 SSE framing 是三个不同阶段。

### 实现与生产就绪

一个 Capability 可能已经 `implemented`，但还没有完成：

```text
tested → released → observed → rollback-ready
测试       进入版本      可观测       可回退
```

研究某项能力时，应分别问：

1. Frontend 接受和拒绝什么？
2. 它如何转换和流式输出？
3. 失败行为是什么？
4. 如何观测、取消和排空？
5. 如何回退到已知可用路径？

## 源码映射方向

后续阅读固定版本源码时，将概念映射到以下 workspace 层：

| 概念 | 初始源码入口 |
|---|---|
| Frontend、Protocol、Request、Response | `vllm-server` |
| Chat、structured events、parser | `vllm-chat` |
| Token、tokenize、detokenize | `vllm-text` |
| token-in/token-out facade | `vllm-llm` |
| Engine Client、内部协议 | `vllm-engine-core-client` |
| CLI 和进程入口 | `vllm-cmd` / `vllm-rs` |

> 这些映射必须在进入正文前固定到具体 release tag 或 commit；浮动 `main` 只用于研究导航。
