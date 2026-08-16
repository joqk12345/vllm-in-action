# 第 11 章 热点注意力与延迟优化

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

TTFT 与 ITL 是两条不同路径。优化前先把延迟写成：

$$TTFT=T_{front}+T_{queue}+T_{prefill}+T_{sample}+T_{network}$$

$$ITL\approx T_{schedule}+T_{decode\ forward}+T_{sample}+T_{stream}$$

## 11.1 Prefill attention

prefill 对序列长度近似呈二次 attention 工作量（具体模型可能 sparse/local/linear），同时 GEMM 较大。FlashAttention 类 tiled kernel 避免显式落地完整 attention matrix，通过片上分块减少 HBM 流量。长上下文可再结合 chunk、PCP 或 sparse attention，但它们分别改变调度、通信和模型语义。

不要以 backend 名称推断性能。`vllm/v1/attention/selector.py` 会按平台、head size、dtype、模型特征和功能选择；日志与 profiler 才是实际路径证据。

## 11.2 Decode attention

decode 的 query 很短，却要读取历史 KV，常是 memory-bound。Paged attention 通过 block table gather 历史；GQA/MQA、KV quant 和 sliding window 能减少读量，但 layout、dequant 与稀疏索引也有开销。短上下文/低并发时，CPU launch 与 sampling 甚至高于 attention。

CUDA Graph 把固定执行序列 replay，减少 launch；shape 变化、动态控制流和未 capture 算子会导致 eager fallback 或多 graph 占用。比较 full/eager/graph 时同时记录 graph memory 和覆盖率。

## 11.3 混合与线性注意力

“线性注意力”常将完整 KV 历史压缩为 recurrent state，使 decode 对历史长度的读取近似固定；但 prefill 的 scan、state 更新、门控和数值稳定需要专门 kernel。混合模型周期性插入 full/local layers，以质量换状态容量和长上下文成本。

vLLM 当前包含 `linear_attn.py`、`gdn_attn.py`、Mamba backends、short-conv 与多种 MLA backend。支持一个 architecture 需要五层同时成立：模型实现、state/KV spec、调度与缓存、backend metadata、kernel；缺一层就可能只能 eager、不能 APC 或无法分布式。

MLA 通过低秩 latent 改变 KV 表示，prefill/decode 可能选择不同 backend；sparse MLA 还多 indexer/top-k 与 metadata 路径。所谓“注意力优化”因此要分别报告 prefill、decode、缓存字节和质量。

## 11.4 推测解码

小 drafter/EAGLE 等一次提出多个 draft token，target 并行验证并接受前缀。期望收益由 draft 成本、验证成本和接受长度决定：接受率高不等于快，drafter 太慢仍会退化；高并发下 target 本已高效批处理，收益往往小于低并发。

测试至少报告 acceptance length 分布、draft/verify 时间、额外显存、TTFT/ITL 和 goodput。任务、temperature 与语言都会改变接受率。任何方法先过无偏/质量契约。

## 11.5 延迟调优树

- queue 高：扩容/admission/调度；
- prefill 高：缩短输入、APC、chunk、prefill kernel/CP；
- decode forward 高：量化、batch、decode backend、spec decode；
- 周期性尖峰：GC、compile、collective、抢占、媒体或慢客户端；
- 单请求快、并发慢：KV/带宽/排队，而非首选换 kernel。

> **方法**：先消掉路径中最大的可行动项。把 attention kernel 加速 20%，若 queue 占 TTFT 的 80%，用户几乎无感。
