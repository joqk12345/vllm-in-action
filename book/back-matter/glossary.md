# 术语表

| 术语 | 英文/缩写 | 本书中的定义 |
|---|---|---|
| 首 token 延迟 | TTFT | 请求到达至首个内容 token 的时长 |
| token 间延迟 | ITL | 相邻流式输出 token 的间隔 |
| 端到端延迟 | E2E | 请求到达至生成结束 |
| 合格吞吐 | goodput | 同时满足既定 SLO 的请求或 token 速率 |
| 预填充 | prefill | 并行处理输入 token 并建立状态的阶段 |
| 解码 | decode | 自回归逐步生成 token 的阶段 |
| KV Cache | key-value cache | 保存历史注意力 K/V 的状态 |
| PagedAttention | 分页注意力 | 通过 block table 访问非连续 KV 页的注意力机制 |
| 自动前缀缓存 | APC | 以 block hash 复用跨请求已计算前缀 |
| 连续批处理 | continuous batching | 每个 engine step 可加入或移除请求的批处理 |
| 分块预填充 | chunked prefill | 将长 prompt 的 prefill 分到多个 step |
| 张量并行 | TP | 切分层内矩阵或 heads 的并行 |
| 流水线并行 | PP | 按层/stage 切分模型的并行 |
| 数据并行 | DP | 按请求扩展 rank/副本的并行 |
| 专家并行 | EP | 把 MoE experts 分布到 ranks |
| 上下文并行 | CP | 沿序列维度切分 attention/state 工作 |
| 专家负载均衡 | EPLB | 依据 expert 热度重排或冗余专家 |
| 多头潜在注意力 | MLA | 以低维 latent 表示 KV 的注意力家族 |
| 分组查询注意力 | GQA | 多个 query heads 共享较少 KV heads |
| 滑动窗口注意力 | SWA | 每个位置只访问局部历史窗口 |
| 混合注意力 | hybrid attention | 一个模型交错 full/local/linear/SSM 等层 |
| 推测解码 | speculative decoding | drafter 提议、target 并行验证 token 的方法 |
| CUDA Graph | CUDA Graph | capture/replay GPU launch DAG 的机制 |
| 服务级目标 | SLO | 可测的延迟、可用性或质量目标 |
| 开放到达 | open-loop | 请求按外部过程到达、不因完成速度自节流 |
| 固定并发 | closed-loop | 完成后补发请求以维持并发的负载模型 |
| 抢占 | preemption | KV/预算不足时暂停并可能重算请求 |
| 计算强度 | arithmetic intensity | FLOPs 与访问字节之比 |
| 前后处理解耦 | P/D disaggregation | 将 prefill 和 decode 放到不同 worker pool |
