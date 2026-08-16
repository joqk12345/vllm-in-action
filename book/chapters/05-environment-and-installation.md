# 第 5 章 环境、安装与可复现基线

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

安装成功只是依赖解析成功。可复现环境还要固定硬件 ISA、driver、runtime、PyTorch、vLLM commit、kernel 库与模型 revision。

## 5.1 从兼容矩阵开始

保存以下 inventory：GPU/CPU 型号与 NUMA、互联（PCIe/NVLink/IB/RoCE）、driver 与 CUDA/ROCm、容器 digest、共享内存、ulimit、文件系统和网络接口。多卡运行先验证 peer access 与 collective，再启动模型。容器能看到设备不代表 NCCL 能选对 NIC。

安装方式按可变性排序：官方固定 tag 镜像适合生产；wheel 适合标准平台；源码构建适合开发新模型或算子。不要把浮动 `latest` 与模型 `main` 组合成基线。

```bash
vllm serve <model-id> \
  --revision <model-commit> \
  --dtype <dtype>
```

命令是示意，参数必须以所用版本 `vllm serve --help` 和模型支持矩阵为准。

## 5.2 启动的四个阶段

1. 配置解析与模型架构识别；
2. rank 创建、权重下载/加载和切分；
3. profile 可用显存并建立 KV cache；
4. compile 与 CUDA Graph capture，完成 health/readiness。

阶段定位非常重要。加载卡住检查存储、CPU RAM 和 rank；profile OOM 检查临时 activation；graph capture OOM 检查 graph 模式与形状；ready 后首请求慢则区分 lazy compile 与冷 cache。

## 5.3 最小正确性门禁

在性能测试前验证：固定 prompt 的 greedy 输出与可信后端一致到允许误差；长上下文、EOS/stop、stream/non-stream、并发取消、结构化输出和目标模型特性可用。量化或新 kernel 必须先过准确性，再进性能比较。

保留启动日志和 resolved config。默认值会随平台、模型与 release 改变，“我没传参数”不是完整配置。

## 5.4 多节点前置检查

各节点镜像、模型文件和时钟一致；rank 能解析彼此地址；端口、防火墙和 MTU 正确；容器拥有足够 `/dev/shm` 和 memlock；NCCL/Gloo/NIXL 所需设备可见。用小 tensor collective 测 latency/bandwidth，避免用 500GB 模型做网络探针。

NUMA 错绑会使 tokenizer、权重 staging 或 host-to-device 路径退化。单机多卡也要记录 GPU—NIC—CPU affinity。

## 5.5 基线配置原则

先用 eager 或默认稳定路径得到正确基线，再逐步加入 compile/graph、量化、prefix caching、spec decode 和分布式特性。每步只改变一个因素，并记录：启动时间、显存、单请求 latency、饱和 goodput 与输出一致性。

若优化只在 warm cache 生效，明确 warm-up 次数；若编译产生 shape-specific artifact，保存 shape 范围。把编译缓存当部署产物管理，而非神秘的本地状态。

## 5.6 版本清单模板

```text
vLLM commit: fe1c317...
model revision: <immutable sha>
image digest: sha256:...
accelerator/topology: ...
driver/runtime/torch: ...
non-default flags/env: ...
workload sha256: ...
```

> **上线门禁**：无法在一台干净机器依据清单重建的 benchmark，不进入容量规划。
