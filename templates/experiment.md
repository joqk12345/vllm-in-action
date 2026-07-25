---
experiment_id: EXP-YYYYMMDD-short-name
status: planned
owner: ""
date: YYYY-MM-DD
vllm_version: ""
vllm_commit: ""
evidence_grade: A
chapters: []
---

# 实验问题

要验证或证伪的单一问题：

## 假设

## 环境

- GPU 型号、数量、显存、互联：
- CPU、内存、NUMA：
- OS、驱动、CUDA/ROCm：
- Python、PyTorch、vLLM：
- 容器镜像/锁文件：

## 模型与配置

- 模型与 revision：
- tokenizer：
- dtype / quantization：
- tensor / pipeline / data parallel：
- 关键引擎参数：

## 工作负载

- 输入/输出 token 分布：
- 并发与到达过程：
- warm-up：
- 随机种子：

## 执行命令

```bash
# 完整可复制命令；敏感信息改用变量名
```

## 指标与接受标准

| 指标 | 基线 | 候选 | 接受标准 |
|---|---:|---:|---:|
| TTFT p50/p95/p99 | | | |
| ITL p50/p95/p99 | | | |
| output tok/s | | | |
| 峰值显存 | | | |
| 错误率 | | | |

## 结果

原始数据路径：

## 结论、边界与回退

- 观察：
- 解释：
- 不适用场景：
- 回退方案：

## 复核

- [ ] 命令可重放
- [ ] 原始结果未被覆盖
- [ ] 结论没有超出实验范围
- [ ] 负结果也已记录
