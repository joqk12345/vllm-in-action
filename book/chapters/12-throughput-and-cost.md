# 第 12 章 算子优化、编译与单位成本

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

吞吐优化的本质是减少每个合格 token 的字节、计算、通信和控制开销，并让它们重叠。

## 12.1 Roofline 心智模型

算术强度 $I=FLOPs/bytes$。若 $I$ 低，性能上限接近内存带宽；若高，接近计算峰值。decode 小 batch 反复读权重，通常偏带宽；prefill/大 batch GEMM 更偏计算。增大 batch 会复用权重并提高强度，却增加排队和 KV 占用。

因此 throughput 与 latency 并非永远对立：饱和前 batching 可同时提高设备效率和请求完成速度；过拐点后 queue 支配尾延迟。

## 12.2 融合算子

RMSNorm+residual、RoPE、activation+gate、quant GEMM、MoE routing/expert、sampling 等融合可减少中间张量和 launch。vLLM 的 custom op 体系允许按平台选择 native、Triton、CUTLASS、FlashInfer、AITER 等实现。

算子验收包含：shape/dtype/stride 边界、数值误差、确定性、graph capture、compile、空 batch/尾块、不同 GPU 架构和 fallback。microbenchmark 应含 warm-up、分位数和带宽/TFLOPS，而不是一次计时。

## 12.3 `torch.compile` 与 vLLM IR

编译器把可支持区域切成 graph，做 fusion/inductor 优化；不可支持的 custom op 可作为 opaque 边界。dynamic shape 会触发 guard/recompile，过多变体增加启动与缓存。vLLM 的编译设计和 optimization levels 会持续演进，实际运行应记录 resolved compilation config。

调试顺序：确认是否编译 → 查看 graph break/guards → 统计 compile time 与 cache hit → 对比 eager correctness → 看 timeline 是否减少 launch/中间读写。仅看到“compile enabled”不足以证明热路径被优化。

## 12.4 CUDA Graph

Graph capture 固化 launch DAG 和部分内存地址，replay 降低 CPU overhead。它最适合重复 decode shapes；全图覆盖更快但更受动态性约束，piecewise graph 可在图间保留动态逻辑。graph pool 会占显存，从而压缩 KV 容量。最终比较必须包含容量变化。

## 12.5 MoE kernel 与通信

MoE 每 token 只激活 top-k experts，理论 FLOPs 低于 dense，但 routing、permute、grouped GEMM、All-to-All 和负载倾斜决定实际性能。模块化 fused MoE kernel 需要把量化、activation、routing 信息作为 feature 组合；不是每个组合都有同等成熟实现。

优化优先级：先平衡 expert token，选择匹配 fabric 的 All-to-All；再调整 grouped GEMM tile 与量化。若最慢 rank 等待不均，单 rank kernel 更快不会改善全局 step。

## 12.6 重叠与推测

dual batch overlap/microbatching 可让一批的通信与另一批计算重叠；PP batch queue 隐藏 stage bubble；异步调度隐藏 CPU。重叠不会消灭工作，只缩短关键路径，并增加 buffer、同步和在途 batch。用 timeline 验证真正 overlap，而非只看配置。

## 12.7 从 token/s 到成本

用满足 SLO 的 output goodput 计算 GPU-hour/token，再加入副本冗余、空闲、失败重算和能耗。量化使单卡可装模型，可能比 10% kernel 加速更改成本结构；APC 在高复用 agent workload 中减少 prefill，也可能比峰值 GEMM 更重要。

> **优化闭环**：业务 profile → roofline/trace 假设 → micro 证实 → engine 集成 → serving goodput → 质量与成本门禁。
