# 第 9 章 构建可信的 Benchmark

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

Benchmark 的职责不是制造一个最大数字，而是降低决策不确定性。每个实验先写假设：“瓶颈是 X，因此改变 Y 会改善 Z，并可能牺牲 Q”。

## 9.1 三层实验

- microbenchmark：单个 GEMM、attention、collective，解释机制；
- engine benchmark：离线/固定 batch，隔离 HTTP；
- serving benchmark：开放到达、真实协议、流式和取消，回答容量。

micro 快不保证 serving 快：新 kernel 可能增加 compile、workspace 或只覆盖少数 shape。serving 快也不能解释因果，所以三层应互证。

## 9.2 控制变量

固定 commit、模型 revision、dtype/quant、并行、GPU clocks/power、workload、seed 和环境。先 warm 权重、allocator、JIT/compile 与 graph；冷启动单独报告。每个点重复多轮，保留原始逐请求数据，而非只保留汇总表。

真实 trace 应匿名化并保存到达间隔、token 长度和 prefix 结构。若用合成数据，明确长度分布、到达过程和 token 生成方式。随机 token 不会产生真实 APC 命中。

## 9.3 找到饱和曲线

从低负载递增 offered rate，画 throughput、goodput、p99 TTFT/ITL 和 queue。开始时 throughput 线性增长；接近容量后 queue 与 tail 急升；再增加负载只增加失败/等待。把满足 SLO 的最后稳定点作为容量，不把过载区的毛吞吐峰值当容量。

固定并发测试适合对比引擎，但要说明 closed-loop；开放到达测试适合 admission planning。突发测试用 on/off 或回放真实 burst，验证恢复时间。

## 9.4 公平比较

比较后端时统一输出 token 数、EOS 策略、精度、prompt、并行和 SLO。若 A 使用量化、B 使用 BF16，应拆成系统方案比较与引擎比较。模型质量变化必须单独报告。

成本可表达为：

$$cost/1M\ tokens=\frac{instance\ price/hour}{goodput\ tokens/s\times3600}\times10^6$$

应使用合格 goodput，不使用不满足体验的峰值 throughput。还要计入副本冗余、空闲、CPU、网络和存储。

## 9.5 Profiler 的证据链

先从业务指标定位区间，再用 engine stats 找 queue/cache/preemption，最后用 Nsight/PyTorch profiler 看 kernel、collective、CPU launch。避免一开始采全量 trace：profiler 自身会扰动时序。

GPU timeline 中关注空洞、短 kernel 洪水、GEMM/attention 比例、collective overlap、memcpy 与 graph replay；CPU 关注 tokenizer、scheduler、序列化和 GC。跨 rank trace 必须时钟对齐。

## 9.6 结果模板

每份报告包含目的、环境、命令、workload hash、warm-up、重复次数、原始数据链接、图、观察、解释、反例和回退线。结论标注 observed，而机制若未 profile 则标注 hypothesis。

> **红队问题**：若交换 A/B 顺序、重启服务或换一份同分布 trace，结论是否仍成立？
