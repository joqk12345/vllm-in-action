---
chapter_id: "07-model-loading-and-precision"
part: II
title: "模型加载、精度与量化"
status: brief
depends_on: ["05-environment-and-installation"]
evidence_status: missing
---

# 章节承诺

从正确性、显存、速度和可运维性四个维度选择 dtype、量化与模型加载策略。

## 必须包含

- 模型、tokenizer、revision 与 remote code 的固定。
- dtype 和量化格式的支持边界。
- 精度回归不能只看吞吐的案例。
- 启动耗时、缓存与权重分发。

## 读者产物

模型准入卡与精度/性能验收矩阵。

## 证据缺口

量化支持矩阵；质量评测基线；加载路径对照实验。
