# 第 15 章 升级、回滚与系统化故障诊断

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

vLLM 演进快，升级不是换镜像，而是重新验证模型—平台—kernel—配置—API 的契约。

## 15.1 变更分诊

阅读目标 release notes，并对照当前 commit diff 搜索：config 默认值、deprecated flags、model implementation、attention backend、scheduler/KV、quant、distributed、API schema 和 metrics。固定模型列表建立影响矩阵，不能用一个小模型代表所有架构。

当前书稿固定到 `fe1c317...`（版本描述 `v0.27.2rc0-129-gfe1c317157`）；读者使用其他版本时，应以对应 tag 的源码和文档重验所有参数。

## 15.2 升级门禁

1. 构建与供应链扫描；
2. 模型加载及功能契约；
3. greedy/任务 eval；
4. baseline performance 与显存；
5. soak、取消、过载、故障；
6. shadow/canary；
7. 分批发布。

性能门禁用区间和统计噪声，不因一次 2% 波动阻断，也不忽略 p99 30% 退化。比较 resolved config 和实际 backend，防止默认选择改变。

## 15.3 回滚必须可执行

保留旧镜像、模型 revision、配置、chat template 和编译 artifact；数据库/路由协议若变化要向后兼容。先定义触发线：错误、SLO burn、质量、OOM/preemption、rank failure。回滚也需 warm 容量，不能等事故后重新下载模型。

缓存/connector 跨版本不应假定兼容；升级切流时可丢缓存并 warm，而不是冒险复用内部状态。

## 15.4 故障树

**启动失败**：配置/architecture → 权重与磁盘/RAM → distributed init → profile OOM → compile/graph。

**TTFT 高**：客户端/代理 → tokenize/media → queue → prefix miss → prefill kernel/collective → sampling/stream。

**ITL 抖动**：batch shape → preemption/recompute → graph fallback/recompile → collective straggler → GC/CPU → backpressure。

**吞吐低**：offered load 不足 → 输出长度不同 → eager/fallback → batch/token budget → memory/compute → communication imbalance。

**多卡 hang**：先保留所有 rank stack/log，再检查某 rank OOM/异常、collective 顺序、NIC、timeout 和拓扑。只看 rank 0 日志通常会错过首个故障。

## 15.5 二分而非乱调

从已知正确 baseline 开始，每次去掉一层：关 spec、APC/connector、compile/graph、quant、新 backend、distributed；缩到单模型/短 prompt/单并发。缩小后在源码链中确认 consumer 与 tests。不要同时变环境与配置。

保存事故时的版本、完整命令、环境变量、模型 config、请求长度、metrics 快照、各 rank 日志与最小复现。敏感正文先脱敏。

## 15.6 常见误诊

- CUDA OOM 不一定是 KV：可能 graph、workspace、临时 weight；
- GPU utilization 低不一定 kernel 慢：可能 queue/CPU/collective；
- 404/400 不一定引擎：可能 model alias/template/API contract；
- 输出变化不一定量化：tokenizer/template/generation defaults 也会变；
- cache hit 下降不一定 bug：路由或 prompt 前缀可能变化。

> **原则**：先确定“从哪个版本、哪个层开始不同”，再解释原因。可回滚性比在事故中找到完美参数更重要。
