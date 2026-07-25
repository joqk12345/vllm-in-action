---
chapter_id: "04-memory-and-kv-cache"
part: I
title: "显存、KV Cache 与容量边界"
status: brief
depends_on: ["03-inside-vllm"]
evidence_status: missing
---

# 章节承诺

让读者能估算权重、运行时和 KV cache 的显存占用，并解释 OOM 与容量拐点。

## 必须解释的机制

- 权重、activation、CUDA graph/运行时与 KV cache 的预算。
- block 化管理、碎片与 prefix reuse。
- 上下文长度、并发、层数、KV heads、dtype 的关系。

## 必须包含

手算模型与实际测量对照；容量阶梯实验；估算失准案例。

## 读者产物

显存预算表和上线前容量检查。

## 证据缺口

目标架构公式核对；不同模型家族实测；offload/量化边界。
