---
chapter_id: "03-inside-vllm"
part: I
title: "vLLM 的请求生命周期"
status: brief
depends_on: ["02-workload-slo-and-metrics"]
evidence_status: missing
---

# 章节承诺

沿一次请求解释入口、预处理、调度、prefill、decode 和输出，使后续调优不再依赖参数猜测。

## 必须解释的机制

- Engine 与 worker 的职责边界。
- continuous batching 与调度循环。
- prefill/decode 的计算与访存差异。
- 请求抢占、完成与资源回收。

## 必须包含

一张版本化请求时序图；一次 trace 对照；关键源码定位方法。

Rust Frontend 作为可选北向 serving 层时，应在同一张图中明确：被替换的是 API frontend，不是 Python engine 或 GPU 执行路径。

## 读者产物

“指标异常 → 生命周期阶段”的初步定位表。

## 证据缺口

目标版本源码锚点；调度行为实验；术语随版本变化记录；Rust/Python frontend 的 engine boundary 对照。[SRC-vllm-rust-frontend-readme]
