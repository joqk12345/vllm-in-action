# 第 7 章 模型加载、精度与量化

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

精度选择同时改变权重容量、kernel、通信、KV cache 和输出质量。把“4 bit”视作单一产品是最常见误区。

## 7.1 权重如何进入 rank

vLLM 依据模型 config 选择注册实现，构造统一的 `torch.nn.Module`。TP/PP 与 quantization 在初始化阶段决定参数形状；loader 只把当前 rank 所需 shard 放入参数，避免每卡先加载完整模型。checkpoint 格式、文件数量、存储吞吐和 CPU RAM 会影响启动，而不只 GPU 显存。

固定模型 revision 并校验 architecture、rope、tokenizer、generation config 和自定义代码。允许 remote code 等于扩展信任边界，应在构建阶段审计并固化。

## 7.2 三类数值对象

- **权重 dtype/quant**：BF16/FP16/FP8/INT8/INT4 等；
- **activation/compute dtype**：kernel 内积累精度可能不同；
- **KV cache dtype**：影响长上下文容量和 attention 数值。

权重量化节省权重显存，不按同比例节省 KV；KV 量化可能增加 conversion/scaling 并影响质量。小 batch 下 decode 受权重带宽限制，权重量化常更有价值；大 batch/prefill 则可能被反量化开销或 GEMM compute 改变收益。

## 7.3 方法不是 bit 数

AWQ/GPTQ 等有各自 group size、zero point、校准和 kernel 支持；FP8 还涉及静态/动态 scale 与硬件代际。某格式能加载，不等于平台存在高性能 kernel。检查支持矩阵和运行日志，确认没有落到慢 fallback。

MoE 还要区分 shared experts、routed experts 与 router 精度。只量化 experts 的收益和风险不同于全模型；expert parallel 下量化布局还会影响 All-to-All 前后数据形态。

## 7.4 质量门禁

至少分三层：

1. token/logit 层：固定小样本与参考实现比较；
2. 任务层：运行与业务对应的 eval；
3. serving 层：长上下文、结构化输出、工具调用、并发和目标采样。

生成随机性会掩盖数值差异，先用 greedy 和固定 seed，再评估分布性任务。模型影响变更不能只报告 perplexity 或“肉眼看起来正常”。

## 7.5 显存账本

```text
device memory
= weight shards
+ KV cache
+ activations/workspace
+ graph pools/compile artifacts
+ communication buffers
+ allocator fragmentation
```

量化释放的显存可用于更多 KV，从而提高并发，但更高并发又改变 batch shape 和 kernel 区域。因此比较应有两组：固定并发看速度，固定 SLO 找最大 goodput。

## 7.6 选择流程

先以 BF16/FP16 建准确性和性能基线；若权重放不下或 decode 带宽受限，选择目标硬件原生支持的格式；验证 kernel 与质量；重新 profile KV 容量；再测真实分布。若吞吐提高但 p99 ITL 或模型质量越界，回退。

> **结论**：量化不是压缩文件，而是把模型映射到特定硬件、kernel 和质量预算的联合设计。
