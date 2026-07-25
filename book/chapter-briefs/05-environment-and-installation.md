---
chapter_id: "05-environment-and-installation"
part: II
title: "环境、安装与兼容性"
status: brief
depends_on: ["01-from-demo-to-production"]
evidence_status: missing
---

# 章节承诺

建立可复制、可诊断的安装基线，避免把环境问题误判为引擎问题。

## 必须包含

- GPU/驱动/CUDA 或 ROCm/PyTorch/vLLM 兼容链。
- wheel、容器、源码构建的选择条件。
- 模型缓存、网络、权限和离线环境。
- 最小 smoke test 与环境采集脚本。

## 读者产物

环境 manifest、安装决策树和首轮诊断清单。

## 证据缺口

官方支持矩阵；不同后端验证环境；容器供应链建议。
